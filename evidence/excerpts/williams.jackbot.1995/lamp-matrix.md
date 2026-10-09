# Jack*Bot — Lamp Matrix (wiring)

Transcribed from `Williams_1995_Jack_Bot_English_Manual.pdf` (SHA-256
`8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`), PDF page 112, printed page `2-34`: the
`Lamp Matrix` table with its column and row headers, the 64 cells and the footnote. The same table is reprinted in
Section 3 on PDF page 122 (printed `3-4`) and in the quick-reference sheet on PDF page 149 (upper half, no printed
folio); both were read as well. Read from the rendered page (300 dpi scan), not from OCR text. Transcriber:
curator, read from the rendered page.

The title line prints `Lamp Matrix`, then at the right: the label `YELLOW (B+)`, a lamp (bulb) symbol drawn as a
circle with a loop, a diode (arrow and bar), and the label `RED`. The diode is printed on all three printings.

## Matrix drive columns

Each column header prints, top to bottom: the column number, the wire (on two lines, e.g. `Yellow-` over `Brown`),
the connector-pin and the drive transistor.

| Column | Wire | Connector-pin | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J137-1 | Q98 |
| 2 | Yellow-Red | J137-2 | Q97 |
| 3 | Yellow-Orange | J137-3 | Q96 |
| 4 | Yellow-Black | J137-4 | Q95 |
| 5 | Yellow-Green | J137-5 | Q94 |
| 6 | Yellow-Blue | J137-6 | Q93 |
| 7 | Yellow-Violet | J137-7 | Q92 |
| 8 | Yellow-Gray | J137-9 | Q91 |

The top-left corner cell of the grid is divided diagonally and prints `COLUMN` and `ROW`. Column 8's
connector-pin is `J137-9` (there is no `J137-8` column). Column 5's wire `Yellow-Green` is printed as `Yellow-`
over `Green` like the others.

## Matrix return rows

Each row header prints, top to bottom: the wire, the connector-pin, the transistor and the row number (large, lower
left; in row 2 the numeral `2` stands at the far left, below the transistor, slightly lower than in the others).

| Row | Wire | Connector-pin | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J134-1 | Q90 |
| 2 | Red-Black | J134-2 | Q89 |
| 3 | Red-Orange | J134-4 | Q88 |
| 4 | Red-Yellow | J134-5 | Q87 |
| 5 | Red-Green | J134-6 | Q87 |
| 6 | Red-Blue | J134-7 | Q86 |
| 7 | Red-Violet | J134-8 | Q84 |
| 8 | Red-Gray | J134-9 | Q83 |

The row connector pins skip `J134-3` (row 2 is `J134-2`, row 3 is `J134-4`). The row transistors as printed are
`Q90, Q89, Q88, Q87, Q87, Q86, Q84, Q83`: **`Q87` is printed on both row 4 and row 5, and `Q85` is not printed
anywhere**, so the sequence breaks. This is the same on all three printings (checked on each at 2.5-3x; the row 5 `Q87` is
clearly an `87`, not `86` or `85`). Likely a misprint (the descending series would give row 5 `Q86`, row 6 `Q85`,
row 7 `Q84`), but it is transcribed as printed and the pattern itself is not proof of which numbers are wrong.

## Matrix cells

