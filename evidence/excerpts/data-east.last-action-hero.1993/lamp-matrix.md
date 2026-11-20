# Last Action Hero (Data East 1993) - Lamp Matrix Chart and Lamp Descriptions

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 30 and 31 (PDF 34 and 35) of the IPDB scan `Data_East_1993_Last_Action_Hero_Manual.pdf`. The scan has no text layer, so every cell below was read from the render.

Printed page 30 states: `Controlled lamps are configured in an 8 x 8 matrix of columns (lamp drives) and rows (lamp returns) with up to 64 lamps possible.` Its Single Lamp text says `The top display indicates lamp name. The bottom display indicates the row and column wire colors and the lamp matrix number. Lamp 01 should light. With the FORWARD/REVERSE push-button switch in the FORWARD (up) position, operating the Game Start push-button switch selects higher-numbered lamps; with it in the REVERSE (down) position, Game Start selects lower-numbered lamps.`

The chart prints a column header per column (column number, drive transistor, wire colour pair, CPU connector pin) and a row header per row (row number, return transistor, wire colour pair, connector pin). Address = (column - 1) x 8 + row, the number printed in the lower right of each cell.

## Column drives (printed header row)

| Column | Drive transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q71 | YEL-BRN | CN7-1 |
| 2 | Q70 | YEL-RED | CN7-2 |
| 3 | Q69 | YEL-ORN | CN7-3 |
| 4 | Q68 | YEL-BLK | CN7-4 |
| 5 | Q67 | YEL-GRN | CN7-6 |
| 6 | Q66 | YEL-BLU | CN7-7 |
| 7 | Q65 | YEL-VIO | CN7-8 |
| 8 | Q64 | YEL-GRY | CN7-9 |

Column 2's wire is printed `YEL- RED` with a space; the transcription closes it up. CN7 pin 5 is not used by any column.

## Row returns (printed header column)

| Row | Return transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q72 | RED-BRN | CN6-1 |
| 2 | Q73 | RED-BLK | CN6-2 |
| 3 | Q74 | RED-ORN | CN6-3 |
| 4 | Q75 | RED-YEL | CN6-5 |
| 5 | Q76 | RED-GRN | CN6-6 |
| 6 | Q77 | RED-BLU | CN6-7 |
| 7 | Q78 | RED-VIO | CN6-8 |
| 8 | Q79 | RED-GRY | CN6-9 |

CN6 pin 4 is not used by any row. Row 3's wire is printed `RED-0RN` with a slashed zero, as the chart's typeface prints every O.

## Lamp Matrix Chart

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Grid: Find Benedict |
| 2 | 1 | 2 | Grid: Last |
| 3 | 1 | 3 | Grid: Action |
| 4 | 1 | 4 | Grid: Hero |
| 5 | 1 | 5 | Super Crane Chaos |
| 6 | 1 | 6 | Left Turbo Bumper |
| 7 | 1 | 7 | Top Turbo Bumper |
| 8 | 1 | 8 | Right Turbo Bumper |
| 9 | 2 | 1 | Grid: Fast Scoring |
| 10 | 2 | 2 | Grid: Go To The Movies |
| 11 | 2 | 3 | Grid: Save Danny |
| 12 | 2 | 4 | Grid: LightExtra Ball |
| 13 | 2 | 5 | Grid: Cat Millions |
| 14 | 2 | 6 | Grid: To The Roof |
| 15 | 2 | 7 | Grid: Red Eye |
| 16 | 2 | 8 | Grid: Big Mistake |
| 17 | 3 | 1 | C |
| 18 | 3 | 2 | R |
| 19 | 3 | 3 | A |
| 20 | 3 | 4 | N |
| 21 | 3 | 5 | E |
| 22 | 3 | 6 | Animated Cat Target |
| 23 | 3 | 7 | Ramp |
| 24 | 3 | 8 | Wild Card |
| 25 | 4 | 1 | Benedicts Eyeball Top |
| 26 | 4 | 2 | Benedicts Eyeball Middle |
| 27 | 4 | 3 | Benedicts Eyeball Bottom |
| 28 | 4 | 4 | Top Rollover Left |
| 29 | 4 | 5 | Top Rollover Middle |
| 30 | 4 | 6 | Top Rollover Right |
| 31 | 4 | 7 | Captive Ball X2 |
| 32 | 4 | 8 | Ticket |
| 33 | 5 | 1 | Shield Left |
| 34 | 5 | 2 | Shield Left Center |
| 35 | 5 | 3 | Shield Right Center |
| 36 | 5 | 4 | Shield Right |
| 37 | 5 | 5 | More Time |
| 38 | 5 | 6 | Extra Ball |
| 39 | 5 | 7 | M-Ball |
| 40 | 5 | 8 | Return Lanes X2 |
| 41 | 6 | 1 | Spinner |
| 42 | 6 | 2 | Chicken |
| 43 | 6 | 3 | Outlanes X2 |
| 44 | 6 | 4 | The Roof |
| 45 | 6 | 5 | Jackpot |
| 46 | 6 | 6 | Ripper |
| 47 | 6 | 7 | Save Danny |
| 48 | 6 | 8 | Right Scoop |
| 49 | 7 | 1 | Shoot Again |
| 50 | 7 | 2 | Lock Bottom (Right) |
| 51 | 7 | 3 | Lock Top (Left) |
| 52 | 7 | 4 | Middle Scoop [bar, dot in box 1 of 4] |
| 53 | 7 | 5 | Middle Scoop [bar, dot in box 2 of 4] |
| 54 | 7 | 6 | Middle Scoop [bar, dot in box 3 of 4] |
| 55 | 7 | 7 | Shoot The Crane |
| 56 | 7 | 8 | Middle Scoop [bar, dot in box 4 of 4] |
| 57 | 8 | 1 | Smart Missile |
| 58 | 8 | 2 | R |
| 59 | 8 | 3 | I |
| 60 | 8 | 4 | P |
| 61 | 8 | 5 | P |
| 62 | 8 | 6 | E |
| 63 | 8 | 7 | R |
| 64 | 8 | 8 | Credit Button |

