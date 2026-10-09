# Safe Cracker — 48 Lamp & Driver PCB A-20909

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`: the parts list and assembly drawing `A-20909 / 48 Lamp & PCB Driver
Assembly` (PDF page 86, printed folio `2-14`), the board connector lists and wiring circuit `48 LAMP & DRIVER P.C.B. A-20909`
(PDF page 145, printed folio `3-21`) and the `48 LAMP & DRIVER P.C.B. SCHEMATIC A-20909` (PDF page 146, printed folio
`3-22`). Read from the rendered pages (300 dpi scan), not from the OCR text. The parts list and the connector lists are
fully legible. The schematic on PDF page 146 is printed with a very small font (about 5 px character height at 300 dpi) and
most of its component labels (lamp numbers, transistor, diode, resistor and IC designators) are NOT legible in the scan; only
the large titles and a few labels could be read. Each unreadable item is reported as such rather than guessed.

## PDF page 86 (printed folio 2-14): parts list

Title lines: `A-20909` / `48 Lamp & Driver PCB Assembly`. The list is printed in two blocks side by side, each with the column headers
`Part Number`, `Designator`, `Description`.

### Left block

| Part Number | Designator | Description |
| --- | --- | --- |
| 5040-09343-00 | C1 | Cap., 10m, 20v (+/-20%) Ax. |
| 5043-08996-00 | C2-C7, C9 | Cap., 0.1m, 50v (+/-20%) Ax. |
| 5048-10994-00 | C8 | Cap., .33mFD, 50v (+/-20%) Ax. |
| 5070-09054-00 | D1 | Diode 1N4004, 1.0A. |
| 5070-08919-00 | D2-D17, D20-D29, D30-D35,D38-D53 | Diode 1N4148 150mA. |
| 5070-09045-00 | D18, D19, D36, D37, D54, D55 | Diode MR501 3.0A. |
| 24-8767 | L1-L48 | Lamp Skirt PCB Twist |
| 5791-13830-07 | J1 | Connector, 7-pin Header |
| 5791-10862-13 | J8 | Connector, 13-pin Header |
| 5671-14516-00 | LED1 | LED Display Red T-1 3/4 |
| 24-8768 | L1-L48 | Bulb #555 6.3v, 0.25A. |
| 5162-13514-00 | Q1-Q48 | Trans. 2N6426 NPN DAR |
| 5010-09358-00 | R1, R2, R4, R5, R7, R8, R10, R11 | Resistor, 1K(ohm), 1/4w, 5% |
| 5010-09416-00 | R120 | Resistor, 470(ohm), 1/4w, 5% |
| 5370-12272-00 | U1 | IC LM339 Quad Comp |
| 5310-14760-00 | U2-U7 | IC 4094 Parallel Out Shift Reg |

(The printed capacitor values use the letter `m` as in `10m`, `0.1m` and `.33mFD`; the printed resistor units use the omega symbol,
shown here as `(ohm)`; `1/4w` on the R120 row is printed `1/4` followed by an omega-like glyph, read as `w`. `+/-20%` is printed with
the plus-minus sign. `LED Display Red T-1 3/4` is printed with a three-quarter glyph.)

### Right block

| Part Number | Designator | Description |
| --- | --- | --- |
| 5010-09034-00 | R3, R6, R9, R12-R14, R16, R18, R20, R22, R24, R26, R28, R30, R32, R34, R36, R38, R40, R42, R44, R46, R47, R49, R51,R53, R55, R57, R59, R61, R63, R65, R67, R69, R71, R73, R75, R77, R79, R80, R82, R84, R86,R88, R90, R92, R94, R96, R98, R100, R102, R104, R106, R108, R110, R112-R117, R121-R123 | Resistor, 10k(ohm), 1/4w, 5% |
| 5070-09999-00 | R15, R17, R19, R21, R23, R25, R27, R29, R31, R33, R35, R37, R39, R41, R43, R45, R48,R50, R52, R54, R56, R58, R60, R62, R64, R66, R68, R70, R72, R74, R76, R78, R81, R83, R85, R87, R89, R91, R93, R95, R97, R99, R101, R103, R105, R107, R109, R111 | Resistor, 2K(ohm), 1/4w, 5% |

(Printed line breaks in the designator cells are not reproduced. Spacing is as printed: `R51,R53`, `R86,R88`, `R48,R50`. The 2K resistor row
has the part number `5070-09999-00`, with a `5070-` prefix, as printed, although the other resistors use the `5010-` prefix.)

Row count: 16 rows in the left block, 2 rows in the right block = 18 rows. `L1-L48` appears twice with different part numbers
(`24-8767` `Lamp Skirt PCB Twist` and `24-8768` `Bulb #555 6.3v, 0.25A.`). `J8` is the printed designator of the 13-pin header, while the
assembly drawing and the connector list on PDF page 145 call the 13-pin connector `J2` (see below).

