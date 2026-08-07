# Fish Tales — Solenoid/Flasher Locations

Transcribed from `Fish_Tales_OPS.pdf`, PDF page 92, printed page 2-44, the `Solenoid/Flasher
Locations` table. Read from the rendered page and cross-checked against a 400 dpi crop, not the OCR
text layer. `*` marks "Not Shown" on the printed playfield map (applies to the General Illumination
and Flippers sections below).

| Item | Coil/Flasher No. | Assy No. | Description |
| --- | --- | --- | --- |
| 01 | AE-23-800 | A-14525 | Ball Shooter |
| 02 | AL-23-800 | A-14947 | Catapult |
| 03 | AE-24-900 | D-11335-1 | Ball Popper |
| 04 | AE-27-1200 | A-15749 | Left Slingshot |
| 05 | AE-27-1200 | A-14369-R | Right Slingshot |
| 06 | A-14406 | A-14422 | Left Gate |
| 07 | AE-23-800 | B-10686-1 | Knocker |
| 08 | AE-23-800 | A-15304 | Backbox Fish |
| 09 | AE-27-1200 | A-8039-3 | Outhole |
| 10 | AE-26-1200 | B-9362-R-3 | Ball Release |
| 11 | AE-26-1200 | B-9362-R-3 | Eject Hole |
| 12 | AE-26-1200 | A-15211 | Drop Target Up |
| 13 | SM1-26-600 | A-15211 | Drop Target Down |
| 14 | AE-26-1200 | A-9415-2 | Left Jet Bumper |
| 15 | AE-26-1200 | A-9415-2 | Center Jet Bumper |
| 16 | AE-26-1200 | A-9415-2 | Right Jet Bumper |
| 17 | 24-8802 | A-12336-1 | Jackpot Flasher #906 |
| 18 | 24-8802 | A-12336-1 | Super Jackpot Flasher #906 |
| 19 | 24-8802 | A-15457 | Instant Multi-ball Flasher #906 |
| 19 | 24-8802 | — | Backbox Insert Flasher #906 |
| 20 | 24-8802 | A-15457 | Light Extra Ball Flasher #906 |
| 20 | 24-8802 | — | Backbox Insert Flasher #906 |
| 21 | 24-8802 | A-15457 | Rock the Boat Flasher #906 |
| 21 | 24-8802 | — | Backbox Insert Flasher #906 |
| 22 | 24-8802 | A-15457 | Video Mode Flasher #906 |
| 22 | 24-8802 | — | Backbox Insert Flasher #906 |
| 23 | 24-8802 | A-15457 | Hold Bonus Flasher #906 |
| 23 | 24-8802 | — | Backbox Insert Flasher #906 |
| 24 | — | — | Not Used |
| 25 | 24-8704 | A-8798 | Reel Flasher #89 |
| 25 | 24-8802 | — | Backbox Insert Flasher #906 |
| 25 | 24-8802 | A-12336-1 | Hood Flasher #906 |
| 26 | 24-8704 | A-8798 | Top Left Flasher #89 |
| 26 | 24-8802 | A-12336-1 | Top Left Flasher #906 |
| 27 | 24-8704 | A-9302 | Caster Club Flasher #89 |
| 27 | 24-8802 | — | Backbox Insert Flasher #906 |
| 28 | 14-7967 | A-14945 | Reel Motor |

Item 25 (Reel Flasher) is the only address with **three** rows: a playfield #89 bulb (`A-8798`), a
backbox insert #906 bulb (no assembly listed), and a hood #906 bulb (`A-12336-1`). Compare to the
Solenoid Table wiring row for the same address (`solenoid-flasher-wiring.md`), whose Connections
cell prints a matching third field.

## General Illumination

| Item | Bulb | Assy | Description |
| --- | --- | --- | --- |
| 01 | 24-8768 | — | *Backbox G.I. #555 |
| 02 | 24-8768 | — | *Backbox & Hood G.I. #555 |
| 03 | 24-6549 | — | *Playfield G.I. #44 |
| 04 | 24-8768 | — | *Backbox G.I. #555 |
| 05 | 24-6549 | — | *Playfield & Coin Door G.I. #44 |

Five GI strings, all "Not Shown" on the printed playfield map (none has an assembly number — they
are bulb-only circuits). Only two of the five (03, 05) are described as reaching the playfield at
all; 01, 02, and 04 are backbox/hood-only.

## Flippers

| Coil | Assy | Description |
| --- | --- | --- |
| FL-11629 | A-15205-R-2 | *Lower Right Flipper |
| FL-11629 | A-15205-L-2 | *Lower Left Flipper |

Exactly two flipper coils are listed. There is no row for an upper-right or upper-left flipper coil
— not even a "NOT USED" placeholder of the kind this page uses elsewhere (see item 24, "Not Used",
printed with an explicit row). See `manual-transcription.md` for the cross-check against the
Fliptronic II Flipper Assembly parts page and the Switch Locations table, which independently agree
this machine has no upper flippers fitted, and against the generic Fliptronic II board circuit
diagrams (`boards-and-assemblies.md`), which do show wiring for a full four-flipper complement
regardless of fitment.
