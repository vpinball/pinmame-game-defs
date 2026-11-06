# Xenon matrix, coils and GI

PDF48 W-1192-24c: complete five-column/eight-row playfield matrix. Blanks are printed unwired cells; cabin contacts live on W-1186-9c. Source cell labels normalized to the Figure V names, not completed from another game.

| Row / A4J2 return pin / wire | ST0 pin1 wire51 | ST1 pin2 wire70 | ST2 pin3 wire93 | ST3 pin4 wire53 | ST4 pin5 wire31 |
| --- | --- | --- | --- | --- | --- |
| I0 / 8 / 54 | 01: END OF TUBE LANE | 09: [BLANK] | 17: #4 BUTTON | 25: SHOOTER LANE | 33: SIDE SAUCER |
| I1 / 9 / 63 | 02: BALL RELEASE #1 | 10: [BLANK] | 18: #3 BUTTON | 26: 30 POINT REBOUND (2) | 34: TOP SAUCER |
| I2 / 10 / 57 | 03: UPPER SIDE TARGET | 11: [BLANK] | 19: #2 BUTTON | 27: TUBE SWITCH | 35: RIGHT SLINGSHOT |
| I3 / 11 / 78 | 04: LOWER SIDE TARGET | 12: [BLANK] | 20: #1 BUTTON | 28: BALL RELEASE #2 | 36: LEFT SLINGSHOT |
| I4 / 12 / 15 | 05: SPINNER | 13: [BLANK] | 21: #4 DROP TARGET | 29: LEFT OUTLANE | 37: LOWER THUMPER BUMPER |
| I5 / 13 / 56 | 06: [BLANK] | 14: [BLANK] | 22: #3 DROP TARGET | 30: FLIP FEED LANE (LEFT) | 38: MIDDLE THUMPER BUMPER |
| I6 / 14 / 65 | 07: TILT (3) | 15: [BLANK] | 23: #2 DROP TARGET | 31: FLIP FEED LANE (RIGHT) | 39: RIGHT THUMPER BUMPER |
| I7 / 15 / 52 | 08: OUTHOLE | 16: [BLANK] | 24: #1 DROP TARGET | 32: RIGHT OUTLANE | 40: LEFT THUMPER BUMPER |

All matrix contact symbols are normally open. The cabinet sheet names PLUMB BOB and ROLL CAGE at I6/ST0, SLAM at I7/ST1. Figure V gives three tilt contacts and two slam contacts. Flipper buttons are power contacts supplied from A2J2-2, separate from the CPU matrix; their two coils have EOS contacts.

PDF24 printed20 complete ASSEMBLY COILS region:

| Description | Part number |
| --- | --- |
| Coin Lockout | FO-36-7000 |
| Flipper (2) | AQ-25-500/34-4500 |
| Knocker | AR-26-1200 |
| Outhole Kicker | AN-26-1200 |
| Thumper-Bumper (4) | AN-26-1200 |
| Sling-Shot (2) | AN-26-1200 |
| Drop Target Reset | NO-26-1900 |
| Individual Drop Targets (4) | CJ-31-2000 |
| Saucer (2) | AO-27-1300 |
| Ball Release | AO-27-1300 |

PDF54 complete A3J1/J2/J5 output connector regions:

| Connector pin | Wire | Function |
| --- | --- | --- |
| A3J1-1 | [blank] | N/U |
| A3J1-2 | 18 | *1 DROP TAR. |
| A3J1-3 | 67 | 4 D.T. RESET |
| A3J1-4 | [blank] | N/U |
| A3J1-5 | 95 | OUTHOLE |
| A3J1-6 | [blank] | N/U |
| A3J1-7 | [blank] | KEY |
| A3J1-8 | 40 | L FLIP COIL |
| A3J1-9 | 70 | R FLIP COIL |
| A3J2-1 | 10 | R FLIP SW. |
| A3J2-2 | 20 | L FLIP SW. |
| A3J2-3 | [blank] | KEY |
| A3J2-4 | [blank] | N/U |
| A3J2-5 | 85 | KNOCKER |
| A3J2-6 | [blank] | NOTE1. |
| A3J2-7 | 31 | TEST SW. RET. |
| A3J2-8 | 36 | COIN LOCKOUT |
| A3J2-9 | 58 | N/U |
| A3J2-10 | 81 | *2 DROP TAR. |
| A3J2-11 | 80 | *3 DROP TAR. |
| A3J2-12 | 75 | *4 DROP TAR. |
| A3J2-13 | [blank] | [blank] |
| A3J2-14 | [blank] | [blank] |
| A3J2-15 | [blank] | [blank] |
| A3J5-1 | [blank] | N/U |
| A3J5-2 | [blank] | N/U |
| A3J5-3 | [blank] | N/U |
| A3J5-4 | [blank] | N/U |
| A3J5-5 | [blank] | N/U |
| A3J5-6 | [blank] | KEY |
| A3J5-7 | 81 | TOP SAUCER |
| A3J5-8 | 18 | RIGHT SLINGSHOT |
| A3J5-9 | 71 | RIGHT THUMPER BUMPER |
| A3J5-10 | 85 | BALL RELEASE |
| A3J5-11 | 78 | LEFT THUMPER BUMPER |
| A3J5-12 | 80 | SIDE SAUCER |
| A3J5-13 | 67 | LOWER THUMPER BUMPER |
| A3J5-14 | 83 | LEFT SLINGSHOT |
| A3J5-15 | 74 | MIDDLE THUMPER BUMPER |

W-1192-24c prints #1 target/reset at A3J2-2/3 and outhole at A3J5-5. W-1183-28c and W-1187-24c agree on A3J1-2/3/5, and J5-5 is N/U. This is a settled wiring-detail note. K1 is internal on A3, driven by Q15/PB6; Q17/PB4 drives top saucer17; Q19/PB5 drives coin lockout18; Q18/PB7 ends at A3J2-15 N/U. The relay coil is not NOTE1 at A3J2-6.

Bare AC GI: W-1192-24c buses10 A2J1-4 /70 A2J1-1, returns40 A2J1-6 /50 A2J1-3; generic lamp symbol, no count. W-1187-24c insert GI pairs A2J4-8/1 (10/50) and A2J4-9/4 (70/40). W-1186-9c cabinet GI bus A2J2-6 wire38. No CPU/lamp-driver branch.
