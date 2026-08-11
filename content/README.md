# Editing course content

Everything the site shows comes from the plain-text files in this folder.
After editing anything here, run `./publish.sh "what you changed"` from the
repo root — that rebuilds `data.js` and pushes it live.

## `weeks/s1-w06.md` — one file per week

```markdown
---
semester: s1
week: 6
concepts: c2, c3
focus: Strings continue; conditionals (if/else, booleans) begin.
---

## Slides
- [Conditionals Week 6](https://docs.google.com/presentation/...)

## Resources
- [Code: s1-w6](https://classroom.github.com/a/...)

## Homework
- [HW #1: Strings Analysis](https://...)

## Due
- Quiz #1: String Analysis

## CS in the News
- LLMs: How do they Work?
```

- **`concepts:`** — the concept id(s) being taught that week (see `concepts.md`
  for the list). Comma-separated if more than one (common on transition
  weeks). This drives both the "Unit" column on the week page and which
  concept(s) this week's items show up under on the topics page.
- **`focus:`** — one line, shown on the week page and in the "This Week" card.
- Every `##` section is optional to fill in — leave the `<!-- ... -->`
  placeholder if there's nothing for that section this week. Don't rename or
  remove the section headers themselves; the build script only recognizes
  exactly these five: `Slides`, `Resources`, `Homework`, `Due`, `CS in the News`.
- Bullets are plain markdown: `- [Title](url)` for a link, or `- Title` with
  no link.

### Concept tags on shared/overlap weeks

Most weeks only have one concept, so bullets don't need any tag — an
untagged item just belongs to whatever's in `concepts:`. On a week with
**more than one** concept active (a transition week), you can mark which
concept a specific item actually belongs to:

```markdown
concepts: c7, c8

## Due
- (c7) Quiz #3: 2D Array
- (ap-review) AP Classroom: FRQ: Methods and Control Structures
```

An untagged bullet in a multi-concept week is treated as shared by all the
concepts listed in `concepts:` — fine for something like a CS-in-the-News
article that's genuinely relevant to both units. Tag it when it's really
specific to one (like a unit test), so it doesn't also show up under the
wrong unit's page.

## `concepts.md` — the list of units

One line per concept, `id: title`, in teaching order (this order controls
display order everywhere on the site):

```
c1: Concept 1: Classes & Objects
c2: Concept 2: Strings
```

Don't reuse an id or rename one that's already referenced by a week file's
`concepts:` field, unless you also update those week files.

## `course-info.md` — the one non-weekly page

Syllabus, textbook, seating chart, schedule links — stuff that isn't tied to
any particular week. Just a flat bullet list under the heading, same bullet
syntax as everywhere else (`- [Title](url)` or `- Title`).

## What's *not* in here

`../source/canvas-migration/` is the one-time script that generated this
`content/` folder from the original Canvas export. It's historical — don't
run it again, it would overwrite anything you've since edited here.
