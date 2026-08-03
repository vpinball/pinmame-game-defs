# The Walking Dead Premium / Limited Edition (Stern, 2014)

Coverage: **author-ready — physical inventory, PinMAME bindings, mechanisms, recreation behavior, and normalized spatial placements validated.**

## Identity and variants

This definition covers the Premium and Limited Edition physical layout used by PinMAME's `twd_*h` ROMs. The `h` and `hc` driver descriptions identify Limited Edition firmware; `c` is a color-ROM change only. Non-`h` drivers belong to the physically different Pro definition and are deliberately excluded even though PinMAME keeps both editions in one clone tree.

## Evidence precedence

The known-working VPW table script `The Walking Dead LE Premium (Stern 2014) day 1.1.vbs` is authoritative for the callbacks it implements, active states, initial balls, and mechanism causality. The service manual is authoritative for physical construction, parts, dual-winding coils, wiring, and lamp quantities. PinMAME is authoritative for SAM node-board mapping, native display topology, inversion, and driver metadata; an exact firmware output-name table resolves a documented lighting-renderer shortcut in the VPX. This matters because the retired VPE hint data also disagreed with the working script on several extended lamp channels.

## Playfield inputs

The physical switch matrix uses addresses 1-64, dedicated switches D1-D8 map to PinMAME 65-72, flipper switches D9-D16 map to 81-88 in SAM's right/left and EOS ordering, D17-D24 map to -7 through 0, and D25-D32 are the eight DIP inputs. Every used and unused position is enumerated in the machine JSON with matrix row/column wire colors and connectors.

Premium/LE-only inputs are right drop target 48, Bicycle Girl 49, crossbow home 50, crossbow mark 51, and crossbow eject/ball-loaded 52. The bottom and top star rollovers are dedicated inputs 70 and 72; matrix positions 12 and 13 are unused on this edition. Fire button input is 71. Switch 2 is active at the Well Walker's rest position in the working script. Although the manual calls switch 4 “Prison Doors Closed,” the working script exposes it inactive at the closed initial state and active at the fully open stop; authors must follow that runtime behavior.

## Lamps and general illumination

The conventional physical lamp numbering is 1-80, but RGB devices on the SAM node boards are exposed through extended `ChangedLamps` addresses. Use the JSON bindings, not the physical lamp number, for controller callbacks. Right-loop arrow 24 maps to R/G/B 168/169/170; left-loop arrow 33 to 195/196/197; left-ramp arrow 36 to 203/204/205; right-ramp arrow 41 to 152/153/154; center-lane arrow 57 to 187/188/189. Because of PinMAME's backward-compatible channel ordering, bottom star rollover 79 maps R/G/B to 138/137/136 and top star rollover 80 maps R/G/B to 135/134/133. Lockbar fire button lamp 81 maps R/G/B to 122/121/120.

The exact `TWD160h.BIN` localized output-name table identifies node-board-3 1-based output IDs 25-28 as `WHITE`, `BACK PANEL`, `LEFT DROP TARGET BANK`, and `RED`. PinMAME `sam.c:1913-1919` maps zero-based node-board-3 `ledMap` index i to `CORE_MODOUT_LAMP0 + 81 + i`, which is public lamp `82 + i`; firmware IDs 25-28 are indices 24-27 and therefore public addresses 106-109. Manual sheet Y26 independently lists the corresponding four physical circuits as GI-0-WHT, GI-1-BACK PANEL, GI-2-GRN, and GI-3-RED. The resulting physical mapping is therefore 106 = 23 white playfield emitters, 107 = two red emitters on the five-socket GI panel, 108 = the panel's three green emitters controlled by the firmware effect named `LEFT DROP TARGET BANK`, and 109 = 14 red playfield emitters. The boot/start trace independently modulates 106 while 107-109 remain byte-for-byte identical; the lamp-diagnostic trace observes one common 255 event on each of 106-109. These traces prove public activity but not the individual identities supplied by the exact firmware table.

The known-working VPX correctly consumes 106 as white GI but applies 107 as a broad red-GI rendering channel and omits 108/109. That script remains authoritative for its proven controller and mechanism behavior, but its simplified lighting model conflicts with the exact firmware name table and the manual's physical circuit inventory. The definition records the physical machine mapping from the exact-ROM-plus-manual evidence instead of propagating the table's rendering shortcut.

## Coils, magnets, flashers, and motors

