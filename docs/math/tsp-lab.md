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
