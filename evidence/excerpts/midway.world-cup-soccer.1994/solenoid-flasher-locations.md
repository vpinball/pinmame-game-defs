# World Cup Soccer — Solenoid/Flasher Locations (parts list)

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF page 114, printed page 2-48, the
`SOLENOID/FLASHER LOCATIONS` parts list below the wiring table (see `solenoid-flasher-wiring.md`).
`*Not Shown` marks items without a playfield-diagram position on this page (their exact position is
reported by the retained VPX table or the mechanism it belongs to — see the curator's spatial
report).

| Item | Coil/Flasher Number | Assembly Number | Description |
| --- | --- | --- | --- |
| 01 | AE-23-800 | A-17839 | Goal Popper |
| 02 | AE-26-1500 | A-18213 | TV Popper |
| 03 | AE-23-800 | B-11873 | Kickback |
| 04 | AE-26-1500 | A-18155 | Lock Release |
| 05 | AE-26-1200 | B-9362-R-3 | Upper Eject Hole |
| 06 | AE-26-1500 | A-16765 | Trough |
| 07 | AE-23-800 | B-10686-1 | *Knocker |
| 08 | FL-11753-1 | A-18138 | Ramp Diverter |
| 09 | AE-26-1200 | A-9415-2 | Left Jet Bumper |
| 10 | AE-26-1200 | A-9415-2 | Upper Jet Bumper |
| 11 | AE-26-1200 | A-9415-2 | Lower Jet Bumper |
| 12 | AE-26-1200 | B-9362-L-2 | Left Slingshot |
| 13 | AE-26-1200 | B-9362-R-3 | Right Slingshot |
| 14 | AE-26-1200 | B-9362-L-2 | Right Eject Hole |
| 15 | AE-26-1200 | B-9362-L-2 | Left Eject Hole |
| 16 | FL-11753-1 | A-18138 | Diverter Hold |
| 17 | 24-8802 | A-12336-1 | Goal Cage Top (2) |
| 18 | 24-8802 / 24-8704 | A-18384 / A-17803 | Goal (2) |
| 19 | 24-8802 / 24-8704 | A-12336-1 / A-17803 | Skill Shot (2) |
| 20 | 24-8704 | A-17803 | Jet Bumpers |
| 21 | 14-7997 | A-17741 | Goalie Drive |
| 22 | 24-8704 | A-17983 | Spinning Ball (2) |
| 23 | 14-7996 | A-17569 | Ball Clockwise |
| 24 | 14-7996 | A-17569 | Ball Counter-Clockwise |
| 25 | 24-8704 | A-17983 | Left Ramp Entrance |
| 26 | 24-8802 | A-12336-1 | Lock Area |
| 27 | 24-8704 | A-17983 | Flipper Lanes (2) |
| 28 | 24-8802 | A-12336-1 | Ramp Rear (2) |
| 33 | 20-9247 | --- | Magna Goalie |
| 34 | A-14406 | A-17796 | Lock Gate |
| 35 | 20-9247 | A-18222 | Loop Magnet |

`*Not Shown` applies to item 07 (Knocker), which is backbox-mounted.

**Curator note on internal naming (not part of the transcription):** this page's own two tables
disagree with each other on solenoid 34's name — the wiring table above prints "Loop Gate" (see
`solenoid-flasher-wiring.md`), matching the pinned PinMAME driver's own `#define sLoopGate 34`,
while this locations table prints "Lock Gate" for the identical device (same coil part `A-14406`,
same assembly `A-17796`). Likewise this table swaps "Loop Magnet" onto item 35, where the wiring
table and `wcs.c`'s `#define sMagLock 35` both agree on "Lock Magnet". Two independently-agreeing
sources (driver source + this page's own primary wiring table) resolve both names in the
Function-column direction; both disagreements are recorded here for transparency but do not block
promotion since they are resolvable, unlike the switch 112/114 opto-polarity conflict.
