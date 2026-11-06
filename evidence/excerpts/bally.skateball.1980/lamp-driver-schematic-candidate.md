# Skateball — A5 lamp driver schematic

Bally Game #1210, A5 LAMP DRIVER SCHEMATIC W-1182-28C, PDF page 3 of IPDB schematic set SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`. Transcribed from native-resolution render by a curation worker; **visually reviewed against the retained native-resolution render by the primary curator**. Connector lists are in the order printed, without asserting that a connector's destination label identifies each load's physical location. This sheet labels J1 and J3 TO PLAYFIELD and J2 TO BACK BOX; sheet W-1192-23C separately draws eight J2 loads on playfield A6.

| Connector | Printed pin and label in source order |
|---|---|
| J1 | 22 N/U; 21 N/U; 20 KEY; 18 1K BONUS; 19 5K BONUS; 17 9K BONUS; 23 E DROP TARGET; 14 S DROP TARGET; 15 2X BONUS; 16 20K SAUCER; 28 SAUCER COLLECT BONUS; 24 1-2-3 SPECIAL; 25 TOP RIGHT D.T. ARROW; 26 N/U; 27 RIGHT OUT SPECIAL; 1 2K BONUS; 9 6K BONUS; 8 10K BONUS; 3 T DROP TARGET; 2 B LANE; 10 3X BONUS; 7 30K SAUCER; 6 #3 LANE; 5 RIGHT THUMPER BUMPER; 11 TOP CENTER D.T. ARROW; 13 #2 LANE; 4 N/U; 12 LOWER ROLLOVER BUTTON |
| J2 | 21 SHOOT AGAIN; 13 N/U; 22 BALL IN PLAY; 16 LEFT OUT SPECIAL; 14 BONUS SPECIAL; 8 MATCH; 12 N/U; 23 HIGH SCORE TO DATE; 20 10K CENTER (MIDDLE D.T.); 15 20K RIGHT ARROW (MIDDLE D.T.); 11 GAME OVER; 6 100K (MIDDLE D.T.); 2 10K RIGHT (MIDDLE D.T.); 9 N/U; 4 N/U; 5 N/U; 3 N/U; 10 TILT; 7 10K LEFT (MIDDLE D.T.); 1 20K LEFT ARROW (MIDDLE D.T.); 17 N/U; 18 KEY; 19 N/U |
| J3 | 26 3K BONUS; 25 7K BONUS; 19 20K BONUS; 17 A DROP TARGET; 16 A LANE; 23 4X BONUS; 27 50K SAUCER; 21 BOTTOM THUMPER BUMPER; 20 TOP LEFT D.T. ARROW; 22 SAME PLAYER S.A.; 24 UPPER ROLLOVER BUTTON; 1 4K BONUS; 12 8K BONUS; 15 40K BONUS; 11 K DROP TARGET; 9 60K BONUS; 3 5X BONUS; 4 SAUCER X BALL; 2 #1 LANE; 10 LEFT THUMPER BUMPER; 18 SPOTS X; 13 CREDIT INDICATOR; 14 1K SPINNER; 5 N/U; 6 N/U; 7 N/U; 8 KEY; 28 N/U |

Decoder output-to-SCR labels traced directly from drawing, indexed by the printed decoder output number. Output 15 on each decoder has no SCR branch shown. `**` marks the printed SCR type annotation, retained here rather than inferred from a neighboring circuit.

| Output | U1 SCR | U2 SCR | U3 SCR | U4 SCR |
|---:|---|---|---|---|
| 0 | Q14 | Q29 | Q36 | Q57 |
| 1 | Q12 | Q27 | Q38 | Q50 |
| 2 | Q13 | Q28 | Q44 | Q51 |
| 3 | Q8** | Q35** | Q49** | Q54** |
| 4 | Q9** | Q34** | Q48** | Q55** |
| 5 | Q10** | Q22** | Q37 | Q60 |
| 6 | Q11 | Q26 | Q32 | Q59 |
| 7 | Q4 | Q25 | Q20 | Q58 |
| 8 | Q1** | Q24** | Q42** | Q56** |
| 9 | Q2** | Q17** | Q41** | Q46 |
| 10 | Q3** | Q23** | Q40** | Q52 |
| 11 | Q7 | Q21 | Q39 | Q53 |
| 12 | Q16** | Q15** | Q33** | Q47** |
| 13 | Q5 | Q18 | Q30 | Q43 |
| 14 | Q6 | Q19 | Q31 | Q45 |
| 15 | [no branch] | [no branch] | [no branch] | [no branch] |

The printed note says ** SCRs are MCR 106-1 (E-585-29); all others 2N5060 (E-585-14) or equivalents. Prefix reference designations with A5. SCR-to-connector association requires tracing the page's crossing and junction lines; this excerpt does not assert that association.
