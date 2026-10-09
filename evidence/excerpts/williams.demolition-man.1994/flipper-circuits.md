# Demolition Man — Flipper Circuits

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, read from the
rendered pages (308 dpi 1-bit scan), not from the OCR text:

- PDF page 115, printed `DEMOLITION MAN 3-11`, `Flipper Circuit Diagram`.
- PDF page 116, printed `DEMOLITION MAN 3-12`, `Flipper Coil Circuits` (`Left Flipper Circuit`, `Right Flipper
  Circuit`) and `Flipper End-of-Stroke Switches`.
- PDF page 117, printed `DEMOLITION MAN 3-13`, `Flipper Cabinet Switch Circuit Diagram` and `Flipper Cabinet
  Switches`.
- PDF page 118, printed `DEMOLITION MAN 3-14`, `A-17316 Flipper Opto PCB Assembly` with the left and right side
  `Flipper Cabinet Opto Switch Board` connector lists.
- PDF page 102, printed `DEMOLITION MAN 2-46`, the `Flipper Circuits` block at the bottom of the
  `SOLENOID/FLASHER TABLE`.

The Fliptronic II board's own connector list (PDF page 135) is in `cpu-and-fliptronic-connectors.md`. None of
these pages mentions a gun handle, trigger or thumb button: the cabinet flipper switches are drawn only as
`Flipper Opto Assembly` boards (A-17316), two opto switches per board, one board on the left and one on the
right of the cabinet. Where a drawing prints a name it is kept literally.

## Flipper block of the solenoid/flasher table (PDF page 102)

Printed numbers `(29)` through `(36)` are in parentheses; the function names are printed in the `Flipper Circuits`
heading cells, the second cell of each row is the printed coil-circuit name. Blank cells are printed blank. The
bracketed solenoid numbers repeat for both rows of each flipper (merged cells; the function name is printed once
across a pair of rows and is repeated here).

| (Sol.) | Flipper Circuits function | Circuit | Voltage connection playfield | Drive transistor power | Drive transistor hold | Drive connection playfield | Drive wire color power | Drive wire color hold | Coil part number | Coil colors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (29) | Lower Right Flipper | Lwr. Rt. Power | J907-1 (Red-Grn) | Q4 |  | J902-13 | Yel-Grn |  | FL-11629 | Blue |
| (30) | Lower Right Flipper | Lwr. Rt. Hold | J907-1 (Red-Grn) |  | Q11 | J902-11 |  | Org-Grn | FL-11629 | Blue |
| (31) | Lower Left Flipper | Lwr. Lt. Power | J907-4 (Red-Blu) | Q3 |  | J902-9 | Yel-Blu |  | FL-11629 | Blue |
| (32) | Lower Left Flipper | Lwr. Lt. Hold | J907-4 (Red-Blu) |  | Q9 | J902-7 |  | Org-Blu | FL-11629 | Blue |
| (33) | Claw Magnet | Up Rt. Power | J907-6 (Red-Vio) | Q2 |  | J902-6 | Yel-Vio |  | SZ-33-3000 |  |
| (34) | Not Used | Up Rt. Hold | J907-6 (Red-Vio) |  | Q7 | J902-4 |  | Org-Vio |  |  |
| (35) | Upper Left Flipper | Up Lt. Power | J907-8 (Red-Gry) | Q1 |  | J902-3 | Yel-Gry |  | FL-11630 | Red |
| (36) | Upper Left Flipper | Up Lt. Hold | J907-8 (Red-Gry) |  | Q5 | J902-1 |  | Org-Gry | FL-11630 | Red |

