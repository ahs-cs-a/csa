import re, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "modules_raw.tsv")

CONCEPT_META = [
    ("course-info", "Course Information", None, None),
    ("c1", "Concept 1: Classes & Objects", 1, "s1"),
    ("c2", "Concept 2: Strings", 2, "s1"),
    ("c3", "Concept 3: Conditionals", 3, "s1"),
    ("c4", "Concept 4: Iteration", 4, "s1"),
    ("c5", "Concept 5: ArrayLists", 5, "s2"),
    ("c6", "Concept 6: Arrays", 6, "s2"),
    ("c7", "Concept 7: 2D Arrays", 7, "s2"),
    ("c8", "Concept 8: Recursion", 8, "s2"),
    ("ap-review", "AP Exam Review", None, "s2"),
    ("c9", "Concept 9: Data & Regression", 9, "s2"),
    ("final", "Final Moments", None, "s2"),
]
TITLE_TO_ID = {
    "Course Information": "course-info",
    "Concept #1: Classes and Objects ": "c1",
    "Concept #2: Strings": "c2",
    "Concept #3: Conditionals": "c3",
    "Concept #4: Iteration": "c4",
    "Concept #5: ArrayLists": "c5",
    "Concept #6: Arrays": "c6",
    "Concept #7: 2D Arrays": "c7",
    "Concept #8: Recursion": "c8",
    "AP Review": "ap-review",
    "Concept #9: Data and Regression": "c9",
    "Final Moments": "final",
}

def parse_week(title):
    t = title.strip()
    sem = None
    m = re.search(r'\bS([12])\s*:\s*', t)
    if m:
        sem = "s" + m.group(1)
    m2 = re.search(r'\bWeek\s*#?\s*(\d+)', t, re.IGNORECASE)
    week = int(m2.group(1)) if m2 else None
    m3 = re.search(r'\bs([12])-w(\d+)', t, re.IGNORECASE)
    if m3 and week is None:
        sem = "s" + m3.group(1)
        week = int(m3.group(2))
    return sem, week

concepts = {}
for cid, disp, num, defsem in CONCEPT_META:
    concepts[cid] = {"id": cid, "title": disp, "number": num, "defaultSemester": defsem, "sections": {}}

current_section = "General"
with open(RAW) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 4:
            continue
        modtitle, ctype, title, url = fields[0], fields[1], fields[2], fields[3]
        cid = TITLE_TO_ID.get(modtitle)
        if cid is None:
            continue
        if ctype == "ContextModuleSubHeader":
            current_section = title.strip()
            concepts[cid]["sections"].setdefault(current_section, [])
            continue
        if not title.strip():
            continue
        sem, week = parse_week(title)
        concepts[cid]["sections"].setdefault(current_section, [])
        concepts[cid]["sections"][current_section].append({
            "title": title.strip(),
            "type": ctype,
            "url": url.strip() if url.strip() else None,
            "semester": sem,
            "week": week,
        })

out = {"concepts": [concepts[c[0]] for c in CONCEPT_META]}
with open(os.path.join(HERE, "concepts.json"), "w") as f:
    json.dump(out, f, indent=2)
print("done", sum(len(v) for c in concepts.values() for v in c["sections"].values()), "items")
