# WHO dunnit — solenoid, flasher, G.I. and flipper circuits

Source: Bally *WHO dunnit* manual, PDF pages 128–129, printed 2-46–2-47, duplicate PDF 137, printed 3-5, PDF page 155, printed 3-23 reel driver connectors, and PDF pages 158–159, printed 3-26–3-27 board layout/list. Transcribed and visually checked against the original embedded rasters at native dimensions on 2026-09-30. The printed “Solenoid Type” column is retained even where it calls a motor a flasher. PDF 137 repeats the solenoid, reel and G.I. circuit cells above/below; it belongs to the same manual and is not an independent document family. Its differing lower-flipper coil cells are retained separately.

| No. | Function | Printed type | Voltage connector | Drive transistor | Drive connector | Wire | Fitted device |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Trough | High Power | J107-2 playfield | Q82 | J130-1 playfield | Vio-Brn | AE-26-1500 |
| 02 | Plunger | High Power | J107-2 playfield | Q80 | J130-2 playfield | Vio-Red | AE-23-800 |
| 03 | Left Lock Up | High Power | J107-2 playfield | Q78 | J130-4 playfield | Vio-Org | AE-27-1200 |
| 04 | Right Back Popper | High Power | J107-2 playfield | Q76 | J130-5 playfield | Vio-Yel | AE-24-900 |
| 05 | Ramp Down | High Power | J107-2 playfield | Q64 | J130-6 playfield | Vio-Grn | AE-26-1200 |
| 06 | Not Used | High Power | blank | Q66 | blank | Vio-Blu | --- |
| 07 | Knocker | High Power | J107-2 backbox | Q68 | J130-8 backbox | Vio-Blk | AE-23-800 |
| 08 | Right Front Popper | High Power | J107-2 playfield | Q70 | J130-9 playfield | Vio-Gry | AE-23-800 |
| 09 | Left Sling | Low Power | J107-3 playfield | Q58 | J127-1 playfield | Brn-Blk | AE-26-1200 |
| 10 | Right Sling | Low Power | J107-3 playfield | Q56 | J127-3 playfield | Brn-Red | AE-26-1200 |
| 11 | Left Jet | Low Power | J107-3 playfield | Q54 | J127-4 playfield | Brn-Org | AE-26-1200 |
| 12 | Bottom Jet | Low Power | J107-3 playfield | Q52 | J127-5 playfield | Brn-Yel | AE-26-1200 |
| 13 | Right Jet | Low Power | J107-3 playfield | Q50 | J127-6 playfield | Brn-Grn | AE-26-1500 |
| 14 | Phone Flasher | Low Power | J107-6 playfield | Q48 | J127-7 playfield | Brn-Blu | #906 (1) |
| 15 | Not Used | Low Power | blank | Q46 | blank | Brn-Vio | --- |
| 16 | Ramp Up | Low Power | J107-3 playfield | Q44 | J127-9 playfield | Brn-Gry | SM1-28-900-DC |
| 17 | Back Flasher | Flasher | J107-6 playfield; J105-5 backbox | Q42 | J126-1 playfield; J125-1 backbox | Blk-Brn | #906 (2) playfield; #906 (1) backbox |
| 18 | Autofire Flasher | Flasher | J107-6 playfield | Q40 | J126-2 playfield | Blk-Red | #89 (1) |
| 19 | Lower Left Flasher | Flasher | J107-6 playfield; J105-5 backbox | Q38 | J126-3 playfield; J125-3 backbox | Blk-Org | #906 (1) playfield; #906 (1) backbox |
| 20 | Spinner Flasher | Flasher | J107-6 playfield; J105-5 backbox | Q36 | J126-4 playfield; J125-5 backbox | Blk-Yel | #906 (1) playfield; #906 (2) backbox |
| 21 | Lower Right Flasher | Flasher | J107-6 playfield; J105-5 backbox | Q28 | J126-5 playfield; J125-6 backbox | Blu-Grn | #906 (1) playfield; #906 (1) backbox |
| 22 | Motor 3-Bank | Flasher | J116-2 playfield | Q30 | J126-6 playfield | Blu-Blk | 14-8026 12V |
| 23 | Left Slot B | Flasher | J116-2 playfield | Q34 | J126-7 playfield | Blu-Vio | 14-8024 12V |
| 24 | Left Slot A | Flasher | J116-2 playfield | Q32 | J126-8 playfield | Blu-Gry | 14-8024 12V |
| 25 | Center Slot B | Gen. Purpose | J116-2 playfield | Q26 | J122-1 playfield | Blu-Brn | 14-8024 12V |
| 26 | Center Slot A | Gen. Purpose | J116-2 playfield | Q24 | J122-2 playfield | Blu-Red | 14-8024 12V |
| 27 | Right Slot B | Gen. Purpose | J116-2 playfield | Q22 | J122-3 playfield | Blu-Org | 14-8024 12V |
| 28 | Right Slot A | Gen. Purpose | J116-2 playfield | Q20 | J122-4 playfield | Blu-Yel | 14-8024 12V |
| 36 | Up Down Post | Low Power | J907-8,9 playfield | Q5 | J902-1 playfield | Org-Gry | AE-27-1200 |

