# Scared Stiff — Solenoid/Flasher Table

Transcribed from `Scared_Stiff_OPS.pdf`, PDF page 2 (short form) and PDF pages 118-120 (printed
3-5/3-6, the same table again), the Solenoid/Flasher Table. Produced by rendering the retained PDF at
300-600 dpi with `pdftoppm` and reading the table directly; this scan's text layer is garbled
multi-column OCR and was never trusted.

| Addr | Function | Type | Xistor | Drive conn. | Wire | Part |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Auto Plunger | High Power | Q72 | J116-1 | Vio-Brn | AE-23-800 |
| 02 | Loop Gate | High Power | Q68 | J116-2 | Vio-Red | A-14406 |
| 03 | Right Popper | High Power | Q71 | J116-4 | Vio-Org | AE-24-900 |
| 04 | Coffin Popper | High Power | Q67 | J116-5 | Vio-Yel | AE-23-800 |
| 05 | Coffin Door | High Power | Q70 | J116-6 | Vio-Grn | AE-26-1500 |
| 06 | Crate Kickout | High Power | Q66 | J116-7 | Vio-Blu | AE-24-900 |
| 07 | Knocker (backbox) | High Power | Q69 | J116-8 (backbox) | Vio-Blk | AE-23-800 (backbox) |
| 08 | Crate Post Power | High Power | Q65 | J116-9 | Vio-Gry | FL-11629 |
| 09 | Trough Eject | Low Power | Q44 | J113-1 | Brn-Blk | AE-26-1500 |
| 10 | Left Sling | Low Power | Q48 | J113-3 | Brn-Red | AE-25-1000 |
| 11 | Right Sling | Low Power | Q43 | J113-4 | Brn-Org | AE-25-1000 |
| 12 | Center Jet | Low Power | Q47 | J113-5 | Brn-Yel | AE-26-1200 |
| 13 | Upper Jet | Low Power | Q42 | J113-6 | Brn-Grn | AE-26-1200 |
| 14 | Lower Jet | Low Power | Q46 | J113-7 | Brn-Blu | AE-26-1200 |
| 15 | Upper Slingshot | Low Power | Q41 | J113-8 | Brn-Vio | AE-26-1200 |
| 16 | Crate Post Hold | Low Power | Q45 | J113-9 | Brn-Gry | FL-11629 |
| 17 | Top Jet Flasher | Flasher | Q28 | J111-1 (+J112-1 backbox) | Blk-Brn | 24-8802 / 24-8704 |
| 18 | Middle Jet Flasher | Flasher | Q32 | J111-2 (+J112-2 backbox) | Blk-Red | 24-8802 / 24-8704 |
| 19 | Lower Jet Flasher | Flasher | Q27 | J111-3 (+J112-3 backbox) | Blk-Org | 24-8802 / 24-8704 |
| 20 | Playfield Bolts | Flasher | Q31 | J111-4 | Blk-Yel | 24-8704 (2) |
| 21 | Skull Flasher Left | Flasher | Q25 | J111-5 | Blu-Grn | 24-8802 |
| 22 | Upper Right Flasher | Flasher | Q30 | J111-6 | Blu-Blk | 24-8802 |
| 23 | Left Ramp Flasher | Flasher | (see note) | J111-7 | Blu-Vio | 24-8802 |
| 24 | Center Left Flasher | Flasher | Q29 | J111-8 | Blu-Gry | 24-8802 |
| 25 | Skull Flasher Right | Gen. Purpose | Q16 | J109-1 | Blu-Brn | 24-8802 |
| 26 | Center TV | Gen. Purpose | Q15 | J109-2 (+J107-3) | Blu-Red | 24-8802 |
| 27 | Upper Left Flasher | Gen. Purpose | Q14 | J109-3 | Blu-Org | 24-8802 |
| 28 | Center Right Flasher | Gen. Purpose | Q13 | J109-4 | Blu-Yel | 24-8802 |
| 33 | Left Diverter Power | High Power | Q84 | J120-6 | Yel-Vio | A-20099 |
| 34 | Left Diverter Hold | Low Power | Q86 | J120-4 | Org-Vio | A-20099 |
| 35 | Lower Left Flasher | High Power (DLPDC) | Q81 | J120-3 | Yel-Gry | 24-8802 |
| 36 | Lower Right Flasher | Low Power (DLPDC) | Q83 | J120-1 | Org-Gry | 24-8802 |
| 37 | Aux Lamp Clock (backbox) | DLPDC | -- | J110-1 | Brn-Wht | A-20781 |
| 38 | Aux Lamp Data (backbox) | DLPDC | -- | J110-3 | Org-Wht | A-20781 |
| 39 | Spider Wheel 1 (1.8V, backbox) | DLPDC | -- | J110-4 | Yel-Wht | 14-8024 |
| 40 | Spider Wheel 2 (1.8V, backbox) | DLPDC | -- | J110-5 | Grn-Wht | 14-8024 |
| 45 | Lower Right Flipper Power | Fliptronic | Q90 | J120-13 | Yel-Grn | FL-11629 |
| 46 | Lower Right Flipper Hold | Fliptronic | Q92 | J120-11 | Org-Grn | FL-11629 |
| 47 | Lower Left Flipper Power | Fliptronic | Q87 | J120-9 | Yel-Blu | FL-11629 |
| 48 | Lower Left Flipper Hold | Fliptronic | Q89 | J120-7 | Org-Blu | FL-11629 |

Note on Xistor readings: the scan's dot-matrix resolution makes several individual `Q##` glyphs in
rows 21-24 ambiguous under magnification up to 1200 dpi; the values recorded above (`Q25`, `Q30`,
best-effort `Q26` inferred for the ambiguous row-23 glyph to avoid an implausible duplicate of row
21's confident `Q25`, `Q29`) are secondary provenance and do not gate any authoring-critical fact
(address, function, and polarity are all independently confirmed by the retained script's
`SolModCallback` table and `solenoid-flasher-locations.md`).

## Solenoids 33-36: repurposed upper-flipper circuit

The Flipper Circuits legend printed at the foot of page 3-5 is the generic WPC-95 driver-board
silkscreen table (present on every WPC-95 game regardless of whether upper flippers are fitted): it
captions printed 33/34 "Upr. Rt. Power/Hold" and 35/36 "Upr. Lt. Power/Hold", with coil part number
"SEE ABOVE" pointing back at the game-specific table. The game-specific Solenoid/Flasher table above
overrides that silkscreen caption: 33/34 are "Left Diverter Power/Hold" (driving a lock-gate
mechanism, confirmed by `ss.c`'s own `#define sLDiverterPower 33` / `#define sLDiverterHold 34`) and
35/36 are plain "Lower Left/Right Flasher" outputs. Pinned `ss.c` declares `FLIP_SOL(FLIP_L)` only —
no `FLIP_UR`/`FLIP_UL` bit — so `core_getSol` never routes public 33-36 through any flipper-coil
path; they pass straight through untranslated, exactly like Tales of the Arabian Nights' printed
33-36 and unlike the lower-flipper pair (printed 29-32, which do translate to public 45-48 via
`CORE_FIRSTLFLIPSOL`).
