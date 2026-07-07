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

## Overall progress: 20%

```
[█████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 20%
```

Progress reset from 45% — the original backend needs reconciliation with
the tech spec before it counts toward the real target.

---

## Stage overview

| Stage | Description | Status |
|---|---|---|
| 0 | Reconcile existing backend with tech spec | 🔄 IN PROGRESS |
| 1 | Backend foundation (restructured) | ⏳ PENDING |
| 2 | Backend domains: cycles, workouts, exercises | ⏳ PENDING |
| 3 | Backend domains: symptoms, medications, dashboard, insights | ⏳ PENDING |
| 4 | Frontend foundation: router, auth flow, API client | ⏳ PENDING |
| 5 | Frontend pages: dashboard, cycle log, workout log | ⏳ PENDING |
| 6 | Frontend pages: insights, history, settings | ⏳ PENDING |
| 7 | Hosting: Railway deploy, env vars, end-to-end test | ⏳ PENDING |

---

## Detailed checklist

### Stage 0 — Reconciliation (DO THIS FIRST)
- [ ] Rename project folder to liftcycle/ (or keep name, update references)
- [ ] Copy updated CLAUDE.md to project root
- [ ] Copy 01_pdr.md, 02_user_stories.md, 03_tech_spec.md to project root
- [ ] Run Reconciliation Prompt 1: restructure backend folders
- [ ] Run Reconciliation Prompt 2: update config, database, models to spec
- [ ] Run Reconciliation Prompt 3: update auth to HttpOnly cookies
- [ ] Run Reconciliation Prompt 4: update tests for new structure
- [ ] All existing tests green after reconciliation

### Stage 1 — Backend foundation
- [ ] config.py (pydantic-settings)
- [ ] database.py (engine, session, UUID support)
- [ ] users/models.py (full User table per spec)
- [ ] auth/ (router, service, schemas, dependencies)
- [ ] users/ (router, service, schemas)
- [ ] Alembic initialised, first migration created and applied

### Stage 2 — Backend: cycles + workouts + exercises
- [ ] cycles/ (models, schemas, service with phase inference, router)
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

## CURRENT SESSION: Stage 0 — Reconciliation

### What exists right now (built in previous session)
```
backend/
├── app/
│   ├── main.py          ✓ exists, needs restructuring + /api/v1 prefix
│   ├── models.py        ✓ exists, needs: UUID PKs, domain split, missing fields
│   ├── db.py            ✓ exists, rename to database.py, move to domain pattern
│   ├── auth.py          ✓ exists, needs: cookie auth, refresh token, restructure
│   ├── services.py      ✓ exists, needs: split into cycles/service.py
│   └── routers/
│       ├── auth.py      ✓ exists, needs: cookie response, refresh endpoint
│       └── cycles.py    ✓ exists, mostly reusable
├── tests/
│   └── test_api.py      ✓ exists, needs updating after restructure
frontend/
├── src/
│   ├── App.tsx          ✓ exists (minimal shell)
│   ├── main.tsx         ✓ exists (minimal)
│   └── index.css        ✓ exists (empty)
```

### Why reconciliation is needed (gap summary)
| Gap | Current state | Required by spec |
|---|---|---|
| Auth token storage | Bearer token in Authorization header | HttpOnly cookies |
| Primary keys | Auto-increment integers | UUIDs |
| Project structure | Flat (routers/, services.py, models.py) | Domain folders |
| User model fields | email, hashed_password, is_active | + unit_preference, cycle_length_override, last_period_start, updated_at |
| Config loading | os.getenv() directly | pydantic-settings in config.py |
| API base path | No prefix | /api/v1 |
| Access token expiry | 30 min | 15 min |
| Refresh token | Not implemented | 30-day refresh with silent retry |

---

## Next actions — run these prompts in order

### Reconciliation Prompt 1 — Restructure folders

