# Demolition Man — Lamp Matrix

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF page 98,
printed page `DEMOLITION MAN 2-42`, the `LAMPS` matrix table. Read from the rendered page
(308 dpi 1-bit scan), not from the OCR text.

The page carries only this table. Above the top-right corner of the table a legend is printed: the text
`Yellow (B+)` under a line that runs through a lamp symbol (a circle with three spokes) and a diode symbol
(triangle pointing right with a bar) to the text `Red`. It shows each lamp wired between a column (yellow
wire, B+ side) and a row (red wire, through the diode). The diagonal-split corner cell of the table reads
`Column` (upper right) and `Row` (lower left). Each cell prints its label centered and its lamp number in
bold at the lower right; the row number (1 to 8) is printed in bold at the lower left of each row header.
Label text wraps over two or three printed lines inside a cell; the wrap is joined with single spaces below.
In every cell the printed number equals `10 * column + row` (for example column 3, row 2 is `32`); that is an
observation about the printed numbers, not a printed rule.

No cell carries a colour, bulb or insert mark, and no cell is shaded: all 64 cells were checked by eye and by
measuring the dark-pixel fraction of every cell (0.06 to 0.17, against 0.28 to 0.38 for the halftone cells of
the switch matrix on the PDF page 139 reprint). The reprints were checked by eye only. There are no footnotes, asterisks or daggers on the page. No
cell is blank; the two unused positions print the words `Not Used`.

The same table is reprinted on PDF page 108 (Section 3, printed `DEMOLITION MAN 3-4`) and on PDF page 139
(a foldout chart that pairs it with the switch matrix). Those are copies of the same table, not independent
sources; every difference is listed under "Differences from the reprints".

## Column headers

Each column header prints, on separate lines, the column number, the wire colour, the connector pin and the
drive transistor.

| Column | Wire colour | Connector-pin | Transistor |
| ---: | --- | --- | --- |
| 1 | Yellow-Brown | J137-1 | Q98 |
| 2 | Yellow-Red | J137-2 | Q97 |
| 3 | Yellow-Orange | J137-3 | Q96 |
| 4 | Yellow-Black | J137-4 | Q95 |
| 5 | Yellow-Green | J137-5 | Q94 |
| 6 | Yellow-Blue | J137-6 | Q93 |
| 7 | Yellow-Violet | J137-7 | Q92 |
| 8 | Yellow-Gray | J137-9 | Q91 |

Column 8 prints `J137-9`; no column prints `J137-8`.

## Row headers

Each row header prints the wire colour, the connector pin and the drive transistor, with the row number at the
lower left.

| Row | Wire colour | Connector-pin | Transistor |
| ---: | --- | --- | --- |
| 1 | Red-Brown | J133-1 | Q90 |
| 2 | Red-Black | J133-2 | Q89 |
| 3 | Red-Orange | J133-4 | Q88 |
| 4 | Red-Yellow | J133-5 | Q87 |
| 5 | Red-Green | J133-6 | Q86 |
| 6 | Red-Blue | J133-7 | Q85 |
| 7 | Red-Violet | J133-8 | Q84 |
| 8 | Red-Gray | J133-9 | Q83 |

The row connector pins print as `J133-1`, `J133-2`, `J133-4`, `J133-5`, `J133-6`, `J133-7`, `J133-8`, `J133-9`:
`J133-3` is not printed, row 3 is `J133-4`. The reprints on PDF pages 108 and 139 print `J134-` for every row,
see the differences section.

## Matrix cells

Cell format: `lamp number` then the printed label. Rows are the table rows, columns the table columns.

