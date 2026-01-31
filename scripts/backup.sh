#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

with_blobs=0
if [[ "${1:-}" == "--with-blobs" ]]; then
  with_blobs=1
fi

backup_dir="${root_dir}/backups"
mkdir -p "${backup_dir}"

stamp="$(date -u +%Y%m%d-%H%M%S)"
name="asf-backup-${stamp}"
out="${backup_dir}/${name}.tar.gz"

extra=()
if [[ "${with_blobs}" -eq 1 ]]; then
  extra+=("store/blobs" "store/derived")
fi

tar \
  --create \
  --gzip \
  --file "${out}" \
  --directory "${root_dir}" \
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
  rules \
  tools \
  scripts \
  distro \
  gemini.md \
  index \
  units \
  "${extra[@]}"

printf "backup: %s\n" "${out}"
