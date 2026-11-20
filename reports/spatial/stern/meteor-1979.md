# Meteor (Stern, 1979) spatial review

Status: incomplete. No playfield lamp is placed, every placement is `observed` or `conflicted`, so the machine record stays `partial` at `machines/partial/stern/meteor-1979.json`.

The geometry source is the retained `Meteor (Stern 1979).vpx` (bord, 1.0, December 2020) at SHA-256 `0f8c826c3e9565835189b79d599a1dd72aa5dd20e1347d6fab8477fa1ff65614`; its embedded script (SHA-256 `b5a7109e18348aabe6aaa1b16f539110ba3df33deaef99eae1a84f7bfb23098a`) is the pinned corpus script with whitespace differences. Exact playfield bounds are left 0, top 0, right 952.9412, bottom 1976.4706, and every canonical coordinate is x/952.9412 and y/1976.4706 rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.

## Evidence decisions

- The script's bindings choose each switch's and coil's object. A switch sits on its trigger, target wall, bumper, stand-up target or spinner; a coil sits on the object it moves, or at the mean of the targets a reset coil raises.
- The world-space mesh source is the vpxtool git:v0.33.3 `export obj --units vpu` export of the retained table, `stern/meteor-1979/world-obj/Meteor (Stern 1979).obj` under the VPX sources root (SHA-256 `d971105c3b755f73d08ec18dea5ad007cae2b8bd45804538cd749dcc8af24bc5`, 31095858 bytes, outside Git), whose x and y are playfield VPX units.
- The two passive scoring bumpers are baked-mesh primitives at the origin, invisible collidables that the export leaves out. Each is placed on the world-space bounding-box centre of its mesh in the same export of a visibility-only derivative, `stern/meteor-1979/bumpers-visible/Meteor (Stern 1979) bumpers visible.vpx` (SHA-256 `08409a84fcac343ff26117e32f785644d7c2975f535f26be8eed37e3e10ac718`, outside Git): the retained extraction with `is_visible` set to true in `Primitive.bumper2.json` and `Primitive.bumper3.json` and nothing else changed, assembled with vpxtool. Its re-extraction differs from the retained extraction only in those two files, and its export, `stern/meteor-1979/bumpers-visible/world-obj/Meteor (Stern 1979) bumpers visible.obj` (SHA-256 `8080122eda9a0258560a94383fd7d96f3de068b2550a44a2dd647410e7ad3d53`, 31136534 bytes), adds only those two objects to the table's, every other object's vertices unchanged. The exported centres equal the primitive's position plus each local vertex times its size (185.274, no rotation) within 0.0001 VPX units, and fall within 1.3 VPX units of each bumper's own light.
- Lamps are not placed. The table's 302 lights are all bulb-mode, but none shows a bulb mesh, and docs/SPATIAL.md requires a real bulb for a socket.
- General illumination is placed on the export's world-space bounding-box centres of the 17 connected pieces of the baked `layer1bulbs` mesh, each with a `Light<n>` general-illumination light within 3.6 VPX units of its centre. The playfield sheet draws one `GEN. ILLUM` string (feed A2J1-8, return A2J1-1) as a single lamp symbol, so no machine source gives the sockets' positions or count, and the placements stay `observed`.
- The playfield sheet labels each three-bank's matrix cells top, lower and middle; the table binds them top, middle and lower. The placements follow the sheet and are `conflicted` until the record's conflict is settled.

## Explicit projections

