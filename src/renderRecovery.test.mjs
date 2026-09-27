import { test } from 'node:test';
import assert from 'node:assert/strict';
import { describeError, serializeThrown, toError } from './standalone/errors.js';
import {
  guardedCallback,
  installSceneRenderRecovery,
  isRenderableCartesian,
  runGuardedFrame,
  runGuardedRecord,
} from './renderRecovery.js';
import { resolveViewerMsaaSamples } from './webglCapabilities.js';

test('root cause: a plain object throw becomes an Error with JSON details', () => {
  // Cesium's default panel does error.toString() + error.stack. A thrown {}
  // therefore renders as "[object Object]" / "undefined" and the scene dies.
  const thrown = { provider: 'google-3d', x: 12, y: 34, level: 9 };
  assert.equal(String(thrown), '[object Object]');
  assert.equal(thrown.stack, undefined);
  const error = toError(thrown, 'flights');
  assert.ok(error instanceof Error);
  assert.match(error.message, /flights/);
  assert.match(error.message, /"level":9/);
  assert.notEqual(error.message, '[object Object]');
  assert.ok(error.stack);
  assert.match(serializeThrown(thrown), /google-3d/);
  assert.equal(describeError(thrown).includes('google-3d'), true);
});

test('non-finite and earth-center Cartesians are not renderable', () => {
  assert.equal(isRenderableCartesian({ x: 1, y: 2, z: 3 }), true);
  assert.equal(isRenderableCartesian({ x: NaN, y: 0, z: 0 }), false);
  assert.equal(isRenderableCartesian({ x: 0, y: 0, z: 0 }), false);
  assert.equal(isRenderableCartesian(null), false);
});

test('guarded frame/record wrappers swallow non-Error throws and keep going', () => {
  const warnings = [];
  const original = console.warn;
  console.warn = (...args) => warnings.push(args.join(' '));
  try {
    assert.equal(runGuardedFrame('flights', () => { throw { tile: 7 }; }), undefined);
    assert.equal(runGuardedRecord('flights', 'abc123', () => { throw { hex: 'abc123' }; }), undefined);
    assert.equal(runGuardedRecord('flights', 'ok', () => 42), 42);
  } finally {
    console.warn = original;
  }
  assert.ok(warnings.some((line) => line.includes('flights') && line.includes('tile')));
  assert.ok(warnings.some((line) => line.includes('abc123')));
});

test('renderError recovery re-enables the default render loop', () => {
  const listeners = new Set();
  const viewer = {
    useDefaultRenderLoop: false,
    container: { querySelectorAll: () => [] },
    scene: {
      renderError: {
        addEventListener(fn) {
          listeners.add(fn);
          return () => listeners.delete(fn);
        },
      },
      requestRender() { viewer.requested = true; },
    },
  };
  installSceneRenderRecovery(viewer);
  assert.equal(listeners.size, 1);
  [...listeners][0](viewer.scene, { reason: 'tile-content', lon: -117.8682 });
  assert.equal(viewer.useDefaultRenderLoop, true);
  assert.equal(viewer.requested, true);
});

test('guarded CallbackProperty evaluators swallow non-Error throws', () => {
  const cb = guardedCallback('flights:pos', () => { throw { x: NaN, y: 0, z: 0 }; }, null);
  assert.equal(cb(), null);
  const safe = guardedCallback('flights:pos', () => ({ x: 1, y: 2, z: 3 }));
  assert.deepEqual(safe(), { x: 1, y: 2, z: 3 });
  const nan = guardedCallback('flights:pos', () => ({ x: NaN, y: 0, z: 0 }), null);
  assert.equal(nan(), null);
});

test('WebGL1 never requests 4x MSAA', () => {
  assert.equal(resolveViewerMsaaSamples({ webgl2: false, maxSamples: 0, requested: 4 }), 1);
  assert.equal(resolveViewerMsaaSamples({ webgl2: true, maxSamples: 8, requested: 4 }), 4);
  assert.equal(resolveViewerMsaaSamples({ webgl2: true, maxSamples: 2, requested: 4 }), 2);
});
