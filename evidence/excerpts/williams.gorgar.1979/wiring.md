# Gorgar playfield and insert-board wiring

Williams Gorgar Schematic Diagrams, PDF pages 19–21, printed pages 15–17. The playfield switch sheet prints GRN-ORG where Figure 5 prints GRN-ORN. Columns 7 and 8 terminate at N/C on the playfield side.

| Switch drive column | Driver board 2J2/2P2 | Playfield 8P1/8J1 | Wire as drawn |
| --- | --- | --- | --- |
| 1 | 9 | — | GRN-BRN |
| 2 | 8 | 1 | GRN-RED |
| 3 | 7 | 2 | GRN-ORG |
| 4 | 6 | 3 | GRN-YEL |
| 5 | 5 | 4 | GRN-BLK |
| 6 | 3 | 5 | GRN-BLU |
| 7 | 2 | 6 (N/C) | GRN-VIO |
| 8 | 1 | 7 (N/C) | GRN-GRY |

| Switch return row | Driver board 2J3/2P3 | Playfield 8P1/8J1 | Wire as drawn |
| --- | --- | --- | --- |
| 1 | 9 | 8 | WHT-BRN |
| 2 | 8 | 9 | WHT-RED |
| 3 | 7 | 10 | WHT-ORG |
| 4 | 6 | 11 | WHT-YEL |
| 5 | 5 | 12 | WHT-GRN |
| 6 | 4 | 13 | WHT-BLU |
| 7 | 3 | 14 | WHT-VIO |
| 8 | 1 | 15 | WHT-GRY |

The switch diagram draws one open contact (8SW9–8SW44) in series with one diode (8D9–8D44), and names those switches in the same order as the booklet matrix. The coil sheet draws independent normally-open direct-drive contacts 8SW65–8SW69 for top, left and bottom jet and left and right kicker. The two windings and EOS on 8L24 (left) and 8L25 (right) are part of the cabinet-button circuit; the driver board's Z1 gates their ground.

The cabinet diagram routes Column 1 through 7P1-19 to 7SW1–7SW8. Its eight returns run through 7P1-21 through 7P1-28, in ordinal order. The cabinet shows three G.I. bulbs across 7J2-1/2. The power diagram feeds cabinet, playfield and insert-board G.I. from the same 6.3 VAC secondary.

| Lamp drive column | Driver board 2J5/2P5 | Playfield 8P2/8J2 | Insert 9J1 | Wire as drawn at 2J5 |
| --- | --- | --- | --- | --- |
| 1 | 8 | 3 | — | YEL-BRN |
| 2 | 9 | 4 | — | YEL-RED |
| 3 | 6 | 5 | — | YEL-ORG |
| 4 | 7 | 6 | — | YEL-BLK |
| 5 | 3 | 7 | — | YEL-GRN |
| 6 | 5 | 8 | — | YEL-BLU |
| 7 | 1 | 9 | 6 | YEL-VIO |
| 8 | — | — | 7 | — |

Figure 6 gives YEL-GRY for column 8. The playfield sheet has no 2J5 or 8P2 pin for this insert-only column.

| Lamp return row | Driver board 2J7/2P7 | Playfield 8P2/8J2 | Insert 9J1 | Wire as drawn at 2J7 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 11 | 8 | RED-BRN |
| 2 | 2 | 12 | 9 | RED-BLK |
| 3 | 3 | 13 | 10 | RED-ORG |
| 4 | 4 | 14 | 11 | RED-YEL |
| 5 | 5 | 15 | 12 | RED-GRN |
| 6 | 6 | 16 | 13 | RED-BLU |
| 7 | 9 | 17 | 14 | RED-VIO |
| 8 | 8 | 18 | 15 | RED-GRY |

The playfield lamp diagram has one lamp and series diode per used matrix entry in columns 1–6 and for 56 in column 7. The accompanying bulb list repeats Figure 6 for 01–49 and 56, except for minor wording and "When Lit" on Spinner. It names neither 50–55 nor 57–64 because they are on the insert board.

| Insert 9J1 | Labels as drawn | Bulbs per label in order |
| --- | --- | --- |
| 1, 2, 4, 5 | 6.3 VAC | Continuation |
| 3 | N.C. | — |
| 6 | LAMP COLUMN 7 | — |
| 7 | LAMP COLUMN 8 | — |
| 8 | PLAYER 1 UP | 1 |
| 9 | 1 CAN PLAY / PLAYER 2 UP | 1 / 1 |
| 10 | 2 CAN PLAY / PLAYER 3 UP | 1 / 1 |
| 11 | 3 CAN PLAY / PLAYER 4 UP | 1 / 1 |
| 12 | 4 CAN PLAY / TILT | 1 / 1 |
| 13 | MATCH / GAME OVER | 1 / 2 |
| 14 | BALL IN PLAY / SAME PLAYER SHOOTS | 1 / 2 |
| 15 | HIGH SCORE | 2 |

The playfield solenoid sheet draws the independent loads 8L5 MAGNET RELAY and 8B65/8B66 MAGNET LAMPS (two TYPE 89 bulbs). The relay contact switches ground on separate magnet 8L27 through fuse 8F1 (8A). The playfield 6.3 VAC G.I. enters at pins 1 (YEL) and 2 (YEL-WHT) of 8P2/8J2. The playfield and insert G.I. drawings show continuation branches, so the drawn representative lamps do not establish socket counts.
