# WHO dunnit spatial blockers

Retained VPX SHA-256 `a0f18c07f98ec7dce96cc030eb11af11a0c28d0d1cffb5390744067b9221e2a9`; script `034fe6483660fbc9516aa15a4727d8dc6da0cfb3db0321b0c1357523967ccd44`; 631-file extraction manifest `0fd20d012d8219583a8222b51a0997ca4876247cc9ec19352e5a06d270d3643c`; manual `5fa08344d905c9730c86c6baee79b43e6a4a1c4e2230f67a08c2973b57bc714e`.

Bounds: `left=0 top=0 right=953 bottom=2128`. x=object_x/953; y=object_y/2128; player view, rear y=0, apron y=1; values rounded to six decimals.

95 devices have exact-name VPX object candidates; 46 used devices have no placement. No candidate is promoted to a physical socket without reconciling the manual location drawing. Flasher sprites, shared backbox bulbs, G.I. strings, reels and the under-playfield mechanisms need separate anchors.

## Retained registers and projection classes

The [VPX object register](../../../tools/seeds/bally/who-dunnit-1995-spatial.json) has SHA-256 `e6c9f386a0e7b420893cd4736b89236ef3e25c68b36067ca4b743508588bd885`; the [G.I. bulb-mesh register](../../../tools/seeds/bally/who-dunnit-1995-gi-candidates.json) has SHA-256 `feb5185273d8f36596e75ec7753a4ff1a1d962a001005593c8b14bc38ae999d1`. The JSON form of this report embeds each named object, file and normalized point.

- **switch (32 candidate devices):** Exact-name VPX collision object centre for matrix switch or F5 Spinner, candidate only; cabinet, EOS and always-closed positions use controlled not_applicable.
- **lamp (60 candidate devices):** Exact LNN VPX Light centre, candidate only. L16/L17/L18 glow helpers are excluded; the factory location drawing on PDF 125 still needs device-by-device socket reconciliation.
- **gi (3 candidate devices):** Script collection members GI_Left/GI_Right/GI_Top with bulb mesh; 11/10/28 retained. Other collection members are glow/reflection leads, not sockets. Factory GI socket quantity is unknown.
- **flasher_and_coil (0 candidate devices):** No Flasher sprite, mesh offset or target glow is accepted as a physical load centre; factory callout and exact-table lens/mesh reconciliation remain pending.
- **manual_drawing (0 candidate devices):** PDF 125 printed 2-43 provides numbered lamp callouts, but has not been metrically fitted to the VPX table frame. No callout balloon is used as a coordinate.

## Missing placements

- `switch.matrix-11`
- `switch.matrix-12`
- `switch.matrix-25`
- `switch.matrix-31`
- `switch.matrix-32`
- `switch.matrix-33`
- `switch.matrix-34`
- `switch.matrix-35`
- `switch.matrix-48`
- `switch.matrix-61`
- `switch.matrix-62`
- `switch.matrix-66`
- `switch.matrix-67`
- `switch.matrix-68`
- `switch.matrix-73`
- `switch.matrix-74`
- `solenoid.01`
- `solenoid.02`
- `solenoid.03`
- `solenoid.04`
- `solenoid.05`
- `solenoid.08`
- `solenoid.09`
- `solenoid.10`
- `solenoid.11`
- `solenoid.12`
- `solenoid.13`
- `solenoid.14`
- `solenoid.16`
- `solenoid.17`
- `solenoid.18`
- `solenoid.19`
- `solenoid.20`
- `solenoid.21`
- `solenoid.22`
- `solenoid.23`
- `solenoid.24`
- `solenoid.25`
- `solenoid.26`
- `solenoid.27`
- `solenoid.28`
- `solenoid.36`
- `solenoid.45`
- `solenoid.46`
- `solenoid.47`
- `solenoid.48`
