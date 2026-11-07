# Pro diagnostic coil wires: complete comparison

All 28 pinned coil-selector frames were inspected at their native pixels, with nearest-neighbor enlargement as a reading aid. Frame paths and hashes are in `tools/seeds/stern/x-men-pro-2012-coil-wiring.json`, tied to the existing immutable runtime seed. The own Pro chart is PDF 16 / printed 14, SHA-256 d6ae672cf65299ff60e108a6b039275dd2393619b6c9e930c681cd285f635fbe. This table preserves complete literal wire cells; spaces normalize line breaks only. No selector omission establishes non-fitment.

| Output | ROM power | ROM control | Own Pro power cell | Own Pro control | Comparison |
| ---: | --- | --- | --- | --- | --- |
| 1 | YEL-VIO | BRN-BLK | YEL-VIO | BRN-BLK | Wire identities agree |
| 2 | YEL-VIO | BRN-RED | YEL-VIO | BRN-RED | Wire identities agree |
| 3 | YEL-VIO | BRN-ORG | YEL-VIO | BRN-ORG | Wire identities agree |
| 4 | VIO-YEL | BRN-YEL | VIO-YEL | BRN-YEL | Wire identities agree |
| 5 | YEL-VIO | BRN-GRN | YEL-VIO | BRN-GRN | Wire identities agree |
| 6 | YEL-VIO | BRN-BLU | YEL-VIO | BRN-BLU | Wire identities agree |
| 7 | YEL-VIO | BRN-VIO | YEL-VIO | BRN-VIO | Wire identities agree |
| 8 | RED-WHT | BRN-GRY | RED-WHT | BRN-GRY | Wire identities agree |
| 9 | YEL-VIO | BLU-BRN | YEL-VIO | BLU-BRN | Wire identities agree |
| 10 | YEL-VIO | BLU-RED | YEL-VIO | BLU-RED | Wire identities agree |
| 11 | YEL-VIO | BLU-ORG | YEL-VIO | BLU-ORG | Wire identities agree |
| 12 | RED-YEL | BLU-YEL | GRY-YEL 3A | BLU-YEL | Power differs |
| 13 | YEL-VIO | BLU-GRN | YEL-VIO | BLU-GRN | Wire identities agree |
| 14 | YEL-VIO | BLU-BLK | YEL-VIO | BLU-BLU | Control differs |
| 15 | GRY-YEL | ORG-GRY | GRY-YEL-3A Fuse-RED-YEL | ORG-GRY | ROM omits compound fuse-path detail |
| 16 | BLU-YEL | ORG-VIO | BLU-YEL-3A Fuse-RED-YEL | ORG-VIO | ROM omits compound fuse-path detail |
| 17 | ORG | VIO-BRN | ORG | VIO-BRN | Wire identities agree |
| 18 | ORG | VIO-RED | ORG | VIO-RED | Wire identities agree |
| 21 | ORG | VIO-GRN | ORG | VIO-GRN | Wire identities agree |
| 22 | ORG | VIO-BLU | ORG | VIO-BLU | Wire identities agree |
| 24 | RED | VIO-GRY | RED | VIO-GRY | Wire identities agree |
| 25 | ORG | BLK-BRN | ORG | BLK-BRN | Wire identities agree |
| 26 | BRN | BLK-RED | BRN | BLK-RED | Wire identities agree |
| 27 | ORG | BLK-ORG | ORG | BLK-ORG | Wire identities agree |
| 28 | ORG | BLK-YEL | ORG | BLK-YEL | Wire identities agree |
| 29 | ORG | BLK-GRN | ORG | BLK-GRN | Wire identities agree |
| 31 | ORG | BLK-VIO | ORG | BLK-VIO | Wire identities agree |
| 32 | BRN | BLK-GRY | VIO-YEL | BLK-GRY | Power differs |

The Pro chart governs physical harness facts. Output 12 has only GRY-YEL 3 A printed, so no RED-YEL continuation is invented. Outputs 15/16 preserve their complete printed fuse-path cells; output 16 begins BLU-YEL. Output 14 retains chart BLU-BLU alongside display BLU-BLK. Output 32 retains chart VIO-YEL alongside display BRN. These are wiring details, not incompatible claims about device identity, address or fitment; no new machine conflict is asserted. The chart’s copied J8 cells and exact-board correction are handled separately in `pro-sam-board-connectors.md`.