The block's column headings are `Voltage Connections Playfield`, `Drive Transistors Power Hold`, `Drive Connections
Playfield`, `Drive Wire Colors Power Hold`, `Coil Part Number`, `Coil Colors`. The coil part number is printed once
across each pair of rows for the Lower Right, Lower Left and Upper Left flippers (`FL-11629`, `FL-11629`,
`FL-11630`); the Claw Magnet row prints `SZ-33-3000` and no coil colour; the `Not Used` row prints neither. The
footer printed under the block is `J1XX-X = Power Driver Board, JX-X 8-driver Board, J9XX-X = Fliptronic II Board`.
The function cell for solenoids 33 and 34 reads `Claw Magnet` and `Not Used`; the circuit cells for the same two
rows still read `Up Rt. Power` and `Up Rt. Hold`.

## Flipper Circuit Diagram (PDF page 115, printed 3-11)

Boxes and labels as printed. The diagram is centred on the `FLIPTRONIC II BOARD`.

Top, the four `+50Vdc` supply wires, each running from a pin of connector `J907` to a coil box:

| J907 pin | Wire label | Goes to coil box |
| --- | --- | --- |
| 4 | Red-Blue +50Vdc | LOWER LEFT FLIPPER COIL |
| 8 | Red-Gray +50Vdc | UPPER LEFT FLIPPER COIL |
| 1 | Red-Green +50Vdc | LOWER RIGHT FLIPPER COIL |
| 6 | Red-Violet +50Vdc | UPPER** RIGHT FLIPPER COIL |

`END-OF-STROKE SWITCHES`, connector `J906`:

| J906 pin | Wire | Switch name | Switch id |
| --- | --- | --- | --- |
| 5 | Black-Gray | U. Left Flipper | F7 |
| 3 | Black-Blue | L. Left Flipper | F3 |
| 4 | Black-Violet | U. Right Flipper | F5* |
| 1 | Black-Green | L. Right Flipper | F1 |
| 6 | Orange | Ground |  |

Drive wires, connector `J902`, each ending in a transistor label at the coil box:

| J902 pin | Wire | Function | Transistor | Coil box |
| --- | --- | --- | --- | --- |
| 6 | Yellow-Violet | Power | Q2 | UPPER** RIGHT FLIPPER COIL |
| 4 | Orange-Violet | Holding | Q7 | UPPER** RIGHT FLIPPER COIL |
| 13 | Yellow-Green | Power | Q4 | LOWER RIGHT FLIPPER COIL |
| 11 | Orange-Green | Holding | Q11 | LOWER RIGHT FLIPPER COIL |
| 3 | Yellow-Gray | Power | Q1 | UPPER LEFT FLIPPER COIL |
| 1 | Orange-Gray | Holding | Q5 | UPPER LEFT FLIPPER COIL |
| 9 | Yellow-Blue | Power | Q3 | LOWER LEFT FLIPPER COIL |
| 7 | Orange-Blue | Holding | Q9 | LOWER LEFT FLIPPER COIL |

Cabinet switch (opto) wires, connector `J905`, to the box `FLIPPER OPTO ASSEMBLIES`:

| J905 pin | Wire | Switch name | Switch id |
| --- | --- | --- | --- |
| 5 | Black-Blue | U. Left Flipper | F8 |
| 2 | Blue-Gray | L. Left Flipper | F4 |
| 3 | Blue-Violet | U. Right Flipper | F6* |
| 1 | Black-Yellow | L. Right Flipper | F2 |
| 6 | Orange | Ground |  |

Also on the page: a `Gray-Yellow +12V` wire from the `FLIPPER OPTO ASSEMBLIES` box to Power Driver Board
connector `J116` pin 2; connector `J901` pins 1 and 5, both `White-Blue 50Vac`, to Power Driver Board connector
`J105` pins 1 and 2 (pin 1 of J901 to J105 pin 1 and pin 5 of J901 to J105 pin 2 as the lines are drawn);
connector `J904` pins 4 and 5 `Black Ground`, pin 1 `Gray +5V`, pin 2 `Gray-Green +12V`, to Power Driver Board
connector `J114` pins 1-7 (the drawn J114 pins are `1 2 3 4 5 7`); a ribbon cable `J903` on the Fliptronic II
board to `J202` on the `CPU BOARD`.

Footnotes printed at the bottom of the page, verbatim:

- `*Not used on this game.`
- `** Upper right flipper power drive is used as the Claw magnet drive.`
- `   Upper right flipper holding drive is not used.`

## Flipper Coil Circuits (PDF page 116, printed 3-12)

`Left Flipper Circuit` (inside a dashed `FLIPTRONIC II BOARD` outline): connector `J901` pins 1, 2, 3, 5 feed a
bridge `BR1` and capacitor `C2`; the rectified supply passes two fuses `F904` and `F902` to connector `J907`
pins 4 and 5 (`Red-Blue`, lower left coil +50V) and pins 8 and 9 (`Red-Gray`, upper left coil +50V); pins 4/5 and
8/9 are each drawn tied together. Drive: `J902` pin 9 `Yellow-Blue` `Power`, pin 7 `Orange-Blue` `Holding`
(`Lower Left Flipper` coil with its diodes), and pin 3 `Yellow-Gray` `Power`, pin 1 `Orange-Gray` `Holding`
(`Upper Left Flipper` coil). End-of-stroke switches on `J906`: pin 3 `Black-Blue` `Lower Left End-of-Stroke
Switch` and pin 5 `Black-Gray` `Upper Left End-of-Stroke Switch`, each returning on `Orange` to pin 6 (ground).

`Right Flipper Circuit`: connector `J901` pins 1, 2, 3, 5 feed `BR1` and `C2`; fuses `F903` and `F901`
feed connector `J907` pins 1 and 2 (`Red-Green`, lower right coil) and pins 6 and 7 (`Red-Violet`, upper right
coil); pins 1/2 and 6/7 are each drawn tied together. Drive: `J902` pin 13 `Yellow-Green` `Power`, pin 11
`Orange-Green` `Holding` (`Lower Right Flipper` coil), and pin 6 `Yellow-Violet` `Power`, pin 4 `Orange-Violet`
`Holding` (`Upper Right Flipper` coil). End-of-stroke switches on `J906`: pin 1 `Black-Green` `Lower Right
End-of-Stroke Switch` and pin 4 `Black-Violet` `Upper Right End-of-Stroke Switch`, each returning on `Orange` to
pin 6 (ground).

The page does not print a note that the `Upper Right Flipper` here is the claw magnet; that note is the footnote
on PDF page 115 and the `Claw Magnet` row of the solenoid table on PDF page 102.

## Flipper End-of-Stroke Switches (PDF page 116, lower half)

Key printed at the upper left: `F1 Lower Right Flipper`, `F5 Upper Right Flipper`, `F3 Lower Left Flipper`,
`F7 Upper Left Flipper`.

`FLIPTRONIC II BOARD`, connector `J906`:

| J906 pin | Wire | Chip pin | Switch |
| --- | --- | --- | --- |
| 1 | Black-Green | (U4A-5) | F1 |
| 4 | Black-Violet | (U6A-5) | F5 |
| 3 | Black-Blue | (U4C-9) | F3 |
| 5 | Black-Gray | (U6C-9) | F7 |
| 6 | Orange |  | common to the four switches |

Below, a second `FLIPTRONIC II BOARD` drawing, `Dedicated Input`: a `74HCT244` driving through `10K` (to `+5V`),
an `LM339` comparator with points `A` and `B`, a `1K` pull-up to `+12V`, a `1N4004` diode, to `J906` with an
`End-of-Stroke Switch` between a `Black-xxx` wire and `Orange` (pin 6, ground). Truth table printed: `Switch` /
`A` / `B`: `Open` `H` `H` `Off`; `Closed` `L` `L` `On`.

Text printed beneath: `The flipper switch circuits operate similar to the dedicated switch circuit.  The
circuits are active low and tied to ground through the switch.` and `When a switch closes the row side
(dedicated input) of the circuit activates.  The "+" input to the LM339 drops below +5V therefore its output is
low.  Since the row (dedicated input) circuit is tied directly to ground through the switch, the switch is
considered closed by the microprocessor.  When the switch opens, the "+" input to the LM339 is above +5V, its
output is high and the row (dedicated input) is inactive.`

## Flipper Cabinet Switch Circuit Diagram (PDF page 117, printed 3-13, upper drawing)

Two boxes `LEFT FLIPPER OPTO ASSEMBLY` and `RIGHT FLIPPER OPTO ASSEMBLY`, each with connector `J1` (pins 6, 7, 3,
4, 1, 2) and a harness connector beside it (also pins 6, 7, 3, 4, 1, 2). Wires drawn to `FLIPTRONIC II BOARD`
connector `J905` and `POWER DRIVER BOARD` connector `J116`:

| Wire label | Meaning label | Switch | Connector pin |
| --- | --- | --- | --- |
| Gray-Yellow | +12V | | J116 pin 2 (from harness pin 6 of the left board) |
| Orange | Ground | | J905 pin 6 (from harness pin 3 of the left board; dashed) |
| Blue-Gray | L. Left Flipper | F4 | J905 pin 2 (harness pin 1 of the left board) |
| Black-Blue | U. Left Flipper | F8 | J905 pin 5 (harness pin 2 of the left board) |
| Black-Yellow | L. Right Flipper | F2 | J905 pin 1 (harness pin 1 of the right board) |
| Blue-Violet | U. Right Flipper | F6 | J905 pin 3 (harness pin 2 of the right board) |

The left board's harness pin 7 is drawn joined to the right board's harness pin 6 (the `+12V` loop) and the left
board's harness pin 4 to the right board's harness pin 3 (the ground loop, dashed). Each board's own `J1` pins 6
and 7 are drawn jumpered together and pins 3 and 4 are drawn jumpered together (dashed).

## Flipper Cabinet Switches (PDF page 117, lower drawings)

Key at the left: `F2 Lower Right Flipper`, `F6 Upper Right Flipper`, `F4 Lower Left Flipper`, `F8 Upper Left Flipper`.
`FLIPTRONIC II BOARD` connector `J905`:

| J905 pin | Chip pin | Wire | Switch |
| --- | --- | --- | --- |
| 1 | (U4B-7) | Black-Yellow | F2 |
| 3 | (U6B-7) | Blue-Violet | F6 |
| 2 | (U4D-11) | Blue-Gray | F4 |
| 5 | (U6D-11) | Black-Blue | F8 |
| 6 |  | Orange | ground |

The four wires go to four opto switch symbols in `FLIPPER OPTO ASSEMBLIES` (two dashed groups of two, each opto
with a pull-up resistor to `+12V`). Below: a `Dedicated Input` drawing identical in form to PDF page 116's, a
`FLIPPER OPTO ASSEMBLY` box with connector `J1` (pins 3 and 6), `Cabinet Switch` opto, `470Ω` resistor, wires
`Blue-xxx`, `Black-xxx`, `Orange` and `Gray-Yellow`, and a `POWER DRIVER BOARD` `J116` pin 2 `+12V`. Truth table
printed as on page 116: `Open` `H` `H` `Off`, `Closed` `L` `L` `On`. The same two paragraphs of text as on
PDF page 116 are printed beneath (`The flipper switch circuits operate similar ...`).

## A-17316 Flipper Opto PCB Assembly (PDF page 118, printed 3-14)

Board drawing with `OPTO 1` and `OPTO 2`, resistors `R1` and `R2` (`470Ω` each in the schematic), and connector
`J1` with the pin-name legend printed beside it: `SW 1`, `SW 2`, `GND`, `GND`, `KEY`, `+12VDC`, `+12VDC` (pins 1 to
7 in that order). The schematic labels `J1` pins: 7 `+12VDC`, 6 `+12VDC`, 5 `KEY`, 1 `SW 1`, 2 `SW 2`, 3 `GND`,
4 `GND`.

`Left Side Flipper Cabinet Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J1-1 | Blue-Gray from Fliptronic II Board J905-2 |
| J1-2 | Black-Blue from Fliptronic II Board J905-5 |
| J1-3 | N/C |
| J1-4 | Orange from Fliptronic II Board J905-6 |
| J1-5 | N/C |
| J1-6 | Gray-Yellow from Fliptronic II Board J904-2 |
| J1-7 | Gray-Yellow from Fliptronic II Board J904-2 |

