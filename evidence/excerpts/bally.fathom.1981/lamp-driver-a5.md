# Bally Fathom — A5 Lamp Driver schematic (W-1182-34c)

Source: `Bally_1981_Fathom_Schematics.pdf`, PDF page 8. Title block reads `A5 LAMP DRIVER
SCHEMATIC` / `FATHOM` / `# 1233` / `W-1182-34c`, sheet `11`. Transcribed by hand from a 400 dpi
render in five overlapping crops. Notes printed on the sheet:

1. `**SCR'S ARE MCR 106-1 (E-585-29), ALL OTHERS ARE 2N5060 (E-585-14) OR EQUIVALENTS.`
2. `ALL RESISTORS ARE 1/4W, +-5%.`
3. `PREFIX ALL REFERENCE DESIGNATIONS WITH "A5".`
4. `* INDICATES "AID" TEST POINT.`

## Address decode

`J4` carries the strobe from the MPU: pins 14/15/16/17 are `AD0`/`AD1`/`AD2`/`AD3` (printed
`LAMP ADDRESS`), pins 7/6/5/4 are `PD0`/`PD1`/`PD2`/`PD3` (printed `LAMP DATA`), pin 13 is
`STROBE 1`. Pins 8/9/10 are `KEY`/`SPARE`/`SPARE`.

Four `MC14514CP` (`E-620-37`) `BINARY TO ONE OF SIXTEEN DECODERS`, U1-U4. All four share the same
four address lines AD0-AD3 on inputs D1-D4 and the same `ST` strobe; each is enabled by one lamp
data line on its `I` (inhibit) pin: `PD0 -> U1`, `PD1 -> U2`, `PD2 -> U3`, `PD3 -> U4`. Sixty
`2.0K TYP. (X60)` resistors and sixty SCRs, Q1-Q60.

Every decoder uses outputs 0 through 14 and leaves output 15 (`1111-15`, chip pin 15) unconnected,
which is exactly the decoder-selector value PinMAME's `by35_lampStrobe` skips.

Decoder-output pin order is identical on all four chips: output 0 = pin 11, 1 = 9, 2 = 10, 3 = 8,
4 = 7, 5 = 6, 6 = 5, 7 = 4, 8 = 18, 9 = 17, 10 = 20, 11 = 19, 12 = 14, 13 = 13, 14 = 16, 15 = 15.
The drawn row order differs between chips: U1 and U2 are drawn 0..15, while U3 and U4 are drawn
12, 13, 14, 0, 1, ..., 11, 15.

Output-to-SCR, read row by row:

| output | U1 (PD0) | U2 (PD1) | U3 (PD2) | U4 (PD3) |
| --- | --- | --- | --- | --- |
| 0 | Q14 | Q29 | Q36 | Q57 |
| 1 | Q12 | Q27 | Q38 | Q50 |
| 2 | Q13 | Q28 | Q44 | Q51 |
| 3 | Q8 | Q35 | Q49 | Q54 |
| 4 | Q9 | Q34 | Q48 | Q55 |
| 5 | Q10 | Q22 | Q37 | Q60 |
| 6 | Q11 | Q26 | Q32 | Q59 |
| 7 | Q4 | Q25 | Q20 | Q58 |
| 8 | Q1 | Q24 | Q42 | Q56 |
| 9 | Q2 | Q17 | Q41 | Q46 |
| 10 | Q3 | Q23 | Q40 | Q52 |
| 11 | Q7 | Q21 | Q39 | Q53 |
| 12 | Q16 | Q15 | Q33 | Q47 |
| 13 | Q5 | Q18 | Q30 | Q43 |
| 14 | Q6 | Q19 | Q31 | Q45 |

## Connector pin functions, verbatim

Sixty-eight of the ninety-three connector positions drawn on this sheet carry an arrow from an SCR.
Sixty SCRs feed sixty-eight pins, so eight SCRs branch to a second pin; several of the branch
destinations are printed `N/U`. Pins printed `KEY` never carry an arrow.

`J1`, marked `TO PLAYFIELD`, first block (pins 22, 21 and 20 carry no arrow):

| pin | function |
| --- | --- |
| 22 | `N/U` (no arrow) |
| 21 | `N/U` (no arrow) |
| 20 | `KEY` (no arrow) |
| 18 | `50K RIGHT RETURN LANE` |
| 19 | `1K BLUE BONUS` |
| 17 | `5K BLUE BONUS` |
| 23 | `9K BLUE BONUS` |
| 14 | `3X BLUE BONUS` |
| 15 | `1K GREEN BONUS` |
| 16 | `5K GREEN BONUS` |
| 28 | `9K GREEN BONUS` |
| 24 | `3X GREEN BONUS` |
| 25 | `"C" LANE` |
| 26 | `N/U` |
| 27 | `RIGHT THUMPER BUMPER` |

`J1` second block:

