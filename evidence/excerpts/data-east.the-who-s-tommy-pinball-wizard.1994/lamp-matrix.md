# The Who's Tommy Pinball Wizard (Data East 1994) - Lamp Matrix Chart and Lamp Matrix Locations

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 34 and 35 (PDF 38 and 39) of the IPDB-hosted scan `Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf`. The scan has no text layer; OCR text was used only to locate the pages, and every cell below was read from the render.

Printed page 34 says controlled lamps are an 8 x 8 matrix of columns (lamp drives) and rows (lamp returns), and that in the Single Lamp test "With the FORWARD/REVERSE push-button switch in the FORWARD (up) position, operating the Game Start push-button switch selects higher-numbered lamps; with it in the REVERSE (down) position, Game Start selects lower-numbered lamps." The chart is column-major: address = (column - 1) x 8 + row, which is the number printed in the lower right of each cell except at address 42 (below).

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

CN7 pin 5 is not used by any column; the printed header skips from CN7-4 to CN7-6.

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

CN6 pin 4 is not used by any row; the printed header skips from CN6-3 to CN6-5.

## Lamp Matrix Chart

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Insert X2 (T)OMMY |
| 2 | 1 | 2 | Grid: Christmas |
| 3 | 1 | 3 | Grid: Cousin Kevin |
| 4 | 1 | 4 | Grid: Holiday Camp |
| 5 | 1 | 5 | Grid: Lite Extra Ball |
| 6 | 1 | 6 | Grid: Silver Ball |
| 7 | 1 | 7 | Grid: Captain Walker |
| 8 | 1 | 8 | Grid: Wizard |
| 9 | 2 | 1 | Skill Shot |
| 10 | 2 | 2 | Insert X2 T(O)MMY |
| 11 | 2 | 3 | Grid: Smash the Mirror |
| 12 | 2 | 4 | Grid: Fiddle About |
| 13 | 2 | 5 | Grid: Acid Queen |
| 14 | 2 | 6 | Grid: There's A Doctor |
| 15 | 2 | 7 | Grid: Tommy Scoring |
| 16 | 2 | 8 | Grid: Sally Simpson |
| 17 | 3 | 1 | Jackpot |
| 18 | 3 | 2 | Double Jackpot |
| 19 | 3 | 3 | Insert X2 TO(M)MY |
| 20 | 3 | 4 | LT Ramp S-U LT |
| 21 | 3 | 5 | LT Ramp S-U RT |
| 22 | 3 | 6 | RT. Ramp S-U Top |
| 23 | 3 | 7 | Extra Ball Button |
| 24 | 3 | 8 | Silver Ball |
| 25 | 4 | 1 | LT 3-Bank S-U BOT |
| 26 | 4 | 2 | LT 3-Bank S-U MID |
| 27 | 4 | 3 | LT 3-Bank S-U Top |
| 28 | 4 | 4 | Insert X2 TOM(M)Y |
| 29 | 4 | 5 | Spinner Bonus LT |
| 30 | 4 | 6 | Extra Ball |
| 31 | 4 | 7 | Lite Union Jack LT |
| 32 | 4 | 8 | Genius |
| 33 | 5 | 1 | RT 3-Bank S-U Top |
| 34 | 5 | 2 | RT 3-Bank S-U MID |
| 35 | 5 | 3 | RT 3-Bank S-U BOT |
| 36 | 5 | 4 | Mystery |
| 37 | 5 | 5 | Insert X2 TOMM(Y) |
| 38 | 5 | 6 | More Time |
| 39 | 5 | 7 | Captain Walker LT |
| 40 | 5 | 8 | Captain Walker RT |
| 41 | 6 | 1 | P/F (T)OMMY |
| 42 | 6 | 2 | P/F T(O)MMY |
| 43 | 6 | 3 | P/F TO(M)MY |
| 44 | 6 | 4 | P/F TOM(M)Y |
| 45 | 6 | 5 | P/F TOMM(Y) |
| 46 | 6 | 6 | Outlanes X2 |
| 47 | 6 | 7 | Mirror Multiball |
| 48 | 6 | 8 | Shoot Again |
| 49 | 7 | 1 | Left Turbo Bumper |
| 50 | 7 | 2 | CT Turbo Bumper |
| 51 | 7 | 3 | RT Turbo Bumper |
| 52 | 7 | 4 | Spinner Bonus RT |
| 53 | 7 | 5 | Lite Union Jack RT |
| 54 | 7 | 6 | Holiday Camp |
| 55 | 7 | 7 | Return Lanes X2 |
| 56 | 7 | 8 | Airplane |
| 57 | 8 | 1 | Acid Queen LT |
| 58 | 8 | 2 | Acid Queen CT |
| 59 | 8 | 3 | Acid Queen RT |
| 60 | 8 | 4 | Sally Simpson LT |
| 61 | 8 | 5 | Sally Simpson RT |
| 62 | 8 | 6 | Scoop Multiball |
| 63 | 8 | 7 | Collect Union Jack |
| 64 | 8 | 8 | Credit Button |

