# Toolchain Kit (Offline)

Goal: carry the development stack on the USB so the four agents can compile and operate without network access.

## Agent Toolchains

- Rust agent:
  - `rustup`, `cargo`, stable toolchain
  - components: `rust-src`, `clippy`, `rustfmt`
- C/C++ agent:
  - `gcc`, `g++`, `clang`, `lld`, `make`, `cmake`, `gdb`
- COBOL agent:
  - `gnucobol` (package name varies by distro)
- Emergent agent:
  - `python3`, `pip`, `venv`
  - `node`, `npm`

Optional:
- `go`
- `java` (if needed for tooling)

## USB Layout

```
USBROOT/
  toolchains/
    fedora/
      packages/
      repo/
    debian/
      packages/
      repo/
    arch/
      packages/
      repo/
    gentoo/
      distfiles/
      binpkgs/
```

## Fedora (Host: current system)

- Use `dnf download --resolve` to gather RPMs into `toolchains/fedora/packages/`.
- Build a local repo with `createrepo_c` and store metadata under `toolchains/fedora/repo/`.

## Debian / Ubuntu

- Use `apt-get download` or `apt-get install --download-only` into `toolchains/debian/packages/`.
- Build a local repo with `dpkg-scanpackages` and store under `toolchains/debian/repo/`.

## Arch / Endeavour / Manjaro

- Use `pacman -Sw` to cache packages into `toolchains/arch/packages/`.
- Build a local repo with `repo-add`.

## Gentoo

- Keep distfiles under `toolchains/gentoo/distfiles/`.
- Build binpkgs for offline install and store under `toolchains/gentoo/binpkgs/`.

## Rust Offline Strategy

Two paths:

1) Copy `~/.rustup` and `~/.cargo` to USB (fast, large).
2) Mirror the rustup toolchain and crates into a local cache (cleaner, slower).

## LLM Runtimes

- Ollama: store binary and model files under `llm/ollama/` and `llm/models/`.
- Koboldcpp / llama.cpp: store binaries under `llm/koboldcpp/` and `llm/llama.cpp/`.

## Notes

- Package names vary by distro; keep a per-distro manifest.
- Avoid shipping proprietary tooling unless licensed.
