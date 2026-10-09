# Black Knight (Williams, 1980) spatial audit

Status: validated and promoted to machines/author-ready/williams/black-knight-1980.json.

The coordinate source is the retained `Black Knight (Williams 1980).vpx` 3.0 by Bord at SHA-256 `bfaf38dfacd2c7982a609ec219e041c01886eb53cb368ae225e1d7924a5c994c`, bounds `left=0 top=0 right=952 bottom=1974`, so every coordinate is x/952 and y/1974 rounded to at most six places. The lower flipper pivots land at y 0.829, the shooter-lane switch at 0.879 and the drain kicker at 0.986, which is the check that the y divisor is right. The upper playfield's objects share the same frame, so upper-playfield devices overlie the rear of the lower playfield in normalized space.

## Evidence decisions

- Switch, lamp and coil objects are the ones the retained script binds: switch handlers, the DTArray drop-target primaries, the cvpmBallStack and cvpmMagnet objects, and the insert lights InitLights binds by TimerInterval. Each was checked against the booklet's Figure 2 and Figure 3.
- Eight hidden switches have no table object and take the booklet's Figure 3, registered onto the table frame, at two decimals: the outhole (20), the three ball-ramp positions (17, 18, 19), the three lockup-trough positions (41, 42, 43) and the playfield tilt (46). The fit uses eighteen control points with a 9.4 table-unit RMS residual, and every reading lies inside the controls' convex hull; the registered lockup switches land on the table's lock kickers, and the registered outhole lies 7.6 table units from the outhole tab of the playfield cut-out shown in the table's playfield image.
- The three rebound standups 28, 32 and 40 are optional, fitted on early machines only; each is projected onto its bank's centre target.
- The Magna-Save magnets (relays 9 and 10) take the table's invisible magnet triggers. Figure 2's dashed callouts lie further inboard and higher, but IPDB's stripped-playfield and under-playfield photographs show the emblems and the magnets near the sides, where the table puts them.
- Lamp placements are the insert lights; every playfield lamp has exactly one bulb. Lamp 7 (Credits (Playfield)) and 43-46 have no bulb on the machine.
- Backbox lamps 1-6 and 8, the bell (15), the coin lockout (16), the GI relay (11), the game-on relay (25), all cabinet and service switches, the DIPs and the displays take controlled not_applicable records.

## Explicit projections

