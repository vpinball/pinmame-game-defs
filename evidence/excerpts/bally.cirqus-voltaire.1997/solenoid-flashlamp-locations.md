# Cirqus Voltaire — Solenoid/Flashlamp Locations

Transcribed from `Bally_1997_Cirqus_Voltaire_Manual.pdf`, PDF page 152, printed page 2-46, the
Solenoid/Flashlamp Locations parts list -- the assembly-part-number companion to
`solenoid-flasher-table.md`. Read from `pdftotext -layout`; every assembly number below matches its
sibling function/wiring row on the primary wiring table.

| Item | Assembly Part Number | Coil/Flasher Part | Description |
| --- | --- | --- | --- |
| 01 | A-21022 | AE-23-800 | Auto Plunger |
| 02 | B-11873 | AE-23-800 | Backbox Kicker |
| 03 | (blank) | 20-10197 | Left Loop Magnet |
| 04 | A-21564 | AE-23-800 | Middle Jet Bumper |
| 05 | A-21959 | 20-10197 | Ramp Magnet |
| 06 | A-22035 | FL-11753 | Diverter Power |
| 07 | A-21564 | FL-11630 | Jet Up |
| 08 | A-21564 | SM1-26-600 | Jet Release |
| 09 | A-19963-1 | AE-26-1500 | Trough Eject |
| 10 | A-21527 | AE-26-1200 | Left Slingshot |
| 11 | A-21527 | AE-26-1200 | Right Slingshot |
| 12 | A-9415-2 | AE-26-1200 | Upper Jet Bumper |
| 13 | A-9415-2 | AE-26-1200 | Lower Jet Bumper |
| 14 | A-21829 | AE-27-1200 | Left Saucer |
| 15 | A-21829 | AE-27-1200 | Right Saucer |
| 16 | A-21825 | AE-26-1500 | Lock Post |
| 22 | A-21953 | A-15680 | Motor Enable |

Item 07 and 08 (Jet Up/Jet Release) share assembly `A-21564`, the "Disappear Jet Bump Assembly" from
the Lower Playfield Parts list (item 8) -- confirmed independently by Service Bulletin 101 ("Subject:
Disappearing Jet Bumper assembly not releasing... brass latch which releases the disappearing jet
bumper was installed incorrectly"). Item 22 (Motor Enable, part A-15680) matches the Ring Master
Assembly (A-21953) and the same A-15680 part reused for solenoid 39 (Motor Direction) on the primary
wiring table.

## Flippers block (same page)

| Item | Assembly Part Number | Coil Part | Description |
| --- | --- | --- | --- |
| 29-30 | A-14876-R | FL-11630 | Lower Right Flipper |
| 31-32 | A-15849-L | FL-11630 | Lower Left Flipper |
| 33 | A-21824 | AL-25-1000 | Popper |
| 34 | A-22035 | FL-11730 | Diverter Hold |
| 35 | A-21953 | 20-10197 | Ringmaster Magnet |
| 36 | A-17932 | AE-27-1200 | Upper Post |

## Motor block (same page)

| Item | Assembly Part Number | PC Board Part | Description |
| --- | --- | --- | --- |
| 37 | A-21577 | -- | Neon |
| 38 | -- | -- | Not Used |
| 39 | A-21953 | A-15680 | Motor Direction |
| 40 | -- | A-22151-2 | Eddy Board |

## General Illumination (same page)

| Item | Bulb Number | Bulb Type | Description |
| --- | --- | --- | --- |
| 01 | 24-6549 | #44 | Playfield Right |
| 02 | 24-6549 | #44 | Playfield Middle |
| 03 | 24-6549 | #44 | Playfield Left |
| 04 | 24-8768 | #555 | Backbox 1 |
| 05 | 24-8768 | #555 | Backbox 2 |

This page's own GI item 04/05 labels ("Backbox 1"/"Backbox 2") are the reverse of the primary wiring
table's item 04/05 labels ("Backbox 2"/"Backbox 1"); see `conflict.gi-backbox-string-numbering`. This
locations page carries no connector data to arbitrate the disagreement, so `solenoid-flasher-table.md`
(which does carry the J106/J104 connector numbers) is used as the connector-to-address source in the
machine definition.
