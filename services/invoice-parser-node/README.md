# Invoice Parser Service (Node/TypeScript)

Your existing invoice parser stays exactly as-is, just wrapped in a thin HTTP layer
so the (Python) Manager App can call it like any other module.

## What to do (replaces the old "migrate to Python" task)

1. Copy your existing parsing logic files into `src/` (e.g. `src/parser.ts`)
2. In `src/index.ts`, uncomment the import and replace the placeholder `/run` handler
   body with a real call to your parsing function
3. If your parser currently writes to Google Sheets directly, keep that — no need
   to change it. The Manager App only needs to know "did the run succeed," not
   take over the output step.

## Run locally
```bash
npm install
npm run dev
```
Visit `http://localhost:8001/health` to confirm it's up.

## How the Manager App talks to this service
The Python backend calls `POST /run` on this service over HTTP (see
`app/shared/module_client.py` in the main repo). Same pattern will be used for
any other non-Python module you add later — the Manager App treats every module
as "something with a `/health` and `/run` endpoint," regardless of language.
