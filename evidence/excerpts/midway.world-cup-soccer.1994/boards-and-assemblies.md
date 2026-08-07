# World Cup Soccer — Board and assembly pages fixing device construction

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF pages 78, 80, 81 (printed 2-12, 2-14, 2-15) and
PDF page 108 (printed 2-42, Lower Playfield Parts, relevant opto/motor items only).

## A-17316 — Flipper Opto PCB Assembly (PDF page 78, printed 2-12)

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | 03-9001 | Interrupter Flip-Opto |
| 2 | A-16384 | Flipper Opto Switch Assembly |
| — | 5010-08930-00 | Resistor, 470Ω, 1/2w, 5% |
| — | 5490-12451-00 | Opto Inter Lg. 10mA |
| — | 5791-12462-07 | Connector, 7-pin Header |

This is genuine opto-interrupter construction (an LED/phototransistor pair, "Opto Inter Lg. 10mA"),
confirming the switch-matrix page's "Right/Left Flipper Opto" shading at public 112/114 — see
`switch-matrix.md`.

## A-18159 — 10-Switch Opto Assembly (PDF page 78, printed 2-12)

Board with connectors J1 (9-pin), J2 (9-pin), and J3 (12-pin), three LM339 quad comparators
(U1-U3), and up to 21 channel resistors (R1-R21). The board's own item name states 10-switch
capacity; pinned PinMAME's `wcsGameData` inverted-switch mask normalizes exactly 8 addresses
(41-45, 51-53) from this board's channels — see `switch-matrix.md`. Two of the board's ten physical
channels are not consumed by this ROM revision; no address is asserted for them.

## A-16120 — DC Motor Control Assembly (PDF page 80, printed 2-14)

H-bridge motor driver board: `U4` a 3A D.O.S. Bridge Driver IC, `U1`/`U2` 4N25 opto isolators (input
isolation from the CPU-side signal, not a playfield switch), `U3` a 74LS32 quad OR gate, plus
supporting inductors (`L1`/`L2`, 4.7 mH) and a `7805` 5V regulator (`Q1`). This is the board that
drives the spinning soccer ball turntable motor via public solenoids 23 (clockwise) and 24
(counter-clockwise) — see `wcs.c`'s `wcs_ballMech` (`MECH_TWODIRSOL`) and the retained script's
`SolBallMotorCW`/`SolBallMotorCCW` handlers. It is item 12 ("A-17569 Motor Assembly") + item 21
("A-16120 D.C. Motor Control Assy.") on the Lower Playfield Parts page below.

## A-15576 — 7-Switch Opto PCB Assembly (PDF page 81, printed 2-15)

Board with two 10-pin headers (J1, J2) and one 12-pin header (J3), two LM339 quad comparators
(U1, U2), seven channel resistors (R15-R21) plus fourteen input-side resistors (R1-R14), and nine
diodes (D1-D9). This is the trough opto board referenced on the Lower Playfield Parts page as item
31 ("A-15576 ?-Switch Opto Board", OCR-garbled but confirmed `7-Switch` from this page's own title)
and cross-referenced elsewhere in the manual as the source of the "7 Opto Trough Cable" (`H-18757`
input, `H-18758` output). Pinned PinMAME's `wcsGameData` inverted-switch mask normalizes six
addresses from this board's channels (31-36, matrix column 3); the board's own title states seven
physical channels, so one channel is not consumed as a distinct public switch address by this ROM
revision — the same one-spare-channel pattern documented for the 10-Switch Opto Assembly above.

## Lower Playfield Parts (PDF page 108, printed 2-42) — relevant items only

| Item | Part No. | Description |
| --- | --- | --- |
| 4 | A-15849-R-2 | Flipper Assembly, Right |
| 9 | B-9361-R-5 (x2) | Ball Eject Assy., Right |
| 10 | A-18213 | Ball Popper Assembly |
| 12 | A-17569 | Motor Assembly |
| 13 | A-17749.1-2 | Plfd. Slide Mech. Assy., R. |
| 14 | A-9415-2 (x3) | Jet Bumper Coil Assy. |
| 15 | A-17796 | Ball Gate Actuator Assy. |
| 17 | A-18138 | Diverter Assembly |
| 18 | A-17749.1-1 | Plfd. Slide Mech. Assy., L. |
| 19 | A-17908 | Ball Eject Assembly |
| 20 | A-15542 | Motor EMI PCB Assy. |
| 21 | A-16120 | D.C. Motor Control Assy. |
| 22 | A-18155 | Up/Down Post Unit Assy. |
| 25 | A-15849-L-2 | Flipper Assembly, Left |
| 26 | A-17839 | Goalie Ball Popper Assy. |
| 27 | A-17741 | Goalie Unit Assembly |
| 31 | A-15576 | 7-Switch Opto PCB (OCR-garbled leading digit on the plain-text layer; confirmed from page 81's own title) |
| 32 | A-15257 | Bracket & Pole Piece |
| 33 | A-18159 | 10-Switch Opto PCB |

Item 27 (A-17741 Goalie Unit Assembly) and item 26 (A-17839 Goalie Ball Popper Assy.) are the
motorized goalie mechanism; item 22 (A-18155 Up/Down Post Unit Assy.) is the lock-release post
(public solenoid 4); item 17 (A-18138 Diverter Assembly) is the ramp diverter (public solenoids 8
and 16); item 15 (A-17796 Ball Gate Actuator Assy.) is the "Loop Gate"/"Lock Gate" solenoid 34 (see
`solenoid-flasher-locations.md` for the two printed names of the same device); item 12 + item 21
(A-17569 Motor Assembly + A-16120 D.C. Motor Control Assy.) are the spinning-ball turntable motor
and its H-bridge driver board.
