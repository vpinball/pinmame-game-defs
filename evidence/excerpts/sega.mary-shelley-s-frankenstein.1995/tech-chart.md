# Mary Shelley's Frankenstein Tech Chart (820-6104-06)

Source: `Sega_1995_Mary_Shelley_s_Frankenstein_Solenoid_Switch_and_Lamp_Matrix_Charts.pdf` (SHA-256 `1aaf40f86466ad57b5e6c2dfc4d040dce2d8ddfe98a67855084815304129ed97`), one page, read from a 309 ppi colour scan. Footer as printed: `Abbr.: X=Times LT=Left RT=Right BOT=Bottom MID=Middle CT=Center P/F=Playfield D.T.=Drop Target S-U=Stand-Up` and `820-6104-06`.

Conventions: wrapped lines inside a cell are joined with a single space, except a hyphen that only breaks a word across lines (e.g. `Sarcopha-` / `gus`, `Franken-` / `stein`, `Out-` / `Lane`), which is joined without the hyphen. Quotation marks are printed with a space inside them (e.g. `" F "`); they are written here without those inner spaces. Small-type text above a coil/flashlamp description is given in square brackets. Letters in the lamp matrix cells 01-12 are large printed letters. The printed column heading spells `Drive Trans istor (D.T.)`, `D.T. Control Line Connect` and `Power Line Connnection`; the headings below use the normalized names. `[blank]` marks a blank cell, `[shaded]` a shaded cell, `[?...]` an uncertain reading. No other normalization was applied.

## Switched, CPU Controlled Auxiliary & Constant Power Solenoids

The table title is printed `Switched, CPU Controlled Auxillary & Constant Power Solenoids` (sic, `Auxillary`).

| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil/Flash Type |
|---|---|---|---|---|---|---|---|---|---|
| 1L | [Coil:] 6-Ball Assembly Lockout | Q46 (merged cell, repeated) | CPU (merged cell, repeated) | VIO-BRN | PPB J 2-1 | BRN | PPB J 6-1, 2 | 32v L | 25-1240 |
| 1R | [Flashlamp: X1 P/F, Insert X3] Flash above "A-N-K" | Q46 (merged cell, repeated) | CPU (merged cell, repeated) | BLK-BRN | PPB J 9-1 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 2L | [Coil:] Trough Up-Kicker (TRUK) | Q45 (merged cell, repeated) | CPU (merged cell, repeated) | VIO-RED | PPB J 2-2 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 2R | [Flashlamp: X2 P/F, Insert X2] Flashes above "F-R" | Q45 (merged cell, repeated) | CPU (merged cell, repeated) | BLK-RED | PPB J 9-2 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 3L | [Coil:] Auto Launch 50v | Q44/Q5 | CPU/PPB | VIO-ORN | PPB J 8-2 | YEL/VIO | PPB J 7-8 | 50v L | 24-940 |
| 3R | [Flashlamp: X1 P/F, Insert X3] Flash above "I-N" | Q44 | CPU | BLK-ORN | PPB J 9-3 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 4L | [Coil:] Bottom Scoop Kick-Big | Q43 (merged cell, repeated) | CPU (merged cell, repeated) | VIO-YEL | PPB J 2-4 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 4R | [Flashlamp: X4 P/F, Insert X0] Flashes by Pop Bumpers | Q43 (merged cell, repeated) | CPU (merged cell, repeated) | BLK-YEL | PPB J 9-4 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 5L | [Coil:] Top Scoop Kick-Big 50v | Q42/Q2 | CPU | VIO-GRN | PPB J 2-5 | YEL/VIO | PPB J 7-8 | 50v L | 23-800 |
| 5R | [Flashlamp: X2 P/F, Insert X2] Flashes by Spinner | Q42 | CPU/PPB | BLK-GRN | PPB J 9-5 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 6L | [Coil:] Playfield Ball Eject | Q41 (merged cell, repeated) | PPB | VIO-BLU | PPB J 2-6 | BRN | PPB J 6-1, 2 | 32v L | 24-940 |
| 6R | [Flashlamp: X3 P/F, Insert X1] Flashes Upr. Left Corner | Q41 (merged cell, repeated) | CPU | BLK-BLU | PPB J 9-6 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 7L | [Coil:] VUK 50v | Q40/Q4 (merged cell, repeated) | CPU (merged cell, repeated) | VIO-BLK | PPB J 8-4 | YEL/VIO | PPB J 7-8, 2 | 50v L | 24-940 |
| 7R | [Flashlamp: X3 P/F, Insert X1] Flashes around VUK | Q40/Q4 (merged cell, repeated) | CPU (merged cell, repeated) | BLK-VIO | PPB J 9-7 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 8L | [Coil:] Knocker 32v (In Cabinet) | Q39 (merged cell, repeated) | CPU (merged cell, repeated) | VIO-GRY | PPB J 2-8 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 8R | [Flashlamp: X0 P/F, Insert X0] Not used in this game. | Q39 (merged cell, repeated) | CPU (merged cell, repeated) | —.— | —.— | —.— | —.— | —.— | —.— |
| 09 | [Coil:] Ramp Trap Door Right | Q30 | CPU | BRN-BLK | CPU CN 12-1 | RED | PS CN 3-6,7 | 32v | 28-1050 |
| 10 | [Coil: Loc. on PPB in Backbox] Left & Right Relay | Q29 | CPU | BLK-RED | CPU CN 12-2 | RED | PS CN 6-7 | 32v | 24v DC 10A DPDT |
| 11 | [Coil: Loc. on P/S Bd.] G.I. Relay | Q28 | CPU | BRN-ORN | CPU CN 12-4 | RED | PS CN 3-6,7 | 32v | 24v DC 10A DPDT |
| 12 | [Coil:] Ramp Trap Door Left | Q27 | CPU | BRN-YEL | CPU CN 12-5 | RED | PS CN 3-6,7 | 32v | 28-1050 |
| 13 | [Coil:] Monster Arms 50v | Q26/Q3 | CPU/PPB | BRN-GRN | PPB J 8-7 | VIO-YEL | PPB J 7-3 | 50v | 23-800 |
| 14 | [Coil:] Right Orbit Ball Diverter | Q25 | CPU | BRN-BLU | CPU CN 12-7 | RED | PS CN 3-6, 7 | 32v | 27-1400 |
| 15 | [Flashlamp: X4 P/F, Insert X0] Flashes around VUK | Q24 | CPU | BRN-VIO | CPU CN 12-8 | RED | PS CN 3-6,7 | 32v | 27-1500 |
| 16 | [Coil:] Laser Kick 50v | Q23/Q1 | CPU/PPB | BRN-GRY | PPB J8-12 | VIO-YEL | PPB J 7-3 | 50v | 23-800 |
| 17 | [Coil:] Top Turbo Bumper | Q11 | CPU | BLU-BRN | CPU CN 19-7 | RED | PS CN 3-6 | 32v | 23-700 |
| 18 | [Coil:] Middle Left Turbo Bumper | Q9 | CPU | BLU-RED | CPU CN 19-4 | RED | PS CN 3-6 | 32v | 23-700 |
| 19 | [Coil:] Mid. Right Turbo Bumper | Q8 | CPU | BLU-ORN | CPU CN 19-3 | RED | PS CN 3-6 | 32v | 23-700 |
| 20 | [Coil:] Bottom Turbo Bumper | Q10 | CPU | BLU-YEL | CPU CN 19-6 | RED | PS CN 6-6, 7 | 32v | 23-800 |
| 21 | [Coil:] Left Slingshot | Q12 | CPU | BLU-GRN | CPU CN 19-8 | RED | PS CN 6-6, 7 | 32v | 23-800 |
| 22 | [Coil:] Right Slingshot | [?Q13] | CPU | BLU-BLK | CPU CN 19-9 | RED | PS CN 6-6, 7 | 32v | 23-800 |

