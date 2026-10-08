# CocoaCraft Roast web deployment probe

This small FastAPI/Matplotlib proof of concept is intentionally isolated from Artisan's original desktop code and dependency tree. Its roast values are **simulated** and it is not a validated roasting engine.

## Vercel

In the existing Vercel project `cocoacraft-roast`, change **Settings → Build and Deployment → Root Directory** from `src` to `roast-web` and choose the **FastAPI** framework preset if available (otherwise Other/Python auto-detection). Deploy the `master` branch. The recognized root-level `app.py` exposes a FastAPI ASGI instance named `app`.

Routes: `/` for a demonstration chart, `/api/chart.svg` for the Matplotlib SVG, and `/api/health` for status.

No Supabase configuration, background workers, or hardware integrations are required for this probe. Original Artisan source and AGPL obligations remain unchanged.