Each cell prints its description (multi-line text joined here by single spaces) and the two-digit lamp number in
its bottom-right corner, column digit first, row digit second. No cell carries a colour or bulb marking other than
the colour word in the description itself (`YELLOW`, `BLUE`, `AMBER`, `GREEN`, `RED`), and no cell is shaded.
`JACK•BOT` is printed with a centred bullet (`•`) between the two words, no spaces.

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 YELLOW ARROW | 21 BLUE ARROW | 31 AMBER ARROW | 41 GREEN ARROW |
| 2 | 12 YELLOW 1 (HIGH) | 22 BLUE 1 (HIGH) | 32 AMBER 1 (HIGH) | 42 GREEN 1 (HIGH) |
| 3 | 13 YELLOW 2 | 23 BLUE 2 | 33 AMBER 2 | 43 GREEN 2 |
| 4 | 14 YELLOW 3 | 24 BLUE 3 | 34 AMBER 3 | 44 GREEN 3 |
| 5 | 15 YELLOW 4 | 25 BLUE 4 | 35 AMBER 4 | 45 GREEN 4 |
| 6 | 16 YELLOW 5 (LOW) | 26 BLUE 5 (LOW) | 36 AMBER 5 (LOW) | 46 GREEN 5 (LOW) |
| 7 | 17 LEFT OUTLANE | 27 BONUS 2X | 37 SHOOT AGAIN | 47 BONUS 5X |
| 8 | 18 LEFT FLIPPER LANE | 28 BONUS 3X | 38 BONUS 4X | 48 JACK•BOT (TARGET) |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 RED ARROW | 61 CARD 1 (LEFT) | 71 CASHIER MINI-PLFD | 81 PINBOT POKER |
| 2 | 52 RED 1 (HIGH) | 62 CARD 2 | 72 MEGA RAMP MINI-PLFD | 82 SLOT MACHINE |
| 3 | 53 RED 2 | 63 CARD 3 | 73 LIGHT EX. BALL MINI-PLFD | 83 ROLL THE DICE |
| 4 | 54 RED 3 | 64 CARD 4 | 74 JACK•BOT MINI-PLFD | 84 KENO |
| 5 | 55 RED 4 | 65 CARD 5 (RIGHT) | 75 GAME SAUCER | 85 CASHIER (UNDER RAMP) |
| 6 | 56 RED 5 (LOW) | 66 CASINO RUN | 76 MEGA RAMP | 86 JACK•BOT (RAMP) |
| 7 | 57 RIGHT FLIPPER LANE | 67 HIT ME | 77 HIGH DROP TARGET | 87 BUY-IN BUTTON |
| 8 | 58 RIGHT OUTLANE | 68 LOW DROP TARGET | 78 CENTER DROP TARGET | 88 START BUTTON |

Notes on the cell text:

- Cells 12, 22, 32, 42, 52 print three lines `<COLOUR>` / `1` / `(HIGH)`; cells 16, 26, 36, 46, 56 print `<COLOUR>`
  / `5` / `(LOW)`.
- Cell 61 prints `CARD` / `1` / `(LEFT)`; cell 65 prints `CARD` / `5` / `(RIGHT)` (the `(RIGHT)` touches the digits
  `65`); cells 62-64 print `CARD` / `2`, `3`, `4`.
- Cell 71 prints `CASHIER` / `MINI-PLFD`; 72 `MEGA` / `RAMP` / `MINI-PLFD`; 73 `LIGHT` / `EX. BALL` / `MINI-PLFD`; 74
  `JACK•BOT` / `MINI-PLFD`. Each `MINI-PLFD` line touches the right border of its cell.
- Cell 85 prints `CASHIER` / `(UNDER` / `RAMP)` and the `RAMP)` touches the digits `85`.
- Cell 67 prints `HIT ME` with a double space; cell 83 prints `ROLL` / `THE` / `DICE`.
- Cell 18 shows a small stray mark just left of the digits `18` (a speck on the scan, not a character).
- Cells 87 and 88 print `BUY-IN` / `BUTTON` and `START` / `BUTTON`.

## Footnote

`J1XX = POWER DRIVER BOARD` (printed below the table, left). Printed folio `2-34`.

## The reprints (PDF page 122, printed `3-4`; PDF page 149 upper half)

