# Bram Stoker's Dracula — Switch Locations

Transcribed from `Dracula_Bram_Stoker_OPS.pdf`, PDF page 109, printed page 2-46, the
SWITCH LOCATIONS parts list and playfield diagram. Rendered at 300 dpi grayscale with
`pdftoppm`.

| Item | Switch/Part No. | Where Used |
| --- | --- | --- |
| F1 | SW-1A-193 | Lwr Rt. Flipper EOS |
| F2 | 5490-12451-00 | Lwr Rt. Flipper Cab. |
| F3 | SW-1A-193 | Lwr Lt. Flipper EOS |
| F4 | 5490-12451-00 | Lwr Lt. Flipper Cab. |
| F5-F8 | *(no row printed)* | *(absent)* |
| 13 | 20-9663-1 | Start Button |
| 14 | A-6502-A † | Plumb Bob Tilt |
| 15 | 5647-12693-31 | L. Drop Target |
| 16 | 5647-12693-19 | L. Drop Score |
| 17 | 5647-12693-04 | Shooter Lane |
| 18 | (blank) | Not Used |
| 21 | SW-1A-117 † | Slam Tilt |
| 22 | 5643-09288-00 † | Coin Door Closed |
| 23 | (blank) | Not Used |
| 24 | 5643-09288-00 † | Always Closed |
| 25 | 5647-12693-19 | Top 3-lane Left |
| 26 | 5647-12693-19 | Top 3-lane Middle |
| 27 | 5647-12693-19 | Top 3-lane Right |
| 28 | 5647-12693-21 | R. Ramp Score |
| 31 | 5647-12693-19 | Under Shooter Ramp |
| 32-33 | (blank) | Not Used |
| 34 | A-15896-1 | Launch Ball |
| 35 | 5647-12693-19 | Left Drain |
| 35 (sic, printed twice; physical address 36) | 5647-12693-19 | Left Return |
| 37 | 5647-12693-19 | Right Return |
| 38 | 5647-12693-19 | Right Drain |
| 41 | 5647-12693-08 | Trough 1 Ball |
| 42 | 5647-09957-00 | Trough 2 Balls |
| 43 | 5647-09957-00 | Trough 3 Balls |
| 44 | 5647-09957-00 | Trough 4 Balls |
| 45-47 | (blank) | Not Used |
| 48 | 5647-12133-12 | Outhole |
| 51 | A-14315 (LED) + A-14316 (Trans) | Opto T.R. Lane |
| 52 | A-14315 (LED) + A-14316 (Trans) | Opto Mag. Lt. Pocket |
| 53 | A-14315 (LED) + A-14316 (Trans) | Opto Castle 1 |
| 54 | A-14315 (LED) + A-14316 (Trans) | Opto Castle 2 |
| 55 | A-14315 (LED) + A-14316 (Trans) | Opto Wire Ramp Popper |
| 56 | A-14315 (LED) + A-14316 (Trans) | Opto Crypt Popper |
| 57 | A-14315 (LED) + A-14316 (Trans) | Opto Castle 3 |
| 58 | 5647-12693-13 | Mystery Hole |
| 61 | SW-11A-37 | Left Jet Bumper |
| 62 | SW-11A-37 | Right Jet Bumper |
| 63 | SW-11A-37 | Bottom Jet Bumper |
| 64 | SW-1A-114 (Kick) + SW-1A-120 (Score) * | Left Sling |
| 65 | SW-1A-114 (Kick) + SW-1A-120 (Score) * | Right Sling |
| 66 | A-14691-2 | Left 3-bank Top |
| 67 | A-14691-4 | Left 3-bank Middle |
| 68 | A-14691-2 | Left 3-bank Bottom |
| 71 | A-14315 (LED) + A-14316 (Trans) | Opto Castle Popper |
| 72 | A-14315 (LED) + A-14316 (Trans) | Opto Coffin Popper |
| 73 | A-14315 (LED) + A-14316 (Trans) | Opto L. Ramp Entry |
| 74-76 | (blank) | Not Used |
| 77 | 5647-12693-36 | R. Ramp Up |
| 78 | (blank) | Not Used |
| 81 | 5647-12693-14 | Magnet Left |
| 82 | A-14315 (LED) + A-14316 (Trans) | Ball On Magnet |
| 83 | 5647-12693-14 | Magnet Right |
| 84 | 5647-12693-21 | L. Ramp Score |
| 85 | 5647-12693-21 | L. Ramp Diverted |
| 86 | A-14691-2 | Middle 3-bank Left |
| 87 | A-14691-4 | Middle 3-bank Middle |
| 88 | A-14691-2 | Middle 3-bank Right |

Footnotes printed on the page: `† Not Shown` (14, 21, 22, 24 are cabinet-mounted, not
drawn on the playfield diagram); `* The Score slingshot switches have diodes across
them.`

## Resolved facts

- **Switch 23**: the Switch Matrix page (`switch-matrix.md`) labels this "Ticket Opto.",
  but this parts list prints a blank Switch No. with "Not Used". The blank parts-list
  entry is physical-fitment ground truth (same pattern as Williams Indiana Jones's switch
  23); treated as unused here.
- **Switches 81/82/83 (Magnet Left / Ball On Magnet / Magnet Right)**: only 82 carries
  genuine A-14315(LED)+A-14316(Trans) opto construction. 81 and 83 use the ordinary leaf
  part 5647-12693-14. This matches pinned PinMAME's inverted-switch mask column 8
  (`0x02`, bit 1 = row 2 = address 82 only) exactly, with zero disagreement.
- **F5-F8 absent**: unlike Scared Stiff (which prints an explicit blank `---` row for its
  unfitted F5-F8), this page has no row at all for F5-F8 — the Lower positions (F1-F4)
  are the only Fliptronic entries present. Combined with the Solenoid/Flasher Table's two
  flipper rows (`solenoid-flasher-wiring.md`) and the retained script's silence on public
  115-118, this machine has no physical upper flippers.
