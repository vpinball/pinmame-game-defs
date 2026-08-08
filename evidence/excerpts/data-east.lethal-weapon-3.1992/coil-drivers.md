# Lethal Weapon 3 (Data East 1992) - Coil drivers and the Left/Right relay

Transcribed by hand from a 400 dpi render of printed page 28 and 29 (PDF 32 and 33). The contributor-supplied manual has no text layer at all (93 pages, 0 characters), so nothing here came from `pdftotext`.

## Drives 1-8, switched between a left and a right set by the relay

| Drive | Transistor | Wire | Left (coil) | Coil type | Right (flash lamps) |
| --- | --- | --- | --- | --- | --- |
| 1 | Q46 | GRY-BRN CN-11 | Outhole | 23-840 | (4) No. 89 (2 playfield, 2 insert) |
| 2 | Q45 | GRY-RED CN-11 | Trough Eject | 23-840 | (4) No. 89 (3 back panel, 1 playfield) |
| 3 | Q44 | GRY-ORN CN-11 | NO COIL THIS LOCATION | - | (4) No. 89 (3 playfield, 1 insert) |
| 4 | Q43 | GRY-YEL CN-11 | Left Eject | 23-840 | (3) No. 89 (3 playfield) |
| 5 | Q42 | GRY-GRN CN-11 | Right Eject | 23-840 | (4) No. 89 (2 playfield, 2 insert) |
| 6 | Q41 | GRY-BLU CN-11 | Left 3 Bank | 23-800 | (3) No. 89 (3 playfield) |
| 7 | Q40 | GRY-VIO CN-11 | Right 3 Bank | 23-800 | (4) No. 89 (2 playfield, 2 insert) |
| 8 | Q39 | GRY-BLK CN-11 | Knocker | 23-800 | (4) No. 89 (3 playfield, 1 insert) |

## Drives 9-16, direct on CN-12

| Drive | Transistor | Wire | Device |
| --- | --- | --- | --- |
| 9 | Q30 | BRN-BLK CN-12 | IWSC Building Flash Lamps |
| 10 | Q29 | BLK-RED CN-12 | Left/Right Coil Relay |
| 11 | Q28 | BRN-ORN CN-12 | General Illumination Relay |
| 12 | Q27 | BRN-YEL CN-12 | Ball Launch |
| 13 | Q26 | BRN-GRN CN-12 | NO COIL AT THIS LOCATION |
| 14 | Q25 | BRN-BLU CN-12 | (no coil type printed; see the note below) |
| 15 | Q24 | WHT-VIO CN-12 | VUK |
| 16 | Q23 | BRN-GRY CN-12 | Flash Lamps |

## Drives 17-22, the CPU Controlled Auxiliary Solenoids

| Drive | Description | Control | Power | Transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 20 | Left Slingshot | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Kickback | BLU-BLK CPU CN19-9 | RED PS CN3-6 | Q13 | 23-800 |

## Flipper Solenoids (printed as its own unnumbered table)

| Flipper | Assembly | Control | Flipper PCB | Power | Coil type |
| --- | --- | --- | --- | --- | --- |
| Left | 090-5030-00 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-1100 |
| Right | 090-5030-00 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN1-1 | 23-1100 |

There is no upper flipper of either hand on this table.

## Coil and flash location drawing

The committed crop `coil-flash-location.webp` preserves the complete printed-page-28 playfield drawing at enough resolution to read its callouts. Its numbered callouts cover coils 15-22. The readable left-series callouts are `1L`, `2L`, `3L`, `4L`, `5L`, `6L` and `7L`; no readable `8L` appears. The `6L` callout sits on the center three-bank and `7L` sits on the right three-bank, while `3L` appears in the lower-right shooter-housing/cabinet extension even though the Special Coil Wiring Diagram prints `NO COIL THIS LOCATION` for drive 3. The right-series drawing shows `1R` through `8R`, with repeated callouts where a drive feeds multiple effects. The `6L` callout settles the otherwise misleading left/right table label for drive 6, while the unresolved `3L` contradiction is preserved as a first-class conflict. The drawing supplies feature-level locations, not exact winding centers or a one-to-one survey of every flash bulb socket.

## Reconciliation, which is NOT part of the printed transcription

The printed diagram draws a MARS LIGHT through a GRY lead, a 1 AMP S.B. fuse and a BLU lead to
PSCN 4, on a node that both drive 13 and drive 14 touch, and prints "NO COIL AT THIS LOCATION"
against drive 13. The drawing alone does not say which drive energises the beacon.

The retained known-working script settles it: `SolCallback(14) = "SolRotateBeacons"`, commented
"Mars Light aka Beacon". That is a script assertion, not a manual one, and is separated here so
the transcription above stays a record of what the page prints.
