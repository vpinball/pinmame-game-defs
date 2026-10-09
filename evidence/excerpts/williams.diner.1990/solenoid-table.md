# Diner — Solenoid Table and ROM and Jumper Table (PDF page 2, no printed folio)

Source: `Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf` (106
pages, SHA-256 `da75ffb79e6d6b8d1b332ce65f93ee1486a5a7ff8d9060878f07a91438b573aa`), PDF page 2. The page
prints no folio and no other text; it carries the "DINER ROM and Jumper Table" above the "DINER Solenoid
Table". Read from the rendered 150 dpi page image, cropped and enlarged in strips; the OCR text layer was
not trusted. Every row and every column is transcribed. Superscript note markers are written `^n`.

## DINER ROM and Jumper Table

Printed immediately above the Solenoid Table on the same page. Table heading: "DINER ROM and Jumper
Table". A hatched vertical divider is printed between the Jumpers column and the Audio Bd column. Cell text
printed on two lines is written on one line with the line break shown as a space (the part numbers break
after the second hyphen, for example `A-5343-` / `576-2`, written `A-5343-576-2`).

| Game | CPU Rev | P/N - U15 Game µP | P/N - U27 G. ROM 1 | P/N - U26 G. ROM 2 | Jumpers | Audio Bd | P/N - U4 A. ROM 1 | P/N - U19 A. ROM 2 | P/N - U20 A. ROM 3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ROLLERGAMES | System 11C | 5400-09150-00 | A-5343-576-2 | A-5343-576-1 | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 | System 11C | A-5343-576-3 | A-5343-576-4 | A-5343-576-5 |
| DINER | System 11C | 5400-09150-00 | A-5343-571-2 | A-5343-571-1 | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 | System 11C | A-5343-571-3 | A-5343-571-4 | A-5343-571-5 |

The ROM-number suffixes in the headers ("G. ROM 1", "G. ROM 2", "A. ROM 1", "A. ROM 2", "A. ROM 3") are
clipped by the cell borders in the scan; see Uncertain cells.

## DINER Solenoid Table

Column headers as printed: `Sol. No.` | `Function` | `Solenoid Type` | `Wire Color` with superscript `1` |
`Connections` spanning two sub-columns `CPU Bd` and `Playfield/ Cabinet` | `Driver Trnstr` | `Solenoid
Part Number / Flashlamp Type`, with the small line `g= B'glass; p=Pl'field` under that last heading.

In rows 01A to 08C the wire colours of an A/C pair are joined by a closing brace `}` printed at the right
of the Wire Color column, and the CPU Bd cell of the pair prints the A-row pin on the first line and the
C-row bracketed wire colour (for example `(Gry-Brn)`) on the second line. In the table below each A/C pair
keeps both printed lines as separate rows; the brace is noted here and not repeated.

