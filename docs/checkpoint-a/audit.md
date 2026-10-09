# CocoaCraft Roast architecture audit and implementation sequence

CocoaCraft Roast can reuse Artisan's numerical logic while replacing its desktop event loop and Qt presentation boundary. The imported code is not a headless web engine: 89 of the 123 inventoried Artisan and plus modules directly import Qt. The initial software implementation therefore extracts a small, source-preserved calculation boundary and validates it before expanding to smoothing, profile analysis or control.

The user authorized execution without an additional audit approval stop on October 8, 2026. Database structure, RLS, migrations, billing, live record writes, AI and hardware remain outside this work.

## Source versions and requirements authority

| Source | Version or evidence | Use |
|---|---|---|
| Pinnacle-Apps/CocoaCraft-Roast | `562eca83144f954f271c98a51d5d6192863eeab7`, imported source on master | Artisan functions, desktop dependencies, prototype baseline |
| Pinnacle-Apps/CocoaCraft | `f96fab124f90a1845287aa075ed7e1c0e0ebb27d`, fetched origin/main | Current application and database structure context |
| Supabase snapshots | Generated `2026-10-08T13:23:04.404858+00:00`; both JSON and SQL read from the pinned Git revision | Structure only; hashes and relevant columns in `cocoacraft-context.json` |
| User's current request and follow-up | Full core policies supplied here; execution subsequently authorized | Current actionable requirements |
| Roaster integration status | Conversation `6ac7f925-f2d0-83e9-b217-08acffe7a6b7`; all five history pages read | User decisions available; assistant plans represented by content-reference placeholders |
| Project ZIP and metadata CSV | Named in project instructions but absent from the current `sources` folder | Historical context unavailable; current repository snapshots take precedence for structure |

**The complete master plan v1.1 and preceding expanded phases have not been recovered verbatim.** This audit and implementation sequence are new work based on inspected source and explicit user policies, not a replacement presented as that missing original. No claim of a complete verbatim transfer should be made. The authoritative original remains the referenced conversation.

## Current application structure

The Roast repository contains the complete imported desktop source under `src/artisanlib`, Artisan plus integration under `src/plus`, device support, desktop packaging workflows, translation assets, documentation and tests. Preserve these as the source baseline and regression oracle. Do not rename the complete repository into a web-only project or bundle the desktop dependency tree into Vercel.

The initial `roast-web/app.py` was a deployment probe: generated ET, BT and target curves with NumPy, used `np.gradient` for demonstration RoR, rendered an SVG with Matplotlib, and exposed public health/chart routes. It had no profile ingestion, CocoaCraft login, session contract, persistence or production linking. Its visual success did not validate Artisan math or cacao defaults.

CocoaCraft's current `pages/workspace/roast-profiles.tsx` and `pages/api/roast-profiles/index.ts` already handle profile definitions. The latter uses `createSupabaseSsrClient`, validates `auth.getUser`, resolves workspace context, and accepts up to 250 curve points. That sparse profile representation is unsuitable as the unmodified storage contract for long recorded sample streams. Preserve its current behavior during this software work.

Production execution uses `pages/api/production-runs`, with telemetry in `[id]/telemetry.ts`, and actual lots belong to production runs. `lib/supabase/server.ts` accepts verified account requests through SSR cookies or bearer tokens. `lib/user-org-context.ts` resolves the account workspace. Cross-host cookies and browser sign-in cannot be assumed to propagate to the independent Roast origin.

## Function and dependency map

The generated inventory covers 123 modules and 4,239 functions or methods. `module-map.md` summarizes module size, direct Qt imports and internal dependencies. `function-dependency-map.json` records each method's source range and syntactic calls plus each module's SHA-256. This is a static inventory, not a claim that dynamic callbacks or runtime import edges have been fully resolved.

