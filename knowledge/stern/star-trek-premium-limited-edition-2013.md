# Star Trek Premium / Limited Edition (Stern, 2013)

Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, recreation behavior, and spatial placements validated**

## Identity and evidence precedence

This definition covers `st_*h` and `st_*hc` drivers. Those revisions share the Premium/LE playfield; `c` only changes ROM display colorization. Non-`h` drivers are the different Pro machine and have their own definition. The known-working `Star Trek LE (Stern 2013) v1.10.vbs` is ground truth for controller bindings, callbacks, mechanism causality, and active behavior. For the trough alone, the exact Neo table governs initialization and ejection sensing because its switches 18-21 and downstream switch-22 pulse agree with the official manual; v1.10's switch-18 drain and 19-22 ball chain remain a documented virtual-table exception. The official Stern manual governs physical inventory, wiring, diagnostic numbering, and assemblies. Pinned PinMAME source governs the SAM transport, display, custom-solenoid serialization, node-board topology, and driver identity.

## Controller topology

The four node boards expose public lamp ranges 81-144, 146-209, 211-274, and 276-339. Public addresses 145, 210, and 275 are deliberate compatibility gaps, not lamps. The JSON enumerates every addressable lamp channel and marks unused channels explicitly. Main solenoids are 1-32. The auxiliary board exposes Q51-Q56 as public 51-56 and physical Q41-Q46 as public 59-64; 57-58 and 65-66 are explicit unused holes.

## Switches and initial ball state

All matrix positions 1-64, dedicated D1-D24, and DIP inputs are enumerated. The physical four-ball trough has left-to-right sensors 18-21 plus downstream jam opto 22. The official manual and exact Neo table agree that the four balls occupy 18-21 and output 1 ejects from switch 21; Neo pulses switch 22 on ejection. The older v1.10 table instead uses switch 18 as its drain and creates balls on 19-22. That virtual-table layout is preserved as a portability warning but rejected for physical construction and initial switch state. Shooter lane is 23. Fire is public 71/D7; the upper-right flipper button is public 86/D15. Lower buttons are 84 left and 82 right, with normally-closed EOS contacts 83 left and 81 right.

## Lamps

Manual physical lamp numbers are diagnostic identities, while the JSON binding is the PinMAME `ChangedLamps` callback address observed in the working script. Physical lamps 1-49 are RGB node-board devices; their public channels are not their printed numbers. For example physical lamp 1 maps red/green/blue to public 84/85/86. Physical 50 and 51 map to 276/277. The RGB warp emblem 52 maps to 278/279/280. Start, tournament, and fire-button channels occupy public 76-80. Warp chasers map to 292-299 in script order. Cabinet Enterprise is public 75; cabinet phaser diagnostics 79-100 map to public 51-72. Always bind to public addresses and retain the printed number only as `manual.address`.

## Center memory target and magnet lock

The single center target uses switch 11, output 4 up, and output 5 down. The script activates switch 11 while down and releases a captured ball when raising it. The lock magnet is PWM output 3; the proven table uses a radius-135 centered field and allows multiple-ball capture. Lower and upper lock optos are 33 and 34.

## Left eject and rotating VUK

Switch 10 remains active while the left eject holds a ball. Output 55 rotates its two-way VUK/deflector and output 6 ejects along the selected path; no position switch exists. The known normal path uses 85 degrees, force 38, and Z 100. Build the rotating routing geometry even though both operations share the same scoop opening.

## Vengeance battleship

The ship is a latched animated mechanism, not a decorative flasher. PWM output 53 drives its dive and shake, output 56 controls the latch/return, and switch 53 represents the crashed/latched state. Output 7 then returns the ball at super speed. The working 100 Hz animation uses down steps 2-50, shake steps 101-154, and return steps 201-250; use these as a proven timing and motion baseline, then align geometry to the physical ship.

## Gates, kickback, laser, and standard devices

Outputs 51/52 control the left/right orbit gates. Output 54 is the bottom right-drain kickback paired with switch 44; output 7 is instead the Vengeance kicker. Output 22 drives the laser projector without a position sensor. The machine has three flippers, three pops, two slings, a spinner at switch 12, three ramps, four balls, a six-target red bank, a center three-bank, a left two-bank, and the four TREK targets. Output 8 is the optional shaker and output 24 the optional coin meter.

## Recreation checklist

- Construct all physical inputs and outputs, including explicit unused controller addresses, four node boards, auxiliary board, GI group, and native 128x32 DMD.
- Initialize four physical trough balls on switches 18-21 and keep downstream jam opto 22 clear until ejection; do not reproduce the older v1.10 table's switch-18 drain and 19-22 ball-chain simplification.
- Preserve PWM for the center magnet and Vengeance actuator; do not reduce either to a simple pulse.
- Model the memory target, multi-ball magnet hold, rotating VUK route, Vengeance latch/crash/return sequence, orbit gates, bottom kickback, laser motor, upper flipper, and all sensed ball paths.
- Use public JSON callback bindings for node LEDs and auxiliary outputs; use manual numbers only in service/diagnostic UI.
- Treat VPX force, angle, animation, and capture values as proven authoring baselines and refine only the physical geometry without changing controller causality.

