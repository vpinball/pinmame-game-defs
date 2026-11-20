# Factory switch wiring, #1104-E

W-1192-1c (schematics PDF page 8), PLAYFIELD A6, complete switch
matrix. Cells reproduce the labels by return and strobe. `[blank]`
marks an open-contact symbol with no function caption, and `—` marks
the absent A6 contact at I6/ST1, whose return is wired in the cabinet.
All drawn contacts in this block are shown open. Parenthetical notes
below describe the drawings. Public address is row ordinal plus
eight times the zero-based ST index.

| Return | Code | Pin | ST0 (51 A4J2-1) | ST1 (93 A4J2-2) | ST2 (52 A4J2-3) | ST3 (53 A4J2-4) | ST4 (31 A4J2-5) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I0 | 54 | A4J2-8 | [blank] | [blank] | RT DROP TARGET ‘D’ | RT FEEDER LANE | RT OUT LANE |
| I1 | 56 | A4J2-9 | [blank] | [blank] | RT DROP TARGET ‘C’ | LT FEEDER LANE | LT OUT LANE |
| I2 | 57 | A4J2-10 | [blank] | [blank] | RT DROP TARGET ‘B’ | DROP TARGETS | RT SLING SHOT |
| I3 | 58 | A4J2-11 | [blank] | [blank] | RT DROP TARGET ‘A’ | RT ‘B’ LANE | LT SLING SHOT |
| I4 | 60 | A4J2-12 | [blank] | [blank] | LT DROP TARGET ‘D’ | LT ‘A’ LANE | BOTTOM RT BUMPER |
| I5 | 63 | A4J2-13 | [blank] | [blank] | LT DROP TARGET ‘C’ | TOP ‘B’ LANE | BOTTOM LT BUMPER |
| I6 | 65 | A4J2-14 | TILT | — | LT DROP TARGET ‘B’ | TOP ‘A’ LANE | TOP RT BUMPER |
| I7 | 70 | A4J2-15 | OUT HOLE | [blank] | LT DROP TARGET ‘A’ | SAUCER | TOP LT BUMPER |

The two DROP TARGETS contacts are drawn in parallel to one diode.
The .05 µF marks appear at RT ‘B’ LANE, LT ‘A’ LANE, all four
thumpers, and across the separate cabinet tilt branches on the A7
sheet. A6 says all diodes are 1N4004, E 587-6 and all caps .05,
E 586-80.

W-1186-4c (schematics PDF page 6), A7 CABINET ASSY. WIRING.
Complete game switch branches, in cabinet-drawing label order.
COIN NO. 3 reaches I0, COIN NO. 1 reaches I1, and COIN NO. 2
reaches I2. The A6 blank symbols at these positions do not erase
the cabinet branches. The cabinet tilt pair is in parallel with
the playfield tilt. The two SLAM branches are parallel. The flipper
buttons join the common FLIP SW. RET., outside the switch matrix.

| Label | Strobe or return common | Return or individual lead |
| --- | --- | --- |
| SLAM (door) | 14 A4J3-3 via CR12 | I7 50 A4J3-16 |
| COIN NO. 2 | 14 A4J3-3 | I2 20 A4J3-11 |
| COIN NO. 1 | 14 A4J3-3 | I1 65 A4J3-10 |
| COIN NO. 3 | 14 A4J3-3 | I0 15 A4J3-9 |
| CREDIT RESET | 13 A4J3-2 via CR4 | I5 23 A4J3-14 |
| SLAM (cabinet) | 14 A4J3-3 via CR11 | I7 50 A4J3-16 |
| TILT PLUMB BOB | 13 A4J3-2 via CR10 | I6 27 A4J3-15 |
| TILT ROLL CAGE | 13 A4J3-2 via CR10 | I6 27 A4J3-15 |
| LEFT FLIPPER SWITCH | 70 A2J2-9 | 20 A3J2-2 |
| RIGHT FLIPPER SWITCH | 70 A2J2-9 | 10 A3J2-1 |
| TEST SW | 31 A3J2-7 | 10 A4J3-1 |

W-1187-1c (schematics PDF page 7) calls A4J2-1..5 ST 0..4
and A4J3-2..3 ST 0..1. A4J2-6 and A4J3-4 are KEY.
A4J2-7 and A4J3-5..8 are N/U. The A3J3/A4J4 connections
in W-1183-5c do not add a sixth switch strobe to the game harness.

Wire colour key (W-1187-1c): 1 RED, 2 BLUE, 3 YELLOW, 4 GREEN,
5 WHITE, 6 BROWN, 7 ORANGE, 8 BLACK, 9 GRAY, 0 NO TRACE.
