# Black Rose — Flipper Circuit Drawings, Flipper Opto Switch Board and Fliptronic II Board Connector List

Transcribed from `Bally_1992_Black_Rose_Manual.pdf`, PDF pages 113, 116 and 123, printed pages `BLACK ROSE 3-9`,
`BLACK ROSE 3-12` and `BLACK ROSE 3-19` (footers read on each page): the `Left Flipper Circuit`, `Right Flipper Circuit` and
`Block Diagram Of Flipper Circuit` drawings (page 113), the `Flipper Opto Switch Board A-15894` pin lists and wiring
sketch (page 116) and the `FLIPTRONIC II BOARD A-15472` connector list (page 123). Read from the rendered pages
(300 dpi image-only scan), not from the OCR text.

Page 123 and page 116 pin lines are given one per row in printed order, split into the pin designator and the rest of
the printed line. Page 113 is a schematic; its text labels are listed by drawing, with the connector pin each label sits
on. Page 113 prints no coil part number, no transistor designators and no EOS switch part number: the only component
designators printed are `BR1`, `C2`, `F901` to `F904`; the coils are drawn as a two-winding symbol with a diode across
each winding, and "power" and "holding" are the labels of the two wires entering `J902`. Spelling, capitalization
and the mix of `-`, `/` and abbreviations in colour names are as printed (`ORG-BLU` and `ORG/GRY` both appear on page 113;
`BLK/YEL` and `BLK-BLU` both appear). Printed oddities kept literally: page 116 `J1 - 3 Orange ((Switch Grd) loop from
Left Side Opto Board J1-4` has a doubled opening parenthesis; `J1 - 4 Orange  (Switch Grd)` has two spaces; the note
prints `gound` and `though`; page 123 `J907-5`, `J907-7`, `J907-9` have two spaces before `loop`, and
`J901-3 White-Blue, 50VAC loop, from J105-2` has a comma after `loop`. In the left circuit drawing the `J902` pin numbers are
printed only for the lower-left windings (`9`, `7`); the two rows of the upper-left coil carry no pin number. The right circuit
drawing prints all four. No cell is illegible.

## PDF page 113 (printed `BLACK ROSE 3-9`)

The page carries three drawings: `Left Flipper Circuit` (top), `Right Flipper Circuit` (middle) and
`Block Diagram Of Flipper Circuit` (bottom, the caption is printed below the drawing).

### `Left Flipper Circuit`

Text labels, left to right and top to bottom.

- Left of the J901 connector box, on J901 pins `1`, `3`, `4`, `5` (box title `J901`): pins 1 and 3 are drawn tied together and pins 4 and 5 are drawn tied together; the pairs feed the bridge `BR1` (capacitor `C2`).
- Board name beside J901/J902: `FLIPTRONIC II CONTROLLER BOARD` (printed on the left side, three lines `FLIPTRONIC II` / `CONTROLLER` / `BOARD`).
- Fuses: `F903` into `J907` pin `7` (pin `6` drawn tied to `7`); `F901` into `J907` pin `1` (pin `2` drawn tied to `1`). Connector box title `J907`.
- Wire labels leaving J907: `GRY-YEL` on the pin 6/7 side (to the lower-left coil assembly) and `GRY-YEL` on the pin 1/2 side (to the upper-left coil assembly).
- Heading beside the lower assembly: `LOWER LEFT`, with the label `Flipper Assembly` beside the coil.
- `J902` box (the controller board connector), wire rows:

| J902 pin | Wire colour as printed | Winding label | Coil it feeds |
| --- | --- | --- | --- |
| 9 | BLU-GRY | POWER | `LOWER LEFT` |
| 7 | ORG-BLU | HOLDING | `LOWER LEFT` |
| (no pin number printed) | BLK-BLU | POWER | the lower coil, headed `UPPER LEFT (NOT USED)` |
| (no pin number printed) | ORG/GRY | HOLDING | the lower coil, headed `UPPER LEFT (NOT USED)` |

- Heading under the lower coil: `UPPER LEFT (NOT USED)`.
- `J906` box (the end-of-stroke connector), top right: pin `3` carries wire `BLK-BLU` to an `End-of-stroke Switch` (switch symbol, label printed beside the switch as `End-of-stroke Switch`) whose other side carries wire `ORG` to pin `6` (pin 6 is drawn grounded). The lower `End-of-stroke Switch` runs from pin `5` (no colour label on the pin 5 wire) to a wire labelled `ORG` joining the same ground line. The board label to the right of J906: `FLIPTRONIC II CONTROLLER BOARD` (`FLIPTRONIC II` / `CONTROLLER` / `BOARD`). The upper end-of-stroke switch is the one beside the `LOWER LEFT` heading; the lower end-of-stroke switch is the one beside the `UPPER LEFT (NOT USED)` heading.

