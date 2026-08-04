# Spider-Man (Stern 2007)

Coverage: **author-ready — exact inventory, causality, and normalized spatial placements validated.**

This note supplements the canonical definition with the physical and behavioral information needed to reproduce Stern's original Spider-Man table. The JSON enumerates all 96 controller inputs, 117 outputs, the 128×32 DMD, all 45 supported ROM variants, and 15 ball-device or moving assemblies.

## Evidence policy used for this machine

The embedded Script stream freshly extracted from the exact retained `Spider-Man_3.0.vpx` is ground truth for controller addresses, callbacks, ball routing, initial logical states, and mechanism causality. Stern's 2007 service-game manual is ground truth for physical names, contacts, parts, assemblies, wiring, voltages, lamp technology, and playfield layout. PinMAME revision `4ec52ff0ac133ac251681518aed2249e19fe26eb` controls SAM routing, DMD topology, output types, and ROM membership. The adjacent `Spider-Man_3.0.vbs` sidecar is retained only as secondary/corroborating evidence because it is not byte-identical to the embedded stream.

This separation matters when comparing the original game with the 2016 Vault Edition. They share most playfield addresses and mechanism causality, but the original uses incandescent controlled lamps except for three white bumper LEDs, has only the three standard optional ticket-service identities 33–35, and actively shakes the Green Goblin from output 19.

The exact retained table has table SHA-256 `97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47`; fresh `vpxtool git:v0.33.3` extraction produced embedded Script SHA-256 `ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128`. The secondary sidecar SHA-256 `cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237` declares `NoUpperRightFlipper`/`NoUpperLeftFlipper` and `UseSolenoids = 2`; the embedded stream has neither declaration and uses `UseSolenoids = 1`. The sidecar also adds cvpmSaucer exit-variance and later audio/rolling helpers. These differences are disclosed but never allowed to override embedded runtime semantics.

## Controller and variants

The original table is a Stern S.A.M. machine with a 64-position switch matrix, 32 dedicated positions including eight DIP switches, an 80-lamp matrix, 32 main driver outputs, three optional physical ticket/coin service functions, one logical GI relay, and one 128×32 DMD. PinMAME exposes normalized active switch state, so a recreation must not reapply emulator inversion; the definition's `normally_closed` values describe the physical contacts only. PinMAME public solenoid 33 is a separate synthetic game-on state.

Matrix switches are public addresses 1–64. Dedicated D1–D8 are 65–72; D9–D16 map to 84, 83, 82, 81, 88, 87, 86, and 85; D15 (86) is the upper-right flipper button and D16 (85) its normally-closed EOS; D17–D24 are -7 through 0; and D25–D32 are DIP addresses 1–8 in the DIP group. Lower-left EOS 83, lower-right EOS 81, and upper-right EOS 85 are normally closed by the physical manual; ordinary playfield switches and optos close when actuated; and the optional slam-tilt circuit is normally closed. The embedded script asserts public 86 from `RightFlipperKey` but does not assert 85, so it is not evidence for the EOS identity or polarity.

The 45 supported `sman_*` drivers are firmware revisions, language packages, or display/audio ROM modifications on the same physical product. `sman_262` replaces music but does not change the playfield I/O, wiring, mechanisms, or DMD dimensions. Driver years extending through 2014 are software release dates; the physical machine remains the 2007 Stern product.

## Ball inventory and trough

The game requires four balls. Manual PDF page 37 shows the service trough test and explicitly identifies occupied trough switches 18–21, stack/jam opto 22, and shooter lane 23. Assembly 500-6318-24-ND uses three roller switches and a dual transmitter/receiver opto pair. A blocked opto beam closes its controller switch.

The embedded script constructs a four-ball trough in shooter-to-drain order 21, 20, 19, 18, initializes it with four balls, and binds output 1 to release the shooter-side ball (`Spider-Man_3.0.vpx` embedded Script stream, lines 104–108 and 411–416). Output 2 fires the automatic launcher when switch 23 reports the ball in the shooter lane.

## Doc Ock assemblies

Switch 36 is the Doc Ock VUK, and output 4 ejects its captured ball. The VUK is assembly 500-7078-01 with a 23-800 coil and subminiature roller switch. Output 3 controls the playfield magnet directly.

