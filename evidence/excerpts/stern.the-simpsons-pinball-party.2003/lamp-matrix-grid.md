# The Simpsons Pinball Party — Lamp Matrix Grid (wiring)

Transcribed from `The_Simpsons_Manual.pdf`, PDF page 36, printed page 22,
table "LAMP MATRIX GRID". `method: mixed` (page located via the printed
footer in the OCR text layer; every cell read from a 150 dpi render). Eight
drive columns by ten return rows, addressed row-major (row 1 = public 1-8,
row 2 = 9-16, ... row 10 = 73-80), confirmed directly against the printed
page's own numbering. The complete 80-position grid is transcribed.

Column (drive, 18V) wiring: `1` YEL-BRN/J13-P9/U17, `2` YEL-RED/J13-P8/U16,
`3` YEL-ORG/J13-P7/U15, `4` YEL-BLK/J13-P6/U14, `5` YEL-GRN/J13-P5/U13, `6`
YEL-BLU/J13-P4/U12, `7` YEL-VIO/J13-P3/U11, `8` YEL-GRY/J13-P1/U10.

Row (return/ground) wiring: `1` RED-BRN/J12-P1/Q33, `2` RED-BLK/J12-P2/Q34,
`3` RED-ORG/J12-P3/Q35, `4` RED-YEL/J12-P4/Q36, `5` RED-GRN/J12-P5/Q37, `6`
RED-BLU/J12-P6/Q38, `7` RED-VIO/J12-P8/Q39, `8` RED-GRY/J12-P9/Q40, `9`
RED-WHT/J12-P10/Q41, `10` RED/J12-P11/Q42.

`[DOTS]` marks a cell also marked "Diode On Terminal Strip".

| Row | Col1 | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 #555 LEFT OUT EXTRA BALL | 2 #555 LEFT RETURN EXTRA BALL | 3 #555 SHOOT AGAIN | 4 #555 RIGHT RETURN EXTRA BALL | 5 #555 SPECIAL | 6 #555 SHOOTER LANE SKILL SHOT | 7 #555 LIGHT OTTO | 8 #555 ADV. POPS |
| 2 | 9 #555 SPAY ANYTHING | 10 #555 KITTY KITTY BANG BANG | 11 #555 FIELD OF SCREAMS | 12 #555 ESOPHAGUS NOW | 13 #555 I&S ARROW | 14 #555 START I&S MULTIBALL | 15 #555 I&S 2X SCORING | 16 #44(x2) POPS 2X SCORING |
| 3 | 17 #555 LEFT POP BUMPER [DOTS] | 18 #555 RIGHT POP BUMPER [DOTS] | 19 #555 BOTTOM POP BUMPER [DOTS] | 20 #555 MORE TIME | 21 #555 COLLECT NUCLEAR PLANT | 22 #555 LEFT ORBIT ARROW | 23 #555 CLETUS 2X SCORING | 24 #555 LEFT ORBIT HURRY UP |
| 4 | 25 #555 CBG SKILL SHOT | 26 #555 CBG START HURRY UP | 27 #555 DAREDEVIL RAMPS | 28 #555 DAREDEVIL BUMPERS | 29 #555 DAREDEVIL LOOPS | 30 #555 DAREDEVIL TARGETS | 31 #555 START BUTTON [DOTS] | 32 #555 TOURNAMENT BUTTON [DOTS] |
| 5 | 33 #555 LEFT RAMP ARROW | 34 #555 TREEHOUSE OF HORROR | 35 #555 TREEHOUSE 2X SCORING | 36 #555 LEFT RAMP HURRY UP | 37 #555 RIGHT RAMP ARROW | 38 #555 GET DUFFED! | 39 #555 MOE'S 2X SCORING | 40 #555 RIGHT RAMP HURRY UP |
| 6 | 41 #555 MINI LOOP ARROW | 42 #555 2X SCORING KWIK-E-MART | 43 #555 KWIK-E-MART HURRY UP | 44 #555 GARAGE ARROW | 45 #555 CLEAN THE GARAGE | 46 #555 GARAGE 2X SCORING | 47 #555 GARAGE HURRY UP | 48 #555 RIGHT ORBIT ARROW |
| 7 | 49 #555 RIGHT LOOP ARROW | 50 #555 OTTO'S BUS TOURS | 51 #555 ELEMENTARY 2X SCORING | 52 #555 BULLY 3-BANK (TOP) | 53 #555 BULLY 3-BANK (MID) | 54 #555 BULLY 3-BANK (BOT) | 55 #555 KRUSTY 2X SCORING | 56 #555 RIGHT ORBIT HURRY UP |
| 8 | 57 #555 HOMER | 58 #555 MARGE | 59 #555 BART | 60 #555 LISA | 61 #555 MAGGIE | 62 #555 GRANDPA | 63 #44 LEFT HEADLIGHT | 64 #44 RIGHT HEADLIGHT |
| 9 | 65 #555 LIVING ROOM 2X SCORING [DOTS] | 66 #555 (LIGHT) LOCK [DOTS] | 67 #555 LIGHT (LOCK) [DOTS] | 68 #555 LOCK (SQUARE) [DOTS] | 69 #555 SUPER JACKPOT [DOTS] | 70 #555 TV ARROW | 71 NOT USED | 72 NOT USED |
| 10 | 73 Green LED (LED) DUFFMAN | 74 Green LED (LED) HOMER'S DAY | 75 Green LED (LED) WILLIE'S WOES | 76 Green LED (LED) WIGGUM VS SNAKE | 77 Green LED (LED) BART'S DAY | 78 Green LED (LED) KRUSTY'S LAST STAND | 79 Green LED (LED) STOP THE MONORAIL | 80 Red LED(x2) (LED) ALIEN INVASION |

## Lamp Matrix Grid Locations (PDF page 37, printed page 23) — legend and footnotes

Same mounting-location legend as the coil/switch pages: `[white]` = above
playfield, `[black]` = below playfield, `[gray]` = in cabinet. Lamps 73-80
are drawn stacked at the top of the diagram labelled "on Sign" (the Mini-DMD
sign panel), matching their construction note below.

> **Lamp Part Note:** #555 Bulb Clear = 165-5002-00. #44 Bulb Clear =
> 165-5000-44. See Section 4, Chapter 1, Parts Id. & Location, Pages 72-74 for
> more details on bulbs and corresponding sockets.
>
> **Lamp Part Note:** For Green or Red LEDs are attached to LED PC Bd.,
> 520-5219-00. See Section 5, Chapter 4, Printed Circuit Boards (PCBs), Page
> 143.
>
> **Some Lamp Diodes are located under the playfield** on Terminal Strips or
> Diode Boards and not on the assemblies.
>
> DOTS: Diode On Terminal Strip *or* DODB: Diode On Diode Board (only if
> noted in the Matrix Grid).
>
> **Lamp 31, Start Button:** DOTS (2-Lug) in Cabinet under Button (RED-YEL /
> ORG-YEL to YEL-VIO).
>
> **Lamp 32, Tournament Button** (Optional with Tournament Kit, Diode in
> Connector).

The "LED PC Bd., 520-5219-00" part number is the exact board pinned PinMAME's
`segames.c` declares for this driver
(`SE_BOARDID_520_5219_00 // The Simpson's Pinball Party Mini DMD`), confirming
lamps 73-80 are physically the eight LEDs on the Mini-DMD sign board, not
eight independent playfield bulb positions — consistent with the retained VPX
table modelling them as one stacked panel object rather than eight distinct
locations (see `vpx-geometry.txt`). Lamp 32 (Tournament Button) is confirmed
optional, gated behind the same Tournament Kit as switch 53.
