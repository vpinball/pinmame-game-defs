# Big Buck Hunter Pro (Stern, 2010) spatial review

Status: partial. The physical machine record is `partial` at `machines/partial/stern/big-buck-hunter-pro-2010.json`. Two conflicts, the stacked-bulb and G.I. spatial gaps, and the large unknown address set are recorded in the definition itself.

The matching source is the retained known-working `Big Buck Hunter Pro (Stern 2010).vpx` at SHA-256 `347f5533c2a673611eec9689b8c2ab7456e01db94ea8cae1082eec2545d80626`. The retained extraction produced the embedded script at SHA-256 `da706d513c20c0936013e7c76eba6394408b20a6e9c7e9526873c969211b2e5c`; that embedded stream is the runtime and causality authority. Exact playfield bounds from the table's own `gamedata.json` are `left=0 top=0 right=979 bottom=2162`, so every canonical coordinate is x/979.0 and y/2162.0 rounded to at most six fractional places. Note the x divisor: this table is 979 units wide, not the 952 most WPC-era tables in this project use.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the IPDB-hosted partial manual is the physical construction authority for the addresses its drawings label; pinned PinMAME owns controller topology; the retained table supplies geometry.
- This manual carries no electrical tables and PinMAME's own game block says none exists; its per-game output typing was reconstructed from the community table this project retains. Every unbound address is therefore recorded `unknown`, never `unused`.
- The trough is the one mechanism whose addresses the manual labels directly (SW. 18-22 on PDF page 3), and it anchors the construction evidence for the switch matrix.
- The Buck target mechanism's table-side substitute animation (lamp-following with 71/72 writes) is disclosed as a property of the retained recreation, never promoted to machine behavior.
- Public solenoids 33 to 66 are enumerated because `hw.custSol` is hardcoded 16 for every Stern S.A.M. game, but nothing on this machine can drive 51-66 (`SAM_NO_AUX`, gameSpecific1 = 0) and 33 is PinMAME's synthetic game-on state. All carry controlled `virtual` or `unused` records.

## Explicit projections

- pinmame.input.switch address 1: The Buck is a moving target: its hit is detected by the retained table through which of the thirty-one BuckWall ladder segments is raised at the Buck's current animated position, so the hit sensor has no single playfield coordinate. Placement projects onto the Buck target's home position (Primitive.Buck), where the mechanism rests and where the wall ladder begins.
- pinmame.input.switch address 18: Below-playfield trough assembly; the manual's cut-away draws the trough and labels its switches but gives no playfield-surface coordinate. Placement projects onto the trough's own ball-release kicker (Kicker.BallRelease), the same documented projection every other thin-table trough in this project uses.
- pinmame.input.switch address 19: Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.
- pinmame.input.switch address 20: Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.
- pinmame.input.switch address 21: Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.
- pinmame.input.switch address 22: Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.
- pinmame.input.switch address 37: The Buck drive's position feedback travels with the moving target along the deer-track fiber assembly; no fixed sensor coordinate exists in any retained source. Placement projects onto the deer-track ladder's midpoint (the mean of the BuckWall1-31 drag-point centroids), disclosed as a projection, not an observation.
- pinmame.input.switch address 45: Same Buck-drive position-feedback projection as switch 37.
- pinmame.output.solenoid address 1: Below-playfield coil; placed at its own ball-release kicker's position like the trough sensors, the standard thin-table trough projection.
- pinmame.output.solenoid address 2: The auto-launch coil sits behind the plunger assembly; placed at the Plunger object's position as the assembly's own anchor.
- pinmame.output.solenoid address 3: The Buck drive's coils and motor live inside the moving-target mechanism below/behind the track; all three project onto the Buck target's home position (Primitive.Buck), the mechanism's own fixed anchor, disclosed as a projection rather than a coil-body coordinate.
- pinmame.output.solenoid address 4: See solenoid 3's projection note.
- pinmame.output.solenoid address 5: See solenoid 3's projection note.
- pinmame.output.solenoid address 12: Below-playfield coil; placed at the Kicker.sw34 ball-sense position it serves, disclosed as an assembly anchor rather than the coil body's own coordinate.
- pinmame.output.solenoid address 14: The Elk diverter's coil is inside the mini-flipper assembly; placed at the Elkdiverter flipper object's own pivot.
- pinmame.output.solenoid address 15: The flipper coil sits inside the flipper assembly below the playfield; placed at the LeftFlipper object's own pivot as the assembly's anchor, not the coil body's coordinate.
- pinmame.output.solenoid address 16: See solenoid 15's projection note (RightFlipper pivot).
- pinmame.output.solenoid address 26: The f126 flasher is a tall shape carried by drag points; placed at the centroid of its four drag points, recorded as a derivation rather than a measured center.

