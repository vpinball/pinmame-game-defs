# Pirates of the Caribbean (Stern, 2006) spatial review

Status: partial. The physical machine record is `partial` at `machines/partial/stern/pirates-of-the-caribbean-2006.json`. Two output addresses carry no spatial record at all and are named below; four unresolved conflicts and incomplete recreation knowledge are recorded in the definition itself.

The matching source is the retained known-working `Pirates of the Caribbean (Stern 2006).vpx` at SHA-256 `d69fea24ad8d1dd4fc49c84214e71b448d6a602b6ef768a329a55a94f15aad59`. The retained extraction produced the embedded script at SHA-256 `fb6cec754fc907f1fbb41f1f71273d6585db73365073b3a18cfe2c12d90c39e3`; that embedded stream is the runtime and causality authority. Exact playfield bounds from the table's own `gamedata.json` are `left=0 top=0 right=952 bottom=2155`, so every canonical coordinate is x/952.0 and y/2155.0 rounded to at most six fractional places. Note the y divisor: this table is 2155 units tall, not the 2162 most WPC-era tables in this project use.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Stern service manual is the physical inventory, quantity, wiring and location authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- This is a thin recreation by this project's standards: 1,229 extracted files and a 32,543-byte script, against the 240-290 kB VPW-authored scripts several other games in this run used. It is judged on what it actually models rather than promoted for being present. Where it models an address with a plausibly placed object, that object is used; where it does not, no coordinate is invented.
- Lamps 33-39 and 78-80 are back-panel devices per printed page 91 and the Lamp Locations page's own back-panel inset, so all ten carry a controlled `cabinet_or_service` record even though the retained table models a Light object for each at the extreme rear edge of the playfield (normalized y 0.020 to 0.022). Those rear-edge coordinates are recorded in the retained geometry dump and deliberately not promoted.
- Lamps 1 and 2 are cabinet button lamps: neither is drawn on the Lamp Locations playfield plan and neither has an object in the retained table's `AllLamps` collection.
- The three pop bumpers are placed from the manual's own left/right/bottom naming and the retained table's own geometry, which admit exactly one coherent bijection, rather than from the retained script's naive numeric object ordering. See `conflict.pop-bumper-position-naming`.
- Public solenoid 22 (`FLASH: REAR CENTER (X2)`) is a backbox device: printed page 91 lists two `#89` sockets on the back panel and labels both `Q22 FLASH`. It carries a controlled `cabinet_or_service` record with quantity 2.
- Public solenoids 33 to 66 are enumerated because `hw.custSol` is hardcoded 16 for every Stern S.A.M. game, but nothing on this machine drives any of them; 33 is PinMAME's synthetic game-on state and the rest are dead address space. All carry a controlled `virtual` or `unused` record.

## Explicit projections

- pinmame.input.switch address 18: Trough position #4; the four trough position switches and the trough jam opto have no individual objects in the retained table, which models the whole 4-ball trough through one cvpmBallStack instance. Projected onto the trough's own ball-release kicker (BallRelease), the object bsTROUGH.InitKick names.
- pinmame.input.switch address 19: Trough position #3; projected onto the trough's own ball-release kicker for the same reason as address 18.
- pinmame.input.switch address 20: Trough position #2; projected onto the trough's own ball-release kicker for the same reason as address 18.
- pinmame.input.switch address 21: Trough position #1; projected onto the trough's own ball-release kicker for the same reason as address 18.
- pinmame.input.switch address 22: Trough jam / stack opto, which sits in the trough's own exit path; the retained script asserts it with vpmTimer.PulseSw 22 from inside SolTrough rather than through an object. Projected onto the trough's own ball-release kicker.
- pinmame.input.switch address 62: Ship Fully Sunk; the retained script derives it from the ship mechanism's own software position counter (ShipTimer_Timer, ShipPos 0-3) with no sensor object anywhere in the table. Projected onto the ship assembly's own Primitive.
- pinmame.input.switch address 63: Ship Home; derived from the same software position counter. Projected onto the ship assembly's own Primitive.
- pinmame.input.switch address 81: Right flipper end-of-stroke switch, part 180-5149-00 on the Flipper Asm.; projected onto the right flipper assembly's own object, which is also where public solenoid 16 is placed.
- pinmame.input.switch address 83: Left flipper end-of-stroke switch, part 180-5149-00 on the Flipper Asm.; projected onto the left flipper assembly's own object, which is also where public solenoid 15 is placed.
- pinmame.output.solenoid address 5: Raise Sails; the sails latch has no separate visible object, so this is projected onto the ship's own SailsUp state Wall, which SolSailsUp is the sub that drops.
- pinmame.output.solenoid address 21: Ship Motor; a motor has no single point of action, so this is projected onto the ship assembly's own Primitive, the object SolShipMotor translates.
- pinmame.output.solenoid address 27: Ship Motor Relay; a Relay PCB (511-5024-03) with no point of action on the playfield at all. Projected onto the ship assembly it reverses, the mechanism it belongs to. The Coil & Flash Lamp Locations page draws its callout on the playfield beside the ship motor's own callout.
- pinmame.output.solenoid address 28: Lower Sails Latch; projected onto the ship's own SailsDown state Wall, which SolSailsDown is the sub that drops.

