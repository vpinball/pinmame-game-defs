# Lethal Weapon 3 (Data East 1992) - Switch Matrix Chart

Transcribed by hand from 400 dpi renders of printed pages 24 and 25 (PDF 28 and 29). The contributor-supplied manual has no text layer at all (93 pages, 0 characters), so nothing here came from `pdftotext`.

Both printed matrices are column-major: address = (column - 1) x 8 + row.

Column 1 is the dedicated cabinet/coin column. Position 2 is printed 4th Coin, where s11.h's shared DE_COMPORTS macro says Ball Tilt. The matrix chart prints positions 15 and 16 as flipper end-of-stroke switches, but the adjacent Switch Part Numbers table explicitly identifies both as cabinet flipper switches. That within-manual discrepancy is preserved below; the definition follows the parts table, PinMAME, and the known-working script for the public semantics.

## Complete Switch Part Numbers table

The adjacent table on printed page 25 is transcribed in full so its fitment, part-number, and legend evidence remains reviewable without selecting only rows used by the definition.

| Addr | Description | Part number |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | - |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08 | Not Used | - |
| 09 | Launch Trigger | 180-5040-01 |
| 10 | Outhole | 180-5011-00 |
| 11 | Trough #1 Left | 180-5009-00 |
| 12 | Trough #2 Center | 180-5009-00 |
| 13 | Trough #3 Right | 180-5010-00 |
| 14 | Shooter Lane | 180-5053-00 |
| 15* | Left Flip. Cab | 180-5048-01 |
| 16* | Right Flip. Cab. | 180-5048-01 |
| 17 | † Left 4 Bank Top 4 | 180-5082-06 |
| 18 | † Left 4 Bank Mid. 3 | 180-5082-06 |
| 19 | † Left 4 Bank Mid. 2 | 180-5082-06 |
| 20 | † Left 4 Bank Bot. 1 | 180-5082-06 |
| 21 | Left Orbit Rollover | 500-5142-00 |
| 22 | Right Orbit Rollover | 515-5138-00 |
| 23 | Not Used | - |
| 24 | Not Used | - |
| 25 | Center Drop Tar. Left | 180-5092-01 |
| 26 | Center Drop Tar. Mid. | 180-5092-01 |
| 27 | Center Drop Tar. Bot. | 180-5092-01 |
| 28 | Left Outlane | 500-5142-00 |
| 29 | Left Return | 500-5142-00 |
| 30 | Left Slingshot | 180-5054-00 |
| 31 | Vertical Up Kicker | 180-5064-00 |
| 32 | Right Saucer | 180-5027-00 |
| 33 | Right Drop Tar. Top | 180-5092-01 |
| 34 | Right Drop Tar. Mid. | 180-5092-01 |
| 35 | Right Drop Tar. Bot. | 180-5092-01 |
| 36 | Right Outlane | 515-5138-00 |
| 37 | Right Return | 515-5138-00 |
| 38 | Right Slingshot | 180-5054-00 |
| 39 | † Left Stand-up Tar. | 500-5252-06 |
| 40 | Left Saucer | 180-5027-00 |
| 41 | Left Top Lane | 500-5142-00 |
| 42 | Center Top Lane | 500-5142-00 |
| 43 | Right Top Lane | 500-5142-00 |
| 44 | Left Turbo Bumper | 180-5015-00 |
| 45 | Center Turbo Bumper | 180-5015-00 |
| 46 | Right Turbo Bumper | 180-5015-00 |
| 47 | Left Spinner | 180-5010-04 |
| 48 | Right Spinner | 180-5010-04 |
| 49 | Ramp Entrance | 180-5087-00 |
| 50 | Ramp Exit | 180-5101-00 |
| 51 | Not Used | - |
| 52 | Right 10 Point | 500-5033-00 |
| 53 | Not Used | - |
| 54 | Left Orbit R.O.Backup | 500-5142-00 |
| 55 | Right Orbit R.O. Backup | 515-5138-00 |
| 56 | Not Used Through 64 | - |

The printed legends say `† Misc.- Back-up plates 535-5116-00 for Stand-Up Targets` and `* Indicates Cabinet Switches`. The asterisk appears on 01-07 and 15-16, but not on 09 Launch Trigger; the retained script and absence of a 09 playfield callout nevertheless establish 09 as the cabinet gun-launch input. The parts table also prints address 27 as `Center Drop Tar. Bot.` while the matrix chart prints `Center Drop Tar. Right`; the within-manual variance is preserved rather than silently reconciled.

