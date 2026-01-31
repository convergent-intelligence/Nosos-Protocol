# Lost User Field Guide

If you are offline or stranded, this USB should let you install an OS and bring up the Agent Systems Framework (ASF) without GitHub access.

Start here:

1) Choose a path:
   - Debian (fastest)
   - Gentoo (full control)
   - Arch (simple, rolling)

2) Open the Boot Companion:
   - `docs/boot-companion.html`

3) Boot from ISO under `iso/` and install the OS.

4) After install, mount this USB and run the ASF installer.

## ASF Install (All Distros)

Requirements: python3, tar, file

```bash
sudo bash /path/to/usb/asf/install-asf.sh /path/to/usb/asf/agent-systems-framework-YYYYMMDD.tar.gz /opt/agent-systems-framework
```

Then validate:

```bash
cd /opt/agent-systems-framework/agent-systems-framework
./scripts/validate.sh
./scripts/autofile init
./scripts/health.sh
```

## Web3 Auth (Brave)

If you need Web3 authentication, install Brave from the USB kit:

- Packages live under `browsers/brave/`
- See `docs/deploy/brave-offline.md`

## Debian Path (Fastest)

- Use the Debian ISO under `iso/debian/`
- Netinst requires network; DVD ISO does not
- After install, run the ASF install steps above

## Gentoo Path

- Use the Gentoo minimal ISO under `iso/gentoo/`
- Use stage3 tarballs under `gentoo/stages/`
- Follow the offline handbook under `docs/gentoo-handbook/`
- After chroot and base system setup, install ASF

## Arch Path

- Use the Arch ISO under `iso/arch/`
- Follow the offline install guide under `docs/arch-install-guide/`
- After base system setup, install ASF
