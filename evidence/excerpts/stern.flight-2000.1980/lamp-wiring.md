# Flight 2000 feature lamp wiring

Stern Electronics instruction manual, PDF page 42, drawing 12B-431S-128 (right side of the LDA chart). PDF page 38 repeats the list. Text and pin spellings are as printed, including abbreviated colors and leading zeroes. The table below does not correct discordant entries on the driver schematic.

| Description | Wire color | LDA jack | Pin |
| --- | --- | --- | --- |
| B ROLL-OVER BOTTOM LEFT | W-BLU | J3 | 3 |
| L ROLL-OVER TOP | W-GREY | J3 | 23 |
| A ROLL-OVER TOP | GREY-BLU | J1 | 10 |
| S ROLL-OVER TOP | GREY-Y | J1 | 15 |
| T ROLL-OVER TOP | R-W | J3 | 4 |
| O ROLL-OVER TOP | R-B | J3 | 16 |
| F ROLL-OVER BOTTOM LEFT | GREY-O | J1 | 14 |
| F ROLL-OVER BOTTOM RIGHT | PUR-W | J1 | 2 |
| BONUS 1,000 | BRN-B | J1 | 18 |
| BONUS 2,000 | BLU-R | J1 | 1 |
| BONUS 3,000 | BRN | J3 | 26 |
| BONUS 4,000 | G-R | J3 | 1 |
| BONUS 5,000 | GREY-G | J1 | 19 |
| BONUS 6,000 | GREY | J1 | 9 |
| BONUS 7,000 | R-Y | J3 | 25 |
| BONUS 8,000 | O-G | J3 | 12 |
| BONUS 9,000 | PUR | J1 | 17 |
| BONUS 10,000 | G-B | J1 | 8 |
| BONUS MULTIPLIER 1X | W-B | J3 | 15 |
| BONUS MULTIPLIER 2X | BLU-W | J1 | 23 |
| BONUS MULTIPLIER 3X | R-G | J1 | 3 |
| BONUS MULTIPLIER 4X | Y-BLU | J3 | 17 |
| BONUS MULTIPLIER 5X | W | J3 | 11 |
| FIRST STAGE GO LEFT | Y-BLU | J2 | 7 |
| FIRST STAGE GO TOP | Y-BLU | J2 | 7 |
| GAME OVER | GREY-W | J2 | 11 |
| HIGH SCORE TO DATE | GREY-O | J2 | 22 |
| LEFT HAND CORNER B | Y-G | J3 | 02 |
| LEFT HAND CORNER L | W-BLU | J1 | 13 |
| LEFT HAND CORNER A | BRN-R | J1 | 6 |
| LEFT HAND CORNER S | B-W | J1 | 28 |
| LEFT HAND CORNER T | R-W | J3 | 4 |
| LEFT HAND CORNER O | O-W | J3 | 27 |
| LEFT HAND CORNER F | Y-G | J1 | 7 |
| LEFT HAND CORNER F | B | J1 | 16 |
| MATCH | GREY-Y | J2 | 1 |
| RELEASE NEXT ROCKET | B-R | J3 | 19 |
| RIGHT BANK | BRN-BLU | J1 | 24 |
| RIGHT SPINNER -500 | PUR-B | J1 | 4 |
| RIGHT SPINNER -1,000 | R | J3 | 22 |
| RIGHT SPINNER -1,500 | B | J3 | 13 |
| RIGHT SPINNER -2,000 | W-BRN | J1 | 27 |
| SECOND STAGE GO LEFT | W-BLU | J2 | 5 |
| SECOND STAGE GO TOP | W-BLU | J2 | 5 |
| SHOOT AGAIN (BACKBOX) | GREY-R | J2 | 21 |
| SHOOT AGAIN (PLAYFIELD) | GREY-R | J1 | 26 |
| SPECIAL LANE | W | J2 | 16 |
| SPECIAL LANE TOP | PUR-W | J2 | 30 |
| SPECIAL OUT LANE LEFT | W-G | J2 | 15 |
| SPECIAL OUT LANE RIGHT | G-W | J2 | 14 |
| SPOT BLAST | G-B | J3 | 21 |
| TILT | GREY-B | J2 | 10 |
| #1 AT 5 BANK | GREY-B | J3 | 10 |
| #2 AT 5 BANK | PUR-B | J1 | 25 |
| #3 AT 5 BANK | B-O | J1 | 11 |
| #4 AT 5 BANK | W-O | J3 | 20 |
| #5 AT 5 BANK | R-BLU | J3 | 18 |
| ALL SYSTEMS GO LEFT | BLU-Y | J2 | 20 |
| ALL SYSTEMS GO TOP | BRN-O | J1 | 12 |
| LEFT SPINNER | BLU-O | J1 | 05 |

The board drawing shows cross-connector ties from Q3 to J1-26 and its J2 branch, Q7 to J1-27 and J2-3, Q40 to J3-22 and J2-9, and Q39 to J3-24 and J2-1. The factory load list identifies Q3's backbox Shoot Again at J2-21, while the drawing appears to print J2-2 for both Q3 and Q31. A board tie alone gives a common driver. A separately named load establishes a second fitted bulb. See the separate decoder transcription for the literal connector reads.