Main outputs 1-32 and their deliberately unused positions are listed with manual power/control wiring. Outputs 3 and 4 are the prison-door dual-winding power and hold windings; 5 is the ramp-diverter magnet; 6 is the Well magnet; 7 is the prison magnet; 8 is the optional shaker; 21 is the crossbow motor. Premium/LE auxiliary outputs are 51 crossbow eject, 52 right drop target down, 53 right drop target up, 55 Bicycle Girl ramp power, and 56 Bicycle Girl ramp hold; 54 is unused. Output 24 is an optional coin-meter output.

## Trough and launch path

Four balls are created at switches 18, 19, 20, and 21. A drain enters the left side; after a 150 ms settle interval the working script cascades a vacancy 18 → 19 → 20 → 21, with switch 22 covering the entrance/jam position. Output 1 kicks the ball from switch 21 toward shooter-lane switch 23. Output 2 fires the auto-plunger from the shooter lane. These are functional starting values from the known-working recreation rather than factory timing specifications.

## Prison assembly

The two prison doors rotate together in opposite directions. Output 3 begins opening with the power winding. The working script begins closing when output 4 de-asserts; it animates twelve non-linear angular steps between 0 and roughly 96 degrees. Treat switch 4 exactly as the script does: false at closed, true at the open stop. Switch 46 is the entry opto. Output 7 controls the capture magnet behind the doors; on release, the working recreation adds a small randomized forward and lateral velocity to avoid a straight-down return.

## Crossbow cannon

At home, switch 50 is active. A ball entering the cannon makes switch 52 active. Output 21 starts the motorized sweep: once it leaves home the script clears switches 50 and 52, activates switch 51 at the aiming mark near the middle, continues to its far limit, pauses, reverses, clears 51, and reactivates 50 on reaching home. If it still carries a ball, 52 reactivates at home. Output 51 ejects the ball in the current cannon direction, so the firing angle must be sampled from the current mechanism position rather than hard-coded.

## Drop targets

The left three-bank comprises switches 9, 10, and 11. A target switch remains active while its target is down; output 12 raises the whole bank. The working script uses about 110 ms for downward travel, 40 ms for the first upward movement, and a 40 ms overshoot pause before settling. The separate right drop target uses switch 48, output 52 to force it down, and output 53 to raise it.

## Bicycle Girl ramp and target

The ramp uses a physical dual-winding coil: output 55 is the short power/open winding and output 56 is the hold winding. The known-working script intentionally attaches its animation to output 56 only: asserted raises the ramp and disables the blocking surface, while de-asserted lowers it and restores the surface. Do not wait for an output-55 callback before animating. The nearby Bicycle Girl bash figure is a spring-return target on switch 49 and is independent of ramp position.

## Well Walker and prison walker

The Well Walker is a spring-return bash toy combined with the output-6 magnetic ball-control zone. Its switch 2 is active at rest, clears when struck, and becomes active again after return. The Prison Walker is a separate spring-return bash target on switch 3. Their flashers are output 19 for Well Walker and outputs 26/27 around the prison area.

## Standard mechanisms

The left and right spinners pulse switches 40 and 1. Pop bumpers pair switches 30-32 with outputs 9-11. Slingshots pair switches 26/27 with outputs 13/14. Lower flippers use outputs 15/16, buttons 84/82, and normally-closed EOS inputs 83/81. Ramp, lane, outlane, and loop switches are fully enumerated in the JSON and should be placed according to the manual's switch and lamp location drawings.

## Spatial reconstruction

All coordinates use normalized player view: x=0 at the left rail, x=1 at the right rail, y=0 at the rear/backglass end, and y=1 at the apron. The exact VPW table geometry supplies object centers and the manual's switch, lamp, flasher, and GI location drawings supply physical identity and emitter quantity. Of 96 enumerated inputs, 46 playfield sensors are located and the remaining 50 are explicitly controlled as non-playfield cabinet/service switches, DIP switches, or unused matrix positions. The four trough sensors share their physical trough-path area, while switches belonging to the prison doors, cannon, Well Walker, drop banks, and Bicycle Girl mechanisms are located at their real assemblies rather than spread apart for diagram readability.

Lamp channels that drive one physical package deliberately share a coordinate. This includes paired lamp callouts 70/71, the three-channel fire-button package 73/74/75, and every RGB arrow, star-rollover, and lockbar package. Each physical flasher emitter is represented separately: outputs 19, 20, 25, 26, 28, 29, 31, and 32 have one emitter each, while output 27 has two prison-area emitters. GI emitter inventory follows manual sheet Y26 exactly: public 106 places 23 white playfield lamps, 107 places two red lamps on the five-socket GI mounting panel, 108 places the same panel's three green lamps, and 109 places 14 red playfield lamps. `LEFT DROP TARGET BANK` is the firmware's effect name for 108, not a claim that those three sockets sit directly over the target bank.

