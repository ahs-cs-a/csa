import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
concepts = json.load(open(os.path.join(HERE, "concepts.json")))
weeks = json.load(open(os.path.join(HERE, "weeks.json")))

out_path = os.path.join(HERE, "..", "..", "data.js")
with open(out_path, "w") as f:
    f.write("const CONCEPTS = " + json.dumps(concepts["concepts"]) + ";\n")
    f.write("const WEEKS = " + json.dumps(weeks["weeks"]) + ";\n")
print("wrote", os.path.abspath(out_path))
