Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF pages 24 and 25, drawing number `12B-434-S-114` (printed at the foot of page 24 and in a box at the top right of page 25), title block `STERN ELECTRONICS INC.`, `1725 DIVERSEY BLVD. CHICAGO 60614`, `CABINET AND FRONT DOOR WIRING`, `FOR STANDARD`, `DRN. C.W.`, `DATE 10-16-79` (the `AM'T`, `MAT` and `FIN.` cells carry initials; `APPR.` is blank). The sheet's footer also prints `DIETZGEN NO. 198M AGEPROOF`. The two pages are the left (page 24) and right (page 25) halves of one sheet; both are upright. They were read from crops at 450 dpi, no rotation. The sheet is titled `FOR STANDARD`, not `FOR GALAXY`.

## Test and memory-clear buttons (page 24, top)

- `A4J3-5 (-W-)` runs to one terminal of a push button labelled `S33` `MEMORY CLEAR` (the colour is printed `(-W-)` with a hyphen on each side).
- `A4J3-1 (R)` runs to a push button labelled `TEST SWITCH`.
- `A3J2-7 (Y-R)` runs along the top and joins the other terminal of the `TEST SWITCH` and the other terminal of `S33 MEMORY CLEAR` (a single line closing both).

## Cabinet switch matrix (page 24)

Five strobe columns, drawn each with an open contact per row; column headings, verbatim: `ST0` over `A`, `ST1` over `B`, `ST2` over `C`, `ST3` over `D`, `ST4` over `E`. Row labels at the left margin: `I0` to `I7`. Return wires entering each row from the left: `A4J3-9 (R-W)` (`I0`), `A4J3-10 (BRN-W)` (`I1`), `A4J3-11 (BLU)` (`I2`), (no wire label printed) (`I3`), (no wire label printed) (`I4`), `A4J3-14 (BLU-W)` (`I5`), `A4J3-15 (BLU-O)` (`I6`), `A4J3-16 (Y)` (`I7`). Strobe wires at the foot, in order from the nearest column: `A4J3-2 (R-Y)`, `A4J3-3 (R-G)`, then three further strobe wires with no label (the lines for `ST2`, `ST3` and `ST4`).

Cell labels (written in the box above the contact), verbatim; `(blank)` is a contact drawn with no label:

| Row | ST0 A | ST1 B | ST2 C | ST3 D | ST4 E |
| --- | --- | --- | --- | --- | --- |
| I0 | CHUTE | (blank) | (blank) | (blank) | (blank) |
| I1 | CHUTE | (blank) | (blank) | (blank) | (blank) |
| I2 | CHUTE | (blank) | (blank) | (blank) | (blank) |
| I3 | (blank) | (blank) | (blank) | (blank) | (blank), two contacts, see below |
| I4 | (blank) | (blank) | (blank) | (blank) | (blank), two contacts, see below |
| I5 | CREDIT | (blank) | (blank) | (blank) | (blank) |
| I6 | TILT | (blank) | (blank) | (blank) | (blank) |
| I7 | SLAM | (blank) | (blank) | (blank) | (blank) |

Drawn details:

- Diodes: a series diode is drawn on some contacts and not on others, as follows (`d` = diode drawn, `-` = none): I0 `d - d d -`; I1 `- - - - -`; I2 `- - - d -`; I3 `d d d d d`; I4 `d d d d d`; I5 `d - d d d`; I6 `d d d d -`; I7 `d d d d -` (columns ST0 to ST4). The note on the sheet reads `ALL DIODES ARE IN-4004`.
- `I3` and `I4`, ST4: each is drawn as two open contacts, one in series with the diode and a second contact in parallel with the first, joined at the diode side (the cell shows two switch symbols one above the other joined at one end); neither carries a label. The `I3` and `I4` rows carry no wire label at the left.
- `I6`, ST0 (`TILT`): a second open contact is drawn below the `TILT` contact connecting the `I6` return line (through a capacitor symbol at the left of the row) to the same node; the capacitor and the second contact carry no label.
- `I1`, ST2: the circle after the contact has a tick through it (a mark on the scan).

