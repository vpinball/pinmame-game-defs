# Transcription: Kingpin C1.01 Switch Test (ROM service menu)

Source: the kpb105 ROM's own service menu, walked by `tools/harness-scenarios/capcom/kpb105-switch-test.json` on fresh isolated state with pinned LibPinMAME (`pinmame64.dll`, SHA-256 `ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d`, built from vpinball/pinmame `8371478a7640f1896dcdf565aed340dc5df989ba`) and ROM archive SHA-256 `fb64bcbc1dcd361ccc888cc235dde089e17907eac880af4cdfc3c7812269c0c5`. Raw run SHA-256 `42d9948e815e7ba05fb4d3f57391845ee911e5c3d525eea9af66b87664f8e8b9` (retained externally as `review-artifacts/kingpin/harness-runs/final-switch-test/run.json` with every DMD frame).

Text is decoded from the 128x32 DMD frames by exact bitmap matching against the ROM's two fixed fonts (glyphs labelled from the ROM's own name strings, the rest by hand) and was checked by eye against the rendered frames; the companion image is a contact sheet of the decoded frames in table order. Wire colours and pins are what the ROM prints: its service code composes them from fixed colour tables, so they are the manufacturer's standard harness colour code for each position, not a harness trace.

Each row is one step that held exactly one public switch; `Shown` is the switch number the ROM printed for the closed switch. The first wire is the switch's own line, the second the column return.

