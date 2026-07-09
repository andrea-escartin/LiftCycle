# LiftCycle — PLAN.md

> **How to use this file:**
> Start every new Claude Code session with:
> "Claude, continue with PLAN.md"
> Claude Code reads this file, understands current state, and picks up exactly
> where the last session ended.
> Update this file at the END of every session before closing.

---

## Project overview

**LiftCycle** — a multi-user health tracking web app where users track their
menstrual cycle alongside workouts to understand how hormonal phases affect
training performance.

**Stack:** Python 3.12 + FastAPI + SQLModel + PostgreSQL + Alembic (backend)
         React 18 + TypeScript + Vite + Axios (frontend)
**Auth:** HttpOnly cookies (NOT localStorage)
**Hosting:** Railway (backend + DB + frontend)
**Docs:** 01_pdr.md · 02_user_stories.md · 03_tech_spec.md (project root)

---

## Overall progress: 37%

```
[█████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░] 37%
```

Stage 0 and Stage 1 complete (Alembic initialised, first migration applied).
Stage 2 in progress — cycles domain (CRUD + phase inference) complete;
workouts and exercises remain.

---

## Stage overview

| Stage | Description | Status |
|---|---|---|
| 0 | Reconcile existing backend with tech spec | ✅ COMPLETE |
| 1 | Backend foundation (restructured) | ✅ COMPLETE |
| 2 | Backend domains: cycles, workouts, exercises | 🔄 IN PROGRESS |
| 3 | Backend domains: symptoms, medications, dashboard, insights | ⏳ PENDING |
| 4 | Frontend foundation: router, auth flow, API client | ⏳ PENDING |
| 5 | Frontend pages: dashboard, cycle log, workout log | ⏳ PENDING |
| 6 | Frontend pages: insights, history, settings | ⏳ PENDING |
| 7 | Hosting: Railway deploy, env vars, end-to-end test | ⏳ PENDING |

---

## Detailed checklist

### Stage 0 — Reconciliation ✅ COMPLETE
- [x] Copy updated CLAUDE.md to project root
- [x] Copy 01_pdr.md, 02_user_stories.md, 03_tech_spec.md to project root
- [x] Reconciliation Prompt 1: restructure backend into domain folders
- [x] Reconciliation Prompt 2: UUID PKs, User model fields, UserUpdate schema
- [x] Reconciliation Prompt 3: HttpOnly cookie auth, /refresh, /logout endpoints
- [x] Reconciliation Prompt 4: tests updated for new structure
- [x] All 15 tests green after reconciliation

### Stage 1 — Backend foundation ✅ COMPLETE
- [x] config.py (pydantic-settings, all env vars)
- [x] database.py (engine, session, create_db_and_tables)
- [x] users/models.py (UUID PK, unit_preference, cycle_length_override, last_period_start, updated_at)
- [x] auth/ (router, service, schemas, dependencies — full cookie auth)
- [x] users/ (models, schemas, router stub, service stub)
- [x] cycles/ (models, schemas, service, router — UUID IDs)
- [x] Alembic initialised, first migration created and applied

### Stage 2 — Backend: cycles + workouts + exercises 🔄 IN PROGRESS
- [x] cycles/ phase inference logic added to service.py (exact algorithm from 03_tech_spec.md §5)
- [x] cycles/ missed-period warning surfaced on `POST /cycles` response
- [x] cycles/ `GET /cycles/phase/current` endpoint
- [x] Tests for cycles (25 tests passing: CRUD, phase inference unit tests, current-phase endpoint, missed-period warning, auth)
- [ ] workouts/ (models, schemas, service, router)
- [ ] exercises/ (models, seed migration with 60-80 presets, router)
- [ ] Tests for workouts + exercises

### Stage 3 — Backend: remaining domains
- [ ] symptoms/ (models, schemas, service, router)
- [ ] medications/ (models, schemas, service, router)
- [ ] dashboard/ (service assembles month data, router)
- [ ] insights/ (aggregation service, router)
- [ ] Tests for all above

### Stage 4 — Frontend foundation
- [ ] Install date-fns
- [ ] src/api/client.ts (Axios instance, withCredentials, 401 interceptor)
- [ ] src/context/AuthContext.tsx
- [ ] src/types/ (all interfaces mirroring backend schemas)
- [ ] src/App.tsx (router config, protected route wrapper)
- [ ] src/main.tsx (BrowserRouter, AuthContext provider)
- [ ] Page shells: Login, Register, Dashboard, CycleLog, WorkoutLog,
       WorkoutHistory, Insights, Settings
- [ ] src/api/auth.ts + Login and Register pages wired up
- [ ] src/utils/phaseInference.ts (mirrors backend logic exactly)
- [ ] src/utils/unitConversion.ts

