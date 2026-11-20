Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 28-29 and 37: the Lamp Driver schematic 12B-431S-113 decoders and connector blocks, and both copies of the lamp list. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) lamp driver transcription

Sources: PDF page 28 (decoders), PDF page 29 (connector blocks, lamp list copy), PDF page 37 (lamp list). Drawing 12B-431S-113.

Legend on sheet (verbatim, PDF page 28): `NOTES: 1. ▲ INDICATES MCR106-1 TRANSISTOR. 2. THIS DOCUMENT FOR LDA-100 REV. A AND LDA-REV. B SINGLE SIDED P.C. BOARDS.` SCRs without the triangle are printed `ZN5060` (the glyph reads 2N5060 in a 1979 scan font).

## 1. Decoder table (U1-U4, MC14514B)

Each decoder output Sn passes through a 2K ohm resistor R<n> to the gate of SCR Q<n>. In every one of the 60 lines the R number and the Q number are equal. Outputs S0-S14 are drawn; S15 has no line on any decoder. Rows are in the order of the drawing top to bottom (U3 and U4 print S12, S13, S14 first, then S0..S11).

| Decoder | Output | Resistor | SCR | Part printed at SCR |
|---|---|---|---|---|
| U1 | S0 | R14 | Q14 | 2N5060 (printed ZN5060) |
| U1 | S1 | R12 | Q12 | 2N5060 (printed ZN5060) |
| U1 | S2 | R13 | Q13 | 2N5060 (printed ZN5060) |
| U1 | S3 | R8 | Q8 | MCR106-1 (triangle) |
| U1 | S4 | R9 | Q9 | MCR106-1 (triangle) |
| U1 | S5 | R10 | Q10 | MCR106-1 (triangle) |
| U1 | S6 | R11 | Q11 | 2N5060 (printed ZN5060) |
| U1 | S7 | R4 | Q4 | 2N5060 (printed ZN5060) |
| U1 | S8 | R1 | Q1 | MCR106-1 (triangle) |
| U1 | S9 | R2 | Q2 | MCR106-1 (triangle) |
| U1 | S10 | R3 | Q3 | MCR106-1 (triangle) |
| U1 | S11 | R7 | Q7 | 2N5060 (printed ZN5060) |
| U1 | S12 | R16 | Q16 | MCR106-1 (triangle) |
| U1 | S13 | R5 | Q5 | 2N5060 (printed ZN5060) |
| U1 | S14 | R6 | Q6 | 2N5060 (printed ZN5060) |
| U1 | S15 | none drawn | none | |
| U2 | S0 | R29 | Q29 | 2N5060 (printed ZN5060) |
| U2 | S1 | R27 | Q27 | 2N5060 (printed ZN5060) |
| U2 | S2 | R28 | Q28 | 2N5060 (printed ZN5060) |
| U2 | S3 | R35 | Q35 | MCR106-1 (triangle) |
| U2 | S4 | R34 | Q34 | MCR106-1 (triangle) |
| U2 | S5 | R22 | Q22 | MCR106-1 (triangle) |
| U2 | S6 | R26 | Q26 | 2N5060 (printed ZN5060) |
| U2 | S7 | R25 | Q25 | 2N5060 (printed ZN5060) |
| U2 | S8 | R24 | Q24 | MCR106-1 (triangle) |
| U2 | S9 | R17 | Q17 | MCR106-1 (triangle) |
| U2 | S10 | R23 | Q23 | MCR106-1 (triangle) |
| U2 | S11 | R21 | Q21 | 2N5060 (printed ZN5060) |
| U2 | S12 | R15 | Q15 | MCR106-1 (triangle) |
| U2 | S13 | R18 | Q18 | 2N5060 (printed ZN5060) |
| U2 | S14 | R19 | Q19 | 2N5060 (printed ZN5060) |
| U2 | S15 | none drawn | none | |
| U3 | S12 | R33 | Q33 | MCR106-1 (triangle) |
| U3 | S13 | R30 | Q30 | 2N5060 (printed ZN5060) |
| U3 | S14 | R31 | Q31 | 2N5060 (printed ZN5060) |
| U3 | S0 | R36 | Q36 | 2N5060 (printed ZN5060) |
| U3 | S1 | R38 | Q38 | 2N5060 (printed ZN5060) |
| U3 | S2 | R44 | Q44 | 2N5060 (printed ZN5060) |
| U3 | S3 | R49 | Q49 | MCR106-1 (triangle) |
| U3 | S4 | R48 | Q48 | MCR106-1 (triangle) |
| U3 | S5 | R37 | Q37 | 2N5060 (printed ZN5060) |
| U3 | S6 | R32 | Q32 | 2N5060 (printed ZN5060) |
| U3 | S7 | R20 | Q20 | 2N5060 (printed ZN5060) |
| U3 | S8 | R42 | Q42 | MCR106-1 (triangle) |
| U3 | S9 | R41 | Q41 | MCR106-1 (triangle) |
| U3 | S10 | R40 | Q40 | MCR106-1 (triangle) |
| U3 | S11 | R39 | Q39 | 2N5060 (printed ZN5060) |
| U3 | S15 | none drawn | none | |
| U4 | S12 | R47 | Q47 | MCR106-1 (triangle) |
| U4 | S13 | R43 | Q43 | 2N5060 (printed ZN5060) |
| U4 | S14 | R45 | Q45 | 2N5060 (printed ZN5060) |
| U4 | S0 | R57 | Q57 | 2N5060 (printed ZN5060) |
| U4 | S1 | R50 | Q50 | 2N5060 (printed ZN5060) |
| U4 | S2 | R51 | Q51 | 2N5060 (printed ZN5060) |
| U4 | S3 | R54 | Q54 | MCR106-1 (triangle) |
| U4 | S4 | R55 | Q55 | MCR106-1 (triangle) |
| U4 | S5 | R60 | Q60 | 2N5060 (printed ZN5060) |
| U4 | S6 | R59 | Q59 | 2N5060 (printed ZN5060) |
| U4 | S7 | R58 | Q58 | 2N5060 (printed ZN5060) |
| U4 | S8 | R56 | Q56 | MCR106-1 (triangle) |
| U4 | S9 | R46 | Q46 | 2N5060 (printed ZN5060) |
| U4 | S10 | R52 | Q52 | 2N5060 (printed ZN5060) |
| U4 | S11 | R53 | Q53 | 2N5060 (printed ZN5060) |
| U4 | S15 | none drawn | none | |

