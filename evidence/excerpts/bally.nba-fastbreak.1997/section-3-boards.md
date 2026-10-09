# NBA Fastbreak — Section 3 Boards, Wiring Diagrams and Circuit Text

Transcribed from `Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf` (document
16-50053.1-101, May 1997), Section Three `GAME WIRING AND SCHEMATICS`. PDF pages and printed folios used:

| PDF page | Printed folios | Content transcribed here |
| --- | --- | --- |
| 72 | 3-6, 3-7 | Solenoid Wiring (coils), Flashlamps wiring |
| 73 | 3-8, 3-9 | High/Low Power Solenoid, Special (General Purpose) Solenoid and Flashlamp circuits |
| 74 | 3-10, 3-11 | General Illumination circuit; Flipper Circuit Diagram |
| 75 | 3-12, 3-13 | Flipper Coil Circuits, Flipper E.O.S. Switch Circuit, Flipper Cabinet Switch Circuits |
| 76 | 3-14, 3-15 | Flipper Opto Board Assembly A-17316; Trough IR LED Board A-18617-1 |
| 77 | 3-16, 3-17 | Trough IR Photo Transistor Board A-18618-1; Ball Trough Opto Switches Wiring; Center Ramp / Right Loop Enter Opto wiring |
| 78 | 3-18, 3-19 | 7-Opto Switch Board A-15576.1 assembly and schematic |
| 79 | 3-20, 3-21 | 24-Opto Switch Board A-15646 assembly and schematic |
| 80 | 3-22, 3-23 | LED Board A-16908 / Photo Transistor Board A-16909; Defender Switch Board A-21402 |
| 81 | 3-24, 3-25 | 2 LED Driver Board A-21399; 2 LED Display Board A-21380; Shot Clock Assembly wiring |
| 82 | 3-26, 3-27 | High Current Driver Board C-13963-1; Security CPU Board A-21377-50053 connector list |
| 83 | 3-28, 3-29 | Audio Visual Board A-20516-50053 connector list; Power Driver Board (see `power-driver-board.md`) |
| 85 | 3-32, 3-33 | Coin Door Interface Board A-20580 connector list and schematic |

PDF page 69 is the Section Three title page (`SECTION THREE`, `GAME WIRING AND SCHEMATICS`, `CONNECTOR & COMPONENT
IDENTIFICATION`, printed `3-1`; its text says that a J-designation is a male connector and a P-designation a female
connector, that `J101-3` is pin 3 of jack 1 of board 1, and that the prefix numbers are `J1XX` Power Driver board
jacks and `F1XX` Power Driver board fuses, `J2XX` CPU board (no fuses), `J5XX` and `J6XX` Audio Video board jacks and
`F5XX` and `F6XX` Audio Video board fuses; and in bold that schematics for standard WPC backbox boards are found in the
WPC Schematics Manual and that playfield, cabinet and all other backbox board schematics are found in this section).
The matrices on PDF page 70 (`3-2`, `3-3`) and 71 (`3-4`, `3-5`) are covered in `switch-matrix.md`, `lamp-matrix.md`
and `solenoid-flasher-table.md`. Pages 83 (right, `3-29`) and 84 (`3-30`, `3-31`) are the Power Driver Board
connector list, in `power-driver-board.md`. PDF page 86 (printed `3-36`) is a reprint of the Lamp Matrix and Switch
Matrix (see `differences-march-vs-may.md`). Read from the rendered pages (300 dpi scan), not from the OCR text.

## Opto summary: which switches are optos and on which board

From the Switch Locations list (`switch-locations.md`), the matrix legend `= OPTO, TYPICALLY CLOSED` (`switch-matrix.md`)
and the board pages below:

| Switch | Printed name | Board / opto assembly |
| --- | --- | --- |
| F2 | Lower Right Flipper Opto | Right Flipper Opto Board A-17316, `J1-2` (`SW2`, `Blue-Violet`, CPU `J212-12`) |
| F4 | Lower Left Flipper Opto | Left Flipper Opto Board A-17316, `J1-2` (`SW2`, `Blue-Gray`, CPU `J212-11`) |
| F6 | Upper Right Flipper Opto | Right Flipper Opto Board A-17316, `J1-1` (`SW1`, `Black-Yellow`, CPU `J212-10`) |
| F8 | Upper Left Flipper Opto | Left Flipper Opto Board A-17316, `J1-1` (`SW1`, `Black-Blue`, CPU `J212-9`) |
| F5 | BASKET MADE OPTO | 24-Opto Switch Board A-15646 |
| 31 | TROUGH EJECT | Trough IR LED A-18617-1 (LED 1, `Jam Ball`) + Photo Transistor A-18618-1 (Q1) via 7-Opto Switch Board A-15576.1 |
| 32 | TROUGH BALL 1 | Trough IR boards, LED 2 / Q2 (`Ball 1`) |
| 33 | TROUGH BALL 2 | Trough IR boards, LED 3 / Q3 (`Ball 2`) |
| 34 | TROUGH BALL 3 | Trough IR boards, LED 4 / Q4 (`Ball 3`) |
| 35 | TROUGH BALL 4 | Trough IR boards, LED 5 / Q5 (`Ball 4`) |
| 36 | CENTER RAMP OPTO | LED Board A-16908 + Photo Transistor Board A-16909, via 7-Opto Switch Board A-15576.1 |
| 37 | RIGHT LOOP ENTER OPTO | LED Board A-16908 + Photo Transistor Board A-16909, via 7-Opto Switch Board A-15576.1 |
| 51 | DEFENDER POSITION 4 | Defender Switch Board A-21402 (Switch Row 1, `J1-5`, `WHT-BRN`, `J208-1`) |
| 52 | DEFENDER POSITION 3 | Defender Switch Board A-21402 (Switch Row 2, `J1-6`, `WHT-RED`, `J208-2`) |
| 53 | DEFENDER LOCK POSITION | Defender Switch Board A-21402 (Switch Row 3, `J1-7`, `WHT-ORG`, `J208-3`) |
| 54 | DEFENDER POSITION 2 | Defender Switch Board A-21402 (Switch Row 4, `J1-8`, `WHT-YEL`, `J208-4`) |
| 55 | DEFENDER POSITION 1 | Defender Switch Board A-21402 (Switch Row 5, `J1-9`, `WHT-GRN`, `J208-5`) |

(Each flipper opto board has two optos, `OPTO1` on `SW1` (`J1-1`) and `OPTO2` on `SW2` (`J1-2`); the page does not print which switch letter belongs to which opto, only the `J1` pin the CPU wires name (`3-14`, `3-27`). The Switch Locations list (`2-42`) prints the assembly cells for F6 and F8 as `NOT USED` and for F2 and F4 as `A-17316`.)

(The Defender board's page says `FOR DEFENDER POSITIONS AND DEFENDER LOCK OPTO SWITCHES` and prints five opto positions `U1`-`U5` (each with
`Q1`-`Q5`); the page does not say which of `U1`-`U5` is which switch, only that the five `Switch Row 1` to `Switch Row 5` pins, with `Switch Column 5`,
give matrix switches 51-55. The Flipper Opto Board page does not name F6 and F8 by number; the CPU connector list and the F-numbers on
`3-11` and `3-13` do: `J212-9 BLK-BLU, F8, to left flipper opto board J1-1`, `J212-10 BLK-YEL, F6, to right flipper
opto board J1-1`, `J212-11 BLU-GRY, F4, to left flipper opto board J1-2`, `J212-12 BLU-VIO, F2, to right flipper opto
board J1-2`.) The `F1`, `F3`, `F7` flipper cells and the `BASKET HOLD` `F7` are mechanical (end-of-stroke / basket
hold) switches wired to `J208`, not optos.

## Printed page 3-6: Solenoid Wiring (coils)

Heading `SOLENOID WIRING`, subheading `COILS`; the drawing shows the `POWER DRIVER BOARD` boundary with connectors J133,
J109, J113, J116, J117, J119 and J120 and the coil boxes. Printed wire labels and pins:

| Connector pin | Printed label |
| --- | --- |
| J133 pin 1 | RED-ORG, +50V |
| J133 pin 2 | RED-BRN, +50V |
| J133 pin 3 | RED-BLK, +50V |
| J109 pin 1 / 2 / 3 / 4 | BLU-BRN / BLU-RED / BLU-ORG / BLU-YEL (to boxes `PASS RIGHT 1 SOL. 25`, `PASS LEFT 3 SOL. 26`, `PASS RIGHT 3 SOL. 27`, `PASS LEFT 4 SOL. 28`) |
| J113 pins 1, 3, 4, 5, 6, 7, 8, 9 | BRN-BLK, BRN-RED, BRN-ORG, BRN-YEL, BRN-GRN, BRN-BLU, BRN-VIO, BRN-GRY (to boxes `TROUGH EJECT SOL. 9`, `LEFT SLINGSHOT SOL. 10`, `RIGHT SLINGSHOT SOL. 11`, `LEFT JET BUMPER SOL. 12`, `MIDDLE JET BUMPER SOL. 13`, `RIGHT JET BUMPER SOL. 14`, `PASS RIGHT 2 SOL. 15`, `PASS LEFT 2 SOL. 16`) |
| J116 pins 1, 4, 5, 6, 7, 9 | VIO-BRN, VIO-ORG, VIO-YEL, VIO-GRN, VIO-BLU, VIO-GRY (to `AUTO-PLUNGER SOL. 1`, `LEFT RAMP DIVERTER SOL. 3`, `RIGHT LOOP DIVERTER SOL. 4`, `EJECT SOL. 5`, `LOOP GATE SOL. 6`, `BALL CATCH MAGNET SOL. 8`) |
| J117 pin 3 | VIO-BLK (to `BACKBOX FLIPPER SOL. 7`) |
| J119 pin 8 | RED-GRY, +50V (to `SHOOT 3 SOL. 35` and `SHOOT 4 SOL. 36`) |
| J119 pin 6 | RED-VIO, +50V (to `SHOOT 1 SOL. 33` and `SHOOT 2 SOL. 34`) |
| J120 pins 6, 4, 3, 1 | YEL-VIO, ORG-VIO, YEL-GRY, ORG-GRY (to `SHOOT 1 SOL. 33`, `SHOOT 2 SOL. 34`, `SHOOT 3 SOL. 35`, `SHOOT 4 SOL. 36`) |

The drawing puts `SHOOT 2` (solenoid 34) on `J120` pin 4, as the Solenoid/Flasher Table does (`J120-4`), whereas the Power Driver Board connector list prints solenoid 34's `ORG-VIO` wire on `J120-5` and `J120-4 N/C` (see `power-driver-board.md`).

In the drawing the +50V line from J133 pin 1 runs to the bus above the four `PASS` boxes 25-28, J133 pin 3 to the bus above
the eight boxes `TROUGH EJECT` through `PASS LEFT 2` (9-16), and J133 pin 2 to the bus above the boxes `AUTO-PLUNGER`
through `BALL CATCH MAGNET` (1, 3, 4, 5, 6, 7, 8). The Solenoid/Flasher Table gives the same assignment: High Power 01-08 on
`J133-2`, Low Power 09-16 on `J133-3`, General Purpose 25-28 on `J133-1`. The drawing prints no box for solenoid 2.

## Printed page 3-7: Flashlamps wiring

Heading `FLASHLAMPS`. Two drawings.

`INSERT PANEL`: `J134` pin 5 `RED-WHT, +20V`; `J112` pin 3 `BLK-ORG  SOLENOID 19  UPPER LEFT FLASHER`; `J112` pin 5
`BLK-YEL  SOLENOID 20  UPPER RIGHT FLASHER`.

`PLAYFIELD`: `J133` pin 6 `RED-WHT, +20V`; then `J111`:

| J111 pin | Wire | Printed solenoid number | Printed name |
| --- | --- | --- | --- |
| 1 | BLK-BRN | SOLENOID 17 | EJECT KICKOUT FLASHER |
| 2 | BLK-RED | SOLENOID 19 | LEFT JET BUMPER FLASHER |
| 3 | BLK-ORG | SOLENOID 20 | UPPER LEFT FLASHER |
| 4 | BLK-YEL | SOLENOID 22 | UPPER RIGHT FLASHER |
| 6 | BLU-BLK | SOLENOID 23 | TROPHY INSERT FLASHER |
| 8 | BLU-GRY | SOLENOID 24 | LOWER RIGHT & LEFT FLASHERS (two bulbs in parallel on this line) |

Printed discrepancy: this drawing prints the solenoid numbers 19, 20, 22 and 23 on `J111` pins 2, 3, 4 and 6, where the
Solenoid/Flasher Table (`2-50`, `3-5`) and the Power Driver Board connector list print 18, 19, 20 and 22 for the same
wires (`BLK-RED`, `BLK-ORG`, `BLK-YEL`, `BLU-BLK`). The `INSERT PANEL` drawing prints 19 and 20 for `BLK-ORG` and `BLK-YEL`,
in agreement with the table. The wire colours, connector pins and names agree throughout; only these printed numbers
differ.

## Printed page 3-8: High Power and Low Power Solenoid Circuits

`HIGH POWER SOLENOID CIRCUIT`: Drive section (`J102`, `LS374`, `A`, `470`, `4.7K`, `MPSD52`, `B`, `1N4004`, `68`, `2.7K`,
`TIP102`, `C`, `TIP36C`, `220`, `1N4004`, `+50V`, `VCC`), connector `J116` to `Violet-XXX` to the `COIL`; Power section
(`J128` pins 9, 8, 6, 5, `F108`, `D22 D20 D19 D21`, `all P600D`, `100mf 100V`, `+50V`, `F103`, `10K 1W`, `LED`), `J133` pin 2
`Red-Brown`. Text: `The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of the
2N5401 transistor, is high. A high at point "B" causes point "C", the collector of the TIP102 transistor and point "D", the emitter
of the TIP36C transistor, to drop low. When point "D" is low, the coil is grounded through the transistor and turns on. The coil shuts
off when point "A" toggles high.`

`LOW POWER SOLENOID CIRCUIT`: the same drive section without the TIP36C (`J113`, `Brown-XXX`, `COIL`), `J133` pin 3 `Red-Black`
through `F102`. Text: `The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of the
2N5401 transistor, is high. A high at point "B" turns on the TIP102 transistor and causes point "C" to drop low. When point "C" is low the
coil is grounded through the transistor and turns on. The coil shuts off when point "A" toggles high.`

## Printed page 3-9: Special (General Purpose) Solenoid and Flashlamp Circuits

`SPECIAL (GENERAL PURPOSE) SOLENOID CIRCUIT`: drive section with `J109` (`Blue-XXX`), a `FLASHER or COIL` load, power
section with `J128` pins 9, 8, 6, 5, `F108`, `F104`, `+50V`, `J133` pin 1 `Red-White`. Text: `The microprocessor toggles the output of the
74LS374. When point "A" is low, point "B" the collector of the 2N5401 transistor , is high. A high at point "B" causes a low at point "C".
When point "C" is low, the coil/flashlamp is grounded through the transistor and turns on. When point "A" toggles high the coil/flashlamp
turns off.` and `* Tieback diode is not used for flashlamp circuit.`

Printed anomaly: the `J133` pin 1 line of this drawing is labelled `Red-White`, where the Power Driver Board list and the Solenoid/Flasher Table give `J133-1` as `RED-ORG, +50V to coils` (`Red-White` is `J133-6`, +20V). The Special circuit also shows the `FLASHER or COIL` load (a coil symbol and a lamp symbol side by side) with the `+50V` through fuse `F104`.

`FLASHLAMP CIRCUIT`: drive section with `J111` (`Black-XXX`), a `FLASHER` load, power section with `J128` pins 3, 4, 1, 2, `F107`, `D16 D15 D18 D17`,
`+20V`, `0.12 10W`, `10,000mf 35V`, `2K`, `LED`, `J133` pin 6 `Red-White`. Text: `The microprocessor toggles the output of the 74LS374. When
point "A" is low, point "B" the collector of the 2N5401 transistor, is high. Once point "B" is high, point "C" the collector of the TIP102
transistor is low. When point "C" is low, the flashlamp is grounded through the transistor and turns on. When point "A" toggles high, the
current shuts off.`

## Printed page 3-10: General Illumination