### Stage 5 — Frontend: core pages
- [ ] Dashboard page (calendar, today card, recent workouts)
- [ ] CycleLog page (log period, symptoms, medications)
- [ ] WorkoutLog page (log workout, add exercises, templates)
- [ ] src/api/cycles.ts, workouts.ts, exercises.ts wired to pages

### Stage 6 — Frontend: remaining pages
- [ ] WorkoutHistory page (paginated list, filter by type)
- [ ] Insights page (charts, phase breakdown, exercise progression)
- [ ] Settings page (unit pref, cycle length, edit email/password, delete account)
- [ ] src/api/insights.ts, dashboard.ts, users.ts

### Stage 7 — Hosting
- [ ] GitHub repository created and pushed
- [ ] Railway account created
- [ ] PostgreSQL add-on created on Railway
- [ ] Backend deployed to Railway
- [ ] All env vars set on Railway
- [ ] Frontend deployed (Railway or Vercel)
- [ ] VITE_API_BASE_URL set to deployed backend URL
- [ ] Full end-to-end test on live URLs

---

## CURRENT SESSION RESULTS

### What was accomplished this session
1. Alembic initialised and wired to `app.config.settings` / `SQLModel.metadata`;
   first migration created and applied (`user`, `cycleentry` tables, UUID PKs).
2. Full cycles domain implemented: phase inference algorithm (03_tech_spec.md §5),
   missed-period warning on create, `GET /cycles/phase/current` endpoint.
   A second migration picked up an unrelated pending `user.period_length_override`
   column from a prior session and applied it.
3. 10 new tests added (25 total, all green); ruff lint/format clean.

### Current backend state
```
backend/
├── .env                     ← configured with real DB credentials
├── alembic/                 ✓ initialised, env.py wired to settings + models
│   └── versions/
│       ├── 13ababff6f70_initial_schema.py       ✓ user, cycleentry tables
│       └── e943cccae0e9_cycles_updated_schema.py ✓ user.period_length_override
├── app/
│   ├── main.py              ✓ /api/v1 prefix, cookie CORS, imports from domains
│   ├── config.py            ✓ pydantic-settings, all env vars
│   ├── database.py          ✓ engine, session, create_db_and_tables
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py        ✓ register, login, refresh, logout (cookie auth)
│   │   ├── service.py       ✓ hash, verify, create_access_token, create_refresh_token, verify_token
│   │   ├── schemas.py       ✓ stub
│   │   └── dependencies.py  ✓ get_current_user reads access_token cookie
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py        ✓ UUID PK, all spec fields + period_length_override
│   │   ├── schemas.py       ✓ UserCreate, UserRead, UserUpdate
│   │   ├── router.py        ✓ stub
│   │   └── service.py       ✓ stub
│   └── cycles/
│       ├── __init__.py
│       ├── models.py        ✓ UUID PK, UUID FK, updated_at
│       ├── schemas.py       ✓ CycleCreate/Update/Read, CycleCreateResponse, Phase, PhaseResult
│       ├── service.py       ✓ full CRUD + infer_phase (pure) + get_current_phase
│       └── router.py        ✓ CRUD + GET /cycles/phase/current
└── tests/
    ├── conftest.py          ✓ client fixture (in-memory SQLite)
    └── test_api.py          ✓ 25 tests, all passing
```

### Gaps closed this session
| Gap | Before | After |
|---|---|---|
| Migrations | None | Alembic initialised, 2 migrations applied |
| Cycle phase inference | Not implemented | `infer_phase` pure function, exact §5 algorithm |
| Missed-period warning | Not implemented | Surfaced as `missed_period_warning` on `POST /cycles` response |
| Current phase lookup | Not implemented | `GET /cycles/phase/current` |
| Test count | 15 tests | 25 tests (added phase inference + current phase + warning) |

### Decisions made this session
- Kept the existing `notes` field on cycle schemas and the existing
  `GET /cycles/{id}` endpoint rather than pruning to the narrower set in
  03_tech_spec.md §6 — both were already implemented and covered by passing
  tests; removing them wasn't asked for. (User confirmed this choice when asked.)