## 2. Connector blocks (PDF page 29)

### J1 (25 listed branches, printed order top to bottom)

| # | Pin | SCR | Triangle | Mark |
|---|---|---|---|---|
| 1 | 18 | Q14 | no |  |
| 2 | 19 | Q12 | no |  |
| 3 | 17 | Q13 | no |  |
| 4 | 23 | Q8 | yes |  |
| 5 | ?(4) | Q9 | yes | pin digit overprinted by a blob over the arrowhead; reads '?4', the first digit illegible (the lamp list prints J-1 pin 4 on row 46 and J-1 pin 14 on row 48) |
| 6 | 15 | Q10 | yes |  |
| 7 | 16 | Q11 | no |  |
| 8 | 28 | Q4 | no |  |
| 9 | 24 | Q1 | yes |  |
| 10 | 25 | Q2 | yes |  |
| 11 | 26 | Q3 | yes |  |
| 12 | 27 | Q7 | no |  |
| 13 | 1 | Q29 | no | pin digit faint, reads '1' |
| 14 | 9 | Q27 | no |  |
| 15 | 8 | Q28 | no |  |
| 16 | 3 | Q35 | yes |  |
| 17 | 2 | Q34 | yes |  |
| 18 | 10 | Q22 | yes |  |
| 19 | 7 | Q26 | no |  |
| 20 | 6 | Q25 | no |  |
| 21 | 5 | Q24 | yes |  |
| 22 | 11 | Q17 | yes |  |
| 23 | 13 | Q20 | no | first digit smeared, reads 13 |
| 24 | 14 | Q23 | yes |  |
| 25 | 12 | Q21 | no | X drawn through the triangle column between pin 12 and Q21 |

### J2 (20 listed branches, printed order top to bottom)

