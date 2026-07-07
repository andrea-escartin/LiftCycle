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

## Overall progress: 30%

```
[█████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30%
```

Stage 0 complete. Stage 1 code complete — only Alembic migration remaining.

---

## Stage overview

| Stage | Description | Status |
|---|---|---|
| 0 | Reconcile existing backend with tech spec | ✅ COMPLETE |
| 1 | Backend foundation (restructured) | 🔄 IN PROGRESS |
| 2 | Backend domains: cycles, workouts, exercises | ⏳ PENDING |
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

### Stage 1 — Backend foundation 🔄 IN PROGRESS
- [x] config.py (pydantic-settings, all env vars)
- [x] database.py (engine, session, create_db_and_tables)
- [x] users/models.py (UUID PK, unit_preference, cycle_length_override, last_period_start, updated_at)
- [x] auth/ (router, service, schemas, dependencies — full cookie auth)
- [x] users/ (models, schemas, router stub, service stub)
- [x] cycles/ (models, schemas, service, router — UUID IDs)
- [ ] Alembic initialised, first migration created and applied

### Stage 2 — Backend: cycles + workouts + exercises
- [ ] cycles/ phase inference logic added to service.py
- [ ] workouts/ (models, schemas, service, router)
- [ ] exercises/ (models, seed migration with 60-80 presets, router)
- [ ] Tests for all above

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
All 4 reconciliation prompts completed. Backend is now spec-compliant.

### Current backend state
```
backend/
├── .env                     ← configured with real DB credentials
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
│   │   ├── models.py        ✓ UUID PK, all spec fields
│   │   ├── schemas.py       ✓ UserCreate, UserRead, UserUpdate
│   │   ├── router.py        ✓ stub
│   │   └── service.py       ✓ stub
│   └── cycles/
│       ├── __init__.py
│       ├── models.py        ✓ UUID PK, UUID FK, updated_at
│       ├── schemas.py       ✓ UUID types
│       ├── service.py       ✓ full CRUD with UUID types
│       └── router.py        ✓ UUID path params
└── tests/
    ├── conftest.py          ✓ client fixture (in-memory SQLite)
    └── test_api.py          ✓ 15 tests, all passing, cookie-based auth
```

### Gaps closed this session
| Gap | Before | After |
|---|---|---|
| Project structure | Flat (routers/, services.py, models.py) | Domain folders |
| Auth token storage | Bearer token in Authorization header | HttpOnly cookies |
| Primary keys | Auto-increment integers | UUIDs |
| User model fields | email, hashed_password, is_active | + unit_preference, cycle_length_override, last_period_start, updated_at |
| Config loading | os.getenv() directly | pydantic-settings config.py |
| API base path | No prefix | /api/v1 |
| Refresh token | Not implemented | POST /api/v1/auth/refresh |
| Logout | Not implemented | POST /api/v1/auth/logout |
| Test count | 13 tests | 15 tests (added refresh + logout) |

---

## Next session — Stage 1 completion + Stage 2 start

### Next prompt: Alembic setup

```
Following CLAUDE.md, set up Alembic for database migrations.
State your plan first.

1. Initialise Alembic from inside backend/:
   uv run alembic init alembic

2. Update alembic/env.py:
   - Import settings from app.config
   - Set sqlalchemy.url = settings.DATABASE_URL
   - Import all SQLModel models so Alembic can detect them:
     from app.users.models import User
     from app.cycles.models import CycleEntry
   - Use SQLModel.metadata as target_metadata

3. Create the first migration:
   uv run alembic revision --autogenerate -m "initial schema"
   Review the generated file — confirm it creates users and cycle_entry
   tables with UUID primary keys.

4. Apply the migration:
   uv run alembic upgrade head

5. Confirm tables exist:
   uv run python -c "
   from sqlmodel import Session
   from app.database import engine
   from sqlmodel import text
   with Session(engine) as s:
       result = s.exec(text(\"SELECT tablename FROM pg_tables WHERE schemaname='public'\"))
       print(list(result))
   "

Touch only alembic/ files. Do not modify app/ files.
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
│   ├── alembic/           ← Migrations (after Alembic init — NEXT STEP)
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── auth/
│   │   ├── users/
│   │   ├── cycles/
│   │   ├── workouts/      ← future (Stage 2)
│   │   ├── exercises/     ← future (Stage 2)
│   │   ├── symptoms/      ← future (Stage 3)
│   │   ├── medications/   ← future (Stage 3)
│   │   ├── dashboard/     ← future (Stage 3)
│   │   └── insights/      ← future (Stage 3)
│   └── tests/
│       ├── conftest.py    ← client fixture
│       └── test_api.py    ← 15 tests, all green
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

*Last updated: Session 2 complete. Stage 0 done, Stage 1 code done.
Next: Alembic init + first migration, then Stage 2 (workouts, exercises).*
