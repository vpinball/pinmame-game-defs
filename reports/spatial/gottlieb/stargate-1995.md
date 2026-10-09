# Stargate (Gottlieb, 1995) spatial review

Status: observed. The machine record stays `partial` at `machines/partial/gottlieb/stargate-1995.json`; its spatial dimension stays open because of the 4 spatial blockers below.

The geometry source is the retained known-working `Stargate (Gottlieb 1995) v2.0.vpx` by VPin Workshop, SHA-256 `581ffc6fc4f5f1cb2b835d8e341272215ce41f4c5e25064cdfc30fe61848904b`, whose embedded script (SHA-256 `eda1f035a56672f83411efe228ff98291a2bdaf9b85114d1da7dc4ab337974a1`) is the binding authority. Bounds are `left=0 top=0 right=952.941 bottom=2164.706`; every coordinate is x/952.941 and y/2164.706, rounded to at most six places.

## Evidence decisions

- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker or bumper for a switch, the `L<n>` bulb light `vpmMapLights` binds to each lamp and auxiliary flasher, the object a coil moves or kicks from, and each G.I. bulb light of the `GI` collection.
- Baked-mesh primitives (the drop targets, the Horus guardians, the pyramid top, the glider and the auto-plunger arm) are placed at the centre of their world-space mesh from `vpxtool export obj --units vpu`. Control: `BM_KT_sw14` lies within 1.4 units of `HitTarget sw14`'s stored position.
- Sensors and coils with no table object of their own are documented projections onto their own mechanism's object.
- Backbox and cabinet devices take controlled `not_applicable` records: the nine lightbox lamps and the two lightbox flashers (126, 127), the credit-button lamp, the rope lights, the lightbox and game-over relays, the knocker, the coin meter, the cabinet and flipper-button switches, the test inputs and the DMD.
- No placement is validated: no factory drawing is retained to check it, and the two retained tables share ancestry.

## Explicit projections

- Switch 20: Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the switch senses the Glidercraft's left-right drive and has no table object; the retained script never writes it.
- Switch 21: Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the script writes it from its GliderTimer when the glider is retracted (lines 1406-1410) and has no object for the switch.
- Switch 30: Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the script writes it from its GliderTimer at the right end of the swing (lines 1412-1416) and has no object for the switch.
- Switch 101: Projected onto the lower left ball gate (Flipper Flipper1, object centre), the moving part whose position the script reports here from SolDiv (lines 782-792); the sensor has no object of its own.
- Switch 102: Projected onto the pyramid top (Primitive BM_Pyramid1, world mesh centre), whose open state the script reports here from SolPyramid (line 1339); the sensor has no object of its own.
- Solenoid 5: Projected onto the kicking target it drives; the coil sits behind it and has no object of its own.
- Solenoid 6: Projected onto the kicking target it drives; the coil sits behind it and has no object of its own.
- Solenoid 7: Projected onto the kicking target it drives; the coil sits behind it and has no object of its own.
- Solenoid 8: Projected onto the kicker hole the script ejects from; the coil has no object of its own.
- Solenoid 10: Projected onto the upkicker the script lifts the ball from; the coil has no object of its own.
- Solenoid 11: Projected onto the upkicker the script lifts the ball from; the coil has no object of its own.
- Solenoid 12: Projected onto the upkicker the script lifts the ball from; the coil has no object of its own.
- Solenoid 13: Projected onto the ball gate it swings; the coil has no object of its own.
- Solenoid 14: Projected onto the left Horus guardian it raises; the coil sits below the playfield and has no object of its own.
- Solenoid 15: Projected onto the right Horus guardian it raises; the coil sits below the playfield and has no object of its own.
- Solenoid 16: Projected onto the pyramid top it opens; the drive has no object of its own.
- Solenoid 17: Projected onto the bank's middle drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 18: Projected onto the bank's first drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 19: Projected onto the single drop target it raises; the coil has no object of its own.
- Solenoid 20: Projected onto the single drop target it knocks down; the coil has no object of its own.
- Solenoid 23: Projected onto the glider it swings; the motor has no object of its own.
- Solenoid 24: Projected onto the glider it moves out and back; the motor has no object of its own.
- Solenoid 28: Projected onto the trough kicker the script releases balls from; the coil has no object of its own.
- Solenoid 29: Projected onto the outhole kicker the script receives drained balls on; the coil has no object of its own.

## Counts

- Placements: 135 (observed 135)
- Located input addresses: 38
- Located output bindings: 82
- Outputs with an omitted spatial key: 0
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `unused` record: 55
- Inputs with a controlled `virtual` record: 1
- Outputs with a controlled `cabinet_or_service` record: 17
- Outputs with a controlled `unused` record: 37
- Outputs with a controlled `virtual` record: 4

## Blockers

- No factory drawing is retained: IPDB lists the operations manual without hosting it, and no other attributable copy was found, so no placement can be checked against the machine's own switch, lamp or coil location drawings.
- The two retained tables are not independent: the VPW v2.0 table credits the 32Assassin and JLouLoulou v1.3.0 release as the table it rebuilt, so their agreement could only supplement a placement, never validate it. Every placement here comes from the VPW table and stays observed.
- Solenoid 31 (Tilt Relay, playfield G.I.): the 16 placements are the bulb lights of the VPW table's GI collection; a table's grouping is not the machine's wiring and the bulb count is unknown, so they stay observed without a quantity.
- Glider switches 20, 21 and 30, ball gate sensor 101 and pyramid sensor 102 have no table object of their own and are projected onto the glider, the ball gate and the pyramid top.

## Promotion decision

Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the mechanisms are covered, polarity is settled by the read path with the ROM's or the known-working script's active level for every switch except GLIDER LEFT (MOTOR) (20), and all six drivers name every address alike. Promotion to `author_ready` is refused because every playfield placement rests on one community table's geometry with nothing independent to check it and switch 20's active level is unknown, so `coverage.missing` is `["polarity", "spatial_placement"]`. The Stargate operations manual's switch, lamp and coil location drawings, or a second table built independently from the machine, would close the spatial gap.
