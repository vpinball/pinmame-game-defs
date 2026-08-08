# Laser War coil/transistor evidence (PDF pages 23-24; printed pages 21-22)

Human transcription checked cell-by-cell against 400 dpi Poppler renders. The PDF text layer was not used to decide cells, and the scan's damaged schematic pages were not used.

## Coil I.D. Chart — literal printed cells (PDF page 23; printed page 21)

| Printed coil label | Printed description | Drive wire | Power wire | Printed drive transistor | Printed device type |
| --- | --- | --- | --- | --- | --- |
| 1L | EXPLOSION | VIO-BRN | BRN | Q 46 | #89 BULBS |
| 2L | RAMP MULTIPLIER | BLK-BRN | ORN | Q 46 | #89 BULBS |
| 2L | RED HOT DOG | VIO-RED | BRN | Q 45 | #89 BULBS |
| 2R | GREEN SHIELD | BLK-RED | ORN | Q 45 | #89 BULBS |
| 3L | YELLOW HOT DOG | VIO-ORN | BRN | Q 44 | #89 BULBS |
| 3R | WARRIIRS (Back Glass) | BLK-ORN | ORN | Q 44 | #89 BULBS |
| 4L | BLUE HOT DOG | VIO-YEL | BRN | Q 43 | #89 BULBS |
| 4R | LASER WIRE (Back Glass) | BLK-YEL | ORN | Q 43 | #89 BULBS |
| 5L | ION CANNON | VIO-GRN | BRN | Q 42 | #89 BULBS |
| 5R | KNOCKER | BLK-GRN | ORN | Q 42 | COIL: 23-800 |
| 6L | MARS YELLOW | VIO-BLU | BRN | Q 41 | COIL: 23-800 |
| 6R | NOT USED | BLK-BLU | ORN | Q 41 |  |
| 7L | MARS RED | VIO-BLK | BRN | Q 40 | #89 BULBS |
| 7R | NOT USED | BLK-VIO | ORN | Q 40 |  |
| 8L | MARS BLUE | VIO-GRY | BRN | Q 39 | #89 BULBS |
| 8R | NOT USED | BLK-GRY | ORN | Q 39 |  |
| 9 | BALL TROUGH EJECT | BLK-BRN | RED | Q 30 | COIL: 23-840 |
| 10 | L/R POWER RELAY | BRN-RED | RED | Q 29 | RELAY: 24 VDC |
| 11 | G. I. RELAY | BRN-ORN | RED | Q 28 | RELAY: 24 VDC |
| 12 | RED EJECT | BRN-YEL | RED | Q 27 | COIL: 27-1500 |
| 13 | YELLOW EJECT | BRN-GRN | RED | Q 26 | COIL: 27-1500 |
| 14 | BLUE EJECT | BRN-BLU | RED | Q 25 | COIL: 27-1500 |
| 15 | LASER KICK RELAY | BRN-VIO | RED | Q 24 | RELAY: 24 VDC |
| 16 | OUTHOLE | BRN-GRY | RED | Q 23 | COIL: 23-840 |

The chart above literally prints `2L` twice: once for RAMP MULTIPLIER and once for RED HOT DOG. It also literally prints `WARRIIRS (Back Glass)` and prints `COIL: 23-800` for MARS YELLOW. Those cells are not silently corrected here.

## Playfield Coil Location Illustration list — literal printed cells (PDF page 24; printed page 22)

