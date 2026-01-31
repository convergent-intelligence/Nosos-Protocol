#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path


def die(msg: str) -> None:
    raise SystemExit(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_cmd(name: str) -> str:
    p = shutil.which(name)
    if not p:
        die(f"missing prerequisite: {name}")
    return p


def extract_iso(xorriso: str, base_iso: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [xorriso, "-osirrox", "on", "-indev", str(base_iso), "-extract", "/", str(out_dir)],
        check=True,
    )


def patch_boot_configs(root: Path, preseed_path: str) -> int:
    changed = 0

    def patch_file(p: Path) -> None:
        nonlocal changed
        text = p.read_text(encoding="utf-8", errors="replace")
        new = text

        # ISOLINUX: append ... ---
        if "append" in text:
            new = re.sub(
                r"(\bappend\b[^\n]*?)\s+---",
                r"\1 auto=true priority=critical preseed/file=" + preseed_path + r" ---",
                new,
            )

        # GRUB: linux ... ---
        if "linux" in text:
            new = re.sub(
                r"(\blinux\b[^\n]*?)\s+---",
                r"\1 auto=true priority=critical preseed/file=" + preseed_path + r" ---",
                new,
            )

        if new != text:
            p.write_text(new, encoding="utf-8")
            changed += 1

    candidates = [
        root / "isolinux" / "txt.cfg",
        root / "isolinux" / "isolinux.cfg",
        root / "boot" / "grub" / "grub.cfg",
        root / "EFI" / "BOOT" / "grub.cfg",
    ]

    for p in candidates:
        if p.exists() and p.is_file():
            patch_file(p)

    return changed


def write_md5sum(root: Path) -> bool:
    md5_path = root / "md5sum.txt"
    if not md5_path.exists():
        return False

    entries = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = p.relative_to(root)
            if str(rel) == "md5sum.txt":
                continue
            # Debian uses ./path format
            digest = hashlib.md5(p.read_bytes()).hexdigest()  # noqa: S324
            entries.append(f"{digest}  ./{rel.as_posix()}")

    entries.sort()
    md5_path.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return True


def build_iso(xorriso: str, base_iso: Path, iso_root: Path, out_iso: Path) -> None:
    out_iso.parent.mkdir(parents=True, exist_ok=True)
    if out_iso.exists():
        out_iso.unlink()
    subprocess.run(
        [
            xorriso,
            "-indev",
            str(base_iso),
            "-outdev",
            str(out_iso),
            "-map",
            str(iso_root),
            "/",
            "-boot_image",
            "any",
            "replay",
        ],
        check=True,
    )


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="repack-debian-iso")
    ap.add_argument("--base-iso", required=True)
    ap.add_argument("--distro", required=True)
    ap.add_argument("--preseed", required=True)
    ap.add_argument("--out-iso", required=True)
    ap.add_argument("--work-dir", required=True)
    args = ap.parse_args(argv)

    xorriso = require_cmd("xorriso")

    base_iso = Path(args.base_iso).expanduser().resolve()
    distro = Path(args.distro).expanduser().resolve()
    preseed = Path(args.preseed).expanduser().resolve()
    out_iso = Path(args.out_iso).expanduser().resolve()
    work_dir = Path(args.work_dir).expanduser().resolve()

    if not base_iso.is_file():
        die(f"missing base iso: {base_iso}")
    if not distro.is_file():
        die(f"missing distro tarball: {distro}")
    if not preseed.is_file():
        die(f"missing preseed: {preseed}")

    iso_root = work_dir / "iso-root"
    if iso_root.exists():
        shutil.rmtree(iso_root)

    extract_iso(xorriso, base_iso, iso_root)

    # Payload layout
    asf_dir = iso_root / "asf"
    asf_dir.mkdir(parents=True, exist_ok=True)

    # Copy distro tarball to a stable name
    target_distro = asf_dir / "agent-systems-framework.tar.gz"
    shutil.copy2(distro, target_distro)

    # Copy installer helper
    repo_root = Path(__file__).resolve().parents[2]
    install_sh = repo_root / "scripts" / "deploy" / "install-asf.sh"
    if not install_sh.exists():
        die(f"missing install script in repo: {install_sh}")
    shutil.copy2(install_sh, asf_dir / "install-asf.sh")

    # Copy preseed to ISO root
    shutil.copy2(preseed, iso_root / "preseed.cfg")

    changed = patch_boot_configs(iso_root, "/cdrom/preseed.cfg")
    wrote_md5 = write_md5sum(iso_root)

    build_iso(xorriso, base_iso, iso_root, out_iso)

    print(f"built: {out_iso}")
    print(f"base_sha256: {sha256(base_iso)}")
    print(f"out_sha256: {sha256(out_iso)}")
    print(f"boot_cfg_patched_files: {changed}")
    print(f"md5sum_updated: {wrote_md5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