The Doc Ock webslinger combines the gate, target opto 63, flasher 21, and two curved ball guides. The motorized gate assembly uses the 500-7061-00 mechanism family: a 24 VAC 60 Hz 12 RPM clockwise synchronous motor, driver disc, relay 500-6700-00 on output 5, and limit switches 57 down and 58 up. The embedded script advances the assembly on output-5 activations and initializes it down with switch 57 active (`Spider-Man_3.0.vpx` embedded Script stream, lines 158–160 and 425–438).

## Sandman assemblies

Switch 59 is the Sandman VUK, and output 12 ejects its captured ball. The Sandman moving gate is assembly 500-7061-00, again using a 24 VAC synchronous motor and driver disc. Output 13 drives its relay, switch 53 reports down, switch 54 reports up, and target opto 42 represents the exposed Sandman target. The embedded script initializes the assembly down and toggles the two limits on each activation (`Spider-Man_3.0.vpx` embedded Script stream, lines 158–160 and 440–453).

Output 20 drives the Sandman motorized 3-bank. Its motor frame/motor section is assembly 500-7057-00 and the target bank is 500-7056-01. Switches 9, 10, and 11 are the three target contacts; 49 is the down limit and 50 is the up limit. The embedded script initializes switch 50 active, sets 50 while raising the bank, and sets 49 while lowering it (`Spider-Man_3.0.vpx` embedded Script stream, lines 158–160 and 463–478).

## Green Goblin, gates, diverter, and flippers

The original Green Goblin assembly is 511-5058-00. Output 19 drives its 28-900 no-diode mini-coil and short plunger against the spring-suspended figurine. The embedded script binds output 19 to `solGoblin`, producing the shake animation; switches 1–5 are the five adjacent Goblin target contacts (`Spider-Man_3.0.vpx` embedded Script stream, lines 380 and 456–461). This is the clearest behavioral difference from the Vault Edition, whose working script intentionally disables the same callback.

Outputs 7 and 8 operate the left and right magnetic control gates. Output 22 operates the loop diverter: it starts dropped, rises when energized, and returns to the dropped route when de-energized. Output 15 drives the lower-left flipper with button 84 and normally-closed EOS 83; output 16 drives the lower-right flipper with button 82 and normally-closed EOS 81; output 14 drives the upper-right flipper with D15/button 86 and manual-defined normally-closed D16/EOS 85. The embedded script asserts switch 86 from `RightFlipperKey` and maps Q14 to `solURFlipper`/`RightFlipper2`; it does not assert switch 85.

## Other controlled devices

Outputs 9–11 are the three pop bumpers, 17–18 are the slingshots, and 21, 23, and 25–31 are PWM flashers using #89 bulbs. Output 6 is the optional shaker kit and remains optional because the embedded script leaves that callback commented out. Output 24 is the manual's optional 5 V device position and is used as a virtual knocker callback by the embedded script. Physical ticket-service identities 33–35 exist only when the optional dispenser/meter is fitted and live in `physical.output.ticket`; the stable LibPinMAME solenoid API does not transport them. Public PinMAME solenoid 33 is instead the virtual SAM game-on state. The original game has no additional physical outputs 36–44.

## Lighting, GI, and display

Manual PDF page 8 is the authoritative 80-position lamp matrix. Lamps 55, 56, 73, 79, and 80 are unused, and lamp 2 is the optional tournament-start button. The controlled lamps are predominantly #44 or #555 incandescent bulbs according to location. Lamps 60–62 are the white pop-bumper LEDs, which PinMAME explicitly models as LED strobes for `sman_*`; flashers 21, 23, and 25–31 remain modulated #89 bulbs.

One logical GI relay controls four separately fused 5.7 VAC circuits on manual PDF page 121. This entry is explicitly scoped to US/non-Euro hardware: brown/white has 8 middle/lower-left playfield bulbs, yellow/white has 11 right-side bulbs, green/white has 10 back-panel plus 2 US coin-door bulbs, and violet/white has 13 upper-right bulbs. Euro hardware has 3 coin-door bulbs and requires a regional variant rather than silently reusing this quantity. The manual warns that production quantities may vary.

The display is a single 128×32 DMD. Language, colored-display, and music modifications do not change that physical topology.

## Recreation sequence

Initialize four trough balls, assert position switches 50, 53, and 57, and leave the loop diverter dropped. Then establish these causal paths before tuning motion: drain → switches 18–21 → output-1 release → switch-23 shooter lane → output-2 launch; switch-36 Doc Ock capture → output-4 eject; switch-59 Sandman capture → output-12 eject; output-5 Doc Ock position toggle; output-13 Sandman position toggle; output-20 three-bank toggle; and output-19 Green Goblin shake.

