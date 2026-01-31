#!/usr/bin/env bash
set -euo pipefail

usb_root="${1:-}"

if [[ -z "${usb_root}" ]]; then
  printf "usage: %s <usb-root>\n" "$0" >&2
  exit 1
fi

if [[ ! -d "${usb_root}" ]]; then
  printf "missing usb root: %s\n" "${usb_root}" >&2
  exit 1
fi

if command -v apt-get >/dev/null 2>&1; then
  deb_pkg=("${usb_root}/browsers/brave/deb/"*.deb)
  sudo dpkg -i "${deb_pkg[@]}" || true
  sudo apt-get -f install
  exit 0
fi

if command -v dnf >/dev/null 2>&1; then
  rpm_pkg=("${usb_root}/browsers/brave/rpm/"*.rpm)
  sudo dnf install "${rpm_pkg[@]}"
  exit 0
fi

if command -v pacman >/dev/null 2>&1; then
  arch_pkg=("${usb_root}/browsers/brave/arch/"*.pkg.tar.zst)
  sudo pacman -U "${arch_pkg[@]}"
  exit 0
fi

printf "unsupported distro or missing package manager\n" >&2
exit 1
