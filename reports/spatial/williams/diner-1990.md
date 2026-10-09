# Diner (Williams, 1990) spatial review

Status: validated. The machine record stays `partial` at `machines/partial/williams/diner-1990.json`; its spatial dimension stays open because of the 5 spatial blockers below.

The geometry source is the retained known-working `Diner VPX 1.2.vpx` by Flupper, SHA-256 `f59be95f63e485415b36ff4a46ce07c3b4060d20f512dbe3e36a64b0bbde69b1`, whose embedded script (SHA-256 `df18744ca1550d20c2eba5e940b8723dd0fc0498d98f6a252d417bd5429e6162`) is the binding authority. Bounds are `left=0 top=0 right=1000 bottom=2000`; every coordinate is x/1000 and y/2000, rounded to at most six places.

## Evidence decisions

- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker, bumper, spinner or primitive for a switch, the `LightN` insert light of each lamp, the modelled flasher dome or script-driven Light for a flasher, and each G.I. bulb light.
- 79 of the 90 table placements the manual's numbered drawings check land within 0.07 normalized of their own callout under both fits (rule below) and are validated; the others keep the table's `observed` status.
- Sensors and coils with no table object of their own (the ramp, trough and sub-playfield switches, and the outhole, ramp, drop-reset, sub-playfield, diverter and feeder drives) are documented projections onto their own mechanism's object and are not checked against the drawings.
- Baked-mesh primitives (the cash-register windows and the E-A-T sign circles) are placed at the centre of their world-space mesh from `vpxtool export obj --units vpu`.
- Backbox and cabinet devices take controlled `not_applicable` records: the clock lamps 49-60, the clock flashers (31), the clock stepper (15, 16) and its opto (59), the knocker, the A/C relay and its contact, the cabinet, flipper-opto and diagnostic switches, the Country jumper and both displays.

## Callout check

Rule: A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it.

- pdf-77 (Diner manual PDF 77, printed DINER 73: Solenoids/Flashers locations drawing): 5 controls, control RMS 0.0026, control leave-one-out max 0.0066; 17 callout pairs, 17 in the callout fit, leave-one-out max 0.063.
- pdf-78 (Diner manual PDF 78, printed DINER 74: Switches locations drawing): 5 controls, control RMS 0.0042, control leave-one-out max 0.0226; 28 callout pairs, 26 in the callout fit, leave-one-out max 0.0581.
- pdf-81 (Diner manual PDF 81, printed DINER 77: Lamps locations drawing): 5 controls, control RMS 0.0028, control leave-one-out max 0.007; 45 callout pairs, 45 in the callout fit, leave-one-out max 0.0619.

Checked 90, validated 79.

Not validated by the check:

- `device.cup-flashers.emitter`: page pdf-77, label 6C, control_offset 0.1056, callout_offset 0.0619
- `device.left-jet-bumper.effect`: page pdf-77, label 17, control_offset 0.0714, callout_offset 0.0391
- `device.right-jet-bumper.effect`: page pdf-77, label 19, control_offset 0.0834, callout_offset 0.063
- `device.upper-left-eject.effect`: page pdf-77, label 5A, control_offset 0.0763, callout_offset 0.0268
- `lamp.matrix-12.emitter`: page pdf-81, label 12, control_offset 0.0791, callout_offset 0.0619
- `switch.matrix-17.sensor`: page pdf-78, label 17, control_offset 0.2113, callout_offset 0.1728
- `switch.matrix-27.sensor`: page pdf-78, label 27, control_offset 0.0689, callout_offset 0.0981
- `switch.matrix-28.sensor`: page pdf-78, label 28, control_offset 0.0716, callout_offset 0.0581
- `switch.matrix-29.sensor`: page pdf-78, label 29, control_offset 0.0787, callout_offset 0.0384
- `switch.matrix-36.sensor`: page pdf-78, label 36, control_offset 0.0726, callout_offset 0.0387
- `switch.matrix-49.sensor`: page pdf-78, label 49, control_offset 0.0867, callout_offset 0.05

