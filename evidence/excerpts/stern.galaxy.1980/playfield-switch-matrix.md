Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF page 23, drawing number `12B-432-S-114` (printed at the foot of the page), title block `STERN ELECTRONICS INC. 1725 DIVERSEY BLVD. CHICAGO 60614`, `PLAYFIELD` / `WIRING DIAGRAM` / `FOR GALAXY`, `DRN. CW.`, `DATE 10-11-79` (the title block is cut by the seam between PDF pages 22 and 23). The page is upright. It was read from crops at 400 to 700 dpi, no rotation. This is the left half of the playfield wiring diagram; the switch matrix is at the left of the page.

The switch matrix: five strobe columns and eight return rows. Every cell is a contact drawn as an open switch with a series diode; no capacitor is drawn on any contact. Note printed on the sheet: `ALL DIODES ARE IN - 4004`.

Column headings, verbatim (hand lettered): `STO` over `A` (a zero written like an O), `ST1` over `B`, `ST2` over `C`, `ST 3` over `D`, `ST 4` over `E`. The strobe wires run along the foot of the matrix, in order: `A4J2-1 (W-R)`, `A4J2-2 (BRN-W)`, `A4J2-3 (W-BLU)`, `A4J2-4 (W-Y)`, `A4J2-5 (Y-R)`. They are listed in the order printed from the nearest column to the farthest; each wire joins the vertical bus of one column, `A4J2-1` the leftmost (ST0/A) through `A4J2-5` the rightmost (ST4/E). The drawing does not print a strobe number against these wires.

Return rows: the horizontal wires entering from the left, top to bottom. The left margin prints the labels `I1` to `I7` beside the second to eighth rows; the topmost row prints no `I` label. Wires, verbatim: `A4J2-8 (BRN)` (topmost row, printed with the letter `A` after it, `A4J2-8(BRN) A`), `A4J2-9 (GREY)` (labelled `I1`), `A4J2-10 (W-O)` (`I2`), `A4J2-11 (W-B)` (`I3`), `A4J2-12 (W-G)` (`I4`), `A4J2-13 (W-BRN)` (`I5`), `A4J2-14 (BRN-Y)` (`I6`), `A4J2-15 (O)` (`I7`). The `O` of the last is written `(0)` in the drawing.

Cell labels are hand lettered, some inside the box above a contact and some below it; the table gives each cell the text belonging to its contact. Where a cell carries two separately placed pieces of text they are given as printed, upper piece first. `(blank)` is not used: every contact has a label.

| Return row (wire) | ST0 A | ST1 B | ST2 C | ST3 D | ST4 E |
| --- | --- | --- | --- | --- | --- |
| top row (A4J2-8) | CHUTE #1 | D.T. / BLACK | N/U | N/U | OUT-HOLE |
| I1 (A4J2-9) | CHUTE #2 | D.T. / YEL. | CENTER R.O.B(2) | S.U.T. / BLUE | N/U |
| I2 (A4J2-10) | CHUTE #3 | D.T. / BLU | R. RETURN LANE | N/U | BALL KICK. |
| I3 (A4J2-11) | D.T. / (RED) | TOP THUMP. | R. MID. LANE | N/U | TOP-L. R.O.W. |
| I4 (A4J2-12) | SP. T. | LOW. R. THUMP. | L. RETURN LANE | S.U.T. / YELLOW | TOP MID. R.O.W. |
| I5 (A4J2-13) | CREDIT | LOW. L. THUMP. | L. MID. LANE | S.U.T. / BLACK | TOP R. R.O.W. (see below) |
| I6 (A4J2-14) | TILTS | R. SLING SHOT | R. OUT-LANE / R.O.B. | N/U | TOP-R. R.O.W. |
| I7 (A4J2-15) | SLAM | L. SLING SHOT | R.O.B. / L. OUT-LANE | N/U | SAUCER |

Notes on individual cells:

- `CHUTE #2` and `CHUTE #3` carry a small extra `#` mark above the printed `#` (an overwrite); the number `2` or `3` follows it. `CHUTE #1` is printed `CHUTE #1`.
- ST1 top three rows: the `D.T.` is printed in the box above the contact and the colour (`BLACK`, `YEL.`, `BLU`) beside it; row I3's ST0 cell is `D.T.` above the contact with `(RED)` circled to the left of the box.
- ST3 `S.U.T.` rows: the colour (`BLUE`, `YELLOW`, `BLACK`) is printed below the contact.
- ST2 rows I6 and I7: each contact has two pieces of text. For I6, `R. OUT-LANE` is printed in the box above the contact and `R.O.B.` below it; for I7, `R.O.B.` is printed in the box above the contact and `L. OUT-LANE` below it. This is how the text sits relative to the contacts; the drawing does not state which piece pairs with which.
- ST4 row I5: the first line reads `TOP R.` with the `P` overwritten (it looks like `TOAR.`); second line `R.O.W.`. The row I6 cell reads `TOP-R.` / `R.O.W.` with a hyphen. These two are legible only as printed above.

Below the matrix: a box fed by `A2J1-8 (W)` with `6 VAC`, drawn with a lamp symbol labelled `GEN. ILLUM`, returning on `A2J1-1 (R)` marked `RETURN`. No switch, relay or driver transistor is drawn in that circuit. The return rows' common line runs out of the matrix at the lower left with an arrowhead.

Notes, verbatim (typed, under `NOTES:`):

- `N/U = NOT USED`
- `ALL DIODES ARE IN - 4004`
- `D.T. = DROP TARGET`
- `S.U. = STAND-UP TARGET`
- `R.O.B. = ROLL-OVER BUTTON`
- `SP.T. = SPINNING TARGET`
- `R.O.W. = ROLL-OVER WIRE FORM`