The VPX kick speeds, motor-animation timing, magnet strength, and mesh translations are proven working digital values, not measurements of every physical specimen. Use them as the behavioral baseline, then tune geometry and motion against the manual drawings and a physical table reference.

## Sources

- Stern Pinball, *Spider-Man Pinball Service Game Manual*, June 2007, especially PDF pages 6, 8, 10–11, 37, 68–69, 85, 91–100, and 118–121; external cache SHA-256 `63462d261c7558739b198e96db47a32d7edd4e01bb1e89cd3483736c51043cbe`. Rendered review pages and their hashes are listed in `reports/spatial/stern.spider-man-2007.json`.
- Exact retained `Spider-Man_3.0.vpx` embedded Script stream, freshly extracted with `vpxtool git:v0.33.3`, table SHA-256 `97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47`, embedded script SHA-256 `ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128`.
- Secondary/corroborating `sverrewl/vpxtable_scripts`, `Spider-Man_3.0.vbs` at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237`; this sidecar is not paired with the retained table and cannot override its embedded runtime semantics.
- `vpinball/pinmame`, `src/wpc/sam.c` at revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`, especially the `sman_*` output configuration and game declarations.

## Spatial curation and coordinate contract

The exact matching `Spider-Man_3.0.vpx` is retained outside the repository at `external:pinmame-vpx-sources/stern/spider-man-2007/source/Spider-Man_3.0.vpx`, SHA-256 `97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47`, and was extracted with vpxtool `git:v0.33.3`; its embedded Script stream is SHA-256 `ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128`. Its playfield bounds are exactly 952 by 2115 VPX units. JSON placements use x=0 at the left edge, x=1 at the right edge, y=0 at the rear/backglass edge, and y=1 at the apron edge.

Direct VPX centers are used for all visible inserts, lanes, ramps, kickers, flippers, pops, slingshots, flashers, targets, gates, and optos. Render-only lightmap objects (`LA*`, `LB*`, `l*r`, `Illumina*`, `Fotocellula*`) are not counted as physical sockets. Lamps 66-71 use the exact `bulbPr3`-`bulbPr8` table anchors; the VPX helpers sit at y=-12 because they render on the back panel, so they are explicitly projected to the canonical y=0 boundary. The manual page-9 lamp map independently identifies these six lamps as back-panel lamps.

The VPX contains no physical-center objects for the trough switches, motor limit switches, or some physical flasher bulbs. The definition therefore records the exact table assembly anchor where available: `Primitive.Bank` for switches 49/50 and Q20, `Primitive.Sandman` for switches 53/54 and Q13/Q27, `Primitive.Octopus` for switches 57/58 and Q5, `RightFlipper2` for D16/EOS 85, and `Primitive.Goblin` for Q19. The five trough points are the manual 500-6318-24-ND under-apron assembly projection in ball order; SW22 remains a distinct jam opto rather than a fifth cvpmTrough ball position. Manual page 11 supplies the two Q23, two Q25, one Q26, one Q27, two Q28, two back-panel, and three pop-bumper flasher multiplicities. Q28's two distinct normalized points are projections of the two manual callouts in the underside view; Q29/Q30 retain their VPX x anchors but are projected to y=0 because the manual identifies them as back-panel bulbs. Those projections are disclosed in the device notes and do not pretend that a VPX render helper is a socket.

GI is one logical public relay with 42 normalized playfield/rear-panel placements, split as manual page 121 circuits brown=8, yellow=11, violet=13, and green rear-panel=10. The physical quantity is explicitly 44 for the US/non-Euro variant because the same green/white circuit adds two US coin-door bulbs; Euro adds a third coin-door bulb and is outside this entry's regional scope. Those cabinet bulbs are intentionally quantity-only and have no playfield coordinate. The manual page-121 rear view is projected to y=0 and the coordinate placement is kept separate from the VPX GI collection's synchronized render helpers.

The source order is deliberate: the Stern manual resolves physical construction, multiplicity, EOS wiring, and polarity; the exact table's embedded Script stream resolves runtime address causality and startup states; the matching VPX table resolves direct normalized geometry; and PinMAME resolves SAM public routing and display topology. The sidecar is retained only as explicitly divergent corroboration. No Vault Edition or virtual-only table evidence is used for this definition.