## Counts

- Placements: 144
- Located input addresses: 50
- Located output bindings: 91
- Inputs with a controlled `cabinet_or_service` record: 18
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 20
- Outputs with a controlled `cabinet_or_service` record: 14
- Outputs with a controlled `unused` record: 22
- Outputs with a controlled `virtual` record: 18
- Devices with no `spatial` key at all: 2

## Named spatial gaps

- outputs[binding.device=30] (pinmame.output.solenoid, FLASH: BACK RIGHT [X3]) has no spatial key: the manual disagrees with itself about how its three #89 bulbs split between the playfield and the back panel, so no placement set can match the printed quantity without picking a side. See conflict.flasher-back-panel-bulb-count.
- outputs[binding.device=0] (pinmame.output.gi, General Illumination Relay) has no spatial key: this manual prints no general-illumination bulb table, so neither a bulb quantity nor a placement set can be asserted. The ten back-panel G.I. sockets and the three right-ramp LED modules are the only G.I. inventory it states; the playfield G.I. bulbs are spread across the Section 4 assembly pages and were not exhaustively enumerated in this pass.

## Excluded retained objects

- l27D, l27e, l27f -- second Light object at each of the three pop-bumper positions already placed from l27c, l27b and l27a; the manual prints POP BUMPER (X3), so three placements, not six.
- l24B, l32b, l40b, l48b, l56b -- Flasher objects the retained script drives from the matching Light's own state (MiscTimer_Timer sets l24B.visible = L24.state and so on). Render doubles of the 520-5258-00 HEART LED PCB, not additional bulbs.
- GISpot1b, GISpot2b, GISpot3b -- Flasher render doubles the same timer drives from GISpot1-3's own state; general-illumination effects, not matrix lamps.
- GISpot1b3 -- a fourth spot-flasher parked at raw (-1295.169, 3806.534), far outside the playfield bounds; a table modelling leftover, excluded rather than clamped.

## Promotion decision

Promotion to `author_ready` is refused. Two output addresses have no spatial record, four conflicts remain unresolved (`conflict.sam-invsw-never-populated`, `conflict.flasher-back-panel-bulb-count`, `conflict.pop-bumper-position-naming`, `conflict.coin-door-adjust-button-order`), opto polarity is unsettled for all seven manual-identified opto addresses because pinned Stern S.A.M. source normalizes nothing. Recreation knowledge remains observed until the missing placements and polarity conflicts can be reconciled. The record therefore stays `partial` with `coverage.missing = ["polarity", "recreation_notes", "spatial_placement", "unresolved_conflicts"]` and `coverage.dimensions.physical_wiring = "conflicted"`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/pirates-of-the-caribbean-2006/extracted-vpxtool.manifest.json`, SHA-256 `b462146e7b641f57fdb08a032c9298ce921675e63798ba245bcca0e3904fe799`, 1229 files, 85415058 bytes.
- Curation record of which manual pages were rendered and read, SHA-256 `e440218cd68c47b1a21a1643f53cb82a7a2f5bb3530b59035045d9a0eb199314`.
- Full per-object geometry dump of the retained extraction, SHA-256 `12f88a9f9a2a76a13a6c71cf3491bf96d4480842663bdf5dc8b388733d6c3dfe`.
- Committed, digest-verified manual transcriptions under `evidence/excerpts/stern.pirates-of-the-caribbean.2006/`.
