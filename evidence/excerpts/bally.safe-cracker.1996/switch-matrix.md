# Safe Cracker — Switch Matrix (wiring)

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`, PDF page 114, printed page `2-42` (top part of the
page): the `SWITCH MATRIX` table with its `Dedicated Grounded Switches` column (D1-D8), its `Flipper Grounded
Switches` column (F1-F8), the 8 x 8 matrix cells, the legend and the switch drawing in the title line. The
bottom part of the same page is the `SWITCH LOCATIONS` list (`switch-locations.md`). The Section 3 reprint of
the same table (PDF page 126, printed page `3-2`) and the `DEDICATED SWITCHES` wiring drawing (PDF page 127,
printed page `3-3`) are transcribed below. Read from the rendered page (300 dpi scan), not from the OCR text.

The title line prints `SWITCH MATRIX`, then at the right a switch drawing with the label `White` (left), a line
with a diode arrow pointing right into a bar, an open switch contact, and the label `Green` (right).

## Matrix drive columns

Printed in the header row of the grid: column number (bold), then wire name over two lines (`Green-` over the
colour, bold), then the connector pin, then the IC pin.

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
left). Column 8 prints `J206-9` (no `J206-8` is printed).

## Matrix return rows

Printed in the left header column of the grid: row number (bold), then wire name over two lines (`White-` over
the colour, bold), then the connector pin, then the IC pin.

| Row | Wire | Connector-pin | Return IC pin |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | J208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

Row 6 prints `J208-7`; the pin `J208-6` is not printed on any row (row 5 is `J208-5`, row 6 is `J208-7`).

## Dedicated grounded switches (left column)

Header cell prints `Dedicated` / `Grounded` / `Switches`. Each cell prints, top to bottom: wire (bold), connector-pin
and IC pin on one line (bold), the label (bold), and the cell id (D1-D8) at the bottom right.

| Switch | Wire | Connector-pin | IC pin | Printed label |
| --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | U17-5 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | U17-7 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | U17-11 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | U17-9 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | U16-9 | Normal Function: Ser Credits; Test Function: Esc |
| D6 | Orange-Blue | J205-7 | U16-11 | Normal Function: Vol Down; Test Function: Down |
| D7 | Orange-Violet | J205-8 | U16-7 | Normal Function: Vol Up; Test Function: Up |
| D8 | Orange-Gray | J205-9 | U16-5 | Normal Function: Begin Test; Test Function: Enter |

Notes:
- For D5-D8 the label area is a two-column sub-table: the left column prints `Normal` / `Function` in small
  type over the function name (bold), the right column `Test` / `Function` in small type over the function name
  (bold), separated by a vertical rule. D1-D4 carry no function sub-table.
- D2 prints its label on two lines: `Center` then `Coin Chute` (id `D2` at the right of the second line).
- D5 prints `Ser Credits` (not `Srv Credits`); this is the printed spelling. The `DEDICATED SWITCHES` drawing
  (PDF page 127) spells it `Service Credits`.
- The connector pins skip `J205-5` (D4 is `J205-4`, D5 is `J205-6`).

## Flipper grounded switches (right column)

Header cell prints `Flipper` / `Grounded` / `Switches`. Each cell prints, top to bottom: wire (bold),
connector-pin, label (bold, two lines) with the cell id (F1-F8) at the right of the second label line.

| Switch | Wire | Connector-pin | Printed label | Shaded |
| --- | --- | --- | --- | --- |
| F1 | Black-Green | J208-13 | Lower Right Flipper EOS | no |
| F2 | Blue-Violet | J212-12 | Lower Right Flipper Opto | yes |
| F3 | Black-Blue | J208-12 | Lower Left Flipper EOS | no |
| F4 | Blue-Gray | J212-11 | Lower Left Flipper Opto | yes |
| F5 | Black-Violet | J208-11 | Upper Right Flipper EOS | no |
| F6 | Black-Yellow | J212-10 | Upper Right Flipper Opto | yes |
| F7 | Black-Gray | J208-10 | Upper Left Flipper EOS | no |
| F8 | Black-Blue | J212-9 | Upper Left Flipper Opto | yes |

Notes: F3 and F8 both print the wire `Black-Blue` (on `J208-12` and `J212-9`). F5 and F7 have an empty strip
below the label on this page (the Section 3 reprint prints `(NOT USED)` there, see below). In the shaded cells the
text is printed bold over the grey stipple; every wire and pin was read on 2x enlargements.

## Matrix cells

Each cell prints its description (multi-line text joined here by single spaces) and the two-digit address in
its bottom-right corner, column digit first, row digit second. `Shaded` records whether the cell has the grey
halftone background of the legend.

### Column 1 and 2

| Cell | Printed label | Shaded |
| --- | --- | --- |
| 11 | TP TROUGH (ROOF) | no |
| 12 | TP TROUGH (VARI) | no |
| 13 | START BUTTON | no |
| 14 | PLUMB BOB TILT | no |
| 15 | RIGHT ORBIT | no |
| 16 | LEFT OUTLANE | no |
| 17 | RIGHT OUTLANE | no |
| 18 | BALL SHOOTER | no |
| 21 | SLAM TILT | no |
| 22 | COIN DOOR CLOSED | no |
| 23 | NOT USED | no |
| 24 | ALWAYS CLOSED | no |
| 25 | UPPER RIGHT FLIP ROLLOVER | no |
| 26 | LEFT RETURN | no |
| 27 | RIGHT RETURN | no |
| 28 | LEFT ORBIT | no |

### Column 3 and 4

| Cell | Printed label | Shaded |
| --- | --- | --- |
| 31 | TROUGH EJECT | yes |
| 32 | TROUGH BALL 1 | yes |
| 33 | TROUGH BALL 2 | yes |
| 34 | TROUGH BALL 3 | yes |
| 35 | TROUGH BALL 4 | yes |
| 36 | LOCKUP 1 FRONT | yes |
| 37 | LOCKUP 2 REAR | yes |
| 38 | NOT USED | no |
| 41 | KICKBACK | yes |
| 42 | LEFT BIG KICK | yes |
| 43 | TOKEN CHUTE JAM | yes |
| 44 | LEFT JET | no |
| 45 | RIGHT JET | no |
| 46 | TOP JET | no |
| 47 | LEFT SLINGSHOT | no |
| 48 | RIGHT SLINGSHOT | no |

### Column 5 and 6

| Cell | Printed label | Shaded |
| --- | --- | --- |
| 51 | (A)LARM STANDUP | no |
| 52 | A(L)ARM STANDUP | no |
| 53 | AL(A)RM STANDUP | no |
| 54 | ALA(R)M STANDUP | no |
| 55 | ALAR(M) STANDUP | no |
| 56 | VARI TARGET C | yes |
| 57 | VARI TARGET B | yes |
| 58 | VARI TARGET A | yes |
| 61 | TOP LEFT 3-BANK TOP | yes |
| 62 | TOP LEFT 3-BANK MIDDLE | yes |
| 63 | TOP LEFT 3-BANK BOTTOM | yes |
| 64 | TOP RIGHT 3-BANK BOTTOM | yes |
| 65 | TOP RIGHT 3-BANK MIDDLE | yes |
| 66 | TOP RIGHT 3-BANK TOP | yes |
| 67 | TOP LEFT LANE | no |
| 68 | TOP POPPER | no |

### Column 7 and 8

| Cell | Printed label | Shaded |
| --- | --- | --- |
| 71 | BOTTOM LEFT 3-BANK TOP | yes |
| 72 | BOTTOM LEFT 3-BANK MIDDLE | yes |
| 73 | BOTTOM LEFT 3-BANK BOTTOM | yes |
| 74 | BOTTOM RIGHT 3-BANK BOTTOM | yes |
| 75 | BOTTOM RIGHT 3-BANK MIDDLE | yes |
| 76 | BOTTOM RIGHT 3-BANK TOP | yes |
| 77 | BANK KICKOUT | no |
| 78 | TOP RIGHT LANE | no |
| 81 | LEFT TOKEN LEVEL | no |
| 82 | RIGHT TOKEN LEVEL | no |
| 83 | RAMP ENTRANCE | no |
| 84 | RAMP MADE | no |
| 85 | WHEEL CHANNEL A | yes |
| 86 | WHEEL CHANNEL B | yes |
| 87 | NOT USED | no |
| 88 | NOT USED | no |

Total: 64 cells (8 columns x 8 rows). 27 matrix cells are shaded: 31-37, 41-43, 56-58, 61-66, 71-76, 85 and 86
(7 + 3 + 3 + 6 + 6 + 2), plus the four shaded flipper cells F2, F4, F6, F8. Cells printed `NOT USED`: 23, 38, 87, 88.

Notes on the cell text:
- The cell descriptions are printed in capitals, broken over two to four lines; the row/column address is the small
  number at the bottom right of each cell.
- The standup cells 51-55 spell `ALARM` with one letter in parentheses per cell: `(A)LARM`, `A(L)ARM`, `AL(A)RM`,
  `ALA(R)M`, `ALAR(M)`, then `STANDUP` on the next line.
- Cells 56, 57, 58 read `VARI TARGET` over `C`, `B`, `A` (descending with the address; the Section 3 reprint reads
  `A`, `B`, `C`).
- Cell 25 prints `UPPER RIGHT FLIP ROLLOVER` on four lines. Cells 11 and 12 print `(ROOF)` and `(VARI)` in
  parentheses.
- The shaded cells in the column-3 (trough/lockup), column-4 (kickback, big kick, token chute jam) and the
  3-bank cells print their text in bold over the stipple.

## Legend and footer

Below the table, left: `J2XX = CPU Board;`. Then a small rectangle with the same grey stipple as the shaded
cells followed by `= Opto, Typically Closed`. There is no further legend or footnote on the page between the
table and the `SWITCH LOCATIONS` heading.

## Comparison with the reprint

The Section 3 reprint (PDF page 126, printed page `3-2`, top half; the lower half is the `SWITCH MATRIX
CIRCUIT` drawing) was read cell by cell. Layout, row and column headers, wires, connector pins, IC pins, the D1-D8
block, the shading pattern and the legend (`J2XX = CPU Board;` and the stippled rectangle `= Opto, Typically
Closed`) agree with `2-42`, except for the items below. The reprint's own contents are listed in full here.

Differences in cell labels (reprint reading, then `2-42` reading):

| Cell | Reprint (3-2) | Primary (2-42) |
| --- | --- | --- |
| 36 | LOCKUP 1 | LOCKUP 1 FRONT |
| 37 | LOCKUP 2. (a small dot follows the 2) | LOCKUP 2 REAR |
| 42 | LEFT BIT KICK | LEFT BIG KICK |
| 43 | COIN CHUTE | TOKEN CHUTE JAM |
| 51 | STANDUP 1 | (A)LARM STANDUP |
| 52 | STANDUP 2 | A(L)ARM STANDUP |
| 53 | STANDUP 3 | AL(A)RM STANDUP |
| 54 | STANDUP 4 | ALA(R)M STANDUP |
| 55 | STANDUP 5 | ALAR(M) STANDUP |
| 56 | VARI TARGET A | VARI TARGET C |
| 57 | VARI TARGET B | VARI TARGET B |
| 58 | VARI TARGET C | VARI TARGET A |
| 61 | TOP LEFT 3-BANK (TOP) | TOP LEFT 3-BANK TOP |
| 62 | TOP LEFT 3-BANK (MIDDLE) | TOP LEFT 3-BANK MIDDLE |
| 63 | TOP LEFT 3-BANK (BOTTOM) | TOP LEFT 3-BANK BOTTOM |
| 64 | TOP RIGHT 3-BANK (BOTTOM) | TOP RIGHT 3-BANK BOTTOM |
| 65 | TOP RIGHT 3-BANK (MIDDLE) | TOP RIGHT 3-BANK MIDDLE |
| 66 | TOP RIGHT 3-BANK (TOP) | TOP RIGHT 3-BANK TOP |
| 67 | LEFT LANE | TOP LEFT LANE |
| 71 | BOTTOM LEFT 3-BANK (TOP) | BOTTOM LEFT 3-BANK TOP |
| 72 | BOTTOM LEFT 3-BANK (MIDDLE) | BOTTOM LEFT 3-BANK MIDDLE |
| 73 | BOTTOM LEFT 3-BANK (BOTTOM) | BOTTOM LEFT 3-BANK BOTTOM |
| 74 | BOTTOM RIGHT 3-BANK (BOTTOM) | BOTTOM RIGHT 3-BANK BOTTOM |
| 75 | BOTTOM RIGHT 3-BANK (MIDDLE) | BOTTOM RIGHT 3-BANK MIDDLE |
| 76 | BOTTOM RIGHT 3-BANK (TOP) | BOTTOM RIGHT 3-BANK TOP |
| 77 | SCOOP KICK | BANK KICKOUT |
| 78 | RIGHT LANE | TOP RIGHT LANE |
| 81 | TOKEN LEVEL 1 | LEFT TOKEN LEVEL |
| 82 | TOKEN LEVEL 2 | RIGHT TOKEN LEVEL |

Other differences:
- F5 and F7 cells: the reprint prints an extra line `(NOT USED)` (in parentheses, regular weight) under the label,
  at the bottom of the cell, on both F5 (`Upper Right Flipper EOS`) and F7 (`Upper Left Flipper EOS`). The `2-42`
  page prints nothing there.
- Row 5 and row 6 header text, wires, pins, IC pins: identical. Row 6 prints `J208-7 U19-9` in both.
- Shading: identical in both copies (same 27 shaded matrix cells and F2, F4, F6, F8 shaded; cell 37 is shaded in
  both; cells 51-55 unshaded in both; 56, 57, 58 shaded in both).
- Cells not listed above (11-18, 21-28, 31-35, 38, 41, 44-48, 68, 83-88 and the D1-D8 / F1-F4 / F6 / F8 blocks)
  carry the same text, wire, pin and id in both copies. D5 prints `Ser Credits` / `Esc` in both.
- Printed folio: `3-2` (reprint) against `2-42`.

The reprint's `SWITCH MATRIX CIRCUIT` drawing is not transcribed in full here; its printed content is limited to: truth tables `COLUMN: INACTIVE H L OFF / ACTIVE L H ON` (columns A, B) and `ROW: SWITCH
OPEN H H L OFF / SWITCH CLOSED L L H ON` (columns C, D, E), and the paragraph beneath beginning `The
microprocessor is constantly strobing the column side of the switch.`

## DEDICATED SWITCHES (PDF page 127, printed page 3-3)

Read from the rendered page (300 dpi scan), not from the OCR text. The page carries two drawings, the
`DEDICATED SWITCHES` wiring drawing and the `DEDICATED SWITCH CIRCUIT` drawing, with the legend and a paragraph.

### Wiring drawing

Two boxed regions drawn with dashed outlines. Left box, labelled `CPU` / `BOARD`, connector `J205`; right box,
labelled `COIN DOOR` / `INTERFACE` / `BOARD`, with connectors `J1` and `J5`. Each wire runs straight from the
`J205` pin through the `J1` pin to the `J5` pin and then to a switch drawn to the right of the box; all switches
return to a common vertical line on the right that ties to `J5` pin 3.

Wire labels, as printed along the wires (each followed by the IC pin in parentheses and the switch id):

| J205 pin | Wire label | IC pin | Id | J1 pin | J5 pin | Switch drawn at J5 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Orange-Brown | (U17-5) | D1 | 8 | 4 | yes |
| 2 | Orange-Red | (U17-7) | D2 | 7 | 5 | yes |
| 3 | Orange-Black | (U17-11) | D3 | 6 | 6 | yes |
| 4 | Orange-Yellow | (U17-9) | D4 | 5 | (blank, no J5 pin printed) | no |
| 6 | Orange-Green | (U16-9) | D5 | 4 | 7 | yes |
| 7 | Orange-Blue | (U16-11) | D6 | 3 | 8 | yes |
| 8 | Orange-Violet | (U16-7) | D7 | 2 | 9 | yes |
| 9 | Orange-Gray | (U16-5) | D8 | 1 | 11 | yes |
| 10 | Black | `Ground` (printed in place of an IC pin and id) | (none) | 10 | 3 | none; this line joins the common return of all switches |

Further drawing details:
- `J205` pins printed: 1, 2, 3, 4, 6, 7, 8, 9, 10 (no pin 5). Pin 10 is also tied to a ground symbol drawn at
  the lower left of the CPU box.
- `J1` pins printed top to bottom: 8, 7, 6, 5, 4, 3, 2, 1, 10.
- `J5` pins printed top to bottom: 4, 5, 6, (nothing on the D4 line), 7, 8, 9, 11, 3. The D4 line reaches `J5`
  without a pin number and without a switch symbol; the `J5` rectangle has no pin printed for it.
- The coin door interface connector is labelled `J5` here (the label sits above the second connector). Seven
  open-contact switch symbols are drawn (D1, D2, D3, D5, D6, D7, D8); none for D4.
- Board names: `CPU BOARD`, `COIN DOOR INTERFACE BOARD`.

### Legend under the drawing

`Coin Acceptor Switches` (underlined heading):
- `D1 - Left Coin Chute`
- `D2 - Center Coin Chute`
- `D3 - Right Coin Chute`
- `D4 - Fourth Coin Chute`

`Control Switches` (underlined heading):
- `D5 - Normal Function, Service Credits; Test Function, Escape`
- `D6 - Normal Function, Volume Down; Test Function, Down`
- `D7 - Normal Function, Volume Up; Test Function, Up`
- `D8 - Normal Function, Begin Test; Test Function, Enter`

### DEDICATED SWITCH CIRCUIT drawing

Printed labels: CPU box `CPU BOARD` containing `+5V`, `74LS240` (input `C`, inverting bubble), `10K`, `LM339`
(`+` and `-` inputs, output node `B`), `+12V`, two `1K` resistors, node `A`, `1N4148` diode, `470pf` capacitor to
ground, the label `Dedicated Input`, and `J205` with a pin marked `X` and pin `10`. Wire labels `Orange-XXX`
and `Black` run to the `COIN DOOR INTERFACE BOARD`, whose first connector shows `X` and pin `15` and whose second
connector shows `X` and pin `3`; at the right the label `Coin Acceptor` / `or` / `Control Switch` beside an open
switch whose far end returns to pin 3. Truth table (columns `SWITCH | A | B | C |`):
`OPEN H H L OFF` and `CLOSED L L H ON`.

Paragraph beneath, verbatim:

```
The dedicated switches operate similar in the matrix, except that instead of a column circuit there is a direct tie to
ground.  Therefore, the column side is constantly active (low).  When a switch closes, the row side (dedicated input)
of the circuit activates.  The "+" input to the LM339 drops below +5V, therefore the output is low.  Since the row
circuit (dedicated input) is tied directly to ground through the switch, the switch is considered closed by the
microprocessor.  When the switch opens, the "+" input to the LM339 is above +5V, it output is high and the row is
inactive
```

(The paragraph ends without a full stop, and reads `operate similar in the matrix` and `it output is high` as
printed.) Printed folio `3-3`.

## Reading uncertainties

- Cell 37 in the reprint: the label prints `LOCKUP` over `2.` with a small dot after the 2; it may be a speck of
  the scan rather than a period. Reported as a speck-or-period; no other reading is in doubt.
- Cells 42 (reprint `LEFT BIT KICK`) and 43 (reprint `COIN CHUTE`) were read on native-resolution crops; the
  readings `BIT` and `COIN CHUTE` are as printed and clear, and differ from the `2-42` copy.
- Wire names inside the shaded F2, F4, F6, F8 cells are printed over a heavy stipple; they were read on 2x
  enlargements and are consistent between `2-42` and `3-2`.
