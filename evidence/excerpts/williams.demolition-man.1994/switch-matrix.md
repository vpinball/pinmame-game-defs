# Demolition Man — Switch Matrix

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF page 100,
printed page `DEMOLITION MAN 2-44`, the `SWITCHES` matrix table with its dedicated and flipper
grounded-switch blocks. Read from the rendered page (308 dpi 1-bit scan), not from the OCR text. The page holds
only this table: three blocks side by side (`Dedicated Grounded Switches` on the left, the 8 x 8 matrix in the
middle, `Flipper Grounded Switches` on the right), a small wiring symbol above the matrix and the legend line
below it. Labels are printed wrapped over two or three lines inside their cell; they are written here on one
line, joined by single spaces, with no other change. No cell is printed blank: the matrix, the dedicated block and
the flipper block all carry a label in every cell.

Every matrix cell prints its two-digit switch number in its bottom-right corner: the tens digit is the column and
the units digit is the row (column 3, row 1 prints `31`; column 1, row 3 prints `13`). In the halftone cells the
number is partly lost in the shading, so those numbers were cross-checked against the cell position and the
neighbouring cells. The row-header cell prints the row number (`1` to `8`) at its lower left and the column-header cell
prints the column number (`1` to `8`) at its top.

The same table is reprinted on PDF page 106 (printed `DEMOLITION MAN 3-2`); that copy is not a second source. It
was compared cell by cell (see `Differences from the reprint`); the only textual difference is switch 75.
The dedicated-switch wiring drawing on PDF page 107 is transcribed in its own section at the end of this file.

## Wiring symbol above the matrix

A small symbol is printed above columns 6 to 8: a line labelled `Green` on the left, then a switch contact, then a diode, then a line
labelled `White` on the right. The diode arrowhead points towards the `White` side. It illustrates that the green wire is the
column drive and the white wire the row return.

## Legend

| Mark | Printed meaning |
| --- | --- |
| halftone-shaded square | `= Opto Switch` |
| `*` | `= Not Used` |

The `*` appears in the grounded-switch blocks only on the flipper block: `E.O.S.*` (F5) and `Opto*` (F6). No matrix cell and no dedicated-switch cell carries a `*`.

## Drive columns

Header row of the matrix. The corner cell prints `Column` (upper right) and `Row` (lower left) either side of a diagonal line.

| Column | Wire | Connector-pin | Drive IC |
| ---: | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

Column 8 prints `J207-9`; no column prints `J207-8`.

## Return rows

Left header cell of each matrix row; the row number is printed at the lower left of the cell.

| Row | Wire | Connector-pin | Receiver IC |
| ---: | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

The receiver-IC pins are not in monotonic order: row 3 prints `U18-5` and row 4 `U18-7`, while row 2 prints `U18-9` and row 1 `U18-11`;
rows 5 to 8 print `U19-11`, `U19-9`, `U19-5`, `U19-7`. Row 6 prints `J209-7` and row 7 `J209-8`; no row prints `J209-6`.

## Matrix cells

One line per cell in page reading order (row 1 left to right, then row 2, and so on).
`Shaded` is `yes` where the cell carries the halftone `Opto Switch` shading.

