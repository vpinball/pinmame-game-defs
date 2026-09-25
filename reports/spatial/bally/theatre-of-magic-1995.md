# Theatre of Magic (Bally, 1995) spatial review

Status: partial. Every switch, coil, and lamp address is enumerated and the trunk mechanism is fully mapped. The two playfield G.I. strings are placed only from the retained script's per-string binding, 14 retained playfield G.I. bulbs have no proven string, and the script's playfield binding of insert strings 03/04 is an open conflict; see the promotion decision below.

The matching source is the retained known-working `Theatre of Magic (Bally 1995) 2.4.vpx` at SHA-256 `5f8bb3e0493c408484e475516e2f2c3d84b3487dcfb63eb231bca2c40b531253`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `596c926f27c1782819a0184566f083a161be362fec7a3bbc634a9138d97b47c3`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2594.1` -- unusually tall -- and every canonical coordinate is x/952 and y/2594.1 rounded to at most six fractional places. Using the more common y/2162 divisor used by every standard-height WPC game curated so far would have compressed every y coordinate by roughly 20% and silently corrupted the whole spatial set; front devices (flippers, trough, outhole) were sanity-checked to land near y=1.0 and top-lane devices near the low end of the range before this report was accepted.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries an OCR text layer, but every printed table used here was independently verified against a 300 dpi render of the same page and transcribed into `external:pinmame-review-artifacts/theatre-of-magic-1995/manual-transcription.md`; the OCR text was never treated as authoritative on its own.
- The four Cube Position switches (55-58) have no fixed playfield sensor object; the retained script sets all four from one continuous TrunkAngle counter, so they are documented projections onto the rotating trunk's own table-object center (Primitive Trunk/Trunk1/Trunk2), matching the precedent established for Williams Monster Bash's Dracula-position optos and Williams Star Trek: TNG's idol-wheel optos.
- Solenoids 17/18 (trunk motor) and 33 (cube magnet, fires inside the rotating box) are likewise projected onto the trunk's own table-object center rather than invented as separate fixed coordinates.
- Lamp 85 (Lamp In Cube) rides inside the rotating trunk and is projected onto the same trunk object center for the same reason.
- G.I. location comes from the game's own Power Driver Board connector list (printed 3-27, PDF page 149): J120 carries strings 01 and 02 (public G.I. 0 and 1) 'to playfield' and J121 carries strings 03-05 (G.I. 2-4) 'to insert'. The Solenoid/Flasher Table's G.I. rows print the opposite location columns; the same connector list agrees with that table on every flashlamp row, so the G.I. rows are the misprint. #555 wedge bulbs (the jet-bumper bulb, printed 2-20) go with strings 01-02 and #44 with 03-05. The earlier conflict that followed the table is closed.
- The retained script still dims playfield collections GIRight and GIMiddle from insert strings 03 and 04. Under the split-authority rule the manual classifies the strings and the script owns the runtime binding, so this is recorded as `conflict.gi-strings-3-4-insert-vs-script-playfield-binding`, and those coordinates are not promoted.
- G.I. 2, 3 and 4 are backbox insert-board strings with controlled `cabinet_or_service` records; G.I. 4 also feeds the coin door through J119 by its wire colours (printed 3-32).
- G.I. 0 and 1 are placed from the retained script's per-string `UpdateGI` binding (case 0 GITop + GIBumpers, case 1 GILeft): 22 and 9 bulbs, each at one Light object's own centre, render doubles collapsed to the modelled bulb (then the smallest falloff). They stay `observed`: the table also dims playfield collections GIRight and GIMiddle from insert strings 03 and 04, so its playfield partition is not the machine's, and those 14 bulbs are listed as unassigned.
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

## General illumination placements

- G.I. 0 (GITop + GIBumpers, observed): 22 bulbs -- light006, light007, light008, light015, light020, light18, light2, light24, light25, light26, light27, light28, light30, light31, light32, light34, light36, light37, light8, l1, l2, l3
- G.I. 1 (GILeft, observed): 9 bulbs -- light002, light003, light009, light010, light011, light10, light11, light14, light9
- Unassigned GIRight (UpdateGI case 2 (insert string 03)): 9 playfield bulbs on string 01 or 02 -- light004, light005, light012, light013, light12, light13, light15, light16, light17
- Unassigned GIMiddle (UpdateGI case 3 (insert string 04)): 5 playfield bulbs on string 01 or 02 -- light001, light016, light20, light018, light019

## Counts

- Placements: 179
- Located input addresses: 49
- Located output bindings: 92
- Outputs with no spatial record (missing evidence): 0
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 13
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `unused` record: 7
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Every switch, coil, and lamp address is enumerated with an honest disposition, the trunk/subway/lock/vanish-lock mechanism chain is fully documented with real causality from the retained script, and the opto-polarity sweep found zero disagreement between the manual's shading and PinMAME's inverted-switch mask. Which strings feed the playfield is settled by the manual's own connector list. Promotion to `author_ready` is still refused: which of the two playfield strings each playfield G.I. bulb is on is not proven for any bulb, and the script's playfield binding of insert strings 03/04 is an open conflict, so `coverage.dimensions.spatial_placement = "observed"` and `coverage.missing = ["unresolved_conflicts", "spatial_placement"]`. The machine's G.I. test run string by string on an unrestored machine, with each lit bulb recorded, would settle both.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/theatre-of-magic-1995/extracted-vpxtool.manifest.json`, SHA-256 `2db2ef0933b9738ff48e79e3ca6f2332e97e5457321f711d4b8430d4f0c6cc45`, 1994 files, 151153328 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `c7a4dd783f33e63413bc33b9dcdf99c7381f80e82eb84017cf0b2a1354d6b9fb`.
- Curated VPX geometry reference, SHA-256 `df048e59d6638d8d5fc91e9c2d857de6f3437fc70cf858c265439289d809fa2a`.
