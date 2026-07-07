# LiftCycle — User Stories & Acceptance Criteria (DRAFT v0.2)

**Convention:**
- Priority: `P0` = must-have for v1 launch, `P1` = strong v1 goal, `P2` = defer to v2
- Each story has a unique ID (`US-XXX`) for reference in tasks and PRs.

---

## Authentication

### US-001 — Register with email and password `P0`
**As a** new user,
**I want to** create an account with my email and a password,
**So that** my data is private and persists between sessions.

**Acceptance Criteria:**
- Email must be valid format and not already registered.
- Password must be at least 8 characters.
- During registration, the user is required to enter their last period start date and estimated cycle length.
- After 3 full cycles are logged, the app automatically switches from the manual cycle length to a rolling average. See phase inference logic in Tech Spec for details.
- On success: user is logged in and redirected to the dashboard.
- On failure: a specific, readable error message is shown (e.g. "Email already in use", "Password too short").
- Passwords are stored as hashes — never plaintext.

---

### US-002 — Log in `P0`
**As a** returning user,
**I want to** log in with my email and password,
**So that** I can access my data.

**Acceptance Criteria:**
- Invalid credentials show a generic "Incorrect email or password" message (no enumeration).
- Session persists across page refreshes.

---

### US-003 — Log out `P0`
**As a** logged-in user,
**I want to** log out,
**So that** my account is not accessible on shared devices.

**Acceptance Criteria:**
- Clears session.
- Redirects to login page.

---

### US-004 — Reset forgotten password `P1`
**As a** user who forgot their password,
**I want to** receive a reset link by email,
**So that** I can regain access to my account.

**Acceptance Criteria:**
- Submitting a registered email sends a time-limited reset link (expires in 1 hour).
- Submitting an unregistered email shows the same success message (prevents enumeration).
- Using the link lets the user set a new password; the link is then invalidated.

---

### US-005 — Log in with Google `P2`
**As a** user,
**I want to** log in with my Google account,
**So that** I don't have to manage a separate password.

**Acceptance Criteria:**
- Google OAuth login works as an alternative to email/password.
- On first Google login, user still completes the onboarding step (last period date + cycle length).

---

### US-006 — Import data from another period tracker `P2`
**As a** user switching from another app,
**I want to** import my historical cycle data,
**So that** I have a longer history from day one and predictions are more accurate immediately.

**Acceptance Criteria:**
- Supported import formats to be defined during v2 scoping (at minimum: Clue and Flo exports).
- Imported data is clearly flagged as "imported" in the cycle history view.
- In case of conflicts with manually entered data, the user is asked to resolve them.
- Import is optional and can be skipped.

---

## Cycle Tracking

### US-010 — Log a period start `P0`
**As a** user,
**I want to** mark today (or a past date) as the start of my period,
**So that** the app can track my cycle.

**Acceptance Criteria:**
- User can pick any date ≤ today.
- The calendar view immediately reflects the logged start.
- If the selected date is more than 1.5x the user's expected cycle length since the last logged period start, the app warns the user and asks them to confirm — to account for possible missed logging. The 1.5x threshold is calculated against: the rolling average if ≥3 cycles are logged, otherwise the manual override, otherwise the 28-day default.

---

### US-011 — Log a period end `P1`
**As a** user,
**I want to** mark when my period ended,
**So that** the app knows the duration of my menstrual phase accurately.

**Acceptance Criteria:**
- Period end date must be ≥ period start date and ≤ today.
- End date can be added retroactively.
- If no end date is logged, the app uses a 5-day default duration for phase calculations.

---

### US-012 — Log daily symptoms `P1`
**As a** user,
**I want to** log how I'm feeling on a given day,
**So that** I can look back and notice patterns.

**Acceptance Criteria:**
- Symptoms available: Cramps, Bloating, Fatigue, Low mood, Spotting, Headache, High energy, Other.
- Multiple symptoms can be selected for the same day.
- Symptoms can be logged for today or any past date.
- Symptoms can be edited or removed after logging.

