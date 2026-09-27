import * as Cesium from 'cesium';
import { installSceneRenderRecovery } from '../renderRecovery.js';
import { detectWebglCapabilities, resolveViewerMsaaSamples } from '../webglCapabilities.js';
import { toError } from '../standalone/errors.js';

/** Create the standard globe viewer in caller-owned, visible containers. */
export function createApplicationViewer({ container, creditContainer }) {
  if (!container || !creditContainer)
    throw new TypeError('Viewer and credit containers are required');
  const caps = detectWebglCapabilities();
  const msaaSamples = resolveViewerMsaaSamples({
    ...caps,
    requested: 4,
  });
  const viewer = new Cesium.Viewer(container, {
    timeline: false,
    animation: false,
    baseLayerPicker: false,
    geocoder: false,
    homeButton: false,
    sceneModePicker: false,
    navigationHelpButton: false,
    fullscreenButton: false,
    vrButton: false,
    selectionIndicator: false,
    infoBox: false,
    baseLayer: false,
    creditContainer,
    msaaSamples,
    contextOptions: { webgl: { preserveDrawingBuffer: true } },
  });
  try {
    viewer.targetFrameRate = 60;
    viewer.scene.globe.show = false;
    viewer.scene.skyAtmosphere.show = true;
    viewer.scene.skyAtmosphere.atmosphereLightIntensity = 18;
    viewer.scene.skyAtmosphere.saturationShift = -0.12;
    viewer.scene.skyAtmosphere.brightnessShift = -0.08;
    viewer._removeRenderRecovery = installSceneRenderRecovery(viewer);
    return viewer;
  } catch (error) {
    viewer.destroy();
    throw toError(error, 'createApplicationViewer');
  }
}