| # | Pin | SCR | Triangle | Mark |
|---|---|---|---|---|
| 1 | 2 | Q3 | yes |  |
| 2 | 13 | Q7 | no |  |
| 3 | ?2 | Q16 | yes | first digit illegible |
| 4 | 16 | Q5 | yes |  |
| 5 | 1? | Q6 | no | second digit illegible |
| 6 | ? (3, 5 or 8) | Q23 | yes | single glyph, ambiguous |
| 7 | 12 | Q21 | no |  |
| 8 | ?3 | Q15 | yes | first digit illegible |
| 9 | 20 | Q18 | no |  |
| 10 | 15 | Q19 | no |  |
| 11 | 11 | Q33 | yes |  |
| 12 | ? | Q30 | no | pin digit smudged, nothing legible (looks like a '6'-ish smudge) |
| 13 | 2 | Q31 | no |  |
| 14 | 9 | Q40 | yes |  |
| 15 | ? (4) | Q39 | no | bold smudge, reads '4' with a mark |
| 16 | 5 | Q52 | no |  |
| 17 | 10 | Q47 | yes |  |
| 18 | 7 | Q43 | no |  |
| 19 | 1 | Q45 | no |  |
| 20 | 3 | Q53 | no |  |

### J3 (23 listed branches, printed order top to bottom)

| # | Pin | SCR | Triangle | Mark |
|---|---|---|---|---|
| 1 | 26 | Q36 | no |  |
| 2 | 25 | Q38 | no |  |
| 3 | 9 | Q44 | no |  |
| 4 | 17 | Q49 | yes |  |
| 5 | 6 | Q48 | yes |  |
| 6 | 23 | Q37 | no |  |
| 7 | 27 | Q32 | no |  |
| 8 | 21 | Q42 | yes |  |
| 9 | 20 | Q41 | yes |  |
| 10 | 22 | Q40 | yes |  |
| 11 | 24 | Q39 | no |  |
| 12 | ? | Q57 | no | pin cell blank except a stray dot |
| 13 | 12 | Q50 | no | reads '12' with a faint first digit |
| 14 | 15 | Q51 | no |  |
| 15 | ? | Q54 | yes | pin cell blank |
| 16 | ? (9) | Q55 | yes | smudged blob, reads '9' |
| 17 | ? (3) | Q60 | no | smudged blob, reads '3' |
| 18 | 4 | Q59 | no |  |
| 19 | 2 | Q58 | no |  |
| 20 | 10 | Q56 | yes |  |
| 21 | 8 | Q46 | no |  |
| 22 | 3 | Q52 | no |  |
| 23 | 14 | Q53 | no |  |

## 3. Lamp list (PDF page 37, printed order; "dash" = rows with leader dashes)