Normalization: the printed cell breaks a name across lines and the transcription joins those lines with a single space; `Sally Simp-` / `son` is joined as `Sally Simpson`. The TOMMY cells print the lit letter in bold inside parentheses with the other letters in small capitals (for example `(T)OMMY`); the transcription keeps the parentheses and capitalizes every letter. The cell at column 6, row 2 (address 42) prints the cell number `41`, the same number as the cell above it; its column and row make it 42, and the location table below lists 42 as `...O (Playfield)`, so the printed `41` is read as a misprint of `42`. Address 22 is printed `RT. Ramp S-U Top` where the location table prints `Left Ramp Stand-Up Top`.

## Lamp Matrix No. & Description (location table, printed page 35)

The table is printed in three panels. The notes under it read `* Location - In Cabinet`, `** Location - Backbox (Insert)`, `1 RAMPS ARE NOT SHOWN`, `2 AIRPLANE IS NOT SHOWN`, `3 General Illumination (G.I.) Lamps NOT SHOWN` and `4 For Bulb Type & PNs, See Page 43`. A drawing above the playfield drawing, captioned `** Backbox Insert Locations`, shows two balloons each for 01, 10, 19, 28 and 37.

| No. | Description |
| --- | --- |
| 01** | ...T (Insert X2) |
| 02 | Grid: Christmas |
| 03 | Grid: Cousin Kevin |
| 04 | Grid: Holiday Camp |
| 05 | Grid: Lite Extra Ball |
| 06 | Grid: Silver Ball |
| 07 | Grid: Captain Walker |
| 08 | Grid: Wizard |
| 09 | Skill Shot |
| 10** | ...O (Insert X2) |
| 11 | Grid: Smash the Mirror |
| 12 | Grid: Fiddle About |
| 13 | Grid: Acid Queen |
| 14 | Grid: There's A Doctor |
| 15 | Grid: Tommy Scoring |
| 16 | Grid: Sally Simpson |
| 17 | Jackpot |
| 18 | Double Jackpot |
| 19** | ...M (Insert X2) |
| 20 | Left Ramp Stand-Up Left |
| 21 | Left Ramp Stand-Up Right |
| 22 | Left Ramp Stand-Up Top |
| 23* | Extra Ball Button (Cabinet) |
| 24 | Silver Ball |
| 25 | Left 3-Bank Stand-Up Bottom |
| 26 | Left 3-Bank Stand-Up Middle |
| 27 | Left 3-Bank Stand-Up Top |
| 28** | ...M (Insert X2) |
| 29 | Spinner Bonus Left |
| 30 | Extra Ball |
| 31 | Light Union Jack Left (Spinner) |
| 32 | Genius |
| 33 | Right 3-Bank Stand-Up Top |
| 34 | Right 3-Bank S.U. Middle |
| 35 | Right 3-Bank S.U. Bottom |
| 36 | Mystery |
| 37** | ...Y (Insert X2) |
| 38 | More Time |
| 39 | Captain Walker LT (See Note 1) |
| 40 | Captain Walker RT (See Note 1) |
| 41 | ...T (Playfield) |
| 42 | ...O (Playfield) |
| 43 | ...M (Playfield) |
| 44 | ...M (Playfield) |
| 45 | ...Y (Playfield) |
| 46 | Outlanes X2 |
| 47 | Mirror Multiball |
| 48 | Shoot Again |
| 49 | Left Turbo Bumper |
| 50 | Center Turbo Bumper |
| 51 | Right Turbo Bumper |
| 52 | Spinner Bonus |
| 53 | Lite Union Jack RT (Spinner) |
| 54 | Holiday Camp |
| 55 | Return Lanes X2 |
| 56 | Airplane (See Note 2) |
| 57 | Acid Queen Left |
| 58 | Acid Queen Center |
| 59 | Acid Queen Right |
| 60 | Sally Simpson LT (See Note 1) |
| 61 | Sally Simpson RT (See Note 1) |
| 62 | Scoop Multiball |
| 63 | Collect Union Jack |
| 64* | Credit Button (Cabinet) |

Normalization: the `Grid:` prefix and the `(See Note n)`, `(Spinner)` and `the` (in `Smash the Mirror`) words are printed in a smaller type; they are transcribed in the running text. Notes 1 and 2 are referenced as `See Note 1` / `See Note1` and `See Note 2`; the transcription spaces them uniformly.

## Lamp Locations drawing (printed page 35)

The playfield drawing places a balloon for every playfield lamp. Balloons `46` and `55` appear twice each (left and right outlane and return lane). Balloons `39`, `40`, `60` and `61` (the Note 1 ramp lamps) are drawn on the playfield at the ramp positions; `56` (Note 2) is drawn at the upper centre although the note says the airplane is not shown. Balloons `64*` and `23*` sit below the playfield outline at the cabinet front.
