# LiftCycle — Technical Specification v0.1

**This document is the authoritative reference for the implementing agent.**
Read `PRD.md` and `USER_STORIES.md` first for product context.

---

## 1. Stack & Tooling

| Layer | Choice | Notes |
|---|---|---|
| Language (backend) | Python 3.12 | |
| Framework (backend) | FastAPI | |
| ORM | SQLModel | Wraps SQLAlchemy + Pydantic |
| Database | PostgreSQL | |
| Migrations | Alembic | Exercise seed data lives here too |
| Auth | JWT via `python-jose`, passwords via `passlib[bcrypt]` | |
| Dependency manager | `uv` | Always prefix commands with `uv run` |
| Tests (backend) | pytest + httpx (async) | |
| Language (frontend) | TypeScript | |
| Framework (frontend) | React 18 | |
| Bundler | Vite | |
| Routing | React Router v6 | |
| HTTP client | Axios | All calls go through `src/api/` — never use `fetch()` directly |
| Date handling | date-fns | Never use `new Date()` directly for display |
| Styling | Plain CSS Modules per component | No CSS framework |
| Hosting | Railway | Free tier; PostgreSQL add-on included |

---

## 2. Auth Token Strategy

**Chosen approach: HttpOnly cookies.**

Reason: this app stores sensitive menstrual and health data. Storing tokens in
localStorage exposes them to any JavaScript running on the page (XSS risk).
HttpOnly cookies are inaccessible to JavaScript — the browser sends them
automatically with every request and they cannot be read or stolen via script.

Implementation details:
- On login/register, the backend sets two HttpOnly cookies: `access_token`
  (15 min expiry) and `refresh_token` (30 day expiry).
- The frontend Axios instance sends requests `withCredentials: true`.
- On a 401 response, the Axios interceptor calls `/auth/refresh` automatically,
  then retries the original request.
- On logout, the backend clears both cookies by setting them with past expiry.
- CORS must be configured with `allow_credentials=True` and an explicit
  `allow_origins` list (not `*`).

---

## 3. Project Structure

```
liftcycle/
├── backend/
│   ├── alembic/
│   │   └── versions/
│   │       └── 001_seed_exercises.py   # Exercise preset list seed
│   ├── app/
│   │   ├── main.py                     # FastAPI app factory, router registration
│   │   ├── config.py                   # Settings via pydantic-settings (.env)
│   │   ├── database.py                 # Engine, session dependency
│   │   ├── auth/
│   │   │   ├── router.py               # /auth/* endpoints
│   │   │   ├── service.py              # Business logic: tokens, hashing
│   │   │   ├── schemas.py              # Pydantic I/O models
│   │   │   └── dependencies.py         # get_current_user dependency
│   │   ├── cycles/
│   │   │   ├── router.py
│   │   │   ├── service.py              # CRUD + phase inference
│   │   │   ├── models.py               # SQLModel table models
│   │   │   └── schemas.py
│   │   ├── workouts/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── exercises/
│   │   │   ├── router.py               # /exercises/presets (read-only list)
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── symptoms/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── medications/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── users/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── insights/
│   │   │   ├── router.py
│   │   │   └── service.py              # Aggregation queries only, no models
│   │   └── dashboard/
│   │       ├── router.py
│   │       └── service.py              # Assembles day-by-day month data
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_*.py
│   ├── alembic.ini
│   └── pyproject.toml
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   ├── client.ts               # Axios instance, interceptors, cookie config
    │   │   ├── auth.ts
    │   │   ├── cycles.ts
    │   │   ├── workouts.ts
    │   │   ├── exercises.ts
    │   │   ├── symptoms.ts
    │   │   ├── medications.ts
    │   │   ├── insights.ts
    │   │   ├── dashboard.ts
    │   │   └── users.ts
    │   ├── components/
    │   │   └── [ComponentName]/
    │   │       ├── ComponentName.tsx
    │   │       └── ComponentName.module.css
    │   ├── pages/
    │   │   ├── Dashboard/
    │   │   ├── CycleLog/
    │   │   ├── WorkoutLog/
    │   │   ├── WorkoutHistory/
    │   │   ├── Insights/
    │   │   ├── Settings/
    │   │   ├── Login/
    │   │   └── Register/
    │   ├── hooks/                      # useAuth, useCycles, useWorkouts, etc.
    │   ├── context/                    # AuthContext
    │   ├── types/                      # Interfaces mirroring backend schemas
    │   ├── utils/
    │   │   ├── phaseInference.ts       # Client-side phase calculation (mirrors backend)
    │   │   └── unitConversion.ts       # kg ↔ lbs helpers
    │   ├── App.tsx
    │   └── main.tsx
    ├── index.html
    ├── vite.config.ts
    └── tsconfig.json
```

---

## 4. Database Schema

All tables include `id` (UUID, PK), `created_at`, and `updated_at` unless noted.