| # | Description | Wire color | Jack | Pin | Leader dashes |
|---|---|---|---|---|---|
| 1 | BOT. LT. BANK "WOW" | R-G | J-2 | 7 |  |
| 2 | BOT. LT. D.T. SPECIAL | BRN-B | J-1 | 18 |  |
| 3 | GAME OVER | GREY-W | J-2 | 11 | yes |
| 4 | HIGH SCORE TO DATE | GREY-O | J-2 | 22 |  |
| 5 | LT. OUT LANE & RT. BUMPER | B-BLU | J-2 | 23 |  |
| 6 | LT. R/O & RETURN LANE | BRN-BLU | J-1 | 24 |  |
| 7 | MATCH | GREY-Y | J-2 | 1 | yes |
| 8 | METEOR "DROP" E | PUR-B | J-1 | 25 |  |
| 9 | METEOR "DROP #1E | W-O | J-3 | 20 |  |
| 10 | METEOR "DROP" R | B-G | J-3 | 21 |  |
| 11 | METEOR "DROP" T | B-O | J-1 | 11 | yes |
| 12 | METEOR "DROP" M | R-BLU | J-3 | 18 |  |
| 13 | METEOR "DROP "O" | GREY-B | J-3 | 10 |  |
| 14 | METEOR "WOW" E | W-BLUE | J-1 | 13 |  |
| 15 | METEOR "WOW" 2E | B-W | J-1 | 28 | yes |
| 16 | METEOR "WOW" M | Y-G | J-3 | 2 |  |
| 17 | METEOR "WOW" O | R-W | J-3 | 4 |  |
| 18 | METEOR "WOW" R | O-W | J-3 | 27 |  |
| 19 | METEOR "WOW" T | BRN-R | J-1 | 6 | yes |
| 20 | #1 (L) ROCKET 1K | O-R | J-3 | 12 |  |
| 21 | #1 (L) ROCKET 2K | R-Y | J-3 | 25 |  |
| 22 | #1 (L) ROCKET 3K | GREY | J-1 | 9 |  |
| 23 | #1 (L) ROCKET 4K | GREY-G | J-1 | 19 | yes |
| 24 | #1 (L) ROCKET 5K | G-R | J-3 | 1 |  |
| 25 | #1 (L) ROCKET 6K | -B- | J-3 | 26 |  |
| 26 | #1 (L) ROCKET 7K | BLU-R | J-1 | 1 |  |
| 27 | 1X | BLU-R | J-2 | 14 | yes |
| 28 | #2 (M) ROCKET 1K | -W- | J-3 | 11 |  |
| 29 | #2 (M) ROCKET 2K | Y-BLUE | J-3 | 17 |  |
| 30 | #2 (M) ROCKET 3K | R-G | J-1 | 3 |  |
| 31 | #2 (M) ROCKET 4K | BLU-W | J-1 | 23 | yes |
| 32 | #2 (M) ROCKET 5K | W-B | J-3 | 15 |  |
| 33 | #2 (M) Rocket 6K | B-R | J-3 | 19 |  |
| 34 | #2 (M) ROCKET 7K | G-B | J-1 | 8 |  |
| 35 | 2X | O-B | J-3 | 15 | yes |
| 36 | #3 (R) ROCKET 1K | W-BLU | J-3 | 3 |  |
| 37 | #3 (R) ROCKET 2K | W-GREY | J-3 | 23 |  |
| 38 | #3 (R) ROCKET 3K | GREY-BLU | J-1 | 10 |  |
| 39 | #3 (R) ROCKET 4K | GREY-Y | J-1 | 15 | yes |
| 40 | #3 (R) ROCKET 5K | W-R | J-3 | 9 |  |
| 41 | #3 (R) ROCKET 6K | R-B | J-3 | 16 |  |
| 42 | #3 (R) ROCKET 7K | PUR-W | J-1 | 2 |  |
| 43 | 4X | R-BLU | J-2 | 2 | yes |
| 44 | RT. BANK SPECIAL | Y-G | J-1 | 7 |  |
| 45 | RT. BANK "WOW" | Y-B | J-2 | 20 |  |
| 46 | RT. OUT-LANE & LT. BUMPER | PUR-Y | J-1 | 4 |  |
| 47 | RT. R/O & LT. RETURN LANE | BLU-O | J-1 | 5 | yes |
| 48 | M . R/O TAR. & S.U. SPOT METEOR | GREY-O | J-1 | 14 |  |
| 49 | SHOOT AGAIN (INSERT) | GREY-R | J-2 | 21 |  |
| 50 | SPIN #1 | B-W | J-3 | 14 |  |
| 51 | SPIN #2 | GREY-W | J-3 | 24 | yes |
| 52 | SPIN #3 | W-Y | J-1 | 12 |  |
| 53 | SPIN #4 | GREY-B | J-1 | 27 |  |
| 54 | SPIN #5 | B-Y | J-3 | 13 |  |
| 55 | SPIN #6 | GREY | J-3 | 22 | yes |
| 56 | S.P.S.A. | GREY-R | J-1 | 26 |  |
| 57 | S.U. TAR. SPECIAL | -B- | J-1 | 16 |  |
| 58 | S.U. TAR."WOW | Y-BLU | J-2 | 16 |  |
| 59 | BOT LT. BANK "WOW" | R-G | J-3 | 7 | yes |
| 60 | TOP LT. BANK "WOW" | BLU-W | J-2 | 6 |  |
| 61 | TOP LT. D.T.SPECIAL | -PUR- | J-1 | 17 |  |

Header as printed: `DESCRIPTION / WIRE COLOR / JACK "A" LDA-J1 / PIN NO.`

### Differences PDF page 29 copy vs PDF page 37

| Row | Item | Difference |
|---|---|---|
| 6 | LT. R/O & RETURN LANE | PDF page 29 has a handwritten 'rt.' after 'LANE' (ink, small, beside the row); PDF page 37 has nothing |
| after 61 | Tilt | PDF page 29 has a handwritten extra row below the typed list: 'Tilt' / 'grey-blk' / 'J-2' / '10' (written in a single hand with no leader dashes); not on PDF page 37 |
| heading | PDF page 29 prints 'METEOR' (underlined) above the WIRE COLOR column; PDF page 37 copy has no such title line (page header differs) | title line only |
| 59 | BOT LT. BANK "WOW" | PDF page 29 scan is smudged on wire colour and pin (reads 'R-G' J-3, pin a smudge resembling 9/7); PDF page 37 reads R-G J-3 7. Treated as legibility, not a content difference |
| 35, 39 | 2X and #3 4K rows | PDF page 29 has tiny stray marks after 'J-3'/'J-1' (specks), not text |
| 20-26 | #1 (L) rows | PDF page 29 shows a vertical ruled bar beside '(L)'; likely scan artefact |
| all others |  | descriptions, wire colours, jacks and pins agree row by row with PDF page 37 (PDF page 29 is a lower-quality copy; blurred glyphs such as GREY-G/GREY-O, G-R/O-R, 23/25 were resolved at 4x zoom to agree with PDF page 37) |

