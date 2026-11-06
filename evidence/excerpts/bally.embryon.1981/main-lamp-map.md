# Embryon A5 lamp decoding and loads

The primary visually traced the native `lamp.tif` decoder, SCRs and connector branches
and crosschecked the corrected load names against the retained v2.0.2 script and playfield.
The public-to-load table below is normalized; source-literal connector rows remain in the
separate connector transcript. A board connector N/U marks that branch, not necessarily
the SCR's other branch. In particular public 11 and 27 feed backbox loads.

| Public | SCR | Physical load |
|---:|---|---|
| 1 | Q14 | 1K BONUS |
| 2 | Q12 | 5K BONUS |
| 3 | Q13 | 9K BONUS |
| 4 | Q8 | 20K BONUS |
| 5 | Q9 | 2X BONUS |
| 6 | Q10 | BOTTOM ROLLOVER BUTTON |
| 7 | Q11 | E |
| 8 | Q4 | Y |
| 9 | Q1 | A LANE |
| 10 | Q2 | 25K ARROW (TOP LANES) |
| 11 | Q3 | SHOOT AGAIN (BACKBOX) |
| 12 | Q7 | RIGHT BOTTOM THUMPER BUMPER |
| 13 | Q16 | BALL IN PLAY |
| 14 | Q5 | E BACKGLASS |
| 15 | Q6 | Y BACKGLASS |
| 17 | Q29 | 2K BONUS |
| 18 | Q27 | 6K BONUS |
| 19 | Q28 | 10K BONUS |
| 20 | Q35 | 40K BONUS |
| 21 | Q34 | 3X BONUS |
| 22 | Q22 | MIDDLE ROLLOVER BUTTON |
| 23 | Q26 | M |
| 24 | Q25 | O |
| 25 | Q24 | B LANE |
| 26 | Q17 | 50K ARROW (TOP LANES) |
| 27 | Q23 | MATCH |
| 28 | Q21 | RIGHT TOP THUMPER BUMPER |
| 29 | Q15 | HIGH SCORE TO DATE |
| 30 | Q18 | M BACKGLASS |
| 31 | Q19 | O BACKGLASS |
| 33 | Q36 | 3K BONUS |
| 34 | Q38 | 7K BONUS |
| 35 | Q44 | RIGHT OUTLANE SPECIAL |
| 36 | Q49 | BONUS SPECIAL |
| 37 | Q48 | 4X BONUS |
| 38 | Q37 | TOP ROLLOVER BUTTON |
| 39 | Q32 | B |
| 40 | Q20 | N |
| 41 | Q42 | 1 LANE |
| 42 | Q41 | EXTRA BALL ARROW (TOP LANES) |
| 43 | Q40 | SAME PLAYER SHOOT AGAIN |
| 44 | Q39 | LEFT BOTTOM THUMPER BUMPER |
| 45 | Q33 | GAME OVER |
| 46 | Q30 | B BACKGLASS |
| 47 | Q31 | N BACKGLASS |
| 49 | Q57 | 4K BONUS |
| 50 | Q50 | 8K BONUS |
| 51 | Q51 | LEFT OUTLANE SPECIAL |
| 52 | Q54 | N/U |
| 53 | Q55 | 5X ARROW |
| 54 | Q60 | SAUCER ARROW |
| 55 | Q59 | R |
| 56 | Q58 | A10 LAMP FLASH DRIVER AND #44 LAMP |
| 57 | Q56 | 2 LANE |
| 58 | Q46 | SPECIAL ARROW (TOP LANES) |
| 59 | Q52 | CREDIT INDICATOR |
| 60 | Q53 | LEFT TOP THUMPER BUMPER |
| 61 | Q47 | TILT |
| 62 | Q43 | R BACKGLASS |
| 63 | Q45 | N/U |

A5J4 source labels: 14 AD0, 15 AD1, 16 AD2, 17 AD3; 7 PD0, 6 PD1, 5 PD2,
4 PD3; 13 STROBE1; 3 +5V; 12, 11, 2 and 1 GND; 8 KEY; 9 and 10 SPARE.
A5J3-2 is printed N/U on the board sheet, but the game's W-1192-29c harness routes it
to A10J1-3. A10 W-1252b has four #921 flasher lamps and one #44 lamp in the A10
control circuit. The #44 lamp's physical purpose, visibility and socket location are unknown.
Public 59 is the apron credit indicator. Playfield and backbox letter bits are separate.
