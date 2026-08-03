# PinMAME machine definitions

This repository builds a VPE-neutral, independently versioned catalog of the switches, lamps, GI, controlled devices, displays, mechanisms, and controller variants needed to recreate PinMAME-supported physical machines.

When evidence disagrees, a known-working VPX table script is the tie-breaker for controller mapping and behavior, the physical manual controls wiring and assembly facts, and pinned PinMAME source controls emulator routing and display/output metadata.

The legacy `games/` and `platforms/` directories are migration inputs. Canonical definitions live under `machines/`, the physical-machine-scope LibPinMAME driver catalog lives under `catalog/`, evidence lives under `evidence/`, and source-linked recreation knowledge lives under `knowledge/`. Custom ROMs made only for community virtual tables are excluded; ROM revisions and conversions that can run on physical hardware remain in scope.

## Coverage is fail-closed

Every definition declares `coverage.status` as `stub`, `partial`, or `author_ready`.

- `stub` means only catalog identity or generated structure is known. The machine is not usable for recreation.
- `partial` means semantic evidence exists, but one or more authoring requirements remain missing or conflicted.
- `author_ready` means the completeness validator found the full semantic I/O, display, mechanism, variant, provenance, and recreation-note information required by the schema and policy.

Generated placeholders are named `stub.pinmame.<root-driver>` and stored under `machines/stubs/` so they are conspicuous in source, indexes, and consumer APIs. Stubs and partial definitions contribute zero to completed-game coverage.

## Spatial placement evidence

Machine schema v2 adds optional device-level `spatial` evidence while retaining full compatibility for v1 stubs and partial definitions. The canonical global `playfield` space is normalized VPX/player view: `x=0` is left, `x=1` is right, `y=0` is the rear/backglass end, and `y=1` is the front/apron end. It is defined once globally rather than repeated in each machine definition.

`physical.location` remains construction prose and is never promoted automatically. A located spatial assertion contains one or more source-backed sensor, effect, or emitter placements. A controlled `not_applicable` assertion records why a device has no playfield point; it is not a distributed-GI/flasher exemption. Author-ready v2 definitions require validated spatial evidence for every device, including individual emitter placements for lamps, GI, and flashers.

`extract-spatial` reads a vpxtool extraction directory (with the source VPX supplied for hashing) or invokes an explicitly supplied external vpxtool executable. It emits candidate geometry only; it never claims a semantic controller mapping or writes canonical placements. `render-spatial-overlay` produces a deterministic stdlib-only SVG of canonical placements without committing a licensed playfield image.

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
