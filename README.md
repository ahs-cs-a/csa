# CSA course site — mockup

Two static pages, no build step, no server needed — just open `index.html` in a browser.

- **`index.html`** — "This Week" view. A clean table, one row per week, with the current week highlighted and a semester toggle (S1/S2). Meant to be the front door for students: what's happening now, what's due, what to read.
- **`topics.html`** — "By Topic" view. Every unit (Concept #1–#9, AP Review, Final Moments) as a collapsible section with its Slides / Resources / Homework / Assessments / CS-in-the-News items — mirrors your Canvas module structure exactly. Good for review or catching up.
- **`data.js`** — all course content, generated from your Canvas export (`~/Desktop/csa-2025-26-export`). This is the single source of truth both pages read from.
- **`styles.css`** / **`script.js`** — shared look and behavior (light/dark aware, collapsible sections, current-week logic).

## What's real vs. reconstructed

Every item title, section grouping, and external link (Slides, GitHub Classroom, Google Docs) came straight from your Canvas `module_meta.xml` — nothing was invented. 172 items, 66 live links.

What I had to **reconstruct**, because Canvas's own week labels weren't fully consistent (some said "S1"/"S2", most just said "Week N," a few said "Week 9/10"):

- The **chronological order of units** — inferred from Canvas's module list order (which runs newest-first, so I reversed it): Classes & Objects → Strings → Conditionals → Iteration → ArrayLists → Arrays → 2D Arrays → Recursion → AP Review → Data & Regression → Final Moments.
- **Which semester each "Week N" belongs to**, for modules that didn't say S1/S2 explicitly.
- **Concept 5 (ArrayLists) spans the semester boundary** — S1 Week 15 through S2 Week 5 — since that's the one unit Canvas tagged explicitly and it lines up with the rest.

**Double-check the week-by-week assignments against your actual pacing guide before handing this to students** — the reconstruction is my best read of the Canvas structure, not a copy of a verified calendar. They live in `source/build_weeks.py`, in the `S1` and `S2` lists near the top (each row is `(week, [concept ids], focus blurb)`).

## To update

- **"What week is it?"** — edit the `CURRENT` constant at the very top of `script.js` (e.g. `{ semester: "s2", week: 9 }`). Everything else (highlighting, the "This Week" card, done/upcoming greying) follows from that one value. No rebuild needed for this one.
- **Fix a week's unit/focus text, or which items show up** — edit `source/build_weeks.py` (the `S1`/`S2` lists), then from `source/` run:
  ```
  python3 build_data.py && python3 build_weeks.py && python3 build_data_js.py
  ```
  That re-parses `modules_raw.tsv` (the raw Canvas export) and rewrites `../data.js`.
- **Add/edit an individual item's title or link** — you can also hand-edit `data.js` directly (it's just two JS arrays, `CONCEPTS` and `WEEKS`); just know a future rebuild from `source/` will overwrite those changes unless you also update `modules_raw.tsv` or the build scripts.
- **Real dates instead of "Week N"** — not wired up yet. Easiest path: add a start-date to each semester and compute date ranges in `script.js`.

## Not done yet (this is CSA only, per our conversation)

The other three exported courses aren't in here. Once this template feels right, the same `build_data.py`-style parsing + `data.js` shape can be reused for each.
