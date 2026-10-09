# Williams Black Knight (game 500) — Cabinet Wiring Diagram

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310),
PDF page 65, printed page `21`, sheet marked `500`. The sheet is a landscape scan; its caption, printed page number and
sheet number run sideways, but the drawing itself reads upright in the unrotated landscape render (`man600-65.png`), so
no rotation was applied for reading. Transcribed by hand from the 600 dpi render.

Heading, verbatim: italic caption `Cabinet Wiring Diagram` (left margin, sideways); printed page number `21`; sheet number `500`.
There is no in-drawing title block on this sheet.

Cross-check against the 300 dpi colour copy (`Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf`, PDF page 19,
right half; it is printed rotated and carries handwritten pen marks, for example `16` beside the 7J1 pin printed `3` for
BRN-BLU and a small mark near pin 27/28, which are not part of the printed drawing). The colour copy is **not an identical
drawing**; its differences from this scan are listed under Observations. This file transcribes the 600 dpi English-manual page.

Normalizations: none to spelling or wire colours (`ORN-GRY`, `YEL-WHT` / `WHT-YEL` kept literal as printed on each
drawing). Pin numbers are as printed next to each connector bar. Where a connector pair is drawn as `nJm` (jack) then `nPm`
(plug), the pin number is printed once between them. Switch diodes on this sheet are drawn with the bar at the switch (upper) end
and the triangle pointing up toward the bar. "Dot" means a drawn solder-junction dot.

## Left-hand source connectors and the 7P1 / 7J1 bar

7P1 / 7J1 is a pair of tall connector bars (7P1 left, 7J1 right) with pin numbers printed between them; each wire is drawn
from a source connector's plug (`nPm`) straight across 7P1 to 7J1.

### Sound board (brace label `SOUND BOARD`)
| Connector | Pin | Printed signal label (left of jack) | Wire colour as printed | Goes to |
|---|---|---|---|---|
| 10J4 / 10P4 | 2 | AUDIO OUT | (not printed) | through a drawn shield symbol (dashed oval) to the top end of 7R1 REMOTE VOLUME (resistor symbol) |
| 10J4 / 10P4 | 1 | AUDIO IN | (not printed) | through the shield symbol to the wiper arrow of 7R1 |
| 10J4 / 10P4 | 4 | SHIELD | (not printed) | to the shield symbol; the bottom end of 7R1 is wired back through a second shield symbol |
| 10J2 / 10P2 | 2 | AUDIO | BLK-BRN | 7P1 / 7J1 pin 33 |
| 10J2 / 10P2 | 3 | GRD | BLACK | 7P1 / 7J1 pin 32 |

`7R1` printed with legend `REMOTE VOLUME` (a potentiometer symbol with a wiper arrow). `SPEAKER` (printed): speaker symbol with
coil, `+` printed beside the coil end on the 7J1 pin 33 side; the other end goes to 7J1 pin 32. No designator is printed for the
speaker.

### Power supply +28 V
| Connector | Pin | Label | Wire colour | Goes to |
|---|---|---|---|---|
| 3J3 / 3P3 | 7 | `+28V` (brace label `POWER SUPPLY`) | RED | 7P1 / 7J1 pin 3 |

### Driver board solenoids (brace label `DRIVER BOARD` covers this and the following driver-board groups)
| Connector | Pin | Label printed left of jack | Wire colour | 7P1 / 7J1 pin |
|---|---|---|---|---|
| 2J9 / 2P9 | 4 | SOL. 14 (Q41) | BRN-BLU | printed `3`; a line from 7J1 pin 3 on this wire ends at the text `NC` (see Observations) |
| 2J9 / 2P9 | 5 | SOL. 15 (Q43) | BRN-VIO | 17 |
| 2J9 / 2P9 | 6 | SOL. 16 (Q45) | BRN-GRY | 18 |

### Driver board lamp columns
| Connector | Pin | Label | Wire colour | 7P1 / 7J1 pin |
|---|---|---|---|---|
| 2J2 / 2P2 | 9 | COL. 1 | GRN-BRN | 19 |
| 2J2 / 2P2 | 8 | COL. 2 | GRN-RED | 20 |

