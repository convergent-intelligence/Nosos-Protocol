#!/usr/bin/env bash
set -euo pipefail

# Phase 0 stub: we document and prepare, but do not yet generate an ISO.
# This script exists so the workflow has a stable entrypoint.

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf "ISO build is not automated yet.\n\n"
printf "Next steps:\n"
printf "- Decide installer-vs-live: %s\n" "${root_dir}/docs/decisions/0002-iso-build-approach.md"
printf "- Confirm IONOS target: %s\n" "${root_dir}/docs/deploy/ionos-iso.md"
printf "- Build distro tarball: %s\n" "${root_dir}/scripts/build-distro.sh"

printf "\nTooling that will likely be needed (varies by approach):\n"
printf "- xorriso / genisoimage\n"
printf "- debian-cd or live-build (Debian), or Ubuntu autoinstall tooling\n"
printf "\nWhen DEPLOY-001 is decided, implement DEPLOY-002 to build the ISO.\n"