| Capability | Existing source anchors | Dependencies and coupling | Extraction decision |
|---|---|---|---|
| Desktop application and profile state | `main.py`: `ApplicationWindow`, `loadFile`, `validateProfileDict`, `setProfile`, `getProfile` | Widgets, settings, canvas, plus synchronization, device lifecycle and UI errors | Keep upstream intact; introduce independent import/transport models |
| RoR | `canvas.py:4423` `compute_ror_simple`; `canvas.py:4437` `compute_ror` | Only NumPy, warnings, logging and `polyfitRoRcalc` within these selected methods | Extract verbatim into a tiny headless class; pin provenance and test against original AST |
| Input filtering and sampling | `canvas.py:4305` `inputFilter`; `sample_processing` immediately follows RoR | Profile semaphore, LCD updates, timestamps, extra probes, symbolic evaluation, events | Separate raw readings from display/control; no claim of a completed port |
| Recomputed deltas and smoothing | `canvas.py:8498` `recomputeDeltas`; `smoothETBT`, `smoothETBTBkgnd` | Canvas options, smoothing state, foreground/background arrays and rendering | Add offline smoothing only after fixture parity and missing-reading tests |
| Online filters | `filters.py`: `LiveLFilter`, `LiveSosFilter`, `LiveMedian`, `LiveMean` | NumPy, deques, bisect; no direct Qt import | Suitable later extraction; retain initialization and state semantics |
| Plot lifecycle | `canvas.py:178` `MplCanvas`; `redraw`, `drawDeltaET`, `drawDeltaBT`, `drawAUC` | `FigureCanvasQTAgg`, QWidget, signals, GUI renderer/layout state | Preserve Matplotlib; use `Figure` and Agg for web rendering; full desktop plot parity deferred |
| Background comparison and designer | `background.py`, `designer.py`, canvas BT/ET interpolation and spline methods | Canvas state, transforms, draggable annotations and Qt events | First add read-only overlays; editor follows validated calculation contracts |
| Replay | `simulator.py:147` `read`; `readextra` | NumPy interpolation; util conversion imports pull Qt transitively | Start with deterministic sample replay; preserve Artisan interpolation in later parity work |
| Profile interchange | `atypes.py` `ProfileData`; `main.py` load/validate methods; `roastlog.py`, `roastpath.py` | `atypes` imports QDateTime; extractors may fetch remote URLs and use Qt/url utilities | Parse supplied bytes only; retain original source text and unknown fields; no URL fetching |
| Events and alarms | `events.py`, `alarms.py`; canvas `EventRecordAction`, event playback | UI actions, hardware commands and stateful sampling | Record observations first; never execute commands imported from profiles |
| PID calculation | `pid.py` controller and integral-limit helpers | NumPy, filters, Qt semaphore | Future numerical isolation requires locking/time adapter and parity; no hardware control now |
| PID orchestration | `pid_control.py`: `FujiPID`, `PIDcontrol`, `DtaPID` | Application window, sliders, controller state, serial commands | Keep outside web runtime |
| Devices | `comm.py`, `async_comm.py`, `device_registry.py`, `modbusport.py`, Phidgets, BLE, MQTT and serial modules | PyQt, USB/native SDKs, platform tools, connections, timing and threads | Mock adapter first; local hardware bridge design only after software and hosting validation |
| Artisan plus | `src/plus` controller/account/stock/roast/queue/sync | Existing external service, credentials and persistence behavior | Do not repurpose it as CocoaCraft persistence or infer rights to hosted plus APIs |

## Qt decoupling assessment

Changing the Matplotlib backend alone does not remove Qt. `canvas.py` imports widgets, `QTimer`, `QSemaphore`, `QThread` and `FigureCanvasQTAgg`. `pid.py` directly imports `QSemaphore`; `atypes.py` imports QDateTime despite looking like a transport schema; `simulator.py` imports util functions with their transitive dependency tree. The original source metadata requires Python 3.12 or newer, while some dependency-file comments mention older versions; executable source and project metadata govern the new service.

Keep the desktop import path separate. Introduce three boundaries: numerical calculation on typed inputs; plotting from calculation output; acquisition and application integration through adapters. The first two must not import desktop canvas, application windows, Qt, hardware drivers or plus. Every extraction should preserve original numerical statements, document source hashes, and compare against an original-method oracle and independent expected results.

