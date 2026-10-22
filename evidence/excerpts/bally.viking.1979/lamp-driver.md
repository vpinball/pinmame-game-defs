# Viking lamp driver output regions

Source: Bally Viking manual PDF pages 44 (W-1187-21c, LAMP DRIVER A5 and Table B) and 45 (W-1182-25d, A5 LAMP DRIVER SCHEMATIC).
Method: manual transcription and primary-curator visual check against the rendered page; OCR used only to locate cells.

The two source drawings label the headers, SCRs and decoder outputs; the public column below is DERIVED, not printed: public = 16 * PD + output + 1. PD0..PD3 are U1..U4 and selector 15 is disconnected. Connector designators are expanded with the printed A5 prefix. The wire-color numeric codes are retained separately; no unused pin is inferred from another game.

| Public (derived) | Decoder output | SCR | Connector | Printed function |
| ---: | --- | --- | --- | --- |
| 1 | U1:0 | A5Q14 | A5J1-18 | 1K BONUS |
| 2 | U1:1 | A5Q12 | A5J1-19 | 5K BONUS |
| 3 | U1:2 | A5Q13 | A5J1-17 | 9K BONUS |
| 4 | U1:3 | A5Q8 | A5J1-23 | 2X BONUS |
| 5 | U1:4 | A5Q9 | A5J1-14 | 1 SPINNER (BOTTOM) |
| 6 | U1:5 | A5Q10 | A5J1-15 | 5 SPINNER |
| 7 | U1:6 | A5Q11 | A5J1-16 | 9 SPINNER |
| 8 | U1:7 | A5Q4 | A5J1-28 | 1K IN LINE DROP TARGET |
| 9 | U1:8 | A5Q1 | A5J1-24 | 5K IN LINE DROP TARGET |
| 10 | U1:9 | A5Q2 | A5J1-25 | RIGHT LANE ARROW |
| 11 | U1:10 | A5Q3 | A5J2-21 and A5J1-26 | SHOOT AGAIN / SAME PLAYER S.A. |
| 12 | U1:11 | A5Q7 | A5J1-27 | RIGHT OUT 25K |
| 13 | U1:12 | A5Q16 | A5J2-22 | BALL IN PLAY |
| 14 | U1:13 | A5Q5 | A5J2-16 | 2K 3 DROP TARGET |
| 15 | U1:14 | A5Q6 | A5J2-14 | 10K 3 DROP TARGET |
| 17 | U2:0 | A5Q29 | A5J1-1 | 2K BONUS |
| 18 | U2:1 | A5Q27 | A5J1-9 | 6K BONUS |
| 19 | U2:2 | A5Q28 | A5J1-8 | 10K BONUS |
| 20 | U2:3 | A5Q35 | A5J1-3 | 3X BONUS |
| 21 | U2:4 | A5Q34 | A5J1-2 | 2 SPINNER |
| 22 | U2:5 | A5Q22 | A5J1-10 | 6 SPINNER |
| 23 | U2:6 | A5Q26 | A5J1-7 | 10 SPINNER (TOP) |
| 24 | U2:7 | A5Q25 | A5J1-6 | 2K IN LINE DROP TARGET |
| 25 | U2:8 | A5Q24 | A5J1-5 | IN LINE TARGET SPECIAL |
| 26 | U2:9 | A5Q17 | A5J1-11 | SAUCER BONUS & CENTER ARROW |
| 27 | U2:10 | A5Q23 | A5J2-8 | MATCH |
| 28 | U2:11 | A5Q21 | A5J1-12 | RIGHT FLIP. FEED SPECIAL |
| 29 | U2:12 | A5Q15 | A5J2-23 | HIGH SCORE TO DATE |
| 30 | U2:13 | A5Q18 | A5J2-20 | 4K 3 DROP TARGET |
| 31 | U2:14 | A5Q19 | A5J2-15 | 10X 3 DROP TARGET |
| 33 | U3:0 | A5Q36 | A5J3-26 | 3K BONUS |
| 34 | U3:1 | A5Q38 | A5J3-25 | 7K BONUS |
| 35 | U3:2 | A5Q44 | A5J3-19 | 20K BONUS |
| 36 | U3:3 | A5Q49 | A5J3-17 | 4X BONUS |
| 37 | U3:4 | A5Q48 | A5J3-16 | 3 SPINNER |
| 38 | U3:5 | A5Q37 | A5J3-23 | 7 SPINNER |
| 39 | U3:6 | A5Q32 | A5J3-27 | 100 SPINNER |
| 40 | U3:7 | A5Q20 | A5J1-13 | 3K IN LINE DROP TARGET |
| 41 | U3:8 | A5Q42 | A5J3-21 | LEFT RED TARGET 50K |
| 42 | U3:9 | A5Q41 | A5J3-20 | EXTRA BALL ARROW |
| 43 | U3:10 | A5Q40 | A5J3-22 | TOP SAUCER SPECIAL |
| 44 | U3:11 | A5Q39 | A5J3-24 | LEFT FLIP. FEED SPECIAL |
| 45 | U3:12 | A5Q33 | A5J2-11 | GAME OVER |
| 46 | U3:13 | A5Q30 | A5J2-6 | 6K 3 DROP TARGET |
| 47 | U3:14 | A5Q31 | A5J2-2 | "B" ROLLOVER |
| 49 | U4:0 | A5Q57 | A5J3-1 | 4K BONUS |
| 50 | U4:1 | A5Q50 | A5J3-12 | 8K BONUS |
| 51 | U4:2 | A5Q51 | A5J3-15 | 40K BONUS |
| 52 | U4:3 | A5Q54 | A5J3-11 | 5X BONUS |
| 53 | U4:4 | A5Q55 | A5J3-9 | 4 SPINNER |
| 54 | U4:5 | A5Q60 | A5J3-3 | 8 SPINNER |
| 55 | U4:6 | A5Q59 | A5J3-4 | 1000 SPINNER |
| 56 | U4:7 | A5Q58 | A5J3-2 | 4K IN LINE DROP TARGET |
| 57 | U4:8 | A5Q56 | A5J3-10 | IN LINE TARGET 50K |
| 58 | U4:9 | A5Q46 | A5J3-18 | SPECIAL ARROW |
| 59 | U4:10 | A5Q52 | A5J3-13 | CREDIT INDICATOR |
| 60 | U4:11 | A5Q53 | A5J3-14 | LEFT OUT 25K |
| 61 | U4:12 | A5Q47 | A5J2-10 | TILT |
| 62 | U4:13 | A5Q43 | A5J2-7 | 8K 3 DROP TARGET |
| 63 | U4:14 | A5Q45 | A5J2-1 | "A" ROLLOVER |

