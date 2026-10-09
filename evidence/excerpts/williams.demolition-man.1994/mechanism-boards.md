# Demolition Man — Mechanism and Interface Boards

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF pages 119 to 131
(printed pages `DEMOLITION MAN 3-15` to `3-27`), the schematics, assembly drawings and connector-wiring lists of
the opto, motor, driver and interface boards. Read from the rendered pages (308 dpi 1-bit scan), not from the OCR
text. Every connector pin line is transcribed literally (spelling, capitalisation, `sw.`, `N/C`); blank cells in a
table are printed blank. Reading a schematic by tracing wires is marked `Traced` below and is not a printed
statement; printed text is quoted. The image beside this file shows the Cryoclaw opto / D.C. motor page (PDF page 124); the 7-opto board
page (PDF page 122) and the 8-driver page (PDF page 128) are transcribed from their own renders.

Switch numbers in this manual are column then row (`#71` is column 7, row 1); this is confirmed by the printed pairs
on the 7-opto board (`switch #71` on a `White-Brown (switch row 1)` / `Green-Violet (switch column 7)` matrix).

| Board | Assembly | PDF pages | Printed pages |
| --- | --- | --- | --- |
| LED PCB (green) and Photo Transistor PCB (blue) | A-16908 / A-16909 | 119 | 3-15 |
| 7 Ball Trough Photo Transistor PCB | A-17981 | 120, 121 | 3-16, 3-17 |
| 7 Ball Trough LED PCB | A-17982 | 121 | 3-17 |
| 7-Opto Switch Board | A-15576 | 122, 123 | 3-18, 3-19 |
| Cryoclaw Opto PCB | A-16986 | 124 | 3-20 |
| D.C. Motor Control | A-16120 | 125 | 3-21 |
| Elevator Opto PCB | A-17596 | 126 | 3-22 |
| Motor EMI PCB | A-15542 | 127 | 3-23 |
| 8-Driver (Aux. Driver) PCB | A-16100-2 | 128, 129 | 3-24, 3-25 |
| Coin Door Interface PCB | A-17051-1 | 130, 131 | 3-26, 3-27 |

## A-16908 LED PCB Assembly (green board) and A-16909 Photo Transistor PCB Assembly (blue board) (PDF page 119, printed 3-15)

- `A-16908 LED PCB Assembly (green board)`: drawings `solder side` (pads `A` and `K`), `component side` (`K` `A`) and
  `schematic` (LED, `A` `K`).
- `A-16909 Photo Transistor PCB Assembly (blue board)`: `solder side` (`C` and `E`), `component side` (`E` `C`) and
  `schematic` (phototransistor, `C` `E`).
- `Typical Circuit Schematic`: `LED Board Transmitter` `1.0 - 1.4 volts` with the wires `Gray-XXX` and `Black,
  ground`; `Photo Transistor Board Receiver` `0.1 - 0.7 volts unblocked` `11 - 13 volts blocked` with the wires
  `Gray-Yellow, +12V` and `Orange-XXX`.
- `Typical Circuit Diagram`: the same two boards face each other across an `INFRARED BEAM`; the LED board is
  labelled `GREEN` (top), `WHITE` (side), wires `GRAY` and `BLACK`; the receiver is labelled `BLACK` (side), `BLUE`
  (top), wires `GRAY - YELLOW` and `ORANGE`. Voltages as above.

## A-17981 7 Ball Trough Photo Transistor PCB Assembly (PDF pages 120 and 121, printed 3-16 and 3-17)

Schematic (PDF page 120) with seven phototransistors `Q1` to `Q7` (labelled `OPTO 1` to `OPTO 7`), comparators
`U2D`, `U2C`, `U2B`, `U1B`, `U1A`, `U1D`, `U1C` (all `LM339`), one more `LM339` section `U2A` and diodes `D1`-`D9`,
and connector `J1` (12 pins). The schematic labels `J1` pins: `12 +12V`, `11 +12V`, `10 GND`, `9 Key`, `3 R1`,
`2 R2`, `4 R3`, `7 R4`, `8 R5`, `6 R6`, `5 R7`, `1 Col.`

`7 Ball Trough Photo Transistor PCB Assembly Connector Wiring` (PDF page 121):

| Pin | Printed text |
| --- | --- |
| J1-1 | Green-Orange, sw. col. 3 from CPU Board J207-3 |
| J1-2 | White-Green, sw. row 5 from CPU Board J209-5 |
| J1-3 | N/C |
| J1-4 | White-Yellow, sw. row 4 from CPU Board J209-4 |
| J1-5 | White-Blue, sw. row 6 from CPU Board J209-7 |
| J1-6 | White-Brown, sw. row 1 from CPU Board J209-1 |
| J1-7 | White-Orange, sw. row 3 from CPU Board J209-3 |
| J1-8 | White-Red, sw. row 2 from CPU Board J209-2 |
| J1-9 | Key |
| J1-10 | Black, ground from Power Driver Board J118-3 |
| J1-11 | N/C |
| J1-12 | Gray-Yellow, +12V from Power Driver Board J118-2 |

