# Starship Troopers — Switch Matrix Grid and dedicated switches

Read from `Sega_1997_Starship_Troopers_Manual.pdf` (IPDB 4341, 150 scanned pages, no text layer). The Switch Matrix
Grid is the front-matter drawing printed `DR. 4` on PDF page 6; its part numbers repeat in the printed page-21 table
"Switch Matrix Grid Descriptions with Part Numbers and Locations" on PDF page 35. Every cell was read from a 400 dpi
render and checked against a Windows OCR pass.

## Matrix drives and returns

| Column | Drive transistor | Drive wire | Connector |
| --- | --- | --- | --- |
| 1 | Q1 | GRN-BRN | CN5-P1 |
| 2 | Q2 | GRN-RED | CN5-P3 |
| 3 | Q3 | GRN-ORG | CN5-P4 |
| 4 | Q4 | GRN-YEL | CN5-P5 |
| 5 | Q5 | GRN-BLK | CN5-P6 |
| 6 | Q6 | GRN-BLU | CN5-P7 |
| 7 | Q7 | GRN-VIO | CN5-P8 |
| 8 | Q8 | GRN-GRY | CN5-P9 |

| Row | Receiver | Return wire | Connector |
| --- | --- | --- | --- |
| 1 | U400 | WHT-BRN | CN7-P9 |
| 2 | U400 | WHT-RED | CN7-P8 |
| 3 | U400 | WHT-ORG | CN7-P7 |
| 4 | U400 | WHT-YEL | CN7-P6 |
| 5 | U401 | WHT-GRN | CN7-P5 |
| 6 | U401 | WHT-BLU | CN7-P3 |
| 7 | U401 | WHT-VIO | CN7-P2 |
| 8 | U401 | WHT-GRY | CN7-P1 |

## Matrix switches

Switch number = (column − 1) × 8 + row. "Grid" is the DR. 4 cell text; "Page 21" is the table's description, kept
where it differs; "Col/Row" is the page-21 table's own column and row cells. A part cell the table prints once beside
several rows is marked "(shared cell)". "DOTS" marks the vertical "Diode On Terminal Strip" tag, which DR. 4 and page
21 print on the same switches. A NOT USED cell is shaded on both pages and has no part number. An asterisk is the page-21
table's own mark on the switch number.

