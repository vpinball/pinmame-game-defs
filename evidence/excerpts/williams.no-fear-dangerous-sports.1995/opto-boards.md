# No Fear: Dangerous Sports — Flipper opto, trough and 16-opto boards

From `Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf` (operations manual 16-50025-101, April 1995, a 144-page scan without a text layer; SHA-256 `176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b`), PDF pages 127-134 (printed 3-14 to 3-21: Flipper Opto Board A-17316, Outhole Trough Block Diagram, Trough IR LED and photo transistor boards A-18617-1 and A-18618-1, single LED and photo transistor boards A-16908 and A-16909, 16-Opto Switch Board A-16998.1 wiring, assembly and schematic) and PDF pages 84-85 (printed 2-11 and 2-12, the trough board and 16-opto parts lists). Transcribed from the 200 dpi renders by a delegated reader and not yet checked line by line against the page by the curator. Wire colours, abbreviations and punctuation as printed; "Key", "N/C" and "Not Used" kept as printed. Cells are kept as printed, including misspellings and abbreviations; `—` marks a cell that is blank on the page. `p-NNN` is the PDF page; the printed page number follows it.

## PDF p-127 [3-14] Flipper Opto Board Assembly, A-17316

Drawing: board outline with two opto slots OPTO1 and OPTO2, resistors R1 and R2, connector J1 (7 pins, labels beside the footprint: SW1, SW2, GND, GND, KEY, +12V, +12V). Schematic below: R1 470 ohm and R2 470 ohm from +12V each feed an IR LED; each LED faces a photo transistor (OPTO1, OPTO2); OPTO1 collector side to J1-1 "SW1", OPTO2 to J1-2 "SW2"; emitters to GND; J1 pin labels: 7 +12V, 6 +12V, 5 KEY, 1 SW1, 2 SW2, 3 GND, 4 GND. Schematic text printed "R1 470 Ω", "R2 470 Ω".

Left Flipper Opto Board Assembly

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-1 | Black-Blue | from Fliptronic II Board J905-5 |
| J1-2 | Blue-Gray | from Fliptronic II Board J905-2 |
| J1-3 | | N/C |
| J1-4 | Orange | from Fliptronic II Board J905-6 |
| J1-5 | | N/C |
| J1-6 | Gray-Yellow | from Power Driver Board J116-2 |
| J1-7 | Gray-Yellow | from Power Driver Board J116-2 |

Right Flipper Opto Board Assembly

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-1 | Black-Yellow | from Fliptronic II Board J905-1 |
| J1-2 | Blue-Violet | from Fliptronic II Board J905-3 |
| J1-3 | Orange | from Fliptronic II Board J905-6 |
| J1-4 | Orange | from Left Flipper Opto Board Assy J1-4 |
| J1-5 | | N/C |
| J1-6 | Gray-Yellow | from Left Flipper Opto Board Assy J1-6 |
| J1-7 | | N/C |

Note: the printed J905 pin numbers in these two lists (J905-1/-3 for right, -5/-2 for left) differ from the Fliptronic II page's J905 list (J905-1 right J1-2, J905-3 right J1-1, J905-2 left J1-2, J905-5 left J1-1). Both are as printed.

## PDF p-128 [3-15] Outhole Trough Block Diagram

Drawing: block diagram. Four boxes at left: TROUGH IR LED BOARD (GREEN BOARD) J1; TROUGH IR PHOTO TRANSISTOR BOARD (BLUE BOARD) J1; POWER DRIVER BOARD J118 (with J113 ribbon to CPU J211); CPU BOARD J209 and J207. Right: 16-OPTO SWITCH BOARD with J1, J2, J5. Wires labelled as below. Lower part: a typical LED / photo transistor pair with the beam between them. Printed note: "IN THE OUTHOLE TROUGH CIRCUIT, THE BALL ROLLS BETWEEN THE TROUGH IR LED BOARD AND THE TROUGH IR PHOTO TRANSISTOR BOARD AND BREAKS THE BEAM. WHEN THE BEAM IS BROKEN, THE SWITCH IS READ AS MADE."

