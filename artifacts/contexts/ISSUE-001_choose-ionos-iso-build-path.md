# Context Capsule: Choose IONOS ISO build path

Work ID: ISSUE-001
Kind: issue
Domain: builder
Priority: high
Status: in_progress
Owner: builder
Generated: 2026-01-30T04:02:19Z

## Objective

Need provider target and ISO approach

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
- `artifacts/issues/ISSUE-001_choose-ionos-iso-build-path.md`

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

### `artifacts/issues/ISSUE-001_choose-ionos-iso-build-path.md`

```
# Issue: Choose IONOS ISO build path

ID: ISSUE-001
Date: 2026-01-30

## Problem

We want to share a complete server image via IONOS by uploading an ISO.

We need to pick the most reliable, least-surprising path that:
- is reproducible
- does not embed secrets or workstation state
- yields a working system on first boot

## Constraints

- IONOS product varies (Cloud Server vs VPS vs Dedicated) and changes ISO attach/boot flow.
- We must not bake in user data (`store/blobs/`, sqlite index, audit logs).
- We must assume unknown network constraints during install (some environments restrict outbound).
- We want one ISO artifact to share (self-contained preferred).

## Options

- Option A (recommended): Debian 12 installer ISO + automated install (preseed/autoinstall)
  - self-contained, deterministic
  - best for sharing and repeated provisioning

- Option B: Keep official Debian ISO, use network preseed + postinstall script
  - simplest build (no ISO repack)
  - depends on hosting the preseed and having network access

- Option C: Live ISO
  - best for demos
  - higher risk of shipping state, harder to harden

- Option D: VM image (qcow2/raw) instead of ISO
  - may be better depending on IONOS product support

## Decision / Next

Next:
- Confirm target IONOS product (Cloud/VPS/Dedicated).
- Choose installer-vs-live and base OS/version.
- Record the decision in `docs/decisions/0002-iso-build-approach.md`.
- Implement the chosen pipeline under `DEPLOY-002`.

Reference:
- `docs/deploy/ionos-iso.md`
- `docs/deploy/debian-preseed.md`
- `docs/deploy/image-spec.md`
```

