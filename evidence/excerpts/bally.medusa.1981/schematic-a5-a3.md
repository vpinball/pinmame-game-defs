# Medusa A5 and A3 schematic transcription

Source: Bally_1981_Medusa_Schematics_paginated.pdf SHA256
`a4a8d3c6717cde7afc8015e556400ddec19c420bc1f3990977c8514a872b93b6`.
PDF pages5 (A5 W-1182-35) and6 (A3). Entire authoring-relevant connector
regions, preserving blank versus not drawn versus N/U. Transcribed by
GPT Terra; primary GPT Sol checked the decoder/SCR sequence and output paths
against native renders. Table claims remain independently inspectable in the
retained originals. Wire codes are not completed from another game's harness.

## A5 lamp decoder to SCR to connector

The public address is derived from the pinned `by35_lampStrobe` and sequential lamp conversion: for decoder `Uk` and output `Sa`, public address is `16 × (k − 1) + a + 1`. Each decoder’s S15 is unpopulated on the sheet, and the strobe code excludes address `0x0f`. The function text below is the **page 05 connector label**. Shared branches are listed together; a connector labelled `N/U` can still be electrically tied to another connector.

### U1

| Public | Decoder | SCR | Page 05 connector and literal function |
| ---: | --- | --- | --- |
| 1 | S0 | Q14 | J1-18 — 10K RIGHT GATE LANE |
| 2 | S1 | Q12 | J1-19 — 50K RIGHT GATE LANE |
| 3 | S2 | Q13 | J1-17 — 50K SAUCER |
| 4 | S3 | Q8 | J1-23 — L & R GATE LANE ARROW |
| 5 | S4 | Q9 | J1-14 — 2X LEFT GATE LANE |
| 6 | S5 | Q10 | J1-15 — 1K MEDUSA BONUS |
| 7 | S6 | Q11 | J1-16 — 5K MEDUSA BONUS |
| 8 | S7 | Q4 | J1-28 — 9K MEDUSA BONUS |
| 9 | S8 | Q1 | J1-24 — SPECIAL SAUCER |
| 10 | S9 | Q2 | J1-25 — TOP “B” ARROW |
| 11 | S10 | Q3 | J1-26 — N/U; **J2-21 — SHOOT AGAIN** |
| 12 | S11 | Q7 | J1-27 — #1 TARGET ARROW; **J2-13 — N/U** |
| 13 | S12 | Q16 | J2-22 — BALL IN PLAY |
| 14 | S13 | Q5 | J2-16 — 30K COLOSSUS BONUS |
| 15 | S14 | Q6 | J2-14 — 150K COLOSSUS BONUS |

### U2

| Public | Decoder | SCR | Page 05 connector and literal function |
| ---: | --- | --- | --- |
| 17 | S0 | Q29 | J1-1 — 20K RIGHT GATE LANE |
| 18 | S1 | Q27 | J1-9 — SPECIAL RIGHT GATE LANE |
| 19 | S2 | Q28 | J1-8 — 100K SAUCER |
| 20 | S3 | Q35 | J1-3 — 3 ADVANCE OLYMPUS |
| 21 | S4 | Q34 | J1-2 — 3X LEFT GATE LANE, 2X BONUS |
| 22 | S5 | Q22 | J1-10 — 2K MEDUSA BONUS |
| 23 | S6 | Q26 | J1-7 — 6K MEDUSA BNNUS |
| 24 | S7 | Q25 | J1-6 — 10K MEDUSA BONUS |
| 25 | S8 | Q24 | J1-5 — SAUCER BONUS ARROW |
| 26 | S9 | Q17 | J1-11 — TOP “A” ARROW |
| 27 | S10 | Q23 | J2-8 — MATCH; **J1-4 — N/U** |
| 28 | S11 | Q21 | J2-12 — N/U; **J1-12 — #2 TARGET ARROW** |
| 29 | S12 | Q15 | J2-23 — HIGH SCORE TO DATE |
| 30 | S13 | Q18 | J2-20 — 60K COLOSSUS BONUS |
| 31 | S14 | Q19 | J2-15 — COLOSSUS SPECIAL |

### U3

