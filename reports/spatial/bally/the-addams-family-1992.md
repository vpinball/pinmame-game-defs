# Spatial audit -- bally.the-addams-family.1992

Coverage status: `partial`

## Blockers

- coverage.missing = ["recreation_notes"]: knowledge/bally/the-addams-family-1992.md documents every mechanism this definition references, but as a single unreviewed curation pass it has not had the independent high-tier review this project requires before a knowledge note counts as validated recreation_knowledge. No conflict, unresolved address, or missing spatial placement remains -- this is the sole reason the record stays partial rather than a genuine gap in the electrical or spatial evidence.

## Evidence

- VPX table SHA-256 `85af088f0ed6d59c83599102e6245cc2eab5674e69d29882db6f0eaacf05e858`
  - Bounds `left=0 top=0 right=952.965 bottom=2164.76`; normalization `x/952.965; 0=left, 1=right` / `y/2164.76; 0=rear/backglass, 1=apron/player`
- Extraction manifest `external:pinmame-vpx-sources/bally/the-addams-family-1992/extracted-vpxtool.manifest.json`, SHA-256 `d79a5a3723fbd4041460764ec598a78683963370566033d0701cacc93ad1d4dc`, 1277 files, 415715342 bytes (vpxtool git:v0.33.3)
- Manual transcription `external:pinmame-review-artifacts/the-addams-family-1992/manual-transcription.md`, SHA-256 `17e8aed2524e79b671633026c0872cda8c6724d5d2e3b2bf9d6c49018fb5462e`
- Rendered page cache `external:pinmame-manuals/rendered/bally.the-addams-family.1992/`

## Resolved input addresses (47)

15, 16, 17, 18, 25, 26, 27, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 47, 48, 51, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 86, 87

## Not-applicable inputs by reason

- `cabinet_or_service`: 1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 21, 22, 112, 114, 116, 118
- `constant`: 24
- `dip_switch`: 1, 2, 3, 4, 5, 6, 7, 8
- `internal_nonvisual`: 81, 82, 84, 85, 111, 113, 115, 117
- `unused`: 11, 12, 23, 28, 46, 52, 83, 88

## Resolved output bindings (98)

- `pinmame.output.gi`: 0, 4
- `pinmame.output.lamp`: 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 77, 78, 81, 82, 83, 84, 85, 86, 87
- `pinmame.output.solenoid`: 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 33, 34, 35, 36, 45, 46, 47, 48

## Not-applicable outputs by reason

- `cabinet_or_service`: pinmame.output.gi:1, pinmame.output.gi:2, pinmame.output.lamp:88, pinmame.output.solenoid:2
- `unused`: pinmame.output.gi:3, pinmame.output.lamp:41, pinmame.output.lamp:76
- `virtual`: pinmame.output.solenoid:29, pinmame.output.solenoid:30, pinmame.output.solenoid:31, pinmame.output.solenoid:32, pinmame.output.solenoid:37, pinmame.output.solenoid:38, pinmame.output.solenoid:39, pinmame.output.solenoid:40, pinmame.output.solenoid:41, pinmame.output.solenoid:42, pinmame.output.solenoid:43, pinmame.output.solenoid:44, pinmame.output.solenoid:49, pinmame.output.solenoid:50

## Projections (documented, onto the device's own mechanism assembly)

- `switch.matrix-81` -> vault_base (Bookcase assembly primitive center): taf_handleMech synthesizes swBookOpen purely from motor position; no discrete playfield sensor.
- `switch.matrix-82` -> vault_base (Bookcase assembly primitive center): taf_handleMech synthesizes swBookClose purely from motor position; no discrete playfield sensor.
- `switch.matrix-84` -> Thing (Thing hand assembly primitive center): taf_handleMech synthesizes swThingDn purely from motor position; no discrete playfield sensor.
- `switch.matrix-85` -> Thing (Thing hand assembly primitive center): taf_handleMech synthesizes swThingUp purely from motor position; no discrete playfield sensor.
- `device.thing-motor` -> Thing (Thing hand assembly primitive center): ThingMotor mechanism callback rotates Thing/handMAGNET/thingBox directly; no separate motor object in the retained table.
- `device.bookcase-motor` -> vault_base (Bookcase assembly primitive center): BookCaseMotor mechanism callback rotates vault_base directly; no separate motor object in the retained table.

## Excluded object classes

- L11b, L12b, ... L87b-style co-located brightness-doubling Light objects at every lamp address (render doubling, not a second physical bulb)
- L45old (superseded art duplicate of L45bold at the same 'The Mamushku' insert)
- GILeftPrims / GIRightPrims collection members (shaded plastics that dim with GI, not individual bulb sockets)

## Placement count: 169
