# Firepower (Williams, 1980) spatial audit

Status: validated and promoted to machines/author-ready/williams/firepower-1980.json.

The coordinate source is the retained `Firepower (Williams 1980).vpx` V1.0 by 3rdaxis, Slydog43 & G5K at SHA-256 `7786f7d073b6580e808acfb8aff60d1f30436f9d4d224b0ff57ca2ef899db179`, bounds `left=0 top=0 right=952 bottom=1974`, so every coordinate is x/952 and y/1974 rounded to at most six places. The flipper pivots land at y 0.827, the shooter-lane switch at 0.885 and the table's drain at 0.988, which is the check that the y divisor is right.

## Evidence decisions

- Every table object used was identified against the booklet's own location drawings (Figure 3 for coils, Figure 4 for switches) rather than taken from the script alone, because the script has one systematic binding defect: every StandupTarget handler pulses switch 48 (eight handlers, seven walls in the base table). Figure 4 was registered onto the table frame with ten control points (RMS 21.1 table units, about 0.02 of the width) and the seven walls resolved to standups 16, 31, 37, 14, 48, 50 and 38.
- Seven hidden devices have no table object and take the registered Figure 4 callout at two decimals: the outhole (9), the playfield tilt (47), the lane-change switch (45), the three ball-ramp positions (51, 58, 57) and standup 49. The base table has no wall for 49; the Vs A.I. revision's StandupTarget8 wall sits at (0.1116, 0.3699), within 0.01 of the registered callout, and corroborates it.
- The three POWER targets and the top centre target are collidable primitives whose stored position is a local offset; their placements are the centres of their world-space mesh bounds from `vpxtool export obj --units vpu`.
- Lamp placements are the table's Light objects bound by `vpmMapLights` (TimerInterval = lamp number) and its explicit `Set Lights()` lines. Lamps 3 and 4 have two bulbs each, as Figure 6's `(x2)` says. Lamp 56, the playfield credit lamp, is modelled only by the Vs A.I. revision (CreditLight1, behind the apron's credit window, which IPDB's playfield photographs show).
- Solenoid 15 has two emitters, the two Type 89 flash lamps under the FIRE and POWER inserts, matching Figure 3's two callouts.
- Backbox lamps 50-55 and 57-64, the knocker (14), the coin lockout (16), the game-on relay (23), all cabinet and service switches, the DIPs and the displays take controlled not_applicable records.

## Explicit projections

- switch 9: Registered from the booklet's Figure 4 callout (outhole); the retained table has no object for this device. Two-decimal precision.
- switch 12: Drag-point centroid of the retained LeftSlingShot wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber.
- switch 14: Drag-point centroid of the retained StandupTarget4 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 16: Drag-point centroid of the retained StandupTarget1 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 29: Centre of the world-space mesh bounds of the retained TopTarget_6 primitive.
- switch 31: Drag-point centroid of the retained StandupTarget2 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 37: Drag-point centroid of the retained StandupTarget3 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 38: Drag-point centroid of the retained StandupTarget7 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 39: Centre of the world-space mesh bounds of the retained PTTarget_6 primitive.
- switch 40: Centre of the world-space mesh bounds of the retained PMTarget_6 primitive.
- switch 41: Centre of the world-space mesh bounds of the retained PBTarget_6 primitive.
- switch 42: Drag-point centroid of the retained RightSlingShot wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber.
- switch 45: Registered from the booklet's Figure 4 callout (lane-change); the retained table has no object for this device. Two-decimal precision.
- switch 47: Registered from the booklet's Figure 4 callout (playfield-tilt); the retained table has no object for this device. Two-decimal precision.
- switch 48: Drag-point centroid of the retained StandupTarget5 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 49: Registered from the booklet's Figure 4 callout (center-middle-left-standup); the base table has no wall for this standup. The Vs A.I. revision's StandupTarget8 wall at (0.111636, 0.369892) corroborates it to within 0.01. Two-decimal precision.
- switch 50: Drag-point centroid of the retained StandupTarget6 wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall).
- switch 51: Registered from the booklet's Figure 4 callout (left-ball-ramp); the retained table has no object for this device. Two-decimal precision.
- switch 57: Registered from the booklet's Figure 4 callout (right-ball-ramp); the retained table has no object for this device. Two-decimal precision.
- switch 58: Registered from the booklet's Figure 4 callout (center-ball-ramp); the retained table has no object for this device. Two-decimal precision.
- solenoid 1: Ball Release sits with the outhole below the apron; placed at the registered Figure 4 outhole callout, which Figure 3's callout 01 matches.
- solenoid 8: Ball Ramp Thrower sits at the exit end of the ball ramp below the apron; placed on the retained trough's exit kicker BallRelease, which throws into the shooter lane.
- solenoid 17: Projected onto the retained Bumper1 object the coil drives.
- solenoid 18: Projected onto the retained Bumper4 object the coil drives.
- solenoid 19: Projected onto the retained Bumper2 object the coil drives.
- solenoid 20: Projected onto the retained Bumper3 object the coil drives.
- solenoid 21: Projected onto the retained RightSlingShot object the coil drives.
- solenoid 22: Projected onto the retained LeftSlingShot object the coil drives.

## Excluded object classes

- ComboTrigger1-4, invisible triggers between the six 1-6 targets that pulse two adjacent target switches at once; a table aid for shots that strike two targets, not a device.
- B1T1-B4T8, rings of invisible triggers around the jet bumpers used only for the table's animation.
- StandupTarget walls' own switch number: all eight handlers pulse 48, so their identity comes from Figure 4 rather than the script.
- Drain, the retained trough's entry kicker on the table's bottom edge; the outhole placement is the booklet's registered callout instead.
- LBlueTopB/LBlueMiddleB/LBlueBottomB, LBumper*B and LBackHole1, co-located bloom and halo copies of bound lights.
- GI_* lights: general illumination is an unswitched 6.3 VAC supply with no controller address.
- All backglass Light, Flasher and Reel objects, which render the backbox and score displays.

## Counts

- Placements: 110
- Located input addresses: 45
- Located output bindings: 62
- Inputs with a controlled `cabinet_or_service` record: 13
- Inputs with a controlled `dip_switch` record: 18
- Inputs with a controlled `unused` record: 11
- Inputs with a controlled `virtual` record: 8
- Outputs with a controlled `cabinet_or_service` record: 17
- Outputs with a controlled `internal_nonvisual` record: 5
- Outputs with a controlled `unused` record: 3
- Outputs with a controlled `virtual` record: 4

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-vs-ai-v3.4.2.manifest.json`, SHA-256 `cb8357b34e6ed744e9bae39f3845fd6477a1361925f5d8248f54936349252055`, 1065 files, 332893876 bytes.
- Extraction manifest `external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-williams-1980-v1.0.manifest.json`, SHA-256 `119ea4e367f16ae078fe76ac9dcd50f80f8b01192e4bd413b1dbb963f9c26c31`, 1098 files, 252535142 bytes.
- Candidate geometry dump `external:pinmame-review-artifacts/firepower-1980/vpx-spatial-candidates.json`, SHA-256 `0dbb74f4f0d508c3b6b772f62f3dec5fe1e052b259def1f8698b0791e934d85c`.
- Primitive world bounds `external:pinmame-review-artifacts/firepower-1980/primitive-world-bounds.json`, SHA-256 `0d4a67a9f99f6e04c67a56ff231eba434e855282a1d87e936920319f4b5c7fc1`.
- Transcribed excerpts and crops under `evidence/excerpts/williams.firepower.1980/`.
