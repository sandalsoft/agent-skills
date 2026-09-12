import cesium from 'vite-plugin-cesium';

/** Loopback binds keep local HMR. Anything else is a public/LAN listen. */
export function isLoopbackHost(host) {
  return (
    !host || host === 'localhost' || host === '127.0.0.1' || host === '::1'
  );
}

/**
 * Hosted / public binds: Render (`hosted: true`) or a non-loopback HOST.
 * Prefer HMR off behind a TLS-terminating reverse proxy — the browser must
 * not fall back to `wss://localhost:$PORT`.
 */
export function isHostedViteServer({ hosted = false, host } = {}) {
  return Boolean(hosted) || !isLoopbackHost(host);
}

/**
 * Vite 6 still injects `@vite/client` when `server.hmr === false`. That client
 * opens a websocket and falls back to `localhost:$PORT` — exactly the Render
 * proxy failure. Serve a style-capable stub with no WebSocket instead.
 */
export const HOSTED_VITE_CLIENT_STUB = `const sheets = new Map();
export class ErrorOverlay extends HTMLElement {}
export function createHotContext() {
  return {
    accept() {},
    decline() {},
    dispose() {},
    prune() {},
    invalidate() {},
    on() {},
    off() {},
    send() {},
    data: {},
  };
}
export function updateStyle(id, content) {
  if (typeof document === 'undefined') return;
  let el = sheets.get(id);
  if (!el) {
    el = document.createElement('style');
    el.setAttribute('type', 'text/css');
    el.setAttribute('data-vite-dev-id', id);
    document.head.appendChild(el);
    sheets.set(id, el);
  }
  el.textContent = content;
}
export function removeStyle(id) {
  const el = sheets.get(id);
  if (!el || typeof document === 'undefined') return;
  el.remove();
  sheets.delete(id);
}
export function injectQuery(url) {
  return url;
}
`;

export function hostedNoHmrPlugin() {
  return {
    name: 'gev-hosted-no-hmr',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const path = req.url?.split('?')[0];
        if (path !== '/@vite/client') return next();
        res.setHeader('Content-Type', 'application/javascript');
        res.end(HOSTED_VITE_CLIENT_STUB);
      });
    },
  };
}

/** Build browser assets with explicit inputs; never load environment or providers. */
export function createBrowserViteConfig({
  plugins = [],
  googleApiKey,
  cesiumToken,
  host = 'localhost',
  port = 4173,
  hosted = false,
} = {}) {
  const bindHost = host || 'localhost';
  const hostedServer = isHostedViteServer({ hosted, host: bindHost });
  return {
    plugins: [
      cesium(),
      ...plugins,
      ...(hostedServer ? [hostedNoHmrPlugin()] : []),
    ],
    server: {
      host: bindHost,
      port: parseInt(port, 10) || 4173,
      ...(hostedServer
        ? {
            hmr: false,
            strictPort: true,
            allowedHosts: true,
          }
        : {
            allowedHosts: ['localhost', '127.0.0.1', '.local'],
          }),
      fs: {
        deny: ['.env', '.env.*', '*.{crt,pem}', '**/.git/**', '**/ENVIRONMENT'],
      },
      // These headers protect the document containing Provider Settings.
      headers: {
        'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "frame-ancestors 'none'",
      },
    },
    define: {
      'import.meta.env.GOOGLE_MAPS_API_KEY': JSON.stringify(googleApiKey),
      'import.meta.env.CESIUM_ION_TOKEN': JSON.stringify(cesiumToken),
    },
    build: { chunkSizeWarningLimit: 1500 },
  };
}
