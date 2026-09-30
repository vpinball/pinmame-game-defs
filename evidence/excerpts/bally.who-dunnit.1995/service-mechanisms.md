# WHO dunnit — Security board and mechanism service tests

Source: Bally *WHO dunnit* manual, PDF page 2 DIP chart, PDF page 4 attention notice, PDF page 45 printed 1-17, PDF page 46 printed 1-18, and PDF page 109 printed 2-27 reel assembly. Checked against the retained PDF on 2026-09-30. This is a factual condensation of the printed control/state tables, not a substitute for the operator's safety instructions.

The front quick-reference chart enumerates CPU DIP switches SW1–SW8. Its country rows are America `Off Off On On On On On On`, European `Off Off On On On Off On On`, French `Off Off On On On On Off Off`, German `Off Off On On On On On Off`, and Spain `Off Off On On Off On On On`. The chart also prints EPROM jumpers W1 In and W2 Out; these are jumpers, not public DIP bits.

The A-20425 reel assembly on printed 2-27 has three item-4 `14-8024` stepper motors labelled 1.8 degrees, three item-17 A-20511 reel opto PCB assemblies, and three item-6 A-19745-1 stepper motor PCBs. A 1.8-degree full step implies 200 full steps per revolution. The drawing does not establish motor phase sequence, the ROM's homing policy or the index-window width.

PDF pages 155–156 (printed 3-23–3-24) identify three separately fitted A-19043-1 Stepper Motor Driver P.C.B.s, one per reel. Each receives two public solenoid phase lines at J1-1/J1-3, +12 V DC at J1-4 from J116-2, and ground at J1-5 from J116-3. The left board takes 23/24 from J122-3/-4, center takes 25/26 from J122-1/-2, and right takes 27/28 from J126-7/-8; each board drives four motor leads through J2. The driver schematic shows input A/B through LM339 comparators to four transistor bridge legs. This establishes paired-phase board topology and fitted PCB count, but not live phase order, index window, or a home offset.

The page-4 notice calls the fitted board a **Security CPU Board** with a replaceable game-specific security chip. The display shows the nine-digit electronic ID at power-up. The page says this new board is not downward compatible with prior CPU boards and that the security chip/software must match the game.

| Printed test | Selection/state | Effect or checkpoint |
| --- | --- | --- |
| T.16 3-Bank Test | CYCLE | Cycle the motorized three-bank between up and down. |
| T.16 3-Bank Test | BANK UP | Move the bank up. |
| T.16 3-Bank Test | BANK DOWN | Move the bank down. |
| T.16 3-Bank Test | STOPPED / RUNNING | Stationary / permitted to move; switch states shown below. |
| T.17 Ramp Test | RAMP UP | Move the up/down ramp up. |
| T.17 Ramp Test | RAMP DOWN | Move the ramp down. |
| T.17 Ramp Test | RUNNING / REPEAT / STOPPED | Move if necessary / fire the selected coil irrespective of position / stationary; switch state shown below. |
| T.18 Reel Test | LEFT REEL | Select and start the left reel. |
| T.18 Reel Test | CENTER REEL | Select and start the center reel. |
| T.18 Reel Test | RIGHT REEL | Select and start the right reel. |
| T.18 Reel Test | STOP TEST | Stop all reels; the selected reel lamp is lit during the test and the current index-switch state is shown below. |

T.16 and T.17 use `+`/`-` to select and Enter to toggle execution; Escape leaves the test. T.18 uses `+`/`-` to select a reel or stop; Enter exits only while STOP TEST is selected. These are ROM-owned diagnostic checkpoints suitable for a future controlled harness run.
