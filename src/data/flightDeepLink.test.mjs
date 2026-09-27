import { test } from 'node:test';
import assert from 'node:assert/strict';
import { expandFlightQuery } from './flightIdentity.js';
import { FlightDeepLinkController } from './flightDeepLink.js';

function fakeLayer(store) {
  return {
    getAnalystRecords() { return store.records; },
    trackById(id) {
      store.tracked = id;
      return true;
    },
    setFollowEnabled(on) { store.follow = on; },
    ingestLookupRecords(records) { store.ingested = records; },
  };
}

function fakeManager(store) {
  return {
    async setEnabled(id, on) {
      store.enabled = { id, on };
      return true;
    },
  };
}

test('waits, then auto-picks the aircraft when it appears', async () => {
  const store = { records: [], tracked: null, follow: false, enabled: null };
  const statuses = [];
  const timers = [];
  const controller = new FlightDeepLinkController({
    dataManager: fakeManager(store),
    flightsLayer: fakeLayer(store),
    fetchLookup: async () => null,
    onStatus: (status) => statuses.push(status.status),
    setTimer: (fn) => {
      timers.push(fn);
      return 1;
    },
    clearTimer: () => {},
  });

  const first = await controller.start({ query: expandFlightQuery('UA4051') });
  assert.equal(first.status, 'waiting');
  assert.deepEqual(store.enabled, { id: 'flights', on: true });
  assert.equal(store.tracked, null);
  assert.ok(statuses.includes('waiting'));
  assert.equal(controller.sharePayload().flight, 'UA4051');

  store.records = [{ icao24: 'a00ash', callsign: 'ASH4051', lat: 30, lon: -95, routeOrigin: 'IAH', routeDestination: 'JAX' }];
  const later = await timers[0]();
  assert.equal(later.status, 'found');
  assert.equal(store.tracked, 'a00ash');
  assert.equal(controller.sharePayload().flight, 'ASH4051');
  assert.ok(statuses.includes('found'));
  controller.destroy();
});

test('global lookup latches an aircraft the viewport snapshot missed', async () => {
  const store = { records: [], tracked: null, ingested: null };
  const controller = new FlightDeepLinkController({
    dataManager: fakeManager(store),
    flightsLayer: fakeLayer(store),
    fetchLookup: async (token) => {
      if (token !== 'ASH4051' && token !== 'UAL4051') return null;
      return {
        ingest: true,
        records: [{ icao24: 'aabbcc', callsign: 'ASH4051', lat: 29.9, lon: -95.3 }],
      };
    },
    setTimer: () => 1,
    clearTimer: () => {},
  });
  const result = await controller.start({ query: expandFlightQuery('UA4051') });
  assert.equal(result.status, 'found');
  assert.equal(store.tracked, 'aabbcc');
  assert.equal(store.ingested[0].callsign, 'ASH4051');
  controller.destroy();
});
