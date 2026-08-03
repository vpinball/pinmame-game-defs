# Star Trek Premium / Limited Edition (Stern, 2013)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `st_*h` and `st_*hc` drivers. Those revisions share the Premium/LE playfield; `c` only changes ROM display colorization. Non-`h` drivers are the different Pro machine and have their own definition. The known-working `Star Trek LE (Stern 2013) v1.10.vbs` is ground truth for controller bindings, callbacks, initial state, mechanism causality, and active behavior. The official Stern manual governs physical inventory, wiring, diagnostic numbering, and assemblies. Pinned PinMAME source governs the SAM transport, display, custom-solenoid serialization, node-board topology, and driver identity.

## Controller topology

The four node boards expose public lamp ranges 81-144, 146-209, 211-274, and 276-339. Public addresses 145, 210, and 275 are deliberate compatibility gaps, not lamps. The JSON enumerates every addressable lamp channel and marks unused channels explicitly. Main solenoids are 1-32. The auxiliary board exposes Q51-Q56 as public 51-56 and physical Q41-Q46 as public 59-64; 57-58 and 65-66 are explicit unused holes.

## Switches and initial ball state

All matrix positions 1-64, dedicated D1-D24, and DIP inputs are enumerated. The physical four-ball trough has left-to-right sensors 18-21 plus jam opto 22. The working script initializes four balls on 19-22, leaving 18 clear. Shooter lane is 23. Fire is public 71/D7; the upper-right flipper button is public 86/D15. Lower buttons are 84 left and 82 right, with normally-closed EOS contacts 83 left and 81 right.

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
- Initialize four trough balls exactly as the working script does: 19-22 active and 18 clear.
- Preserve PWM for the center magnet and Vengeance actuator; do not reduce either to a simple pulse.
- Model the memory target, multi-ball magnet hold, rotating VUK route, Vengeance latch/crash/return sequence, orbit gates, bottom kickback, laser motor, upper flipper, and all sensed ball paths.
- Use public JSON callback bindings for node LEDs and auxiliary outputs; use manual numbers only in service/diagnostic UI.
- Treat VPX force, angle, animation, and capture values as proven authoring baselines and refine only the physical geometry without changing controller causality.

## Sources

- `manual.star-trek-premium-le`: official Stern `Star-Trek-LE-Manual.pdf`, SHA-256 `ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d`; I/O and wiring tables on PDF pages 68-77, 114-119, and 153-155.
- `vpx.star-trek-le-1.10`: known-working script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `3337481b28144a67f1df3c3650355be91699104930d8b3cc8503e14225a9d4ff`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, four node boards, custom outputs, display, and driver configuration.
