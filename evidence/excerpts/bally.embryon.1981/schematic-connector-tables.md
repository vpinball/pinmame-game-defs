# Embryon schematic connector tables

Source-literal transcription from native TIFFs, checked against the sheets by the
primary curator. Blank cells, N/U and KEY are retained distinctly. Source W-1255
and A9 disagree on the quantities at public 70 and 86. Public address columns are
derived from the emulator's decoder formula; they are not printed on the drawings.

## A5 connector regions: lamp.tif

### J1

| Pin | Literal label |
|---:|---|
| 22 | N/U |
| 21 | N/U |
| 20 | KEY |
| 18 | 1K BONUS |
| 19 | 5K BONUS |
| 17 | 9K BONUS |
| 23 | 20K BONUS |
| 14 | 2X BONUS |
| 15 | BOTTOM ROLLOVER BUTTON |
| 16 | "E" |
| 28 | "Y" |
| 24 | "A" LANE |
| 25 | 25K ARROW (TOP LANES) |
| 26 | N/U |
| 27 | RIGHT BOTTOM THUMPER BUMPER |
| 1 | 2K BONUS |
| 9 | 6K BONUS |
| 8 | 10K BONUS |
| 3 | 40K BONUS |
| 2 | 3X BONUS |
| 10 | MIDDLE ROLLOVER BUTTON |
| 7 | "M" |
| 6 | "O" |
| 5 | "B" LANE |
| 11 | 50K ARROW (TOP LANES) |
| 13 | "N" |
| 4 | N/U |
| 12 | RIGHT TOP THUMPER BUMPER |

### J2

| Pin | Literal label |
|---:|---|
| 21 | SHOOT AGAIN |
| 13 | N/U |
| 22 | BALL IN PLAY |
| 16 | "E" BACKGLASS |
| 14 | "Y" BACKGLASS |
| 8 | MATCH |
| 12 | N/U |
| 23 | HIGH SCORE TO DATE |
| 20 | "M" BACKGLASS |
| 15 | "O" BACKGLASS |
| 11 | GAME OVER |
| 6 | "B" BACKGLASS |
| 2 | "N" BACKGLASS |
| 9 | N/U |
| 4 | N/U |
| 5 | N/U |
| 3 | N/U |
| 10 | TILT |
| 7 | "R" BACKGLASS |
| 1 | N/U |
| 17 | N/U |
| 18 | KEY |
| 19 | N/U |

### J3

| Pin | Literal label |
|---:|---|
| 26 | 3K BONUS |
| 25 | 7K BONUS |
| 19 | RIGHT OUTLANE SPECIAL |
| 17 | BONUS SPECIAL |
| 16 | 4X BONUS |
| 23 | TOP ROLLOVER BUTTON |
| 27 | "B" |
| 21 | "1" LANE |
| 20 | EXTRA BALL ARROW (TOP LANES) |
| 22 | SAME PLAYER SHOOT AGAIN |
| 24 | LEFT BOTTOM THUMPER BUMPER |
| 1 | 4K BONUS |
| 12 | 8K BONUS |
| 15 | LEFT OUTLANE SPECIAL |
| 11 | N/U |
| 9 | 5X ARROW |
| 3 | SAUCER ARROW |
| 4 | "R" |
| 2 | N/U |
| 10 | "2" LANE |
| 18 | SPECIAL ARROW (TOP LANES) |
| 13 | CREDIT INDICATOR |
| 14 | LEFT TOP THUMPER BUMPER |
| 5 | N/U |
| 6 | N/U |
| 7 | N/U |
| 8 | KEY |
| 28 | N/U |

## A9 outputs: lampaux.tif

