# Transcription: Kingpin C1.01 Switch Test (ROM service menu)

Source: the kpb105 ROM's own service menu, walked by `tools/harness-scenarios/capcom/kpb105-switch-test.json` on fresh isolated state with pinned LibPinMAME (`pinmame64.dll`, SHA-256 `ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d`, built from vpinball/pinmame `8371478a7640f1896dcdf565aed340dc5df989ba`) and ROM archive SHA-256 `fb64bcbc1dcd361ccc888cc235dde089e17907eac880af4cdfc3c7812269c0c5`. Raw run SHA-256 `42d9948e815e7ba05fb4d3f57391845ee911e5c3d525eea9af66b87664f8e8b9` (retained externally as `review-artifacts/kingpin/harness-runs/final-switch-test/run.json` with every DMD frame).

Text is decoded from the 128x32 DMD frames by exact bitmap matching against the ROM's two fixed fonts (glyphs labelled from the ROM's own name strings, the rest by hand) and was checked by eye against the rendered frames; the companion image is a contact sheet of the decoded frames in table order. Wire colours and pins are what the ROM prints: its service code composes them from fixed colour tables, so they are the manufacturer's standard harness colour code for each position, not a harness trace.

Each row is one step that held exactly one public switch; `Shown` is the switch number the ROM printed for the closed switch. The first wire is the switch's own line, the second the column return. The name stays on the display after the switch is released, so it does not show the level. The level is in a small icon the test draws in the left half of the display, in a cell that depends on the switch: `Icon at 1` is read from the frame taken while the switch was held at public 1, `Icon at 0` from the frame after it was released to public 0. The ROM draws four icons (`#` a lit dot, one text line per DMD row): contact closed `###` / `#.#`; contact open `..#` / `.#.` / `#..` / `#.#`, a raised lever; beam broken `###` / `...` / `...` / `###`; beam clear `###` / `.#.` / `.#.` / `###`. In the contact sheet each held frame is followed by its released frame.

