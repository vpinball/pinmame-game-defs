# Star Trek: The Next Generation — Solenoid/Flasher Table

Transcribed from `Star_Trek_TNG_OPS.pdf`, PDF page 96, printed page 2-44, the Solenoid/Flasher Table,
together with the Flipper Circuits sub-table printed on the same page. This scan carries a searchable
OCR text layer, but it was visually confirmed against the rendered page. The General Illumination
wiring table printed on the same page is transcribed separately as `general-illumination.md`.

| Sol. | Function | Type | Playfield conn. | Drive transistor | Drive conn. | Wire | Part |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Left Gun Kicker | High Power | J107-3 | Q82 | J130-1 | Vio-Brn | AE-23-800 |
| 02 | Right Gun Kicker | High Power | J107-3 | Q80 | J130-2 | Vio-Red | AE-23-800 |
| 03 | Left Gun Popper | High Power | J107-3 | Q78 | J130-4 | Vio-Org | AE-23-800 |
| 04 | Right Gun Popper | High Power | J107-3 | Q76 | J130-5 | Vio-Yel | AE-23-800 |
| 05 | Left Popper | High Power | J107-3 | Q64 | J130-6 | Vio-Grn | AE-23-800 |
| 06 | Plunger | High Power | J107-3 | Q66 | J130-7 | Vio-Blu | AE-23-800 |
| 07 | Knocker | High Power | (backbox J107-3) | Q68 | J130-8 (backbox) | Vio-Blk | AE-23-800 (backbox) |
| 08 | Kickback | High Power | J107-3 | Q70 | J130-9 | Vio-Gry | AE-23-800 |
| 09 | Left Slingshot | Low Power | J107-2 | Q58 | J127-1 | Brn-Blk | AE-26-1200 |
| 10 | Right Slingshot | Low Power | J107-2 | Q56 | J127-3 | Brn-Red | AE-26-1200 |
| 11 | Trough | Low Power | J107-2 | Q54 | J127-4 | Brn-Org | AE-26-1500 |
| 12 | Left Jet Bumper | Low Power | J107-2 | Q52 | J127-5 | Brn-Yel | AE-26-1200 |
| 13 | Right Jet Bumper | Low Power | J107-2 | Q50 | J127-6 | Brn-Grn | AE-26-1200 |
| 14 | Bottom Jet Bumper | Low Power | J107-2 | Q48 | J127-7 | Brn-Blu | AE-26-1200 |
| 15 | Top Divertor | Low Power | J107-2 | Q46 | J127-8 | Brn-Vio | AE-25-1000 |
| 16 | Borg Kicker | Low Power | J107-2 | Q44 | J127-9 | Brn-Gry | AL-23-800 |
| 17 | Left Gun Motor | Low Power | J118-2 | Q42 | J126-1 | Blk-Brn | A-17562 |
| 18 | Right Gun Motor | Low Power | J118-2 | Q40 | J126-2 | Blk-Red | A-17562 |
| 19 | Not Used | — | — | Q38 | — | Blk-Org | — |
| 20 | Jets Flasher | Flasher | J107-6 | Q36 | J126-4 | Blk-Yel | #89 (1) |
| 21 | Right Popper Flasher | Flasher | J107-6 / J106-5 | Q28 | J126-5 / J125-6 | Blu-Grn | #89(1) playfield, #906(1) backbox |
| 22 | Middle Ramp Flasher | Flasher | J107-6 | Q30 | J126-6 | Blu-Blk | #89(1) |
| 23 | Shields Flasher | Flasher | J107-6 / J106-5 | Q34 | J126-7 / J125-8 | Blu-Vio | #906(3) playfield, #906(1) backbox |
| 24 | Autofire Flasher | Flasher | J107-6 | Q32 | J126-8 | Blu-Gry | #906(1) |
| 25 | Exit Un. Gnd. Flasher | Gen. Purpose | J107-6 / J106-5 | Q26 | J122-1 / J124-1 | Blu-Brn | #89(1) playfield, #906(1) backbox |
| 26 | Right Borg Flasher | Gen. Purpose | J107-6 / J106-5 | Q24 | J122-2 / J124-2 | Blu-Red | #906(2) playfield, #906(1) backbox |
| 27 | Left Borg Flasher | Gen. Purpose | J107-6 / J106-5 | Q22 | J122-3 / J124-3 | Blu-Org | #906(2) playfield, #906(1) backbox |
| 28 | Center Borg Flasher | Gen. Purpose | J107-6 / J106-5 | Q20 | J122-4 / J124-5 | Blu-Yel | #906(2) playfield, #906(1) backbox |
| 29-36 | see Flipper Circuits | — | — | — | — | — | — |
| 37\* | Under Divertor Top | Low Power | J107-1 | Q16 | J4-2 | Brn-Wht | AE-25-1000 |
| 38\* | Under Divertor Bot. | Low Power | J107-1 | Q15 | J4-4 | Blk-Wht | AE-25-1000 |
| 39\* | Top Drop Up | Low Power | J107-1 | Q14 | J4-5 | Org-Wht | AE-26-1200 |
| 40\* | Top Drop Down | Low Power | J107-1 | Q13 | J4-6 | Yel-Wht | SM1-26-600 |
| 41\* | Romulan Flashers | Low Power | J107-6 / J106-5 | Q9 | J3-2 / J3-2 | Gm-Wht | #906(1) playfield, #906(1) backbox |
| 42\* | Right Ramp Flashers | Low Power | J107-6 / J106-5 | Q10 | J3-3 / J3-3 | Blu-Wht | #89(1) playfield, #906(1) backbox |

