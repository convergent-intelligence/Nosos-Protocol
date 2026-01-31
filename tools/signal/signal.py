#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path


def _utc_now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_root() -> Path:
    env = os.environ.get("ASF_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _signal_id() -> str:
    # Timestamp-based id, stable enough for file naming.
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")


def write_signal(
    root: Path,
    kind: str,
    *,
    topic: str,
    claim: str,
    from_: str,
    to: str,
    urgency: str,
    expects_response: bool,
    response_by: str | None,
    evidence: list[str],
    asks: list[str],
    next_actions: list[str],
) -> Path:
    sig = {
        "header": {
            "id": _signal_id(),
            "timestamp": _utc_now_rfc3339(),
            "from": from_,
            "to": to,
            "kind": kind,
            "urgency": urgency,
        },
        "body": {
            "topic": topic,
            "claim": claim,
            "evidence": evidence,
            "confidence": "medium",
            "asks": asks,
            "next_actions": next_actions,
        },
        "footer": {
            "expects_response": expects_response,
            "response_by": response_by or "",
        },
    }

    out_dir = root / ".bridges" / "signals"
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{sig['header']['id']}_{kind}_{topic.replace(' ', '_')}.json"
    path = out_dir / fname
    path.write_text(json.dumps(sig, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="signal")
    parser.add_argument("kind", choices=["proclamation", "missive", "council_call"])
    parser.add_argument("--topic", required=True)
    parser.add_argument("--claim", required=True)
    parser.add_argument("--from", dest="from_", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--urgency", default="normal", choices=["low", "normal", "high", "critical"])
    parser.add_argument("--expects-response", action="store_true")
    parser.add_argument("--response-by")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--ask", action="append", default=[])
    parser.add_argument("--next", action="append", default=[])
    args = parser.parse_args(argv)

    root = _resolve_root()
    p = write_signal(
        root,
        args.kind,
        topic=args.topic,
        claim=args.claim,
        from_=args.from_,
        to=args.to,
        urgency=args.urgency,
        expects_response=bool(args.expects_response),
        response_by=args.response_by,
        evidence=list(args.evidence),
        asks=list(args.ask),
        next_actions=list(args.next),
    )
    print(str(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
