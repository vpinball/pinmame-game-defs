# Tales from the Crypt (Data East 1993) - Switch Matrix Chart and Switch Part Numbers

Transcribed by hand from native-resolution renders of printed pages 28 and 29 (PDF 32 and 33) of the GameEx-hosted scan `Data_East_1993_Tales_from_the_Crypt_Manual.pdf`. The scan has no text layer (122 image-only pages), so nothing here came from `pdftotext`; the OCR text the contributor generated was used only to locate pages, and every cell below was read from the render.

The chart prints a column header per column (column number, drive transistor, wire colour pair, CPU connector pin) and a row header per row (row number, wire colour pair, connector pin). The chart's own text says switches are an 8 x 8 matrix of columns (switch drives) and rows (switch returns). Both printed matrices are column-major: address = (column - 1) x 8 + row, and that is exactly the number printed in the lower right of each cell.

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
| 8 | 1 | 8 | Buy-In Type |
| 9 | 2 | 1 | Trough #1 Left |
| 10 | 2 | 2 | Trough #2 |
| 11 | 2 | 3 | Trough #3 |
| 12 | 2 | 4 | Trough #4 |
| 13 | 2 | 5 | Trough #5 |
| 14 | 2 | 6 | Trough #6 |
| 15 | 2 | 7 | Trough #7 Right |
| 16 | 2 | 8 | Shooter Lane |
| 17 | 3 | 1 | Left Outlane |
| 18 | 3 | 2 | Left Return |
| 19 | 3 | 3 | Left Slingshot |
| 20 | 3 | 4 | Left Bottom 3-Bank |
| 21 | 3 | 5 | Left Middle 3-Bank |
| 22 | 3 | 6 | Left Top 3-Bank |
| 23 | 3 | 7 | Left Bottom Orbit |
| 24 | 3 | 8 | Left Top Orbit |
| 25 | 4 | 1 | Right Outlane |
| 26 | 4 | 2 | Right Return |
| 27 | 4 | 3 | Right Slingshot |
| 28 | 4 | 4 | Right Bottom 3-Bank |
| 29 | 4 | 5 | Right Middle 3-Bank |
| 30 | 4 | 6 | Right Top 3-Bank |
| 31 | 4 | 7 | Right Bottom Orbit |
| 32 | 4 | 8 | Right Top Orbit |
| 33 | 5 | 1 | Up |
| 34 | 5 | 2 | Not Used |
| 35 | 5 | 3 | Not Used |
| 36 | 5 | 4 | Down |
| 37 | 5 | 5 | Grave-Stone |
| 38 | 5 | 6 | VUK Left |
| 39 | 5 | 7 | Captive Ball |
| 40 | 5 | 8 | Left Spinner |
| 41 | 6 | 1 | Left Drop |
| 42 | 6 | 2 | Middle Drop |
| 43 | 6 | 3 | Right Drop |
| 44 | 6 | 4 | Left Ramp Enter |
| 45 | 6 | 5 | Left Ramp Middle |
| 46 | 6 | 6 | Right Ramp Enter |
| 47 | 6 | 7 | Right Ramp Exit |
| 48 | 6 | 8 | Right Spinner |
| 49 | 7 | 1 | Left Turbo |
| 50 | 7 | 2 | Bottom Turbo |
| 51 | 7 | 3 | Right Turbo |
| 52 | 7 | 4 | Super VUK Right |
| 53 | 7 | 5 | Small Trough |
| 54 | 7 | 6 | Large Trough |
| 55 | 7 | 7 | Power Scoop |
| 56 | 7 | 8 | Middle Spinner |
| 57 | 8 | 1 | Lamp Ramp Exit |
| 58 | 8 | 2 | Not Used |
| 59 | 8 | 3 | Not Used |
| 60 | 8 | 4 | Not Used |
| 61 | 8 | 5 | Not Used |
| 62 | 8 | 6 | Launch Button |
| 63 | 8 | 7 | Left End of Stroke |
| 64 | 8 | 8 | Right End of Stroke |

Normalization: the printed cell breaks a name across lines (for example `Left` / `Bottom` / `3-Bank`) and the transcription joins those lines with a single space. Address 57 is printed `Lamp` / `Ramp` / `Exit`; it is transcribed literally, and the parts table below prints the same address as `Left Ramp Exit`. The chart's address 8 is printed `Buy-In Type`; the parts table prints it `Buy-In Button`. The chart prints address 37 `Grave-Stone`, where the parts table prints `Tombstone Score`.

