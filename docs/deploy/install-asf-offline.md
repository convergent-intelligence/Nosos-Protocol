# Install ASF Offline

Use this when you have the ASF tarball on local media and no network access.

## Requirements

- python3
- tar
- file (optional but recommended)

## Install

```bash
sudo bash /path/to/usb/asf/install-asf.sh /path/to/usb/asf/agent-systems-framework-YYYYMMDD.tar.gz /opt/agent-systems-framework
```

## Validate

```bash
cd /opt/agent-systems-framework/agent-systems-framework
./scripts/validate.sh
./scripts/autofile init
./scripts/health.sh
```

## Package Commands (If Needed)

Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3 tar file
```

Gentoo:

```bash
sudo emerge sys-apps/tar app-misc/file dev-lang/python
```

Arch:

```bash
sudo pacman -S python tar file
```
