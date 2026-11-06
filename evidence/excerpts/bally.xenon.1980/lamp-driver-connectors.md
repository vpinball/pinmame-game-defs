# Xenon A5 lamp driver: complete connectors and decoder trace

PDF page47 W-1182-27 and PDF54 W-1187-24c. These are different regions of one factory schematic set, not independent corroboration. J1/J3 go TO PLAYFIELD; J2 goes TO BACK BOX but its populated Table B branches also feed the playfield. The wire code is literal two-digit Bally code; [blank] means no wire code printed. Abbreviations vary between the two sheets; below preserves the connector list lettering from W-1187-24c and * markers as printed, with * on tube labels meaning the numbered group, not an extra circuit. Source spelling SAUCER/S.A. retained.

## A5J1

| Pin | Wire | Function |
| --- | --- | --- |
| 1 | 41 | DROP TARGET SPECIAL |
| 2 | 52 | DROP TAR. 3 & TOP 3 |
| 3 | 45 | 2nd AMBER "N" |
| 4 | 35 | N/U |
| 5 | 48 | UPPER SIDE TARGET ARROW |
| 6 | 25 | 30K SIDE SAUCER |
| 7 | 34 | 10K SIDE SAUCER |
| 8 | 51 | AMBER "X" |
| 9 | 43 | BLUE "E" |
| 10 | 23 | LEFT FLIPPER FEED ARROW |
| 11 | 65 | TUBE ENTRANCE & END OF TUBE |
| 12 | 61 | 2nd TOP SAUCER "X" |
| 13 | 96 | 35K SIDE SAUCER |
| 14 | 67 | DROP TAR. 4 & TOP 4 |
| 15 | 13 | LT. OUTLANE ARROW |
| 16 | 90 | 5K SIDE SAUCER |
| 17 | 57 | 2nd BLUE "N" |
| 18 | 58 | N/U |
| 19 | 60 | BLUE "X" |
| 20 | [blank] | KEY |
| 21 | [blank] | N/U |
| 22 | [blank] | N/U |
| 23 | 12 | AMBER "O" |
| 24 | 50 | 50K SIDE SAUCER |
| 25 | 75 | *5 TUBE LITES |
| 26 | 91 | N/U |
| 27 | 53 | 1st TOP SAUCER "X" |
| 28 | 78 | 25K SIDE SAUCER |

## A5J2

| Pin | Wire | Function |
| --- | --- | --- |
| 1 | 60 | X-BALL DROP TAR. |
| 2 | 20 | 25K DROP TARGET |
| 3 | [blank] | N/U |
| 4 | [blank] | N/U |
| 5 | [blank] | N/U |
| 6 | 85 | *3 TUBE LITES |
| 7 | 91 | *4 TUBE LITES |
| 8 | 70 | MATCH |
| 9 | [blank] | N/U |
| 10 | 34 | TILT |
| 11 | 95 | GAME OVER |
| 12 | [blank] | N/U |
| 13 | [blank] | N/U |
| 14 | 12 | 2X DROP TARGET |
| 15 | 23 | 4X DROP TARGET |
| 16 | 34 | *1 TUBE LITES |
| 17 | [blank] | N/U |
| 18 | [blank] | KEY |
| 19 | [blank] | N/U |
| 20 | 98 | *2 TUBE LITES |
| 21 | 47 | SHOOT AGAIN |
| 22 | 62 | BALL IN PLAY |
| 23 | 97 | HIGH SCORE TO DATE |

## A5J3

