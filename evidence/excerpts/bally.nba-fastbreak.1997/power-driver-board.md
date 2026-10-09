# NBA Fastbreak — Power Driver Board Connectors

Transcribed from `Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf` (document
16-50053.1-101, May 1997): the `Power Driver Board Assembly A-20028` connector list, which runs over three printed
pages: `3-29` (PDF page 83, right half; connectors J101-J107, under the board layout drawing), `3-30` (PDF page 84,
left half; J108-J123, headed `Power Driver Board Continued...`) and `3-31` (PDF page 84, right half; J124-J141,
headed `Power Driver Board Continued...`). The page prints these as text lists of `connector-pin  wire, function`
lines; each line is given here as one table row, the printed text after the pin number kept literally in the `Printed
text` column. Blank lines between connectors on the page are not rows. Read from the rendered page (300 dpi scan),
not from the OCR text. The board layout drawing on `3-29` prints the connector designators J101-J141 (and fuses
F101-F118, LED100-LED105) in their physical positions; it carries no pin labels.

The List is a connector table, not a schematic. It names the wire colour and the function of each pin (for example
`BLK-ORG, solenoid 19 drive to playfield flasher`). The structured-data device names (switch, lamp, solenoid
numbers) must come from the Switch/Lamp Matrix and Solenoid/Flasher Table; the wire colour printed here is the
cross-reference. Several printed anomalies are listed in the Observations at the end.


## Printed page 3-29

### J101

| Pin | Printed text |
| --- | --- |
| J101-1 | GRY-GRN, +12V to J210-6, 7; J606-1 |
| J101-2 | GRY-GRN, +12V to J210-6, 7; J606-2 |
| J101-3 | GRY, +5V to J210-4, 5; J3-1,3; J606-3 |
| J101-4 | GRY, +5V to J210-4, 5; J3-1,3; J606-4 |
| J101-5 | BLK, ground to J210-1, 3; J606-5 |
| J101-6 | KEY |
| J101-7 | BLK, ground to J210-1,3; J606-7 |

J102, 34-pin ribbon cable, data to/from CPU J211

### J103

| Pin | Printed text |
| --- | --- |
| J103-1 | YEL-WHT, 6.8Vac from xformer secondary |
| J103-2 | WHT-BRN, 6.8Vac from xformer secondary |
| J103-3 | WHT-BRN, 6.8Vac from xformer secondary |
| J103-4 | WHT-ORG, 6.8Vac from xformer secondary |
| J103-5 | WHT-YEL, 6.8Vac from xformer secondary |
| J103-6 | WHT-YEL, 6.8Vac from xformer secondary |
| J103-7 | ORG, 6.8Vac from xformer secondary |
| J103-8 | ORG 6.8Vac from xformer secondary |
| J103-9 | KEY |
| J103-10 | GRN, 6.8Vac from xformer secondary |
| J103-11 | BRN, 6.8Vac from xformer secondary |
| J103-12 | BRN, 6.8Vac from xformer secondary |

### J104

| Pin | Printed text |
| --- | --- |
| J104-1 | VIO, return, G.I. to Coin Door Board J2-3 |
| J104-2 | KEY |
| J104-3 | WHT-VIO, 6.8Vac, G.I. to Coin Door BrdJ2-5 |

### J105

| Pin | Printed text |
| --- | --- |
| J105-1 | BRN, return, G.I. to insert panel |
| J105-2 | ORG, return, G.I. to insert panel |
| J105-3 | YEL, return, G.I. to insert panel |
| J105-4 | KEY |
| J105-5 | N/C |
| J105-6 | VIO, return, G.I. to insert panel |
| J105-7 | WHT-BRN, 6.8Vac, G.I. to insert panel |
| J105-8 | WHT-ORG, 6.8Vac, G.I. to insert panel |
| J105-9 | WHT-YEL, 6.8Vac, G.I. to insert panel |
| J105-10 | N/C |
| J105-11 | WHT-VIO, 6.8Vac, G.I. to insert panel |

### J106

