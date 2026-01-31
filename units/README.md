# Units

A unit is a folder that represents one coherent thing (an entity):
- a document set
- a meeting
- a dataset
- a feature
- a case/incident

The unit folder is human-facing.
The index in `index/autofile.sqlite` is the machine-facing source of truth.

Each unit contains:
- `unit.yaml` (stable metadata)
- `attachments.jsonl` (append-only attachment records)
- `notes.md` (optional)