## Counts

- Placements: 117
- Located input addresses: 37
- Located output bindings: 74
- Inputs with a controlled `cabinet_or_service` record: 25
- Inputs with a controlled `dip_switch` record: 8
- Outputs with a controlled `unused` record: 16
- Outputs with a controlled `virtual` record: 18
- Devices with no `spatial` key at all: 73

## Named spatial gaps

- outputs[binding.device=27,28,29,30] (pinmame.output.lamp) carry no spatial key: the retained table renders all four as colored bulb Primitives stacked at raw (401.3, 263.9, z 290) with Flash-glow partners clustered around raw (352.5, 250-371), so four distinct physical bulb positions cannot be derived from the stack. See the lamp records' own notes.
- outputs[binding.device=0] (pinmame.output.gi) has no spatial key: the partial manual prints no G.I. bulb inventory, and the retained script's UpdateGI drives one 27-light collection for any string index, so no per-bulb placement set can be asserted. The 27 retained GI positions are in the geometry dump.
- The switch and solenoid semantics the retained sources cannot reach stay unknown: matrix switches 2, 3, 4, 12, 17 and 46-64, solenoids 6, 8-11, 13, 17, 18, 24, 28 and 30, the 73-80 extended switch block, and lamps 1-2 (never observed driven). The attract-mode harness run resolved the other twenty lamp addresses to observed-driven; the remaining route is a service-menu coil/switch harness run, whose navigation is mapped in the knowledge note.

## Excluded retained objects

- Stacked bulb Primitives L27-L30 and their Flash partners f27-f30: four lamp addresses rendered at one position, so no distinct per-address placement exists.
- Unbound decorative flasher shapes f1, f2, f5, f6, f7 (above the playfield's top edge) and unbound lights f131a1/f131a2: no callback binds them to any address.
- Ten Timer objects (BuckTimer, LampTimer, ...): editor timers with arbitrary positions, not physical devices.

## Promotion decision

Promotion to `author_ready` is refused. Two conflicts remain unresolved (`conflict.sam-invsw-never-populated`, `conflict.elk-button-physical-control`); the switch semantics of the 46-64 matrix block and the eight-address 73-80 extended block, the identities of eleven solenoids, and lamps 1-2 remain unknown because no electrical table exists in any retained source; the attract-mode harness run resolved the other twenty lamp addresses to observed-driven and the remaining route is a service-menu coil/switch run whose entry key is still unmapped; recreation knowledge remains observed until that run exercises the ROM's Buck feedback and the Elk button path; and the stacked-bulb and G.I. spatial gaps have no honest placement set. The record therefore stays `partial` with `coverage.missing = ["input_semantics", "output_semantics", "polarity", "recreation_notes", "spatial_placement", "unresolved_conflicts"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/big-buck-hunter-pro-2010/extracted-vpxtool.manifest.json`, SHA-256 `3b50291ecc3fe665c082567801ae2319f31b49142153ae24f6e2bfff5d80d9e9`, 822 files, 100412917 bytes.
- Full per-object geometry dump of the retained extraction, SHA-256 `7cbd1ece1730ced491bf178d81b0812d8c0ac70721ed1adfb236fc9347f0a88e`.
- Committed, digest-verified manual transcriptions under `evidence/excerpts/stern.big-buck-hunter-pro.2010/`.
- ROM identity verification (three exact matches, one mismatching 1.7 dump) recorded in the `rom.stern.big-buck-hunter-pro` source record and the bbh_170 driver note.
