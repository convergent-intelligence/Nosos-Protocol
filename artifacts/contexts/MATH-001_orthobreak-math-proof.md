# Context Capsule: OrthoBreak math proof

Work ID: MATH-001
Kind: plan
Domain: scribe
Priority: medium
Status: pending
Owner: unassigned
Generated: 2026-01-30T05:25:59Z

## Objective

Novel billiards/Breakout periodicity problem using lcm/gcd and CRT

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
- `docs/math/orthobreak.md`

Commands:

```bash
./scripts/validate.sh
./scripts/health.sh
```

## Current State

- Health: yellow
- AutoFile: blobs=5 units=6 quarantined_units=2

Recent signals:
- `.bridges/signals/20260130-051335_proclamation_plan.json`
- `.bridges/signals/20260130-051335_missive_assignment.json`
- `.bridges/signals/20260130-051043_proclamation_plan.json`
- `.bridges/signals/20260130-050544_proclamation_plan.json`
- `.bridges/signals/20260130-050543_missive_assignment.json`

## Drift Guards

- Do not pull in extra context unless the capsule says so.
- If you need more than 5 files, stop and create a stub explaining why.
- If the task is ambiguous, stop and emit a council_call signal.

## Embedded Context

### `docs/math/orthobreak.md`

```
# OrthoBreak: A Periodic Breakout Problem

This is a novel math problem framed as Breakout (billiards-in-a-rectangle).

It connects directly to our system:
- strict counts (periodic table Z)
- deterministic core (classical)
- measured checkpoints (field)

## The Game Model

Board is a rectangle of width W and height H.

A ball moves with constant velocity vector (a, b) and reflects specularly off the walls.
No paddle needed; this is pure geometry.

## The Problem (Neon / Magnesium / Chlorine)

Pick:

- W = 17  (Cl)
- H = 10  (Ne)
- (a, b) = (12, 17) (Mg, Cl)

Start the ball at (0, 0).

Questions:

1) After how many steps does the full state repeat (same position and same direction)?
2) After how many steps does the ball hit a corner?

## The Unfolding Trick (Core Insight)

Reflecting in a rectangle is equivalent to moving in a straight line on an unfolded plane.

Instead of reflecting the ball, reflect the room.

Then the position after t steps is:

- X(t) = a t
- Y(t) = b t

but interpreted modulo (2W, 2H) to account for reflections.

So the state repeats when:

  a t == 0 (mod 2W)
  b t == 0 (mod 2H)

The smallest such t is:

  T = lcm( 2W / gcd(2W, a), 2H / gcd(2H, b) )

## Solution

Here:

- 2W = 34, gcd(34, 12) = 2  -> 34/2 = 17
- 2H = 20, gcd(20, 17) = 1  -> 20/1 = 20

So:

  T = lcm(17, 20) = 340

Answer (1): the full state repeats after 340 steps.

Corner hits (in the original rectangle) occur when the unfolded position lands on the W-by-H lattice:

  a t == 0 (mod W)
  b t == 0 (mod H)

Smallest such t is:

  Tc = lcm( W / gcd(W, a), H / gcd(H, b) )

Compute:

- W=17, gcd(17,12)=1 -> 17
- H=10, gcd(10,17)=1 -> 10

  Tc = lcm(17,10) = 170

Answer (2): the ball hits a corner every 170 steps.

## Why This Is Interesting

- The period 340 is the CRT signature of two independent cycles (17 and 20).
- This is the same math as orchestration:
  - independent subsystem cycles combine via lcm
  - collisions correspond to simultaneous congruences

## Generalization

For any W,H and integer direction (a,b):

- Full state period:
  T = lcm( 2W/gcd(2W,a), 2H/gcd(2H,b) )

- Corner-hit period:
  Tc = lcm( W/gcd(W,a), H/gcd(H,b) )
```

