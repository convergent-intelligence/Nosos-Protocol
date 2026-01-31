# Context Capsule: Implement ISO build automation

Work ID: DEPLOY-002
Kind: plan
Domain: builder
Priority: high
Status: in_progress
Owner: builder
Generated: 2026-01-30T04:01:07Z

## Objective

Create a bootable ISO that installs OS + unpacks distro + validates

## Boundaries

In scope:
- Execute this work item exactly as written.
Out of scope:
- Redesign unrelated systems or expand scope without a new item.

## Invariants

- Do not delete originals during automation.
- Blob storage remains content-addressed and immutable.
- Actions remain auditable (append-only log).

## Touch Points

Files linked on the item:
- `scripts/build-iso.sh`
- `docs/deploy/iso-build.md`
- `docs/deploy/image-spec.md`
- `scripts/deploy/install-asf.sh`
- `docs/deploy/debian-preseed.md`
- `scripts/deploy/build-debian-preseed-iso.sh`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=2 units=3 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-035938_missive_assignment.json`
- `.bridges/signals/20260130-035836_proclamation_plan.json`
- `.bridges/signals/20260130-035647_missive_assignment.json`
- `.bridges/signals/20260130-035536_missive_assignment.json`
- `.bridges/signals/20260130-035536_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `scripts/build-iso.sh`

```
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
```

### `docs/deploy/iso-build.md`

```
# ISO Build Notes (Phase 0)

We will choose one of these when implementing the real ISO build.

## Option A: Debian Installer + Preseed (Recommended)

Pros:
- repeatable, minimal, secure by default
- can provision a user and install packages during install

Cons:
- more fiddly to get 100% unattended

## Option B: Ubuntu Autoinstall

Pros:
- first-class unattended install

Cons:
- ties you to Ubuntu tooling choices

## Option C: Live ISO

Pros:
- great for demos

Cons:
- harder to harden
- easier to accidentally ship state

## Phase 0 Decision

Record in `docs/decisions/0002-iso-build-approach.md`.
```

### `docs/deploy/image-spec.md`

```
# Image Spec: Agent Systems Framework Server

This is the target shape of a server image intended for sharing.

## Goals

- boots into a minimal, stable OS
- framework installed in a predictable location
- no baked-in user data (no blobs/index from a workstation)
- safe defaults (no secrets)

## Target Layout

- Install root: `/opt/agent-systems-framework/agent-systems-framework/`
- Primary user: `asf` (non-root)
- Data directories (owned by `asf`):
  - `/opt/agent-systems-framework/agent-systems-framework/store/`
  - `/opt/agent-systems-framework/agent-systems-framework/index/`
  - `/opt/agent-systems-framework/agent-systems-framework/units/`

## Minimum Dependencies

- Python 3
- `tar`
- optional: `file(1)`

## First Boot Checklist

- create user `asf`
- unpack distro tarball into `/opt/agent-systems-framework/`
- run:

```bash
cd /opt/agent-systems-framework/agent-systems-framework
./scripts/validate.sh
./scripts/autofile init
./scripts/health.sh
```

## What Must Not Be Included

- any `store/blobs/` content
- `index/autofile.sqlite`
- `index/audit.jsonl`
- any SSH private keys or tokens
```

### `scripts/deploy/install-asf.sh`

```
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
```

### `docs/deploy/debian-preseed.md`

```
# Deploy: Debian Installer + Preseed (ISO Strategy)

This is the recommended ISO strategy for a reproducible server image.

## Why This Approach

- deterministic installs
- minimal shipped state
- easy to keep secret-free

## Inputs

- Official Debian netinst ISO (downloaded from debian.org)
- Preseed file (`preseed.cfg`)
- Agent Systems Framework distro tarball (`dist/agent-systems-framework-YYYYMMDD.tar.gz`)
- First-boot install script (`scripts/deploy/install-asf.sh`)

## Output

- A bootable ISO that:
  - boots the Debian installer
  - runs unattended install (preseed)
  - copies the distro tarball onto the installed system
  - runs install validation

## Implementation Notes

There are two common implementation patterns:

1) Repack the Debian ISO
- extract ISO contents
- add `preseed.cfg` and the distro tarball
- adjust bootloader config to use preseed by default
- rebuild ISO

2) No repack; use network preseed
- keep the official ISO unchanged
- host preseed at a URL
- boot with `auto=true priority=critical preseed/url=...`

Pattern (2) is simpler but depends on network access to the preseed URL.
Pattern (1) is self-contained and best for sharing.
```

