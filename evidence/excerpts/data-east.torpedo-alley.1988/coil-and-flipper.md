# Torpedo Alley coil, flash-lamp, special-solenoid, and flipper tables

## CPU Controlled Coil and Flash Lamp Connections — literal printed cells

| Printed number | Printed description | CPU wire | Device wire | Power | Driver | Printed device | Qty |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| 01L | Destroyer Hotdog | GRY-BRN | VIO-GRN | BRN (+32 V) | Q46 | #906 | 2 |
| 02L | Release Torpedo Hotdog | GRY-RED | VIO-RED | BRN (+32 V) | Q45 | #906 | 2 |
| 03L | Flagship Hotdog | GRY-ORN | VIO-ORN | BRN (+32 V) | Q44 | #906 | 2 |
| 04L | Aircraft Carrier Hotdog | GRY-YEL | VIO-YEL | BRN (+32 V) | Q43 | #906 | 2 |
| 05L | Special Hotdog | GRY-GRN | VIO-GRN | BRN (+32 V) | Q42 | #906 | 2 |
| 06L | Cruiser Hotdog | GRY-BLU | VIO-BLU | BRN (+32 V) | Q41 | #906 | 2 |
| 07L | Scope | GRY-VIO | VIO-BLK | BRN (+32 V) | Q40 | #89 | 2 |
| 08L | Insert Top | GRY-BLK | VIO-GRY | BRN (+32 V) | Q39 | #89 | 2 |
| 09 | Left Pair | BRN-BLK | BRN-BLK | RED | Q30 | #89 | 2 |
| 10 | Left/Right Coil Relay | BRN-RED | BLK-RED | +32 V | Q29 | K1 relay | 1 |
| 11 | General Illumination Relay | BRN-ORN | BRN-ORN | +32 V | Q28 | K1 relay | 1 |
| 12 | Unused Solenoid 12 | BRN-YEL | N.C. | N.C. | Q27 | N.C. | 1 |
| 13 | Unused Solenoid 13 | BRN-GRN | N.C. | N.C. | Q26 | N.C. | 1 |
| 14 | Center Pair | BRN-BLU | BRN-BLU | RED | Q25 | #89 | 2 |
| 15 | Right Pair | BRN-VIO | BRN-VIO | RED | Q24 | #89 | 2 |
| 16 | Trough | BRN-GRY | BRN-GRY | RED | Q23 | 23-840 | 1 |
| 01R | Laser Kicker | GRY-BRN | BLK-BRN | VIO-YEL (+50 V) | Q46 | 23-800 | 1 |
| 02R | Left Kickback | GRY-RED | BLK-RED | VIO-YEL (+50 V) | Q45 | 24-900 | 1 |
| 03R | Vertical Up Kicker | GRY-ORN | BLK-ORN | ORN (+32 V) | Q44 | 23-800 | 1 |
| 04R | Center Kickback | GRY-YEL | BLK-YEL | VIO-YEL (+50 V) | Q43 | 24-900 | 1 |
| 05R | 3-Bank Drop Target Reset | GRY-GRN | BLK-GRN | ORN (+32 V) | Q42 | 23-1200 | 1 |
| 06R | Knocker | GRY-BLU | BLK-BLU | ORN (+32 V) | Q41 | 23-800 | 1 |
| 07R | Outhole | GRY-VIO | BLK-VIO | ORN (+32 V) | Q40 | 23-840 | 1 |
| 08R | Sinking Ship | GRY-BLK | BLK-GRY | ORN (+32 V) | Q39 | 30-800 | 1 |

The diagnostics prose literally says coil 10 switches `+34 volts` between the `left` and `right` sets. The connection drawing identifies K1 as the `LEFT/RIGHT COIL RELAY`. The L/R and SP printed numbers above are manual aliases only; neither table prints a PinMAME public special-solenoid address. The rendered connection drawing explicitly marks every 01L-08L branch with `(2)`, so each quantity of two is physical manual evidence rather than an inference from the device name.

## Switch Triggered Solenoids — literal description cells

| Printed number | Description | Control line | Power line | Trigger line | Driver | Coil type |
| --- | --- | --- | --- | --- | --- | --- |
| SP1 | Center Thumper Bumper | BLU-ORN / CPU CN19-3 | RED / PS CN3-6 | ORN-BRN / CPU CN18-2 | Q8 | 23-800 |
| SP2 | Right Thumper Bumper | BLU-RED / CPU CN19-4 | RED / PS CN3-6 | ORN-RED / CPN CN18-3 | Q9 | 23-800 |
| SP3 | Left Slingsho | BLU-YEL / CPU CN19-6 | RED / PS CN3-6 | ORN-YEL / CPU CN18-4 | Q10 | 23-800 |
| SP4 | Left Thumper Bumper | BLU-BRN / CPU CN19-7 | RED / PS CN3-6 | ORN-BRN / CPU CN18-5 | Q11 | 23-800 |
| SP5 | Right Slingshot | BLU-GRN / CPU CN19-8 | RED / PS CN3-6 | ORN-GRN / CPU CN18-8 | Q12 | 23-800 |
| SP6 | NOT USED | -- / CPU CN19-9 | -- / PS CN3-6 | -- / CPU CN18-9 | Q13 | -- |

The printed special-coil wiring diagram instead labels SP2 `CENTER THUMPER BUMPER` and SP1 `RIGHT THUMPER BUMPER`. The location plan and the table above print SP1 at the center bumper and SP2 at the right bumper; this contradiction is retained as a conflict. `Left Slingsho` is the table's literal truncated cell, not a curator typo. Three other rendered anomalies are also preserved literally: 01L and 05L both print device wire `VIO-GRN`, SP1 and SP4 both print trigger wire `ORN-BRN`, and SP2 prints connector prefix `CPN CN18-3` rather than `CPU`.

## Flipper Solenoids

| Description | Flipper GND (CPU to Cab) | Flipper GND (Cab to Coil) | Power line (PPB to Coil) | Coil type |
| --- | --- | --- | --- | --- |
| Left Flipper | ORN-BLU / CPU CN19-2 | BLU-GRY / 1M/F-24 | GRY-YEL / PPB J7-5 | 23-700/30-2600 |
| Right Flipper | ORN-RED / CPU CN19-1 | BLU-VIO / 1M/F-21 | BLK-WHT / PPB J7-1,2 | 23-700/30-2600 |
| Upper Right Flipper | ORN-RED / CPU CN19-1 | WHT-BLK / 1M/F-19 | BLK-WHT / PPB J7-1,2 | 23-700/30-2600 |

The coil part-number chart prints quantities: 8 × 23-800 (`090-5001-00`), 2 × 24-900 (`090-5002-00`), 2 × 23-840 (`090-5005-00`), 1 × 23-1200 (`090-5008-00`), 1 × 30-800 (`090-5010-00`), and 3 × 23-700/30-2600 (`090-5013-00`).