| Row \ Column | 1 (Yellow-Brown) | 2 (Yellow-Red) | 3 (Yellow-Orange) | 4 (Yellow-Black) | 5 (Yellow-Green) | 6 (Yellow-Blue) | 7 (Yellow-Violet) | 8 (Yellow-Gray) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (Red-Brown) | `11` Ball Save | `21` Right Ramp Jackpot | `31` Right Loop Jackpot | `41` Right Ramp Explode | `51` Underground Arrow | `61` Claw "Capture Simon" | `71` "Super Jackpot" | `81` Center Ramp Middle |
| 2 (Red-Black) | `12` Fortress Multiball | `22` Right Loop Explode | `32` Standup 5 | `42` Right Ramp Car Chase | `52` Underground Jackpot | `62` Claw "Sup. Jets" | `72` "Computer" | `82` Center Ramp Outer |
| 3 (Red-Orange) | `13` Museum Multiball | `23` Light Quick Freeze | `33` Right Ramp Arrow | `43` Quick Freeze | `53` Standup 2 | `63` Claw "Prison Break" | `73` "Demo Time" | `83` Center Ramp Inner |
| 4 (Red-Yellow) | `14` Cryoprison Multiball | `24` Freeze 4 | `34` Left Ramp Jackpot | `44` Left Ramp Car Chase | `54` Left Ramp Arrow | `64` Claw "Freeze" | `74` Not Used | `84` Center Ramp Arrow |
| 5 (Red-Green) | `15` Wasteland Multiball | `25` Claw Ready | `35` Left Loop Jackpot | `45` Extra Ball | `55` Side Ramp Jackpot | `65` Claw "ACMAG" | `75` Not Used | `85` Right Loop Arrow |
| 6 (Red-Blue) | `16` Shoot Again | `26` Freeze 3 | `36` Car Crash Top | `46` Start Multiball | `56` Side Ramp Arrow | `66` Middle Rollover | `76` Standup 4 | `86` Buy-in Button |
| 7 (Red-Violet) | `17` Access Claw | `27` Freeze 2 | `37` Standup 1 | `47` Car Crash Bottom | `57` Left Loop Arrow | `67` Top Rollover | `77` Standup 3 | `87` Ball Launch |
| 8 (Red-Gray) | `18` Left Ramp Explode | `28` Freeze 1 | `38` Car Crash Center | `48` Left Loop Explode | `58` Center Ramp Jackpot | `68` Lower Rollover | `78` Retina Scan | `88` Start Button |

## Cell list (same data, one cell per row)

