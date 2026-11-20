# Last Action Hero (Data East 1993) - Switch Matrix Chart and Switch Part Numbers

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 28 and 29 (PDF 32 and 33) of the IPDB scan `Data_East_1993_Last_Action_Hero_Manual.pdf` (manual pages 1-48). The scan has no text layer (53 image-only pages), so every cell below was read from the render.

Printed page 28 states: `Switches are configured in an 8 x 8 matrix of columns (switch drives) and rows (switch returns) with up to 64 switches possible. The switch tests include three parts; switch test, active switches, and bad switches.` Its Switch Test text says `Close each switch and observe the displays. The Player 1 and 2 displays will indicate the switch name, the Player 3 display indicates the row and column wire colors, and the Player 4 display indicates the switch number.` Its Active Switches text says `If any switches are stuck closed (or made from the presence of a ball), the Player 1 and 2 displays sequence through switch names`.

The chart prints a column header per column (column number, drive transistor, wire colour pair, CPU connector pin) and a row header per row (row number, wire colour pair, connector pin). Both printed matrices are column-major: address = (column - 1) x 8 + row, and that is the number printed in the lower right of each cell.

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
| 8 | 1 | 8 | Launch Trigger |
| 9 | 2 | 1 | Trough #1 Left |
| 10 | 2 | 2 | Trough #2 |
| 11 | 2 | 3 | Trough #3 |
| 12 | 2 | 4 | Trough #4 |
| 13 | 2 | 5 | Trough #5 |
| 14 | 2 | 6 | Trough #6 |
| 15 | 2 | 7 | Trough #7 Right |
| 16 | 2 | 8 | Shooter Lane |
| 17 | 3 | 1 | Drop Target C |
| 18 | 3 | 2 | Drop Target R |
| 19 | 3 | 3 | Drop Target A |
| 20 | 3 | 4 | Drop Target N |
| 21 | 3 | 5 | Drop Target E |
| 22 | 3 | 6 | Left Lock Top |
| 23 | 3 | 7 | Left Lock Bottom |
| 24 | 3 | 8 | Single Left Rollover |
| 25 | 4 | 1 | Right Stand Up Top |
| 26 | 4 | 2 | Right Stand Up Middle |
| 27 | 4 | 3 | Right Stand Up Bottom |
| 28 | 4 | 4 | Top Rollover Left |
| 29 | 4 | 5 | Top Rollover Middle |
| 30 | 4 | 6 | Top Rollover Right |
| 31 | 4 | 7 | Right Scoop Assem. |
| 32 | 4 | 8 | Animated Cat Target |
| 33 | 5 | 1 | Left Turbo Bumper |
| 34 | 5 | 2 | Bottom Turbo Bumper |
| 35 | 5 | 3 | Right Turbo Bumper |
| 36 | 5 | 4 | Left Slingshot |
| 37 | 5 | 5 | Right Slingshot |
| 38 | 5 | 6 | Right Scoop R.O. |
| 39 | 5 | 7 | Left Captive Rollover |
| 40 | 5 | 8 | Left Captive Ball Target |
| 41 | 6 | 1 | Left Return |
| 42 | 6 | 2 | Right Return |
| 43 | 6 | 3 | Left Outlane |
| 44 | 6 | 4 | Right Outlane |
| 45 | 6 | 5 | Left Ramp Exit |
| 46 | 6 | 6 | Left Ramp Enter |
| 47 | 6 | 7 | VUK |
| 48 | 6 | 8 | Ripper Kickback |
| 49 | 7 | 1 | Not Used |
| 50 | 7 | 2 | Not Used |
| 51 | 7 | 3 | Not Used |
| 52 | 7 | 4 | Not Used |
| 53 | 7 | 5 | Not Used |
| 54 | 7 | 6 | Drop Target Bar (2) |
| 55 | 7 | 7 | Right Captive Rollover |
| 56 | 7 | 8 | Right Captive Target |
| 57 | 8 | 1 | Middle Scoop Left |
| 58 | 8 | 2 | Middle Scoop Right |
| 59 | 8 | 3 | Scoop Spinner |
| 60 | 8 | 4 | Crane Left Limit |
| 61 | 8 | 5 | Crane Right Limit |
| 62 | 8 | 6 | Smart Missile |
| 63 | 8 | 7 | Left Flipper |
| 64 | 8 | 8 | Right Flipper |

Normalization: the printed cell breaks a name across lines (for example `Right` / `Stand Up` / `Top`) and the transcription joins those lines with a single space. Address 25-27 print `Stand Up` without a hyphen; the parts table prints `Stand-Up`. Address 38 prints the abbreviation `R.O.` and address 31 `Assem.` exactly as shown.

