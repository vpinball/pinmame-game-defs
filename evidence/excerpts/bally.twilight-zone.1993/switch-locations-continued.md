# Twilight Zone — Switch Locations (Continued)

Transcribed from `Twilight_Zone_OPS.pdf`, PDF page 61, printed page 2-51, "SWITCH LOCATIONS
(Continued)", items 34-98. Read from the rendered page; the retained scan is image-only.

The retained scan skips every even-numbered printed page from 2-48 through 2-54 inclusive, so the
"Switch Locations" table covering items 1-33 (printed 2-50, which also carries the Switch Matrix
wiring and its printed opto-shading legend) is not available from this manual. Labels, addresses, and
polarity for addresses below 34 are sourced from the pinned PinMAME driver instead of this manual;
this excerpt only carries items 34 and above.

| Item | Switch/Part Number | Where Used |
| --- | --- | --- |
| 34 | SW-1A-114 (kicker) / SW-1A-120 (score) | Left Slingshot |
| 35 | SW-1A-114 (kicker) / SW-1A-120 (score) | Right Slingshot |
| 36 | 5647-12693-19 | Left Outlane |
| 37 | 5647-12693-19 | Left Inlane 1 |
| 38 | 5647-12693-19 | Left Inlane 2 |
| 41 | 5647-12693-13 | Dead End |
| 42 | 5647-12693-13 | Mini-playfield Top Hole |
| 43 | 5647-12693-13 | Player Piano |
| 44 | 5647-12693-19 | Mini-playfield Enter |
| 45 | 5647-12693-11 | Mini-playfield Left (2) |
| 46 | 5647-12693-11 | Mini-playfield Right (2) |
| 47 | A-15658-2 | Clock Millions |
| 48 | A-14691-6 | Lower Left 5 Million |
| 51 | 5647-12693-13 | Gumball Popper Lane |
| 52 | 5647-12693-19 | Hitch-hicker |
| 53 | 5647-12693-11 | Left Ramp Enter |
| 54 | 5647-12693-21 | Left Ramp |
| 55 | 5647-12393-08 | †Gumball Geneva |
| 56 | 5647-12693-19 | Gumball Exit |
| 57 | A-16535 | †Slot Proximity |
| 58 | 5647-12693-25 | †Slot Kickout |
| 61 | 5647-12693-32 | Lower Skill |
| 62 | 5647-12693-53 | Center Skill |
| 63 | 5647-12693-54 | Upper Skill |
| 64 | A-14691-6 | Upper Right 5 Million |
| 65 | A-14691-4 | Power Payoff (2) |
| 66 | A-14691-6 | Middle Right 5 Million 1 |
| 67 | A-14691-6 | Middle Right 5 Million 2 |
| 68 | A-15658-6 | Lower Right 5 Million |
| 71 | ---- | Not Used |
| 72 | A-14231 (LED) / A-14232 (Trans) | Auto-Fire Kicker |
| 73 | A-14231 (LED) / A-14232 (Trans) | Right Ramp |
| 74 | A-14231 (LED) / A-14232 (Trans) | Gumball Popper |
| 75 | A-14231 (LED) / A-14232 (Trans) | Mini-playfield Top |
| 76 | A-14231 (LED) / A-14232 (Trans) | Mini-playfield Exit |
| 77 | A-14691-6 | Middle Left 5 Million |
| 78 | A-14691-6 | Upper Left 5 Million |
| 81 | A-14231 (LED) / A-14232 (Trans) | Lower Right Magnet |
| 82 | ---- | Not Used |
| 83 | A-14231 (LED) / A-14232 (Trans) | Left Magnet |
| 84 | A-14231 (LED) / A-14232 (Trans) | Lock Center |
| 85 | A-14231 (LED) / A-14232 (Trans) | Lock Upper |
| 86 | ---- | Not Used |
| 87 | A-14231 (LED) / A-14232 (Trans) | Gumball Enter |
| 88 | 5647-12133-11 | Lock Lower |
| 91 | A-16220 | *Clock 15 Minutes |
| 92 | A-16220 | *Clock 0 Minutes |
| 93 | A-16220 | *Clock 45 Minutes |
| 94 | A-16220 | *Clock 30 Minutes |
| 95 | A-16219 | *Clock Hour 1 |
| 96 | A-16219 | *Clock Hour 2 |
| 97 | A-16219 | *Clock Hour 3 |
| 98 | A-16219 | *Clock Hour 4 |

`*` = not shown on the diagram. `†` = located on the underside of the playfield.

## Construction evidence for opto polarity

Items 72-76, 81, 83-85, 87 (and the entire custom column 91-98) use the "A-14231 (LED) / A-14232
(Trans)" LED-plus-phototransistor opto pair. This matches pinned PinMAME's `tzGameData`
inverted-switch mask exactly: column 7 (addresses 71-78) = `0x3f` (bits 0-5 = 71-76 inverted, 77/78
not), column 8 (addresses 81-88) = `0x7f` (bits 0-6 = 81-87 inverted, 88 not), and the custom column =
`0xff` (all of 91-98 inverted). Every address the manual builds from opto parts falls inside
PinMAME's inverted range, and every address built from a plain switch part (77, 78, 88, and the
mechanical-leaf items 34-68) falls outside it. No polarity conflict was found for this range. There
is no shaded-cell drawing to crop here: the switch matrix wiring page that would carry the printed
opto-shading legend (2-50) is one of the pages missing from this retained scan, so polarity for these
addresses rests on the parts-list construction column above, cross-checked against the PinMAME mask,
not on a printed shading legend.

## Items printed "Not Used"

Switches 71 ("Big Kick"), 82 ("Upper Right Magnet"), and 86 ("Clock Lane") are printed "Not Used" —
no coil/switch part number at all, the strongest form of "not fitted" in this manual's convention.
These three correspond exactly to the `tz.c` `tz_inportData` simulator's own "Third Magnet", "Big
Kick", and "Clock Lane" pseudo-DIP toggles, which belong to PinMAME's internal text-mode
ball-tracking simulator (`sim.c`) rather than to any physical CPU-board DIP switch or documented
factory option; no manual/schematic evidence was found of a production variant that fits them.
