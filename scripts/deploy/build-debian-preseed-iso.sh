#!/usr/bin/env bash
set -euo pipefail

# Builds a Debian installer ISO that includes:
# - preseed.cfg (unattended install except user password)
# - ASF distro tarball
# - installer helper script
#
# Requires: xorriso

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

base_iso="${1:-}"
out_iso="${2:-${root_dir}/dist/asf-debian-preseed.iso}"

if [[ -z "${base_iso}" ]]; then
  printf "usage: %s <debian-netinst.iso> [out.iso]\n" "$0" >&2
  exit 1
fi

if [[ ! -f "${base_iso}" ]]; then
  printf "missing base ISO: %s\n" "${base_iso}" >&2
  exit 1
fi

if ! command -v xorriso >/dev/null 2>&1; then
  printf "missing prerequisite: xorriso\n" >&2
  printf "install (debian/ubuntu): apt-get update && apt-get install -y xorriso\n" >&2
  exit 1
fi

# Ensure we have a distro tarball.
"${root_dir}/scripts/build-distro.sh" >/dev/null

distro_tarball="$(ls -1t "${root_dir}/dist"/agent-systems-framework-*.tar.gz | head -n 1)"
preseed_cfg="${root_dir}/scripts/deploy/preseed.cfg"

work_dir="${root_dir}/dist/iso-work/$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "${work_dir}"

python3 "${root_dir}/scripts/deploy/repack-debian-iso.py" \
  --base-iso "${base_iso}" \
  --distro "${distro_tarball}" \
  --preseed "${preseed_cfg}" \
  --out-iso "${out_iso}" \
  --work-dir "${work_dir}"