The current extraction contains only `compute_ror_simple` and `compute_ror`. It preserves simple-window endpoint averaging, least-squares NumPy polyfit, per-minute units, final probe-dropout fallback, and exception handling. It does not claim parity for full sampling, smoothing, AUC, background transforms, alarms, symbolic expressions or PID. Do not replace these functions with `np.gradient` or a browser chart library.

## Cacao adaptation

The useful reusable mechanisms are recording timed ET/BT readings, rate of rise, target/background comparison, control observations, replay, notes, export and eventual probe adapters. Cacao configuration belongs in metadata and presentation defaults, rather than changes to the numerical algorithms.

Record whole-bean versus nib form, origin and lot, fermentation observations, moisture, bean size, batch/output mass, roaster identity, probe location, airflow/power/drum observations and sensory outcomes. These fields are descriptive software data, not a universal roasting prescription. Preserve source temperature units and sample times, including pre-charge values; do not silently sort, resample or relabel probe measurements.

Use charge, drop, cooling completion and user observations as native cacao events. Preserve imported coffee markers explicitly as original Artisan markers. Do not silently convert first crack, second crack, dry end or coffee development metrics into cacao milestones. Validating cacao phase semantics, reference profiles and any thermal kill-step claims requires separate domain evidence; this implementation provides none of those claims.

The reference catalog requires source citation, reviewer, review date and applicability. All account types can create editable copies; editing a copy cannot mutate the curated source. The catalog starts empty because no documented, reviewed cacao reference data was supplied. Synthetic fixtures are tests and must never appear as curated production guidance.

## CocoaCraft database context

Both current structure snapshots contain `roast_profiles`, `production_runs`, `production_run_steps`, `machine_runs`, `machine_telemetry` and `org_members`. The JSON records columns, constraints and policies; the SQL confirms table definitions. Relevant structure and hashes are saved in `cocoacraft-context.json` with no row data.

`roast_profiles` stores definitions, `curve_points`, guidance objects and status. `production_runs` stores execution, has `machine_run_id`, and records actual yields and consumption status. `production_run_steps` references its run and machine; `machine_runs` has target profile and summary; `machine_telemetry` records time, metric, value and unit. These existing fields are context for a future mapping, not authorization to force the new transport record into them.

The software contract must settle raw sample density, reference-copy provenance, ownership/workspace scope, events, settings, import fidelity, lifecycle and retry semantics before a persistence mapping is implemented. No table, policy, migration, billing rule or production record is changed. The local mock production adapter does not create or complete CocoaCraft runs or consume lots.

## Service and API contracts

The new stateless endpoints operate on `RoastSession` schema version `1.0`. Both standalone and mock production-linked workflows use exactly this model; the latter adds a `production_link`, not a second record format. It contains identity, owner, timestamps, cacao metadata, original source units, ordered samples, explicit events, engine settings, notes and optional original Artisan text.

| Endpoint | Request | Response and behavior |
|---|---|---|
| `GET /api/health` | None | Public service status; no readings or account data |
| `GET /api/source` | None | Public AGPL notice and source repository |
| `POST /api/v1/sessions/import` | `{profile_text: string}` | Safely parsed Artisan session with owner taken from verified account |
| `POST /api/v1/sessions/validate` | Complete session | Validated record; duplicate/nonincreasing timestamps rejected |
| `POST /api/v1/sessions/analyze` | Complete session | ET and BT RoR, units, method and explicit analysis scope |
| `POST /api/v1/sessions/chart.svg` | Complete session | Matplotlib SVG; temperature and RoR axes, original event labels |
| `POST /api/v1/sessions/export` | Complete session | Versioned JSON export |
| `POST /api/v1/sessions/original.alog` | Imported session | Original text unchanged; does not claim to export edits as a rewritten alog |
| `GET /api/v1/reference-profiles` | None | Curated catalog metadata; currently empty |
| `POST /api/v1/reference-profiles/{id}/copy` | None | Independent editable session copy; missing ids return 404 |

