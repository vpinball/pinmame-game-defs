# The Avengers Limited Edition (Stern, 2012)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete Limited Edition I/O, wiring, mechanisms, lighting, initial state, and controller bindings validated; spatial evidence is partial**

## Identity and evidence precedence

This definition covers `avs_120h`, `avs_140h`, `avs_170h`, and `avs_170hc`. The `h` family is the physical Limited Edition; the colored `hc` ROM does not change hardware. The known-working JP Salas LE script is ground truth for PinMAME addresses, callbacks, initial state, ball routing, and mechanism causality. The official Stern LE manual governs physical inventory, service numbers, coil specifications, wiring, assembly construction, and location maps. The isolated exact-ROM run validates the native 128x32 four-bit DMD, public GI 0, conventional lamp callback range, and runtime availability without redistributing ROM content.

## Six-ball trough and launcher

The LE has six balls on trough switches 17-22 and jam switch 23. Initialize all six position switches active and jam clear; output 1 ejects from the right end and the table pulses jam during transfer. The shooter lane is dedicated D15/public switch 86, not matrix 23. Output 2 auto-launches with a proven 0.6-second impulse, power 62, and 0.3 randomness.

## Two drop banks

The left THOR bank uses maintained drop switches 1-4 and main output 6 resets it. The center HULK bank uses switches 52-55 and the LE auxiliary board: PinMAME public output 51 is physical driver 41. Do not reuse the Pro mapping, where main output 6 resets only the center HULK bank and THOR is passive.

## Hulk assembly

Outputs 3/4 rotate Hulk counterclockwise/clockwise and optos 41/42 report wheel position. Public auxiliary 56, physical driver 46, lifts the arms; the proven animation spans roughly 130-200 degrees. Switch 57 detects a ball on the platter and public auxiliary 54/physical 44 energizes the radius-16 magnet without forcing the ball to center. Switch 62 holds a ball at the Hulk eject until main output 5 kicks it at the proven angle 25 and force 16. Switch 63 is the separate Hulk standup target.

## Loki lock

The three lock optos 49-51 are active-low: initialize them high when empty and drive them low as balls occupy bottom, middle, and top positions. Main output 12 drops the retaining post and releases the visible three-ball lock. Preserve the lock as physical ball storage; it is not a simulated bookkeeping-only lock.

## Bridge, gates, and Tesseract

The bridge uses motor output 22, direction/state relay 23, down switch 8, and up switch 9. The proven table treats relay 23 active as down and inactive as up; add limit cutoff at both sensors. Main output 7 opens the left orbit, public auxiliary 57/physical 47 opens the right orbit, and public auxiliary 52/53 (physical 42/43) actuate the right/left ramp gates. The Tesseract is an inertial playfield spinner, not a ROM-driven motor: the ball imparts angular velocity, optos 45/46 pulse at opposed positions, and drag gradually stops it.

## Lighting and standard devices

The conventional 1-80 lamp matrix is fully enumerated, including unused 13, 69-71, and 79. GI is public address 0. The LE additionally uses three physical color relays: main 17 is blue, auxiliary 55/physical 45 is green, and auxiliary 58/physical 48 is red. These switch the 112-5033 RGB GI LED rails shown on the manual location map and must remain distinct even if a renderer also offers combined brightness. Three pops are switches 30-32/outputs 9-11, slings are 26/27 and 13/14, and lower flippers are outputs 15/16 with dedicated buttons and normally-closed EOS contacts.

## Spatial evidence pass

Coordinates use normalized playfield space: x=0 is left and x=1 is right; y=0 is rear/backglass and y=1 is the apron. The promoted subset is observed against the official LE switch, lamp, coil, and RGB-GI maps on manual pages 63, 64, 66, 68, and 117. Assembly anchors are explicitly labeled when the manual groups paired optos or a multi-device mechanism. No coordinate in this LE definition is sourced from a Pro VPX table.

The organized local VPX candidate `Avengers (Stern 2012)-WIP HD neo Hulk rascalV2.vpx` is retained as a review artifact but rejected for LE spatial use: its script identifies ROM `avs_170`, which is Pro-family evidence. The LE evidence itself has an unresolved upper-right-orbit address: the manual's physical location drawing marks the disputed coordinate 61, its switch matrix grid says 58, and the known-working LE script drives `sw58` without a `sw61` handler. Neither input receives that coordinate, and 61 is not classified as unused. The same fail-closed rule applies to LE bridge, auxiliary-board, lock-lamp, Tesseract-lamp, and any relocated geometry.

Controlled N/A assertions cover DIP switches, unused devices, cabinet/service controls, rear-panel flashers, internal GI/bridge relays, the optional shaker and coin meter, and the virtual game-on output. Remaining physical devices intentionally have no spatial assertion until their individual LE geometry is reconciled: bridge endpoints 8/9, trough contacts 17-23, shooter switch 86, unlocated coils/auxiliary effects, the used lamp matrix, RGB-GI per-emitter locations and multiplicity, and the DMD display field (schema v2 has no display spatial-placement member). This keeps the machine schema-v2 partial and identifies the exact authoring blockers instead of inventing placements.

## Recreation checklist

- Build the six-ball trough, dedicated-switch shooter lane, two resettable four-target banks, three-ball active-low Loki lock, motorized sensed bridge, full Hulk motor/arms/magnet/eject assembly, four controlled gates, and passive inertial Tesseract.
- Bind the auxiliary board by public PinMAME addresses 51-58 while retaining physical diagnostic numbers 41-48 for service UI and wiring.
- Preserve sustained/PWM behavior for motors, magnet, relay, and flipper drives; do not turn every output into a fixed pulse.
- Implement every explicit unused switch and lamp address so omissions are distinguishable from unknown data.
- Use the script force, angle, timing, and rotation values as proven authoring baselines, then align geometry to the manual assembly drawings without changing controller causality.

## Sources

- `manual.avengers-limited-edition`: official Stern `Avengers-LE-Manual-compressed.pdf`, SHA-256 `4687ae0ed0ac249411deff3b0284d5c13d8fab154e430e95b6bd9f7bb82dca62`; I/O charts on PDF pages 63-69, auxiliary board on 108, RGB GI map on 117, and assembly drawings throughout.
- `vpx.avengers-le.jp-salas-v600`: known-working JP Salas LE script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `c6da231a360a0f062fa5b434d08faca3c1b7b6a5436cc51b5b54dac924e1a3b4`.
- `runtime.avengers-le.boot-start`: isolated exact `avs_170h.zip` run, raw SHA-256 `3fdb8e048c0c8ff130163333e508953b6ec3bfb0670931af9cbddc957c011bd3`; ROM archive SHA-256 `a5ea0eafcc45671ce66b29336c81f875f49515235034520f53e3042dfdefc74d` remains external.
