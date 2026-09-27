import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ShareLinkManager } from './sharelink.js';

function makeManager(hash = '') {
  globalThis.window = { location: { hash, href: `http://localhost/${hash}` } };
  globalThis.history = {
    replaceState(_state, _title, nextHash) {
      window.location.hash = nextHash;
    },
  };
  const viewer = {
    camera: {
      changed: { addEventListener() {} },
      positionCartographic: { latitude: 0, longitude: 0, height: 1000 },
      heading: 0,
      pitch: -Math.PI / 2,
      roll: 0,
    },
  };
  return new ShareLinkManager(viewer);
}

test('flight-only hash is a valid share without camera coordinates', () => {
  const state = makeManager('#flight=UA4051').parseInitialHash();
  assert.ok(state);
  assert.equal(state.lat, null);
  assert.equal(state.lon, null);
  assert.equal(state.flightRef.flight, 'UA4051');
  assert.ok(state.flightRef.query.callsigns.includes('ASH4051'));
});

test('icao24-only hash is a valid share', () => {
  const state = makeManager('#icao24=abc123').parseInitialHash();
  assert.ok(state);
  assert.equal(state.flightRef.icao24, 'abc123');
});

test('existing camera hash still parses and has no flight ref', () => {
  const state = makeManager(
    '#lat=33.6757&lon=-117.8682&alt=25000&heading=0&pitch=-45',
  ).parseInitialHash();
  assert.ok(state);
  assert.equal(state.lat, 33.6757);
  assert.equal(state.lon, -117.8682);
  assert.equal(state.flightRef.query, null);
});

test('camera + flight params coexist', () => {
  const state = makeManager(
    '#lat=33.6757&lon=-117.8682&alt=25000&flight=UA700',
  ).parseInitialHash();
  assert.equal(state.lat, 33.6757);
  assert.equal(state.flightRef.flight, 'UA700');
  assert.ok(state.flightRef.query.callsigns.includes('UAL700'));
});

test('encoded share includes selected flight without dropping camera keys', () => {
  const manager = makeManager('#lat=10&lon=20');
  manager.parseInitialHash();
  manager.completeInitialRestore();
  manager.setFlightShareProvider(() => ({ flight: 'ASH4051', icao24: 'a00ash' }));
  const params = manager._buildHashParams();
  assert.equal(params.get('lat'), '0.0000');
  assert.equal(params.get('flight'), 'ASH4051');
  assert.equal(params.get('icao24'), 'a00ash');
  assert.ok(params.get('style'));
});

test('applyState skips camera flyTo when only a flight is present', async () => {
  const manager = makeManager('#flight=UAL700');
  const state = manager.parseInitialHash();
  let flew = false;
  manager.viewer.camera.flyTo = () => { flew = true; };
  const result = await manager.applyState(state);
  assert.equal(result.camera, 'skipped');
  assert.equal(flew, false);
});
