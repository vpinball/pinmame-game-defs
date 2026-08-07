# The Addams Family — Switch Locations (parts list)

Transcribed from `Bally_1992_The_Addams_Family_Operations_Manual_January_1992_includes_schematics_OCR_searchable.pdf`,
printed page 2-39, the authoritative switch parts list (preferred over the Handbook's matrix page for
labels per project policy). Visual re-transcription from the rendered page, not the OCR text layer.
Columns: Item (public address), Switch Number (switch part number), Switch Assy. (assembly part
number, or the opto-pair part number when the position is an opto interrupter), Description. `*` =
not shown on the printed playfield map; `†` = located on the underside of the playfield.

| Item | Switch Number | Switch Assy. | Description |
| --- | --- | --- | --- |
| 11-12 | -- | -- | Not Used |
| 13 | -- | 20-9663-1 | Start Button |
| 14 | -- | 20-6502-A | *Plumb Bob Tilt |
| 15 | 5647-09957-00 | B-8925 | Left Trough |
| 16 | 5647-09957-00 | B-8925 | Center Trough |
| 17 | 5647-12693-08 | A-11680 | Right Trough |
| 18 | 5647-12133-12 | A-10417 | Outhole |
| 21 | -- | 27-1066 | *Slam Tilt |
| 22 | -- | A-8630 | *Coin Door Closed |
| 23 | -- | Not Used | *Ticket Opto. |
| 24 | -- | A-8630 | *Always Closed |
| 25 | 5647-12693-19 | A-12688 | Right Flipper Lane |
| 26 | 5647-12693-19 | A-12688 | Right Outlane |
| 27 | 5647-12693-04 | A-11619 | Ball Shooter |
| 28 | -- | -- | Not Used |
| 31 | SW-11A-37 | B-12030-2 | Upper Left Jet |
| 32 | SW-11A-37 | B-12030-2 | Upper Right Jet |
| 33 | SW-11A-37 | B-12030-2 | Center Left Jet |
| 34 | SW-11A-37 | B-12030-2 | Center Right Jet |
| 35 | SW-11A-37 | B-12030-2 | Lower Jet |
| 36 | SW-1A-114 | B-8284-1 | Left Slingshot |
| 37 | SW-1A-120 | A-11539-1 | Right Slingshot |
| 38 | 5647-12693-19 | A-12688 | Upper Left Loop |
| 41 | -- | B-11696-1 | Grave "G" |
| 42 | -- | B-11696-1 | Grave "R" |
| 43 | 5647-12693-25 | A-14962 | †Chair Kickout |
| 44a | -- | B-11696-4 | Cousin It (2) |
| 44b | -- | B-12583-4 | (2) |
| 45 | -- | B-11696-15 | Lower Swamp Million |
| 46 | -- | -- | Not Used |
| 47 | -- | B-11696-15 | Center Swamp Million |
| 48 | -- | B-11696-15 | Upper Swamp Million |
| 51 | 5647-12693-19 | A-15372 | Shooter Lane |
| 52 | -- | -- | Not Used |
| 53 | -- | A-15017/A-15018 | Bookcase Opto 1 |
| 54 | -- | A-15017/A-15018 | Bookcase Opto 2 |
| 55 | -- | A-15017/A-15018 | Bookcase Opto 3 |
| 56 | -- | A-15017/A-15018 | Bookcase Opto 4 |
| 57 | -- | A-14231/A-14232 | Bumper Lane Opto |
| 58 | 5647-12693-21 | A-14972 | Right Ramp Exit |
| 61 | 5647-12693-11 | A-14492 | Left Ramp Enter |
| 62 | -- | B-11696-5 | Train Wreck |
| 63 | 5647-12693-19 | A-12688 | Thing Eject Lane |
| 64 | 5647-12693-11 | A-13627-2 | Right Ramp Enter |
| 65 | 5647-12693-21 | A-15047 | Right Ramp Top |
| 66 | 5647-12693-21 | A-15047 | Left Ramp Top |
| 67 | 5647-12693-19 | A-12688 | Upper Right Loop |
| 68 | 5647-12693-08 | A-15070 | Vault |
| 71 | 5647-12693-25 | A-14964 | †Swamp Lock Upper |
| 72 | 5647-12693-25 | A-14964 | †Swamp Lock Center |
| 73 | 5647-12693-25 | A-14964 | †Swamp Lock Lower |
| 74 | 5647-12693-25 | A-14964 | †Lockup Kickout |
| 75 | 5647-12693-19 | A-12688 | Left Outlane |
| 76 | 5647-12693-19 | A-12688 | Left Flipper Lane 2 |
| 77 | 5647-12693-25 | A-15200 | †Thing Kickout |
| 78 | 5647-12693-19 | A-12688 | Left Flipper Lane 1 |
| 81 | 5647-12693-08 | A-14970 | †Bookcase Open |
| 82 | 5647-12693-08 | A-14970 | †Bookcase Closed |
| 83 | -- | -- | Not Used |
| 84 | -- | A-15285 | †Thing Down Opto |
| 85 | -- | A-15285 | †Thing Up Opto |
| 86 | -- | B-12583-1 | Grave "A" |
| 87 | 5647-12133-11 | A-9381-R | Thing Eject Hole |
| 88 | -- | -- | Not Used |

## Opto determination (sweep of every row above)

Sweeping every row above for both cues (blank Switch Number with a populated, paired-part-number
"Opto" Assy, or "Opto" literally in the description): addresses **53, 54, 55, 56, 57, 84, 85** carry
a blank switch-part number and a populated opto-assembly part number (`A-15017/A-15018` for the four
Bookcase optos, `A-14231/A-14232` for the Bumper Lane opto, `A-15285` for both Thing position optos),
and each description explicitly says "Opto". Address 23 ("*Ticket Opto.") is the one row where the
description also says "Opto" but both columns read "Not Used" — this position is enumerated but
genuinely unfitted, not a physically-installed opto, matching the "blank voltage AND blank drive
connection prove nothing is fitted" pattern used elsewhere in this project for unfitted solenoids.

## Cross-check against pinned PinMAME

`tafGameData`'s inverted-switch mask (`src/wpc/sims/wpc/full/taf.c`):

```
/*Coin    1     2     3     4     5     6     7     8     9    10   Cab.  Cust */
{ 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00}
```

Column 5 (`0x7c` = bits 2-6) marks rows 3-7 inverted, i.e. addresses **53, 54, 55, 56, 57**. Column 8
(`0x18` = bits 3-4) marks rows 4-5 inverted, i.e. addresses **84, 85**. That is exactly the
seven-address opto set the manual sweep found above, column for column and row for row. Full
agreement, zero disagreement — unlike Monster Bash's Dracula-position optos or Centaur's lamp 113,
this machine's opto polarity has no unresolved conflict. `physical.normally_closed = true` for
53/54/55/56/57/84/85 and `controller.inversion_applied_by_emulator = true` (already normalized by
PinMAME) for the same seven; address 23 stays `normally_closed` unset because no opto is fitted
there. There is no shaded-cell drawing to crop for this machine: this manual establishes opto
polarity from the parts-list construction column above, not from a printed shading legend on a
switch-matrix drawing.
