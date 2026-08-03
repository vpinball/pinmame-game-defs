# Batman: The Dark Knight Pro (Stern, 2008)

Coverage: **author-ready - complete public I/O inventory, factory wiring and lamp parts, custom mechanisms, firmware family, and recreation behavior validated**

## Identity and evidence precedence

This is the 2008 commercial machine, IPDB 5307, called the Pro model in current Stern/PinMAME terminology. It covers `bdk_130`, `bdk_150`, `bdk_160`, `bdk_200`, `bdk_210`, `bdk_220`, `bdk_240`, `bdk_290`, and `bdk_294`. The known-working exact `bdk_294` VPX script is controller-semantic and causal ground truth; the official manual governs physical construction, wiring, bulb/board types, and service assemblies; pinned PinMAME governs transport, display, and driver identity. The firmware readme documents software-only changes to Scarecrow multiball, Batmobile-ramp handling, crane adjustment/calibration, and Joker motor behavior.

## Balls, trough, shooter, and ejects

Four balls rest on trough switches 18-21. Q1 feeds the rightmost ball through jam opto 22 to shooter switch 23, where it can be plunged manually or fired by Q2. Top-right switch 44/Q3 and Scarecrow VUK switch 12/Q6/exit 42 are separate eject paths. Joker lock switch 46 retains a ball until Q4 fires. Preserve sustained occupancy and explicit physical release transactions rather than pulsing every ball-position switch.

## Joker reveal, target, and lock

The Joker area contains three distinct mechanisms. The lockup is switch 46/Q4. The active drop target is switch 45 with Q5 up and Q7 down. The rotating reveal uses motor Q26 through relay Q30 with three positions: 52 away/revealed, 51 middle, and 50 home/hidden. The proven script models a 1500 ms, 360-step one-direction cycle with windows 52 at 0, 51 at 178-182, and 50 at 359. Use the ROM Joker Motor Test to calibrate the physical assembly, retain mutually exclusive position contacts, and never merge its motor, drop, and ball lock into one animation.

## Scarecrow crane

The chain-driven crane uses Q31 motor through relay Q28. Position optos run 56 away, 57, 58, 59, 60, and 61 home; D16/public 85 is the ball-hit leaf. The proven table models 90 steps over 110 ms with windows 56=0-1, 57=30-33, 58=47-50, 59=59-62, 60=71-74, and 61=89. PinMAME exposes the board LEDs at lamps 86-88. The official manual documents two factory crane variants with different hub and motor-shaft shapes. Identify the actual variant before selecting parts, never rotate it by hand, and use the ROM test for direction, endpoint, and adjustment.

## Batmobile bridge and upper mini-playfield

Q13 pivots the Batmobile bridge between an approximately 10-degree raised return path and its lowered release path, while Q14 controls the gate. Switch 64 captures a real ball on the moving ramp. Lowering the bridge releases that ball and drives the linked Batmobile crash path through switch 47; move collision geometry and the captured ball throughout travel. The proven script uses an invisible helper ball only to animate the Batmobile and pulse the crash transaction, so do not add it to the physical ball count. The upper mini-playfield is a separate elevated area with contacts 53 top-left, 54 top-right, 55 bottom-left, and 63 bottom-right.

## Standard devices, routes, lamps, and display

Flippers are Q15/Q16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed. Pops are Q9/SW30, Q10/SW31, Q11/SW32 and slings are Q17/SW26, Q18/SW27. Q12 controls the left gate and Q8 is an optional shaker. Every lane, standup, spinner, loop, ramp, and target is enumerated in JSON with the manual's assembly part and the working script's pulse/sustained behavior. Lamps 1-80 follow the official grid exactly; only 30 and 46 are unused. Original #555, #44, green, and white-LED parts are preserved, ordinary GI is aggregate 0, crane-board LEDs are 86-88, and the display is native 128x32 four-bit DMD. Public solenoid 33 is synthetic fast-flip/game-on, while 51-66 are unused compatibility capacity.

## Author construction checklist

- Build the four-ball path, manual/auto shooter, both ejects, Joker lock/drop/reveal, six-position crane, moving Batmobile bridge/gate/crash transaction, upper mini-playfield, flippers, pops, slings, left gate, shaker option, routes, targets, complete lamps/GI, and DMD.
- Initialize trough 18-21, Joker home 50, and crane home 61; preserve normally-closed EOS contacts, ball occupancy, position windows, moving collision, drop latching, gate direction, and physical release causality.
- Bind matrix 1-64, dedicated/DIP inputs, Q1-Q32, synthetic 33, unused 51-66, lamps 1-88, GI 0, and the DMD. Never infer Home hardware from the bdk_300 clone edge.

## Sources

- `manual.stern-batman-the-dark-knight.2008`: official 207-page manual SHA-256 `c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219`, organized under the external manual cache with native-text extraction and rendered grid review.
- `vpx.batman-the-dark-knight-pro-1.16`: exact working script SHA-256 `1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0`.
- `rom.stern-batman-the-dark-knight.bdk-294`: exact archive SHA-256 `b82a4b996c6561b273a7eda6bcf2a540cb67b3b8947bf439b8e9a8928ace3f49`; ROM bytes remain external.
- `runtime.batman-the-dark-knight-pro.boot-start`: exact boot/start trace SHA-256 `e54ff7c90c52a3305e10961f5e5833a20506e04f373b58d955f47a40b8780bb4`.
