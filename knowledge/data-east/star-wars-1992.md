# Star Wars (Data East, 1992)

Full semantic curation of the physical game, IPDB 2358, model 500-5524-01. The physical release is 1992; the catalog root's 2012 year belongs to anniversary firmware. Identity was checked against the retained archived IPDB page and factory manual independently of the VPX header.

## Controller and inputs

All eleven catalog drivers share Data East CPU revision 3, GEN_DEDMD32, DE2 sound and one 128×32 DMD. The definition enumerates 75 inputs: service -7/-6, matrix 1-64, flipper column 81-88 and CPU jumper DIP 0. The factory board calls it J8 at PIA 11B PA7, factory installed (DIP 0 = 0), not a bank of operator adjustments. The shared Williams W7/Germany/USA terminology is not declared by this Data East driver and is not assigned to this jumper. No extra/custom switch or lamp columns, custom coils, or printer line are enabled.

The factory matrix contacts are normally open. INITGAMES11 has no inversion mask; pia4a_r reads core_getSwCol directly. The ROM's Active Switch Test names used contacts at public 1. A ball resting on a trough or cam mark does not turn its contact into normally-closed construction. The cabinet flipper leaf switch closes its ground circuit; use host 84 left and 82 right. core_updateSw copies them to matrix 15/16 and synthesizes 47/48 and 45/46 while game-on 23 is enabled. No EOS or upper flipper feedback is modeled. Do not independently drive the matrix copies or invert public inputs again.

Black Advance -7 is a momentary step; Green -6 is maintained (0 forward/up, 1 reverse/down). The harness enters diagnostics by the ROM's exact displayed title, never by counting page presses. Its pulse helper reasserts a held input every 10ms; the diagnostic names seen during forced matrix 15/16 holds are therefore not proof that direct matrix writes survive core rewrites.

Factory-unused matrix 18 and 52 have ROM diagnostic names MIDDLE LOOP and SHIFT UP. The factory switch parts list and retained script establish no fitted device there, so they remain unused with the software names disclosed. Matrix 2 is fourth coin, not the generic platform's ball-roll tilt: this manual explicitly says the game has no ball-roll tilt. Unused positions 8/9/18/49/52-64 and flipper-column 81/83/85-88 are explicitly disposed.

## Outputs and display

All 128 output positions are enumerated: solenoids 1-64 and lamps 1-64. The independent ROM coil test confirms 17 top bumper, 18 left bumper, 19 right bumper, 20 bottom bumper, 21 left sling, 22 right sling. The Data East PIA permutation is derived for this initializer rather than borrowed from another game. Drivers 13/14 are test-pulsed as NOT USED and the factory drawing explicitly fits no load. Reserved, printer, upper-flipper, simulator and custom ranges are positively explained by the pinned core.

K1 relay 10 multiplexes A-side coils 1-8 and C-side flash banks 25-32; PinMAME already publishes their separated states. Solenoid 11 controls GI in reverse: 1 turns the lights off, 0 on. Lampz111 was a VPW-local helper, not a native lamp. The invalid native lamp 111 record is removed, and its VPE legacy lamp aliases now target the actual GI binding. The old duplicate semantic ID is retired; retained semantic IDs for real controller bindings are otherwise preserved. GI geometry remains an observed table grouping and does not prove the full factory bulb inventory.

The missing knocker (8), multiplexer (10), cabinet credit lamp (25), sphere lamps (29/30), service controls and full synthetic flipper range are present. Lamp 17 is physically Not Used despite the ROM's X MODE sweep label. The single-lamp test identifies all 64 addresses; activity alone never proves a populated load. The backbox has one controller-index-0 128×32 DMD; the sound-layout callback is not another physical display.

## Mechanisms and recreation

Install three balls, with the queue sensing contacts 11/12/13 occupied once settled and the separate outhole 10 clear. Factory recommended pitch is approximately 6.5 degrees. Preserve real occupancy and failed eject/reset states so the ROM can perform its own retry and ball-search handling. Do not start with diagnostic switches or tilt active. Mechanism descriptions below separate factory topology from retained VPW implementation and explicitly identify table-owned tuning.

### Outhole and Three-Ball Feed Trough

Outhole switch 10 detects a drained ball; coil 1 returns it to the feed trough. Three physical trough contacts 11/12/13 sense the queue; coil 2 ejects its leading ball toward shooter switch 14. Factory names left/center/right are distinct from VPW's virtual array (11,13,12,10). Initialize three balls; do not model switch 10 as a fourth trough contact. A failed eject must leave the actual occupied contact closed for the ROM's retry/search logic.

