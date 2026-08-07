# Congo -- Solenoid/Flasher Table, General Illumination, Flipper Circuits (manual printed page 2-42, PDF page 111)

Transcribed verbatim from a 300 dpi render of `Congo_OPS.pdf` page 111. Footnote: "J1XX = POWER DRIVER BOARD" and "24-6549 = #44 BULB; 24-8704 = #89 BULB; 24-8768 = #555 BULB; 24-8802 = #906 BULB".

## Solenoid/Flasher Table

Columns: Sol. No. | Function | Solenoid Type | Voltage Connections (Playfield / Backbox / Cabinet) | Drive Xistor | Voltage Connections (Playfield / Backbox / Cabinet) | Drive Wire Color | Solenoid Part Number / Flashlamp Type (Playfield / Backbox).

| No. | Function | Type | Conn 1 (PF/BB/Cab) | Xistor | Conn 2 (PF/BB/Cab) | Wire | Part No. (PF / BB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Auto Plunger | High Power | J133-2 | Q72 | J116-1 | Vio-Brn | AE-23-800 |
| 02 | Kickback | High Power | J133-2 | Q68 | J116-2 | Vio-Red | AE-23-800 |
| 03 | 2-Way Popper Up | High Power | J133-2 | Q71 | J116-4 | Vio-Org | AE-23-800 |
| 04 | 2-Way Popper Down | High Power | J133-2 | Q67 | J116-5 | Vio-Yel | AE-23-800 |
| 05 | Ramp Diverter | High Power | J133-2 | Q70 | J116-6 | Vio-Grn | AE-26-1500 |
| 06 | Volcano Popper | High Power | J133-2 | Q66 | J116-7 | Vio-Blu | AE-23-800 |
| 07 | Knocker | High Power | Cabinet: J133-2 | Q69 | Backbox: J116-8 | Vio-Blk | Backbox: AE-23-800 |
| 08 | Top Loop Post | High Power | J133-2 | Q65 | J116-9 | Vio-Gry | AE-26-1500 |
| 09 | Trough Eject | Low Power | J133-3 | Q44 | J113-1 | Brn-Blk | AE-26-1500 |
| 10 | Left Slingshot | Low Power | J133-3 | Q48 | J113-3 | Brn-Red | AE-26-1200 |
| 11 | Right Slingshot | Low Power | J133-3 | Q43 | J113-4 | Brn-Org | AE-26-1200 |
| 12 | Left Jet Bumper | Low Power | J133-3 | Q47 | J113-5 | Brn-Yel | AE-26-1200 |
| 13 | Right Jet Bumper | Low Power | J133-3 | Q42 | J113-6 | Brn-Grn | AE-26-1200 |
| 14 | Bottom Jet Bumper | Low Power | J133-3 | Q46 | J113-7 | Brn-Blu | AE-26-1200 |
| 15 | Gorilla Right | Low Power | J133-3 | Q41 | J113-8 | Brn-Vio | AE-25-1000 |
| 16 | Gorilla Left | Low Power | J133-3 | Q45 | J113-9 | Brn-Gry | AE-25-1000 |
| 17 | Amy Flasher | Flasher | J133-6 / J134-5 | Q28 | J111-1 / J112-1 | Blk-Brn | #906 (1) / #906 (1) |
| 18 | Left Ramp Fls | Flasher | J133-6 | Q32 | J111-2 | Blk-Red | #89 (1) |
| 19 | 2-Way Popper Fls | Flasher | J133-6 | Q27 | J111-3 | Blk-Org | #89 (1) |
| 20 | Skill Shot Fls | Flasher | J133-6 / J134-5 | Q31 | J111-4 / J112-5 | Blk-Yel | #89 (1) / #906 (1) |
| 21 | Gray Gorilla Fls | Flasher | J133-6 / J134-5 | Q26 | J111-5 / J112-6 | Blu-Grn | #906 (1) / #906 (1) |
| 22 | Map Eject | Flasher | J133-1 | Q30 | J111-6 | Blu-Blk | AE-26-1200 |
| 23 | Left Gate | Flasher | J133-1 | Q25 | J111-7 | Blu-Vio | A-14406 |
| 24 | Right Gate | Flasher | J133-1 | Q29 | J111-8 | Blu-Gry | A-14406 |
| 25 | Lower Right Fls | Gen. Purpose | J133-6 | Q16 | J109-1 | Blu-Brn | #89 (1) |
| 26 | Right Ramp Fls | Gen. Purpose | J133-6 | Q15 | J109-2 | Blu-Red | #89 (1) |
| 27 | Volcano Fls | Gen. Purpose | J133-6 / J134-5 | Q14 | J109-3 / J107-4 | Blu-Org | #89 (2) #906 (1) / #906 (1) |
| 28 | Prmtr Dfns Fls | Gen. Purpose | J133-6 / J134-5 | Q13 | J109-4 / J107-5 | Blu-Yel | #89 (1) / #906 (1) |

Note: the printed "Solenoid Type" column names the power-driver-board circuit class (High Power / Low Power / Flasher / Gen. Purpose), not necessarily the device's function -- rows 22-24 (Map Eject, Left Gate, Right Gate) are wired through the "Flasher" bank alongside the five genuine light flashers (17-21) but are ordinary kicker/gate coils, while the "Gen. Purpose" bank (25-28) drives four genuine flasher bulbs. This is a driver-board wiring-section label, not a `physical.switch_type`/output-kind classification.

Gorilla Left/Right naming (rows 15-16): this printed copy of the table (page 111, printed 2-42) reads row 15 "GORILLA RIGHT" (Q41, J113-8) and row 16 "GORILLA LEFT" (Q45, J113-9). The manual prints this same table two more times -- once in a front-matter quick-reference copy (PDF page 2, no printed page number) and once beside the Section 3 schematics (PDF page 118, printed 3-5) -- and BOTH of those independently read row 15 "GORILLA LEFT" and row 16 "GORILLA RIGHT", the opposite of this page. The Solenoid/Flashlamp Locations page (evidence/excerpts/williams.congo.1995/solenoid-flashlamp-locations.md, printed 2-43) agrees with *this* page's order (15 Right / 16 Left). The manual is therefore split 2-2 across its four printed copies of this fact. The retained known-working script's own solenoid callbacks are named `SolCallBack(15) = "GorillaRight"` and `SolCallBack(16) = "GorillaLeft"` (matching this page's naming), but the callback bodies themselves rotate the opposite-side object: `GorillaRight` (solenoid 15) animates the `GoFlipperLeft` primitive (retained table center x=401.5, left of table center) and `GorillaLeft` (solenoid 16) animates `GoFlipperRight` (center x=461.5, right of table center). Taking the VPX script's actual physical object manipulation as runtime-semantics ground truth over its own sub-naming, solenoid 15 physically drives the left-side arm and solenoid 16 the right-side arm -- agreeing with the front-matter and Section-3 copies (2 of 4 printed instances) rather than this page and the Locations page (the other 2 of 4). The curated definition therefore labels solenoid 15 "Gorilla Left" and solenoid 16 "Gorilla Right", the opposite of the row order printed on this specific page.

## General Illumination

| No. | Function | Type | Conn 1 (PF/BB/Cab) | Xistor | Conn 2 (PF/BB/Cab) | Wire | Bulb (PF/BB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Playfield Gorilla | G.I. | J105-1 / J106-1 | Q5 | J105-7 / J106-7 | Wht-Brn | #555 |
| 02 | Playfield Top | G.I. | J105-2 | Q4 | J105-8 | Wht-Org | #44 |
| 03 | Playfield Bottom | G.I. | J105-3 / J106-3 | Q3 | J105-9 / J106-9 | Wht-Yel | #44 |
| 04 | Backbox String 1 | G.I. | J106-5 | Q2 | J106-10 | Wht-Grn | #555 |
| 05 | Backbox String 2 | G.I. | J106-6 / J104-3 (Cabinet) | Q1 | J106-11 / J104-1 | Wht-Vio | #555 |

## Flipper Circuits

Columns: Sol No. | Circuit label | Voltage Connection (Playfield) | Drive Transistors (Power/Hold) | Drive Connections (Playfield) | Drive Wire Colors (Power/Hold) | Coil Part No. | Coil Color.

| No. | Circuit | Voltage Conn. | Xistor | Drive Conn. | Wire | Coil Part No. | Coil Color |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | Lwr. Rt. Power | J119-1 (Red-Grn) | Q90 | J120-13 | Yel-Grn | -- | -- |
| 30 | LWR RIGHT FLIPPER: Lwr. Rt. Hold | J119-1 (Red-Grn) | Q92 | J120-11 | Org-Grn | FL-11629 | BLUE |
| 31 | Lwr. Lt. Power | J119-4 (Red-Blu) | Q87 | J120-9 | Yel-Blu | -- | -- |
| 32 | LWR LEFT FLIPPER: Lwr. Lt. Hold | J119-4 (Red-Blu) | Q89 | J120-7 | Org-Blu | FL-11629 | BLUE |
| 33 | Upr. Rt. Power | J119-6 (Red-Vio) | Q84 | J120-6 | Yel-Vio | -- | -- |
| 34 | UPPER LEFT POST: Upr. Rt. Hold | J119-6 (Red-Vio) | Q86 | J120-4 | Org-Vio | AE-26-1200 | -- |
| 35 | Upr. Lt. Power | J119-8 (Red-Gry) | Q81 | J120-3 | Yel-Gry | -- | -- |
| 36 | UPR LEFT FLIPPER: Upr. Lt. Hold | J119-8 (Red-Gry) | Q83 | J120-1 | Org-Gry | FL-11630 | RED |

Notes:

- Rows 29-32 are printed in the "Lwr. Rt. Power/Hold" and "Lwr. Lt. Power/Hold" circuit-label slots and physically drive the lower-right and lower-left flippers; PinMAME's public addresses for these two coils are 45-48 (`CORE_FIRSTLFLIPSOL=45`), not the printed 29-32.
- Rows 33-36 sit in the printed "Upr. Rt." and "Upr. Lt." slots, but the manual's own row labels in this table are literally "UPPER LEFT POST" (33/34, not a flipper at all) and "UPR LEFT FLIPPER" (35/36); there is no "Upper Right Flipper" row in this table at all -- confirmed independently by the Switch Locations page marking F5/F6 (Upper Right Flipper E.O.S./Cabinet) "Not Used". PinMAME's `CORE_FIRSTUFLIPSOL=33` places these four printed circuit numbers at identical public addresses 33-36 (no translation).
- The Solenoid/Flashlamp Locations page (evidence/excerpts/williams.congo.1995/solenoid-flashlamp-locations.md) independently names public solenoid 33 "Upper Left Post" and public solenoid 34 "Mystery Eject" -- confirming 33/34 are ordinary non-flipper coils reusing the upper-flipper driver slot, not evidence of a second upper flipper.
