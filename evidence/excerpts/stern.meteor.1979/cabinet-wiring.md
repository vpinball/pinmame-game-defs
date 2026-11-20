Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 32-33: cabinet and front door wiring. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) - Cabinet and front door wiring (PDF page 32, PDF page 33)

Pages: PDF page 32 (left: cabinet switch matrix, test switch, flipper buttons, knocker/lockout) and PDF page 33 (right: knocker coil, power on/off, line filter, front door jack table). Title block (PDF page 33): "STERN ELECTRONICS INC. 1725 DIVERSEY BLVD. CHICAGO 60614 - CABINET AND FRONT DOOR WIRING - FOR STANDARD - DRN. J.J. DATE 2-6-79".

Notes printed (PDF page 32 bottom): "N/U = NOT USED", "ALL DIODES ARE 1N-4004". The part number's first character is the sheet's digit 1 (a flag and a base, as in its `I1` row label), not its letter I, which carries a full top bar.

## Test switch (top of matrix)
| Item | Printed |
| --- | --- |
| Left terminal | A4J3-1 (R) |
| Switch | "TEST SWITCH" (push-button symbol), open |
| Right terminal | wire down and left to A3J2-7 (Y-R) |

## Matrix rows (return lines) and strobe columns of the cabinet grid (5 x 8, labelled "ST0 A" ... "ST4 E" and I0..I7)

| Row | Printed connector/colour |
| --- | --- |
| I0 | A4J3-9 (R-W) |
| I1 | A4J3-10 (BRN-W) |
| I2 | A4J3-11 (BLU) |
| I3 | (blank) |
| I4 | (blank) |
| I5 | A4J3-14 (BLU-W) |
| I6 | A4J3-15 (BLU-O) |
| I7 | A4J3-16 (Y) |

| Strobe | Printed connector/colour |
| --- | --- |
| ST0 (A) | A4J3-2 (R-Y) |
| ST1 (B) | A4J3-3 (R-G) |
| ST2 (C) | (blank - bottom line not labelled) |
| ST3 (D) | (blank) |
| ST4 (E) | (blank) |

## Cabinet matrix cells (label verbatim; D = diode drawn; all unlabelled cells show a bare switch symbol)

| Row | ST0 | ST1 | ST2 | ST3 | ST4 |
| --- | --- | --- | --- | --- | --- |
| I0 | CHUTE #3, D | (blank), no D | (blank), D | (blank), D | (blank), no D |
| I1 | CHUTE #2, no D | (blank), no D | (blank), no D | (blank), no D | (blank), no D |
| I2 | CHUTE #1, no D | (blank), no D | (blank), no D | (blank), D | (blank), no D |
| I3 | (blank), D | (blank), D | (blank), D | (blank), D | two parallel switches (blank), D (one diode after them) |
| I4 | (blank), D | (blank), D | (blank), D | (blank), D | two parallel switches (blank), D |
| I5 | CREDIT, D | (blank), no D | (blank), D (slashed, see uncertain) | (blank), D | (blank), D |
| I6 | TILT, D, plus a second unlabelled switch in parallel with TILT with a capacitor beside it | (blank), D | (blank), D | (blank), D | (blank), no D |
| I7 | SLAM, D | (blank), D | (blank), D | (blank), D | (blank), no D |

Cell-level details:
- I6 ST0: left of the TILT cell there is a second switch (unlabelled) wired from the row-I6 line to the TILT cell's post-contact node, in parallel with TILT; a capacitor symbol (a curved upper plate facing a straight lower plate) is drawn on the far left: its upper lead runs from a dot on the vertical lead that drops from the row node, and its lower lead to the dot at the second switch's left terminal, where that vertical lead also ends. The `A4J3-16 (Y)` label printed just below belongs to the next row (I7, SLAM), not to this node. Capacitor: yes; diode on this second switch: no (only the TILT cell diode after the common node).
- I3 ST4 and I4 ST4: two switch symbols stacked; upper switch's left end taps the row line with a dot, its right terminal is wired down to the lower switch's right terminal; lower switch's left end taps the row line; one diode follows. So two switches in parallel feeding one diode, unlabelled.
- Capacitors in the cabinet matrix: only the one beside TILT (I6 ST0).
- The cabinet drawing prints no label on ST1..ST4 cells (all unlabelled bare switches); only the ST0 cells and the TILT/CREDIT/SLAM positions are labelled.

