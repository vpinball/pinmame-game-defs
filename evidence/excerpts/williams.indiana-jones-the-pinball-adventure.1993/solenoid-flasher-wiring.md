# Indiana Jones — Solenoid/Flasher Table

Transcribed from `Indiana_Jones_OPS.pdf`, PDF page 114, printed page 2-50, the Solenoid/Flasher
Table, together with the Flipper Circuits sub-table printed on the same page. Read from the rendered
page, not the OCR text stream, which is scrambled on this scan. The General Illumination line printed
on the same page is transcribed separately as `general-illumination.md`.

| Sol | Function | Type | Drive Xistor | Wire | Part |
| --- | --- | --- | --- | --- | --- |
| 01 | Ball Popper | High Power | Q82 | Vio-Brn | AE-26-1200 |
| 02 | Ball Launch | High Power | Q80 | Vio-Red | AE-23-800 |
| 03 | Totem Drop Up | High Power | Q78 | Vio-Org | AE-26-1200 |
| 04 | Ball Release | High Power | Q76 | Vio-Yel | AE-26-1500 |
| 05 | Center Drop Bank | High Power | Q64 | Vio-Grn | AE-26-1200 |
| 06 | Idol Release | High Power | Q66 | Vio-Blu | AE-26-1200 |
| 07 | Knocker | High Power | Q68 | Vio-Blk | AE-23-800 |
| 08 | Left Eject | High Power | Q70 | Vio-Gry | AE-26-1200 |
| 09 | Left Jet Bumper | Low Power | Q58 | Brn-Blk | AE-26-1200 |
| 10 | Right Jet Bumper | Low Power | Q56 | Brn-Red | AE-26-1200 |
| 11 | Bumper Bottom ("Bumpeur Bas") | Low Power | Q54 | Brn-Org | AE-26-1200 |
| 12 | Left Slingshot (printed; script+driver say Right — see below) | Low Power | Q52 | Brn-Yel | AE-27-1200 |
| 13 | Right Slingshot (printed; script+driver say Left — see below) | Low Power | Q50 | Brn-Grn | AE-27-1200 |
| 14 | Left Control Gate | Low Power | Q48 | Brn-Blu | A-14406 |
| 15 | Right Control Gate | Low Power | Q46 | Brn-Vio | A-14406 |
| 16 | Totem Drop Down | Low Power | Q44 | Brn-Gry | SM1-26-600 |
| 17 | Eternal Life | Flasher | Q42 | Blk-Brn | #906(1)pf/#906(3)bb |
| 18 | Light Jackpot | Flasher | Q40 | Blk-Red | #906(1)pf |
| 19 | Super Jackpot | Flasher | Q38 | Blk-Org | #89(1)pf |
| 20 | Jackpot | Flasher | Q36 | Blk-Yel | #89(1)pf/#906(2)bb |
| 21 | Path Of Adventure | Flasher | Q28 | Blu-Grn | #89(1)pf/#906(4)bb |
| 22 | Mini Motor Left | Low Power | Q30 | Blu-Blk | (blank) |
| 23 | Mini Motor Right | Low Power | Q34 | Blu-Vio | 14-7988 |
| 24 | Plane Gun LEDS | Flasher | Q32 | Blu-Gry | A-16834 |
| 25 | Dogfight Hurry Up | Gen. Purpose | Q26 | Blu-Brn | #89(1) |
| 26 | Right Ramp | Gen. Purpose | Q24 | Blu-Red | #89(3)pf/#906(1)bb |
| 27 | Left Ramp | Gen. Purpose | Q22 | Blu-Org | #89(1)pf/#906(1)bb |
| 28 | Subway Release | Gen. Purpose | Q20 | Blu-Yel | AE-26-1500 |
| 29-36 | *See Flipper Circuits* | | | | |
| 37\* | Left Side Flasher | Low Power | Q16 | Brn-Wht | #89(2)pf/#906(1)bb |
| 38\* | Right Side Flasher | Low Power | Q15 | Blk-Wht | #89(2)pf/#906(1)bb |
| 39\* | Special Flasher | Low Power | Q14 | Org-Wht | #89(2) |
| 40\* | Totem Multiball | Low Power | Q13 | Yel-Wht | #89(1) |
| 41\* | Jackpot Multiplier Fl. | Low Power | Q9 | Grn-Wht | #89(1) |
| 42\* | Wheel Motor | Low Power | Q10 | Blu-Wht | 14-7982 |

