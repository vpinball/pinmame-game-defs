# PinMAME machine definitions

The goal of this repo is to collect machine-readable definitions for physical pinball machines supported by PinMAME. Each record can describe switches, lamps, GI, coils, displays, mechanisms, controller bindings, edition differences, normalized playfield positions, and source-linked recreation knowledge.

Evidence follows a simple precedence rule: a known-working table script governs controller behavior, official manuals govern physical construction and wiring, and pinned PinMAME source governs emulator routing and driver identity.

## Repository layout

- `machines/` contains canonical definitions classified as `stub`, `partial`, or `author_ready`.
- `catalog/` maps every in-scope PinMAME driver to one physical-machine definition.
- `controllers/` defines shared platform address ranges, routing, normalization, and optional reviewed Markdown technical notes.
- `knowledge/` documents mechanisms, ball paths, edition differences, and recreation guidance.
- `evidence/` and `reports/` retain reproducible extraction and validation results.
- `schemas/`, `src/`, and `tools/` contain the format, validators, generators, and extraction utilities.
- `site/` builds the static catalog browser.

Coverage is fail-closed: a stub contains identity-level data, a partial definition has explicit missing or conflicted requirements, and only a fully validated record is marked author-ready. Community-only virtual games and rethemes are outside the catalog’s physical-machine scope.

Playfield coordinates use normalized player view: `x=0` left, `x=1` right, `y=0` rear/backglass, and `y=1` front/apron. Candidate table geometry is never promoted automatically to canonical placement.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence and validation requirements.

## License

Repository code and original project content are available under the [MIT License](LICENSE); referenced third-party sources retain their own rights and attribution terms.