`GENERAL ILLUMINATION CIRCUIT`: `Figure #1` (drive section `J102`, `LS374`, `A`, `560`, `MPSD52`, `B`, `51`, `SC141` triac, `C`,
`J106`; power section `J103`, `S.B.`; `G.I. LIGHTS` three lamps) and `Figure #2` (`J103` to `all P600D` bridge to `J106`, `POWER DRIVER BOARD`,
three lamps). Text: `There are five general illumination strings; three like figure #1 and two like figure #2. When point "A" toggles
low, points, "B" and "C" are high. This turns on the triac and the desired general illumination string of lights.` Block diagram:
`BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT` (`Playfield or Backbox G.I. Lights. Up to 18 bulbs per string.`, `6.3 volt secondary`,
`Power Driver Board`, `Triac Drivers`, `LS374 Latch`, `all P600D`, `OR`, `5 volt secondary`, `Zero Cross Detection Circuit`, `CPU Board`,
`Microprocessor`).

## Printed page 3-11: Flipper Circuit Diagram

Printed: `RED-GRAY +50V`, `RED-VIOLET +50V`, `RED-BLUE +50V`, `RED-GREEN +50V` into `J119` (pins `8 6 4 1` drawn); coils and drive
wires on `J120`:

| Coil | Wire | Label | Transistor |
| --- | --- | --- | --- |
| LOWER RIGHT FLIPPER COIL | YELLOW-GREEN | POWER | Q90 |
| LOWER RIGHT FLIPPER COIL | ORANGE-GREEN | HOLD | Q92 |
| LOWER LEFT FLIPPER COIL | YELLOW-BLUE | POWER | Q87 |
| LOWER LEFT FLIPPER COIL | ORANGE-BLUE | HOLD | Q89 |
| (no coil title) | YELLOW-VIOLET | *SHOOT 1 | Q84 |
| (no coil title) | ORANGE-VIOLET | *SHOOT 2 | Q86 |
| (no coil title) | YELLOW-GRAY | *SHOOT 3 | Q81 |
| (no coil title) | ORANGE-GRAY | *SHOOT 4 | Q83 |

`J139` pin 2 `GRAY-YELLOW +12V`. `CABINET OPTO SWITCHES` on `J212` (pin 13 `ORANGE GROUND`):

| J212 pin | Wire | Label | Switch | IC pin |
| --- | --- | --- | --- | --- |
| 12 | BLUE-VIOLET | L. RIGHT FLIPPER | F2 | U25A-1 |
| 11 | BLUE-GRAY | L. LEFT FLIPPER | F4 | U25B-2 |
| 10 | BLACK-YELLOW | U. RIGHT FLIPPER | F6 | U25C-14 |
| 9 | BLACK-BLUE | U. LEFT FLIPPER | F8 | U25D-13 |

(feeding the `FLIPPER OPTO BOARDS` box). `END-OF-STROKE SWITCHES` on `J208` (pin 14 `ORANGE GROUND`):

| J208 pin | Wire | Label | Switch | IC pin |
| --- | --- | --- | --- | --- |
| 13 | BLACK-GREEN | L. RIGHT FLIPPER | F1 | U26A-1 |
| 12 | BLACK-BLUE | L. LEFT FLIPPER | F3 | U26B-2 |
| 11 | BLACK-VIOLET | *BASKET MADE OPTO | F5 | U26C-14 |
| 10 | BLACK-GRAY | *BASKET HOLD | F7 | U26D-13 |

Footnote, bold: `* INDICATES A FLIPPER CIRCUIT USED FOR ANOTHER PURPOSE.`

So the manual itself marks the upper-flipper coil drives (`SHOOT 1` to `SHOOT 4`, solenoids 33-36) and the `F5` / `F7` inputs
as flipper circuits used for another purpose. The `SHOOT` coils and the basket switches use the flipper circuit hardware.

## Printed page 3-12: Flipper Coil Circuits and Flipper End-of-Stroke Switch Circuit

`FLIPPER COIL CIRCUITS`, two drawings, each with a `POWER DRIVER BOARD` box, a `PLAYFIELD` label, a `CPU BOARD` box (linked by the ribbon `J102` to `J211`) and a cabinet opto board box.

`LEFT FLIPPER CIRCUIT`: `J128` pins 9, 8, 6, 5, `F108`, bridge `D22 D20 D19 D21` (`all P600D`), `100mf 100V` capacitors, `10K 1W` and `LED`, fuses `F116` and `F117`, `J119` pins `4 5` and `8 9`:
`RED-BLUE` and `RED-GRAY` leave towards the playfield coils. `J120`:

| J120 pin | Wire | Role | Coil |
| --- | --- | --- | --- |
| 9 | YELLOW-BLUE | POWER | LOWER LEFT FLIPPER |
| 7 | ORANGE-BLUE | HOLD | LOWER LEFT FLIPPER |
| 3 | YELLOW-GRAY | POWER | UPPER LEFT FLIPPER |
| 1 | ORANGE-GRAY | HOLD | UPPER LEFT FLIPPER |

Cabinet side: `CPU BOARD` `J212` pin 13 (`GROUND`, `ORANGE`), pin 11 (`F4 LOWER`, `BLUE-GRAY`) and pin 9 (`F8 UPPER`, `BLACK-BLUE`) to the `LEFT CABINET OPTO BOARD J1` (pins drawn 6, 7, 3, 4, 1, 2).
`J208` pin 12 (`BLACK-BLUE`) and pin 10 (`BLACK-GRAY`), each paired with `ORANGE` (pin 14, ground), to `LOWER LEFT E.O.S. SWITCH` and `UPPER LEFT E.O.S. SWITCH`.

`RIGHT FLIPPER CIRCUIT`: the same power section with fuses `F115` and `F118`, `J119` pins `1 2` and `6 7`: `RED-GREEN` and `RED-VIOLET` towards the playfield coils. `J120`:

| J120 pin | Wire | Role | Coil |
| --- | --- | --- | --- |
| 12 | YELLOW-GREEN | POWER | LOWER RIGHT FLIPPER |
| 11 | ORANGE-GREEN | HOLD | LOWER RIGHT FLIPPER |
| 6 | YELLOW-VIOLET | POWER | UPPER RIGHT FLIPPER |
| 4 | ORANGE-VIOLET | HOLD | UPPER RIGHT FLIPPER |

Cabinet side: `J212` pin 13 (`GROUND`, `ORANGE`), pin 12 (`F2 LOWER`, `BLUE-VIOLET`) and pin 10 (`F6 UPPER`, `BLACK-YELLOW`) to the `RIGHT CABINET OPTO BOARD J1`. `J208` pin 13 (`BLACK-GREEN`)
and pin 11 (`BLACK-VIOLET`), each paired with `ORANGE` (pin 14), to `LOWER RIGHT E.O.S. SWITCH` and `UPPER RIGHT E.O.S. SWITCH`.

Note: this drawing prints `UPPER LEFT E.O.S. SWITCH` and `UPPER RIGHT E.O.S. SWITCH` on `J208` pins 10 and 11, and calls the coils on `J120` pins 3/1 and 6/4 `UPPER LEFT FLIPPER` and `UPPER RIGHT FLIPPER`, where
`3-11`, the CPU connector list and the Switch Matrix print `BASKET HOLD` / `BASKET MADE OPTO` and `SHOOT 1` to `SHOOT 4` for the same pins (`J208-10`, `J208-11`; solenoids 33-36). The drawing
also puts the `YELLOW-GRAY`/`ORANGE-GRAY` pair (solenoids 35, 36) on the left circuit and `YELLOW-VIOLET`/`ORANGE-VIOLET` (33, 34) on the right.

`FLIPPER END-OF-STROKE SWITCH CIRCUIT`: `CPU BOARD` `Dedicated Input`, `HCT244`, `10K` to `+5V`, `LM339` (points `A`, `B`), `1K`, `470pf`, `1K` to `+12V`, `1N4148`, `J208` pin `X` `BLACK-XXX` to a switch in the `PLAYFIELD`,
`J208` pin 14 `ORANGE` (ground); truth table `SWITCH A B / OPEN H H OFF / CLOSED L L ON`. Text, verbatim: `The flipper E.O.S. circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch.`
/ `When a switch closes, the row side, (dedicated input), of the circuit activates. The "+" input of the LM339 drops below +5V therefore its output is low. Since the row (dedicated input), circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row (dedicated input) is inactive.`

## Printed page 3-13: Flipper Cabinet Switch Circuits

