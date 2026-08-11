"""
One-time script: converts the archived Canvas parse (concepts.json) plus the
hand-reconstructed pacing guide (below, copied from the old build_weeks.py)
into the new content/*.md authoring format.

Run once from repo root:  python3 source/canvas-migration/generate_markdown.py
Do not re-run after content/ has been hand-edited — it will overwrite it.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
CONTENT = os.path.join(ROOT, "content")

concepts = json.load(open(os.path.join(HERE, "concepts.json")))["concepts"]
BY_ID = {c["id"]: c for c in concepts}

CONCEPT_META = [
    ("course-info", "Course Information"),
    ("c1", "Concept 1: Classes & Objects"),
    ("c2", "Concept 2: Strings"),
    ("c3", "Concept 3: Conditionals"),
    ("c4", "Concept 4: Iteration"),
    ("c5", "Concept 5: ArrayLists"),
    ("c6", "Concept 6: Arrays"),
    ("c7", "Concept 7: 2D Arrays"),
    ("c8", "Concept 8: Recursion"),
    ("ap-review", "AP Exam Review"),
    ("c9", "Concept 9: Data & Regression"),
    ("final", "Final Moments"),
]

S1 = [
    (1, ["c1"], "Intro to classes & objects: fields, constructors, instance methods."),
    (2, ["c1"], "Building objects with state — the BodyOfWater class."),
    (3, ["c1"], "More classes & objects practice; Quiz #2."),
    (4, ["c1", "c2"], "Wrapping up classes & objects; strings begin."),
    (5, ["c1", "c2"], "Concept #1 Test. String methods & analysis start."),
    (6, ["c2", "c3"], "Strings continue; conditionals (if/else, booleans) begin."),
    (7, ["c2", "c3"], "String creation practice; conditionals continue."),
    (8, ["c2", "c3"], "Concept #2 Test. Conditionals: the Virtual Pet project."),
    (9, ["c3"], "Conditionals continue — Quiz #1."),
    (10, ["c3"], "Conditionals continue — Quiz #2."),
    (11, ["c3"], "Conditionals wrap-up — Quiz #3, XEyes case study."),
    (12, ["c3", "c4"], "Concept #3 Test. Iteration (loops) begins."),
    (13, ["c4"], "Iteration continues — HW #1, Quiz #1."),
    (14, ["c4"], "Iteration continues — HW #2, Quiz #2."),
    (15, ["c4", "c5"], "Iteration wraps — Quiz #3. ArrayLists preview begins."),
    (16, ["c4"], "Concept #4 Test — loops."),
    (17, [], "Semester 1 finals: on-computer final + final project."),
]
S2 = [
    (1, ["c5"], "ArrayLists: storing and managing collections of objects."),
    (2, ["c5"], "ArrayLists continue — HW #2."),
    (3, ["c5"], "ArrayLists continue — HW #3, Quiz #1."),
    (4, ["c5"], "ArrayLists — Sound Project, Quiz #2."),
    (5, ["c5", "c6"], "Concept #5 Test. Arrays (fixed-size) begin."),
    (6, ["c6"], "Arrays continue — HW #1, Quiz #1."),
    (7, ["c6"], "Arrays continue — HW #2, sorting & binary search practice."),
    (8, ["c6", "c7"], "Test: Arrays. 2D arrays begin."),
    (9, ["c7", "c8"], "2D arrays continue. Recursion introduced."),
    (10, ["c7"], "2D arrays — Quiz #1 (2D Arrays/Exceptions)."),
    (11, ["c7"], "2D arrays — Quiz #2, small-models demo."),
    (12, ["c7", "c8"], "2D arrays — binary search practice. Recursion resumes."),
    (13, ["c7", "c8", "ap-review"], "2D arrays Quiz #3. Recursion debugging. AP Review begins."),
    (14, ["c7", "c8", "ap-review"], "2D Array concept test. Recursion HW #1. AP Review: FRQs."),
    (15, ["ap-review"], "AP Review wraps. AP Computer Science A Exam."),
    (16, ["c9"], "Post-exam unit: data & regression, Data Project #1."),
    (17, ["c9"], "Data & regression continues — Data Project #1b."),
    (18, ["c9", "final"], "Data Project #2. Final: Connect-4."),
]

SECTION_TO_BUCKET = {
    "Slides": "slides",
    "Homework": "homework",
    "Resources": "resources",
    "Resources and Code": "resources",
    "Code": "resources",
    "Assessments": "due",
    "Assessements": "due",
    "Quiz/Test": "due",
    "Quizzes": "due",
    "Quiz/Tests": "due",
    "Reviews": "due",
    "CS in the News": "news",
}
BUCKET_HEADERS = [
    ("slides", "Slides"),
    ("resources", "Resources"),
    ("homework", "Homework"),
    ("due", "Due"),
    ("news", "CS in the News"),
]


def clean_title(t, strip_news_prefix=False):
    t = re.sub(r'^S[12]:\s*', '', t.strip(), flags=re.I)
    t = re.sub(r'^Week\s*\d+(\s*/\s*\d+)?[:\s]*', '', t, flags=re.I)
    if strip_news_prefix:
        t = re.sub(r'^CS in the News:\s*', '', t.strip(), flags=re.I)
    return t.strip()


def bullet(item, bucket=None):
    title = clean_title(item["title"], strip_news_prefix=(bucket == "news")) or item["title"]
    if item["url"]:
        return f"- [{title}]({item['url']})"
    return f"- {title}"


def dedupe_tagged(tagged_items):
    """tagged_items: list of (concept_id, item). Merges identical (title,url)
    items contributed by multiple concepts into one, tracking which concepts
    it belongs to — so topics.html can attribute it correctly instead of
    handing every item in an overlap week to every concept active that week."""
    merged = {}  # (title, url) -> {"item": item, "concepts": set()}
    order = []
    for cid, it in tagged_items:
        key = (it["title"], it["url"])
        if key not in merged:
            merged[key] = {"item": it, "concepts": set()}
            order.append(key)
        merged[key]["concepts"].add(cid)
    return [(merged[k]["concepts"], merged[k]["item"]) for k in order]


# ---- bucket every weeked item from every real concept, by (semester, week) ----
# Each item is tagged with the concept it actually came from, so overlap
# weeks (e.g. one week with 2D Arrays + Recursion + AP Review all active)
# don't get every item attributed to every concept.
grid = {}  # (sem, week) -> {bucket: [(concept_id, item), ...]}
for c in concepts:
    if c["id"] == "course-info":
        continue
    for section, items in c["sections"].items():
        bucket = SECTION_TO_BUCKET.get(section)
        if bucket is None:
            continue  # "General" on final/course-info, or unmapped — skipped
        for it in items:
            if it["week"] is None:
                continue  # left out per decision — add manually once the real week is known
            sem = it["semester"] or c["defaultSemester"]
            key = (sem, it["week"])
            grid.setdefault(key, {"slides": [], "resources": [], "homework": [], "due": [], "news": []})
            grid[key][bucket].append((c["id"], it))

os.makedirs(os.path.join(CONTENT, "weeks"), exist_ok=True)


def write_week(sem, week, concept_ids, focus):
    bucketed = grid.get((sem, week), {"slides": [], "resources": [], "homework": [], "due": [], "news": []})
    fname = f"{sem}-w{week:02d}.md"
    lines = ["---", f"semester: {sem}", f"week: {week}", f"concepts: {', '.join(concept_ids)}", f"focus: {focus}", "---", ""]
    multi = len(concept_ids) > 1
    for bucket_key, header in BUCKET_HEADERS:
        lines.append(f"## {header}")
        items = dedupe_tagged(bucketed[bucket_key])
        if items:
            for cids, it in items:
                line = bullet(it, bucket=bucket_key)
                # only tag items in weeks with more than one concept, and only
                # when the item doesn't apply to every concept active that week
                # (otherwise the tag would be redundant noise)
                if multi and cids != set(concept_ids):
                    tag = ", ".join(cid for cid in concept_ids if cid in cids)
                    line = f"- ({tag}) {line[2:]}"
                lines.append(line)
        else:
            lines.append("<!-- - [Title](https://example.com) -->")
        lines.append("")
    with open(os.path.join(CONTENT, "weeks", fname), "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")


for week, cids, focus in S1:
    write_week("s1", week, cids, focus)
for week, cids, focus in S2:
    write_week("s2", week, cids, focus)

# ---- concepts.md registry ----
# One "id: title" per line, in teaching order (this order controls display
# order everywhere on the site).
with open(os.path.join(CONTENT, "concepts.md"), "w") as f:
    for cid, title in CONCEPT_META:
        f.write(f"{cid}: {title}\n")

# ---- course-info.md (static, non-weekly) ----
course_info_items = BY_ID["course-info"]["sections"].get("General", [])
with open(os.path.join(CONTENT, "course-info.md"), "w") as f:
    f.write("# Course Information\n\n")
    for it in course_info_items:
        f.write(bullet(it) + "\n")

print(f"wrote {len(S1) + len(S2)} week files, concepts.md, course-info.md to {os.path.abspath(CONTENT)}")