## Spatial coordinate model

Every physical playfield input, actuator, lamp, and GI socket has a normalized player-view placement: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. The 952 by 2300 Neo table is the sole normalized coordinate frame. Direct Neo object centers are accepted only after reconciliation with the official manual and proven v1.10 script. Geometry absent from Neo is never copied from another normalized table frame: the donor table's switch 18 drain is rejected, its four ball positions 19-22 are locally registered and mapped in order to physical Premium/LE switches 18-21, lamp 51 is registered by the shared upper-right flipper, and Vengeance bulb-mesh points by the shared ship parent. The manual-required jam opto 22 is absent as a direct Neo sensor and receives a disclosed approximate point on the ejection corridor. Slingshot sensors/coils, the Vengeance crash opto, EOS contacts, laser motor, composite multi-bulb assemblies, and GI sockets use explicitly disclosed assembly or drawing projections. Cabinet, service, backbox fixtures, virtual, unpopulated, unused, and DIP devices are outside playfield space.

The lamp audit preserves physical multiplicity that render geometry can both hide and exaggerate. Lamp 51 has two Enterprise emitters but only one defensible composite assembly anchor; lamps 63 and 64 likewise each have two apron emitters represented by one composite Neo assembly center. No false bulb separation is invented. Lamp 57 has two separately recoverable Vengeance nacelle centers. The manual proves one physical lamp for each warp-chaser number 70-77; v1.10's paired beam segments and WarpAmbient object are render helpers, while Neo's direct l70-l77 lamp objects supply one canonical point per output. Cabinet Enterprise and every cabinet phaser output also retain the manual's ×2 physical quantity even though they have no playfield coordinate.

The moving Vengeance is one spatial assembly with separate causality: output 53 supplies PWM dive/shake motion, output 56 controls the latch/return, switch 53 reports the crash/latch state, output 7 returns the captive ball, output 31 flashes the ship, and lamps 56/57 illuminate the saucer and two nacelles. The v1.10 script proves output 31's Vengeance semantics through F31/F31a, while Neo maps that same output to VengFlashGI and supplies the canonical assembly anchor. Their points are canonical-frame, parent-relative rest-state placements; co-located assembly anchors do not collapse them into one device or claim identical internal actuator locations. The broad F31/F31a bloom geometry is a render helper and is not used as output 31's physical position. The left eject and output-55 rotating VUK likewise belong to one scoop but use separate Neo eject-mouth and rotating-pivot points, with no invented position switch.

The page-152 GI drawing proves 34 playfield emitters: 31 sockets plus three illuminated pop-bumper assemblies. Its separate backbox inset proves seven additional physical GI lamps. The aggregate output therefore keeps quantity 41, but only the 34 playfield emitters receive playfield-space placements; the backbox row is not misrepresented at y=0. The 31 drawing-derived socket centers preserve validated identity and physical region, but the drawing does not support a quantified per-socket positional tolerance; their six-decimal projected values are not claims of sub-object measurement precision. The official coil-location drawing places the unsensed laser motor beneath the lower-left apron; its coordinate is a disclosed approximate region rather than a calibrated point, and the broad Laser render fields are effects, not motor locations. The auxiliary drawing proves two Q42 speaker-panel flashers, two Q43 backbox flashers, and one each on Q44-Q46. Those quantities remain in the definition while all seven fixtures stay outside normalized playfield space.

## Sources

- `manual.star-trek-premium-le`: official Stern `Star-Trek-LE-Manual.pdf`, SHA-256 `ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d`; I/O and physical location drawings on PDF pages 68-77, wiring on 114-119 and 153-155, and the physical GI/socket drawing on PDF page 152.
- `vpx-table.star-trek-le-neo-real-1.0.2-geometry`: exact `Star Trek LE Neo real Mod 1.0.2.vpx`, 191,655,936 bytes, SHA-256 `f7edee3cbcebff1a078496b7ef7dcef7368158a61b48934f2241792a70bc233c`; retained externally under `pinmame-vpx-sources/stern/star-trek-premium-limited-edition-2013/source` and used as the sole normalized geometry frame after semantic reconciliation.
- `vpx-table.star-trek-enterprise-le-geometry`: exact `Star Trek Enterprise Limited Edition (Stern 2012).vpx`, 66,732,032 bytes, SHA-256 `46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e`; retained beside the Neo table and used only for missing geometry that is locally registered into the Neo frame by a shared physical anchor.
- `vpx.star-trek-le-1.10`: known-working script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `3337481b28144a67f1df3c3650355be91699104930d8b3cc8503e14225a9d4ff`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, four node boards, custom outputs, display, and driver configuration.