| Printed item | Printed description | Printed device type / setting |
| --- | --- | --- |
| 1L | EXPLOSION | #89 BULBS |
| 1R | RAMP MULTIPLIER | #89 BULBS |
| 2L | RED HOT DOG | #89 BULBS |
| 2R | GREEN SHIELD | #89 BULBS |
| 3L | YELLOW HOT DOG | #89 BULBS |
| 3R | WARRIORS (BACK GLASS) | #89 BULBS |
| 4L | BLUE HOT DOG | #89 BULBS |
| 5L | ION CANNON | #89 BULBS |
| 5R | KNOCKER | COIL: 23-800 |
| 6L | MARS YELLOW | COIL: 23-800 |
| 6R | NOT USED | — |
| 7L | MARS RED | #89 BULBS |
| 7R | NOT USED | — |
| 8L | MARS BLUE | #89 BULBS |
| 8R | NOT USED | — |
| 9 | BALL TROUGH EJECT | COIL: 23-840 |
| 10 | L/R POWER RELAY | RELAY: 24 VDC |
| 11 | G.I. RELAY | RELAY: 24 VDC |
| 12 | RED EJECT | COIL: 27-1500 |
| 13 | YELLOW EJECT | COIL: 27-1500 |
| 14 | BLUE EJECT | COIL: 27-1500 |
| 15 | LASER KICK RELAY | RELAY: 24 VDC |
| 16 | OUTHOLE | COIL: 23-840 |
| 30 | INSTALL ADD-A-BALL | OFF |
| 31 | INSTALL 5 BALL PLAY | OFF |
| 32 | INSTALL NOVELTY PLAY | OFF |
| 33 | INSTALL EXTRA EASY | OFF |
| 34 | INSTALL EASY | OFF |
| 35 | INSTALL MEDIUM | ON |
| 36 | INSTALL HARD | OFF |
| 37 | INSTALL EXTRA HARD | OFF |
| 38 | ARROW MEMORY | ON |
| 39 | RAMP SPOTS BONUS | ON |
| 40 | ATTRACT MODE SOUNDS | ON |
| 41 | W.A.R. LANES EXTRA BALL | ON |
| 42 | TARGETS TO LIGHT SPECIAL | 06 |
| 43 | RAMP LIGHTS FLIPPER LANES | OFF |
| 44 | FLIPPER RETURN LANES | OFF |
| 45 | LASER KICK | ON |
| 46 | AUDITS RESET | OFF |
| 47 | RESTORE FACTORY SETTINGS | OFF |

This second printed list corrects RAMP MULTIPLIER to `1R` and spells WARRIORS normally, but it repeats `COIL: 23-800` for MARS YELLOW. It omits the `4R` LASER WIRE row that is present in the Coil I.D. Chart.

## Reconciliation to PinMAME public addresses and semantic kinds

The raw printed cells above remain the evidence. The following are explicit resolutions, not transcription edits:

- Each transistor pairs one `VIO-*` / `BRN` left drive with one `BLK-*` / `ORN` right drive. RAMP MULTIPLIER is `BLK-BRN` / `ORN` on Q 46, paired with `1L` EXPLOSION (`VIO-BRN` / `BRN`, Q 46), so the duplicated chart label `2L` is electrically `1R`. The location list independently prints `1R`. In PinMAME's relay-selected bank, `1R` is public address 25. The retained script corroborates this with `SolCallback(25) = "SolFlasherRampMultiplier"`, followed by public 26 Green Shield (`2R`) and public 29 Knocker (`5R`).
- The chart and location list both print MARS YELLOW as `COIL: 23-800`, while the same two lists print MARS RED and MARS BLUE as `#89 BULBS`. Pinned `s11.c` lines 1131-1135 independently describe 'the yellow, red & blue mars flashers' as one two-bulb-per-colour group. The canonical `kind: flasher` is therefore the recorded resolution, while the printed device-type disagreement remains a first-class conflict.
- The Coil I.D. Chart's `WARRIIRS (Back Glass)` is retained verbatim above. The following location list prints `WARRIORS (BACK GLASS)`, so the canonical label normalizes the evident chart typo to `Warriors (Back Glass)`.
- Public addresses 25-32 are the relay-selected right bank corresponding to printed 1R-8R; printed 6R-8R (public 30-32) are NOT USED. Public addresses 9-16 are printed directly. Special switched-coil circuits 17-22 are described by the manual prose, but their address-to-device mapping falls in the damaged schematic section and is deliberately not inferred.

Source document SHA-256: `f6c6a09a6c9be42d8851790a5b40060fef7a4dbd6e452e1aa89af4765783a3db`
