# Bad Cats Seafood Wheel driver

Williams D-12046, the one-page schematic retained through IPDB machine 127. The drawing calls out P2 at the stepper and J1 at the game's harness. Its winding labels use an overbar on the second end of each pair.

| J1 pin | Signal | Harness color as printed |
| --- | --- | --- |
| 1 | Matrix row through D1 and Q9 | WHT-YEL |
| 2 | Key | [blank] |
| 3 | Matrix column at Q9 | GRN-BLU |
| 4 | Input A | BRN-GRY |
| 5 | Input B | BRN-VIO |
| 6 | +12V Power | GRY-YEL |
| 7 | Ckt Gnd | BLK-YEL |

| P2 pin | Terminal | 14-7948 / #3102 wire | 14-7948-1 / #3100 wire |
| --- | --- | --- | --- |
| 1 | B̄ | BLK | RED |
| 2 | B | GRN | BRN |
| 3 | Key | [blank] | [blank] |
| 4 | n/c | [blank] | [blank] |
| 5 | Ā | BRN | GRN |
| 6 | A | RED | BLK |

The board outline shows Opto 1 beside the shaft opening. The opto drives a PNP stage (Q9, 2N3906) between matrix row and column through D1. The channel pairs use four sections of the LM339 and eight switching transistors. This is one reversible two-winding stepper. The two CPU outputs enter the control board as A and B; neither output by itself specifies direction.
