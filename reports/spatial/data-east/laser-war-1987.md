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
- Manual SHA-256: `e8e55768c990f2967594f4112bc2ec7403c55e5283c7b69fae2ff5c1d21fefbf`
- Technical chart SHA-256: `30a1def10178a2cf7e753046ed44f07d01075a6333791669e4fe0c4e165ddfe7`
- Extraction manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Extraction manifest SHA-256: `9642a642737c4513b1a26d311a5c298e0f7c511e83f7bdfad7d70f0e211c10c1`
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
- Placement records: 116
- Candidate/projection devices: `switch.matrix-14`, `switch.matrix-15`, `switch.matrix-21`, `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `coil.driver-25`, `coil.driver-26`

## Explicit projection classes

- `helper-group-centroid` (candidate): `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-25`, `coil.driver-26`. The retained script drives groups of visual helper objects but exposes no single physical socket object; their group centroids remain candidate effect anchors, not observed emitter positions.
- `special-solenoid-to-mechanism` (candidate): `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`. The community technical chart identifies each physical special-solenoid device, while the known-working table supplies the matching bumper or slingshot assembly. Coordinates project the hidden coil to that assembly rather than claim a winding-center measurement.
- `wall-drag-point-centroid` (candidate): `switch.matrix-14`, `switch.matrix-15`, `switch.matrix-21`. The retained VPX implements these rubber contacts as Wall surfaces. Their placements are centroids of authoring drag points, useful as reconstruction anchors but not observed physical switch-body centers.

## Excluded helper classes

- `backwall_flashers`: Flasherbase1/2 effects added by the retained table are not extra devices in the printed coil chart
- `lamp_suffix_a`: secondary insert glow/light-map primitives are not physical bulbs
- `tower_lights`: l8a-v/l9a-v/l10a-v/l11a-v are aggregate tower render helpers, not defensible socket observations

## Blockers

- **controller_platform** — `pinmame.dataeast`: Laser War uses Data East CPU/driver hardware, not a Williams System 11 board. No reviewed pinmame.dataeast controller profile exists yet. Would resolve: A reviewed Data East controller profile derived from pinned source and original board documentation.
- **polarity** — `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`, `switch.matrix-46`, `switch.matrix-47`: The community technical chart prints the physical flipper/EOS wiring, but controller-facing runtime behavior conflicts with the printed EOS labels and no retained evidence establishes the polarity translation. Would resolve: Bench observation of controller-facing flipper-button and EOS polarity synchronized with the physical contacts.
- **output_semantics** — `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `coil.driver-22`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`: The explicit game-specific Coil No. 17-22 table and the mapping inferred from shared Data East PIA comments plus setSSSol disagree on four of the six special-solenoid bindings. The chart marks physical special circuit 22 and right-bank branches 6R-8R unfitted, but pinned PinMAME can still publish their PIA or K1-multiplexed public state at addresses 22 and 30-32. Would resolve: A LibPinMAME trace observing public outputs 17-22 and 30-32 while each bumper and slingshot switch is fired and relay K1 is toggled.
- **mechanism_behavior** — `mechanism.kickback`, `coil.driver-15`, `switch.matrix-17`: The chart proves that public output 15 drives a relay and that a separately powered 23-900 coil performs the kick, while the script proves that switch 17 triggers the local kick only while the relay is armed. The retained sources do not expose the relay-to-local-coil interface or timing well enough to make the downstream coil a controller actuator. Would resolve: A traced schematic path or synchronized bench capture of output 15, switch 17, and the local kickback winding.
- **spatial_placement** — `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-49`, `coil.driver-5`, `coil.driver-11`: The retained table exposes only aggregate tower helpers for these controlled lamps/flashers and does not map its downstream GI bulbs to the physical relay circuit. Would resolve: A socket-level playfield/tower and GI-harness survey tied to printed addresses.

## Conflicts

- `conflict.switch-17-name`
- `conflict.right-flipper-eos-runtime`
- `conflict.left-flipper-eos-runtime`
- `conflict.lamp-8-runtime-binding`
- `conflict.lamp-26-printed-label-duplicate`
- `conflict.mars-yellow-printed-device-type`
- `conflict.mux-bank-output-typing`
- `conflict.special-solenoid-public-mapping`
- `conflict.synthetic-flipper-public-state`

## Promotion decision

Keep partial. The special-solenoid public mapping remains conflicted, and the Data East controller profile, kickback's relay-to-local-coil implementation, flipper/EOS polarity, and socket-level tower/GI placements remain authoring-critical blockers.