`Traced` from the schematic (PDF page 120), opto to comparator to `J1` pin (the comparator and diode pairings are read from wire routing in a dense drawing and are the least certain part of this table; the `J1` pin labels and the wiring list are printed text); the page prints no switch numbers for
this board. Each phototransistor's `OPTO n` line feeds a resistor divider, one `LM339` section and a diode to the
`J1` pin named `Rn`; the pin-to-matrix-row assignment is the printed wiring list above:

| Opto (phototransistor) | Comparator and diode | Schematic J1 pin label | J1 pin | Printed wiring list for that pin | Column/row |
| --- | --- | --- | --- | --- | --- |
| OPTO 1 (Q1) | U2D, D7 | R1 | 3 | N/C | none wired |
| OPTO 2 (Q2) | U2C, D8 | R2 | 2 | White-Green, sw. row 5 | col. 3 row 5 |
| OPTO 3 (Q3) | U2B, D6 | R3 | 4 | White-Yellow, sw. row 4 | col. 3 row 4 |
| OPTO 4 (Q4) | U1B, D3 | R4 | 7 | White-Orange, sw. row 3 | col. 3 row 3 |
| OPTO 5 (Q5) | U1A, D2 | R5 | 8 | White-Red, sw. row 2 | col. 3 row 2 |
| OPTO 6 (Q6) | U1D, D4 | R6 | 6 | White-Brown, sw. row 1 | col. 3 row 1 |
| OPTO 7 (Q7) | U1C, D5 | R7 | 5 | White-Blue, sw. row 6 | col. 3 row 6 |

The board's `Col.` is `J1` pin 1 (`Green-Orange, sw. col. 3`). OPTO 1 lands on an `N/C` pin on this list.

## A-17982 7 Ball Trough LED PCB Assembly (PDF page 121, printed 3-17)

Schematic: eight LEDs `LED 1` to `LED 8` in parallel (`R1` to `R7` `270`, `R8` `1.2K` on `LED 8`) between the `+12`
pins and `GND`. Schematic `J1` pin labels: `1 +12`, `2 +12`, `3 GND`, `4 KEY`, `5 GND`.

`7 Ball Trough LED PCB Assembly Connector Wiring`:

| Pin | Printed text |
| --- | --- |
| J1-1 | N/C |
| J1-2 | Gray-Yellow, +12V from Power Driver Board J118-2 |
| J1-3 | N/C |
| J1-4 | Key |
| J1-5 | Black, ground from Power Driver Board J118-3 |

## A-15576 7-Opto Switch Board Assembly (PDF pages 122 and 123, printed 3-18 and 3-19)

Connector wiring lists (PDF page 122, as printed):

