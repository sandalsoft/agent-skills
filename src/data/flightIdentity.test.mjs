import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  IATA_TO_ICAO,
  callsignMatchesQuery,
  expandFlightQuery,
  normalizeCallsign,
  normalizeFlightToken,
  normalizeIcao24,
  parseFlightHashParams,
  splitAirlineAndNumber,
} from './flightIdentity.js';

test('normalizes case, spaces, hyphens, and leading zeros', () => {
  assert.equal(normalizeFlightToken(' ua 4051 '), 'UA4051');
  assert.equal(normalizeFlightToken('UAL-4051'), 'UAL4051');
  assert.deepEqual(splitAirlineAndNumber('UA04051'), {
    airline: 'UA',
    number: '4051',
    form: 'iata',
  });
  assert.deepEqual(splitAirlineAndNumber('ual04051'), {
    airline: 'UAL',
    number: '4051',
    form: 'icao',
  });
  assert.equal(normalizeCallsign('  skw 04051 '), 'SKW4051');
});

test('IATA airline prefixes expand to ICAO callsigns', () => {
  assert.equal(IATA_TO_ICAO.UA, 'UAL');
  assert.equal(IATA_TO_ICAO.AA, 'AAL');
  assert.equal(IATA_TO_ICAO.DL, 'DAL');
  assert.equal(IATA_TO_ICAO.WN, 'SWA');
  assert.equal(IATA_TO_ICAO.AS, 'ASA');
  assert.equal(IATA_TO_ICAO.B6, 'JBU');
  assert.equal(IATA_TO_ICAO.NK, 'NKS');
  assert.equal(IATA_TO_ICAO.F9, 'FFT');
  const ua = expandFlightQuery('UA4051');
  assert.equal(ua.display, 'UA4051');
  assert.ok(ua.callsigns.includes('UAL4051'));
  assert.ok(ua.callsigns.includes('ASH4051'));
  assert.ok(ua.callsigns.includes('SKW4051'));
});

test('icao24 pads and lowercases hex, rejects junk', () => {
  assert.equal(normalizeIcao24('ABC123'), 'abc123');
  assert.equal(normalizeIcao24('  a1b '), '000a1b');
  assert.equal(normalizeIcao24('nothex'), null);
  assert.equal(expandFlightQuery('a1b2c3').icao24, 'a1b2c3');
});

test('hash parser reads flight= and icao24= without requiring camera keys', () => {
  const both = parseFlightHashParams(new URLSearchParams('flight=UA4051&icao24=abc123&lat=10'));
  assert.equal(both.flight, 'UA4051');
  assert.equal(both.icao24, 'abc123');
  assert.ok(both.query.callsigns.includes('ASH4051'));
  const hexOnly = parseFlightHashParams(new URLSearchParams('icao24=aa11bb'));
  assert.equal(hexOnly.icao24, 'aa11bb');
  const empty = parseFlightHashParams(new URLSearchParams('lat=1&lon=2'));
  assert.equal(empty.query, null);
});

test('live callsign matching is tolerant of padding and spaces', () => {
  const query = expandFlightQuery('UA4051');
  assert.equal(callsignMatchesQuery('ASH4051', query), true);
  assert.equal(callsignMatchesQuery(' ASH04051 ', query), true);
  assert.equal(callsignMatchesQuery('UAL4051', query), true);
  assert.equal(callsignMatchesQuery('DAL4051', query), false);
});
