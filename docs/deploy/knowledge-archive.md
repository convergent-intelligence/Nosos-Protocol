# Knowledge Archive (Offline)

Goal: provide offline references and search so child agents can find what they need without network access.

## Layout

```
USBROOT/
  knowledge/
    kiwix/
    zims/
    references/
    manpages/
    games/
  search/
    tools/
    indexes/
```

## Suggested Sources (Offline)

- Kiwix ZIMs:
  - Wikipedia (en)
  - Wiktionary (en)
  - Wikibooks (science/math)
- Programming references:
  - Rust book + standard library docs
  - Python docs
  - C/C++ references
  - Git, Make, and Linux manpages
- Web references (HTML snapshots):
  - MDN web docs
  - Debian/Fedora/Gentoo/Arch install guides

- Learning games and puzzles:
  - logic puzzles and grid packs (PDF)
  - math games and science demos
  - offline-friendly open-source games

## Search Strategy

- Provide simple local search tools:
  - `ripgrep` and `fzf` for text search
  - `sqlite` indexes for curated content
- Keep indexes under `search/indexes/` with a short README per index.

## For Children

- Keep a simple start page under `knowledge/games/index.html`.
- Use short paths and clear labels.
- Use `docs/deploy/games-index.html` as the template.
- Add `knowledge/index.html` using `docs/deploy/knowledge-index.html`.

## Notes

- Expect large sizes (Wikipedia alone can be tens of GB).
- Track licenses and source versions in a manifest.
- Keep a "first steps" index page for children.
