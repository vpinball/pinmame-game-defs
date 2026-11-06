# Skateball — playfield switch and coil wiring

Bally Game #1210, SWITCH MATRIX, PLAYFIELD A6, sheet W-1192-23C, schematic PDF page 10, SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`. Transcribed from the native 300 dpi page by a curation worker; **visually reviewed against the retained native-resolution render by the primary curator**. `[blank]` means an unlabeled drawn switch cell, not an independently established unused input. Matrix strobe and return labels and wire codes are printed on the drawing. Every cell is drawn with a contact and diode; this does not by itself determine emulator polarity.

| Return / connector / wire | ST 0 / A4J2-1 / 51 | ST 1 / A4J2-2 / 70 | ST 2 / A4J2-3 / 93 | ST 3 / A4J2-4 / 53 | ST 4 / A4J2-5 / 31 |
|---|---|---|---|---|---|
| I 0 / A4J2-8 / 54 | [blank] | [blank] | 3 DROP TARGET & 4 30 POINT REBOUNDS | [blank] | SPINNER |
| I 1 / A4J2-9 / 63 | MIDDLE RIGHT DROP TARGET | [blank] | B LANE | TOP RIGHT DROP TARGET | RIGHT OUT SPECIAL |
| I 2 / A4J2-10 / 57 | MIDDLE CENTER DROP TARGET | [blank] | A LANE | TOP CENTER DROP TARGET | LEFT OUT SPECIAL |
| I 3 / A4J2-11 / 78 | MIDDLE LEFT DROP TARGET | [blank] | E DROP TARGET | TOP LEFT DROP TARGET | RIGHT SLINGSHOT |
| I 4 / A4J2-12 / 60 | SAUCER | #3 LANE | T DROP TARGET | [blank] | LEFT SLINGSHOT |
| I 5 / A4J2-13 / 56 | [blank] | #2 LANE | A DROP TARGET | LOWER ROLLOVER BUTTON | RIGHT THUMPER BUMPER |
| I 6 / A4J2-14 / 65 | TILT | #1 LANE | K DROP TARGET | UPPER ROLLOVER BUTTON | BOTTOM THUMPER BUMPER |
| I 7 / A4J2-15 / 52 | OUTHOLE | [blank] | S DROP TARGET | RIGHT FLIPPER BUTTON | LEFT THUMPER BUMPER |

The page also draws these named playfield coils, sharing +43 VDC from A2J1-6 (wire 60), with individual returns as shown. The table transcribes every named branch on that coil drawing, including flippers. Parenthetical positions preserve the printed labels, not an inferred bank order.

| Return wire | Connector | Label |
|---:|---|---|
| 40 | A3J1-8 | LEFT FLIPPER |
| 40 | A3J1-8 | UPPER LEFT FLIPPER |
| 70 | A3J1-9 | RIGHT FLIPPER |
| 70 | A3J1-9 | UPPER RIGHT FLIPPER |
| 95 | A3J1-5 | OUTHOLE KICKER |
| 85 | A3J5-10 | 5 DROP TARGET |
| 78 | A3J5-11 | 3 DROP TARGET (MIDDLE) |
| 80 | A3J5-12 | 3 DROP TARGET (TOP) |
| 71 | A3J5-9 | LEFT THUMPER BUMPER |
| 74 | A3J5-15 | BOTTOM THUMPER BUMPER |
| 67 | A3J5-13 | RIGHT THUMPER BUMPER |
| 83 | A3J5-14 | LEFT SLINGSHOT |
| 18 | A3J5-8 | RIGHT SLINGSHOT |
| 67 | A3J1-2 | SAUCER |

The flippers are wired through the depicted N.O. flipper contacts, with N.C. contacts drawn at each lower flipper assembly. This transcription does not assert a PinMAME binding or the detailed construction of the unlabeled upper-flipper contacts. Notes specify coil diodes 1N4004 (E-587-6), switch diodes 1N4148 (E-587-14), capacitors .05 MFD (E-586-80), and a Germany-only .01 MFD at 500 V capacitor (E-586-65).