---

### US-013 — Log daily medication `P1`
**As a** user,
**I want to** log medication I took on a given day (e.g. birth control, painkillers),
**So that** I can factor it in when reviewing my cycle and workout data.

**Acceptance Criteria:**
- Free-text medication name plus optional dosage note.
- Can be logged for today or any past date.
- Can be edited or deleted.

---

### US-014 — View current cycle phase `P0`
**As a** user,
**I want to** see what phase of my cycle I'm currently in,
**So that** I have hormonal context before logging or reviewing a workout.

**Acceptance Criteria:**
- Current phase is visible on the dashboard and on the workout logging screen.
- Includes phase name and a plain-language description.
- If no cycle data has been logged yet, prompts the user to log their last period.

---

### US-015 — View and edit cycle history `P1`
**As a** user,
**I want to** see a list of my past logged cycles,
**So that** I can review or correct my data.

**Acceptance Criteria:**
- List shows each cycle: start date, end date (or "ongoing"), and cycle length in days.
- Each entry can be edited or deleted.
- Deleting a cycle entry asks for confirmation.

---

## Workout Logging

### US-020 — Log a workout `P0`
**As a** user,
**I want to** record a workout I completed,
**So that** I can track my exercise history alongside my cycle.

**Acceptance Criteria:**
- Required fields: date (defaults to today), workout type, duration in minutes.
- Optional fields: RPE (1–10), free-text notes.
- Any date ≤ today is valid (retroactive logging supported).
- Current cycle phase is displayed on the logging screen.
- Workout is immediately visible on the calendar and recent workouts list.

---

### US-021 — Log exercises within a strength workout `P1`
**As a** user doing strength training,
**I want to** log individual exercises with sets, reps, and weight,
**So that** I can track progression over time.

**Acceptance Criteria:**
- Exercise name is selected from a searchable preset list of common gym exercises. If not found, user can add a custom exercise name.
- Fields per exercise: name, sets, reps, weight (respects unit preference).
- When an exercise name is selected and the user has logged it before, sets, reps, and weight pre-fill with values from the last time that exercise was logged.
- Multiple exercises can be added to one workout.
- Exercises can be added, edited, or removed at any time.
- Weight is stored internally in kg regardless of display preference.

---

### US-022 — Edit or delete a workout `P0`
**As a** user,
**I want to** correct or remove a workout I logged,
**So that** my history stays accurate.

**Acceptance Criteria:**
- All fields of a logged workout can be edited.
- Deleting asks for confirmation.
- Changes immediately update the calendar and insights.

---

### US-023 — Save a workout as a template `P1`
**As a** user with a regular training routine,
**I want to** save a workout as a template I can reuse,
**So that** I don't have to re-enter the same exercises every time.

**Acceptance Criteria:**
- Any logged workout can be saved as a named template.
- When logging a new workout, user can select a template to pre-fill the exercises.
- Pre-filled values can be edited before saving the new workout.
- Templates can be renamed, edited, and deleted.
- Templates do not appear in workout history or insights on their own.

---

### US-024 — Plan a future workout `P1`
**As a** user,
**I want to** schedule a workout for a future date,
**So that** I can plan my training week in advance.

**Acceptance Criteria:**
- Future workouts appear on the calendar as "planned" with a distinct visual treatment.
- Planned workouts are excluded from all insights calculations until the date has passed.
- When the date arrives, the planned workout appears as a prompt on the dashboard to confirm or edit it as completed.

---

### US-025 — View workout history `P1`
**As a** user,
**I want to** see a list of all my past workouts,
**So that** I can review my training history.

**Acceptance Criteria:**
- List is paginated, newest first.
- Each item shows: date, type, duration, RPE, and cycle phase for that day.
- Tapping an item opens the full detail view including exercises.
- Filterable by workout type.

---

## Dashboard

### US-030 — View monthly calendar `P0`
**As a** user,
**I want to** see a month view combining my cycle and workouts,
**So that** I can see my patterns at a glance.