The 8R row prints the placeholder `—.—` in the control line, connect, power line, power connection, power description and type cells. Rows 1L-8R: 16 rows; rows 09-22: 14 rows; total 30. Rows 7L/7R share one printed Q40/Q4 and CPU cell; 1, 2, 4, 6 (transistor only) and 8 likewise share a transistor cell, and 1, 2, 4, 8 share the board cell.

## Switch Matrix Chart

Header text: `Column (Drive)` / `Row (Return)`. Column headings (each printed as number, drive transistor, drive wire, connector; shaded cells):

| Column | Drive transistor | Drive wire | Connector |
|---|---|---|---|
| 1 | Q55 | GRN-BRN | CN8-1 |
| 2 | Q54 | GRN-RED | CN8-2 |
| 3 | Q53 | GRN-ORN | CN8-3 |
| 4 | Q52 | GRN-YEL | CN8-4 |
| 5 | Q51 | GRN-BLK | CN8-5 |
| 6 | Q50 | GRN-BLU | CN8-7 |
| 7 | Q49 | GRN-VIO | CN8-8 |
| 8 | Q48 | GRN-GRY | CN8-9 |

Row headings (shaded; number, return wire, connector). The connector numbering skips CN10-4 as printed:

| Row | Return wire | Connector |
|---|---|---|
| 1 | WHT-BRN | CN10-9 |
| 2 | WHT-RED | CN10-8 |
| 3 | WHT-ORN | CN10-7 |
| 4 | WHT-YEL | CN10-6 |
| 5 | WHT-GRN | CN10-5 |
| 6 | WHT-BLU | CN10-3 |
| 7 | WHT-VIO | CN10-2 |
| 8 | WHT-GRY | CN10-1 |

Each cell prints its number small in the bottom-right corner. Number = (Column-1)*8 + Row.

| Number | Column | Row | Cell text |
|---|---|---|---|
| 01 | 1 | 1 | Plumb Tilt |
| 02 | 1 | 2 | 4th Coin |
| 03 | 1 | 3 | Credit Button |
| 04 | 1 | 4 | Right Coin |
| 05 | 1 | 5 | Center Coin |
| 06 | 1 | 6 | Left Coin |
| 07 | 1 | 7 | Slam Tilt |
| 08 | 1 | 8 | Extra Ball Button |
| 09 | 2 | 1 | #1 (Left) Ball Trough |
| 10 | 2 | 2 | #2 Ball Trough |
| 11 | 2 | 3 | #3 Ball Trough |
| 12 | 2 | 4 | #4 Ball Trough |
| 13 | 2 | 5 | #5 Ball Trough |
| 14 | 2 | 6 | #6 Ball Trough |
| 15 | 2 | 7 | #7 (Right) Ball Trough |
| 16 | 2 | 8 | Shooter Lane |
| 17 | 3 | 1 | Bottom 2-Bank S-U Left "F" |
| 18 | 3 | 2 | Bottom 2-Bank S-U Right "R" |
| 19 | 3 | 3 | Middle 3-Bank S-U Bot. "A" |
| 20 | 3 | 4 | Middle 3-Bank S-U Mid. "N" |
| 21 | 3 | 5 | Middle 3-Bank S-U Top "K" |
| 22 | 3 | 6 | Top 3-Bank S-U Left "E" |
| 23 | 3 | 7 | Top 3-Bank S-U Mid. "N" |
| 24 | 3 | 8 | Top 3-Bank S-U Right "S" |
| 25 | 4 | 1 | Middle 1-Bank S-U "Move Jackpot" |
| 26 | 4 | 2 | Ramp 1-Bank S-U Left "T" |
| 27 | 4 | 3 | Ramp 1-Bank S-U Right "E" |
| 28 | 4 | 4 | Right 2-Bank S-U Top "I" |
| 29 | 4 | 5 | Right 2-Bank S-U Bot. "N" |
| 30 | 4 | 6 | Not Used |
| 31 | 4 | 7 | Sarcophagus Upper Scoop |
| 32 | 4 | 8 | Geneva Lower Scoop |
| 33 | 5 | 1 | Left Orbit Rollover Bottom |
| 34 | 5 | 2 | Left Orbit Rollover Top |
| 35 | 5 | 3 | Right Orbit Rollover Top |
| 36 | 5 | 4 | Right Orbit Rollover Bottom |
| 37 | 5 | 5 | Left Outlane Rollover |
| 38 | 5 | 6 | Left Return Lane Rollover |
| 39 | 5 | 7 | Rt. Return Lane Rollover |
| 40 | 5 | 8 | Right Outlane Rollover |
| 41 | 6 | 1 | Top Turbo Bumper |
| 42 | 6 | 2 | Mid. Left Turbo Bumper |
| 43 | 6 | 3 | Mid. Right Turbo Bumper |
| 44 | 6 | 4 | Bottom Turbo Bumper |
| 45 | 6 | 5 | Ramp Entrance Gate |
| 46 | 6 | 6 | Ramp Exit Gate |
| 47 | 6 | 7 | Left Slingshot |
| 48 | 6 | 8 | Right Slingshot |
| 49 | 7 | 1 | Not Used |
| 50 | 7 | 2 | Not Used |
| 51 | 7 | 3 | Not Used |
| 52 | 7 | 4 | Not Used |
| 53 | 7 | 5 | "North Pole" VUK |
| 54 | 7 | 6 | "Ingolstadt" Rt. Orbit Spinner |
| 55 | 7 | 7 | "Ice Cave" above Ball Eject |
| 56 | 7 | 8 | Mini-Orbit Rollover By Eject |
| 57 | 8 | 1 | Not Used |
| 58 | 8 | 2 | Not Used |
| 59 | 8 | 3 | Not Used |
| 60 | 8 | 4 | Not Used |
| 61 | 8 | 5 | Not Used |
| 62 | 8 | 6 | "The Switch" Lever |
| 63 | 8 | 7 | Left Flipper Lower |
| 64 | 8 | 8 | Right Flipper Upr./Lwr. |

