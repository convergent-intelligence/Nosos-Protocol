#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [[ ! -f "${root_dir}/STATUS.md" ]]; then
  printf "Missing STATUS.md at %s\n" "${root_dir}" >&2
  exit 1
fi

printf "Initialized substrate for %s\n" "${root_dir}"