`FLIPPER CABINET SWITCH CIRCUITS`: `LEFT CABINET OPTO BOARD J1` and `RIGHT CABINET OPTO BOARD J1` (each drawn with pins 6, 7, 3, 4, 1, 2 and small jumper symbols on pins 6/7 and 3/4), joined by pin to a connector column
(6; 7 3 4 1 2) with `GRAY-YELLOW +12V` from `POWER DRIVER BOARD` `J139` pin 2 to pin 6, `ORANGE` `GROUND` from `CPU BOARD` `J212` pin 13 to the `3`/`4` side, `BLUE-GRAY` `L. LEFT FLIPPER F4` to `J212` pin 11,
`BLACK-BLUE` `U. LEFT FLIPPER F8` to pin 9, `BLUE-VIOLET` `L. RIGHT FLIPPER F2` to pin 12, `BLACK-YELLOW` `U. RIGHT FLIPPER F6` to pin 10. Below, the dedicated-input circuit again (`HCT244`, `10K`, `+5V`, `LM339`, `1K`, `+12V`,
`470pf`, `1N4148`, `J212` pin `X` `BLUE-XXX` / `BLACK-XXX`, pin 13 `ORANGE` ground) driving a `FLIPPER OPTO BOARD` `J1` (pins `X`, 3 and 6; `470` ohm; opto drawn as a phototransistor and an LED; pin 6 `GRAY-YELLOW` from `J139` pin 2, `+12Vo`).
Text, verbatim: `The flipper switch circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch circuit.` / `When a switch closes, the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V, therefore, its output is low. Since the row, (dedicated input) circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row, (dedicated Input) is inactive.`

## Printed page 3-14: Flipper Opto Board Assembly A-17316

Board drawing (`OPTO1`, `OPTO2`, `R1`, `R2`, `J1` with pin legend `SW1 SW2 GND GND KEY +12V +12V`) and schematic: `R1` / `R2` `470 ohm`, opto 1 and opto 2, `J1`
pins `+12V` (7), `+12V` (6), `KEY` (5), `SW1` (1), `SW2` (2), `GND` (3), `GND` (4) [the pin numbers are as drawn; the board silk reads 1-7].

| Left Flipper Opto Board Assembly | Right Flipper Opto Board Assembly |
| --- | --- |
| J1-1 Black-Blue from CPU board J212-9 | J1-1 Black-Yellow from CPU board J212-10 |
| J1-2 Blue-Gray from CPU board J212-11 | J1-2 Blue-Violet from CPU board J212-12 |
| J1-3 N/C | J1-3 Orange from CPU board J212-13 |
| J1-4 Orange from CPU board J212-13 | J1-4 Orange from Left Flipper Opto Board Assy J1-4 |
| J1-5 N/C | J1-5 N/C |
| J1-6 Gray-Yellow from Power Driver Board J139-2 | J1-6 Gray-Yellow from Left Flipper Opto Board Assy J1-6 |
| J1-7 Gray-Yellow from Power Driver Board J139-2 | J1-7 N/C |

