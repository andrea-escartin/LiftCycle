# Coding Discipline

Principles governing how Claude approaches implementation work.
These override default tendencies toward verbosity, speculation,
and over-engineering.

## 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan before starting:
1. [Step] → verify: [check]
2. [Step] → verify: [check]

---

# Project: LiftCycle

A multi-user health tracking web app. Users register, log in, and track
their menstrual cycle alongside their workouts to understand how hormonal
phases affect training performance.

## Product documents (read before implementing any feature)
- 01_pdr.md — product goals, personas, design principles, non-goals
- 02_user_stories.md — acceptance criteria per feature, priority labels (P0/P1/P2)
- 03_tech_spec.md — authoritative technical reference

These three files live in the project root. Always consult them.
P0 stories are must-have for v1. P1 are strong v1 goals. P2 are deferred.

---

## Stack

### Backend
- Python 3.12, FastAPI, SQLModel (ORM), PostgreSQL
- Alembic for migrations and exercise preset seeding
- JWT authentication via python-jose (HttpOnly cookies — NOT localStorage)
- passlib[bcrypt] for password hashing (cost factor ≥ 12)
- pydantic-settings for config via .env
- uv for dependency management — ALWAYS use `uv run` prefix
- pytest + httpx for tests

### Frontend
- React 18, TypeScript, Vite
- React Router v6 for navigation
- Axios for all HTTP calls — NEVER use fetch() directly
- date-fns for all date arithmetic and formatting — NEVER use new Date() for display
- Plain CSS Modules per component — NO CSS framework
- AuthContext for auth state management

---

## Architecture

- Monorepo: backend/ and frontend/ in one repo
- Backend is a REST API. Base path: /api/v1
- Frontend is a separate SPA that calls the API
- Each domain has its own folder: router.py, service.py, models.py, schemas.py
- Auth uses HttpOnly cookies (access_token 15min, refresh_token 30 days)
- Axios instance configured with withCredentials: true
- 401 responses trigger silent token refresh then retry via Axios interceptor

---

## Backend project layout

```
backend/app/
├── main.py              — FastAPI app factory, router registration, CORS
├── config.py            — pydantic-settings, loads .env
├── database.py          — engine, get_session dependency
├── auth/
│   ├── router.py        — /auth/* endpoints
│   ├── service.py       — token creation, hashing logic
│   ├── schemas.py       — Pydantic I/O models
│   └── dependencies.py  — get_current_user dependency
├── users/
│   ├── router.py        — /users/me endpoints
│   ├── service.py
│   ├── models.py        — User SQLModel table
│   └── schemas.py
├── cycles/
│   ├── router.py        — /cycles endpoints
│   ├── service.py       — CRUD + phase inference
│   ├── models.py        — Cycle SQLModel table
│   └── schemas.py
├── workouts/
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── exercises/
│   ├── router.py        — /exercises/presets (read-only)
│   ├── models.py
│   └── schemas.py
├── symptoms/
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── medications/
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── dashboard/
│   ├── router.py        — /dashboard/month
│   └── service.py
└── insights/
    ├── router.py        — /insights/*
    └── service.py
```

## Frontend project layout

```
frontend/src/
├── api/
│   ├── client.ts        — Axios instance, withCredentials, 401 interceptor
│   ├── auth.ts
│   ├── cycles.ts
│   ├── workouts.ts
│   ├── exercises.ts
│   ├── symptoms.ts
│   ├── medications.ts
│   ├── insights.ts
│   ├── dashboard.ts
│   └── users.ts
├── components/
│   └── [ComponentName]/
│       ├── ComponentName.tsx
│       └── ComponentName.module.css
├── pages/
│   ├── Dashboard/
│   ├── CycleLog/
│   ├── WorkoutLog/
│   ├── WorkoutHistory/
│   ├── Insights/
│   ├── Settings/
│   ├── Login/
│   └── Register/
├── hooks/               — useAuth, useCycles, useWorkouts, etc.
├── context/             — AuthContext
├── types/               — interfaces mirroring backend schemas
├── utils/
│   ├── phaseInference.ts   — client-side phase calculation
│   └── unitConversion.ts   — kg ↔ lbs helpers
├── App.tsx
└── main.tsx
```