| Pin | Printed text |
| --- | --- |
| J106-1 | BRN, return, G.I. to playfield |
| J106-2 | ORG, return, G.I. to playfield |
| J106-3 | YEL, return, G.I. to playfield |
| J106-4 | KEY |
| J106-5 | GRN, return, G.I. to playfield |
| J106-6 | VIO, return, G.I. to playfield |
| J106-7 | WHT-BRN, 6.8Vac, G.I. to playfield |
| J106-8 | WHT-ORG, 6.8Vac, G.I. to playfield |
| J106-9 | WHT-YEL, 6.8Vac, G.I. to playfield |
| J106-10 | WHT-GRN, 6.8Vac, G.I. to playfield |
| J106-11 | WHT-VIO, 6.8Vac, G.I. to playfield |

J107-NOT USED

## Printed page 3-30

J108- NOT USED

### J109

| Pin | Printed text |
| --- | --- |
| J109-1 | BLU-BRN, solenoid 25 drive to playfield flasher |
| J109-2 | BLU-RED, solenoid 26 drive to playfield flasher |
| J109-3 | BLU-ORG, solenoid 27 drive to playfield flasher |
| J109-4 | BLU-YEL, solenoid 28 drive to playfield flasher |
| J109-5 | RED-ORG tieback diode |
| J109-6 | RED-ORG tieback diode |
| J109-7 | KEY |
| J109-8 | RED-ORG tieback diode |
| J109-9 | RED-ORG tieback diode |

### J110

| Pin | Printed text |
| --- | --- |
| J110-1 | BRN-WHT, solenoid 37 drive to High Current Driver board |
| J110-2 | KEY |
| J110-3 | ORG-WHT, solenoid 38 drive to High Current Driver board |
| J110-4 | YEL-WHT, solenoid 39 drive to 2 LED Driver board |
| J110-5 | BLU-WHT, solenoid 40 drive to 2 LED Driver board |

### J111

| Pin | Printed text |
| --- | --- |
| J111-1 | BLK-BRN, solenoid 17 drive to playfield flasher |
| J111-2 | BLK-RED, solenoid 18 drive to playfield flasher |
| J111-3 | BLK-ORG, solenoid 19 drive to playfield flasher |
| J111-4 | BLK-YEL, solenoid 20 drive to playfield flasher |
| J111-5 | N/C |
| J111-6 | BLU-BLK, solenoid 22 drive to playfield flasher |
| J111-7 | N/C |
| J111-8 | BLU-GRY, solenoid 24 drive to playfield flasher |
| J111-9 | KEY |
| J111-10 | N/C |
| J111-11 | N/C |
| J111-12 | N/C |
| J111-13 | N/C |

### J112

| Pin | Printed text |
| --- | --- |
| J112-1 | N/C |
| J112-2 | N/C |
| J112-3 | BLK-ORG, solenoid 19 drive to insert flasher |
| J112-4 | KEY |
| J112-5 | BLK-YEL, solenoid 20 drive to insert flasher |
| J112-6 | N/C |
| J112-7 | N/C |
| J112-8 | N/C |
| J112-9 | N/C |

### J113

| Pin | Printed text |
| --- | --- |
| J113-1 | BRN-BLK, solenoid 9 drive to playfield coil |
| J113-2 | KEY |
| J113-3 | BRN-RED, solenoid 10 drive to playfield coil |
| J113-4 | BRN-ORG, solenoid 11 drive to playfield coil |
| J113-5 | BRN-YEL, solenoid 12 drive playfield coil |
| J113-6 | BRN-GRN, solenoid 13 drive playfield coil |
| J113-7 | BRN-BLU, solenoid 14 drive playfield coil |
| J113-8 | BRN-VIO, solenoid 15 drive to playfield coil |
| J113-9 | BRN-GRY, solenoid 16 drive to playfield coil |

J114- NOT USED

J115- NOT USED

### J116

| Pin | Printed text |
| --- | --- |
| J116-1 | VIO-BRN, solenoid 1 drive to playfield coil |
| J116-2 | N/C |
| J116-3 | KEY |
| J116-4 | VIO-ORG, solenoid 3 drive to playfield coil |
| J116-5 | VIO-YEL, solenoid 4 drive playfield coil |
| J116-6 | VIO-GRN, solenoid 5 drive to playfield coil |
| J116-7 | VIO-BLU, solenoid 6 drive to playfield coil |
| J116-8 | N/C |
| J116-9 | VIO-GRY, solenoid 8 drive playfield coil |

### J117

| Pin | Printed text |
| --- | --- |
| J117-1 | N/C |
| J117-2 | N/C |
| J117-3 | VIO-BLK, solenoid 7 drive to insert panel coil |
| J117-4 | KEY |
| J117-5 | N/C |

