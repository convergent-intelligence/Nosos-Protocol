# Context Capsule: TSP exact + heuristic + verifier

Work ID: QAI-001
Kind: plan
Domain: scribe
Priority: high
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:29:24Z

## Objective

Testable proof-of-capability: exact Held-Karp for irrefutable optima; heuristic baseline; solution verifier

## Boundaries

In scope:
- Execute this work item exactly as written.
Out of scope:
- Redesign unrelated systems or expand scope without a new item.

## Invariants

- Do not delete originals during automation.
- Blob storage remains content-addressed and immutable.
- Actions remain auditable (append-only log).

## Touch Points

Files linked on the item:
- `docs/math/tsp-lab.md`
- `tools/qai/tsp.py`
- `scripts/tsp`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-052559_proclamation_plan.json`
- `.bridges/signals/20260130-051335_proclamation_plan.json`
- `.bridges/signals/20260130-051335_missive_assignment.json`
- `.bridges/signals/20260130-051043_proclamation_plan.json`
- `.bridges/signals/20260130-050544_proclamation_plan.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/math/tsp-lab.md`

```
# TSP Lab (Testable, Reproducible)

This is a credibility demo:
- deterministic instance generation
- exact solver for small n (irrefutable optimality)
- verifier for claimed solutions

## Quick Demo

```bash
./scripts/tsp self-test
./scripts/tsp demo --n 12 --seed 17 --grid 100
```

## Reproducible Evidence Run

1) Generate an instance:

```bash
./scripts/tsp generate --n 14 --seed 42 --grid 200 --out artifacts/math/tsp_n14_seed42.json
```

2) Solve exactly:

```bash
./scripts/tsp solve --input artifacts/math/tsp_n14_seed42.json --method exact --out artifacts/math/tsp_n14_seed42_exact.json
```

3) Verify the solution (independent check):

```bash
./scripts/tsp verify --input artifacts/math/tsp_n14_seed42.json --solution artifacts/math/tsp_n14_seed42_exact.json
```

## Notes

- Exact method is Held-Karp DP (O(n^2 2^n)); keep n small.
- Metric is Manhattan (L1) to keep distances integer and deterministic.
```

### `tools/qai/tsp.py`

```
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _dist_l1(p: tuple[int, int], q: tuple[int, int]) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def _tour_length(points: list[tuple[int, int]], tour: list[int]) -> int:
    n = len(points)
    if len(tour) != n:
        raise ValueError("tour length mismatch")
    total = 0
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]
        total += _dist_l1(points[a], points[b])
    return total


def _verify_tour(n: int, tour: list[int]) -> None:
    if len(tour) != n:
        raise ValueError(f"expected {n} nodes, got {len(tour)}")
    seen = set(tour)
    if len(seen) != n:
        raise ValueError("tour has duplicates")
    if min(seen) != 0 or max(seen) != n - 1:
        raise ValueError("tour indices out of range")


def generate_instance(n: int, *, seed: int, grid: int) -> dict:
    rng = random.Random(seed)
    pts: list[tuple[int, int]] = []
    used = set()
    while len(pts) < n:
        x = rng.randrange(0, grid)
        y = rng.randrange(0, grid)
        if (x, y) in used:
            continue
        used.add((x, y))
        pts.append((x, y))
    return {
        "name": f"tsp_l1_n{n}_seed{seed}",
        "metric": "l1",
        "grid": grid,
        "seed": seed,
        "points": [{"x": x, "y": y} for x, y in pts],
    }


def _points_from_instance(inst: dict) -> list[tuple[int, int]]:
    if inst.get("metric") != "l1":
        raise ValueError("only metric=l1 supported")
    pts = []
    for p in inst.get("points", []):
        pts.append((int(p["x"]), int(p["y"])))
    return pts


def nearest_neighbor(points: list[tuple[int, int]], start: int = 0) -> list[int]:
    n = len(points)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: _dist_l1(points[cur], points[j]))
        unvisited.remove(nxt)
        tour.append(nxt)
        cur = nxt
    return tour


def two_opt(points: list[tuple[int, int]], tour: list[int], *, max_passes: int = 50) -> list[int]:
    n = len(points)
    best = tour[:]
    best_len = _tour_length(points, best)

    for _ in range(max_passes):
        improved = False
        for i in range(1, n - 2):
            for k in range(i + 1, n - 1):
                a, b = best[i - 1], best[i]
                c, d = best[k], best[(k + 1) % n]
                # delta if we reverse segment [i..k]
                before = _dist_l1(points[a], points[b]) + _dist_l1(points[c], points[d])
                after = _dist_l1(points[a], points[c]) + _dist_l1(points[b], points[d])
                if after < before:
                    best[i : k + 1] = reversed(best[i : k + 1])
                    best_len = best_len - before + after
                    improved = True
        if not improved:
            break
    return best


@dataclass(frozen=True)
class ExactResult:
    tour: list[int]
    length: int
    states: int

(truncated: 338 lines total)
```

### `scripts/tsp`

```
#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

exec python3 "${root_dir}/tools/qai/tsp.py" "$@"
```

