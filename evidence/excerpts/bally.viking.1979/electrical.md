# Viking switch rows and coil wiring

Source: manual PDF p43, W-1192-21c SWITCH MATRIX / playfield wiring.
Method: primary GPT-6.1-Sol visual/transcription review; Windows OCR only locates cells.

Every drawn playfield switch contact is open. The schematic has five strobe branches ST0..ST4; the public column is derived from the sequential BY35 convention (strobe * 8 + row + 1). Blank label cells remain [blank]; physical cabinet contacts are named in the separate printed self-test table.

| Row | Return wire | Return connector |
| --- | --- | --- |
| I0 | 54 | A4J2-8 |
| I1 | 56 | A4J2-9 |
| I2 | 57 | A4J2-10 |
| I3 | 58 | A4J2-11 |
| I4 | 60 | A4J2-12 |
| I5 | 63 | A4J2-13 |
| I6 | 65 | A4J2-14 |
| I7 | 70 | A4J2-15 |

| Strobe | Wire | Connector |
| --- | --- | --- |
| ST0 | 51 | A4J2-1 |
| ST1 | 93 | A4J2-2 |
| ST2 | 52 | A4J2-3 |
| ST3 | 53 | A4J2-4 |
| ST4 | 31 | A4J2-5 |

The complete printed self-test labels, including all blanks, are in identification.md.

## Coil endpoints, whole drawn playfield coil region

| Printed coil | Wire | Endpoint |
| --- | --- | --- |
| LEFT FLIPPER | 40 | A3J1-8 |
| RIGHT FLIPPER | 70 | A3J1-9 |
| OUTHOLE KICKER | 95 | A3J1-5 |
| KICK UP SAUCER | 74 | A3J5-10 |
| TOP LEFT THUMPER BUMPER | 78 | A3J5-11 |
| KICK DOWN SAUCER | 75 | A3J5-12 |
| TOP RIGHT THUMPER BUMPER | 71 | A3J5-9 |
| LEFT SIDE THUMPER BUMPER | 85 | A3J5-15 |
| RIGHT SIDE THUMPER BUMPER | 80 | A3J5-13 |
| LEFT SLINGSHOT | 83 | A3J5-14 |
| RIGHT SLINGSHOT | 18 | A3J5-8 |
| TOP SAUCER | 81 | A3J5-7 |
| 3 DROP TARGET 1 (TOP) | 67 | A3J2-10 |
| 3 DROP TARGET 2 | 74 | A3J2-11 |
| 3 DROP TARGET 3 (BOTTOM) | 81 | A3J2-12 |
| 3 DROP TARGET RESET | 91 | A3J1-2 |
| IN LINE DROP TARGET RESET | 81 | A3J1-3 |

The common coil supply is printed +43 VDC, wire60 through a 1A S.B. fuse to wire30. Coils have suppression diodes; flippers have power/hold windings and an EOS contact, not a CPU-controlled pair of outputs. General illumination is separately printed 5.9 VAC, from A2J1-8 (wire10), A2J1-5 (wire70), return A2J1-2 (wire40) and A2J1-1 (wire50). It has no PinMAME lamp/GI address.
