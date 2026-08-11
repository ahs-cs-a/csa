"""
Parses content/*.md into data.js. This is the live content pipeline —
run this (or ./publish.sh from the repo root) after editing anything in content/.
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CONTENT = os.path.join(ROOT, "content")

BUCKET_TO_SECTION = {
    "slides": "Slides",
    "resources": "Resources",
    "homework": "Homework",
    "due": "Due",
    "news": "CS in the News",
}
BUCKET_ORDER = ["slides", "resources", "homework", "due", "news"]


def parse_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', text, re.S)
    if not m:
        raise ValueError("missing frontmatter block")
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_text.splitlines():
        if not line.strip() or ':' not in line:
            continue
        key, val = line.split(':', 1)
        fm[key.strip()] = val.strip()
    return fm, body


def parse_bullets(section_text):
    """Parses "- [Title](url)" / "- Title" bullets. A line may start with an
    optional "(c7, c8)" concept tag — only needed in weeks with more than one
    concept active, to say which concept an item actually belongs to (see
    content/README.md). Untagged items in a multi-concept week are treated as
    shared by all concepts active that week."""
    items = []
    for line in section_text.splitlines():
        line = line.strip()
        if not line.startswith('-'):
            continue
        line = line[1:].strip()
        if line.startswith('<!--'):
            continue
        tag_concepts = None
        tag_match = re.match(r'^\(([\w,\s-]+)\)\s+(.*)$', line)
        if tag_match:
            tag_concepts = [c.strip() for c in tag_match.group(1).split(',') if c.strip()]
            line = tag_match.group(2)
        m = re.match(r'^\[(.+?)\]\((.+?)\)$', line)
        if m:
            item = {"title": m.group(1).strip(), "url": m.group(2).strip()}
        else:
            item = {"title": line, "url": None}
        if tag_concepts:
            item["_concepts"] = tag_concepts
        items.append(item)
    return items


def parse_week_file(path):
    fm, body = parse_frontmatter(open(path).read())
    week = {
        "semester": fm["semester"],
        "week": int(fm["week"]),
        "concepts": [c.strip() for c in fm.get("concepts", "").split(",") if c.strip()],
        "focus": fm.get("focus", ""),
    }
    sections = re.split(r'^##\s+(.+?)\s*$', body, flags=re.M)
    # sections[0] is preamble (ignored); then alternating header, body, header, body...
    buckets = {b: [] for b in BUCKET_ORDER}
    header_to_bucket = {v: k for k, v in BUCKET_TO_SECTION.items()}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        section_body = sections[i + 1] if i + 1 < len(sections) else ""
        bucket = header_to_bucket.get(header)
        if bucket:
            buckets[bucket] = parse_bullets(section_body)
    week.update(buckets)
    return week


def parse_concepts_registry(path):
    concepts = []
    for line in open(path):
        line = line.strip()
        if not line or ':' not in line:
            continue
        cid, title = line.split(':', 1)
        concepts.append({"id": cid.strip(), "title": title.strip()})
    return concepts


def parse_course_info(path):
    text = open(path).read()
    body = re.sub(r'^#.*\n', '', text, count=1)  # drop the leading "# Course Information" heading
    return parse_bullets(body)


# ---------------------------------------------------------------- build WEEKS
week_files = sorted(glob.glob(os.path.join(CONTENT, "weeks", "*.md")))
weeks = [parse_week_file(p) for p in week_files]
weeks.sort(key=lambda w: (w["semester"], w["week"]))

# --------------------------------------------------------------- build CONCEPTS
# (must happen before the due->assessments rename below, since it reads w["due"])
registry = parse_concepts_registry(os.path.join(CONTENT, "concepts.md"))
concepts_by_id = {c["id"]: {"id": c["id"], "title": c["title"], "sections": {}} for c in registry}

if "course-info" in concepts_by_id:
    concepts_by_id["course-info"]["sections"]["General"] = parse_course_info(os.path.join(CONTENT, "course-info.md"))

def strip_internal(item):
    return {k: v for k, v in item.items() if not k.startswith('_')}


for w in weeks:
    for cid in w["concepts"]:
        if cid not in concepts_by_id:
            continue
        sections = concepts_by_id[cid]["sections"]
        for bucket in BUCKET_ORDER:
            header = BUCKET_TO_SECTION[bucket]
            for it in w[bucket]:
                # an item tagged "(c7, c8)" only belongs to those concepts;
                # untagged items belong to every concept active that week
                owners = it.get("_concepts")
                if owners is not None and cid not in owners:
                    continue
                sections.setdefault(header, [])
                sections[header].append({**strip_internal(it), "week": w["week"], "semester": w["semester"]})

concepts = [concepts_by_id[c["id"]] for c in registry if c["id"] in concepts_by_id]

# rename "due" -> "assessments" to match the field name script.js expects on
# WEEKS, and drop the internal "_concepts" tag now that attribution is done
for w in weeks:
    w["assessments"] = [strip_internal(it) for it in w.pop("due")]
    for bucket in ("slides", "resources", "homework", "news"):
        w[bucket] = [strip_internal(it) for it in w[bucket]]

# ------------------------------------------------------------------- write out
with open(os.path.join(ROOT, "data.js"), "w") as f:
    f.write("const CONCEPTS = " + json.dumps(concepts) + ";\n")
    f.write("const WEEKS = " + json.dumps(weeks) + ";\n")

print(f"wrote data.js from {len(weeks)} week files and {len(concepts)} concepts")
