#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

autofile_status="$("${root_dir}/scripts/autofile" status)"

failed_inbox=0
if [[ -d "${root_dir}/inbox/failed" ]]; then
  failed_inbox="$(ls -1 "${root_dir}/inbox/failed" 2>/dev/null | wc -l | tr -d ' ')"
fi

health="green"
if [[ "${failed_inbox}" -gt 0 ]]; then
  health="red"
fi

# quarantined is often expected; mark yellow unless already red
quarantined_units="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("quarantined_units",0))' <<<"${autofile_status}")"
if [[ "${health}" != "red" && "${quarantined_units}" -gt 0 ]]; then
  health="yellow"
fi

export TS="${ts}"
export HEALTH="${health}"
export FAILED_INBOX="${failed_inbox}"
export AUTOFILE_STATUS="${autofile_status}"

out="$(python3 - <<'PY'
import json, os, sys

ts = os.environ["TS"]
health = os.environ["HEALTH"]
failed_inbox = int(os.environ["FAILED_INBOX"])
status = json.loads(os.environ["AUTOFILE_STATUS"])

print(json.dumps({
  "ts": ts,
  "health": health,
  "inbox_failed": failed_inbox,
  "autofile": status,
}, indent=2))
PY
)"

state_dir="${root_dir}/.substrate/state"
mkdir -p "${state_dir}"
printf "%s\n" "${out}" > "${state_dir}/health.json"

printf "%s\n" "${out}"
