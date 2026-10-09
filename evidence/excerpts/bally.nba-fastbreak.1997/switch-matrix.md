# NBA Fastbreak — Switch Matrix (wiring)

Transcribed from `Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf` (document
16-50053.1-101, May 1997), PDF page 67, left half of the 2-up spread, printed page `2-48`: the `SWITCH
MATRIX` table with its dedicated grounded switch column (D1-D8), its flipper grounded switch column
(F1-F8), the 8 x 8 matrix cells, the legend and the switch drawing in the title line. The right half of the
same PDF page is the Lamp Matrix (`lamp-matrix.md`). The same table in the March 1997 edition
(`Bally_1997_NBA_Fastbreak_Operations_Manual_Final_no_schematics.pdf`, PDF page 126, printed page `2-48`) was
read as well; where the editions differ this is stated. Read from the rendered page (300 dpi scan), not from the
OCR text.

The title line prints `SWITCH MATRIX`, then at the right a switch drawing with the labels `White` (left), a diode
symbol, an open switch contact, and `Green` (right).

## Matrix drive columns

| Column | Wire | Connector-pin | Drive IC pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-Yellow | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

The top-left corner cell of the grid is divided diagonally and prints `Column` (upper right) and `Row` (lower
left). The wire names are printed on two lines (`Green-` over `Brown`).

## Matrix return rows

| Row | Wire | Connector-pin | Return IC pin |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | U208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

Row 6 prints its connector-pin as `U208-7` (a `U` where every other row prints `J`); transcribed literally. The
March edition prints the same `U208-7`. The `J208` series of the other rows and the `J208-6` pin that would
follow `J208-5` are not printed: row 5 is `J208-5`, row 6 is `U208-7`, row 7 is `J208-8`.

## Dedicated grounded switches (left column)

Each cell prints, top to bottom: wire (bold), connector-pin (bold) with a second pin to its right for D5-D8, the
label, and the cell id (D1-D8) at the bottom right. For D1-D4 the third line is the IC pin (`U17-n`).

| Switch | Wire | Connector-pin | IC pin | Printed label |
| --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | U17-5 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | U17-7 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | U17-11 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | U17-9 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | U16-9 | Normal Function: Srv Crdts; Test Function: Escape |
| D6 | Orange-Blue | J205-7 | U16-11 | Normal Function: Volume Dn; Test Function: Down |
| D7 | Orange-Violet | J205-8 | U16-7 | Normal Function: Volume Up; Test Function: Up |
| D8 | Orange-Gray | J205-9 | U16-5 | Normal Function: Begin Test; Test Function: Enter |

For D5-D8 the label area is a two-column sub-table: left column `Normal Function` over the function name (bold),
right column `Test Function` over the function name (bold), separated by a vertical rule. The first letter of
`Normal` / `Function` / `Srv Crdts` / `Volume Dn` etc. is partly clipped by the left border of the cell in the
scan; the readings are not in doubt. D1-D4 carry no function sub-table. The connector pins skip `J205-5` (D4 is
`J205-4`, D5 is `J205-6`).

## Flipper grounded switches (right column)

Each cell prints, top to bottom: wire (bold), connector-pin (bold), label, and the cell id (F1-F8) at the bottom
right.

| Switch | Wire | Connector-pin | Printed label |
| --- | --- | --- | --- |
| F1 | Black-Green | J208-13 | Lower Right Flipper E.O.S. |
| F2 | Blue-Violet | J212-12 | Lower Right Flipper Opto |
| F3 | Black-Blue | J208-12 | Lower Left Flipper E.O.S. |
| F4 | Blue-Gray | J212-11 | Lower Left Flipper Opto |
| F5 | Black-Violet | J208-11 | BASKET MADE OPTO |
| F6 | Black-Yellow | J212-10 | Upper Right Flipper Opto |
| F7 | Black--Gray | J208-10 | BASKET HOLD |
| F8 | Black-Blue | J212-9 | Upper Left Flipper Opto |

F7's wire prints with a doubled hyphen, `Black--Gray` (both editions). F3 and F8 both print the wire `Black-Blue`
(on `J208-12` and `J212-9`). The F5 label is three lines, `BASKET` / `MADE` / `OPTO`; F7's is `BASKET` / `HOLD`.

## Matrix cells