Private endpoints validate an existing CocoaCraft bearer token through that account system's Auth user endpoint. Missing tokens return 401; unconfigured verification returns 503; another owner returns 403; invalid data returns 422; excessive body size returns 413. Anonymous Auth users do not satisfy account-required policy. There is no deployment bypass switch, plan quota, paid-core restriction, AI entitlement endpoint or billing write.

The hosted login UI and token handoff still require application integration. Do not place tokens in query strings or localStorage, infer membership from user-editable metadata, or assume cross-origin cookies work. Production workspace authorization must remain with verified CocoaCraft membership. Hosted requests reject production links with 501 until a real authorized integration exists; local mock linking tests the contract first.

The service stores no sessions globally and writes no filesystem data. Callers own their current record and exports. The in-memory repository is an explicitly local test adapter. Per-request limits (2 MB body, 1 MB source text and 10,000 samples) bound CPU and parsing; they are not paid-plan quotas or a cap on free session count.

## AGPL obligations and source fidelity

Artisan headers and the root AGPL license remain in place. The numerical excerpts retain the original copyright/license header and carry a provenance file with source lines and SHA-256 hashes. New Roast work is designated AGPL-3.0-or-later and stays in the independent public Roast repository.

AGPL section 13 addresses corresponding source for users interacting remotely with a modified program. Hosted users must have an accessible source offer for the exact deployed implementation, including build instructions and dependencies. A generic credit, a link to unmodified Artisan or a private repository is insufficient. Publish the deployed revision and retain its build manifest. See [the repository license](https://github.com/Pinnacle-Apps/CocoaCraft-Roast/blob/master/LICENSE) and [the GNU AGPL text](https://www.gnu.org/licenses/agpl-3.0.html).

A separate repository and HTTP API are engineering boundaries, not a conclusive legal determination about combined or derivative work. Keep Artisan code and numerical execution in Roast, use documented transport contracts in CocoaCraft, and obtain a licensing review if later integration closely combines code or behavior. Do not imply that Artisan plus service/API access follows from the desktop source license, and do not imply Artisan endorsement of cacao adaptations.

## Vercel hosting risks and performance gate

Vercel remains the first platform for software tests. Its [Python runtime](https://vercel.com/docs/functions/runtimes/python) supports the existing `roast-web/app.py` ASGI entrypoint and documents a standard 500 MB uncompressed bundle limit. It includes reachable Python files by default, so keep Root Directory at `roast-web`; do not package the gigabyte-scale imported wiki, Qt desktop runtime or all drivers.

Function lifetime is not a durable roast session. Keep requests bounded and stateless; process restarts, scaling and deployments must not lose the only copy of readings. Reassess persistent hosting after measurements, including cold/warm latency, NumPy and font initialization, bundle size, process memory, response size, render contention and account-verification latency. Current [function limits](https://vercel.com/docs/functions/limitations) and project settings must be checked at test time; do not rely on historical timeout assumptions or assume beta features are enabled.

[Matplotlib's thread guidance](https://matplotlib.org/stable/users/faq.html#work-with-threads) requires care around concurrent access. The new renderer uses a noninteractive backend, request-local figures and a process-local render lock. This serializes figure work within an instance; load testing must measure the throughput cost. The lock is not shared state for sessions and does not coordinate separate instances.

Proposed performance acceptance targets, to be validated rather than reported as achieved: correct concurrent renders without cross-account leakage; no raw data in logs; no increasing figure/memory retention across repeated renders; p95 warm analysis/render of a 1,800-sample file below two seconds at five concurrent requests; cold response below five seconds; bodies and responses below platform limits; deployed dependency bundle below its configured limit. Record actual observed values and revise hosting only on evidence. No hardware timing/control loop should depend on these function timings.

## Project structure

```text
src/artisanlib/                 imported Artisan source and oracle
src/plus/                      original integration, not CocoaCraft storage
src/test/                      upstream regression suite
roast-web/app.py               Vercel entrypoint
roast-web/cocoaroast/
  models.py                    unified record and cacao metadata
  profiles.py                  safe supplied-file ingestion and source round trip
  engine.py                    numerical orchestration
  plotting.py                  headless Matplotlib rendering
  adapters.py                  local mock replay, repository and production linking
  references.py                reviewed catalog and isolated copies
  auth.py                      existing account verification boundary
  api.py                       stateless API and request limits
  vendor/                      source-preserved excerpts and provenance
roast-web/tests/               parity, interchange, account isolation and API tests
tools/                         reproducible static audit and extraction scripts
docs/checkpoint-a/             audit, dependency map and structural context
docs/roast/                    requirements, API, validation and implementation status
```

## Stepwise implementation PR plan

| PR | Implementation | Acceptance checks | Status |
|---|---|---|---|
| 1 Audit and software foundation | Inventory, structure evidence, unified model, safe profile import, original RoR, mock adapters, reference-copy boundary, authenticated stateless API and Matplotlib SVG | Original method parity; expected linear units; dropout/irregular-time cases; invalid-data rejection; unchanged original source export; account isolation; concurrent rendering | Implemented locally with this audit; test results recorded separately |
| 2 Hosted workspace and account handoff | Integrate existing CocoaCraft sign-in through verified workspace entry; browser import, observations, settings, chart and export; standalone first | Real hosted account flow, no token logs/URL queries, expiry/logout, free-plan core access, accessible chart controls | Pending; account credentials and hosted entry integration not configured by this PR |
| 3 Full offline engine parity | Extract original smoothing/delta/AUC functions, background overlays, time alignment and designer boundaries | Golden upstream profile corpus across settings, units and missing data; explicit tolerances and preserved source hashes | Pending |
| 4 Production workflow with mocks | Launch from synthetic run context, same session schema, link/relink/complete transitions and retry semantics | Wrong owner/workspace rejected; standalone fields retained; repeated completion idempotent; no inventory writes | Local link/replay primitives complete; application workflow pending |
| 5 Curated reference registry | Evidence-backed cacao profiles with provenance, reviewer, scope and copy UI | No unreviewed recipes; immutable source; independent editable copies for free and paid accounts | Data model complete; real reviewed entries pending |
| 6 Vercel performance tests | Instrument bounded requests; record representative profile cases and concurrency; actual hosting comparison if required | Cold/warm p50/p95, memory, bundle and retention evidence; correctness under concurrency | Local test tooling and results to be recorded; hosted gate pending |
| 7 Persistence design after software | Map settled contract to current CocoaCraft structure and identify only necessary changes | Explicit later database authorization; migrations and automated snapshot refresh if structure changes are approved | Deferred by user constraint; no SQL/migration proposal in this work |
| 8 Hardware bridge later | Local acquisition adapter, clock semantics, disconnection recovery, device capabilities and safety/control separation | Replay versus device traces; connection loss; timestamps; local control safety | Deferred |
| 9 Paid-plan AI later | Assistance on every paid plan with free core unchanged, grounded inputs and suggestions only | Entitlement tests for all paid plans; no core quotas; provenance and review; no autonomous hardware changes | Deferred; no AI or billing implementation |

## Completion checklist

- [x] Inspect current Roast and CocoaCraft source revisions.
- [x] Read both current Supabase structure snapshots without querying or exporting rows.
- [x] Produce full static function/module inventory and Qt assessment.
- [x] Preserve upstream source and selected numerical methods with provenance.
- [x] Define cacao metadata without changing Artisan numerical statements.
- [x] Define one record format for standalone and mock production-linked sessions.
- [x] Implement mock adapters before database and hardware integration.
- [x] Require existing account verification for private hosted endpoints, fail closed when unconfigured.
- [x] Keep core independent of paid-plan checks; leave AI deferred.
- [ ] Complete verbatim master plan v1.1 transfer; reader currently exposes placeholders.
- [ ] Complete hosted workspace and real account-entry integration.
- [ ] Validate full offline Artisan calculation pipeline beyond selected RoR functions.
- [ ] Supply documented, reviewed cacao references.
- [ ] Measure hosted Vercel performance and bundle behavior.
- [ ] Implement persistence or hardware only in their later authorized phases.

Local checks and actual measurements belong in `../roast/validation.md`. None of the pending gates should be described as complete merely because the first software PR passes.