## Switch Matrix Locations, Descriptions & Switch Part Numbers (complete table)

The table is printed in two panels on printed page 29. The legend under the location drawing reads `* = Location is in the cabinet.`

| Addr | Description | Part no. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | -- |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08* | Buy-In Button | 180-5073-00 |
| 09 | Trough #1 Left | 180-5119-00 |
| 10 | Trough #2 | 180-5119-00 |
| 11 | Trough #3 | 180-5119-00 |
| 12 | Trough #4 | 180-5119-00 |
| 13 | Trough #5 | 180-5119-00 |
| 14 | Trough #6 | 180-5119-00 |
| 15 | Trough #7 Right | 180-5118-00 |
| 16 | Shooter Lane | 180-5100-01 |
| 17 | Left Outlane | 500-5706-00 |
| 18 | Left Return | 500-5706-00 |
| 19 | Left Slingshot | 180-5023-00 |
| 20 | Left Bottom 3 Bank | 180-5130-02 |
| 21 | Left Mid 3 Bank | 180-5130-01 |
| 22 | Left Top 3 Bank | 180-5130-00 |
| 23 | Left Bottom Orbit | 500-5706-00 |
| 24 | Left Top Orbit | 500-5707-00 |
| 25 | Right Outlane | 500-5707-00 |
| 26 | Right Return | 500-5707-00 |
| 27 | Right Slingshot | 180-5023-00 |
| 28 | Right Bottom 3 Bank | 180-5130-02 |
| 29 | Right Mid 3 Bank | 180-5130-01 |
| 30 | Right Top 3 Bank | 180-5130-02 |
| 31 | Right Bottom Orbit | 500-5706-00 |
| 32 | Right Top Orbit | 500-5707-00 |
| 33* | Up (Tomb) | 180-5052-00 |
| 34 | Not Used | -- |
| 35 | Not Used | -- |
| 36* | Down (Tomb) | 180-5052-00 |
| 37* | Tombstone Score | 180-5083-00 |
| 38 | VUK Left | 180-5064-00 |
| 39 | Captive Ball Trgt. Switch | 180-5114-08 |
| 40 | Left Spinner | 180-5010-04 |
| 41 | Left Drop Target | 180-5092-01 |
| 42 | Mid Drop Target | 180-5092-01 |
| 43 | Right Drop Target | 180-5092-01 |
| 44 | Left Ramp Enter | 180-5090-00 |
| 45 | Left Ramp Middle | 180-5090-00 |
| 46 | Right Ramp Enter | 180-5090-00 |
| 47 | Right Ramp Exit | 180-5093-00 |
| 48 | Right Spinner | 180-5010-04 |
| 49 | Left Turbo Bumper | 180-5015-01 |
| 50 | Bottom Turbo Bumper | 180-5015-01 |
| 51 | Right Turbo Bumper | 180-5015-01 |
| 52 | Super VUK Right | 180-5064-01 |
| 53 | Small Trough | 180-5093-00 |
| 54 | Large Trough | 180-5093-00 |
| 55 | Power Scoop | 500-5057-00 |
| 56 | Middle Spinner | 180-5010-04 |
| 57 | Left Ramp Exit | 180-5090-00 |
| 58 | Not Used | -- |
| 59 | Not Used | -- |
| 60 | Not Used | -- |
| 61 | Not Used | -- |
| 62 | Launch Button | 180-5073-00 |
| 63 | Left End of Stroke | 180-5124-00 |
| 64 | Right End of Stroke | 180-5124-00 |

The asterisk (the legend says: location is in the cabinet) marks 01-08 and, unexpectedly, 33, 36 and 37, the three tombstone-mechanism switches. None of 33, 36 or 37 has a callout on the playfield location drawing beside the table, which is the only visible effect of the marking; the same manual's Playfield - Major Assemblies page lists the Motor, Cam & Switch Assembly (item 2) as a part below the playfield (a circled item) and its Gravestone Up & Down Test describes the two limit switches as part of the gravestone motor mechanism.

The location drawing beside the table prints callout boxes for the playfield addresses; it has no callout for 33, 36 or 37, and none for the asterisked cabinet addresses 01-08.
