# pinmame-game-defs

JSON database of pinball machine I/O mappings for VPE (Visual Pinball Engine).

## What This Is
Each pinball ROM communicates via numbered switch/coil/lamp connections. This repo documents what those numbers mean (e.g., "switch 56 = Left Outlane") so VPE authors can wire their tables correctly.

## Structure
- `platforms/` — Cabinet-level defaults per MPU era (wpc.json, sam.json, bally.json, system80.json)
- `games/` — One file per game with playfield-specific mappings (t2.json, afm.json, etc.)
- Platform + game files are merged at load time by VPE

## Schema
- `_format`: "vpe-game-mapping" (games) or "vpe-game-mapping-platform" (platforms)
- `_version`: "0.1"
- `_source.origin`: "vpe-csharp" (Phase 1 migration) or "vbscript-parser" (Phase 2 extraction)
- Core fields: `description`, `vpx_name`, `device_hint`
- Parser metadata (prefixed with `_`): `_vbscript_name`, `_vbscript_callback`, `_inferred_type`

## Phases
1. **C# → JSON** (complete): 11 games + 4 platforms converted from VPE's hardcoded C# classes
2. **VBScript extraction** (in progress): Parse VPX table scripts to extract mappings for ~770 machines
3. **Community UI** (future): Web editor for community verification/contribution

## Key Links
- VPE: https://github.com/freezy/VisualPinball.Engine
- PinMAME plugin: https://github.com/VisualPinball/VisualPinball.Engine.PinMAME
- Schema + design decisions: see life-ops/projects/vpe/research/ on Ben's Mac

## Dev Notes
- VPX tables with VBScript: /home/ben/Games/VPX/tables/
- VPE repos: ~/projects/VPE/
- Full project context: life-ops/projects/vpe/README.md on Ben's Mac
