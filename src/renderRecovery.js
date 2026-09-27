import { serializeThrown, toError } from './standalone/errors.js';

/**
 * True when a Cartesian can be handed to Cesium (billboard, ENU frame,
 * CallbackProperty) without producing NaN GPU state. Zero is the ellipsoid
 * center — `eastNorthUpToFixedFrame` throws there.
 * @param {*} position
 * @returns {boolean}
 */
export function isRenderableCartesian(position) {
  if (!position || typeof position !== 'object') return false;
  const { x, y, z } = position;
  if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(z)) return false;
  return (x * x) + (y * y) + (z * z) > 1;
}

/**
 * Run a per-frame owner. One bad frame is logged and skipped; it must not
 * escape into Cesium's render loop (that stops the scene).
 * @param {string} ownerId
 * @param {Function} fn
 * @returns {*}
 */
export function runGuardedFrame(ownerId, fn) {
  try {
    return fn();
  } catch (value) {
    const error = toError(value, ownerId);
    console.warn(`[render] ${ownerId} skipped a frame:`, error.message, error.details || serializeThrown(value));
    return undefined;
  }
}

/**
 * Run work for one record/contact. A single bad aircraft/tile/row cannot
 * kill the rest of the fleet pass.
 * @param {string} ownerId
 * @param {string|number} recordId
 * @param {Function} fn
 * @returns {*}
 */
export function runGuardedRecord(ownerId, recordId, fn) {
  try {
    return fn();
  } catch (value) {
    const error = toError(value, `${ownerId}:${recordId}`);
    console.warn(
      `[render] ${ownerId} skipped record ${recordId}:`,
      error.message,
      error.details || serializeThrown(value),
    );
    return undefined;
  }
}

/**
 * Wrap a Cesium CallbackProperty evaluator. A throw inside the render
 * loop (NaN Cartesian, bad ENU frame, rejected tile promise) must not
 * escape as a plain object.
 * @param {string} ownerId
 * @param {Function} fn
 * @param {*} [fallback]
 */
export function guardedCallback(ownerId, fn, fallback = undefined) {
  return (...args) => {
    try {
      const result = fn(...args);
      if (result && typeof result === 'object' && 'x' in result && !isRenderableCartesian(result)) {
        return typeof fallback === 'function' ? fallback() : fallback;
      }
      return result;
    } catch (value) {
      const error = toError(value, ownerId);
      console.warn(
        `[render] ${ownerId} callback skipped:`,
        error.message,
        error.details || serializeThrown(value),
      );
      return typeof fallback === 'function' ? fallback() : fallback;
    }
  };
}

/**
 * Install a `scene.renderError` handler that logs the real thrown value and
 * attempts to restart Cesium's default render loop instead of leaving the
 * black error panel up.
 * @param {object} viewer Cesium Viewer
 * @returns {Function} disposer
 */
export function installSceneRenderRecovery(viewer) {
  const scene = viewer?.scene;
  if (!scene?.renderError?.addEventListener) {
    throw new TypeError('installSceneRenderRecovery requires a Cesium scene with renderError');
  }
  let recovering = false;
  const remove = scene.renderError.addEventListener((failedScene, thrown) => {
    const error = toError(thrown, 'scene.renderError');
    console.error('[render] scene.renderError', error.message, error.details || serializeThrown(thrown), error);
    if (recovering) return;
    recovering = true;
    try {
      hideCesiumErrorPanel(viewer);
      if (viewer && viewer.useDefaultRenderLoop === false) {
        viewer.useDefaultRenderLoop = true;
      }
      failedScene?.requestRender?.();
    } catch (recoveryError) {
      console.warn('[render] recovery failed', toError(recoveryError).message);
    } finally {
      queueMicrotask(() => { recovering = false; });
    }
  });
  return typeof remove === 'function' ? remove : () => {};
}

/**
 * Isolate 3D-tile load/content failures so a bad photoreal tile logs details
 * instead of throwing a non-Error into `scene.render`.
 * @param {object} tileset
 * @returns {Function} disposer
 */
export function isolateTilesetErrors(tileset) {
  if (!tileset?.tileFailed?.addEventListener) return () => {};
  const remove = tileset.tileFailed.addEventListener((tileError) => {
    console.warn('[render] tileset tileFailed', serializeThrown(tileError) || tileError);
  });
  return typeof remove === 'function' ? remove : () => {};
}

function hideCesiumErrorPanel(viewer) {
  const root = viewer?.cesiumWidget?.container || viewer?.container;
  if (!root?.querySelectorAll) return;
  for (const panel of root.querySelectorAll('.cesium-widget-errorPanel')) {
    panel.remove();
  }
}