| Public held | Shown | ROM name | Switch wire / pin | Return wire / pin |
| --- | --- | --- | --- | --- |
| 1 | 01 | COIN 1 | GRN-BRN J9.1 | BLK-GRN J9.10 |
| 2 | 02 | COIN 2 | GRN-RED J9.2 | BLK-GRN J9.10 |
| 3 | 03 | COIN 3 | GRN-ORG J9.3 | BLK-GRN J9.10 |
| 4 | 04 | COIN 4 | GRN-YEL J9.4 | BLK-GRN J9.10 |
| 9 | 09 | SLAM | WHT-BRN J7.1 | BLK-WHT J7.10 |
| 10 | 10 | TILT | WHT-RED J7.2 | BLK-WHT J7.10 |
| 11 | 11 | NOT USED | WHT-ORG J7.3 | BLK-WHT J7.10 |
| 12 | 12 | NOT USED | WHT-YEL J7.4 | BLK-WHT J7.10 |
| 13 | 13 | TOKEN EXTRA | WHT-GRN J7.5 | BLK-WHT J7.10 |
| 14 | 14 | AUTO PLUNGER | WHT-BLU J7.7 | BLK-WHT J7.10 |
| 15 | 15 | TOKEN EXIT | WHT-VIO J7.8 | BLK-WHT J7.10 |
| 16 | 16 | TICKET NOTCH | WHT-GRY J7.9 | BLK-WHT J7.10 |
| 17 | 17 | R. RAMP SPINNER | BRN-BLK J1.1 | BLK-BRN J1.10 |
| 18 | 18 | R. RAMP EXIT | BRN-RED J1.2 | BLK-BRN J1.10 |
| 19 | 19 | L. RETURN | BRN-ORG J1.3 | BLK-BRN J1.10 |
| 20 | 20 | R. RETURN | BRN-YEL J1.4 | BLK-BRN J1.10 |
| 21 | 21 | L. OUTLANE | BRN-GRN J1.5 | BLK-BRN J1.10 |
| 22 | 22 | R. OUTLANE | BRN-BLU J1.6 | BLK-BRN J1.10 |
| 23 | 23 | LEFT ORBIT | BRN-VIO J1.7 | BLK-BRN J1.10 |
| 24 | 24 | RIGHT ORBIT | BRN-GRY J1.9 | BLK-BRN J1.10 |
| 25 | 25 | DROP K | RED-BRN J2.1 | BLK-RED J2.10 |
| 26 | 26 | DROP I | RED-BLK J2.2 | BLK-RED J2.10 |
| 27 | 27 | DROP N | RED-ORG J2.3 | BLK-RED J2.10 |
| 28 | 28 | DROP G | RED-YEL J2.4 | BLK-RED J2.10 |
| 29 | 29 | DROP P | RED-GRN J2.5 | BLK-RED J2.10 |
| 30 | 30 | DROP I | RED-BLU J2.7 | BLK-RED J2.10 |
| 31 | 31 | DROP N | RED-VIO J2.8 | BLK-RED J2.10 |
| 32 | 32 | CAPTIVE BALL | RED-GRY J2.9 | BLK-RED J2.10 |
| 33 | 33 | EOS L | ORG-BRN J3.1 | BLK-ORG J3.10 |
| 34 | 34 | EOS R | ORG-RED J3.2 | BLK-ORG J3.10 |
| 35 | 35 | OUTHOLE | ORG-BLK J3.3 | BLK-ORG J3.10 |
| 36 | 36 | TROUGH 1 | ORG-YEL J3.4 | BLK-ORG J3.10 |
| 37 | 37 | TROUGH 2 | ORG-GRN J3.5 | BLK-ORG J3.10 |
| 38 | 38 | TROUGH 3 | ORG-BLU J3.7 | BLK-ORG J3.10 |
| 39 | 39 | TROUGH 4 | ORG-VIO J3.8 | BLK-ORG J3.10 |
| 40 | 40 | NOT USED | ORG-GRY J3.9 | BLK-ORG J3.10 |
| 41 | 41 | L. SLING | YEL-BRN J4.1 | BLK-YEL J4.10 |
| 42 | 42 | R. SLING | YEL-RED J4.2 | BLK-YEL J4.10 |
| 43 | 43 | SHOOTER | YEL-ORG J4.3 | BLK-YEL J4.10 |
| 44 | 44 | GUN LOCK 1 | YEL-BLK J4.4 | BLK-YEL J4.10 |
| 45 | 45 | GUN LOCK 2 | YEL-GRN J4.5 | BLK-YEL J4.10 |
| 46 | 46 | GUN LOCK 3 | YEL-BLU J4.7 | BLK-YEL J4.10 |
| 47 | 47 | RAMP, DOWN | YEL-VIO J4.8 | BLK-YEL J4.10 |
| 48 | 48 | GUN TROUGH OPTO | YEL-GRY J4.9 | BLK-YEL J4.10 |
| 49 | 49 | L. SLOT STANDUP | GRN-BRN J5.1 | BLK-GRN J5.10 |
| 50 | 50 | R. SLOT STANDUP | GRN-RED J5.2 | BLK-GRN J5.10 |
| 51 | 51 | SLOT SAUCER | GRN-ORG J5.3 | BLK-GRN J5.10 |
| 52 | 52 | SLOT OPTO | GRN-YEL J5.4 | BLK-GRN J5.10 |
| 53 | 53 | L. TOPLANE | GRN-BLK J5.5 | BLK-GRN J5.10 |
| 54 | 54 | C. TOPLANE | GRN-BLU J5.7 | BLK-GRN J5.10 |
| 55 | 55 | R. TOPLANE | GRN-VIO J5.8 | BLK-GRN J5.10 |
| 56 | 56 | NOT USED | GRN-GRY J5.9 | BLK-GRN J5.10 |
| 57 | 57 | L. STAR BUMPER | BLU-BRN J6.1 | BLK-BLU J6.10 |
| 58 | 58 | C. STAR BUMPER | BLU-RED J6.2 | BLK-BLU J6.10 |
| 59 | 59 | R. STAR BUMPER | BLU-ORG J6.3 | BLK-BLU J6.10 |
| 60 | 60 | UR. BALL STANDUP | BLU-YEL J6.4 | BLK-BLU J6.10 |
| 61 | 61 | L. RAMP SPINNER | BLU-GRN J6.5 | BLK-BLU J6.10 |
| 62 | 62 | L. RAMP EXIT | BLU-BLK J6.7 | BLK-BLU J6.10 |
| 63 | 63 | RAMP STANDUP | BLU-VIO J6.8 | BLK-BLU J6.10 |
| 64 | 64 | NOT USED | BLU-GRY J6.9 | BLK-BLU J6.10 |
| 65 | 65 | NOT USED | VIO-BRN J7.1 | BLK-VIO J7.10 |
| 66 | 66 | NOT USED | VIO-RED J7.2 | BLK-VIO J7.10 |
| 67 | 67 | NOT USED | VIO-ORG J7.3 | BLK-VIO J7.10 |
| 68 | 68 | NOT USED | VIO-YEL J7.4 | BLK-VIO J7.10 |
| 69 | 69 | NOT USED | VIO-GRN J7.5 | BLK-VIO J7.10 |
| 70 | 70 | NOT USED | VIO-BLU J7.7 | BLK-VIO J7.10 |
| 71 | 71 | NOT USED | VIO-BLK J7.8 | BLK-VIO J7.10 |
| 72 | 72 | NOT USED | VIO-GRY J7.9 | BLK-VIO J7.10 |
| 73 | 73 | NOT USED | GRY-BRN J8.1 | BLK-GRY J8.10 |
| 74 | 74 | NOT USED | GRY-RED J8.2 | BLK-GRY J8.10 |
| 75 | 75 | NOT USED | GRY-ORG J8.3 | BLK-GRY J8.10 |
| 76 | 76 | NOT USED | GRY-YEL J8.4 | BLK-GRY J8.10 |
| 77 | 77 | NOT USED | GRY-GRN J8.5 | BLK-GRY J8.10 |
| 78 | 78 | NOT USED | GRY-BLU J8.7 | BLK-GRY J8.10 |
| 79 | 79 | NOT USED | GRY-VIO J8.8 | BLK-GRY J8.10 |
| 80 | 80 | NOT USED | GRY-BLK J8.9 | BLK-GRY J8.10 |

Cabinet entries the menu navigation itself uses cannot be held without leaving the test, so they were shown by browsing the list with the flipper buttons (left back, right forward) from the 07 entry the Start press produced:

| Shown | ROM name | Switch wire / pin | Return wire / pin | Browse step |
| --- | --- | --- | --- | --- |
| 05 | LEFT FLIPPER | GRN-BLK J9.5 | BLK-GRN J9.10 | left flipper button (84): browse back to 05 |
| 06 | RIGHT FLIPPER | GRN-BLU J9.6 | BLK-GRN J9.10 | left flipper button (84): browse the Switch Test list back to 06 |
| 07 | START BUTTON | GRN-VIO J9.7 | BLK-GRN J9.10 | Start: enter SWITCH TEST (the Start press itself is shown as 07 START BUTTON) |
| 08 | COIN DOOR | GRN-GRY J9.9 | BLK-GRN J9.10 | right flipper button (82): browse forward to 08 |