J118- NOT USED

### J119

| Pin | Printed text |
| --- | --- |
| J119-1 | RED-GRN, +50V to lower right flipper coil |
| J119-2 | RED-GRN, loop from J119-1 |
| J119-3 | KEY |
| J119-4 | RED-BLU, loop from J119-5 |
| J119-5 | RED-BLU, +50V to lower left flipper coil |
| J119-6 | RED-VIO, loop from J119-7 |
| J119-7 | RED-VIO, +50V to solenoids 33 & 34 |
| J119-8 | RED-GRY, loop from J119-9 |
| J119-9 | RED-GRY, +50V to solenoids 35 & 36 |

### J120

| Pin | Printed text |
| --- | --- |
| J120-1 | ORG-GRY, solenoid 36 drive to playfield coil |
| J120-2 | N/C |
| J120-3 | YEL-GRY, solenoid 35 drive to playfield coil |
| J120-4 | N/C |
| J120-5 | ORG-VIO, solenoid 34 drive to playfield coil |
| J120-6 | YEL-VIO, solenoid 33 drive to playfield coil |
| J120-7 | ORG-BLU, holding, lower left flipper coil |
| J120-8 | N/C |
| J120-9 | YEL-BLU, power, lower left flipper coil |
| J120-10 | KEY |
| J120-11 | ORG-GRN, holding, lower right flipper coil |
| J120-12 | N/C |
| J120-13 | YEL-GRN, power, lower right flipper coil |

J121- NOT USED

### J122

| Pin | Printed text |
| --- | --- |
| J122-1 | KEY |
| J122-2 | N/C |
| J122-3 | YEL-GRY, lamp column 8 to cabinet |

### J123

| Pin | Printed text |
| --- | --- |
| J123-1 | YEL-BRN, lamp column 1 to playfield |
| J123-2 | YEL-RED, lamp column 2 to playfield |
| J123-3 | YEL-ORG, lamp column 3 to playfield |
| J123-4 | YEL-BLK, lamp column 4 to playfield |
| J123-5 | YEL-GRN, lamp column 5 to playfield |
| J123-6 | YEL-BLU, lamp column 6 to playfield |
| J123-7 | YEL-VIO, lamp column 7 to playfield |
| J123-8 | KEY |
| J123-9 | YEL-GRY, lamp column 8 to playfield |

## Printed page 3-31

### J124

| Pin | Printed text |
| --- | --- |
| J124-1 | RED-BRN, lamp row 1 to playfield |
| J124-2 | RED-BLK, lamp row 2 to playfield |
| J124-3 | KEY |
| J124-4 | RED-ORG, lamp row 3 to playfield |
| J124-5 | RED-YEL, lamp row 4 to playfield |
| J124-6 | RED-GRN, lamp row 5 to playfield |
| J124-7 | RED-BLU, lamp row 6 to playfield |
| J124-8 | RED-VIO, lamp row 7 to playfield |
| J124-9 | RED-GRY, lamp row 8 to playfield |

### J125

| Pin | Printed text |
| --- | --- |
| J125-1 | N/C |
| J125-2 | N/C |
| J125-3 | KEY |
| J125-4 | N/C |
| J125-5 | N/C |
| J125-6 | N/C |
| J125-7 | RED-BLU, lamp row 6 to cabinet |
| J125-8 | RED-VIO, lamp row 7 to cabinet |
| J126-9 | RED-GRY, lamp row 8 to cabinet |

J126- NOT USED

### J127

| Pin | Printed text |
| --- | --- |
| J127-1 | WHT-GRN, 9.8Vac from xformer secondary |
| J127-2 | WHT-GRN, 9.8Vac loop from J112-1 |
| J127-3 | WHT-GRN, 9.8Vac from xformer secondary |
| J127-4 | KEY |
| J127-5 | WHT-GRN, 9.8VAC loop from J112-3 |

### J128

| Pin | Printed text |
| --- | --- |
| J128-1 | WHT-RED, 16Vac loop from J102-2 |
| J128-2 | WHT-RED, 16Vac from xformer secondary |
| J128-3 | WHT-RED, 16Vac loop from J102-4 |
| J128-4 | WHT-RED, 16Vac from xformer secondary |
| J128-5 | BLK-YEL, 16Vac loop from J102-6 |
| J128-6 | BLK-YEL, 16Vac from xformer secondary |
| J128-7 | KEY |
| J128-8 | BLK-YEL, 16Vac loop from J102-9 |
| J128-9 | BLK-YEL, 16Vac from xformer secondary |