| Pin | Wire | Function |
| --- | --- | --- |
| 1 | 10 | 4X BONUS |
| 2 | 95 | 40K SIDE SAUCER |
| 3 | 81 | RT. OUTLANE ARROW |
| 4 | 14 | 20K SIDE SAUCER |
| 5 | [blank] | N/U |
| 6 | [blank] | N/U |
| 7 | [blank] | N/U |
| 8 | [blank] | KEY |
| 9 | 15 | DROP TAR. 1 & TOP 1 |
| 10 | 91 | LOWER SIDE TARGET ARROW |
| 11 | 20 | 40K & SPECIAL XENON |
| 12 | 21 | BLUE "O" |
| 13 | 35 | CREDIT INDICATOR |
| 14 | 84 | TOP SAUCER CAPTIVE BALL |
| 15 | 53 | 1st AMBER "N" |
| 16 | 25 | DROP TAR. 2 & TOP 2 |
| 17 | 13 | 20K XENON |
| 18 | 56 | SPINNER |
| 19 | 67 | AMBER "E" |
| 20 | 64 | SPECIAL SIDE SAUCER |
| 21 | 30 | DROP TARGET ARROW |
| 22 | 23 | SAME PLAYER S.A. |
| 23 | 98 | RIGHT FLIPPER FEED ARROW |
| 24 | 72 | 3rd TOP SAUCER "X" |
| 25 | 36 | 1st BLUE "N" |
| 26 | 43 | 2X BONUS |
| 27 | 40 | 15K SIDE SAUCER |
| 28 | [blank] | N/U |

## Derived public mapping, every MC14514 output

The public column is derived, not printed: 16*d+a+1, decoder U(d+1) output a=0..14. Output15 is the idle selector and has no public address.

