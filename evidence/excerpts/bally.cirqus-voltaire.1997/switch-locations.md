# Cirqus Voltaire — Switch Locations

Transcribed from `Bally_1997_Cirqus_Voltaire_Manual.pdf`, PDF pages 150-151, printed pages 2-44/2-45,
the Switch Locations parts list. Read from `pdftotext -layout` (this scan's text layer is present but
the columns shift per row); cross-checked against 300 dpi renders of both pages for every row that
feeds a `physical.switch_type` or `physical.assembly_part_number` claim. This is the physical-fitment
authority: a blank Switch Assembly/Opto Assembly Part Number column is a genuine "nothing installed"
claim, not merely absent from a diagram.

## Fliptronic F1-F8

| Item | Assembly / Opto Part | Switch Part | Description |
| --- | --- | --- | --- |
| F1 | A-17316 | SW-1A-194 | *Lower Right Flipper E.O.S. |
| F2 | (blank) | (blank) | Lower Right Flipper Cabinet |
| F3 | (blank) | SW-1A-194 | *Lower Left Flipper E.O.S. |
| F4 | A-17316 / A-21801-2 | (blank) | Lower Left Flipper Cabinet |
| F5 | (blank) | 5647-12693-24 | Right Spinner |
| F6 | NOT USED | (blank) | Upper Right Flipper Cabinet |
| F7 | A-21801-1 | 5647-12693-24 | Left Spinner |
| F8 | NOT USED | (blank) | Upper Left Flipper Cabinet |

`*` = "Not Shown" on the playfield map (cabinet-mounted E.O.S. leaf). F2/F4 (the flipper button
opto assemblies, A-17316/A-21801-2) are physically fitted per this list even though this page shows
no separate part number in the same row as F1/F3 — the assembly numbers are the flipper button opto
kit shared with the E.O.S. row above each pair on the printed page. F6 and F8 are explicitly
"NOT USED" here, in contrast with the wired opto template the Switch Matrix page (`switch-matrix.md`)
prints for the same two positions; see that file's note on the resolution.

## Matrix switches 11-38 (selected rows with construction detail)

| Addr | Assembly / Opto Part | Switch Part | Description |
| --- | --- | --- | --- |
| 11 | (blank) | 5647-12693-19 | Backbox Luck |
| 12 | (blank) | 5647-12693-13 | Wire Ramp Enter |
| 13 | 20-9663-16 | (blank) | Start Button |
| 14 | (blank) | 04-10346 | Plumb Bob Tilt |
| 15 | A-17813 | 5647-12693-19 | Left Loop Upper |
| 16 | A-20036 | (blank) | Top Eddy |
| 17 | A-18008-1 | A-16443 | Right Inlane |
| 18 | (blank) | 5647-12693-68 | Shooter Lane |
| 21 | A-17238 | (blank) | *Slam Tilt |
| 22 | (blank) | 5643-09268-00 | *Coin Door Closed |
| 23 | A-17813-1 | 5647-12693-19 | Right Loop Upper |
| 24 | (blank) | 5643-15190-00 | *Always Closed |
| 25 | A-17813 | 5647-12693-19 | Inner Loop Left |
| 26 | A-18008-1 | A-16443 | Left Inlane |
| 27 | A-17813-1 | 5647-12693-19 | Left Outlane |
| 28 | A-17813-1 | 5647-12693-19 | Inner Loop Right |
| 31 | A-18617-1 (LED) / A-18618-1 (photo trans) | (blank) | Trough Eject |
| 32 | A-18617-1 (LED) / A-18618-1 (photo trans) | (blank) | Trough Ball 1 |
| 33 | A-18617-1 (LED) / A-18618-1 (photo trans) | (blank) | Trough Ball 2 |
| 34 | A-18617-1 (LED) / A-18618-1 (photo trans) | (blank) | Trough Ball 3 |
| 35 | A-18617-1 (LED) / A-18618-1 (photo trans) | (blank) | Trough Ball 4 |
| 36 | A-16908 (LED) / A-16909 (photo trans) | (blank) | Popper |
| 37 | A-21960-6 | (blank) | "WOW" Targets (3) |
| 38 | A-18530-6 | (blank) | Top Targets (2) |

Note: this LEDs/photo-transistor construction (A-1861x pair for the trough, A-16908/A-16909 for the
popper) confirms the printed opto shading on the Switch Matrix page for column 3 (31-38). The eddy
construction (A-18008-1 assembly, A-16443 switch part) for switches 17/26 is the same construction as
75/76 (`"Volt" Right`/`"Volt" Left`); see `general-illumination.md`'s sibling table for the retained
script's confirmation that switches 17/26/75/76 each toggle one of four `volt1..volt4` table objects.

## Matrix switches 41-76 (selected)

| Addr | Assembly / Opto Part | Switch Part | Description |
| --- | --- | --- | --- |
| 42 | (blank) | 5647-12693-01 | Ringmaster Up |
| 43 | (blank) | 5647-12693-01 | Ringmaster Middle |
| 44 | (blank) | 5647-12693-01 | Ringmaster Down |
| 45 | (blank) | 5647-12693-21 | Left Ramp Made |
| 46 | (blank) | 5647-12693-13 | Trough Upper |
| 47 | (blank) | 5647-12693-13 | Trough Middle |
| 48 | A-17813-1 | 5647-12693-19 | Left Loop Enter |
| 53 | B-12030-2 | A-16443 | Upper Jet Bumper |
| 54 | (blank) | SW-1A-213 | Middle Jet Bumper |
| 55 | B-12030-2 | A-16443 | Lower Jet Bumper |
| 56 | A-20846-9 | (blank) | Skill Shot |
| 57 | A-17813 | (blank) | Right Outlane |
| 58 | A-20846-9 | 5647-12693-19 | Ring "N" & "G" |
| 61 | A-18530-6 | (blank) | "Light" Standup Target |
| 62 | A-18530-6 | (blank) | "Lock" Standup Target |
| 63 | (blank) | 20-10293 | Ramp Enter |
| 64 | (blank) | 5647-12693-13 | Ramp Magnet |
| 65 | (blank) | 5647-12693-13 | Ramp Made |
| 66 | (blank) | 5647-12693-66 | Ramp Lock Low |
| 67 | (blank) | 5647-12693-66 | Ramp Lock Middle |
| 68 | (blank) | 5647-12693-66 | Ramp Lock High |
| 74 | A-17794 | A-17793 | Big Ball Rebound |
| 75 | A-18008-1 | A-16443 | "Volt" Right |
| 76 | A-18008-1 | A-16443 | "Volt" Left |
| 77 to 88 | (blank) | (blank) | Not Used |

Footnotes on this page: `*NOT SHOWN.` `**SCORE SWITCHES HAVE DIODES ATTACHED.` `NOTE 1 - THIS IS A
COMPLETE ASSEMBLY, NOT JUST A SWITCH ASSEMBLY.` Part 5647-12693-66 (switches 66/67/68, the three
Ramp Lock switches on the Center Wire A-21851) is independently confirmed by Service Bulletin 104
("Stiff or Hard-to-Actuate Lock Switches on Center Wire (A-21851)... three center LOCK switches (p/n
5647-12693-66)").
