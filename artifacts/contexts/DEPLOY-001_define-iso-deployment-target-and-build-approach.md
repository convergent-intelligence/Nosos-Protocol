# Context Capsule: Define ISO deployment target and build approach

Work ID: DEPLOY-001
Kind: plan
Domain: builder
Priority: high
Status: in_progress
Owner: builder
Generated: 2026-01-30T04:02:11Z

## Objective

Pick IONOS product + base OS + installer-vs-live; then automate

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
- `docs/deploy/ionos-iso.md`
- `docs/decisions/0002-iso-build-approach.md`
- `docs/decisions/0003-ionos-target.md`

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

### `docs/deploy/ionos-iso.md`

```
# Deploy: IONOS ISO Upload (Server Image Sharing)

Goal: create a shareable server image that boots into a ready-to-run Agent Systems Framework environment.

This doc is intentionally provider-agnostic in the build step, and IONOS-specific in the upload/attach step.

## What We Are Shipping

Two layers:

1) Framework distro (tarball)
- Built with `./scripts/build-distro.sh`
- Artifact: `dist/agent-systems-framework-YYYYMMDD.tar.gz`

2) Bootable ISO (installer or live)
- Contains a minimal OS installer/config + the distro tarball
- On first boot, installs/unpacks the framework into a target directory

Target spec:
- `docs/deploy/image-spec.md`

## Recommended Approach

Use a Debian-based ISO with an automated install (preseed or autoinstall), then a first-boot script that:
- creates a dedicated user
- installs runtime deps (python3, file(1), tar)
- unpacks the distro tarball
- runs `./scripts/validate.sh`

Installer helper:
- `scripts/deploy/install-asf.sh`

Recommended ISO strategy:
- `docs/deploy/debian-preseed.md`

## Build Steps (Local)

1. Build distro tarball:

```bash
./scripts/build-distro.sh
./scripts/verify-distro.sh
```

2. Build ISO:

Pick one:
- Installer ISO (automated install): best for reproducibility
- Live ISO: best for demos

For Phase 0, document the choice and keep it simple.

## Upload to IONOS (Manual)

The exact UI varies by IONOS product (Cloud vs Dedicated vs VPS).

Typical flow:

1. Upload ISO to your IONOS account (ISO images/media section).
2. Create a server.
3. Attach the ISO as virtual media.
4. Boot from ISO.
5. Complete install (automated preferred).
6. Confirm framework presence and run:

```bash
cd agent-systems-framework
./scripts/validate.sh
./scripts/health.sh
```

## Post-Install Verification

- `./scripts/orchestrate status`
- `./scripts/orchestrate next`
- ingest smoke test: drop a file into `inbox/` and run `./scripts/autofile watch-inbox --once`

## Security Notes

- Never bake secrets into the image.
- Ensure the ISO does not include `store/blobs/` or `index/*.sqlite` from your workstation.
- Prefer a first-boot credential rotation step.

## Open Questions (Need Answers Before We Automate)

- Which IONOS product are we targeting (Cloud Server vs VPS vs Dedicated)?
- Do we want an installer ISO (autoinstall) or a live ISO?
- Target base OS and version?
```

### `docs/decisions/0002-iso-build-approach.md`

```
# Decision 0002: ISO Build Approach

Date: 2026-01-30
Status: proposed

## Context

We want to share a real server image that boots into a ready-to-run Agent Systems Framework environment. The target provider is IONOS.

## Decision

Pick one approach:

1) Installer ISO with automated install (recommended)
- deterministic, reproducible installs
- easier to keep clean (no baked-in runtime state)

2) Live ISO
- better for demos
- tends to accumulate state and requires more careful hardening

## Consequences

- Determines tooling (preseed/autoinstall vs live-build)
- Determines where first-boot config runs

## Alternatives Considered

- Distribute a VM image (qcow2/raw) instead of an ISO
- Use cloud-init images instead of ISO upload
```

### `docs/decisions/0003-ionos-target.md`

```
# Decision 0003: IONOS Target

Date: 2026-01-30
Status: proposed

## Context

ISO upload/attach/boot steps differ across IONOS products (Cloud Server vs VPS vs Dedicated). The build pipeline (and how automated it can be) depends on the target.

## Decision

Choose a target:

- IONOS Cloud Server (recommended default)
- IONOS VPS
- IONOS Dedicated

## Consequences

- Determines the exact UI flow and boot media support.
- Determines whether we should ship ISO vs VM image.

## Next

Once target is chosen:
- update `docs/deploy/ionos-iso.md` with exact steps
- implement DEPLOY-002 against the chosen target
```