Each cell prints its description (multi-line text joined here by single spaces) and the two-digit address in its
bottom-right corner, column digit first, row digit second. Columns 7 and 8 print `NOT USED` in every row.

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 BALL LAUNCH | 21 SLAM TILT | 31 TROUGH EJECT | 41 STANDUP TARGET '3' |
| 2 | 12 BACKBOX BASKET | 22 COIN DOOR CLOSED | 32 TROUGH BALL 1 | 42 STANDUP TARGET 'P' |
| 3 | 13 START BUTTON | 23 RIGHT JET BUMPER | 33 TROUGH BALL 2 | 43 STANDUP TARGET 'T' |
| 4 | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH BALL 3 | 44 RIGHT RAMP ENTER |
| 5 | 15 SHOOTER LANE | 25 EJECT HOLE | 35 TROUGH BALL 4 | 45 LEFT RAMP ENTER |
| 6 | 16 LEFT RETURN LANE | 26 LEFT OUTLANE | 36 CENTER RAMP OPTO | 46 LEFT RAMP MADE |
| 7 | 17 RIGHT RETURN LANE | 27 RIGHT OUTLANE | 37 RIGHT LOOP ENTER OPTO | 47 LEFT LOOP ENTER |
| 8 | 18 LOWER RIGHT STANDUP TARGET | 28 UPPER RIGHT STANDUP TARGET | 38 RIGHT LOOP EXIT | 48 LEFT LOOP MADE |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 DEFENDER POSITION 4 | 61 LEFT JET BUMPER | 71 NOT USED | 81 NOT USED |
| 2 | 52 DEFENDER POSITION 3 | 62 MIDDLE JET BUMPER | 72 NOT USED | 82 NOT USED |
| 3 | 53 DEFENDER LOCK POSITION | 63 LEFT LOOP RAMP EXIT | 73 NOT USED | 83 NOT USED |
| 4 | 54 DEFENDER POSITION 2 | 64 RIGHT RAMP MADE | 74 NOT USED | 84 NOT USED |
| 5 | 55 DEFENDER POSITION 1 | 65 IN THE PAINT 4 | 75 NOT USED | 85 NOT USED |
| 6 | 56 JETS BALL DRAIN | 66 IN THE PAINT 3 | 76 NOT USED | 86 NOT USED |
| 7 | 57 LEFT SLINGSHOT | 67 IN THE PAINT 2 | 77 NOT USED | 87 NOT USED |
| 8 | 58 RIGHT SLINGSHOT | 68 IN THE PAINT 1 | 78 NOT USED | 88 NOT USED |

Notes on the cell text: the standup-target cells print the letter or digit in single quotes on its own line
(`'3'`, `'P'`, `'T'`). Cell 23 prints `RIGHT JET BUMPER` (in column 2, row 3) while the other two jet bumpers are
cells 61 and 62 (column 6). Cells 36 and 37 print `OPTO` as their last word. The four `IN THE PAINT` cells are
numbered 4, 3, 2, 1 in cells 65, 66, 67, 68 (descending with the address).

## Legend and footer

Below the table: `J2XX = CPU BOARD`, then a small empty rectangle (shaded, see below) followed by `= OPTO,
TYPICALLY CLOSED`. In the March edition a stray small mark sits between the rectangle and the `=` sign.

## Legend shading, measured

The legend `= OPTO, TYPICALLY CLOSED` is shown by a rectangle with a stippled light-grey background, and the cells it
marks are drawn with the same stippled grey. In the May scan the stipple is very faint (a bilevel-style dither on
a near-white page, with extra-bold text in the shaded cells); in the March scan it is a uniform light grey wash.

Method: both pages were rendered at 300 dpi and converted to 8-bit grey (255 = white). The cell grid was located by
detecting the long dark ruling lines (May x boundaries 576, 747, 922, 1094, 1269, 1446, 1620, 1783, 1954, 2159 px
and y boundaries 306, 486, 664, 840, 1016, 1192, 1366, 1540, 1716 px; March x 656, 827, 1002, 1178, 1354, 1528,
1701, 1864, 2035, 2244 px and y 311, 489, 667, 842, 1016, 1191, 1365, 1538, 1712 px). For each cell the "strip
mean" is the mean grey level of a small text-free rectangle (first choice: 30 px wide by 60 px tall at the
bottom-left of the cell, left of the cell number; for F1-F8 a strip at the right edge above the number; a
fallback rectangle was used only where the first touched ink). A second figure, for the May edition only, is the
share of background pixels (pixels more than 6 px away from any ink below grey 140, inside the cell with a 12 px
margin) that are below grey 250, which separates the faint May stipple from clean white: unshaded cells score
0.000-0.006, shaded cells 0.027-0.53. A cell is judged shaded in May when that share is at least 0.02, and in
March when its strip mean is below 240 (every March cell is either about 213-231 or about 252-255).

