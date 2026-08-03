# Batman: The Dark Knight Standard/Home Edition (Stern, 2010)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete V3.00 public I/O inventory, physical product differences, retained crane, transport corrections, and recreation behavior validated**

## Identity and evidence precedence

This is the distinct 2010 Standard/Home/Costco product, IPDB 5583, covered only by `bdk_300`. PinMAME makes it a clone of `bdk_294` for software lineage, but its playfield and address map are materially different. Exact V3.00 ROM switch/lamp/coil diagnostics are machine-specific ground truth. The held matrix sweep validates switch addresses, semantics, and unused holes, not contact duration; pulse/sustained behavior is a functional inference from each named device class and the proven Pro analogue where one exists. IPDB photos govern visible product identity. The official Pro manual supplies only shared SAM connector topology and retained crane-board context; it must not add omitted Pro mechanisms. The known-working Pro script is used only as a clearly labeled comparative reference for the retained six-position crane pattern.

## Balls, trough, shooter, and ejects

The Home product has three balls on trough switches 53-55, jam switch 56, and shooter switch 58. Q1 releases the rightmost ball and Q2 auto-launches it. Top-right eject is switch 33/Q3. The Scarecrow VUK is switch 6/Q6 with exit 25. The single Joker lock is switch 27/Q4. These addresses replace the Pro ball path; never initialize or construct a Pro trough at 18-22.

## Retained Scarecrow crane

The Home crane still uses Q31 motor through relay Q28, D16/public 85 for the ball hit, and board LEDs 86-88. Its position sensors are 10 away, 11, 12, 13, 14, and 15 home. This sequence is exact V3.00 ROM evidence and differs from Pro 56-61. D16 lies outside the 1-64 matrix sweep; its Home identity is supported by PinMAME's shared `SAM_GAME_3LEDS_BSTB` configuration, the retained physical crane/IPDB review, the official crane-board manual, and the proven Pro hit-input behavior. Use the Home ROM's crane test to establish direction and tune endpoint windows. The Pro script confirms the retained board's one-direction six-position design only; its 110 ms timing and Pro address ranges are not automatically Home calibration values.

## Simplified playfield and negative knowledge

The Batmobile path is fixed and reports ramp exit 24. Q26 is an orange-fed Batmobile flasher and Q32 the crash flasher; Q13/Q14 are unused, so there is no pivoting bridge or controlled gate. The product has no upper mini-playfield, no Joker reveal motor/relay/position bank, and no active Joker drop target. Q5, Q7, Q12-Q14, Q20, and Q30 are explicitly unused. Build the fixed ramp, three top lanes, both loops, two spinners, VUK, two eject/lock devices, targets, lower lanes, pops, slings, and flippers exactly at the Home addresses rather than removing Pro toys visually while retaining their I/O.

## Lamps and the pinned PinMAME transport correction

The exact ROM Single Lamp Test defines lamps 1-80; only 47, 68, and 73-75 are Not Used. Real lamp 30 is Harvey Dent and real lamp 46 is Crane Position 3. Pinned PinMAME revision `4ec52ff` applies the Pro model's `CORE_MODOUT_NONE` settings to both, suppressing their physical/PWM ChangedLamps callbacks, while unused Home address 47 remains transport-active. A LibPinMAME consumer must restore a non-NONE lamp output type at the same addresses 30 and 46 after `bdk_300` starts and must ignore 47; never remap 30/46 or treat 47 as Crane Position 3. This is a resolved emulator-metadata defect, not a physical ambiguity. The Home ROM also uses crane-board LEDs 86-88 and aggregate GI 0.

## Flippers and game-on state

Flippers are Q15/Q16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed. The pinned PinMAME fast-flip table contains `bdk_294` but no `bdk_300`, and the exact Home boot/start trace produces no synthetic solenoid 33 event. Consume Q15/Q16 directly and do not invent a Q33 transistor. A future verified fast-flip address would be an emulator improvement, not a change to physical machine construction.

## Author construction checklist

- Build the three-ball path, manual/auto shooter, top eject, single Joker lock, Scarecrow VUK, six-position crane, fixed Batmobile ramp, flippers, pops, slings, routes, targets, complete Home lamps/GI, and DMD.
- Initialize trough 53-55 and crane home 15; preserve jam/shooter occupancy, crane positions/hit input, normally-closed EOS state, ball locks, and eject causality.
- Bind every matrix/dedicated/DIP input, Q1-Q32 including all explicit unused holes, unavailable synthetic 33, unused 51-66, lamps 1-88 with the 30/46 output-type correction, GI 0, and the 128x32 DMD.
- Do not add the Pro's Joker reveal/drop, pivoting Batmobile bridge/gate, upper mini-playfield, four-ball trough, or Pro switch/output addresses.

## Sources

- `rom.stern-batman-the-dark-knight-home.bdk-300`: exact V3.00 archive SHA-256 `4d34254e60422503a203206e2a50970a2becdb20941f008da159927ed8292612`, retained under `vpinmame/roms`; ROM bytes remain external.
- `runtime.batman-the-dark-knight-home.switch-diagnostic`: complete held matrix trace SHA-256 `028db927129a01aeb2226081b21c63203b0f6fc547187e7b487113538f16a7d1`.
- `runtime.batman-the-dark-knight-home.lamp-diagnostic`: exact lamp selector trace SHA-256 `cb5eedfa59f79658cd91f68104c8062dd329cbe9cc582d504b822c16584f50f6`.
- `runtime.batman-the-dark-knight-home.coil-diagnostic`: exact Q selector trace SHA-256 `fb2850475661a0e3470e7dbeb2d5d1ff852db86e421a625204fa1b0640a4c52e`.
- `runtime.batman-the-dark-knight-home.boot-start`: corrected three-ball boot/start trace SHA-256 `1e53a038cdf49bfea8524d938a56560dc36eba03d6ef45c3d18e75629d675029`.
