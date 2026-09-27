import {
  expandFlightQuery,
  normalizeCallsign,
  parseFlightHashParams,
} from './flightIdentity.js';
import {
  resolveFlightRecord,
  resolveConfiguredAlias,
  routeHintForQuery,
} from './flightResolver.js';

const WAITING_POLL_MS = 2_000;

/**
 * Per-flight deep link: enable the flights layer, resolve marketing→operating
 * callsigns, wait for the aircraft to appear, then select + follow it.
 */
export class FlightDeepLinkController {
  constructor({
    dataManager,
    flightsLayer,
    shareLinkManager,
    onStatus,
    onFollowChange,
    fetchLookup = defaultFlightLookup,
    setTimer = setTimeout,
    clearTimer = clearTimeout,
  } = {}) {
    this.dataManager = dataManager;
    this.flightsLayer = flightsLayer;
    this.shareLinkManager = shareLinkManager;
    this.onStatus = onStatus;
    this.onFollowChange = onFollowChange;
    this.fetchLookup = fetchLookup;
    this.setTimer = setTimer;
    this.clearTimer = clearTimer;
    this._query = null;
    this._display = '';
    this._found = null;
    this._followEnabled = true;
    this._timer = null;
    this._generation = 0;
    this._destroyed = false;
    this._waiting = false;
  }

  /** Begin from a parsed share-link flight ref. */
  async start(flightRef) {
    if (this._destroyed) return { status: 'destroyed' };
    this.stop();
    const query = flightRef?.query
      || (flightRef?.flight || flightRef?.icao24
        ? expandFlightQuery(flightRef.flight || flightRef.icao24)
        : null);
    if (!query || (!query.callsigns.length && !query.icao24)) {
      return { status: 'skipped', reason: 'no-flight' };
    }
    this._query = query;
    this._display = query.display || flightRef.flight || query.icao24;
    this._found = null;
    this._followEnabled = true;
    this._waiting = true;
    const generation = ++this._generation;
    await this._enableFlightsLayer();
    this._emitStatus('waiting');
    return this._poll(generation);
  }

  stop() {
    this._generation += 1;
    if (this._timer != null) this.clearTimer(this._timer);
    this._timer = null;
    this._waiting = false;
  }

  destroy() {
    this._destroyed = true;
    this.stop();
    this._query = null;
    this._found = null;
  }

  /** Current hash payload when a flight is selected or still awaited. */
  sharePayload() {
    if (this._found?.callsign || this._found?.icao24) {
      return {
        flight: normalizeCallsign(this._found.callsign) || this._display || null,
        icao24: this._found.icao24 || null,
      };
    }
    if (this._query) {
      return {
        flight: this._display || this._query.display || null,
        icao24: this._query.icao24 || null,
      };
    }
    return null;
  }

  get followEnabled() {
    return this._followEnabled;
  }

  setFollowEnabled(enabled) {
    this._followEnabled = !!enabled;
    if (this._followEnabled && this._found?.icao24) {
      this.flightsLayer?.setFollowEnabled?.(true);
      this.flightsLayer?.trackById?.(this._found.icao24, { origin: 'user' });
    } else if (!this._followEnabled) {
      this.flightsLayer?.releaseFollowCamera?.();
    }
    this.onFollowChange?.({
      enabled: this._followEnabled,
      found: this._found,
      display: this._display,
    });
  }

  /** Keep the controller in sync when the user breaks follow by dragging. */
  syncFollowEnabled(enabled) {
    this._followEnabled = !!enabled;
    this.onFollowChange?.({
      enabled: this._followEnabled,
      found: this._found,
      display: this._display,
    });
  }

  /** Live feed just refreshed — try to pick the aircraft up. */
  onFlightsRefresh(records) {
    if (!this._query || this._destroyed) return null;
    return this._tryResolve(records);
  }

  _emitStatus(status, extra = {}) {
    const label = this._display || 'flight';
    this.onStatus?.({
      status,
      display: label,
      waiting: status === 'waiting',
      message: status === 'waiting' ? `Waiting for ${label}…` : extra.message || '',
      found: this._found,
      ...extra,
    });
  }

  async _enableFlightsLayer() {
    if (!this.dataManager?.setEnabled) return;
    try {
      await this.dataManager.setEnabled('flights', true, { origin: 'share-restore' });
    } catch (error) {
      console.warn('[flight-deeplink] failed to enable flights', error);
    }
  }

  async _poll(generation) {
    if (this._destroyed || generation !== this._generation) return { status: 'cancelled' };
    const found = this._tryResolve(this._liveRecords())
      || await this._lookupGlobally();
    if (this._destroyed || generation !== this._generation) return { status: 'cancelled' };
    if (found) return { status: 'found', found };
    this._timer = this.setTimer(() => {
      this._timer = null;
      return this._poll(generation);
    }, WAITING_POLL_MS);
    this._timer?.unref?.();
    return { status: 'waiting', display: this._display };
  }

  _liveRecords() {
    const layer = this.flightsLayer;
    if (!layer?.getAnalystRecords) return [];
    try {
      return layer.getAnalystRecords(4000) || [];
    } catch {
      return [];
    }
  }

  _tryResolve(records) {
    if (!this._query) return null;
    const hint = routeHintForQuery(this._query);
    const resolved = resolveFlightRecord(records, this._query, hint);
    if (!resolved?.record) return null;
    return this._latch(resolved.record);
  }

  async _lookupGlobally() {
    if (!this.fetchLookup || !this._query) return null;
    const alias = resolveConfiguredAlias(this._display);
    const tokens = [this._query.icao24, ...alias.candidates].filter(Boolean);
    for (const token of tokens) {
      let payload = null;
      try {
        payload = await this.fetchLookup(token);
      } catch (error) {
        console.warn('[flight-deeplink] lookup failed', token, error);
        continue;
      }
      if (!payload) continue;
      const records = Array.isArray(payload.records) ? payload.records : [payload];
      const found = this._tryResolve(records);
      if (found) {
        if (payload.ingest && this.flightsLayer?.ingestLookupRecords) {
          this.flightsLayer.ingestLookupRecords(records);
        }
        return found;
      }
    }
    return null;
  }

  _latch(record) {
    const icao24 = String(record.icao24 || '').trim().toLowerCase();
    if (!icao24) return null;
    this._found = {
      icao24,
      callsign: normalizeCallsign(record.callsign) || this._display,
    };
    this._waiting = false;
    if (this._timer != null) this.clearTimer(this._timer);
    this._timer = null;
    const tracked = this.flightsLayer?.trackById?.(icao24, { origin: 'share-restore' });
    if (this._followEnabled && this.flightsLayer?.setFollowEnabled) {
      this.flightsLayer.setFollowEnabled(true);
    }
    this._emitStatus('found', { tracked: !!tracked });
    this.onFollowChange?.({
      enabled: this._followEnabled,
      found: this._found,
      display: this._display,
    });
    this.shareLinkManager?.onLayerStateChange?.();
    return this._found;
  }
}

export function flightRefFromShareState(state) {
  if (state?.flightRef?.query) return state.flightRef;
  return parseFlightHashParams(new URLSearchParams());
}

async function defaultFlightLookup(token) {
  const params = new URLSearchParams();
  if (/^[0-9a-f]{6}$/i.test(String(token))) params.set('icao24', String(token).toLowerCase());
  else params.set('callsign', String(token));
  const response = await fetch(`/api/flight-lookup?${params}`, {
    headers: { Accept: 'application/json' },
  });
  if (!response.ok) return null;
  const body = await response.json();
  const records = Array.isArray(body?.records) ? body.records : [];
  return { records, ingest: true };
}