### J129

| Pin | Printed text |
| --- | --- |
| J129-1 | RED, 9Vac from xformer secondary |
| J129-2 | RED, 9Vac from transformer secondary |
| J129-3 | KEY |
| J129-4 | BLU-WHT, 13Vac from xformer secondary |
| J129-5 | BLU-WHT, 13Vac loop from J101-4 |
| J129-6 | BLU-WHT, 13Vac from xformer secondary |
| J129-7 | BLU-WHT, 13Vac loop from J101-6 |

J130-NOT USED

J131-NOT USED

J132-NOT USED

### J133

| Pin | Printed text |
| --- | --- |
| J133-1 | RED-ORG, +50V to coils |
| J133-2 | RED-BRN, +50V to coils |
| J133-3 | RED-BLK, +50V to coils |
| J133-4 | KEY |
| J133-5 | N/C |
| J133-6 | RED-WHT, +20V to playfield flasher |

### J134

| Pin | Printed text |
| --- | --- |
| J134-1 | N/C |
| J134-2 | N/C |
| J134-3 | RED-BRN, +50V to insert panel coil |
| J134-4 | KEY |
| J134-5 | RED-WHT, +20V to insert panel flasher |

J135- NOT USED

J136- NOT USED

J137- NOT USED

J138- NOT USED

### J139

| Pin | Printed text |
| --- | --- |
| J139-1 | KEY |
| J139-2 | GRY-YEL, +12V to playfield boards |
| J139-3 | BLK, ground to playfield boards |
| J139-4 | N/C |
| J139-5 | BLK-WHT, signal for coin meter to Coin Door Interface board J2-7. |

### J140

| Pin | Printed text |
| --- | --- |
| J140-1 | KEY |
| J140-2 | GRY-YEL, +12V |
| J140-3 | BLK, ground |
| J140-4 | N/C |

### J141

| Pin | Printed text |
| --- | --- |
| J141-1 | KEY |
| J141-2 | GRY-YEL, +12V to Coin Door Board J2-2 |
| J141-3 | BLK, ground to Coin Door Board J2-1 |
| J141-4 | N/C |

## Observations on the printed text

- Lamp matrix connectors. The Lamp Matrix table (`lamp-matrix.md`, printed `2-49` and `3-4`) prints the column wire
  connector as `J121-1` ... `J121-9` and the row connector as `J125-1` ... `J125-9`. This Power Driver Board list prints
  `J121- NOT USED`; the lamp columns for the playfield are `J123-1` ... `J123-9` (`YEL-BRN` ... `YEL-GRY`, `lamp column
  1` ... `lamp column 8 to playfield`, with `J123-8 KEY` so column 8 is on `J123-9`), column 8 to the cabinet is `J122-3`, the
  playfield lamp rows are `J124-1` ... `J124-9` (`RED-BRN` ... `RED-GRY`, `lamp row 1` ... `lamp row 8 to playfield`,
  with `J124-3 KEY`), and `J125` carries only rows 6, 7 and 8 to the cabinet (`J125-7`, `J125-8`, and a line printed
  `J126-9`). The wire colours agree in all cases (the lamp matrix's `Yellow-Brown` column 1 is `YEL-BRN`; row 1
  `Red-Brown` is `RED-BRN`), so the connector designators of the matrix table and of this list disagree while the wire
  colours agree.
- `J126-9 RED-GRY, lamp row 8 to cabinet` is printed in the J125 group directly above `J126- NOT USED`; the `J126` is
  probably a typographical error for `J125-9` (the lamp matrix row 8 return is `J125-9`), transcribed as printed.
- Solenoid 19 and 20 appear twice: `J111-3` / `J111-4` (`to playfield flasher`) and `J112-3` / `J112-5` (`to insert
  flasher`), on the same wire colours (`BLK-ORG`, `BLK-YEL`), matching the Solenoid/Flasher Table's playfield and
  backbox drive connections for rows 19 and 20. There is no solenoid 21 or 23 pin (`J111-5` and `J111-7` are `N/C`),
  no solenoid 2 pin (`J116-2` `N/C`), and no solenoid 7 pin on a playfield connector (`J117-3`, `to insert panel coil`).