(The Left board's `J1-1` is F8 and `J1-2` is F4; the Right board's `J1-1` is F6 and `J1-2` is F2, per `3-11` and `3-13`.) Printed
inconsistency: the Right board's `J1-3` is printed `Orange from CPU board J212-13` and its `J1-4` `Orange from Left Flipper Opto Board
Assy J1-4`; the Left board prints `J1-3 N/C` and `J1-4 Orange from CPU board J212-13`. The Flipper Opto Board is not given an assembly
part number for the optos by this page except `A-17316`; the Switch Locations list calls the F2/F4 assembly `A-17316` and F6/F8 `NOT USED`.

## Printed page 3-15: Trough IR LED Board Assembly (transmitter, green board) A-18617-1

Board drawing (`LED1`-`LED7`, `J1` pins 9..1) and schematic with the LED labels: `LED7 (Ball 6)`, `LED6 (Ball 5)`, `LED5 (Ball 4)`, `LED4 (Ball 3)`,
`LED3 (Ball 2)`, `LED2 (Ball 1)`, `LED1 (Jam Ball)`; `J1` pin legend `1 Ball 6`, `2 Ball 5`, `3 Ball 4`, `4 Ball 3`, `5 Ball 2`, `6 Ball 1`, `7 Jam Ball`, `8 Key`, `9 Common`.

| Pin | Printed text |
| --- | --- |
| J1-1 | N/C |
| J1-2 | N/C |
| J1-3 | GRY-GRN, LED 5, to 7-Opto Switch Board J1-4 |
| J1-4 | GRY-BLK, LED 4, to 7-Opto Switch Board J1-5 |
| J1-5 | GRY-ORG, LED 3, to 7-Opto Switch Board J1-6 |
| J1-6 | GRY-RED, LED 2, to 7-Opto Switch Board J1-7 |
| J1-7 | GRY-BRN, LED 1, to 7-Opto Switch Board J1-8 |
| J1-8 | Key |
| J1-9 | BLK, ground, to 7-Opto Switch Board J1-9, J-10 |

The pin legend drawn beside the schematic's `J1` and the text list agree: pins 1 and 2 (`Ball 6`, `Ball 5`) are `N/C` in the list, pins 3-7 are `Ball 4` ... `Jam Ball` = `LED 5` ... `LED 1`, pin 8 is `Key` and pin 9 is `Common`. The list's `LED n` numbering is the schematic's `LEDn`; `LED1` is the `Jam Ball` LED.

## Printed page 3-16: Trough IR Photo Transistor Board Assembly (receiver, blue board) A-18618-1

Board drawing (`Q1`-`Q7`, `J1` pins 9..1) and schematic: `Q1 (Jam Ball)`, `Q2 (Ball 1)`, `Q3 (Ball 2)`, `Q4 (Ball 3)`, `Q5 (Ball 4)`, `Q6 (Ball 5)`, `Q7 (Ball 6)`; `J1` pin legend
`1 Common`, `2 Key`, `3 Jam Ball`, `4 Ball 1`, `5 Ball 2`, `6 Ball 3`, `7 Ball 4`, `8 Ball 5`, `9 Ball 6`.

| Pin | Printed text |
| --- | --- |
| J1-1 | GRY-YEL, +12V, to 7-Opto Switch Board J2-9, J2-10 |
| J1-2 | Key |
| J1-3 | ORG-BRN, Photo Transistor 1, to 7-Opto Switch Board J2-7 |
| J1-4 | ORG-RED, Photo Transistor 2, to 7-Opto Switch Board J2-6 |
| J1-5 | ORG-BLK, Photo Transistor 3, to 7-Opto Switch Board J2-5 |
| J1-6 | ORG-YEL, Photo Transistor 4, to 7-Opto Switch Board J2-4 |
| J1-7 | ORG-GRN, Photo Transistor 5, to 7-Opto Switch Board J2-3 |
| J1-8 | N/C |
| J1-9 | N/C |

The drawn pin legend and the text list agree: `J1-1` `Common` carries `+12V`, `J1-3` (`Jam Ball`, drawn `Q1`) is `Photo Transistor 1` ... `J1-7` (`Ball 4`, `Q5`) is `Photo Transistor 5`; `J1-8` and `J1-9` (`Ball 5`, `Ball 6`) are `N/C`.

## Printed page 3-17: Ball Trough Opto Switches Wiring Diagram; Center Ramp Opto and Right Loop Enter Opto Switches Wiring Diagram

`Ball Trough Opto Switches Wiring Diagram`: `LED BOARD` `J1` pins 3, 4, 5, 6, 7, 9 wired `GRY-GRN`, `GRY-BLK`, `GRY-ORG`, `GRY-RED`, `GRY-BRN`, `BLK, GROUND` to `7-OPTO SWITCH
BOARD` `J1` pins 4, 5, 6, 7, 9, 10. Five opto pairs labelled `SWITCH 35 TROUGH 4`, `SWITCH 34 TROUGH 3`, `SWITCH 33 TROUGH 2`, `SWITCH 32 TROUGH 1`, `SWITCH 31 TROUGH
EJECT` (LED above, photo transistor below). `PHOTO TRANSISTOR BOARD` `J1` pins 1, 3, 4, 5, 6, 7 wired `GRY-YEL, +12V`, `ORG-BRN`, `ORG-RED`, `ORG-BLK`, `ORG-YEL`,
`ORG-GRN` to `7-OPTO SWITCH BOARD` `J2` pins 1, 10, 9, 8, 7, 6 (as drawn; the lists on `3-16` and `3-18` put the same wires on `J2` pins 9/10 (+12V) and 7, 6, 5, 4, 3, see below). The per-switch wire assignment is printed on `3-18`: switch 35 (Trough 4) `GRY-GRN` / `ORG-GRN`, 34 `GRY-BLK` / `ORG-YEL`, 33 `GRY-ORG` / `ORG-BLK`, 32 `GRY-RED` / `ORG-RED`, 31 `GRY-BRN` / `ORG-BRN`; this drawing labels wire colours at the connectors only, not beside the individual opto pairs. Bold text under the second diagram: `THE BALL ROLLS BETWEEN THE LED BOARD AND THE PHOTO TRANSISTOR BOARD, BREAKING THE BEAM.
WHEN THE BEAM IS BROKEN THE SWITCH IS MADE.`

`Center Ramp Opto and Right Loop Enter Opto Switches Wiring Diagram`: `SWITCH 36 CENTER RAMP OPTO` (photo transistor `ORG-BLU` to `7-OPTO SWITCH BOARD` `J2` pin 2; LED `GRY-BLU` to `J1`
pin 2), `SWITCH 37 RIGHT LOOP ENTER OPTO` (photo transistor `ORG-VIO` to `J2` pin 1; LED `GRY-VIO` to `J1` pin 1), common `GRY-YEL` to `J2` pin 9 and `BLK` to `J1` pin 9;
`7-OPTO SWITCH BOARD` `J3`: pin 1 `GRY-YEL +12V` to `POWER DRIVER BOARD J139` pin 2, pin 3 `BLK GRD` to `J139` pin 3, pins 5-11 `WHT-BRN ROW 1`, `WHT-RED ROW 2`, `WHT-ORG ROW 3`,
`WHT-YEL ROW 4`, `WHT-GRN ROW 5`, `WHT-BLU ROW 6`, `WHT-VIO ROW 7` to `CPU BOARD J208` pins 1, 2, 3, 4, 5, 7, 8, and pin 12 `GRN-ORG COL. 3` to `J206` pin 3.

## Printed page 3-18: 7-Opto Switch Board Assembly A-15576.1

Title line: `(FOR BALL TROUGH, CENTER RAMP OPTO, AND RIGHT LOOP ENTER OPTO SWITCHES)`.

| Pin | Wire | Text |
| --- | --- | --- |
| J1-1 | GRY-VIO | To switch #37, RIGHT LOOP ENTER OPTO LED board |
| J1-2 | GRY-BLU | To switch #36, CENTER RAMP OPTO LED board |
| J1-3 | GRY-GRN | To switch #35, BALL TROUGH, LED board |
| J1-4 | N/C | (blank) |
| J1-5 | GRY-BLK | To switch #34, BALL TROUGH LED board |
| J1-6 | GRY-ORG | To switch #33, BALL TROUGH LED board |
| J1-7 | GRY-RED | To switch #32, BALL TROUGH LED board |
| J1-8 | GRY-BRN | To switch #31, BALL TROUGH LED board |
| J1-9 | BLK | Ground to LED boards |
| J1-10 | BLK | Ground to LED boards |
| J2-1 | ORG-VIO | To switch #37, RIGHT LOOP ENTER PHOTO TRANS. board |
| J2-2 | ORG-BLU | To switch #36, CENTER RAMP OPTO PHOTO TRANS. board |
| J2-3 | ORG-GRN | To switch #35, BALL TROUGH PHOTO TRANS. board |
| J2-4 | ORG-YEL | To switch #34, BALL TROUGH PHOTO TRANS. board |
| J2-5 | ORG-BLK | To switch #33, BALL TROUGH PHOTO TRANS. board |
| J2-6 | ORG-RED | To switch #32, BALL TROUGH PHOTO TRANS. board |
| J2-7 | ORG-BRN | To switch #31, BALL TROUGH PHOTO TRANS. board |
| J2-8 | N/C | (blank) |
| J2-9 | GRY-YEL | +12V to PHOTO TRANS. boards |
| J2-10 | GRY-YEL | +12V to PHOTO TRANS. boards |
| J3-1 | GRY-YEL | +12V from POWER DRIVER board J139-2 |
| J3-2 | N/C | (blank) |
| J3-3 | BLK | Ground from POWER DRIVER board J139-3 |
| J3-4 | N/C | (blank) |
| J3-5 | WHT-BRN | Switch Row 1, from CPU board J208-1 |
| J3-6 | WHT-RED | Switch Row 2, from CPU board J208-2 |
| J3-7 | WHT-ORG | Switch Row 3, from CPU board J208-3 |
| J3-8 | WHT-YEL | Switch Row 4, from CPU board J208-4 |
| J3-9 | WHT-GRN | Switch Row 5, from CPU board J208-5 |
| J3-10 | WHT-BLU | Switch Row 6, from CPU board J208-7 |
| J3-11 | WHT-VIO | Switch Row 7, from CPU board J208-8 |
| J3-12 | GRN-ORG | Switch Column 3, from CPU board J206-3 |

The trough optos (31-35) are thus all in matrix column 3 (`GRN-ORG`, `J206-3`) rows 1-5, with `Switch Row 6` (`J208-7`) and `Switch Row 7` (`J208-8`)
carrying switches 36 and 37. Printed anomalies: on this page `J1-3` prints a comma after `BALL TROUGH` (`BALL TROUGH, LED board`). The 7-Opto `J1` pin numbers of the LED wires
disagree between pages: this list puts `GRY-GRN` (switch 35) on `J1-3`, `J1-4` `N/C`, `GRY-BLK` on `J1-5`, `GRY-ORG` on `J1-6`, `GRY-RED` on `J1-7` and `GRY-BRN`
on `J1-8`, whereas the Trough IR LED Board list (`3-15`) sends `GRY-GRN` to `7-Opto J1-4`, `GRY-BLK` to `J1-5`, `GRY-ORG` to `J1-6`, `GRY-RED` to `J1-7`, `GRY-BRN` to `J1-8`, and the `3-17`
drawing prints `7-OPTO SWITCH BOARD J1` pins 4, 5, 6, 7, 9, 10 for `GRY-GRN`, `GRY-BLK`, `GRY-ORG`, `GRY-RED`, `GRY-BRN`, `BLK, GROUND`. The wire colours per switch are
consistent in all three places. For the photo-transistor wires, this list and `3-16` put `ORG-GRN` ... `ORG-BRN` on `J2-3` ... `J2-7`, while the `3-17` drawing prints `J2` pins 6-10.

## Printed page 3-19: 7-Opto Switch Board Schematic A-15576.1

Title lines `7-Opto Switch Board Schematic`, `A-15576.1`, `(FOR BALL TROUGH, CENTER RAMP OPTO, AND RIGHT LOOP ENTER OPTO SWITCHES)`. A schematic: LM339 comparators `U1A`-`U1D` and `U2A`-`U2D` (resistor pairs `2K`, `1N4004` diodes `D2`-`D8`, `D9`, `R26` `100K`, `R28` `22K`, `R23` `100K`),
`J1` labelled `Cathodes` / `Cathodes A1 ... A7` / `key` with `270` ohm resistors `R15`-`R21`, `J2` labelled `Collectors` / `Collectors` / `key` / `E1 ... E7`, and `J3` (`Col`, rows). No text beyond part and signal labels.

## Printed page 3-20: 24-Opto Switch Board Assembly A-15646

Title line: `(FOR BASKET MADE OPTO SWITCH)`.

| Pin | Wire | Text |
| --- | --- | --- |
| J1-1 | ORG | To switch #F5, BASKET MADE OPTO PHOTO TRANS. board |
| J1-2 | N/C | (blank) |
| J1-3 | GRY-YEL | To switch #F5, BASKET MADE OPTO PHOTO TRANS. board |
| J2-1 | BLK | To switch #F5, BASKET MADE OPTO LED board |
| J2-2 | BLK-VIO | To switch #F5, BASKET MADE OPTO LED board |
| J3-1 | BLK-VIO | From CPU board J208-11 |
| J3-2 | N/C | (blank) |
| J3-3 | ORG | From CPU board J212-13 |
| J3-4 | BLK | Ground from POWER DRIVER board J139-3 |
| J3-5 | GRY-YEL | +12V from POWER DRIVER board J139-2 |

Wiring drawing: `BASKET MADE OPTO SWITCH` opto (photo transistor on `ORG` `J1` pin 1 and `GRY-YEL` pin 3; LED on `BLK` `J2` pin 1 and `BLK-VIO` pin 2) to the `24-OPTO SWITCH BOARD` `J1`, `J2`, `J3`;
`J3` pin 1 `SWITCH F5` `BLK-VIO` to `CPU BOARD` `J208` pin 11, pin 3 `GRD` `ORG` to `J212` pin 13, pin 4 `GRD` `BLK` to `POWER DRIVER BOARD` `J139` pin 3, pin 5 `+12V` `GRY-YEL` to `J139` pin 2.
The Switch Locations list names the assembly `A-16908 (LED) / A-16909 (PHOTO TRANS)` for F5.

## Printed page 3-21: 24-Opto Switch Board Schematic A-15646

Title lines `24-Opto Switch Board Schematic`, `A-15646`, `(FOR BASKET MADE OPTO SWITCH)`. A schematic rotated 90 degrees on the page (`MC3373` `U1`, `LM555` `U3`, `4N25` `U2`, `PNP DAR` `Q1`, `1N4004` `D1`-`D3`, `10mH` `L1`, `LED1`); connector labels: `J3` `+12 VDC GND KEY ROW COLUMN` (pins 5 4 2 1 3, `.156`),
`J1` `C KEY E` (pins 3 2 1), `J2` `A K` (pins 2 1). No text beyond part and signal labels.

## Printed page 3-22: LED Board Assembly A-16908 and Photo Transistor Board Assembly A-16909

`LED BOARD ASSEMBLY A-16908 (TRANSMITTER-GREEN BOARD)`: solder side (`A` `K`), component side, schematic (diode). `PHOTO TRANSISTOR BOARD ASSEMBLY A-16909 (RECEIVER-BLUE BOARD)`: solder side
(`C` `E`), component side, schematic. `TYPICAL CIRCUIT DIAGRAM`: `LED BOARD Transmitter 1.0-1.4 volts` (wires `Gray-XXX`, `Black, Ground`) and `PHOTO TRANSISTOR BOARD Receiver
0.1-0.7 volts unblocked 11-13 volts blocked` (wires `Gray-Yellow, +12V`, `Orange-XXX`); photographs of the two boards labelled `Green`, `Gray`, `Black`, `Solder`, `White`,
`Infrared Beam`, `Blue`, `Orange`, `Gray-Yellow`. There are no connector pin tables on this page.

## Printed page 3-23: Defender Switch Board A-21402

Title line: `(FOR DEFENDER POSITIONS AND DEFENDER LOCK OPTO SWITCHES)`. Board layout (`U1`-`U5`, `Q1`-`Q5`, `J1`) and schematic: five optos (`U1`-`U5`, each with `680` LED resistor and `2.2K`
resistors) driving `Q1`-`Q5` with diodes `D1`-`D10` onto `J1`; `J1` legend `+12V GND Key COL ROW1 ROW2 ROW3 ROW4 ROW5`; each opto labelled `STOPTO`.

| Pin | Wire | Text |
| --- | --- | --- |
| J1-1 | GRY-YEL | +12V from POWER DRIVER board J139-2 |
| J1-2 | BLK | Ground from POWER DRIVER board J139-3 |
| J1-3 | N/C | (blank) |
| J1-4 | GRN-BLK | Switch Column 5, from CPU board J206-5 |
| J1-5 | WHT-BRN | Switch Row 1, from CPU board J208-1 |
| J1-6 | WHT-RED | Switch Row 2, from CPU board J208-2 |
| J1-7 | WHT-ORG | Switch Row 3, from CPU board J208-3 |
| J1-8 | WHT-YEL | Switch Row 4, from CPU board J208-4 |
| J1-9 | WHT-GRN | Switch Row 5, from CPU board J208-5 |

Wiring drawing: `POWER DRIVER BOARD J139` pins 2, 3 (`+12V GRY-YEL`, `GRD BLK`) and `CPU BOARD` `J206` pin 5 (`COL. 5 GRN-BLK`), `J208` pins 1-5 (`ROW 1` to `ROW 5`,
`WHT-BRN` ... `WHT-GRN`) to the `DEFENDER SWITCH BOARD` `J1` pins 1, 2, 4, 5-9. The page does not name which of the five optos is `Defender Position 1` to `4` or `Defender Lock`
beyond the rows (the Switch Matrix names 51-55, rows 1-5 of column 5, `DEFENDER POSITION 4`, `3`, `LOCK POSITION`, `2`, `1`).

## Printed page 3-24: 2 LED Driver Board A-21399 (for shot clock)

Board layout (`U1`-`U5`, `Q1`, `J1`, `J2`) and schematic (LM339 `U1A`-`U1C`, `4029B` `U3` and `U2`, `HEF4511B` `U5` and `U4`, `LM7812` `Q1`, `1N5817` `D2`/`D3`, `470` ohm segment resistors). Connectors:

| Pin | Wire | Text |
| --- | --- | --- |
| J1-1 | GRY-YEL | +12V from POWER DRIVER board J139-2 |
| J1-2 | BLK | Ground from POWER DRIVER board J139-3 |
| J1-3 | N/C | (blank) |
| J1-4 | YEL-WHT | solenoid #39, SHOT CLOCK ENABLE, from POWER DRIVER board J110-4 |
| J1-5 | BLU-WHT | solenoid #40, SHOT CLOCK COUNT, from POWER DRIVER board J110-5 |
| J2 | (single line) | Connected directly to J1 on 2 LED DISPLAY board |

The schematic's `J1` connector side labels read `COUNT`, `BLANKING`, `N.C.`, `GND`, `+12V` (small print, pins 5 down to 1).

## Printed page 3-25: 2 LED Display Board A-21380 (for shot clock)

Board drawing: `DISPLAY1`, `DISPLAY2`, `J1`. Schematic: `DISPLAY 2` (`ONES DIGET`) and `DISPLAY 1` (`TENS DIGIT`) seven-segment displays (display part label partly blurred, reads `LMNS-1805DR`) with
segment pins `F-SEG G-SEG A-SEG B-SEG C-SEG D-SEG E-SEG DP CATH CATH` wired to `J1` (`HEADER 16`, labels `GND 1F 1G 1A 1B 1C 1D 1E 2F 2G 2A 2B 2C 2D 2E GND`, pins 1-16). The
spelling `ONES DIGET` is as printed. Text: `J1 Connected directly to J2 on 2 LED DRIVER Board`.

`SHOT CLOCK ASSEMBLY` wiring: `POWER DRIVER BOARD J139` pins 2 (`+12V GRY-YEL`), 3 (`GRD BLK`) and `J110` pins 4 (`SOL. 39 YEL-WHT`), 5 (`SOL. 40 BLU-WHT`) to the assembly's `J1` pins 1, 2, 4, 5;
the assembly holds the `2 LED DRIVER BOARD` (`J2`) and `2 LED DISPLAY BOARD` (`J1`) joined by their connectors.

No explanatory text describing how the shot clock counts is printed on pages 3-24 or 3-25 beyond the connector lists and the wiring diagram. The only functional statements are the pin
names `solenoid #39, SHOT CLOCK ENABLE` and `solenoid #40, SHOT CLOCK COUNT`, the matching Solenoid/Flasher Table rows (`SHOT CLOCK ENABLE` 39, `SHOT CLOCK COUNT` 40,
`Low Power`, gates `U3G, U3H` and `U3E, U3F`, `J110-4` `YEL-WHT` and `J110-5` `BLU-WHT`, device `A-21380`) and the table's bold line `SHOT CLOCK WIRING DIAGRAM IS SHOWN ON PAGE 3-25.`