### users
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| email | VARCHAR(255) | Unique, indexed |
| hashed_password | VARCHAR | bcrypt, cost ≥12 |
| unit_preference | ENUM('kg','lbs') | Default 'kg' |
| cycle_length_override | INTEGER | Nullable; range 21–45; ignored once 3 cycles logged |
| last_period_start | DATE | Set during onboarding |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### cycles
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users, cascade delete |
| start_date | DATE | |
| end_date | DATE | Nullable |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### symptoms
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users, cascade delete |
| date | DATE | |
| symptom | ENUM | See values below |
| created_at | TIMESTAMP | |

Unique constraint: `(user_id, date, symptom)`

**Symptom enum:** `cramps`, `bloating`, `fatigue`, `low_mood`, `spotting`,
`headache`, `high_energy`, `other`

### medications
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users, cascade delete |
| date | DATE | |
| name | VARCHAR(255) | Free text |
| dosage_note | VARCHAR(255) | Nullable, free text |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### workouts
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users, cascade delete |
| date | DATE | |
| type | ENUM | See values below |
| duration_minutes | INTEGER | >0 |
| rpe | INTEGER | Nullable; 1–10 |
| notes | TEXT | Nullable |
| is_planned | BOOLEAN | Default false; planned future workouts |
| is_template | BOOLEAN | Default false; saved templates |
| template_name | VARCHAR(255) | Nullable; only set when is_template=true |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**Workout type enum:** `strength`, `cardio`, `hiit`, `yoga`, `sport`,
`walk_hike`, `other`

### workout_exercises
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| workout_id | UUID | FK → workouts, cascade delete |
| exercise_preset_id | UUID | FK → exercise_presets, nullable |
| custom_name | VARCHAR(255) | Nullable; used when exercise is not from preset list |
| sets | INTEGER | Nullable |
| reps | INTEGER | Nullable |
| weight_kg | DECIMAL(6,2) | Nullable; always stored in kg |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

Constraint: either `exercise_preset_id` OR `custom_name` must be set, not both null.

### exercise_presets
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(255) | Unique |
| category | VARCHAR(100) | e.g. "Push", "Pull", "Legs", "Core", "Cardio" |
| created_at | TIMESTAMP | |

Populated via Alembic seed migration. Read-only at runtime.
The seed file should include at minimum 60–80 common gym exercises across all
categories. The implementing agent should populate this list.

---

## 5. Phase Inference Logic

Lives in `backend/app/cycles/service.py` and is mirrored in
`frontend/src/utils/phaseInference.ts`. The calendar renders phases client-side
without a per-day round trip.

**Research note:** The luteal phase is physiologically consistent at ~14 days
across most people. All cycle length variability occurs in the follicular phase.
This is incorporated into the algorithm below.

```
Given: target_date, user's cycle entries [], user settings

1. Find the most recent cycle start_date ≤ target_date.
   If none exists → return phase: UNKNOWN

2. Determine cycle_length:
   - If user has ≥3 complete cycles logged:
       cycle_length = rolling average of last 3 cycle lengths
   - Else if cycle_length_override is set:
       cycle_length = cycle_length_override
   - Else:
       cycle_length = 28

3. days_into_cycle = target_date − cycle_start_date  (0-indexed)

4. Determine menstrual_end_offset:
   - If cycle has an end_date: menstrual_end_offset = end_date − start_date
   - Else: menstrual_end_offset = 4  (5-day default, 0-indexed)

5. estimated_ovulation_day = cycle_length − 14  (luteal phase is fixed at 14 days)

6. Phase assignment:
   - days_into_cycle ≤ menstrual_end_offset           → MENSTRUAL
   - days_into_cycle < estimated_ovulation_day − 1    → FOLLICULAR
   - days_into_cycle in [ovulation_day−1, ovulation_day] → OVULATORY
   - days_into_cycle > estimated_ovulation_day         → LUTEAL

7. Missed period warning (US-010):
   If (today − last_cycle_start) > (cycle_length × 1.5) → trigger warning
```

---

## 6. API Endpoints

Base path: `/api/v1`
All endpoints except `/auth/register`, `/auth/login`, `/auth/forgot-password`,
and `/auth/reset-password` require a valid session cookie.

### Auth
| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Create user, set session cookies |
| POST | `/auth/login` | Verify credentials, set session cookies |
| POST | `/auth/refresh` | Refresh access token cookie |
| POST | `/auth/logout` | Clear session cookies |
| POST | `/auth/forgot-password` | Send reset email |
| POST | `/auth/reset-password` | Consume reset token, set new password |

### Users
| Method | Path | Description |
|---|---|---|
| GET | `/users/me` | Get current user profile + settings |
| PATCH | `/users/me` | Update email, password, unit pref, cycle length override |
| DELETE | `/users/me` | Hard delete account + all data (requires password in body) |
| GET | `/users/me/export` | Download full data export as JSON |

### Cycles
| Method | Path | Description |
|---|---|---|
| GET | `/cycles` | List all cycles, newest first |
| POST | `/cycles` | Create a new cycle entry |
| PATCH | `/cycles/{id}` | Update start/end date |
| DELETE | `/cycles/{id}` | Delete a cycle entry |