| Public held | Shown | ROM name | Switch wire / pin | Return wire / pin | Icon at 1 | Icon at 0 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 01 | COIN 1 | GRN-BRN J9.1 | BLK-GRN J9.10 | contact closed | contact open |
| 2 | 02 | COIN 2 | GRN-RED J9.2 | BLK-GRN J9.10 | contact closed | contact open |
| 3 | 03 | COIN 3 | GRN-ORG J9.3 | BLK-GRN J9.10 | contact closed | contact open |
| 4 | 04 | COIN 4 | GRN-YEL J9.4 | BLK-GRN J9.10 | contact closed | contact open |
| 9 | 09 | SLAM | WHT-BRN J7.1 | BLK-WHT J7.10 | contact closed | contact open |
| 10 | 10 | TILT | WHT-RED J7.2 | BLK-WHT J7.10 | contact closed | contact open |
| 11 | 11 | NOT USED | WHT-ORG J7.3 | BLK-WHT J7.10 | contact closed | contact open |
| 12 | 12 | NOT USED | WHT-YEL J7.4 | BLK-WHT J7.10 | contact closed | contact open |
| 13 | 13 | TOKEN EXTRA | WHT-GRN J7.5 | BLK-WHT J7.10 | contact closed | contact open |
| 14 | 14 | AUTO PLUNGER | WHT-BLU J7.7 | BLK-WHT J7.10 | contact closed | contact open |
| 15 | 15 | TOKEN EXIT | WHT-VIO J7.8 | BLK-WHT J7.10 | contact closed | contact open |
| 16 | 16 | TICKET NOTCH | WHT-GRY J7.9 | BLK-WHT J7.10 | contact closed | contact open |
| 17 | 17 | R. RAMP SPINNER | BRN-BLK J1.1 | BLK-BRN J1.10 | beam broken | beam clear |
| 18 | 18 | R. RAMP EXIT | BRN-RED J1.2 | BLK-BRN J1.10 | contact closed | contact open |
| 19 | 19 | L. RETURN | BRN-ORG J1.3 | BLK-BRN J1.10 | contact closed | contact open |
| 20 | 20 | R. RETURN | BRN-YEL J1.4 | BLK-BRN J1.10 | contact closed | contact open |
| 21 | 21 | L. OUTLANE | BRN-GRN J1.5 | BLK-BRN J1.10 | contact closed | contact open |
| 22 | 22 | R. OUTLANE | BRN-BLU J1.6 | BLK-BRN J1.10 | contact closed | contact open |
| 23 | 23 | LEFT ORBIT | BRN-VIO J1.7 | BLK-BRN J1.10 | contact closed | contact open |
| 24 | 24 | RIGHT ORBIT | BRN-GRY J1.9 | BLK-BRN J1.10 | contact closed | contact open |
| 25 | 25 | DROP K | RED-BRN J2.1 | BLK-RED J2.10 | contact closed | contact open |
| 26 | 26 | DROP I | RED-BLK J2.2 | BLK-RED J2.10 | contact closed | contact open |
| 27 | 27 | DROP N | RED-ORG J2.3 | BLK-RED J2.10 | contact closed | contact open |
| 28 | 28 | DROP G | RED-YEL J2.4 | BLK-RED J2.10 | contact closed | contact open |
| 29 | 29 | DROP P | RED-GRN J2.5 | BLK-RED J2.10 | contact closed | contact open |
| 30 | 30 | DROP I | RED-BLU J2.7 | BLK-RED J2.10 | contact closed | contact open |
| 31 | 31 | DROP N | RED-VIO J2.8 | BLK-RED J2.10 | contact closed | contact open |
| 32 | 32 | CAPTIVE BALL | RED-GRY J2.9 | BLK-RED J2.10 | contact closed | contact open |
| 33 | 33 | EOS L | ORG-BRN J3.1 | BLK-ORG J3.10 | contact closed | contact open |
| 34 | 34 | EOS R | ORG-RED J3.2 | BLK-ORG J3.10 | contact closed | contact open |
| 35 | 35 | OUTHOLE | ORG-BLK J3.3 | BLK-ORG J3.10 | contact closed | contact open |
| 36 | 36 | TROUGH 1 | ORG-YEL J3.4 | BLK-ORG J3.10 | beam broken | beam clear |
| 37 | 37 | TROUGH 2 | ORG-GRN J3.5 | BLK-ORG J3.10 | beam broken | beam clear |
| 38 | 38 | TROUGH 3 | ORG-BLU J3.7 | BLK-ORG J3.10 | beam broken | beam clear |
| 39 | 39 | TROUGH 4 | ORG-VIO J3.8 | BLK-ORG J3.10 | beam broken | beam clear |
| 40 | 40 | NOT USED | ORG-GRY J3.9 | BLK-ORG J3.10 | contact closed | contact open |
| 41 | 41 | L. SLING | YEL-BRN J4.1 | BLK-YEL J4.10 | contact closed | contact open |
| 42 | 42 | R. SLING | YEL-RED J4.2 | BLK-YEL J4.10 | contact closed | contact open |
| 43 | 43 | SHOOTER | YEL-ORG J4.3 | BLK-YEL J4.10 | contact closed | contact open |
| 44 | 44 | GUN LOCK 1 | YEL-BLK J4.4 | BLK-YEL J4.10 | beam broken | beam clear |
| 45 | 45 | GUN LOCK 2 | YEL-GRN J4.5 | BLK-YEL J4.10 | contact closed | contact open |
| 46 | 46 | GUN LOCK 3 | YEL-BLU J4.7 | BLK-YEL J4.10 | contact closed | contact open |
| 47 | 47 | RAMP, DOWN | YEL-VIO J4.8 | BLK-YEL J4.10 | contact closed | contact open |
| 48 | 48 | GUN TROUGH OPTO | YEL-GRY J4.9 | BLK-YEL J4.10 | beam broken | beam clear |
| 49 | 49 | L. SLOT STANDUP | GRN-BRN J5.1 | BLK-GRN J5.10 | contact closed | contact open |
| 50 | 50 | R. SLOT STANDUP | GRN-RED J5.2 | BLK-GRN J5.10 | contact closed | contact open |
| 51 | 51 | SLOT SAUCER | GRN-ORG J5.3 | BLK-GRN J5.10 | contact closed | contact open |
| 52 | 52 | SLOT OPTO | GRN-YEL J5.4 | BLK-GRN J5.10 | beam broken | beam clear |
| 53 | 53 | L. TOPLANE | GRN-BLK J5.5 | BLK-GRN J5.10 | contact closed | contact open |
| 54 | 54 | C. TOPLANE | GRN-BLU J5.7 | BLK-GRN J5.10 | contact closed | contact open |
| 55 | 55 | R. TOPLANE | GRN-VIO J5.8 | BLK-GRN J5.10 | contact closed | contact open |
| 56 | 56 | NOT USED | GRN-GRY J5.9 | BLK-GRN J5.10 | contact closed | contact open |
| 57 | 57 | L. STAR BUMPER | BLU-BRN J6.1 | BLK-BLU J6.10 | contact closed | contact open |
| 58 | 58 | C. STAR BUMPER | BLU-RED J6.2 | BLK-BLU J6.10 | contact closed | contact open |
| 59 | 59 | R. STAR BUMPER | BLU-ORG J6.3 | BLK-BLU J6.10 | contact closed | contact open |
| 60 | 60 | UR. BALL STANDUP | BLU-YEL J6.4 | BLK-BLU J6.10 | contact closed | contact open |
| 61 | 61 | L. RAMP SPINNER | BLU-GRN J6.5 | BLK-BLU J6.10 | beam broken | beam clear |
| 62 | 62 | L. RAMP EXIT | BLU-BLK J6.7 | BLK-BLU J6.10 | contact closed | contact open |
| 63 | 63 | RAMP STANDUP | BLU-VIO J6.8 | BLK-BLU J6.10 | contact closed | contact open |
| 64 | 64 | NOT USED | BLU-GRY J6.9 | BLK-BLU J6.10 | contact closed | contact open |
| 65 | 65 | NOT USED | VIO-BRN J7.1 | BLK-VIO J7.10 | contact closed | contact open |
| 66 | 66 | NOT USED | VIO-RED J7.2 | BLK-VIO J7.10 | contact closed | contact open |
| 67 | 67 | NOT USED | VIO-ORG J7.3 | BLK-VIO J7.10 | contact closed | contact open |
| 68 | 68 | NOT USED | VIO-YEL J7.4 | BLK-VIO J7.10 | contact closed | contact open |
| 69 | 69 | NOT USED | VIO-GRN J7.5 | BLK-VIO J7.10 | contact closed | contact open |
| 70 | 70 | NOT USED | VIO-BLU J7.7 | BLK-VIO J7.10 | contact closed | contact open |
| 71 | 71 | NOT USED | VIO-BLK J7.8 | BLK-VIO J7.10 | contact closed | contact open |
| 72 | 72 | NOT USED | VIO-GRY J7.9 | BLK-VIO J7.10 | contact closed | contact open |
| 73 | 73 | NOT USED | GRY-BRN J8.1 | BLK-GRY J8.10 | contact closed | contact open |
| 74 | 74 | NOT USED | GRY-RED J8.2 | BLK-GRY J8.10 | contact closed | contact open |
| 75 | 75 | NOT USED | GRY-ORG J8.3 | BLK-GRY J8.10 | contact closed | contact open |
| 76 | 76 | NOT USED | GRY-YEL J8.4 | BLK-GRY J8.10 | contact closed | contact open |
| 77 | 77 | NOT USED | GRY-GRN J8.5 | BLK-GRY J8.10 | contact closed | contact open |
| 78 | 78 | NOT USED | GRY-BLU J8.7 | BLK-GRY J8.10 | contact closed | contact open |
| 79 | 79 | NOT USED | GRY-VIO J8.8 | BLK-GRY J8.10 | contact closed | contact open |
| 80 | 80 | NOT USED | GRY-BLK J8.9 | BLK-GRY J8.10 | contact closed | contact open |

Cabinet entries the menu navigation itself uses cannot be held without leaving the test, so they were shown by browsing the list with the flipper buttons (left back, right forward) from the 07 entry the Start press produced. `Level` is the switch's public level in that frame: the flipper buttons and Start were released, while the coin door switch 8 stayed at 1 from the step that opened the menu:

| Shown | ROM name | Switch wire / pin | Return wire / pin | Browse step | Level | Icon |
| --- | --- | --- | --- | --- | --- | --- |
| 05 | LEFT FLIPPER | GRN-BLK J9.5 | BLK-GRN J9.10 | left flipper button (84): browse back to 05 | 0 | contact open |
| 06 | RIGHT FLIPPER | GRN-BLU J9.6 | BLK-GRN J9.10 | left flipper button (84): browse the Switch Test list back to 06 | 0 | contact open |
| 07 | START BUTTON | GRN-VIO J9.7 | BLK-GRN J9.10 | Start: enter SWITCH TEST (the Start press itself is shown as 07 START BUTTON) | 0 | contact open |
| 08 | COIN DOOR | GRN-GRY J9.9 | BLK-GRN J9.10 | right flipper button (82): browse forward to 08 | 1 | contact closed |