The same printed 2-46 page's solenoid location list calls Right Jet 13 an `AE-26-1200` coil in A-9415-2, while the drive table above prints `AE-26-1500`. The A-9415-2 jet bumper exploded parts drawing on PDF page 103, printed 2-21, also lists `AE-26-1200`. This is a real discrepancy within the factory manual; preserve both readings until an original fitted assembly or another authoritative factory correction resolves it.

Rows 23/24 and 27/28 above are also disputed physical connector claims: PDF 155 (3-23) labels Left Reel Sol 23 & 24 at J122-3/-4 Blue-Orange/Blue-Yellow and Right Reel Sol 27 & 28 at J126-7/-8 Blue-Violet/Blue-Gray, reversing the left/right connector assignments in this table. Center 25/26 J122-1/-2 agrees. Both claims are retained in [the reel driver excerpt](service-mechanisms.md) and `conflict.reel-drive-connectors`; the structured table transcription is conflicted, not a resolved routing choice.

| Printed G.I. no. | Function | Type | Voltage connector | Triac | Return connector | Wire | Bulb/location |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Left Playfield | G.I. | J121-1 playfield | Q18 | J121-7 playfield | Wht-Brn | #44, string 1 |
| 02 | Right Playfield | G.I. | J121-2 playfield | Q10 | J121-8 playfield | Wht-Org | #44, string 2 |
| 03 | Back Playfield | G.I. | J121-3 playfield | Q14 | J121-9 playfield | Wht-Yel | #44, string 3 |
| 04 | Insert 1 | G.I. | J120-5 backbox | Q16 | J120-10 backbox | Wht-Grn | #555, string 4 |
| 05 | Insert 2 | G.I. | J120-6 backbox | Q12 | J120-11 backbox | Wht-Vio | #555, string 5 |

All five G.I. rows are **circuit/location-table claims**, including the #44/#555 bulbs and playfield/backbox columns. Native PDF 158's A-12697-4 layout shows J120/J121, but its pin list ends J111; PDF 159 resumes J128. The omitted J112–J127 connector-list entries supply no G.I. pin destinations. Wiring, bulb/location fields and backbox exclusions remain source-specific candidates pending the game's populated-branch schematic/list or an original harness survey. The gap alone is not an incompatible physical claim and creates no new conflict. Script collection bindings remain separately scoped emulator evidence.

The complete applicable bulb part legend printed at the bottom of PDF 128 and PDF 137 and beside the PDF 129 location list is:

| Printed part number | Printed bulb type |
| --- | --- |
| 24-6549 | #44 |
| 24-8704 | #89 |
| 24-8768 | #555 |
| 24-8802 | #906 |

The flipper circuit table prints lower-right power/hold as 29/30, lower-left power/hold as 31/32, upper-right power/hold as 33/34 and upper-left power/hold as 35/36. PDF 128/129 names FL-15411 orange in assemblies A-14876-R-5 and A-15849-L-4; duplicate PDF 137 instead prints **FL-11541** for both lower flippers. PDF 98/99 assembly item 12 also prints FL-15411, but no applicable factory correction explicitly settles the duplicate reading. Both coil claims remain unresolved in `conflict.lower-flipper-coil-part`; no fitted coil part is selected. [The complete winding/assembly excerpt](flipper-circuits.md) retains both readings. Upper-right says “NOT USED” in both coil columns. Upper-left prints “SEE” in the Coil Part No. column and “ABOVE” in the Coil Color column: “SEE ABOVE” spans both columns. The separate 36 row and location list identify its repurposed Up Down Post load. The lower-flipper drives are J902-13/-11 and J902-9/-7; the upper drives J902-6/-4 and J902-3/-1. The parts list on 2-47 names fitted output assemblies A-19963-1, A-20439, A-20435, A-19543, A-20231, B-10686-1, A-20488, B-9362-L-2, B-9362-R-3, A-9415-2, A-17802, A-20420, A-17803, A-20531, A-20493, A-20523, A-20483, A-20425 and A-17932; the functions match the numbered table above.
