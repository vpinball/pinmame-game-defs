# Time Machine spatial-resolution report

Exact retained-table bounds: `left=0`, `top=0`, `right=1000`, `bottom=1910`.

The resolver fails if either right or bottom changes. Coordinates use player-view playfield space; backbox and service devices are never projected onto it.

## Extraction identity

- Manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Manifest SHA-256: `91bb4c4b3be5b24ea9b77493e46d83810dd549ca10186ae47da4a1f8f9eaa185`

## Promotion decision

Keep partial. Runtime activity of mux states 29-32, SP1/SP2 placement, EOS/button semantics, lamp 25 location, special-coil behavior, polarity, and socket-level placement remain unresolved.

## Blockers

### output_semantics

Pinned source configures four distinct emulator-published mux-state output types at 29-32, but static evidence does not prove runtime activity. The retained manual has no printed device row for these public states and the retained script registers no callback, so availability is unknown and no physical quantity or socket is claimed.

Would resolve: A retained original-machine or LibPinMAME runtime trace that records each public state 29-32 under controlled relay conditions, paired with a source-backed circuit or socket survey.

Devices: `coil.driver-29`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`

### mechanism_behavior

Hardware-triggered special-coil pulse timing is absent from the retained public callbacks, and SP1/SP2 physical assignment conflicts.

Would resolve: Original-machine captures of each bumper/slingshot switch and special-solenoid state, with right and center bumpers exercised separately.

Devices: `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-21`, `coil.driver-22`

### polarity

Physical EOS contacts and controller-facing button/synthetic winding states share public meanings without an at-rest/end-of-stroke bench capture.

Would resolve: Bench capture of cabinet button, EOS at rest/end of stroke, and public power/hold states on an original machine or faithful harness.

Devices: `switch.matrix-15`, `switch.matrix-16`, `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`

### spatial_placement

Lamp positions are table candidates, two pop actuators conflict, and flash groups lack socket-level coordinates.

Would resolve: A photographed socket/address survey above and below an original playfield plus the backbox/back-panel lamp boards.

Devices: `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-9`, `coil.driver-12`, `coil.driver-13`, `coil.driver-14`, `coil.driver-15`, `coil.driver-17`, `coil.driver-22`, `coil.driver-29`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`

### unresolved_conflicts

Three machine-specific source disagreements remain first-class and promotion-critical. The two flipper end-of-stroke naming records are recorded as ignored: the answer cannot reach a recreation, so they are not listed here.

Would resolve: Corrected upstream sources or independent original-machine traces that explicitly settle each conflicting state.

Devices: `conflict.shared-port-position-2-vs-unfitted`, `conflict.special-coil-right-center-location`, `conflict.lamp-25-playfield-vs-table-backglass`

## Resolver controls

- Asserted both exact gamedata.json bounds (0,0)-(1000,1910) before normalization; width agreement alone is insufficient.
- Removed whole-line VBScript comments before attributing callbacks or vpmMapLights membership.
- Resolved switch coordinates only from executable sensor objects or the native slingshot wall segment tied to that public address.
- Established the lamp idiom from executable vpmMapLights AllLamps plus each Light TimerInterval. The collection has 134 Light members: TimerInterval 1-64 map hardware addresses; sole TimerInterval 65 member l65 is unreachable from the 64-address controller matrix.
- Recorded numeric l1-l64 centers at candidate strength only where the manual places the lamp on the playfield. Backbox/back-panel lamps are controlled not_applicable records; lamp 25 has no placement because source locations conflict.
- Used script for causal topology and the rendered manual for construction. A printed feature label by itself never created a mechanism edge.

## Excluded helpers

- `lamp_65`: l65 is an is_backglass=true hSpacewarpLights helper with TimerInterval 65. PinMAME publishes only lamp addresses 1-64, so ChangedLamps can never update slot 65; it is not a 65th output.
- `lamp_reflections`: Additional AllLamps members sharing TimerInterval values are reflection, bloom, or backglass presentation objects; they do not multiply physical ROM addresses.
- `backbox_lamps`: Manual construction places 1-8 and 62 on the insert/backbox presentation and 26-30 on the back panel; table coordinates are presentation proxies, not playfield emitters.
- `flash_groups`: Callbacks for Flash No.1-No.9 expose visual effects but neither script grouping nor generic manual labels establish surveyed physical bulb centers.
- `muxed_states_29_32`: The manual describes the full left/right multiplexing design as effectively 23 regular coils, and s11.c configures four individual emulator-published mux-state types at 29-32. The device chart stops at SIDE R 04, the script binds no callback, and no runtime trace establishes per-address activity, fitted circuit, quantity, feature, or socket for R05-R08.
