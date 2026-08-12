# Data East Secret Service (1988) spatial audit

Status: **partial**. Format `pinmame-spatial-blockers`.

## Coordinate convention

- Space: `playfield`
- x: `raw_x / 952`; 0=left, 1=right
- y: `raw_y / 2162`; 0=rear/backglass, 1=apron/player
- Source bounds: `{"bottom": 2162.0, "left": 0.0, "right": 952.0, "top": 0.0}`

## Extraction identity

- Table SHA-256: `5d724f84cfd2b9580a0e438655397919d0ba289be356adea67e7f12f4d7e19e8`
- Script SHA-256: `b49f27dd97ad6a106a2f2bf4a0181bda86e58e31b0e88efe3663e614ace237e3`
- Production manual SHA-256: `f2d9c030951d1d8fef3db36447457689b69bac557935053293dd3c143ec4252a`
- Extraction manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Extraction manifest SHA-256: `5c80483c2010460c736a8d2e91ef887a72766f08b98fbf939e8abb727aae68ce`
- Extraction files: 972, bytes: 53434484
- vpxtool: `git:0561bb4`

## Method

- Asserted exact gamedata.json bounds (0,0)-(952,2162) before normalization.
- Stripped whole-line VBScript comments before recognizing callbacks; commented SolCallback(12/13) lines contribute no placement.
- Resolved switch objects only where executable handlers or BallStack/VLock initialization expose the object/address relationship.
- Resolved all L1..L64 coordinates at candidate strength only: the name convention and custom ChangedLamps loop are not an observed physical ROM-to-socket binding.
- Mapped active 101-109 pseudo-lamp visuals only where UpdateLamps exposes a defensible physical projection set; output 7 has no pseudo-lamp 107 visual, while the single S106/S109 proxies cannot place both printed locations of outputs 6/9.
- Omitted spatial keys where this thin retained table cannot support a physical placement.

## Placements

- Resolved device records: 112
- Placement records: 118
- Candidate devices: `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-8`, `coil.driver-14`, `coil.driver-15`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-30`, `coil.driver-32`, `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`

## Explicit projection classes

- `lamp-object-name-candidate` (candidate): `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`. Exactly 64 Light objects are named L1..L64, but object names and the custom fading loop do not prove physical socket bindings.
- `pseudo-lamp-visual-proxy` (candidate): `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-8`. Active SolCallback lines route these outputs through pseudo-lamps 101-105/108; visual objects are effect proxies, not surveyed bulb sockets.
- `mechanical-effect-object` (candidate): `coil.driver-14`, `coil.driver-15`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-30`, `coil.driver-32`. Direct callbacks establish the moving table object or object group, but the coordinate is an effect anchor rather than an observed under-playfield coil center.

## Excluded helper classes

- `backbox_only_callbacks`: whole-line-commented SolCallback(12/13) statements are excluded from executable evidence
- `flasher_objects`: the nine extracted Flasher gameitems are ball-shadow/general render effects, not controller-output emitters
- `gi_collection`: the GI collection mixes inserts, playfield effects and helpers and cannot support a socket count or socket-level placement
- `lamp_suffix_helpers`: L22a and L39a/L39b are additional render emitters, not extra matrix addresses
- `lamp_visual_binding`: L1..L64 names are visual candidates, not observed physical ROM-to-socket bindings
- `missing_pseudo_107`: SolCallback(7) sets pseudo-lamp 107 but UpdateLamps has no 107 visual object
- `missing_switch_27_object`: the script contains an S27_Hit handler but the extraction has no gameitem named S27
- `mixed_location_single_proxies`: S106 and S109 are single presentation proxies for outputs whose printed descriptions each name both a playfield feature and a cabinet emitter; neither can represent the complete physical placement set.

## Unresolved records

- **physical_socket_binding** — `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`: All L-number placements remain candidate.
- **gi_socket_placement** — `coil.driver-11`: The retained GI collection mixes inserts, effects and helpers.
- **switch_placement** — `switch.matrix-27`: The script has S27_Hit but no extracted S27 gameitem.
- **output_placement** — `coil.driver-6`, `coil.driver-7`, `coil.driver-9`, `coil.driver-13`, `coil.driver-16`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`: No defensible complete socket/actuator placement is bound. Outputs 6, 7 and 9 span a printed playfield feature plus a cabinet emitter but have at most one retained visual proxy; output 13's Coil Test adds an unresolved Clear Mars emitter to its detailed-table backglass label.

## Blockers

- **output_semantics** — `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`: PinMAME modulation types conflict with the manual-plus-script L/R public mapping. Would resolve: A PinMAME maintainer explanation or corrected output-type block, plus a controller trace proving public callbacks across relay states.
- **spatial_placement** — `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`, `coil.driver-6`, `coil.driver-7`, `coil.driver-9`, `coil.driver-11`, `coil.driver-13`, `coil.driver-16`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `switch.matrix-27`: Object-name lamp candidates, mixed GI helpers, unresolved mixed-location output emitters, unplaced mechanisms and one missing switch object prevent validated socket-level placement. Would resolve: A socket-address survey of an original playfield/back panel and a corrected retained table object for switch 27.
- **mechanism_behavior** — `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`: The manual identifies each fitted special-coil circuit, but the public 17-22 source interpretation is disputed and the retained script provides no SolCallback pulse timing or actuator-center evidence. Would resolve: A runtime trace that captures each public special-solenoid pulse while its trigger switch is exercised, plus an under-playfield actuator survey.
- **polarity** — `switch.matrix-30`, `switch.matrix-31`, `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`: EOS-numbered matrix addresses carry simulated button state, and the right callback combines lower and upper flippers. Would resolve: Bench capture of button/EOS states and public power/hold outputs on an original machine or faithful PinMAME harness.

## Conflicts

- `conflict.switch-score-labels-matrix-vs-list`
- `conflict.left-flipper-eos-runtime`
- `conflict.right-flipper-eos-runtime`
- `conflict.lamp-matrix-vs-description-list`
- `conflict.mux-bank-output-typing`
- `conflict.right-flipper-power-wire`
- `conflict.output-13-description`
- `conflict.special-solenoid-public-mapping`
- `conflict.special-coil-driver-transistors`
- `conflict.synthetic-flipper-public-state`

## Promotion decision

Keep partial. Mux-bank output typing, traced special-coil public mapping and timing, flipper/EOS behavior, and validated physical placements remain authoring-critical blockers.
