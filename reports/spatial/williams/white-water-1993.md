# White Water (Williams, 1993) spatial review

Status: candidate. Two lamp addresses (17, 55) have no resolvable playfield coordinate and are listed under Unresolved placements below; every other spatial dimension audited here is complete. The physical machine record itself remains `partial` at `machines/partial/williams/white-water-1993.json` for that reason alone -- every other coverage dimension, including the switch-matrix opto polarity sweep, is validated with zero disagreement; see the promotion decision below.

The matching source is the retained known-working `Whitewater (Williams 1993).vpx` at SHA-256 `7c59095e9c6a7e100e79f80d7d83497b1c87817bc9daf939721f1a8727a781cd`. The retained extraction produced the embedded script at SHA-256 `0676acb1e610bda8f42f94a915a70bb1b71b6e48462326dd43083a3ab4fa0096`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2092`, and every canonical coordinate is x/952 and y/2092 rounded to at most six fractional places.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual carries a real text layer, but its Section 2/3 tables scramble under column-aware `pdftotext -layout` extraction, so every printed table used here was read from 200 dpi renders and transcribed by hand into `external:pinmame-review-artifacts/white-water/manual-transcription.md` and the excerpt files it indexes.
- Switches 86/87 (the Bigfoot head-position optos) have no dedicated playfield trigger object: the retained script sets them directly from an internal motor-step counter, matching pinned PinMAME's own ww_handleMech. Both are documented projections onto the Bigfoot figure's own retained primitive.
- Solenoids 25/26 (Bigfoot Drive/Enable) project onto the same Bigfoot figure primitive for the same reason. Solenoid 21 (Insanity Falls flasher) uses the one positioned Flasher object (Flasher16) that its own script routine also toggles, because its dedicated helper objects (Flasherlight21/FlasherFlash21) sit outside the retained table's playfield bounds.
- GImiddle member Light2 sits at normalized x=-0.041783, outside the retained table's 0..1 playfield bounds, and is excluded as a table modeling anomaly; five more GImiddle members (l21b2..l21b6) are lamp-21 brightness doublers, not distinct GI bulbs, leaving 11 placements for GI address 1.
- GI strings 3 and 4 (Backglass Boat, Backglass Sky) print no Playfield connection at all on the solenoid/flasher wiring page, and the retained script's UpdateGI has no case for public GI addresses 3/4 -- full agreement between the manual and the runtime script -- so both take a controlled `cabinet_or_service` record.
- The sixteen auxiliary lamp addresses (91-98, 101-108) published through wwGameData's `hw.lampCol = 2` are backbox chase-lamp hardware per the Backbox Assembly parts breakdown; the retained table does not model their individual bulbs, so all sixteen take a controlled `cabinet_or_service` record with no fabricated coordinate.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 86: Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center): the two head-position optos 86/87 are printed on a board mounted inside the Bigfoot mechanism, not as separate playfield objects, and PinMAME's ww_handleMech reads them from a single 7-bit motor-position counter (locals.bigfootPos) rather than from any Trigger/Kicker on the retained table.
- Switch 87: Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); see switch 86.
- Solenoid 21: Coordinate taken from Flasher16, the one positioned VPX object toggled by the retained script's Flasherset21 routine alongside the off-table Flasherlight21/FlasherFlash21 helper objects (both of which sit outside the 0..1 playfield bounds and are excluded as table-modeling anomalies).
- Solenoid 25: Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); solenoid 25 is the H-bridge-style drive pulse for the head motor.
- Solenoid 26: Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); solenoid 26 sets the head motor's rotation direction.

## Counts

- Placements: 194
- Located input addresses: 48
- Located output bindings: 88
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 30
- Outputs with a controlled `unused` record: 5
- Outputs with a controlled `virtual` record: 10

## Unresolved placements

- pinmame.output.lamp 17: Drives a dedicated image-cycling Primitive (Primitive99 for lamp 17, Primitive100 for lamp 55) rather than a positioned Light object; both retained primitives sit at raw (0,0), a local origin rather than a playfield coordinate, so no position is asserted.
- pinmame.output.lamp 55: Drives a dedicated image-cycling Primitive (Primitive99 for lamp 17, Primitive100 for lamp 55) rather than a positioned Light object; both retained primitives sit at raw (0,0), a local origin rather than a playfield coordinate, so no position is asserted.

## Promotion decision

Every authoring-critical placement, quantity, and semantic question is resolved for the addresses this audit covers except one: lamps 17 and 55 drive dedicated image-cycling primitives that sit at a raw local origin rather than a playfield coordinate, so neither has an asserted position. The switch-matrix opto polarity sweep found zero disagreement (every address in `OPTO_SWITCHES` is covered by `wwGameData`'s inverted-switch mask), so `conflicts` is empty and `coverage.dimensions.physical_wiring = "validated"`. The deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte, but the unpositioned lamp pair is still an authoring-relevant gap, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["spatial_placement"]` until a positioned proxy for lamps 17/55 is established.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/white-water-1993/extracted-vpxtool.manifest.json`, SHA-256 `0ec3e7f0c856de3767d1f7e3bf285cd14e533501c798fedcf316833962076b59`, 1166 files, 141788903 bytes.
- Human transcription index of every printed table read from the rendered manual pages, SHA-256 `0c55e5c896738526846d9a04b3b96f5ca61fbfbd5dc85fdd3516c29f1f94a64f`.
