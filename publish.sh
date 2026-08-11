#!/usr/bin/env bash
# Rebuild the site from source/ and publish.
# Run this after editing source/build_weeks.py, source/build_data.py,
# or source/modules_raw.tsv.
#
#   ./publish.sh "fixed the 2D arrays slide link"
#
set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-Update course content}"

cd source
python3 build_data.py
python3 build_weeks.py
python3 build_data_js.py
cd ..

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

git add -A
git commit -m "$MSG"
git push
echo "Live at https://ahs-cs-a.github.io/csa/"