(The word `COL.` is as printed; these are the switch-matrix columns of the cabinet switches.)

### Driver board rows (2J3 / 2P3)
| 2J3 pin | Label | Wire colour | 7P1 / 7J1 pin |
|---|---|---|---|
| 9 | ROW 1 | WHT-BRN | 21 |
| 8 | ROW 2 | WHT-RED | 22 |
| 7 | ROW 3 | WHT-ORN | 23 |
| 6 | ROW 4 | WHT-YEL | 24 |
| 5 | ROW 5 | WHT-GRN | 25 |
| 4 | ROW 6 | WHT-BLU | 26 |
| 3 | ROW 7 | WHT-VIO | 27 |
| 1 | ROW 8 | WHT-GRY | 28 |

### Flipper ground (2J12 / 2P12; brace label `FLIPPER GRD`, inside the `DRIVER BOARD` brace)
| Pin | Wire colour | 7P1 / 7J1 pin |
|---|---|---|
| 2 | ORN-GRY | 9 |
| 1 | ORN-VIO | 7 |

### Playfield flipper coils (8J3 / 8P3; brace label `PLAYFIELD FLIPPER COILS`)
| 8J3 pin | Wire colour | 7P1 / 7J1 pin |
|---|---|---|
| 3 | BLU-VIO | 8 |
| 15 | BLK-YEL | 31 |
| 4 | BLU-GRY | 10 |
| 9 | BLK-BLU | 30 |

### CPU board (1J4 / 1P4; brace label `CPU BOARD`)
| 1J4 pin | Label | Wire colour | 7P1 / 7J1 pin |
|---|---|---|---|
| 1 | MEM. PROT. | BLK-RED | 34 |
| 2 | GRD. | WHT | 4 |
| 3 | ADVANCE | GRN | 5 |
| 4 | AUTO./MAN. | BLU | 6 |

### Power supply 6.3 VAC (lower left; label `POWER SUPPLY`, small label `POWER SUPPLY 6.3 VAC` with a brace)
A first connector pair with no designator printed carries pin `4` (wire `YEL`) and pin `9` (wire `WHT-YEL`) and goes to a second pair
printed `3J8` / `3P8`, whose pins are printed `6`, `3`, `2`, `5` (top to bottom). Wiring drawn:
- the `YEL` wire goes to 3J8 pin 2; the `WHT-YEL` wire goes to 3J8 pin 5.
- 3J8 pin 6 is wired to 7P1 / 7J1 pin 2; 3J8 pin 3 is wired to 7P1 / 7J1 pin 1.
- on the 3P8 side the top two arrows are printed `YEL` (pin-6 level) and `WHT-YEL` (pin-3 level); a lamp symbol labelled
  `UPPER PLAYFIELD` (no designator) is drawn across the 3P8 pin-2 and pin-5 levels, with the `YEL` line returning to the
  pin-5 level and the `WHT-YEL` line to the pin-2 level.
- 7P1 / 7J1 pins `1` and `2` run straight across to 7J2 / 7P2 pins `1` and `2` and the three general-illumination lamps (below).

## Bell and coin lockout (solenoid-driven)
| Designator | Printed legend | Diode | One end | Other end |
|---|---|---|---|---|
| 7L15 | BELL | 7D15 (across the coil, triangle pointing up toward the bar at its top end) | 7J1 pin 3 (+28 V RED line; dots at the line) | 7J1 pin 17 (BRN-VIO, SOL. 15 (Q43)) |
| 7L16 | COIN LOCKOUT | 7D10 (across the coil, triangle pointing up toward the bar at its top end) | 7P2 pin 3 (continuation of the 7J1 pin 3 line through 7J2 pin 3 to 7P2 pin 3) | 7P2 pin 4 (continuation of 7J1 pin 18, BRN-GRY, SOL. 16 (Q45), through 7J2 pin 4 to 7P2 pin 4) |