### Automatic Ball Launcher

A served ball closes shooter-lane 14; coil 3 launches it. Shifter fire button 50 is the player's launch/skill-shot control, not the lane occupancy switch. VPW uses cvpmImpulseP; its speed 65 and 0.5 tuning are table physics, not factory travel time.

### Cabinet Shifter and Fire Button

Hand-operated front-cabinet assembly 500-5620-00 contains the fire/button harness (50), the Shift Down microswitch (51), and a spring. The factory chart explicitly leaves 52 unfitted despite the ROM's SHIFT UP diagnostic label; do not invent another input. VPW's Plunger/LockBar key asserts both 50 and 51 and clears both on release, while Left/Right Magna-Save latch 51 off/on; neither writes 50. These keyboard conveniences do not change the two fitted physical contacts or prove a motorized lever, spring force or travel specification.

### Left Force Scoop

Ball occupancy holds the scoop contact closed until the corresponding eject coil releases the ball back onto the playfield. Keep occupancy during a failed eject. The two scoops have separate switches and coils; do not route them through the VUK counter.

### Right Sarlacc Scoop

Ball occupancy holds the scoop contact closed until the corresponding eject coil releases the ball back onto the playfield. Keep occupancy during a failed eject. The two scoops have separate switches and coils; do not route them through the VUK counter.

### Death Star / Obi-Wan Underchute and Left VUK

Death Star trough 34 and Obi-Wan trough 35 route balls beneath the playfield to the left VUK 36. Coil 5 lifts a waiting ball to the wire ramp. VPW AddVUK delays its virtual arrival 200ms, counts queued balls, and holds 36 until its queue empties. That counter is a recreation of the shared return, not extra physical switches or measured transit time. A jam leaves the corresponding real occupancy contact closed.

### Three-Bank Drop Target Reset

Hits drop individual top/middle/bottom targets and close 30/31/32; they stay down and active until coil 6 resets the bank. Reset opens all three after the targets rise. Preserve partially dropped banks and failed resets; fixed X-Wing targets 25-29 do not share this reset.

### Death Star Entrance Bar

Motor/relay 12 raises or lowers the entrance bar carrying hit target 40. End contacts 41 UP and 42 DOWN close just before their respective travel limits and must never be on together. VPW models reciprocal travel with vpmMechReverse, 72 steps and marks 0/71, disabling target 40 collision when lowered. These are software marks, not degrees or factory timing. Start with actual bar state and sensor feedback; do not fabricate a successful limit on a jam.

### Death Star and R2D2 Rotation Drive

Shared relay 15 drives two separate 28VAC motors: Death Star 515-5570-00 and R2D2 515-5571-00 (R2D2 unit 500-5484-00). No rotation index contact is listed. VPW uses a 360-step circular Death Star model and invokes UpdateR2Head, oscillating artwork between -80 and +60 degrees. These are visual phase/travel choices, not measured factory steps or travel. Turning off the relay stops drive, with table-owned coast tuning. One controller actuator is intentionally owned by this combined drive mechanism.

### R2D2 Raise / Dance

Coil 9 lifts the R2D2 body; releasing it returns the toy. Switch 38 is the entrance ball switch, not a toy-position sensor. VPW SolR2/UpdateR2 animates height separately from output 15's head rotation. Its height/speed constants are artwork tuning; there is no encoded physical position telemetry.

### Left Outlane Laser Kickback

When the ROM enables Laser Kick, a ball at left outlane 24 is returned by coil 16; otherwise it drains. VPW pulls back the kickback at initialization, fires on the output's rising state, and retracts on release. Lamp 56 is the lit feature indication, not an actuator.

### Top Turbo Bumper

Ball contact closes the scoring/trigger switch and the corresponding special coil kicks the ball away. The physical trigger circuit and ROM diagnostic share this coil; do not assume a host switch closure makes PinMAME synthesize a special output (ssSw is empty). Return the skirt/contact when the ball leaves.

### Left Turbo Bumper

Ball contact closes the scoring/trigger switch and the corresponding special coil kicks the ball away. The physical trigger circuit and ROM diagnostic share this coil; do not assume a host switch closure makes PinMAME synthesize a special output (ssSw is empty). Return the skirt/contact when the ball leaves.

