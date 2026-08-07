# Twilight Zone — General Illumination Circuits

Transcribed from `Twilight_Zone_OPS.pdf`, PDF page 62, printed page 2-53, the "General Illumination
Circuits" block printed on the same page as the Solenoid/Flasher Locations table (see
`solenoid-flasher-locations.md`). Read from the rendered page; the retained scan is image-only.

| Item | Description | Coil/Flasher Number |
| --- | --- | --- |
| *01 | Playfield Left | 24-6549 |
| *02 | Mini-playfield & Insert | 24-8768 |
| *03 | Clock & Insert | 24-8829, 24-8768 |
| *04 | Insert Main | 24-8768 |
| *05 | Playfield Right | 24-6549 |

Public GI addresses are zero-based (0-4); string 01 = public 0 (Playfield Left) through string 05 =
public 4 (Playfield Right), matching the retained script's `UpdateGI` dispatch (case 0 = left
playfield light collection, case 1 = mini-playfield, case 2 = clock, case 3 = no light collection
bound in this table, case 4 = right playfield).
