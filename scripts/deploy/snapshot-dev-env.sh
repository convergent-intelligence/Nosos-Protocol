#!/usr/bin/env bash
set -euo pipefail

out_file="${1:-}"

if [[ -z "${out_file}" ]]; then
  printf "usage: %s <output-file>\n" "$0" >&2
  exit 1
fi

{
  printf "Host: %s\n" "$(uname -a)"
  printf "Date: %s\n\n" "$(date -u)"

  printf "Toolchain binaries:\n"
  command -v rustc cargo rustup gcc g++ clang lld gdb cmake make cobc python3 pip node npm go || true
  printf "\n"

  printf "Versions:\n"
  rustc --version 2>/dev/null || true
  cargo --version 2>/dev/null || true
  rustup --version 2>/dev/null || true
  gcc --version 2>/dev/null || true
  g++ --version 2>/dev/null || true
  clang --version 2>/dev/null || true
  cobc --version 2>/dev/null || true
  python3 --version 2>/dev/null || true
  node --version 2>/dev/null || true
  npm --version 2>/dev/null || true
  go version 2>/dev/null || true
  printf "\n"
} > "${out_file}"

printf "wrote: %s\n" "${out_file}"
