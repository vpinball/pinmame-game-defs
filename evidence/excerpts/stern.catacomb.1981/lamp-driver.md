# Catacomb lamp-driver sheet

Source: Stern Electronics, Catacomb schematics PDF page 6, Lamp Driver LDA-100 drawing 340-431-S rev D. Original SHA-256 `45fd3691ca719eab243553b98967aef4fb7cbe6c1ce7340e3342ecf0a1d24294`.

Method: candidate transcription, checked and corrected by the curator against the entire printed load table and connector blocks in the retained native render. `[blank]` marks a printed blank; an omitted row is stated separately. Wire spelling/case and source column order are preserved. The shoot-again continuation prints only J2 and 21; other fields are genuinely blank on that line.

## Entire printed load table

| description | wire_color | jack_lda | jack_pin_no | transistor | ic | ic_pin_no | code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DROP TARGET BANK "A" LAMP | O-R | J1 | 18 | Q14 | U1 | 11 | 0000 |
| DROP TARGET BANK "B" LAMP | R-Y | J1 | 1 | Q29 | U2 | 11 | 0000 |
| DROP TARGET BANK "C" LAMP | GREY | J3 | 26 | Q36 | U3 | 11 | 0000 |
| DROP TARGET BANK "D" LAMP | GREY-Y | J3 | 1 | Q57 | U4 | 11 | 0000 |
| SPOT 1 LAMP | BLU-Y | J1 | 9 | Q27 | U2 | 9 | 0001 |
| SPOT 2 LAMP | BLU-R | J3 | 25 | Q38 | U3 | 9 | 0001 |
| SPOT 6 LAMP | BLU-W | J3 | 12 | Q50 | U4 | 9 | 0001 |
| BONUS GREEN 14 | B-G | J1 | 17 | Q13 | U1 | 10 | 0010 |
| BONUS BLUE 9 | G-W | J1 | 8 | Q28 | U2 | 10 | 0010 |
| BONUS AMBER 1 | BRN-BLU | J3 | 19 | Q44 | U3 | 10 | 0010 |
| BONUS RED 6 | W-B | J3 | 15 | Q51 | U4 | 10 | 0010 |
| DROP TARGET BANK "A" GREEN 14 | BLU-W | J1 | 23 | Q8 | U1 | 8 | 0011 |
| DROP TARGET BANK "A" BLUE 9 | R-G | J1 | 3 | Q35 | U2 | 8 | 0011 |
| DROP TARGET BANK "A" AMBER 1 | Y-BLU | J3 | 17 | Q49 | U3 | 8 | 0011 |
| DROP TARGET BANK "A" RED 6 | -W- | J3 | 11 | Q54 | U4 | 8 | 0011 |
| BONUS GREEN 3 | GREY-O | J1 | 14 | Q9 | U1 | 7 | 0100 |
| BONUS BLUE 8 | GREY | J1 | 2 | Q34 | U2 | 7 | 0100 |
| BONUS AMBER 16 | O-BLU | J3 | 16 | Q48 | U3 | 7 | 0100 |
| BONUS RED 11 | O-B | J3 | 9 | Q55 | U4 | 7 | 0100 |
| DROP TARGET BANK "B" GREEN 3 | GREY-Y | J1 | 15 | Q10 | U1 | 6 | 0101 |
| DROP TARGET BANK "B" BLUE 8 | GREY-BLU | J1 | 10 | Q22 | U2 | 6 | 0101 |
| DROP TARGET BANK "B" AMBER 16 | GREY-W | J3 | 23 | Q37 | U3 | 6 | 0101 |
| DROP TARGET BANK "B" RED 11 | W-BLU | J3 | 3 | Q60 | U4 | 6 | 0101 |
| BONUS GREEN 15 | -B- | J1 | 16 | Q11 | U1 | 5 | 0110 |
| BONUS BLUE 12 | Y-G | J1 | 7 | Q26 | U2 | 5 | 0110 |
| BONUS AMBER 4 | O-W | J3 | 27 | Q32 | U3 | 5 | 0110 |
| BONUS RED 7 | R-W | J3 | 4 | Q59 | U4 | 5 | 0110 |
| DROP TARGET BANK "C" GREEN 15 | B-W | J1 | 28 | Q4 | U1 | 4 | 0111 |
| DROP TARGET BANK "C" BLUE 12 | BRN-R | J1 | 6 | Q25 | U2 | 4 | 0111 |
| DROP TARGET BANK "C" AMBER 4 | W-BLU | J1 | 13 | Q20 | U3 | 4 | 0111 |
| DROP TARGET BANK "C" RED 7 | BLU-O | J3 | 2 | Q58 | U4 | 4 | 0111 |
| BONUS GREEN 2 | BRN-BLU | J1 | 24 | Q1 | U1 | 18 | 1000 |
| BONUS BLUE 5 | PUR-W | J1 | 5 | Q24 | U2 | 18 | 1000 |
| BONUS AMBER 13 | G-B | J3 | 21 | Q42 | U3 | 18 | 1000 |
| BONUS RED 10 | GREY-B | J3 | 10 | Q56 | U4 | 18 | 1000 |
| DROP TARGET BANK "D" GREEN 2 | B-BLU | J1 | 25 | Q2 | U1 | 17 | 1001 |
| DROP TARGET BANK "D" BLUE 5 | B-O | J1 | 11 | Q17 | U2 | 17 | 1001 |
| DROP TARGET BANK "D" AMBER 13 | W-O | J3 | 20 | Q41 | U3 | 17 | 1001 |
| DROP TARGET BANK "D" RED 10 | R-BLU | J3 | 18 | Q46 | U4 | 17 | 1001 |
| SHOOT AGAIN | GREY-R | J1 | 26 | Q3 | U1 | 20 | 1010 |
| [blank] | [blank] | J2 | 21 | [blank] | [blank] | [blank] | [blank] |
| MULTIPLIER 2X | B-R | J2 | 8 | Q23 | U2 | 20 | 1010 |
| MULTIPLIER 3X | W-R | J2 | 9 | Q40 | U3 | 20 | 1010 |
| MULTIPLIER 4X | B-Y | J2 | 5 | Q52 | U4 | 20 | 1010 |
| MULTIPLIER 5X | GREY-G | J2 | 13 | Q7 | U1 | 19 | 1011 |
| SPINNER LANE EXTRA BALL LAMP | R-W | J2 | 12 | Q21 | U2 | 19 | 1011 |
| SPINNER LANE SPECIAL LAMP | PUR-B | J2 | 4 | Q39 | U3 | 19 | 1011 |
| SUPER BONUS | B-W | J2 | 3 | Q53 | U4 | 19 | 1011 |
| HIGH SCORE TO DATE | GREY-O | J2 | 22 | Q16 | U1 | 14 | 1100 |
| GAME OVER | GREY-W | J2 | 11 | Q33 | U3 | 14 | 1100 |
| TILT | GREY-BLU | J2 | 10 | Q47 | U4 | 14 | 1100 |
| LEFT RETURN LANE | -B- | J2 | 16 | Q5 | U1 | 13 | 1101 |
| RIGHT RETURN LANE | -O- | J2 | 20 | Q18 | U2 | 13 | 1101 |
| LEFT OUT LANE | -Y- | J2 | 6 | Q30 | U3 | 13 | 1101 |
| RIGHT OUT LANE | BLU-W | J2 | 7 | Q43 | U4 | 13 | 1101 |
| SPINNER 1000 POINT LAMP TOP | BRN-R | J2 | 14 | Q6 | U1 | 16 | 1110 |
| SPINNER 1000 POINT LAMP MIDDLE | O-BLU | J2 | 15 | Q19 | U2 | 16 | 1110 |
| SPINNER 1000 POINT LAMP BOTTOM | G-O | J2 | 2 | Q31 | U3 | 16 | 1110 |
| MATCH | GREY-W | J2 | 1 | Q45 | U4 | 16 | 1110 |