`*Note: Controlled from the 8-Driver Board, not the Power Driver Board.` These six items are printed
37-42 on the board's own silkscreen and are captured only as `manual.address` aliases: `sttng.c`
declares `hw.custSol = 6`, publishing at `CORE_CUSTSOLNO(n) = CORE_FIRSTCUSTSOL - 1 + n = 50 + n`,
i.e. public 51-56. The retained known-working script's own `SolCallBack(51) = "UnderDiverterTop"`,
`(52) = "UnderDiverterBottom"`, `(53) = "TopDrop.SolDropUp"`, `(54) = "TopDrop.SolDropDown"`,
`SolModCallBack(55) = "Flash141"` ("RomulanFlasher"), `(56) = "Flash142"` ("RightRampFlasher")
independently confirm 51-56 — and structurally, `core_getSol`'s `solNo <= 44` branch returns
constant 0 for `GEN_WPCDCS` before ever reaching `hw.getSol`, so `sttng_getSol` (which implements
these six outputs by reading `WPC_EXTBOARD1` bits 0-5) could only ever be invoked at addresses above
50 in the first place — three independent lines of evidence (core.h arithmetic, the retained script,
and the dispatch structure itself) agree on 51-56 against the manual/driver-comment's stale "37-42".

## Flipper Circuits

Printed items map to WPC-DCS public solenoids per the `pinmame.wpc-dcs` profile: printed 29/30 →
public 45/46, printed 31/32 → public 47/48, printed 33-36 → public 33-36 unchanged.

| Printed | Function | Voltage conn. | Power/Hold transistor | Drive conn. | Coil part |
| --- | --- | --- | --- | --- | --- |
| 29 | Lower Right Power | J907-7 (Blu-Yel) | Q4 | J902-13 | FL-11629 |
| 30 | Lower Right Hold | J907-7 (Blu-Yel) | Q11 | J902-11 | FL-11629 |
| 31 | Lower Left Power | J907-9 (Gry-Yel) | Q3 | J902-9 | FL-11629 |
| 32 | Lower Left Hold | J907-9 (Gry-Yel) | Q9 | J902-7 | FL-11629 |
| 33 | Upper Right Power | J907-1 (Blu-Yel) | Q2 | J902-6 | FL-11629 |
| 34 | Upper Right Hold | J907-1 (Blu-Yel) | Q7 | J902-4 | FL-11629 |
| 35 | Upper Left Power | J907-4 (Gry-Yel) | Q1 | J902-3 | Not Used |
| 36 | Upper Left Hold | J907-4 (Gry-Yel) | Q5 | J902-1 | Not Used |
