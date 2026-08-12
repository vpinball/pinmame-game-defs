# Data East Torpedo Alley (1988) spatial audit

Status: **partial**. Format `pinmame-spatial-blockers`.

## Coordinate convention

- Space: `playfield`
- x: `raw_x / 1000`; 0=left, 1=right
- y: `raw_y / 2000`; 0=rear/backglass, 1=apron/player
- Source bounds: `{"bottom": 2000.0, "left": 0.0, "right": 1000.0, "top": 0.0}`

## Extraction identity

- Table SHA-256: `f876db907452c59da2e6589536ab9df19945a91f06dc6d5e32f6e679e3ac2472`
- Script SHA-256: `5123b70af3dcfaba40f19ee4f941111621b35e24707dc7f461e76c0514fea61b`
- Manual SHA-256: `63ca7a98a303713487318c1f1d8ee77cc8b9ba37b20c918aa51e469e5aee5960`
- Extraction manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Extraction manifest SHA-256: `6ba07f0ac3d1e9e2bb1e441dde4066d99033bf5e7b11b81337708b16d1afe92e`
- Extraction files: 2111, bytes: 156444993
- vpxtool: `git:0561bb4`

## Method

- Asserted exact gamedata.json bounds (0,0)-(1000,2000) before normalization.
- Stripped whole-line VBScript comments before attributing callbacks or shared Lights() membership.
- Resolved switch objects only where executable handlers or explicit table primitives expose the address relationship; SW23 and SW36 stay candidate because their active handlers pulse the wrong public addresses.
- Recorded all L1..L64 coordinates at candidate strength. For 63 addresses, active script lines add visual groups to shared Lights(); address 24 is name-only. Neither class is a physical socket survey.
- UseLamps=1 delegates ChangedLamps consumption to the shared VPM core; the table script has no SetLamp/LampCallback/UpdateLamps/AllLamps loop of its own.
- Downgraded every drag-point and object-group centroid to candidate strength. A centroid is a computed derivation, not an observed object center.
- Retained the manual's two-bulb quantity for every 01L-08L flasher branch. The retained table supplies one usable effect anchor for 01L-06L, while 07L spans two disjoint helper clusters and 08L has no active callback; no unsupported physical socket positions are published.
- Omitted spatial keys where callbacks, helpers, or native physics cannot support a physical placement.

## Coordinate origins

- Measured object centers: 99
- Computed centroids: 18 (17 drag-point; 1 object-group)
- Computed devices: `coil.driver-29`, `switch.matrix-20`, `switch.matrix-21`, `switch.matrix-22`, `switch.matrix-24`, `switch.matrix-29`, `switch.matrix-30`, `switch.matrix-31`, `switch.matrix-33`, `switch.matrix-34`, `switch.matrix-35`, `switch.matrix-37`, `switch.matrix-38`, `switch.matrix-39`, `switch.matrix-40`, `switch.matrix-52`, `switch.matrix-53`, `switch.matrix-56`
- Disclosure: Point-like VPX objects carry their own center. Extended objects are represented by a computed drag-point centroid, while multi-object visual or mechanism groups use a computed group centroid. A centroid is a derivation, not an observation, and every such placement is reported separately at candidate strength.

## Placements