**Acceptance Criteria:**
- Each day shows cycle phase (colour-coded background) and workout icon if logged.
- Period days are more strongly highlighted than other phases.
- Planned future workouts appear with a distinct visual treatment.
- Clicking a day opens a detail/logging view for that day.
- Navigation to previous and next months.
- Today is clearly highlighted.

---

### US-031 — View today's summary card `P0`
**As a** user visiting the dashboard,
**I want to** see a summary of where I am today,
**So that** I get immediate context without digging.

**Acceptance Criteria:**
- Shows current cycle phase and day number within phase.
- Shows today's logged workout or a prompt to log one.
- Shows any symptoms logged today.

---

### US-032 — View recent workouts in current phase `P1`
**As a** user,
**I want to** see my last 5 workouts from the same cycle phase I'm currently in,
**So that** I can compare today's performance to how I usually feel at this point in my cycle.

**Acceptance Criteria:**
- Displayed on the dashboard below the today card.
- Only shows workouts logged during the same phase in previous cycles.
- If fewer than 5 exist, shows however many are available.
- If none exist yet, the section is hidden.

---

## Insights

### US-040 — View workout frequency by cycle phase `P1`
**As a** user with at least 4 weeks of data,
**I want to** see how often I work out in each cycle phase,
**So that** I can understand my natural rhythms.

**Acceptance Criteria:**
- Chart showing average workouts per week broken down by phase.
- Only shown after 4 weeks of combined cycle and workout data.
- If insufficient data, shows a prompt explaining when it will unlock.

---

### US-041 — View average effort by cycle phase `P1`
**As a** user,
**I want to** see my average RPE per cycle phase,
**So that** I can see whether I push harder or easier at certain points in my cycle.

**Acceptance Criteria:**
- Only calculated from workouts with an RPE value logged.
- Phases with fewer than 3 data points show a "not enough data yet" indicator rather than a potentially misleading average.

---

### US-042 — View exercise progression `P1`
**As a** user,
**I want to** select an exercise and see my performance over time,
**So that** I can track progression and see how my cycle affects it.

**Acceptance Criteria:**
- User selects any exercise they have logged at least twice.
- Chart shows performance over time (weight, reps, or sets — user selects metric).
- Data points are colour-coded by cycle phase.
- Filterable by cycle phase.

---

## Profile & Settings

### US-050 — Set unit preference `P1`
**As a** user,
**I want to** choose between kg and lbs,
**So that** I can use the units I'm familiar with.

**Acceptance Criteria:**
- Default is kg.
- Changing the preference updates all displayed weight values immediately.
- Preference is saved to the user's account (not just local).

---

### US-051 — Set default cycle length `P1`
**As a** user who knows their cycle length,
**I want to** set it manually,
**So that** phase predictions are accurate from the start.

**Acceptance Criteria:**
- Accepts integers from 21 to 45 days.
- Once 3+ full cycles are logged, the app uses the calculated rolling average and the manual override is ignored, with an explanatory note shown to the user.

---

### US-052 — Edit email and password `P1`
**As a** user,
**I want to** update my email or password,
**So that** I can keep my account secure.

**Acceptance Criteria:**
- Changing email requires current password confirmation.
- Changing password requires current password confirmation.

---

### US-053 — Delete account `P1`
**As a** user,
**I want to** permanently delete my account and all my data,
**So that** I have full control over my personal health information.

**Acceptance Criteria:**
- Requires password confirmation before deletion.
- All user data is hard-deleted from the database.
- User is logged out and shown a confirmation screen.

---

### US-054 — Export data `P2`
**As a** user,
**I want to** download all my data as a JSON file,
**So that** I can keep a personal backup.

**Acceptance Criteria:**
- Single button in Settings.
- Export includes all cycle entries, workouts, exercises, symptoms, medication logs, and account metadata.
- File named `liftcycle-export-YYYY-MM-DD.json`.