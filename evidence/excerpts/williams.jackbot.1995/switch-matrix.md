# Jack*Bot — Switch Matrix (wiring)

Transcribed from `Williams_1995_Jack_Bot_English_Manual.pdf` (SHA-256
`8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`), PDF page 114, printed page `2-36`: the
`Switch Matrix` table with its dedicated grounded switch column (D1-D8), its flipper grounded switch column
(F1-F8), the row-header column, the 8 x 8 matrix cells, the legend and the switch drawing in the title line.
The same table is reprinted in Section 3 on PDF page 120 (printed `3-2`) and in the quick-reference sheet on PDF
page 149 (lower half, no printed folio); both reprints were read as well and the differences are listed below.
The Dedicated Switches wiring page (PDF page 121, printed `3-3`) is transcribed at the end of this file.
Transcriber: curator, read from the rendered page (300 dpi scan), not from OCR text.

The title line prints `Switch Matrix`, then at the right a switch drawing: the label `WHITE`, a diode symbol (arrow
and bar), an open switch contact, and the label `GREEN`.

Layout, left to right: a `Dedicated Grounded Switches` block (D1-D8, one cell per matrix row), a row-header
column, eight matrix columns, and a `Flipper Grounded Switches` block (F1-F8). The dedicated block, the row
header and the flipper block each carry one cell per matrix row (rows 1-8), so D1/F1 are level with row 1, and
so on. The top-left corner cell of the grid is divided diagonally and prints `COLUMN` (upper right) and `ROW`
(lower left).

## Matrix drive columns

Each column header prints, top to bottom: the column number, the wire (on two lines, e.g. `Green-` over
`Brown`), the connector-pin and the IC pin.

| Column | Wire | Connector-pin | Drive IC pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

Column 8's connector-pin is `J207-9`; there is no `J207-8`.

## Matrix return rows

Each row header prints, top to bottom: the wire, the connector-pin, the IC pin and the row number (large, lower
left).

| Row | Wire | Connector-pin | Return IC pin |
| --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

The row connector pins skip `J209-6` (row 5 is `J209-5`, row 6 is `J209-7`).

## Dedicated grounded switches (left block)

Each cell prints, top to bottom: the wire in abbreviated form, the connector-pin, a label, and the cell id
(D1-D8) at the bottom right. Wire colours are abbreviated here (`Org-Brn`), where the matrix columns and rows
spell them out. D1-D4 carry a one-name label; D5-D8 carry a two-column sub-table (left `Normal` over the function,
right `Test` over the function). No IC pin is printed in these cells (the Section 3 wiring page, below, prints
`(U17-5)` after every dedicated wire).

| Switch | Wire (as printed) | Connector-pin | Printed label |
| --- | --- | --- | --- |
| D1 | Org-Brn | J205-1 | Left Coin Chute |
| D2 | Org-Red | J205-2 | Center Coin Chute |
| D3 | Org-Blk | J205-3 | Right Coin Chute |
| D4 | Org-Yel | J205-4 | 4th Coin Chute |
| D5 | Org-Grn | J205-6 | Normal: Service Credit; Test: Escape |
| D6 | Org-Blu | J205-7 | Normal: Volume Down; Test: Down |
| D7 | Org-Vio | J205-8 | Normal: Volume Up; Test: Up |
| D8 | Org-Gry | J205-9 | Normal: Begin Test; Test: Enter |

