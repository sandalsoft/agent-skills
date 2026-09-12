import test from 'node:test';
import assert from 'node:assert/strict';
import {
  basicAuthGate,
  localProviderPlugins,
} from '../server/providers/local.js';
import { knownKeySetupEnvVars } from './keySetupCore.mjs';

function install(plugin) {
  const layers = [];
  const server = {
    middlewares: {
      stack: layers,
      use(handler) {
        layers.push({ route: '', handle: handler });
      },
    },
  };
  const post = plugin.configureServer(server);
  return { layers, post, middleware: layers[0]?.handle };
}

function request(middleware, headers = {}) {
  let nextCalled = false;
  const response = {
    status: 0,
    headers: {},
    writeHead(status, headers) {
      this.status = status;
      this.headers = headers;
    },
    end(body) {
      this.body = body;
    },
  };
  middleware({ headers, url: '/', method: 'GET' }, response, () => {
    nextCalled = true;
  });
  return { response, nextCalled };
}

function withAuthEnv(user, password, fn) {
  const previousUser = process.env.GEV_BASIC_AUTH_USER;
  const previousPassword = process.env.GEV_BASIC_AUTH_PASSWORD;
  const assign = (key, value, previous) => {
    if (value === undefined) {
      if (previous === undefined) delete process.env[key];
      else process.env[key] = previous;
      return;
    }
    process.env[key] = value;
  };
  assign('GEV_BASIC_AUTH_USER', user, undefined);
  assign('GEV_BASIC_AUTH_PASSWORD', password, undefined);
  try {
    return fn();
  } finally {
    assign('GEV_BASIC_AUTH_USER', previousUser, previousUser);
    assign('GEV_BASIC_AUTH_PASSWORD', previousPassword, previousPassword);
  }
}

test('basic auth is the first local provider so it wraps every later proxy', () => {
  assert.equal(localProviderPlugins()[0].name, 'gev-basic-auth');
});

test('hosted auth credentials stay out of the Provider Settings write set', () => {
  const known = knownKeySetupEnvVars();
  assert.equal(known.has('GEV_BASIC_AUTH_USER'), false);
  assert.equal(known.has('GEV_BASIC_AUTH_PASSWORD'), false);
});

test('auth is inactive unless both credentials are set', () => {
  const { middleware } = install(basicAuthGate());
  withAuthEnv(undefined, undefined, () => {
    const { response, nextCalled } = request(middleware);
    assert.equal(nextCalled, true);
    assert.equal(response.status, 0);
  });
  withAuthEnv('only-user', undefined, () => {
    const { nextCalled } = request(middleware);
    assert.equal(nextCalled, true);
  });
  withAuthEnv(undefined, 'only-password', () => {
    const { nextCalled } = request(middleware);
    assert.equal(nextCalled, true);
  });
});

test('missing or wrong credentials receive 401 and a Basic challenge', () => {
  const { middleware } = install(basicAuthGate());
  withAuthEnv('gev', 'secret', () => {
    const missing = request(middleware);
    assert.equal(missing.nextCalled, false);
    assert.equal(missing.response.status, 401);
    assert.equal(
      missing.response.headers['WWW-Authenticate'],
      'Basic realm="Gods Eye View"',
    );

    const wrong = request(middleware, {
      authorization: `Basic ${Buffer.from('gev:wrong').toString('base64')}`,
    });
    assert.equal(wrong.nextCalled, false);
    assert.equal(wrong.response.status, 401);
    assert.equal(
      wrong.response.headers['WWW-Authenticate'],
      'Basic realm="Gods Eye View"',
    );
  });
});

test('valid credentials pass through to later middleware', () => {
  const { middleware } = install(basicAuthGate());
  withAuthEnv('gev', 'secret', () => {
    const { response, nextCalled } = request(middleware, {
      authorization: `Basic ${Buffer.from('gev:secret').toString('base64')}`,
    });
    assert.equal(nextCalled, true);
    assert.equal(response.status, 0);
  });
});

test('configureServer post-hook moves the gate to the front of the stack', () => {
  const plugin = basicAuthGate();
  const layers = [
    { route: '', handle: () => {} },
    { route: '', handle: () => {} },
  ];
  const server = {
    middlewares: {
      stack: layers,
      use(handler) {
        layers.push({ route: '', handle: handler });
      },
    },
  };
  const post = plugin.configureServer(server);
  assert.equal(typeof post, 'function');
  const gate = layers[2].handle;
  post();
  assert.equal(layers[0].handle, gate);
  assert.equal(layers.length, 3);
});
