Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF page 36, left part: the PLAYFIELD switch matrix and the GEN. ILLUM string. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) - Playfield switch matrix (PDF page 36, left half)

Page: PDF page 36 (left part; the right part is the coil drawing, see the playfield coil wiring excerpt). "PLAYFIELD" is printed (handwritten italic) under the drawing; the title block is on PDF page 37.

Printed bottom-left notes (verbatim): "N/U = NOT USED", "ALL DIODES ARE 1N-4004.", "ROB = ROLL-OVER BUTTON.", "DT = DROP TARGET", "SU = STAND-UP TARGET". The part number's first character is the sheet's digit 1 (a flag and a base, as in its `I1` row label), not its letter I, which carries a full top bar.

## Strobe columns (vertical lines, strobe labels printed at top "ST0 A" ... "ST4 E")

| Strobe | Letter | Connector-pin and colour (printed at bottom of the matrix) |
| --- | --- | --- |
| ST0 | A | A4J2-1 (W-R) |
| ST1 | B | A4J2-2 (BRN-W) |
| ST2 | C | A4J2-3 (W-BLU) |
| ST3 | D | A4J2-4 (W-Y) |
| ST4 | E | A4J2-5 (Y-R) |

Column-to-pin mapping was read from the curved connections of the vertical lines to the five bottom lines: leftmost vertical = A4J2-1, next = -2, ... rightmost = -5. The printed "ST0..ST4" and letters are over the column heads.

## Return rows (horizontal lines, labelled I0..I7 at left)

| Row | Connector-pin and colour (printed) |
| --- | --- |
| I0 | A4J2-8 (BRN) |
| I1 | A4J2-9 (GREY) |
| I2 | A4J2-10 (W-O) |
| I3 | A4J2-11 (W-B) |
| I4 | A4J2-12 (W-G) |
| I5 | A4J2-13 (W-BRN) |
| I6 | A4J2-14 (BRN-Y) |
| I7 | A4J2-15 (O) |

## Cells (label verbatim; "/" separates lines of a two-line label; D = diode drawn in the cell; C = capacitor drawn in the cell)

All diodes are drawn between the switch's contact and the strobe column, the arrow pointing left towards the contact with the cathode bar on the contact side, so the cathode faces the contact (and through it the return row) and the anode the strobe column. A capacitor is drawn as a curved plate facing a straight plate, distinct from the diode's arrow and bar, on a branch below the switch, wired from the row-side node to the post-contact node.

| Row | ST0 (A) | ST1 (B) | ST2 (C) | ST3 (D) | ST4 (E) |
| --- | --- | --- | --- | --- | --- |
| I0 | (blank), no D | RT. 3-BANK / TOP TARG., no D, no C | N/U, D | N/U, no D | OUT-HOLE, D |
| I1 | (blank), no D | RT. 3-BANK / LOWER TARG., D, C | N/U, D | N/U, D | R.OUT-LANE, D |
| I2 | (blank), no D | RT. 3-BANK / MID. TARG., D, C | TOP LEFT 3-BANK / TOP TARG., D, no C | 6-BANK / "R" TARG., D | LEFT OUT-LANE, D |
| I3 | S.U. TARG., D | BUMPER / UP. R.T., D, C | TOP LEFT 3-BANK / LOW. TARG, D, C | 6-BANK / "O" TARG., D | R.RETURN LANE, D |
| I4 | SPIN. TARG., D | BUMPER / UP. LFT., D, no C | TOP LEFT 3-BANK / MID. TARG, D, C | 6-BANK / "E" TARG., D | L.RETURN LANE, D |
| I5 | CREDIT, no D | THUMPER, D | LOWER LFT. 3-BANK / TOP TARG., D, C | 6-BANK / "T" TARG., D | UPPER R.O.B., D |
| I6 | TILTS, D | RIGHT SLING-ST., D | LOWER LFT. 3-BANK / LOW TARG, D, C | 6-BANK / "E" TARG., D | MIDDLE R.O.B., D |
| I7 | SLAM, D | L.SLING-S., D | LOWER LFT. 3-BANK / MID. TARG, D, C | 6-BANK / "M" TARG., D | LOWER R.O.B., D |

Capacitor cells (8): ST1 I1, ST1 I2, ST1 I3, ST2 I3, ST2 I4, ST2 I5, ST2 I6, ST2 I7. Cells that look similar but have no capacitor drawn: ST1 I0 and ST2 I2 (the first/"TOP TARG." target of each 3-bank) and ST1 I4 (BUMPER UP. LFT.).

Printed sub-labels as written (the second line of a cell label sits outside/below the switch): "TOP TARG.", "LOWER TARG." (the printed text reads "LOWER ... TARG." split around the capacitor), "MID. TARG.", "UP. R.T." (printed `UP. R.T.` with a stray mark after R), "UP. LFT.", "LOW. TARG", "MID. TARG", "TOP TARG.", "LOW TARG", "MID. TARG".

## General illumination string (bottom of PDF page 36)
- A2J1-8 (W), "6 VAC" at the top; return A2J1-1 (R), "RETURN"; a lamp symbol (circle) between them labelled "GEN. ILLUM". The return line runs off the bottom of the page to the matrix return bus (arrow to the left).

## Uncertain readings
- ST0 I0-I2 cells have a switch but no label, no diode; I0's right terminal wires straight to the column without a junction dot, I1 and I2 with a dot. Best reading: unlabelled switch cells, no diode.
- ST3 I1 N/U diode is drawn smaller/lighter than the others (best reading: diode present). ST3 I0 N/U: no diode drawn (best reading).
- ST4 R.OUT-LANE switch is drawn lower than neighbours; reading unchanged.
- the capacitor symbol in ST1 I3 (UP. R.T.) is drawn like the others; ST1 I4 (UP. LFT.) has none (label "UP. LFT." in its place).
- Diode polarity is not graded; presence only.
