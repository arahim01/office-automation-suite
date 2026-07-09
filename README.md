# Office Automation Suite

Manager app + 10 automation modules. Built as one FastAPI backend, one Postgres database,
one deployable web app.

## Day 1 setup (do this today)

### 1. Local environment
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Start Postgres locally
```bash
docker compose up -d
```

### 3. Run the app
```bash
uvicorn app.main:app --reload
```
Visit **http://localhost:8000** — you should see the Manager dashboard with all 10 modules
listed as "Not Started" (2 marked "Existing" for your invoice parser and meeting summary apps).

Visit **http://localhost:8000/api/modules** to see the same data as JSON — this is the API
the rest of the modules and, eventually, the orchestrator will read from.

### 4. Deploy to get a live URL (Railway or Render)
1. Push this repo to GitHub
2. Create a new project on Railway (railway.app) or Render (render.com), connect the repo
3. Add a Postgres addon/database from their dashboard
4. Set the `DATABASE_URL` environment variable in the platform to the addon's connection string
5. Deploy — both platforms detect the `Dockerfile` automatically
6. Confirm the deployed URL shows the same dashboard

That's Day 1 done: **repo, database, and a live deployed URL, with a working status dashboard
seeded with all 10 modules + the manager app itself.**

## Project structure
```
app/
  main.py            → FastAPI entrypoint, seeds the modules table on startup
  core/
    config.py        → environment/settings
    database.py      → SQLAlchemy engine/session
  manager/
    models.py        → Module table (status, priority, last_run)
    routes.py         → dashboard + /api/modules endpoints
  apps/
    meeting_summary/  → Day 4: migrate existing script here (Python)
    (remaining Python modules get their own folder as you build them, Week 2 onward)
  shared/
    module_client.py  → generic HTTP client the Manager App uses to call ANY module,
                         Python or otherwise (this is how the Node invoice parser plugs in)
  templates/
    dashboard.html    → the Manager App's status view (v0)

services/
  invoice-parser-node/  → your existing TypeScript invoice parser, wrapped in a thin
                           Express HTTP API (/health, /run). Runs as its own service —
                           no rewrite needed. See its own README for the 3-step wiring.
```

## A note on the invoice parser
It's TypeScript/Node, not Python — and that's fine. Rather than rewriting working logic,
it runs as its own small service exposing `/health` and `/run`, and the Manager App calls
it over HTTP via `app/shared/module_client.py`. This is the same pattern you'd use for
any future module written in a different language — the Manager App only cares that a
module answers `/health` and `/run`, not what it's written in.

## What's NOT built yet (by design)
This is a walking skeleton, not a finished manager app. The `/api/modules/{slug}/status`
PATCH endpoint lets you update a module's status manually for now — real orchestration
(scheduling, triggering, logging per-module) comes in Week 6, once the modules it needs
to orchestrate actually exist.
