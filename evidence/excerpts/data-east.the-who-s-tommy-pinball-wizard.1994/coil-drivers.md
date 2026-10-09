# The Who's Tommy Pinball Wizard (Data East 1994) - Coil and flash-lamp drivers, Flipper Solenoids and the coil chart schematic

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 36, 37 and 38 (PDF 40, 41 and 42) of the IPDB-hosted scan `Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf`. The scan has no text layer; OCR text was used only to locate the pages, and every cell below was read from the render.

Printed page 36 states: `Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.` It names the Flash Lamp test (all flash lamps fire randomly), the Automatic Test (`ALL COILS`, pulsing each regular solenoid or flash lamp in sequence with its name and wire colours) and the Select Coil test (`Operate either Flipper push-button switch to select the coil or flash lamp to be tested`).

## Coil test index (printed page 36)

The page prints a two-column index under a playfield drawing and a `Backbox Flash Lamps` drawing, and the footnote `Note: Shaded areas not shown on Diagrams.` (no row is visibly shaded on the 1-bit scan).

| Coil | Name |
| --- | --- |
| 1L | 6-Ball Ass'y Lockout |
| 1R | Bot. Arch Lt. & Rt. |
| 2L | Ball Eject |
| 2R | Upper Rt. Corner |
| 3L | Auto Ball Launch |
| 3R | Left Scoop |
| 4L | VUK |
| 4R | Upper Right |
| 5L | Left Scoop |
| 5R | Turbo Hot Dog |
| 6L | Eject |
| 6R | Back Panel |
| 7L | NOT USED |
| 7R | Lower Rt. Hot Dog |
| 8L | Knocker |
| 8R | Hot Dogs |
| 09 | NOT USED |
| 10 | Left/Right Relay |
| 11 | G.I. Relay |
| 12 | Top Diverter |
| 13 | Airplane Motor |
| 14 | Mirror Motor Relay |
| 15 | Tommy Flash |
| 16 | NOT USED |
| 17 | Top Left Turbo |
| 18 | Top Center Turbo |
| 19 | Top Right Turbo |
| 20 | Left Slingshot |
| 21 | Right Slingshot |
| 22 | NOT USED |

The `Backbox Flash Lamps` drawing shows balloons `15` (three), `3R` (two), `4R` (two) and `7R` (two).

## Switched, CPU Controlled Auxiliary & Constant Power Solenoids (printed page 37)

The table's subtitle reads `GRY-BRN through GRY-BLK`. Its headings are `Coil No.`, `Coil or Flashlamp Description`, `Drive Transistor (D.T.)`, `On Which Board?`, `D.T. Control Line`, `D.T. Control Line Connect`, `Power Line`, `Power Line Connection`, `Power Description` and `Coil or Flash Type`. Drives 1-8 print one transistor and board cell merged across the L and R rows; the transcription repeats it on both rows.

