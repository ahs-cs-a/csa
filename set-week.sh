#!/usr/bin/env bash
# Update which week the site treats as "now" and publish it.
#
#   ./set-week.sh s2 9
#
set -euo pipefail
cd "$(dirname "$0")"

SEM="${1:-}"
WEEK="${2:-}"

if [[ -z "$SEM" || -z "$WEEK" ]]; then
  echo "Usage: ./set-week.sh <s1|s2> <week number>"
  echo "Example: ./set-week.sh s2 9"
  exit 1
fi

if [[ "$SEM" != "s1" && "$SEM" != "s2" ]]; then
  echo "Semester must be s1 or s2, got: $SEM"
  exit 1
fi

if ! [[ "$WEEK" =~ ^[0-9]+$ ]]; then
  echo "Week must be a number, got: $WEEK"
  exit 1
fi

# Confirm that week actually exists in data.js before touching anything.
# (Concatenated into a real script file rather than `node -e ... eval(...)`,
# since indirect eval doesn't leak top-level `const` bindings. Written next
# to data.js, not /tmp, so this works regardless of OS temp-dir quirks.)
CHECK_FILE="./.week-check-tmp.js"
trap 'rm -f "$CHECK_FILE"' EXIT
cat data.js > "$CHECK_FILE"
cat >> "$CHECK_FILE" << 'EOF'
const sem = process.argv[2];
const week = parseInt(process.argv[3], 10);
console.log(WEEKS.some(w => w.semester === sem && w.week === week) ? "yes" : "no");
EOF
EXISTS=$(node "$CHECK_FILE" "$SEM" "$WEEK")
rm -f "$CHECK_FILE"

if [[ "$EXISTS" != "yes" ]]; then
  echo "No such week in data.js: $SEM week $WEEK. Check source/build_weeks.py for the valid range."
  exit 1
fi

sed -i '' -E "s/const CURRENT = \{ semester: \"[a-z0-9]+\", week: [0-9]+ \};/const CURRENT = { semester: \"$SEM\", week: $WEEK };/" script.js

echo "Set CURRENT to $SEM week $WEEK."
git add script.js
git commit -m "Set current week: $(echo "$SEM" | tr '[:lower:]' '[:upper:]') Week $WEEK"
git push
echo "Live at https://ahs-cs-a.github.io/csa/"
