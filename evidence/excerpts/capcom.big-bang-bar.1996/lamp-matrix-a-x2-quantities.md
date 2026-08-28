# Transcription: Capcom Big Bang Bar schematic set, sheet 9 of 12 (Lamp Matrix "A" Wiring) — X2 bulb-quantity annotations

Source: `manual-schematic.capcom.big-bang-bar.1996`
(SHA-256 `fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603`),
"DIAGRAM, LAMP MATRIX "A" WIRING", PB-5 WIRING, drawn by B. Ziegler, dated
6/7/96. This file's companion image is the **complete matrix-A wiring grid**
(all eight columns, lamp numbers 11-18 through 81-88, with the dashed
"COIN DOOR / CABINET" boundary drawn around the first column), so the X2 census
below is verifiable from the committed crop alone.

The sheet's numbering key (No. / Description; sheet numbers are column*10+row
within matrix A; the public PinMAME address is (column-1)*8 + row):

| 11 **COIN DOOR 1&2** | 21 4-BANK G.I. 1 | 31 U.R. FLIPPER G.I. 1 | 41 TUBE G.I. 1 | 51 HOOT G.I. 1 | 61 RIGHT ORBIT CHASE 1 | 71 ROLLOVER "B" | 81 (ELECTRO) RAMP 1 |
| 12 **COIN DOOR 3&4** | 22 4-BANK G.I. 2 | 32 EJECT HOLE G.I. 1 | 42 TUBE G.I. 2 | 52 HOOT G.I. 2 | 62 RIGHT ORBIT CHASE 2 | 72 ROLLOVER "A" | 82 (ELECTRO) RAMP 2 |
| 13 START | 23 4-BANK G.I. 3 | 33 SPACESHIP G.I. 1 | 43 TUBE G.I. 3 | 53 HOOT G.I. 3 | 63 RIGHT ORBIT CHASE 3 | 73 ROLLOVER "R" | 83 (ELECTRO) RAMP 3 |
| 14 UNUSED | 24 L. SLINGSHOT G.I. 1 | 34 SPACESHIP G.I. 2 | 44 TUBE G.I. 4 | 54 HOOT G.I. 4 | 64 ALIEN LOCK LEFT | 74 TUBE SIGN X-BALL | 84 (ELECTRO) UNUSED |
| 15 UNUSED | 25 UNUSED | 35 R. SLINGSHOT G.I. 1 | 45 TUBE G.I. 5 | 55 ALIEN G.I. 1 | 65 ALIEN LOCK RIGHT | 75 TUBE SIGN 10 MILLION | 85 (ELECTRO) UNUSED |
| 16 UNUSED | 26 L. FLIPPER G.I. 1 | 36 R. SLINGSHOT G.I. 2 | 46 LEFT ORBIT CHASE 1 | 56 ALIEN G.I. 2 | 66 UNUSED | 76 TUBE SIGN JACKPOT | 86 **(ELECTRO) BLACK LIGHT** |
| 17 UNUSED | 27 UNUSED | 37 R. FLIPPER G.I. 1 | 47 LEFT ORBIT CHASE 2 | 57 ALIEN G.I. 3 | 67 UNUSED | 77 UNUSED | 87 (ELECTRO) UNUSED |
| 18 UNUSED | 28 UNUSED | 38 R. FLIPPER G.I. 2 | 48 LEFT ORBIT CHASE 3 | 58 CAPTIVE G.I. 1 | 68 UNUSED | 78 UNUSED | 88 (ELECTRO) UNUSED |

In the wiring grid, exactly two A-matrix lamp symbols carry an "X2" annotation,
both inside the dashed COIN DOOR / CABINET boundary:

- **"11 X2"** -- matrix A column 1, row 1 = public lamp address **1, Coin Door
  1&2 (#259, LP00113)**: two bulbs in parallel at one address.
- **"12 X2"** -- matrix A column 1, row 2 = public lamp address **2, Coin Door
  3&4 (#259, LP00113)**: two bulbs in parallel at one address.

Every other lamp symbol in the committed grid carries no X2 annotation. The
sheet's detail legend (drawn beside the grid) defines X2 as two #44-or-#555
bulbs wired in parallel between the column and row lines, each with its own
1N4004 diode. The companion matrix-B sheet (sheet 10 of 12) carries the same X2
annotation on exactly two playfield lamps -- "37 FREE SHOT (OUTLANE LEFT) X2"
(public lamp 87) and "85 DANCE FLOOR X2" (public lamp 125); its complete grid is
committed as the companion image of `lamp-matrix-b-x2-quantities.md`.

Sheet footer block: "Capcom Coin-Op, Inc. 3311 North Kennicott Avenue, Arlington
Heights, Illinois 60004 -- TITLE: DIAGRAM, LAMP MATRIX "A" WIRING -- PART NO.
PB-5 WIRING -- DRAWN B.ZIEGLER -- DATE 6/7/96 -- SHEET 9 OF 12".

Note: the printed operators-manual lamp table (printed page 81) prints no
quantity column, so these X2 marks are the only bulb-quantity evidence in the
retained document set.
