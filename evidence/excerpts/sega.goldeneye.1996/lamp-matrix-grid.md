# Sega GoldenEye (1996) — Lamp Matrix Grid

Source: Sega Pinball *GoldenEye* operations manual (`Sega_1996_Goldeneye_Manual.pdf`), PDF page 5,
Find-It-In-Front: Dr. Pinball page iii, table **LAMP MATRIX GRID**. Read from the native 300 dpi render.
Every populated cell prints `#44 Bulb`; the lamp number is printed in the cell's black box.

## Column header (18v drive)

| Column | Driver | Wire | Connector |
| --- | --- | --- | --- |
| 1 | U10 | YEL-BRN | J13-1 |
| 2 | U11 | YEL-RED | J13-3 |
| 3 | U12 | YEL-ORG | J13-4 |
| 4 | U13 | YEL-BLK | J13-5 |
| 5 | U14 | YEL-GRN | J13-6 |
| 6 | U15 | YEL-BLU | J13-7 |
| 7 | U16 | YEL-VIO | J13-8 |
| 8 | U17 | YEL-GRY | J13-9 |

## Row header (GND)

| Row | Transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q33 | RED-BRN | J12-1 |
| 2 | Q34 | RED-BLK | J12-2 |
| 3 | Q35 | RED-ORG | J12-3 |
| 4 | Q36 | RED-YEL | J12-4 |
| 5 | Q37 | RED-GRN | J12-5 |
| 6 | Q38 | RED-BLU | J12-6 |
| 7 | Q39 | RED-VIO | J12-8 |
| 8 | Q40 | RED-GRY | J12-9 |
| 9 | Q41 | RED-WHT | J12-10 |
| 10 | Q42 | RED | J12-11 |

## Cells

| No. | Printed text | No. | Printed text |
| --- | --- | --- | --- |
| 1 | MILITARY INTEL-LIGENCE HQ | 41 | RIGHT TURBO BUMPER |
| 2 | EJECT HURRY-UP | 42 | SCOOP ARROW |
| 3 | ELECTRO MAG-NETIC PULSE | 43 | LEFT RAMP ARROW |
| 4 | SEVERNAYA STATION | 44 | NARROW ESCAPE |
| 5 | TANK CHASE | 45 | LT. 5-BANK MID-TOP |
| 6 | PETYA STATION | 46 | LT. 5-BANK MIDDLE |
| 7 | CAT AND MOUSE | 47 | LT. 5-BANK MID-BOT |
| 8 | NERVE GAS | 48 | LT. 5-BANK BOTTOM |
| 9 | NOT USED (shaded, no bulb) | 49 | HELICOPTER |
| 10 | RIGHT OUTLANE | 50 | CENTER RAMP ENTER LEFT |
| 11 | RIGHT RE-TURN LANE | 51 | CENTER RAMP ENTER RIGHT |
| 12 | LEFT RE-TURN LANE | 52 | RT. 5-BANK BOTTOM |
| 13 | SHOOT AGAIN | 53 | RT. 5-BANK MID-BOT |
| 14 | JUMP RAMP | 54 | RT. 5-BANK MIDDLE |
| 15 | GOLDENEYE | 55 | RT. 5-BANK MID-TOP |
| 16 | MISCHA SATELLITE | 56 | RT. 5-BANK TOP |
| 17 | SCOOP BOTTOM | 57 | START BUTTON |
| 18 | SCOOP TOP | 58 | BEHIND EJECT S-U |
| 19 | LEF TURBO BUMPER | 59 | ABOVE EJECT S-U |
| 20 | RIGHT RAMP ARROW | 60 | LOCK 1 |
| 21 | RIGHT RAMP TOP | 61 | LOCK 2 |
| 22 | RIGHT RAMP BOTTOM | 62 | RIGHT FIRE MISSILE |
| 23 | 2-BANK BOTTOM | 63 | LEFT FIRE MISSILE |
| 24 | 2-BANK TOP | 64 | NOT USED (shaded, no bulb) |
| 25 | LEFT STAND-UP LEFT | 65 | 100 MILLION |
| 26 | LEFT STAND-UP RIGHT | 66 | 75 MILLION |
| 27 | BOT. TURBO BUMPER | 67 | 50 MILLION |
| 28 | EJECT BOTTOM | 68 | 25 MILLION |
| 29 | EJECT TOP | 69 | HELICOPTER SPOTLITE |
| 30 | LEFT TOP LANE | 70 | NOT USED (shaded, no bulb) |
| 31 | MIDDLE TOP LANE | 71 | NOT USED (shaded, no bulb) |
| 32 | RIGHT TOP LANE | 72 | GOLDEN-EY( E ) |
| 33 | LEFT OUTLANE | 73 | ( G )OLDEN-EYE |
| 34 | RIGHT RAMP ENTER | 74 | G( O )LDEN-EYE |
| 35 | LEFT RAMP | 75 | GO( L )DEN-EYE |
| 36 | LEFT RAMP TOP | 76 | GOL( D )EN-EYE |
| 37 | MID. RAMP BOTTOM | 77 | GOLD( E )N-EYE |
| 38 | MID. RAMP TOP | 78 | GOLDE( N )-EYE |
| 39 | UNDER RAMP TOP | 79 | GOLDEN-( E )YE |
| 40 | UNDER RAMP BOT. | 80 | GOLDEN-E( Y )E |

Numbering is row-major: lamp = (row - 1) x 8 + column. Rows 9 and 10 are the two extra rows beyond
the standard eight. Cell 19 is printed `LEF TURBO BUMPER` as shown.