- Solenoid 34 (`ORG-VIO`, Upr. Rt. Hold) is printed on `J120-5` in this list (`J120-4` is `N/C`), but on `J120-4` in the Solenoid/Flasher
  Table (`2-50`, `3-5`) and on the `3-6` Solenoid Wiring drawing; the wire colour agrees. Solenoids 33, 35 and 36 (`J120-6`, `J120-3`, `J120-1`)
  agree everywhere. The `J119` pins named by the Solenoid/Flasher Table's Voltage Connection column (`J119-1`, `J119-4`, `J119-6`, `J119-8`) are, in this list, `J119-1` the lower-right +50V pin, and `J119-4`, `J119-6`, `J119-8` the `loop` pins (`J119-5` carries the lower-left +50V, `J119-7` carries solenoids 33 and 34, `J119-9` carries 35 and 36).
- Coin door G.I. wires: this list prints `J104-1 VIO, return, G.I. to Coin Door Board J2-3` and `J104-3 WHT-VIO, 6.8Vac, G.I. to Coin Door Brd J2-5`;
  the Coin Door Interface Board list (`section-3-boards.md`, `3-32`) prints `J2-3 WHT-VIO, G.I. 6.8vac from Power Driver J104-1` and `J2-5 VIO, G.I. from
  Power Driver Board J104-3`, i.e. the two wire colours are exchanged between the two lists. The General Illumination block of the Solenoid/Flasher
  Table lists `J104-3` as the string 5 Cabinet voltage connection and `J104-1` as its drive connection.
- `J109-5`, `J109-6`, `J109-8` and `J109-9` are the tieback diodes for solenoids 25 to 28 (the Solenoid/Flasher
  Table's footnote names the same four pins).
- `J119` is the flipper `+50V` connector: `J119-1` (lower right, with its loop on `J119-2`), `J119-5` (lower left, loop on
  `J119-4`), `J119-7` (solenoids 33 and 34, loop on `J119-6`), `J119-9` (solenoids 35 and 36, loop on `J119-8`).
  `J120` has the drive pins; the Hold wires are printed `holding` (`J120-7`, `J120-11`) and the Power wires `power`
  (`J120-9`, `J120-13`); solenoids 33-36 are the four upper-flipper (`Shoot`) coils `J120-6`, `J120-5`, `J120-3`, `J120-1`.
- `J133` carries the `+50V to coils` pins `J133-1` (`RED-ORG`), `J133-2` (`RED-BRN`), `J133-3` (`RED-BLK`) and
  `J133-6` (`RED-WHT`, `+20V to playfield flasher`). `J134-5` is `+20V to insert panel flasher` and `J134-3` is
  `+50V to insert panel coil`.
- `J127-2` is printed `WHT-GRN, 9.8Vac loop from J112-1` and `J127-5` `9.8VAC loop from J112-3` (J112 is the insert-flasher
  connector on this page; the text is as printed).
- `J129-2` prints `from transformer secondary` where the neighbouring lines print `from xformer secondary`; `J103-8`
  prints `ORG 6.8Vac` without a comma.
- G.I. strings. Return pins (the lamp-socket return side) and the 6.8 Vac drive pins: playfield `J106` returns `J106-1
  BRN`, `J106-2 ORG`, `J106-3 YEL`, `J106-5 GRN`, `J106-6 VIO` with drives `J106-7 WHT-BRN`, `J106-8 WHT-ORG`, `J106-9
  WHT-YEL`, `J106-10 WHT-GRN`, `J106-11 WHT-VIO`; insert panel `J105` returns `J105-1 BRN`, `J105-2 ORG`, `J105-3 YEL`, `J105-6
  VIO` with drives `J105-7` to `J105-9` and `J105-11` (`J105-5` and `J105-10` are `N/C`); cabinet/coin door `J104-1 VIO`
  return and `J104-3 WHT-VIO` drive. These agree with the General Illumination block of the Solenoid/Flasher Table
  (strings 1-3 on `J106` and `J105`, string 4 on `J106` only, string 5 on `J106`, `J105` and `J104`).
- `J107`, `J108`, `J114`, `J115`, `J118`, `J121`, `J126`, `J130`, `J131`, `J132`, `J135`, `J136`, `J137` and `J138` are printed
  `NOT USED`. `J102` is the 34-pin ribbon cable to the CPU board `J211`.

## Uncertain readings

None.