| # | Col | Row | Grid | Page 21 | Page-21 Col/Row | Part | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | NOT USED | NOT USED | 1 1 | | |
| 2 | 1 | 2 | 4TH COIN SLOT | 4TH COIN SLOT | 1 2 | 180-5024-00 | 2* |
| 3 | 1 | 3 | 6TH COIN SLOT | *6TH COIN SLOT* (italic) | 1 3 | (Future Use) | 3* |
| 4 | 1 | 4 | RIGHT COIN SLOT | RIGHT COIN SLOT | 1 4 | 180-5024-00 (shared cell) | 4* |
| 5 | 1 | 5 | CENTER COIN SLOT / DBA | CENTER COIN SLOT / DBA | 1 5 | 180-5024-00 (shared cell) | 5* |
| 6 | 1 | 6 | LEFT COIN SLOT | LEFT COIN SLOT | 1 6 | 180-5024-00 (shared cell) | 6* |
| 7 | 1 | 7 | 5TH COIN SLOT | *5TH COIN SLOT* (italic) | 1 7 | (Future Use) | 7* |
| 8 | 1 | 8 | NOT USED | NOT USED | 1 8 | | |
| 9 | 2 | 1 | U'TROUGH: SKILL SHOT | U'TROUGH: SKILL SHOT | 2 1 | 180-5057-00 (shared cell) | |
| 10 | 2 | 2 | U'TROUGH: BUG HOLE | U'TROUGH: BUG HOLE | 2 2 | 180-5057-00 (shared cell) | |
| 11 | 2 | 3 | NOT USED | NOT USED | 2 3 | | |
| 12 | 2 | 4 | 4-BALL TROUGH #1 (LEFT) | 4-BALL TROUGH #1 (LEFT) | 2 4 | 180-5119-00 (shared cell) | |
| 13 | 2 | 5 | 4-BALL TROUGH #2 | 4-BALL TROUGH #2 | 2 5 | 180-5119-00 (shared cell) | |
| 14 | 2 | 6 | 4-BALL TROUGH #3 | 4-BALL TROUGH #3 | 2 6 | 180-5119-00 (shared cell) | |
| 15 | 2 | 7 | 4-BALL TROUGH VUK OPTO | 4-BALL TROUGH VUK OPTO | 2 7 | TRANS 520-5124-00 / REC 520-5125-00 | |
| 16 | 2 | 8 | SHOOTER LANE | SHOOTER LANE | 2 8 | 500-5096-00 | DOTS |
| 17 | 3 | 1 | LEFT BOTTOM S-U (GRN) | LEFT BOTTOM S-U (GRN) | 3 1 | 500-6139-04 | |
| 18 | 3 | 2 | LEFT MIDDLE S-U (YEL) | LEFT MIDDLE S-U (YEL) | 3 2 | 500-6138-06 | |
| 19 | 3 | 3 | LEFT MIDDLE S-U (RED) | LEFT MIDDLE S-U (RED) | 3 3 | 500-6075-02 | |
| 20 | 3 | 4 | LEFT TOP S-U (YEL) | LEFT TOP S-U (YEL) | 3 4 | 500-6138-06 | |
| 21 | 3 | 5 | RIGHT BOTTOM S-U (RED) | RIGHT BOTTOM S-U (RED) | 3 5 | 500-6075-02 | |
| 22 | 3 | 6 | RIGHT MIDDLE S-U (YEL) | RIGHT MIDDLE S-U (YEL) | 3 6 | 500-6138-06 | |
| 23 | 3 | 7 | RIGHT MIDDLE S-U (GRN) | RIGHT MIDDLE S-U (GRN) | 3 7 | 500-6139-04 | |
| 24 | 3 | 8 | RIGHT TOP S-U (YEL) | RIGHT TOP S-U (YEL) | 3 8 | 500-6138-06 | |
| 25 | 4 | 1 | LEFT RAMP ENTER | LEFT RAMP ENTER | 4 1 | 180-5087-00 | |
| 26 | 4 | 2 | LEFT RAMP EXIT | LEFT RAMP EXIT (on Wire Ramp) | 4 2 | 180-5093-00 | DOTS |
| 27 | 4 | 3 | LEFT RAMP S-U (YEL) | LEFT RAMP S-U (YEL) | 4 3 | 500-6138-06 | |
| 28 | 4 | 4 | POP S-U (BLU) | POP S-U (BLU) | 4 4 | 500-6228-05 | |
| 29 | 4 | 5 | POP. S-U (GRN) | POP S-U (GRN) | 4 5 | 500-6139-04 (shared cell) | |
| 30 | 4 | 6 | VUK S-U (GRN) | VUK S-U (GRN) | 4 6 | 500-6139-04 (shared cell) | |
| 31 | 4 | 7 | VUK S-U (BLU) | VUK S-U (BLU) | 4 7 | 500-6228-05 | |
| 32 | 4 | 8 | RIGHT RAMP S-U (YEL) | RIGHT RAMP S-U (YEL) | 4 8 | 500-6138-06 | |
| 33 | 5 | 1 | STEPPER MOTOR REAR | STEPPER MOTOR REAR | 5 1 | 180-5119-00 (shared cell) | DOTS |
| 34 | 5 | 2 | STEPPER MOTOR FRONT | STEPPER MOTOR FRONT | 5 2 | 180-5119-00 (shared cell) | DOTS |
| 35 | 5 | 3 | STEPPER MOTOR BUG | STEPPER MOTOR BUG | 5 3 | 180-5119-00 (shared cell) | DOTS |
| 36 | 5 | 4 | NOT USED | NOT USED | 5 4 | | |
| 37 | 5 | 5 | BRAIN BUG UP | BRAIN BUG UP | 5 5 | 180-5165-00 (shared cell) | |
| 38 | 5 | 6 | BRAIN BUG HIT | BRAIN BUG HIT | 5 6 | 180-5165-00 (shared cell) | DOTS |
| 39 | 5 | 7 | BRAIN BUG UP | BRAIN BUG UP | 5 7 | 180-5165-00 (shared cell) | |
| 40 | 5 | 8 | U'TROUGH POP EXIT HOLE | U'TROUGH: POP EXIT HOLE | 5 8 | 180-5057-00 | DOTS |
| 41 | 6 | 1 | LEFT TOP LANE | LEFT TOP LANE | 6 1 | 500-6227-02 (shared cell) | |
| 42 | 6 | 2 | MIDDLE TOP LANE | MIDDLE TOP LANE | 6 2 | 500-6227-02 (shared cell) | |
| 43 | 6 | 3 | RIGHT TOP LANE | RIGHT TOP LANE | 6 3 | 500-6227-02 (shared cell) | |
| 44 | 6 | 4 | NOT USED | NOT USED | 6 4 | | |
| 45 | 6 | 5 | VUK | VUK | 6 5 | 180-5116-01 | DOTS |
| 46 | 6 | 6 | SUPER VUK | SUPER VUK | 6 6 | 180-5052-00 | DOTS |
| 47 | 6 | 7 | LEFT ORBIT | LEFT ORBIT (OPTO) | 6 7 | TRANS 520-5082-00 / REC 520-5083-01 | |
| 48 | 6 | 8 | RIGHT ORBIT | RIGHT ORBIT (OPTO) | 6 8 | TRANS 520-5082-00 / REC 520-5083-01 | |
| 49 | 7 | 1 | LEFT TURBO BUMPER | TOP TURBO BUMPER | 7 4 | 180-5015-03 (shared cell) | page 21 prints the row cell "4" |
| 50 | 7 | 2 | BOTTOM TURBO BUMPER | BOTTOM TURBO BUMPER | 7 2 | 180-5015-03 (shared cell) | |
| 51 | 7 | 3 | RIGHT TURBO BUMPER | RIGHT TURBO BUMPER | 7 3 | 180-5015-03 (shared cell) | |
| 52 | 7 | 4 | RIGHT RAMP ENTER | RIGHT RAMP ENTER | 7 4 | 180-5087-00 (shared cell) | |
| 53 | 7 | 5 | RIGHT RAMP EXIT | RIGHT RAMP EXIT | 7 5 | 180-5087-00 (shared cell) | |
| 54 | 7 | 6 | START BUTTON | START BUTTON | 7 6 | 500-6090-06 | 54* |
| 55 | 7 | 7 | SLAM TILT | SLAM TILT (On Coin Door) | 7 7 | 180-5022-00 | 55* |
| 56 | 7 | 8 | PLUMB BOB TILT | PLUMB BOB TILT | 7 8 | HANGER 535-5319-00 / CONTACT 535-7563-01 | 56* |
| 57 | 8 | 1 | LEFT OUTLANE | LEFT OUTLANE | 8 1 | 500-6227-02 (shared cell) | |
| 58 | 8 | 2 | LEFT RETURN LANE | LEFT RETURN LANE | 8 2 | 500-6227-02 (shared cell) | |
| 59 | 8 | 3 | LEFT SLINGSHOT | LEFT SLINGSHOT | 8 3 | 180-5054-00 | |
| 60 | 8 | 4 | RIGHT OUTLANE | RIGHT OUTLANE | 8 4 | 500-6227-02 (shared cell) | |
| 61 | 8 | 5 | RIGHT RETURN LANE | RIGHT RETURN LANE | 8 5 | 500-6227-02 (shared cell) | |
| 62 | 8 | 6 | RIGHT SLINGSHOT | RIGHT SLINGSHOT | 8 6 | 180-5054-00 | |
| 63 | 8 | 7 | NOT USED | NOT USED | 8 7 | | |
| 64 | 8 | 8 | NOT USED | NOT USED | 8 8 | | |