| Switch | Column | Row | Printed label | Shaded |
| ---: | ---: | ---: | --- | --- |
| 11 | 1 | 1 | Ball Launch | no |
| 21 | 2 | 1 | Slam Tilt | no |
| 31 | 3 | 1 | Trough 1 | yes |
| 41 | 4 | 1 | Left Slingshot | no |
| 51 | 5 | 1 | Left Ramp Enter | no |
| 61 | 6 | 1 | Side Ramp Enter | no |
| 71 | 7 | 1 | Chase Car 1 | yes |
| 81 | 8 | 1 | Claw "Capture Simon" | no |
| 12 | 1 | 2 | Left Handle Button | no |
| 22 | 2 | 2 | Coin Door Closed | no |
| 32 | 3 | 2 | Trough 2 | yes |
| 42 | 4 | 2 | Right Slingshot | no |
| 52 | 5 | 2 | Left Ramp Exit | no |
| 62 | 6 | 2 | Side Ramp Exit | no |
| 72 | 7 | 2 | Chase Car 2 | yes |
| 82 | 8 | 2 | Claw "Sup. Jets" | no |
| 13 | 1 | 3 | Start Button | no |
| 23 | 2 | 3 | Buy-in Button | no |
| 33 | 3 | 3 | Trough 3 | yes |
| 43 | 4 | 3 | Left Jet Bumper | no |
| 53 | 5 | 3 | Center Ramp | no |
| 63 | 6 | 3 | Left Rollover | no |
| 73 | 7 | 3 | Top Popper | yes |
| 83 | 8 | 3 | Claw "Prison Break" | no |
| 14 | 1 | 4 | Plumb Bob Tilt | no |
| 24 | 2 | 4 | Always Closed | no |
| 34 | 3 | 4 | Trough 4 | yes |
| 44 | 4 | 4 | Top Slingshot | no |
| 54 | 5 | 4 | Upper Rebound | no |
| 64 | 6 | 4 | Center Rollover | no |
| 74 | 7 | 4 | Elevator Hold | yes |
| 84 | 8 | 4 | Claw "Freeze" | no |
| 15 | 1 | 5 | Left Outlane | no |
| 25 | 2 | 5 | Claw Position 1 | yes |
| 35 | 3 | 5 | Trough 5 | yes |
| 45 | 4 | 5 | Right Jet Bumper | no |
| 55 | 5 | 5 | Left Loop | no |
| 65 | 6 | 5 | Right Rollover | no |
| 75 | 7 | 5 | Elevator Ramp | no |
| 85 | 8 | 5 | Claw "ACMAG" | no |
| 16 | 1 | 6 | Left Inlane | no |
| 26 | 2 | 6 | Claw Position 2 | yes |
| 36 | 3 | 6 | Trough Jam | yes |
| 46 | 4 | 6 | Right Ramp Enter | no |
| 56 | 5 | 6 | Standup 2 | no |
| 66 | 6 | 6 | Eject | no |
| 76 | 7 | 6 | Bottom Popper | yes |
| 86 | 8 | 6 | Upper Left Flipper Gate | no |
| 17 | 1 | 7 | Right Inlane | no |
| 27 | 2 | 7 | Shooter Lane | no |
| 37 | 3 | 7 | Not Used | no |
| 47 | 4 | 7 | Right Ramp Exit | no |
| 57 | 5 | 7 | Standup 3 | no |
| 67 | 6 | 7 | Elevator Index | yes |
| 77 | 7 | 7 | Eyeball Standup | no |
| 87 | 8 | 7 | Car Chase Standup | no |
| 18 | 1 | 8 | Right Outlane | no |
| 28 | 2 | 8 | Not Used | no |
| 38 | 3 | 8 | Standup 5 | no |
| 48 | 4 | 8 | Right Freeway | no |
| 58 | 5 | 8 | Standup 4 | no |
| 68 | 6 | 8 | Not Used | no |
| 78 | 7 | 8 | Standup 1 | no |
| 88 | 8 | 8 | Lower Rebound | no |

The same 64 cells in printed layout, rows top to bottom and columns left to right (a `[opto]` suffix marks a halftone-shaded cell):