- Resolved device records: 114
- Placement records: 117
- Candidate devices: `switch.matrix-20`, `switch.matrix-21`, `switch.matrix-22`, `switch.matrix-23`, `switch.matrix-24`, `switch.matrix-29`, `switch.matrix-30`, `switch.matrix-31`, `switch.matrix-33`, `switch.matrix-34`, `switch.matrix-35`, `switch.matrix-36`, `switch.matrix-37`, `switch.matrix-38`, `switch.matrix-39`, `switch.matrix-40`, `switch.matrix-52`, `switch.matrix-53`, `switch.matrix-56`, `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-9`, `coil.driver-14`, `coil.driver-15`, `coil.driver-16`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-31`, `coil.driver-32`, `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`

## Explicit projection classes

- `shared-lights-array-coordinate-candidate` (candidate): `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`. Executable membership proves a shared runtime visual group, not a physical ROM-to-socket binding.
- `lamp-object-name-only-candidate` (candidate): `lamp.matrix-24`. L24 exists, but its only Lights(24) assignment is a whole-line comment.
- `flasher-visual-proxy` (candidate): `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-9`, `coil.driver-14`, `coil.driver-15`. Direct callbacks expose table effect objects; those objects are not surveyed physical bulb centers.
- `mechanical-effect-object` (candidate): `coil.driver-16`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-31`, `coil.driver-32`. Direct callbacks expose moving objects or effect anchors rather than under-playfield coil centers.
- `drag-point-centroid` (candidate): `switch.matrix-20`, `switch.matrix-21`, `switch.matrix-22`, `switch.matrix-24`, `switch.matrix-29`, `switch.matrix-30`, `switch.matrix-31`, `switch.matrix-33`, `switch.matrix-34`, `switch.matrix-35`, `switch.matrix-37`, `switch.matrix-38`, `switch.matrix-39`, `switch.matrix-40`, `switch.matrix-52`, `switch.matrix-53`, `switch.matrix-56`. Extended Wall objects have no intrinsic point; the published coordinate is the arithmetic centroid of their drag points and is not an observation.
- `object-group-centroid` (candidate): `coil.driver-29`. The published coordinate averages multiple VPX object centers and is only a mechanism/effect anchor, not any one physical device location.
- `physical-quantity-exceeds-effect-placement-count` (candidate): `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`. The manual fits two bulbs on every 01L-08L branch. The table exposes one usable candidate anchor for 01L-06L, two disjoint helper clusters rather than a physical center for 07L, and no active callback for 08L; missing socket positions are not duplicated or invented.
- `physical-lamp-quantity-exceeds-placement-count` (candidate): `lamp.matrix-1`, `lamp.matrix-16`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-8`. The manual prints two bulbs at these lamp addresses while the retained table supplies one candidate Light-object coordinate per address; second socket positions are not duplicated or invented.

## Excluded helper classes

- `backglass_proxies`: S10, S11, S12, S13 and S23 lie outside playfield bounds and are visual-only backglass proxies, not physical output relabelings
- `gi`: UseGI=0 and the output-11 GIUpdate assignment is overwritten later by Sol11BG; no socket-level GI placement is supported
- `lamp_24`: the only Lights(24) assignment is a whole-line comment; L24 remains a name-only coordinate candidate
- `lamp_object_names`: L1..L64 names alone are candidates, never observed physical ROM-to-socket bindings
- `output_8`: the manual fits 08L, but the retained output-8 callback is whole-line commented
- `shared_vpm_consumer`: UseLamps=1 delegates ChangedLamps consumption to the shared VPM core; this table script only populates the shared Lights() array
- `special_coils`: The manual and Data East PIA routing establish the five public special-coil mappings, but native bumper/slingshot physics has no executable SolCallback or physical effect object from which to derive an actuator center.
- `scope_flasher_group`: The output-7 callback drives six VPX lights in two widely separated clusters. Their arithmetic centroid lands in empty playfield, so it is not published as a physical Scope bulb position.

## Unresolved records

- **physical_socket_binding** — `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`: All lamp coordinates remain candidate; 24 lacks even active shared-array membership, and addresses 1, 8, 16, 23, 24, 31 and 32 each have a manual quantity of two but only one candidate object coordinate.
- **flasher_socket_quantity_placement** — `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`: The manual fits two bulbs at each 01L-08L address. The retained table exposes one usable effect anchor for 01L-06L, two disjoint helper clusters rather than a physical center for 07L and no active callback for 08L, so none supplies two independently identified physical socket centers.
- **gi_socket_placement** — `coil.driver-11`: The effective retained callback is an outside-playfield backglass proxy and UseGI=0 supplies no GI collection.
- **special_coil_placement** — `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-21`, `coil.driver-22`: Manual construction and Data East public mapping establish circuit topology, but native physics has no public SolCallback or physical effect object from which to derive an actuator center.

## Blockers

- **output_semantics** — `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`, `coil.driver-11`, `lamp.matrix-24`: Pinned output typing, effective callback 11 and active lamp-24 membership disagree with manual construction. Would resolve: A PinMAME maintainer explanation or corrected torp_ typing plus a controller trace of relay sides, GI 11 and lamp 24.
- **polarity** — `switch.matrix-15`, `switch.matrix-16`, `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`: Physical EOS contacts and cabinet-button simulation occupy the same public addresses without a bench state capture. Would resolve: Bench capture of cabinet-button, EOS-at-rest/end-of-stroke, and public power/hold states on an original machine or faithful harness.
- **spatial_placement** — `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`, `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-11`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-21`, `coil.driver-22`: Candidate visual names/effects, incomplete 01L-08L two-bulb socket counts, unbound GI and special coils do not establish every socket or actuator center. Would resolve: A socket/address and under-playfield actuator survey of an original playfield, insert board and backbox.
- **unresolved_conflicts** — `conflict.left-flipper-eos-runtime`, `conflict.right-flipper-eos-runtime`, `conflict.mux-bank-output-typing`, `conflict.special-solenoid-sp1-sp2-schematic-swap`, `conflict.output-11-callback-overwrite`, `conflict.switch-23-runtime-misroute`, `conflict.switch-36-runtime-misroute`, `conflict.lamp-24-runtime-omission`: Eight source disagreements remain first-class and promotion-critical. Would resolve: Corrected upstream sources or independent original-machine traces that explicitly choose each conflicting state without inference.

## Conflicts

- `conflict.left-flipper-eos-runtime`
- `conflict.right-flipper-eos-runtime`
- `conflict.mux-bank-output-typing`
- `conflict.special-solenoid-sp1-sp2-schematic-swap`
- `conflict.output-11-callback-overwrite`
- `conflict.switch-23-runtime-misroute`
- `conflict.switch-36-runtime-misroute`
- `conflict.lamp-24-runtime-omission`

## Promotion decision

Keep partial. Output typing, EOS/button state, special-coil semantic conflict and placement, two misrouted switches, lamp 24, GI behavior, the second physical bulb positions for 01L-08L, and other socket-level placements remain unresolved.
