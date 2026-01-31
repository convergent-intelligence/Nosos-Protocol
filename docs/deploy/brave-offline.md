# Brave Offline Install (Web3 Auth)

Goal: provide a local Brave install path so Web3 auth works without external download.

## USB Layout

Store packages under:

```
USBROOT/browsers/brave/
  deb/
  rpm/
  arch/
```

## Debian / Ubuntu

Place a local Brave `.deb` in `browsers/brave/deb/`.

Install:

```bash
sudo dpkg -i /media/usb/browsers/brave/deb/brave-browser_*.deb
sudo apt-get -f install
```

Notes:
- `apt-get -f install` may require the Debian DVD ISO or a local mirror for dependencies.

## Fedora / RHEL / Rocky / Alma

Place a local Brave `.rpm` in `browsers/brave/rpm/`.

Install:

```bash
sudo dnf install /media/usb/browsers/brave/rpm/brave-browser-*.rpm
```

Notes:
- If dependencies are missing, you need a local repo or offline package cache.

## Arch / Endeavour / Manjaro

Options:
- Install from a local pacman package cache.
- Use a local repo built ahead of time.

Install (local package):

```bash
sudo pacman -U /media/usb/browsers/brave/arch/brave-browser-*.pkg.tar.zst
```

Notes:
- AUR builds require build deps and are not ideal offline.

## Gentoo

Gentoo typically installs Brave via ebuilds and build deps. For offline use, create a local distfiles cache and binpkg repo ahead of time.
