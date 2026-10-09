# The Who's Tommy Pinball Wizard (Data East 1994) - Switch Matrix Chart and Switch Part Numbers

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 32 and 33 (PDF 36 and 37) of the IPDB-hosted scan `Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf`. The scan has no text layer (117 image-only pages); OCR text was used only to locate the pages, and every cell below was read from the render.

The chart prints a column header per column (column number, drive transistor, wire colour pair, CPU connector pin) and a row header per row (row number, wire colour pair, connector pin). Printed page 32 says switches are an 8 x 8 matrix of columns (switch drives) and rows (switch returns). The chart is column-major: address = (column - 1) x 8 + row, and that is exactly the number printed in the lower right of each cell.

## Column drives (printed header row)

| Column | Drive transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q55 | GRN-BRN | CN8-1 |
| 2 | Q54 | GRN-RED | CN8-2 |
| 3 | Q53 | GRN-ORN | CN8-3 |
| 4 | Q52 | GRN-YEL | CN8-4 |
| 5 | Q51 | GRN-BLK | CN8-5 |
| 6 | Q50 | GRN-BLU | CN8-7 |
| 7 | Q49 | GRN-VIO | CN8-8 |
| 8 | Q48 | GRN-GRY | CN8-9 |

CN8 pin 6 is not used by any column; the printed header skips from CN8-5 to CN8-7.

## Row returns (printed header column)

| Row | Wire | Connector |
| --- | --- | --- |
| 1 | WHT-BRN | CN10-9 |
| 2 | WHT-RED | CN10-8 |
| 3 | WHT-ORN | CN10-7 |
| 4 | WHT-YEL | CN10-6 |
| 5 | WHT-GRN | CN10-5 |
| 6 | WHT-BLU | CN10-3 |
| 7 | WHT-VIO | CN10-2 |
| 8 | WHT-GRY | CN10-1 |

CN10 pin 4 is not used by any row; the printed header skips from CN10-5 to CN10-3. The chart carries no shaded (opto) cell and no legend marking any cell as an opto or as normally closed.

## Switch Matrix Chart

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Plumb Tilt |
| 2 | 1 | 2 | 4th Coin |
| 3 | 1 | 3 | Credit Button |
| 4 | 1 | 4 | Right Coin |
| 5 | 1 | 5 | Center Coin |
| 6 | 1 | 6 | Left Coin |
| 7 | 1 | 7 | Slam Tilt |
| 8 | 1 | 8 | Extra Ball Button |
| 9 | 2 | 1 | Ball Trough #1 LT |
| 10 | 2 | 2 | Ball Trough #2 |
| 11 | 2 | 3 | Ball Trough #3 |
| 12 | 2 | 4 | Ball Trough #4 |
| 13 | 2 | 5 | Ball Trough #5 |
| 14 | 2 | 6 | Ball Trough #6 |
| 15 | 2 | 7 | Ball Trough #7 RT |
| 16 | 2 | 8 | Shooter Lane |
| 17 | 3 | 1 | Left Slingshot |
| 18 | 3 | 2 | Right Slingshot |
| 19 | 3 | 3 | VUK |
| 20 | 3 | 4 | LT Ramp S-U LT |
| 21 | 3 | 5 | LT Ramp S-U RT |
| 22 | 3 | 6 | Right RampS-U |
| 23 | 3 | 7 | Left Scoop |
| 24 | 3 | 8 | Silver Ball Target |
| 25 | 4 | 1 | LT 3-Bank S-U BOT |
| 26 | 4 | 2 | LT 3-Bank S-U MID |
| 27 | 4 | 3 | LT 3-Bank S-U Top |
| 28 | 4 | 4 | Mirror Up |
| 29 | 4 | 5 | Top Left Rollover |
| 30 | 4 | 6 | Right Ramp Enter |
| 31 | 4 | 7 | Mirror Down |
| 32 | 4 | 8 | Mirror Target |
| 33 | 5 | 1 | RT 3-Bank S-U Top |
| 34 | 5 | 2 | RT 3-Bank S-U MID |
| 35 | 5 | 3 | RT 3-Bank S-U BOT |
| 36 | 5 | 4 | Left Return Lane |
| 37 | 5 | 5 | RT Return Lane |
| 38 | 5 | 6 | Middle Stand-Up |
| 39 | 5 | 7 | Left Spinner |
| 40 | 5 | 8 | Right Spinner |
| 41 | 6 | 1 | Mirror Trough |
| 42 | 6 | 2 | Skill Trough |
| 43 | 6 | 3 | Captive Ball |
| 44 | 6 | 4 | Not Used |
| 45 | 6 | 5 | Not Used |
| 46 | 6 | 6 | Not Used |
| 47 | 6 | 7 | Eject |
| 48 | 6 | 8 | Top Right Rollover |
| 49 | 7 | 1 | Left Turbo Bumper |
| 50 | 7 | 2 | Center Turbo Bumper |
| 51 | 7 | 3 | RT Turbo Bumper |
| 52 | 7 | 4 | Not Used |
| 53 | 7 | 5 | Not Used |
| 54 | 7 | 6 | Not Used |
| 55 | 7 | 7 | Left Outlane |
| 56 | 7 | 8 | Right Outlane |
| 57 | 8 | 1 | Left Ramp Enter |
| 58 | 8 | 2 | Left Ramp Exit |
| 59 | 8 | 3 | Not Used |
| 60 | 8 | 4 | Not Used |
| 61 | 8 | 5 | Not Used |
| 62 | 8 | 6 | Right Ramp Exit |
| 63 | 8 | 7 | Left Flipper |
| 64 | 8 | 8 | Right Flipper |

