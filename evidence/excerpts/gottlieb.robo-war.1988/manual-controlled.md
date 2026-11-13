---
source: pinball_robowar_gottlieb_instruction_manual_2_of_2.pdf
source_sha256: f96ce0b20bebce7fdd085809e00c2eef6cc044957ec3942353f48fd053debb83
locator: PDF page 11; printed folio 41; X. WIRING AND SCHEMATIC DIAGRAMS, PARTS LISTS - PLAYBOARD "CONTROLLED" SOLENOIDS AND ILLUMINATION (no drawing number printed on this page; the facing page 42 carries E-25887)
method: Visual transcription from the 600 dpi native page render, checked against Windows OCR
transcribed_by: curator transcription
reviewed: true
status: curator transcription checked cell by cell against the rendered page; uncertain readings are marked
---

# Page 41 - Playboard "controlled" solenoids and illumination

Page heading: `X. WIRING AND SCHEMATIC DIAGRAMS, PARTS LISTS` (only `X. WIRING AND SCHEMATI` is visible; the rest is cut off at the page edge). Sub-heading: `PLAYBOARD "CONTROLLED" SOLENOIDS AND ILLUMINATION`. Folio `41`.

Conventions on the drawing: a boxed number such as `[133]` is a wire colour code (note 4: "XXX indicates wire color"; the colour code table is below). Connector symbols are printed as a pair, e.g. `A9P7/J7` with the pin number printed twice (once per mating half); "10/10" below means that pin number is printed on both halves.

## Printed tables and notes

### Parts reference table (top right)

| REFERENCE | PART NO. |
| --- | --- |
| #44 LAMP | LA-0 |
| #67 LAMP | LA-5 |
| D1-D10 (1N5401) | XO-263 |
| (six further rows) | **[blank]** |

### COLOR CODE

| Digit | Colour |
| --- | --- |
| 0 | BLACK |
| 1 | BROWN |
| 2 | RED |
| 3 | ORANGE |
| 4 | YELLOW |
| 5 | GREEN |
| 6 | BLUE |
| 7 | VIOLET |
| 8 | GRAY |
| 9 | WHITE |

### NOTES (printed)

1. UNLESS OTHERWISE SPECIFIED, ALL DIODES ARE TYPE 1N4004.
2. LAMPS L4 THRU L11 AND L32 THRU L43 ARE DRIVEN BY MPS-A13'S; EXCEPT FOR "AL" LAMPS, ALL OTHER LAMPS ARE DRIVEN BY MPS-U45'S.
3. UNLESS OTHERWISE SPECIFIED, GROUND WIRE COLOR IS 9, 18 GAUGE.
4. [XXX] INDICATES WIRE COLOR.
5. UNLESS OTHERWISE SPECIFIED, ALL LAMPS ARE TYPE #44.

Other printed block labels: `OUTPUT FROM A3 MASTER DRIVER BOARD` (brace at A3J4, and a second brace at A3J3-22); `OUTPUT FROM A3 MASTER DRIVER BOARD (SEE SCHEMATIC FOR LAMP DRIVER TRANSISTOR)` (brace in the right-hand column, beside the notes); `A13 RESISTOR BOARD MA-1101`; `A19 SWITCHING DIODE BOARD MA-1102, D1-D10`; `TRANSISTOR DRIVER BOARD 1A16` with `MA-1104`; `TRANSISTOR DRIVER BOARD 2A16` with `MA-1079`.

## 1. Relays (top block)

Each relay is drawn as a coil labelled `16890` with a diode (arrow symbol) across it. The right-hand ends of all four coils join one vertical line. Wires `[222]` at A9P7/J7 pins 4 and 5 leave that same vertical line, and so does the contact `Q` (below).

| Relay | Lamp driver | A3 connector pin | Wire at A3 | Via | Wire at coil | Coil part | Printed label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S | L12 | A3J3 pin 25 | [133] | A9P7/J7 pin 10 (10/10) | [133] | 16890 | SWITCHING RELAY "S" |
| T | L1 | A3J3 pin B (printed with an overbar) | [288] | A9P7/J7 pin 8 (8/8) | [288] | 16890 | TILT RELAY "T" |
| Q | L0 | A3J3 pin A (printed with an overbar) | [277] | A9P7/J7 pin 9 (9/9) | [277] | 16890 | GAME OVER RELAY "Q" |
| A | L13 | A3J3 pin 24 | [122] | none drawn | no wire box on the coil side | 16890 | AUX.LAMP RELAY "A" |