| Row | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Ball Launch | 21 Slam Tilt | 31 Trough 1 [opto] | 41 Left Slingshot | 51 Left Ramp Enter | 61 Side Ramp Enter | 71 Chase Car 1 [opto] | 81 Claw "Capture Simon" |
| 2 | 12 Left Handle Button | 22 Coin Door Closed | 32 Trough 2 [opto] | 42 Right Slingshot | 52 Left Ramp Exit | 62 Side Ramp Exit | 72 Chase Car 2 [opto] | 82 Claw "Sup. Jets" |
| 3 | 13 Start Button | 23 Buy-in Button | 33 Trough 3 [opto] | 43 Left Jet Bumper | 53 Center Ramp | 63 Left Rollover | 73 Top Popper [opto] | 83 Claw "Prison Break" |
| 4 | 14 Plumb Bob Tilt | 24 Always Closed | 34 Trough 4 [opto] | 44 Top Slingshot | 54 Upper Rebound | 64 Center Rollover | 74 Elevator Hold [opto] | 84 Claw "Freeze" |
| 5 | 15 Left Outlane | 25 Claw Position 1 [opto] | 35 Trough 5 [opto] | 45 Right Jet Bumper | 55 Left Loop | 65 Right Rollover | 75 Elevator Ramp | 85 Claw "ACMAG" |
| 6 | 16 Left Inlane | 26 Claw Position 2 [opto] | 36 Trough Jam [opto] | 46 Right Ramp Enter | 56 Standup 2 | 66 Eject | 76 Bottom Popper [opto] | 86 Upper Left Flipper Gate |
| 7 | 17 Right Inlane | 27 Shooter Lane | 37 Not Used | 47 Right Ramp Exit | 57 Standup 3 | 67 Elevator Index [opto] | 77 Eyeball Standup | 87 Car Chase Standup |
| 8 | 18 Right Outlane | 28 Not Used | 38 Standup 5 | 48 Right Freeway | 58 Standup 4 | 68 Not Used | 78 Standup 1 | 88 Lower Rebound |

### Shading sweep

All 64 matrix cells, the 8 dedicated cells and the 8 flipper cells were checked for halftone shading, by eye and by a
pixel measurement (fraction of black/white pixel transitions per cell in the 1-bit render: 0.31 to 0.38 in the shaded matrix cells,
0.03 to 0.09 in the unshaded matrix cells, 0.09 to 0.16 in the dedicated and flipper cells, which are all unshaded).
The halftone-shaded matrix cells on this page are these fourteen:

- column 3, rows 1 to 6: 31 Trough 1, 32 Trough 2, 33 Trough 3, 34 Trough 4, 35 Trough 5, 36 Trough Jam
- column 7, rows 1 to 4: 71 Chase Car 1, 72 Chase Car 2, 73 Top Popper, 74 Elevator Hold
- column 2, rows 5 and 6: 25 Claw Position 1, 26 Claw Position 2
- column 7, row 6: 76 Bottom Popper
- column 6, row 7: 67 Elevator Index

The other 50 matrix cells, the eight dedicated cells and the eight flipper cells are unshaded. In particular cell 75 (`Elevator Ramp` on this page) is unshaded.
The `Not Used` cells on this page are 37 (column 3, row 7), 28 (column 2, row 8) and 68 (column 6, row 8); all three are unshaded and none carries a `*`.

## Dedicated Grounded Switches

Left block, heading cell `Dedicated Grounded Switches` and eight stacked cells. Each cell prints the wire colour, the connector-pin, the label and the `Dn` designator at its lower right.
D1 to D4 print a plain two-line label. D5 to D8 print a two-column label: the left half is headed `Normal Function`, the right half, after a vertical bar,
`Test Function`; the table gives the text printed under each heading.

| Switch | Wire | Connector-pin | Label | Normal Function | Test Function |
| --- | --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute | | |
| D2 | Orange-Red | J205-2 | Center Coin Chute | | |
| D3 | Orange-Black | J205-3 | Right Coin Chute | | |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute | | |
| D5 | Orange-Green | J205-6 | | Service Credits | Escape |
| D6 | Orange-Blue | J205-7 | | Volume Down | Down |
| D7 | Orange-Violet | J205-8 | | Volume Up | Up |
| D8 | Orange-Gray | J205-9 | | Begin Test | Enter |

No `J205-5` is printed: D4 prints `J205-4` and D5 prints `J205-6`.

## Flipper Grounded Switches

Right block, heading cell `Flipper Grounded Switches` and eight stacked cells. Each cell prints the wire colour, the connector-pin, the label and the `Fn` designator at its lower right.

