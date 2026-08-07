# World Cup Soccer — General Illumination

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF page 115, printed page 2-49, the
`General Illumination Circuits` summary and Flipper Coils note. The wiring table itself (with
connectors, driver transistors, and printed bulb types) is transcribed in
`solenoid-flasher-wiring.md`, which lives on the same physical page (2-48) as the primary
Solenoid/Flasher Table.

## General Illumination Circuits (page 2-49 summary)

| Public (0-based) | Printed # | Description | Bulb type | GI String |
| --- | --- | --- | --- | --- |
| 0 | *01 | Playfield Left | #44, #555 | GI String 1 |
| 1 | *02 | Playfield Right | #44, #555 | GI String 2 |
| 2 | *03 | Insert Background | #555 | GI String 3 |
| 3 | *04 | Insert Title | #555 | GI String 4 |
| 4 | *05 | Playfield Top | #555 | GI String 5 |

`*Not Shown` (no playfield-diagram position printed for any GI string on this page).

Bulb legend: `24-6549=#44 Bulb; 24-8704=#89 Bulb; 24-8768=#555 Bulb; 24-8802=#906 Bulb`.

## Flipper Coils (repeated on this page)

| Coil Part | Color | Assembly | Position |
| --- | --- | --- | --- |
| *FL-11629 | Blue | A-15849-L-2 | Lwr. Left Flipper |
| *FL-11629 | Blue | A-15849-R-2 | Lwr. Right Flipper |

`*Not Shown`. Confirms (again) that only the two lower flippers carry a fitted coil; see
`solenoid-flasher-wiring.md`'s Flipper Circuits table for the upper-position "Not Used" rows.

## Cross-check against the retained known-working script (curator note)

The retained script's `GIUpdate2(no, pwm)` dispatch (in `script.vbs`) implements exactly three
`Case` branches — `Case 0` (drives collection `GILeft`), `Case 1` (drives collection `GIRight`), and
`Case 4` (drives collection `GITop`) — with no `Case 2` or `Case 3` at all. This matches this page's
own wiring table exactly: GI strings 0, 1, and 4 (printed 01, 02, 05) are the only three with a
Playfield voltage/drive connection printed; strings 2 and 3 (printed 03, 04, "Insert Background"/
"Insert Title") are Backbox-only. Unlike several other WPC-era games curated in this project (Tales
of the Arabian Nights, Theatre of Magic), there is **no** disagreement here between the manual's
physical wiring and the script's runtime implementation.