Legend rectangle: March interior mean 227 (share below 250: 1.00); May interior mean 223-239 depending on the
sub-area (the measured box includes a few dark border pixels), share below 250 about 0.13-0.22, against 254.6
for plain white paper next to it.

Result, identical in both editions: the shaded ("OPTO, TYPICALLY CLOSED") matrix cells are 31, 32, 33, 34, 35, 36,
37 (column 3, rows 1-7) and 51, 52, 53, 54, 55 (column 5, rows 1-5). Among the flipper-column cells F2, F4, F5, F6
and F8 are shaded. Not shaded: 38, 56, all of columns 1, 2, 4, 6, 7, 8, and F1, F3, F7. The D1-D8 cells and the row
header cells are not shaded. The method detects only background shading, not meaning: the shaded cells include the
trough cells 32-35 and the optos named in their text (36 `CENTER RAMP OPTO`, 37 `RIGHT LOOP ENTER OPTO`), the
`TROUGH EJECT` cell 31, the five defender positions 51-55 (including 53 `DEFENDER LOCK POSITION`), and F5
`BASKET MADE OPTO` plus the four flipper `Opto` cells; the unshaded cell 38 `RIGHT LOOP EXIT` and the unshaded F7
`BASKET HOLD` carry no shading in either edition.

| Cell | May strip mean | May share of background pixels below 250 | May judged | March strip mean | March judged |
| --- | ---: | ---: | --- | ---: | --- |
| 11 | 254.6 | 0.000 | unshaded | 255.0 | unshaded |
| 12 | 254.8 | 0.002 | unshaded | 255.0 | unshaded |
| 13 | 254.7 | 0.001 | unshaded | 255.0 | unshaded |
| 14 | 255.0 | 0.001 | unshaded | 255.0 | unshaded |
| 15 | 254.6 | 0.003 | unshaded | 255.0 | unshaded |
| 16 | 254.8 | 0.001 | unshaded | 255.0 | unshaded |
| 17 | 254.1 | 0.006 | unshaded | 255.0 | unshaded |
| 18 | 254.0 | 0.006 | unshaded | 255.0 | unshaded |
| 21 | 254.5 | 0.001 | unshaded | 255.0 | unshaded |
| 22 | 254.8 | 0.006 | unshaded | 255.0 | unshaded |
| 23 | 254.9 | 0.000 | unshaded | 254.8 | unshaded |
| 24 | 254.5 | 0.000 | unshaded | 255.0 | unshaded |
| 25 | 254.9 | 0.001 | unshaded | 255.0 | unshaded |
| 26 | 254.6 | 0.000 | unshaded | 255.0 | unshaded |
| 27 | 254.4 | 0.001 | unshaded | 255.0 | unshaded |
| 28 | 254.8 | 0.001 | unshaded | 255.0 | unshaded |
| 31 | 244.6 | 0.413 | shaded | 212.7 | shaded |
| 32 | 243.7 | 0.529 | shaded | 217.2 | shaded |
| 33 | 248.8 | 0.247 | shaded | 214.9 | shaded |
| 34 | 254.8 | 0.106 | shaded | 216.2 | shaded |
| 35 | 254.0 | 0.027 | shaded | 217.8 | shaded |
| 36 | 252.8 | 0.031 | shaded | 220.7 | shaded |
| 37 | 246.9 | 0.109 | shaded | 221.7 | shaded |
| 38 | 255.0 | 0.000 | unshaded | 255.0 | unshaded |
| 41 | 254.7 | 0.000 | unshaded | 254.6 | unshaded |
| 42 | 254.8 | 0.001 | unshaded | 254.6 | unshaded |
| 43 | 255.0 | 0.000 | unshaded | 254.5 | unshaded |
| 44 | 254.8 | 0.000 | unshaded | 254.6 | unshaded |
| 45 | 255.0 | 0.001 | unshaded | 254.6 | unshaded |
| 46 | 255.0 | 0.002 | unshaded | 254.2 | unshaded |
| 47 | 254.3 | 0.000 | unshaded | 254.2 | unshaded |
| 48 | 254.7 | 0.000 | unshaded | 255.0 | unshaded |
| 51 | 250.9 | 0.506 | shaded | 226.9 | shaded |
| 52 | 249.5 | 0.341 | shaded | 224.5 | shaded |
| 53 | 245.9 | 0.425 | shaded | 225.8 | shaded |
| 54 | 252.5 | 0.340 | shaded | 228.0 | shaded |
| 55 | 253.4 | 0.316 | shaded | 231.2 | shaded |
| 56 | 254.9 | 0.000 | unshaded | 254.9 | unshaded |
| 57 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 58 | 254.7 | 0.001 | unshaded | 255.0 | unshaded |
| 61 | 254.9 | 0.000 | unshaded | 254.7 | unshaded |
| 62 | 255.0 | 0.001 | unshaded | 254.8 | unshaded |
| 63 | 255.0 | 0.000 | unshaded | 254.9 | unshaded |
| 64 | 254.7 | 0.003 | unshaded | 254.8 | unshaded |
| 65 | 254.8 | 0.002 | unshaded | 254.7 | unshaded |
| 66 | 254.9 | 0.001 | unshaded | 255.0 | unshaded |
| 67 | 254.5 | 0.000 | unshaded | 255.0 | unshaded |
| 68 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 71 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 72 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 73 | 254.5 | 0.004 | unshaded | 255.0 | unshaded |
| 74 | 254.7 | 0.000 | unshaded | 255.0 | unshaded |
| 75 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 76 | 254.8 | 0.002 | unshaded | 255.0 | unshaded |
| 77 | 254.8 | 0.001 | unshaded | 255.0 | unshaded |
| 78 | 254.6 | 0.003 | unshaded | 255.0 | unshaded |
| 81 | 255.0 | 0.000 | unshaded | 255.0 | unshaded |
| 82 | 254.8 | 0.000 | unshaded | 255.0 | unshaded |
| 83 | 254.8 | 0.001 | unshaded | 255.0 | unshaded |
| 84 | 254.3 | 0.000 | unshaded | 255.0 | unshaded |
| 85 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| 86 | 254.5 | 0.001 | unshaded | 255.0 | unshaded |
| 87 | 254.5 | 0.002 | unshaded | 255.0 | unshaded |
| 88 | 254.9 | 0.000 | unshaded | 255.0 | unshaded |
| F1 | 254.8 | 0.003 | unshaded | 254.1 | unshaded |
| F2 | 247.3 | 0.278 | shaded | 221.6 | shaded |
| F3 | 254.4 | 0.005 | unshaded | 252.7 | unshaded |
| F4 | 252.0 | 0.251 | shaded | 222.8 | shaded |
| F5 | 253.7 | 0.120 | shaded | 223.4 | shaded |
| F6 | 252.8 | 0.088 | shaded | 224.2 | shaded |
| F7 | 254.9 | 0.001 | unshaded | 254.5 | unshaded |
| F8 | 253.1 | 0.227 | shaded | 221.9 | shaded |