### `Right Flipper Circuit`

- Same left-hand layout as the left circuit: `J901` pins `1`, `3`, `4`, `5`; `BR1`; `C2`; board label `FLIPTRONIC II CONTROLLER BOARD`.
- Fuses: `F904` into `J907` pin `9` (pin `8` drawn tied to `9`); `F902` into `J907` pin `4` (pin `5` drawn tied to `4`).
- Wire labels leaving J907: `BLU-YEL` on the pin 8/9 side (to the lower-right coil assembly) and `BLU-YEL` on the pin 4/5 side (to the upper-right coil assembly).
- Heading beside the upper assembly: `LOWER RIGHT`, with the label `Flipper Assembly` beside the coil.
- `J902` box, wire rows:

| J902 pin | Wire colour as printed | Winding label | Coil it feeds |
| --- | --- | --- | --- |
| 13 | BLU-VIO | POWER | `LOWER RIGHT` |
| 11 | ORG/GRN | HOLDING | `LOWER RIGHT` |
| 6 | BLK/YEL | POWER | the lower coil, headed `UPPER RIGHT` |
| 4 | ORG/VIO | HOLDING | the lower coil, headed `UPPER RIGHT` |

- Heading under the lower coil: `UPPER RIGHT`.
- `J906` box, top right: pin `1` carries wire `BLK-GRN` to an `End-of-stroke Switch` (beside the `LOWER RIGHT` heading) whose other side carries wire `ORG` to pin `6` (grounded). Pin `4` carries wire `BLK-VIO` to the second `End-of-stroke Switch` (beside the `UPPER RIGHT` heading), whose other side carries `ORG` to the same ground line. Board label: `FLIPTRONIC II CONTROLLER BOARD`.

### `Block Diagram Of Flipper Circuit`

Text labels:

- `J907` with `+50V` printed in a box beside it; `FLIPTRONIC II CONTROLLER BOARD`; connector boxes `J906`, `J902`, `J901`, `J903`, `J904`, `J905` on the board outline. A single generic flipper coil (two windings with two diodes) and a single switch symbol are drawn to the right of J906/J902 with no part labels.
- Left of the board, a dashed box labelled `CABINET` containing two boxes, `LEFT CABINET OPTO BOARD` and `RIGHT CABINET OPTO BOARD` (divided by a diagonal line).
- Wires from the cabinet opto boards to `J905`, printed as colour label then J905 pin: `BLK-BLU` to pin `5`, `BLU-GRY` to pin `2` (both from the `LEFT CABINET OPTO BOARD`); `BLK-YEL` to pin `3`, `BLU-VIO` to pin `1`, `ORG` to pin `6` (these three wires leave the `RIGHT CABINET OPTO BOARD` part of the box; the diagonal line separates the two boards).
- `J903` connects down to `J202` on the box `CPU BOARD`.
- `J904` connects to `J114` on the box `POWER DRIVER BOARD`, with branch labels `+5V` and `+12V` (and a ground arrow); `J901` connects to `J105` on the same box, with branch label `50VAC` (arrow).
- Box labels: `POWER DRIVER BOARD`, `CPU BOARD`.

## PDF page 116 (printed `BLACK ROSE 3-12`)

Heading: `Flipper Opto Switch Board` / `A-15894`.

### `Left Side Flipper Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Blue-Gray (lower flipper) from Fliptronic II Board J905-2 |
| J1 - 2 | Black-Blue (upper flipper) from Fliptronic II Board J905-5 |
| J1 - 3 | Orange (Switch Grd) from Fliptronic II Board J906-6 |
| J1 - 4 | Orange  (Switch Grd) loop from J1-3 |
| J1 - 5 | Key |
| J1 - 6 | Gray-Yellow (+12V) from Power Driver Board J116-2 |
| J1 - 7 | Gray-Yellow (+12V) loop from J1-6 |

