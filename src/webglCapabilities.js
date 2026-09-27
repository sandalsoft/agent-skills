/**
 * Resolve a Cesium `msaaSamples` value that will not request more samples
 * than the context can give. WebGL1 reports `MAX_SAMPLES = 0`; asking for 4
 * there is how a framebuffer setup throws a plain object into the render
 * loop (Cesium's panel then shows `[object Object]` / `undefined`).
 *
 * @param {{webgl2?: boolean, maxSamples?: number, requested?: number}} caps
 * @returns {number} Samples to pass to `Cesium.Viewer` / `scene.msaaSamples`.
 */
export function resolveViewerMsaaSamples({
  webgl2 = false,
  maxSamples = 0,
  requested = 4,
} = {}) {
  const want = Number.isFinite(requested) && requested > 0 ? Math.floor(requested) : 4;
  if (!webgl2) return 1;
  const max = Number.isFinite(maxSamples) ? Math.floor(maxSamples) : 0;
  if (max <= 1) return 1;
  return Math.max(1, Math.min(want, max));
}

/**
 * Probe the current document for WebGL2 + MSAA support. Safe in Node tests:
 * missing `document` / canvas yields the conservative WebGL1 path.
 * @returns {{webgl2: boolean, maxSamples: number}}
 */
export function detectWebglCapabilities(createCanvas = defaultCanvas) {
  try {
    const canvas = createCanvas?.();
    const gl = canvas?.getContext?.('webgl2');
    if (!gl) return { webgl2: false, maxSamples: 0 };
    const maxSamples = Number(gl.getParameter(gl.MAX_SAMPLES));
    return {
      webgl2: true,
      maxSamples: Number.isFinite(maxSamples) ? maxSamples : 0,
    };
  } catch {
    return { webgl2: false, maxSamples: 0 };
  }
}

function defaultCanvas() {
  if (typeof document === 'undefined') return null;
  return document.createElement('canvas');
}
