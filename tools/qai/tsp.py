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


def held_karp(points: list[tuple[int, int]]) -> ExactResult:
    """Exact TSP via Held-Karp dynamic programming.

    Fix start at 0; DP over subsets of {1..n-1}.
    """

    n = len(points)
    if n < 2:
        return ExactResult(tour=[0], length=0, states=0)

    # dp[(mask, j)] = (cost, prev)
    # mask covers nodes 1..n-1 (bit i-1 corresponds to node i)
    dp: dict[tuple[int, int], tuple[int, int]] = {}
    states = 0

    # Initialize: paths from 0 to j
    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[(mask, j)] = (_dist_l1(points[0], points[j]), 0)
        states += 1

    full_mask = (1 << (n - 1)) - 1
    for mask in range(1, full_mask + 1):
        # skip singletons; already initialized
        if mask & (mask - 1) == 0:
            continue
        for j in range(1, n):
            bit = 1 << (j - 1)
            if mask & bit == 0:
                continue
            prev_mask = mask ^ bit
            best = None
            best_prev = -1
            for k in range(1, n):
                kbit = 1 << (k - 1)
                if prev_mask & kbit == 0:
                    continue
                prev = dp.get((prev_mask, k))
                if prev is None:
                    continue
                cand = prev[0] + _dist_l1(points[k], points[j])
                if best is None or cand < best:
                    best = cand
                    best_prev = k
            if best is not None:
                dp[(mask, j)] = (best, best_prev)
                states += 1

    # Close tour back to 0
    best_cost = None
    best_last = -1
    for j in range(1, n):
        val = dp.get((full_mask, j))
        if val is None:
            continue
        cand = val[0] + _dist_l1(points[j], points[0])
        if best_cost is None or cand < best_cost:
            best_cost = cand
            best_last = j

    if best_cost is None:
        raise RuntimeError("dp failed")

    # Reconstruct
    tour = [0] * n
    mask = full_mask
    last = best_last
    for i in range(n - 1, 0, -1):
        tour[i] = last
        bit = 1 << (last - 1)
        prev_cost, prev = dp[(mask, last)]
        mask ^= bit
        last = prev
    tour[0] = 0
    _verify_tour(n, tour)
    return ExactResult(tour=tour, length=int(best_cost), states=states)


def cmd_generate(args: argparse.Namespace) -> int:
    inst = generate_instance(int(args.n), seed=int(args.seed), grid=int(args.grid))
    out = Path(args.out).expanduser().resolve() if args.out else None
    if out:
        _write_json(out, inst)
        print(str(out))
    else:
        print(json.dumps(inst, indent=2, sort_keys=True))
    return 0


def cmd_solve(args: argparse.Namespace) -> int:
    inst = _read_json(Path(args.input).expanduser().resolve())
    points = _points_from_instance(inst)
    n = len(points)
    method = args.method

    if method == "exact":
        if n > int(args.max_n):
            raise SystemExit(f"n={n} too large for exact; set --max-n higher at your own risk")
        res = held_karp(points)
        out = {
            "method": "exact",
            "n": n,
            "length": res.length,
            "tour": res.tour,
            "states": res.states,
        }
    elif method == "2opt":
        tour0 = nearest_neighbor(points, start=0)
        tour = two_opt(points, tour0)
        out = {
            "method": "2opt",
            "n": n,
            "length": _tour_length(points, tour),
            "tour": tour,
        }
    else:
        raise SystemExit("unknown method")

    out_path = Path(args.out).expanduser().resolve() if args.out else None
    if out_path:
        _write_json(out_path, out)
        print(str(out_path))
    else:
        print(json.dumps(out, indent=2, sort_keys=True))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    inst = _read_json(Path(args.input).expanduser().resolve())
    points = _points_from_instance(inst)
    n = len(points)
    sol = _read_json(Path(args.solution).expanduser().resolve())
    tour = list(map(int, sol.get("tour", [])))
    _verify_tour(n, tour)
    length = _tour_length(points, tour)
    expected = sol.get("length")
    ok = expected is None or int(expected) == int(length)
    if not ok:
        raise SystemExit(f"length mismatch: claimed={expected} computed={length}")
    print(json.dumps({"ok": True, "n": n, "length": length}, indent=2, sort_keys=True))
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    # Deterministic demo instance.
    inst = generate_instance(int(args.n), seed=int(args.seed), grid=int(args.grid))
    points = _points_from_instance(inst)
    exact = held_karp(points) if len(points) <= int(args.max_n) else None
    heur_tour = two_opt(points, nearest_neighbor(points, 0))
    heur_len = _tour_length(points, heur_tour)

    out: dict[str, Any] = {
        "instance": {"n": len(points), "seed": inst["seed"], "grid": inst["grid"], "metric": inst["metric"]},
        "heuristic": {"method": "2opt", "length": heur_len},
    }
    if exact is not None:
        out["exact"] = {"method": "held_karp", "length": exact.length, "states": exact.states}
        out["gap"] = {"heur_minus_opt": heur_len - exact.length}

    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


def cmd_self_test(args: argparse.Namespace) -> int:
    # Square (0,0),(1,0),(1,1),(0,1) in L1: optimal tour length is 4.
    inst = {
        "metric": "l1",
        "points": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}, {"x": 0, "y": 1}],
    }
    points = _points_from_instance(inst)
    res = held_karp(points)
    if res.length != 4:
        raise SystemExit(f"self-test failed: expected 4, got {res.length}")
    print(json.dumps({"ok": True, "case": "square", "opt": res.length}, indent=2, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="tsp")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--n", default="12")
    g.add_argument("--seed", default="17")
    g.add_argument("--grid", default="100")
    g.add_argument("--out")
    g.set_defaults(fn=cmd_generate)

    s = sub.add_parser("solve")
    s.add_argument("--input", required=True)
    s.add_argument("--method", choices=["exact", "2opt"], default="exact")
    s.add_argument("--max-n", default="18")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_solve)

    v = sub.add_parser("verify")
    v.add_argument("--input", required=True)
    v.add_argument("--solution", required=True)
    v.set_defaults(fn=cmd_verify)

    d = sub.add_parser("demo")
    d.add_argument("--n", default="12")
    d.add_argument("--seed", default="17")
    d.add_argument("--grid", default="100")
    d.add_argument("--max-n", default="18")
    d.set_defaults(fn=cmd_demo)

    t = sub.add_parser("self-test")
    t.set_defaults(fn=cmd_self_test)

    args = ap.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
