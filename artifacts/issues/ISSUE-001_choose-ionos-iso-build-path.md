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

Current decision:
- Target: IONOS Cloud Server (`docs/decisions/0003-ionos-target.md`)
- Approach: Debian installer ISO with automated install (`docs/decisions/0002-iso-build-approach.md`)

Reference:
- `docs/deploy/ionos-iso.md`
- `docs/deploy/debian-preseed.md`
- `docs/deploy/image-spec.md`