- `missed_period_warning` is only returned on the `POST /cycles` create
  response (via `CycleCreateResponse`), not on `CycleRead` generally, and not
  on the phase endpoint — matches the literal instruction ("include a warning
  flag in the response" was scoped to `create_cycle`).
- "Complete cycle" for the rolling-average cycle length = the gap in days
  between two consecutive cycle `start_date`s; the most recent cycle is never
  "complete" since it has no successor yet.

---

## Next session — Stage 2 continuation: workouts + exercises

### Next prompt draft

```
Following CLAUDE.md, implement the workouts and exercises domains.
Consult 03_tech_spec.md Section 4 (workouts, workout_exercises, exercise_presets
tables) and Section 6 (API endpoints). Consult 02_user_stories.md US-020 through
US-025 for acceptance criteria (log workout, log exercises, edit/delete,
save as template, plan a future workout, view history).
State your plan first.

Key rules to carry over from CLAUDE.md:
- is_planned=true workouts excluded from all insight calculations
- is_template=true workouts excluded from history and insight calculations
- weight_kg always stored in kg; conversion is a display concern only
- workout_exercises: either exercise_preset_id OR custom_name must be set

1. exercises/models.py — ExercisePreset (UUID PK, name unique, category)
2. Alembic seed migration — 60-80 common gym exercises across categories
   (Push, Pull, Legs, Core, Cardio, etc.)
3. workouts/models.py — Workout + WorkoutExercise (UUID PKs, cascade delete)
4. workouts/schemas.py, workouts/service.py, workouts/router.py per the
   endpoint table in 03_tech_spec.md §6 (create/list/get/patch/delete workout,
   add/update/delete exercise, save-as-template)
5. exercises/router.py — GET /exercises/presets, GET /exercises/presets/{id}/last-logged
6. Register both routers in main.py
7. Migration: alembic revision --autogenerate + upgrade head
8. Tests in tests/test_api.py for both domains; run uv run pytest -v, fix failures

Touch only workouts/, exercises/ files, main.py, and test_api.py.
```

---

## Key decisions log

| Decision | Choice | Reason |
|---|---|---|
| Backend framework | FastAPI | Type hints, auto docs, API-first |
| Database | PostgreSQL | Multi-user concurrent writes |
| ORM | SQLModel | Combines SQLAlchemy + Pydantic |
| Auth | HttpOnly cookies | Sensitive health data; XSS protection |
| Primary keys | UUID | No record count exposure, enumeration resistant |
| Package manager | uv | Faster than pip, auto venv |
| Frontend | React + TypeScript | Component model, type safety |
| Build tool | Vite | Fast HMR, CRA replacement |
| HTTP client | Axios | withCredentials support, interceptor for refresh |
| Date library | date-fns | Safe date arithmetic, no new Date() display issues |
| Styling | CSS Modules | No framework, per spec |
| Hosting | Railway | Free tier, PostgreSQL add-on, simpler than Render+Vercel |
| Architecture | Monorepo | Claude Code sees both sides at once |
| Structure | Domain folders | Scales better than flat routers/ |
| Build order | Reconcile → backend → frontend | Fix foundation before building up |
| Login response | Returns UserRead + sets cookies | Frontend gets user data on login without a separate /me call |
| conftest.py | client fixture lives there | Proper pytest convention; test_api.py is tests only |
| Cycles schema scope | Kept `notes` field + `GET /cycles/{id}` beyond tech-spec §6/§4 | Already implemented and tested; removing working, tested behavior wasn't asked for |
| Missed-period warning placement | Only on `POST /cycles` response (`CycleCreateResponse`) | Instruction scoped the warning to the create flow, not phase lookups |

---

## Important file locations

```
liftcycle/
├── CLAUDE.md              ← Claude Code reads this every task
├── PLAN.md                ← This file — session continuity
├── 01_pdr.md              ← Product requirements
├── 02_user_stories.md     ← User stories + acceptance criteria
├── 03_tech_spec.md        ← Authoritative tech reference
├── backend/
│   ├── .env               ← Secrets — never commit
│   ├── alembic/           ← Initialised, 2 migrations applied
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── auth/
│   │   ├── users/
│   │   ├── cycles/        ← CRUD + phase inference complete
│   │   ├── workouts/      ← future (Stage 2, NEXT STEP)
│   │   ├── exercises/     ← future (Stage 2, NEXT STEP)
│   │   ├── symptoms/      ← future (Stage 3)
│   │   ├── medications/   ← future (Stage 3)
│   │   ├── dashboard/     ← future (Stage 3)
│   │   └── insights/      ← future (Stage 3)
│   └── tests/
│       ├── conftest.py    ← client fixture
│       └── test_api.py    ← 25 tests, all green
└── frontend/
    ├── src/
    │   ├── App.tsx        ← minimal shell
    │   ├── main.tsx       ← minimal
    │   └── index.css      ← empty
    └── vite.config.ts
```

---

## Commands reference

```bash
# Backend (run from backend/)
uv run uvicorn app.main:app --reload --port 8000
uv run pytest -v
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"

# Frontend (run from frontend/)
npm run dev       # http://localhost:5173
npm run build
npm run lint

# Start next session
"Claude, continue with PLAN.md"
```

---

*Last updated: Session 3 complete. Stage 0 and Stage 1 done. Stage 2: cycles
domain (CRUD + phase inference + missed-period warning) done.
Next: workouts + exercises domains.*
