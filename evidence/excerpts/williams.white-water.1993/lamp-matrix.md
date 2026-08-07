# White Water — Lamp Matrix (wiring table)

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF page 112, printed
page 3-2 ("Lamps" / "Lamp Matrix"). Transcribed from a 200 dpi render.

Column headers (drive wire / connector / driver transistor): 1 Yellow-Brown
J137-1 Q98, 2 Yellow-Red J137-2 Q97, 3 Yellow-Orange J137-3 Q96, 4
Yellow-Black J137-4 Q95, 5 Yellow-Green J137-5 Q94, 6 Yellow-Blue J137-6
Q93, 7 Yellow-Violet J137-7 Q92, 8 Yellow-Gray J137-9 Q91.

Row headers (return wire / connector / driver transistor): 1 Red-Brown
J133-1 Q90, 2 Red-Black J133-2 Q89, 3 Red-Orange J133-4 Q88, 4 Red-Yellow
J133-5 Q87, 5 Red-Green J133-6 Q86, 6 Red-Blue J133-7 Q85, 7 Red-Violet
J133-8 Q84, 8 Red-Gray J133-9 Q83.

Address = column*10 + row.

| addr | label | addr | label | addr | label | addr | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Shoot Again | 21 | River "R1" | 31 | Raft 7 | 41 | 3-Bank Center |
| 12 | Kickback | 22 | River "I" | 32 | Raft 8 | 42 | 3-Bank Lower |
| 13 | Left Outlane | 23 | River "V" | 33 | Wet Willie | 43 | Lock Release |
| 14 | Left Flipper Lane | 24 | River "E" | 34 | Ramp Millions | 44 | 3-Bank Top |
| 15 | Right Flipper Lane | 25 | River "R2" | 35 | Hazzard 4 | 45 | Hazzard 4 |
| 16 | Right Outlane | 26 | Hazzard 3 | 36 | Left Light Lock | 46 | Right Light Lock |
| 17 | Lights Whirlpool | 27 | Lock 1 | 37 | 2X Multiplier | 47 | 4X Multiplier |
| 18 | 6X Multiplier | 28 | Lock 2 | 38 | 3X Multiplier | 48 | 5X Multiplier |

| addr | label | addr | label | addr | label | addr | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | Hazzard 1 | 61 | Raft 1 | 71 | Whirlpool 1 | 81 | Light Extra Ball |
| 52 | Hazzard 5 | 62 | Raft 2 | 72 | Whirlpool 2 | 82 | Advance Raft |
| 53 | Hazzard 6 | 63 | Raft 3 | 73 | Whirlpool 3 | 83 | Mystery |
| 54 | Hazzard 7 | 64 | Raft 4 | 74 | Whirlpool 4 | 84 | Boulder 5X Award |
| 55 | Whirlpool Lit | 65 | Raft 5 | 75 | Whirlpool 5 | 85 | Not Used |
| 56 | Extra Ball | 66 | Raft 6 | 76 | Whirlpool 6 | 86 | Not Used |
| 57 | Whirl Challange | 67 | 2-Bank Upper | 77 | Multi Jackpot | 87 | Not Used |
| 58 | Boulder Man Over | 68 | 2-Bank Lower | 78 | Bigfoot Jackpot | 88 | Start Button |

Addresses 35 and 45 are both printed "Hazzard 4" — a genuine duplicate on
the printed page, not a transcription error (both cells were independently
re-read from the render). Addresses 17 and 55 carry real feature names here
("Lights Whirlpool", "Whirlpool Lit") despite the Lamp Locations parts list
marking both "Not Used" — see `lamp-locations.md` for the cross-page
disagreement and its resolution.