### Assembly drawing on this page

The drawing is a board outline (portrait on the page) with the lamp positions drawn as hexagonal outlines each carrying a rotated
label `L1` ... `L48` (all 48 labels, one per position, printed inside or beside each lamp socket outline), plus, next to the lamps,
small resistor / transistor / diode symbols with rotated designators and six IC outlines. The designators on the drawing are rotated
and small; the legible printed labels are:

- Lamp labels `L1` through `L48`: 48 lamp positions, scattered in an oval/ring arrangement (not in row order). Positions read from the
  overview include `L44`, `L45`, `L46`, `L47`, `L48` down the left edge (top to bottom `L45`, `L46`, `L47`, `L48`) and `L43`, `L41`, `L30` along
  the top right, `L25` and `L26` at the bottom edge, `L22`, `L23`, `L24` down the left; the full list of 48 labels is present but the mapping of each label
  to its (x, y) was not transcribed.
- Connectors: a 13-pin vertical header at the lower left labelled `J2` (rotated; the parts list calls it `J8`) and a 6/7-pin header below it labelled `J1`.
  A star (`*`) marker is drawn at one pin position of each.
- Diodes (large bodies) labelled `D54`, `D55`, `D36`, `D37`, `D18`, `D19` beside the 13-pin connector.
- ICs: seven IC outlines are drawn; designators `U1` (near `J1`) and `U2`-`U7` are printed in small type (individual readings uncertain, see below).
- `LED1` near `J1`, `C1`, `C8` near `J1`.
- Folio: `2-14`.

Reading uncertainties for this drawing: which IC outline carries which of `U2`-`U7` could not be read reliably (the IC designators are printed
small and in a rotated orientation); the lamp-to-position mapping was not transcribed; lamp labels other than those listed above were not individually verified.

## PDF page 145 (printed folio 3-21): board drawing, connector lists and circuit

Title lines: `48 LAMP & DRIVER P.C.B.` / `A-20909`. The top of the page is a board outline with 48 plain lamp-position symbols (no printed lamp numbers),
small component symbols (resistors, transistor/diode pairs, six IC outlines each flanked by two resistor-array groups), and two headers at the lower right labelled
`J2` (the 13-pin header, with a star at one pin) and `J1` (the smaller header). There are no other printed labels on the drawing.

### J1 (as printed, left column under the drawing)

| Pin | Printed text |
| --- | --- |
| J1-1 | Gray-Yellow +12VDC from J138-2 |
| J1-2 | Black, Ground from J138-3 |
| J1-3 | Key |
| J1-4 | Brown-White from J110-1 |
| J1-5 | Orange-White from J110-3 |
| J1-6 | Yellow-White from J110-4 |
| J1-7 | Green-White from J110-5 |

### J2 (as printed, right column under the drawing)

| Pin | Printed text |
| --- | --- |
| J2-1 | Orange loop end from J2-2 |
| J2-2 | Orange from Transformer Secondary |
| J2-3 | White-Orange loop end from J2-4 |
| J2-4 | White-Orange from J106-8 |
| J2-5 | Key |
| J2-6 | Green loop end from J2-7 |
| J2-7 | Green from Transformer Secondary |
| J2-8 | White-Green loop end from J2-9 |
| J2-9 | White-Green from J106-10 |
| J2-10 | Violet loop end from J2-11 |
| J2-11 | Violet from Transformer Secondary |
| J2-12 | White-Violet loop end from J2-13 |
| J2-13 | White-Violet from J106-11 |