PDF page 122 (printed `3-4`) is headed `LAMP MATRIX` and reprints the whole table at a smaller scale, with the
title-line drawing (`YELLOW (B+)`, lamp, diode, `RED`), the footnote `J1XX = POWER DRIVER BOARD`, a `LAMP MATRIX
CIRCUIT` drawing and explanatory text. The circuit drawing prints a `POWER DRIVER BOARD` box with a `Column
(example)` circuit (`J113`, `LS240`, `LS374`, `ULN-2803` with points `A` and `B`, `560`, `1.2K`, `TIP107`, `+18V`, to
`J137` with wire `Yellow-XXX` and a lamp and a diode in the `PLAYFIELD`) and a `Row (example)` circuit (`J134`,
`Red-XXX`, `LS74` with `D`, `CLK`, `Q`, points `E`, `F`, `G`, `1K`, `TIP102`, `.2`, `.22mf`, `1.4V ref`, `LM339`, `10K` to
`VCC`), with the truth tables `COLUMN | A | B`: `H L OFF`, `L H ON` and `ROW | C | D | E | F | G`: `NORMAL H L H L H OFF`,
`OPERATION H L L H L ON`. Its text reads: `The microprocessor sends a signal to the column circuit causing the
output of the UNL-2803 to toggle. When point "A" drops low, the TIP107 transistor conducts and point "B" changes to a
high state. At the same time, the microprocessor drives the input of the 74LS74 low, causing a high at output "F". A
high state at the base of the TIP102 causes the transistor to conducts, bringing the row circuit to ground and
turning the lamp on.` / `The microprocessor changes the input of the 74LS74 to a high state to turn the lamp off.` /
`In overcurrent conditions, the lamp is shut off through the comparator. If the voltage at the negative input of the
LM339 rises above 1.4V, the output changes to a low, which is fed back to the 74LS74 and shuts the row circuit off.`
(Printed typos `UNL-2803` and `to conducts`; the circuit drawing and text are not part of the matrix evidence.)

PDF page 149 holds the quick-reference sheet: the Lamp Matrix in the upper half, titled `LAMP MATRIX`, and the Switch
Matrix in the lower half (`switch-matrix.md`). It carries no folio.

Every header and cell of both reprints was compared with the `2-34` reading above, tile by tile, and agrees:
the column headers `J137-1 Q98` ... `J137-9 Q91`, the row headers `J134-1 Q90`, `J134-2 Q89`, `J134-4 Q88`, `J134-5 Q87`,
`J134-6 Q87`, `J134-7 Q86`, `J134-8 Q84`, `J134-9 Q83`, all 64 cell texts and addresses, and the footnote.

Differences found: none in any wire, connector-pin, transistor, lamp number or description. Only scan quality
and scale differ (page 112 is the largest and sharpest; 122 is smaller; 149 is smaller still and a little softer),
and the title text face (`Lamp Matrix` in mixed case on `2-34`, `LAMP MATRIX` in capitals on the two reprints).

## Cross-check with the lamp parts list (`lamp-locations.md`, PDF page 113, printed `2-35`)

The parts list does not agree with the matrix for the four mini-playfield lamps. The matrix prints 71 `CASHIER
MINI-PLFD`, 72 `MEGA RAMP MINI-PLFD`, 73 `LIGHT EX. BALL MINI-PLFD`, 74 `JACK•BOT MINI-PLFD`; the parts list prints 71
`Light Ex. Ball (Mini Plfd)`, 72 `Mega Ramp (Mini Plfd)`, 73 `Cashier (Mini Plfd)`, 74 `25 Million (Mini Plfd)`. Cells 71
and 73 are swapped between the two, and 74 differs in name. Every other cell's description matches the parts list
(allowing for capitalisation and for `Jack•Bot (Target)` / `(Ramp)` against `JACK•BOT (TARGET)` / `(RAMP)`, which
agree).

## Suspected typos and anomalies

- Row 4 and row 5 both print `Q87` (see above); the 8-step transistor series has no `Q85`.
- Column connector pins skip `J137-8`; row connector pins skip `J134-3`. Both are as printed on all three
  printings.
- The matrix and the parts list disagree on lamps 71, 73 and 74 (above).

## Uncertain readings

None in the matrix text. The row 5 transistor `Q87` was checked on all three printings at 2.5-3x enlargement because of the
duplicate; it reads `Q87` each time (as does row 4).
