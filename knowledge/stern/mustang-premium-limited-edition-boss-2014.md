# Mustang Premium / Limited Edition / Boss (Stern, 2014)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**

## Identity and variants

This definition covers the shared Premium, Limited Edition, and Boss playfield used by PinMAME `mt_*h`, `mt_*hb`, and `mt_*hc` drivers. Boss changes the presentation package; `c` changes ROM display colorization. Non-`h` drivers are the physically different Pro machine and belong to a separate partial definition.

## Evidence precedence

The known-working VPW table script `Mustang (Stern 2014) v1.27.vbs` is authoritative for controller-facing addresses, callbacks, initial runtime state, active polarity, ball routing, and mechanism causality. The official Stern manual is authoritative for physical device inventory, construction, wiring, part numbers, and diagnostic numbering. Pinned PinMAME source is authoritative for SAM controller topology, custom-solenoid routing, display shape, and driver identity. Static analysis of exact Mustang 1.45 LE firmware supports ROM-resident diagnostic semantics but never overrides observed working-script behavior.

## Switch topology

Matrix switches 1-64, dedicated D1-D8 at public 65-72, flipper switches D9-D16 at public 81-88, D17-D24 at public -7 through 0, and DIP D25-D32 are all enumerated. Switches 49 and 50 are the mid-ramp-down and upper-ramp-down positions shown by the manual; the working script only actively updates 50. Switches 52 and 53 are the turntable index and home optos. Single drop targets are 56 right and 57 left. The normally-closed EOS contacts are 83 left and 81 right.

## Lamp addressing

Physical service-manual diagnostic numbers and PinMAME callback channels are not identical for the 64 Board-5 LED channels. The JSON therefore keeps the physical number as `manual.address` while binding the public `ChangedLamps` address. Standard lamps 1-80 are direct. Diagnostic 98 Toolbox is public 103 and diagnostic 99 New Car is public 102. Diagnostic white arrows 109-112 are public 98-101; 113-116 remain public 113-116. RGB channels serialize in G/B/R-style groups: for example physical arrow-1 diagnostics 117/118/119 map to public 119/117/118. Physical action-button white 141 is public 129, and red/green/blue 142/143/144 map to public 144/142/143. Bind the controller to JSON addresses, not the printed diagnostic number.

## Coils and auxiliary driver board

Main outputs 1-32 use the SAM I/O Power Driver board. The 12-transistor board 520-5326-02 is split by PinMAME into public addresses 51-56 for physical Q51-Q56 and public 59-64 for physical Q41-Q46. Thus the right scoop printed as manual output 41 is public 59, the diverter 42 is public 60, backbox flashers 43-45 are public 61-63, and unused Q46 is public 64. Public holes 57, 58, 65, and 66 are enumerated as unused so the complete 16-custom-solenoid SAM space remains explicit.

## Trough and shooter lane

The manual defines six ball-position sensors 17-22 plus jam opto 23. The working script creates six balls but calls `InitSw 0,23,22,21,20,19,18,0`, so its proven runtime model occupies 18-23 and omits physical sensor 17. Recreate all seven physical inputs, preserve the script-compatible runtime ordering until a ROM harness proves a better mapping, and keep this discrepancy visible. Output 1 ejects from the right end and the script pulses switch 22; output 2 auto-launches from shooter-lane switch 47.

## Raising ramps

The mid ramp uses power output 3, hold output 4, and physical down switch 49. The working script keys motion from hold output 4 but does not update 49: asserted lowers its modeled height from 60 to 0 and enables the upper collision surface, while de-asserted raises it and removes that surface. The upper ramp similarly uses power 5 and hold 6; asserted hold lowers from 120 to 60, removes its blocker, and clears switch 50, while de-asserted raises it, restores the blocker, and activates 50. Follow this working-script polarity even though the printed `Upper Ramp Down` label makes the active raised state counterintuitive.

## Turntable and car

Output 22 runs the Mustang car turntable. The working recreation advances the car by 0.1 degree per timer tick. Index opto 52 is active across seven broad sectors separated by narrow clear windows. Home opto 53 becomes active above roughly 352 degrees through wraparound and clears between approximately 3 and 5 degrees. The car and opposite decorative disc rotate in opposite directions; sample current turntable angle for any attached visuals rather than assuming a fixed home-only animation.

## Drop targets and gates

GEARS switches 34-38 latch while down and output 7 resets the entire five-bank. The right single target uses switch 56 with outputs 53 up and 54 down; the left uses switch 57 with outputs 55 up and 56 down. Their switch states are sustained. Public outputs 51 and 52 open the left and right orbit gates while asserted. Public output 60 selects the alternate left-ramp route and has no separate position sensor.

## Scoop and captive ball

The right scoop holds a ball on switch 43 and public output 59 ejects it. The working table uses direction 185 degrees, force 20, Z 0.4, and force variance 2. Its optional erratic-scoop helper momentarily applies a script-only magnet to make settling look natural; do not invent a PinMAME magnet output for it. The captive-ball assembly contains one nailed ball, uses back switch 8 and front/rest switch 9, and in the working recreation uses force transfer 1, minimum impact force 7, and captive travel parameter 10.

## Standard mechanisms

Four pop bumpers pair switches 30-33 with outputs 9-12. Slingshots pair switches 26/27 with outputs 13/14. Lower flippers use outputs 15/16, buttons 84/82, and normally-closed EOS inputs 83/81. Spinner rotations pulse switch 48. Standups 1-5, 41-42, and 54-55 pulse; lane, orbit, outlane, trough, scoop, ramp, and target-position switches remain active while occupied or positioned as described by the JSON.

## Recreation checklist

- Build every physical input and output listed in the JSON, including explicit unused controller addresses, the seven trough/jam sensors, 12-transistor board, standard matrix lamps, Board-5 LEDs, and native 128x32 DMD.
- Initialize the five-bank and both single targets raised, the turntable at home, ramps according to the working callback states, and the captive ball at front/rest switch 9.
- Use public callback bindings from the JSON for node-board LEDs and auxiliary outputs; retain printed numbers as diagnostic aliases only.
- Preserve separate power and hold windings for both ramps even though the working VPX animation keys primarily from hold outputs.
- Treat VPX force, angle, travel, and timing values as proven authoring starting points; refine geometry against physical measurements without changing controller causality.

## Sources

- `manual.mustang-premium-boss-le`: official Stern manual `Mustang_LE_web.pdf`, SHA-256 `b2ae8cdffdfba0640e4f82951369b0596d7599f52111acd1cf794918145917cc`; I/O tables on PDF pages 8-17 and parts/mechanism drawings later in the document.
- `vpx.mustang-premium-le-vpw-1.27`: known-working VPW script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `092611fc754374d11d032b81b63638b5a2dc2f43464ee6c7c3cd27874c77e5c3`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and Mustang node-board/custom-solenoid configuration.
- `rom.mustang-le-1.45-static-analysis`: exact 1.45 LE image, CRC32 `20ec78b3`, SHA-256 `4d26f0cca37435800ea84fa6687e0d6be006437194db36d9087e0e8bcdb9cf25`; ROM bytes remain external and are never committed.
