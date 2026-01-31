# Quantum Convergence: When to Model Reality Differently

We can treat the system as "quantum" without turning it into mysticism.

Operational meaning:
- quantum = we explicitly represent uncertainty as distributions
- measurement = we commit a decision and collapse uncertainty into a chosen state

## Recommendation

Use a two-layer model:

1) Classical core (deterministic)
- files, schemas, leases, budgets, and audits are deterministic
- execution is reproducible

2) Quantum overlay (probabilistic)
- multiple hypotheses and plans can exist simultaneously
- we track confidence and expected outcomes
- we collapse only at decision/commit boundaries

This gives convergence:
- exploration stays probabilistic
- production execution stays deterministic

## Quantum Primitives (Mapped to Our Tools)

- Superposition (many plausible worlds)
  - stubs + issues represent alternative hypotheses

- Amplitude (weight)
  - store confidence as a number (0..1) in the writeup

- Measurement (collapse)
  - a decision record or a council_call resolution
  - a work item moved to in_progress/done

- Entanglement (coupling)
  - shared resources
  - operationally: oxygen leases + budgets

## Where Quantum Stops

Quantum does not apply to:
- blob immutability
- audit logs
- lease semantics
- schema versions

Those stay classical.

## How to Operationalize Next

Add one new practice:
- every stub/issue includes:
  - confidence
  - expected impact
  - what measurement would change the weight

Then:
- the "knower" uses synthesis to update weights
- the council uses thresholds to decide when to collapse
