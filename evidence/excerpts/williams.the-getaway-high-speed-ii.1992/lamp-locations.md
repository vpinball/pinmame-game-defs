# The Getaway: High Speed II — Lamp Locations parts list

Transcribed from `Getaway_HSII_OPS.pdf`, PDF page 102, printed page 2-41, "Lamp Locations". Rendered
at 300 dpi with `pdftoppm` and read directly.

| Item | Bulb No. | Lamp Assy No. | Description |
| --- | --- | --- | --- |
| 11 | 24-8768 | A-15144 | Freeway 1 #555 |
| 12 | 24-8768 | A-15144 | Freeway 2 #555 |
| 13 | 24-8768 | A-15144 | Freeway 3 #555 |
| 14 | 24-8768 | A-15144 | Freeway 4 #555 |
| 15 | 24-8768 | A-15144 | Freeway 5 #555 |
| 16 | 24-8768 | A-15147/B-12224 | Speed (2) #555 |
| 17 | 24-8768 | A-15147 | Left Freeway #555 |
| 18 | 24-8768 | A-15147/B-12224 | Lock (2) #555 |
| 21 | 24-6549 | A-11754 | 2X #44 |
| 22 | 24-8768 | A-15144 | 4X #555 |
| 23 | 24-8768 | A-15144 | Hold Bonus #555 |
| 24 | 24-8768 | A-15144 | 6X #555 |
| 25 | 24-6549 | A-11754 | 8X #44 |
| 26 | 24-8768 | B-12224 | Getaway #555 |
| 27 | 24-8768 | B-12224 | Speed Millions #555 |
| 28 | 24-6549 | A-11754 | Super Jackpot #44 |
| 31 | 24-8768 | C-13361 | Top Red #555 |
| 32 | 24-8768 | C-13361 | Top Yellow #555 |
| 33 | 24-8768 | C-13361 | Top Green #555 |
| 34 | 24-8768 | B-12224 | Right Freeway #555 |
| 35 | 24-8768 | B-12224 | Special (2) #555 |
| 36 | 24-8768 | A-15147 | Video Mode #555 |
| 37 | 24-8768 | A-15147 | Random Lamp #555 |
| 38 | 24-8768 | A-15147 | Extra Ball #555 |
| 41 | 24-6549 | A-11754 | Tach 1 #44 |
| 42 | 24-8768 | A-15143 | Tach 2 #555 |
| 43 | 24-8768 | A-15143 | Tach 3 #555 |
| 44 | 24-8768 | A-15143 | Tach 4 #555 |
| 45 | 24-8768 | A-15143 | Tach 5 #555 |
| 46 | 24-8768 | C-13361 | Bottom Red #555 |
| 47 | 24-8768 | C-13361 | Bottom Yellow #555 |
| 48 | 24-8768 | C-13361 | Bottom Green #555 |
| 51 | 24-6549 | A-11754 | Shoot Again #44 |
| 52 | 24-8768 | B-12224 | Kickback #555 |
| 53 | 24-8768 | A-15145 | Tach 11 #555 |
| 54 | 24-8768 | A-15145 | Tach 12 #555 |
| 55 | 24-8768 | A-15145 | Tach13 #555 |
| 56 | 24-8768 | A-15145 | Tach 14 #555 |
| 57 | 24-6549 | A-11754 | Tach 15 #44 |
| 58 | 24-6549 | A-11754 | Shift #44 |
| 61 | 24-8768 | A-15145 | Right Return Lane #555 |
| 62 | 24-8768 | A-15143 | Left Return Lane #555 |
| 63 | 24-8768 | A-15143/A-15145 | Six Bank Bottom(2) #555 |
| 64 | 24-8768 | A-15143/A-15145 | Six Bank Middle(2) #555 |
| 65 | 24-8768 | A-15143/A-15145 | Six Bank Top(2) #555 |
| 66 | 24-8768 | A-15456-6 | Supercharger #555 |
| 67 | 24-8768 | A-15456-6 | Red Line Mania #555 |
| 68 | 24-6549 | 20-9663-3 | Start Button #44 |
| 71 | 24-8768 | A-15146 | 4th Gear #555 |
| 72 | 24-8768 | A-15146 | 5th Gear #555 |
| 73 | 24-8768 | B-15283 | Stop Light Red #555 |
| 74 | 24-8768 | B-15283 | Stop Light Yellow #555 |
| 75 | 24-8768 | B-15283 | Stop Light Green #555 |
| 76 | 24-8768 | A-15146 | 1st Gear #555 |
| 77 | 24-8768 | A-15146 | 2nd Gear #555 |
| 78 | 24-8768 | A-15146 | 3rd Gear #555 |
| 81 | 24-8768 | A-15146 | Tach 9 #555 |
| 82 | 24-8768 | A-15146 | Tach 10 #555 |
| 83 | 24-8768 | C-13361 | Middle Red #555 |
| 84 | 24-8768 | C-13361 | Middle Yellow #555 |
| 85 | 24-8768 | C-13361 | Middle Green #555 |
| 86 | 24-8768 | A-15146 | Tach 6 #555 |
| 87 | 24-8768 | A-15146 | Tach 7 #555 |
| 88 | 24-8768 | A-15146 | Tach 8 #555 |

Six items print a dual assembly number with a `(2)` bulb-count suffix: 16 (Speed), 18 (Lock), 35
(Special), 63 (Six Bank Bottom), 64 (Six Bank Middle), 65 (Six Bank Top) — each has two physical
bulbs. Every other row is a single bulb. This matches `gw_lampPos` in the pinned driver source
(`gw.c`), which independently splits the identical six matrix addresses (16, 18, 35, 63, 64, 65) into
two drawn bulb positions each, and no others.

Cross-referencing this list against the printed diagram callouts (not transcribed row-by-row here,
since the wiring table `lamp-matrix.md` already gives the authoritative address-to-label mapping used
by this definition) confirms every address 11-88 is accounted for with no unlabeled gap.