D1-D4's label wraps to a second line (`Left Coin` / `Chute`, `Center Coin` / `Chute`, `Right Coin` / `Chute`, `4th
Coin` / `Chute`). In D5-D8 the sub-table text is in small bold type: `Normal` / `Service` / `Credit` beside `Test` /
`Escape`; `Normal` / `Volume` / `Down` beside `Test` / `Down`; `Normal` / `Volume` / `Up` beside `Test` / `Up`;
`Normal` / `Begin` / `Test` beside `Test` / `Enter`. The word under `Normal` in D5 prints `Service Credit` (singular
`Credit`; the Section 3 function list prints `Service Credits`). The connector pins skip `J205-5` (D4 is `J205-4`,
D5 is `J205-6`).

## Flipper grounded switches (right block)

Each cell prints, top to bottom: the wire, the connector-pin, a label and the cell id (F1-F8) at the bottom
right. The legend (below) prints `J9XX = FLIPTRONIC II BOARD`; no comparator or IC pin is printed in these cells.

| Switch | Wire | Connector-pin | Printed label | Shaded |
| --- | --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right E.O.S. | no |
| F2 | Blue-Violet | J905-1 | Lower Right Opto | yes |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S. | no |
| F4 | Blue-Gray | J905-2 | Lower Left Opto | yes |
| F5 | Black-Violet | J906-4 | Visor Closed | no |
| F6 | Black-Yellow | J905-3 | Upper Right Opto | yes |
| F7 | Black-Gray | J906-5 | Visor Open | no |
| F8 | Black-Blue | J905-5 | Upper Left Opto | yes |

F3 and F8 both print the wire `Black-Blue` (on `J906-3` and `J905-5`). The `J906` pins used are 1, 3, 4, 5 (no
`J906-2`), and the `J905` pins used are 1, 2, 3, 5 (no `J905-4`). In the shaded F2, F4, F6 and F8 cells the text
is overprinted by the stipple; each was read on a 3.5x enlargement and the readings `J905-1`, `J905-2`, `J905-3`,
`J905-5` are certain on the enlargement (all four readings agree on the Section 3 and quick-reference reprints).

## Matrix cells

Each cell prints its description (multi-line text joined here by single spaces) and the two-digit address in its
bottom-right corner, column digit first, row digit second. Columns 7 and 8 print `NOT USED` in every row. `*`
marks a shaded cell (legend `OPTO, TYPICALLY CLOSED`, measured below).

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 LOWER LEFT 10 POINT | 21 SLAM TILT | 31 TROUGH JAM | 41 VISOR 1 (LEFT) * |
| 2 | 12 UPPER LEFT 10 POINT | 22 COIN DOOR CLOSED | 32 TROUGH 1 (RIGHT) | 42 VISOR 2 * |
| 3 | 13 START BUTTON | 23 BUY EXTRA BALL | 33 TROUGH 2 | 43 VISOR 3 * |
| 4 | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH 3 | 44 VISOR 4 * |
| 5 | 15 RAMP IS DOWN | 25 LEFT OUTLANE | 35 TROUGH 4 LEFT | 45 VISOR 5 (RIGHT) * |
| 6 | 16 HIGH DROP TARGET * | 26 LEFT FLIPPER LANE | 36 RAMP EXIT | 46 FAR LEFT EJECT |
| 7 | 17 CENTER DROP TARGET * | 27 RIGHT FLIPPER LANE | 37 RAMP ENTRANCE | 47 LEFT EJECT HOLE (VISOR) |
| 8 | 18 LOW DROP TARGET * | 28 RIGHT OUTLANE | 38 TARGET UNDER RAMP | 48 RIGHT EJECT HOLE (VISOR) |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 5-BANK TARGET 1 (UPPER) | 61 UPPER JET BUMPER | 71 NOT USED | 81 NOT USED |
| 2 | 52 5-BANK TARGET 2 | 62 LEFT JET BUMPER | 72 NOT USED | 82 NOT USED |
| 3 | 53 5-BANK TARGET 3 | 63 LOWER JET BUMPER | 73 NOT USED | 83 NOT USED |
| 4 | 54 5-BANK TARGET 4 | 64 RIGHT SLINGSHOT | 74 NOT USED | 84 NOT USED |
| 5 | 55 5-BANK TARGET 5 (LOWER) | 65 LEFT SLINGSHOT | 75 NOT USED | 85 NOT USED |
| 6 | 56 VORTEX UPPER | 66 RIGHT 10 POINT | 76 NOT USED | 86 NOT USED |
| 7 | 57 VORTEX CENTER | 67 HIT ME TARGET | 77 NOT USED | 87 NOT USED |
| 8 | 58 VORTEX LOWER | 68 BALL SHOOTER | 78 NOT USED | 88 NOT USED |

Notes on the cell text:

- Cell 35 prints three lines `TROUGH` / `4` / `LEFT`; cell 32 prints `TROUGH` / `1` / `(RIGHT)`; cells 33 and 34
  print `TROUGH` / `2` and `TROUGH` / `3`. Cell 31 prints `TROUGH` / `JAM`. None of the trough cells is shaded.
- Cell 41 prints `VISOR` / `1` / `(LEFT)` and cell 45 prints `VISOR` / `5` / `(RIGHT)`; in the shaded cells the
  brackets of `(LEFT)` and `(RIGHT)` are partly overprinted by the stipple but read unambiguously on the
  enlargement.
- Cell 51 prints `5-BANK` / `TARGET` / `1` / `(UPPER)` and cell 55 prints `5-BANK` / `TARGET` / `5` / `(LOWER)`;
  the parenthesised word touches the address digits at the bottom right in both cells.
- Cells 47 and 48 print `LEFT` / `EJECT` / `HOLE` / `(VISOR)` and `RIGHT` / `EJECT` / `HOLE` / `(VISOR)`; the
  `(VISOR)` line touches the address digits.
- Cell 16 `HIGH` / `DROP` / `TARGET`, cell 17 `CENTER` / `DROP` / `TARGET`, cell 18 `LOW` / `DROP` / `TARGET`
  (all shaded; the stipple overprints the text, which is legible on the enlargement).
- Cell 66 prints `RIGHT` / `10` / `POINT` while the other `10 POINT` cell (11, `LOWER LEFT 10 POINT`) and cell 12
  (`UPPER LEFT 10 POINT`) are in column 1. Cell 67 prints `HIT ME` / `TARGET` with a double space between `HIT`
  and `ME`.
- Cell 21 prints `SLAM` / `TILT`; cell 24 prints `ALWAYS` / `CLOSED`; cell 22 prints `COIN` / `DOOR` / `CLOSED`.

## Legend and footer

Below the table, one line: `J2XX = CPU BOARD; J9XX = FLIPTRONIC II BOARD`, then a small rectangle filled with the
same stipple as the shaded cells, followed by `= OPTO, TYPICALLY CLOSED`. The printed folio below the table is
`2-36`.

## Shading, measured

The shading is a dither of fine black dots (a bilevel scan; the same stipple fills the legend rectangle). Shaded
cells carry the stipple over their whole background and their text is overprinted by it; unshaded cells are white
with scan speckle.

Method: page rendered at 300 dpi and converted to 8-bit grey (255 = white, 0 = black). The cell grid was located
from the long dark ruling lines (PDF page 114 matrix x boundaries 744, 895, 1044, 1195, 1350, 1500, 1652, 1809,
1966 px; D block x 290-484; F block x 1999-2190; y boundaries 571, 717, 867, 1017, 1167, 1320, 1464, 1613,
1765 px; the column-5/6 boundary at 1500 is interpolated because its thin line is broken). For every cell a
14 px margin from the ruling lines was removed, solid ink (text and ruling) was found by morphological opening of
the pixels darker than grey 100 with a 5 x 5 square, a 7 px halo around the solid ink was excluded, and the
mean grey of the remaining background pixels was computed ("background mean"). "Interior mean" is the plain mean
of the cell interior including text. A cell is judged shaded when its background mean is below 195. The
separation is wide: every shaded cell measures 155-189 (background mean), every unshaded cell measures 208-243;
there is no value in between. Because the scan carries speckle, unshaded cells do not reach 255.

| Cell | Interior mean (p.114) | Background mean p.114 (2-36) | Background mean p.120 (3-2) | Background mean p.149 (quick ref.) | Judged |
| --- | ---: | ---: | ---: | ---: | --- |
| 11 | 218.5 | 228.6 | 225.4 | 223.7 | unshaded |
| 12 | 221.9 | 223.3 | 222.3 | 223.6 | unshaded |
| 13 | 230.3 | 232.4 | 231.9 | 233.4 | unshaded |
| 14 | 227.2 | 232.4 | 230.4 | 231.4 | unshaded |
| 15 | 228.6 | 239.5 | 238.6 | 239.2 | unshaded |
| 16 | 159.1 | 167.0 | 168.5 | 173.2 | shaded |
| 17 | 158.5 | 171.4 | 168.9 | 174.2 | shaded |
| 18 | 159.4 | 170.3 | 174.2 | 184.6 | shaded |
| 21 | 237.8 | 241.3 | 242.2 | 242.5 | unshaded |
| 22 | 220.7 | 222.6 | 222.0 | 224.2 | unshaded |
| 23 | 227.9 | 229.8 | 227.3 | 234.3 | unshaded |
| 24 | 225.2 | 232.1 | 228.4 | 230.5 | unshaded |
| 25 | 231.3 | 234.3 | 234.3 | 236.6 | unshaded |
| 26 | 220.9 | 225.0 | 226.4 | 226.3 | unshaded |
| 27 | 219.1 | 225.3 | 223.6 | 224.0 | unshaded |
| 28 | 228.3 | 231.8 | 230.5 | 232.9 | unshaded |
| 31 | 229.8 | 235.2 | 233.1 | 236.1 | unshaded |
| 32 | 224.8 | 224.8 | 226.7 | 226.9 | unshaded |
| 33 | 237.4 | 237.4 | 238.3 | 238.1 | unshaded |
| 34 | 236.4 | 239.3 | 238.2 | 236.4 | unshaded |
| 35 | 229.3 | 235.5 | 230.3 | 232.1 | unshaded |
| 36 | 234.0 | 242.9 | 237.5 | 238.4 | unshaded |
| 37 | 222.7 | 232.1 | 230.9 | 228.4 | unshaded |
| 38 | 216.8 | 227.1 | 223.6 | 223.8 | unshaded |
| 41 | 159.6 | 162.7 | 166.6 | 171.5 | shaded |
| 42 | 173.3 | 178.9 | 179.7 | 187.7 | shaded |
| 43 | 174.4 | 183.2 | 179.0 | 188.8 | shaded |
| 44 | 172.7 | 181.5 | 179.7 | 186.0 | shaded |
| 45 | 164.1 | 170.4 | 171.4 | 178.6 | shaded |
| 46 | 226.9 | 230.2 | 227.3 | 229.0 | unshaded |
| 47 | 212.2 | 213.2 | 211.5 | 217.5 | unshaded |
| 48 | 211.4 | 211.4 | 211.5 | 214.4 | unshaded |
| 51 | 206.6 | 210.2 | 209.2 | 210.2 | unshaded |
| 52 | 223.5 | 223.5 | 224.2 | 230.3 | unshaded |
| 53 | 224.2 | 226.6 | 223.0 | 228.2 | unshaded |
| 54 | 223.0 | 229.6 | 226.1 | 230.5 | unshaded |
| 55 | 208.5 | 218.1 | 213.3 | 214.4 | unshaded |
| 56 | 226.0 | 229.3 | 224.9 | 227.7 | unshaded |
| 57 | 224.5 | 228.6 | 227.6 | 227.6 | unshaded |
| 58 | 225.9 | 233.4 | 233.0 | 232.4 | unshaded |
| 61 | 215.6 | 223.9 | 221.2 | 220.2 | unshaded |
| 62 | 223.6 | 227.4 | 229.2 | 228.1 | unshaded |
| 63 | 219.0 | 226.4 | 226.9 | 225.8 | unshaded |
| 64 | 222.5 | 224.4 | 222.8 | 228.0 | unshaded |
| 65 | 227.7 | 230.8 | 229.2 | 227.8 | unshaded |
| 66 | 226.9 | 229.9 | 231.3 | 231.8 | unshaded |
| 67 | 227.8 | 232.9 | 231.5 | 234.0 | unshaded |
| 68 | 227.5 | 227.5 | 227.8 | 229.1 | unshaded |
| 71 | 234.1 | 236.9 | 238.8 | 237.5 | unshaded |
| 72 | 235.0 | 238.0 | 239.4 | 238.8 | unshaded |
| 73 | 236.1 | 237.3 | 238.5 | 238.8 | unshaded |
| 74 | 235.0 | 237.7 | 238.9 | 239.0 | unshaded |
| 75 | 235.5 | 238.4 | 239.9 | 238.8 | unshaded |
| 76 | 233.8 | 236.4 | 238.1 | 237.8 | unshaded |
| 77 | 235.2 | 238.0 | 239.6 | 238.8 | unshaded |
| 78 | 235.5 | 238.3 | 238.8 | 239.3 | unshaded |
| 81 | 234.4 | 236.6 | 238.2 | 236.3 | unshaded |
| 82 | 235.8 | 238.2 | 236.5 | 239.8 | unshaded |
| 83 | 236.2 | 238.2 | 239.2 | 237.2 | unshaded |
| 84 | 234.2 | 238.4 | 241.0 | 240.6 | unshaded |
| 85 | 236.1 | 238.6 | 239.0 | 240.2 | unshaded |
| 86 | 234.7 | 237.3 | 236.6 | 237.4 | unshaded |
| 87 | 234.9 | 237.7 | 238.8 | 238.5 | unshaded |
| 88 | 235.9 | 238.5 | 239.2 | 239.1 | unshaded |
| D1 | 215.4 | 217.8 | 217.0 | 219.7 | unshaded |
| D2 | 208.7 | 214.0 | 209.3 | 216.1 | unshaded |
| D3 | 213.6 | 213.6 | 210.2 | 216.7 | unshaded |
| D4 | 216.9 | 218.6 | 215.3 | 219.1 | unshaded |
| D5 | 205.1 | 222.1 | 215.8 | 221.6 | unshaded |
| D6 | 205.3 | 212.6 | 216.3 | 217.2 | unshaded |
| D7 | 209.3 | 213.6 | 214.2 | 218.6 | unshaded |
| D8 | 207.6 | 218.8 | 214.1 | 222.1 | unshaded |
| F1 | 206.0 | 217.0 | 211.4 | 208.9 | unshaded |
| F2 | 148.5 | 165.9 | 163.3 | 163.5 | shaded |
| F3 | 210.6 | 215.1 | 212.2 | 220.1 | unshaded |
| F4 | 146.5 | 158.4 | 161.4 | 156.0 | shaded |
| F5 | 210.3 | 219.7 | 214.6 | 221.6 | unshaded |
| F6 | 143.2 | 154.8 | 156.4 | 167.7 | shaded |
| F7 | 210.6 | 214.8 | 216.4 | 216.9 | unshaded |
| F8 | 148.6 | 159.9 | 163.1 | 173.4 | shaded |

(Grids for the reprints, same method: PDF page 120 matrix x 771, 912, 1055, 1198, 1343, 1484, 1631, 1782, 1930 px,
D block x 349-526, F block x 1960-2135, y 688, 818, 952, 1085, 1218, 1353, 1482, 1615, 1750 px; PDF page 149
matrix x 718, 869, 1022, 1172, 1330, 1482, 1638, 1795, 1952 px, D block x 273-464, F block x 1988-2172, y 1860,
1990, 2128, 2265, 2403, 2543, 2679, 2817, 2955 px. The row-header cells were also measured and are not shaded.)

Result, identical on all three printings: the shaded ("OPTO, TYPICALLY CLOSED") matrix cells are 16, 17, 18
(column 1, rows 6-8: `HIGH DROP TARGET`, `CENTER DROP TARGET`, `LOW DROP TARGET`) and 41, 42, 43, 44, 45 (column 4,
rows 1-5: `VISOR 1 (LEFT)` through `VISOR 5 (RIGHT)`). Among the flipper-block cells F2, F4, F6 and F8 (the four
`Opto` cells) are shaded. Not shaded: every other matrix cell, in particular all trough cells (31-35), the ramp
cells 36-38, the eject cells 46-48, the five-bank cells 51-55, `RAMP IS DOWN` (15), F1 and F3 (the `E.O.S.` cells),
F5 `Visor Closed` and F7 `Visor Open`, all D1-D8 cells and the row-header cells. The method detects background
shading only, not construction: it says nothing about the nature of the unshaded switches.

Cells 47, 48, 51 and 55 measure the lowest of the unshaded group (208-218) because their text sits close to the
cell walls and the scan has more speckle there; the gap to the shaded group (<= 189) is still about 20 grey levels
and the enlarged crops show them white.

## The Section 3 reprint (PDF page 120, printed `3-2`) and the quick-reference reprint (PDF page 149)

PDF page 120 (printed `3-2`) is headed `SWITCH MATRIX` and reprints the whole table, followed by a `SWITCH MATRIX
CIRCUIT` drawing (CPU board `Column (example)`: `LS374SC` output into an inverter, point `B`, to `J207`, point `A`,
`+12V` pull-up, `Green-XXX` to the playfield switch and a diode; `Row (example)`: `White-XXX` from `J209` through
`1N4148`, `1KΩ`, `470pf` (point `C`) to the `+` input (point `D`) of the `LM339` (`1.2KΩ` to `+12V`, `10KΩ` and `+5V`
on the other input) and the `74LS240` input (point `E`); and the truth tables `COLUMN | A | B`: `INACTIVE H L OFF`,
`ACTIVE L H ON`; `ROW | C | D | E`: `SWITCH OPEN H H L OFF`, `SWITCH CLOSED L L H ON`) and a text of which the first
sentence pair and the closing paragraph read: `The microprocessor is constantly strobing the column side of the
switch. When point "A" on the column circuit toggles low, the column side is active.` and `When a switch closes, the
row side of the circuit activates. The "+" input to the LM339 drops below +5V, therefore, its output is low.
Corresponding row and column switches must be low at the same time for the switch to be considered closed by the
microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is
inactive.` Its legend line prints `J2XX = CPU BOARD; J9XX = FLIPTRONIC II BOARD` and the `= OPTO, TYPICALLY CLOSED`
rectangle. Printed folio `3-2`.

PDF page 149 holds the quick-reference sheet: the Lamp Matrix in the upper half and this Switch Matrix in the
lower half, titled `SWITCH MATRIX` and with the same title-line drawing, legend and shading; it carries no folio.

Every printed cell, wire, connector-pin, IC pin and label of the grid, the column and row headers, the D block and
the F block on both reprints was compared with the `2-36` reading above, tile by tile, and agrees, including
`J207-9` for column 8, `J209-7` for row 6, `J905-1/-2/-3/-5` and `J906-1/-3/-4/-5` in the F block, `Visor Closed` and
`Visor Open` for F5 and F7, and `TROUGH 4 LEFT` for cell 35. Shading pattern identical (table above).

Differences found:

1. PDF page 149, D6: the wire prints `Org-Biu` (the second letter reads as an `i`, the `l` of `Blu` being drawn
   short); pages 114 and 120 print `Org-Blu`. Read on a 4x enlargement; judged a print or scan artefact of the
   reprint's lettering, not a different wire. The structured reading is `Org-Blu`.
2. PDF page 120 and PDF page 149 print the folio only on 120 (`3-2`); 149 prints none (not a content difference).
3. Scan quality: page 114 is the sharpest, page 149 slightly softer, and the stipple differs a little in density
   (page 149's background means in most shaded cells are up to about 14 grey levels lighter than page 114's). No cell content differs.

No other differences were found: all 64 cell texts, all 8 column headers, all 8 row headers, D1-D8, F1-F8 and the
legend are the same on `2-36`, `3-2` and the quick-reference sheet.

## Dedicated Switches (PDF page 121, printed `3-3`)

The page is headed `DEDICATED SWITCHES` and shows two dashed boxes: `CPU BOARD` (left, connector `J205`) and `COIN
DOOR INTERFACE BOARD` (right, connectors `J1` and `J3`), joined by nine wires. Left to right the wire label,
then the `J1` pin, then the `J3` pin, then a switch. Wire label text is printed above each line as `Orange-<colour>
(U17-5) D<n>`; the black line is labelled `Black`.

| Switch | CPU `J205` pin | Wire label, as printed | Coin door interface `J1` pin | `J3` pin | Switch symbol at `J3` |
| --- | ---: | --- | ---: | ---: | --- |
| D1 | 1 | Orange-Brown (U17-5) D1 | 14 | 4 | yes |
| D2 | 2 | Orange-Red (U17-5) D2 | 13 | 5 | yes |
| D3 | 3 | Orange-Black (U17-5) D3 | 12 | 6 | yes |
| D4 | 4 | Orange-Yellow (U17-5) D4 | 17 | (blank) | (none; the line ends at the `J3` connector with no pin number and no switch) |
| D5 | 6 | Orange-Green (U17-5) D5 | 11 | 7 | yes |
| D6 | 7 | Orange-Blue (U17-5) D6 | 10 | 8 | yes |
| D7 | 8 | Orange-Violet (U17-5) D7 | 8 | 9 | yes |
| D8 | 9 | Orange-Gray (U17-5) D8 | 9 | 11 | yes |
| (common) | 11 | Black | 15 | 3 | return rail joining the right ends of all switches |

The `J205` pin column prints 1, 2, 3, 4, 6, 7, 8, 9, 11 (no pin 5, no pin 10); pin 11 is tied to the ground symbol
at the lower left of the CPU box. The `J1` column prints 14, 13, 12, 17, 11, 10, 8, 9, 15 (top to bottom). The `J3`
column prints 4, 5, 6, (blank), 7, 8, 9, 11, 3. Seven switch symbols (open contacts) are drawn, for D1-D3 and
D5-D8; their right ends are joined to a vertical rail that returns to `J3` pin 3 and from there, through `J1` pin
15, to the black wire on `J205` pin 11. Every dedicated wire label prints the same IC pin `(U17-5)`, so as printed it
cannot be a per-switch IC pin (the D cells on `2-36` print none).

Below the drawing the page prints two lists:

- `Coin Acceptor Switches` (underlined heading): `D1 - Left Coin Chute`, `D2 - Center Coin Chute`, `D3 - Right Coin
  Chute`, `D4 - Fourth Coin Chute`.
- `Control Switches` (underlined heading): `D5 - Normal Function, Service Credits; Test Function, Escape`, `D6 -
  Normal Function, Volume Down; Test Function, Down`, `D7 - Normal Function, Volume Up; Test Function, Up`, `D8 -
  Normal Function, Begin Test; Test Function, Enter`.

The lower drawing, headed `DEDICATED SWITCH CIRCUIT`, shows the CPU board input (`74LS240` input `C`, `+5V`, `LS374SC`,
`10KΩ`, `LM339`, `+12V`, `1.2KΩ`, `1KΩ`, point `A`, point `B`, `1N4148`, `470pf`, `Dedicated Input`) to connector
`J205`, wire `Orange-XXX` to the `COIN DOOR INTERFACE BOARD` (pins `X`, `15`, `3`) and a `Coin Acceptor or Control
Switch`; and a truth table `SWITCH | A | B | C`: `OPEN H H L OFF`, `CLOSED L L H ON`; the black wire `J205` pin `11` to `J1` pin
`15` and `J3` pin `3`. Text: `The dedicated switches operate similar in the matrix, except that instead of a column
circuit there is a direct tie to ground. Therefore, the column side is constantly active (low).` and `When a switch
closes, the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V,
therefore the output is low. Since the row circuit (dedicated input) is tied directly to ground through the switch,
the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above
+5V, it output is high and the row is inactive.` (printed `it output`, as shown). Folio `3-3`.

## Notes on spelling and suspected typos

- Printed `Service Credit` (D5 on 2-36) against `Service Credits` on 3-3: not a conflict about the device.
- Printed `4th Coin Chute` (2-36) and `Fourth Coin Chute` (3-3): two spellings of one label.
- `it output` and `similar in the matrix` in the 3-3 text are printed so (probably `its output`, `similar to the matrix`).
- On 3-3 every dedicated wire carries `(U17-5)`; the D1-D8 cells on 2-36 carry no IC pin. Whether the IC pin is
  a copy error cannot be told from this manual.
- Page 149 D6 `Org-Biu`: see difference 1 above.
- The column and row headers use spelled-out colours (`Green-Brown`); the D block uses abbreviations (`Org-Brn`);
  the F block uses spelled-out colours.

## Uncertain readings

- F2, F4, F6, F8 and cells 16-18, 41-45 sit under the stipple. All were read on 2x-3.5x enlargements and agree on
  all three printings; none is in real doubt. The brackets in `(LEFT)` / `(RIGHT)` of cells 41 and 45 are the
  least clear glyphs, still unambiguous across the three printings.
- The measurement thresholds (195 grey) were chosen from the observed gap; nothing else decides the shading
  statement.