## Decoder output lines (drawing)

Public address = `16 * (IC number - 1) + S output + 1`, derived from pinned by35_lampStrobe and sequential core conversion. The resistor number at each SCR gives its Q number. These are the game sheet's own lines, including crossed U2 S7/S8 and U3/U4 S9 pairings.

| IC | S output | IC pin | Resistor | SCR | Public |
| --- | --- | --- | --- | --- | --- |
| U1 | S0 | 11 | R14 | Q14 | 1 |
| U1 | S1 | 9 | R12 | Q12 | 2 |
| U1 | S2 | 10 | R13 | Q13 | 3 |
| U1 | S3 | 8 | R8 | Q8 | 4 |
| U1 | S4 | 7 | R9 | Q9 | 5 |
| U1 | S5 | 6 | R10 | Q10 | 6 |
| U1 | S6 | 5 | R11 | Q11 | 7 |
| U1 | S7 | 4 | R4 | Q4 | 8 |
| U1 | S8 | 18 | R1 | Q1 | 9 |
| U1 | S9 | 17 | R2 | Q2 | 10 |
| U1 | S10 | 20 | R3 | Q3 | 11 |
| U1 | S11 | 19 | R7 | Q7 | 12 |
| U1 | S12 | 14 | R16 | Q16 | 13 |
| U1 | S13 | 13 | R5 | Q5 | 14 |
| U1 | S14 | 16 | R6 | Q6 | 15 |
| U2 | S0 | 11 | R29 | Q29 | 17 |
| U2 | S1 | 9 | R27 | Q27 | 18 |
| U2 | S2 | 10 | R28 | Q28 | 19 |
| U2 | S3 | 8 | R35 | Q35 | 20 |
| U2 | S4 | 7 | R34 | Q34 | 21 |
| U2 | S5 | 6 | R22 | Q22 | 22 |
| U2 | S6 | 5 | R26 | Q26 | 23 |
| U2 | S7 | 4 | R25 | Q25 | 24 |
| U2 | S8 | 18 | R24 | Q24 | 25 |
| U2 | S9 | 17 | R17 | Q17 | 26 |
| U2 | S10 | 20 | R23 | Q23 | 27 |
| U2 | S11 | 19 | R21 | Q21 | 28 |
| U2 | S12 | 14 | R15 | Q15 | 29 |
| U2 | S13 | 13 | R18 | Q18 | 30 |
| U2 | S14 | 16 | R19 | Q19 | 31 |
| U3 | S0 | 11 | R36 | Q36 | 33 |
| U3 | S1 | 9 | R38 | Q38 | 34 |
| U3 | S2 | 10 | R44 | Q44 | 35 |
| U3 | S3 | 8 | R49 | Q49 | 36 |
| U3 | S4 | 7 | R48 | Q48 | 37 |
| U3 | S5 | 6 | R37 | Q37 | 38 |
| U3 | S6 | 5 | R32 | Q32 | 39 |
| U3 | S7 | 4 | R20 | Q20 | 40 |
| U3 | S8 | 18 | R42 | Q42 | 41 |
| U3 | S9 | 17 | R41 | Q41 | 42 |
| U3 | S10 | 20 | R40 | Q40 | 43 |
| U3 | S11 | 19 | R39 | Q39 | 44 |
| U3 | S12 | 14 | R33 | Q33 | 45 |
| U3 | S13 | 13 | R30 | Q30 | 46 |
| U3 | S14 | 16 | R31 | Q31 | 47 |
| U4 | S0 | 11 | R57 | Q57 | 49 |
| U4 | S1 | 9 | R50 | Q50 | 50 |
| U4 | S2 | 10 | R51 | Q51 | 51 |
| U4 | S3 | 8 | R54 | Q54 | 52 |
| U4 | S4 | 7 | R55 | Q55 | 53 |
| U4 | S5 | 6 | R60 | Q60 | 54 |
| U4 | S6 | 5 | R59 | Q59 | 55 |
| U4 | S7 | 4 | R58 | Q58 | 56 |
| U4 | S8 | 18 | R56 | Q56 | 57 |
| U4 | S9 | 17 | R46 | Q46 | 58 |
| U4 | S10 | 20 | R52 | Q52 | 59 |
| U4 | S11 | 19 | R53 | Q53 | 60 |
| U4 | S12 | 14 | R47 | Q47 | 61 |
| U4 | S13 | 13 | R43 | Q43 | 62 |
| U4 | S14 | 16 | R45 | Q45 | 63 |