- pinmame.input.switch 12: Placed on the world-space centre of the table's collidable dead-bumper mesh `bumper2` (its `Bumper2_Hit` pulses 12), taken from the export of the visibility-only derivative that makes it visible; it coincides within 0.4 VPX units with the bumper's light `L29A`.
- pinmame.input.switch 13: Placed on the world-space centre of the table's collidable dead-bumper mesh `bumper3` (its `Bumper3_Hit` pulses 13), taken from the export of the visibility-only derivative that makes it visible; it coincides within 1.3 VPX units with the bumper's light `L27A`.
- pinmame.input.switch 15: Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own slingshot event.
- pinmame.input.switch 16: Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own slingshot event.
- pinmame.output.solenoid 1: Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 3: Projected onto the top left three-bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object.
- pinmame.output.solenoid 4: Placed on the METEOR target it knocks down (table `sw32`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 5: Placed on the METEOR target it knocks down (table `sw31`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 7: Projected onto the lower left three-bank it resets: the mean of the table's own three target objects.
- pinmame.output.solenoid 8: Placed on the METEOR target it knocks down (table `sw30`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 9: Projected onto the right three-bank it resets: the mean of the table's own three target objects.
- pinmame.output.solenoid 10: Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 11: Placed on the METEOR target it knocks down (table `sw29`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 12: Placed on the METEOR target it knocks down (table `sw28`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 13: Projected onto the METEOR bank it resets: the mean of the table's own six target objects.
- pinmame.output.solenoid 14: Placed on the METEOR target it knocks down (table `sw27`); the coil sits behind the target and has no object.
- physical.input.direct 1: Placed on the left flipper pivot: the end-of-stroke contact is mounted on its flipper assembly.
- physical.input.direct 2: Placed on the right flipper pivots: each end-of-stroke contact is mounted on its flipper assembly.

## Counts

- Placements: 65 (6 conflicted, 59 observed) on 47 records
- Records with a controlled `cabinet_or_service` record: 22
- Records with a controlled `dip_switch` record: 32
- Records with a controlled `internal_nonvisual` record: 1
- Records with a controlled `unused` record: 8
- Records with a controlled `virtual` record: 3
- Records with no spatial key: 59

## Excluded table objects

- L<n>, L<n>a and L<n>A lights: insert lights the scripts bind to lamp numbers; none of the table's 302 lights shows a bulb mesh, so none marks a socket
- Light<n> lights: the general-illumination glows, placed through the `layer1bulbs` mesh piece each sits on, not on their own
- LED<n> lights, the LED/led display-segment flashers, the FlBGL backglass flashers, the L13, L45, L61 and L63 and EMReel reels, and the VR room walls and ramps: backbox, desktop and render helpers, not playfield devices
- <target>y walls (sw9y and the like) and the psw<n> primitives: the drop targets' animation helpers; each target is placed on its own sw<n> wall
- DRAIN and BallRelease kickers: the one-ball virtual stack's entry and its shooter-lane exit, not the physical outhole
- Gate003 and Gate7 and the TriggerLF, TriggerRF and ballatplunger triggers: passive or helper objects with no controller binding

## Blockers

- No playfield lamp is placed (56 of the 60 lamp outputs; the other four are backbox lamps): the retained table, the only Meteor table available, draws every insert with lights that show no bulb mesh, and the manual's playfield parts drawing draws the insert circles without lamp numbers, so no source marks a socket (docs/SPATIAL.md, Picking the bulb).
- The outhole switch 33 and the outhole kicker (public 15) are not placed: both known-working scripts and the table model the outhole as a one-ball virtual stack with no object at the switch, and the playfield parts drawing does not show the outhole.
- The upper right flipper's series `E.O.S.` contact (physical direct input 6) is not placed: the playfield coil sheet draws it in the circuit only and does not say which flipper assembly carries it.
- Every switch, coil and general-illumination placement is `observed` from the one table; no factory-drawing callout check was made, and the manual has no switch or lamp location drawing.
- The placements of the three-banks' middle and lower targets (switches 10, 11, 20, 21, 23 and 24) are `conflicted`: they follow the playfield sheet's matrix labels, which the known-working scripts' bindings contradict (the record's conflict).

## Promotion decision

Promotion to `author_ready` is refused: no playfield lamp has a socket, the outhole has no physical object, every placement rests on one table with no factory-drawing check, and the three-banks' middle and lower targets carry an unresolved conflict about their switch numbers. It stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/meteor-1979/archive/extracted-vpxtool.manifest.json`, SHA-256 `9b16fc8e7a8138c42388241618c9799ba4b40ba41b68dff363bc8ed9b443aab8`, 1169 files, 115729773 bytes.