### Right Turbo Bumper

Ball contact closes the scoring/trigger switch and the corresponding special coil kicks the ball away. The physical trigger circuit and ROM diagnostic share this coil; do not assume a host switch closure makes PinMAME synthesize a special output (ssSw is empty). Return the skirt/contact when the ball leaves.

### Bottom Turbo Bumper

Ball contact closes the scoring/trigger switch and the corresponding special coil kicks the ball away. The physical trigger circuit and ROM diagnostic share this coil; do not assume a host switch closure makes PinMAME synthesize a special output (ssSw is empty). Return the skirt/contact when the ball leaves.

### Left Slingshot

Rubber deflection closes the sling switch and the physical special-solenoid circuit kicks the ball. ROM diagnostics publish the named output; ssSw is empty, so a recreation must not rely on PinMAME deriving a kick from a host switch pulse alone.

### Right Slingshot

Rubber deflection closes the sling switch and the physical special-solenoid circuit kicks the ball. ROM diagnostics publish the named output; ssSw is empty, so a recreation must not rely on PinMAME deriving a kick from a host switch pulse alone.

### Left Flipper

Cabinet button drives the solid-state flipper hardware while game-on output 23 enables it. PinMAME supplies identical synthetic power/hold states for this non-CPU-controlled initializer; they do not measure winding duty or EOS. Drive host button 84 left / 82 right and release to return the bat. Physical coil 090-5032-00 (22-1080); table physics determines stroke/return.

### Right Flipper

Cabinet button drives the solid-state flipper hardware while game-on output 23 enables it. PinMAME supplies identical synthetic power/hold states for this non-CPU-controlled initializer; they do not measure winding duty or EOS. Drive host button 84 left / 82 right and release to return the bat. Physical coil 090-5032-00 (22-1080); table physics determines stroke/return.

### Cabinet Knocker

Momentary coil 8 strikes the cabinet knocker. It has no scoring/position switch; release returns the striker. The retained table defines a sound routine without assigning SolCallback(8), an omitted recreation callback rather than evidence of absent factory hardware.

## Evidence and reproducibility

Factory authority: the complete switch-parts and lamp-location tables, all eight flash-bank annotations, cabinet/shifter parts, auxiliary/flipper coils, major assemblies, contact construction and motor-relay diagrams are committed under evidence/excerpts/data-east.star-wars.1992. Native renders and OCR remain beside the hashed original PDFs in the external manuals root. The operator scan and separate schematics are related factory material, not independent confirmations.

Runtime authority: retained VPW v1.2.2 (table ea240a0193d6…, script 1d5252b9ef7d…) and the exact stwr_103 CPU 1.03 / display 1.05 diagnostic runs. tools/star_wars_pinmame.json pins the initializer, complete ROM chip manifests and source hashes at PinMAME 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. The native DLL is dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead; its source snapshot was verified against all source/build files at that commit before running. No ROM bytes, manuals or table files are redistributed.

The compact runtime derivative pins every raw trace and DMD snapshot; build_star_wars_runtime.py recomputes it from the retained runs. The normal curator uses an immutable baseline plus committed source/excerpt/runtime seeds and is independent of external roots. Its --check mode refuses byte drift. Runtime names are software observations; table coordinates and the factory physical construction have separate authority.

## Remaining requirements

Coverage remains partial with three explicit missing requirements, for an 81% completion score:

- **variant_differences**: all eleven ROM manifests and logical controller/display differences are inventoried, but real-board socket compatibility of one- versus two-chip DMD sets and the anniversary revisions is not established by the emulator initializer. Obtain game-board/EPROM fitting instructions or a verified physical upgrade report before assigning physical_compatibility; all variants remain unknown.
- **spatial_placement**: every published coordinate remains observed, not independently validated. Flash banks 5R/7R/8R and sphere lamps 29/30 lack defensible individual socket positions. Trough, cam sensors and coil effects use disclosed assembly projections; the GI table grouping is incomplete as a physical socket inventory. Output 15's Death Star anchor does not locate its second, R2D2 motor.
- **unresolved_conflicts**: factory flash-bank annotations disagree on 4R/6R totals and 8R playfield versus insert-panel placement. The operator sheet's 6R total also differs from the separate schematic. ROM strings cannot settle fitted socket counts. Resolution requires photographs of populated banks and their harnesses or a later factory correction.

This is not author-ready and no requirement is cleared merely because a controller address toggled.