## Connector endpoints omitted from the load table

| Public | IC/output | SCR | Drawn endpoint | Drawn region | Named load/wire in table |
| --- | --- | --- | --- | --- | --- |
| 2 | U1/S1 | Q12 | J1-19 | TO PLAYFIELD | [row omitted] |
| 29 | U2/S12 | Q15 | J2-23 | TO BACK BOX | [row omitted] |

The primary curator traced these against the full-resolution connector block. Earlier scratch candidate notes incorrectly said J2-18/J2-19; those readings are rejected. The exact endpoints above agree with the visible J1 group (18 Q14, 19 Q12, 17 Q13) and J2 group (12 Q21, 23 Q15, 20 Q18). The insert harness table on PDF p1 includes A5J2-23 at insert A1J2-5; it does not name the load. Neither a connector endpoint nor an omitted name establishes fitted/unfitted status. Public 2 has script render proxies but no proven socket; public 29 has no retained script light binding. Both remain unknown.

J1/J3 are labelled TO PLAYFIELD and J2 TO BACK BOX, but wiring routes do not override physically observed load locations. The named spinner and lane inserts are on the playfield in both the retained table and physical photos. Shoot Again has two connector endpoints J1-26 and J2-21; its playfield insert and backbox legend are one controlled circuit with two physical emitters. No S15 output is drawn; PinMAME explicitly suppresses decoder code 15, so public 16,32,48,64 are not usable lamp addresses.
