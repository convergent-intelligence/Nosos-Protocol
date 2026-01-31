# ISO Build Notes (Phase 0)

We will choose one of these when implementing the real ISO build.

## Option A: Debian Installer + Preseed (Recommended)

Pros:
- repeatable, minimal, secure by default
- can provision a user and install packages during install

Cons:
- more fiddly to get 100% unattended

## Option B: Ubuntu Autoinstall

Pros:
- first-class unattended install

Cons:
- ties you to Ubuntu tooling choices

## Option C: Live ISO

Pros:
- great for demos

Cons:
- harder to harden
- easier to accidentally ship state

## Phase 0 Decision

Record in `docs/decisions/0002-iso-build-approach.md`.