| Coil | Description | Drive transistor | Board | Control line | Control connect | Power line | Power connection | Power description | Coil or flash type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1L | Coil: 6-Ball Ass'y Lockout | Q46 | CPU | VIO-BRN | PPB J2-10 | BRN | PPB J6-3 | 32v L | 25-1240 |
| 1R | Flashlamp: X4 By Bottom Arch Lt & Right | Q46 | CPU | BLK-BRN | PPB J9-5 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 2L | Coil: Ball Eject | Q45 | CPU | VIO-RED | PPB J2-9 | BRN | PPB J6-3 | 32v L | 23-800 |
| 2R | Flashlamp: X4 Upper Right Corner | Q45 | CPU | BLK-RED | PPB J9-6 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 3L | Coil: Auto Ball Launch | Q44 | CPU | VIO-ORG | PPB J8-2 | YEL/VIO | PPB J7-8, 9 | 32v L | 22-600 |
| 3R | Flashlamp: X2 Left Scoop | Q44 | CPU | BLK-ORG | PPB J9-7 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 4L | Coil: VUK | Q43 | CPU | VIO-YEL | PPB J8-4 | BRN/VIO | PPB J7-8, 9 | 32v L | 23-800 |
| 4R | Flashlamp: X2 Upper Right | Q43 | CPU | BLK-YEL | PPB J9-8 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 5L | Coil: Left Scoop | Q42 | CPU | VIO-GRN | PPB J2-6 | BRN | PPB J6-3 | 32v L | 23-800 |
| 5R | Flashlamp: X4 Turbo Hot Dog | Q42 | CPU | BLK-GRN | PPB J9-9 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 6L | Coil: Eject | Q41 | CPU | VIO-BLU | PPB J2-5 | BRN | PPB J6-3 | 32v L | 24-940 |
| 6R | Flashlamp: X4 Back Panel | Q41 | CPU | BLK-BLU | PPB J9-10 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 7L | Coil: Not Used | Q40 | CPU | Not Used | PPB J2-3 | Not Used | --- | --- | Not Used |
| 7R | Flashlamp: X2 Lower Right Hot Dog | Q40 | CPU | BLK-VIO | PPB J9-11 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 8L | Coil: Knocker | Q39 | CPU | VIO-GRY | PPB J2-2 | BRN | PPB J6-3 | 32v L | 23-800 |
| 8R | Flashlamp: X4 Hot Dogs | Q39 | CPU | BLK-GRY | PPB J9-12 | ORG | PPB J6-4, 5 | 32v R | Bulb #89 |
| 09 | Coil: Shaker Motor TIP 36C | Q1 | PPB | BRN-BLK | PPB J9-12 | GRY/GRN | PS CN3-10 | 9v AC | --- |
| 10 | Coil: Left & Right Relay | Q29 | CPU | BRN-RED | CPU CN12-2 | RED/WHT | PS CN3-5 | 32v | 24v DC 10A OPDT |
| 11 | Coil: G.I. Relay | Q28 | CPU | BRN-ORG | CPU CN12-4 | RED | PS CN3-6, 7, 8 | 32v | (blank) |
| 12 | Coil: Top Diverter | Q27 | CPU | BRY-YEL | CPU CN12-5 | RED | PS CN3-6, 7, /F/8 | 32v | 27-1500 |
| 13 | Coil: Airplane Motor | Q26 | CPU | BRN-GRN | CPU CN12-6 | BLU/GRY | SMB J3-P 1/3 | 9v DC | --- |
| 14 | Coil: Mirror Motor Relay | Q25 | CPU | BRN-BLU | CPU CN12-7 | RED | PS CN3-6, 7, 8 | 32v | --- |
| 15 | Flashlamp: X1 Tommy | Q24 | CPU | BRN-VIO | CPU CN12-8 | RED | PPB J6-4, 5 | 32v R | Bulb #89 |
| 16 | Coil: Not Used | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | Coil: Top Left Turbo Bumper | Q11 | CPU | BLU-BRN | CPU CN19-7 | RED | PS CN3-6 | 32v | 23-800 |
| 18 | Coil: Top Center Turbo Bumper | Q9 | CPU | BLU-RED | CPU CN19-4 | RED | PS CN3-6 | 32v | 23-800 |
| 19 | Coil: Top Right Turbo Bumper | Q8 | CPU | BLU-ORG | CPU CN19-3 | RED | PS CN3-6 | 32v | 23-800 |
| 20 | Coil: Left Slingshot | Q10 | CPU | BLU-YEL | CPU CN19-5 | RED | PS CN3-6 | 32v | 23-800 |
| 21 | Coil: Right Slingshot | Q12 | CPU | BLU-GRN | CPU CN19-8 | RED | PS CN3-6 | 32v | 23-800 |
| 22 | Coil: Not Used | --- | --- | --- | CPU CN19-9 | --- | PPB J7-3 | 32v | 23-800 |

Normalization and readings: the scan fills in the first digit of several PPB connector numbers (the `J?-5` to `J?-12` right-set returns, the `J?-2` and `J?-4` cells of 3L and 4L, and every `J?-3` / `J?-4, 5` power cell). Those digits were settled from the coil chart schematic on printed page 38 (below), which prints `J9` beside every right-set return, `J8` at the booster outputs of drives 3 and 4, `J6` at every `+32 VR` and `+32 VL` pin and `J7` at the `+50 VL` pins. Drive 09's control-connect cell is printed `PPB J9-12` (the same filled-in digit), which repeats 8R's connector. `BRY-YEL` on drive 12 is the print's own spelling (the schematic draws the wire `BRN/YEL`). The 12 power-connection cell is printed `CN 3-6, 7, /F/8`, transcribed with the print's slash marks. The 11 coil-type cell is printed empty. Drive 22 prints dashes in every cell except `CPU CN19-9`, `PPB J7-3`, `32v` and `23-800`.

