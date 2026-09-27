import { test } from 'node:test';
import assert from 'node:assert/strict';
import { expandFlightQuery } from './flightIdentity.js';
import {
  KNOWN_FLIGHT_ROUTES,
  resolveConfiguredAlias,
  resolveFlightRecord,
  routeHintForQuery,
  scoreFlightCandidate,
} from './flightResolver.js';

test('UA4051 alias table resolves Mesa ASH4051', () => {
  const resolved = resolveConfiguredAlias('UA4051');
  assert.ok(resolved.candidates.includes('ASH4051'));
  assert.equal(KNOWN_FLIGHT_ROUTES.UA4051.operatingCallsign, 'ASH4051');
  assert.equal(KNOWN_FLIGHT_ROUTES.UA4051.operator, 'Mesa Airlines');
  assert.equal(KNOWN_FLIGHT_ROUTES.UA4051.origin, 'IAH');
  assert.equal(KNOWN_FLIGHT_ROUTES.UA4051.destination, 'JAX');
});

test('UA700 alias table resolves mainline UAL700', () => {
  const resolved = resolveConfiguredAlias('UA700');
  assert.ok(resolved.candidates.includes('UAL700'));
  assert.equal(KNOWN_FLIGHT_ROUTES.UA700.operatingCallsign, 'UAL700');
  assert.equal(KNOWN_FLIGHT_ROUTES.UA700.origin, 'SNA');
  assert.equal(KNOWN_FLIGHT_ROUTES.UA700.destination, 'IAH');
});

test('resolver prefers the operating regional on the researched route', () => {
  const query = expandFlightQuery('UA4051');
  const hint = routeHintForQuery(query);
  const records = [
    { icao24: 'a11111', callsign: 'SKW4051', lat: 41.97, lon: -87.9, routeOrigin: 'ORD', routeDestination: 'MSP' },
    { icao24: 'a22222', callsign: 'ASH4051', lat: 30.1, lon: -94.8, routeOrigin: 'IAH', routeDestination: 'JAX' },
  ];
  const winner = resolveFlightRecord(records, query, hint);
  assert.equal(winner.record.icao24, 'a22222');
  assert.ok(
    scoreFlightCandidate(records[1], query, hint)
    > scoreFlightCandidate(records[0], query, hint),
  );
});

test('resolver matches icao24 exactly even when callsign differs', () => {
  const query = expandFlightQuery('abc123');
  const winner = resolveFlightRecord([
    { icao24: 'abc123', callsign: 'N123AB', lat: 33.6, lon: -117.8 },
  ], query);
  assert.equal(winner.record.callsign, 'N123AB');
});

test('resolver returns null while the aircraft is absent', () => {
  assert.equal(resolveFlightRecord([], 'UA4051'), null);
  assert.equal(
    resolveFlightRecord([{ icao24: 'ffff00', callsign: 'SWA1' }], 'UA4051'),
    null,
  );
});
