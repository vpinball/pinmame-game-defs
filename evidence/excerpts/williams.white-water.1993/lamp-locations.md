# White Water — Lamp Locations (parts list)

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF page 102, printed
page 2-40 ("Lamp Locations"). Transcribed from a 200 dpi render (the
OCR text layer for this page is garbled where the right-hand continuation
column overlaps the location diagram).

Columns are `Item No. | Bulb No. | Lamp Assy No. | Description`.

| Item | Bulb | Assy | Description |
| --- | --- | --- | --- |
| 11 | 24-6549 | A-11754 | Shoot Again #44 |
| 12 | 24-6549 | A-11754 | Kickback #44 |
| 13 | 24-6549 | A-11271 | Left Outlane #44 |
| 14 | 24-6549 | A-11271 | Left Flipper Lane #44 |
| 15 | 24-6549 | A-11754 | Right Flipper Lane #44 |
| 16 | 24-6549 | A-11754 | Right Outlane #44 |
| 17 | — | — | Not Used |
| 18 | 24-6549 | A-11754 | 6X Multiplier #44 |
| 21 | 24-8768 | A-15763 | River "R1" #555 |
| 22 | 24-8768 | A-15763 | River "I" #555 |
| 23 | 24-8768 | A-15763 | River "V" #555 |
| 24 | 24-8768 | A-15763 | River "E" #555 |
| 25 | 24-8768 | A-15763 | River "R2" #555 |
| 26 | 24-8768 | A-15766 | Hazzard 3 #555 |
| 27 | 24-8768 | A-15766 | Lock 1 #555 |
| 28 | 24-8768 | A-15766 | Lock 2 #555 |
| 31 | 24-8768 | A-15767 | Raft 7 #555 |
| 32 | 24-8768 | A-15767 | Raft 8 #555 |
| 33 | 24-8768 | A-15767 | Wet Willie #555 |
| 34 | 24-8768 | A-15767 | Ramps Millions #555 |
| 35 | 24-8768 | A-15767 | Hazzard 4 #555 |
| 36 | 24-8768 | A-15767 | Left Light Lock #555 |
| 37 | 24-6549 | A-11271 | 2X Multiplier #44 |
| 38 | 24-6549 | A-11754 | 3X Multiplier #44 |
| 41 | 24-8768 | A-15767 | 3-bank Center #555 |
| 42 | 24-8768 | A-15767 | 3-bank Lower #555 |
| 43 | 24-8768 | A-15767 | Lock Release #555 |
| 44 | 24-8768 | A-15767 | 3-bank Top #555 |
| 45 | 24-8768 | A-15767 | Hazzard 4 #555 |
| 46 | 24-8768 | A-15767 | Right Light Lock #555 |
| 47 | 24-6549 | A-11754 | 4X Multiplier #44 |
| 48 | 24-6549 | A-11271 | 5X Multiplier #44 |
| 51 | 24-6549 | A-11271 | Hazzard 1 #44 |
| 52 | 24-6549 | A-11271 | Hazzard 5 #44 |
| 53 | 24-6549 | A-11905 | Hazzard 6 #44 |
| 54 | 24-6549 | A-11905 | Hazzard 7 #44 |
| 55 | — | — | Not Used |
| 56 | 24-8768 | A-15764 | Extra Ball #555 |
| 57 | 24-8768 | A-15764 | Whirl Challange #555 |
| 58 | 24-8768 | A-15764 | Boulder Man Over #555 |
| 61 | 24-8768 | A-15764 | Raft 1 #555 |
| 62 | 24-8768 | A-15764 | Raft 2 #555 |
| 63 | 24-8768 | A-15764 | Raft 3 #555 |
| 64 | 24-8768 | A-15764 | Raft 4 #555 |
| 65 | 24-8768 | A-15764 | Raft 5 #555 |
| 66 | 24-8768 | A-15764 | Raft 6 #555 |
| 67 | 24-8768 | A-15764 | 2-bank Upper #555 |
| 68 | 24-8768 | A-15764 | 2-bank Lower #555 |
| 71 | 24-8768 | A-15768 | Whirlpool 1 #555 |
| 72 | 24-8768 | A-15768 | Whirlpool 2 #555 |
| 73 | 24-8768 | A-15768 | Whirlpool 3 #555 |
| 74 | 24-8768 | A-15768 | Whirlpool 4 #555 |
| 75 | 24-8768 | A-15768 | Whirlpool 5 #555 |
| 76 | 24-8768 | A-15768 | Whirlpool 6 #555 |
| 77 | 24-6549 | A-11905 | Multi Jackpot #44 |
| 78 | 24-6549 | A-11905 | Bigfoot Jackpot #44 |
| 81 | 24-6549 | A-11271 | Light Extra Ball #44 |
| 82 | 24-6549 | A-11754 | Advance Raft #44 |
| 83 | 24-6549 | A-11754 | Mystery #44 |
| 84 | 24-6549 | A-11271 | Boulder 5X Award #44 |
| 85 to 87 | — | — | Not Used |
| 88 | — | 20-9663-1 | Start Button |

Items 17 and 55 are printed "Not Used" here with every field blank — the
same blank signature used for the genuinely unfitted positions 85-87. The
Lamp Matrix wiring page (`lamp-matrix.md`) prints real feature names at both
addresses ("Lights Whirlpool" at 17, "Whirl Lit"/"Whirlpool Lit" at 55), and
the retained VPX script's `LampTimer_Timer` special-cases both addresses by
name (`upf_yellow_light` at 17, `upf_red_light` at 55) driving dedicated
image-cycling primitives — see `knowledge/williams/white-water.md` for the
resolution.
