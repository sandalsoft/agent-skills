# God's Eye View (sandalsoft fork)

Private equivalent of [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view).
Do not push or open PRs against upstream.

## Hosted (Render)

- **Build:** `npm ci`
- **Start:** `npm start` → `HOST=0.0.0.0 vite` (respects `process.env.PORT`, default 4173)
- **Runtime:** Node `>=24.14.0` (`NODE_VERSION=24.14.0` in `render.yaml`)
- **HMR:** off when `RENDER` is set or `HOST` is not loopback. `server.hmr =
  false` is not enough in Vite 6 — `@vite/client` still connects and falls
  back to `localhost:$PORT`. Hosted mode appends `gev-hosted-no-hmr`, which
  stubs `/@vite/client` with no WebSocket.
- **Auth:** set both `GEV_BASIC_AUTH_USER` and `GEV_BASIC_AUTH_PASSWORD`. The
  `gev-basic-auth` plugin is first in `localProviderPlugins()` and is moved to
  the front of the Connect stack so it wraps Vite internals, Cesium assets, and
  every `/api` proxy. Leave both unset for passwordless localhost `npm run dev`.
- **Google Maps (browser key):** Map Tiles API + billing, HTTP referrer
  `https://gods-eye-view-std.onrender.com/*`.

## Layout

- `server/standalone/vite.config.js` — loads env, attaches `localProviderPlugins()`,
  passes `hosted` from `RENDER`
- `server/providers/local.js` — provider proxies + `basicAuthGate()`
- `build/vite.js` — browser Vite config (`HOST`/`PORT`, `allowedHosts`, HMR off when hosted)