| Switch | Wire | Connector-pin | Printed label |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right E.O.S. |
| F2 | Blue-Violet | J905-1 | Lower Right Opto |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S. |
| F4 | Blue-Gray | J905-2 | Lower Left Opto |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S.* |
| F6 | Black-Yellow | J905-3 | Upper Right Opto* |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. |
| F8 | Black-Blue | J905-5 | Upper Left Opto |

F3 and F8 both print the wire colour `Black-Blue` (F3 on `J906-3`, F8 on `J905-5`). F1, F3, F5 and F7 use connector `J906`; F2, F4, F6 and F8 use `J905`.
F5 `E.O.S.*` and F6 `Opto*` carry the legend's `*` (`Not Used`); F1 to F4, F7 and F8 carry none.

## Differences from the reprint

Compared cell by cell with the reprint on PDF page 106 (printed `DEMOLITION MAN 3-2`): column headers (number, wire, connector-pin, IC), row headers,
all 64 cell labels and numbers, the shaded cells (the same fourteen, measured the same way on that page), the eight dedicated cells including the
D5 to D8 function text, and the eight flipper cells including the `*` marks on F5 and F6.

| Item | PDF page 100 (printed 2-44) | PDF page 106 (printed 3-2) |
| --- | --- | --- |
| Cell 75 (column 7, row 5) | `Elevator Ramp` (unshaded) | `Not Used` (unshaded) |

There is no other textual difference. The page-106 scan has two non-text differences: a small tick-like mark to the left of the `15` in the `Left Outlane` cell and a few
short dark flecks inside the halftone of cells 25 and 35; they look like scan or hand marks, not printed characters, and they change no label or shading.
Page 106 also carries a `Switch Matrix Circuit` drawing and two paragraphs of text below the table (next section); page 100 does not.

## Switch Matrix Circuit (PDF page 106 only)

Printed below the reprint, headed `Switch Matrix Circuit`; it is not on page 100. A dashed `CPU BOARD` box holds a column example and a row example, joined through a playfield switch.

- Column (example): `LS 374SC` feeds the `ULN-2803` (inverting symbol; point `B` is labelled beside its input side), whose output node `A` has a `1KΩ` pull-up to `+12V` and a `470 pf` capacitor to ground, then connector `J207` and a wire labelled `Green-XXX`.
- Playfield: a switch in series with a diode, from the `Green-XXX` wire to the `White-XXX` wire.
- Row (example): `White-XXX` wire into connector `J209`, then diode `1N4148` to node `C` (`1.2KΩ` pull-up to `+12V`, `470 pf` to ground), a `1KΩ` series resistor to the `+` input of an `LM339` comparator (its `-` input to `+5V`; a `10KΩ` resistor from its output to `+5V`), output node `D` into a `74LS240` inverting buffer whose output is point `E`.

| Column | A | B | |
| --- | --- | --- | --- |
| Inactive | H | L | Off |
| Active | L | H | On |

| Row | C | D | E | |
| --- | --- | --- | --- | --- |
| Switch Open | H | H | L | Off |
| Switch Closed | L | L | H | On |

Text printed under the circuit: `The microprocessor is constantly strobing the column side of the switch. When point "A" on the column circuit toggles low the column side is active.` and `When a switch closes the row side of the circuit activates. The "+" input to the LM339 drops below +5V therefore its output is low. Corresponding row and column switches must be  low at the same time, for the switch to be considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is inactive.` (the double space before `low` is as printed).

## Dedicated Switches wiring (PDF page 107)