| pin | function |
| --- | --- |
| 1 | `RIGHT OUT SPECIAL` |
| 9 | `2K BLUE BONUS` |
| 8 | `6K BLUE BONUS` |
| 3 | `10K BLUE BONUS` |
| 2 | `4X BLUE BONUS` |
| 10 | `2K GREEN BONUS` |
| 7 | `6K GREEN BONUS` |
| 6 | `10K GREEN BONUS` |
| 5 | `4X GREEN BONUS` |
| 11 | `"B" LANE` |
| 13 | `RELEASE LAGOON CAPTIVE BALL` |
| 4 | `N/U` |
| 12 | `BOTTOM THUMPER BUMPER` |

`J2`, marked `TO BACK BOX` (pins 17, 18 and 19 carry no arrow):

| pin | function |
| --- | --- |
| 21 | `SHOOT AGAIN` |
| 13 | `N/U` |
| 22 | `BALL IN PLAY` |
| 16 | `DBL. PLAYFIELD SCORES` |
| 14 | `TOP SAUCER LANE ARR` |
| 8 | `MATCH` |
| 12 | `N/U` |
| 23 | `HIGH SCORE TO DATE` |
| 20 | `TRIPLE PLAYFIELD SCR.` |
| 15 | `RIGHT SAUCER ARROW` |
| 11 | `GAME OVER` |
| 6 | `IN SEQUENCE` |
| 2 | `TO AUX. EXPANDOR J1-2` |
| 9 | `N/U` |
| 4 | `N/U` |
| 5 | `N/U` |
| 3 | `N/U` |
| 10 | `TILT` |
| 7 | `EXTRA BALL` |
| 1 | `BONUS SPECIAL` |
| 17 | `N/U` (no arrow) |
| 18 | `KEY` (no arrow) |
| 19 | `N/U` (no arrow) |

`J3`, marked `TO PLAYFIELD` (pins 5, 6, 7, 8 and 28 carry no arrow):

| pin | function |
| --- | --- |
| 26 | `LEFT OUT SPECIAL` |
| 25 | `3K BLUE BONUS` |
| 19 | `7K BLUE BONUS` |
| 17 | `ADVANCE GREEN BONUS (2)` |
| 16 | `5X BLUE BONUS` |
| 23 | `3K GREEN BONUS` |
| 27 | `7K GREEN BONUS` |
| 21 | `5X GREEN BONUS` |
| 20 | `"A" LANE` |
| 22 | `SAME PLAYER SHOOT AGAIN` |
| 24 | `LEFT THUMPER BUMPER` |
| 1 | `50K LEFT RETURN LANE` |
| 12 | `4K BLUE BONUS` |
| 15 | `8K BLUE BONUS` |
| 11 | `ADVANCE BLUE BONUS (2)` |
| 9 | `55K BLUE BONUS` |
| 3 | `4K GREEN BONUS` |
| 4 | `8K GREEN BONUS` |
| 2 | `RELEASE CAVE CAPTIVE BALL` |
| 10 | `55K GREEN BONUS` |
| 18 | `A-B-C SPECIAL` |
| 13 | `CREDIT INDICATOR` |
| 14 | `SPINNER` |
| 5 | `N/U` (no arrow) |
| 6 | `N/U` (no arrow) |
| 7 | `N/U` (no arrow) |
| 8 | `KEY` (no arrow) |
| 28 | `N/U` (no arrow) |

`(2)` after a function name is a bulb quantity: two bulbs on that one circuit.

## Which SCR reaches which pin

Only U1's first twelve SCRs run straight across the sheet with no crossing and can be paired with
their connector pin from the retained scan without ambiguity:

| decoder output | SCR | J1 pin | printed function |
| --- | --- | --- | --- |
| U1 0 | Q14 | 18 | `50K RIGHT RETURN LANE` |
| U1 1 | Q12 | 19 | `1K BLUE BONUS` |
| U1 2 | Q13 | 17 | `5K BLUE BONUS` |
| U1 3 | Q8 | 23 | `9K BLUE BONUS` |
| U1 4 | Q9 | 14 | `3X BLUE BONUS` |
| U1 5 | Q10 | 15 | `1K GREEN BONUS` |
| U1 6 | Q11 | 16 | `5K GREEN BONUS` |
| U1 7 | Q4 | 28 | `9K GREEN BONUS` |
| U1 8 | Q1 | 24 | `3X GREEN BONUS` |
| U1 9 | Q2 | 25 | `"C" LANE` |
| U1 10 | Q3 | 26 | `N/U` |
| U1 11 | Q7 | 27 | `RIGHT THUMPER BUMPER` |

The lines into J1-26 and J1-27 each carry a further vertical branch to a lower connector, which the
retained scan does not resolve.

The remaining forty-eight SCRs reach their pins through deeply nested staircase routing across the
middle of the sheet. The nesting order can be seen, but individual risers cannot be followed from
end to end on this scan with the confidence a validated assertion needs, and no other retained
source maps a connector pin to a public lamp address. Those forty-eight addresses are therefore
left semantically unresolved in the machine definition rather than assigned by inference.