Normalization: the printed cell breaks a name across lines (for example `LT 3-Bank` / `S-U BOT`) and the transcription joins those lines with a single space. Address 22 is printed `Right` / `RampS-U` with no space between `Ramp` and `S-U`; it is transcribed literally. Address 50 prints `Bumper` partly hidden by the cell's lower border; the word is clear.

## Switch Matrix Locations, Descriptions & Switch Part Numbers (complete table)

Printed page 33 heads the page `Switch Matrix Locations, Descriptions & Swtich Part Numbers` (the second `Swtich` is the print's own spelling) and prints the table in two panels. The legend under the location drawing reads `* Location - In Cabinet`, `** Locatoin - Under Playfield` (the print's own spelling), `ET Enter Trough (Mirror & Skill)` and `NOTE: RAMPS ARE NOT SHOWN ABOVE`.

| Addr | Description | Part no. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin (On Coin Door) | -- |
| 03* | Credit Button (Left of Coin Door) | 500-5097-02 |
| 04* | Right Coin (On Coin Door) | 180-5024-00 |
| 05* | Center Coin (On Coin Door) | 180-5024-00 |
| 06* | Left Coin (On Coin Door) | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08* | Extra Ball Button (Under 03) | (blank) |
| 09 | Ball Trough #1 Left | 180-5119-00 |
| 10 | Ball Trough #2 | 180-5119-00 |
| 11 | Ball Trough #3 | 180-5119-00 |
| 12 | Ball Trough #4 | 180-5119-00 |
| 13 | Ball Trough #5 | 180-5119-00 |
| 14 | Ball Trough #6 | 180-5119-00 |
| 15 | Ball Trough #7 Right | 180-5118-00 |
| 16 | Shooter Lane | 180-5100-01 |
| 17 | Left Slingshot | 180-5023-00 |
| 18 | Right Slingshot | 180-5023-00 |
| 19 | VUK Microswitch | 180-5064-00 |
| 20 | Left Ramp Stand-Up LEFT | 515-5967-08 |
| 21 | Left Ramp Stand-Up RIGHT | 515-5967-08 |
| 22 | Right Ramp Stand-Up | 515-5967-08 |
| 23 | Left Scoop | 180-5116-00 |
| 24 | Silver Ball Target | 515-5932-00 |
| 25 | Left 3-Bank Stand-Up Bottom | 515-5966-06 |
| 26 | Left 3-Bank Stand-Up Middle | 515-5966-07 |
| 27 | Left 3-Bank Stand-Up Top | 515-5966-03 |
| 28 | Mirror Up | 180-5052-00 |
| 29 | Top Left Rollover | 500-5706-00 |
| 30 | Right Ramp Enter | 180-5090-00 |
| 31 | Mirror Down | 180-5052-00 |
| 32 | Mirror Target | 180-5083-00 |
| 33 | Right 3-Bank Stand-Up Top | 515-5966-03 |
| 34 | Right 3-Bank Stand-Up Middle | 515-5966-07 |
| 35 | Right 3-Bank Stand-Up Bottom | 515-5966-06 |
| 36 | Left Return Lane | 500-5707-00 |
| 37 | Right Return Lane | 500-5706-00 |
| 38 | Middle Stand-Up | 515-5966-08 |
| 39 | Left Spinner | 180-5010-04 |
| 40 | Right Spinner | 180-5010-04 |
| 41** | Mirror Trough | 180-5057-00 |
| 42** | Skill Trough | 180-5057-00 |
| 43 | Captive Ball (Target Switch) | 180-5114-08 |
| 44 | Not Used | -- |
| 45 | Not Used | -- |
| 46 | Not Used | -- |
| 47 | Eject (Micro Switch) | 180-5027-01 |
| 48 | Top Right Rollover | 500-5706-00 |
| 49 | Left Turbo Bumper | 180-5015-01 |
| 50 | Center Turbo Bumper | 180-5015-01 |
| 51 | Right Turbo Bumper | 180-5015-01 |
| 52 | Not Used | -- |
| 53 | Not Used | -- |
| 54 | Not Used | -- |
| 55 | Left Outlane | 500-5706-00 |
| 56 | Right Outlane | 500-5706-00 |
| 57 | Left Ramp Enter | 180-5090-00 |
| 58 | Left Ramp Exit | 180-5093-00 |
| 59 | Not Used | -- |
| 60 | Not Used | -- |
| 61 | Not Used | -- |
| 62 | Right Ramp Exit | 180-5093-00 |
| 63* | Left Flipper (Cabinet) | 180-5124-00 |
| 64* | Right Flipper (Cabinet) | 180-5124-00 |

Normalization: the print uses an em dash for an empty part number; it is transcribed `--`. Address 08's part-number cell is printed empty, with no dash, and is transcribed `(blank)`. Addresses are printed with a leading zero below 10, as here.

## Switch Locations drawing (printed page 33)

The playfield drawing marks each switch with a black balloon carrying its number. Two circled `ET` marks (the legend's `Enter Trough (Mirror & Skill)`) sit at the upper right, each beside a balloon whose first digit is hidden by a leader line (the visible digits read `2` and `1`). Balloons `58` and `62` sit at the left and right rails beside the words `ON WIRE RAMP`. Below the playfield outline, at the cabinet front, are a balloon `63` at the left and two touching balloons, the right one printed `8*`, the left one's number not legible.