| Lamp | Row | Row wire | Row pin | Row transistor | Column | Column wire | Column pin | Column transistor | Printed label |
| ---: | ---: | --- | --- | --- | ---: | --- | --- | --- | --- |
| 11 | 1 | Red-Brown | J133-1 | Q90 | 1 | Yellow-Brown | J137-1 | Q98 | Ball Save |
| 12 | 2 | Red-Black | J133-2 | Q89 | 1 | Yellow-Brown | J137-1 | Q98 | Fortress Multiball |
| 13 | 3 | Red-Orange | J133-4 | Q88 | 1 | Yellow-Brown | J137-1 | Q98 | Museum Multiball |
| 14 | 4 | Red-Yellow | J133-5 | Q87 | 1 | Yellow-Brown | J137-1 | Q98 | Cryoprison Multiball |
| 15 | 5 | Red-Green | J133-6 | Q86 | 1 | Yellow-Brown | J137-1 | Q98 | Wasteland Multiball |
| 16 | 6 | Red-Blue | J133-7 | Q85 | 1 | Yellow-Brown | J137-1 | Q98 | Shoot Again |
| 17 | 7 | Red-Violet | J133-8 | Q84 | 1 | Yellow-Brown | J137-1 | Q98 | Access Claw |
| 18 | 8 | Red-Gray | J133-9 | Q83 | 1 | Yellow-Brown | J137-1 | Q98 | Left Ramp Explode |
| 21 | 1 | Red-Brown | J133-1 | Q90 | 2 | Yellow-Red | J137-2 | Q97 | Right Ramp Jackpot |
| 22 | 2 | Red-Black | J133-2 | Q89 | 2 | Yellow-Red | J137-2 | Q97 | Right Loop Explode |
| 23 | 3 | Red-Orange | J133-4 | Q88 | 2 | Yellow-Red | J137-2 | Q97 | Light Quick Freeze |
| 24 | 4 | Red-Yellow | J133-5 | Q87 | 2 | Yellow-Red | J137-2 | Q97 | Freeze 4 |
| 25 | 5 | Red-Green | J133-6 | Q86 | 2 | Yellow-Red | J137-2 | Q97 | Claw Ready |
| 26 | 6 | Red-Blue | J133-7 | Q85 | 2 | Yellow-Red | J137-2 | Q97 | Freeze 3 |
| 27 | 7 | Red-Violet | J133-8 | Q84 | 2 | Yellow-Red | J137-2 | Q97 | Freeze 2 |
| 28 | 8 | Red-Gray | J133-9 | Q83 | 2 | Yellow-Red | J137-2 | Q97 | Freeze 1 |
| 31 | 1 | Red-Brown | J133-1 | Q90 | 3 | Yellow-Orange | J137-3 | Q96 | Right Loop Jackpot |
| 32 | 2 | Red-Black | J133-2 | Q89 | 3 | Yellow-Orange | J137-3 | Q96 | Standup 5 |
| 33 | 3 | Red-Orange | J133-4 | Q88 | 3 | Yellow-Orange | J137-3 | Q96 | Right Ramp Arrow |
| 34 | 4 | Red-Yellow | J133-5 | Q87 | 3 | Yellow-Orange | J137-3 | Q96 | Left Ramp Jackpot |
| 35 | 5 | Red-Green | J133-6 | Q86 | 3 | Yellow-Orange | J137-3 | Q96 | Left Loop Jackpot |
| 36 | 6 | Red-Blue | J133-7 | Q85 | 3 | Yellow-Orange | J137-3 | Q96 | Car Crash Top |
| 37 | 7 | Red-Violet | J133-8 | Q84 | 3 | Yellow-Orange | J137-3 | Q96 | Standup 1 |
| 38 | 8 | Red-Gray | J133-9 | Q83 | 3 | Yellow-Orange | J137-3 | Q96 | Car Crash Center |
| 41 | 1 | Red-Brown | J133-1 | Q90 | 4 | Yellow-Black | J137-4 | Q95 | Right Ramp Explode |
| 42 | 2 | Red-Black | J133-2 | Q89 | 4 | Yellow-Black | J137-4 | Q95 | Right Ramp Car Chase |
| 43 | 3 | Red-Orange | J133-4 | Q88 | 4 | Yellow-Black | J137-4 | Q95 | Quick Freeze |
| 44 | 4 | Red-Yellow | J133-5 | Q87 | 4 | Yellow-Black | J137-4 | Q95 | Left Ramp Car Chase |
| 45 | 5 | Red-Green | J133-6 | Q86 | 4 | Yellow-Black | J137-4 | Q95 | Extra Ball |
| 46 | 6 | Red-Blue | J133-7 | Q85 | 4 | Yellow-Black | J137-4 | Q95 | Start Multiball |
| 47 | 7 | Red-Violet | J133-8 | Q84 | 4 | Yellow-Black | J137-4 | Q95 | Car Crash Bottom |
| 48 | 8 | Red-Gray | J133-9 | Q83 | 4 | Yellow-Black | J137-4 | Q95 | Left Loop Explode |
| 51 | 1 | Red-Brown | J133-1 | Q90 | 5 | Yellow-Green | J137-5 | Q94 | Underground Arrow |
| 52 | 2 | Red-Black | J133-2 | Q89 | 5 | Yellow-Green | J137-5 | Q94 | Underground Jackpot |
| 53 | 3 | Red-Orange | J133-4 | Q88 | 5 | Yellow-Green | J137-5 | Q94 | Standup 2 |
| 54 | 4 | Red-Yellow | J133-5 | Q87 | 5 | Yellow-Green | J137-5 | Q94 | Left Ramp Arrow |
| 55 | 5 | Red-Green | J133-6 | Q86 | 5 | Yellow-Green | J137-5 | Q94 | Side Ramp Jackpot |
| 56 | 6 | Red-Blue | J133-7 | Q85 | 5 | Yellow-Green | J137-5 | Q94 | Side Ramp Arrow |
| 57 | 7 | Red-Violet | J133-8 | Q84 | 5 | Yellow-Green | J137-5 | Q94 | Left Loop Arrow |
| 58 | 8 | Red-Gray | J133-9 | Q83 | 5 | Yellow-Green | J137-5 | Q94 | Center Ramp Jackpot |
| 61 | 1 | Red-Brown | J133-1 | Q90 | 6 | Yellow-Blue | J137-6 | Q93 | Claw "Capture Simon" |
| 62 | 2 | Red-Black | J133-2 | Q89 | 6 | Yellow-Blue | J137-6 | Q93 | Claw "Sup. Jets" |
| 63 | 3 | Red-Orange | J133-4 | Q88 | 6 | Yellow-Blue | J137-6 | Q93 | Claw "Prison Break" |
| 64 | 4 | Red-Yellow | J133-5 | Q87 | 6 | Yellow-Blue | J137-6 | Q93 | Claw "Freeze" |
| 65 | 5 | Red-Green | J133-6 | Q86 | 6 | Yellow-Blue | J137-6 | Q93 | Claw "ACMAG" |
| 66 | 6 | Red-Blue | J133-7 | Q85 | 6 | Yellow-Blue | J137-6 | Q93 | Middle Rollover |
| 67 | 7 | Red-Violet | J133-8 | Q84 | 6 | Yellow-Blue | J137-6 | Q93 | Top Rollover |
| 68 | 8 | Red-Gray | J133-9 | Q83 | 6 | Yellow-Blue | J137-6 | Q93 | Lower Rollover |
| 71 | 1 | Red-Brown | J133-1 | Q90 | 7 | Yellow-Violet | J137-7 | Q92 | "Super Jackpot" |
| 72 | 2 | Red-Black | J133-2 | Q89 | 7 | Yellow-Violet | J137-7 | Q92 | "Computer" |
| 73 | 3 | Red-Orange | J133-4 | Q88 | 7 | Yellow-Violet | J137-7 | Q92 | "Demo Time" |
| 74 | 4 | Red-Yellow | J133-5 | Q87 | 7 | Yellow-Violet | J137-7 | Q92 | Not Used |
| 75 | 5 | Red-Green | J133-6 | Q86 | 7 | Yellow-Violet | J137-7 | Q92 | Not Used |
| 76 | 6 | Red-Blue | J133-7 | Q85 | 7 | Yellow-Violet | J137-7 | Q92 | Standup 4 |
| 77 | 7 | Red-Violet | J133-8 | Q84 | 7 | Yellow-Violet | J137-7 | Q92 | Standup 3 |
| 78 | 8 | Red-Gray | J133-9 | Q83 | 7 | Yellow-Violet | J137-7 | Q92 | Retina Scan |
| 81 | 1 | Red-Brown | J133-1 | Q90 | 8 | Yellow-Gray | J137-9 | Q91 | Center Ramp Middle |
| 82 | 2 | Red-Black | J133-2 | Q89 | 8 | Yellow-Gray | J137-9 | Q91 | Center Ramp Outer |
| 83 | 3 | Red-Orange | J133-4 | Q88 | 8 | Yellow-Gray | J137-9 | Q91 | Center Ramp Inner |
| 84 | 4 | Red-Yellow | J133-5 | Q87 | 8 | Yellow-Gray | J137-9 | Q91 | Center Ramp Arrow |
| 85 | 5 | Red-Green | J133-6 | Q86 | 8 | Yellow-Gray | J137-9 | Q91 | Right Loop Arrow |
| 86 | 6 | Red-Blue | J133-7 | Q85 | 8 | Yellow-Gray | J137-9 | Q91 | Buy-in Button |
| 87 | 7 | Red-Violet | J133-8 | Q84 | 8 | Yellow-Gray | J137-9 | Q91 | Ball Launch |
| 88 | 8 | Red-Gray | J133-9 | Q83 | 8 | Yellow-Gray | J137-9 | Q91 | Start Button |

