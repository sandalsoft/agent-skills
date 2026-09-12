import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  createBrowserViteConfig,
  isHostedViteServer,
} from '../../build/vite.js';
import standaloneConfig, * as compatibility from '../../vite.config.js';
import * as providers from '../../server/providers/local.js';

test('explicit build inputs preserve browser-only defines, plugin order and loopback protections', () => {
  const plugin = { name: 'fixture-provider' };
  const config = createBrowserViteConfig({
    plugins: [plugin],
    googleApiKey: 'browser-fixture',
    cesiumToken: 'ion-fixture',
  });
  assert.equal(config.plugins[1], plugin);
  assert.equal(config.server.host, 'localhost');
  assert.equal(config.server.port, 4173);
  assert.deepEqual(config.server.allowedHosts, [
    'localhost',
    '127.0.0.1',
    '.local',
  ]);
  assert.ok(config.server.fs.deny.includes('**/ENVIRONMENT'));
  assert.ok(config.server.fs.deny.includes('.env.*'));
  assert.equal(config.server.headers['X-Frame-Options'], 'DENY');
  assert.equal(
    config.server.headers['Content-Security-Policy'],
    "frame-ancestors 'none'",
  );
  assert.deepEqual(config.define, {
    'import.meta.env.GOOGLE_MAPS_API_KEY': '"browser-fixture"',
    'import.meta.env.CESIUM_ION_TOKEN': '"ion-fixture"',
  });
  const publicBind = createBrowserViteConfig({ host: '0.0.0.0', port: '4800' });
  assert.equal(publicBind.server.allowedHosts, true);
  assert.equal(publicBind.server.hmr, false);
  assert.equal(publicBind.server.strictPort, true);
  assert.equal(publicBind.plugins.at(-1).name, 'gev-hosted-no-hmr');
  assert.equal(
    createBrowserViteConfig({ host: '::', port: '4800' }).server.port,
    4800,
  );
  const renderHosted = createBrowserViteConfig({
    hosted: true,
    host: 'localhost',
    port: '10000',
  });
  assert.equal(renderHosted.server.hmr, false);
  assert.equal(renderHosted.server.strictPort, true);
  assert.equal(renderHosted.server.allowedHosts, true);
  assert.equal(renderHosted.server.host, 'localhost');
  assert.equal(renderHosted.server.port, 10000);
  assert.equal(renderHosted.plugins.at(-1).name, 'gev-hosted-no-hmr');
  assert.equal(
    config.plugins.some((plugin) => plugin.name === 'gev-hosted-no-hmr'),
    false,
  );
  assert.equal(config.server.hmr, undefined);
  assert.equal(config.server.strictPort, undefined);
});

test('build helper does not discover environment values or construct local providers', () => {
  const beforeKey = process.env.GOOGLE_MAPS_API_KEY;
  const beforeRender = process.env.RENDER;
  const beforeHost = process.env.HOST;
  process.env.GOOGLE_MAPS_API_KEY = 'environment-fixture';
  process.env.RENDER = 'true';
  process.env.HOST = '0.0.0.0';
  try {
    const config = createBrowserViteConfig();
    assert.equal(
      config.define['import.meta.env.GOOGLE_MAPS_API_KEY'],
      undefined,
    );
    assert.equal(config.plugins.length, 1);
    assert.equal(config.server.host, 'localhost');
    assert.equal(config.server.hmr, undefined);
    assert.equal(isHostedViteServer({}), false);
  } finally {
    if (beforeKey === undefined) delete process.env.GOOGLE_MAPS_API_KEY;
    else process.env.GOOGLE_MAPS_API_KEY = beforeKey;
    if (beforeRender === undefined) delete process.env.RENDER;
    else process.env.RENDER = beforeRender;
    if (beforeHost === undefined) delete process.env.HOST;
    else process.env.HOST = beforeHost;
  }
});

test('root config retains existing named exports and standalone provider order', () => {
  for (const [name, value] of Object.entries(providers))
    assert.equal(compatibility[name], value, name);
  const config = standaloneConfig({ mode: 'test' });
  assert.deepEqual(
    config.plugins.slice(1).map((plugin) => plugin.name),
    providers.localProviderPlugins().map((plugin) => plugin.name),
  );
  assert.equal(config.plugins[1].name, 'gev-basic-auth');
  assert.equal(config.plugins.at(-1).name, 'gev-key-setup');
});

test('standalone config disables HMR when Render marks the process hosted', () => {
  const beforeRender = process.env.RENDER;
  const beforeHost = process.env.HOST;
  const beforePort = process.env.PORT;
  process.env.RENDER = 'true';
  process.env.HOST = '0.0.0.0';
  process.env.PORT = '10000';
  try {
    const config = standaloneConfig({ mode: 'test' });
    assert.equal(config.server.hmr, false);
    assert.equal(config.server.strictPort, true);
    assert.equal(config.server.host, '0.0.0.0');
    assert.equal(config.server.port, 10000);
    assert.equal(config.server.allowedHosts, true);
    assert.equal(config.plugins[1].name, 'gev-basic-auth');
    assert.equal(config.plugins.at(-2).name, 'gev-key-setup');
    assert.equal(config.plugins.at(-1).name, 'gev-hosted-no-hmr');
  } finally {
    if (beforeRender === undefined) delete process.env.RENDER;
    else process.env.RENDER = beforeRender;
    if (beforeHost === undefined) delete process.env.HOST;
    else process.env.HOST = beforeHost;
    if (beforePort === undefined) delete process.env.PORT;
    else process.env.PORT = beforePort;
  }
});

test('hosted HMR stub serves a client with no websocket', () => {
  const plugin = createBrowserViteConfig({ hosted: true }).plugins.find(
    (entry) => entry.name === 'gev-hosted-no-hmr',
  );
  assert.ok(plugin);
  const layers = [];
  plugin.configureServer({
    middlewares: {
      use(handler) {
        layers.push(handler);
      },
    },
  });
  const response = {
    headers: {},
    setHeader(name, value) {
      this.headers[name] = value;
    },
    end(body) {
      this.body = body;
    },
  };
  let nextCalled = false;
  layers[0]({ url: '/@vite/client?t=1' }, response, () => {
    nextCalled = true;
  });
  assert.equal(nextCalled, false);
  assert.equal(response.headers['Content-Type'], 'application/javascript');
  assert.match(response.body, /createHotContext/);
  assert.match(response.body, /updateStyle/);
  assert.equal(response.body.includes('WebSocket'), false);
  assert.equal(response.body.includes('localhost'), false);
  nextCalled = false;
  layers[0]({ url: '/src/main.js' }, response, () => {
    nextCalled = true;
  });
  assert.equal(nextCalled, true);
});

test('build export resolves in Node and has no browser fallback', async () => {
  const exported = await import('gods-eye-view/build/vite');
  assert.equal(exported.createBrowserViteConfig, createBrowserViteConfig);
  const pkg = JSON.parse(
    readFileSync(new URL('../../package.json', import.meta.url)),
  );
  assert.deepEqual(pkg.exports['./build/vite'], { node: './build/vite.js' });
});
