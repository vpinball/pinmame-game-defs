# Earthshaker (Williams, 1989) spatial review

Status: partial.

Geometry comes from the retained known-working VPW-Lite v006 table (SHA-256 `7df82a9ab3196214bc03df98a0b2669bf49b27cee91814f341bb4bc1c27d9522`), whose embedded script (SHA-256 `0c2bb47c3469e9b04d28a44f94469c3935050aa4975d31ee12e6fb344392eb72`) is the runtime authority. Exact bounds are `left=0 top=0 right=964 bottom=2162`; every coordinate is x/964 and y/2162. The Williams operations manual is the physical authority; its location drawings were used to check sides and order, not to measure positions.

## Evidence decisions

- Jet-bumper switches follow the manual's drawing (54 top, 53 right, 52 left), the ROM's names, and the lamp and coil drawings, not the retained script, whose Bumper1/Bumper3 handlers swap 52 and 54.
- Coin chutes follow the switches list and the ROM (4 right, 6 left) over the matrix table's reversed pair.
- Right-ramp flashers follow the coil drawing (08C twice at the top, then 07C, then 06C down the right side), which agrees with the retained script's dome bindings.
- Speaker-panel jackpot lamps 58-64, the insert-board G.I. (11), the knocker (7), and the quake shaker (22) take controlled `cabinet_or_service` records.
- G.I. strings 10 and 15 are placed at the retained GIU and GI collections' bulbs; the manual prints no G.I. bulb count.

## Blocking gaps

- Solenoid 14: 2 bulbs printed, 1 placed; the location drawing gives two callout-14 leaders; the first ends on the center arrow insert where the table's f114 light sits, and the second on lamp 45's own insert (the lamp drawing's lamp-45 leader reaches the same insert), where the table models no flasher. The table's second bound light, f114a, sits on an unlabelled round insert that neither drawing gives a callout, so it is not used.
- Solenoid 16: 2 bulbs printed, 1 placed; the table models one dome (the on-ramp flasher at the upper left, where the manual's callout 16 leads); the jet-bumper bulb has no drawn or modelled location.
- Solenoid 26: 2 bulbs printed, 1 placed; the table models one dome (the center-ramp flasher where callout 02C leads); the building bulb has no drawn or modelled location.
- Solenoid 27: 2 bulbs printed, 1 placed; the table models one dome (beside the top jet bumper and spinner, where callout 03C leads); the second bulb has no drawn or modelled location.
- pinmame.input.switch 25, 26: observed only. Prototype building-height optos anchored at the building primitives' shared origin; no source draws the positioner board.
- pinmame.output.lamp 17, 18, 19, 20, 21, 22, 23, 24, 25: observed only. Building windows placed at their window meshes' centres, one point per column; the lamp-board sockets behind them are not surveyed.

## Explicit projections

- pinmame.input.switch 25: Building Height 1 is an optotransistor on the prototype Bldg Positioner Bd (p/o C-12406), which no retained source draws; it is anchored at the Institute building it senses. The anchor is the InstituteBackWall primitive's origin, which the building's baked meshes share, not a sensor position, so the placement is observed only.
- pinmame.input.switch 26: Building Height 2 shares switch 25's anchor for the same reason.
- pinmame.input.switch 37: The Top Ball Popper switch (A-11658) sits in the popper assembly under its cap; anchored at the retained TopVUK kicker, which the script closes 37 from.
- pinmame.input.switch 40: The Bottom Ball Popper switch (A-11658) sits in the popper assembly; anchored at the retained BottomVuk kicker, which the script closes 40 from.
- pinmame.input.switch 42: Fault Open is the roller micro-switch (item 12, 5647-12073-06) inside the Zone Opener Assembly (C-12429) under the California/Nevada fault; no retained object models it, so it is anchored at the California map primitive (CalPrim) the fault coil slides.
- pinmame.input.switch 55: The slingshot switch pair (A-4834-H; B-8734-1) is inside the slingshot; anchored at the drag-point centroid of the retained LeftSlingShot wall.
- pinmame.input.switch 56: Anchored at the drag-point centroid of the retained RightSlingShot wall.
- pinmame.output.solenoid 3: Drop Target Reset placed on the middle target (sw28) of the bank it resets.
- pinmame.output.solenoid 4: California Fault placed on the California map primitive the zone opener slides.
- pinmame.output.lamp 17: Building windows 17-25 are placed at their window meshes' centres (one point per column, rows differ only in height); the derivation is in each lamp's note.

## Counts

- Placements: 154
- Located input addresses: 43
- Located output bindings: 81
- Unresolved records: 0
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 10
- Outputs with a controlled `cabinet_or_service` record: 10
- Outputs with a controlled `internal_nonvisual` record: 2
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 20

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/earthshaker-1989/extracted-vpxtool.manifest.json`, SHA-256 `cc52978345233ac0650ea8e54173b18494e19d1e75d57a88c95941c295159f76`, 2447 files, 258155460 bytes.
- Manual SHA-256 `94ad82c16f1ae72fd7b71cdadf4616c8166fd545a2740efe5cda2cc9b1a8db3b`; committed excerpts under `evidence/excerpts/williams.earthshaker.1989/`.
- Runtime evidence `evidence/runtime/system-11/earthshaker-la3-service-and-mechanisms.json` and `evidence/runtime/system-11/earthshaker-pa1-prototype-service.json`.