| Sol. No. | Function | Solenoid Type | Wire Color | CPU Bd | Playfield/Cabinet | Driver Trnstr | Solenoid Part Number / Flashlamp Type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01A^3 | Outhole Kicker | Switched | Vio-Brn | 1P11-1 | 5J1-9: 5J4-9 (A) | Q33 | AE-23-800 |
| 01C^3 | Haji Flash | Switched | Blk-Brn | (Gry-Brn) | 5J5-9 (C) | Q33 | #89/906 flashlamps  1p,1g |
| 02A^3 | Ramp Down | Switched | Vio-Red | 1P11-3 | 5J1-7: 5J4-8 (A) | Q25 | SM-1-26-600 |
| 02C^3 | Babs Flash | Switched | Blk-Red | (Gry-Red) | 5J5-8 (C) | Q25 | #89/906 flashlamps  1p,1g |
| 03A^3 | Center 3-Bk Dr Tgt Reset | Switched | Vio-Orn | 1P11-4 | 5J1-6: 5J4-7 (A) | Q32 | AE-26-1200 |
| 03C^3 | Boris Flash | Switched | Blk-Orn | (Gry-Orn) | 5J5-7(C) | Q32 | #89/906 flashlamps  1p,1g |
| 04A^3 | Ramp Up | Switched | Vio- Yel | 1P11-5 | 5J1-5:  5J4-6 (A) | Q24 | AE-23-800 |
| 04C^3 | Pepe Flash | Switched | Blk-Yel | (Gry-Yel) | 5J5-5 (C) | Q24 | #89/906 flashlamps  1p,1g |
| 05A^3 | Upper Left Eject | Switched | Vio-Grn | 1P11-6 | 5J1-4: 5J4-5 (A) | Q31 | AE-23-800 |
| 05C^3 | Buck Flash | Switched | Blk-Grn | (Gry-Grn) | 5J5-4 (C) | Q31 | #89/906 flashlamps  1p,1g |
| 06A^3 | Sub-P'fld Shooter | Switched | Vio-Blu | 1P11-7 | 5J1-3: 5J4-4 (A) | Q23 | AE-23-800 |
| 06C^3 | Cup Flashers | Switched | Blk-Blu | (Gry-Blu) | 5J5-3 (C) | Q23 | #89/906 flashlamps  4p |
| 07A^3 | Knocker (in Backbox) | Switched | Vio-Blk | 1P11-8 | 5J1-2: 5J4-2 (A) | Q30 | AE-23-800 |
| 07C^3 | Clock Flashers | Switched | Blk-Vio | (Gry-Vio) | 5J5-2 (C) | Q30 | #89 flashlamps  2g |
| 08A^3 | Lower Left Eject | Switched | Vio-Gry | 1P11-9 | 5J1-1: 5J4-1 (A) | Q22 | AE-23-800 |
| 08C^3 | DINE - TIME Flashers | Switched | Blk-Gry | (Gry-Blk) | 5J5-1 (C) | Q22 | #89 flashlamps  1p,2g |
| 09 | Right Ramp Flashers | Controlled | Brn-Blk | 1P12-1 | 5J2-9:5J6-9:2J4-10 | Q17 | #89/906 flashlamps  2p,1g |
| 10 | Backbox/Pl'fld  Illum Relay | Controlled | Brn-Red | 1P12-2 | 5J2-8:5J6-8:2J4-11 | Q9 | 5580-09555-01^4a |
| 11 | Left Ramp Flashers | Controlled | Brn-Orn | 1P12-4 | 5J2-6:5J6-7:2J4-12 | Q16 | #906 flashlamps  2p |
| 12 | A/C Select Relay | Controlled | Brn-Yel | 1P12-5 | 5J2-5 | Q8 | 5580-09555-01^5 |
| 13 | Left 3-Bk Dr Tgt Reset | Controlled | Brn-Grn | 1P12-6 | 5J2-4:5J6-5:2J4-13 | Q15 | AE-26-1200 |
| 14 | Diverter | Controlled | Brn-Blu | 1P12-7 | 5J2-3:5J6-3:2J4-14 | Q7 | AE-26-1200 |
| 15 | Clock Wheel (B) | Controlled | Brn-Vio | 1P12-8 | 2J4-15: 2J11-2 | Q14 | } Stepper Motor 14-7948 |
| 16 | Clock Wheel (A) | Controlled | Brn-Gry | 1P12-9 | 2J4-16: 2J11-1 | Q6 | } Stepper Motor 14-7948 |
| 17 | Left Jet Bumper | Special #1 | Blu-Brn | 1P19-7 | 5J3-7: 5J7-7 | Q75 | AE-23-800 |
| 18 | Left Kicker ("sling") | Special #2 | Blu-Red | 1P19-4 | 5J3-6: 5J7-6 | Q71 | AE-26-1200 |
| 19 | Right  Jet Bumper | Special #3 | Blu-Orn | 1P19-3 | 5J3-3: 5J7-3 | Q73 | AE-23-800 |
| 20 | Right Kicker ("sling") | Special #4 | Blu-Yel | 1P19-6 | 5J3-4: 5J7-5 | Q69 | AE-26-1200 |
| 21 | Lower Jet Bumper | Special #5 | Blu-Grn | 1P19-8 | 5J3-2: 5J7-2 | Q77 | AE-23-800 |
| 22 | Shooter Lane Feeder | Special #6 | Blu-Blk | 1P19-9 | 5J3-1: 5J7-1 | Q79 | AE-23-800 |
| - | Right Flipper (underlined, right-aligned on the first line); Lower Right Flipper (second line) | - | Orn-Vio; (Blu-Vio)^2 | 1P19-1 | 2J5-5: 2J10-7; (2J10-1: 2J8-15) | - | (blank) on the first line; FL11630/50VDC on the second line |
| - | Left Flipper (underlined, right-aligned on the first line); Lower Left Flipper (second line) | - | Orn-Gry^2; (Blu-Gry)^2 | 1P19-2 | 2J5-4: 2J10-8; (2J10-2:2J8-14) | - | (blank) on the first line; FL11630/50VDC on the second line |

Notes on cell layout: Sol. No. 09 to 22 print no superscript. In rows 15 and 16 the Part Number cell is one
closing-brace-joined cell, `} Stepper Motor 14-7948`, spanning both rows (the brace opens to the right of
Q14 and Q6). In the two flipper rows the Solenoid Type "-" is printed on the first line of the Right
Flipper row and on the second line of the Left Flipper row; the Driver Trnstr "-" is printed on the first
line of the Right Flipper row and on the second line of the Left Flipper row. On the Left Flipper row the
"2" after `Orn-Gry` is printed lowered beside the comma-shaped mark, and written `^2` here.