## Flipper buttons and front door lights (page 24, bottom)

- `A3J2-2 (BLU)` to a contact labelled `LEFT FLIPPER`; `A3J2-1 (R)` to a contact labelled `RIGHT FLIPPER`; the two contacts' other ends join a common line that returns on `A2J2-9 (O)`.
- `FRONT DOOR LITES`: a lamp symbol fed by `A2J2-1 (Y-B)` (printed `Y-3` with the `B` overwritten) and returning on `A2J2-5 (G-R)`.
- The return rows join a common line at the foot that exits at the lower left with an arrowhead.

Notes at the foot, verbatim (hand lettered): `N/U = NOT USED`, `ALL DIODES ARE 1N-4004`.

## Cabinet loads (page 24 right, continued on page 25)

The three coils share a rail fed from `A2J2-2 (G)`. Each is drawn as one winding with a diode across it.

| Load, as labelled | Return wire, as printed | Notes |
| --- | --- | --- |
| COIN LOCKOUT | A3J2-8 (Y-W) | |
| GEN. ILLUM. RELAY | A3J5-7 (W-BLU) | the wire ends in a double chevron `>>` just before it turns up to the relay |
| KNOCKER | A3J2-5 (B-Y) | double chevron `>>` as above; the colour is printed `(B-Y)` with the `B` overwritten |

Feed rail: `A2J2-2` (colour `G`), joining all three loads.

## Power input (pages 24 and 25)

- A two-pole switch labelled `POWER ON/OFF` (with an arrow to the switch). Its two outputs run down the left of page 25 to vertical wires labelled `A2J2-6 (Y)` and `A2J2-7 (BLU-W)` (printed along the wires).
- A third vertical wire, `A2J2-10 (G)`, runs to line input pin `3`.
- Line input: three pins drawn as chevrons with a number, each continuing into a `LINE FILTER` box: pin `1` labelled `L1` (wire colour `(B)`), pin `2` labelled `L2` (wire colour `(W)`), pin `3` joined to the ground. A `SERVICE OUTLET` symbol (a lamp-like circle) is connected between pins 1 and 2; its ground connection is labelled `GRD` and joins the line from pin 3.
- From the `LINE FILTER`: outputs labelled `120 VAC`, `GRD` and `120 VAC RETURN`; a ground tab labelled `GRD. BRAID` below the filter.
- A varistor `VR1`, labelled `GE #V130LA10A` and `VARISTOR`, between the `120 VAC` line and the `120 VAC RETURN` line.

## Front door jack (page 25)

Headed `FRONT DOOR JACK`, columns `JACK PIN NO.` and `FROM :`. Rows, verbatim; a dashed leader from the pin number to the source is shown as `(dotted)`:

| JACK PIN NO. | FROM | Notes |
| ---: | --- | --- |
| 1 | A4J3-9 | |
| 2 | A4J3-10 | |
| 3 | A4J3-11 | (dotted) |
| 4 | A4J3-12 | |
| 5 | A4J3-13 | |
| 6 | A4J3-14 | (dotted) |
| 7 | A4J3-15 | |
| 8 | A4J3-16 | |
| 10 | A4J3-2 | (dotted) |
| 15 | A2J2-2 | |
| 16 | A3J2-8 | (dotted) |
| 17 | A2J2-1 | |
| 18 | A2J2-5 | |
| 19 | A4J3-1 | (dotted) |
| 20 | A3J2-7 | |

Pins 9 and 11 to 14 are not listed. A blank line separates pins `10` and `15`. Pins `1` to `8` and `10` are the matrix return wires `A4J3-9` to `A4J3-16` and strobe `A4J3-2`; pins `15`, `16`, `17`, `18`, `19` and `20` are the loads and test circuit pins as listed.
