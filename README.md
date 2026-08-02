# PinMAME machine definitions

This repository builds a VPE-neutral, independently versioned catalog of the switches, lamps, GI, controlled devices, displays, mechanisms, and controller variants needed to recreate PinMAME-supported physical machines.

When evidence disagrees, a known-working VPX table script is the tie-breaker for controller mapping and behavior, the physical manual controls wiring and assembly facts, and pinned PinMAME source controls emulator routing and display/output metadata.

The legacy `games/` and `platforms/` directories are migration inputs. Canonical definitions live under `machines/`, the complete LibPinMAME driver catalog lives under `catalog/`, evidence lives under `evidence/`, and source-linked recreation knowledge lives under `knowledge/`.

## Coverage is fail-closed

Every definition declares `coverage.status` as `stub`, `partial`, or `author_ready`.

- `stub` means only catalog identity or generated structure is known. The machine is not usable for recreation.
- `partial` means semantic evidence exists, but one or more authoring requirements remain missing or conflicted.
- `author_ready` means the completeness validator found the full semantic I/O, display, mechanism, variant, provenance, and recreation-note information required by the schema and policy.

Generated placeholders are named `stub.pinmame.<root-driver>` and stored under `machines/stubs/` so they are conspicuous in source, indexes, and consumer APIs. Stubs and partial definitions contribute zero to completed-game coverage.

## VPE boundary

Canonical definitions do not contain Unity object-name regexes, device matching hints, match counts, VPE input-map actions, or an open-ended `extensions.vpe` object. Portable cabinet roles such as `cabinet.start`, `service.up`, and `flipper.lower.left` are allowed. VPE owns role-to-input configuration and table-object mapping.

Legacy numeric and zero-padded IDs can be retained as explicitly namespaced compatibility aliases while old tables migrate. The import report records every dropped hint.

## Commands

Run from a checkout without installing:

```powershell
$env:PYTHONPATH = "src"
python -m pinmame_game_defs --help
python -m unittest discover -s tests -v
```

See [the implementation plan](docs/MACHINE_DEFINITIONS_PLAN.md) for the source inventory, format rationale, extraction pipeline, validation policy, harness design, Ghidra criteria, distribution model, and current implementation status.