## Cabinet switches (matrix; column lines drawn horizontally, row lines horizontally)
Column lines: `7J1 pin 19` (GRN-BRN, COL. 1) feeds 7SW1, 7SW2, 7SW3 and, through 7J2 / 7P2 pin `6`, 7SW4-7SW8;
`7J1 pin 20` (GRN-RED, COL. 2) feeds 7SW9 and 7SW10. Row lines: 7J1 pins 21-28 (WHT-BRN ... WHT-GRY, ROW 1 ... ROW 8); the
coin-door switches' diodes go to 7J2 / 7P2 pins 8-12.

| Switch | Printed name (lines joined with space) | Diode | Top terminal wired to | Diode lower end wired to |
|---|---|---|---|---|
| 7SW9 | RIGHT MAGNET BUTTON | 7D9 | 7J1 pin 20 line (COL. 2, GRN-RED) | 7J1 pin 21 line (ROW 1, WHT-BRN) |
| 7SW10 | LEFT MAGNET BUTTON | 7D10 | 7J1 pin 20 line (COL. 2, GRN-RED) | 7J1 pin 22 line (ROW 2, WHT-RED) |
| 7SW1 | PLUMB BOB TILT | 7D1 | 7J1 pin 19 vertical (COL. 1, GRN-BRN) and the line continuing to 7J2 / 7P2 pin 6 | 7J1 pin 21 line (ROW 1, WHT-BRN) |
| 7SW2 | BALL ROLL TILT | 7D2 | the same COL. 1 line (7J2/7P2 pin 6 line) | 7J1 pin 22 line (ROW 2, WHT-RED) |
| 7SW3 | CREDIT BUTTON | 7D3 | the same COL. 1 line | 7J1 pin 23 line (ROW 3, WHT-ORN) |
| 7SW4 | RIGHT COIN CHUTE | 7D4 | 7P2 pin 6 line (COL. 1) | 7P2 pin 8 |
| 7SW5 | CENTER COIN CHUTE | 7D5 | 7P2 pin 6 line | 7P2 pin 9 |
| 7SW6 | LEFT COIN CHUTE | 7D6 | 7P2 pin 6 line | 7P2 pin 10 |
| 7SW7 | SLAM TILT | 7D7 | 7P2 pin 6 line | 7P2 pin 11 |
| 7SW8 | HIGH SCORE RESET | 7D8 | 7P2 pin 6 line | 7P2 pin 12 |

7J1 pins 24-28 (ROW 4-8) continue as lines to 7J2 pins 8-12 (see Observations on the ROW 4 line). 7J2 / 7P2 pins 8-12 are the
row connections for 7SW4-7SW8: 7P2 pin 8 <- 7D4, 9 <- 7D5, 10 <- 7D6, 11 <- 7D7, 12 <- 7D8.

All switches here are drawn as single-pole open contacts (blade drawn open).

## Flipper buttons
`7SW72` legend `RIGHT FLIPPER` and `7SW73` legend `LEFT FLIPPER`. Each is drawn as two switch symbols side by side; the
designator is printed beside the first symbol of each pair only (the second symbol of each pair has no designator).
| Button | Common (upper) terminals | Lower terminal of 1st symbol | Lower terminal of 2nd symbol |
|---|---|---|---|
| 7SW72 RIGHT FLIPPER | joined, wired to 7P1 / 7J1 pin 7 (ORN-VIO) | 7P1 / 7J1 pin 8 (BLU-VIO) | 7P1 / 7J1 pin 31 (BLK-YEL) |
| 7SW73 LEFT FLIPPER | joined, wired to 7P1 / 7J1 pin 9 (ORN-GRY) | 7P1 / 7J1 pin 10 (BLU-GRY) | 7P1 / 7J1 pin 30 (BLK-BLU) |