| From (box pin) | Wire | Label | To 16-Opto pin |
| --- | --- | --- | --- |
| LED board J1-9 | BLK | GROUND | J1-10 |
| LED board J1-7 | GRY-BRN | LED 1 | J1-9 |
| LED board J1-6 | GRY-RED | LED 2 | J1-7 |
| LED board J1-5 | GRY-ORG | LED 3 | J1-6 |
| LED board J1-4 | GRY-BLK | LED 4 | J1-5 |
| LED board J1-3 | GRY-GRN | LED 5 | J1-4 |
| Photo transistor board J1-1 | GRY-YEL | +12v | J2-1 |
| Photo transistor board J1-3 | ORG-BRN | PHOTO TRANSISTOR 1 | J2-10 |
| Photo transistor board J1-4 | ORG-RED | PHOTO TRANSISTOR 2 | J2-9 |
| Photo transistor board J1-5 | ORG-BLK | PHOTO TRANSISTOR 3 | J2-8 |
| Photo transistor board J1-6 | ORG-YEL | PHOTO TRANSISTOR 4 | J2-7 |
| Photo transistor board J1-7 | ORG-GRN | PHOTO TRANSISTOR 5 | J2-6 |
| Power Driver J118-2 | GRY-YEL | +12V | J5-12 |
| Power Driver J118-3 | BLK | GND | J5-13 |
| CPU J209-1 | WHT-BRN | SW. ROW 1 | J5-1 |
| CPU J209-2 | WHT-RED | SW. ROW 2 | J5-2 |
| CPU J209-3 | WHT-ORG | SW. ROW 3 | J5-3 |
| CPU J209-4 | WHT-YEL | SW. ROW 4 | J5-4 |
| CPU J209-5 | WHT-GRN | SW. ROW 5 | J5-5 |
| CPU J207-3 | GRN-ORG | SW. COL. 3 | J5-9 |
| CPU J207-4 | GRN-YEL | SW. COL. 4 | J5-10 |

Lower diagram labels: "TROUGH IR LED BOARD", "REPEATED FOR ALL FIVE LEDS." with GRY-GRN LED5, GRY-BLK LED4, GRY-ORG LED3, GRY-RED LED2, GRY-BRN LED1; "BLK, GND"; "GRY-YEL, +12V"; "REPEATED FOR ALL FIVE PHOTO TRANSISTORS." with ORG-BRN PHOTO TRANSISTOR1 .. ORG-GRN PHOTO TRANSISTOR5; "TROUGH IR PHOTO TRANSISTOR BOARD"; "16-OPTO SWITCH BOARD".

## PDF p-129 [3-16] Trough IR LED Board Assembly (transmitter-green board), A-18617-1

Drawing: board with seven LED positions LED1-LED7 and 9-pin J1 (pins 9..1). Schematic: LED7 (Ball 6), LED6 (Ball 5), LED5 (Ball 4), LED4 (Ball 3), LED3 (Ball 2), LED2 (Ball 1), LED1 (Jam Ball), cathodes common. J1 side labels: 1 Ball 6, 2 Ball 5, 3 Ball 4, 4 Ball 3, 5 Ball 2, 6 Ball 1, 7 Jam Ball, 8 Key, 9 Common.

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-1 | | LED7, NOT USED |
| J1-2 | | LED6, NOT USED |
| J1-3 | Gray-Green | LED5, to 16-Opto Switch Board J1-4 |
| J1-4 | Gray-Black | LED4, to 16-Opto Switch Board J1-5 |
| J1-5 | Gray-Orange | LED3, to 16-Opto Switch Board J1-6 |
| J1-6 | Gray-Red | LED2, to 16-Opto Switch Board J1-7 |
| J1-7 | Gray-Brown | LED1, to 16-Opto Switch Board J1-9 |
| J1-8 | | Key |
| J1-9 | Black | ground, to 16-Opto Switch Board J1-10 |

## PDF p-130 [3-17] Trough IR Photo Transistor Board Assembly (receiver-blue board), A-18618-1

Drawing: board with Q1-Q7 and J1. Schematic: Q1 (Jam Ball), Q2 (Ball 1), Q3 (Ball 2), Q4 (Ball 3), Q5 (Ball 4), Q6 (Ball 5), Q7 (Ball 6); collectors common. J1 labels: 1 Common, 2 Key, 3 Jam Ball, 4 Ball 1, 5 Ball 2, 6 Ball 3, 7 Ball 4, 8 Ball 5, 9 Ball 6.

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-1 | Gray-Yellow | +12V, to 16-Opto Switch Board J2-1 |
| J1-2 | | Key |
| J1-3 | Orange-Brown | Photo Transistor 1, to 16-Opto Switch Board J2-10 |
| J1-4 | Orange-Red | Photo Transistor 2, to 16-Opto Switch Board J2-9 |
| J1-5 | Orange-Black | Photo Transistor 3, to 16-Opto Switch Board J2-8 |
| J1-6 | Orange-Yellow | Photo Transistor 4, to 16-Opto Switch Board J2-7 |
| J1-7 | Orange-Green | Photo Transistor  5, to 16-Opto Switch Board J2-6 |
| J1-8 | | Photo Transistor 6, NOT USED |
| J1-9 | | Photo Transistor 7, NOT USED |