| Addr | Column | Row | Description | Column drive | Row return |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Plumb Tilt | Q55 GRN-BRN CN8-1 | WHT-BRN CN10-9 |
| 2 | 1 | 2 | 4th Coin | Q55 GRN-BRN CN8-1 | WHT-RED CN10-8 |
| 3 | 1 | 3 | Credit Button | Q55 GRN-BRN CN8-1 | WHT-ORN CN10-7 |
| 4 | 1 | 4 | Right Coin | Q55 GRN-BRN CN8-1 | WHT-YEL CN10-6 |
| 5 | 1 | 5 | Center Coin | Q55 GRN-BRN CN8-1 | WHT-GRN CN10-5 |
| 6 | 1 | 6 | Left Coin | Q55 GRN-BRN CN8-1 | WHT-BLU CN10-3 |
| 7 | 1 | 7 | Slam Tilt | Q55 GRN-BRN CN8-1 | WHT-VIO CN10-2 |
| 8 | 1 | 8 | Not Used | Q55 GRN-BRN CN8-1 | WHT-GRY CN10-1 |
| 9 | 2 | 1 | Launch Trigger | Q54 GRN-RED CN8-2 | WHT-BRN CN10-9 |
| 10 | 2 | 2 | Outhole | Q54 GRN-RED CN8-2 | WHT-RED CN10-8 |
| 11 | 2 | 3 | Trough #1 Left | Q54 GRN-RED CN8-2 | WHT-ORN CN10-7 |
| 12 | 2 | 4 | Trough #2 Center | Q54 GRN-RED CN8-2 | WHT-YEL CN10-6 |
| 13 | 2 | 5 | Trough #3 Right | Q54 GRN-RED CN8-2 | WHT-GRN CN10-5 |
| 14 | 2 | 6 | Shooter Lane | Q54 GRN-RED CN8-2 | WHT-BLU CN10-3 |
| 15 | 2 | 7 | Left EOS | Q54 GRN-RED CN8-2 | WHT-VIO CN10-2 |
| 16 | 2 | 8 | Right EOS | Q54 GRN-RED CN8-2 | WHT-GRY CN10-1 |
| 17 | 3 | 1 | Left 4 Bank Top 4 | Q53 GRN-ORN CN8-3 | WHT-BRN CN10-9 |
| 18 | 3 | 2 | Left 4 Bank Mid. 3 | Q53 GRN-ORN CN8-3 | WHT-RED CN10-8 |
| 19 | 3 | 3 | Left 4 Bank Mid. 2 | Q53 GRN-ORN CN8-3 | WHT-ORN CN10-7 |
| 20 | 3 | 4 | Left 4 Bank Bot. 1 | Q53 GRN-ORN CN8-3 | WHT-YEL CN10-6 |
| 21 | 3 | 5 | Left Orbit Rollover | Q53 GRN-ORN CN8-3 | WHT-GRN CN10-5 |
| 22 | 3 | 6 | Right Orbit Rollover | Q53 GRN-ORN CN8-3 | WHT-BLU CN10-3 |
| 23 | 3 | 7 | Not Used | Q53 GRN-ORN CN8-3 | WHT-VIO CN10-2 |
| 24 | 3 | 8 | Not Used | Q53 GRN-ORN CN8-3 | WHT-GRY CN10-1 |
| 25 | 4 | 1 | Center Drop Tar. Left | Q52 GRN-YEL CN8-4 | WHT-BRN CN10-9 |
| 26 | 4 | 2 | Center Drop Tar. Mid. | Q52 GRN-YEL CN8-4 | WHT-RED CN10-8 |
| 27 | 4 | 3 | Center Drop Tar. Right | Q52 GRN-YEL CN8-4 | WHT-ORN CN10-7 |
| 28 | 4 | 4 | Left Outlane | Q52 GRN-YEL CN8-4 | WHT-YEL CN10-6 |
| 29 | 4 | 5 | Left Return | Q52 GRN-YEL CN8-4 | WHT-GRN CN10-5 |
| 30 | 4 | 6 | Left Slingshot | Q52 GRN-YEL CN8-4 | WHT-BLU CN10-3 |
| 31 | 4 | 7 | VUK | Q52 GRN-YEL CN8-4 | WHT-VIO CN10-2 |
| 32 | 4 | 8 | Right Saucer | Q52 GRN-YEL CN8-4 | WHT-GRY CN10-1 |
| 33 | 5 | 1 | Right Drop Tar. Top | Q51 GRN-BLK CN8-5 | WHT-BRN CN10-9 |
| 34 | 5 | 2 | Right Drop Tar. Mid. | Q51 GRN-BLK CN8-5 | WHT-RED CN10-8 |
| 35 | 5 | 3 | Right Drop Tar. Bot. | Q51 GRN-BLK CN8-5 | WHT-ORN CN10-7 |
| 36 | 5 | 4 | Right Outlane | Q51 GRN-BLK CN8-5 | WHT-YEL CN10-6 |
| 37 | 5 | 5 | Right Return | Q51 GRN-BLK CN8-5 | WHT-GRN CN10-5 |
| 38 | 5 | 6 | Right Slingshot | Q51 GRN-BLK CN8-5 | WHT-BLU CN10-3 |
| 39 | 5 | 7 | Left Stand-Up Target | Q51 GRN-BLK CN8-5 | WHT-VIO CN10-2 |
| 40 | 5 | 8 | Left Saucer | Q51 GRN-BLK CN8-5 | WHT-GRY CN10-1 |
| 41 | 6 | 1 | Left Top Lane | Q50 GRN-BLU CN8-7 | WHT-BRN CN10-9 |
| 42 | 6 | 2 | Center Top Lane | Q50 GRN-BLU CN8-7 | WHT-RED CN10-8 |
| 43 | 6 | 3 | Right Top Lane | Q50 GRN-BLU CN8-7 | WHT-ORN CN10-7 |
| 44 | 6 | 4 | Left Turbo Bumper | Q50 GRN-BLU CN8-7 | WHT-YEL CN10-6 |
| 45 | 6 | 5 | Center Turbo Bumper | Q50 GRN-BLU CN8-7 | WHT-GRN CN10-5 |
| 46 | 6 | 6 | Right Turbo Bumper | Q50 GRN-BLU CN8-7 | WHT-BLU CN10-3 |
| 47 | 6 | 7 | Left Spinner | Q50 GRN-BLU CN8-7 | WHT-VIO CN10-2 |
| 48 | 6 | 8 | Right Spinner | Q50 GRN-BLU CN8-7 | WHT-GRY CN10-1 |
| 49 | 7 | 1 | Ramp Entrance | Q49 GRN-VIO CN8-8 | WHT-BRN CN10-9 |
| 50 | 7 | 2 | Ramp Exit | Q49 GRN-VIO CN8-8 | WHT-RED CN10-8 |
| 51 | 7 | 3 | Not Used | Q49 GRN-VIO CN8-8 | WHT-ORN CN10-7 |
| 52 | 7 | 4 | Right 10 Point | Q49 GRN-VIO CN8-8 | WHT-YEL CN10-6 |
| 53 | 7 | 5 | Not Used | Q49 GRN-VIO CN8-8 | WHT-GRN CN10-5 |
| 54 | 7 | 6 | Left Orbit R.O. Back Up | Q49 GRN-VIO CN8-8 | WHT-BLU CN10-3 |
| 55 | 7 | 7 | Right Orbit R.O. Back Up | Q49 GRN-VIO CN8-8 | WHT-VIO CN10-2 |
| 56 | 7 | 8 | Not Used | Q49 GRN-VIO CN8-8 | WHT-GRY CN10-1 |
| 57 | 8 | 1 | Not Used | Q48 GRN-GRY CN8-9 | WHT-BRN CN10-9 |
| 58 | 8 | 2 | Not Used | Q48 GRN-GRY CN8-9 | WHT-RED CN10-8 |
| 59 | 8 | 3 | Not Used | Q48 GRN-GRY CN8-9 | WHT-ORN CN10-7 |
| 60 | 8 | 4 | Not Used | Q48 GRN-GRY CN8-9 | WHT-YEL CN10-6 |
| 61 | 8 | 5 | Not Used | Q48 GRN-GRY CN8-9 | WHT-GRN CN10-5 |
| 62 | 8 | 6 | Not Used | Q48 GRN-GRY CN8-9 | WHT-BLU CN10-3 |
| 63 | 8 | 7 | Not Used | Q48 GRN-GRY CN8-9 | WHT-VIO CN10-2 |
| 64 | 8 | 8 | Not Used | Q48 GRN-GRY CN8-9 | WHT-GRY CN10-1 |
