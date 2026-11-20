# Last Action Hero (Data East 1993) - Coil drivers, the Left/Right relay and the Special Coil Wiring Diagram

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 32 and 33 (PDF 36 and 37) of the IPDB scan `Data_East_1993_Last_Action_Hero_Manual.pdf`. The scan has no text layer, so every cell was read from the render. Page 33 is a schematic (title block: `DWN PHILLIS`, `DATE 07-22-93`, game `LAST ACTION HERO`, `DATA EAST PINBALL, INC.`); its pin numbers were read from 300 dpi crops enlarged three times. The pin boxes are about fifteen pixels tall in the scan, so a few digits are blurred; each such digit is named below.

Printed page 32 states: `Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.` The page also names the Flash Lamp test (`All Flash lamps will fire randomly`), the Automatic Test (`ALL COILS`, `The test pulses each regular solenoid or flash lamp sequentially with the coil/flash lamp name indicated in the Player 1 and 2 displays and the wire colors in the Player 3 and 4 displays`) and the Select Coil test.

## Drives 1-8, switched between a left set (coil) and a right set (flash lamps) by the relay

Every drive follows one pattern on the drawing: CPU board `SIDE L nn` and `SIDE R nn` outputs share one `TIP 122` transistor, and the CN-11 pin feeds the PPB board input, where one diode and one diode-resistor branch (`D9-R1` through `D16-R8`) separate the left (coil) path from the right (flash lamp) path. The left coil wire leaves the PPB board at `J2` and the right-set return leaves at `J9`; the coil's other end returns to a `+32 VL` pin of the PPB board, and the flash lamps take `+32 VR` through an `ORG` wire from PPB `J6` pins 4,5 and return through the `J9` wire.

| Drive | Transistor | CN-11 pin | CPU to PPB wire | PPB input | Coil wire (to coil) | Return wire | Left coil | Coil type | Coil power | Right set |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Q46 | 1 | GRY-BRN | J1-1 | VIO-BRN (J2-10) | BLK-BRN (J9-5) | 6 Ball Ass'y Lockout | 25-1240 | BRN J6-3 +32 VL | (4) TOP RIGHT POLICE LIGHTS (4) 89 |
| 2 | Q45 | 3 | GRY-RED | J1-2 | VIO-RED (J2-9) | BLK-RED (J9-6) | Ball Release | 23-800 | BRN J6-3 +32 VL | (3) PLFD UPPER LEFT (1) INSERT (4) 89 |
| 3 | Q44 | 4 | GRY-ORG | J2-3 | WHT-ORG (J2-8), J8-1 Q5 TIP 36C J8-2, VIO-ORG | BLK-ORG (J9-7) | Ball Launch | 23-800 | YEL-VIO J7-8,9 +32 VL | (2) RAMP (2) INSERT (4) 89 |
| 4 | Q43 | 5 | GRY-YEL | J1-4 | VIO-YEL (J2-7) | BLK-YEL (J9-8) | Crane Lock | 32-1800 | BRN J6-3 +32 VL | (1) PLFD - UPPER RIGHT (2) INSERT (1) BACK PANEL (4) 89 |
| 5 | Q42 | 6 | GRY-GRN | J2-5 | WHT-GRN (J2-6), J8-3 Q4 TIP 36C J8-4, VIO-GRN | BLK-GRN (J9-9) | VUK | 23-800 | YEL-VIO J7-8,9 +32 VL | (3) MID RIGHT PLFD (1) INSERT (4) 89 |
| 6 | Q41 | 7 | GRY-BLU | J1-6 | WHT/BLU (J2-5), J8-6 Q3 TIP 36C J8-7, VIO-BLU | BLK-BLU (J9-10) | Right Scoop Ass'y | 23-800 | YEL-VIO J7-8,9 +32 VL | (4) PLFD-LOWER RIGHT (4) 89 |
| 7 | Q40 | 8 | GRY-VIO | J1-7 | VIO-BLK (J2-3) | BLK-VIO (J9-11) | Ball Lock | 27-1400 | BRN J6-3 +32 VL | (4) TOP LEFT POLICE LIGHTS (4) 89 |
| 8 | Q39 | 9 | GRY-BLK | J1-8 | VIO-GRY (J2-2) | BLK-GRY (J9-12) | Knocker | 23-800 | BRN J7-8,9 +32 VL | (2) LOW LEFT PLFD (2) INSERT (4) 89 |

The coil names are printed above each coil symbol in capitals (`6 BALL ASS'Y LOCKOUT 25-1240`, `BALL RELEASE 23-800`, `BALL LAUNCH 23-800`, `CRANE LOCK 32-1800`, `VUK 23-800`, `RIGHT SCOOP ASS'Y 23-800`, `BALL LOCK 27-1400`, `KNOCKER 23-800`); the table title-cases them. Drives 3 and 5 print their PPB input header as `J2` where the other six print `J1`, exactly as drawn. Drive 6's coil wire is printed `WHT/BLU` with a slash where the other booster rows print a hyphen. Drives 3, 5 and 6 pass through a `TIP 36C` booster on the PPB board (`Q5`, `Q4`, `Q3`) and return their coil through `YEL-VIO` to J7 pins 8,9; the PPB box on those three rows, and on drive 8's, is labelled `+ 32 VL` like the J6-3 rows. Blurred digits: the CN-11 pin of drive 2 (read `3`) and of drive 4 (read `5`), and the J9 pin of drive 5 (read `9`); each reading continues the sequence of its neighbours (CN-11 1, 3-9 with pin 2 absent; J9 5-12). The location words are the drawing's: PLFD (playfield), INSERT, BACK PANEL, and the two POLICE LIGHTS groups.