### `Right Side Flipper Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Blue-Violet (lower flipper) from Fliptronic II Board J905-1 |
| J1 - 2 | Black-Yellow (upper flipper) from Fliptronic II Board J905-3 |
| J1 - 3 | Orange ((Switch Grd) loop from Left Side Opto Board J1-4 |
| J1 - 4 | N/C |
| J1 - 5 | Key |
| J1 - 6 | Gray-Yellow (+12V) from Power Driver Board J116-2 |
| J1 - 7 | Gray-Yellow (+12V) loop from J1-6 |

### Note block (bold, printed under the pin lists)

```
Please Note:
The Left Flipper Opto Switch Board must be
connected in order for the Right Flipper Opto
Switch Board to operate because power and
gound are connected though the printed
circuit board.
```

### Drawings on the page

- Top right: a board outline whose parts are labelled `opto 1`, `opto 2`, `R1`, `R2` and a seven-position connector `J1` (pin `7` at the left end, pin `1` at the right end, the key position drawn as a star).
- Schematic below the note: two resistors `R1` `470Ω` and `R2` `470Ω` each feeding a light-emitting diode, each diode paired with a phototransistor (opto interrupter); labels `opto 1`, `opto 2`, and on the connector `7`, `+12VDC` (pin 6), `SW-1` (pin 1), `SW-2` (pin 2), `Key` (pin 5), `GND` (pins 3 and 4 tied). Printed pin numbers beside the connector, top to bottom: `7`, `6`, `1`, `2`, `5`, `3`, `4`.
- Wiring sketch at the bottom: boxes `Left Flipper Opto Switch Board` and `Right Flipper Opto Switch Board` (each with `J1`, pins `6`, `7`, `3`, `4`, `1`, `2` drawn), a box `Power Driver Board` with `J116` pin `2`, and a box `Fliptronic II Board` with `J906` pin `6` and `J905` pins `2`, `5`, `1`, `3`. Wire labels: `+12V` (to J116 pin 2), `Gnd` (dashed, to J906 pin 6), `L. Left Flipper` (to J905 pin 2), `U. Left Flipper` (to J905 pin 5), `L. Right Flipper` (to J905 pin 1), `U. Right Flipper` (to J905 pin 3).

## PDF page 123 (printed `BLACK ROSE 3-19`)

Heading: `FLIPTRONIC II BOARD` / `A-15472`. The page also prints a board layout drawing at the top (connectors `J902` 1 to 13, `J907` 1 to 9, `J901` 1 to 5, `J903` 1/2 and 33/34, `J904` 1 to 5, `J905` 1 to 6, `J906` 1 to 6), not transcribed beyond these pin counts.

### Left column

| Pin | Printed text |
| --- | --- |
| J901-1 | White-Blue, 50VAC loop from J105-1 |
| J901-2 | White-Blue, loop from J901-1 |
| J901-3 | White-Blue, 50VAC loop, from J105-2 |
| J901-4 | Key |
| J901-5 | White-Blue, loop from J901-3 |
| J902-1 | Not Used |
| J902-2 | Not Used |
| J902-3 | Not Used |
| J902-4 | Orange-Violet, holding to upper right flipper |
| J902-5 | Not Used |
| J902-6 | Black-Yellow, power to upper right flipper |
| J902-7 | Orange-Blue, holding to lower left flipper |
| J902-8 | Not Used |
| J902-9 | Blue-Gray, power to lower left flipper |
| J902-10 | Key |
| J902-11 | Orange-Green, holding to lower right flipper |
| J902-12 | Not Used |
| J902-13 | Blue-Violet, power to lower right flipper |
| J903 | Ribbon Cable, data to/from J202; J506; J601 |
| J904-1 | Gray, +5V from J114-4 |
| J904-2 | Gray-Green, +12V from J114-2 |
| J904-3 | Key |
| J904-4 | Black, Ground from J114-7 |
| J904-5 | Black, Ground from J114-5 |

### Right column

| Pin | Printed text |
| --- | --- |
| J905-1 | Blue-Violet, to right flipper button opto |
| J905-2 | Blue-Gray, to left flipper button opto |
| J905-3 | Black-Yellow, to right flipper button opto |
| J905-4 | Key |
| J905-5 | Black-Blue, to left flipper button opto |
| J905-6 | Orange, Ground to cabinet optos |
| J906-1 | Black-Green, to lower right end-of-stroke switch |
| J906-2 | Key |
| J906-3 | Black-Blue, to lower left end-of-stroke switch |
| J906-4 | Black-Violet, to upper right end-of-stroke switch |
| J906-5 | Not Used |
| J906-6 | Orange, Ground to end-of-stroke switches |
| J907-1 | Not Used |
| J907-2 | Not Used |
| J907-3 | Key |
| J907-4 | Blue-Yellow, +50V to upper right flipper |
| J907-5 | Blue-Yellow,  loop from J907-4 |
| J907-6 | Gray-Yellow, +50V to lower left flipper |
| J907-7 | Gray-Yellow,  loop from J907-6 |
| J907-8 | Blue-Yellow, +50V to lower right flipper |
| J907-9 | Blue-Yellow,  loop from J907-8 |

The `P.C. Board Legend` box (J1-J6 Coin Door Interface Board, J1xx Power Driver Board, J2xx CPU Board, J5xx Audio Board, J6xx Dot Matrix Controller Board, J9xx Fliptronic II Board) is printed below the right column.
