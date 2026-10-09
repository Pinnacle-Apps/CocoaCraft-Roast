# CocoaCraft Roast software validation

The first software foundation passes 12 local tests on Windows with Python 3.12.14. Dependency consistency and whitespace checks pass. This validates the first slice, not the complete Artisan engine or hosted CocoaCraft integration.

| Check | Result |
|---|---|
| Verbatim source extraction | Both selected RoR methods match the imported `canvas.py` source exactly |
| Numerical parity | Original-method oracle matches across 640 prefix cases: two methods, four window settings, irregular timestamps and probe dropouts |
| Independent expected result | Linear temperature ramps produce the expected 10 degrees/minute; final dropout repeats prior RoR |
| Actual upstream alog fixtures | All five files under `src/test` import, analyze and retain their original source text |
| Session interchange | JSON round trip preserves versioned fields, original markers, missing readings and source text |
| Malformed and unsafe input | Executable expressions, missing/mismatched arrays, duplicate times and nonfinite readings rejected |
| Account gate | Every private session endpoint rejects missing authentication; absent configuration returns 503; upstream rejection and anonymous users rejected |
| Account isolation | Cross-account submitted sessions rejected; mock repository and run linkage reject other owners |
| Reference copies | New ids and independent mutable copies; originals cannot be changed by editing a copy |
| API sequence | Import, analyze, render, JSON export and unchanged original alog export pass |
| Body and link boundaries | Oversized requests rejected; live production linkage unavailable rather than silently mocked |
| Concurrent plotting | Four concurrent SVG renders succeed with user-title escaping and no raw script elements |

The account tests use mocked upstream responses. No real account token, Supabase query, production record, billing data or hardware is used. The upstream desktop Qt suite was not run because the imported desktop code is unchanged and the new service deliberately does not install its desktop/device dependencies.

## Local performance measurements

For a synthetic 1,800-sample file, analysis took approximately 20–40 ms. The first analysis/render took 1.33 seconds, excluding a 4.57-second initial module import. Five concurrent requests completed in 1.52–6.97 seconds, with figure rendering serialized per process for Matplotlib safety. SVG output was 19,198 bytes. Exact measurements are in `local-benchmark.json`.

These are local Windows measurements with one small synthetic fixture and five concurrent calls, not a statistical p95 or Vercel cold-start benchmark. The proposed two-second concurrent rendering target is not demonstrated by these results. Hosted CPU, fonts, initialization, account verification, memory retention, bundle size and representative profile complexity must be measured before a persistent hosting decision or throughput promise.

## Remaining validation gates

- Real hosted CocoaCraft sign-in, token handoff, expiry/logout and workspace authorization.
- Full original smoothing, AUC, offline recomputation and background comparison parity.
- Cacao metadata/event workflows and evidence-backed reference profile applicability.
- Real production-run launch/return flow, retry behavior and persistence design.
- Vercel deployment correctness, bundle footprint, cold/warm latency and memory retention.
- Retrieval and verbatim preservation of the unavailable master plan v1.1 prose.

The test output includes a third-party Starlette/AnyIO deprecation warning. It does not fail these checks; an eventual dependency update should consider it separately from the numerical extraction.