## Drives 9-16, direct on CN-12 (not affected by the relay)

| Drive | Transistor | CN-12 pin | Wire | Device as drawn |
| --- | --- | --- | --- | --- |
| 9 | Q30 | 1 | BRN/BLK | Through `P/O PPB BOARD` (wire BRN/BLK on both sides) to four flash lamps labelled `(2) CRANE (2) INSERT` and `(4) NO. 89`, whose common returns to PS board CN3-6 `+32V` |
| 10 | Q29 | 2 | BLK-RED | `L/R COIL RELAY` (PPB pins 9 and 2), power wire RED/WHT to PS board CN3-5 `+32V` |
| 11 | Q28 | 4 | BRN-ORG | `GENERAL ILLUM. RELAY`: a box labelled `K-1` across PS board `CN7` pins 1 and 3; the BRN-ORG line enters pin 1, and pin 3 joins the line of PS board `CN3` pins 6, 7, 8 `+32V`; PS board `CN3` pin 5 `+32V`, drive 10's RED/WHT supply, is drawn above it |
| 12 | Q27 | 5 | BRN-YEL | `DIVERTER 27-1400`, power wire RED |
| 13 | Q26 | 6 | BRN/GRN | `DROP TARGET 23-800`, power wire RED |
| 14 | Q25 | 7 | BRN-BLU | `CRANE MOTOR` (drawn as a circle enclosing `~`), then `GRY`, a `FUSE`, then `GRY/RED` to PS board CN6 pin 3 `+12VDC` |
| 15 | Q24 | 8 | BRN-VIO | `MIDDLE SCOOP 23-800`, power wire RED |
| 16 | Q23 | 9 | WHT/GRY | Cabinet shaker motor: `TIP 36C` Q4 through D18 `1N4004` and R16 `220`, output BRN/GRY to the `SHAKER MOTOR BOARD J1-P6/7`, `CABINET SHAKER MOTOR 12VDC` with a `1/2 TO 1 RESISTOR`, board fed `9VAC` from PS CN1 pins 10 and 11 through three `1N5404` diodes and `2.5A` fuses (`J1-P1/2` GRY-GRN, `J1-P4/5` GRY) |

CN-12 pin 3 is not drawn. The RED power wires of 12, 13 and 15 join one bus that ends on PS board CN3 pins 6, 7, 8 `+32V`. The `Q4` of drive 16 is a transistor drawn beside the shaker circuit, not drive 5's PPB booster of the same designator.

## CPU Controlled Auxiliary Solenoids (printed table)

The heading is printed `CPU Controlled Auxillary Solenoids`.

| Coil number | Coil description | Control line (CPU to coil) | Power line (PS to coil) | Drive transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 20 | Left Slingshot | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Ripper Kickback (See Schematic) | WHT-VIO CPU CN19-9 | VIO-YEL PPB J7-3 | Q13 | 23-800 |

## Flipper Solenoids (printed as its own unnumbered table)

The printed headings are `Coil Description`, `Flipper GND CPU to Flip Sw. to Flip.PCB`, `Power Lines FlipPc toCoil`, `Coil Type` and `Power Input To Flip PCB`. The Power Input cell spans both rows.

| Coil description | Assembly | CPU to flipper switch | Flipper switch to Flip. PCB | Power line, Flip. PCB to coil | Coil type | Power input to Flip. PCB |
| --- | --- | --- | --- | --- | --- | --- |
| Left Flipper | 090-5020-30 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-10 | GRY-YEL CN2-1,2 | 23-900 | BLK-WHT 50VDC, GRY, GRY-GRN 8VAC |
| Right Flipper | 090-5020-30 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-7 | BLU-YEL CN2-4,5 | 23-900 | BLK-WHT 50VDC, GRY, GRY-GRN 8VAC |

The machine has two flippers; there is no upper-flipper row. The Power Input cell is merged across the two rows and is repeated on both here.

## Drawing: Flash Lamp / Coil Tests location diagram (printed page 32)

The playfield drawing is annotated with left-set coil callouts `1L`, `2L`, `3L` (shooter lane, bottom right), `5L` (top right corner, circled), `6L` (right side, above the right return lane) and `7L` (left side, on the hatched lock area); no `4L` or `8L` appears. Right-set flash-lamp callouts: `2R` three times (upper left), `3R` twice (top left and left side), `4R` twice (top right), `5R` twice (upper centre-right), `6R` four times (right side and lower centre) and `8R` once (left side); no `1R` or `7R` appears on the playfield. Direct drives: `9` twice and `14` once at the crane (upper centre), `12` (centre-left, at the diverter), `13` (left side), `15` (centre, at the middle scoop), `17`, `18` and `19` at the three turbo bumpers, `20` and `21` at the two slingshots, and `22` (upper right).

A second drawing, `Backbox Flash Lamps`, shows ten backbox flash-lamp sockets labelled `2R`, `3R` (twice), `4R` (twice), `5R`, `8R` (twice) and `9R` (twice).