## PDF p-131 [3-18] LED Board Assembly (transmitter-green board) A-16908 / Photo Transistor Board Assembly (receiver-blue board) A-16909

Drawings: single-device boards. A-16908: solder side, component side, schematic; pads labelled A and K (component side shows K left, A right); schematic is an IR LED, A and K. A-16909: pads C and E; schematic is a photo transistor, C and E. "Typical Circuit Diagram": LED BOARD Transmitter 1.0-1.4 volts; PHOTO TRANSISTOR BOARD Receiver 0.1-0.7 volts unblocked, 11-13 volts blocked; wires "Gray-XXX", "Black, Ground" (LED), "Gray-Yellow, +12V", "Orange-XXX" (photo transistor); "BEAM". Bottom drawing: LED board (green; wires Gray-XXX at A side, Black at K side; "Solder"), white edge view, "Infrared Beam", photo transistor board (blue; Gray-Yellow at C side, Orange-XXX at E side). Text labels: Green, White, Black, Blue, Solder, Gray-XXX, Black, Gray-Yellow, Orange-XXX.

## PDF p-132 [3-19] 16-Opto Switch Board Circuit Diagram

Drawing: wiring diagram of the 16-Opto Switch Board connectors J1-J5. Wires printed as "wire colour, SW. #nn NAME" next to the connector pin.

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-10 | BLK | GND |
| J1-9 | GRY-BRN | SW. #31 TROUGH STACK |
| J1-7 | GRY-RED | SW. #32 TROUGH 1 |
| J1-6 | GRY-ORG | SW. #33 TROUGH 2 |
| J1-5 | GRY-BLK | SW. #34 TROUGH 3 |
| J1-4 | GRY-GRN | SW. #35 TROUGH 4 |
| J1-2 | GRY-VIO | SW. #37 CENTER TROUGH ENTER |
| J1-1 | GRY-WHT | SW. #38 LEFT TROUGH ENTER |
| J2-1 | GRY-YEL | +12V |
| J2-2 | ORG-GRY | SW. #38 LEFT TROUGH ENTER |
| J2-3 | ORG-VIO | SW. #37 CENTER TROUGH ENTER |
| J2-6 | ORG-GRN | SW. #35 TROUGH 4 |
| J2-7 | ORG-YEL | SW. #34 TROUGH 3 |
| J2-8 | ORG-BLK | SW. #33 TROUGH 2 |
| J2-9 | ORG-RED | SW. #32 TROUGH 1 |
| J2-10 | ORG-BRN | SW. #31 TROUGH STACK |
| J3-1 | BLK | GND |
| J3-3 | GRY-BRN | SW. #41 RIGHT POPPER 1 |
| J3-4 | GRY-RED | SW. #42 RIGHT POPPER 2 |
| J3-8 | GRY-BLU | SW. #46 RAMP LEFT MAGNET |
| J3-9 | GRY-VIO | SW. #47 RAMP CENTER MAGNET |
| J3-10 | GRY-WHT | SW. #48 RAMP RIGHT MAGNET |
| J4-1 | GRY-YEL | +12V |
| J4-2 | ORG-BRN | SW. #41 RIGHT POPPER 1 |
| J4-3 | ORG-RED | SW. #42 RIGHT POPPER 2 |
| J4-8 | ORG-BLU | SW. #46 RAMP LEFT MAGNET |
| J4-9 | ORG-VIO | SW. #47 RAMP CENTER MAGNET |
| J4-10 | ORG-GRY | SW. #48 RAMP RIGHT MAGNET |
| J5-13 (from Power Driver J118-3) | BLK | GRN [sic, printed "GRN"; pin 13 ground] |
| J5-12 (from Power Driver J118-2) | GRY-YEL | +12V |
| J5-10 (from CPU J207-4) | GRN-YEL | SW. COL. 4 |
| J5-9 (from CPU J207-3) | GRN-ORG | SW. COL. 3 |
| J5-8 (from CPU J209-9) | WHT-GRY | SW. ROW 8 |
| J5-7 (from CPU J209-8) | WHT-VIO | SW. ROW 7 |
| J5-6 (from CPU J209-7) | WHT-BLU | SW. ROW 6 |
| J5-5 (from CPU J209-5) | WHT-GRN | SW. ROW 5 |
| J5-4 (from CPU J209-4) | WHT-YEL | SW. ROW 4 |
| J5-3 (from CPU J209-3) | WHT-ORG | SW. ROW 3 |
| J5-2 (from CPU J209-2) | WHT-RED | SW. ROW 2 |
| J5-1 (from CPU J209-1) | WHT-BRN | SW. ROW 1 |