Typical Switch (Side View) drawing: a microswitch with terminals labelled `NC`, `NO`, `COM`; a `WHT` wire at the `NC` terminal side and a `GRN` wire at the `NO` terminal; a diode drawn from the `WHT` wire junction (below `NC`) to the `COM` terminal; caption `Diode 1N4001`.

In cell 25 the words `"Move Jackpot"` are printed in smaller type below `Middle 1-Bank S-U`.

## Lamp Matrix Chart

Header text: `Column 18V` / `Row GND`. Column headings (shaded; number, transistor, wire, connector). The connector numbering skips CN7-5 as printed:

| Column | Transistor | Wire | Connector |
|---|---|---|---|
| 1 | Q71 | YEL-BRN | CN7-1 |
| 2 | Q70 | YEL-RED | CN7-2 |
| 3 | Q69 | YEL-ORN | CN7-3 |
| 4 | Q68 | YEL-BLK | CN7-4 |
| 5 | Q67 | YEL-GRN | CN7-6 |
| 6 | Q66 | YEL-BLU | CN7-7 |
| 7 | Q65 | YEL-VIO | CN7-8 |
| 8 | Q64 | YEL-GRY | CN7-9 |

Row headings (shaded; number, transistor, wire, connector). The connector numbering skips CN6-4 as printed:

| Row | Transistor | Wire | Connector |
|---|---|---|---|
| 1 | Q72 | RED-BRN | CN6-1 |
| 2 | Q73 | RED-BLK | CN6-2 |
| 3 | Q74 | RED-ORN | CN6-3 |
| 4 | Q75 | RED-YEL | CN6-5 |
| 5 | Q76 | RED-GRN | CN6-6 |
| 6 | Q77 | RED-BLU | CN6-7 |
| 7 | Q78 | RED-VIO | CN6-8 |
| 8 | Q79 | RED-GRY | CN6-9 |

Cells 01-12 (column 1 rows 1-8, column 2 rows 1-4) are printed as large letters that spell F R A N K E N / S T E I N (FRANKENSTEIN), each with its small number; the letter is given as the cell text. Number = (Column-1)*8 + Row.