## 4. Cross-reference (jack, pin) to SCR

| # | Description | Jack | Pin | SCR via connector blocks |
|---|---|---|---|---|
| 1 | BOT. LT. BANK "WOW" | J-2 | 7 | Q43 |
| 2 | BOT. LT. D.T. SPECIAL | J-1 | 18 | Q14 |
| 3 | GAME OVER | J-2 | 11 | Q33 |
| 4 | HIGH SCORE TO DATE | J-2 | 22 | none |
| 5 | LT. OUT LANE & RT. BUMPER | J-2 | 23 | none |
| 6 | LT. R/O & RETURN LANE | J-1 | 24 | Q1 |
| 7 | MATCH | J-2 | 1 | Q45 |
| 8 | METEOR "DROP" E | J-1 | 25 | Q2 |
| 9 | METEOR "DROP #1E | J-3 | 20 | Q41 |
| 10 | METEOR "DROP" R | J-3 | 21 | Q42 |
| 11 | METEOR "DROP" T | J-1 | 11 | Q17 |
| 12 | METEOR "DROP" M | J-3 | 18 | none |
| 13 | METEOR "DROP "O" | J-3 | 10 | Q56 |
| 14 | METEOR "WOW" E | J-1 | 13 | Q20 |
| 15 | METEOR "WOW" 2E | J-1 | 28 | Q4 |
| 16 | METEOR "WOW" M | J-3 | 2 | Q58 |
| 17 | METEOR "WOW" O | J-3 | 4 | Q59 |
| 18 | METEOR "WOW" R | J-3 | 27 | Q32 |
| 19 | METEOR "WOW" T | J-1 | 6 | Q25 |
| 20 | #1 (L) ROCKET 1K | J-3 | 12 | Q50 |
| 21 | #1 (L) ROCKET 2K | J-3 | 25 | Q38 |
| 22 | #1 (L) ROCKET 3K | J-1 | 9 | Q27 |
| 23 | #1 (L) ROCKET 4K | J-1 | 19 | Q12 |
| 24 | #1 (L) ROCKET 5K | J-3 | 1 | none |
| 25 | #1 (L) ROCKET 6K | J-3 | 26 | Q36 |
| 26 | #1 (L) ROCKET 7K | J-1 | 1 | Q29 |
| 27 | 1X | J-2 | 14 | none |
| 28 | #2 (M) ROCKET 1K | J-3 | 11 | none |
| 29 | #2 (M) ROCKET 2K | J-3 | 17 | Q49 |
| 30 | #2 (M) ROCKET 3K | J-1 | 3 | Q35 |
| 31 | #2 (M) ROCKET 4K | J-1 | 23 | Q8 |
| 32 | #2 (M) ROCKET 5K | J-3 | 15 | Q51 |
| 33 | #2 (M) Rocket 6K | J-3 | 19 | none |
| 34 | #2 (M) ROCKET 7K | J-1 | 8 | Q28 |
| 35 | 2X | J-3 | 15 | Q51 |
| 36 | #3 (R) ROCKET 1K | J-3 | 3 | Q52 |
| 37 | #3 (R) ROCKET 2K | J-3 | 23 | Q37 |
| 38 | #3 (R) ROCKET 3K | J-1 | 10 | Q22 |
| 39 | #3 (R) ROCKET 4K | J-1 | 15 | Q10 |
| 40 | #3 (R) ROCKET 5K | J-3 | 9 | Q44 |
| 41 | #3 (R) ROCKET 6K | J-3 | 16 | none |
| 42 | #3 (R) ROCKET 7K | J-1 | 2 | Q34 |
| 43 | 4X | J-2 | 2 | Q3, Q31 |
| 44 | RT. BANK SPECIAL | J-1 | 7 | Q26 |
| 45 | RT. BANK "WOW" | J-2 | 20 | Q18 |
| 46 | RT. OUT-LANE & LT. BUMPER | J-1 | 4 | none |
| 47 | RT. R/O & LT. RETURN LANE | J-1 | 5 | Q24 |
| 48 | M . R/O TAR. & S.U. SPOT METEOR | J-1 | 14 | Q23 |
| 49 | SHOOT AGAIN (INSERT) | J-2 | 21 | none |
| 50 | SPIN #1 | J-3 | 14 | Q53 |
| 51 | SPIN #2 | J-3 | 24 | Q39 |
| 52 | SPIN #3 | J-1 | 12 | Q21 |
| 53 | SPIN #4 | J-1 | 27 | Q7 |
| 54 | SPIN #5 | J-3 | 13 | none |
| 55 | SPIN #6 | J-3 | 22 | Q40 |
| 56 | S.P.S.A. | J-1 | 26 | Q3 |
| 57 | S.U. TAR. SPECIAL | J-1 | 16 | Q11 |
| 58 | S.U. TAR."WOW | J-2 | 16 | Q5 |
| 59 | BOT LT. BANK "WOW" | J-3 | 7 | none |
| 60 | TOP LT. BANK "WOW" | J-2 | 6 | none |
| 61 | TOP LT. D.T.SPECIAL | J-1 | 17 | Q13 |