Printed text next to the relays: `SWITCHED +24V DC`, with a curved arrow pointing at the node just right of contact Q.

### Relay contacts as drawn

| Relay | Contact symbol | Connector pins | Wires | Connects (as drawn) |
| --- | --- | --- | --- | --- |
| Q | two parallel plates (normally-open symbol), label `Q` above | A9P7/J7 pins 6 (6/6) and 7 (7/7) | [388] at pin 6 on both halves; [388] at pin 7 on both halves | The coil-common vertical line (which also feeds [222] at A9P7/J7 pins 4 and 5) to the wire-388 node. The node after the contact feeds pin 6 directly and pin 7 through a vertical branch. |
| S | two parallel plates (normally-open symbol), label `S` above | A9P7/J7 pin 12 (12/12) | [055] on both sides | Wire 055 to a node that joins the line running up the right-hand side of the drawing. |
| S | two parallel plates with a diagonal slash (normally-closed symbol), label `S` below | A9P7/J7 pin 11 (11/11) | [077] on both sides | Wire 077 to the same node as the other S contact. |
| T | two parallel plates with a diagonal slash (normally-closed symbol), label `T` above | A9P7/J7 pin 1 (1/1) | [066] | Wire 066 (6.3V AC, pin 1) to the node joining the two [788] wires of A9P7/J7 pins 2 and 3 (section 8). |
| A | two parallel plates (normally-open symbol), label `A`, bottom right of the page | none | none | The common bus of the Playboard Light Show / Glass Stop lamps (which also takes wire [666] from A9P8/J8 pin 11) to the long horizontal line along the bottom of the drawing. |

Wire [077] is also the line that runs from the node joining the outputs of fuses F13 and F14 up to A9P7/J7 pin 11 (section 4).

## 2. Transistor driver board 1A16 (MA-1104): solenoids 7, 4 and 3

Inputs come from connector `A3J6` into `1A16J1/P1`; outputs leave on `1A16P1/J1`.

| Solenoid (printed) | A3J6 pin | Wire | 1A16J1/P1 pin | Transistor | Base resistor | Resistor on emitter side | 1A16P1/J1 pin | Output wire | Load |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOLENOID 7 | 1 | [633] | 2 | Q1, MJ2955 DRIVER | R2 4.7K 1/4W | R3 8 ohm, 5W WW | 3 | [377] | LEFT SIDE lamp, #67 |
| SOLENOID 4 | 2 | [644] | 4 | Q2, MJ2955 DRIVER | R5 4.7K 1/4W | R6 8 ohm, 5W WW | 5 | [588] | RIGHT SIDE lamp, #67 |
| SOLENOID 3 | 3 | [655] | 9 | Q3, MJ2955 DRIVER | R8 4.7K 1/4W | none drawn | 10 | [033] | STARGATE lamps (below) |

Other 1A16P1/J1 pins: pin 1 = wire [9] with the arrow label `GROUND FROM 1A18J2-4`; pin 7 = wire [222]. The Left Side and Right Side lamps are each one `#67` bulb, drawn between the transistor output wire and the heavy vertical line carrying the arrow label `+24V DC` (wire box [222] at the top of that line).

### Stargate lamps (solenoid 3 circuit)

- Wire [033] from 1A16P1/J1 pin 10 goes to `A19J3/P3` pin 2 (2/2), then to a node that has diode **D9** (arrow pointing towards A19P3/J3 pin 1) and diode **D10** (arrow pointing from A19P3/J3 pin 3 towards the node) connected to it. Connector `A19P3/J3`: pins 1 and 3 (1/1, 3/3).
- A19P3/J3 pin 1 feeds two lamps labelled `STARGATE`, both `#67`, drawn in parallel (one on a loop line above, one on the main line). A small box `[700]` with an arrow points at the left node of the lower lamp.
- The right-hand node of the lamps continues as wire [044] to `A13J1/P1` pin 5 (R5, section 5).
- A19P3/J3 pin 3 leaves as wire [055], which runs right and down the page to A13J1/P1 pin 7 (section 5), A9P7/J7 pin 12 (S contact, section 1) and the left end of the Hole coil (section 4).

