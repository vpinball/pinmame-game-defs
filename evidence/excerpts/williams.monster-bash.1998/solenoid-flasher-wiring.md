# Monster Bash — Solenoid/Flasher Table (wiring)

Transcribed from `Williams_1998_Monster_Bash_English_Manual.pdf`, PDF page 121, printed page 2-53,
the solenoid/flasher wiring table. Read from the rendered page; the retained scan is image-only. The
general-illumination wiring block printed on the same page is transcribed separately as
`general-illumination.md`.

| Printed | Function | Type | Voltage (playfield / insert) | Drive Xistor | Drive (playfield / insert) |
| --- | --- | --- | --- | --- | --- |
| 01 | AUTO PLUNGER | High Power | J133-2 | Q72 | J116-1 |
| 02 | BRIDE POST | High Power | J133-2 | Q68 | J116-2 |
| 03 | MUMMY COFFIN | High Power | J133-2 | Q71 | J116-4 |
| 04 | NOT USED | High Power | — | Q67 | — |
| 05 | LEFT GATE | High Power | J133-2 | Q70 | J116-6 |
| 06 | RIGHT GATE | High Power | J133-2 | Q66 | J116-7 |
| 07 | NOT USED | High Power | — | Q69 | — |
| 08 | RAMP LOCK POST | High Power | J133-2 | Q65 | J116-9 |
| 09 | TROUGH EJECT | Low Power | J133-3 | Q44 | J113-1 |
| 10 | LEFT SLINGSHOT | Low Power | J133-3 | Q48 | J113-3 |
| 11 | RIGHT SLINGSHOT | Low Power | J133-3 | Q43 | J113-4 |
| 12 | LEFT JET BUMPER | Low Power | J133-3 | Q47 | J113-5 |
| 13 | RIGHT JET BUMPER | Low Power | J133-3 | Q42 | J113-6 |
| 14 | BOTTOM JET BUMPER | Low Power | J133-3 | Q46 | J113-7 |
| 15 | LEFT EJECT | Low Power | J133-3 | Q41 | J113-8 |
| 16 | RIGHT POPPER | Low Power | J133-3 | Q45 | J113-9 |
| 17 | WOLFMAN FLASHERS | Flasher | J133-6 / J134-5 | Q28 | J111-1 / J112-1 |
| 18 | BRIDE FLASHERS | Flasher | J133-6 / J134-5 | Q32 | J111-2 / J112-2 |
| 19 | FRANKENSTEIN FLASHERS | Flasher | J133-6 / J134-5 | Q27 | J111-3 / J112-3 |
| 20 | DRACULA COFFIN FLASHERS | Flasher | J133-6 / J134-5 | Q31 | J111-4 / J112-5 |
| 21 | CREATURE FLASHERS | Flasher | J133-6 | Q26 | J111-5 |
| 22 | JETS/MUMMY FLASHERS | Flasher | J133-6 / J134-5 | Q30 | J111-6 / J112-7 |
| 23 | RIGHT POPPER FLASHER | Flasher | J133-6 | Q25 | J111-7 |
| 24 | FRANK ARROW FLASHER | Flasher | J133-6 | Q29 | J111-8 |
| 25 | MONSTERS OF ROCK FLASHER | Gen. Purpose | J133-6 / J134-5 | Q16 | J109-1 / J108-1 |
| 26 | WOLFMAN LOOP FLASHER | Gen. Purpose | J133-6 | Q15 | J109-2 |
| 27 | FRANKENSTEIN MOTOR | Gen. Purpose | J140-2 | Q14 | J109-3 |
| 28 | UP/DOWN BANK MOTOR | Gen. Purpose | J140-2 | Q13 | J109-4 |

Addresses 04 and 07 each have a populated power-driver transistor (Q67, Q69) but no voltage
connection and no drive connection in any of the playfield, insert, or cabinet columns. No solenoid,
flasher, flipper or motor row in this table uses the cabinet columns at all, so this machine fits no
cabinet solenoid — there is no knocker coil. (The only cabinet connection anywhere on the page is on
general-illumination string 05; see `general-illumination.md`.)

## Flipper circuits (printed numbering)

| Printed | Type | Playfield voltage | Drive Xistor | Playfield drive | Drive wire |
| --- | --- | --- | --- | --- | --- |
| 29 | Power | J119-1 (RED-GRN) | Q90 | J120-13 | YEL-GRN |
| 30 | Hold | J119-1 (RED-GRN) | Q92 | J120-11 | ORG-GRN |
| 31 | Power | J119-4 (RED-BLU) | Q87 | J120-9 | YEL-BLU |
| 32 | Hold | J119-4 (RED-BLU) | Q89 | J120-7 | ORG-BLU |
| 33 | Power (NOT USED) | J119-6 (RED-VIO) | Q84 | J120-6 | YEL-VIO |
| 34 | Hold (NOT USED) | J119-6 (RED-VIO) | Q86 | J120-4 | ORG-VIO |
| 35 | Power (NOT USED) | J119-8 (RED-GRY) | Q81 | J120-3 | YEL-GRY |
| 36 | Hold (NOT USED) | J119-8 (RED-GRY) | Q83 | J120-1 | ORG-GRY |

## Dracula motor circuits (printed numbering)

| Printed | Type | Playfield voltage | Drive gates | Playfield drive |
| --- | --- | --- | --- | --- |
| 37 | Low Power | J141-2 | U3A, U3B | J110-1 |
| 38 | Low Power | J141-2 | U3C, U3D | J110-3 |
