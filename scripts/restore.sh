#!/usr/bin/env bash
set -euo pipefail

# Restores a backup tarball created by scripts/backup.sh.

tarball="${1:-}"
target="${2:-}"

if [[ -z "${tarball}" || -z "${target}" ]]; then
  printf "usage: %s <backup.tar.gz> <target-dir>\n" "$0" >&2
  exit 1
fi

if [[ ! -f "${tarball}" ]]; then
  printf "missing backup: %s\n" "${tarball}" >&2
  exit 1
fi

mkdir -p "${target}"

# Require the target to be empty (safety).
if [[ -n "$(ls -A "${target}" 2>/dev/null || true)" ]]; then
  printf "target not empty: %s\n" "${target}" >&2
  exit 1
fi

tar -xzf "${tarball}" -C "${target}"

printf "restored to: %s\n" "${target}"
