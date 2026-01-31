#!/usr/bin/env bash
set -euo pipefail

src_dir="${1:-}"
usb_dir="${2:-}"
checksums="${3:-}"

if [[ -z "${src_dir}" || -z "${usb_dir}" ]]; then
  printf "usage: %s <staging-dir> <usb-mount> [--checksums]\n" "$0" >&2
  exit 1
fi

if [[ ! -d "${src_dir}" ]]; then
  printf "missing staging dir: %s\n" "${src_dir}" >&2
  exit 1
fi

if [[ ! -d "${usb_dir}" ]]; then
  printf "missing usb mount: %s\n" "${usb_dir}" >&2
  exit 1
fi

cp -a "${src_dir}/." "${usb_dir}/"

if [[ "${checksums}" == "--checksums" ]]; then
  if command -v sha256sum >/dev/null 2>&1; then
    (
      cd "${usb_dir}"
      find . -type f -print0 | sort -z | xargs -0 sha256sum > manifest.sha256
    )
    printf "wrote checksums: %s/manifest.sha256\n" "${usb_dir}"
  else
    printf "sha256sum not available; skipping checksums\n" >&2
  fi
fi

printf "copied staging to usb: %s -> %s\n" "${src_dir}" "${usb_dir}"