## Printed page 3-26: High Current Driver Board C-13963-1 (for motor)

Board layout and schematic (`LM339` `U1A`-`U1D`, `TIP102` `Q1`/`Q3`, `TIP107` `Q2`/`Q4`/`Q5`, `1N4004` `D1`-`D4`, `L1`/`L2` inductors, `W1`-`W3`, `R9` `Not Inserted`, `C1 1uF`). Connectors:

| Pin | Wire | Text |
| --- | --- | --- |
| J1-1 | BRN-WHT | solenoid #37, MOTOR ENABLE, from POWER DRIVER board J110-1 |
| J1-2 | ORG-WHT | solenoid #38, MOTOR DIRECTION, from POWER DRIVER board J110-3 |
| J1-3 | N/C | (blank) |
| J1-4 | BLK | Ground from POWER DRIVER board J139-3 |
| J1-5 | GRY-YEL | +12V from POWER DRIVER board J139-2 |
| J2-1 | RED | MOTOR + |
| J2-2 | N/C | (blank) |
| J2-3 | BLK | MOTOR - |
| J2-4 | N/C | (blank) |

The schematic's `J1` side is labelled `+12 VDC GND KEY DRIVER UP/DN ENABLE` and its `J2` side `MOTOR + KEY MOTOR - N/C`. Wiring drawing: `POWER DRIVER BOARD J139` pins 2, 3 (`+12V GRY-YEL`,
`GRD BLK`) and `J110` pins 3, 1 (`SOL. 38 ORG-WHT`, `SOL. 37 BRN-WHT`) to the `HIGH CURRENT DRIVER BOARD` `J1` pins 5, 4, 2, 1; `J2` pin 1 `RED +` to the `MOTOR` and pin 3 `BLACK`.
No explanatory text describing the defender motor's operation is printed; the only functional statements are the pin names `MOTOR ENABLE` / `MOTOR DIRECTION`, the schematic's
`DRIVER UP/DN` and `ENABLE` labels, and the Solenoid/Flasher Table's bold line `MOTOR WIRING DIAGRAM IS SHOWN ON PAGE 3-26.` The manual's page 3-26 does not name this motor as the defender motor
(the word `defender` does not appear on `3-26`); the Switch Matrix and the Defender Switch Board name the `DEFENDER POSITION` and `DEFENDER LOCK POSITION` opto switches.

