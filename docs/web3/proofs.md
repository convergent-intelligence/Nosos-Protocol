# Blockchain Proof of Discoveries

Goal: provide cryptographic, portable proof that a discovery existed at a time, with evidence.

We do this in layers:

Layer 0 (now): local, deterministic attestation
- compute hashes of evidence files
- compute a Merkle root
- compute a canonical attestation hash
- store the attestation in-repo as an artifact

Layer 1 (web3 login): wallet signature
- user signs the attestation hash (or typed data)
- signature is stored with the attestation

Layer 2 (on-chain): anchor
- submit the attestation hash (or Merkle root) to a chain
- store tx hash back in the attestation

## Why This Helps All Substrates

- Any agent can produce an attestation.
- Any verifier can re-hash evidence and confirm the same digest.
- Wallet signature provides accountability without identity disclosure.

## Artifact Format

Attestations live in:
- `artifacts/proofs/`

Each attestation contains:
- claim
- evidence file list with SHA-256
- Merkle root
- canonical attestation hash
- optional wallet signature
- optional on-chain tx hash

## Tooling

- Create an attestation:

```bash
./scripts/proof create --title "TSP exact optimum n=14" --claim "Held-Karp yields optimal tour length 990" \
  --evidence artifacts/math/tsp_n14_seed42.json \
  --evidence artifacts/math/tsp_n14_seed42_exact.json
```

This writes an attestation JSON and prints its hash.
