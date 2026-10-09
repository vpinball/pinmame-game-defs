# Pin-Bot (Williams, 1986) spatial review

Status: validated. The machine record stays `partial` at `machines/partial/williams/pinbot-1986.json` because of the 3 spatial blockers below.

The geometry source is the retained known-working `PinBot (Williams 1986).vpx` by bord (v1.1), SHA-256 `5d0f4c4c0908065a7550864e290bff6ed0afcecf1bce5ba46553bb74903f9e56`, whose embedded script (SHA-256 `164eb3b24ae1be991ad2646d2b80292453712eb6f76658f06d9f936e35a23776`) is the binding authority. Bounds are `left=0 top=0 right=952 bottom=1974`; every coordinate is x/952 and y/1974, rounded to at most six places.

## Evidence decisions

- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker or bumper for a switch, the `lN` insert light of each lamp's FadeLights triple, the modelled flasher dome or script-driven Light for a flasher, and the bulb-mesh `LightN` of each GI socket pair.
- 98 of the 99 table placements the manual's numbered drawings check land within 0.07 normalized of their own callout under both fits (rule below) and are validated; the others keep the table's `observed` status.
- Sensors and coils with no table object of their own (the lane-change, outhole, trough, ramp-down and visor limit switches, and the outhole, trough-feeder, drop-reset, ramp and visor drives) are documented projections onto their own mechanism's object and are not checked against the drawings.
- Flashers have no factory drawing; their placements are the table's modelled domes or lights, bound by the script and matching the manual's location wording. Playfield G.I. sockets come from the table's GI collection and stay `observed`.
- Backbox and cabinet devices take controlled `not_applicable` records: lamps 1-8, the robot-face, insert-board and top backbox flashers, the backbox G.I. relay, the knocker, the cabinet and diagnostic switches, the Country jumper and all eight display positions.

## Callout check

Rule: A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it.

- pdf-56 (Pin-Bot manual PDF 56, printed PIN-BOT 50: Solenoids/Flashers locations drawing): 5 controls, control RMS 0.0009, control leave-one-out max 0.0038; 8 callout pairs, 8 in the callout fit, leave-one-out max 0.0235.
- pdf-57 (Pin-Bot manual PDF 57, printed PIN-BOT 51: Lamps locations drawing): 5 controls, control RMS 0.0009, control leave-one-out max 0.0048; 55 callout pairs, 55 in the callout fit, leave-one-out max 0.0031.
- pdf-58 (Pin-Bot manual PDF 58, printed PIN-BOT 52: Switches locations drawing): 5 controls, control RMS 0.0014, control leave-one-out max 0.0063; 36 callout pairs, 36 in the callout fit, leave-one-out max 0.0652.

Checked 99, validated 98.

Not validated by the check:

- `switch.matrix-40.sensor`: page pdf-58, label 40, control_offset 0.075, callout_offset 0.0652

## Explicit projections

- Switch 10: Projected onto the left flipper's own assembly (Flipper LeftFlipper, object centre). The Lane Change switch is item 2b (SW-1A-150) of the C-9954 Flipper Base/Lane Change Assembly below the playfield, and the switch drawing (printed page 52) ends leader 10 on a dashed switch outline beside the left flipper's pivot. The retained script never drives this address; core_updateSw copies public 84 into it.
- Switch 11: Projected onto the right flipper's own assembly (Flipper RightFlipper, object centre); see switch 10.
- Switch 16: Projected onto the table's drain kicker (Kicker Drain, object centre), where its cvpmBallStack receives a drained ball (bsTrough.InitSw 16,17,18). The switch drawing ends leader 16 at the lower-left end of the outhole tube, 0.04 normalized from that kicker.
- Switch 17: Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the two-ball trough as one cvpmBallStack (bsTrough.InitSw 16,17,18 with bsTrough.InitKick BallRelease) and has no object per trough position. The switch drawing ends leader 17 at the shooter end of the trough tube.
- Switch 18: Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 17. The switch drawing ends leader 18 further down the same trough tube, where the second ball waits behind the first.
- Switch 44: Projected onto the table's ramp-lift lever (Primitive lramplever_prim, object position), the ramp lifting mechanism's own moving part. The Ramp Down switch is the B-11304 Ramp Lifting Mechanism's microswitch (5647-12001-00, item 14) below the playfield; the retained script writes this address from its RampTimer when the ramp reaches its lowered position and has no switch object. The switch drawing's leader 44 runs to the lifting mechanism beside the ramp lever, about 0.02 normalized from this point.
- Switch 46: Projected onto the visor (Primitive visorflat_prim, object position): Visor Closed is one of the two 5647-10529-00 limit switches on the visor motor's cam (Visor Motor Assembly B-11169, item 7) below the playfield, and the retained script models it as position 0 of its cvpmMech visor (mVisor.AddSw 46,0,0). The switch drawing draws only a dashed leader line towards the visor box for 46 and 47.
- Switch 47: Projected onto the visor (Primitive visorflat_prim, object position), the other cam limit switch; the retained script places it at the end of the visor's travel (mVisor.AddSw 47,58,58). See switch 46.
- Solenoid 1: Projected onto the drain kicker the trough's cvpmBallStack receives balls on; the outhole kicker coil has no object of its own.
- Solenoid 2: Projected onto the ball-release kicker the script kicks from; the trough feeder coil has no object of its own.
- Solenoid 4: Projected onto the bank's middle drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 5: Projected onto the ramp-lift lever, the moving part the B-11304 mechanism's raise coil drives.
- Solenoid 6: Projected onto the ramp-lift lever; the lowering coil (SM-26-600-DC, item 22) acts on the same mechanism.
- Solenoid 13: Projected onto the visor the motor moves; the relay and motor sit below the playfield and have no object of their own.

## Counts

- Placements: 148 (observed 28, validated 120)
- Located input addresses: 44
- Located output bindings: 75
- Outputs with an omitted spatial key: 2
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `unused` record: 17
- Outputs with a controlled `cabinet_or_service` record: 15
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 20

## Blockers

- Solenoids 10 and 18 (Right and Left Visor G.I.) are #1251 flash lamps that light the visor, but neither the manual nor the retained table gives their sockets a position: the locations drawings mark no visor lamp, and the table lights one Flasher sprite between the eyes for both. Their spatial keys are omitted.
- Switch 40 (Enter Ramp): the retained table's trigger sits about 0.075 normalized from where the switch drawing's leader 40 ends further down the same ramp curve, beyond the 0.07 callout limit, so its placement stays observed.
- Solenoid 12 (Playfield G.I. Relay): the 27 placements are the sockets of the retained table's GI collection. The manual prints no G.I. bulb count or layout and a table's grouping is not the machine's wiring, so they stay observed without a quantity.

## Promotion decision

Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is refused because two visor G.I. outputs have no placement, the playfield G.I. placements come only from the table's grouping and one switch placement is not validated, so `coverage.missing` is `["spatial_placement"]`. A photograph or drawing of the visor lamp sockets, a G.I. lamp layout from the machine, and a second, independent recreation or measurement of the ramp-entrance switch would close them.
