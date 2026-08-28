# Transcription: Capcom Big Bang Bar schematic set, sheet 10 of 12 (Lamp Matrix "B" Wiring) — X2 bulb-quantity annotations

Source: `manual-schematic.capcom.big-bang-bar.1996`
(SHA-256 `fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603`),
"DIAGRAM, LAMP MATRIX "B" WIRING", PB-5 WIRING, drawn by B. Ziegler, dated
6/7/96. This file's companion image is the **complete matrix-B wiring grid**
(all eight columns, lamp numbers 11-18 through 81-88), so the X2 census below is
verifiable from the committed crop alone.

The sheet's numbering key (No. / Description; sheet numbers are column*10+row
within matrix B; the public PinMAME address is 64 + (column-1)*8 + row):

| 11 BONUS 2X | 21 MODE: BABE SCANNER | 31 SHOOT: LEFT ORBIT | 41 MODE: COSMIC DARTZ | 51 RAMP JACKPOT | 61 CAPTIVE: LEFT 4 | 71 3-BANK URANUS | 81 SHOOT: UNDERGROUND 2 |
| 12 BONUS 3X | 22 MODE: CHASE WAITRESS | 32 SHOOT: BABE SCANNER | 42 MODE: TOUR DE BAR | 52 RAMP STANDUP LEFT | 62 CAPTIVE: LEFT 3 | 72 3-BANK NEPTUNE | 82 STAR BUMPER LEFT |
| 13 MODE: UNDERGROUND | 23 SHOOT: COSMIC DARTZ | 33 4-BANK MARS | 43 MODE: MOSH A GO-GO | 53 RAMP STANDUP RIGHT | 63 CAPTIVE: LEFT 2 | 73 3-BANK PLUTO | 83 STAR BUMPER MIDDLE |
| 14 MODE: BIG BANG | 24 SPECIAL (OUTLANE RIGHT) | 34 4-BANK PYTHOS | 44 MODE: HAPPY HOUR | 54 RAMP STANDUP SIDE | 64 CAPTIVE: LEFT 1 | 74 SHOOT: RIGHT ORBIT | 84 STAR BUMPER RIGHT |
| 15 MODE: BAR ROOM BRAWL | 25 BONUS 5X | 35 4-BANK VENUS | 45 MODE: EXTRA BALL | 55 DOUBLE JACKPOT | 65 CAPTIVE: RIGHT 4 | 75 D.J. EYES G.I. | 85 **DANCE FLOOR** |
| 16 MODE: RAY'S BALL BUSTERS | 26 BONUS 4X | 36 4-BANK MERCURY | 46 MODE: GET LUCKY | 56 SHOOT: TOUR DE BAR | 66 CAPTIVE: RIGHT 3 | 76 SHOOT: LUNA PALOOZA | 86 SHOOT: EXTRA BALL |
| 17 MODE: LOOPED IN SPACE | 27 BONUS 4X | 37 **FREE SHOT (OUTLANE LEFT)** | 47 MODE: LUNA PALOOZA | 57 SHOOT: UNDERGROUND 1 | 67 CAPTIVE: RIGHT 2 | 77 ISLAND: LOCK READY | 87 SHOOT: BIG BANG |
| 18 SHOOT AGAIN | 28 INLANE LEFT | 38 INLANE LEFT | 48 UNUSED | 58 QUALIFY MODE | 68 CAPTIVE: RIGHT 1 | 78 ISLAND: MODE READY | 88 U.R. FLIPPER G.I. 2 |

(as printed; the sheet prints "37 FREE SHOT (OUTLANE LEFT)" and "38 INLANE LEFT"
in column 3 -- the operators-manual lamp table's rows for the same test refs
agree, NO-counter aside -- and prints "38 UNUSED" only in the matrix-A key.)

In the wiring grid, exactly two B-matrix lamp symbols carry an "X2" annotation,
and the sheet set's own detail legend defines what X2 means: two #44-or-#555
bulbs wired in parallel between the column and row lines, each with its own
1N4004 diode (the legend is drawn beside the matrix-A grid and repeated on this
sheet's sibling detail):

- **"85 X2"** -- matrix B column 8, row 5 = public lamp address **125, Dance
  Floor (#44, LP00104)**: two #44 bulbs in parallel at one address.
- **"37 X2"** -- matrix B column 3, row 7 = public lamp address **87, Free Shot
  (Outlane L.) (#44, LP00104)**: two #44 bulbs in parallel at one address.

Every other lamp symbol in the committed grid carries no X2 annotation.

The companion matrix-A sheet (sheet 9 of 12, "DIAGRAM, LAMP MATRIX "A" WIRING")
carries the same X2 annotation on exactly its two coin-door lamps -- "11 COIN
DOOR 1&2 X2" (public lamp 1) and "12 COIN DOOR 3&4 X2" (public lamp 2); its
complete grid is committed as the companion image of
`lamp-matrix-a-x2-quantities.md`.

Sheet footer block: "Capcom Coin-Op, Inc. 3311 North Kennicott Avenue, Arlington
Heights, Illinois 60004 -- TITLE: DIAGRAM, LAMP MATRIX "B" WIRING -- PART NO.
PB-5 WIRING -- DRAWN B.ZIEGLER -- DATE 6/7/96 -- SHEET 10 OF 12".

Note: the printed operators-manual lamp table (printed page 81) prints no
quantity column, so these X2 marks are the only bulb-quantity evidence in the
retained document set.