```
Following CLAUDE.md, restructure the backend folder layout to match the
domain-based structure in the tech spec. This is a refactoring task —
no logic changes, only file reorganisation.

State your plan before making any changes.

Create these new files/folders (move and adapt existing code):
- backend/app/config.py
    Load all settings via pydantic-settings from .env:
    DATABASE_URL, SECRET_KEY, REFRESH_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES (int), REFRESH_TOKEN_EXPIRE_DAYS (int),
    FRONTEND_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    EMAIL_FROM, ENVIRONMENT
    Export a single settings = Settings() instance.

- backend/app/database.py
    Move content from app/db.py here. No logic changes.
    Import DATABASE_URL from config.py instead of os.getenv().

- backend/app/auth/ (folder)
    Create: __init__.py, router.py, service.py, schemas.py, dependencies.py
    Move auth logic from app/auth.py and app/routers/auth.py into these files.
    No logic changes yet — just reorganise.

- backend/app/cycles/ (folder)
    Create: __init__.py, router.py, service.py, models.py, schemas.py
    Move cycle logic from app/services.py and app/routers/cycles.py.
    Move CycleEntry model and schemas from app/models.py.
    No logic changes yet.

- backend/app/users/ (folder)
    Create: __init__.py, router.py, service.py, models.py, schemas.py
    Move User model and schemas from app/models.py.
    router.py and service.py can be empty stubs for now.

Update backend/app/main.py:
    - Import from new domain paths
    - Register routers with prefix /api/v1
    - No other logic changes

After reorganising, run: uv run uvicorn app.main:app --reload --port 8000
Confirm /api/v1/health returns {"status": "ok"} and /api/v1/docs loads.
Then run: uv run pytest -v
All existing tests must still pass. Fix any import errors.

Delete old files after confirming tests pass:
app/db.py, app/auth.py, app/models.py, app/services.py,
app/routers/auth.py, app/routers/cycles.py, app/routers/__init__.py
```

---

### Reconciliation Prompt 2 — UUIDs, User model, config

```
Following CLAUDE.md, update models and config. State your plan first.

1. backend/app/users/models.py — update User table to match spec exactly:
   - id: UUID primary key (use uuid4 as default)
   - email: str, unique, indexed
   - hashed_password: str
   - unit_preference: str, default "kg"  (values: "kg" or "lbs")
   - cycle_length_override: int | None = None  (range 21-45, nullable)
   - last_period_start: date | None = None
   - is_active: bool, default True
   - created_at: datetime, default utcnow
   - updated_at: datetime, default utcnow (update on every save)

   Update UserCreate schema: add last_period_start (required) and
   cycle_length_override (optional, default 28).
   Update UserRead schema: include all new fields except hashed_password.

2. backend/app/cycles/models.py — update CycleEntry table:
   - id: UUID primary key
   - user_id: UUID, foreign key to user.id
   - All other fields stay the same
   - Add updated_at: datetime

3. backend/app/database.py — ensure UUID columns work with SQLModel.
   No other changes.

4. backend/app/users/schemas.py — add:
   - UserUpdate: optional email, optional password, optional unit_preference,
     optional cycle_length_override

After changes run: uv run pytest -v
Fix any failures. Tests may need User creation calls updated to include
last_period_start field.
Touch only the files listed above.
```

---

### Reconciliation Prompt 3 — HttpOnly cookie auth

