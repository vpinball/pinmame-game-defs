# Williams Black Knight (game 500) — Playfield Solenoid Wiring Diagram

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310),
PDF page 67, printed page `23`, sheet marked `500`. The sheet is a landscape scan; its caption, printed page number and
sheet number run sideways, but the drawing itself reads upright in the unrotated landscape render (`man600-67.png`), so
no rotation was applied for reading. Transcribed by hand from the 600 dpi render, cross-checked against the 300 dpi colour
copy (`Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf`, PDF page 20, right half), which carries
handwritten pen marks that are not part of the printed drawing and are ignored here.

Heading, verbatim: `Playfield Solenoid Wiring Diagram` (italic caption, left margin, sideways); printed page number `23`
(left, sideways); sheet number `500` (right, sideways).

Normalizations: none to spelling. Wire colours are kept literal (`GRY-BLK`, `ORG-GRY`, `ORN-BLK`, `WHT-RED`, ...); note that
the drawing uses `ORG-` for the two flipper-button wires on 2P12 and `ORN-` for the special-switch wires on 2P13.
"Sol." numbers are the printed `SOL. n`. Connector pin numbers are as printed on the J (jack) side next to the connector
bar; the P (plug) bar at each pair carries the same numbers except 8P6/8J6, which are renumbered (see the 8P3/8J3 to 8P6/8J6
table). Diode triangle direction is stated as drawn (the triangle's point and the bar end) without electrical interpretation.
All coils are drawn as coil symbols with the legend printed beside them; where the legend is split over lines it is shown
joined with `/`.

## Connector chain, left side (driver board / power supply / cabinet, to the 8P3/8J3 playfield connector)

The chain is drawn: source connector `nJm` (jack, printed with arrows into it) -> `nPm` (plug) -> printed wire colour and
`SOL. n` label -> `8P3` pin (plug bar) -> `8J3` pin (jack bar, same number).

### 2J11 / 2P11 (labelled `DRIVER BOARD`, brace on the Q column)
| Driver transistor | 2J11 pin | 2P11 wire colour | Printed label | 8P3 pin / 8J3 pin |
|---|---|---|---|---|
| Q29 | 1 | GRY-BLK | SOL. 8 | 8 |
| Q25 | 3 | GRY-BLU | SOL. 6 | 6 |
| Q19 | 7 | GRY-ORN | SOL. 3 | 3 |
| Q17 | 5 | GRY-RED | SOL. 2 | 2 |
| Q15 | 4 | GRY-BRN | SOL. 1 | 1 |
| Q23 | 9 | GRY-GRN | SOL. 5 | 5 |
| Q21 | 8 | GRY-YEL | SOL. 4 | 4 |
| Q27 | 2 | GRY-VIO | SOL. 7 | 7 (the GRY-VIO line is drawn with a right-angle bend; it lands on 8P3 pin 7, below the pin-4 row) |

### 3J3 / 3P3 (labelled `POWER SUPPLY`, brace on the two arrows)
| 3J3 pin | 3P3 wire colour | Printed label | 8P3 pin |
|---|---|---|---|
| 6 | RED | SOL. B+ | 36 |
| 3 | BLK | GROUND | 35 |

### 2J9 / 2P9 (inside the large unlabelled dashed enclosure at left)
| Driver transistor | 2J9 pin | 2P9 wire colour | Printed label | 8P3 pin | Right of 8J3 |
|---|---|---|---|---|---|
| Q31 | 9 | BRN-BLK | SOL. 9 | 9 | continues |
| Q33 | 7 | BRN-RED | SOL. 10 | 10 | continues |
| Q37 | 2 | BRN-YEL | SOL. 12 | 12 | `N.C.` printed right of 8J3 pin 12 |
| Q39 | 3 | BRN-GRN | SOL. 13 | 13 | `N.C.` printed right of 8J3 pin 13 |

### 2J12 / 2P12 (same dashed enclosure)
| Source | 2J12 pin | 2P12 wire colour | Printed label | 8P3 pin | Right of 8J3 |
|---|---|---|---|---|---|
| Q6 | 3 | BLU-ORN | SOL. 19 | 19 | continues |
| Q2 | 7 | BLU-BRN | SOL. 17 | 17 | continues |
| Q4 | 4 | BLU-RED | SOL. 18 | 18 | continues |
| Q8 | 6 | BLU-YEL | SOL. 20 | 20 | `N.C.` |
| Q10 | 8 | BLU-GRN | SOL. 21 | 21 | `N.C.` |
| Q12 | 9 | BLU-BLK | SOL. 22 | 22 | `N.C.` |
| (no Q printed; node shared with Z1 contact) | 2 | ORG-GRY | (no label printed) | wire runs to 7P1 pin 9 "LEFT FLIPPER" | — |
| (no Q printed; node shared with Z1 contact) | 1 | ORG-VIO | (no label printed) | wire runs to 7P1 pin 7 "RIGHT FLIPPER" | — |

Relay `Z1` (drawn in its own small dashed box inside the large dashed enclosure, label `Z1`): a switch symbol (blade drawn
open) and a separate coil symbol with both coil ends unconnected. One switch terminal goes to a ground symbol (at left); the
other switch terminal goes to a dot that is joined to both 2J12 pin 2 and 2J12 pin 1 (both arrows enter 2J12 from this node).
No `Z1` coil connection, designator pin or coil drive is drawn.

### 2J13 / 2P13 (same dashed enclosure; sources printed as `SOL. nn SPEC. SW`)
| Source label | 2J13 pin | 2P13 wire colour | 8P3 pin | Right of 8J3 |
|---|---|---|---|---|
| SOL. 19 SPEC. SW | 2 | ORN-BLK | 26 | to 8SW67 / 8C3 / 8R3 node |
| SOL. 17 SPEC. SW | 5 | ORN-BRN | 24 | continues to 8P6 pin 10 |
| SOL. 18 SPEC. SW | 3 | ORN-RED | 25 | continues to 8P6 pin 11 |
| SOL. 20 SPEC. SW | 4 | ORN-YEL | 27 | `N.C.` |
| SOL. 21 SPEC. SW | 8 | ORN-GRN | 28 | `N.C.` |
| SOL. 22 SPEC. SW | 9 | ORN-BLU | 29 | `N.C.` |

### 7J1 / 7P1 (dashed box labelled `PART OF CABINET`)
| 7J1 pin | 7P1 wire/label as printed | 8P3 pin |
|---|---|---|
| 7 | `RIGHT FLIPPER` (label only, no colour printed on this line; line turns up and runs to the ORG-VIO wire from 2P12 pin 1) | — |
| 31 | BLK-YEL | 33 |
| 8 | BLU-VIO | 34 |
| 10 | BLU-GRY | 32 |
| 30 | BLK-BLU | 31 |
| 9 | `LEFT FLIPPER` (label only, no colour printed on this line; line turns up and runs to the ORG-GRY wire from 2P12 pin 2) | — |

Flipper buttons inside `PART OF CABINET`: `RIGHT FLIPPER BUTTON` is drawn as two switches (two blades). Their upper terminals are
joined together and wired to 7J1 pin 7; the lower terminal of the first switch is wired to 7J1 pin 8, the lower terminal of
the second switch to 7J1 pin 31. `LEFT FLIPPER BUTTON` is drawn as two switches; their lower terminals are joined and wired
to 7J1 pin 9; the upper terminal of the first switch is wired to 7J1 pin 10, the upper terminal of the second to 7J1 pin 30.
The blades are drawn open (not touching the lower/upper contact respectively) in all four switches.

### Flipper B+ (bottom left)
| 3J3 pin | 3P3 wire colour | Goes to |
|---|---|---|
| 4 | BLU | 8P2 pin 23 (and, over the same rail, 8P5 pin 23) |
| 5 | GRY | 8P2 pin 24 (and 8P5 pin 24) |

Printed label on the 3J3 pair: `FLIPPER B+ FROM POWER SUPPLY` (brace on the two arrows).

## 8P3/8J3 to 8P6/8J6 pin correspondence (the drawing prints the numbers on all four bars)
| 8P3 / 8J3 pin | Source wire | Goes to 8P6/8J6 pin |
|---|---|---|
| 8 | GRY-BLK SOL. 8 | 5 |
| 6 | GRY-BLU SOL. 6 | 4 |
| 3 | GRY-ORN SOL. 3 | 3 |
| 2 | GRY-RED SOL. 2 | 2 |
| 1 | GRY-BRN SOL. 1 | 1 |
| 5 | GRY-GRN SOL. 5 | stays on the 8J3 bar (to 8L5) |
| 4 | GRY-YEL SOL. 4 | stays on the 8J3 bar (to 8L4) |
| 36 | RED SOL. B+ | 15 (common of the coil network) and to 8L4/8L5/8L7/8L19 on the 8J3 bar |
| 7 | GRY-VIO SOL. 7 | stays on the 8J3 bar (to 8L7) |
| 9 | BRN-BLK SOL. 9 | 6 |
| 10 | BRN-RED SOL. 10 | 7 |
| 12, 13 | BRN-YEL SOL. 12, BRN-GRN SOL. 13 | `N.C.` at 8J3; no 8P6 pin |
| 19 | BLU-ORN SOL. 19 | stays on the 8J3 bar (to 8L19) |
| 17 | BLU-BRN SOL. 17 | 8 |
| 18 | BLU-RED SOL. 18 | 9 |
| 20, 21, 22 | BLU-YEL, BLU-GRN, BLU-BLK | `N.C.` at 8J3 |
| 35 | BLK GROUND | 14 |
| 26 | ORN-BLK (SOL. 19 SPEC. SW) | stays on the 8J3 bar (8SW67 / 8C3 / 8R3) |
| 24 | ORN-BRN (SOL. 17 SPEC. SW) | 10 |
| 25 | ORN-RED (SOL. 18 SPEC. SW) | 11 |
| 27, 28, 29 | ORN-YEL, ORN-GRN, ORN-BLU | `N.C.` at 8J3 |
| 33 | BLK-YEL (7P1 pin 31) | stays on the 8J3 bar (to 8L27) |
| 34 | BLU-VIO (7P1 pin 8) | 13 |
| 32 | BLU-GRY (7P1 pin 10) | 12 |
| 31 | BLK-BLU (7P1 pin 30) | stays on the 8J3 bar (to 8L26) |

Other connectors with printed pins on this sheet: `8P7` / `8J7` pin `1` with a line labelled `WHT-RED` running left to a ground
symbol; `8P2` / `8J2` pins `23` and `24`; `8P5` / `8J5` pins `23` and `24`.

## Coils, each drawn with a diode across it

Every solenoid below is drawn as a coil with its diode in parallel. "Top end" and "bottom end" are as drawn on the sheet
(coil vertical). The common node (`8J3` pin `36` / `8J6` pin `15`, source `RED SOL. B+`) is the horizontal line that runs
from 8J3 pin 36 to 8P6/8J6 pin 15.

| Coil | Printed name (verbatim, lines joined with `/`) | Diode | Coil top end (as drawn) | Coil bottom end (as drawn) | Diode orientation as drawn |
|---|---|---|---|---|---|
| 8L1 | BALL / RELEASE | 8D129 | 8J6 pin 1 (8P3 pin 1, GRY-BRN SOL. 1, Q15) | common (8J6 pin 15) | triangle points toward the common-node end |
| 8L2 | LOWER LEFT / 3-BANK / DROP TARGETS / RESET | 8D130 | 8J6 pin 2 (8P3 pin 2, GRY-RED SOL. 2, Q17) | common | triangle points toward the common-node end |
| 8L3 | LOWER RIGHT / 3-BANK / DROP TARGETS / RESET | 8D131 | 8J6 pin 3 (8P3 pin 3, GRY-ORN SOL. 3, Q19) | common | triangle points toward the common-node end |
| 8L4 | UPPER LEFT / 3-BANK / DROP TARGETS / RESET | 8D132 | 8J3 pin 4 (GRY-YEL SOL. 4, Q21) | common (8J3 pin 36) | triangle points toward the common-node end |
| 8L5 | UPPER RIGHT / 3-BANK / DROP TARGETS / RESET | 8D133 | 8J3 pin 5 (GRY-GRN SOL. 5, Q23) | common (8J3 pin 36) | triangle points toward the common-node end |
| 8L6 | BALL / RAMP / THROWER | 8D134 | 8J6 pin 4 (8P3 pin 6, GRY-BLU SOL. 6, Q25) | common | triangle points toward the common-node end |
| 8L7 | "MULTIBALL" / RELEASE (quotation marks printed around MULTIBALL) | 8D135 | common (8J3 pin 36) | 8J3 pin 7 (GRY-VIO SOL. 7, Q27) | triangle points toward the common-node end |
| 8L8 | LOWER / EJECT / HOLE | 8D136 | 8J6 pin 5 (8P3 pin 8, GRY-BLK SOL. 8, Q29) | common | triangle points toward the common-node end |
| 8L17 | LEFT / KICKER | 8D145 | common (8J6 pin 15) | 8J6 pin 8 (8P3 pin 17, BLU-BRN SOL. 17, Q2) | triangle points toward the common-node end |
| 8L18 | RIGHT / KICKER | 8D146 | common (8J6 pin 15) | 8J6 pin 9 (8P3 pin 18, BLU-RED SOL. 18, Q4) | triangle points toward the common-node end |
| 8L19 | JET / BUMPER | 8D147 | common (8J3 pin 36) | 8J3 pin 19 (BLU-ORN SOL. 19, Q6) | triangle points toward the common-node end |

Notes on the table: 8L1/8L2/8L3/8L6/8L8/8L17/8L18 hang on the 8J6 bar; 8L4/8L5/8L7/8L19 hang on the 8J3 bar. 8L17 and 8L18 sit
directly below 8L3 and 8L6 and share the common line with them (the common line runs between the upper coil and the lower
coil of each pair; 8L7 sits under 8L4, 8L19 under 8L5 in the same way).

## Magnet relay coils (each with a diode across the coil and a series resistor)
| Coil | Printed name | Diode | Series resistor (printed value) | Drive line pin (top end) | Resistor far end goes to |
|---|---|---|---|---|---|
| 8L10 | RIGHT / MAGNET / RELAY | 8D138 | 8R8, `100`, `3W` | 8J6 pin 7 (8P6 pin 7, from 8J3 pin 10, BRN-RED SOL. 10, Q33) | line routed down and right to the rail after fuse 8F2 (the 8J5/8P5 pin 23, `BLU` rail) |
| 8L9 | LEFT / MAGNET / RELAY | 8D137 | 8R7, `100`, `3W` | 8J6 pin 6 (8P6 pin 6, from 8J3 pin 9, BRN-BLK SOL. 9, Q31) | line routed right across the sheet to the rail after fuse 8F1 (the 8J5/8P5 pin 24, `GRY` rail) |

(The diode is drawn across the coil only, between the drive-line node and the coil/resistor node; triangle points toward the
coil/resistor node. The `8J3` pin 9 and pin 10 lines are the SOL. 9 and SOL. 10 wires.)

## Magnets (contacts drawn from the relay coils, each with a fuse and a diode)
| Magnet coil | Printed name | Diode | Fuse (printed) | Contact drawn above it, printed designator | Contact top terminal wired to | Coil bottom wired to |
|---|---|---|---|---|---|---|
| 8L28 | RIGHT / MAGNET | 8D156 | 8F1, `8A` | `8L9` | the `8P7`/`8J7` pin 1 line (`WHT-RED`, ground symbol at left) | rail after fuse 8F1 (8J5/8P5 pin 24, `GRY`, via 8F1) |
| 8L29 | LEFT / MAGNET | 8D157 | 8F2, `8A` | `8L10` | the `8P7`/`8J7` pin 1 line (`WHT-RED`) | rail after fuse 8F2 (8J5/8P5 pin 23, `BLU`, via 8F2) |

The two contact symbols are printed with the relay-coil designators `8L9` (above 8L28 RIGHT MAGNET) and `8L10` (above
8L29 LEFT MAGNET). The diode (8D156 / 8D157) is drawn across the magnet coil, triangle pointing toward the fuse-side rail node.
Fuse symbols: `8F1` on the pin-24 rail (right of 8L25 BOTTOM RIGHT FLIPPER's rail node and its diode 8D153, left of the 8L28
node); `8F2` on the pin-23 rail (right of 8L24 BOTTOM LEFT FLIPPER's rail node and its diode 8D152, left of the 8L29 node).

## Flipper coils (four; each drawn with an end-of-stroke-style switch across the upper winding section and a diode across the coil)
Each flipper coil is drawn as one coil symbol with a tap: a switch symbol (no designator printed; blade drawn open) is wired
from the coil's top node to the coil's mid tap, and a diode is wired across the whole coil.

| Coil | Printed name | Diode | Top node wired to | Bottom node wired to |
|---|---|---|---|---|
| 8L24 | BOTTOM / LEFT / FLIPPER | 8D152 (see Observations) | 8J6 pin 12 (8P6 pin 12, from 8J3 pin 32, BLU-GRY; 7P1 pin 10) | rail 8J5/8P5 pin 23 (BLU), through to the left side of fuse 8F2 |
| 8L25 | BOTTOM / RIGHT / FLIPPER | 8D153 | 8J6 pin 13 (8P6 pin 13, from 8J3 pin 34, BLU-VIO; 7P1 pin 8) | rail 8J5/8P5 pin 24 (GRY), to the left side of fuse 8F1 |
| 8L26 | UPPER / LEFT / FLIPPER | 8D152 (see Observations) | 8J3 pin 31 (BLK-BLU; 7P1 pin 30) | rail 8J2/8P2 pin 23 (BLU) |
| 8L27 | UPPER / RIGHT / FLIPPER | 8D155 | 8J3 pin 33 (BLK-YEL; 7P1 pin 31) | rail 8J2/8P2 pin 24 (GRY) |

For all four flipper diodes the triangle points toward the rail (B+) end and the bar is at the rail end.
The rails: `8P2`/`8J2` pins 23 and 24 and `8P5`/`8J5` pins 23 and 24 are joined by two horizontal lines (the pin-23 line and
the pin-24 line each run unbroken between 8J2 and 8J5; both carry `BLU` / `GRY` from 3P3 pins 4 and 5). 8L26 taps the
pin-23 line, 8L27 taps the pin-24 line.

## Special switches (`SPEC. SW`) and their RC parts (all sit on the 8P6/8J6 pin-14 line)

The common node of these is `8P6`/`8J6` pin `14`, joined to `8J3` pin 35 (BLK GROUND from 3P3 pin 3).

| Designator | Printed name | Contacts drawn | Series RC across it | Pins | Source wire (8J3) |
|---|---|---|---|---|---|
| 8SW65 | LEFT / KICKER | two parallel-wired blades (drawn as two switch symbols side by side, both top ends on the pin-14 line, both bottom ends on the pin-10 line) | `8C1` `22` (plus sign printed beside the plate on the 8R1 side) in series with `8R1` `100` between pin 14 and pin 10 | 8P6/8J6 pin 14 and pin 10 | pin 24, ORN-BRN, SOL. 17 SPEC. SW (2J13 pin 5) |
| 8SW66 | RIGHT / KICKER | two parallel-wired blades (both top ends on the pin-14 line, both bottom ends on the pin-11 line) | `8C2` `22` (plus sign beside the plate on the 8R2 side) in series with `8R2` `100` between pin 14 and pin 11 | 8P6/8J6 pin 14 and pin 11 | pin 25, ORN-RED, SOL. 18 SPEC. SW (2J13 pin 3) |
| 8SW67 | JET / BUMPER | one blade; top end on the 8J3 pin-35 / 8P6 pin-14 line | `8C3` `22` (plus sign beside the plate on the 8R3 side) in series with `8R3` `100` between pin 35 and pin 26 | 8J3 pin 35 and pin 26 | pin 26, ORN-BLK, SOL. 19 SPEC. SW (2J13 pin 2) |

(8SW67's pin-35 line also continues to 8P6/8J6 pin 14, so pin 14 and 8J3 pin 35 are one net.)

## Inside the dashed enclosure at left: relay `Z1`
See the 2J12 section above. Printed text: `Z 1`; coil drawn but with no connections shown to it; switch terminals to a ground symbol
and to the node tying 2J12 pins 1 and 2.

## Observations (internal disagreements and oddities, recorded literally)
- Magnet relay naming versus contact legends. The coil legended `8L10 RIGHT MAGNET RELAY` (drive line 8J6 pin 7 = SOL. 10 /
  BRN-RED / Q33, resistor 8R8, diode 8D138) is drawn with its contact symbol printed `8L10`, and that contact feeds the coil
  legended `8L29 LEFT MAGNET` (fuse 8F2, diode 8D157, rail BLU pin 23). The coil legended `8L9 LEFT MAGNET RELAY` (drive line
  8J6 pin 6 = SOL. 9 / BRN-BLK / Q31, resistor 8R7, diode 8D137) is drawn with its contact symbol printed `8L9`, and that
  contact feeds the coil legended `8L28 RIGHT MAGNET` (fuse 8F1, diode 8D156, rail GRY pin 24). So each relay legend says one
  side ("RIGHT" relay 8L10, "LEFT" relay 8L9) and the magnet whose contact it carries is on the opposite side by legend.
  The drawing does not say which side a given magnet is physically on.
- Relay-coil return resistors are also crossed with the fuse rails: 8R8 (relay 8L10) returns to the pin-23 rail after fuse 8F2,
  which also feeds 8L29 (the magnet legended LEFT) via that same fuse; 8R7 (relay 8L9) returns to the pin-24 rail after fuse 8F1,
  which also feeds 8L28 (legended RIGHT).
- Duplicate designator: `8D152` is printed twice, once beside the diode across 8L26 UPPER LEFT FLIPPER and once beside the
  diode across 8L24 BOTTOM LEFT FLIPPER. No `8D154` is printed on this sheet. 8L25 carries `8D153`, 8L27 carries `8D155`.
  Both legends legible in the 600 dpi render and in the colour copy.
- The wire labelled `RIGHT FLIPPER` on 7P1 pin 7 and the wire labelled `LEFT FLIPPER` on 7P1 pin 9 carry no colour at the 7P1
  end; their colours (ORG-VIO and ORG-GRY) are printed only at the 2P12 end (pins 1 and 2).
- Pins printed N.C.: 8J3 pins 12, 13, 20, 21, 22, 27, 28, 29. No solenoid numbers 11, 14, 15, 16 appear on this sheet.
- No transistor Q numbers are printed for 2J12 pins 1 and 2 (ORG-VIO and ORG-GRY); they connect to the Z1 contact node.

## Illegible / uncertain items
None. The routing of the two unlabelled-colour 7P1 wires was followed in a zoomed crop: the inner vertical run from 2P12 pin 1
(ORG-VIO) ends at 7P1 pin 7 `RIGHT FLIPPER`; the outer vertical run from 2P12 pin 2 (ORG-GRY) ends at 7P1 pin 9 `LEFT FLIPPER`.
They do not cross.