Row counts: J1 7 rows, J2 13 rows. Each pin appears once; no pin is skipped.

### Circuit diagram at the bottom of the page (caption `Circuit`)

Boxes and labels as printed: a box `POWER DRIVER BOARD` with connectors `J110` (pins `1`, `3`, `4`, `5`), `J138` (pins `2`, `3`) and `J106` (pins `8`, `10`, `11`); a box
`TRANSFORMER SECONDARY` with a connector (pins `9`, `3`, `3`) and an in-line connector; and a large box `48 LAMP & DRIVER P.C.B. A-20909` with connectors `J1` (pins `4`, `5`, `6`, `7`, `1`, `2`, top to bottom in
that order) and `J2` (pins `4`, `3`, `9`, `8`, `13`, `12`, then `2`, `1`, `7`, `6`, `11`, `12`, top to bottom). Wires, with their printed colour labels:

| From | Wire label | To (pin on the 48 Lamp & Driver PCB) |
| --- | --- | --- |
| Power Driver Board J110-1 | Brown-White | J1-4 |
| Power Driver Board J110-3 | Orange-White | J1-5 |
| Power Driver Board J110-4 | Yellow-White | J1-6 |
| Power Driver Board J110-5 | Green-White | J1-7 |
| J138-2 | Gray-Yellow +12V | J1-1 |
| J138-3 | Black | J1-2 |
| J106-8 | White-Orange | J2-4 and J2-3 (a dot at the junction, one wire to each pin) |
| J106-10 | White-Green | J2-9 and J2-8 |
| J106-11 | White-Violet | J2-13 and J2-12 |
| Transformer secondary pin 9 | Orange | J2-2 and J2-1 (via the in-line connector; the wire after it is labelled `Orange`) |
| Transformer secondary pin 3 (upper) | Brown (before the in-line connector) / Green (after it) | J2-7 and J2-6 |
| Transformer secondary pin 3 (lower) | Brown (before the in-line connector) / Violet (after it) | J2-11 and J2-12 |

Differences within this page: the circuit drawing shows the Violet pair on `J2-11` and `J2-12` (and `J2-12` is also the second pin of the White-Violet pair), whereas the J2 list prints Violet on `J2-10`/`J2-11`
and White-Violet on `J2-12`/`J2-13`. The circuit drawing also shows the White-Violet pair as `13` and `12`, which matches the list. The Violet pair `11`/`12` in the drawing disagrees with the list's `10`/`11`. The transformer connector pins are printed `9`, `3`, `3` (pin `3` appears twice, as printed).
The wires from the transformer are printed `Orange`, `Brown`, `Brown` before the in-line connector and `Orange`, `Green`, `Violet` after it.

## PDF page 146 (printed folio 3-22): schematic

Title lines: `48 LAMP & DRIVER P.C.B. SCHEMATIC` / `A-20909`. Folio `3-22`. The schematic is printed in portrait orientation.

### Legible labels

| Label as printed | Where |
| --- | --- |
| `DATA 2 STRING (LAMPS 25-48)` | Rotated, above the top group of lamps (top centre of the schematic) |
| `DATA 1 STRING (LAMPS 1-24)` | Rotated, on the left beside the middle-left lamp group |
| `J1` | Connector at the lower right of the schematic (7 pins; pin numbers 1-7 printed beside the pins) |
| `J2` | Connector at the lower left of the schematic (13 pins; pin numbers 1-13 printed beside the pins, `Key` printed beside pin 5) |
| `U2 bypass`, `U3 bypass` ... `U7 bypass` (six labels; individual readings approximate: `U3 bypass`, `U5 bypass`?, `U7 bypass` along the top and `U2 bypass`, `U4 bypass`, `U6 bypass` along the bottom of a row of six capacitors labelled `C2` ... `C7`) | Lower right (bypass capacitors) |
| `LED1` with a resistor labelled `R120 470` and a ground symbol | Lower right |
| `D1` / `1N4004` (reading approximate) and `C1` / `C8` ... | Lower right power section |
| `Vref` | Beside the comparators (supply-rail labels at the supply symbols are not legible) |

