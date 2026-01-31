# Content Stubs (Download Queue)

Use this file as the authoritative list of downloads. Items are listed as placeholders so the kit can be structured before files arrive.
If you see `.stub` files on the USB, they are intentional placeholders.

## OS ISOs

Common:
- `iso/common/debian-12.x.x-amd64-netinst.iso`  https://www.debian.org/distrib/
- `iso/common/debian-12.x.x-amd64-DVD-1.iso`    https://www.debian.org/distrib/
- `iso/common/fedora-YYYY.iso`                  https://getfedora.org/
- `iso/common/ubuntu-YYYY.iso`                  https://ubuntu.com/download
- `iso/common/linuxmint-YYYY.iso`               https://linuxmint.com/download.php
- `iso/common/popos-YYYY.iso`                   https://pop.system76.com/

Uncommon:
- `iso/uncommon/gentoo-minimal-YYYYMMDD.iso`    https://www.gentoo.org/downloads/
- `iso/uncommon/archlinux-YYYY.MM.DD-x86_64.iso` https://archlinux.org/download/
- `iso/uncommon/alpine-YYYY.iso`                https://alpinelinux.org/downloads/
- `iso/uncommon/void-YYYY.iso`                  https://voidlinux.org/download/

Privacy:
- `iso/privacy/tails-YYYY.iso`                  https://tails.net/

Rescue:
- `iso/rescue/systemrescue-YYYY.iso`            https://www.system-rescue.org/
- `iso/rescue/gparted-YYYY.iso`                 https://gparted.org/livecd.php
- `iso/rescue/rescuezilla-YYYY.iso`             https://rescuezilla.com/
- `iso/rescue/clonezilla-YYYY.iso`              https://clonezilla.org/

## VM Images

- `vm/whonix/whonix-gateway.ova`                 https://www.whonix.org/wiki/Download
- `vm/whonix/whonix-workstation.ova`             https://www.whonix.org/wiki/Download

## Knowledge (Offline)

Kiwix ZIMs:
- Wikipedia (en)
- Wiktionary (en)
- Wikibooks (math/science)
Source: https://library.kiwix.org/

Programming references:
- Rust book + std docs
- Python docs
- C/C++ references
- Linux manpages

## Games and Learning

- Puzzle packs (PDF)
- Logic grids
- Math games
- Science activity sheets

## LLM Runtimes and Models

Runtimes:
- Ollama (Linux)
- llama.cpp (prebuilt)
- koboldcpp (prebuilt)

Models:
- Small/medium GGUF models that fit the device

## Web3 Browser

- Brave packages for deb/rpm/arch
See `docs/deploy/brave-offline.md`.

## Toolchains

- Rust toolchain cache
- gcc/clang toolchain packages
- gnucobol packages
- python/node packages
See `docs/deploy/toolchain-kit.md`.

## Licensing

Only include proprietary media if you own valid licenses.
