# Twilight Zone (Bally, 1993) spatial review

Status: partial. The physical machine record is `partial` at `machines/partial/bally/twilight-zone-1993.json`, driven by one unresolved semantic conflict (`conflict.clock-motor-direction-naming`) and a small number of switches/one GI string with no validated playfield placement; see the promotion decision below.

The matching source is the retained known-working `Twilight Zone (Bally 1993) 2.4.5.vpx` at SHA-256 `4fcca01a076591384caec5b06d4f58547299cbeae9fac2a67faa29cc5af0d814`. The retained extraction produced the embedded script at SHA-256 `122ef6811ff2e6912593a28a75078a467e6d58dd208c98e313c82712aee2bc4e`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=1082.353 bottom=2164.706`, wider than the standard VPW WPC table divisor used elsewhere in this repository; every canonical coordinate here is x/1082.353 and y/2164.706 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime and address/causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and label authority; pinned PinMAME owns controller topology and the emulator-normalization mask; the retained table supplies geometry.
- The retained manual PDF is an image-only scan. Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md`.
- This retained scan is missing every even printed page from 2-48 through 2-54 inclusive, removing the Switch Matrix (2-50, which also carries the first Switch Locations table for items 1-33), Solenoid/Flasher Table (2-52), and Lamp Matrix (2-54) wiring pages. Wire colors and connector/pin assignments are therefore not asserted for any device in this definition, and switches below address 34 rely on pinned PinMAME's own #defines and inverted-switch mask rather than a printed part-number cross-check.
- The manual's printed auxiliary-board item numbers 37-44 for the custom solenoid board are not the same as PinMAME's public solenoid addresses for the same physical outputs; the retained script's own comments bridge the two numbering schemes explicitly (see manual-transcription.md), resolving what would otherwise look like a large unexplained address gap.
- Switches 71 (Big Kick), 82 (Upper Right Magnet), and 86 (Clock Lane), and solenoid 22 (Upper Right Magnet), are printed "Not Used" with no part number at all. PinMAME's own simulator-only input-port toggles of the same names belong to its internal text-mode ball tracker (sim.c), not a documented physical factory option, so no fitted variant is claimed.
- GI address 2 (Clock & Insert) is bound in the retained script to a single light object (l102) whose raw coordinate sits outside the playfield bounds; excluded as a table-modeling anomaly rather than promoted to a false placement, the same treatment Monster Bash's curation gave its GIbot light11 anomaly.
- Solenoids 37-44 do not carry the WPC-95 LPDC duplication: this is a WPC-Fliptronic (pre-95, pre-integrated board) generation, and pinned PinMAME's core_getSol only serves that address range for WPC-95/S11 generations; Twilight Zone's own driver hook does not claim it either, so 37-44 are simply unused here.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 52: Projected onto the Trigger.sw52 object, the only VPX trigger the retained script binds to switch 52; the geometry file lists it under the Hitchhiker figure's lane.

## Unresolved spatial evidence

- pinmame.input.switch 26: No VPX object binds switch 26 (Trough Proximity / powerball detect); the retained script sets it from tz_handleBallState's ball-type detection rather than a Hit event.
- pinmame.input.switch 45: No gameitem, collection, or object event binding named sw45/sw45a was found anywhere in the retained extraction, despite the retained script defining Sub sw45_Hit and Sub sw45a_Hit.
- pinmame.input.switch 46: No gameitem, collection, or object event binding named sw46/sw46a was found anywhere in the retained extraction, despite the retained script defining Sub sw46_Hit and Sub sw46a_Hit.
- pinmame.input.switch 55: No VPX object binds switch 55 (Gumball Geneva); pinned PinMAME's tz_handleMech sets it synthetically from the internal gumball-motor position counter rather than from a table Hit event, and the manual documents it only as "located on the underside of the playfield".
- pinmame.output.gi 2: Bound light object l102 sits outside the playfield bounds; excluded as an anomaly rather than promoted.

## Counts

- Placements: 137
- Located input addresses: 48
- Located output bindings: 66
- Inputs with a controlled `cabinet_or_service` record: 17
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 19
- Inputs with a controlled `unused` record: 4
- Outputs with a controlled `cabinet_or_service` record: 29
- Outputs with a controlled `internal_nonvisual` record: 17
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 15

## Promotion decision

Identity, controller platform, address enumeration, mechanism inventory/behavior, variant coverage, and recreation knowledge are all complete and validated. Promotion to `author_ready` is refused for two reasons: `conflict.clock-motor-direction-naming` is a genuine, unresolved disagreement between pinned PinMAME's internal #define names and two independent sources (the printed manual and the retained script author's own cross-reference comment) about which of solenoids 56/57 is the clock's forward drive line, and a small number of addresses (switches 26/45/46/55 and GI address 2) have no validated playfield placement because no bound VPX object exists for them in the retained extraction. The definition therefore carries a non-empty `conflicts` array, `coverage.dimensions.semantic_naming = "conflicted"`, and `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`. Resolving the clock-direction conflict needs a LibPinMAME harness trace or the missing D.C. Motor Control Assembly schematic; resolving the remaining spatial gaps needs either a corrected retained table build or the missing 2-50 manual page.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/twilight-zone-1993/extracted-vpxtool.manifest.json`, SHA-256 `6188e966e86cafeece592dfecf0603f8b3a16b7bc188d3b9ed876a2425d506c8`, 3176 files, 546282740 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `022e91ceaedb44fdaf410cca90bfa534aa11c89fcd832dd2a0f94166c24de39a`.
- Raw retained-table object geometry, SHA-256 `dc8a49f6b1d1568ba9027af7453157039da05a08d6ffd2ac0a60c54940cb2f3a`.