Other labels: "LED BOARD", "PHOTO TRANSISTOR BOARD", "See Outhole Trough Block Diagram, pg. 3-15." (twice), "TYPICAL WIRING FOR ALL SINGLE LED BOARDS." (twice), "TYPICAL WIRING FOR ALL SINGLE PHOTO TRANSISTOR BOARDS." (twice), POWER DRIVER BOARD J113/J118 (pins 3 and 2), CPU BOARD J211, J207 (pins 4, 3), J209 (pins 9,8,7,5,4,3,2,1). The first J1 group (five trough LEDs, SW #31-35) is attached to a drawn LED board; J1-2 and J1-1 are the "typical" single-LED wires for #37 and #38. The J3 group is the second LED board; J3/J4 group switches #41, #42, #46, #47, #48.

## PDF p-133 [3-20] 16-Opto Switch Board Assembly, A-16998.1

Drawing: PCB component layout with J1-J4 (10-pin) and J5 (13-pin), resistors R1-R59, diodes D1-D19, ICs U1-U5, capacitors C1-C6, LED.

| Connector-pin | Wire colour | Function text |
| --- | --- | --- |
| J1-1 | GRY-WHT | to sw. #38, Left Trough Enter |
| J1-2 | GRY-VIO | to sw. #37, Center Trough Enter |
| J1-3 | | N/C |
| J1-4 | GRY-GRN | to sw. #35, Trough 4 |
| J1-5 | GRY-BLK | to sw. #34, Trough 3 |
| J1-6 | GRY-ORG | to sw. #33, Trough 2 |
| J1-7 | GRY-RED | to sw. #32, Trough 1 |
| J1-8 | | KEY |
| J1-9 | GRY-BRN | to sw. #31, Trough Stack |
| J1-10 | BLK | Ground, to sw #31 through sw. #38 |
| J2-1 | GRY-YEL | +12V, to sw. #31 through sw. #38 |
| J2-2 | ORG-GRY | to sw. #38, Left Trough Enter |
| J2-3 | ORG-VIO | to sw. #37, Center Trough Enter |
| J2-4 | | N/C |
| J2-5 | | KEY |
| J2-6 | ORG-GRN | to sw. #35, Trough 4 |
| J2-7 | ORG-YEL | to sw. #34, Trough 3 |
| J2-8 | ORG-BLK | to sw. #33, Trough 2 |
| J2-9 | ORG-RED | to sw. #32, Trough 1 |
| J2-10 | ORG-BRN | to sw. #31, Trough Stack |
| J3-1 | BLK | Ground, to sw. #41 through sw. #48 |
| J3-2 | | KEY |
| J3-3 | GRY-BRN | to sw. #41, Right Popper 1 |
| J3-4 | GRY-RED | to sw. #42, Right Popper 2 |
| J3-5 | | N/C |
| J3-6 | | N/C |
| J3-7 | | N/C |
| J3-8 | GRY-BLU | to sw. #46, Ramp Left Magnet |
| J3-9 | GRY-VIO | to sw. #47, Ramp Center Magnet |
| J3-10 | GRY-WHT | to sw. #48, Ramp Right Magnet |
| J4-1 | GRY-YEL | +12V, to sw. #41 through sw. #48 |
| J4-2 | ORG-BRN | to sw. #41, Right Popper 1 |
| J4-3 | ORG-RED | to sw. #42, Right Popper 2 |
| J4-4 | | KEY |
| J4-5 | | N/C |
| J4-6 | | N/C |
| J4-7 | | N/C |
| J4-8 | ORG-BLU | to sw. #46, Ramp Left Magnet |
| J4-9 | ORG-VIO | to sw #47, Ramp Center Magnet |
| J4-10 | ORG-GRY | to sw. #48, Ramp Right Magnet |
| J5-1 | WHT-BRN | sw. row 1, from CPU board J209-1 |
| J5-2 | WHT-RED | sw. row 2, from CPU board J209-2 |
| J5-3 | WHT-ORG | sw row 3, from CPU board J209-3 |
| J5-4 | WHT-YEL | sw. row 4, from CPU board J209-4 |
| J5-5 | WHT-GRN | sw. row 5, from CPU board J209-5 |
| J5-6 | WHT-BLU | sw. row 6, from CPU board J209-7 |
| J5-7 | WHT-VIO | sw. row 7, from CPU board J209-8 |
| J5-8 | WHT-GRY | sw. row 8, from CPU board J209-9 |
| J5-9 | GRN-ORG | sw. col. 3, from CPU board J207-3 |
| J5-10 | GRN-YEL | sw. col. 4, from CPU board J207-4 |
| J5-11 | KEY | |
| J5-12 | GRY-YEL | +12V, from Power Driver board J118-2 |
| J5-13 | BLK | Ground, from Power Driver board J118-3 |

## PDF p-134 [3-21] 16-Opto Switch Board Assembly Schematic, A-16998.1

Drawing: full schematic (LM339 comparators U1-U5, diodes D1-D19 1N4004, resistors, C1-C6, LED1). Legible labels: J5 header "10 MATRIX & POWER" with pins labelled R1 R2 R3 R4 R5 R6 R7 R8 C1 C2 KEY +12V GND; J1 "Col. 1 Sensors" with pins A1-A8, KEY, Cathodes (pin 10); J2 collectors E1-E8, KEY, Collectors; J3 "Cathodes" with A9..A16, KEY; J4 "Col. 2 Sensors" collectors E9-E16, KEY. LED resistors R1-R4, R23-R30, R47-R50 shown 270 2W; pull-downs 2K; R58 100K, R59 100K, R13/R14 22K, R51 22K, R52/R54/R56 100K, R53/R55 10K, C6 470/35, R57 1.2K, LED1, D19 1N4004. The detailed net-by-net wiring of the comparators is not transcribed (not legibly traceable at this resolution).

## PDF p-084 [2-11] A-18617-1 Trough IRED LED PCB Assembly / A-18618-1 Trough IRED Transistor PCB Assembly

A-18617-1 drawing: board outline with LED1-LED5 and J1 (9-pin, 9..1).

| Part Number | Designator | Description |
| --- | --- | --- |
| 5671-12731-00 | LED1 - LED5 | Infra Red Diode |
| 5791-12622-09 | J1 | Connector, 9-pin Header Sq. |

A-18618-1 drawing: board outline with Q1-Q5 and J1 (9-pin).

| Part Number | Designator | Description |
| --- | --- | --- |
| 5163-14114-00 | Q1 - Q5 | Infra Red Photo Transistor |
| 5791-12622-09 | J1 | Connector, 9-pin Header Sq. |

## PDF p-085 [2-12] A-17223 16-Opto PCB & Bracket Assembly

| Part Number | Designator | Description |
| --- | --- | --- |
| A-16898.1 | - | 16-Opto Dual Mount PCB Assy. |
| 5043-08996-00 | C1 -C5 | Capacitor, 0.1µF, 50v(±20%) Axial |
| 5040-13102-00 | C6 | Capacitor, 470µF, @35v (±20%) |
| 5791-13830-10 | J1-J4 | Connector, 10-pin Header STR Sq. |
| 5791-10862-13 | J5 | Connector, 13-pin Header STR Sq. |
| 5671-13732-00 | LED1 | Display LED Red |
| 5010-12928-00 | R1-R4, R23-R30, R47-R50 | Resistor, 270Ω, 2w, 5% |
| 5010-09999-00 | R5-R12, R15-R22, R31-R46 | Resistor, 2KΩ, 1/4w, 5% |
| 5010-08774-00 | R13, R14, R51 | Resistor, 22KΩ, 1/4w, 5% |
| 5010-09162-00 | R52, R54, R56, | Resistor, 100KΩ, 1/4w, 5% |
| 5010-09034-00 | R53, R55 | Resistor, 10KΩ, 1/4w, 5% |
| 5010-10631-00 | R57 | Resistor, 1.2KΩ, 1/2w, 5% |
| 5370-12272-00 | U1-U5 | IC LM339 Quad Comp. |
| 5070-09054-00 | D1 - D19 | Diode 1N4004 1.0A. |
| 01-20756 | - | PCB Mounting Bracket |
| 07-6688-18N | - | Rivet 3/16 x 1/8" Nickel |

Drawing: component layout with J1-J4, J5, U1-U5, R1-R59, D1-D19, C1-C6, LED1.

## Transcription notes

- p-132 J5-13 label: the printed text reads "BLK, GRN" ("GRN" where GND is expected); in the Outhole page the same wire is "BLK GND". Transcribed as read; the scan is slightly noisy there.
- p-132 and p-128 pin numbers on the right edge of the wiring diagram were read from the pin boxes; p-133's own tables agree for every pin.
- p-134 schematic: net-by-net comparator wiring not transcribed (dense, low contrast); only labels and values.
- p-128 diagrams list ORG/GRY wires for photo transistor 1-5 only; LED 6, LED 7 / PT 6, 7 are not wired (see p-129 / p-130 "NOT USED").
