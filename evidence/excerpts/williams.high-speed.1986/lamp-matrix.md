# High Speed — Lamp-Matrix Table

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 4 — the unpaginated quick-reference
foldout bound at the front of this copy, which carries the Switch-Matrix Table on its upper half and
the Lamp-Matrix Table on its lower half. Read from a 300 dpi `pdftoppm` render. The accompanying crop
covers the legend and the first three columns, where the "two lamps in circuit" markers are.

Public address = `(column - 1) * 8 + row`, the same System 11 sequential column-major numbering the
switch matrix uses; the printed number in each cell is that public address.

## Legend, verbatim

> `[2]` Two lamps in circuit.

The marker is a small boxed numeral 2 printed inside the cell, next to the address. Sweeping all 64
cells of the rendered page, the marker appears on **four** addresses and no others: **1, 3, 9, 40**.
Columns 4 through 8 carry the marker on address 40 only; columns 1-3 carry it on 1, 3 and 9. No cell
carries any other marker or footnote.

## Column and row wiring, verbatim

Column headers (drive): 1 = Q66 YEL-BRN 1J7-1; 2 = Q64 YEL-RED 1J7-2; 3 = Q62 YEL-ORN 1J7-3;
4 = Q60 YEL-BLK 1J7-4; 5 = Q58 YEL-GRN 1J7-6; 6 = Q56 YEL-BLU 1J7-7; 7 = Q54 YEL-VIO 1J7-8;
8 = Q52 YEL-GRY 1J7-9. (1J7-5 is skipped.)

Row headers (return): 1 = Q80 RED-BRN 1J6-1; 2 = Q81 RED-BLK 1J6-2; 3 = Q82 RED-ORN 1J6-3;
4 = Q83 RED-YEL 1J6-5; 5 = Q84 RED-GRN 1J6-6; 6 = Q85 RED-BLU 1J6-7; 7 = Q86 RED-VIO 1J6-8;
8 = Q87 RED-GRY 1J6-9. (1J6-4 is skipped.)

Unlike the switch matrix, this page names a driver transistor for the **rows** as well as the columns.

## The full 8 x 8 matrix, verbatim cell text

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Game Over `[2]` (1) | Flipper Return Lanes `[2]` (9) | Upper Left Target Bank - Red Light (17) | Standup Target Arrow #1 (25) | Freeway Scores 75,000 (33) | Stoplights Light Escape (Center) (41) | Bonus 5000 (49) | Bonus 40,000 (57) |
| 2 | Match (2) | Center Spinner 1000 Arrow (10) | Upper Left Target Bank - Yellow Light (18) | Standup Target Arrow #2 (26) | Freeway Scores 100,000 (34) | Ramp Stoplight Red Light (42) | Bonus 6000 (50) | Bonus 50,000 (58) |
| 3 | Shoot Again - Drive Again `[2]` (3) | Extra Ball (Eject Hole) (11) | Upper Left Target Bank - Green Light (19) | Standup Target Arrow #3 (27) | Freeway Lights Extra Ball (35) | Ramp Stoplight Yellow Light (43) | Bonus 7000 (51) | Bonus 60,000 (59) |
| 4 | Left Outlane Special (4) | Escape (Eject Hole) (12) | Left Freeway Arrow (20) | Standup Target Arrow #4 (28) | Ramp Earns Bonus X (36) | Ramp Stoplight Green Light (44) | Bonus 8000 (52) | Bonus 5X (60) |
| 5 | Right Outlane Special (5) | Lower Left Target Bank - Red Light (13) | Right Freeway Arrow (21) | Standup Target Arrow #5 (29) | Ramp Earns Ramp Bonus (37) | Bonus 1000 (45) | Bonus 9000 (53) | Bonus 4X (61) |
| 6 | Ball In Play (6) | Lower Left Target Bank - Yellow Light (14) | Right Target Bank - Red Light (22) | Standup Target Arrow #6 (30) | Ramp Earns Getaway (38) | Bonus 2000 (46) | Bonus 10,000 (54) | Hold Bonus (62) |
| 7 | Left Spinner 1000 Arrow (7) | Lower Left Target Bank - Green Light (15) | Right Target Bank - Yellow Light (23) | Freeway Scores 25,000 (31) | Ramp Earns Hideout (39) | Bonus 3000 (47) | Bonus 20,000 (55) | Bonus 3X (63) |
| 8 | Right Spinner 1000 Arrow (8) | Left Outlane Kickback Arrow (16) | Right Target Bank - Green Light (24) | Freeway Scores 50,000 (32) | Ramp Earns Hideout Jackpot `[2]` (40) | Bonus 4000 (48) | Bonus 30,000 (56) | Bonus 2X (64) |

All 64 addresses carry a device name. No lamp address is printed "Not Used" on this page — unlike the
switch matrix, where twelve are.

## Wording differences against the Lamps parts list (printed page 33)

Both pages are transcribed in full; `lamp-locations.md` holds the parts list. The differences are all
synonymous or additive rather than contradictory:

- 9: this page "Flipper Return Lanes"; parts list "20,000 Light Kickback (Left & Right Flipper
  Lanes)" — the parts list also supplies the two bulb locations that make the `[2]` marker concrete.
- 1, 2, 6: this page "Game Over" / "Match" / "Ball In Play"; parts list adds "(Backglass)" to each.
- 3: this page "Shoot Again - Drive Again"; parts list splits the two bulbs of the `[2]` circuit as
  "Shoot Again (Backglass)" and "Drive Again (Playfield)".
- 17-19, 13-15, 22-24: this page "…Target Bank - Red/Yellow/Green Light"; parts list "Red/Yellow/Green
  Light (Upr Left / Lwr Left / Right Target Bank)".
- 42-44: this page "Ramp Stoplight Red/Yellow/Green Light"; parts list "Red/Yellow/Green Light (Ramp
  Stoplight)".
- 41: this page "Stoplights Light Escape (Center)"; parts list "Stoplights Light Escape (Center)".
