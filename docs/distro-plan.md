# Distro Plan: Agent Systems Framework

This plan defines how to ship a "distro" (a distributable bundle) of the Agent Systems Framework.

The distro is designed to be:
- copyable (one tarball)
- safe (no user blobs, secrets, or indexes by default)
- self-describing (manifest + docs)
- extensible (drop-in tools like AutoFile)

## What The Distro Is

A distro is a snapshot of:
- the scaffold directory structure
- core docs and protocols
- tool entrypoints under `scripts/`
- reference schemas and templates

It is not:
- a runtime deployment
- a secret store
- a data dump

## Release Artifact

- Output: `dist/agent-systems-framework-YYYYMMDD.tar.gz`
- Contents are governed by `distro/MANIFEST.yaml`.

## Build Phases

### Phase A: Package The Scaffold (now)

Deliverables:
- `scripts/build-distro.sh` creates a tarball
- explicit excludes for `store/blobs`, `index/*.sqlite`, and any inbox content
- a manifest describing included paths

Success:
- build is deterministic enough for humans (repeatable on the same tree)
- tarball untars cleanly and validates with `scripts/validate.sh`

### Phase B: Add Verification

Deliverables:
- `scripts/verify-distro.sh` to untar into a temp dir and run validation
- record checksums of the tarball

Success:
- verification is one command

### Phase C: Add Upgrade Path

Deliverables:
- schema/version bump rules
- migration notes for `index/` and `unit.yaml`

Success:
- new distros can be adopted without breaking existing user data

## Guardrails

- Never include:
  - `store/blobs/`
  - `store/derived/`
  - `index/autofile.sqlite`
  - `inbox/` contents
  - `quarantine/` contents
- Always include:
  - docs and templates
  - tool source under `tools/`
  - entry scripts under `scripts/`