## 3. A3J4 solenoids 1, 2, 5, 6, 9 and the A19 switching diode board (MA-1102, D1-D10)

A3J4 pins and wires as printed:

| Printed | A3J4 pin | Wire |
| --- | --- | --- |
| SOLENOID 1 | 7 | [266] |
| SOLENOID 2 | 13 | [200] |
| SOLENOID 5 | 6 | [211] |
| SOLENOID 6 | 12 | [233] |
| SOLENOID 9 | 8 | [244] |

Connectors on the A19 board: `A19J1/P1` pins 2 and 5; `A19J2/P2` pins 2 and 5; `A19P1/J1` pins 1, 4 (upper pair) and 3, 6 (lower pair); `A19P2/J2` pins 1, 4 (upper pair) and 3, 6 (lower pair). A hand-drawn curved arrow from the title `A19 SWITCHING DIODE BOARD MA-1102, D1-D10` points at D2. D2 and D4 are enclosed in grey highlight boxes and the solenoid 2 line down to D4 is overdrawn with a grey stroke (marks on the scan, not part of the printed drawing).

Each solenoid line (A19J1/P1 or A19J2/P2, pin 2 or 5) splits into two diodes, all with the arrow pointing away from the solenoid line:

| Solenoid (A3J4 pin, wire) | A19 in-pin | Diode | Out pin / wire | Load | Diode | Out pin / wire | Load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (A3J4-7, [266]) | A19J1/P1 pin 2 | D1 | A19P1/J1 pin 1, [400] | LEFT TOP DOME lamp | D2 | A19P1/J1 pin 3, [088] | 1 BANK RESET coil |
| 2 (A3J4-13, [200]) | A19J1/P1 pin 5 | D3 | A19P1/J1 pin 4, [411] | LEFT CENTER DOME lamp | D4 | A19P1/J1 pin 6, [288] | 2 BANK RESET coil |
| 5 (A3J4-6, [211]) | A19J2/P2 pin 2 | D5 | A19P2/J2 pin 1, [422] | LEFT BOTTOM DOME lamp | D6 | A19P2/J2 pin 3, [588] | 3 BANK RESET coil |
| 6 (A3J4-12, [233]) | A19J2/P2 pin 5 | D7 | A19P2/J2 pin 4, [866] | RIGHT TOP DOME lamp | D8 | A19P2/J2 pin 6, [888] | 4 BANK RESET coil |

(Which lower diode belongs to which solenoid line is read from the nested routing lines; see Uncertain readings 2.)

### Dome lamps

| Printed lamp | Wire from A19 | Connector A9P9/J9 | Lamp | Wire after lamp | Connector A9J9/P9 | A13 pin |
| --- | --- | --- | --- | --- | --- | --- |
| LEFT TOP DOME | [400] | pin 1 (1/1), [400] | #67 | [811] | pin 2 (2/2), [811] | A13J1/P1 pin 1 (R1) |
| LEFT CENTER DOME | [411] | pin 3 (3/3), [411] | #67 | [833] | pin 4 (4/4), [833] | A13J1/P1 pin 2 (R2) |
| LEFT BOTTOM DOME | [422] | pin 5 (5/5), [422] | #67 | [855] | pin 6 (6/6), [855] | A13J1/P1 pin 3 (R3) |
| RIGHT TOP DOME | [866] | none drawn | #67 | [877] | none drawn | A13J1/P1 pin 4 (R4) |

## 4. Coils fed through fuses

Every coil below is drawn with a diode across it.

