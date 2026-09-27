/**
 * Flight share-link identity: parse, normalize, and expand `flight=` /
 * `icao24=` hash values so UA4051, UAL4051, and a hex address all mean the
 * same lookup.
 */

/** IATA airline code → ICAO telephony prefix. Common scheduled carriers. */
export const IATA_TO_ICAO = Object.freeze({
  UA: 'UAL',
  AA: 'AAL',
  DL: 'DAL',
  WN: 'SWA',
  AS: 'ASA',
  B6: 'JBU',
  NK: 'NKS',
  F9: 'FFT',
  HA: 'HAL',
  G4: 'AAY',
  SY: 'SCX',
  MX: 'MXY',
  XP: 'CXP',
  AC: 'ACA',
  WS: 'WJA',
  PD: 'POE',
  TS: 'TSC',
  BA: 'BAW',
  LH: 'DLH',
  AF: 'AFR',
  KL: 'KLM',
  EK: 'UAE',
  QR: 'QTR',
  EY: 'ETD',
  SQ: 'SIA',
  CX: 'CPA',
  QF: 'QFA',
  NZ: 'ANZ',
  TK: 'THY',
  IB: 'IBE',
  LX: 'SWR',
  OS: 'AUA',
  SK: 'SAS',
  AY: 'FIN',
  TP: 'TAP',
  AZ: 'ITY',
  VS: 'VIR',
  EI: 'EIN',
  AM: 'AMX',
  CM: 'CMP',
  AV: 'AVA',
  LA: 'LAN',
  NH: 'ANA',
  JL: 'JAL',
  KE: 'KAL',
  OZ: 'AAR',
  CI: 'CAL',
  BR: 'EVA',
  // United Express regionals (IATA of the operator, when the user types that)
  YV: 'ASH',
  OO: 'SKW',
  YX: 'RPA',
  C5: 'UCA',
  G7: 'GJS',
  ZW: 'AWI',
  MQ: 'ENY',
});

/**
 * United Express (and similar) operating prefixes tried when a marketing
 * IATA/ICAO callsign is not on the wire. Same flight number, different
 * three-letter prefix.
 */
export const UNITED_EXPRESS_PREFIXES = Object.freeze([
  'SKW',
  'RPA',
  'ASH',
  'ENY',
  'UCA',
  'GJS',
  'AWI',
]);

/**
 * Marketing → operating callsign aliases researched for a specific date.
 * Keys and values are normalized ICAO-style callsigns (no spaces, no
 * leading zeros in the numeric part).
 *
 * UA4051 IAH→JAX on 2026-09-27: FlightStats, "Operated by Mesa Airlines
 * on behalf of United Airlines", E175, scheduled 14:35 CDT. Mesa's
 * broadcast prefix is ASH. Tail/icao24 was not yet public (not departed).
 *
 * UA700 SNA→IAH on 2026-09-27: FlightStats, mainline United 737 MAX 8,
 * scheduled 08:10 PDT. Broadcast callsign is UAL700.
 */
export const FLIGHT_ALIASES = Object.freeze({
  UA4051: Object.freeze(['ASH4051', 'UAL4051']),
  UAL4051: Object.freeze(['ASH4051', 'UAL4051']),
  UA700: Object.freeze(['UAL700']),
  UAL700: Object.freeze(['UAL700']),
});

const IATA_AIRLINE = /^(?:[A-Z]{2}|[A-Z][0-9]|[0-9][A-Z])$/;
const ICAO_AIRLINE = /^[A-Z]{3}$/;
const ICAO24 = /^[0-9A-F]{1,6}$/;

/** Strip spaces / hyphens and uppercase. */
export function normalizeFlightToken(raw) {
  return String(raw ?? '').replace(/[\s._-]+/g, '').toUpperCase();
}

/**
 * Split a flight id into airline + number, dropping leading zeros on the
 * number (`UA04051` → UA / 4051). Returns null when the token is not a
 * flight number (hex addresses go through {@link normalizeIcao24}).
 * @param {string} raw
 * @returns {{airline: string, number: string, form: 'iata'|'icao'}|null}
 */
