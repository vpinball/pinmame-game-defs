# The Who's Tommy Pinball Wizard (Data East 1994) - Cabinet parts and the motor circuits of the playfield coil wiring diagram

Transcribed by hand from native-resolution (300 dpi) renders of printed page 39 (PDF 43, `Cabinet Parts Illustration`) and printed page 64 (PDF 71, the left half of the `Playfield Coil/Flashlamp Wiring Diagram`) of the IPDB-hosted scan `Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf`. Every cell was read from the render.

## Cabinet Parts Illustration (printed page 39), the rows this definition cites

The page notes `An asterisk (*) indicates item is not shown in above illustration.` The rows below are the ones the definition cites, transcribed literally; the table's other rows (legs, glass, hinges, cash box and similar hardware) are not transcribed.

| Item | Description | Part No. |
| --- | --- | --- |
| 2 | Flipper Button | 500-5026-32 |
| 12A | Memory Protect Switch (Loc. in item 13) | 180-5000-00 |
| 12B | Interlock & Momentary Diagnostics Switch Set (Located in Item 13) | 180-5012-00 |
| 14 | Start Button Switch Ass'y (Touch Me) | 500-5728-01 |
| 15 | Flipper Switch, Double, Left Top/Bottom | 180-5122-00 |
| 15A | Flipper Switch, Upper, Right * | 180-5048-01 |
| 17 | Plumb Bob Tilt Assembly | 500-5023-00 |
| 25 | Solid State 3 - Flipper Board (SSFB) | 520-5076-00 |
| 33 | Coin Door (w/Validator) USA | 500-5018-17 |
| 34 | Shaker Motor (Not Used in this Game) | 515-5893-00 |
| 35 | Shaker Motor P.C. Board | 520-5065-00 |
| 39 | Extra Ball Switch Ass'y (Orange) | 500-5779-07 |
| 40 | Knocker | 500-5081-00 |

## Playfield Coil/Flashlamp Wiring Diagram (printed page 64), the motor and direct-drive circuits

The left half of the drawing shows, from CPU connector `CN 12`:

- pin `6` (`Q26`): wire `BLU/GRN` to `AIRPLANE MOTORS`, two motor symbols drawn in parallel, whose other side returns on `GRY/BLU` to `SHAKER MOTOR BOARD J1-P4/5`;
- pin `5` (`Q27`): wire `BRN/YEL` to `DIVERTER 27-1500`, powered `RED` from `+32 VDC PS CN3-7/6`;
- a `BRN/VIO` wire that runs right into the drawing's connector fan-out (the coil tables put `BRN-VIO` on CPU CN12-8, drive 15): four bulbs labelled `(1) PLFD (3) INSERT`, powered `ORG` from `+32VDCR PPB J6-4/5`;
- pin `7` (`Q25`): wire `BRN/BLU` to the coil of a `RELAY BOARD 520-5010-00` powered `RED` from `+32 VDC PS CN3-7/6`; the relay's `N.O.` contact takes `WHT/RED` `FROM BR2 28 VAC`, its `COMM` contact returns `WHT/RED` to a motor symbol whose other side is `WHT`, and its `N.C.` contact is marked `N.U.`;
- pin `1` (`Q30`): wire `WHT/BRN` through `D18 1N4004` and `R16 220` to the base of `Q1 TIP 36C`, whose output `BRN/BLK` runs to `SHAKER MOTOR BOARD J1-P6/7` and the `CABINET SHAKER MOTOR 12VDC` through a `1/2 Ω TO 1 Ω RESISTOR`. The shaker motor board takes `9VAC` from `POWER SUPPLY CN1-P11` (`GRY`) and `CN1-P10` (`GRY-GRN`) through three `2.5A` fuses `F1`-`F3` and diodes `1N5404` `D1`-`D3`; its `J1-P1/3` output on `GRY-BLU` is labelled `TO AIRPLANE MOTOR`.

The right half of the same page draws the knocker (`KNOCKER 23-800 8L`, `VIO/GRY`, `+32VL PPB J6-2/1`) and the PPB connector fan-out; it is not transcribed here.