Page-21 notes, verbatim:

- Title footnote: "† The sw. locations correspond with the Sw. Nº in the table below and the Switch Matrix Grid. *Note:*
  Diode On Terminal Strip (DOTS) if noted."
- Above row 1: "Note: The ¥ Coin Switch (for Japan) is 180-5091-00"
- "* The following switches are located in the cabinet and are not noted in the diagram above: 2 4 5 6 55 56"
- "The following switches are not used: 1 8 11 36 44 63 64"
- Legend: white box "= Switches mounted above playfield.", black box "= Switches mounted below playfield."

## Dedicated switches (U206 inputs; ground BLK, CN6-P1 and CN6-P11)

| Input | Wire | Connector | Function as printed |
| --- | --- | --- | --- |
| DS-1 | GRY-BRN | CN6-P2 | #1 LEFT FLIPPER BUTTON |
| DS-2 | GRY-RED | CN6-P3 | #2 LEFT FLIPPER E.O.S (End-of-Stroke) |
| DS-3 | GRY-ORG | CN6-P4 | #3 RIGHT FLIPPER BUTTON |
| DS-4 | GRY-YEL | CN6-P6 | #4 RIGHT FLIPPER E.O.S. |
| DS-5 | GRY-GRN | CN6-P7 | #5 MINI FLIPPER BUTTON |
| DS-6 | GRY-BLU | CN6-P8 | #6 VOLUME (RED BUTTON) (Normal) (In Test: LEFT) |
| DS-7 | GRY-VIO | CN6-P9 | #7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT) |
| DS-8 | GRY-BLK | CN6-P10 | #8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER) |
