# Factory A5 lamp decoding and connector lists

W-1182-5c, schematics PDF page 2 and standalone A5 scan. Whole
decoder fan-out, grouped by data input PD0–PD3 (U1–U4).
The public address is derived as `16 * n + selector + 1` for
decoder U(n+1). A slash identifies additional connector branches
where the same SCR reaches a second pin. The independent wire
codes below are read from W-1187-1c, schematics PDF page 7.
`[blank]` is an undrawn wire code; `N/U` is printed text.

| Public | SCR | A5 jack | W-1182-5c function |
| --- | --- | --- | --- |
| 1 | Q14 | J1-18 | BONUS 1K |
| 2 | Q12 | J1-19 | BONUS 5K |
| 3 | Q13 | J1-17 | BONUS 9K |
| 4 | Q8 | J1-23 | N/U |
| 5 | Q9 | J1-14 | N/U |
| 6 | Q10 | J1-15 | “A B” VALUE 1K |
| 7 | Q11 | J1-16 | “A B” VALUE 5K |
| 8 | Q4 | J1-28 | N/U |
| 9 | Q1 | J1-24 | N/U |
| 10 | Q2 | J1-25 | N/U |
| 11 | Q3 | J2-21 / J1-26 | SHOOT AGAIN / N/U |
| 12 | Q7 | J1-27 / J2-13 | N/U / N/U |
| 13 | Q16 | J2-22 | BALL IN PLAY |
| 14 | Q5 | J2-16 | N PLAYER 1 |
| 15 | Q6 | J2-14 | PLAYER UP 1 |
| 16 | [blank] | [blank] | [selector 15 open] |
| 17 | Q29 | J1-1 | BONUS 2K |
| 18 | Q27 | J1-9 | BONUS 6K |
| 19 | Q28 | J1-8 | BONUS 10K |
| 20 | Q35 | J1-3 | N/U |
| 21 | Q34 | J1-2 | N/U |
| 22 | Q22 | J1-10 | “A B” VALUE 2K |
| 23 | Q26 | J1-7 | “A B” VALUE X BALL |
| 24 | Q25 | J1-6 | N/U |
| 25 | Q24 | J1-5 | N/U |
| 26 | Q17 | J1-11 | 5X POTENTIAL |
| 27 | Q23 | J2-8 | MATCH |
| 28 | Q21 | J1-12 / J2-12 | 5X MULTIPLIER / N/U |
| 29 | Q15 | J2-23 | HIGH GAME TO DATE |
| 30 | Q18 | J2-20 | N PLAYER 2 |
| 31 | Q19 | J2-15 | PLAYER UP 2 |
| 32 | [blank] | [blank] | [selector 15 open] |
| 33 | Q36 | J3-26 | BONUS 3K |
| 34 | Q38 | J3-25 | BONUS 7K |
| 35 | Q44 | J3-19 | BONUS 20K |
| 36 | Q49 | J3-17 | “B” TARGET (X2) |
| 37 | Q48 | J3-16 | N/U |
| 38 | Q37 | J3-23 | “A B” VALUE 3K |
| 39 | Q32 | J3-27 | “A B” VALUE SPEC |
| 40 | Q20 | J1-13 | RT OUTLANE 50K |
| 41 | Q42 | J3-21 | RT BOTTOM BUMPER |
| 42 | Q41 | J3-20 | 3X POTENTIAL |
| 43 | Q40 | J3-22 / J2-9 | PLAY FIELD SHOOT AGAIN / N/U |
| 44 | Q39 | J3-24 / J2-4 | 3X MULTIPLIER / N/U |
| 45 | Q33 | J2-11 | GAME OVER |
| 46 | Q30 | J2-6 | N PLAYER 3 |
| 47 | Q31 | J2-2 | PLAYER UP 3 |
| 48 | [blank] | [blank] | [selector 15 open] |
| 49 | Q57 | J3-1 | BONUS 4K |
| 50 | Q50 | J3-12 | BONUS 8K |
| 51 | Q51 | J3-15 | DROP TARGET SPEC |
| 52 | Q54 | J3-11 | “A” TARGET (X2) |
| 53 | Q55 | J3-9 | N/U |
| 54 | Q60 | J3-3 | “A B” VALUE 4K |
| 55 | Q59 | J3-4 | N/U |
| 56 | Q58 | J3-2 | LT OUTLANE 50K |
| 57 | Q56 | J3-10 | LT BOTTOM BUMPER |
| 58 | Q46 | J3-18 | 2X POTENTIAL |
| 59 | Q52 | J3-13 | CREDIT INDICATOR |
| 60 | Q53 | J3-14 / J2-3 | 2X MULTIPLIER / N/U |
| 61 | Q47 | J2-10 | TILT |
| 62 | Q43 | J2-7 | N PLAYER 4 |
| 63 | Q45 | J2-1 | PLAYER UP 4 |
| 64 | [blank] | [blank] | [selector 15 open] |