## Differences from the reprints

Compared cell by cell (all 64 labels and numbers, all 8 column headers, all 8 row headers) with the reprint on
PDF page 108 (printed `DEMOLITION MAN 3-4`) and the reprint on PDF page 139 (no printed folio).

| Item | PDF page 98 (2-42) | PDF page 108 (3-4) | PDF page 139 |
| --- | --- | --- | --- |
| Row 1 connector pin | `J133-1` | `J134-1` | `J134-1` |
| Row 2 connector pin | `J133-2` | `J134-2` | `J134-2` |
| Row 3 connector pin | `J133-4` | `J134-4` | `J134-4` |
| Row 4 connector pin | `J133-5` | `J134-5` | `J134-5` |
| Row 5 connector pin | `J133-6` | `J134-6` | `J134-6` |
| Row 6 connector pin | `J133-7` | `J134-7` | `J134-7` |
| Row 7 connector pin | `J133-8` | `J134-8` | `J134-8` |
| Row 8 connector pin | `J133-9` | `J134-9` | `J134-9` |

There is no other difference: the 8 column headers (number, wire colour, `J137-` pin, transistor), the 8 row
wire colours and transistors, the legend, and all 64 lamp numbers and labels, including the wrap points of the
label lines and the two `Not Used` cells (74, 75), read identically on all three printings. No printing
shades any lamp cell.

