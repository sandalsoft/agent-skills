import {
  UNITED_EXPRESS_PREFIXES,
  callsignMatchesQuery,
  expandFlightQuery,
  normalizeCallsign,
  normalizeIcao24,
} from './flightIdentity.js';

/**
 * Score a live aircraft row against a deep-link query. Higher wins.
 * Route/position near a known origin/destination breaks ties when several
 * regionals share the same number.
 *
 * @param {object} record live aircraft ({icao24, callsign, lat, lon, routeOrigin, routeDestination})
 * @param {ReturnType<typeof expandFlightQuery>} query
 * @param {{origin?: string, destination?: string, originLat?: number, originLon?: number, destLat?: number, destLon?: number}|null} routeHint
 * @returns {number}
 */
export function scoreFlightCandidate(record, query, routeHint = null) {
  if (!record || !query) return 0;
  const hex = normalizeIcao24(record.icao24);
  if (query.icao24 && hex && hex === query.icao24) return 1000;
  const live = normalizeCallsign(record.callsign);
  if (!live) return 0;
  if (callsignMatchesQuery(live, query)) {
    let score = 400;
    score += routeAffinity(record, routeHint);
    return score;
  }
  if (query.number && live.endsWith(query.number)) {
    const prefix = live.slice(0, live.length - query.number.length);
    if (UNITED_EXPRESS_PREFIXES.includes(prefix)) {
      return 200 + routeAffinity(record, routeHint);
    }
  }
  return 0;
}

function routeAffinity(record, routeHint) {
  if (!routeHint) return 0;
  let score = 0;
  const origin = String(record.routeOrigin || record.origin || '').toUpperCase();
  const dest = String(record.routeDestination || record.destination || '').toUpperCase();
  if (routeHint.origin && origin === String(routeHint.origin).toUpperCase()) score += 40;
  if (routeHint.destination && dest === String(routeHint.destination).toUpperCase()) score += 40;
  if (Number.isFinite(record.lat) && Number.isFinite(record.lon)) {
    if (near(record, routeHint.originLat, routeHint.originLon)) score += 25;
    if (near(record, routeHint.destLat, routeHint.destLon)) score += 25;
  }
  return score;
}

function near(record, lat, lon) {
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return false;
  const dlat = record.lat - lat;
  const dlon = record.lon - lon;
  return (dlat * dlat) + (dlon * dlon) < 4; // ~2° — corridor, not a pin
}

/**
 * Pick the best live row for a query. Returns null when nothing scores.
 * @param {Array<object>} records
 * @param {string|ReturnType<typeof expandFlightQuery>} queryOrRaw
 * @param {object} [routeHint]
 */
export function resolveFlightRecord(records, queryOrRaw, routeHint = null) {
  const query = typeof queryOrRaw === 'string' ? expandFlightQuery(queryOrRaw) : queryOrRaw;
  if (!query || !Array.isArray(records) || records.length === 0) return null;
  let best = null;
  let bestScore = 0;
  for (const record of records) {
    const score = scoreFlightCandidate(record, query, routeHint);
    if (score > bestScore) {
      best = record;
      bestScore = score;
    }
  }
  return bestScore > 0 ? { record: best, score: bestScore, query } : null;
}

/**
 * Static marketing→operating resolution used before live data arrives.
 * UA4051 resolves to Mesa ASH4051 (2026-09-27 IAH→JAX). UA700 is mainline
 * UAL700 (2026-09-27 SNA→IAH).
 * @param {string} raw
 */
export function resolveConfiguredAlias(raw) {
  const query = expandFlightQuery(raw);
  const primary = query.callsigns[0] || query.display;
  return {
    query,
    operatingCallsign: primary,
    candidates: query.callsigns,
    icao24: query.icao24,
  };
}

/** IAH / JAX / SNA used to bias regional-number collisions. */
export const KNOWN_FLIGHT_ROUTES = Object.freeze({
  UA4051: Object.freeze({
    origin: 'IAH',
    destination: 'JAX',
    originLat: 29.9844,
    originLon: -95.3414,
    destLat: 30.4941,
    destLon: -81.6879,
    operator: 'Mesa Airlines',
    operatingCallsign: 'ASH4051',
    source: 'FlightStats 2026-09-27 (operated by Mesa on behalf of United)',
    confidence: 'high',
  }),
  UAL4051: Object.freeze({
    origin: 'IAH',
    destination: 'JAX',
    originLat: 29.9844,
    originLon: -95.3414,
    destLat: 30.4941,
    destLon: -81.6879,
    operator: 'Mesa Airlines',
    operatingCallsign: 'ASH4051',
    source: 'FlightStats 2026-09-27 (operated by Mesa on behalf of United)',
    confidence: 'high',
  }),
  UA700: Object.freeze({
    origin: 'SNA',
    destination: 'IAH',
    originLat: 33.6757,
    originLon: -117.8682,
    destLat: 29.9844,
    destLon: -95.3414,
    operator: 'United Airlines',
    operatingCallsign: 'UAL700',
    source: 'FlightStats 2026-09-27 (mainline 737 MAX 8 SNA→IAH)',
    confidence: 'high',
  }),
  UAL700: Object.freeze({
    origin: 'SNA',
    destination: 'IAH',
    originLat: 33.6757,
    originLon: -117.8682,
    destLat: 29.9844,
    destLon: -95.3414,
    operator: 'United Airlines',
    operatingCallsign: 'UAL700',
    source: 'FlightStats 2026-09-27 (mainline 737 MAX 8 SNA→IAH)',
    confidence: 'high',
  }),
});

export function routeHintForQuery(query) {
  if (!query) return null;
  for (const key of [query.display, ...(query.callsigns || [])]) {
    if (KNOWN_FLIGHT_ROUTES[key]) return KNOWN_FLIGHT_ROUTES[key];
  }
  return null;
}
