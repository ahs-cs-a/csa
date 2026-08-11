import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
concepts = json.load(open(os.path.join(HERE, "concepts.json")))["concepts"]
BY_ID = {c["id"]: c for c in concepts}

# Hand-reconstructed pacing guide from Canvas module order + week labels found in item titles.
# Each entry: (semester, week, [concept_ids active], focus blurb)
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

def collect_items(concept_ids, semester, week):
    items = []
    for cid in concept_ids:
        c = BY_ID[cid]
        for section, its in c["sections"].items():
            for it in its:
                if it["week"] == week and (it["semester"] == semester or it["semester"] is None):
                    items.append({**it, "concept": cid, "conceptTitle": c["title"], "section": section})
    return items

def build_semester(label, rows, sem_key):
    out = []
    for week, cids, focus in rows:
        items = collect_items(cids, sem_key, week)
        slides = [i for i in items if i["section"] == "Slides"]
        hw = [i for i in items if i["section"] in ("Homework",)]
        assess = [i for i in items if i["section"] in ("Assessments", "Quiz/Tests", "Quizzes", "Quiz/Test", "Reviews")]
        news = [i for i in items if i["section"] == "CS in the News"]
        out.append({
            "semester": sem_key,
            "week": week,
            "concepts": cids,
            "focus": focus,
            "slides": slides,
            "homework": hw,
            "assessments": assess,
            "news": news,
        })
    return out

weeks = build_semester("Semester 1", S1, "s1") + build_semester("Semester 2", S2, "s2")
json.dump({"weeks": weeks}, open(os.path.join(HERE, "weeks.json"), "w"), indent=2)
print("built", len(weeks), "weeks")