- switch 17: Registered from the booklet's Figure 3 (right-ball-ramp); the retained table has no object for this switch. Two-decimal precision.
- switch 18: Registered from the booklet's Figure 3 (center-ball-ramp); the retained table has no object for this switch. Two-decimal precision.
- switch 19: Registered from the booklet's Figure 3 (left-ball-ramp); the retained table has no object for this switch. Two-decimal precision.
- switch 20: Registered from the booklet's Figure 3 (outhole); the retained table has no object for this switch. Two-decimal precision.
- switch 21: Drag-point centroid of the retained LeftSlingshot wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber.
- switch 22: Drag-point centroid of the retained RightSlingshot wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber.
- switch 25: Drag-point centroid of the retained sw25 drop-target wall, the primary of this target in the script's DTArray.
- switch 26: Drag-point centroid of the retained sw26 drop-target wall, the primary of this target in the script's DTArray.
- switch 27: Drag-point centroid of the retained sw27 drop-target wall, the primary of this target in the script's DTArray.
- switch 29: Drag-point centroid of the retained sw29 drop-target wall, the primary of this target in the script's DTArray.
- switch 30: Drag-point centroid of the retained sw30 drop-target wall, the primary of this target in the script's DTArray.
- switch 31: Drag-point centroid of the retained sw31 drop-target wall, the primary of this target in the script's DTArray.
- switch 33: Drag-point centroid of the retained sw33 drop-target wall, the primary of this target in the script's DTArray.
- switch 34: Drag-point centroid of the retained sw34 drop-target wall, the primary of this target in the script's DTArray.
- switch 35: Drag-point centroid of the retained sw35 drop-target wall, the primary of this target in the script's DTArray.
- switch 37: Drag-point centroid of the retained sw37 drop-target wall, the primary of this target in the script's DTArray.
- switch 38: Drag-point centroid of the retained sw38 drop-target wall, the primary of this target in the script's DTArray.
- switch 39: Drag-point centroid of the retained sw39 drop-target wall, the primary of this target in the script's DTArray.
- switch 41: Registered from the booklet's Figure 3 (lockup-bottom); the retained table has no object for this switch. Two-decimal precision.
- switch 42: Registered from the booklet's Figure 3 (lockup-center); the retained table has no object for this switch. Two-decimal precision.
- switch 43: Registered from the booklet's Figure 3 (lockup-top); the retained table has no object for this switch. Two-decimal precision.
- switch 46: Registered from the booklet's Figure 3 (playfield-tilt); the retained table has no object for this switch. Two-decimal precision.
- switch 28: Projected onto the lower left bank's centre target (sw26): the rebound switch stood in the playfield cutout behind the bank, and neither the table nor any drawing locates it more exactly.
- switch 32: Projected onto the lower right bank's centre target (sw30): the rebound switch stood in the playfield cutout behind the bank, and neither the table nor any drawing locates it more exactly.
- switch 40: Projected onto the top right bank's centre target (sw38): the rebound switch stood in the playfield cutout behind the bank, and neither the table nor any drawing locates it more exactly.
- solenoid 1: Ball Release sits at the outhole below the apron; placed at the registered Figure 3 outhole, which Figure 2's callout 01 matches.
- solenoid 6: Ball Ramp Thrower sits at the exit end of the ball ramp below the apron; placed on the retained trough's exit kicker BallRelease, which throws into the shooter lane.
- solenoid 7: Multi-Ball Release placed on the retained lock's exit kicker LockOut, which the registered lockup-trough drawing confirms within 0.01.
- solenoid 2: Drop-target reset coil projected onto the bank's centre target (sw26); the coil sits under the bank.
- solenoid 3: Drop-target reset coil projected onto the bank's centre target (sw30); the coil sits under the bank.
- solenoid 4: Drop-target reset coil projected onto the bank's centre target (sw34); the coil sits under the bank.
- solenoid 5: Drop-target reset coil projected onto the bank's centre target (sw38); the coil sits under the bank.
- solenoid 9: The relay switches a magnet; placed at the retained table's invisible magnet trigger MagnetR, which IPDB's stripped and under-playfield photographs corroborate. Figure 2's dashed callout sits further inboard and higher and is a label, not the device.
- solenoid 10: The relay switches a magnet; placed at the retained table's invisible magnet trigger MagnetL, which IPDB's stripped and under-playfield photographs corroborate. Figure 2's dashed callout sits further inboard and higher and is a label, not the device.
- solenoid 17: Projected onto the retained LeftSlingshot object the coil drives.
- solenoid 18: Projected onto the retained RightSlingshot object the coil drives.
- solenoid 19: Projected onto the retained Bumper1 object the coil drives.

## Excluded object classes

- l7, an apron Light at the credit-window position whose TimerInterval is 36: it lights with the jet bumper, and lamp 7 has no bulb on the machine.
- Drain, the retained trough's entry kicker on the table's bottom edge; the outhole placement is the booklet's registered callout instead.
- LockMech, the lock's entry kicker, which carries all three lockup switches; the switches take the registered Figure 3 positions.
- sw25y-sw39y secondary drop-target walls and the psw primitives, animation parts of the drop-target system; the primary walls are used.
- GI_* lights and Light17 (TimerInterval 100), the table's general illumination, which has no controller address beyond relay 11.
- TriggerLF, TriggerRF and metaltrigger_*, physics and sound helpers with no switch.
- All backglass Light, Flasher, Reel and TextBox objects, which render the backbox and score displays.

## Counts

- Placements: 101
- Located input addresses: 36
- Located output bindings: 65
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `dip_switch` record: 18
- Inputs with a controlled `unused` record: 18
- Inputs with a controlled `virtual` record: 8
- Outputs with a controlled `cabinet_or_service` record: 11
- Outputs with a controlled `unused` record: 13
- Outputs with a controlled `virtual` record: 4

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/black-knight-1980/extracted-vpxtool/black-knight-bord-3.0.manifest.json`, SHA-256 `dc16b9dbfc8b1d9fe199f26f8cd7daec7f16ce1d7938c1b8ae4f22e9a571948f`, 1323 files, 164805613 bytes.
- Figure 3 registration fit `external:pinmame-review-artifacts/black-knight-1980/figure3-registration-fit.py`.
- IPDB photographs `external:pinmame-review-artifacts/black-knight-1980/ipdb-images/`.
- Transcribed excerpts under `evidence/excerpts/williams.black-knight.1980/`.
