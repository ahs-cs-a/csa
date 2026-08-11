#!/usr/bin/env bash
# Rebuild the site from content/ and publish.
# Run this after editing anything in content/ (weekly files, concepts.md,
# course-info.md).
#
#   ./publish.sh "fixed the 2D arrays slide link"
#
set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-Update course content}"

python3 source/build_from_markdown.py

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

git add -A
git commit -m "$MSG"
git push
echo "Live at https://ahs-cs-a.github.io/csa/"