Lamp rows with no SCR on that (jack, pin): row 4 HIGH SCORE TO DATE J-2 pin 22; row 5 LT. OUT LANE & RT. BUMPER J-2 pin 23; row 12 METEOR "DROP" M J-3 pin 18; row 24 #1 (L) ROCKET 5K J-3 pin 1; row 27 1X J-2 pin 14; row 28 #2 (M) ROCKET 1K J-3 pin 11; row 33 #2 (M) Rocket 6K J-3 pin 19; row 41 #3 (R) ROCKET 6K J-3 pin 16; row 46 RT. OUT-LANE & LT. BUMPER J-1 pin 4; row 49 SHOOT AGAIN (INSERT) J-2 pin 21; row 54 SPIN #5 J-3 pin 13; row 59 BOT LT. BANK "WOW" J-3 pin 7; row 60 TOP LT. BANK "WOW" J-2 pin 6

Lamp rows sharing a (jack, pin): {"J-3 pin 15": [32, 35]}

Connector (block, pin) carrying two SCRs: {"J-2 pin 2": ["Q3", "Q31"]}

SCRs appearing in more than one connector block: Q3, Q7, Q21, Q23, Q39, Q40, Q52, Q53

SCRs in a connector block but named by no lamp row (literal pins only): Q6, Q9, Q15, Q16, Q19, Q30, Q46, Q47, Q48, Q54, Q55, Q57, Q60

SCRs in the decoder table that appear in no connector block: none

## Uncertain readings

- J1 Q9 pin: `?4` (blob over arrow), the first digit not read. The lamp list prints both J-1 pin 4 (row 46) and J-1 pin 14 (row 48), so the list does not settle it.
- J1 Q29 pin: faint `1`.
- J1 Q20 pin: `13` with a smeared first digit.
- J2 Q16 pin `?2`, Q6 pin `1?`, Q23 pin single ambiguous glyph (3/5/8), Q15 pin `?3`, Q30 pin illegible, Q39 pin `?4`.
- J3 Q57 and Q54 pin cells blank, Q55 pin `?9`, Q60 pin `?3`. J3 Q48 pin reads 6.
- J1 Q21: an X is drawn in the triangle column at pin 12; it may cancel the entry.
- Decoder U2 S9 SCR label Q17 is half cut off where two enlargements meet; confirmed only by the J1 block listing Q17.
- Decoder U4 S7 resistor label R58 is printed bold and heavy; read as R58, SCR Q58 clear.
- Decoder S-index labels at U3/U4 top show S12 S13 S14 first, not S0 first; transcribed as drawn.
- Lamp list PDF page 29 copy is blurred at 300 dpi; wire colours GREY-G/GREY-O and pins 23/25 on #1/#3 rocket rows were settled at 4x zoom.
- Row 9 description reads `METEOR "DROP #1E` on both pages (the opening quote is unpaired; `#1` looks hand-typed over the original).
