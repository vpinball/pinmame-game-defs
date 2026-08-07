# Tales of the Arabian Nights — Switch Locations (parts list)

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, PDF page 121, printed page
2-39, the Switch Locations parts list (fitment ground truth). The retained PDF carries a genuine OCR
text layer, but the layout extraction badly garbles multi-column tables, so this was re-verified
against the 300 dpi rendered page image, which is the source of record.

| Item | Switch/Opto part | Description |
| --- | --- | --- |
| F1 | SW-1A-194 | Lower Right Flipper E.O.S. |
| F2 | A-17316 | Lower Right Flipper Cabinet |
| F3 | SW-1A-194 | Lower Left Flipper E.O.S. |
| F4 | A-17316 | Lower Left Flipper Cabinet |
| F5 | Not Used | Upper Right Flipper E.O.S. |
| F6 | Not Used | Upper Right Flipper Cabinet |
| F7 | Not Used | Upper Left Flipper E.O.S. |
| F8 | Not Used | Upper Left Flipper Cabinet |
| 11 | A-12238 | Harem Passage |
| 12 | A-12238 | Vanish Tunnel |
| 13 | 20-9663-1 | Start Button |
| 14 | 04-10346 | Plumb Bob Tilt* |
| 15 | 5647-12693-36 | Ramp Enter |
| 16 | A-16443 | Left Outlane |
| 17 | A-17813 | Right Inlane |
| 18 | A-20842 | Ball Shooter |
| 21 | A-17238 | Slam Tilt* |
| 22 | 5643-09268-00 | Coin Door Closed* |
| 23 | A-18530-6 | Genie Standup |
| 24 | 5643-09112-00 | Always Closed* |
| 25 | 5647-12693-13 | Bazaar Eject |
| 26 | A-17813-1 | Left Inlane |
| 27 | A-16443 | Right Outlane |
| 28 | 5647-12693-21 | Left Wire Make |
| 31 | A-18617-1 (LED) / A-18618-1 (photo transistor) | Trough Eject |
| 32 | A-18617-1 (LED) / A-18618-1 (photo transistor) | Trough Ball 1 |
| 33 | A-18617-1 (LED) / A-18618-1 (photo transistor) | Trough Ball 2 |
| 34 | A-18617-1 (LED) / A-18618-1 (photo transistor) | Trough Ball 3 |
| 35 | A-18617-1 (LED) / A-18618-1 (photo transistor) | Trough Ball 4 |
| 36 | A-16908 (LED) / A-16909 (photo transistor) | Left Cage Opto |
| 37 | A-16908 (LED) / A-16909 (photo transistor) | Right Cage Opto |
| 38 | A-17985-R | Left Eject |
| 41 | A-12238 | Ramp Made Left |
| 42 | SW-1A-207 (left) / SW-1A-208 (right) | Genie Target |
| 43 | A-17813 | Left Loop |
| 44 | A-17813 | Inner Loop Left |
| 45 | A-17813 | Inner Loop Right |
| 46 | A-18017-6 | Mini Standups (3) |
| 47 | A-12238 | Ramp Made Right |
| 48 | A-18530-6 | Right Captive Ball |
| 51 | A-17800 (Kick) / A-17793 (Score)** | Left Slingshot |
| 52 | A-17800 (Kick) / A-17793 (Score)** | Right Slingshot |
| 53 | A-16443 | Left Jet Bumper |
| 54 | A-16443 | Right Jet Bumper |
| 55 | A-16443 | Middle Jet Bumper |
| 56 | SW-1A-206 | Lamp Spin CCW |
| 57 | SW-1A-206 | Lamp Spin CW |
| 58 | A-18530-6 | Left Captive Ball |
| 61 | A-20846-9 (top) / A-20499-9 (middle) / A-20499-9 (bottom) | Left Standups |
| 62 | A-20846-9 (top) / A-20499-9 (middle) / A-20499-9 (bottom) | Right Standups |
| 63 | SW-1A-202-15 | Top Skill |
| 64 | SW-1A-202-15 | Middle Skill |
| 65 | SW-1A-202-15 | Bottom Skill |
| 66 | A-17985-R | Lock 1 (bottom) |
| 67 | A-14820 | Lock 2 (middle) |
| 68 | A-14820 | Lock 3 (top) |
| 71-88 | — | Not Used |

`*` NOT SHOWN on playfield map. `**` SCORE SWITCHES HAVE DIODES ATTACHED.

## Opto cross-check against pinned PinMAME

No switch outside matrix column 3 (rows 1-7, addresses 31-37) uses an LED/photo transistor opto
pair; every other fitted switch uses a mechanical part number (leaf, standup, gate, or
proximity-style hardware). This matches PinMAME's `totanGameData` inverted-switch mask
(`{0x00,0x00,0x00,0x7f,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}`) exactly: index 3 (matrix column 3)
is `0x7f` (bits 0-6 set = rows 1-7 = addresses 31-37), and no other index is nonzero. Zero polarity
disagreements between the manual and pinned PinMAME.