| Public | Decoder | SCR | Page 05 connector and literal function |
| ---: | --- | --- | --- |
| 33 | S0 | Q36 | J3-26 — 30K RIGHT GATE LANE |
| 34 | S1 | Q38 | J3-25 — TO AUX. EXPANDER J1-2 |
| 35 | S2 | Q44 | J3-19 — 150K SAUCER |
| 36 | S3 | Q49 | J3-17 — 2 ADVANCE OLYMPUS |
| 37 | S4 | Q48 | J3-16 — 5X LEFT GATE, 3X BONUS |
| 38 | S5 | Q37 | J3-23 — 3K MEDUSA BONUS |
| 39 | S6 | Q32 | J3-27 — 7K MEDUSA BONUS |
| 40 | S7 | Q20 | J1-13 — 20K MEDUSA BONUS |
| 41 | S8 | Q42 | J3-21 — LAST BALL X-TENDED PLAY |
| 42 | S9 | Q41 | J3-20 — 60K MEDUSA BONUS |
| 43 | S10 | Q40 | J3-22 — SAME PLAYER SHOOT AGAIN; **J2-9 — N/U** |
| 44 | S11 | Q39 | J3-24 — #3 TARGET ARROW; **J2-4 — N/U** |
| 45 | S12 | Q33 | J2-11 — GAME OVER |
| 46 | S13 | Q30 | J2-6 — 90K COLOSSUS BONUS |
| 47 | S14 | Q31 | J2-2 — TOP MIDDLE BACK TARGET |

### U4

| Public | Decoder | SCR | Page 05 connector and literal function |
| ---: | --- | --- | --- |
| 49 | S0 | Q57 | J3-1 — 40K RIGHT GATE LANE |
| 50 | S1 | Q50 | J3-12 — N/U |
| 51 | S2 | Q51 | J3-15 — 200K SAUCER |
| 52 | S3 | Q54 | J3-11 — 1 ADVANCE OLYMPUS |
| 53 | S4 | Q55 | J3-9 — 50K LEFT GATE LANE, 5X BONUS |
| 54 | S5 | Q60 | J3-3 — 4K MEDUSA BONUS |
| 55 | S6 | Q59 | J3-4 — 8K MEDUSA BONUS |
| 56 | S7 | Q58 | J3-2 — 40K MEDUSA BONUS |
| 57 | S8 | Q56 | J3-10 — SAUCER X-TENDED PLAY ARROW |
| 58 | S9 | Q46 | J3-18 — 80K MEDUSA BONUS; **J2-5 — N/U** |
| 59 | S10 | Q52 | J3-13 — CREDIT INDICATOR; **J2-3 — N/U** |
| 60 | S11 | Q53 | J3-14 — #21 TOP OF PANEL (RIGHT) |
| 61 | S12 | Q47 | J2-10 — TILT |
| 62 | S13 | Q43 | J2-7 — 120K COLOSSUS BONUS |
| 63 | S14 | Q45 | J2-1 — SPECIAL MEDUSA |

The `**` marks on some SCRs are omitted from the table’s identifiers; page 05’s note uses them to distinguish SCR part types. The marks do not change the connector traces. Connector labels and `N/U` are preserved as printed; they are not independent proof of physical socket fitment.

## A3 connector and function inventory

The page 06 connector note specifies J1 key pin 7, J2 key pin 3, J3 key pin 2, J4 key pin 2, and J5 key pin 6. **Not shown** below means the pin has no entry drawn on this sheet; it does not mean `N/U`.

The primary’s independently confirmed harness result is used for the public/self-test relationship: public 1–15 correspond to printed tests 1–15; with lamp 34 set, public 1–6 and 8 correspond to printed tests 16–22. The page 06 `OR` labels are preserved.

### J1 — playfield connector

| Pin | Page 06 function or status | Traced driver / note |
| ---: | --- | --- |
| 1 | Not shown | — |
| 2 | 4 DROP TARGET RESET OR CLOSE MOVABLE FLIPPER | Q1; public 2 / printed tests 2 or 17 |
| 3 | KNOCKER OR OPEN MOVABLE FLIPPER | Q2; public 1 / printed tests 1 or 16 |
| 4 | Not shown | — |
| 5 | SHIELD OF THE GODS POST | Q4; public 7 / printed test 7 |
| 6 | Not shown | — |
| 7 | KEY | Connector note |
| 8 | TO LEFT FLIPPER COIL | K1 switched contact; not a Q output |
| 9 | TO RIGHT FLIPPER COIL | K1 switched contact; not a Q output |

### J2 — cabinet connector and momentary output branches

| Pin | Page 06 function or status | Traced driver / note |
| ---: | --- | --- |
| 1 | TO RIGHT FLIPPER BUTTON | K1 contact |
| 2 | TO LEFT FLIPPER BUTTON | K1 contact |
| 3 | KEY | Connector note |
| 4 | N/U | Q2; also J1-3 |
| 5 | #6 TOP DROP TARGET OR #7 (RIGHT END) | Q3; public 6 / printed tests 6 or 21; also J3-4 |
| 6 | N/U | Q16; also J3-7 and J5-8 |
| 7 | SELF TEST GRD. RETURN | Regulator return |
| 8 | COIN LOCKOUT | Q19 |
| 9 | N/U | Q1; also J1-2 |
| 10 | 7 DROP TARGET RESET OR #1 TOP DROP TARGET (LEFT END) | Q5; public 3 / printed tests 3 or 18 |
| 11 | #2 TOP DROP TARGET OR #3 | Q6; public 4 / printed tests 4 or 19 |
| 12 | #4 TOP DROP TARGET OR #5 | Q7; public 5 / printed tests 5 or 20 |
| 13 | Not shown | — |
| 14 | Not shown | — |
| 15 | N/U | Q18; also J5-3 and J3-9 |

