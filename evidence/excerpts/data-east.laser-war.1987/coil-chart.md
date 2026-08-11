# Laser War coil/transistor evidence (community technical chart)

Human transcription checked cell-by-cell against a retained 300 dpi render of the 2021 Inkochnito community technical chart. The chart, not the incomplete ManualsLib page-image archive, is the source for these cells.

## Switched, CPU controlled auxiliary and constant-power solenoids — printed rows 1L-16

The chart merges each Q46-Q39 transistor cell across its L/R pair; the applicable transistor is repeated below so every row is independently usable. Genuinely blank printed cells are `[blank]`.

| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil or Flash Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1L | Explosion Flasher | Q46 | CPU to DB | Vio-Brn | CPU CN11-1 | Brn | 4M-8 | 32V L | #89 |
| 1R | Ramp Multiplier Flasher | Q46 | Gry-Brn | Blk-Brn | to diode board | Orn | 4M-9 | 32V R | #89 |
| 2L | Red Hot Dog Flasher | Q45 | CPU to DB | Vio-Red | CPU CN11-3 | Brn | 4M-8 | 32V L | #89 |
| 2R | Green Shield Flasher | Q45 | Gry-Red | Blk-Red | to diode board | Orn | 4M-9 | 32V R | #89 |
| 3L | Yellow Hot Dog Flasher | Q44 | CPU to DB | Vio-Orn | CPU CN11-4 | Brn | 4M-8 | 32V L | #89 |
| 3R | Warriors (Back Glass) Flasher | Q44 | Gry-Orn | Blk-Orn | to diode board | Orn | 3F2-6 | 32V R | #89 |
| 4L | Blue Hot Dog Flasher | Q43 | CPU to DB | Vio-Yel | CPU CN11-5 | Brn | 4M-8 | 32V L | #89 |
| 4R | Laser Wire (Back Glass) Flasher | Q43 | Gry-Yel | Blk-Yel | to diode board | Orn | 3F2-6 | 32V R | #89 |
| 5L | Ion Cannon Flasher | Q42 | CPU to DB | Vio-Grn | CPU CN11-6 | Brn | 4M-8 | 32V L | #89 |
| 5R | Knocker | Q42 | Gry-Grn | Blk-Grn | to diode board | Orn | - | 32V R | 23-800 |
| 6L | Mars Yellow | Q41 | CPU to DB | Vio-Blu | CPU CN11-7 | Brn | 4M-8 | 32V L | 23-800 |
| 6R | Not Used | Q41 | Gry-Blu | [blank] | to diode board | [blank] | [blank] | [blank] | [blank] |
| 7L | Mars Red Flasher | Q40 | CPU to DB | Vio-Blk | CPU CN11-8 | Brn | 4M-8 | 32V L | #89 |
| 7R | Not Used | Q40 | Gry-Vio | [blank] | to diode board | [blank] | [blank] | [blank] | [blank] |
| 8L | Mars Blue Flasher | Q39 | CPU to DB | Vio-Gry | CPU CN11-9 | Brn | 4M-8 | 32V L | #89 |
| 8R | Not Used | Q39 | Gry-Blk | [blank] | to diode board | [blank] | [blank] | [blank] | [blank] |
| 9 | Ball Trough Eject | Q30 | CPU | Brn-Blk | CN12-1 | Red | PS CN3-6 | 32V | 23-840 |
| 10 | L/R Power Relay | Q29 | CPU | Brn-Red | CN12-2 | Red | PS CN3-6 | 32V | Relay: 24VDC |
| 11 | General Illumination Relay | Q28 | CPU | Brn-Orn | CN12-4 | [blank] | PS CN3-6 | 32V | Relay: 24VDC |
| 12 | Red Eject | Q27 | CPU | Brn-Yel | CN12-5 | Red | PS CN3-6 | 32V | 27-1500 |
| 13 | Yellow Eject | Q26 | CPU | Brn-Grn | CN12-6 | Red | PS CN3-6 | 32V | 27-1500 |
| 14 | Blue Eject | Q25 | CPU | Brn-Blu | CN12-7 | Red | PS CN3-6 | 32V | 27-1500 |
| 15 | Laser Kick (Relay) | Q24 | CPU | Brn-Vio | CN12-8 | Red (Relay); Blu-Yel (Coil) | PS CN3-6; FPS CN3-6 | 32V (Relay); 50V (Coil) | Relay: 24VDC; Coil: 23-900 |
| 16 | Outhole | Q23 | CPU | Brn-Gry | CN12-9 | Red | PS CN3-6 | 32V | 23-840 |

## Reconciliation to PinMAME public addresses and semantic kinds

- The chart prints RAMP MULTIPLIER as `1R`. PinMAME's relay-selected right bank maps printed 1R-8R to public addresses 25-32, and the retained script independently binds `SolCallback(25)` to the ramp-multiplier flasher.
- The chart prints MARS YELLOW as coil type `23-800`, while its MARS RED and MARS BLUE partners are `#89` lamps. Pinned `s11.c` describes all three as Mars flashers, so the definition records `kind: flasher` while preserving the printed device-type conflict.
- Rows 17-22 are transcribed separately with the chart's additional CPU-board connector fields.

Source document SHA-256: `30a1def10178a2cf7e753046ed44f07d01075a6333791669e4fe0c4e165ddfe7`
