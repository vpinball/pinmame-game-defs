# Data East Laser War (1987) spatial audit

Status: **partial**. Format `pinmame-spatial-blockers`.

## Coordinate convention

- Space: `playfield`
- x: `raw_x / 964`; 0=left, 1=right
- y: `raw_y / 2162`; 0=rear/backglass, 1=apron/player
- Source bounds: `{"bottom": 2162.0, "left": 0.0, "right": 964.0, "top": 0.0}`

## Extraction identity

- Table SHA-256: `43b88ba675a1e8430d822930100c386f5cf63c2e18fa048b339cf54eb4fed586`
- Script SHA-256: `18c2679106173f13dc4a2b38f3d41e76c6be9d86f0637be04a6c6b8ec749d163`
- Manual SHA-256: `f6c6a09a6c9be42d8851790a5b40060fef7a4dbd6e452e1aa89af4765783a3db`
- Extraction manifest SHA-256: `3bfd3b8d21bdeeca6d6a83daf60d7694a4052bff881cbeae6409f6b3a44031b0`
- Extraction files: 2927, bytes: 163816471
- vpxtool: `git:0561bb4`

## Method

- Asserted exact gamedata.json bounds (0,0)-(964,2162) before normalization.
- Resolved switches from the script's actual handlers, including two separate objects for switch 21.
- Mapped matrix lamps only to primary physical-bulb Light objects; excluded suffix-a glow/lightmap and tower render-helper primitives.
- Mapped flasher domes and coils to their exact retained-table objects. Helper-only insert-flasher centroids remain candidate, not observed physical sockets.
- Applied controlled not_applicable dispositions to unused, virtual, cabinet/backbox, service, DIP, display, and internal nonvisual devices.

## Placements

- Resolved device records: 111
- Placement records: 141
- Candidate/projection devices: `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-25`, `coil.driver-26`, `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`

## Explicit projection classes

- `helper-group-centroid` (candidate): `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-25`, `coil.driver-26`. The retained script drives groups of visual helper objects but exposes no single physical socket object; their group centroids remain candidate effect anchors, not observed emitter positions.
- `synthetic-flipper-winding-to-flipper-object` (candidate): `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`. PinMAME synthesizes power/hold outputs for the two physical flippers; each winding is projected onto its corresponding retained flipper object and remains candidate while the physical flipper/EOS circuit is unresolved.

## Excluded helper classes

- `backwall_flashers`: Flasherbase1/2 effects added by the retained table are not extra devices in the printed coil chart
- `lamp_suffix_a`: secondary insert glow/light-map primitives are not physical bulbs
- `tower_lights`: l8a-v/l9a-v/l10a-v/l11a-v are aggregate tower render helpers, not defensible socket observations

## Blockers

- **output_semantics** — `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `coil.driver-22`: The scan's schematic pages 25-34 lose their right halves. The intact manual says circuits 1-6 operate pop bumpers/slingshots but does not map circuit numbers to devices. Would resolve: A complete Laser War switch/special-solenoid schematic or traced original wiring harness.
- **polarity** — `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`, `switch.matrix-46`, `switch.matrix-47`: The physical flipper/EOS circuit lies in the damaged schematic region and controller-facing runtime behavior conflicts with the printed EOS labels. Would resolve: An intact flipper schematic plus bench observation of controller-facing switch polarity.
- **spatial_placement** — `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-49`, `coil.driver-5`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `coil.driver-22`: The retained table exposes only aggregate tower helpers or no binding for these physical devices; special-coil devices are themselves unresolved. Would resolve: Socket-level playfield/tower survey tied to printed addresses, plus the complete special-solenoid schematic.

## Conflicts

- `conflict.switch-17-name`
- `conflict.right-flipper-eos-runtime`
- `conflict.left-flipper-eos-runtime`
- `conflict.lamp-8-runtime-binding`
- `conflict.ramp-multiplier-printed-coil-label`
- `conflict.mars-yellow-printed-device-type`

## Promotion decision

Keep partial. Output semantics for 17-22, flipper/EOS polarity, and socket-level tower/lamp placements remain authoring-critical blockers.
