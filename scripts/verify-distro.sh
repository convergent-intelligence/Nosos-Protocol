#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

tarball="${1:-}"
if [[ -z "${tarball}" ]]; then
  tarball="$(ls -1t "${root_dir}/dist"/agent-systems-framework-*.tar.gz 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "${tarball}" || ! -f "${tarball}" ]]; then
  printf "missing tarball; build first with ./scripts/build-distro.sh\n" >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT

tar -xzf "${tarball}" -C "${tmp}"

pkg_dir="${tmp}/agent-systems-framework"
if [[ ! -d "${pkg_dir}" ]]; then
  printf "unexpected archive layout (expected agent-systems-framework/)\n" >&2
  exit 1
fi

"${pkg_dir}/scripts/validate.sh" >/dev/null

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "${tarball}"
else
  printf "verified: %s\n" "${tarball}"
fi
