# Theatre of Magic (Bally, 1995) spatial review

Status: partial. Every switch, coil, and lamp address is enumerated and the trunk mechanism is fully mapped, but GI address 4 has no VPX-bound coordinate and GI addresses 0/1 carry an unresolved manual-vs-script wiring conflict; see the promotion decision below.

The matching source is the retained known-working `Theatre of Magic (Bally 1995) 2.4.vpx` at SHA-256 `5f8bb3e0493c408484e475516e2f2c3d84b3487dcfb63eb231bca2c40b531253`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `596c926f27c1782819a0184566f083a161be362fec7a3bbc634a9138d97b47c3`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2594.1` -- unusually tall -- and every canonical coordinate is x/952 and y/2594.1 rounded to at most six fractional places. Using the more common y/2162 divisor used by every standard-height WPC game curated so far would have compressed every y coordinate by roughly 20% and silently corrupted the whole spatial set; front devices (flippers, trough, outhole) were sanity-checked to land near y=1.0 and top-lane devices near the low end of the range before this report was accepted.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries an OCR text layer, but every printed table used here was independently verified against a 300 dpi render of the same page and transcribed into `external:pinmame-review-artifacts/theatre-of-magic-1995/manual-transcription.md`; the OCR text was never treated as authoritative on its own.
- The four Cube Position switches (55-58) have no fixed playfield sensor object; the retained script sets all four from one continuous TrunkAngle counter, so they are documented projections onto the rotating trunk's own table-object center (Primitive Trunk/Trunk1/Trunk2), matching the precedent established for Williams Monster Bash's Dracula-position optos and Williams Star Trek: TNG's idol-wheel optos.
- Solenoids 17/18 (trunk motor) and 33 (cube magnet, fires inside the rotating box) are likewise projected onto the trunk's own table-object center rather than invented as separate fixed coordinates.
- Lamp 85 (Lamp In Cube) rides inside the rotating trunk and is projected onto the same trunk object center for the same reason.
- GI strings 3 and 4 (public addresses 2 and 3) use the retained table's GIRight/GIMiddle emitter collections, matching the retained script's UpdateGI dispatch. GI string 5 (address 4) is playfield-wired per the manual but has no UpdateGI case and therefore no VPX object binding; it is left with no spatial record at all rather than a fabricated one, and the corresponding definition entry omits its `spatial` key -- the same honest-omission pattern Williams Star Trek: TNG established for three lamps with no resolvable coordinate.
- GI strings 1 and 2 (addresses 0 and 1) are backbox devices per the manual's own wiring table despite the retained script visually driving playfield light collections for both; see `conflict.gi-strings-1-2-backbox-vs-script-playfield-binding`.
- Solenoids 19 (prototype-only 'Tiger Saw' captive-ball motor) and 23/36 (optional 'Magic Post' flasher and up/down coil, gated behind a table-author toggle that defaults off) are recorded `unused` on the production machine this definition binds, each with the disagreement fully disclosed in `physical.notes`.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 55: Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center): the four Cube Position optos are printed on the trunk's own "Opto Board" (manual page 1-50 teardown diagram) and the retained script's TrunkTimer_Timer sets all four from one TrunkAngle counter (0-360 degrees) rather than from four fixed playfield objects.
- Switch 56: Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.
- Switch 57: Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.
- Switch 58: Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.
- Lamp 85: Lamp In Cube rides inside the rotating trunk; projected onto the trunk's own table-object center (Primitive Trunk).
- Solenoid 17: Box Clockwise: no separate motor-drive object; projected onto the trunk's own table-object center.
- Solenoid 18: Box Counter Clockwise: same projection as 17.
- Solenoid 33: Cube Magnet: fires inside the rotating trunk; projected onto the trunk's own table-object center.

## Counts

- Placements: 173
- Located input addresses: 49
- Located output bindings: 92
- Outputs with no spatial record (missing evidence): 1
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 13
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 7
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Every switch, coil, and lamp address is enumerated with an honest disposition, the trunk/subway/lock/vanish-lock mechanism chain is fully documented with real causality from the retained script, and the opto-polarity sweep found zero disagreement between the manual's shading and PinMAME's inverted-switch mask. However, GI address 4 has no resolvable playfield coordinate and GI addresses 0/1 carry an unresolved conflict between the manual's backbox wiring and the retained script's playfield-collection binding. `coverage.dimensions.physical_wiring = "conflicted"` and `coverage.dimensions.spatial_placement = "partial"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["unresolved_conflicts", "spatial_placement"]` until a LibPinMAME harness trace or a second independent manual copy resolves the GI wiring disagreement and a VPX object binding is found for GI string 5.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/theatre-of-magic-1995/extracted-vpxtool.manifest.json`, SHA-256 `2db2ef0933b9738ff48e79e3ca6f2332e97e5457321f711d4b8430d4f0c6cc45`, 1994 files, 151153328 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `c7a4dd783f33e63413bc33b9dcdf99c7381f80e82eb84017cf0b2a1354d6b9fb`.
- Curated VPX geometry reference, SHA-256 `df048e59d6638d8d5fc91e9c2d857de6f3437fc70cf858c265439289d809fa2a`.