## The Section 3 reprint of this table (May edition, PDF page 70, printed page `3-2`)

The May edition prints the same switch matrix a second time as the first page of the wiring section (PDF page 70,
left half, printed `3-2`, followed by the `SWITCH MATRIX CIRCUIT` drawing; the right half, `3-3`, holds the `DEDICATED
SWITCHES` wiring and `DEDICATED SWITCH CIRCUIT` drawings). That reprint is a cleaner scan, and the stippled shading
is clearly visible in it. Every printed cell, wire, connector-pin, IC pin and label on it was compared with the
`2-48` reading above and agrees (including `U208-7` for row 6, `Black--Gray` for F7, and `Srv Crdts` for D5; in
this scan the first letters of the D5-D8 `Normal`/`Function` labels are partly clipped by the cell border). The
same grid measurement (May 3-2 reprint: x boundaries 620, 788, 964, 1138, 1314, 1489, 1662, 1825, 1996, 2204 px; y
boundaries 484, 664, 842, 1018, 1192, 1368, 1543, 1717, 1891 px; share of non-ink background pixels below grey 250)
gives the same shaded set: cells 31, 32, 33, 34, 35, 36, 37 (shares 0.72-0.88, and 0.49 and 0.42 for 35 and 36,
which hold more text), cells 51, 52, 53, 54, 55 (0.52-0.75), and F2 (0.48), F4 (0.045; clearly shaded on the page, but
its text occupies most of the cell), F5 (0.37), F6 (0.48) and F8 (0.57). Unshaded cells measure 0.000-0.012. The
dedicated D1-D8 cells and the row-header cells are not shaded. The legend rectangle beside `= OPTO, TYPICALLY
CLOSED` is shaded the same way.

