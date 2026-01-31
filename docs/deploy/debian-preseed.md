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

Automation scripts:
- `scripts/deploy/build-debian-preseed-iso.sh`
- `scripts/deploy/repack-debian-iso.py`

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

## Build (Recommended)

1) Download Debian netinst ISO.

2) Build ASF ISO:

```bash
./scripts/deploy/build-debian-preseed-iso.sh /path/to/debian-12.x.x-amd64-netinst.iso dist/asf-debian-preseed.iso
```

Notes:
- Requires `xorriso`.
- The preseed prompts for the `asf` user password (no baked credentials).
