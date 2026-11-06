# Skateball — switch and solenoid connector lists

Bally Game #1210, PLUG CONNECTORS sheet W-1187-23C, schematic PDF page 9, SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`. Transcribed from the 300 dpi render by a curation worker; **visually reviewed against the retained native-resolution render by the primary curator**. This excerpt covers complete A4J2, A4J3 and A3J1/J2/J5 lists, not the other connector blocks on the sheet. Wire codes are source literal; `—` marks a missing printed code, `N/U`, `KEY` and `NOTE 1` are printed. Note 1 says those pins are reserved for future use; note 2 says wire colors are shown for all connector pins, some wires may not be used in all games.

| Pin | A4J2 wire | A4J2 TO | A4J3 wire | A4J3 TO |
|---:|---:|---|---:|---|
| 1 | 51 | ST 0 | 10 | SELF TEST SW. |
| 2 | 70 | ST 1 | 13 | ST 0 |
| 3 | 93 | ST 2 | 14 | ST 1 |
| 4 | 53 | ST 3 | — | KEY |
| 5 | 31 | ST 4 | — | N/U |
| 6 | — | KEY | — | N/U |
| 7 | — | N/U | — | N/U |
| 8 | 54 | I 0 | — | N/U |
| 9 | 63 | I 1 | 15 | I 0 |
| 10 | 57 | I 2 | 65 | I 1 |
| 11 | 78 | I 3 | 20 | I 2 |
| 12 | 60 | I 4 | 21 | I 3 |
| 13 | 56 | I 5 | 23 | I 4 |
| 14 | 65 | I 6 | 25 | I 5 |
| 15 | 52 | I 7 | 27 | I 6 |
| 16 | [not printed] | [no row] | 30 | I 7 |

The diagram groups A4J2 ST 0–4 as PLAYFIELD SW STROBE, I 0–7 as PLAYFIELD SW RETURN; A4J3 ST 0–1 as SW. CAB. STROBE and I 0–7 as CAB. SW. RET.

| Pin | A3J1 wire | A3J1 TO | A3J2 wire | A3J2 TO | A3J5 wire | A3J5 TO |
|---:|---:|---|---:|---|---:|---|
| 1 | — | N/U | 10 | R. FLIP. SW. | — | N/U |
| 2 | 67 | SAUCER | 20 | L. FLIP. SW. | — | N/U |
| 3 | — | N/U | — | KEY | — | N/U |
| 4 | — | N/U | — | N/U | — | N/U |
| 5 | 95 | OUTHOLE | 85 | KNOCKER | — | N/U |
| 6 | — | N/U | — | NOTE 1 | — | KEY |
| 7 | — | KEY | 31 | TEST SW. RET. | 81 | N/U |
| 8 | 40 | L. FLIP COIL | 36 | COIN LOCKOUT | 18 | RIGHT SLINGSHOT |
| 9 | 70 | R. FLIP COIL | 58 | N/U | 71 | LEFT THUMPER BUMPER |
| 10 | [not printed] | [no row] | 57 | N/U | 85 | 5 DROP TARGET |
| 11 | [not printed] | [no row] | 56 | N/U | 78 | 3 DROP TARGET (MIDDLE) |
| 12 | [not printed] | [no row] | 54 | N/U | 80 | 3 DROP TARGET (TOP) |
| 13 | [not printed] | [no row] | — | [blank] | 67 | RIGHT THUMPER BUMPER |
| 14 | [not printed] | [no row] | — | [blank] | 83 | LEFT SLINGSHOT |
| 15 | [not printed] | [no row] | — | [blank] | 74 | BOTTOM THUMPER BUMPER |