| Public | Decoder | Selector | SCR | Connector | Literal label |
|---:|---|---:|---|---|---|
| 65 | U2 | 0 | Q1 | A9J2-7 | 20K SINGLE DROP TARGET |
| 66 | U2 | 1 | Q2 | A9J2-4 | 25K LEFT DROP TARGETS |
| 67 | U2 | 2 | Q3 | A9J2-8 | CENTER RIGHT UPPER TARGET |
| 68 | U2 | 3 | Q4 | A9J2-10 | COLLECT BONUS TOP DROP TARGETS |
| 69 | U2 | 4 | Q5 | A9J2-9 | SPOTS LETTER (RIGHT) TOP DROP TARGETS |
| 70 | U2 | 5 | Q6 | A9J2-6 | RIGHT CENTER CAPTIVE BALLS (2) |
| 71 | U2 | 6 | Q7 | A9J2-5 | TOP CENTER LANE ARROW |
| 72 | U2 | 7 | — | — | N/U |
| 81 | U3 | 0 | Q8 | A9J2-14 | 30K SINGLE DROP TARGET |
| 82 | U3 | 1 | Q9 | A9J2-11 | 50K LEFT DROP TARGETS |
| 83 | U3 | 2 | Q10 | A9J2-15 | CENTER RIGHT LOWER TARGET |
| 84 | U3 | 3 | Q11 | A9J2-18 | SPOTS MULTIPLIER TOP DROP TARGETS |
| 85 | U3 | 4 | Q12 | A9J2-17 | SPOTS LETTER (BOTTOM) TOP DROP TARGETS |
| 86 | U3 | 5 | Q13 | A9J2-13 | LEFT CENTER CAPTIVE BALLS (1) |
| 87 | U3 | 6 | Q14 | A9J2-12 | TOP CENTER LANE L. & R. BLUE SHIELDS |
| 88 | U3 | 7 | — | — | N/U |
| 97 | U4 | 0 | Q15 | A9J3-8 | SPOTS MULTIPLIER SINGLE DROP TARGET |
| 98 | U4 | 1 | Q16 | A9J3-3 | EXTRA BALL LEFT DROP TARGETS |
| 99 | U4 | 2 | Q17 | A9J3-9 | CENTER LEFT LOWER TARGET |
| 100 | U4 | 3 | Q18 | A9J3-11 | EXTRA BALL TOP DROP TARGETS |
| 101 | U4 | 4 | Q19 | A9J3-10 | SPOTS LETTER (LEFT) TOP DROP TARGETS |
| 102 | U4 | 5 | Q20 | A9J3-7 | SPOTS LETTER CENTER BALL |
| 103 | U4 | 6 | Q21 | A9J3-4 | RIGHT FLIPPER BUTTON RELEASE BALL |
| 104 | U4 | 7 | — | — | N/U |
| 113 | U5 | 0 | Q22 | A9J3-15 | SPINNER ARROW |
| 114 | U5 | 1 | Q23 | A9J3-12 | SPECIAL LEFT DROP TARGETS |
| 115 | U5 | 2 | Q24 | A9J3-16 | CENTER LEFT UPPER TARGET |
| 116 | U5 | 3 | Q25 | A9J3-18 | SPECIAL TOP DROP TARGETS |
| 117 | U5 | 4 | Q26 | A9J3-17 | N/U |
| 118 | U5 | 5 | Q27 | A9J3-14 | RELEASE BALL SINGLE DROP TARGET |
| 119 | U5 | 6 | Q28 | A9J3-13 | FLIPSAVE WHEN FLASHING |
| 120 | U5 | 7 | — | — | N/U |

### wiring1.tif — W-1255 playfield feature-lamp harness