| Number | Column | Row | Cell text |
|---|---|---|---|
| 01 | 1 | 1 | F |
| 02 | 1 | 2 | R |
| 03 | 1 | 3 | A |
| 04 | 1 | 4 | N |
| 05 | 1 | 5 | K |
| 06 | 1 | 6 | E |
| 07 | 1 | 7 | N |
| 08 | 1 | 8 | S |
| 09 | 2 | 1 | T |
| 10 | 2 | 2 | E |
| 11 | 2 | 3 | I |
| 12 | 2 | 4 | N |
| 13 | 2 | 5 | Top Turbo Bumper |
| 14 | 2 | 6 | Mid. Left Turbo Bumper |
| 15 | 2 | 7 | Mid. Right Turbo Bumper |
| 16 | 2 | 8 | Bottom Turbo Bumper |
| 17 | 3 | 1 | Frankenstein Millions Mode |
| 18 | 3 | 2 | Stoning Mode |
| 19 | 3 | 3 | Creature Feature Mode |
| 20 | 3 | 4 | Lynch Justine Mode |
| 21 | 3 | 5 | North Pole Mode |
| 22 | 3 | 6 | Lite Extra Ball Mode |
| 23 | 3 | 7 | Voltage Mode |
| 24 | 3 | 8 | Graveyard Mode |
| 25 | 4 | 1 | [?Ramp Jackpot] |
| 26 | 4 | 2 | North Pole VUK Jackpot |
| 27 | 4 | 3 | Ice Cave Ball Eject Jackpot |
| 28 | 4 | 4 | Left Orbit Jackpot |
| 29 | 4 | 5 | Geneva Lower Scoop |
| 30 | 4 | 6 | Sarcophagus Upper Scoop |
| 31 | 4 | 7 | VUK Entrance Left |
| 32 | 4 | 8 | VUK Entrance Right |
| 33 | 5 | 1 | Left Outlane Alive Kick-Back |
| 34 | 5 | 2 | Left Outlane Special |
| 35 | 5 | 3 | Left Return Lane Lite Ingolstadt |
| 36 | 5 | 4 | Rt. Return Lane Lite Geneva |
| 37 | 5 | 5 | Outlane Double Bonus |
| 38 | 5 | 6 | Ice Cave Mode |
| 39 | 5 | 7 | Lite Lock 1 |
| 40 | 5 | 8 | Lite Lock 2 |
| 41 | 6 | 1 | Move Jackpot |
| 42 | 6 | 2 | Change Scene |
| 43 | 6 | 3 | Ingolstadt Spinner Mode |
| 44 | 6 | 4 | Jackpot Grows |
| 45 | 6 | 5 | Justine Mode |
| 46 | 6 | 6 | Extra Ball |
| 47 | 6 | 7 | Creature Mode |
| 48 | 6 | 8 | Shooter Lane |
| 49 | 7 | 1 | Not Used |
| 50 | 7 | 2 | Not Used |
| 51 | 7 | 3 | Not Used |
| 52 | 7 | 4 | Not Used |
| 53 | 7 | 5 | Not Used |
| 54 | 7 | 6 | Not Used |
| 55 | 7 | 7 | Live Again |
| 56 | 7 | 8 | VUK Entrance Middle |
| 57 | 8 | 1 | Not Used |
| 58 | 8 | 2 | Not Used |
| 59 | 8 | 3 | Not Used |
| 60 | 8 | 4 | Not Used |
| 61 | 8 | 5 | Not Used |
| 62 | 8 | 6 | Not Used |
| 63 | 8 | 7 | Extra-Ball Button |
| 64 | 8 | 8 | Start Button |

Note on cell 25: a faint orange-brown dash lies after `Ramp` on the first line; it looks like a print artefact, so the cell is read as `Ramp Jackpot` with an uncertain flag.

## Fuse and board blocks

### Backbox Bridges, Mounted in Backbox

