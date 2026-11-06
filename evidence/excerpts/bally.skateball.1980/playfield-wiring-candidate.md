# Skateball — playfield wiring

Source: Bally Game #1210, sheet W-1192-23C, PDF page 10 of the IPDB schematic set, SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`. Transcribed from the 300 dpi page by a curation worker; **visually reviewed against the retained native-resolution render by the primary curator**. Entries are the entire printed lamp wiring list on the sheet, in source order. Wire is the printed numerical color code. Each row is drawn to the shared lamp bus. N/U is literally printed and the note says N/U means not used on playfield; do not infer load solely from a drawn bulb symbol.

| Wire | Connector | Label |
|---:|---|---|
| 58 | A5J1-18 | 1K BONUS |
| 60 | A5J1-19 | 5K BONUS |
| 57 | A5J1-17 | 9K BONUS |
| 12 | A5J1-23 | E DROP TARGET |
| 54 | A5J1-14 | S DROP TARGET |
| 13 | A5J1-15 | 2X BONUS |
| 90 | A5J1-16 | 20K SAUCER |
| 78 | A5J1-28 | SAUCER COLLECT BONUS |
| 50 | A5J1-24 | 1-2-3 SPECIAL |
| 75 | A5J1-25 | TOP RT. D.T. ARROW |
| 91 | A5J1-26 | N/U |
| 53 | A5J1-27 | RIGHT OUT SPECIAL |
| 41 | A5J1-1 | 2K BONUS |
| 43 | A5J1-9 | 6K BONUS |
| 51 | A5J1-8 | 10K BONUS |
| 45 | A5J1-3 | T DROP TARGET |
| 52 | A5J1-2 | B LANE |
| 23 | A5J1-10 | 3X BONUS |
| 34 | A5J1-7 | 30K SAUCER |
| 25 | A5J1-6 | #3 LANE |
| 48 | A5J1-5 | RT. THUMPER BUMPER |
| 65 | A5J1-11 | TOP CENTER D.T. ARROW |
| 35 | A5J1-4 | N/U |
| 61 | A5J1-12 | LOWER ROLLOVER BUTTON |
| 96 | A5J1-13 | #2 LANE |
| 43 | A5J3-26 | 3K BONUS |
| 36 | A5J3-25 | 7K BONUS |
| 67 | A5J3-19 | 20K BONUS |
| 13 | A5J3-17 | A DROP TARGET |
| 25 | A5J3-16 | A LANE |
| 98 | A5J3-23 | 4X BONUS |
| 40 | A5J3-27 | 50K SAUCER |
| 30 | A5J3-21 | BOTTOM THUMPER BUMPER |
| 64 | A5J3-20 | TOP LEFT D.T. ARROW |
| 23 | A5J3-22 | SAME PLAYER S.A. |
| 72 | A5J3-24 | UPPER ROLLOVER BUTTON |
| 10 | A5J3-1 | 4K BONUS |
| 21 | A5J3-12 | 8K BONUS |
| 53 | A5J3-15 | 40K BONUS |
| 20 | A5J3-11 | K DROP TARGET |
| 15 | A5J3-9 | 60K BONUS |
| 35 | A5J3-13 | CREDIT INDICATOR |
| 14 | A5J3-4 | SAUCER X-BALL |
| 95 | A5J3-2 | #1 LANE |
| 91 | A5J3-10 | LEFT THUMPER BUMPER |
| 56 | A5J3-18 | SPOTS X |
| 81 | A5J3-3 | 5X BONUS |
| 84 | A5J3-14 | 1K SPINNER |
| 20 | A2J1-7 | FEATURE LAMP BUS |

The separately routed group is also drawn inside PLAYFIELD A6, with a shared feature-lamp bus and an arrow to W-1187-23:

| Wire | Connector | Label |
|---:|---|---|
| 60 | A5J2-1 | 20K LEFT ARROW (MIDDLE D.T.) |
| 20 | A5J2-2 | 10K RIGHT (MIDDLE D.T.) |
| 12 | A5J2-14 | BONUS SPECIAL |
| 23 | A5J2-15 | 20K RIGHT ARROW (MIDDLE D.T.) |
| 34 | A5J2-16 | LEFT OUT SPECIAL |
| 98 | A5J2-20 | 10K CENTER (MIDDLE D.T.) |
| 85 | A5J2-6 | 100K (MIDDLE D.T.) |
| 91 | A5J2-7 | 10K LEFT (MIDDLE D.T.) |

The general illumination symbol is explicitly drawn on the playfield sheet and connected to A2J1-5 wire 70 (5.9 VAC) and A2J1-1 wire 50 (RET.). Other nearby unused branches show A2J1-8 wire 10 and A2J1-2 wire 40. This symbolic drawing does not enumerate physical lamp quantities or positions.