```
Following CLAUDE.md, update auth to use HttpOnly cookies.
This replaces the current Bearer token approach.
State your plan and the exact changes before writing any code.

1. backend/app/auth/service.py
   - create_access_token(data: dict) -> str  (unchanged, 15 min expiry)
   - create_refresh_token(data: dict) -> str  (new, 30 day expiry,
     uses REFRESH_SECRET_KEY)
   - verify_token(token: str, secret_key: str) -> dict
     (generalised — used for both token types)

2. backend/app/auth/router.py — update these endpoints:

   POST /api/v1/auth/register
   - Same logic as before
   - On success: set two HttpOnly cookies on the response:
       access_token: 15 min expiry
       refresh_token: 30 day expiry
   - Return UserRead (not the token — cookie is set automatically)

   POST /api/v1/auth/login
   - Same validation logic
   - On success: set same two HttpOnly cookies
   - Return UserRead

   POST /api/v1/auth/refresh  (new endpoint)
   - Read refresh_token from cookies
   - Validate it using REFRESH_SECRET_KEY
   - Issue new access_token cookie (15 min)
   - Return {"ok": true}

   POST /api/v1/auth/logout  (new endpoint)
   - Clear both cookies by setting them with past expiry
   - Return {"ok": true}

3. backend/app/auth/dependencies.py
   - get_current_user: read access_token from cookies (not Authorization header)
   - Same validation logic, different source
   - Raise 401 if cookie missing or invalid

4. backend/app/main.py
   - Update CORS: replace allow_origins=["*"] with
     allow_origins=[settings.FRONTEND_URL]
   - Add allow_credentials=True to CORSMiddleware
   - No other changes

Cookie settings to use in all set_cookie calls:
   httponly=True
   samesite="lax"
   secure=True if settings.ENVIRONMENT == "production" else False
   path="/"

After changes: restart server, manually test register and login in /docs.
Then run: uv run pytest -v
Tests will need updating — update test fixtures to read cookies from
response instead of Authorization headers. Fix all failures.
Touch only the files listed above.
```

---

### Reconciliation Prompt 4 — Update tests

```
Following CLAUDE.md, update backend/tests/test_api.py to work with
the new structure. State your plan first.

The main changes needed:
1. Import paths have changed (new domain folder structure)
2. Auth now uses cookies, not Authorization headers
3. User creation now requires last_period_start field
4. All IDs are now UUIDs (string format in JSON, not integers)
5. API paths now prefixed with /api/v1

Update the test fixtures:
- engine/session fixture: unchanged logic, check imports still work
- client fixture: unchanged
- auth_headers fixture: register + login now set cookies on the
  TestClient automatically — no need to manually set headers.
  Return the user object instead of headers dict.
  Tests that need auth should use the authenticated client directly.

Update all tests:
- Remove Authorization header passing — cookies are automatic
- Update User creation dicts to include last_period_start
- Update ID assertions to expect strings (UUIDs), not integers
- Update all URL paths to include /api/v1 prefix

Run: uv run pytest -v
All 15 tests must pass. Fix any remaining failures.
Touch only test_api.py.
```

---

### After reconciliation — Stage 1 prompt

Once all 4 reconciliation prompts are done and tests are green,
the next prompt is Stage 1: Alembic setup and first migration.

```
Following CLAUDE.md, set up Alembic for database migrations.
State your plan first.

1. Initialise Alembic from inside backend/:
   uv run alembic init alembic

2. Update alembic/env.py:
   - Import settings from app.config
   - Set sqlalchemy.url = settings.DATABASE_URL
   - Import all SQLModel models so Alembic can detect them
   - Use SQLModel.metadata as target_metadata

3. Create the first migration:
   uv run alembic revision --autogenerate -m "initial schema"
   Review the generated file — confirm it creates users and cycles tables
   with UUID primary keys.

4. Apply the migration:
   uv run alembic upgrade head

5. Confirm tables exist by running:
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
│   ├── alembic/           ← Migrations (after Stage 1)
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── auth/
│   │   ├── users/
│   │   ├── cycles/
│   │   ├── workouts/      ← future
│   │   ├── exercises/     ← future
│   │   ├── symptoms/      ← future
│   │   ├── medications/   ← future
│   │   ├── dashboard/     ← future
│   │   └── insights/      ← future
│   └── tests/
│       └── test_api.py
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── context/
    │   ├── hooks/
    │   ├── pages/
    │   ├── types/
    │   └── utils/
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

*Last updated: Reconciliation prompts written. Tech spec incorporated.
Run Reconciliation Prompts 1-4 in order before any other work.*