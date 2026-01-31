#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def _utc_now_rfc3339() -> str:
    return _utc_now().isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _leases_dir(root: Path) -> Path:
    return root / ".substrate" / "state" / "leases"


def _read_budgets(root: Path) -> dict:
    # Minimal YAML-ish parser for .substrate/constants/budgets.yaml.
    # Supports nested keys by reading any `k: v` line.
    path = root / ".substrate" / "constants" / "budgets.yaml"
    defaults = {"max_leases_per_domain": 2}
    if not path.exists():
        return defaults
    out = dict(defaults)
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k in out:
            try:
                out[k] = int(v)
            except Exception:
                pass
    return out


def _safe_name(resource: str) -> str:
    s = resource.strip().lower()
    s = re.sub(r"[^a-z0-9_.:-]+", "_", s)
    return s[:180] or "resource"


def _lease_path(root: Path, resource: str) -> Path:
    return _leases_dir(root) / f"{_safe_name(resource)}.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_expired(lease: dict) -> bool:
    exp = lease.get("expires_at")
    if not exp:
        return False
    try:
        t = dt.datetime.fromisoformat(exp.replace("Z", "+00:00"))
    except Exception:
        return False
    return _utc_now() >= t


def list_leases(root: Path) -> list[dict]:
    d = _leases_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    out: list[dict] = []
    for p in sorted(d.glob("*.json")):
        try:
            lease = _read_json(p)
        except Exception:
            continue
        lease["_path"] = str(p.relative_to(root))
        lease["_expired"] = _is_expired(lease)
        out.append(lease)
    return out


def _active_leases_by_domain(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for lease in list_leases(root):
        if lease.get("_expired"):
            continue
        domain = str(lease.get("domain") or "")
        if not domain:
            continue
        counts[domain] = counts.get(domain, 0) + 1
    return counts


def gc(root: Path) -> dict:
    d = _leases_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    removed = 0
    for p in d.glob("*.json"):
        try:
            lease = _read_json(p)
        except Exception:
            continue
        if _is_expired(lease):
            try:
                p.unlink()
                removed += 1
            except Exception:
                pass
    return {"removed": removed, "ts": _utc_now_rfc3339()}


def claim(
    root: Path,
    *,
    resource: str,
    owner: str,
    domain: str,
    ttl: int,
    override: bool,
    reason: str | None,
) -> dict:
    d = _leases_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    p = _lease_path(root, resource)

    budgets = _read_budgets(root)
    max_leases = int(budgets.get("max_leases_per_domain", 2))
    counts = _active_leases_by_domain(root)
    current = counts.get(domain, 0)
    if current >= max_leases and not override:
        raise SystemExit(f"lease budget exceeded for domain={domain} ({current}/{max_leases}); use --override --reason or wait")
    if current >= max_leases and override and not reason:
        raise SystemExit("--override requires --reason")

    if p.exists():
        lease = _read_json(p)
        if not _is_expired(lease):
            raise SystemExit(f"lease exists: {resource} (owner={lease.get('owner')}, expires_at={lease.get('expires_at')})")
        # expired lease: remove it
        try:
            p.unlink()
        except Exception:
            pass

    created = _utc_now()
    expires = created + dt.timedelta(seconds=int(ttl))
    lease = {
        "resource": resource,
        "owner": owner,
        "domain": domain,
        "ttl_seconds": int(ttl),
        "created_at": created.isoformat().replace("+00:00", "Z"),
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
        "override": bool(override),
        "override_reason": reason or "",
    }

    # Atomic create
    fd = os.open(str(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(lease, indent=2, sort_keys=True) + "\n")
    lease["_path"] = str(p.relative_to(root))
    return lease


def release(root: Path, *, resource: str, owner: str | None) -> dict:
    p = _lease_path(root, resource)
    if not p.exists():
        raise SystemExit(f"no lease for: {resource}")
    lease = _read_json(p)
    if owner is not None and lease.get("owner") != owner:
        raise SystemExit(f"lease owned by {lease.get('owner')}, not {owner}")
    p.unlink()
    return {"released": resource, "ts": _utc_now_rfc3339()}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="oxygen")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="list leases")
    p_list.add_argument("--json", action="store_true")

    p_claim = sub.add_parser("claim", help="claim a lease")
    p_claim.add_argument("resource")
    p_claim.add_argument("--owner", required=True)
    p_claim.add_argument("--domain", required=True)
    p_claim.add_argument("--ttl", type=int, default=1800)
    p_claim.add_argument("--override", action="store_true")
    p_claim.add_argument("--reason")

    p_release = sub.add_parser("release", help="release a lease")
    p_release.add_argument("resource")
    p_release.add_argument("--owner")

    p_gc = sub.add_parser("gc", help="remove expired leases")

    args = ap.parse_args(argv)
    root = _resolve_root()

    if args.cmd == "list":
        leases = list_leases(root)
        if args.json:
            print(json.dumps(leases, indent=2, sort_keys=True))
        else:
            for l in leases:
                status = "expired" if l.get("_expired") else "active"
                print(f"{l.get('resource')} owner={l.get('owner')} domain={l.get('domain')} expires_at={l.get('expires_at')} ({status})")
        return 0

    if args.cmd == "claim":
        lease = claim(
            root,
            resource=args.resource,
            owner=args.owner,
            domain=args.domain,
            ttl=args.ttl,
            override=bool(args.override),
            reason=args.reason,
        )
        print(json.dumps(lease, indent=2, sort_keys=True))
        return 0

    if args.cmd == "release":
        res = release(root, resource=args.resource, owner=args.owner)
        print(json.dumps(res, indent=2, sort_keys=True))
        return 0

    if args.cmd == "gc":
        res = gc(root)
        print(json.dumps(res, indent=2, sort_keys=True))
        return 0

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