Normalization: the printed cell breaks a name across lines and the transcription joins them with a single space; `Grid: LightExtra Ball` (12) is printed without a space between `Light` and `Extra`, and `Benedicts` (25-27) without an apostrophe. Cells 52, 53, 54 and 56 print a small bar of four boxes above the words `Middle Scoop` with a filled dot in one box; the bracketed text records which box, counted from the left, so the four cells read as four positions of one row of inserts. Cell 55 prints no bar.

## Lamp Number / Description (printed page 31)

The page prints `Lamp Number Description` in two panels beside the `Lamp Locations` drawing, with the note `See page 36 for lamp part numbers` under the drawing.

| Addr | Description |
| --- | --- |
| 01 | Find the Ripper |
| 02 | Grid:Last |
| 03 | Grid:Action |
| 04 | Grid:Hero |
| 05 | Grid:Super Crane |
| 06 | Left Turbo Bumper |
| 07 | Top Turbo Bumper |
| 08 | Right Turbo Bumper |
| 09 | Grid:Fast Scoring |
| 10 | Grid:Go to The Movies |
| 11 | Grid:Save Danny |
| 12 | Grid:Light Extra Ball |
| 13 | Grid:Cat Millions |
| 14 | Grid:To The Roof |
| 15 | Grid:Redeye |
| 16 | Grid:Big Mistake |
| 17 | C |
| 18 | R |
| 19 | A |
| 20 | N |
| 21 | E |
| 22 | Animated Cat Target |
| 23 | Left Ramp |
| 24 | Wild Card |
| 25 | Benedict's EyeTop |
| 26 | Benedict's Eye Middle |
| 27 | Benedict's Eye Bottom |
| 28 | Top Rollover Left |
| 29 | Top Rollover Middle |
| 30 | Top Rollover Right |
| 31 | Captive Ball X2 |
| 32 | Ticket |
| 33 | Shield Left |
| 34 | Shield Left Center |
| 35 | Shield Right Center |
| 36 | Shield Right |
| 37 | More Time |
| 38 | Extra Ball |
| 39 | M-Ball |
| 40 | Return Lanes (2 Bulbs) |
| 41 | Spinner |
| 42 | Chicken |
| 43 | Outlanes (2 Bulbs) |
| 44 | The Roof |
| 45 | Jackpot |
| 46 | Ripper |
| 47 | Save Danny |
| 48 | Right Scoop |
| 49 | Shoot Again |
| 50 | Lock Bottom (Right) |
| 51 | Lock Top (Left) |
| 52 | Middle Scoop |
| 53 | Middle Scoop |
| 54 | Middle Scoop |
| 55 | Shoot the Crane |
| 56 | Middle Scoop |
| 57 | Smart Missle |
| 58 | R |
| 59 | I |
| 60 | P |
| 61 | P |
| 62 | E |
| 63 | R |
| 64 | Credit Button |

The description list and the chart disagree in wording on 01 (`Find the Ripper` against `Grid: Find Benedict`), 05 (`Grid:Super Crane` against `Super Crane Chaos`) and 23 (`Left Ramp` against `Ramp`); the other rows agree. Two rows state a bulb count: 40 `Return Lanes (2 Bulbs)` and 43 `Outlanes (2 Bulbs)`; the chart prints the same two as `X2`. `EyeTop` (25) and `Missle` (57) are the print's own spellings.

## Lamp Locations drawing (printed page 31)

The `Lamp Locations` playfield drawing prints each lamp number at the insert it lights, most of them inside the insert's outline. Three numbers are printed twice: `31` once in a box on the lower left beside `33` and `37`, and once in a box on the right below `35` and above `25`, at the two captive-ball areas; `40` at the top of the left and of the right return lane; and `43` beside the left and the right outlane. `32` is printed once, in the open centre of the playfield below `39`, `41` and `42`, with no insert outline around it. `58` to `63` are printed without outlines in a row along the left side of the apron, below the left flipper, and `57` once, without an outline, at the right side of the apron below the right flipper. `64` (Credit Button) is not drawn.
