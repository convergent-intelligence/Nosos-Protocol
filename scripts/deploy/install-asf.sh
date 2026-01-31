#!/usr/bin/env bash
set -euo pipefail

# Installs a distro tarball onto a target machine.
# Safe defaults: does not create secrets, does not start daemons.

tarball="${1:-}"
prefix="${2:-/opt/agent-systems-framework}"

if [[ -z "${tarball}" || ! -f "${tarball}" ]]; then
  printf "usage: %s <agent-systems-framework-*.tar.gz> [prefix]\n" "$0" >&2
  exit 1
fi

mkdir -p "${prefix}"
tar -xzf "${tarball}" -C "${prefix}"

root_dir="${prefix}/agent-systems-framework"
if [[ ! -d "${root_dir}" ]]; then
  printf "unexpected archive layout under %s\n" "${prefix}" >&2
  exit 1
fi

cd "${root_dir}"
./scripts/validate.sh
./scripts/autofile init
./scripts/health.sh >/dev/null

printf "installed: %s\n" "${root_dir}"