## Memory protect, advance, auto/manual
| Designator | Printed legend | Wiring as drawn |
|---|---|---|
| 7SW76 | MEMORY PROTECT INTERLOCK | one terminal to 7P1 / 7J1 pin 34 (BLK-RED, MEM. PROT.); the other terminal to a dot on the 7P1/7J1 pin 4 (WHT, GRD.) line, which runs on to 7J2 / 7P2 pin 13 |
| 7SW75 | ADVANCE | upper terminal on the line from 7J2 / 7P2 pin 13 (shared with the 7SW74 upper terminal); lower terminal to 7J2 / 7P2 pin 14 (the 7P1/7J1 pin 5, GRN, ADVANCE line) |
| 7SW74 | (legends `AUTO-UP` and `MANUAL-DOWN`) | upper terminal on the same line as 7SW75's upper terminal; `AUTO-UP` contact wired to 7J2 / 7P2 pin 15 (the 7P1/7J1 pin 6, BLU, AUTO./MAN. line); `MANUAL-DOWN` contact drawn as an open circle with no wire |

## General illumination
7P1 / 7J1 pins `1` and `2` run through 7J2 / 7P2 pins `1` and `2` to three lamp symbols drawn in parallel (an upper line from pin 1,
a lower line from pin 2, dots at each lamp); legend `GENERAL ILLUMINATION`. The three lamps carry no designators.

## Coin door devices summary (as drawn)
Coin switches 7SW4 / 7SW5 / 7SW6 (right / center / left coin chute), 7SW7 slam tilt, 7SW8 high score reset, 7L16 coin lockout,
7SW9 / 7SW10 magnet buttons (named as buttons, not on the coin door by label), 7SW3 credit button; no other coin-door
device is labelled. The knocker is not drawn on this sheet; `7L15 BELL` is the only chime/bell device printed.

## Observations (internal disagreements and oddities, recorded literally)
- Duplicate designator: `7D10` is printed twice, once as the diode of 7SW10 LEFT MAGNET BUTTON and once as the diode across
  7L16 COIN LOCKOUT. No other designator is repeated.
- Duplicate pin number: 7P1 / 7J1 pin `3` is printed on both the RED +28 V wire (3P3 pin 7) and the BRN-BLU SOL. 14 (Q41)
  wire from 2P9 pin 4; the SOL. 14 line ends at the text `NC` on the 7J1 side. The next printed pin below it is 17. (The
  colour copy carries a handwritten `16` beside this pin.)
- 7P1 pin `7` carries ORN-VIO and pin `9` carries ORN-GRY (printed in the order 9 then 7 on the sheet); the flipper buttons
  7SW72/7SW73 common terminals go to pin 7 and pin 9 respectively. These are the same wires as the 2J12/2P12 `FLIPPER GRD` lines on
  the playfield solenoid sheet, where they are drawn through the Z1 contact node to ground.
- ROW 4 line: the line from 7J1 pin 24 (WHT-YEL) stops short, about three quarters of the way from 7J1 to 7J2 and well before 7J2, and does not reach
  the 7J2 pin 8 arrow (a short stub is drawn at 7J2 pin 8). The ROW 5-ROW 8 lines (pins 25-28) run unbroken to 7J2 pins 9-12.
  The colour copy draws the ROW 4 line unbroken from pin 24 to pin 8.
- 6.3 VAC wiring differs between the two scans: this scan draws an unlabelled connector pair (pins 4, 9; YEL, WHT-YEL) feeding
  `3J8`/`3P8` (pins 6, 3, 2, 5) with an `UPPER PLAYFIELD` lamp and wires from 3J8 pins 3 and 6 to 7P1 pins 1 and 2; the colour copy
  draws a single pair printed `3J8`/`3P8` with pins 4 and 9 (wires `YEL` and `YEL-WHT`) wired directly to 7P1 pins 1 and 2, with no
  upper-playfield lamp and no second connector pair.
- Wire colours are not printed for the 10J4/10P4 audio lines or for the 7R1 / speaker wiring.
- Switch designators on this sheet: 7SW1-7SW10, 7SW72-7SW76 (no 7SW11-7SW71 appear).
- The `MANUAL-DOWN` contact of 7SW74 is an unconnected circle.

## Illegible / uncertain items
None unreadable. `[uncertain]`: the printed value of the pin number beside the BRN-BLU / `NC` line is `3` in this scan (matching
the RED line), and `16` in the pen annotation of the colour copy; recorded as printed (`3`).