## Printed drawings accompanying this table (2-48 and 3-2)

- Title line: a diode symbol and an open switch contact between `White` (left) and `Green` (right).
- `SWITCH MATRIX CIRCUIT` (3-2): a `Column (example)` circuit (74HC237 into ULN2803, 1K to +12V, 470pf, J206 pin to
  `Green-XXX`, a diode toward the playfield) and a `Row (example)` circuit (J208 pin to `White-XXX`, 1N4148, LM339
  comparator with 1K pull-ups, 74LS240, 470pf), with the truth tables `COLUMN: INACTIVE H L OFF / ACTIVE L H ON`
  (columns A, B) and `ROW: SWITCH OPEN H H L OFF / SWITCH CLOSED L L H ON` (columns C, D, E). The text beneath says that the
  microprocessor strobes the column side continuously; that when point `A` toggles low the column side is active; that
  a closing switch makes the row side activate; that the `+` input to the LM339 drops below +5V so its output is low;
  and that corresponding row and column switches must be low at the same time for the microprocessor to consider
  the switch closed.
- `DEDICATED SWITCHES` (3-3): the CPU board `J205` pins 1-9 and 10 (`Black`), the wire names `Orange-Brown (U17-5) D1`,
  `Orange-Red (U17-7) D2`, `Orange-Black (U17-11) D3`, `Orange-Yellow (U17-9) D4`, `Orange-Green (U16-9) D5`,
  `Orange-Blue (U16-11) D6`, `Orange-Violet (U16-7) D7`, `Orange-Gray (U16-5) D8`, running to the `COIN DOOR INTERFACE
  BOARD` (`J1` and `J3`). The drawing prints CPU `J205` pins 1, 2, 3, 4, 6, 7, 8, 9 and 10 (no pin 5; pin 10 is `Black`
  and is grounded). `J205` pin to coin door interface `J1` pin to `J3` pin (switch): D1 `J205-1` to `J1-8` to `J3-4`;
  D2 `J205-2` to `J1-7` to `J3-5`; D3 `J205-3` to `J1-6` to `J3-6`; D4 `J205-4` to `J1-5`, and the `J3` side of this line
  prints no pin number and no switch symbol; D5 `J205-6` to `J1-4` to `J3-7`; D6 `J205-7` to `J1-3` to `J3-8`; D7 `J205-8` to
  `J1-2` to `J3-9`; D8 `J205-9` to `J1-1` to `J3-11`; `Black` `J205-10` to `J1-10` to `J3-3` (the common return of the
  switches). Beneath the drawing: the legend `Coin Acceptor Switches` (`D1 - Left Coin Chute`, `D2 - Center Coin Chute`, `D3 - Right Coin
  Chute`, `D4 - Fourth Coin Chute`) and `Control Switches` (`D5 - Normal Function, Service Credits; Test Function,
  Escape`, `D6 - Normal Function, Volume Down; Test Function, Down`, `D7 - Normal Function, Volume Up; Test Function, Up`,
  `D8 - Normal Function, Begin Test; Test Function, Enter`). `DEDICATED SWITCH CIRCUIT` text: the dedicated switches
  operate like the matrix except that a direct tie to ground replaces the column circuit, so the column side is
  constantly active (low); when a switch closes the row side (dedicated input) activates, the LM339 `+` input drops below
  +5V and the output is low; when it opens the `+` input is above +5V and the output is high and the row inactive.

## Differences between the March and May printings of this table

No difference in any printed cell, wire, connector, IC pin, label or footnote was found (every one of the 64
cells, the D1-D8 and F1-F8 blocks, the row and column headers and the legend text were compared on rendered
crops). The shading pattern is identical. The only differences are scan quality (the May shading is much fainter
and its shaded-cell text is bolder; the March rendering is a lower-resolution scan with a visible grey wash) and
the printed folio (`2-48` in both; in the March edition the page stands alone, in the May edition it shares the
spread with the Lamp Matrix `2-49`).

## Uncertain readings

None in this table. The partly clipped first letters of `Normal`, `Function` and the function names in D5-D8 are
a scan-edge effect and read unambiguously from the repeated words.