| Public | Decoder/output | SCR | Fitted endpoint (or printed N/U) |
| --- | --- | --- | --- |
| 1 | U1/0 | Q14 | A5J1-18: N/U |
| 2 | U1/1 | Q12 | A5J1-19: BLUE "X" |
| 3 | U1/2 | Q13 | A5J1-17: 2nd BLUE "N" |
| 4 | U1/3 | Q8 | A5J1-23: AMBER "O" |
| 5 | U1/4 | Q9 | A5J1-14: DROP TAR. 4 & TOP 4 |
| 6 | U1/5 | Q10 | A5J1-15: LT. OUTLANE ARROW |
| 7 | U1/6 | Q11 | A5J1-16: 5K SIDE SAUCER |
| 8 | U1/7 | Q4 | A5J1-28: 25K SIDE SAUCER |
| 9 | U1/8 | Q1 | A5J1-24: 50K SIDE SAUCER |
| 10 | U1/9 | Q2 | A5J1-25: *5 TUBE LITES |
| 11 | U1/10 | Q3 | A5J3-22: SAME PLAYER S.A. |
| 12 | U1/11 | Q7 | A5J1-27: 1st TOP SAUCER "X" |
| 13 | U1/12 | Q16 | A5J2-22: BALL IN PLAY |
| 14 | U1/13 | Q5 | A5J2-16: *1 TUBE LITES |
| 15 | U1/14 | Q6 | A5J2-14: 2X DROP TARGET |
| 17 | U2/0 | Q29 | A5J1-1: DROP TARGET SPECIAL |
| 18 | U2/1 | Q27 | A5J1-9: BLUE "E" |
| 19 | U2/2 | Q28 | A5J1-8: AMBER "X" |
| 20 | U2/3 | Q35 | A5J1-3: 2nd AMBER "N" |
| 21 | U2/4 | Q34 | A5J1-2: DROP TAR. 3 & TOP 3 |
| 22 | U2/5 | Q22 | A5J1-10: LEFT FLIPPER FEED ARROW |
| 23 | U2/6 | Q26 | A5J1-7: 10K SIDE SAUCER |
| 24 | U2/7 | Q25 | A5J1-6: 30K SIDE SAUCER |
| 25 | U2/8 | Q24 | A5J1-5: UPPER SIDE TARGET ARROW |
| 26 | U2/9 | Q17 | A5J1-11: TUBE ENTRANCE & END OF TUBE |
| 27 | U2/10 | Q23 | A5J2-8: MATCH |
| 28 | U2/11 | Q21 | A5J1-12: 2nd TOP SAUCER "X" |
| 29 | U2/12 | Q15 | A5J2-23: HIGH SCORE TO DATE |
| 30 | U2/13 | Q18 | A5J2-20: *2 TUBE LITES |
| 31 | U2/14 | Q19 | A5J2-15: 4X DROP TARGET |
| 33 | U3/0 | Q36 | A5J3-26: 2X BONUS |
| 34 | U3/1 | Q38 | A5J3-25: 1st BLUE "N" |
| 35 | U3/2 | Q44 | A5J3-19: AMBER "E" |
| 36 | U3/3 | Q49 | A5J3-17: 20K XENON |
| 37 | U3/4 | Q48 | A5J3-16: DROP TAR. 2 & TOP 2 |
| 38 | U3/5 | Q37 | A5J3-23: RIGHT FLIPPER FEED ARROW |
| 39 | U3/6 | Q32 | A5J3-27: 15K SIDE SAUCER |
| 40 | U3/7 | Q20 | A5J1-13: 35K SIDE SAUCER |
| 41 | U3/8 | Q42 | A5J3-21: DROP TARGET ARROW |
| 42 | U3/9 | Q41 | A5J3-20: SPECIAL SIDE SAUCER |
| 43 | U3/10 | Q40 | A5J2-21: SHOOT AGAIN |
| 44 | U3/11 | Q39 | A5J3-24: 3rd TOP SAUCER "X" |
| 45 | U3/12 | Q33 | A5J2-11: GAME OVER |
| 46 | U3/13 | Q30 | A5J2-7: *4 TUBE LITES |
| 47 | U3/14 | Q31 | A5J2-1: X-BALL DROP TAR. |
| 49 | U4/0 | Q57 | A5J3-1: 4X BONUS |
| 50 | U4/1 | Q50 | A5J3-12: BLUE "O" |
| 51 | U4/2 | Q51 | A5J3-15: 1st AMBER "N" |
| 52 | U4/3 | Q54 | A5J3-11: 40K & SPECIAL XENON |
| 53 | U4/4 | Q55 | A5J3-9: DROP TAR. 1 & TOP 1 |
| 54 | U4/5 | Q60 | A5J3-3: RT. OUTLANE ARROW |
| 55 | U4/6 | Q59 | A5J3-4: 20K SIDE SAUCER |
| 56 | U4/7 | Q58 | A5J3-2: 40K SIDE SAUCER |
| 57 | U4/8 | Q56 | A5J3-10: LOWER SIDE TARGET ARROW |
| 58 | U4/9 | Q46 | A5J3-18: SPINNER |
| 59 | U4/10 | Q52 | A5J3-13: CREDIT INDICATOR |
| 60 | U4/11 | Q53 | A5J3-14: TOP SAUCER CAPTIVE BALL |
| 61 | U4/12 | Q47 | A5J2-10: TILT |
| 62 | U4/13 | Q43 | A5J2-6: *3 TUBE LITES |
| 63 | U4/14 | Q45 | A5J2-2: 25K DROP TARGET |

Do not discard branches: public11 also reaches A5J1-26 N/U, but fits the playfield SAME PLAYER S.A. socket through A5J3-22. Public27 also reaches A5J1-4 N/U, but fits MATCH through A5J2-8. Public1 has no fitted endpoint (A5J1-18 and A5J2-13 N/U). The spare J2 entries are not additional lamps.

## Complete Table B: PANEL TO BACK CAB. PLUG

| FROM | TO | WIRE |
| --- | --- | --- |
| A5J2-14 | 1 | 12 |
| A5J2-2 | 2 | 20 |
| A5J2-15 | 3 | 23 |
| A9J2-25 | 4 | 25 |
| A5J2-16 | 5 | 34 |
| A9J2-17 | 6 | 43 |
| A9J2-9 | 7 | 54 |
| A5J2-1 | 8 | 60 |
| A5J2-6 | 9 | 85 |
| A5J2-7 | 10 | 91 |
| A5J2-20 | 11 | 98 |

Literal A9J2-25 is impossible on A9J2 (18 pins); W-1192-24c explicitly takes the BALL SHOOTER branch from A9J3-10 (wire25), agreeing with W-1207-3. Retain the Table B misprint; structured data follows those agreeing wiring sheets.
