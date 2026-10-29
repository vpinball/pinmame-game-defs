# Bally Medusa game #1245 identification tables

Source: `Bally_1981_Medusa_Manual.pdf`, SHA-256
`6137807222d614505ac923df7acd24c091449cf45f1d4d383ab82939d0df6a7b`,
PDF page 17, printed page 17. Complete two tables, including blank rows.
Method: Windows.Media.Ocr search followed by primary curator visual transcription
against retained native `manual-render/page-17.png`. Transcribed/reviewed by GPT Sol.
Capitalization preserved; line wrapping normalized. A handwritten mark crosses the
shield-post row but does not replace its printed label. These solenoid numbers are
**Self Test numbers**, distinct from public addresses.

| Self Test # | SOLENOID IDENTIFICATION |
| --- | --- |
| 01 | KNOCKER |
| 02 | 4 DROP TARGET RESET |
| 03 | 7 DROP TARGET RESET |
| 04 | #2 TOP DROP TARGET |
| 05 | #4 TOP DROP TARGET |
| 06 | #6 TOP DROP TARGET |
| 07 | SHEILD OF THE GODS POST |
| 08 | OUTHOLE KICKER |
| 09 | BOTTOM LEFT THUMPER BUMPER |
| 10 | BOTTOM RIGHT THUMPER BUMPER |
| 11 | TOP LEFT THUMPER BUMPER |
| 12 | TOP RIGHT THUMPER BUMPER |
| 13 | LEFT SLINGSHOT |
| 14 | BOTTOM RIGHT SLINGSHOT |
| 15 | TOP RIGHT SLINGSHOT |
| 16 | OPEN MOVABLE FLIPPER |
| 17 | CLOSE MOVABLE FLIPPER |
| 18 | #1 TOP DROP TARGET FROM LEFT |
| 19 | #3 TOP DROP TARGET |
| 20 | #5 TOP DROP TARGET |
| 21 | #7 TOP DROP TARGET |
| 22 | SAUCER |
| 23 | COIN LOCKOUT DOOR |
| 24 | K1 RELAY (FLIPPER ENABLE) |

| Switch Self Test # | DESCRIPTION |
| --- | --- |
| 01 | 4 DROP TARGET D (BOTTOM) |
| 02 | 4 DROP TARGET C |
| 03 | 4 DROP TARGET B |
| 04 | 4 DROP TARGET A (TOP) |
| 05 | [blank] |
| 06 | CREDIT BUTTON |
| 07 | [blank] |
| 08 | OUTHOLE |
| 09 | COIN III (RIGHT) |
| 10 | COIN I (LEFT) |
| 11 | COIN II (MIDDLE) |
| 12 | LEFT SIDE TOP KICKER |
| 13 | LEFT SIDE MIDDLE TARGET |
| 14 | LEFT SIDE BOTTOM TARGET |
| 15 | TILT (3) |
| 16 | SLAM (2) |
| 17 | CABINET POST BUTTON |
| 18 | 2, 10 POINT & 4 DROP TARGET REBOUND |
| 19 | SAUCER |
| 20 | #1 SHOOTER LANE ROLLOVER BUTTON |
| 21 | #2 SHOOTER LANE ROLLOVER BUTTON |
| 22 | #3 SHOOTER LANE ROLLOVER BUTTON |
| 23 | #4 SHOOTER LANE ROLLOVER BUTTON |
| 24 | #5 SHOOTER LANE ROLLOVER BUTTON |
| 25 | RIGHT AND LEFT LOWER GATE |
| 26 | RIGHT TOP GATE |
| 27 | TOP RIGHT BACK TARGET |
| 28 | LEFT TOP GATE |
| 29 | TOP LEFT BACK TARGET |
| 30 | TOP MIDDLE BACK TARGET |
| 31 | LEFT & RIGHT OUTLANE R.O. BUTTON |
| 32 | LEFT & RIGHT OUTLANE |
| 33 | SPINNER |
| 34 | TOP RIGHT SLINGSHOT |
| 35 | BOTTOM RIGHT SLINGSHOT |
| 36 | LEFT SLINGSHOT |
| 37 | RIGHT TOP THUMPER BUMPER |
| 38 | LEFT TOP THUMPER BUMPER |
| 39 | RIGHT SIDE THUMPER BUMPER |
| 40 | LEFT BOTTOM THUMPER BUMPER |
| 41 | MOVABLE FLIPPER END OF STROKE |
| 42 | #7 TOP DROP TARGET (RIGHT) |
| 43 | #6 TOP DROP TARGET |
| 44 | #5 TOP DROP TARGET |
| 45 | #4 TOP DROP TARGET |
| 46 | #3 TOP DROP TARGET |
| 47 | #2 TOP DROP TARGET |
| 48 | #1 TOP DROP TARGET (LEFT) |

## Figure V, PDF page 18, printed 18

Circles identify switches; squares identify solenoids by the tables above.
Cabinet switches: 15, 16, 17. Door switches: 06, 09, 10, 11, 16.
Door solenoid: 23. Backbox solenoid: 24. Cabinet solenoid: 01.
The playfield drawing pairs bumper switch/solenoid positions: upper left 38/11,
upper right 37/12, bottom left 40/09, bottom right 39/10.
It draws switch 25 on each lower gate, 31 on each outlane star, 32 on each
outlane; switch 18 appears at three rebound locations. Switch 41 is drawn at
the movable flipper linkage, alongside spinner 33. The four flippers carry
square 24 because K1 enables them; 24 is not an individual flipper coil drive.

## Switch construction, schematics PDF page 2 (W-1187-31)

The game's own matrix draws normally open scoring/button contacts. Positions
5 and 7 carry asterisks (legend: NOT USED). Matrix 41 has the explicit annotation
`CLOSED WHEN MOVABLE FLIPPERS ARE OPEN`. Its mechanism position and startup
level are separate from the drawn normally open contact construction.
Return rows I0-I7: A4J2-8/54, -9/63, -10/57, -11/78, -12/60, -13/56,
-14/65, -15/52. Strobes ST0-ST4: A4J2-1/51, -2/70, -3/93, -4/53,
-5/31. ST5: A4J4-8/72. Wire codes are literal numeric codes, not inferred colors.
The matrix calls 12 `LEFT SIDE TOP TARGET`; Figure V and the parts drawing
show its target location. The identification table's word `KICKER` is retained
above and does not introduce an extra coil.