### J1 labels as read from the schematic (rotated text beside the connector pins; low resolution, readings approximate)

| Pin | Label read | Certainty |
| --- | --- | --- |
| J1-1 | `+12V` | uncertain [?] (printed as `+12V` or `+12V` with a leading symbol) |
| J1-2 | `GND` | fairly clear |
| J1-3 | `KEY` | clear |
| J1-4 | `ENABLE` | uncertain [?] (the glyphs read `?NABLE` / `CAN BLE`; the word is probably `ENABLE`) |
| J1-5 | `CLOCK` | clear |
| J1-6 | `DATA 1` | clear |
| J1-7 | `DATA 2` | clear |

The seven pin labels are printed in the order shown, one per pin, in the same order as the pin numbers 1-7 beside the connector.

### J2 labels as read from the schematic (rotated text; low resolution)

Twelve of the 13 pins carry wires that pair up at the connector into six nets (pins 1/2, 3/4, 6/7, 8/9, 10/11, 12/13, matching the loop-end pairs of the J2 list), and the printed labels read as six text lines, each of the form
`Source String n` or `Return String n`: reading top to bottom (in the rotated view), `Source String 3`[?], `Return String 3`[?], `Source String 4`[?], `Return String 4`[?], then a gap (where `Key` is printed beside pin 5),
then `Source String 1`[?], `Return String 1`[?]. The first word (`Source`/`Return`) and the word `String` were readable; the digit after `String` was not reliably legible (the glyphs for `1`, `2`, `3`, `4` are blurred
in the scan). The pairing therefore could not be verified; see Reading uncertainties.

### Schematic structure that could be read (counts and topology only)

- Six groups of eight lamp driver stages, each group topped by a row of eight lamp symbols (each a bulb symbol with a small rotated label of the form `LMP n`, not legible), under each lamp a transistor symbol (NPN Darlington, labelled `Qn`, not legible), a base resistor, a `1N4148` type diode in series, and a pull-down resistor; each group's eight stage inputs run down to one IC drawn as a rectangle carrying eight output pin labels along its top edge (the pin names are not legible), two pin labels along the bottom-left and a small block of pin-note text to its right (not legible, not transcribed).
- Group placement on the page (top to bottom): the top row holds two groups side by side (left and right, 8 lamps each = 16 lamps), under the label `DATA 2 STRING (LAMPS 25-48)`; below them a single group on the right (8 lamps); on the left beside it the label `DATA 1 STRING (LAMPS 1-24)` and a single group (8 lamps); at the bottom a row of two groups (8 lamps each). That is 6 groups x 8 = 48 lamps. The dashed boundary lines on the page enclose the top two groups plus the middle-right group as one region (`DATA 2 STRING`, 24 lamps) and the middle-left plus the two bottom groups as the other region (`DATA 1 STRING`, 24 lamps) [?] (assignment of the middle-right group to the Data 2 region is inferred from the dashed outline and the `LAMPS 25-48` / `1-24` counts).
- Six ICs of one type (the parts list `U2-U7`, `IC 4094 Parallel Out Shift Reg`), one per group, each with a bypass capacitor `C2`-`C7` (`U2 bypass` ... `U7 bypass`); the 4094 pin names printed beside the IC are not legible.
- Four comparator (op-amp triangle) symbols, three along the bottom and one in the middle-right, fed from the `J1` signal lines through resistor/pull-up networks and a divider labelled `Vref`; these correspond to the single `U1`, `IC LM339 Quad Comp` of the parts list (four comparators, one per J1 signal line `ENABLE`, `CLOCK`, `DATA 1`, `DATA 2`) [?] (the connection of each comparator to a specific J1 pin could not be traced reliably).
- `J1` lines (`CLOCK`, `ENABLE` etc.) run up the right side of the page to the six ICs; `DATA 1` and `DATA 2` run to the Data 1 and Data 2 group chains respectively [?].
- Lamp supply: the six `Source String n` / `Return String n` nets from `J2` feed the lamp rows, with `MR501` diodes (parts list `D18`, `D19`, `D36`, `D37`, `D54`, `D55`) drawn at the head of each source line (about six diodes drawn at the left of the lamp groups, labelled with a `D` number, not legible) [?].
- Power section (lower right): a `1N4004` diode (parts list `D1`) from the +12V input, capacitors, a resistor divider (`R12`, `R13`, 10K) producing `Vref`, an LED `LED1` with a series resistor `R120` 470.

