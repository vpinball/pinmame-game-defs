# Johnny Mnemonic (Williams, 1995) spatial review

Status: observed. Every switch, coil, magnet and lamp that has a playfield location is placed from the retained table or carries a controlled `not_applicable` record, except the Clear Matrix coil and the flashers, which are measured on the manual's location drawing and stay `observed`; the playfield G.I. strings are placed from the table's G.I. collections and stay `observed`, and the Left Ramp Flasher and G.I. string 4 have no coordinate, which keeps the record at `machines/partial/williams/johnny-mnemonic-1995.json`.

The geometry source is the retained known-working `Johnny Mnemonic (Williams 1995) VPW v1.2.2.vpx` (SHA-256 `234c81299f3bff614fee39f9fa5594f060dbc06f49d96f8e68673fb07c03acf8`); its embedded script (SHA-256 `1a70a6128f293072261657597b4b62c404d16d5e88e50080a3bc163b2fe1d5ef`) is the runtime binding authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`; every table coordinate is x/964 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority; the September 1995 operations manual and its service bulletins are the physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry for named objects.
- Manual reconciliation (`external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py`): Least-squares affine fit of the 300 dpi render of printed 2-37 onto table coordinates through nine shared features (four corner matrix holes, two upper jet bumper centres, both flipper pivots, the Crazy Bob's eject box); worst control residual 0.013 normalized. The switch-location drawing (printed 2-35) was compared by eye: every placed switch's callout reaches the feature its table object stands on, and the drawing's Cyber Space Assy. inset puts 51/52/53 on the rear row and 71/72/73 at the front, as the script binds the Matrix kickers. Coil callouts measured through the same fit (pixel readings in the artifact): 01 ends 0.051 from its trough eject kicker, 02 0.003 from its autoplunger trigger, 33 (Left Diverter) 0.060 from the table's left diverter walls, and 05 (Clear Matrix) on the coil at the matrix's right rear corner, 0.129 from the centre hole, which is where solenoid 5 is placed. The other coil leaders were not measured.
- The hand's home switches, encoders, Ball In Hand switch and motor-control lines ride the moving Data Glove and carry `internal_nonvisual` records; the hand magnet is placed where the retained table's hand catches the popper ball.
- Flashers 18, 20, 25 and 28 also light a backbox insert-panel bulb, which is not placed; G.I. strings 1-3 also feed #555 backbox bulbs, and string 5 is backbox and cabinet only.

## Blockers

- The Clear Matrix coil (5) and flashers 17-20 and 26-28 have no table object at their location: the retained VPW table drives its flasher lightmaps from lights parked at the cabinet edge. Their coordinates are measured on the manual's solenoid/flashlamp location drawing through a nine-point least-squares fit (worst residual 0.013) and stay observed. Promotion needs a socket survey of a real machine or a retained table with modelled flasher sockets.
- The Left Ramp Flasher (25) has no callout on the location drawing and no socket in the table, so it has no coordinate.
- G.I. string 4 (public 3) is a playfield-only string with no factory socket list and no placed table light, so it has no coordinate.
- Playfield G.I. strings 1-3 have no factory socket list; every coordinate comes from the retained table's GIString1-3 collections and stays observed.
- Trough Jam (31) has no table object and is projected onto the Trough Ball 1 kicker, so it stays observed.

## Explicit projections and measurements

- pinmame.input.switch 31: Projected onto the trough eject kicker (Kicker sw32, the Trough Ball 1 position): the retained table models no Trough Jam object and its SolRelease pulses 31 on every eject, while the manual's switch drawing puts callout 31 at the shooter end of the trough beyond callout 32.
- pinmame.output.solenoid 6: Hand Magnet projected onto Kicker GloveMag, where the retained table's hand catches the ball the popper (Kicker KickToGlove) shoots up: the magnet rides the moving hand. Service Bulletin SB 85's troubleshooting asks the technician to verify that the magnet is positioned approximately over the ball popper when it fails to catch.
- pinmame.output.solenoid 5: Measured on the location drawing at the end of callout 05's leader, on the coil drawn at the right rear corner of the matrix through the affine fit; not a table object.
- pinmame.output.solenoid 17: Measured on the location drawing at the plain dome circle drawn between the two upper jet bumpers through the affine fit; not a table object.
- pinmame.output.solenoid 18: Measured on the location drawing at the end of callout 18's leader at the upper right corner of the Crazy Bob's eject box through the affine fit; not a table object.
- pinmame.output.solenoid 19: Measured on the location drawing at the dome circle drawn inside the left slingshot through the affine fit; not a table object.
- pinmame.output.solenoid 20: Measured on the location drawing at the dome circle drawn inside the right slingshot through the affine fit; not a table object.
- pinmame.output.solenoid 26: Measured on the location drawing at the dome circle drawn at the right of the upper playfield, beside the right loop through the affine fit; not a table object.
- pinmame.output.solenoid 27: Measured on the location drawing at the end of callout 27's leader in the popper mechanism at the rear left through the affine fit; not a table object.
- pinmame.output.solenoid 28: Measured on the location drawing at the end of callout 28's leader at the right end of the back panel through the affine fit; not a table object.

## Counts

- Placements: 162
- Validated input addresses: 40
- Observed-only input addresses: 1
- Validated output bindings: 80
- Observed-only output bindings: 11
- Output bindings with no coordinate: 2
- Inputs with a controlled `cabinet_or_service` record: 18
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 9
- Inputs with a controlled `unused` record: 9
- Inputs with a controlled `virtual` record: 2
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `internal_nonvisual` record: 4
- Outputs with a controlled `unused` record: 3
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Refused. `coverage.missing` is `["spatial_placement"]`: the flasher sockets are known only from the factory drawing's callouts, the playfield G.I. sockets only from one community table's light collections, and the Left Ramp Flasher and G.I. string 4 are not placed at all.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/extracted-vpxtool.manifest.json`, SHA-256 `4cd4fe13f56c9400a0bc7aef22ea70256af35bae8d8ec41937a23b459ef40809`, 3281 files, 729809766 bytes.
- Operations manual SHA-256 `5dfa8c788011a3e1177668eb0815ed081dbd2c96ca4859f3525bf040b9f01519`.
- Drawing fit `external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py` SHA-256 `ababe3e05cf3b95214360f232449f316694a0f2f97cd18234123d60bf6c0d9bb`, output SHA-256 `fb3babc5a6a9410751f7de83f0b9891b2ce241ffc740ba9151b247b15dade0a8`.
