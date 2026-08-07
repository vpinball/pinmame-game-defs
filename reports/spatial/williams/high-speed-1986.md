# High Speed (Williams, 1986) spatial review

Status: validated. The physical machine record itself remains `partial` at `machines/partial/williams/high-speed-1986.json` because of the three spatial gaps and two unresolved conflicts named below; see the promotion decision.

The matching source is the retained known-working `High Speed (Williams 1986).vpx` at SHA-256 `f57801a428f78f85b6cd40f4e47a74bd8e063227355d26ec4f15ef7f11d78af1`. The retained vpxtool extraction produced the embedded script at SHA-256 `149cab01a1fbe7657ffae87f72fa6982ed631653627b938186d5d8ed893195eb`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=1974`, and every canonical coordinate is x/952 and y/1974 rounded to at most six fractional places. The y bound of 1974 is much shorter than the 2115-2594 of the later machines curated in this project, which is what a mid-1980s playfield measures.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams instruction manual is the physical inventory, quantity, wiring and location authority; pinned PinMAME owns controller topology and the System 11 address-space rules; the retained table supplies geometry, but only where the manual's own numbered locations drawings agree with it.
- That last qualification matters on this machine. The retained table binds switch 34 to the rightmost jet bumper and switch 35 to the lowest, which is the opposite of both of the manual's own numbered locations drawings; the coordinates recorded here follow the manual, and the disagreement is disclosed on all three bumper switches.
- System 11 has no separate GI address space: general illumination is one ordinary solenoid address (11) whose per-game bulb-type metadata happens to be a continuous AC GI type, resolved from pinned PinMAME's own per-game MACHINE_INIT block. High Speed has one GI relay where Whirlwind has two.
- High Speed declares no A/C select relay (`sxx.muxSol = 0`) and no sound-overlay board (`hw.gameSpecific1 = 0`), so the platform's 25-32 alias bank and 37-44 overlay range are both enumerated as unpopulated rather than mapped to devices. This is the largest single difference from the project's other System 11 machine.
- Switches 9-12 (outhole and trough), 37/38 (flipper lane change) and 49/50 (slingshot scoring) have no object of their own in the retained table and are documented projections onto their own mechanism's retained object; switches 39 and 47 take their coordinates from two unbound triggers whose positions are corroborated by the manual's own upper-above-lower ordering in each hideout lane.
- Cabinet and backbox devices get controlled `not_applicable` records rather than coordinates: the eight cabinet switches, the four diagnostic buttons, the Country jumper, the police-light relay, the insert-board flashers, the knocker, the coin-lockout relay, the three backglass lamps and all six displays.
- The police beacon is backbox hardware. Both the Solenoid Table's Playfield/Cabinet column and the Solenoids/Flashers parts list say so explicitly, so it takes a controlled `not_applicable` record despite being the machine's signature device.

## Explicit projections

- Switch 9: Projected onto the Drain kicker (Kicker.Drain, table object centre): the outhole switch has no dedicated VPX object because the retained script's cvpmBallStack helper manages it abstractly (bsTrough.InitSw 9,12,11,10) and Drain_Hit is what feeds the stack. The manual's own switch-locations drawing puts switch 9 at the left end of the outhole/trough tube.
- Switch 10: Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre): the three trough positions have no individual VPX objects, the retained script managing all four trough switches through one cvpmBallStack against the single BallRelease exit kicker (bsTrough.InitKick BallRelease,90,10).
- Switch 11: Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre); see switch 10.
- Switch 12: Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre); see switch 10.
- Switch 37: Projected onto the left flipper's own assembly (Flipper.LeftFlipper, table object centre). The Lane Change switch is item 2b of the C-9952-R Flipper Base/Lane Change Assembly, mounted below the playfield as part of that assembly, and the manual's own switch-locations drawing places callout 37 at the left flipper. The retained script never drives this address: pinned PinMAME fabricates it from live flipper-button state in core_updateSw.
- Switch 38: Projected onto the right flipper's own assembly (Flipper.RightFlipper, table object centre); see switch 37, with callout 38 at the right flipper.
- Switch 39: Taken from the retained table's Trigger.sw39, an object with no _Hit handler anywhere in the script. It is used rather than discarded because three things agree: its name matches this address, it sits directly above Kicker.LKick which the script does bind to switch 40 (bsLeftLock.InitSaucer LKick,40), and the manual's own switch-locations drawing draws callout 39 above callout 40 in the same left ball chute.
- Switch 47: Taken from the retained table's Trigger.sw37, whose name is a misnomer -- switch 37 is the left flipper's Lane Change switch at the bottom of the playfield, and this object sits high on the right side. It is the exact mirror of Trigger.sw39: it lies directly above Kicker.RKick, which the script binds to switch 48 (bsRightLock.InitSaucer RKick,48), and the manual draws callout 47 above callout 48 in the right ball chute. The coordinate is therefore derived from the mirror geometry of the right hideout lane plus the manual's own ordering, not from the object's name.
- Switch 49: Kicker (slingshot) scoring switch, projected onto the centroid of its own slingshot wall's four drag points (Wall.LeftSlingShot), the assembly the switch is part of; the script's LeftSlingShot_Slingshot handler is what pulses this address.
- Switch 50: Kicker (slingshot) scoring switch, projected onto the centroid of Wall.RightSlingShot's four drag points; see switch 49.
- Solenoid 1: Projected onto the Drain kicker (Kicker.Drain, table object centre): the outhole kicker coil has no separate actuator object, the retained script routing it through bsTrough.SolIn.
- Solenoid 3: Projected onto the eject-hole saucer's own kicker object (Kicker.sw16, table object centre), the object the retained script initialises as the saucer (bsSaucer.InitSaucer sw16,16,96,5).
- Solenoid 5: Placed at the centre of the single elongated flasher lens the manual's own solenoid-locations drawing gives item 5, taken from Light.F105. The retained table models that lens with three lights: a co-located bulb/glow pair (F105/F105b) at the centre plus F105c and F105d offset about (43.5, -28.5) either side of it. Because the manual draws one lens with one leader line, this is one device location, not three.
- Solenoid 6: Placed at the centre of item 6's elongated lens (Light.F106); see solenoid 5 for the derivation.
- Solenoid 7: Projected onto the left hideout's own kicker object (Kicker.LKick, table object centre), the object the retained script binds to switch 40 and ejects with bsLeftLock.SolOut.
- Solenoid 8: Projected onto the right hideout's own kicker object (Kicker.RKick, table object centre); see solenoid 7.
- Solenoid 13: Projected onto the retained table's left ramp-gate object (Wall.Diverter1, four-drag-point centroid). The manual's Ramp Gate Assembly D-10884 parts list has one coil, one drive arm, one drive link and one gate (C-10888), and the assembly appears once in the Playfield Parts list, so there is one physical gate; the retained table splits it into two gate objects that its single Divert handler moves together, the second at normalized (0.666716, 0.017356). The left object is used as the anchor.
- Solenoid 14: Projected onto the left outlane kickback's own plunger object (Plunger.Plunger1, table object position), which the retained script's SolKickback handler fires.
- Solenoid 17: Projected onto the centroid of its own slingshot wall's four drag points (Wall.LeftSlingShot); the kicker coil and its scoring switch 49 are the same assembly.
- Solenoid 18: Projected onto the centroid of Wall.RightSlingShot's four drag points; see solenoid 17.
- Solenoid 22: Placed at the two Light members of the two Flupper flasher assemblies the retained script drives for this address (Light.Flasherlight5 and Light.Flasherlight6). Their dome base and lit primitives (Flasherbase5/6, Flasherlit5/6) are parked off-table at raw x about -2000, so only the lights carry usable coordinates; both sit along the top edge of the playfield, matching the manual's own item-22 callout to a slot along the top edge.

## Counts

- Placements: 122
- Located input addresses: 43
- Located output bindings: 75
- Outputs with an intentionally omitted spatial key: 4
- Inputs with a controlled `cabinet_or_service` record: 13
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 7
- Outputs with a controlled `virtual` record: 28

## Blockers

- Lamp addresses 42, 43 and 44 (Red/Yellow/Green Light (Ramp Stoplight)) are real bulbs in the playfield Traffic Light Assembly B-10921 but have no derivable coordinate: the retained table's Light objects for them are parked at raw x about -2237 and its stoplight primitives sit at position (0,0,0) with the geometry baked into a mesh whose derived centre is off the top of the playfield. Their spatial keys are omitted rather than invented.
- Lamp address 40 (Ramp Earns Hideout Jackpot) is marked a two-bulb circuit by the Lamp-Matrix Table but the manual never says where the second bulb is and the retained table models only one Light object, so its placement count is one against a quantity of two.
- Solenoid address 11 (General Illumination Relay) switches playfield, cabinet and backbox general illumination together per the Power Wiring Diagram, but no page of the manual enumerates a GI bulb count, bulb type or position. The retained table's 68-member playfield GI light collection is not adopted as a placement set: it is unverifiable against the manual, contains three jet-bumper cap lights that belong to those assemblies, duplicates one member, and includes one light above the top playfield edge. The spatial key is omitted.

## Promotion decision

Every controller address is enumerated and given a semantic disposition, every printed wiring detail is recorded, and the whole mechanism inventory is covered. Polarity is not a gap on this machine: `hsGameData`'s `wpc` struct is zero-initialised by its own `{{0}}` positional initializer so `wpc.invSw` is entirely unset and PinMAME normalizes no address, and the manual documents no opto and no normally-closed matrix switch anywhere -- no row of the Switches parts list carries an opto part number or is printed blank, and neither copy of the Switch-Matrix Table has an opto legend or a single shaded cell.

Promotion to `author_ready` is nonetheless refused. Three addresses have real bulbs with no derivable coordinate (lamps 42-44), one has a manual-stated bulb quantity its placement count cannot meet (lamp 40), one has no enumerable emitter set at all (solenoid 11), and the definition carries two unresolved `conflicts` entries. `coverage.missing` is therefore `["spatial_placement", "unresolved_conflicts"]` and the record stays `partial` until a second independent recreation or a photograph of an unrestored playfield places the Traffic Light Assembly and lamp 40's second bulb, a GI bulb inventory turns up, and the Section 3 flipper schematic settles which button feeds the upper-right flipper coil.

## Retained evidence

- Retained vpxtool extraction, 1712 files.
- Manual reading log with the verified page offset and the questions the manual does not answer, SHA-256 `7ec30ad943a45cf4407cc0ce6001c6dad1b6f5eaf28c7420f349cd531551aa98`.
- VPX script/geometry cross-reference, SHA-256 `58b98d92fc633c8b5ef2f02adda885d8195a2d63dc76cd018041a338fb7f2c0f`.
- Nine transcribed manual excerpts and three rendered crops under `evidence/excerpts/williams.high-speed.1986/`.