export function splitAirlineAndNumber(raw) {
  const token = normalizeFlightToken(raw);
  if (!token) return null;
  const icao = token.match(/^([A-Z]{3})0*([1-9]\d*)$/);
  if (icao && ICAO_AIRLINE.test(icao[1])) {
    return { airline: icao[1], number: icao[2], form: 'icao' };
  }
  const iata = token.match(/^([A-Z][A-Z0-9]|[0-9][A-Z])0*([1-9]\d*)$/);
  if (iata && IATA_AIRLINE.test(iata[1])) {
    return { airline: iata[1], number: iata[2], form: 'iata' };
  }
  return null;
}

/** Pad / lowercase a 1–6 hex icao24. Rejects non-hex. */
export function normalizeIcao24(raw) {
  const token = String(raw ?? '').trim().toLowerCase().replace(/^0x/, '');
  if (!token || !/^[0-9a-f]{1,6}$/.test(token)) return null;
  return token.padStart(6, '0');
}

function callsignFor(airline, number) {
  return `${airline}${number}`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

/**
 * Expand one user-facing flight token into every callsign we should try,
 * plus an icao24 when the token is a hex address.
 * @param {string} raw
 * @returns {{
 *   display: string,
 *   icao24: string|null,
 *   callsigns: string[],
 *   number: string|null,
 *   iata: string|null,
 *   icaoAirline: string|null,
 * }}
 */
export function expandFlightQuery(raw) {
  const token = normalizeFlightToken(raw);
  const hex = normalizeIcao24(token);
  if (hex && !splitAirlineAndNumber(token)) {
    return {
      display: hex,
      icao24: hex,
      callsigns: [],
      number: null,
      iata: null,
      icaoAirline: null,
    };
  }
  const parts = splitAirlineAndNumber(token);
  if (!parts) {
    return {
      display: token || String(raw || '').trim(),
      icao24: hex,
      callsigns: token ? [token] : [],
      number: null,
      iata: null,
      icaoAirline: null,
    };
  }
  const iata = parts.form === 'iata' ? parts.airline : null;
  const icaoAirline = parts.form === 'icao'
    ? parts.airline
    : (IATA_TO_ICAO[parts.airline] || null);
  const marketingIata = iata ? callsignFor(iata, parts.number) : null;
  const marketingIcao = icaoAirline ? callsignFor(icaoAirline, parts.number) : null;
  const aliasKey = marketingIata || marketingIcao;
  const aliases = FLIGHT_ALIASES[aliasKey] || FLIGHT_ALIASES[marketingIcao] || [];
  const regionals = icaoAirline === 'UAL' || iata === 'UA'
    ? UNITED_EXPRESS_PREFIXES.map((prefix) => callsignFor(prefix, parts.number))
    : [];
  return {
    display: marketingIata || marketingIcao || token,
    icao24: hex,
    callsigns: unique([
      marketingIcao,
      marketingIata,
      ...aliases,
      ...regionals,
      callsignFor(parts.airline, parts.number),
    ]),
    number: parts.number,
    iata,
    icaoAirline,
  };
}

/**
 * Read `flight=` and `icao24=` from share-link params without disturbing
 * existing camera/style keys.
 * @param {URLSearchParams} params
 * @returns {{flight: string|null, icao24: string|null, query: ReturnType<typeof expandFlightQuery>|null}}
 */
export function parseFlightHashParams(params) {
  if (!params || typeof params.get !== 'function') {
    return { flight: null, icao24: null, query: null };
  }
  const flightRaw = params.get('flight');
  const icaoRaw = params.get('icao24');
  const flight = flightRaw && String(flightRaw).trim() ? String(flightRaw).trim() : null;
  const icao24 = icaoRaw ? normalizeIcao24(icaoRaw) : null;
  if (!flight && !icao24) return { flight: null, icao24: null, query: null };
  const query = expandFlightQuery(flight || icao24);
  if (icao24) query.icao24 = icao24;
  return {
    flight: flight ? (query.display || normalizeFlightToken(flight)) : null,
    icao24,
    query,
  };
}

/** Canonical callsign for matching live ADS-B rows. */
export function normalizeCallsign(raw) {
  const parts = splitAirlineAndNumber(raw);
  if (parts) return callsignFor(parts.airline, parts.number);
  const token = normalizeFlightToken(raw);
  return token || '';
}

/** True when a live callsign equals one of the expanded candidates. */
export function callsignMatchesQuery(liveCallsign, query) {
  if (!query?.callsigns?.length) return false;
  const live = normalizeCallsign(liveCallsign);
  if (!live) return false;
  return query.callsigns.some((candidate) => normalizeCallsign(candidate) === live);
}
