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

```bash
./scripts/deploy/build-debian-preseed-iso.sh /path/to/debian-12.x.x-amd64-netinst.iso dist/asf-debian-preseed.iso
```

Pick one:
- Installer ISO (automated install): best for reproducibility
- Live ISO: best for demos

For Phase 0, document the choice and keep it simple.

## Upload to IONOS (Manual)

The exact UI varies by IONOS product (Cloud vs Dedicated vs VPS).

Target (chosen): IONOS Cloud Server.

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