The Q3 branch to J1-26 is a second physical emitter on the playfield, sharing the backglass Shoot Again at J2-21. The composite name in the derived row records both literal cells.

## Complete A5J1 output header (pin order normalized)

| Pin | Printed WIRE code | Printed function |
| ---: | --- | --- |
| 1 | 41 | 2K BONUS |
| 2 | 43 | 2 SPINNER |
| 3 | 45 | 3X BONUS |
| 4 | 35 | N/U |
| 5 | 48 | IN LINE TARGET SPECIAL |
| 6 | 25 | 2K IN LINE DROP TARGET |
| 7 | 34 | 10 SPINNER (TOP) |
| 8 | 51 | 10K BONUS |
| 9 | 52 | 6K BONUS |
| 10 | 23 | 6 SPINNER |
| 11 | 65 | SAUCER BONUS & CENTER ARROW |
| 12 | 61 | RIGHT FLIP. FEED SPECIAL |
| 13 | 96 | 3K IN LINE DROP TARGET |
| 14 | 54 | 1 SPINNER (BOTTOM) |
| 15 | 13 | 5 SPINNER |
| 16 | 12 | 9 SPINNER |
| 17 | 57 | 9K BONUS |
| 18 | 58 | 1K BONUS |
| 19 | 60 | 5K BONUS |
| 20 | [blank] | KEY |
| 21 | [blank] | N/U |
| 22 | [blank] | N/U |
| 23 | 56 | 2X BONUS |
| 24 | 50 | 5K IN LINE DROP TARGET |
| 25 | 90 | RIGHT LANE ARROW |
| 26 | 91 | SAME PLAYER S.A. |
| 27 | 53 | RIGHT OUT 25K |
| 28 | 78 | 1K IN LINE DROP TARGET |

