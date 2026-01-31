# Decision 0002: ISO Build Approach

Date: 2026-01-30
Status: accepted

## Context

We want to share a real server image that boots into a ready-to-run Agent Systems Framework environment. The target provider is IONOS.

## Decision

Chosen approach: Installer ISO with automated install.

We target a Debian 12 installer ISO with a preseed/autoinstall strategy.

## Consequences

- Tooling: preseed/autoinstall + postinstall script
- First-boot config runs as part of install and/or first boot (no secrets)

## Alternatives Considered

- Distribute a VM image (qcow2/raw) instead of an ISO
- Use cloud-init images instead of ISO upload