| Wire code | Connector | Literal label |
|---|---|---|
| 72 | A9J3-18 | SPECIAL TOP DROP TARGETS |
| N/U | A9J3-17 | [blank] |
| 56 | A9J3-16 | CENTER LEFT UPPER TARGET |
| 14 | A9J3-15 | SPINNER ARROW |
| 26 | A9J3-14 | RELEASE BALL SINGLE DROP TARGET |
| 96 | A9J3-13 | FLIPSAVE WHEN FLASHING |
| 21 | A9J3-12 | SPECIAL LEFT DROP TARGETS |
| 70 | A9J3-11 | EXTRA BALL TOP DROP TARGETS |
| 25 | A9J3-10 | SPOTS LETTER (LEFT) TOP DROP TARGETS |
| 53 | A9J3-9 | CENTER LEFT LOWER TARGET |
| 13 | A9J3-8 | SPOTS MULTIPLIER SINGLE DROP TARGET |
| 82 | A9J3-7 | SPOTS LETTER CENTER BALL |
| N/U | A9J3-6 | [blank] |
| N/U | A9J3-5 | [blank] |
| 95 | A9J3-4 | RIGHT FLIPPER BUTTON RELEASE BALL |
| 20 | A9J3-3 | EXTRA BALL LEFT DROP TARGETS |
| 57 | A9J2-18 | SPOTS MULTIPLIER TOP DROP TARGETS |
| 43 | A9J2-17 | SPOTS LETTER (BOTTOM) TOP DROP TARGETS |
| N/U | A9J2-16 | [blank] |
| 52 | A9J2-15 | CENTER RIGHT LOWER TARGET |
| 12 | A9J2-14 | 30K SINGLE DROP TARGET |
| 40 | A9J2-13 | LEFT CENTER CAPTIVE BALLS (2) |
| 62 | A9J2-12 | TOP CENTER LANE L.& R. BLUE SHIELDS |
| 18 | A9J2-11 | 50K LEFT DROP TARGETS |
| 80 | A9J2-10 | COLLECT BONUS TOP DROP TARGETS |
| 54 | A9J2-9 | SPOTS LETTER (RIGHT) TOP DROP TARGETS |
| 51 | A9J2-8 | CENTER RIGHT UPPER TARGET |
| 10 | A9J2-7 | 20K SINGLE DROP TARGET |
| 45 | A9J2-6 | RIGHT CENTER CAPTIVE BALLS (1) |
| 60 | A9J2-5 | TOP CENTER LANE ARROW |
| 15 | A9J2-4 | 25K LEFT DROP TARGETS |
| 20 | A2J1-5 | FEATURE LAMP BUS |

The two captive-ball descriptions on W-1255 differ from W-1207-8: J2-6 is (1) here versus (2) there, while J2-13 is (2) here versus (1) there. Preserve both; no resolution is asserted.

## A5 J4 input region — lamp.tif

| Pin | Literal signal |
|---:|---|
| 1 | GND |
| 2 | GND |
| 3 | +5V |
| 4 | PD3 |
| 5 | PD2 |
| 6 | PD1 |
| 7 | PD0 |
| 8 | KEY |
| 9 | SPARE |
| 10 | SPARE |
| 11 | GND |
| 12 | GND |
| 13 | STROBE1 |
| 14 | AD0 |
| 15 | AD1 |
| 16 | AD2 |
| 17 | AD3 |

## A9 connector regions — lampaux.tif

J1's internal circuit labels and harness table are separate printed regions. A
blank harness cell is left blank even where the internal circuit shows ground.

| J1 pin | Internal signal | Harness wire | Harness destination |
|---:|---|---|---|
| 1 | AD1 | 13 | A5J4-15 |
| 2 | AD0 | 32 | A5J4-14 |
| 3 | LAMP STROBE | 90 | A4J1-8 |
| 4 | AD2 | 45 | A5J4-16 |
| 5 | N/U | [blank] | [blank] |
| 6 | KEY | [blank] | KEY |
| 7 | PD1 | 65 | A5J4-6 |
| 8 | PD0 | 63 | A5J4-7 |
| 9 | PD2 | 71 | A5J4-5 |
| 10 | PD3 | 74 | A5J4-4 |
| 11 | +5 | 84 | A5J4-3 |
| 12 | N/U | [blank] | [blank] |
| 13 | GND | [blank] | [blank] |
| 14 | GND | [blank] | [blank] |
| 15 | GND | 58 | A5J4-11 |

Complete J2/J3 harness wire-code tables (different from the circuit's load labels
above). J3-5/6/19/20 have internal ground connections, but the harness prints N/U.

| Pin | A9J2 wire | A9J3 wire |
|---:|---|---|
| 1 | N/U | N/U |
| 2 | N/U | KEY |
| 3 | KEY | 20 |
| 4 | 15 | 95 |
| 5 | 60 | N/U |
| 6 | 45 | N/U |
| 7 | 10 | 82 |
| 8 | 51 | 13 |
| 9 | 54 | 53 |
| 10 | 80 | 25 |
| 11 | 18 | 70 |
| 12 | 62 | 21 |
| 13 | 40 | 96 |
| 14 | 12 | 26 |
| 15 | 52 | 14 |
| 16 | N/U | 56 |
| 17 | 43 | N/U |
| 18 | 57 | 72 |
| 19 | [not present] | N/U |
| 20 | [not present] | N/U |