Items NOT transcribed because the scan is not legible at 300 dpi: every `LMP n` lamp label, every `Qn`, `Rn`, `Dn` designator on the 48 driver stages, the 4094 pin numbers and names, and the IC designators `U2`-`U7` beside the six ICs. The lamp-to-shift-register-output mapping therefore cannot be read from this scan.

## Reading uncertainties (summary)

- Page 86 (assembly drawing): IC designators `U1`-`U7` per outline, lamp label positions; the `J2` label (drawing) versus `J8` (parts list) for the 13-pin header.
- Page 145: none in the connector lists; the circuit drawing's `J2-11/-12` Violet pair differs from the list's `J2-10/-11`.
- Page 146: J1 labels `+12V` [?] and `ENABLE` [?]; the digits of the six `Source/Return String n` labels on J2 [?]; every component designator on the lamp stages; the group-to-string assignment of the middle-right group [?].

## Summary (author's interpretation; not part of the transcription)

- Board inputs. `J1` is a 7-pin header: `+12VDC` (`J1-1`, from `J138-2`), ground (`J1-2`, from `J138-3`), key (`J1-3`), and four logic inputs `J1-4` ... `J1-7`. The connector list on page 145 identifies the four logic wires only as `Brown-White`, `Orange-White`, `Yellow-White` and `Green-White` from Power Driver Board `J110-1`, `J110-3`, `J110-4`, `J110-5`; the Power Driver Board pin list (PDF page 149) names those wires `Solenoid 37`, `Solenoid 38`, `Solenoid 39` and `Solenoid 40` `to Insert`. The schematic's J1 pin labels read (with the uncertainty noted above) `ENABLE` (`J1-4`), `CLOCK` (`J1-5`), `DATA 1` (`J1-6`), `DATA 2` (`J1-7`). Taken together, solenoid driver 37 appears to be the board's enable/strobe line, 38 the shift clock, 39 the serial data for lamps 1-24 and 40 the serial data for lamps 25-48. [?] The `ENABLE` reading is the weakest; whether it is a latch/strobe or an output-enable line is not stated in the legible text.
- Lamp count and numbering. 48 lamps (`L1`-`L48`, `Q1`-`Q48`), driven by six `4094` parallel-out shift registers (`U2`-`U7`, eight outputs each) through NPN Darlington transistors. The schematic's legible titles split them into `DATA 1 STRING (LAMPS 1-24)` and `DATA 2 STRING (LAMPS 25-48)`: three 4094s per data line (24 lamps), each carrying lamps in 8-lamp groups. The Data 1 string is lamps 1-24 and the Data 2 string is lamps 25-48. Which register output (Q0-Q7, pin number) drives which lamp, the chain order of the three registers within a string (which register's output corresponds to lamps 1-8 versus 9-16 versus 17-24) and whether lamp number increases with or against shift order could NOT be read from this scan; this requires a better scan of PDF page 146 (the lamp labels `LMP n` are present on the schematic but illegible at 300 dpi) or a hardware/ROM test.
- Lamp power: lamps (`Bulb #555 6.3v, 0.25A`) are powered from AC taps: `J2` takes three transformer secondary feeds (Orange `J2-2`, Green `J2-7`, Violet `J2-11`) and three `6.8VAC` feeds from the Power Driver Board `J106-8` (White-Orange), `J106-10` (White-Green), `J106-11` (White-Violet), each paired with a loop-end pin; the schematic labels these as `Source String`/`Return String` nets.