| Fuse | Bridge | Text |
|---|---|---|
| F1 | BR2 | 8A Slo-Blo 32v DC Coils/Flashers |
| F2 | BR1 | 8A Slo-Blo 18v DC Lamps |
| F3 | BR3 | 8A Slo-Blo 18v DC Display |

The drawing beside it shows a circle with BR1, BR2, BR3 and F1, F2, F3 callouts and two large capacitors.

### Cabinet Fuses

| Row | Text |
|---|---|
| Main Fuse Line | 8A Slo-Blo 250v |
| International | 2X 4A Slo-Blo 250v |

### Solid State 3-Flipper, SSFB

| Fuse | Text |
|---|---|
| F1 | 3A 250vSlo-Blo 50v DC Output (All Fuses) Right Flipper |
| F2 | 3A 250v Slo-Blo 9v AC Holding |
| F3 | 3A 250v Slo-Blo 50v DC Output Left Flipper |
| F4 | 3A 250v Slo-Blo 9v AC Holding |
| F5 | 3A 250v Slo-Blo 50v DC Output Upper Flipper |

The `250vSlo-Blo` spacing in F1 is as printed. The drawing shows F1-F5 callouts around the board labelled `SSFB`.

### Power Supply Board, PSB

| Fuse | Text |
|---|---|
| F1 | 7A Slo-Blo +5vDC Reg. Input (9vAC) |
| F2 | 7A Slo-Blo +5vDC Reg. Input (9vAC) |
| F3 | Not Used |
| F4 | 8A Slo-Blo Switched Ill. Buss (18vDC) |
| F5 | 4A Slo-Blo Solenoid (32vDC) Bumpers, Slingshots, etc. |
| F6 | 5A Slo-Blo Solenoid Buss (32vDC) L/R Relay Coils/Flash |

Drawing of the `PSB` board with callouts F1, F2, F4, F5, F6 and an arrow from the label `G.I. Relay` pointing to a square component near the top right of the board.

### Playfield Power Board, PPB

| Fuse | Text |
|---|---|
| F1 | G.I. 5A Slo-Blo Playfield |
| F2 | G.I. 5A Slo-Blo Backbox Dr./Spkr. Panel |
| F3 | G.I. 5A Slo-Blo Playfield & Coin Door |
| F4 | G.I. 5A Slo-Blo Backbox Door |
| F5 | 50v 5A Flippers /All 50v Coils |
| F6 | 32v Flash Lamps 3A Slo-Blo/Right |
| F7 | 32v 3A Coils/Flash Right/Left |
| F8 | 50v 4A / 50v Coils |
| F9 | 50v 5A Laser Kick |

Drawing of the `PPB` board with callouts F1-F9 and an arrow labelled `Left/Right Relay` pointing to a square component at the bottom of the board.

### Callouts

- `G.I. Relay` (arrow to the square component on the PSB drawing)
- `Left/Right Relay` (arrow to the square component on the PPB drawing)

### Address and hotline block

`SEGA PINBALL, INC.` logo (with `TM`), then in a bordered box:

```
1990 Janice Av.
Melrose Park, IL
60160
* * * *
Technical
Support
Hotline
1-800-KICKERS
Outside U.S.A.
Telephone
708-345-7700
Facsimile
708-345-001[?]
© 1994 Sega Pinball,[?] Inc.
USA
```

The fax number's last digit and the end of the copyright line are hidden by a white patch on the scan; the copyright line reads `© 1994 Sega Pinball,` followed by an obscured portion and `Inc.` partly visible. The game logo `MARY SHELLEY'S FRANKENSTEIN` is printed at the bottom left of the page.

## Uncertain readings

- Coil 22, Drive Transistor: `[?Q13]` (smudged print, reads Q13 with an overstrike on the Q).
- Lamp Matrix cell 25 (column 4, row 1): `[?Ramp Jackpot]` (stray dash after `Ramp`).
- Address block: fax number `708-345-001[?]` (final digit hidden by a white patch); copyright line `Sega Pinball,[?] Inc.` partly obscured.