### Symptoms
| Method | Path | Description |
|---|---|---|
| GET | `/symptoms` | List symptoms; filter by `?date=` or `?from=&to=` |
| POST | `/symptoms` | Log a symptom for a date |
| DELETE | `/symptoms/{id}` | Remove a symptom entry |

### Medications
| Method | Path | Description |
|---|---|---|
| GET | `/medications` | List medications; filter by `?date=` or `?from=&to=` |
| POST | `/medications` | Log a medication entry |
| PATCH | `/medications/{id}` | Edit name or dosage note |
| DELETE | `/medications/{id}` | Remove a medication entry |

### Workouts
| Method | Path | Description |
|---|---|---|
| GET | `/workouts` | List workouts; supports `?from=&to=`, `?type=`, `?is_planned=`, `?is_template=`, pagination |
| POST | `/workouts` | Log or plan a workout |
| GET | `/workouts/{id}` | Get single workout with exercises |
| PATCH | `/workouts/{id}` | Update workout fields |
| DELETE | `/workouts/{id}` | Delete workout (cascades exercises) |
| POST | `/workouts/{id}/exercises` | Add exercise to workout |
| PATCH | `/workouts/exercises/{id}` | Update an exercise |
| DELETE | `/workouts/exercises/{id}` | Delete an exercise |
| POST | `/workouts/{id}/save-as-template` | Save workout as a named template |

### Exercises
| Method | Path | Description |
|---|---|---|
| GET | `/exercises/presets` | Return full preset list (for search/autocomplete) |
| GET | `/exercises/presets/{id}/last-logged` | Return last logged sets/reps/weight for this exercise for current user |

### Dashboard
| Method | Path | Description |
|---|---|---|
| GET | `/dashboard/month?year={y}&month={m}` | Day-by-day data: phase, workout summary, symptoms, medications |

### Insights
| Method | Path | Description |
|---|---|---|
| GET | `/insights/summary` | Frequency + avg RPE per phase, streak, total workouts |
| GET | `/insights/exercise/{name}` | Exercise progression over time with phase labels |

---

## 7. Frontend Patterns

- **API layer:** every call is a typed function in `src/api/`. The Axios instance
  in `client.ts` is configured with `withCredentials: true` and an interceptor
  that handles 401 → silent refresh → retry.
- **Auth state:** managed in `AuthContext`. Protected routes use a wrapper
  component that redirects to `/login` if unauthenticated.
- **Types:** all response shapes are typed in `src/types/`, mirroring backend
  Pydantic schemas. Never use `any`.
- **Date handling:** use `date-fns` for all arithmetic and formatting.
  Never call `new Date()` for display purposes.
- **CSS:** one `.module.css` per component. Class names in camelCase.
  Global styles only in `src/index.css` (resets + CSS custom properties for
  the phase colour palette and design tokens).
- **Phase colours:** defined as CSS custom properties in `index.css` so they
  are consistent across every component that shows phase data.
- **Error handling:** form validation errors shown inline. Non-form errors
  (network failures, server errors) shown as a toast notification.
- **Weight display:** always read `unit_preference` from user context before
  rendering any weight value. Conversion helpers live in `utils/unitConversion.ts`.

---

## 8. Environment Variables

### Backend (`.env`)
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

### Frontend (`.env`)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Railway deployment notes
- Set `ENVIRONMENT=production` on Railway.
- Set `FRONTEND_URL` to your deployed frontend URL.
- `DATABASE_URL` is provided automatically by the Railway PostgreSQL add-on.
- For the frontend, set `VITE_API_BASE_URL` to your deployed backend URL.
- Cookies require `Secure=True` and `SameSite=None` in production when
  frontend and backend are on different subdomains — the backend should
  set these flags automatically when `ENVIRONMENT=production`.

---

## 9. Testing Guidelines

- Every route must have at least one happy-path test and one error-case test.
- Use pytest fixtures for: test database session, authenticated test client,
  and factory functions for creating test users, cycles, and workouts.
- Tests must not share state — each test uses a fresh DB transaction rolled
  back after the test.
- The exercise preset seed data must be applied in the test database.
- Backend command: `uv run pytest`

---

## 10. Running Locally

```bash
# Backend
cd backend
uv run alembic upgrade head        # runs migrations + seeds exercise presets
uv run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev                        # runs on http://localhost:5173
```

---

## 11. Key Constraints Summary

1. Always use `uv run` for all Python commands.
2. Never call `fetch()` in the frontend — all HTTP via `src/api/`.
3. Weights stored internally in kg always; convert for display only.
4. Phase inference runs both server-side and client-side (see Section 5).
5. No CSS framework — plain CSS Modules only.
6. Cookies require `withCredentials: true` on Axios and proper CORS config.
7. `is_planned=true` workouts are excluded from all insight calculations.
8. `is_template=true` workouts are excluded from history and insight calculations.