## Switch Matrix Locations, Descriptions & Switch Part Numbers (complete table)

The table is printed in two panels on printed page 29 under the heading `Last Action Hero - Switch Part Numbers`; the location drawing below the left panel is captioned `Switch Locations`. The asterisk is printed after the number; the page prints no legend for it.

| Addr | Description | Part no. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | - |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08* | Launch Trigger | 180-5111-00 |
| 09 | Trough #1 Left | 180-5119-00 |
| 10 | Trough #2 | 180-5119-00 |
| 11 | Trough #3 | 180-5119-00 |
| 12 | Trough #4 | 180-5119-00 |
| 13 | Trough #5 | 180-5119-00 |
| 14 | Trough #6 | 180-5119-00 |
| 15 | Trough #7 Right | 180-5118-00 |
| 16 | Shooter Lane | 180-5100-01 |
| 17 | Drop Target C | 180-5092-01 |
| 18 | Drop Target R | 180-5092-01 |
| 19 | Drop Target A | 180-5092-01 |
| 20 | Drop Target N | 180-5092-01 |
| 21 | Drop Target E | 180-5092-01 |
| 22 | Left Lock Top | 180-5128-00 |
| 23 | Left Lock Bottom | 180-5128-00 |
| 24 | Single Left Rollover | 500-5706-00 |
| 25 | Right Stand-Up Top | 180-5130-00 |
| 26 | Right Stand-Up Middle | 180-5130-01 |
| 27 | Right Stand-Up Bottom | 180-5130-02 |
| 28 | Top Rollover Left | 500-5706-00 |
| 29 | Top Rollover Middle | 500-5706-00 |
| 30 | Top Rollover Right | 500-5707-00 |
| 31 | Right Scoop Assembly | 500-5057-00 |
| 32 | Animated Cat Target | 180-5125-02 |
| 33 | Left Turbo Bumper | 180-5015-01 |
| 34 | Bottom Turbo Bumper | 180-5015-01 |
| 35 | Right Turbo Bumper | 180-5015-01 |
| 36 | Left Slingshot | 180-5054-00 |
| 37 | Right Slingshot | 180-5054-00 |
| 38 | Right Scoop Rollover | 500-5707-00 |
| 39 | Left Captive Roilover | 500-5706-00 |
| 40 | Left Captive Target | 180-5114-08 |
| 41 | Left Return | 500-5706-00 |
| 42 | Right Return | 500-5707-00 |
| 43 | Left Outlane | 500-5706-00 |
| 44 | Right Outlane | 500-5707-00 |
| 45 | Left Ramp Exit | 180-5090-00 |
| 46 | Left Ramp Entrance | 180-5090-00 |
| 47 | VUK | 180-5116-00 |
| 48 | Ripper Kickback | 500-5707-00 |
| 49 | Not Used | - |
| 50 | Not Used | - |
| 51 | Not Used | - |
| 52 | Not Used | - |
| 53 | Not Used | - |
| 54 | Drop Target Bar (2) | 180-5129-00 |
| 55 | Right Captive Rollover | 500-5707-00 |
| 56 | Right Captive Tgt. | 180-5114-08 |
| 57 | Middle Scoop Left | 180-5116-00 |
| 58 | Middle Scoop Right | 500-5700-00 |
| 59 | Scoop Spinner | 180-5010-04 |
| 60 | Crane Left Limit | 180-5093-00 |
| 61 | Crane Right Limit | 180-5093-00 |
| 62 | Smart Missle | 180-0028-00 |
| 63 | Left Flip. Cab | 180-5048-01 |
| 64 | Right Flip. Cab | 180-5048-01 |

`Roilover` (39) and `Missle` (62) are the print's own spellings. The dash in the part column of 02 and 49-53 is printed as a single hyphen. The asterisk marks exactly 01-08, and the location drawing has no callout for any of them; it is read as the cabinet marking the sister manuals print with the legend `* = Location is in the cabinet`. Addresses 63 and 64 carry no asterisk, but the parts table names them `Left Flip. Cab` and `Right Flip. Cab` with part 180-5048-01, and the Cabinet Parts list on printed page 34 (excerpt `cabinet-and-assemblies`) names item 15 `Left Flipper Leaf Switch` 180-5048-01 and item 15a `Right Flipper Leaf Switch *` 180-5122-00: the two matrix addresses are cabinet flipper-button contacts, not playfield end-of-stroke switches. The same list names item 14 `Push Button Switch` 180-0028-00, the part number this table prints for 62 `Smart Missle`, and item 1 `Shooter Gun Assy.` 500-5731-00.