The only discrepancy is the row connector designator, `J133` here against `J134` on both reprints. The
connector-list page 138 (printed `DEMOLITION MAN 3-34`, `Power Driver Board Continued...`) is a further place that
prints the pins, read here only for the following lines. It lists `J133-1` to `J133-6` as `N/C`, `J133-7`
`Red-Blue, lamp row 6, not used`, `J133-8` `Red-Violet, lamp row 7, to cabinet`, `J133-9` `Red-Gray, lamp row 8, to
cabinet`; `J134-1` `Red-Brown, lamp row 1, to playfield lamps`, `J134-2` `Red-Black, lamp row 2, to playfield
lamps`, `J134-3` `N/C`, `J134-4` `Red-Orange, lamp row 3, to playfield lamps`, `J134-5` `Red-Yellow, lamp row 4`,
`J134-6` `Red-Green, lamp row 5`, `J134-7` `Red-Blue, lamp row 6`, `J134-8` `Red-Violet, lamp row 7`, `J134-9`
`Red-Gray, lamp row 8` (each `to playfield lamps`); `J136-3` `Yellow-Gray, lamp column 8, to cabinet`; `J137-1` to
`J137-7` `Yellow-<colour>, lamp column 1` to `7, to playfield lamps`, `J137-8` `N/C`, `J137-9` `Yellow-Gray, lamp
column 8, to playfield lamps`. That list uses `J134` with the same pin numbers (`-1`, `-2`, `-4` to `-9`, `-3`
unused) as the reprints, so the `J133-` prefix on this page agrees with the reprints in everything but the
connector number. This is a wiring-detail disagreement only (the colour, pin suffix and transistor agree).

## Lamp Matrix Circuit (printed on PDF page 108 only)

The Section 3 reprint on PDF page 108 also prints a `Lamp Matrix Circuit` schematic and text that this page 98
does not carry. It is transcribed here because it names the drivers.

Schematic labels read: `POWER DRIVER BOARD`; `Column (example)`: connector `J113`, `LS240`, `LS374`,
`ULN-2803` (output `A`, `560Ω` series resistor), `+18V`, `1.2KΩ`, `TIP 107` (output `B`), connector `J137`, wire
`Yel-xxx`, then `Playfield` with a lamp symbol and a diode, wire `Red-xxx` back to connector `J134`; `Row
(example)`: `G` from `J113`, `74LS74` (inputs `D`, `Clk`, outputs `Q`, `Q` bar, node `F`), `TIP102` (node `E`),
`.2Ω`, `1KΩ`, `.22µf` (node `D`), `LM339` comparator (output `C`, `1.4V ref`, `VCC`, `10KΩ`).

Truth tables printed beside it:

| Column | A | B | |
| --- | --- | --- | --- |
| | H | L | Off |
| | L | H | On |

| Row | C | D | E | F | G | |
| --- | --- | --- | --- | --- | --- | --- |
| (normal operation) | H | L | H | L | H | Off |
| (normal operation) | H | L | L | H | L | On |

Text printed below it, verbatim:

> The processor sends a signal to the column circuit causing the output of the UNL-2803 to toggle. When point
> "A" drops low, the TIP107 transistor conducts and point "B" changes to a high state. At the same time the
> processor drives the input of the 74LS74 low, causing a high at output "F". A high state at the base of
> TIP102 causes the transistor to conduct bringing the row circuit to ground and turning the lamp On.
>
> The processor changes the input of the 74LS74 to a high state to turn the lamp Off.
>
> In overcurrent conditions the lamp is shut Off through the comparator. If the voltage at the negative input of
> the LM339 rises above 1.4V the output changes to a low, which is fed back to the 74LS74 and shuts the row
> circuit Off.

## Additional: switch matrix and grounded switches as printed on PDF page 139

PDF page 139 (no printed folio; the page has no footer) is a foldout chart. Its upper half is the `LAMPS` matrix
above (the `J134-` reprint); its lower half is a `SWITCHES` chart carrying three blocks: `Dedicated Grounded
Switches` (left), the switch matrix (centre) and `Flipper Grounded Switches` (right). It is transcribed here
because it is on the page that was asked for. The same switch chart is printed on PDF page 100; that page is
transcribed separately and this chart is a copy of it, so it is not independent evidence for it. It was not
compared against page 100 here.

Above the switch matrix a legend shows a switch symbol: `Green` on the left, a normally drawn contact, a diode,
and `White` on the right. Below the matrix: a halftone swatch followed by `= Opto Switch`, then `* = Not Used`.
Cell format as in the lamp matrix: the switch number is printed at the lower right of each cell, the label centred.

### Switch matrix column headers

| Column | Wire colour | Connector-pin | Pin |
| ---: | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

The wire colour wraps over two printed lines after the hyphen (`Green-` / `Brown`). Column 8 prints `J207-9`;
no column prints `J207-8`.