| Pin | Printed text |
| --- | --- |
| J1 - 1 | N/C |
| J1 - 2 | Gray-Blue (switch #76) to Bottom Popper Opto LED Brd. |
| J1 - 3 | N/C |
| J1 - 4 | Key |
| J1 - 5 | Gray-Black (switch #74) to Elevator Hold Opto LED Brd. |
| J1 - 6 | Gray-Orange (switch #73) to Top Popper Opto LED Brd |
| J1 - 7 | Gray-Red (switch #72) to Chase Car 2 Opto LED Brd. |
| J1 - 8 | Gray-Brown (switch #71) to Chase Car 1 Opto LED Brd. |
| J1 - 9 | N/C |
| J1 - 10 | Black (ground) to Opto LED Brds. |
| J2 - 1 | N/C |
| J2 - 2 | Orange-Blue (switch #76) to Bottom Popper Photo Trans Brd. |
| J2 - 3 | N/C |
| J2 - 4 | Orange-Yellow (switch #74) to Elevator Hold Photo Trans Brd. |
| J2 - 5 | Orange-Black (switch #73) to Top Popper Photo Trans Brd. |
| J2 - 6 | Orange-Red (switch #72) to Chase Car 2 Photo Trans Brd. |
| J2 - 7 | Orange-Brown (switch #71) to Chase Car 1 Photo Trans Brd. |
| J2 - 8 | Key |
| J2 - 9 | N/C |
| J2 - 10 | Gray-Yellow (+12V) to Photo Trans Brds. |
| J3 - 1 | Gray-Yellow (+12V) from Power Driver Board J118-2 |
| J3 - 2 | N/C |
| J3 - 3 | Black (ground) from Power Driver Board J118-3 |
| J3 - 4 | Key |
| J3 - 5 | White-Brown (switch row 1) from CPU J209-1 |
| J3 - 6 | White-Red (switch row 2) from CPU J209-2 |
| J3 - 7 | White-Orange (switch row 3) from CPU J209-3 |
| J3 - 8 | White-Yellow (switch row 4) from CPU J209-4 |
| J3 - 9 | N/C |
| J3 - 10 | White-Blue (switch row 6) from CPU J209-7 |
| J3 - 11 | N/C |
| J3 - 12 | Green-Violet (switch column 7) from CPU J207-7 |

Wiring diagram at the bottom of PDF page 122 (labels as printed, upper-case): `7-OPTO BOARD` with `J1` pins `2`,
`5`, `6`, `7`, `8`, `10` to `GRY-BLU, SW. 76 BOTTOM POPPER`, `GRY-BLK, SW. 74 ELEVATOR HOLD`, `GRY-ORG, SW. 73 TOP
POPPER`, `GRY-RED, SW. 72 CHASE CAR 2`, `GRY-BRN, SW. 71 CHASE CAR 1`, `BLK, GROUND`, followed by an LED symbol marked
`REPEATED 5 TIMES`; `J2` pins `2`, `4`, `5`, `6`, `7`, `10` to `ORG-BLU, SW. 76 BOTTOM POPPER`, `ORG-YEL, SW. 74
ELEVATOR HOLD`, `ORG-BLK, SW. 73 TOP POPPER`, `ORG-RED, SW. 72 CHASE CAR 2`, `ORG-BRN, SW. 71 CHASE CAR 1`, `GRY-YEL,
+12V`, followed by a phototransistor symbol marked `REPEATED 5 TIMES`; `J3` pins `12`, `10`, `8`, `7`, `6`, `5`, `3`,
`1` to `GRN-VIO, SW. COL. 7` (CPU `J207` pin 7), `WHT-BLU, SW. ROW 6` (CPU `J209` pin 7), `WHT-YEL, SW. ROW 4`
(`J209` pin 4), `WHT-ORG, SW. ROW 3` (`J209` pin 3), `WHT-RED, SW. ROW 2` (`J209` pin 2), `WHT-BRN, SW. ROW 1`
(`J209` pin 1), `BLK` and `GRY-YEL, +12V` (Power Driver Board `J118` pins 3 and 2).

Schematic (PDF page 123, `A-15576 7-Opto Switch Board Schematic`):

| Connector | Pin labels as printed (pin: label) |
| --- | --- |
| J2 | 10: +12V; 9: +12V; 8: KEY; 7: E1 OPTO 1; 6: E2 OPTO 2; 5: E3 OPTO 3; 4: E4 OPTO 4; 3: E5 OPTO 5; 2: E6 OPTO 6; 1: E7 OPTO 7 |
| J1 | 9: CATHODE GND; 10: CATHODE GND; 4: KEY; 8: ANODE LED 1 (R15); 7: ANODE LED 2 (R16); 6: ANODE LED 3 (R17); 5: ANODE LED 4 (R18); 3: ANODE LED 5 (R19); 2: ANODE LED 6 (R20); 1: ANODE LED 7 (R21); each LED resistor `2W OR 1/2W` |
| J3 | 1: +12V; 2: +12V; 3: GND; 4: KEY; 5: R1; 6: R2; 7: R3; 8: R4; 9: R5; 10: R6; 11: R7; 12: Col. |

`Traced` from the schematic (comparator pairings read from wire routing, less certain than the printed labels): each of the seven opto inputs `E1` to `E7` (`OPTO 1` to `OPTO 7`) feeds a divider and
one `LM339` section (`U1D`, `U1A`, `U1C`, `U2A`, `U2D`, `U2B`, `U2C` in that order) and a diode `D2`-`D8` to the `J3`
pin labelled `R1` to `R7`.

Opto position, `J1`/`J2` pins, printed switch and printed function (combining the schematic labels with the printed
lists above):

| Opto position | J2 pin (photo transistor) | J1 pin (LED) | J3 pin / row | Printed switch and function |
| --- | --- | --- | --- | --- |
| E1 / OPTO 1 | J2-7 Orange-Brown | J1-8 Gray-Brown | J3-5 row 1 | switch #71 Chase Car 1 |
| E2 / OPTO 2 | J2-6 Orange-Red | J1-7 Gray-Red | J3-6 row 2 | switch #72 Chase Car 2 |
| E3 / OPTO 3 | J2-5 Orange-Black | J1-6 Gray-Orange | J3-7 row 3 | switch #73 Top Popper |
| E4 / OPTO 4 | J2-4 Orange-Yellow | J1-5 Gray-Black | J3-8 row 4 | switch #74 Elevator Hold |
| E5 / OPTO 5 | J2-3 N/C | J1-3 N/C | J3-9 N/C (row 5) | none printed |
| E6 / OPTO 6 | J2-2 Orange-Blue | J1-2 Gray-Blue | J3-10 row 6 | switch #76 Bottom Popper |
| E7 / OPTO 7 | J2-1 N/C | J1-1 N/C | J3-11 N/C (row 7) | none printed |

The `E` to switch pairing is consistent with the printed switch numbers (`E1` to #71 through `E6` to #76): a switch
number's row digit equals the opto number. Optos 5 and 7 have no wire on any of the three connectors and no printed
switch number.

Printed differences (kept literal): the schematic ties `J2` pins 9 and 10 both to `+12V` while the list prints
`J2 - 9 N/C` and `J2 - 10 Gray-Yellow (+12V)`; the schematic ties `J1` pins 9 and 10 both to `CATHODE GND` while the
list prints `J1 - 9 N/C` and `J1 - 10 Black (ground)`; the schematic ties `J3` pins 1 and 2 both to `+12V` and pin 3
to `GND` while the list prints `J3 - 2 N/C`.

## A-16986 Cryoclaw Opto PCB Assembly (PDF page 124, printed 3-20)

Schematic: two LEDs `Opto 1` and `Opto 2` (`R1` and `R2`, `470Ω 1/2W`) and two phototransistors with diodes `D1`,
`D2` (`IN4004`); `J1` pin labels as printed: `1 Gnd`, `2 +12V`, `3 Key`, `4 Col.`, `5 R1`, `6 R2`.

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Black, ground from Power Driver Board J118-3 |
| J1 - 2 | Gray-Yellow, +12V from Power Driver Board J118-2 |
| J1 - 3 | Key |
| J1 - 4 | Green-Red, switch column 2 from CPU Board J207-2 |
| J1 - 5 | White-Green, switch row 5 from CPU Board J209-5 |
| J1 - 6 | White-Blue, switch row 6 from CPU Board J209-7 |

Wiring diagram at the bottom of the page, as printed (upper-case):

- `CRYOCLAW OPTO BOARD` `(SW. #25 CLAW POSITION 1, SW. #26 CLAW POSITION 2)`, connector `J1` pins `6`, `5`, `4`, `2`, `1`,
  wired `WHT-BLU, SW. ROW 6` (CPU `J209` pin 7), `WHT-GRN, SW. ROW 5` (CPU `J209` pin 5), `GRN-RED, SW. COL. 2` (CPU
  `J207` pin 2), `GRY-YEL, +12V`, `BLK, GROUND`.
- `D.C. MOTOR CONTROL BOARD` connector `J1` pins `5`, `4`, `2`, `1` wired to `GRY-YEL` (+12V) and `BLK` ground (both drawn
  from Power Driver Board connector `J118`, pins `2` and `3`), `BLK-ORG, SOL. 19 CLAW LEFT` (Power Driver Board `J126` pin 3)
  and `BLK-YEL, SOL. 20 CLAW RIGHT` (`J126` pin 4); connector `J2` pins `1` and `4` to the `CRYOCLAW MOTOR` wires `RED`
  and `BLK`.

Printed switch pairing (diagram caption with the printed schematic): switch #25 is column 2 row 5 (`J1-5`, `R1`,
`Opto 1`) and switch #26 is column 2 row 6 (`J1-6`, `R2`, `Opto 2`). The caption names #25 `CLAW POSITION 1` and #26
`CLAW POSITION 2`.

## A-16120 D.C. Motor Control Assembly (PDF page 125, printed 3-21)

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Black-Yellow, sol. 20 Claw Motor Right, from Power Driver Board J126-4 |
| J1 - 2 | Black-Orange, sol. 19 Claw Motor Left, from Power Driver Board J126-3 |
| J1 - 3 | Key |
| J1 - 4 | Black, Ground from J118-3 |
| J1 - 5 | Gray-Yellow, +12VDC from J118-2 |
| J2 - 1 | Red, to Cryoclaw Motor |
| J2 - 2 | Key |
| J2 - 3 | Not Used |
| J2 - 4 | Black, to Cryoclaw Motor |

Schematic labels (PDF page 125): `J1` pins `12 B+` (as printed at the top pin), `4 GND`, `3 KEY`, `1 DIR/2`, `2 DIR/1`;
`Q1` `LM7805`, two `4N25` optocouplers `U2` and `U1` (inputs `DIR/2` through `D3` and `DIR/1` through `D2`), an `L6203`
driver `U3` with `IN1` `IN2` `EN`, `74LS32` gates `U3A`-`U3D`, outputs `OUT1` and `OUT2` through `L1` and `L2` to `J2`
(`J2` pins labelled `4`, `3`, `Key 2`, `1`). `Traced`: `DIR/2` (`J1-1`, sol. 20) drives `U2` and `L6203` `IN1`; `DIR/1`
(`J1-2`, sol. 19) drives `U1` and `IN2`; `OUT2` goes through `L2` to `J2` pin 4 and `OUT1` through `L1` to `J2` pin 1.

## A-17596 Elevator Opto PCB Assembly (PDF page 126, printed 3-22)

Schematic labels: `J1` pins `1 +12V`, `2 R1`, `3 Col.`, `4 Key`, `5 Gnd`; one LED/phototransistor `Opto 1`, `R1` `470Ω 1/2W`,
diode `D1` `IN4004`.

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Gray-Yellow, +12V from Power Driver Board J118-2 |
| J1 - 2 | White-Violet, switch row 7 from CPU Board J209-8 |
| J1 - 3 | Green-Blue, switch column 6 from CPU Board J207-6 |
| J1 - 4 | N/C |
| J1 - 5 | Black, ground from Power Driver Board J118-3 |

Wiring diagram: `ELEVATOR OPTO BOARD` `(SW. #67 ELEVATOR INDEX )` connector `J1` pins `5`, `3`, `2`, `1` wired `BLK, GROUND`,
`GRN-BLU, SW. COL. 6` (CPU `J207` pin 6), `WHT-VIO, SW. ROW 7` (CPU `J209` pin 8), `GRY-YEL, +12V`. Below it, `MOTOR EMI
BOARD` `J1` pins `3` and `1` wired `GRY-YEL, +12V` and `BLK-RED, SOL. 18 ELEVATOR MOTOR` (Power Driver Board `J126` pin
2), `J2` pins `1` and `2` to the `ELEVATOR MOTOR` (`RED`, `BLK`).

## A-15542 Motor EMI PCB Assembly (PDF page 127, printed 3-23)

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Black-Red, sol. 18 Elevator Motor, from  Power Driver Board J126-2 |
| J1 - 2 | Key |
| J1 - 3 | Gray-Yellow, +12V from Power Driver Board J118-2 |
| J2 - 1 | Red to Elevator Motor |
| J2 - 2 | Black to Elevator Motor |

Schematic: `J1` pin 3 through `L1` (`4.7MH 3A`) to `J2` pin 1; `J1` pin 1 through `D1` (`1N4004 1A`) and `L2` (`4.7MH 3A`)
to `J2` pin 2; `J1` pin 2 `KEY`.

## A-16100-2 8-Driver (Aux. Driver) PCB Assembly (PDF pages 128 and 129, printed 3-24 and 3-25)

Connector wiring (PDF page 128):

| Pin | Printed text |
| --- | --- |
| J1-1 | Ribbon cable, data, from CPU Board J204 |
| J2-1 | Black-White, digital ground, from Power Driver Board J114-7 |
| J2-2 | Key |
| J2-3 | Gray, +5V, from Power Driver Board J114-3 |
| J2-4 | Black, ground, from Power Driver Board J103-1 |
| J2-5 | Black, ground, from Power Driver Board J103-2 |
| J2-6 | Gray-Green, +12V, from Power Driver Board J114-2 |
| J3-1 | N/C |
| J3-2 | Green-White, sol. 41 Elevator 2 Flasher, to playfield |
| J3-3 | Blue-White, sol. 42 Elevator 1 Flasher, to playfield |
| J3-4 | Violet-White, sol. 43 Diverter Flasher, to playfield |
| J3-5 | Gray-White, sol. 44 Right Ramp Upper Flasher, to playfield |
| J3-6 | Key |
| J3-7 | N/C |
| J4-1 | N/C |
| J4-2 | Brown-White, sol. 37 Car Chase Upper Flasher, to playfield |
| J4-3 | N/C |
| J4-4 | Black-White, sol. 38 Lower Rebound Flasher, to playfield |
| J4-5 | Orange-White, sol. 39 Eyeball Flasher, to playfield |
| J4-6 | Yellow-White, sol. 40 Center Ramp Flasher, to playfield |
| J4-7 | N/C |
| J5-1 | N/C |
| J5-2 | Key |
| J5-3 | N/C |
| J5-4 | N/C |

The `J4-2` line wraps to a second line in the print (`to` / `playfield`). The wiring diagram printed beneath (upper-case
labels): `8-DRIVER BOARD` `J4` pins `2`, `4`, `5`, `6` to `BRN-WHT, SOL. 37 CAR CHASE UPPER FLSHR`, `BLK-WHT, SOL. 38 LOWER
REBOUND FLSHR`, `ORG-WHT, SOL. 39 EYEBALL FLSHR`, `YEL-WHT, SOL. 40 CENTER RAMP FLSHR`; `J3` pins `2`, `3`, `4`, `5` to `GRN-WHT, SOL. 41
ELEVATOR 2 FLSHR`, `BLU-WHT, SOL. 42 ELEVATOR 1 FLSHR`, `VIO-WHT, SOL. 43 DIVERTER FLSHR`, `GRY-WHT SOL. 44 RIGHT RAMP UPPER FLSHR`,
each ending in a lamp symbol, the lamps joined to a common line labelled `RED-WHT, +20V` from Power Driver Board
`J107` pin 6; `J2` pins `1 3 4 5 6` wired `BLK-WHT, DIG. GND` (`J114` pin 7), `GRY, +5V` (`J114` pin 3), `GRY-GRN, +12V`
(`J114` pin 2), `BLK, GND` and `BLK, GND` (`J103` pins 1 and 2); `CPU BOARD` `J204` to `J1`.

Schematic (PDF page 129, rotated, `A-16100-2 8-Driver (Aux. Driver) PCB Schematic`): a `74ALS576` latch `U1`, a
`HEADER 13X2` `J1`, eight `2N4403` transistors `Q1`-`Q8`, eight `TIP 102` output transistors `Q9`-`Q16` and diodes
`D1`-`D16`. Connector labels as printed:

| Connector | Pin labels as printed (pin: label) |
| --- | --- |
| J4 | 1: +50VDC (A); 3: KEY; 2: SOL. 1; 4: SOL. 2; 5: SOL. 3; 6: SOL. 4; 7: GND |
| J3 | 2: SOL. 5; 3: SOL. 6; 4: SOL. 7; 5: SOL. 8; 6: KEY; 7: +50VDC (B); 1: GND |
| J5 | 4: COL. 10; 3: (tied to COL. 10); 2: KEY; 1: COL. 9 |
| J2 | 6: +12VDC; 5: PWR GND; 4: PWR GND (pins 4 and 5 tied); 3: +5VDC; 2: KEY; 1: DIGI. GND |

Output transistor per board output (printed beside the drive stage): `SOL. 1` `Q16`, `SOL. 2` `Q15`, `SOL. 3` `Q14`, `SOL. 4`
`Q13`, `SOL. 5` `Q9`, `SOL. 6` `Q10`, `SOL. 7` `Q11`, `SOL. 8` `Q12`. The `J5` header (pins labelled `COL. 9`, `COL. 10`, `KEY`) and the jumper labels `SW2`, `SW4`, `PW1`, `PW3`, `SW6`,
`PW5` appear on the schematic; the connector list prints every `J5` pin `N/C` or `Key`.

Printed solenoid table (PDF page 102, printed 2-46) for the same outputs, columns `Sol. No.`, `Function`, `Solenoid
Type`, `Voltage Connections Playfield`, `Drive xister`, `Drive Connections Playfield`, `Drive Wire Color`, `Flashlamp Type
Playfield`; each of these rows is printed with an asterisk after the number (`37*`) and the note `*Note: Controlled from
the 8-Driver Board, not the Power Driver Board`:

| Sol. | Function | Type | V playfield | Drive transistor | Drive playfield | Wire colour | Lamp type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 37* | Car Chase Up Flshr | Low Power | J107-6 | Q16 | J4-2 | Brn-Wht | #89 (1) |
| 38* | Lower Rebound Flshr | Low Power | J107-6 | Q15 | J4-4 | Blk-Wht | #89 (1) |
| 39* | Eyeball Flasher | Low Power | J107-6 | Q14 | J4-5 | Org-Wht | #89 (1) |
| 40* | Center Ramp Flasher | Low Power | J107-6 | Q13 | J4-6 | Yel-Wht | #89 (1) |
| 41* | Elevator 2 Flasher | Low Power | J107-6 | Q9 | J3-2 | Grn-Wht | #906 (2) |
| 42* | Elevator 1 Flasher | Low Power | J107-6 | Q10 | J3-3 | Blu-Wht | #906 (1) |
| 43* | Diverter Flasher | Low Power | J107-6 | Q11 | J3-4 | Vio-Wht | #906 (1) |
| 44* | Rt. Ramp Up Flasher | Low Power | J107-6 | Q12 | J3-5 | Gry-Wht | #906 (1) |

Observations: the schematic names `+50VDC (A)` on `J4` pin 1, `+50VDC (B)` on `J3` pin 7 and `GND` on `J4` pin 7 and `J3` pin
1, but the connector list prints those pins `N/C` (J4-1, J4-7, J3-1, J3-7) and the diagram feeds the flashlamps from the `+20V`
line of `J107` pin 6. The list prints `J4-3` as `N/C` and `J3-6` as `Key` while the schematic prints `KEY` on `J4` pin 3
and on `J3` pin 6. The names in the solenoid table (`Car Chase Up Flshr`, `Lower Rebound Flshr`, `Eyeball Flasher`,
`Center Ramp Flasher`, `Elevator 2 Flasher`, `Elevator 1 Flasher`, `Diverter Flasher`, `Rt. Ramp Up Flasher`) differ in
abbreviation from the connector list (`Car Chase Upper Flasher`, `Lower Rebound Flasher`, ..., `Right Ramp Upper Flasher`);
the solenoid numbers, wire colours and pins agree.

## Mechanism-related rows of the printed solenoid table (PDF page 102), for cross-reference

Rows 17-28 of the same table, with their printed connectors (columns as for the G.I. block in
`general-illumination.md`; blank cells printed blank; rows 21-28 are the playfield flashers on the Power Driver
Board; the `Part` column prints a part number for the motors and a lamp type for flashers):

| Sol. | Function | Type | V playfield | V backbox | Drive transistor | Drive playfield | Drive backbox | Wire colour | Part / lamp playfield | Lamp backbox |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | Claw Flasher | Low Power | J107-6 | J106-5 | Q42 | J126-1 | J125-1 | Blk-Brn | #906 (1) | #906 (1) |
| 18 | Elevator Motor |  | J118-2 |  | Q40 | J126-2 |  | Blk-Red | 14-7993 |  |
| 19 | Claw Motor Left |  | J118-2 |  | Q38 | J126-3 |  | Blk-Org | 14-7992 |  |
| 20 | Claw Motor Right |  | J118-2 |  | Q36 | J126-4 |  | Blk-Yel | 14-7992 |  |
| 21 | Jets Flasher | Flasher | J107-6 | J106-5 | Q28 | J126-5 | J125-6 | Blu-Grn | #89 (1) | #906 (1) |
| 22 | Side Ramp Flasher | Flasher | J107-6 | J106-5 | Q30 | J126-6 | J125-7 | Blu-Blk | #89 (1) | #906 (1) |
| 23 | Left Ramp Up Flshr | Flasher | J107-6 | J106-5 | Q34 | J126-7 | J125-8 | Blu-Vio | #906 (1) | #906 (1) |
| 24 | Left Ramp Lwr Flshr | Flasher | J107-6 | J106-5 | Q32 | J126-8 | J125-9 | Blu-Gry | #89 (1) | #906 (1) |
| 25 | Car Chase Cntr Flshr | Gen. Purpose | J107-6 | J106-5 | Q26 | J122-1 | J124-1 | Blu-Brn | #89 (1) | #906 (1) |
| 26 | Car Chase Lwr Flshr | Gen. Purpose | J107-6 | J106-5 | Q24 | J122-2 | J124-2 | Blu-Red | #89 (1) | #906 (1) |
| 27 | Right Ramp Flasher | Gen. Purpose | J107-6 | J106-5 | Q22 | J122-3 | J124-3 | Blu-Org | #89 (1) | #906 (1) |
| 28 | Eject Flasher | Gen. Purpose | J107-6 | J106-5 | Q20 | J122-4 | J124-5 | Blu-Yel | #89 (1) | #906 (1) |

Printed neighbours read on the same page: `15 Diverter Hold` `Low Power` `J107-2` `Q46` `J127-8` `Brn-Vio` `A-15943-1`;
`16 Not Used` `Low Power` `Q44` `Brn-Gry`; `29-36 See Flipper Circuits` (printed in italics). The claw magnet is solenoid
33 in the flipper block (`flipper-circuits.md`).

## Coin Door Interface PCB Assembly A-17051-1 (PDF pages 130 and 131, printed 3-26 and 3-27)

Connector wiring (PDF page 130):

| Pin | Printed text |
| --- | --- |
| J1-1 | Orange-Gray, dedicated row 8 from CPU J205-9 |
| J1-2 | Orange-Violet, dedicated row 7 from CPU J205-8 |
| J1-3 | Orange-Blue, dedicated row 6 from CPU J205-7 |
| J1-4 | Orange-Green, dedicated row 5 from CPU J205-6 |
| J1-5 | Orange-Yellow, dedicated row 4 from CPU J205-4 |
| J1-6 | Orange-Black, dedicated row 3 from CPU J205-3 |
| J1-7 | Orange-Red, dedicated row 2 from CPU J205-2 |
| J1-8 | Orange-Brown, dedicated row 1 from CPU J205-1 |
| J1-9 | N/C |
| J1-10 | Black, ground from CPU J205-10 |
| J1-11 | Orange-White, sw. enable from J205-12 |
| J2-1 | Black, ground from Power Driver Brd J116-3 |
| J2-2 | Gray-Yellow, +12vac from Power Driver Brd J116-2 |
| J2-3 | White-Violet, G.I. 6.8vac from Power Driver Brd J119-1 |
| J2-4 | N/C |
| J2-5 | Violet, G.I. from Power Driver Brd J119-3 |
| J3-1 | Green-Brown, sw. col. 1 from CPU J212-1 |
| J3-2 | Green-Red, sw. col. 2 from CPU J212-2 |
| J3-3 | White-Brown, sw. row 1 from J212-4 |
| J3-4 | White-Red, sw. row 2 from CPU J212-6 |
| J3-5 | White-Orange, sw. row 3 from CPU J212-7 |
| J3-6 | White-Yellow, sw. row 4 from CPU J212-8 |
| J3-7 | N/C |
| J3-8 | Yellow-Gray, lamp col. 8 from Power Driver Brd J136-3 |
| J3-9 | Red-Blue, lamp row 6 from Power Driver Brd J133-7 |
| J3-10 | Red-Violet, lamp row 7 from Power Driver Brd J133-8 |
| J3-11 | Red-Gray, lamp row 8 from Power Driver Brd J133-9 |
| J3-12 | N/C |
| J4 | not used |
| J5-1 | Violet, G.I. return to coin door |
| J5-2 | White-Violet, G.I. 6.8vac to coin door |
| J5-3 | Black, ground to coin door |
| J5-4 | Orange-Brown, dedicated sw. row 1 to coin door |
| J5-5 | Orange-Red, dedicated sw. row 2 to coin door |
| J5-6 | Orange-Black, dedicated sw. row 3 to coin door |
| J5-7 | Orange-Green, dedicated sw. row 5 to coin door |
| J5-8 | Orange-Blue, dedicated sw. row 6 to coin door |
| J5-9 | Orange-Violet, dedicated sw. row 7 to coin door |
| J5-10 | N/C |
| J5-11 | Orange-Gray, dedicated sw. row 8 to coin door |
| J5-12 | Green-Red, sw col. 2 to coin door Slam tilt |
| J5-13 | White-Brown, sw. row 1 to coin door Slam tilt |
| J6 | not used |
| J7-1 | Yellow-Gray, lamp col. 8 to cabinet |
| J7-2 | Red-Blue, lamp row 6 to cabinet |
| J7-3 | Red-Violet, lamp row 7 to cabinet |
| J7-4 | Red-Gray, lamp row 8 to cabinet |
| J7-5 | N/C |
| J7-6 | Green-Brown, sw. col. 1 to cabinet |
| J7-7 | Green-Red, sw. col. 2 to cabinet |
| J7-8 | White-Orange, sw. row 3 to cabinet |
| J7-9 | White-Red, sw. row 2 to cabinet |
| J7-10 | White-Brown, sw. row 1 to cabinet |
| J7-11 | White-Orange, sw. row 3 to cabinet |
| J8-1 | White, sw. row to cabinet Slam tilt |
| J8-2 | N/C |
| J8-3 | Green, sw. col to cabinet Slam tilt |
| J9-1 | White-Yellow, sw. row 4 to Plumb Bob tilt |
| J9-2 | N/C |
| J9-3 | Green-Brown, sw. col. 1 to Plumb Bob tilt |
| J9-4 | White-Red, sw. row 2 to interlock switch |
| J9-5 | Green-Red, sw. col. 2 to interlock switch |

The schematic (PDF page 131) labels the connector pins: `J1 DEDICATED IN` `1 DIG. SW4`, `2 DIG. SW3`, `3 DIG. SW2`, `4 DIG.
SW1`, `5 COIN 4`, `6 RT. COIN 3`, `7 CN. COIN 2`, `8 LT. COIN 1`, `9 KEY`, `10 GND`, `11 ENABLE`; `J2 POWER IN` `5 6.3VAC`, `4 KEY`, `3
6.3VAC`, `2 +12V`, `1 GND`; `J3 SWITCH /LAMP IN` `1 SW. COL. 1`, `2 SW. COL. 2`, `3 SW. ROW 1`, `4 SW. ROW 2`, `5 SW. ROW 3`, `6 SW. ROW 4`, `7
KEY`, `8 LP. COL. 1`, `9 LP. ROW 1`, `10 LP. ROW 2`, `11 LP. ROW 3`, `12 NC`; `J4 NRI`, `J5 COIN DOOR` (`13 SLAM SW. ROW 1`, `12 SLAM SW. COL.
2`, `11 SW4`, `10 KEY`, `9 SW3`, `8 SW2`, `7 SW1`, `6 RT. COIN 3`, `5 CN. COIN 2`, `4 LT. COIN 1`, `3 GND`, `2 GI LAMP`, `1 GI LAMP`), `J6 ECA
COIN DOOR`, `J7 CABINET` (`1 LP. COL. 1`, `2 LP. ROW 1`, `3 LP. ROW 2`, `4 LP. ROW 3`, `5 KEY`, `6 SW. COL. 1`, `7 SW. COL. 2`, `8 SW. ROW 3`, `9 SW. ROW 2`, `10 SW.
ROW 1`, `11 SW. ROW 3`), `J8 SLAM`, `J9 PLUMB BOB/COIN DOOR`. `NOTE: ALL DIODES IN4004`.

Observations: the schematic's J3 and J7 pin labels use the board's own names (`LP. COL. 1`, `LP. ROW 1`...) while the printed
wiring list names the lamp lines as `lamp col. 8`, `lamp row 6/7/8`; `J7-11` repeats `White-Orange, sw. row 3 to cabinet`
(J7-8 prints the same) in both the list and the schematic label (`SW. ROW 3` on pins 8 and 11); the list prints J2-3
`White-Violet, G.I. 6.8vac`, the schematic prints `6.3VAC` on `J2` pins 5 and 3; the list prints `+12vac` for J2-2, the
schematic prints `+12V`. The Power Driver Board list (`power-driver-board-connectors.md`) numbers the same J2 pins in the
reverse order (see the note there).
