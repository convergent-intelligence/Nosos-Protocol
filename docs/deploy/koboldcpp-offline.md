# Koboldcpp Offline Runtime

Goal: run a local LLM server from the USB workspace using Koboldcpp.

## USB Layout

```
USBROOT/
  llm/
    koboldcpp/
      koboldcpp-linux
      koboldcpp.env
      run-koboldcpp.sh
    models/
      model.gguf
```

## Install the Daemon (User Service)

From a host OS, run:

```bash
./scripts/deploy/install-koboldcpp-daemon.sh /media/usb /media/usb/llm/models/model.gguf
```

This creates:
- `llm/koboldcpp/koboldcpp.env`
- `llm/koboldcpp/run-koboldcpp.sh`
- `~/.config/systemd/user/koboldcpp.service`

Then enable:

```bash
systemctl --user daemon-reload
systemctl --user enable --now koboldcpp.service
```

## Notes

- If the binary or model is missing, the service will fail with a clear message.
- Keep models on the USB so the workspace is portable.
