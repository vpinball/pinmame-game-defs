# Black Hole (Gottlieb, 1981) spatial review

Status: observed. The machine record stays `partial` at `machines/partial/gottlieb/black-hole-1981.json`; its spatial dimension stays open because of the blockers below.

The geometry source is the retained `Black Hole (Gottlieb 1981) vpx 1.1.vpx` by cyberpez, SHA-256 `23db54a8c2f3feed3e299c7c64e1cb43a516fd6bba0f55a016dc48c38ce36d3a`, whose embedded script (SHA-256 `9ecdc9f67b2623360335c5ce1e7601ae792a923a6898fe9c60fd11a398530b99`) is the binding authority. Bounds are `left=0 top=0 right=1116 bottom=2186`; every coordinate is x/1116 and y/2186, rounded to at most six places.

## Evidence decisions

- A switch placement is the centre of the table object the script binds to the address: a trigger, hit target, kicker, bumper, spinner or the drag-point centroid of a target or rubber wall. A shared address (06 pop bumpers, 34 and 72 ten-point switches, 71 lower bumpers) gets one placement per object the drawing confirms.
- A lamp placement is the script-bound insert light: the upper playfield's Light objects and the lower playfield's insert Flasher objects, which this table uses as the inserts themselves. Lamps 19 and 20 have three bulbs each, as the drawing prints them.
- Coils on lamp drivers (8, 12-15, 18) sit at the kicker, hole or diverter object the script fires; the bank reset coils are projected under their banks (below).
- Relays, the coin lockout, the coin counters, the knocker, the Sound 16 line, the light box lamps, cabinet and service switches, the DIPs and the four player displays take controlled `not_applicable` records. The two status-display pairs and the lower playfield display are on the playfield and placed on the table's display walls.

## Explicit projections

- Solenoid 1: Midpoint of the H-O-L-E bank's two middle targets (TargetO, TargetL2): the reset coil sits under the bank.
- Solenoid 2: The B-L-A-C-K bank's middle target (TargetA): the reset coil sits under the bank.
- Solenoid 5: Midpoint of the yellow bank's two middle targets (TargetLL50, TargetLL60).
- Solenoid 6: The white bank's middle target (TargetLR51).
- Solenoid 9: The table's drain kicker below the flippers, where the outhole kicker sits.
- Lamp 8: The table's sw53 kicker, where the ball waits at the lower ball gate.
- Lamp 15: The table's trough exit kicker (kicker1), which its ReleaseBall kicks.
- Lamp 18: The table's Flipper1 diverter at the re-entry tube's exit.

## Counts

- Placements: 103 (observed 103)
- Located input addresses: 40
- Located output bindings: 49
- Devices without a spatial record: 4
- Inputs with a controlled `cabinet_or_service` record: 9
- Inputs with a controlled `dip_switch` record: 42
- Inputs with a controlled `unused` record: 27
- Outputs with a controlled `cabinet_or_service` record: 7
- Outputs with a controlled `internal_nonvisual` record: 5
- Outputs with a controlled `unused` record: 3
- Outputs with a controlled `virtual` record: 16

## Blockers

- Every placement comes from one community table (cyberpez's vpx 1.1) and keeps its observed status: the table's objects were matched to the manual's location drawings (printed pages 40 and 42) by side, order and neighbourhood, not by a registered fit with a leave-one-out check, and no second factory-layout table is retained.
- The lower playfield's devices are placed where the table draws them, under the window in the shared plan; the manual's lower playfield drawing has its own frame and has not been registered onto the table.
- Switch 26 (the playboard tilt) has no table object and keeps no spatial record; the drawing prints SW26 at the lower left above the apron.
- Switch 34's table also binds the right kicking rubber (Sling2), where the drawing prints no SW34; it is left unplaced.

## Promotion decision

Promotion is refused. Besides the spatial blockers, the cabinet wiring sheet (printed page 47) is cropped in both retained manual copies, so the fitment of return-7 positions 57, 67 and 77 stays unknown (`input_semantics`). A complete scan of the manual's fold-out sheets, and a registered fit of the two location drawings onto the table, would close both.
