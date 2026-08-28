# Big Bang Bar (Capcom, 1996) spatial review

Status: validated. The physical machine record is `author_ready` at `machines/author-ready/capcom/big-bang-bar-1996.json`: every address is a validated placement or a controlled `not_applicable` record, and no unresolved conflict remains.

The matching source is the retained known-working `Big Bang Bar (Capcom 1996) VPW v1.0.vpx` at SHA-256 `7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5`. The retained extraction produced the embedded script at SHA-256 `db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Capcom operators manual and its companion schematic set are the physical inventory, quantity, polarity, wiring, and device-identity authority (the schematic's own per-device "DEVICE # & DESCRIPTION" table on sheet 7 is the single most authoritative solenoid source found, and the Tube Lady Assembly's own parts list on printed page 109 is the decisive construction source for that mechanism); pinned PinMAME source owns controller topology and per-game hardware metadata; the retained tables supply geometry.
- The manual is an Adobe Paper Capture OCR'd scan whose text layer is unreliable on dense multi-column tables; every printed table used here was read from rendered page images at 200-600 dpi and transcribed into `external:pinmame-review-artifacts/big-bang-bar/manual-transcription.md` and its companion solenoid/schematic document.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (the Alien rotating mechanism's 32-step motor counter) or reuses a table object that also serves another role (kickers, slingshot walls, bumpers). Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- Solenoid coils whose retained-table objects are the assembly they actuate (the two slingshot coils, the three flipper coils, and the two ramp-diverter drop walls) are documented projections onto those objects, each corroborated by the manual's printed page-82 numbered playfield diagram (balloon-centre tolerance ~0.02-0.05, measurement record committed with the diagram excerpt).
- The manual's own parts lists settle the two construction questions the 2026-08-07 curation left open: the Tube Lady Assembly contains no coil (item 1A is a shaft coupling; the drive is the MR00108 motor through a belt), and the alien mechanism's position sensor is the A0020000 slotted-opto PCB reading the MT00501 encoder disc.
- Cabinet lamps 1/2 (coin door, X2) and 3 (START, which the retained script binds to the cabinet start button) carry controlled `cabinet_or_service` records; the retained tables' out-of-bounds glow proxies for them are excluded as modeling artifacts.
- Lamp 62 ((Electro) Black Light) carries a documented projection onto the (Electro) Ramp feature's centroid; lamps 38/125 carry coordinates from the earlier retained recreation where the primary table models no object, each corroborated by same-feature geometry.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- pinmame.input.switch 25: Projected onto the Spinner table object's own center (Spinner.sw25); a physical spinner has no separate fixed sensor position.
- pinmame.input.switch 33: Projected onto the LeftFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolLFlipper with no separate sensor object.
- pinmame.input.switch 34: Projected onto the RightFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolRFlipper with no separate sensor object.
- pinmame.input.switch 35: Projected onto the same Kicker object as the Outhole coil (solenoid 1): the manual's Switch Locations table names Ref.35 "Outhole" and the retained script kicks the ball resting on this object from Sub SolTrough.
- pinmame.input.switch 41: Projected onto the Wall.LeftSlingShot object's own drag-point centroid; resolved via the retained script's LeftSlingShot_Slingshot event sub rather than a differently-named sw41 object.
- pinmame.input.switch 42: Projected onto the Wall.RightSlingShot object's own drag-point centroid; resolved via the retained script's RightSlingShot_Slingshot event sub rather than a differently-named sw42 object.
- pinmame.input.switch 54: Projected onto the Bumper2 table object's own center; resolved via the retained script's Bumper2_Hit event sub, which pulses this switch.
- pinmame.input.switch 55: Projected onto the Bumper3 table object's own center; resolved via the retained script's Bumper3_Hit event sub.
- pinmame.input.switch 56: Projected onto the Bumper1 table object's own center; resolved via the retained script's Bumper1_Hit event sub.
- pinmame.input.switch 57: Projected onto the rotating Alien mechanism's own anchor (Primitive Alien1_BM_Lit_Room): the retained script's ALockTimer_timer reads a single 0-31 motor-position counter and toggles this one opto through a repeating home/quarter/half/three-quarter-turn notch pattern, not a fixed playfield sensor object -- the same pattern established for Monster Bash's Dracula-position optos.
- pinmame.input.switch 68: Projected onto the RightFlipper table object's own center, the same object switch 34 projects onto: the retained script sets both switches together inside Sub SolRFlipper with no separate Upper Right Flipper EOS sensor object modeled.
- pinmame.output.solenoid 4: Projected onto the Wall.LeftSlingShot assembly's own drag-point centroid; the manual's printed page-82 playfield diagram marks callout 4 at the left slingshot coil position (balloon measures to (0.227, 0.756), within ~0.02).
- pinmame.output.solenoid 5: Projected onto the Wall.RightSlingShot assembly's own drag-point centroid; the manual's printed page-82 playfield diagram marks callout 5 at the right slingshot coil position (balloon measures to (0.698, 0.754), within ~0.03).
- pinmame.output.solenoid 7: Projected onto the four 4-Bank drop targets' own switch positions (switches 17-20): one reset coil actuates the whole bank -- the retained script's sol4Bank raises all four targets in one pulse and the mechanism parts page documents one shared reset bar/coil -- so the placement set is the bank's four target positions, not a single coil-body coordinate.
- pinmame.output.solenoid 9: Projected onto the LeftFlipper table object's own pivot centre; the manual's printed page-82 playfield diagram marks callout 9 at the left flipper coil (balloon measures to (0.306, 0.863), within ~0.02).
- pinmame.output.solenoid 10: Projected onto the RightFlipper table object's own pivot centre; the manual's printed page-82 playfield diagram marks callout 10 at the right flipper coil (balloon measures to (0.633, 0.863), within ~0.02).
- pinmame.output.solenoid 11: Projected onto the RightFlipper1 table object's own pivot centre (the upper-right flipper's own bat, positioned mid-playfield); the manual's printed page-82 playfield diagram marks callout 11 at the upper-right flipper coil on the right side (balloon measures to (0.824, 0.491), within ~0.03 of this pivot).
- pinmame.output.solenoid 14: Two-panel drop wall for Ramp Diverter 1; coordinates are the retained table's own Wall.DivTube and Wall.DivTube1 drag-point centroids. The manual's printed page-82 playfield diagram marks callout 14 at the same rear-left position (balloon (0.133, 0.067), within ~0.02-0.04 of both panels).
- pinmame.output.solenoid 15: Drop wall for Ramp Diverter 2; the coordinate is the earlier retained recreation's Wall.DivTube2 drag-point centroid, which agrees with the manual's printed page-82 callout 15 (balloon (0.258, 0.034), within ~0.034). The VPW v1.0 table's same-named wall sits at (0.433, 0.032), ~0.17 normalized units right of both the manual's callout and this recreation, and is disclosed as divergent retained geometry rather than promoted.
- pinmame.output.solenoid 17: Projected onto the three 3-Bank drop targets' own switch positions (switches 49-51): one reset coil actuates the whole bank (sol3Bank; the mechanism parts page's shared reset callout), so the placement set is the bank's three target positions.
- pinmame.output.solenoid 31: Projected onto the two rotating alien figures' own anchors: the forward motor output drives the same reversible mechanism whose encoder the switch-57 opto senses, so the placement set is the two figure anchors.
- pinmame.output.solenoid 32: Projected onto the two rotating alien figures' own anchors: the reverse motor output drives the same reversible mechanism as solenoid 31, so both direction records carry the same two figure anchors.
- pinmame.output.lamp 62: Documented projection: centroid of the three (Electro) Ramp feature lamps the retained table models (lamp 44 (0.768, 0.043), lamp 45 (0.945, 0.081), lamp 46 (0.930, 0.120)). The manual's lamp table names address 62 '(ELECTRO) BLACK LIGHT' (#44, LP00109) for that feature; the exact tube/socket position is not surveyed and neither retained recreation models a usable object (the VPW table's L62 is an out-of-bounds playfield-sized wash mesh, excluded as a modeling artifact).

## Counts

- Placements: 201
- Located input addresses: 56
- Located output bindings: 137
- Unresolved input addresses (used, no coordinate): 0
- Unresolved output bindings (used, no coordinate): 0
- Inputs with a controlled `cabinet_or_service` record: 12
- Inputs with a controlled `constant` record: 4
- Inputs with a controlled `unused` record: 8
- Inputs with a controlled `virtual` record: 2
- Outputs with a controlled `cabinet_or_service` record: 7
- Outputs with a controlled `unused` record: 18
- Outputs with a controlled `virtual` record: 25

## Promotion decision

Every used address carries a validated placement or a controlled `not_applicable` record; `conflicts` is empty; the six capInvSw10-normalized switch addresses all carry positive manufacturer construction evidence (trough opto board part numbers, the 'opto spinner' scoring text, and the alien mechanism's encoder disc + opto PCB); the star-bumper solenoid identity is the manual diagram's own callout positions; and the four former conflicts are resolved with the resolutions documented on the affected devices and in the curator's conflicts() docstring. The record is promoted to `author_ready` with `coverage.missing = []` and every coverage dimension validated.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/capcom/big-bang-bar-1996/extracted-vpxtool.manifest.json`, SHA-256 `8b1b7c6f35b98b0fecf1d88ac0746d81599fd8006189d58998c255de62fc2e90`, 2874 files, 1091052346 bytes.
- Human transcription of every printed switch/lamp table, SHA-256 `3e503420d32c307f409edaa57c80d6f4bfa9f01d90cd0e47dbc6ddc755188994`, and its companion solenoid/schematic transcription, SHA-256 `b996714bd9cd3811481ab0eb0ccce071c3d019819844eaffffaf5318e28c4bd5`.
- VPX object-geometry notes, SHA-256 `e1339971328d98e365b6574733b08f8dc1849814806bb2973019482c93468ac5`.
- Corroboration recreation table SHA-256 `ba5d1384397b8a1a9115b089e4a281634acb9bfb760fe096a320774a8fa2ba46` and its embedded script SHA-256 `cefa47a25952eb96fef752e2c0e718c00f9ce9d0e733aaa86f92ced7c18c5a84`, with the cited gameitems pinned under external:pinmame-review-artifacts/big-bang-bar/corroboration-table-cited/.
- VPinMAME script libraries core.vbs SHA-256 `d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72` and Capcom.VBS SHA-256 `03323ded224c5e67b0f7703978529889339e1fd7f73ebdd15002a4a6b794a95e` under external:pinmame-review-artifacts/big-bang-bar/vpm-script-libs/.
- IPDB machine-4001 photographs SHA-256 `ac3ba370260155e1d1288cc95017ee3c88605d5b0ac56948ef369c47dc7fabd5` (tube lady on the playfield) and `abb750b69bb58cff40f9265785cb91682ad101815a07628a00f5a983d46adf11` (overhead playfield) under external:pinmame-review-artifacts/big-bang-bar/ipdb-photos/.
