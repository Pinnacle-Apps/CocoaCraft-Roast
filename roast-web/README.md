# CocoaCraft Roast software foundation

This FastAPI service imports Artisan profiles, validates a versioned cacao roast-session record, computes RoR using source-preserved Artisan methods, and renders Matplotlib SVG charts. It is isolated from the original Qt desktop runtime and hardware drivers. Core tools have no paid-plan gates or session quotas. AI and hardware remain deferred.

## Vercel

Keep the existing Vercel project's Root Directory at `roast-web`. Python 3.12 and the root-level `app.py` expose the ASGI instance `app`. Deploy preview branches before changing production. The pinned `requirements.txt` includes only the headless service dependencies, not the desktop requirement set.

The public landing page describes development status, `/api/health` reports health, and `/api/source` offers AGPL/source information. `/docs` describes API contracts; all session and reference operations require account verification. The former public simulated `/api/chart.svg` probe has been replaced by authenticated `POST /api/v1/sessions/chart.svg` with a supplied session.

Configure `COCOACRAFT_SUPABASE_URL` and `COCOACRAFT_SUPABASE_PUBLISHABLE_KEY` for **the existing CocoaCraft account system** before private endpoint testing. No service-role key is used. Bearer tokens are validated upstream; missing configuration fails closed. This code does not create users, change database structure, query production rows or write live data. The hosted browser sign-in/handoff flow is still pending.

The caller owns the session between requests. There is no durable server storage; JSON and unchanged original alog text can be exported. Production links are supported by local mock adapters only; hosted APIs reject them until a real authorized integration exists. The curated catalog is empty until documented, reviewed cacao reference profiles are available.

## Local verification

From repository root, create an isolated Python 3.12 environment, install `roast-web/requirements-dev.txt`, then run:

```text
python -m unittest discover -s roast-web/tests -v
python tools/benchmark_roast.py
```

For a local ASGI server, install a chosen development ASGI runner separately and point it at `app:app` from this folder. No development server package is part of the production dependency set.

Read [the architecture audit](../docs/checkpoint-a/audit.md), [requirements authority](../docs/roast/requirements.md) and [validation results](../docs/roast/validation.md). Preserve Artisan attribution, the root AGPL license, and source availability for the exact deployed revision. The service reads Vercel's `VERCEL_GIT_COMMIT_SHA` for its source offer when present; operators must make that revision available. Extracted functions and their provenance are under `cocoaroast/vendor`.
