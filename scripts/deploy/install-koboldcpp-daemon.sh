#!/usr/bin/env bash
set -euo pipefail

usb_root="${1:-}"
model_path="${2:-}"

if [[ -z "${usb_root}" ]]; then
  printf "usage: %s <usb-root> [model-path]\n" "$0" >&2
  exit 1
fi

if [[ ! -d "${usb_root}" ]]; then
  printf "missing usb root: %s\n" "${usb_root}" >&2
  exit 1
fi

runtime_dir="${usb_root}/llm/koboldcpp"
bin_path="${runtime_dir}/koboldcpp-linux"
run_script="${runtime_dir}/run-koboldcpp.sh"
env_file="${runtime_dir}/koboldcpp.env"

mkdir -p "${runtime_dir}"

if [[ -z "${model_path}" ]]; then
  model_path="${usb_root}/llm/models/gguf-medium.gguf"
fi

cat > "${env_file}" <<EOF
KCPP_MODEL="${model_path}"
KCPP_PORT="5001"
KCPP_CTX="4096"
KCPP_ARGS=""
EOF

cat > "${run_script}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_file="${dir}/koboldcpp.env"

if [[ -f "${env_file}" ]]; then
  # shellcheck disable=SC1090
  source "${env_file}"
fi

bin_path="${dir}/koboldcpp-linux"
if [[ ! -x "${bin_path}" ]]; then
  printf "missing koboldcpp binary: %s\n" "${bin_path}" >&2
  exit 1
fi

if [[ -z "${KCPP_MODEL:-}" || ! -f "${KCPP_MODEL}" ]]; then
  printf "missing model: %s\n" "${KCPP_MODEL:-unset}" >&2
  exit 1
fi

port="${KCPP_PORT:-5001}"
ctx="${KCPP_CTX:-4096}"
threads="${KCPP_THREADS:-}"
args="${KCPP_ARGS:-}"

if [[ -z "${threads}" ]]; then
  if command -v nproc >/dev/null 2>&1; then
    threads="$(nproc)"
  else
    threads="4"
  fi
fi

exec "${bin_path}" \
  --model "${KCPP_MODEL}" \
  --port "${port}" \
  --threads "${threads}" \
  --contextsize "${ctx}" \
  ${args}
EOF

chmod +x "${run_script}"

service_dir="${HOME}/.config/systemd/user"
mkdir -p "${service_dir}"

cat > "${service_dir}/koboldcpp.service" <<EOF
[Unit]
Description=Koboldcpp local LLM server (USB workspace)
After=network.target

[Service]
Type=simple
ExecStart=${run_script}
WorkingDirectory=${runtime_dir}
Restart=on-failure

[Install]
WantedBy=default.target
EOF

printf "created: %s\n" "${env_file}"
printf "created: %s\n" "${run_script}"
printf "created: %s\n" "${service_dir}/koboldcpp.service"
printf "enable with: systemctl --user daemon-reload && systemctl --user enable --now koboldcpp.service\n"
if [[ ! -x "${bin_path}" ]]; then
  printf "note: koboldcpp binary missing at %s\n" "${bin_path}" >&2
fi