---

## Database rules

- All primary keys are UUIDs (not integers)
- All tables have created_at and updated_at
- All FK relationships use cascade delete
- Weights always stored in kg internally; convert for display only
- is_planned=true workouts excluded from all insight calculations
- is_template=true workouts excluded from history and insight calculations

---

## Backend conventions

- Type hints on all functions and return values
- SQLModel models for DB tables; separate Pydantic schemas in schemas.py
- Business logic in service.py, never in router handlers
- Every endpoint authenticated except /auth/register, /auth/login,
  /auth/forgot-password, /auth/reset-password
- Return 404 for not found OR wrong user (never 403 — avoids leaking existence)
- Consistent error shape: { detail: string }
- Config loaded via pydantic-settings (config.py), not os.getenv() directly

## Frontend conventions

- All API calls via src/api/ functions — never fetch() directly
- All types defined in src/types/ — never use `any`
- All dates via date-fns — never new Date() for display
- One .module.css per component, class names in camelCase
- Phase colours as CSS custom properties in index.css
- Form errors shown inline; network/server errors as toast notifications
- Always read unit_preference from user context before rendering weight values

---

## Phase inference logic (implement exactly — both backend and frontend)

```
Given: target_date, user's cycle entries [], user settings

1. Find most recent cycle start_date <= target_date.
   If none → return phase: UNKNOWN

2. Determine cycle_length:
   - If user has >= 3 complete cycles: rolling average of last 3
   - Else if cycle_length_override set: use that
   - Else: 28

3. days_into_cycle = target_date − cycle_start_date (0-indexed)

4. menstrual_end_offset:
   - If cycle has end_date: end_date − start_date
   - Else: 4 (5-day default, 0-indexed)

5. estimated_ovulation_day = cycle_length − 14

6. Phase assignment:
   - days_into_cycle <= menstrual_end_offset       → MENSTRUAL
   - days_into_cycle < estimated_ovulation_day − 1 → FOLLICULAR
   - days_into_cycle in [ovulation_day−1, ovulation_day] → OVULATORY
   - days_into_cycle > estimated_ovulation_day      → LUTEAL

7. Missed period warning:
   If (today − last_cycle_start) > (cycle_length × 1.5) → warn user
```

---

## API base path

All endpoints prefixed with /api/v1

---

## Environment variables

### Backend (.env)
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/liftcycle
SECRET_KEY=<random 64-char hex>
REFRESH_SECRET_KEY=<random 64-char hex>
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
FRONTEND_URL=http://localhost:5173
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=noreply@liftcycle.app
ENVIRONMENT=development
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## Commands

### Backend (run from backend/)
- Run server:    uv run uvicorn app.main:app --reload --port 8000
- Run tests:     uv run pytest -v
- Run migration: uv run alembic upgrade head
- Add dep:       uv add <package>

### Frontend (run from frontend/)
- Dev server:    npm run dev   (runs on http://localhost:5173)
- Build:         npm run build
- Add dep:       npm install <package>

---

## What NOT to do

- Do not use integer primary keys — always UUID
- Do not store tokens in localStorage — HttpOnly cookies only
- Do not call fetch() in the frontend — always src/api/ functions
- Do not put business logic in route handlers — always service.py
- Do not store passwords in plaintext — always bcrypt hash
- Do not use new Date() for display — always date-fns
- Do not use any CSS framework — CSS Modules only
- Do not use `any` in TypeScript — always define types in src/types/
- Do not commit .env files
- Do not add features not explicitly requested
- Do not modify files outside the scope of the current task
- Do not include is_planned or is_template workouts in insights