## W-1187-1c LAMP DRIVER A5, complete load connectors

Cells give wire code and TO caption. Brackets identify blank wire
cells. `NOTE 1` means reserved for future use. Note 2 says that
wire colors are shown for all connector pins and that some wires
may not be used in all games. The pin list and actual A6/A1 load
drawings govern fitment. Code 0 means no trace, rather than a
second color. The A5J4 logic/supply connector is separate.

| Pin | J1 | J2 | J3 |
| --- | --- | --- | --- |
| 1 | 41 BONUS 2K | 60 PLAYER UP 4 | 10 BONUS 4K |
| 2 | 43 N/U | 20 PLAYER UP 3 | 95 LT. OUT LANE 50K |
| 3 | 45 N/U | 84 NOTE 1 | 81 “AB” VALUE 4K |
| 4 | 35 N/U | 72 NOTE 1 | 14 N/U |
| 5 | 48 N/U | [blank] NOTE 1 | [blank] N/U |
| 6 | 25 N/U | 85 N. PLAYER 3 | [blank] N/U |
| 7 | 34 “AB” VALUE (X BALL) | 91 N. PLAYER 4 | [blank] N/U |
| 8 | 51 BONUS 10K | 93 MATCH | [blank] KEY |
| 9 | 52 BONUS 6K | 23 NOTE 1 | 15 N/U |
| 10 | 32 “AB” VALUE 2K | 98 TILT | 91 LT. BOTTOM BUMPER |
| 11 | 65 5X POTENTIAL | 95 GAME OVER | 20 “A” TARGET (X2) |
| 12 | 61 5X MULTIPLIER | 61 NOTE 1 | 21 BONUS 8K |
| 13 | 96 RT. OUT | 53 NOTE 1 | 13 CREDIT INDICATOR |
| 14 | 54 N/U | 12 PLAYER UP 1 | 84 2X MULTIPLIER |
| 15 | 13 “AB” VALUE 1K | 32 PLAYER UP 2 | 53 DROP TARGET SPEC. |
| 16 | 12 “AB” VALUE 5K | 34 N. PLAYER 1 | 25 N/U |
| 17 | 57 BONUS 9K | [blank] N/U | 27 “B” TARGET (X2) |
| 18 | 58 BONUS 1K | [blank] KEY | 56 2X POTENTIAL |
| 19 | 60 BONUS 5K | [blank] N/U | 67 BONUS 20K |
| 20 | [blank] KEY | 35 N. PLAYER 2 | 64 3X POTENTIAL |
| 21 | [blank] N/U | 47 SHOOT AGAIN | 30 RT. BOTTOM BUMPER |
| 22 | [blank] N/U | 62 BALL IN PLAY | 23 PLAYFIELD (SHOOT AGAIN) |
| 23 | 56 N/U | 97 HIGH GAME TO DATE | 98 “AB” VALUE 3K |
| 24 | 50 N/U | [no pin] | 72 3X MULTIPLIER |
| 25 | 90 N/U | [no pin] | 36 BONUS 7K |
| 26 | 91 N/U | [no pin] | 38 BONUS 3K |
| 27 | 53 N/U | [no pin] | 40 “AB” VALUE SPECIAL |
| 28 | 78 N/U | [no pin] | [blank] N/U |

W-1192-1c (page 8), A6, draws the feature lamp bus A2J1-7 at
5.4 VDC. Its BONUS 4K line reads A5J1-1 even though W-1182-5c
and W-1187-1c independently place BONUS 4K at A5J3-1 and assign
A5J1-1 to BONUS 2K. A6 names the left outlane LT OUT LANE SPEC.
and gives the two A and B branches explicitly as X2. CREDIT
INDICATOR is on the A6 harness, and the period playfield photograph
shows the corresponding small left apron lens. On W-1187-1c,
the A1 INSERT load drawing puts J2-3, -4 and -12 on spare
branches and labels -5 and -9 NOTE 1. These branch symbols do
not duplicate the playfield lamps.

## General illumination

W-1192-1c labels A6 GEN. ILLUM. 5.9 VAC, with A2J1-8 and
A2J1-5 on the feed, and A2J1-2 and A2J1-1 on RET. It supplies
no per-socket count. W-1187-1c A1 INSERT prints GEN. ILL. LAMPS
(14) on the A2J3-11/A2J3-2 branch and GEN ILL. (16) LAMPS on
the A2J3-10/A2J3-1 branch. W-1186-4c draws three lamps in
parallel between A2J2-1 and A2J2-5 in the coin door harness.
These are transformer-fed circuits with no public GI address.