## Flipper buttons and lamp (bottom of PDF page 32)
| Item | Printed |
| --- | --- |
| LEFT FLIPPER switch | A3J2-2 (BLU) - switch - joins common bus |
| RIGHT FLIPPER switch | A3J2-1 (R) - switch - joins the same common bus |
| Common return | A2J2-9 (O) |
| Lamp (circle, unlabelled) | A2J2-1 (Y-B) and A2J2-5 (G-R) |

(The printed text beside the left flipper reads "A3J2-2 (BLU" with the closing parenthesis cut, and "LEFT FLIPPER"; the right reads "RIGHT FLIPPER".)

## Coil circuits (right of matrix on PDF page 32, continuing on PDF page 33)
| Item | Printed |
| --- | --- |
| Bus | A2J2-2 (G) ">>" to the right onto PDF page 33; branch drops to the COIN LOCKOUT coil |
| COIN LOCKOUT | coil with diode across; low end A3J2-8 (Y-W) |
| KNOCKER | coil with diode across (PDF page 33 left); drive line A3J2-5 (B-Y) ">>" from PDF page 32; top line is the A2J2-2 (G) bus |

(">>" marks connect the two pages.)

## AC power and line filter (PDF page 33)
| Item | Printed |
| --- | --- |
| Line 1 | (B) to terminal "1" ">1>" "L1" of LINE FILTER |
| Line 2 | (W) to terminal "2" ">2>" "L2" |
| Service outlet | symbol between the (B) and (W) lines labelled "SERVICE OUTLET" with "GRD" connection |
| Terminal 3 | ">3>" goes to GRD at the filter ("GRD." ) |
| Line filter outputs | "120 VAC", "GRD", "120 VAC RETURN"; "GRD. BRAID" from the filter bottom |
| VR1 | "GE # V130LA10A VARISTOR" across 120 VAC and 120 VAC RETURN |
| POWER ON/OFF | double-pole switch (label with arrow) breaking the (B) and (W) lines |
| Vertical lines to bottom | A2J2-6 (Y), A2J2-7 (BLU-W), A2J2-10 (G) |

## Front door jack table (verbatim, handwritten)
Header: "FRONT DOOR JACK"; columns "JACK PIN No." and "FROM". Dashed leader lines are printed between the pin number and the FROM entry on rows 3, 6, 10, 16, 19.

| Jack pin | From |
| --- | --- |
| 1 | A4J3-9 |
| 2 | A4J3-10 |
| 3 | A4J3-11 |
| 4 | A4J3-12 |
| 5 | A4J3-13 |
| 6 | A4J3-14 |
| 7 | A4J3-15 |
| 8 | A4J3-16 |
| 9 | (blank, no row) |
| 10 | A4J3-2 |
| 11-14 | (no rows) |
| 15 | A2J2-2 |
| 16 | A3J2-8 |
| 17 | A2J2-1 |
| 18 | A2J2-5 |
| 19 | A4J3-1 |
| 20 | A3J2-7 |

## Uncertain readings
- cabinet I5 ST2 diode has a slash through it (looks like a drawn slash/overprint); read as a diode present.
- I0 ST1 and I1 ST1 etc. - diode absence read from the drawing; some right-hand dot junctions (I1 ST2) have a small stray stroke.
- "A3J2-2 (BLU" closing parenthesis missing; "A2J2-1 (Y-B)" the B looks like an overwritten B.
- whether terminal "3" ties to the line filter GRD or to the service outlet GRD (both lines meet at the GRD dot).