## Explicit projections

- Switch 10: Projected onto the table's lock (Cash Register) ramp (Primitive lockramp, object position), the moving part of the B-11304-2 Ramp Elevator Assembly whose switch this is (5647-12001-00). The retained script has no switch object: it writes this address from SolRampUp/SolRampDown and its lockramptimer when the ramp reaches either end of travel (script lines 662-686).
- Switch 11: Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the trough as one three-ball cvpmTrough (bsTrough.initSwitches Array(11,12,13) with Initexit BallRelease, script lines 462-471) and has no object per trough position. The switch drawing places 11 at the right end of the trough, under the shooter lane.
- Switch 12: Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11. The switch drawing places 12 left of 11 along the same trough.
- Switch 13: Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11. The switch drawing places 13 left of 12, next to the outhole (9).
- Switch 15: Projected onto the table's sub-playfield popper (Kicker SubWaypopper, object centre), where the script's two-ball cvpmTrough bsSubWay holds the balls this switch counts (initSwitches Array(15,16), Initexit SubWaypopper, script lines 505-515); the switch sits in the B-13652 Sub-Playfield Shooter below the playfield and has no object of its own.
- Switch 16: Projected onto the table's sub-playfield popper (Kicker SubWaypopper); see switch 15.
- Solenoid 1: Projected onto the drain kicker the script's cvpmTrough receives balls on; the outhole kicker coil has no object of its own.
- Solenoid 2: Projected onto the lock ramp, the moving part the B-11304-2 Ramp Elevator's SM-1-26-600 armature coil lowers.
- Solenoid 3: Projected onto the bank's middle drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 4: Projected onto the lock ramp, which the B-11304-2 Ramp Elevator's AE-23-800 coil and lift crank raise.
- Solenoid 6: Projected onto the popper the script fires the sub-playfield ball from; the B-13652 shooter coil has no object of its own.
- Solenoid 13: Projected onto the bank's middle drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 14: Projected onto the diverter's pivot; the B-13346 Ramp Diverter coil sits under the right ramp and has no object of its own.
- Solenoid 22: Projected onto the ball-release kicker the script kicks from; the C-9638 feeder coil has no object of its own.

## Counts

- Placements: 143 (observed 50, validated 93)
- Located input addresses: 35
- Located output bindings: 76
- Outputs with an omitted spatial key: 1
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 24
- Outputs with a controlled `cabinet_or_service` record: 16
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `virtual` record: 20

## Blockers

- Solenoid 10 (Backbox and Playfield G.I. Relay): the 28 placements are the bulb lights of the retained table's lightsGI collection. The manual prints no G.I. bulb count or layout and a table's grouping is not the machine's wiring, so they stay observed without a quantity.
- Solenoid 32 (DINE-TIME Flashers): the solenoid drawing marks its one playfield bulb (callout 8C) beside the right ramp, but the retained table has no object for it, so its spatial key is omitted.
- Solenoid 30 (Cup Flashers): the manual prints four playfield bulbs and the drawing two pairs of leaders (at the cup and on the right side), but the table models only the cup's light, so the one placement stays observed.
- Eleven checked table placements land beyond the 0.07 callout limit and stay observed: the cup flasher, the left and right jet bumpers, the upper left eject, lamp 12 and switches 17, 27, 28, 29, 36 and 49 (see the callout check). Most sit at the top of the playfield, above the drawings' bumper and flipper controls.
- Lamps 1-5 and 25-29: the cash register's windows and the jukebox decals are the parts the bulbs light, not modelled sockets (the five jukebox lamps share one point), so these placements stay observed.

## Promotion decision

Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is refused: the G.I. placements come only from the table's grouping, the DINE-TIME playfield flasher has no placement, three cup flashers have no table object, and the PA-0 prototype driver's hardware is unknown, so `coverage.missing` is `["variant_differences", "spatial_placement"]`. A G.I. lamp layout from the machine, a photograph or measurement of the DINE-TIME and cup flasher sockets, and the prototype's ROM (whose service tests name every address it drives) would close them.
