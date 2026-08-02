# The Walking Dead Premium / Limited Edition (Stern, 2014)

Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**

## Identity and variants

This definition covers the Premium and Limited Edition physical layout used by PinMAME's `twd_*h` ROMs. The `h` and `hc` driver descriptions identify Limited Edition firmware; `c` is a color-ROM change only. Non-`h` drivers belong to the physically different Pro definition and are deliberately excluded even though PinMAME keeps both editions in one clone tree.

## Evidence precedence

The known-working VPW table script `The Walking Dead LE Premium (Stern 2014) day 1.1.vbs` is authoritative for emulator-facing addresses, callbacks, active states, initial balls, and mechanism causality. The service manual is authoritative for physical device names, construction, parts, dual-winding coils, and wiring. PinMAME is authoritative for SAM node-board mapping, native display topology, inversion, and driver metadata. This matters because the retired VPE hint data disagreed with the working script on several extended lamp channels.

## Playfield inputs

The physical switch matrix uses addresses 1-64, dedicated switches D1-D8 map to PinMAME 65-72, flipper switches D9-D16 map to 81-88 in SAM's right/left and EOS ordering, D17-D24 map to -7 through 0, and D25-D32 are the eight DIP inputs. Every used and unused position is enumerated in the machine JSON with matrix row/column wire colors and connectors.

Premium/LE-only inputs are right drop target 48, Bicycle Girl 49, crossbow home 50, crossbow mark 51, and crossbow eject/ball-loaded 52. The bottom and top star rollovers are dedicated inputs 70 and 72; matrix positions 12 and 13 are unused on this edition. Fire button input is 71. Switch 2 is active at the Well Walker's rest position in the working script. Although the manual calls switch 4 “Prison Doors Closed,” the working script exposes it inactive at the closed initial state and active at the fully open stop; authors must follow that runtime behavior.

## Lamps and general illumination

The conventional physical lamp numbering is 1-80, but RGB devices on the SAM node boards are exposed through extended `ChangedLamps` addresses. Use the JSON bindings, not the physical lamp number, for controller callbacks. Right-loop arrow 24 maps to R/G/B 168/169/170; left-loop arrow 33 to 195/196/197; left-ramp arrow 36 to 203/204/205; right-ramp arrow 41 to 152/153/154; center-lane arrow 57 to 187/188/189. Because of PinMAME's backward-compatible channel ordering, bottom star rollover 79 maps R/G/B to 138/137/136 and top star rollover 80 maps R/G/B to 135/134/133. Lockbar fire button lamp 81 maps R/G/B to 122/121/120. The known-working script models white GI at 106 and red GI at 107 as 0-255 intensity channels; it does not consume the six RGB GI hints formerly shipped by VPE.

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

## Recreation checklist

- Create four balls at trough switches 18-21, initialize the prison doors closed with switch 4 false, initialize the Well Walker with switch 2 true, initialize the crossbow at home with switch 50 true, and initialize both drop-target assemblies raised.
- Bind controller output callbacks to the extended RGB addresses in the JSON; physical lamp numbers alone are insufficient for the node-board lights.
- Keep the physical power/hold distinction for both dual-winding mechanisms even where the VPX script uses only the hold channel as the animation signal.
- Preserve sustained switch states for trough optos, dropped targets, cannon position/load sensors, lanes, and the prison-door state; spinners, bash targets, pops, and slings are pulses.
- Treat script timing and kick force as proven digital-authoring starting points, then tune geometry and forces against real-machine video or measurements without changing the controller causality.

## Sources

- `manual.walking-dead-premium-le`: Stern service manual cached from Internet Archive, SHA-256 `4dd644210cc0432b254b8252b836c73c878517fa16eda119902155ece24f0b3e`; device tables on PDF pages 8-15 and assembly/parts drawings later in the document.
- `vpx.walking-dead-premium-le-vpw-day-1.1`: known-working VPW script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `bd6868c93f180c58f6835cccd869c0fa1e28832fea6afc5bb4f9660505908e47`.
- `pinmame.core.4ec52ff0ac13`: pinned PinMAME SAM implementation, including TWD node-board emulation and backward-compatible LED channel maps.

