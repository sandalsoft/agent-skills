# Architecture

God's Eye View on this host branch is the standalone Vite app plus local
provider middleware. The browser bundle is configured by
`createBrowserViteConfig()` in `build/vite.js`. That helper takes explicit
inputs only — it does not read `.env` or construct providers.

## Local vs hosted Vite

| Mode | How it starts | Bind | HMR |
|------|---------------|------|-----|
| Local `npm run dev` | `vite` | `localhost:4173` | on |
| Pinokio | launcher overrides host | `127.0.0.1:$PORT` | on |
| Hosted `npm start` | `HOST=0.0.0.0 vite` | `0.0.0.0:$PORT` | **off** |

Hosted mode is `RENDER=true` (Render sets this) or a non-loopback `HOST`.
`server/standalone/vite.config.js` passes `hosted` from `RENDER`; the helper
also treats `0.0.0.0` / `::` as hosted. Then:

- `server.hmr = false` — Vite server-side HMR channel off
- `gev-hosted-no-hmr` — Vite 6 still injects `@vite/client` when `hmr` is
  false; that client opens a websocket and falls back to `localhost:$PORT`.
  The plugin serves a style-capable stub (`updateStyle` / `createHotContext`)
  with no WebSocket so the browser never tries `wss://localhost:10000`.
- `server.strictPort = true` — bind the platform `PORT` or fail
- `server.allowedHosts = true` — accept `*.onrender.com`

Basic Auth (`gev-basic-auth`) stays first among provider plugins. The no-HMR
stub is appended after providers so it does not change that order. Local
loopback `npm run dev` is unchanged.

## Google Maps (hosted)

The client `GOOGLE_MAPS_API_KEY` is injected via Vite `define`. In Google Cloud
it must allow Map Tiles API, have billing enabled, and list referrer
`https://gods-eye-view-std.onrender.com/*`.

## Render crash recovery

iPhone Safari (WebGL1) used to request `msaaSamples: 4` while `MAX_SAMPLES` is 0.
A photoreal tile or NaN Cartesian then threw a plain object into Cesium's
render loop; the default panel printed `[object Object]` / `undefined` and
stopped the scene. `resolveViewerMsaaSamples()` clamps MSAA. Per-frame
layer ticks (`flights`, `militaryFlights`, `worldOverlay`) run through
`runGuardedFrame` / `runGuardedRecord`. `installSceneRenderRecovery()` logs
the real throw via `toError()` and re-enables `useDefaultRenderLoop`.

## Flight deep links

`#flight=UA4051` / `#flight=UAL4051` / `#icao24=<hex>` parse without camera
keys. `flightIdentity.js` normalizes IATA→ICAO and United Express regionals.
`flightResolver.js` scores live rows (configured aliases: UA4051→ASH4051,
UA700→UAL700). `FlightDeepLinkController` enables the flights layer, waits
on each refresh, and queries `/api/flight-lookup` (OpenSky worldwide cache,
then adsb.lol callsign/hex — not the 250 nm viewport fallback). Selected
or followed flights are written back into the share hash.
