# Batman (Data East 1991) - Switch Matrix Chart

Transcribed by hand from a 400 dpi render of printed page 24 (PDF 28). This manual has no text
layer at all (70 pages, 0 characters), so nothing here came from `pdftotext`.

Both printed matrices are column-major: address = (column - 1) x 8 + row.

Column 1 is the dedicated cabinet/coin column. Positions 15 and 16 are printed as the flipper
end-of-stroke switches; see the definition's note on what PinMAME actually publishes there.

| Addr | Column | Row | Description | Column drive | Row return |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Plumb Tilt | Q55 GRN-BRN CN8-1 | WHT-BRN CN10-9 |
| 2 | 1 | 2 | Not Used | Q55 GRN-BRN CN8-1 | WHT-RED CN10-8 |
| 3 | 1 | 3 | Credit Button | Q55 GRN-BRN CN8-1 | WHT-ORN CN10-7 |
| 4 | 1 | 4 | Right Coin | Q55 GRN-BRN CN8-1 | WHT-YEL CN10-6 |
| 5 | 1 | 5 | Center Coin | Q55 GRN-BRN CN8-1 | WHT-GRN CN10-5 |
| 6 | 1 | 6 | Left Coin | Q55 GRN-BRN CN8-1 | WHT-BLU CN10-3 |
| 7 | 1 | 7 | Slam Tilt | Q55 GRN-BRN CN8-1 | WHT-VIO CN10-2 |
| 8 | 1 | 8 | Not Used | Q55 GRN-BRN CN8-1 | WHT-GRY CN10-1 |
| 9 | 2 | 1 | Not Used | Q54 GRN-RED CN8-2 | WHT-BRN CN10-9 |
| 10 | 2 | 2 | Outhole | Q54 GRN-RED CN8-2 | WHT-RED CN10-8 |
| 11 | 2 | 3 | Trough #1 Left | Q54 GRN-RED CN8-2 | WHT-ORN CN10-7 |
| 12 | 2 | 4 | Trough #2 Center | Q54 GRN-RED CN8-2 | WHT-YEL CN10-6 |
| 13 | 2 | 5 | Trough #3 Right | Q54 GRN-RED CN8-2 | WHT-GRN CN10-5 |
| 14 | 2 | 6 | Shooter Lane | Q54 GRN-RED CN8-2 | WHT-BLU CN10-3 |
| 15 | 2 | 7 | Left EOS | Q54 GRN-RED CN8-2 | WHT-VIO CN10-2 |
| 16 | 2 | 8 | Right EOS | Q54 GRN-RED CN8-2 | WHT-GRY CN10-1 |
| 17 | 3 | 1 | Left Top Lane | Q53 GRN-ORN CN8-3 | WHT-BRN CN10-9 |
| 18 | 3 | 2 | Center Top Lane | Q53 GRN-ORN CN8-3 | WHT-RED CN10-8 |
| 19 | 3 | 3 | Right Top Lane | Q53 GRN-ORN CN8-3 | WHT-ORN CN10-7 |
| 20 | 3 | 4 | Not Used | Q53 GRN-ORN CN8-3 | WHT-YEL CN10-6 |
| 21 | 3 | 5 | Left Return | Q53 GRN-ORN CN8-3 | WHT-GRN CN10-5 |
| 22 | 3 | 6 | Right Return | Q53 GRN-ORN CN8-3 | WHT-BLU CN10-3 |
| 23 | 3 | 7 | Left Outlane | Q53 GRN-ORN CN8-3 | WHT-VIO CN10-2 |
| 24 | 3 | 8 | Right Outlane | Q53 GRN-ORN CN8-3 | WHT-GRY CN10-1 |
| 25 | 4 | 1 | Not Used | Q52 GRN-YEL CN8-4 | WHT-BRN CN10-9 |
| 26 | 4 | 2 | Not Used | Q52 GRN-YEL CN8-4 | WHT-RED CN10-8 |
| 27 | 4 | 3 | Not Used | Q52 GRN-YEL CN8-4 | WHT-ORN CN10-7 |
| 28 | 4 | 4 | Ramp Entrance | Q52 GRN-YEL CN8-4 | WHT-YEL CN10-6 |
| 29 | 4 | 5 | Ramp Exit | Q52 GRN-YEL CN8-4 | WHT-GRN CN10-5 |
| 30 | 4 | 6 | Not Used | Q52 GRN-YEL CN8-4 | WHT-BLU CN10-3 |
| 31 | 4 | 7 | Not Used | Q52 GRN-YEL CN8-4 | WHT-VIO CN10-2 |
| 32 | 4 | 8 | Not Used | Q52 GRN-YEL CN8-4 | WHT-GRY CN10-1 |
| 33 | 5 | 1 | Left 3 Bank Top | Q51 GRN-BLK CN8-5 | WHT-BRN CN10-9 |
| 34 | 5 | 2 | Left 3 Bank Middle | Q51 GRN-BLK CN8-5 | WHT-RED CN10-8 |
| 35 | 5 | 3 | Left 3 Bank Bottom | Q51 GRN-BLK CN8-5 | WHT-ORN CN10-7 |
| 36 | 5 | 4 | Joker Left Eye | Q51 GRN-BLK CN8-5 | WHT-YEL CN10-6 |
| 37 | 5 | 5 | Joker Right Eye | Q51 GRN-BLK CN8-5 | WHT-GRN CN10-5 |
| 38 | 5 | 6 | Joker Mouth | Q51 GRN-BLK CN8-5 | WHT-BLU CN10-3 |
| 39 | 5 | 7 | Left VUK | Q51 GRN-BLK CN8-5 | WHT-VIO CN10-2 |
| 40 | 5 | 8 | Not Used | Q51 GRN-BLK CN8-5 | WHT-GRY CN10-1 |
| 41 | 6 | 1 | Right 3 Bank Top | Q50 GRN-BLU CN8-7 | WHT-BRN CN10-9 |
| 42 | 6 | 2 | Right 3 Bank Middle | Q50 GRN-BLU CN8-7 | WHT-RED CN10-8 |
| 43 | 6 | 3 | Right 3 Bank Bottom | Q50 GRN-BLU CN8-7 | WHT-ORN CN10-7 |
| 44 | 6 | 4 | Not Used | Q50 GRN-BLU CN8-7 | WHT-YEL CN10-6 |
| 45 | 6 | 5 | Not Used | Q50 GRN-BLU CN8-7 | WHT-GRN CN10-5 |
| 46 | 6 | 6 | Not Used | Q50 GRN-BLU CN8-7 | WHT-BLU CN10-3 |
| 47 | 6 | 7 | Left Slingshot | Q50 GRN-BLU CN8-7 | WHT-VIO CN10-2 |
| 48 | 6 | 8 | Right Slingshot | Q50 GRN-BLU CN8-7 | WHT-GRY CN10-1 |
| 49 | 7 | 1 | Bat Bar Standup | Q49 GRN-VIO CN8-8 | WHT-BRN CN10-9 |
| 50 | 7 | 2 | Museum Motor Up | Q49 GRN-VIO CN8-8 | WHT-RED CN10-8 |
| 51 | 7 | 3 | Museum Motor Down | Q49 GRN-VIO CN8-8 | WHT-ORN CN10-7 |
| 52 | 7 | 4 | Right VUK Top | Q49 GRN-VIO CN8-8 | WHT-YEL CN10-6 |
| 53 | 7 | 5 | Right VUK Bottom | Q49 GRN-VIO CN8-8 | WHT-GRN CN10-5 |
| 54 | 7 | 6 | Left Turbo Bumper | Q49 GRN-VIO CN8-8 | WHT-BLU CN10-3 |
| 55 | 7 | 7 | Center Turbo Bumper | Q49 GRN-VIO CN8-8 | WHT-VIO CN10-2 |
| 56 | 7 | 8 | Right Turbo Bumper | Q49 GRN-VIO CN8-8 | WHT-GRY CN10-1 |
| 57 | 8 | 1 | Not Used | Q48 GRN-GRY CN8-9 | WHT-BRN CN10-9 |
| 58 | 8 | 2 | Not Used | Q48 GRN-GRY CN8-9 | WHT-RED CN10-8 |
| 59 | 8 | 3 | Not Used | Q48 GRN-GRY CN8-9 | WHT-ORN CN10-7 |
| 60 | 8 | 4 | Not Used | Q48 GRN-GRY CN8-9 | WHT-YEL CN10-6 |
| 61 | 8 | 5 | Not Used | Q48 GRN-GRY CN8-9 | WHT-GRN CN10-5 |
| 62 | 8 | 6 | Not Used | Q48 GRN-GRY CN8-9 | WHT-BLU CN10-3 |
| 63 | 8 | 7 | Not Used | Q48 GRN-GRY CN8-9 | WHT-VIO CN10-2 |
| 64 | 8 | 8 | Not Used | Q48 GRN-GRY CN8-9 | WHT-GRY CN10-1 |