| Printed label | Coil part | Left end | Right end | Fuse | Notes as drawn |
| --- | --- | --- | --- | --- | --- |
| HOLE | 5195 | [055] (no connector drawn); this 055 line also goes to A19P3/J3 pin 3, A13J1/P1 pin 7 and A9P7/J7 pin 12 | [488] (no connector drawn) | F13, 1 AMP, SLO-BLO | No solenoid number is printed on the Hole coil. Its right end [488] joins the F13 input node together with the 1 BANK RESET right end. |
| 1 BANK RESET | 5195 | [088], from A19P1/J1 pin 3 via A9P6/J6 pin 3 (3/3) | [488], via A9J6/P6 pin 4 (4/4) | F13, 1 AMP, SLO-BLO | fed from solenoid 1 via D2 |
| 2 BANK RESET | 19300 | [288], from A19P1/J1 pin 6 via A9P5/J5 pin 4 (4/4) | [188], via A9J5/P5 pin 5 (5/5) | F14, 2 AMP, SLO-BLO | fed from solenoid 2 via D4 |
| 3 BANK RESET | 19300 | [588], from A19P2/J2 pin 3 via A9P4/J4 pin 5 (5/5) | [188], via A9J4/P4 pin 6 (6/6) | F14, 2 AMP, SLO-BLO | fed from solenoid 5 via D6 |
| 4 BANK RESET | 5194 | [888], from A19P2/J2 pin 6 via A9P3/J3 pin 6 (6/6) | [188], via A9J3/P3 pin 7 (7/7) | F14, 2 AMP, SLO-BLO | fed from solenoid 6 via D8 |
| OUTHOLE | 5195 | the line `244 SOLENOID 9` (A3J4 pin 8), straight to the coil | [888] (no connector drawn) | F12, 1 AMP, SLO-BLO | no A19 diodes, no connectors |

Fuse outputs as drawn: the outputs of F13 and F14 are joined (dot) and that line runs up and right as wire [077] to A9P7/J7 pin 11 (the normally-closed S contact). The outputs of F12 and F11 join, together with the [222] line from 2A16P1/J1 pin 7, one vertical line at the left of the `FROM AUX. LAMP DRIVER MA-866` block; that line continues up the page and down to the 222 / +24V line (see Uncertain readings 1). F10 output joins the same vertical line.

## 5. A13 Resistor board (MA-1101)

Connector `A13J1/P1` (pin numbers printed 5/5, 1/1, 2/2, 3/3, 4/4, 7/7).

| Pin | Wire (outside) | Resistor | Value |
| --- | --- | --- | --- |
| 5 | [044] | R5 | 4 ohm, 7W, WW |
| 1 | [811] | R1 | 8 ohm, 5W, WW |
| 2 | [833] | R2 | 8 ohm, 5W, WW |
| 3 | [855] | R3 | 8 ohm, 5W, WW |
| 4 | [877] | R4 | 8 ohm, 5W, WW |
| 7 | [055] | none (inside the board the pin 7 line joins the common right-hand ends of R1-R5) | - |

Wire [055] runs from pin 7 to A9P7/J7 pin 12 (S normally-open contact) and A19P3/J3 pin 3.

## 6. Transistor driver board 2A16 (MA-1079): Ball Release and Stargate Ramp

Input connector `2A16J1/P1`; output connector `2A16P1/J1`.

| Input source (printed) | Connector pin | Name | Wire | 2A16J1/P1 pin | Transistor | Base resistor | 2A16P1/J1 pin | Output wire | Load |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FROM BOTTOM CABINET | A9P1 pin 6 | L2 | [877] | 2 | Q1, MJ2955 DRIVER | R2 4.7K 1/4W | 3 | [266] | BALL RELEASE coil 16570 |
| OUTPUT FROM A3 MASTER DRIVER BOARD | A3J3 pin 22 | L14 | [100] | 9 | Q3, 2N5879 DRIVER | R8 4.7K 1/4W | 10 | [244] | STARGATE RAMP coil 17875 |

- 2A16P1/J1 pin 7 = wire [222]; pin 1 = wire [9] with the arrow label `GROUND FROM 1A18J2-5`.
- BALL RELEASE: coil 16570 with diode across; left end [266], right end [288] to `F11, 1 AMP, SLO-BLO`.
- STARGATE RAMP: coil 17875 with diode across; left end [244], right end [277] to `F10, 2.5AMP, SLO-BLO`. Below the coil a contact labelled `ON RAMP SW.` (parallel plates with a diagonal slash, normally-closed symbol) is connected between a tap at the centre of the coil symbol and the coil's right-hand end.

## 7. Playboard Light Show and Glass Stop (from the aux lamp driver MA-866)

Connector `1A11J2` (label `FROM AUX. LAMP DRIVER MA-866`):

| 1A11J2 pin | Wire |
| --- | --- |
| 1 | [400] |
| 2 | [411] |
| 3 | [422] |
| 4 | [433] |
| 5 | [444] |
| 6 | [455] |
| 7 | [466] |
| 8 | [477] |
| 9 | [600] |
| 10 | [611] |