The five-socket inset is a service/rear-face drawing: it exposes the `077-5000-00` staple-bayonet socket mounting hardware and rear connector/board enclosure rather than the decorated player-facing side. The `R R G G G` marks are ordinary drafting annotations and are not used as handedness evidence. Each socket center is normalized across that inset's panel outline, converted with `x_player = 1 - x_service`, and projected to y=0 because the panel is vertical at the rear playfield boundary. The resulting player-view red positions are x=0.967900 and 0.771000; the green positions are x=0.546400, 0.480000, and 0.415800. This recorded derivation is intentionally separate from the bilaterally symmetric playfield socket sets, whose handedness does not alter their coordinates.

The spatial JSON intentionally distinguishes evidence from inference. The VPX candidate extraction is tied to the exact 217,935,872-byte table, SHA-256 `2aca72eb73ac11cc1f8d5633cd8bb302146ac2dd91bfa5fb8364a314b5179987`; it proves table geometry but not controller semantics. Manual callouts and the proven script resolve ordinary device semantics, while the exact ROM table resolves the four extended GI identities where the VPX is simplified. The runtime trace confirms that public addresses 106-109 exist, but because 107-109 remained lockstep in the observed windows it does not independently prove their logical separation.

## Recreation checklist

- Create four balls at trough switches 18-21, initialize the prison doors closed with switch 4 false, initialize the Well Walker with switch 2 true, initialize the crossbow at home with switch 50 true, and initialize both drop-target assemblies raised.
- Bind controller output callbacks to the extended RGB addresses in the JSON; physical lamp numbers alone are insufficient for the node-board lights.
- Keep the physical power/hold distinction for both dual-winding mechanisms even where the VPX script uses only the hold channel as the animation signal.
- Preserve sustained switch states for trough optos, dropped targets, cannon position/load sensors, lanes, and the prison-door state; spinners, bash targets, pops, and slings are pulses.
- Treat script timing and kick force as proven digital-authoring starting points, then tune geometry and forces against real-machine video or measurements without changing the controller causality.

## Sources

- `manual.walking-dead-premium-le`: Stern service manual cached from Internet Archive, SHA-256 `4dd644210cc0432b254b8252b836c73c878517fa16eda119902155ece24f0b3e`; device tables on PDF pages 8-15 and assembly/parts drawings later in the document.
- `vpx.walking-dead-premium-le-vpw-day-1.1`: known-working VPW script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `bd6868c93f180c58f6835cccd869c0fa1e28832fea6afc5bb4f9660505908e47`.
- `vpx-table.walking-dead-premium-le-vpw-day-1.1`: exact source table retained in the organized VPX evidence cache, 217,935,872 bytes, SHA-256 `2aca72eb73ac11cc1f8d5633cd8bb302146ac2dd91bfa5fb8364a314b5179987`; deterministic candidate extraction SHA-256 `bd5ac67ef82dd077830afce80be113584d3d87283f65f532a0e6f6101d8aa9c4`.
- `rom-static.walking-dead-premium-le-output-names`: exact user-authorized `twd_160h.zip`, SHA-256 `e09cba4477c9d551e858c0b4c8ee005fb041d3008a4cc5e928d502127329d3fd`; archive member `TWD160h.BIN` has SHA-256 `5f618c875d160ce27a73a0edf30659b63f08478147c4476b5b8916a614d6d6a3`, PinMAME-declared SHA-1 `1fbaa077ec834ff9d289008ef1169e0e7fd68271`, and CRC32 `1ed7b80a`. Localized records and their 1-based output-ID table are at file offsets `0x109060` through `0x1090e0`. ROM bytes remain external.
- `runtime.walking-dead-premium-le.boot-start`: exact `twd_160h` boot/start trace SHA-256 `dc40cfe85c90de2cc8c2ae16a8ca5a0d3cf2f8cbdc24d7eba39600601506fa77`, which independently modulates 106 while 107-109 remain lockstep.
- `runtime.walking-dead-premium-le.gi-lamp-diagnostic`: exact `twd_160h` lamp-diagnostic trace SHA-256 `c8f78d6bd0d52632049f1f1ee445e47d10db698355a681dc7e8d1da14b6c4a64`; it observes one common 255 event on each of 106-109. Both runtime traces use PinMAME DLL SHA-256 `79f6cfb0048470218b2302ca4fb0d078839acf7f05883c36fc93881ba8abac84`.
- `pinmame.core.4ec52ff0ac13`: pinned PinMAME SAM implementation, including TWD node-board emulation and backward-compatible LED channel maps.
