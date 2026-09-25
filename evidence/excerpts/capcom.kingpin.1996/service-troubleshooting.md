# Transcription: Kingpin C5 TROUBLESHOOTING (ROM service menu)

Source: the kpb105 ROM's own service menu, walked by `tools/harness-scenarios/capcom/kpb105-troubleshooting-baseline.json`, `kpb105-troubleshooting-held.json` and `kpb105-troubleshooting-slam-tilt.json`, each on fresh isolated state with pinned LibPinMAME (`pinmame64.dll`, SHA-256 `ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d`, built from vpinball/pinmame `8371478a7640f1896dcdf565aed340dc5df989ba`) and ROM archive SHA-256 `fb64bcbc1dcd361ccc888cc235dde089e17907eac880af4cdfc3c7812269c0c5`. Raw run SHA-256s: baseline `ec0014d1d3df20008d50e2264fbed5a51125ea1c3fdb837817a0250dc5c6dbc4`, held `44c0afc0c775e5ba48b9bd62c020d9310a831db1ed851775ce579df1b36fe33c`, slam-tilt `1470b4ff364917d704d1fb0241818802fcccaf020acf5c9f15e14c57cfe1ea04` (retained externally as `review-artifacts/kingpin/harness-runs/final-troubleshooting-<run>/run.json` with every DMD frame).

The three runs differ only in the switches held at public 1 from power-up. The menu is opened with the coin door switch 8 and walked with the flipper buttons (public 84/82) and Start (7), so those inputs are never among the held switches. After C5 TROUBLESHOOTING opens on its summary screen, the right flipper steps through its messages until the summary comes round again. Message text is decoded from the 128x32 DMD frames by exact bitmap matching against the ROM's fonts and was checked by eye; the summary lines were read by eye. The companion image is a contact sheet of each run's summary and message frames, run by run.

## Run `baseline`

Held at public 1 from power-up: 36-39, 47. Every other switch rests at 0. Summary screen: `ERR: 0-SW 0-SOL 0-LP 0-GAME`, `INFO: 0-SW 0-SOL 3-LP 0-GAME`.

| Page | Switch | ROM name | Switch wire / pin | Return wire / pin |
| --- | --- | --- | --- | --- |
| 1 | lamp | 83B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW3-M3B J4/5.4 ORG-BLK |
| 2 | lamp | 84B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW4-M4B J4/5.5 ORG-YEL |
| 3 | lamp | 85B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW5-M5B J4/5.6 ORG-GRN |

## Run `held`

Held at public 1 from power-up: 1-4, 13-39, 41-46, 48-55, 57-63. Every other switch rests at 0. Summary screen: `ERR: 0-SW 0-SOL 0-LP 0-GAME`, `INFO: 28-SW 0-SOL 3-LP 0-GAME`.

| Page | Switch | ROM name | Switch wire / pin | Return wire / pin |
| --- | --- | --- | --- | --- |
| 1 | 01 | COIN 1 | GRN-BRN J9.1 | BLK-GRN J9.10 |
| 2 | 02 | COIN 2 | GRN-RED J9.2 | BLK-GRN J9.10 |
| 3 | 03 | COIN 3 | GRN-ORG J9.3 | BLK-GRN J9.10 |
| 4 | 04 | COIN 4 | GRN-YEL J9.4 | BLK-GRN J9.10 |
| 5 | 14 | AUTO PLUNGER | WHT-BLU J7.7 | BLK-WHT J7.10 |
| 6 | 19 | L. RETURN | BRN-ORG J1.3 | BLK-BRN J1.10 |
| 7 | 20 | R. RETURN | BRN-YEL J1.4 | BLK-BRN J1.10 |
| 8 | 21 | L. OUTLANE | BRN-GRN J1.5 | BLK-BRN J1.10 |
| 9 | 22 | R. OUTLANE | BRN-BLU J1.6 | BLK-BRN J1.10 |
| 10 | 23 | LEFT ORBIT | BRN-VIO J1.7 | BLK-BRN J1.10 |
| 11 | 24 | RIGHT ORBIT | BRN-GRY J1.9 | BLK-BRN J1.10 |
| 12 | 32 | CAPTIVE BALL | RED-GRY J2.9 | BLK-RED J2.10 |
| 13 | 33 | EOS L | ORG-BRN J3.1 | BLK-ORG J3.10 |
| 14 | 34 | EOS R | ORG-RED J3.2 | BLK-ORG J3.10 |
| 15 | 41 | L. SLING | YEL-BRN J4.1 | BLK-YEL J4.10 |
| 16 | 42 | R. SLING | YEL-RED J4.2 | BLK-YEL J4.10 |
| 17 | 47 | RAMP, DOWN | YEL-VIO J4.8 | BLK-YEL J4.10 |
| 18 | 49 | L. SLOT STANDUP | GRN-BRN J5.1 | BLK-GRN J5.10 |
| 19 | 50 | R. SLOT STANDUP | GRN-RED J5.2 | BLK-GRN J5.10 |
| 20 | 53 | L. TOPLANE | GRN-BLK J5.5 | BLK-GRN J5.10 |
| 21 | 54 | C. TOPLANE | GRN-BLU J5.7 | BLK-GRN J5.10 |
| 22 | 55 | R. TOPLANE | GRN-VIO J5.8 | BLK-GRN J5.10 |
| 23 | 57 | L. STAR BUMPER | BLU-BRN J6.1 | BLK-BLU J6.10 |
| 24 | 58 | C. STAR BUMPER | BLU-RED J6.2 | BLK-BLU J6.10 |
| 25 | 59 | R. STAR BUMPER | BLU-ORG J6.3 | BLK-BLU J6.10 |
| 26 | 60 | UR. BALL STANDUP | BLU-YEL J6.4 | BLK-BLU J6.10 |
| 27 | 62 | L. RAMP EXIT | BLU-BLK J6.7 | BLK-BLU J6.10 |
| 28 | 63 | RAMP STANDUP | BLU-VIO J6.8 | BLK-BLU J6.10 |
| 29 | lamp | 83B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW3-M3B J4/5.4 ORG-BLK |
| 30 | lamp | 84B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW4-M4B J4/5.5 ORG-YEL |
| 31 | lamp | 85B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW5-M5B J4/5.6 ORG-GRN |

## Run `slam-tilt`

Held at public 1 from power-up: 9-10, 36-39, 47. Every other switch rests at 0. Summary screen: `ERR: 0-SW 0-SOL 0-LP 0-GAME`, `INFO: 2-SW 0-SOL 3-LP 0-GAME`.

| Page | Switch | ROM name | Switch wire / pin | Return wire / pin |
| --- | --- | --- | --- | --- |
| 1 | 09 | SLAM | WHT-BRN J7.1 | BLK-WHT J7.10 |
| 2 | 10 | TILT | WHT-RED J7.2 | BLK-WHT J7.10 |
| 3 | lamp | 83B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW3-M3B J4/5.4 ORG-BLK |
| 4 | lamp | 84B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW4-M4B J4/5.5 ORG-YEL |
| 5 | lamp | 85B - NOT USED | COL8-SM8B J9/10.9 BLU-GRY | ROW5-M5B J4/5.6 ORG-GRN |
