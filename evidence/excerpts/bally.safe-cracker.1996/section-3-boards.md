# Safe Cracker - Section 3 Boards: flipper circuits, opto boards and target boards (PDF pages 135-144 and 147)

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf` (158-page scan, Bally/Midway "Safe Cracker", 1996). Each heading below is one PDF page and
carries its printed title and printed folio (read at the page bottom). PDF pages 145 and 146 are not transcribed here. Read from the rendered page
(300 dpi scan), not from the OCR text.

| PDF page | Printed folio | Printed title | Content transcribed |
| --- | --- | --- | --- |
| 135 | 3-11 | FLIPPER CIRCUIT DIAGRAM | whole page (drawing labels) |
| 136 | 3-12 | FLIPPER COIL CIRCUITS; FLIPPER END-OF-STROKE SWITCH CIRCUIT | whole page (drawing labels and text) |
| 137 | 3-13 | FLIPPER CABINET SWITCH CIRCUITS | whole page (drawing labels and text) |
| 138 | 3-14 | LED P.C.B. Assembly (transmitter) A-16908; Photo Transistor P.C.B. Assembly (receiver) A-16909 | whole page |
| 139 | 3-15 | Flipper Opto P.C.B. Assembly A-17316 | whole page (pin lists, drawing labels) |
| 140 | 3-16 | TROUGH IRED LED P.C.B. ASSEMBLY A-18617-1 | whole page (pin list, drawing labels) |
| 141 | 3-17 | TROUGH IRED TRANSISTOR P.C.B. ASSEMBLY A-18618-1 | whole page (pin list, drawing labels) |
| 142 | 3-18 | 10 OPTO P.C.B. A-18159 | whole page (pin lists, board drawing) |
| 143 | 3-19 | 10 OPTO P.C.B. (Circuit Diagram; Schematic) | whole page (drawing labels) |
| 144 | 3-20 | 3 OPTO VARI TARGET P.C.B. ASSEMBLY A-20906 | whole page (pin list, drawing labels) |
| 147 | 3-23 | SPIN DISC OPTO P.C.B. A-20952 | whole page (pin list, drawing labels) |

Conventions: wire colours and spellings are as printed on each page (this manual spells them out in full on these pages: `Gray-Yellow`, `Orange-Black`,
`BLUE-VIOLET`). A line of printed text is given in a code span. Where a drawing is described, labels are listed in the order printed, grouped as printed.
Arrows and routing of wires that I traced rather than read as a printed word are marked `(traced)`.

## Opto summary tied together by these pages

Only printed ties are listed (a switch number printed on the page against a board position). Rows and columns are not printed as numbers on the opto
boards themselves; the only printed matrix wires on these pages are the `Sw. Row` and `Sw. Col.` wires of PDF page 143 and the connector pin lists on PDF
pages 144 and 147.

| Switch | Board | Position / pins printed |
| --- | --- | --- |
| `F2` `L. RIGHT FLIPPER` | Right flipper cabinet opto board A-17316 | `J1-2 Blue-Violet from CPU Bd. J212-12` (135 `U25A-1`; 137 right board pin 2) |
| `F4` `L. LEFT FLIPPER` | Left flipper cabinet opto board A-17316 | `J1-2 Blue-Gray from CPU Bd. J212-11` (135 `U25B-2`; 137 left board pin 2) |
| `F6` `U. RIGHT FLIPPER` | Right flipper cabinet opto board A-17316 | `J1-1 Black-Yellow from CPU Bd. J212-10` (135 `U25C-14`) |
| `F8` `U. LEFT FLIPPER` | Left flipper cabinet opto board A-17316 | pin 1 `BLACK-BLUE` on page 137 and 135 (`U25D-13`, `J212-9`); but page 139 prints left `J1-1 Not Used` |
| `F1`, `F3`, `F5`, `F7` | End-of-stroke switches (not optos) | page 135 only: `U26A-1`, `U26B-2`, `U26C-14`, `U26D-13` on `J208-13`, `-12`, `-11`, `-10` |
| `Sw #31` | 10 Opto P.C.B. A-18159 opto 1 | `J1-7 Gray-Brown` (LED) / `J2-8 Orange-Brown` (photo); trough boards A-18617-1 `J1-7`, A-18618-1 `J1-3` |
| `Sw #32` | 10 Opto P.C.B. opto 2 | `J1-6 Gray-Red` / `J2-7 Orange-Red`; trough LED `J1-6`, photo `J1-4` |
| `Sw #33` | 10 Opto P.C.B. opto 3 | `J1-5 Gray-Orange` / `J2-5 Orange-Black`; trough LED `J1-5`, photo `J1-5` |
| `Sw #34` | 10 Opto P.C.B. opto 4 | `J1-4 Gray-Black` / `J2-4 Orange-Yellow`; trough LED `J1-4`, photo `J1-6` |
| `Sw #35` | 10 Opto P.C.B. opto 5 | `J1-3 Gray-Green` / `J2-3 Orange-Green`; trough LED `J1-3`, photo `J1-7` |
| `Sw #36` | 10 Opto P.C.B. opto 6 | `J1-2 Gray-Blue` to A-16908 (LED) / `J2-2 Orange-Blue` to A-16909 (Trans.) |
| `Sw #37` | 10 Opto P.C.B. opto 7 | `J1-1 Gray-Violet` to A-16908 (LED) / `J2-1 Orange-Violet` to A-16909 (Trans.) |
| `Sw #41` | 10 Opto P.C.B. opto 8 (schematic label `J6 OPTO 8`) | `J6-1 Gray-Brown` (LED) / `J6-5 Orange-Brown` (Trans.) |
| `Sw #42` | 10 Opto P.C.B. opto 9 (schematic label `J5 OPTO 9`) | `J5-1 Gray-Red` (LED) / `J5-5 Orange-Red` (Trans.) |
| `Sw #43` | 10 Opto P.C.B. opto 10 (schematic label `J4 OPTO 10`) | `J4-1 Gray-Orange` (LED) / `J4-5 Orange-Black` (Trans.) |
| `Sw #85` | wire `White-Green`, `J208-5`, `J1-5` | printed on both the 3 Opto Vari Target page (144) and the Spin Disc Opto page (147) circuit boxes |
| `Sw #86` | wire `White-Blue`, `J208-7`, `J1-6` | printed on page 144 circuit box labelled Spin Disc Opto P.C.B. A-20952 |
| `Sw #57` | wire `White-Violet`, `J208-7`, `J1-6` | printed on page 147 circuit box (page 147's own pin list says `J1-6 White-Blue from J208-7`) |

No page of this range prints a switch name (such as `TROUGH EJECT`) against an opto; the switch names are `L. RIGHT FLIPPER`, `L. LEFT FLIPPER`,
`U. RIGHT FLIPPER`, `U. LEFT FLIPPER` on pages 135-137 only.

## PDF page 135 - printed title `FLIPPER CIRCUIT DIAGRAM`, folio `3-11`

Whole page: a drawing with the Power Driver Board (connectors `J119`, `J120`, `J139`, `J102`) above and the CPU Board (`J211`, `J212`, `J208`) below.
A footnote at the bottom: `*NOTE: May be used as circuits other than flipper circuits.`

Wires from `J119` (pins drawn `8 6 4 1`, left to right), printed above the drawing, outermost first (the wire from pin 8 is the outermost line):

| J119 pin | Printed wire | Goes to (traced) |
| --- | --- | --- |
| 8 | `RED-GRAY +50V` | `*UPPER LEFT FLIPPER COIL` |
| 6 | `RED-VIOLET +50V` | `*UPPER RIGHT FLIPPER COIL` |
| 4 | `RED-BLUE +50V` | `LOWER LEFT FLIPPER COIL` |
| 1 | `RED-GREEN +50V` | `LOWER RIGHT FLIPPER COIL` |

Coil drive section, `J120` (pins drawn down the left of the connector: 13, 11, 9, 7, 6, 4, 3, 1), each coil drawn with two diodes and two windings:

| Coil title as printed | J120 pin | Wire | Label | Transistor |
| --- | --- | --- | --- | --- |
| `LOWER RIGHT FLIPPER COIL` | 13 | `YELLOW-GREEN` | `POWER` | `Q90` |
| `LOWER RIGHT FLIPPER COIL` | 11 | `ORANGE-GREEN` | `HOLD` | `Q92` |
| `LOWER LEFT FLIPPER COIL` | 9 | `YELLOW-BLUE` | `POWER` | `Q87` |
| `LOWER LEFT FLIPPER COIL` | 7 | `ORANGE-BLUE` | `HOLD` | `Q89` |
| `*UPPER RIGHT FLIPPER COIL` | 6 | `YELLOW-VIOLET` | `POWER` | `Q84` |
| `*UPPER RIGHT FLIPPER COIL` | 4 | `ORANGE-VIOLET` | `HOLD` | `Q86` |
| `*UPPER LEFT FLIPPER COIL` | 3 | `YELLOW-GRAY` | `POWER` | `Q81` |
| `*UPPER LEFT FLIPPER COIL` | 1 | `ORANGE-GRAY` | `HOLD` | `Q83` |

(The asterisk is printed in front of the two upper coil titles and refers to the footnote `*NOTE: May be used as circuits other than flipper circuits.`)

`J139` pin `2`: `GRAY-YELLOW +12V`, running to the box `FLIPPER OPTO BOARDS` at the right of the CPU section.

`J102` (Power Driver Board) is drawn as a ribbon cable to `J211` (CPU Board).

`CABINET OPTO SWITCHES`, CPU Board `J212` (pin 13 has a ground symbol):

| J212 pin | Wire | Label | Switch | IC pin |
| --- | --- | --- | --- | --- |
| 13 | `ORANGE` | `GROUND` | (blank) | (blank) |
| 12 | `BLUE-VIOLET` | `L. RIGHT FLIPPER` | `F2` | `U25A-1` |
| 11 | `BLUE-GRAY` | `L. LEFT FLIPPER` | `F4` | `U25B-2` |
| 10 | `BLACK-YELLOW` | `U. RIGHT FLIPPER` | `F6` | `U25C-14` |
| 9 | `BLACK-BLUE` | `U. LEFT FLIPPER` | `F8` | `U25D-13` |

These lines run to the box `FLIPPER OPTO BOARDS`.

`END-OF-STROKE SWITCHES`, CPU Board `J208` (pin 14 has a ground symbol); each of the four lines ends at a drawn switch contact, and the four contacts share a common line returning to the `ORANGE` ground:

| J208 pin | Wire | Label | Switch | IC pin |
| --- | --- | --- | --- | --- |
| 14 | `ORANGE` | `GROUND` | (blank) | (blank) |
| 13 | `BLACK-GREEN` | `L. RIGHT FLIPPER` | `F1` | `U26A-1` |
| 12 | `BLACK-BLUE` | `L. LEFT FLIPPER` | `F3` | `U26B-2` |
| 11 | `BLACK-VIOLET` | `U. RIGHT FLIPPER` | `F5` | `U26C-14` |
| 10 | `BLACK-GRAY` | `U. LEFT FLIPPER` | `F7` | `U26D-13` |

Notes: the `J212` pin 9 wire is `BLACK-BLUE` and the `J208` pin 12 wire is also `BLACK-BLUE` (two different connectors, same colour name). The page prints no
`BASKET`, `SHOOT` or other alternate names for these circuits; only the footnote about use as circuits other than flipper circuits, attached to the two upper coil titles.

## PDF page 136 - printed title `FLIPPER COIL CIRCUITS` (and `FLIPPER END-OF-STROKE SWITCH CIRCUIT`), folio `3-12`

Two circuit drawings side by side, then the end-of-stroke circuit and its text.

### `LEFT FLIPPER CIRCUIT` (left drawing)

`POWER DRIVER BOARD` box: connector `J128` (pins drawn `9`, `8`, `6`, `5`), fuse `F108`, bridge `D22`, `D20`, `D19`, `D21` with `all P600D` printed inside the
bridge (the last character looks like `D`; the scan shows `P600D`), `+` and `-` marks, two capacitors `100mf 100V`, a resistor `10K 1W` feeding an `LED`, fuses `F116` and `F117`.
`J119` pins drawn `4`, `5` (towards `F116`) and `8`, `9` (towards `F117`); wires leaving to the playfield: `RED-BLUE` (from the 4/5 pair) and `RED-GRAY` (from the 8/9 pair).
`PLAYFIELD` label at the right. `J120`:

| J120 pin | Wire | Role printed | Coil title printed at the right |
| --- | --- | --- | --- |
| 9 | `YELLOW-BLUE` | `POWER` | `LOWER LEFT FLIPPER` |
| 7 | `ORANGE-BLUE` | `HOLD` | `LOWER LEFT FLIPPER` |
| 3 | `YELLOW-GRAY` | `POWER` | `UPPER LEFT FLIPPER` |
| 1 | `ORANGE-GRAY` | `HOLD` | `UPPER LEFT FLIPPER` |

`RED-BLUE` goes to the `LOWER LEFT FLIPPER` coil and `RED-GRAY` to the `UPPER LEFT FLIPPER` coil (traced). `J102` is drawn at the bottom of the Power Driver Board,
joined to `J211` on the `CPU BOARD` box below.

`CPU BOARD` box, `J212` and the box `LEFT CABINET OPTO BOARD` with `J1`:

| J212 pin | Label | Wire |
| --- | --- | --- |
| 13 | `GROUND` | `ORANGE` |
| 11 | `F4  LOWER` | `BLUE-GRAY` |
| 9 | `F8  UPPER` | `BLACK-BLUE` |

The three wires go to a small connector column drawn with pins `6`, `7`, `3`, `4`, `1`, `2` (top to bottom) and then to the `J1` of the `LEFT CABINET OPTO BOARD`, which is drawn with pins `6`, `7`, `3`, `4`, `1`, `2`
with small jumper loops beside `6`/`7` and `3`/`4`. (The ground, `F4` and `F8` wires meet the column at `7`, `4`, `2`; as drawn the line from `J212-13` enters at the `7`/`3` side. The pin
arrangement of this reprint differs from page 137, see the comparison below; read the pin numbers of this small drawing as `[?]`.)

`J208` section: `J208` pin `12` `BLACK-BLUE` to a switch labelled `LOWER LEFT E.O.S. SWITCH`; pin `14` `ORANGE` (ground symbol at the left) is the return for both switches;
pin `10` `BLACK-GRAY` to a switch labelled `UPPER LEFT E.O.S. SWITCH`; a second `ORANGE` label sits under the upper switch.

### `RIGHT FLIPPER CIRCUIT` (right drawing)

Same power section: `J128` pins `9`, `8`, `6`, `5`, fuse `F108`, `D22`, `D20`, `D19`, `D21` (`all P600D`), `100mf 100V` capacitors, `10K 1W`, `LED`, fuses `F115` (towards `J119` pins `1`, `2`) and
`F118` (towards `J119` pins `6`, `7`). Wires to the playfield: `RED-GREEN` (from `J119` 1/2) and `RED-VIOLET` (from `J119` 6/7). `J120`:

| J120 pin | Wire | Role printed | Coil title printed at the right |
| --- | --- | --- | --- |
| 12 | `YELLOW-GREEN` | `POWER` | `LOWER RIGHT FLIPPER` |
| 11 | `ORANGE-GREEN` | `HOLD` | `LOWER RIGHT FLIPPER` |
| 6 | `YELLOW-VIOLET` | `POWER` | `UPPER RIGHT FLIPPER` |
| 4 | `ORANGE-VIOLET` | `HOLD` | `UPPER RIGHT FLIPPER` |

`RED-GREEN` goes to the `LOWER RIGHT FLIPPER` coil and `RED-VIOLET` to the `UPPER RIGHT FLIPPER` coil (traced).

`CPU BOARD`, `J212` and the box `RIGHT CABINET OPTO BOARD` with `J1`:

| J212 pin | Label | Wire |
| --- | --- | --- |
| 13 | `GROUND` | `ORANGE` |
| 12 | `F2  LOWER` | `BLUE-VIOLET` |
| 10 | `F6  UPPER` | `BLACK-YELLOW` |

The `J1` of the `RIGHT CABINET OPTO BOARD` is drawn with pins `6`, `7`, `3`, `4`, `1`, `2` with jumper loops beside `6`/`7` and `3`/`4`, joined by a small connector column `6`, `7`, `3`, `4`, `1`, `2`.
`J208` section: pin `13` `BLACK-GREEN` to `LOWER RIGHT E.O.S. SWITCH`; pin `14` `ORANGE` (ground) common; pin `11` `BLACK-VIOLET` to `UPPER RIGHT E.O.S. SWITCH`; a second `ORANGE` label sits under the upper switch.

Note: this page names the `J208` pin 10/11 switches `UPPER LEFT E.O.S. SWITCH` and `UPPER RIGHT E.O.S. SWITCH`, matching the `U. LEFT FLIPPER F7` / `U. RIGHT FLIPPER F5` labels
of page 135 (which carry the asterisk footnote). This page prints no asterisk.

### `FLIPPER END-OF-STROKE SWITCH CIRCUIT`

Drawing inside a dashed box labelled `Dedicated Input` and `CPU BOARD`: `HCT244`, `10K` to `+5V`, `LM339` with points `A` and `B`, `1K` in series, `1K` to `+12V`, `470pf` to ground, `1N4148`,
connector `J208` with pin `X` and pin `14`; outside the box `BLACK--XXX` through a switch to `PLAYFIELD`, and `ORANGE` from pin `14`. Truth table, printed:

| SWITCH | A | B | (state) |
| --- | --- | --- | --- |
| OPEN | H | H | OFF |
| CLOSED | L | L | ON |

Text, verbatim:

`The flipper E.O.S. circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch. When a switch closes, the row side, (dedicated input), of the circuit activates. The "+" input of the LM339 drops below +5V therefore its output is low. Since the row (dedicated input), circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row (dedicated input) is inactive.`

## PDF page 137 - printed title `FLIPPER CABINET SWITCH CIRCUITS`, folio `3-13`

Top drawing: `LEFT CABINET OPTO BOARD` (`J1`) and `RIGHT CABINET OPTO BOARD` (`J1`), each with a board connector and a harness connector column, `POWER DRIVER BOARD` (`J139` pin `2`), `CPU BOARD` (`J212`).

Left board `J1` pins as drawn: `7`, `6`, `4`, `2`, `1` (a jumper loop joins `7` and `6` on the board). Right board `J1` pins as drawn: `6`, `4`, `3`, `2`, `1` (a jumper loop joins `4` and `3`).
Harness columns repeat the same pin numbers (`7 6 4 2 1` left, `6 4 3 2 1` right).

| Wire printed | Label printed | Switch | Left board pin | Right board pin | CPU / other end |
| --- | --- | --- | --- | --- | --- |
| `GRAY-YELLOW +12V` | (none) | (none) | 7 | (none) | `J139` pin 2 (Power Driver Board) |
| (unlabelled wire) | (none) | (none) | 6 | 6 | joins left 6 to right 6 (traced) |
| (unlabelled wire) | (none) | (none) | 4 | 4 | joins left 4 to right 4 (traced) |
| `BLUE-GRAY` | `L. LEFT FLIPPER` | `F4` | 2 | (none) | `J212` pin 11 |
| `BLACK-BLUE` | `U. LEFT FLIPPER` | `F8` | 1 | (none) | `J212` pin 9 |
| `ORANGE` | `GROUND` | (none) | (none) | 3 | `J212` pin 13 |
| `BLUE-VIOLET` | `L. RIGHT FLIPPER` | `F2` | (none) | 2 | `J212` pin 12 |
| `BLACK-YELLOW` | `U. RIGHT FLIPPER` | `F6` | (none) | 1 | `J212` pin 10 |

Lower drawing: `Dedicated Input` dashed box with `HCT244`, `10K` to `+5V`, `LM339` (points `A` and `B`), `1K`, `1K` to `+12V`, `470pf`, `1N4148`, `J212` pin `X` (wire labelled `BLUE-XXX` / `BLACK-XXX`) and pin `13` (`ORANGE`),
`CPU BOARD`; `POWER DRIVER BOARD` with `J139` pin `2` (`+12Vo`, wire `GRAY-YELLOW`); box `FLIPPER OPTO BOARD` with `J1` pins `X`, `3`, `7`, a phototransistor and LED symbol (optocoupler) and a `470` resistor between pin `7` and the LED.

Text, verbatim:

`The flipper switch circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch circuit.`

`When a switch closes, the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V, therefore, its output is low. Since the row, (dedicated input) circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row, (dedicated Input) is inactive.`

## PDF page 138 - printed title `LED P.C.B. Assembly (transmitter)` `A-16908` and `Photo Transistor P.C.B. Assembly (receiver)` `A-16909`, folio `3-14`

No pin lists. Two part drawings.

`LED P.C.B. Assembly (transmitter) A-16908`: assembly drawing labels `Green` (board top), `WHT` (side view), `A` and `K` (pads), `SOLDER`, wire labels `Gray` (left lead) and `Black` (right lead). Three views:
`solder side` (labels `A`, `K`), `schematic` (LED symbol, `A` and `K`), `component side` (labels `K` at left and `A` at right of the round part).

`Photo Transistor P.C.B. Assembly (receiver) A-16909`: assembly drawing labels `BLK` (side view), `Blue` (board top), `C` and `E` (pads), `SOLDER`, wire labels `Gray-Yellow` (left lead) and `Orange-XXX` (right lead). Three views:
`solder side` (`C`, `E`), `schematic` (phototransistor symbol, `C` at left, `E` at right), `component side` (`E` at left, `C` at right).

## PDF page 139 - printed title `Flipper Opto P.C.B. Assembly` `A-17316`, folio `3-15`

Board drawing: `OPTO 1`, `OPTO 2`, `R1`, `R2`, and `J1` with the pin legend printed beside it from pin 1 (top) to pin 7 (bottom): `SW1`, `SW2`, `GND`, `GND`, `KEY`, `+12VDC`, `+12VDC` (the number `1` is printed above the connector and `7` below it).

Schematic: `R1` `470` ohm (printed `470` with an ohm sign) and `R2` `470` ohm, each in series with the LED of `OPTO1` and `OPTO2`; `J1` pins: `7` `+12VDC`, `6` `+12VDC`, `5` `KEY`, `1` `SW1`, `2` `SW2`, `3` `GND`, `4` `GND`.
The `OPTO1` phototransistor goes to `SW1` (pin 1) and the `OPTO2` phototransistor to `SW2` (pin 2) (traced).

Pin lists, printed as two columns:

| Left Side Flipper Cabinet Opto Switch Board | Right Side Flipper Cabinet Opto Switch Board |
| --- | --- |
| `J1-1 Not Used` | `J1-1 Black-Yellow from CPU Bd. J212-10` |
| `J1-2 Blue-Gray from CPU Bd. J212-11` | `J1-2 Blue-Violet from CPU Bd. J212-12` |
| `J1-3 Orange from Coin Door Interface Bd. J13-1` | `J1-3 Orange to/from Left Flipper Opto Bd. J1-4` |
| `J1-4 Orange to/from Right Flipper Opto Bd. J1-3` | `J1-4 Orange from CPU Bd. J212-13` |
| `J1-5 Key` | `J1-5 Key` |
| `J1-6 Gray-Yellow to/from Right Flipper Opto Bd. J1-6` | `J1-6 Gray-Yellow to/from Left Flipper Opto J1-6` |
| `J1-7 Gray-Yellow from Power Driver Bd. J139-2` | `J1-7 Not Used` |

Note: the printed header for the left list is `Left Side Flipper Cabinet Opto Switch Board` and for the right `Right Side Flipper Cabinet Opto Switch Board`. The right list prints `Left Flipper Opto J1-6` (no `Bd.`) in its `J1-6` line.

## PDF page 140 - printed title `TROUGH IRED LED P.C.B. ASSEMBLY` `A-18617-1`, folio `3-16`

Pin list, printed:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Not Used` |
| J1-2 | `J1-2 Not Used` |
| J1-3 | `J1-3 Gray-Green, from SW-10 Opto P.C.B. J1-3` |
| J1-4 | `J1-4 Gray-Black, from SW-10 Opto P.C.B. J1-4` |
| J1-5 | `J1-5 Gray-Orange, from SW-10 Opto P.C.B. J1-5` |
| J1-6 | `J1-6 Gray-Red, from SW-10 Opto P.C.B. J1-6` |
| J1-7 | `J1-7 Gray-Brown, from SW-10 Opto P.C.B. J1-7` |
| J1-8 | `J1-8 Key` |
| J1-9 | `J1-9 Black, from SW-7 Opto P.C.B. J1-9` |

(The list says `SW-10 Opto P.C.B.` for J1-3 to J1-7 and `SW-7 Opto P.C.B.` for J1-9; this is printed as such, compare the board named `10 OPTO P.C.B.` on PDF pages 142-143.)

Board drawing: outline with `LED1` at the upper left, `LED2`, `LED3`, `LED4`, `LED5` along the lower part, connector `J1` with pin numbers `9` (left) and `1` (right) printed at the ends and an asterisk mark at the pin next to 9 [?: asterisk is the key position]; three or four unlabelled round holes (mounting) also drawn.

Schematic, captioned `Trough 7 IRED Circuit`: five LEDs drawn, labelled `LED 5 (BALL 4)`, `LED 4 (BALL 3)`, `LED 3 (BALL 2)`, `LED 2 (BALL 1)`, `LED 1 (JAM BALL)`, all cathodes to a common line to `COMMON`. `J1` legend, pins 1-9 top to bottom:

| Pin | Printed signal |
| --- | --- |
| 1 | `NOT USED` |
| 2 | `NOT USED` |
| 3 | `BALL 4` |
| 4 | `BALL 3` |
| 5 | `BALL 2` |
| 6 | `BALL 1` |
| 7 | `JAM BALL` |
| 8 | `KEY` |
| 9 | `COMMON` |

Tie of LED label to pin (traced): `LED 5 (BALL 4)` to pin 3, `LED 4 (BALL 3)` to 4, `LED 3 (BALL 2)` to 5, `LED 2 (BALL 1)` to 6, `LED 1 (JAM BALL)` to 7.

## PDF page 141 - printed title `TROUGH IRED TRANSISTOR P.C.B. ASSEMBLY` `A-18618-1`, folio `3-17`

Pin list, printed:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow, from SW-10 Opto P.C.B. J2-9` |
| J1-2 | `J1-2 Key` |
| J1-3 | `J1-3 Orange-Brown, from SW-10 Opto P.C.B. J2-8` |
| J1-4 | `J1-4 Orange-Red, from SW-10 Opto P.C.B. J2-7` |
| J1-5 | `J1-5 Orange-Black, from SW-10 Opto P.C.B. J2-5` |
| J1-6 | `J1-6 Orange-Yellow, from SW-10 Opto P.C.B. J2-4` |
| J1-7 | `J1-7 Orange-Green, from SW-10 Opto P.C.B. J2-3` |
| J1-8 | `J1-8 Not Used` |
| J1-9 | `J1-9 Not Used` |

Board drawing: outline with `Q1` at the upper right, `Q2`, `Q3`, `Q4`, `Q5` along the lower part, `J1` with `9` (left) and `1` (right) printed at the ends.

Schematic, captioned `Trough 7 IR TSTR Circuit`: five phototransistors labelled `Q1 (JAM BALL)`, `Q2 (BALL 1)`, `Q3 (BALL 2)`, `Q4 (BALL 3)`, `Q5 (BALL 4)`, collectors to one common line to `J1` pin 1. `J1` legend, pins 1-9 top to bottom:

| Pin | Printed signal |
| --- | --- |
| 1 | `COL` |
| 2 | `KEY` |
| 3 | `JAM BALL` |
| 4 | `BALL 1` |
| 5 | `BALL 2` |
| 6 | `BALL 3` |
| 7 | `BALL 4` |
| 8 | `NOT USED` |
| 9 | `NOT USED` |

Tie of phototransistor label to pin (traced): `Q1 (JAM BALL)` to pin 3, `Q2 (BALL 1)` to 4, `Q3 (BALL 2)` to 5, `Q4 (BALL 3)` to 6, `Q5 (BALL 4)` to 7.

## PDF page 142 - printed title `10 OPTO P.C.B.` `A-18159`, folio `3-18`

Board drawing: outline with connectors `J1` (pins `1` bottom to `9` top, star key mark near the top), `J2` (pins `1` bottom to `9` top, star key mark near the middle), `J3` (pins `12` at left to `1` at right, star mark near the right end, i.e. between pin 5 and pin 6 positions [?]), and at the right `J4`, `J5`, `J6` (pins `1` at top to `5` at bottom, star key marks at J6 pin 2, J5 pin 3, J4 pin 4).

Pin lists, printed (column 1):

| Connector pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Violet to A-16908 (LED) Sw #37` |
| J1-2 | `J1-2 Gray-Blue to A-16908 (LED) Sw #36` |
| J1-3 | `J1-3 Gray-Green to A-18617-1 (LED) J1-3 Sw #35` |
| J1-4 | `J1-4 Gray-Black to A-18617-1 (LED) J1-4 Sw #34` |
| J1-5 | `J1-5 Gray-Orange to A-18617-1 (LED) J1-5 Sw #33` |
| J1-6 | `J1-6 Gray-Red to A-18617-1 (LED) J1-6 Sw #32` |
| J1-7 | `J1-7 Gray-Brown to A-18617-1 (LED) J1-7 Sw #31` |
| J1-8 | `J1-8 Key` |
| J1-9 | `J1-9 Black Ground to A-18617-1 J1-9` |
| J2-1 | `J2-1 Orange-Violet to A-16909 (Trans.) Sw #37` |
| J2-2 | `J2-2 Orange-Blue to A-16909 (Trans.) Sw #36` |
| J2-3 | `J2-3 Orange-Green to A-18618-1 (Photo) J1-7 Sw #35` |
| J2-4 | `J2-4 Orange-Yellow to A-18618-1 (Photo) J1-6 Sw #34` |
| J2-5 | `J2-5 Orange-Black to A-18618-1 (Photo) J1-5 Sw #33` |
| J2-6 | `J2-6 Key` |
| J2-7 | `J2-7 Orange-Red to A-18618-1 (Photo) J1-4 Sw #32` |
| J2-8 | `J2-8 Orange-Brown to A-18618-1 (Photo) J1-3 Sw #31` |
| J2-9 | `J2-9 Gray-Yellow +12VDC to A-18618-1 (Photo) J1-1` |
| J4-1 | `J4-1 Gray-Orange to A-16908 (LED) Sw #43` |
| J4-2 | `J4-2 Not Used` |
| J4-3 | `J4-3 Not Used` |
| J4-4 | `J4-4 Key` |
| J4-5 | `J4-5 Orange-Black to A-16909 (Trans.) Sw #43` |

Pin lists, printed (column 2):

| Connector pin | Printed text |
| --- | --- |
| J5-1 | `J5-1 Gray-Red to A-16908 (LED) Sw #42` |
| J5-2 | `J5-2 Not Used` |
| J5-3 | `J5-3 Key` |
| J5-4 | `J5-4 Not Used` |
| J5-5 | `J5-5 Orange-Red to A-16909 (Trans.) Sw #42` |
| J6-1 | `J6-1 Gray-Brown to A-16908 (LED) Sw #41` |
| J6-2 | `J6-2 Key` |
| J6-3 | `J6-3 Black Ground` |
| J6-4 | `J6-4 Gray-Yellow +12VDC` |
| J6-5 | `J6-5 Orange-Brown to A-16909 (Trans.) Sw #41` |

There is no `J3` list on this page; `J3` is shown on PDF page 143. The trough opto switches 31-35 are named on this page only by `Sw #` numbers; the page prints no switch names.

## PDF page 143 - printed title `10 OPTO P.C.B.` (captions `Circuit Diagram` and `Schematic`), folio `3-19`

### Circuit Diagram

Top-left `CPU BOARD` box: `J206` pins drawn `3`, `4`; `J208` pins drawn `8`, `7`, `5`, `4`, `3`, `2`, `1`; `J211` (ribbon) to `J102` of the `POWER DRIVER BOARD`; `J141` pins drawn `3`, `2`. Wires printed on the lines from the CPU Board:

| CPU connector pin | Printed wire label |
| --- | --- |
| `J206` pin 3 | `Green-Orange Sw. Col. 3` |
| `J206` pin 4 | `Green-Yellow Sw. Col. 4` |
| `J208` pin 8 | `White-Violet Sw. Row 7` |
| `J208` pin 7 | `White-Blue Sw. Row 6` |
| `J208` pin 5 | `White-Green Sw. Row 5` |
| `J208` pin 4 | `White-Yellow Sw. Row 4` |
| `J208` pin 3 | `White-Orange Sw. Row 3` |
| `J208` pin 2 | `White-Red Sw. Row 2` |
| `J208` pin 1 | `White-Brown Sw. Row 1` |
| `J141` pin 3 (Power Driver Board) | `Black Ground` |
| `J141` pin 2 (Power Driver Board) | `Gray-Yellow +12V` |

Board box `OPTO SW10 P.C.B. A-18159`. Connector `J3` pin numbers are printed top to bottom as `6`, `3`, `7`, `9`, `8`, `9`, `10`, `11`, `12`, `1`, `2` (the `9` appears twice as printed). The wires reach these pins in nested order (traced, outermost wire first):

| Wire | J3 pin printed at its end |
| --- | --- |
| `Green-Orange Sw. Col. 3` | `6` |
| `Green-Yellow Sw. Col. 4` | `3` |
| `White-Violet Sw. Row 7` | `7` |
| `White-Blue Sw. Row 6` | `9` (first of the two `9`s) |
| `White-Green Sw. Row 5` | `8` |
| `White-Yellow Sw. Row 4` | `9` (second `9`) |
| `White-Orange Sw. Row 3` | `10` |
| `White-Red Sw. Row 2` | `11` |
| `White-Brown Sw. Row 1` | `12` |
| `Black Ground` | `1` |
| `Gray-Yellow +12V` | `2` |

(Compare with the `J3` legend in the Schematic below, which prints `12` ROW 1, `11` ROW 2, `10` ROW 3, `9` ROW 4, `8` ROW 5, `7` ROW 6, `6` ROW 7, `5` KEY, `4` COL 1, `3` COL 2, `2` +12VDC, `1` GND. The `Row 1` to `Row 5`, `Black Ground` and `Gray-Yellow +12V` ties agree; the printed `J3` numbers at the `Sw. Row 7`, `Sw. Row 6` and `Sw. Col. 3` wires (`7`, `9`, `6`) differ from the schematic legend (`6`, `7`, `4`). Read as printed; the diagram's `J3` number column is possibly a printer's error [?].)

Right part, `PLAYFIELD` box: `Photo Transistor Board` (labels `E`, `C`, phototransistor), dashed `Beam`, `LED Board` (labels `A`, `K`). Under each, a bundle of 8 wires with an asterisk `*` marking, printed rotated:

- Photo Transistor wires to `J2`, pin numbers printed along the connector bottom `1 2 3 4 5 7 8 9` (no `6`): `Orange-Violet` (1), `Orange-Blue` (2), `Orange-Green` (3), `Orange-Yellow` (4), `Orange-Black` (5), `Orange-Red` (7), `Orange-Brown` (8), `Gray-Yellow` (9).
- LED wires to `J1`, pin numbers printed `1 2 3 4 5 6 7 9` (no `8`): `Gray-Violet` (1), `Gray-Blue` (2), `Gray-Green` (3), `Gray-Black` (4), `Gray-Orange` (5), `Gray-Red` (6), `Gray-Brown` (7), `Black` (9).

Labelled `J2`, `J1`, and under the board `J4`, `J5`, `J6`. Footnote on the drawing: `*Repeat 7 Times.`

Lower connectors of the board box, with wire labels and `(A)`, `(E)`, `(K)`, `(C)` letters printed under the wires:

| Connector | Pins printed | Wires printed (with letter) |
| --- | --- | --- |
| `J4` | `1`, `5` | `Gray-Orange` (A), `Orange-Black` (E) |
| `J5` | `1`, `5` | `Gray-Red` (A), `Orange-Red` (E) |
| `J6` | `1`, `3`, `4`, `5` | `Gray-Brown` (A), `Black` (K), `Gray-Yellow` (C), `Orange-Brown` (E) |

### Schematic

Connector legends printed on the schematic (low resolution print):

`J1` (pins 9 to 1 top to bottom): `9` `CATHODE GND`; `8` `KEY`; `7` `ANODE 1`; `6` `ANODE 2`; `5` `ANODE 3`; `4` `ANODE 4`; `3` `ANODE 5`; `2` `ANODE 6`; `1` `ANODE 7`. Each anode has `220 2W, 1/2W` printed resistors (`R1`-`R7`) to `VCC` (print reads `220 2W, 1/2W`; the first character group may be `220` [?]).

`J2` pin numbers as printed top to bottom `9`, `8`, `7`, `5`, `4`, `3`, `2`, `1`, `6` [?]: `+12VDC` (9); `E1 OPTO 1` (8); `E2 OPTO 2` (7); `E3 OPTO 3` (5); `E4 OPTO 4` (4); `E5 OPTO 5` (3); `E6 OPTO 6` (2); `E7 OPTO 7` (1); `KEY` (6).

`J6 OPTO 8`: pins `1` `A` (with `R25` `220 2W, 1/2W` to `VCC`), `2` `NC`, `3` `K` (to ground), `4` `C` (to `VCC`), `5` `E8`.
`J5 OPTO 9`: pins `1` `A` (with `R28` `220 2W, 1/2W` to `VCC`), `2` `K` (to ground), `3` `NC`, `4` `C` (to `VCC`), `5` `E9`.
`J4 OPTO 10`: pins `1` `A` (with `R31` `220 2W, 1/2W` to `VCC`), `2` `K` (to ground), `3` `C` (to `VCC`), `4` `NC`, `5` `E10`.

Comparators: `LM339` sections `U1A`-`U1D`, `U2A`-`U2D`, `U3A`-`U3D`; input resistor pairs `R8`/`R9`... (`2K` pairs with `R10`, `R12`, `R14`, `R16`, `R18`, `R20`, `R23`, `R26`?, `R27`, `R29`, `R32` `100K`, `R39` `100K`, `R36` `22K`, `R` `22K`), output diodes `D1`-`D12` all `IN4004` (D1-D7 and D10-D12 on the row outputs; `D8` and `D9` on the column outputs), `R37` `10K`, `R38` `10K`, `R33` `22K`, `R35` `100K`, `R40` `100K`, `R41` `100K`, and a `VCC` supply from `D13` `IN4004`, `R22` `1.2K`, `C1` `100UF` and `LED 1`. Component values on this schematic are only partly legible at this print size; none were needed for the tables above.

Row outputs `D10`, `D11`, `D12` run to the short labels `ROW 1`, `ROW 2`, `ROW 3` near the lower left of the `J3` area (traced); `D8` ends at `COL. 1` and `D9` at `COL. 2`.

`J3` legend (pins 12 to 1 top to bottom): `12` `ROW 1`; `11` `ROW 2`; `10` `ROW 3`; `9` `ROW 4`; `8` `ROW 5`; `7` `ROW 6`; `6` `ROW 7`; `5` `KEY`; `4` `COL 1`; `3` `COL 2`; `2` `+12VDC`; `1` `GND`.

## PDF page 144 - printed title `3 OPTO VARI TARGET P.C.B. ASSEMBLY` `A-20906`, folio `3-20`

Board drawing labels: `R2`, `R1`, `R3`, `OPTO3` (pads `A`, `E`, `K`, `C`), `OPTO2` (`A`, `E`, `K`, `C`), `OPTO1` (`A`, `E`, `K`, `C`), `D3`, `D1`, `D2`, `J1` with `1` and `7` printed at the ends and a star key mark at pin 4... (the star is at the fifth position from pin 1 as drawn, i.e. pin 3 [?]; the pin list below says pin 3 is `Key`).

Pin list, printed:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow +12VDC from J141-2` |
| J1-2 | `J1-2 Black, Ground from J141-3` |
| J1-3 | `J1-3 Key` |
| J1-4 | `J1-4 Green-Blue from J206-6` |
| J1-5 | `J1-5 White-Blue from J208-7` |
| J1-6 | `J1-6 White-Violet from J208-8` |
| J1-7 | `J1-7 White-Gray from J208-9` |

Circuit drawing (caption `Circuit`): boxes `POWER DRIVER BOARD` (`J141` pins `2`, `3`), `SECURITY CPU BOARD` (`J206` pin `9`, `J208` pins `5`, `7`) and a box printed `SPIN DISC OPTO P.C.B. A-20952` with `J1` pins `1`, `2`, `4`, `5`, `6`. Wires:

| From | Printed wire label | To J1 pin |
| --- | --- | --- |
| `J141` pin 2 | `Gray-Yellow +12V` | 1 |
| `J141` pin 3 | `Black` | 2 |
| `J206` pin 9 | `Green-Gray` | 4 |
| `J208` pin 5 | `White-Green  Sw #85` | 5 |
| `J208` pin 7 | `White-Blue  Sw #86` | 6 |

Note: this circuit drawing is for the A-20952 Spin Disc board (the identical drawing appears on PDF page 147 with a different second switch) and does not match this page's own pin list (`J1-4 Green-Blue from J206-6`, `J1-5 White-Blue from J208-7`, `J1-6 White-Violet from J208-8`, `J1-7 White-Gray from J208-9`, seven pins) or its seven-pin `J1`. The drawing prints `White-Blue` with `Sw #86` on `J208-7`, whereas the pin list prints `White-Blue from J208-7` on `J1-5`.

Schematic (caption `Schematic`): `R1`, `R2`, `R3` each `470`; `OPTO1`, `OPTO2`, `OPTO3` with pin numbers `4` and `3` (LED side) and `1` and `2` (phototransistor side); `D1`, `D2`, `D3` each `1N4004`; `J1` pins `1` to `7`, pin 3 marked with a cross (key). Connections (traced): `J1-1` (+12V) to the far side of `R1`, `R2`, `R3`; `J1-2` (ground) to LED pin `3` of all three optos; the phototransistor emitters (pin `2`) through `D1`, `D2`, `D3` to a common line to `J1-4`; the phototransistor collectors (pin `1`): `OPTO1` to `J1-5`, `OPTO2` to `J1-6`, `OPTO3` to `J1-7`.

## PDF page 147 - printed title `SPIN DISC OPTO P.C.B.` `A-20952`, folio `3-23`

Board drawing labels: `U1` (pads `A`, `E`, `K`, `C`), `U2` (rotated; pads `A`, `E`, `K`, `C`), `D1`, `D2`, `R2`, `R1`, `J1` (six pins, star key mark at the third pin).

Pin list, printed:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow +12VDC from J141-2` |
| J1-2 | `J1-2 Black, Ground from J141-3` |
| J1-3 | `J1-3 Key` |
| J1-4 | `J1-4 Green-Gray from J206-9` |
| J1-5 | `J1-5 White-Green from J208-5` |
| J1-6 | `J1-6 White-Blue from J208-7` |

Circuit drawing (caption `Circuit`): `POWER DRIVER BOARD` (`J141` pins `2`, `3`), `SECURITY CPU BOARD` (`J206` pin `9`, `J208` pins `5`, `7`), box `SPIN DISC OPTO P.C.B. A-20952` with `J1` pins `1`, `2`, `4`, `5`, `6`. Wires:

| From | Printed wire label | To J1 pin |
| --- | --- | --- |
| `J141` pin 2 | `Gray-Yellow +12V` | 1 |
| `J141` pin 3 | `Black` | 2 |
| `J206` pin 9 | `Green-Gray` | 4 |
| `J208` pin 5 | `White-Green  Sw #85` | 5 |
| `J208` pin 7 | `White-Violet  Sw #57` | 6 |

Note: the circuit drawing prints `White-Violet  Sw #57` on `J208-7`/`J1-6`, whereas this page's pin list prints `J1-6 White-Blue from J208-7`.

Schematic (caption `Schematic`): `R1` `470`, `R2` `470`, `U1` and `U2` (opto pins `4`, `3` for the LED and `1`, `2` for the phototransistor), `D1` `1N4004`, `D2` `1N4004`, `J1` pins `1` to `6` with pin 3 marked with a cross (key). Connections (traced): `J1-1` (+12V) to `R1` and `R2`; `J1-2` (ground) to LED pin `3` of both optos; phototransistor emitters (pin `2`) through `D1` and `D2` to a common line to `J1-4`; the collector (pin `1`) of `U1` to `J1-5` and of `U2` to `J1-6`.

## Comparison of the opto-board descriptions with each other (printed differences)

- Flipper cabinet opto boards: page 137 draws left `J1` pins `7 6 4 2 1` with `F8` (`BLACK-BLUE`) on pin 1 and `F4` (`BLUE-GRAY`) on pin 2, and right `J1` pins `6 4 3 2 1` with `ORANGE` ground from `J212-13` on pin 3, `F2` on 2 and `F6` on 1. Page 139 prints the left board `J1-1 Not Used` and `J1-3 Orange from Coin Door Interface Bd. J13-1`, and the right board `J1-3 Orange to/from Left Flipper Opto Bd. J1-4` with `J1-4 Orange from CPU Bd. J212-13`. Page 139's right board agrees with page 137 for pins 1 and 2 only. The left board's `F8` pin is therefore `J1-1` on page 137 and 135 but `Not Used` on page 139.
- `SW-10 Opto P.C.B.` (pages 140, 141) versus the board printed as `10 OPTO P.C.B. A-18159` (pages 142-143, drawing label `OPTO SW10 P.C.B.`); trough photo wires land on `J2` pins 3, 4, 5, 7, 8 and `+12V` on `J2-9` (page 141 and 142 agree: `J2-3` Orange-Green, `J2-4` Orange-Yellow, `J2-5` Orange-Black, `J2-7` Orange-Red, `J2-8` Orange-Brown, `J2-9` Gray-Yellow). Page 140's `J1-9 Black, from SW-7 Opto P.C.B. J1-9` names `SW-7` rather than `SW-10`.
- The trough boards print `JAM BALL`/`BALL 1`-`BALL 4` (5 positions, `LED 1`-`LED 5`, `Q1`-`Q5`); the title says `Trough 7`. The pages print no trough position beyond `BALL 4`.
- Page 144 and 147 circuit drawings are the same drawing (box title `SPIN DISC OPTO P.C.B. A-20952`); they differ in the printed switch numbers on the second wire (`#86` with `White-Blue` on 144, `#57` with `White-Violet` on 147).

## Reading uncertainties

- Page 136: pin numbers printed in the small connector column between the CPU board and the cabinet opto board (`6`, `7`, `3`, `4`, `1`, `2` as drawn) are low resolution and the routing of which wire meets which number is not reliable; the authoritative pin routing is on page 137 and in page 139's lists.
- Page 143 `J2` schematic pin numbers (`9 8 7 5 4 3 2 1 6`): the print is small and bold; the final `6` next to `KEY` is read [?] but agrees with the page 142 list (`J2-6 Key`).
- Page 143 resistor values on the anode resistors are printed `220 2W, 1/2W` [?] in a tiny font (read as `220`).
- Page 143 `J3` pin numbers beside the diagram wires (`6 3 7 9 8 9 10 11 12 1 2`): read directly from the scan; the repeated `9` is as printed.
- Page 140 and 141 board-drawing star-mark positions on `J1` are described only approximately.
- Page 142 and 144/147 board-drawing star (key) positions are as drawn; the lists give the authoritative key pin.
