# Transcription: Kingpin C1.03 Solenoid Test (ROM service menu)

Source: the kpb105 ROM's own service menu, walked by `tools/harness-scenarios/capcom/kpb105-solenoid-test.json` on fresh isolated state with pinned LibPinMAME (`pinmame64.dll`, SHA-256 `ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d`, built from vpinball/pinmame `8371478a7640f1896dcdf565aed340dc5df989ba`) and ROM archive SHA-256 `fb64bcbc1dcd361ccc888cc235dde089e17907eac880af4cdfc3c7812269c0c5`. Raw run SHA-256 `bf42674850a2d605959a476a6228f973c51e753bc974e2f278c4267cfb24384d` (retained externally as `review-artifacts/kingpin/harness-runs/final-solenoid-test/run.json` with every DMD frame).

Text is decoded from the 128x32 DMD frames by exact bitmap matching against the ROM's two fixed fonts (glyphs labelled from the ROM's own name strings, the rest by hand) and was checked by eye against the rendered frames; the companion image is a contact sheet of the decoded frames in table order. Wire colours and pins are what the ROM prints: its service code composes them from fixed colour tables, so they are the manufacturer's standard harness colour code for each position, not a harness trace.

`Fired` lists the public PinMAME solenoid addresses with a nonzero sampled state in the step that selected the coil. The test pulses the selected coil on selection; the previous flasher can still be decaying, and public 20 pulses throughout the whole test, so the selected address is the one matching the displayed S-number.

| Displayed | ROM name | Drive wire / pin | Supply | Fired (public) |
| --- | --- | --- | --- | --- |
| S01 | OUTHOLE | BRN-BLK J14/13.1 | VIO 50V | 1, 20 |
| S02 | TROUGH | BRN-RED J14/13.2 | VIO 50V | 2, 20 |
| S03 | KNOCKER | BRN-ORG J14/13.3 | VIO 50V | 3, 20 |
| S04 | LEFT SLINGSHOT | BRN-YEL J14/13.4 | VIO 50V | 4, 20 |
| S05 | RIGHT SLINGSHOT | BRN-GRN J14/13.5 | VIO 50V | 5, 20 |
| S06 | KING DROP RESET | BRN-BLU J14/13.6 | VIO 50V | 6, 20 |
| S07 | PIN DROP RESET | BRN-VIO J14/13.7 | VIO 50V | 7, 20 |
| S08 | GUN EJECT | BRN-GRY J14/13.9 | VIO 50V | 8, 20 |
| S09 | LEFT FLIPPER | GRN-BRN J18/17.1 | GRY-RED 50V L | 9, 20, 45 |
| S10 | RIGHT FLIPPER | GRN-RED J18/17.2 | GRY-GRN 50V R | 10, 20, 47 |
| S11 | SLOT EJECT | GRN-ORG J18/17.3 | VIO 50V | 11, 20, 33 |
| S12 | SLOT MOTOR | GRN-YEL J18/17.4 | YEL 12V | 12, 20, 35 |
| S13 | TOPGATES | GRN-BLK J18/17.5 | VIO 50V | 13, 20 |
| S14 | RAMP | GRN-BLU J18/17.7 | VIO 50V | 14, 20 |
| S15 | C. STAR BUMPER | GRN-VIO J18/17.8 | VIO 50V | 15, 20 |
| S16 | R. STAR BUMPER | GRN-GRY J18/17.9 | VIO 50V | 16, 20 |
| S17 | L. STAR BUMPER | VIO-BRN J21/20.1 | VIO 50V | 17, 20 |
| S18 | L. RAMP FLASHERS | VIO-RED J21/20.2 | RED 20V B | 18, 20 |
| S19 | L. KID FLASHER | VIO-ORG J21/20.3 | RED 20V B | 19, 20 |
| S20 | BIG AL FLASHERS | VIO-YEL J21/20.4 | RED 20V B | 20 |
| S21 | GUN TIP FLASHERS | VIO-GRN J21/20.5 | RED 20V B | 20, 21 |
| S22 | R. RAMP FLASHER | VIO-BLU J21/20.6 | RED 20V B | 20, 22 |
| S23 | BUILDING FLASHER | VIO-BLK J21/20.8 | RED 20V B | 20, 22, 23 |
| S24 | R. KID FLASHER | VIO-GRY J21/20.9 | RED 20V B | 20, 23, 24 |
| S25 | CAPTIVE FLASHER | GRY-BRN J25/24.1 | RED 20V B | 20, 24, 25 |
| S26 | BUMPERS FLASHER | GRY-RED J25/24.2 | RED 20V B | 20, 26 |
| S27 | POWER FLASHERS | GRY-ORG J25/24.3 | RED 20V B | 20, 26, 27 |
| S28 | LEX FLASHER | GRY-YEL J25/24.5 | RED 20V B | 20, 28 |
| S29 | L.ORBIT (EAST) FLASHER | GRY-GRN J25/24.6 | RED 20V B | 20, 29 |
| S30 | KING FLASHERS | GRY-BLU J25/24.7 | RED 20V B | 20, 30 |
| S31 | PIN FLASHERS | GRY-VIO J25/24.8 | RED 20V B | 20, 31 |
| S32 | AUTO PLUNGER | GRY-BLK J25/24.9 | VIO 50V | 20, 32 |
