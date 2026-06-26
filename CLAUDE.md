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

# Project: Period & Workout Tracker

A multi-user health tracking web app. Users log in and track their
own cycle data, workouts, body metrics, and nutrition.

## Stack

### Backend
- Python 3.12, FastAPI, SQLModel (ORM), PostgreSQL
- Alembic for database migrations
- JWT authentication (python-jose + passlib/bcrypt)
- uv for dependency management — always use `uv run` prefix
- pytest + httpx for tests

### Frontend
- React 18, TypeScript, Vite
- React Router v6 for navigation
- Axios for API calls (all calls go through src/api/, never fetch() directly)
- No CSS framework yet — plain CSS modules per component

## Architecture

- Monorepo: backend/ and frontend/ in one repo
- Backend is a REST API — all data via JSON endpoints
- Frontend is a separate SPA that calls the API
- Each domain (cycles, workouts, metrics, nutrition) has its own router

## Project layout

### Backend (backend/)
- app/main.py          — FastAPI app, lifespan, router wiring
- app/models.py        — SQLModel table models + Pydantic schemas
- app/db.py            — engine, session dependency
- app/auth.py          — JWT creation and validation
- app/services.py      — shared/cross-domain business logic
- app/routers/auth.py  — login and register endpoints
- app/routers/cycles.py — cycle tracking endpoints
- tests/               — pytest tests

### Frontend (frontend/)
- src/pages/        — one folder per screen
- src/components/   — reusable UI pieces
- src/api/          — one file per domain (auth.ts, cycles.ts)
- src/hooks/        — custom React hooks
- src/main.tsx      — app entry point, router setup

## Conventions

- Type hints on all functions and return values
- SQLModel models for DB tables; separate Pydantic schemas for
  request/response bodies — no raw dicts in endpoints
- Business logic in services, not in route handlers
- Every endpoint needs authentication except /auth/register and /auth/login
- Return 404 when a resource is not found
- Consistent error shape: { detail: string }
- Tests use in-memory SQLite (not the real DB)

## Commands

### Backend
- Install dep:   uv add <package>         (run from backend/)
- Run server:    uv run uvicorn app.main:app --reload --port 3000
- Run tests:     uv run pytest -v
- Migrations:    uv run alembic upgrade head

### Frontend
- Install dep:   npm install <package>    (run from frontend/)
- Dev server:    npm run dev
- Build:         npm run build

## Current status

Building cycle tracking domain first (auth + cycles). Other
domains (workouts, metrics, nutrition) come later.

## What NOT to do

- Do not put business logic in route handlers
- Do not store plain text passwords — always hash with passlib
- Do not commit .env or any secrets
- Do not add features not explicitly asked for
- Do not modify files outside the scope of the current task