#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist_dir="${root_dir}/dist"

stamp="$(date -u +%Y%m%d)"
name="agent-systems-framework"
out="${dist_dir}/${name}-${stamp}.tar.gz"

mkdir -p "${dist_dir}"

# Create a clean tarball without user data.
# This is intentionally conservative; if you add new user-data dirs, update excludes.

tar \
  --create \
  --gzip \
  --file "${out}" \
  --directory "${root_dir}" \
  --transform "s,^,${name}/," \
  --exclude="dist" \
  --exclude="inbox" \
  --exclude="store/blobs" \
  --exclude="store/derived" \
  --exclude="index/*.sqlite" \
  --exclude="index/*.sqlite-*" \
  --exclude="index/audit.jsonl" \
  --exclude="units/*/attachments.jsonl" \
  --exclude="artifacts/issues/*.md" \
  --exclude="artifacts/stubs/*.md" \
  --exclude="artifacts/contexts/*.md" \
  README.md \
  STATUS.md \
  PHASE-0.md \
  docs \
  .agents \
  .bridges \
  .substrate \
  .synthesis \
  .pantheon \
  .tavern \
  quests \
  artifacts \
  tools \
  scripts \
  rules \
  distro \
  gemini.md

printf "built: %s\n" "${out}"