`Right Side Flipper Cabinet Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J1-1 | Black-Yellow from Fliptronic II Board J905-1 |
| J1-2 | Blue-Violet from Fliptronic II Board J905-3 |
| J1-3 | Orange from Fliptronic II Board J905-6 |
| J1-4 | Orange from Left Flipper Opto Assembly J1-4 |
| J1-5 | N/C |
| J1-6 | Gray-Yellow from Left Flipper Opto Assembly  J1-6 |
| J1-7 | N/C |

## Observations and internal disagreements (kept literal above, none resolved)

- Fliptronic II connector list (PDF page 135) prints `J905-1 Blue-Violet, F2, to right flipper opto switch board
  J1-1` and `J905-3 Black-Yellow, F6, to right flipper opto switch board J1-2`. PDF pages 115, 117 and 118 print
  J905-1 as `Black-Yellow` (F2, L. Right Flipper) and J905-3 as `Blue-Violet` (F6, U. Right Flipper). The two
  wire colours are swapped on the page 135 list; the pins, the F-numbers and the destination boards agree.
- The solenoid table block names solenoid 33 the `Claw Magnet` and keeps the printed circuit names `Up Rt.
  Power` / `Up Rt. Hold`; the footnote on PDF page 115 states `Upper right flipper power drive is used as the
  Claw magnet drive` and `Upper right flipper holding drive is not used`, and the solenoid table prints the hold
  row as `Not Used` with transistor `Q7`, `J902-4`, `Org-Vio` still listed.
- The cabinet-switch ground and `+12V` loops differ in detail between PDF page 117's upper drawing and the
  page 118 lists. The drawing joins the left board's harness pin 7 to the right board's harness pin 6 (`+12V`)
  and the left board's harness pin 4 to the right board's harness pin 3 (ground, dashed), with the left board's
  harness pin 3 going to J905 pin 6. The lists print the left board J1-3 and J1-4 both `Orange from Fliptronic II
  Board J905-6`, the right board J1-3 `Orange from Fliptronic II Board J905-6` and J1-4 `Orange from Left Flipper
  Opto Assembly J1-4`, and the right board J1-6 `Gray-Yellow from Left Flipper Opto Assembly J1-6`. The left list
  prints J1-6 and J1-7 as `Gray-Yellow from Fliptronic II Board J904-2` (the Fliptronic II list prints J904-2
  as `Gray-Green, +12V`), whereas PDF pages 115 and 117 draw the opto `+12V` as `Gray-Yellow +12V` from
  Power Driver Board `J116` pin 2. These are wire-routing details of the same ground and +12V nets; the switch
  wires themselves agree on every page apart from the colour swap above.
- PDF page 115 draws the 50Vac pair (`White-Blue 50Vac`, Fliptronic II `J901` pins 1 and 5) going to Power
  Driver Board connector `J105` pins 1 and 2, while the Power Driver Board list (PDF page 136) prints the
  50VAC wires on `J104-1` and `J104-2` (to Fliptronic II `J901-3` and `J901-1`) and prints `J105` as all `N/C`,
  and the Fliptronic II list prints `J901-1 ... from Power Driver Board J104-2`, `J901-3 ... from Power Driver
  Board J104-1`. The connector label on the page 115 drawing differs from both lists.
- `F5` and `F6` (upper right end-of-stroke and cabinet switch) are marked `*` and `*Not used on this game.` on
  PDF page 115; the Fliptronic list (PDF page 135) prints `J906-4 Black-Violet, F5, to upper right EOS switch
  (not used)`.