From `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF page 107, printed page `DEMOLITION MAN 3-3`, the drawing headed `Dedicated Switches`. It is a wiring
diagram of the dedicated (grounded) switches from the CPU board connector `J205`, through the `COIN DOOR INTERFACE BOARD` connectors `J1` and `J3`, to the
`Coin Acceptor or Control Switches`. It is a drawing, read from the image at 308 dpi; it is not part of the page-100 table.

Wire runs, left to right:

| Switch | J205 pin | Wire | Printed chip pin | J1 pin | J3 pin | Switch symbol drawn right of J3 |
| --- | ---: | --- | --- | ---: | --- | --- |
| D1 | 1 | Orange-Brown | (U17-5) | 14 | 4 | yes |
| D2 | 2 | Orange-Red | (U17-7) | 13 | 5 | no |
| D3 | 3 | Orange-Black | (U17-11) | 12 | 6 | yes |
| D4 | 4 | Orange-Yellow | (U17-9) | 17 | none drawn | no |
| D5 | 6 | Orange-Green | (U16-9) | 11 | 7 | yes |
| D6 | 7 | Orange-Blue | (U16-11) | 10 | 8 | yes |
| D7 | 8 | Orange-Violet | (U16-7) | 9 | 9 | yes |
| D8 | 9 | Orange-Gray | (16-5) | 8 | 11 | yes |
| (return) | 11 | Black | | 15 | 3 | common return bus, see below |

Details of the drawing:

- `J205` pins drawn: 1, 2, 3, 4, 6, 7, 8, 9 and 11 (pin 5 is not drawn). Pin 11 carries the `Black` wire and is drawn tied to a ground symbol on the CPU board.
- The chip pin of D8 is printed `(16-5)`, without the `U` the other seven carry.
- The wire colour, the chip pin in brackets and the `Dn` designator are printed above each run, between `J205` and the coin door interface board.
- `J1` pins drawn top to bottom: 14, 13, 12, 17, 11, 10, 9, 8, 15. `J3` pins drawn top to bottom: 4, 5, 6, (no pin level with `J1`-17), 7, 8, 9, 11, 3.
- A switch contact symbol is drawn to the right of `J3` pins 4, 6, 7, 8, 9 and 11. The run `J1`-13 to `J3`-5 (D2) ends at `J3`-5 with no switch symbol drawn after it, and the run for D4 (`J1`-17) is not drawn on to any `J3` pin at all.
- The far ends of the drawn switches join a vertical bus on the right, which runs back along the bottom to `J3` pin 3, then `J1` pin 15 and the `Black` wire (`J205` pin 11).
- Heading above the switch symbols: `Coin Acceptor or Control Switches`.

Legend printed to the right of the switches:

| Switch | Printed text |
| --- | --- |
| | `Coin Acceptor Switches` |
| D1 | Left Coin Chute |
| D2 | Center Coin Chute |
| D3 | Right Coin Chute |
| D4 | Forth Coin Chute |
| | `Control Switches` |
| D5 | Normal Function: Service Credits; Test Function: Escape |
| D6 | Normal Function: Volume Down; Test Function: Down |
| D7 | Normal Function: Volume Up; Test Function: Up |
| D8 | Normal Function: Begin Test; Test Function: Enter |

`Forth Coin Chute` is the printed spelling; page 100 prints `4th Coin Chute` for D4.

### Dedicated Switch Circuit (PDF page 107)

Below the wiring diagram, headed `Dedicated Switch Circuit`: on the `CPU BOARD`, connector `J205` pin `X` with an `Orange-XXX` wire and pin `11` with a `Black` wire to ground;
on the `COIN DOOR INTERFACE BOARD`, `J1` pin `x` and `J3` pin `x` for the signal and `J1` pin `15` and `J3` pin `3` for the black return, with the `Coin Acceptor or Control Switch` drawn between the two.
On the CPU board the `Orange-XXX` wire goes through a `1N4148` diode to node `A` (`1.2KΩ` pull-up to `+12V`, `470 pf` to ground); a `1KΩ` resistor takes it to the `+` input of an `LM339` (`-` input to `+5V`, `10KΩ` from the output to `+5V`) whose output is node `B`, into an inverting buffer whose output is point `C`.

| Switch | A | B | C | |
| --- | --- | --- | --- | --- |
| Open | H | H | L | Off |
| Closed | L | L | H | On |

Text printed under it: `The dedicated  switches operate similar to switches in the matrix except that instead of a column circuit there is a direct tie to ground. Therefore, the column side is constantly active (low).` and `When a switch closes the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V therefore its output is low. Since the row circuit (dedicated input) is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is inactive.` (the double space in `dedicated  switches` is as printed).
