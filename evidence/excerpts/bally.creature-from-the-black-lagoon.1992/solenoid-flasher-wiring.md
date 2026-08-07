# Creature from the Black Lagoon — Solenoid/Flasher Table (full wiring)

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 109, printed page 3-5,
"SOLENOID/FLASHER TABLE". Read directly from a 300 dpi `pdftoppm` render (the OCR text layer on this
page is severely garbled, e.g. "Ton Rinhl Penner" for "Top Right Popper").

Columns: Sol No, Function, Solenoid Type, Voltage Connections (Playfield/Backbox/Cabinet), Drive
Transistor, Drive Connections (Playfield/Backbox/Cabinet), Drive Wire Color, Solenoid Part
Number/Flashlamp Type (Playfield/Backbox).

| No | Function | Type | Volt. PF | Volt. BB | Xistor | Drive PF | Drive BB | Wire | Part (PF) | Part (BB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Top Right Popper | High Power | J107-3 | | Q82 | J130-1 | | Vio-Brn | AE-23-800 | |
| 02 | Left Subway Enter Flasher | High Power | J107-5 | J106-5 | Q80 | J130-2 | J132-2 | Vio-Red | #89 | #906(2) |
| 03 | Lower Right Popper | High Power | J107-3 | | Q78 | J130-4 | | Vio-Org | AE-26-1200 | |
| 04 | Trough | High Power | J107-3 | | Q76 | J130-5 | | Vio-Yel | AE-26-1200 | |
| 05 | Right Slingshot | High Power | J107-3 | | Q64 | J130-6 | | Vio-Grn | AE-27-1200 | |
| 06 | Left Slingshot | High Power | J107-3 | | Q66 | J130-7 | | Vio-Blu | AE-27-1200 | |
| 07 | Knocker | High Power | J107-3 | | Q68 | J130-8 | | Vio-Blk | AE-23-800 | |
| 08 | Bottom Right Flasher | High Power | J107-5 | J106-5 | Q70 | J130-9 | J131-5 | Vio-Gry | #89 | #906(2) |
| 09 | Back Flashers | Low Power | J107-6 | | Q58 | J127-1 | | Brn-Blk | #89(2) | |
| 10 | Bowl Flasher | Low Power | J107-6 | J106-5 | Q56 | J127-3 | J129-2 | Brn-Red | #89 | #906(2) |
| 11 | Creature Flasher | Low Power | | J106-5 | Q54 | | J129-4 | Brn-Org | | #906(2) |
| 12 | Outhole | Low Power | J107-2 | | Q52 | J127-5 | | Brn-Yel | AE-27-1200 | |
| 13 | Left Jet | Low Power | J107-2 | | Q50 | J127-6 | | Brn-Grn | AE-26-1200 | |
| 14 | Right Jet | Low Power | J107-2 | | Q48 | J127-7 | | Brn-Blu | AE-26-1200 | |
| 15 | Bottom Jet | Low Power | J107-2 | | Q46 | J127-8 | | Brn-Vio | AE-26-1200 | |
| 16 | Right Popper Flasher | Low Power | J107-5 | J106-5 | Q44 | J127-9 | J128-5 | Brn-Gry | #89 | #906(2) |
| 17 | Bottom Left Flasher | Flasher | J107-5 | J106-5 | Q42 | J126-1 | J125-1 | Blk-Brn | #89 | #906(1) |
| 18 | Right Ramp Flasher | Flasher | J107-5 | J106-5 | Q40 | J126-2 | J125-2 | Blk-Red | #89 | #906(2) |
| 19 | Left Ramp Flasher | Flasher | J107-5 | J106-5 | Q38 | J126-3 | J125-3 | Blk-Org | #89 | #906(2) |
| 20 | Sequential G.I. #1 | Flasher | J118-2 | | Q36 | J126-4 | | Blk-Yel | #86 | |
| 21 | Hologram Push Motor (playfield) | Flasher | J104-1,2 | | Q28 | J126-5 | | Blu-Grn | 14-7977 48VAC | |
| 22 | Center Hole Flasher | Flasher | J107-6 | J106-5 | Q30 | J126-6 | J125-7 | Blu-Blk | #89 | #906(2) |
| 23 | Up/Down Ramp (up) | Low Power | J107-1 | | Q34 | J126-7** | | Blu-Vio | SM1-2B-900-DC | |
| 24 | Sequential G.I. #2 | Low Power | J118-2 | | Q32 | J126-8 | | Blu-Gry | #86 | |
| 25 | Start Movie Flashers | Flasher | J107-6 | | Q26 | J122-1 | | Blu-Brn | #89(2) | |
| 26 | Up/Down Ramp (down) | Flasher | J107-1 | | Q24 | J122-2* | | Blu-Red | AE-26-1200 | |
| 27 | Creature Motor (mirror) | Flasher | | | Q22 (cabinet J104-1,2) | | J123-4 | Blu-Org | 14-7977 48VAC | |
| 28 | Hologram Lamp (cabinet) | Flasher | | | Q20 (cabinet J118-2) | | J123-5 | Blu-Yel | #1156 | |

`* J122-6, Violet-Green, Tieback Diode.` `** J126-12, Violet-Green, Tieback Diode.`
`J1XX = Power Driver Board, J9XX = Fliptronic II Board.`

## General Illumination (same page)

| No | Function | Volt. PF | Volt. BB | Xistor | Drive PF | Drive BB | Wire | Part (PF) | Part (BB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Sequential G.I. #1 | J120-1 | | Q18 | J120-7 | | Wht-Brn | #86 | |
| 02 | Insert/Playfield (middle) | J120-2 | J121-2 | Q10 | J120-8 | J121-8 | Wht-Org | #44 | #555 |
| 03 | Insert/Playfield (upper) | J120-3 | J121-3 | Q14 | J120-9 | J121-9 | Wht-Yel | #44 | #555 |
| 04 | Sequential G.I. #2 | J120-5 | | Q15 | J120-10 | | Wht-Grn | #86 | |
| 05 | Insert/Playfield (lower) | J120-6 | J121-6 | Q12 | J120-11 | J121-11 | Wht-Vio | #44 | #555 |

## Flipper Circuits (same page)

| Circuit | Volt. PF | Wire | Xistor | Drive PF | Wire | Part | Backbox |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lower Left Flipper | J907-4,5 | Gry-Yel | Q2 (power) / Q7 (holding) | J902-7,9 | Blu-Gry / Org-Blu | FL-15411 | ORG |
| Lower Right Flipper | J907-1,2 | Blu-Yel | Q3 (power) / Q9 (holding) | J902-11,13 | Blu-Vio / Org-Grn | FL-11629 | BLU |

This table is the direct confirmation for the Sequential G.I. mechanism split described in
`solenoid-flasher-locations.md`: GI address 0 ("Sequential G.I. #1", public GI output) is driven from
`J120-1`/`Q18`/`J120-7`, while solenoid 20 (the address-select line of the same printed name) is driven
from an entirely different connector pair `J118-2`/`Q36`/`J126-4`. The same split holds for GI address 3
("Sequential G.I. #2", `J120-5`/`Q15`/`J120-10`) versus solenoid 24 (`J118-2`/`Q32`/`J126-8`). Both
select-line solenoids (20, 24) and the two cabinet-mounted devices (27 Creature Motor, 28 Hologram Lamp)
share connector `J118-2`/`J104-1,2` for their voltage feed, consistent with all four living on the same
under-playfield/cabinet hologram-and-chase-light wiring harness.