## Complete A5J2 output header (pin order normalized)

| Pin | Printed WIRE code | Printed function |
| ---: | --- | --- |
| 1 | 60 | "A" ROLLOVER |
| 2 | 20 | "B" ROLLOVER |
| 3 | 84 | N/U |
| 4 | 72 | N/U |
| 5 | [blank] | N/U |
| 6 | 85 | 6K 3 DROP TARGET |
| 7 | 91 | 8K 3 DROP TARGET |
| 8 | 93 | MATCH |
| 9 | [blank] | N/U |
| 10 | 98 | TILT |
| 11 | 95 | GAME OVER |
| 12 | 61 | N/U |
| 13 | 53 | N/U |
| 14 | 12 | 10K 3 DROP TARGET |
| 15 | 23 | 10X 3 DROP TARGET |
| 16 | 34 | 2K 3 DROP TARGET |
| 17 | [blank] | N/U |
| 18 | [blank] | KEY |
| 19 | [blank] | N/U |
| 20 | 35 | 4K 3 DROP TARGET |
| 21 | 47 | SHOOT AGAIN |
| 22 | 62 | BALL IN PLAY |
| 23 | 97 | HIGH SCORE TO DATE |

## Complete A5J3 output header (pin order normalized)

| Pin | Printed WIRE code | Printed function |
| ---: | --- | --- |
| 1 | 10 | 4K BONUS |
| 2 | 95 | 4K IN LINE DROP TARGET |
| 3 | 81 | 8 SPINNER |
| 4 | 14 | 1000 SPINNER |
| 5 | [blank] | N/U |
| 6 | [blank] | N/U |
| 7 | [blank] | N/U |
| 8 | [blank] | KEY |
| 9 | 15 | 4 SPINNER |
| 10 | 91 | IN LINE TARGET 50K |
| 11 | 20 | 5X BONUS |
| 12 | 21 | 8K BONUS |
| 13 | 13 | CREDIT INDICATOR |
| 14 | 84 | LEFT OUT 25K |
| 15 | 53 | 40K BONUS |
| 16 | 25 | 3 SPINNER |
| 17 | 27 | 4X BONUS |
| 18 | 56 | SPECIAL ARROW |
| 19 | 67 | 20K BONUS |
| 20 | 64 | EXTRA BALL ARROW |
| 21 | 30 | LEFT RED TARGET 50K |
| 22 | 23 | TOP SAUCER SPECIAL |
| 23 | 98 | 7 SPINNER |
| 24 | 72 | LEFT FLIP. FEED SPECIAL |
| 25 | 36 | 7K BONUS |
| 26 | 38 | 3K BONUS |
| 27 | 40 | 100 SPINNER |
| 28 | [blank] | N/U |

The plug-connector page gives J1-21 N/U, J1-22 N/U and J1-4 N/U; J2-3,4,5,9,12,13,17,19 N/U, J2-18 KEY; J3-5,6,7,28 N/U and J3-8 KEY. The lamp-driver schematic p45 instead interchanges the printed J3-7/J3-8 KEY and N/U cells; both are preserved here as a wiring-detail disagreement. No controlled lamp is attached to either position. Printed N/U cells are retained literally. Source schematic header placement TO BACK BOX does not prove every J2 circuit ends there: its Table B explicitly routes eight pins to the playfield.

## Complete Table B, PANEL TO BACK CAB. PLUG

| FROM | TO | WIRE |
| --- | ---: | --- |
| A5J2-14 | 1 | 12 |
| A5J2-2 | 2 | 20 |
| A5J2-15 | 3 | 23 |
| A5J2-16 | 4 | 34 |
| A5J2-20 | 5 | 35 |
| A5J2-1 | 6 | 60 |
| A5J2-6 | 7 | 85 |
| A5J2-7 | 8 | 91 |

## Complete wire color code legend

| Code | Color |
| ---: | --- |
| 1 | RED |
| 2 | BLUE |
| 3 | YELLOW |
| 4 | GREEN |
| 5 | WHITE |
| 6 | BROWN |
| 7 | ORANGE |
| 8 | BLACK |
| 9 | GRAY |
| 0 | NO TRACE |
