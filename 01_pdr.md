**Version:** 1.0
**Platform:** Web (mobile-web responsive; native mobile deferred to v2)
**Audience:** Anyone with a menstrual cycle who exercises

---

## 1. Problem Statement

The menstrual cycle affects the hormones and impacts energy levels, strenght and motivation. Most of the available workout tracking tools ignore this fact. LifCycle will allow people with menstrual cycles who worksout regularly to track their period and log their workouts in one place, so users can see trends reflected based on their cycles and not only as a whole.

---

## 2. Goals

* Users can track their menstrual cycle (start, end, duration, symptops) easily
* Users can log workouts (type, reps, sets, weithgts) easily and also retroactively. Repeat logging should be low-friction — returning users shouldn't have to re-enter the same information from scratch
* Users can select a workout type and see tendencies over time, highlighting the different menstrual phases. Surface basic insights: e.g. "You tend to lift heavier in your follicular phase."
* Users can have template workouts so they don't have to input manually the information each time
* The tool should have an option to estimate duration of the cycle and the menstruation based on previous data. It should predict future periods and cycle phases and display it in a calendar
* Be opinionated but not prescriptive — the app shows patterns; it does not shame rest days or missed entries.
* Users have full control over their data and can export or delete it at any time

---

## 3. Non-Goals (v1)

- No AI-generated workout plans or meal plans.
- No social/sharing features.
- No wearable or third-party app integrations (Apple Health, Garmin, etc.).
- No native mobile app.
- No paid tiers or monetisation logic.
- No push notifications (web notifications only if time permits, not required).
- No nutritional - information logging
- No body measures logging
- Detect improvement and offer to update template

---

## 4. User Personas
1. Person that exercises regularly They exercise 2+ times per week, in different modalities, e.g. gym, pool, classes. Notices that the motivation and strenght does not increase linearly and oscillates in a month. Needs an easy tool to keep track of workouts in relationship with their cycle
Name: Andrea
Age: 30
Office job, works out regularly and wants to understand how their performance is affected by their cycle
Will log off and never come back if logging workouts becomes too tedious

1. Person that does not exercise regularly. They are mainly interested in the period tracking functionallity. They use the workout tracker to add context to their routines, e.g. bad weeks in which they do not workout are explained by their cycle
Name: Carlota
Age: 30
Office job, starting to build a work out routine/ only into casual workouts.
Wants to have accurate period tracking and prediction, and understand its impact on their motivation
Will log off and never come back if logging workouts becomes too tedious, period tracker is not accurate or the non workout days/weeks/periods are punished

---

## 5. Goals

### 5.1 Authentication
- Email + password registration and login (Gmail login deferred to v2).
- Password reset via email.
- Users set their last period date and average cycle duration during onboarding.

### 5.2 Cycle Tracking
- Log a period start date and optionally an end date.
- Optionally log symptoms per day (cramps, bloating, fatigue, mood, spotting, headache, etc).
- Optionally log medication per day (birth control, painkillers, etc).
- The app automatically determines the user's current cycle phase based on logged data,
  and refines its predictions as more cycles are recorded. Phases: Menstrual, Follicular,
  Ovulatory, Luteal.
- Users can view and edit past cycle entries.

### 5.3 Workout Logging
- Log a workout with: date, type (strength, cardio, HIIT, yoga, sport, walk/hike, other),
  duration, perceived effort (RPE 1–10), and free-text notes.
- For strength workouts, log individual exercises: name, sets, reps, and weight
  (kg or lbs based on user preference).
- Users can save workouts as reusable templates (v1).
- Users can plan workouts for future dates; planned workouts are excluded from insights
  until the date has passed.
- Users can view, edit, and delete past workout entries.
- Recurring routines (assigning templates to days of the week) deferred to v2.

### 5.4 Dashboard
- Monthly calendar showing workouts (icon + colour by type) and cycle phases
  (colour-coded, with period days more strongly highlighted).
- Clicking any day opens a detail view for logging or editing workouts, symptoms,
  and medication for that day.
- A "today" card showing current cycle phase, day number within the phase,
  and today's workout if logged.
- A list of the last 5 workouts logged during the current cycle phase.
- A general recent workouts list (last 7 days).

### 5.5 Insights
- Only unlocked after 4 weeks of combined cycle and workout data.
- Average workout frequency per cycle phase.
- Average RPE per cycle phase.
- Longest workout streak and total workouts logged.
- Per-exercise view: select any exercise and see performance over time,
  colour-coded by cycle phase.
- All insights filterable by cycle phase.

### 5.6 Profile & Settings
- Unit preference: kg or lbs.
- Manual cycle length override (used until enough cycles are logged to calculate
  an automatic average).
- Edit email and password.
- Account deletion with full data wipe.

---

### 6. Design Principles

- **Low friction above all.** Logging a workout or a period start should never take more than 3 actions. If it feels tedious, users won't come back.
- **Neutral, non-judgmental tone.** Never use language implying the user should have exercised more or less, or that their symptoms are unusual.  Rest days and low-effort weeks are valid data points.
- **Data belongs to the user.** All data can be exported at any time as JSON. The account and all associated data can be fully and permanently deleted on request.
- **Accessible by design.** The app targets compliance with the European Accessibility Act (EAA / WCAG 2.2). All interactive elements must be keyboard-navigable and compatible with screen readers. Colour is never the only means of conveying information.
- **Cycle-first.** Cycle data is never a secondary feature. The current cycle phase must be visible whenever a user is logging or reviewing a workout, so that exercise data always exists in hormonal context.

---
## 7. Success Metrics (post-launch)

- User logs at least 1 workout AND 1 cycle entry within their first week → retained user.
- Users who have logged ≥2 full cycles return to the app at least 2x per week.
- Insights page viewed by >50% of eligible users (those with 4+ weeks of data).
