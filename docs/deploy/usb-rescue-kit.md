# Deploy: USB Rescue Kit

Goal: create a USB kit that can bootstrap ASF without network access, and preserve the process for a lost or disconnected user.

This is complementary to the Debian preseed ISO flow and the LFS pathway.
It also supports a Ventoy-based multi-boot USB.

## Contents

- OS install media (ISOs)
- Offline handbooks and install guides
- Gentoo stage3 tarballs (and optional custom stages)
- ASF distro tarball + install script
- Checksums and an archive log
- Ventoy field manual (HTML)

## Suggested Layout

USBROOT/
  README.txt
  manifest.txt
  manifest.sha256
  docs/
    boot-companion.html
    learning-arc.html
    knowledge-archive.md
    content-stubs.md
    lost-user-guide.md
    install-asf-offline.md
    ventoy-field-manual.html
    handbooks/
      gentoo/
      arch/
      debian/
      lfs/
      fedora/
      handoff/
  iso/
    common/
      debian-12.x.x-amd64-netinst.iso
      debian-12.x.x-amd64-DVD-1.iso
      fedora-YYYY.iso
    uncommon/
      install-amd64-minimal-YYYYMMDD.iso
      archlinux-YYYY.MM.DD-x86_64.iso
      alpine-YYYY.iso
      void-YYYY.iso
    privacy/
      tails-YYYY.iso
    rescue/
      systemrescue-YYYY.iso
      gparted-YYYY.iso
      rescuezilla-YYYY.iso
      clonezilla-YYYY.iso
  vm/
    whonix/
      whonix-gateway.ova
      whonix-workstation.ova
  gentoo/
    stages/
      stage3-amd64-openrc-YYYYMMDD.tar.xz
      stage3-amd64-systemd-YYYYMMDD.tar.xz
    stages-custom/
  asf/
    agent-systems-framework-YYYYMMDD.tar.gz
    install-asf.sh
  llm/
    ollama/
    koboldcpp/
    llama.cpp/
    models/
    prompts/
  browsers/
    brave/
  toolchains/
    fedora/
    debian/
    arch/
    gentoo/
  knowledge/
    index.html
    kiwix/
    zims/
    references/
    manpages/
    games/
      index.html
  search/
    tools/
    indexes/
  persistence/
  ventoy/
  tools/
    bootloaders/
    gpt-recovery/
  wordlists/
  scripts/
    deploy/
      install-brave-offline.sh
      install-koboldcpp-daemon.sh
      snapshot-dev-env.sh
    system-scripts-framework/
  projects/
    archives/
  public/

Notes:
- Use either Debian netinst or full DVD ISO depending on network availability.
- Place offline docs as HTML/PDF snapshots.

## Ventoy Mode

- Install Ventoy on the USB once, then copy ISOs into `iso/`.
- The HTML manual lives at `docs/ventoy-field-manual.html`.

## Build the ASF Payload

1) Create the distro tarball:

```bash
./scripts/build-distro.sh
```

2) Copy into USB staging:

- `dist/agent-systems-framework-YYYYMMDD.tar.gz`
- `scripts/deploy/install-asf.sh`
- `docs/deploy/install-asf-offline.md`
- `docs/deploy/lost-user-guide.md`

## Offline Resources to Download

Gentoo:
- ISO and stage3: https://www.gentoo.org/downloads/
- Handbook: https://wiki.gentoo.org/wiki/Handbook:AMD64

Arch:
- ISO: https://archlinux.org/download/
- Install guide: https://wiki.archlinux.org/title/Installation_guide

Debian:
- ISO: https://www.debian.org/distrib/

## Assemble USB

Use a staging directory and copy into the USB mount point.

```bash
./scripts/deploy/prepare-usb-kit.sh /path/to/staging /media/usb
```

Optional: generate checksums after copy:

```bash
./scripts/deploy/prepare-usb-kit.sh /path/to/staging /media/usb --checksums
```

## Archive Process

- Record build date, operator, and host in `manifest.txt`
- Store file checksums (sha256) alongside the manifest
- Keep a short log of decisions and versions used

## Lost User Entry Point

Open `docs/lost-user-guide.md` from the USB root.