NOTES block, verbatim (printed beneath the table in a box):

"NOTES: 1. Wire colors, except flipper ORN-VIO and ORN-GRY, are ground connections (to coil terminal with
unbanded end of diode). Flipper ORN-VIO and ORN-GRY wires connect from CPU Board to flipper switch on
cabinet. 2. Flipper connections shown in braces are from flipper switch to flipper coil. 3. "A" circuits
are pulsed, when Sol. 12 is de-energized; "C" circuits are pulsed, with Sol.12 energized. Wire colors in
brackets are those from respective A and Cterminals corresponding to the J1-terminal connection listed for
the Aux Power Driver Board, which controls the device pulsing by Sol. 12. 4. Relay is mounted on Relay
Board: (4a) p/n C-11998-1; (4b) p/n C-11902-1. 5. Relay is mounted on Aux Power Driver Bd, D-12247, in the
backbox."

(The text prints "Cterminals" as one word, as written here. Note 4 names (4a) and (4b); only `4a` is
printed as a superscript in the table.)

## Comparison with the copy on PDF page 36 (printed "DINER 32")

PDF page 36 (printed `DINER 32`, "TEST/DIAGNOSTIC PROCEDURES (Continued)", "SOLENOID TEST.") prints the
same "DINER Solenoid Table" with the same NOTES block. Its introductory paragraph (quoted in part): "(From
Lamp Test) Using AUTO-UP, press ADVANCE. Observe that the upper display shows the message, COIL TEST, the
lower display shows 05 (Solenoid Test identifier). Next, the lower display shows a series of test steps
from 01 through 27, while the upper display shows the solenoid/circuit name. ... Refer to the Solenoid
Table for solenoid numbers and wiring information. CPU Board connections at 1P11, 1P12, and 1P19 are also
listed in the table." (The prose says "01 through 27"; the table lists solenoid numbers 01 to 22 and two
unnumbered flipper rows. This is a difference between prose and table, not between the two table copies.)
Page 36 does not print the ROM and Jumper Table.

The Solenoid Table was compared with the page 2 copy cell by cell from enlarged crops: all column headers
(including the superscript `1` on Wire Color and the "g= B'glass; p=Pl'field" line), all 24 data rows
(Sol. No. with superscripts, Function, Solenoid Type, Wire Color, CPU Bd, Playfield/Cabinet, Driver
Trnstr, Part Number and flashlamp quantities `1p,1g`, `4p`, `2g`, `1p,2g`, `2p,1g`, `2p`, the `4a` and `5`
superscripts, the stepper-motor brace) and the NOTES block agree word for word and digit for digit. There
is no difference in any printed cell. Print differences only: the page 36 copy is printed smaller and with
slightly different spacing, and a small smudge follows "flashlamps" in row 05C and "4p" in row 06C.

The OCR layer was not used for any cell.

Normalization: none beyond joining cell text printed on two lines into one cell where noted, writing
superscripts as `^n`, and writing the two printed lines of the flipper rows in one table row separated by
semicolons.

Uncertain cells:
- ROM and Jumper Table headers "P/N - U27 G. ROM 1", "P/N - U26 G. ROM 2", "P/N - U19 A. ROM 2" and "P/N -
  U20 A. ROM 3" (and "P/N - U4 A. ROM 1"): the final numeral is partly clipped by the vertical cell border
  in the scan. Read as 1 (U27), 2 (U26), 1 (U4), 2 (U19) and 3 (U20); the digits are consistent with the
  sequence of the columns but are not fully formed on the page.
- ROM and Jumper Table, DINER row, U27 and U26 columns: printed `A-5343-571-2` and `A-5343-571-1`
  (U27 holds the "-2" ROM, U26 the "-1" ROM), read as printed. Likewise the ROLLERGAMES row prints
  `576-2` under U27 and `576-1` under U26.
- Row 04A Wire Color: printed `Vio- Yel` with a space after the hyphen. Written as printed.
- Row 04A Playfield/Cabinet: printed `5J1-5:  5J4-6 (A)` with two spaces after the colon. Written as printed.
- Left Flipper row Wire Color: the "2" after `Orn-Gry` is lowered and shares space with a comma-like
  mark; read as a note marker `2`, not as a comma plus a digit. The same appears on page 36.
- Sol. 12 and Sol. 10 Part Number superscripts: `5` and `4a` read as printed; the `4a`/`5` shapes are small.
- Page 2 prints no folio; the folio cannot be checked for this page.
