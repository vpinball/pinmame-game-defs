# World Cup Soccer — Lamp Matrix (wiring)

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF page 110, printed page 2-44, the `LAMP MATRIX`
table. The whole eight-by-eight block is transcribed. Footer: `J1XX = Power Driver Board`.

## Matrix drive columns

| Column | Wire | Connector | Driver |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J138-1 | Q98 |
| 2 | Yellow-Red | J138-2 | Q97 |
| 3 | Yellow-Orange | J138-3 | Q96 |
| 4 | Yellow-Black | J138-4 | Q95 |
| 5 | Yellow-Green | J138-5 | Q94 |
| 6 | Yellow-Blue | J138-6 | Q93 |
| 7 | Yellow-Violet | J138-7 | Q92 |
| 8 | Yellow-Gray | J137-9 | Q91 |

## Matrix return rows

| Row | Wire | Connector | Driver |
| --- | --- | --- | --- |
| 1 | Red-Brown | J135-1 | Q90 |
| 2 | Red-Black | J135-2 | Q89 |
| 3 | Red-Orange | J135-4 | Q88 |
| 4 | Red-Yellow | J135-5 | Q87 |
| 5 | Red-Green | J135-6 | Q86 |
| 6 | Red-Blue | J134-7 / J135-7 | Q85 |
| 7 | Red-Violet | J134-8 / J135-8 | Q84 |
| 8 | Red-Gray | J134-9 / J135-9 | Q83 |

## The 8x8 grid (public address = column*10 + row)

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Chicago "P" (11) | 1 Goal (21) | Free Kick (31) | Kickback Lower (41) | Goal Jackpot (51) | Left Ramp Build Lock (61) | Light Jackpot (2) (71) | Rollover 1 (High) (81) |
| 2 | Dallas "U" (12) | 2 Goals (22) | TV Award (32) | Kickback Center (42) | Extra Ball (52) | Spinner Build Lock (62) | Final Draw (72) | Rollover 2 (82) |
| 3 | Boston "C" (13) | 3 Goals (23) | Ultra Goalie (33) | Kickback Upper (43) | Goal (2) (53) | Travel (63) | Magna-Goal Save (73) | Rollover 3 (83) |
| 4 | New York "D" (14) | 4 Goals Light TV (24) | Ultra Ramps (34) | Right Ramp Build Lock (44) | Upper Build Lock (54) | Los Angeles (64) | Left Flipper Lane (74) | Rollover 4 (Low) (84) |
| 5 | Orlando "L" (15) | Speed (Ball) (25) | Spirit (Ball) (35) | Right Ramp Lock (45) | Light Magna Goalie (55) | Left Ramp Lock (65) | Light Kickback (75) | Skill Shot Rear (85) |
| 6 | Washington D.C. "R" (16) | Strength (Ball) (26) | Skill (Ball) (36) | Ultra Spinner (2) (46) | Right Flipper Lane (56) | Upper Left Lane (66) | Left Ramp Buy Ticket (76) | Skill Shot Center (86) |
| 7 | San Francisco "O" (17) | Stamina (Ball) (27) | Right Ticket Half (37) | Ultra Jets (2) (47) | Shoot Again (57) | Upper Right Lane (67) | Right Ramp Buy Ticket (77) | Buy-in Button (87) |
| 8 | Detroit "W" (18) | Left Ticket Half (28) | Tackle (38) | Striker Billboard (48) | Right Special (58) | Skill Shot Front (68) | Ultra Ramps (2) (78) | Start Button (88) |

All 64 matrix positions carry a printed label; none is marked "Not Used" on this page.
