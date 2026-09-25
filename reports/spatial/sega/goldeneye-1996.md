# GoldenEye (Sega, 1996) spatial review

Status: observed. Every playfield switch, coil, magnet, flasher socket the table models and lamp is placed from the retained table or carries a controlled `not_applicable` record, but every coordinate is `observed`: the retained manual scan lost the callout numbers of its location drawings, so nothing can be checked against a factory drawing. The record stays at `machines/partial/sega/goldeneye-1996.json`.

The geometry source is the retained known-working `Goldeneye (Sega 1996) VPW 1.2.1.vpx` (SHA-256 `4438e8e271d4593abc8b9faa5ef1a586b6b004692010fc8eaafbbf1ce0ef9310`); its embedded script (SHA-256 `b0f1e0d13ee5ca2729e01000d9205a4de75473e082be9338e429a01438f04a84`) is the runtime binding authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`; every coordinate is x/952 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority, cross-checked against the pinned VPW 1.2 script and the independent Dozer script; the operations manual is the physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; hash-pinned harness runs settle the satellite home and VUK opto polarity and the ball-serve sequence; the retained table supplies geometry.
- Trough switches 10-15 are projected onto the table's trough exit kicker, switch 20 onto the satellite dish, switches 23/24 onto the magnet positions and switch 56 onto the tank kicker.
- The lock-ball coil, up-down ramp plunger and satellite motor relay are projected onto the mechanism each moves.
- The speaker-panel GOLDENEYE lamps (72-80), the start button lamp (57), the knocker and coin meter drive lines and the backbox insert flash lamps are cabinet or backbox devices and are not placed.

## Blockers

- The retained manual scan keeps the outlines of its playfield switch, coil and flash-lamp location drawings but none of their callout numbers, so no placement can be checked against a factory drawing. Every coordinate comes from one community table (the VPW GoldenEye 1.2.1, itself built on the JPJ/32Assassin table) and stays observed. Promotion needs a scan with legible callouts, a second independent geometry source, or a survey of a real machine.
- Flasher sockets without a table object: 26 (Lower Flipper Magnet), 30 (Helicopter), the second socket of 28 (Satellite) and 29 (Lower Right Playfield), the Upper Left socket of 31 and both Upper Right sockets of 32 are not placed.
- Lamp 58 (Behind Eject Stand-Up) has no table light and is not placed.
- Lamp 40 (Under Ramp Bottom) is not placed: its only table object, LL40, has no bulb light or insert primitive, a wider falloff than any insert light, and is switched by the satellite launch ramp animation, so it stands for a ramp effect rather than a socket.
- Playfield general illumination has no factory socket list; its 37 emitters come from the retained table's GI collection.

## Explicit projections

- pinmame.input.switch 10: Trough switch projected onto the retained BallRelease kicker, where the table's bsTrough holds balls on 10-14 and ejects them; the table models no per-ball trough object.
- pinmame.input.switch 11: Trough switch projected onto the retained BallRelease kicker (see switch 10).
- pinmame.input.switch 12: Trough switch projected onto the retained BallRelease kicker (see switch 10).
- pinmame.input.switch 13: Trough switch projected onto the retained BallRelease kicker (see switch 10).
- pinmame.input.switch 14: Trough switch projected onto the retained BallRelease kicker (see switch 10).
- pinmame.input.switch 15: VUK opto projected onto the retained BallRelease kicker, the table's stand-in for the trough up-kicker it sits on.
- pinmame.input.switch 20: Satellite home cam switch projected onto the satellite dish primitive RadarA; the switch sits on the motor base under it.
- pinmame.input.switch 23: Magnet-board ball detection projected onto the RadarKicker the table uses to hold a ball on the satellite magnet.
- pinmame.input.switch 24: Magnet-board ball detection projected onto the FlipperMagnet trigger between the flippers.
- pinmame.input.switch 56: Tank switch projected onto the TankKickBig kicker where the table's bsTank (switch 56) holds balls.
- pinmame.output.solenoid 1: Kicker BallRelease (projection: the table's trough exit stands in for the up-kicker)
- pinmame.output.solenoid 17: Kicker BallRelease (projection: the lock-ball coil sits on the trough beside the up-kicker)
- pinmame.output.solenoid 18: Primitive MrampA (projection: the plunger sits under the up-down ramp the script moves)
- pinmame.output.solenoid 21: Primitive RadarA (projection: the relay drives the satellite motor under the dish)

## Counts

- Placements: 171
- Validated input addresses: 0
- Observed-only input addresses: 45
- Validated output bindings: 0
- Observed-only output bindings: 87
- Output bindings without a placement: 4
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 15
- Inputs with a controlled `virtual` record: 2
- Outputs with a controlled `cabinet_or_service` record: 12
- Outputs with a controlled `internal_nonvisual` record: 6
- Outputs with a controlled `unused` record: 10
- Outputs with a controlled `virtual` record: 12

## Promotion decision

Refused. `coverage.missing` is `["output_semantics", "spatial_placement", "unresolved_conflicts"]`: every coordinate rests on one community table with no legible factory drawing to check it against, several flasher sockets and lamps 40 and 58 have no socket object, public solenoids 35 and 36 carry magnet-board latch bits whose meaning no source states, and the manual's lamp grid and bulb pages disagree about bulb types (conflict.bulb-types).

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/sega/goldeneye-1996/extracted-vpxtool.manifest.json`, SHA-256 `d4d2fd649ab9a3b5b1ae9b9e8ad5c2ed720b7a1d1b637db5bb1edc3cff34ab69`, 4144 files, 483050999 bytes.
- Operations manual SHA-256 `0203f37a1342e9ecb0205a37a5d45fa695591904e1355d43291565605214470f`.
