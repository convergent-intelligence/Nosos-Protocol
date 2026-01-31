# Deploy: LFS Pathway (Linux From Scratch)

Goal: produce a minimal, reproducible base OS built from source that boots and installs the Agent Systems Framework without pulling from GitHub.

This is a parallel pathway to the Debian preseed ISO. Debian remains the fastest path for VM testing; LFS is for ultimate control and offline resilience.

## Scope

- Build an LFS-based root filesystem following the LFS book
- Integrate the ASF distro tarball into the image
- Package as bootable ISO or bootable USB

## Inputs

- LFS book (current stable release)
- Host build system (Linux, with toolchain prerequisites)
- Package sources downloaded to a local tarball cache
- ASF distro tarball from `./scripts/build-distro.sh`

## Outputs

- Bootable ISO or USB image with:
  - minimal OS
  - `asf` user
  - ASF installed in `/opt/agent-systems-framework/`

## High-Level Steps

1) Host setup
   - Install LFS host prerequisites
   - Create LFS build user and directory layout
   - Download all LFS package sources to a local cache

2) Toolchain and base system (LFS book)
   - Build temporary toolchain
   - Enter chroot
   - Build base system (glibc, gcc, core utilities)

3) Kernel + bootloader
   - Build Linux kernel
   - Install bootloader (GRUB) for ISO/USB target

4) ASF integration
   - Copy ASF tarball into the build tree
   - Create user `asf`
   - Install ASF using `scripts/deploy/install-asf.sh`

5) Image packaging
   - Create rootfs image
   - Build ISO (grub-mkrescue) or USB image

6) Validation
   - Boot image
   - Run `./scripts/validate.sh`, `./scripts/autofile init`, `./scripts/health.sh`

## Offline/Disconnected Mode

- Keep all LFS sources in a local cache
- Avoid network package mirrors during build and boot
- Include any required runtime dependencies inside the image

## Security Notes

- Do not bake secrets
- Do not include `store/blobs/` or `index/*.sqlite`

## Open Decisions

- Target kernel config (minimal vs. broad hardware support)
- Boot target (ISO vs. USB-first)
- Whether to include a live overlay for USB mode

## References

- `docs/deploy/image-spec.md`
- `docs/deploy/debian-preseed.md`
- `scripts/deploy/install-asf.sh`
