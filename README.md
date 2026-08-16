# CSA course site

Two static pages, no server needed — just open `index.html` in a browser.
Live at https://ahs-cs-a.github.io/csa/

- **`index.html`** — "This Week" view. A clean table, one row per week, with the current week highlighted and a semester toggle (S1/S2). The front door for students: what's happening now, what's due, what to read.
- **`topics.html`** — "By Topic" view. Every unit (Concept #1–#9, AP Review, Final Moments, Course Information) as a collapsible section with its Slides / Resources / Homework / Due / CS-in-the-News items. Good for review or catching up.
- **`content/`** — **this is what you edit.** Plain markdown: one file per week, plus a concepts list and a course-info page. See `content/README.md`.
- **`data.js`** — generated from `content/` by `source/build_from_markdown.py`. Don't hand-edit this — it gets overwritten every time you publish.
- **`styles.css`** / **`script.js`** — shared look and behavior (light/dark aware, collapsible sections, current-week logic).

## Editing content

Edit the markdown in `content/`, then from the repo root:

```
./publish.sh "what you changed"
```

That rebuilds `data.js` from `content/` and pushes it live. See `content/README.md` for the file format (it's short — one frontmatter block plus five optional bullet-list sections per week).

## Updating "what week is it"

Set `current: true` in the frontmatter of the week file that's now current (and remove it from whichever week had it before), then publish:

```
./publish.sh "advance to week 9"
```

Exactly one week file should have `current: true` at a time — `build_from_markdown.py` errors out if it finds more than one. Everything on the site (row highlighting, the now-card, done/upcoming greying) follows from that one flag.

## Where this content came from

The starting content was migrated from a Canvas export (`~/Desktop/csa-2025-26-export`). `source/canvas-migration/` has that one-time script and the raw parse, kept for provenance — it's not part of the ongoing workflow and shouldn't be re-run (it would overwrite anything you've since edited in `content/`).

Some week/semester assignments were reconstructed from Canvas's own (inconsistent) week labels — worth double-checking against your real pacing guide. About a dozen items with no confirmed week in Canvas (a few unit tests, the Data Projects, the AP Test) were **left out** rather than guessed at; add them to the relevant week file once you know the real date.

## Not done yet

The other three exported courses aren't in here — this was built CSA-first. Once this content model feels right, `source/build_from_markdown.py` and the `content/` shape can be reused as-is for each of the others (new repo, same two scripts, new `content/`).
