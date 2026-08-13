# No Good Gofers (Williams, 1997) spatial review

Status: validated. The machine is deliberately partial: spatial_placement remains a fail-closed blocker.

The retained known-working VPX table is SHA-256 `9f5b44285e3a10155fb0bf33a84626df45cc305f193d15963e39228355b91e59`; its extracted script is `fbb6914941bd542f38e1ae9c15a6147b552cd33a22f586c85c3139da08aee766`. Exact table bounds are `left=0 top=0 right=964 bottom=2162`. Every located point is a named retained object center normalized as x/964, y/2162 (left/rear origin convention).

## Spatial decision

- Several physical switches and outputs have no one-to-one retained VPX playfield object (notably the individual six-trough optos, mechanical ramp-down sensors, several gofer hit switches, both wheel optos, slingshot coils, ramp-drop coils, both wheel motor directions, and upper-playfield flasher pairs). They intentionally omit spatial coordinates rather than reusing a mechanism anchor or a presentation proxy.
- Five two-bulb devices have only one directly bound retained-VPX emitter: lamp addresses 13, 28, and 68 plus solenoid/flashers 20 and 25. Their single retained placement is observed rather than complete, and each missing second bulb remains explicit.
- GI 0-2 are real playfield circuits in the manual, but the known-working VPX script sets UseGI=0 and its GI collections are presentation proxies with no manual-calibrated bulb-to-coordinate correspondence. They intentionally receive no fabricated playfield placement.

- Located placements: 143
- Inputs with direct retained coordinates: 43
- Inputs intentionally unresolved: [31, 32, 33, 34, 35, 36, 37, 41, 42, 47, 48, 63, 64, 66, 76]
- Outputs intentionally unresolved: [('pinmame.output.gi', 0), ('pinmame.output.gi', 1), ('pinmame.output.gi', 2), ('pinmame.output.solenoid', 10), ('pinmame.output.solenoid', 11), ('pinmame.output.solenoid', 27), ('pinmame.output.solenoid', 28), ('pinmame.output.solenoid', 37), ('pinmame.output.solenoid', 38), ('pinmame.output.solenoid', 54), ('pinmame.output.solenoid', 55)]
- Outputs with incomplete physical-quantity placement: [('pinmame.output.lamp', 13, 1, 2), ('pinmame.output.lamp', 28, 1, 2), ('pinmame.output.lamp', 68, 1, 2), ('pinmame.output.solenoid', 20, 1, 2), ('pinmame.output.solenoid', 25, 1, 2)]

## Extraction identity

- 927 files, 127738302 bytes; canonical manifest SHA-256 `caf93fabeb7b697f65f3314425286a1f8fa96a37811b51f1abc357eb176ead66`.

## Promotion decision

The definition must not be promoted. It records every coordinate that has a direct named retained-VPX binding and leaves the rest absent instead of converting manual drawing callouts, mechanism anchors, or VPX presentation proxies into invented physical coordinates.