### PLAYBOARD LIGHT SHOW (dashed box)

Each wire from 1A11J2 feeds one row of two bulbs drawn in parallel (one on a loop line above the main line) between the wire and a common vertical bus at the right of the box. Row labels, top to bottom: `#1`, `#2`, `#3`, `#4`, `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, on wires 400, 411, 422, 433, 444, 455, 466, 477, 600, 611 respectively (see Uncertain readings 3).

### GLASS STOP (dashed box), connector `A9P8/J8`

| A9P8/J8 pin | Wire (both halves) | Label next to the bulb |
| --- | --- | --- |
| 1 | [400] | #1 |
| 2 | [411] | #3 |
| 3 | [422] | #5 |
| 4 | [433] | #7 |
| 5 | [444] | #9 |
| 6 | [455] | #10 |
| 7 | [466] | #8 |
| 8 | [477] | #6 |
| 9 | [600] | #4 |
| 10 | [611] | #2 |
| 11 | [666] | no bulb; the right-hand [666] line joins the bus at the right of the box |

One bulb per pin 1-10. The left-hand wires of A9P8/J8 connect by vertical drops to the 1A11J2 wires of the same colour code. Left-hand [666] (pin 11) runs round under the Glass Stop box to the node above contact `A` (section 1).

## 8. Power inputs and playboard illumination

`A12P1` (bracket label `FROM TRANSFORMER PANEL`):

| A12P1 pin | Wire | Label |
| --- | --- | --- |
| 3 | [222] | +24V DC |
| 2 | [066] | 6.3V AC |
| 1 | [000] | 6.3V AC RETURN |
| 4 | [255] | +6V DC |

PLAYBOARD ILLUMINATION: one solid bulb drawn between the [066] line and the [000] line, with two further bulbs drawn with dashed outlines (above and below it) inside a dashed bracket. Connector `A9P7/J7`: pin 1 (1/1) = [066] on the left, [066] on the right going to the `T` contact; pins 2 (2/2) and 3 (3/3) = [788] on the right, joined to one node that is the other side of contact T; on the left, pins 2 and 3 are joined to the [000] return line. The [222] +24V DC line from A12P1 pin 3 runs right and turns up the page at the right of the 2A16 block; the [255] +6V DC line runs off to the right.

## 9. Title block

None printed on page 41. (The title block `Premier Technology / PLAYBOARD SOLENOIDS AND ILLUMINATION / E-25887, APR-2-88` is on page 42.)

## Counts

- Relay coils: 4 (S, T, Q, A). Contacts drawn: S x2 (one normally-open symbol on 055, one normally-closed symbol on 077), Q x1, T x1, A x1.
- Numbered solenoids: 8 (1, 2, 3, 4, 5, 6, 7, 9). Coils driven from lamp-driver outputs L2 and L14: 2 (Ball Release, Stargate Ramp). Coil with no solenoid number: Hole.
- Coils: Hole, 1/2/3/4 Bank Reset, Outhole, Ball Release, Stargate Ramp = 8.
- Fuses: F10 (2.5 AMP), F11 (1 AMP), F12 (1 AMP), F13 (1 AMP), F14 (2 AMP), all SLO-BLO.
- Diodes D1-D10 on the A19 board (D9 and D10 beside A19P3/J3).
- Solenoid number 8 is not printed anywhere on this page.

## Uncertain readings

1. The +24V rail at the right of the drawing is drawn as two nested rectangles. I could not trace every junction with certainty: the node after the S contacts appears to feed the outer line going up the right side; the wire box [222] with the arrow `+24V DC` starts the inner line; the long line along the very bottom of the page ends at contact A. I state only the connections listed in the tables.
2. Which of D2, D4, D6, D8 follows which solenoid was read from the nested routing lines (outermost line to D8, innermost to D2); the grey overdraw on the solenoid 2 line agrees with solenoid 2 to D4.
3. The Light Show rows are labelled `#1`..`#10` with the same `#` mark used for `#44` and `#67`; it is unclear whether these are bulb types or row numbers.
4. Diode arrow directions across the coils were not transcribed except for D1-D10 on the A19 board and D9/D10.
5. The contact `A` is shown after a node tied to wire [666]; the identity of the line it connects to at the bottom of the page is not labelled.