### J3 — backbox, power and output branches

| Pin | Page 06 function or status | Traced driver / note |
| ---: | --- | --- |
| 1 | Not shown | — |
| 2 | KEY | Connector note |
| 3 | FROM A2J3-7 XFMR BRIDGE GROUND | +190 V regulator return |
| 4 | No function label printed | Q3 branch, also J2-5 |
| 5 | TO A2J3-8, A8J1-9 | K1 flipper-enable relay supply |
| 6 | FROM A2J4-6 BRIDGE RECTIFIER | Printed +230 V regulator input |
| 7 | No function label printed | Q16 branch, also J2-6 and J5-8 |
| 8 | +190 VDC TO DISPLAYS | Regulated output |
| 9 | N/U | Q18 branch, also J2-15 and J5-3 |
| 10 | TO TRANSFORMER (BRIDGE AND GND) A2J3-5 | Regulator return |
| 11 | TO MPU | Connected to the unregulated input node |
| 12 | 11.9 VDC UNREGULATED FROM A2J3-10 | Regulator input |
| 13 | A3J3-25 | Dashed jumper shown to J3-25; +5 V node |
| 14 | 2X #22 AWG. TO MPU | +5 V node; printed bracket includes pins 14–15 |
| 15 | 2X #22 AWG. TO MPU | +5 V node; printed bracket includes pins 14–15 |
| 16 | A5J4-3 LAMP DRIVER | +5 V node |
| 17 | DISPLAYS A1J1-20 | +5 V node |
| 18 | 2X #22 AWG. TO MPU | Return node; printed bracket includes pins 18–19 |
| 19 | 2X #22 AWG. TO MPU | Return node; printed bracket includes pins 18–19 |
| 20 | DISPLAYS A1J1-11 | Return node |
| 21 | TRANSFORMER A2J3-5, 6 | Return node; printed bracket includes pins 21–22 |
| 22 | TRANSFORMER A2J3-5, 6 | Return node; printed bracket includes pins 21–22 |
| 23 | GRD. | +43 V SOLENOID GRD. node |
| 24 | GRD. | +43 V SOLENOID GRD. node |
| 25 | A3J3-13 | +5V BUS LINE; dashed jumper to J3-13 |

### J4 — backbox control connector

| Pin | Page 06 function or status | Driver / note |
| ---: | --- | --- |
| 1 | N/U | — |
| 2 | KEY | — |
| 3 | PB3 | Momentary solenoid decoder D |
| 4 | PB2 | Momentary solenoid decoder C |
| 5 | PB1 | Momentary solenoid decoder B |
| 6 | PB0 | Momentary solenoid decoder A |
| 7 | CB2 — LOW WHEN SELECTED | Solenoid bank select |
| 8 | PB6, CONT. 1 — FLIPPER DISABLE | Q15 / K1 flipper-enable relay |
| 9 | PB5, CONT. 4 — COIN LOCK OUT | Q19 |
| 10 | PB7, CONT. 3 | Q18 |
| 11 | PB4, CONT. 2 | Q17 |
| 12 | N/U | — |

### J5 — playfield connector

| Pin | Page 06 function or status | Traced driver / note |
| ---: | --- | --- |
| 1 | Not shown | — |
| 2 | Not shown | — |
| 3 | N/U | Q18; also J2-15 and J3-9 |
| 4 | Not shown | — |
| 5 | Not shown | — |
| 6 | KEY | Connector note |
| 7 | N/U | Q17 |
| 8 | TOP RIGHT SLINGSHOT | Q16; public 15 / printed test 15; also J2-6 and J3-7 |
| 9 | TOP LEFT THUMPER BUMPER | Q9; public 11 / printed test 11 |
| 10 | OUTHOLE OR SAUCER | Q8; public 8 / printed tests 8 or 22 |
| 11 | BOTTOM RIGHT THUMPER BUMPER | Q14; public 10 / printed test 10 |
| 12 | BOTTOM LEFT THUMPER BUMPER | Q13; public 9 / printed test 9 |
| 13 | LEFT SLINGSHOT | Q12; public 13 / printed test 13 |
| 14 | BOTTOM RIGHT SLINGSHOT | Q11; public 14 / printed test 14 |
| 15 | TOP RIGHT THUMPER BUMPER | Q10; public 12 / printed test 12 |

Page 06 supplies connector functions and driver designators, but does **not** print a complete wire-color table beside these A3 entries. No wire colors have been inferred. The unlabeled J3-4 and J3-7 functions are established here only by their drawn shared electrical paths; the sheet prints no separate function text at those two pins.