The table ends with the line `Additional Coil(s) from Auxiliary Board: Servo (GRN/WHT)/ GRY/ORG` and three notes: `NOTE 1: SEE THE PREVIOUS PAGE FOR LOCATIONS OF ABOVE ON THE PLAYFIELD AND BACKBOX.`, `NOTE 2: SEE THE NEXT PAGE FOR THE COIL CHART SCHEMATIC.` and `NOTE 3: FOR FLASHLAMPS, THE "X#" INDICATES FLASERS ON PLAYFIELD, THE REMAINDER ADDING UP TO "4 TOTAL" ON IN THE INSERT.` (`FLASERS` and `ON IN` are the print's own wording).

## Flipper Solenoids (printed page 37)

The printed headings are `Coil Description`, `Flipper GND CPU to Flip. Sw. to Flip. PCB` (spanning two columns), `Power Line FlipPC to Coil`, `Coil Type` and `Power Input To Flip. PCB`. The upper-left row's power-input cell is printed as three dots.

| Coil description | Assembly | CPU to flipper switch | Flipper switch to Flip. PCB | Power line, Flip. PCB to coil | Coil type | Power input to Flip. PCB |
| --- | --- | --- | --- | --- | --- | --- |
| Left Flipper | 090-5032-00 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-10 | GRY-YEL CN2-1,2 | 22-1080 | BLK-WHT 50VDC |
| Right Fliper Lwr. | 090-5032-00 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-7 | BLU-YEL CN2-4,5 | 22-1080 | GRY/GRY-GRN 8VAC |
| Left Flipper Upr. | 090-5032-00 | ORN-VIO CPU CN19-1 | GRY-VIO CN1-12 | BLK-YEL CN2-1,2 | 25-1800 | ... |

`Fliper` in the second row is the print's own spelling. The third row is printed `Left Flipper Upr.` yet shares the right lower flipper's `ORN-VIO CPU CN19-1` flipper-ground line and the left flipper's `CN2-1,2` power pins.

## Coil chart schematic (printed page 38)

The drawing repeats one pattern for drives 1-8: a CPU-board `SIDE L 0n` / `SIDE R 0n` pair on one `TIP 122` transistor, a `CN-11` pin and a `GRY-...` wire into the PPB board, where one diode feeds the left (coil) path out of `J2` and one diode-resistor branch feeds the right (flash lamp) path out of `J9`, and four `89` bulbs fed `+32 VR` through an `ORG` wire from `J6` pins 4,5. The coil names and bulb notes printed beside each drive are:

| Drive | Transistor | Coil as drawn | Bulb note as drawn |
| --- | --- | --- | --- |
| 1 | Q46 | 6 BALL ASSY LOCKOUT 25-1240 | (4) BOTTOM ARCH (4) 89 |
| 2 | Q45 | BALL RELEASE 23-800 | (4) PLFD (4) 89 |
| 3 | Q44 | BALL LAUNCH 22-600, through booster Q5 `TIP 36C` (J8), `YEL-VIO` to `+50 VL` on J7-8,9 | (2) LEFT SCOOP (2) INSERT (4) 89 |
| 4 | Q43 | VUK 23-800, through a booster on J8, `YEL/VIO` to `+50 VL` on J7-8,9 | (2) UPPER RIGHT (2) INSERT (4) 89 |
| 5 | Q42 | LEFT SCOOP 23-800 | (4) PLFD (4) 89 |
| 6 | Q41 | EJECT 24-940 | (4) BACK PANEL (4) 89 |
| 7 | Q40 | NO COIL AT THIS LOCATION | (2) PLFD (2) INSERT (4) 89 |
| 8 | Q39 | KNOCKER 23-800 | (4) PLFD (4) 89 |

The direct drives are drawn on CPU `CN-12`: 10 (`Q29`, pin 2, `BLK-RED`) to the `L/R COIL RELAY` with power `RED/WHT` from the PS board CN3-5 `+32V`; 11 (`Q28`, pin 4, `BRN-ORG`) to the `GENERAL ILLUM RELAY` on the PS board; 12 (`Q27`, pin 5, `BRN/YEL`) to the `DIVERTER 27-1500` (power `RED`); 15 (`Q24`, pin 8, `BRN/VIO`) to four bulbs labelled `(1) PLFD (3) INSERT`, power from the PPB board `+32 VR`; 16 (`Q23`, pin 9, `(BRN/GRY) N.C.`) to a balloon `NO COIL AT THIS LOCATION` with `(RED) N.C.`; 13 (`Q26`, pin 6, `BRN/GRN`) to the `AIRPLANE MOTOR`; 14 (`Q25`, pin 7, `BRN/BLU`) to a relay whose contacts switch an AC motor feed (the contact and voltage labels are only partly legible on this page; the Playfield Coil/Flashlamp Wiring Diagram on printed page 64 draws the same circuit legibly); and 9 (`Q30`, pin 1, `WHT/BRN`) through `Q1 TIP 36C` with `R15 220` and `D18 1N4004` to a `BRN/BLK` wire to the `SHAKER MOTOR BOARD`, a `CABINET SHAKER MOTOR 12VDC` fed through three `1N5404` diodes and `2.5A` fuses. One of those diode branches is labelled `AIRPLANE MOTOR` and runs to `J3-P1/3`.

At the right of the lower drawing, a `SERVO MOTOR INTERFACE BOARD` is drawn with a seven-pin `INPUT P2` and a three-pin `OUTPUT P1`:

| P2 pin | Signal | Wire |
| --- | --- | --- |
| 7 | GROUND | BLK/ORG |
| 6 | 5VDC | GRY/ORG |
| 5 | CLEAR | GRY/BLK |
| 4 | DATA | ORG/GRY |
| 3 | CLOCK | GRN/WHT |
| 2 | (key) | -- |
| 1 | 12VDC | GRY/RED |

| P1 pin | Signal | Wire |
| --- | --- | --- |
| 3 | SIGNAL | ORG |
| 2 | LOGIC GND | BLK |
| 1 | 5VDC | RED |

The source-connector labels to the left of P2 (for example `CPU CN3-...` and `PS CN...`) are too faint on the scan to read pin numbers with confidence and are not transcribed.
