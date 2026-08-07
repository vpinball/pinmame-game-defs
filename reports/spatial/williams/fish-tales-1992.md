# Fish Tales (Williams, 1992) spatial review

Status: validated. Every spatial dimension audited here is complete, but the physical machine record itself remains `partial` at `machines/partial/williams/fish-tales-1992.json` because of two unresolved switch-polarity conflicts and the withheld mandatory independent high-tier review, both outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Fish Tales (Williams 1992) VPW 1.1.vpx` at SHA-256 `1f82c0237831b50c514e53c8938636f59ee584fc4346c143a3216b9f5d8a1029`. The retained extraction produced the embedded script at SHA-256 `b6289a7087f11bd1902d8b059fe663723a6319c6490d1a2fa124d3dd7089e1f5`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.9412 bottom=2164.7058`, and every canonical coordinate is x/952.9412 and y/2164.7058 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF is OCR'd, but its multi-column tables are not reliable from OCR text alone; every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/fish-tales/manual-transcription.md`.
- Switches 37/38 (Reel 1/Reel 2) have no dedicated playfield sensor object; the retained script derives them from the reel's own internal ReelPosition angle counter, so both are documented projections onto the visible Reel drum Primitive that the same counter drives.
- Lamps 16/17/18 are a backbox insert-panel device (A-15339 3-Lamp Board Assembly) despite the retained table modeling two co-located Light objects per address near the playfield's own rear edge for visual effect; neither is treated as a playfield coordinate. GI strings 0, 1, and 3 are likewise backbox circuits with no playfield representation in the retained script, matching this manual's own 'Backbox G.I.' classification for the same three printed addresses.
- GI strings 2 and 4 use the retained table's TopGI/BottomGI emitter collections (21 and 11 members respectively), matching this manual's own 'Playfield G.I.' classification for printed strings 03 and 05 exactly.
- Public solenoids 51/52/53 are PinMAME's own internal reel-position bookkeeping for its built-in ball simulator, never referenced by the retained known-working script, and have no real driver-board transistor behind them; they are declared virtual with a `virtual` spatial record.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 37: Projected onto the Reel drum (Primitive Reel, table object center): switches 37/38 have no dedicated sensor object; the retained script derives both directly from the internal ReelPosition angle counter that also drives the visible Reel primitive's own rotation (Reel.Rotx = ReelPosition + 46).
- Switch 38: Projected onto the Reel drum (Primitive Reel, table object center); see switch 37.

## Counts

- Placements: 158
- Located input addresses: 37
- Located output bindings: 90
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 25
- Outputs with a controlled `cabinet_or_service` record: 10
- Outputs with a controlled `unused` record: 5
- Outputs with a controlled `virtual` record: 17

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, two switch-polarity conflicts remain unresolved (`conflict.reel-opto-switches-not-normalized` and `conflict.ball-popper-drop-target-normalized-non-opto`), and this curation pass did not obtain the mandatory independent high-tier cross-provider review described in `docs/INSTRUCTIONS.md`. The definition therefore carries a non-empty `conflicts` array, `coverage.dimensions.physical_wiring = "conflicted"`, and `recreation_notes` in `coverage.missing`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["polarity", "recreation_notes", "unresolved_conflicts"]` until a LibPinMAME harness trace against a legal ft_l5 ROM resolves the polarity conflicts and the mandatory review runs against the exact proposed tree.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/fish-tales-1992/extracted-vpxtool.manifest.json`, SHA-256 `946a74ffd92d949fd3d1dfac2c8c8c4207eacc9da3e090174f204fdbb28008c5`, 3176 files, 1099189711 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `4d45217f9b63775a5d1f969365a6333a8fd2e55417c84bbad15d81407664df3a`.
