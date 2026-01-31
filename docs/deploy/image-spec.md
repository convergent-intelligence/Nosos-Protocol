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
