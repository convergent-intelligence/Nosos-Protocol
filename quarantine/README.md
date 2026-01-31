# Quarantine

Files/units that should not be automatically routed live here.

Common reasons:
- unknown file type
- low confidence classification
- suspected secrets
- conflicting routing rules

Phase 0: AutoFile does not implement secret scanning yet; this is the landing zone once it does.

Current behavior:
- AutoFile writes quarantine markers to `quarantine/<unit-id>.json` when it detects likely secrets.