### Switch matrix row headers

| Row | Wire colour | Connector-pin | Pin |
| ---: | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

The wire colour wraps over two printed lines after the hyphen on every row (`White-` / `Brown`, and so on). Row 8
prints `J209-9`; no row prints `J209-6`.

### Switch matrix cells

Shaded (halftone, `= Opto Switch`) cells are marked `[opto]`. Shading was found by eye and by measuring every
cell's dark-pixel fraction (0.28 to 0.38 for shaded cells, 0.07 to 0.19 for the rest). The shaded cells are 25, 26,
31, 32, 33, 34, 35, 36, 67, 71, 72, 73, 74 and 76 (14 cells). The cell with `Not Used` at 75 is not shaded;
the other `Not Used` cells (28, 37, 68) are not shaded either.

| Row \ Column | 1 (Green-Brown) | 2 (Green-Red) | 3 (Green-Orange) | 4 (Green-Yellow) | 5 (Green-Black) | 6 (Green-Blue) | 7 (Green-Violet) | 8 (Green-Gray) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (White-Brown) | `11` Ball Launch | `21` Slam Tilt | `31` Trough 1 [opto] | `41` Left Slingshot | `51` Left Ramp Enter | `61` Side Ramp Enter | `71` Chase Car 1 [opto] | `81` Claw "Capture Simon" |
| 2 (White-Red) | `12` Left Handle Button | `22` Coin Door Closed | `32` Trough 2 [opto] | `42` Right Slingshot | `52` Left Ramp Exit | `62` Side Ramp Exit | `72` Chase Car 2 [opto] | `82` Claw "Sup. Jets" |
| 3 (White-Orange) | `13` Start Button | `23` Buy-in Button | `33` Trough 3 [opto] | `43` Left Jet Bumper | `53` Center Ramp | `63` Left Rollover | `73` Top Popper [opto] | `83` Claw "Prison Break" |
| 4 (White-Yellow) | `14` Plumb Bob Tilt | `24` Always Closed | `34` Trough 4 [opto] | `44` Top Slingshot | `54` Upper Rebound | `64` Center Rollover | `74` Elevator Hold [opto] | `84` Claw "Freeze" |
| 5 (White-Green) | `15` Left Outlane | `25` Claw Position 1 [opto] | `35` Trough 5 [opto] | `45` Right Jet Bumper | `55` Left Loop | `65` Right Rollover | `75` Not Used | `85` Claw "ACMAG" |
| 6 (White-Blue) | `16` Left Inlane | `26` Claw Position 2 [opto] | `36` Trough Jam [opto] | `46` Right Ramp Enter | `56` Standup 2 | `66` Eject | `76` Bottom Popper [opto] | `86` Upper Left Flipper Gate |
| 7 (White-Violet) | `17` Right Inlane | `27` Shooter Lane | `37` Not Used | `47` Right Ramp Exit | `57` Standup 3 | `67` Elevator Index [opto] | `77` Eyeball Standup | `87` Car Chase Standup |
| 8 (White-Gray) | `18` Right Outlane | `28` Not Used | `38` Standup 5 | `48` Right Freeway | `58` Standup 4 | `68` Not Used | `78` Standup 1 | `88` Lower Rebound |

### Dedicated Grounded Switches (left block)

| Switch | Wire colour | Connector-pin | Printed label |
| --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | Normal Function: Service Credits; Test Function: Escape |
| D6 | Orange-Blue | J205-7 | Normal Function: Volume Down; Test Function: Down |
| D7 | Orange-Violet | J205-8 | Normal Function: Volume Up; Test Function: Up |
| D8 | Orange-Gray | J205-9 | Normal Function: Begin Test; Test Function: Enter |

D5 to D8 print two small labelled columns separated by a vertical bar, `Normal Function` and `Test Function`.
No `J205-5` is printed.

### Flipper Grounded Switches (right block)

| Switch | Wire colour | Connector-pin | Printed label |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right E.O.S. |
| F2 | Blue-Violet | J905-1 | Lower Right Opto |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S. |
| F4 | Blue-Gray | J905-2 | Lower Left Opto |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S.* |
| F6 | Black-Yellow | J905-3 | Upper Right Opto* |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. |
| F8 | Black-Blue | J905-5 | Upper Left Opto |

`F5` and `F6` carry the asterisk (`* = Not Used` per the legend); the other six labels carry none. No flipper
cell is shaded. The two blocks print no `J906-2` or `J905-4`.