## Printed page 3-27: Security CPU Board Assembly A-21377-50053

Board layout showing `J201` (`I/O EXTEND`), `J202` (`TO I/O SOUND`), `J210`, `J211` (`TO PWR/DRV/FLIP PCB`), `J212` (`CABINET`), `J206` (`PLFD COL`), `J208` (`PLFD ROWS`), `J205` (`DIRECT SW INPUTS`),
`J207` (`B.B. COL`), `J209` (`B.B. ROWS`), battery `B1`, test points `POWER`, `DIAG`, `BLANKING`. Connector list, as printed:

```
J201, 26-pin ribbon cable, data to/from J602
J202, 34-pin ribbon cable, data to/from J601
J203 & J204 - NOT USED

J205-1  ORG-BRN, ded. sw. row 1, to Coin Door Brd J1-8
J205-2  ORG-RED, ded. sw. row 2, to Coin Door Brd J1-7
J205-3  ORG-BLK, ded. sw. row 3, to Coin Door Brd J1-6
J205-4  ORG-YEL, ded. sw. row 4, to Coin Door Brd J1-5
J205-5  N/C
J205-6  ORG-GRN, ded. sw. row 5, to Coin Door Brd J1-4
J205-7  ORG-BLU, ded. sw. row 6, to Coin Door Brd J1-3
J205-8  ORG-VIO, ded. sw. row 7, to Coin Door Brd J1-2
J205-9  ORG-GRY, ded. sw. row 8, to Coin Door Brd J1-1
J205-10 BLK, ground, to Coin Door Brd J1-10
J205-11 KEY
J205-12 ORG-WHT, switch enable, to Coin Door Brd J1-11

J206-1  GRN-BRN, switch column 1, to playfield switches
J206-2  GRN-RED, switch column 2, to playfield switches
J206-3  GRN-ORG, switch column 3, to playfield switches
J206-4  GRN-YEL, switch column 4, to playfield switches
J206-5  GRN-BLK, switch column 5, to playfield switches
J206-6  GRN-BLU, switch column 6, to playfield switches
J206-7  N/C
J206-8  KEY
J206-9  N/C

J207-1  GRN-BRN, switch column 1 to Insert Panel switch
J207-2  N/C
J207-3  N/C
J207-4  N/C
J207-5  N/C
J207-6  N/C
J207-7  N/C
J207-8  Key
J207-9  N/C

J208-1  WHT-BRN, switch row 1, to playfield switches
J208-2  WHT-RED, switch row 2, to playfield switches
J208-3  WHT-ORG, switch row 3, to playfield switches
J208-4  WHT-YEL, switch row 4, to playfield switches
J208-5  WHT-GRN, switch row 5, to playfield switches
J208-6  KEY
J208-7  WHT-BLU, switch row 6, to playfield switches
J208-8  WHT-VIO, switch row 7, to playfield switches
J208-9  WHT-GRY, switch row 8, to playfield switches
J208-10 BLK-GRY, F7 to Basket Hold switch
J208-11 BLK-VIO, F5 to Basket Made Opto switch
J208-12 BLK-BLU, F3 to lower left E.O.S. switch
J208-13 BLK-GRN, F1 to lower right E.O.S. switch
J208-14 ORG, ground to E.O.S. switches

J209-1  WHT-RED, switch row 1, to Insert Panel switch
J209-2
J209-3
J209-4
J209-5
J209-6
J209-7
J209-8
J209-8

J210-1  BLK, ground, from Power Driver Board J101-5,7
J210-2  KEY
J210-3  BLK, ground, from Power Driver Board J101-5, 7
J210-4  GRY, +5V, from Power Driver Board J101-3, 4
J210-5  GRY, +5V, from Power Driver Board J101-3, 4
J210-6  GRY-GRN, +12V, from Power Driver Board J101-1, 2
J210-7  GRY-GRN, +12V, from Power Driver Board J101-1, 2

J211, 34-pin ribbon cable, data to/from J102

J212-1  GRN-BRN, switch col. 1, to coin door board J3-1
J212-2  GRN-RED, switch col. 2, to coin door board J3-2
J212-3  N/C
J212-4  WHT-BRN, switch row 1, to coin door board J3-3
J212-5  KEY
J212-6  WHT-RED, switch row 2, to coin door board J3-4
J212-7  WHT-ORG, switch row 3, to coin door board J3-5
J212-8  WHT-YEL, switch row 4, to coin door board J3-6
J212-9  BLK-BLU, F8, to left flipper opto board J1-1
J212-10 BLK-YEL, F6, to right flipper opto board J1-1
J212-11 BLU-GRY, F4, to left flipper opto board J1-2
J212-12 BLU-VIO, F2, to right flipper opto board J1-2
J212-13 ORG, Ground to left flipper opto board J1-4
```

Printed anomalies: `J209-2` through `J209-8` are printed as bare pin numbers with no text (blank cells), and the pin `J209-8` is printed twice (second one in place of `J209-9`); the `J206-1` and `J206-2` lines stand at the
bottom of the left column of the page and the list continues at `J206-3` at the top of the right column; the `J210-1` line prints `J101-5,7` without a space where `J210-3` prints `J101-5, 7`.

## Printed page 3-28: Audio Visual Board Assembly A-20516-50053

Connector list, as printed (no game devices; summarised): `J601`, 34-pin ribbon cable, data to CPU `J202`; `J602`, 26-pin ribbon cable, data to CPU `J201`; `J603`, 14-pin ribbon cable, data to/from dot matrix
display driver; `J604` 1-8 (`ORG, -125V to display driver pin1`, `BLU, -113V to display driver pin 2`, `KEY`, `BLK, ground to display driver pin 4`, `BLK, ground to display driver pin 5`, `GRY, +5V to display driver pin 6`,
`GRY-YEL, +12 to display driver pin 7`, `BRN, +62 to display driver pin 8`); `J605` 1-11 (`WHT, 80VAC from transformer secondary` x2, `VIO, 100VAC from transformer secondary` x2, `GRY-WHT, 18VAC from transformer
secondary`, `GRY-WHT, loop from J605-5`, `GRY, 18VAC from transformer secondary`, `GRY, loop from J605-7`, `KEY`, `GRY-GRN, 18VAC from transformer secondary`, `GRY-GRN, 18VAC loop from J605-10`); `J606` 1-7 (ground `BLK` from power
driver board `J101-7` and `J101-5`, `GRY` +5V from `J101-4` and `J101-3`, `GRY-GRN` +12V from `J101-2` and `J101-1`, `KEY`); `J607 NOT USED`; `J504` 1-4 (`BLK-YEL, signal to speaker`, `KEY`, `N/C`, `BLK, signal to speaker`);
`J505` 1-4 (`BLK-YEL, signal to speaker`, `N/C`, `KEY`, `BLK, signal to speaker`). No pin of this board names a playfield switch, lamp or solenoid.

## Printed pages 3-32 and 3-33: Coin Door Interface Board A-20580 and schematic

Connector list on `3-32` as printed:

```
J1-1  ORG-GRY, ded. switch row 8 form CPU J205-9
J1-2  ORG-VIO, ded. switch row 7 from CPU J205-8
J1-3  ORG-BLU, ded. switch row 6 from CPU J205-7
J1-4  ORG-GRN, ded. switch row 5 from CPU J205-6
J1-5  ORG-YEL, ded. switch row 4 from CPU J205-4
J1-6  ORG-BLK, ded. switch row 3 from CPU J205-3
J1-7  ORG-RED, ded. switch row  2 from CPU J205-2
J1-8  ORG-BRN, ded. switch row  1 from CPU J205-1
J1-9  KEY
J1-10 BLK, ground from CPU J205-10
J1-11 ORG-WHT, switch enable from CPU J205-12

J2-1  BLK, ground from Power Driver Board J141-3
J2-2  GRY-YEL, +12vac for Power Driver Board J141-2
J2-3  WHT-VIO, G.I. 6.8vac from Power Driver J104-1
J2-4  KEY
J2-5  VIO, G.I. from Power Driver Board J104-3
J2-6  N/C
J2-7  BLK-WHT, signal for coin meter from Power Driver board J139-5

J3-1  GRN-BRN, switch column 1 from CPU J212-1
J3-2  GRN-RED, switch column 2 from CPU J212-2
J3-3  WHT-BRN, switch row 1 from CPU J212-4
J3-4  WHT-RED, switch row 2 from CPU J212-6
J3-5  WHT-ORG, switch row 3 from CPU J212-7
J3-6  WHT-YEL, switch row 4 from CPU J212-8
J3-7  KEY
J3-8  YEL-GRY, lamp col. 8 from Power Driver J122-3
J3-9  RED-BLU, lamp row 6 from Power Driver J125-7
J3-10 RED-VIO, lamp row 7 from Power Driver J125-8
J3-11 RED-GRY, lamp row 8 from Power Driver J125-9

J4- NOT USED

J5-1  VIO, G.I. return to coin door
J5-2  WHT-VIO, G.I. 6.8vac to coin door
J5-3  BLK, ground to coin door
J5-4  ORG-BRN, ded. switch row 1 to coin door
J5-5  ORG-RED, ded. switch row 2 to coin door
J5-6  ORG-BLK, ded. switch row 3 to coin door
J5-7  ORG-GRN, ded. switch row 5 to coin door
J5-8  ORG-BLU, ded. switch row 6 to coin door
J5-9  ORG-VIO, ded. switch row 7 to coin door
J5-10 KEY
J5-11 ORG-GRY, ded. switch row 8 to coin door
J5-12 GRN-RED, switch column 2 to coin door Slam Tilt
J5-13 WHT-BRN, switch row 1 to coin door Slam Tilt

J6- NOT USED

J7-1  YEL-GRY, lamp column 8 to cabinet
J7-2  N/C
J7-3  N/C
J7-4  RED-GRY, lamp row 8 to cabinet
J7-5  KEY
J7-6  GRN-BRN, switch column 1 to cabinet
J7-7  N/C
J7-8  N/C
J7-9  N/C
J7-10 N/C
J7-11 WHT-ORG, switch row 3 to cabinet
J7-12 N/C
J7-13 N/C

J8-1  WHT, switch row to cabinet Slam Tilt
J8-2  KEY
J8-3  GRN, switch column to cabinet Slam Tilt

J9-1  WHT-YEL, switch row 4 to Plumb Bob Tilt
J9-2  KEY
J9-3  GRN-BRN, switch column 1 to Plumb Bob Tilt
J9-4  WHT-RED, switch row 2 to Interlock Switch
J9-5  GRN-RED, switch column 2 to Interlock Switch

J10,  Ribbon cable to cash flow coin mechanism.
```

Printed anomalies: `J1-1` reads `form CPU` (for `from`); `J5` has no `ded. switch row 4` pin (`J5-6` is row 3 and `J5-7` is row 5; the CPU `J205-4`, `ORG-YEL`, row 4, is the `4th Coin Chute` D4 and
reaches `J1-5` only); `J7-4` `RED-GRY lamp row 8 to cabinet` and `J7-1` `YEL-GRY lamp column 8 to cabinet` carry cabinet lamp 88; the `J7-11 WHT-ORG switch row 3 to cabinet` with `J7-6 GRN-BRN switch column 1` addresses matrix switch
13 on the cabinet (`START BUTTON`). `J2-3` and `J2-5` print the G.I. wires as `WHT-VIO, G.I. 6.8vac` and `VIO, G.I.`. The `3-33` page is the board schematic (labelled connectors `J1`-`J11`, a coin counter `CNTR1`, `SW5`, `J4` `NRI INTERFACE`, `J5` `COIN DOOR`, `J6` `ECA COIN DOOR`, `J10` `RS232 INTERFACE from A/V`, `J11` `RS232 OUT INTERFACE`, `J1` `DEDICATED SW.`); it carries no text beyond the part and signal labels (`DIG. SW4`...`DIG. SW1`, `COIN 4`, `COIN 3 (RIGHT)`, `COIN 2 (CENTER)`, `COIN 1 (LEFT)`, `KEY`, `GND`, `ENABLE`, `SLAM SW ROW 1`, `SLAM SW COL 2`, `SW1`-`SW4`, `G.I. LAMP`, `+12V`, `COIN COUNTER`).

## Defender motor, shot clock and backbox basket: printed explanatory text

The manual's Section 3 pages contain no prose that describes how the defender motor, the shot clock or the backbox basket work. The printed functional information is exactly the following:

- Defender motor: `High Current Driver Board C-13963-1 (FOR MOTOR)`; `J1-1 BRN-WHT solenoid #37, MOTOR ENABLE`; `J1-2 ORG-WHT solenoid #38, MOTOR DIRECTION`; `J2-1 RED MOTOR +`; `J2-3 BLK MOTOR -`;
  schematic labels `DRIVER UP/DN` and `ENABLE`; the Solenoid/Flasher Table rows `37 MOTOR ENABLE` and `38 MOTOR DIRECTION` (Low Power, `U3A, U3B` and `U3C, U3D`, `J110-1` `BRN-WHT` and `J110-3` `ORG-WHT`, device `14-8034`
  (and `14-8043` on the locations list for item 38)); the Switch Matrix `DEFENDER POSITION 4`, `DEFENDER POSITION 3`, `DEFENDER LOCK POSITION`, `DEFENDER POSITION 2`, `DEFENDER POSITION 1` opto cells 51-55 on the
  Defender Switch Board A-21402 (`FOR DEFENDER POSITIONS AND DEFENDER LOCK OPTO SWITCHES`).
- Shot clock: `2 LED Driver Board A-21399 (FOR SHOT CLOCK)` and `2 LED Display Board A-21380 (FOR SHOT CLOCK)` (a two-digit display, `TENS DIGIT` and `ONES DIGET`); `solenoid #39, SHOT CLOCK ENABLE` and `solenoid #40,
  SHOT CLOCK COUNT`; the Solenoid/Flasher Table rows 39 and 40.
- Backbox basket: Switch Matrix `F5 BASKET MADE OPTO` (24-Opto Switch Board A-15646, wired to `J208-11` and `J212-13`), `F7 BASKET HOLD` (`J208-10`, a mechanical switch `5647-12693-04`) and cell `12 BACKBOX BASKET`
  (assembly `A-21710`, switch `5647-12693-19`); `07 BACKBOX FLIPPER` coil (`J117-3`, `FL-11753`, `J133-2` / `J117-3`, in the insert panel) and `08 BALL CATCH MAGNET` (`J116-9`, `B-13522`); the Flipper Circuit Diagram's
  footnote `* INDICATES A FLIPPER CIRCUIT USED FOR ANOTHER PURPOSE` against `BASKET MADE OPTO` / `BASKET HOLD` and `SHOOT 1` to `SHOOT 4`.

## Uncertain readings

- Printed page 3-12 (Flipper Coil Circuits drawing): small print; the wire colours and pin numbers listed are read at the limit of the 300 dpi scan and were cross-checked against `3-11` and the CPU connector list; the
  `E.O.S.` captions on `J208` pins 10 and 11 were read as `UPPER LEFT E.O.S. SWITCH` / `UPPER RIGHT E.O.S. SWITCH` in the left and right drawings respectively.
- Printed pages 3-19 and 3-21 schematics: part values and pin legends are small print; only the connector legends given above were read, and none was used as evidence of a device identity.
- The `J1` connector side legend of the 2 LED Driver schematic (`COUNT`, `BLANKING`, `N.C.`, `GND`, `+12V`) is very small print.