`*Note: Controlled from the 8-Driver Board, not the Power Driver Board.`

## Flipper Circuits sub-table

(29) Lower Right Flipper Power / (30) Hold — `FL-11629` blue; (31) Lower Left Flipper Power / (32)
Hold — `FL-11629` blue; 33 Diverter Power / 34 Diverter Hold — `FL-11753-1` brown; 35 Top Lockup
Power / 36 Top Lockup Hold — `A-15943` brown.

## Custom solenoid mapping (printed 37-42, public 51-56)

`ijGameData.hw.custSol = 7` (`{FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L), 1,0,7,...}`) declares 7 custom
solenoids starting at `CORE_FIRSTCUSTSOL = 51` (`CORE_CUSTSOLNO(n) = 50+n`), driven through the
8-Driver PCB's `WPC_EXTBOARD1` register (`0x3feb`, `ij_getSol` reads bits 0-7 for `solNo` in
`[CORE_CUSTSOLNO(1)..CORE_CUSTSOLNO(8)]` = public 51-58). The retained script's own
`SolCallback`/`SolModCallback` comments give the exact mapping, confirmed independently by the
printed Solenoid/Flasher table's identical item list (37-42) and by the driver's single named custom
solenoid (`sWheelMotor = CORE_CUSTSOLNO(6) = 56`):

| Public | Printed | Function |
| --- | --- | --- |
| 51 | 37 | Left Side Flasher (`SolModCallback(51)="solflash51"`) |
| 52 | 38 | Right Side Flasher (`SolModCallback(52)="SolFlash52"`) |
| 53 | 39 | Special Flasher (`SolCallback(53)="SetLamp 116,"`) |
| 54 | 40 | Totem Flasher (`SolCallback(54)="SetLamp 115,"`, comment "Insert:Totem Multi") |
| 55 | 41 | Jackpot Multiplier Flasher (`SolModCallback(55)="solflash55"`) |
| 56 | 42 | Wheel/Idol Motor (`SolCallback(56)="SolMoveIdol"`) |

Public 57 (custSolNo 7, the 7th of the declared 7) and 58 (custSolNo 8, beyond the declared count)
have no printed function and no script binding — recorded `unused`.

## Slingshot solenoid identity: printed vs. runtime (resolved)

Printed row 12 reads "Left Slingshot" and row 13 "Right Slingshot". The retained known-working
script disagrees and is internally self-consistent the other way:
`SolCallback(12)="RandomSoundSlingshotRight" 'Right Sling`,
`SolCallback(13)="RandomSoundSlingshotLeft" 'Left Sling`. `ij.c` agrees with the script:
`#define sRSling 12` / `#define sLSling 13`. The switch side of the same pair is undisputed across
all three sources (switch 33 = Left Slingshot = `swLSling`, switch 48 = Right Slingshot =
`swRSling`), and the script's own physical slingshot objects (`Wall.LeftSlingShot` at normalized
x=0.254, `Wall.RightSlingShot` at x=0.659) sit on the geometrically correct sides for switches 33/48
respectively — so a coil numbered to match the manual's printed row would strike the wrong physical
slingshot relative to its own switch. Two independent, higher-evidence-priority sources (known-
working script + pinned driver) agree against the manual's one row; resolved as public 12 = Right
Slingshot, 13 = Left Slingshot, with the manual's transposed row disclosed here and in the knowledge
note rather than silently corrected.
