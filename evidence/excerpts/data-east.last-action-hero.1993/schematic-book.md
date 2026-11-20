# Last Action Hero (Data East 1993) - Schematic book: coil, switch and lamp wiring diagrams, CPU connector CN3 and jumper J8, the power-supply board's G.I. relay, PPB board inputs, Magnet Control Board, assembly drawings

Transcribed by hand from native-resolution (300 dpi) renders of PDF pages 2, 4, 5, 8, 11, 19, 22, 23 and 25-28 of the IPDB scan `Data_East_1993_Last_Action_Hero_Schematics_BW.pdf` (printed pages 50, 52, 53, 56, 59, 67, 70, 71 and 73-76 of the same manual's schematic section). The scan has no text layer, so every cell below was read from the render.

## Coil/Flash Lamp sheet: left-set coils (printed page 50)

The page is titled `Playfield Coil/Flash Lamp Wiring Diagram`. Its top row draws the Ripper Kickback and the left-set coils of drives 1-8, each a coil with a diode across it, and three supplies: `+50V PPB J7-P3` on a `VIO/YEL` wire to the Ripper Kickback alone, `+50VDCL PPB J7-8/9` on a `YEL/VIO` bus, and `+32VL PPB J6-2/1` on a `BRN` bus. The rows run left to right as drawn. `Drawn label` joins the label's printed lines with spaces; `50V` is printed only under RIGHT SCOOP and VUK.

| Drawn label | Coil type | Position | Supply bus | Coil-side wire | Coil-side end |
| --- | --- | --- | --- | --- | --- |
| RIPPER KICKBACK | 23-800 | SOL 22 | +50V PPB J7-P3 VIO/YEL | BLU/BLK | J8-12 |
| KNOCKER | 23-800 | 8L | +50VDCL PPB J7-8/9 YEL/VIO | VIO/GRY | J8-10 |
| LEFT LOCK | 27-1400 | 7L | +32VL PPB J6-2/1 BRN | VIO/BLK | left-set connector pin 3 |
| RIGHT SCOOP 50V | 23-800 | 6L | +50VDCL PPB J7-8/9 YEL/VIO | VIO/BLU | J8-7 |
| VUK 50V | 23-800 | 5L | +50VDCL PPB J7-8/9 YEL/VIO | VIO/GRN | J8-4 |
| CRANE LOCK ASS'Y | 32-1800 | 4L | +32VL PPB J6-2/1 BRN | VIO/YEL | left-set connector pin 7 |
| BALL LAUNCH | 23-800 | 3L | +50VDCL PPB J7-8/9 YEL/VIO | VIO/ORG | J8-2 |
| BALL RELEASE | 23-800 | 2L | +32VL PPB J6-2/1 BRN | VIO/RED | left-set connector pin 9 |
| 6 BALL LOCKOUT | 25-1240 | 1L | +32VL PPB J6-2/1 BRN | VIO/BRN | left-set connector pin 10 |

## Coil/Flash Lamp sheet: J8 boosters

Connector `J8` carries five `TIP 36C` transistors, each drawn with a `1N4004` diode and a `220 Ω` resistor. One pin of each pair takes the drive line, the other leads to the coil.

| Transistor | Diode | Resistor | Drive-line pin | Drive-line wire | Drive line comes from | Coil pin | Coil wire | Coil |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | D21 | R-19 | J8-11 | WHT/VIO | TO CPU CN19-P9 Q13 (printed in a bubble) | J8-12 | BLU/BLK | RIPPER KICKBACK |
| Q2 | D20 | R-18 | J8-9 | WHT/GRY | left-set connector pin 2 | J8-10 | VIO/GRY | KNOCKER |
| Q3 | D19 | R-17 | J8-6 | WHT/BLU | left-set connector pin 5 | J8-7 | VIO/BLU | RIGHT SCOOP |
| Q4 | D18 | R-16 | J8-3 | WHT/GRN | left-set connector pin 6 | J8-4 | VIO/GRN | VUK |
| Q5 | D17 | R-15 | J8-1 | WHT/ORG | left-set connector pin 8 | J8-2 | VIO/ORG | BALL LAUNCH |

`J8` pins 5 and 8 are not drawn.

## Coil/Flash Lamp sheet: left-set connector

The sheet prints no designator on this ten-pin connector. Its pins are the ones the operator manual's coil-driver drawing (printed page 33, excerpt `coil-drivers`) prints as PPB `J2`: 10, 9, 8, 7, 6, 5, 3 and 2 for drives 1 to 8.

| Pin | Wire | Leads to |
| --- | --- | --- |
| 1 | (none) | N.C. |
| 2 | WHT/GRY | J8-9 (Q2, KNOCKER) |
| 3 | VIO/BLK | LEFT LOCK |
| 4 | (none) | KEY |
| 5 | WHT/BLU | J8-6 (Q3, RIGHT SCOOP) |
| 6 | WHT/GRN | J8-3 (Q4, VUK) |
| 7 | VIO/YEL | CRANE LOCK ASS'Y |
| 8 | WHT/ORG | J8-1 (Q5, BALL LAUNCH) |
| 9 | VIO/RED | BALL RELEASE |
| 10 | VIO/BRN | 6 BALL LOCKOUT |

Printed beside the connector: `A/B RELAY NORMALLY CLOSED SIDE = "N.C." = "L"EFT = "A" SIDE NORMALLY OPEN SIDE = "N.O." = "R"IGHT = "B" SIDE N.U. MEANS "NOT USED"`.

## Coil/Flash Lamp sheet: right-set flash lamp groups

Each group is drawn as four bulb sockets in a box, with the caption printed above the sockets, the group number at the right and the bulb count under it. The `+ 32VDCR PPB J6-4/5` supply on an `ORG` wire is drawn above group 3R and again above group 7R.

| Group | Caption | Bulbs printed under the group |
| --- | --- | --- |
| 1R | (4) TOP RIGHT BACK BOX | (4) NO.89 |
| 2R | (3) PLFD UPPER LEFT (1) INSERT | (4) NO.89 |
| 3R | (2) UPPER LEFT RAMP (2) INSERT | (4) NO.89 |
| 4R | (1) BACK PANEL (1) UPPER PLFD (2) INSERT | (3) NO. 906 (1) NO. 89 |
| 5R | (3) MID RIGHT PLFD (1) INSERT | (3) NO. 906 (1) NO. 89 |
| 6R | (2) LOWER RIGHT PLFD (2) MAGNETS | (4) NO.89 |
| 7R | (4) TOP LEFT BACKBOX | (4) NO.89 |
| 8R | (2) PLFD (2) INSERT | (4) NO.89 |

## Coil/Flash Lamp sheet: CPU drive connectors

The PPB input block draws, for drives 1-8, a resistor and diode in series (`1R`-`8R` with `D9`-`D16`) beside a second diode branch (`R-1`-`R-7` and `R8`, with `D1`-`D8`), both joined to one pin of a fifteen-pin connector; for drives 9-16 it draws a resistor alone. The right-hand nine-pin connectors carry the CPU lines.

| PPB pin | Resistor drawn | CPU connector pin | Wire | Printed at the CPU end |
| --- | --- | --- | --- | --- |
| 1 | 1R, R-1 | first connector 1 | GRY/BRN | SOL. DRIVE 1 Q46 |
| 2 | 2R, R-2 | first connector 3 | GRY/RED | SOL. DRIVE 2 Q45 |
| 3 | 3R, R-3 | first connector 4 | GRY/ORG | SOL. DRIVE 3 Q44 |
| 4 | 4R, R-4 | first connector 5 | GRY/YEL | SOL. DRIVE 4 Q43 |
| 5 | 5R, R-5 | first connector 6 | GRY/GRN | SOL. DRIVE 5 Q42 |
| 6 | 6R, R-6 | first connector 7 | GRY/BLU | SOL. DRIVE 6 Q41 |
| 7 | 7R, R-7 | first connector 8 | GRY/VIO | SOL. DRIVE 7 Q40 |
| 8 | 8R, R8 | first connector 9 | GRY/BLK | SOL. DRIVE 1 Q46 |
| 9 | 9, R9 | CN12 1 | BRN/BLK | SOL. DRIVE 9 Q30 |
| (none) | (none) | CN12 2 | BLK/RED | SOL. DRIVE 10 Q29 |
| (none) | (none) | CN12 4 | BRN/ORG | SOL. DRIVE 11 Q28 |
| (none) | (none) | CN12 5 | BRN/YEL | SOL. DRIVE 12 Q27 |
| (none) | (none) | CN12 6 | WHY/BRN | SOL. DRIVE 13 Q26 |
| (none) | (none) | CN12 7 | BRN/BLU | SOL. DRIVE 14 Q25 |
| (none) | (none) | CN12 8 | BRN/VIO | SOL. DRIVE 15 Q24 |
| (none) | (none) | CN12 9 | BRN/GRY | SOL. DRIVE 16 Q23 |

The first connector's pin 2 is not drawn, and its pin-9 row prints `SOL. DRIVE 1 Q46` again where the sequence leads to drive 8. `WHY/BRN` is the print's own spelling. PPB pins 10 and 12-15 are drawn with resistors labelled `12` to `16` (`R10`-`R14`) and lead nowhere on this sheet; CN12 pins 5-9 begin at open circles. CN12 pin 3 is not drawn. CN12 pin 4's `BRN/ORG` wire goes to pin 3 of a three-pin connector labelled `P.S.CN7`, whose pin 1 is `+ 32V` and pin 2 is `KEY`, across the coil `SOL I` of `RY1 GENERAL ILUMINATION RELAY` on the `POWER SUPPLY BOARD`. CN12 pin 2's `BLK/RED` wire leads off to the left. The block is bracketed `C.P.U. BOARD`.

## Coil/Flash Lamp sheet: direct drives

| Device as drawn | Supply | Supply wire | Device-to-CPU wire | CPU CN 12 pin | Transistor |
| --- | --- | --- | --- | --- | --- |
| (2) CRANE (2) INSERT, (4) NO.89 | +32 VDCR PPBJ6-4/5 | ORG | BRN-BLK | (leads off to the right) | (none printed) |
| DIVERTER | +32 VDC PS CN3-7/6 | RED | BRN/YEL | 5 | Q27 |
| DROP TARGET | +32 VDC PS CN3-7/6 | RED | BRN/GRN | 6 | Q26 |
| MIDDLE SCOOP | +32 VDC PS CN3-7/6 | RED | BRN/VIO | 8 | Q24 |
| CRANE (a circle enclosing `~`) | 12 VDC CN6-P3 P/O PS | GRY/RED, then FUSE, then GRY | BRN/BLU | 7 | Q25 |

The shaker circuit: CPU CN 12 pin 9 (`Q23`) on `WHT/GRY` drives a `TIP 36C` `Q4` through `D18 1N4004` and `R16 220`; its output `BRN/GRY` goes to `SHAKER MOTOR BOARD J1-P6/7`, then the `CABINET SHAKER MOTOR 12VDC` and a `1/2 Ω TO 1 Ω RESISTOR`. The board takes `9VAC` from `POWER SUPPLY CN1-P11` (`GRY`, at `SHAKER MOTOR BOARD J1-P 4/5`) and `POWER SUPPLY CN1-P10` (`GRY-GRN`, at `J1-P1/2`) through three `FUSE 2.5A` and `DIODE 1N5404` pairs, one of them ending at `N.C.`. No coil type is printed on the direct block.

## Coil/Flash Lamp sheet: general illumination lines

Under the heading `GENERAL ILLUMINATION LINES` the sheet draws two nine-pin connectors with no connector name printed on either. The left one is bracketed `POWER SUPPLY BOARD`; the right one stands on the edge of the PPB board's outline, with the four fuses `F1` to `F4` inside the outline. On the left connector pins 1-4 are grouped `6.3 VAC OUTPUT TO BULBS` and pins 6-9 `6.3 VAC OUTPUT TO FUSES`; on the right connector pins 5, 6, 7 and 9 are grouped `6.3 VAC OUTPUT TO BULBS`.

| Power-supply pin | Wire | Group label | Drawn to |
| --- | --- | --- | --- |
| 1 | BRN | 6.3 VAC OUTPUT TO BULBS | a labelled stub |
| 2 | YEL | 6.3 VAC OUTPUT TO BULBS | a labelled stub |
| 3 | GRN | 6.3 VAC OUTPUT TO BULBS | a labelled stub |
| 4 | VIO | 6.3 VAC OUTPUT TO BULBS | a labelled stub |
| 5 | KEY | (none) | a labelled stub |
| 6 | WHT/BRN | 6.3 VAC OUTPUT TO FUSES | PPB connector pin 1, fuse F4, PPB connector pin 5 (WHT/BRN) |
| 7 | WHT/YEL | 6.3 VAC OUTPUT TO FUSES | PPB connector pin 2, fuse F3, PPB connector pin 6 (WHT/YEL) |
| 8 | WHT/GRN | 6.3 VAC OUTPUT TO FUSES | PPB connector pin 3, fuse F2, PPB connector pin 7 (WHT/GRN) |
| 9 | WHT/VIO | 6.3 VAC OUTPUT TO FUSES | PPB connector pin 4, fuse F1, PPB connector pin 9 (WHT/VIO) |

PPB connector pin 8 is `KEY`. The sheet draws no bulb on these lines, so it does not pair a power-supply wire with a fused one; the Playfield Lamp Wiring Diagram's `G.I. LAMPS` block (below) draws `YEL` with `WHT-YEL` and `VIO` with `WHT-VIO`.

In its bottom right corner the sheet draws the G.I. relay. CPU `CN12` pin 4, `SOL. DRIVE 11 Q28`, runs on `BRN/ORG` to pin 3 of a three-pin connector labelled `P.S.CN7`, whose pin 1 is `+ 32V` and pin 2 `KEY`. A coil labelled `SOL I` (as the scan reads) with a diode drawn across it, the diode's bar (its cathode) towards pin 1, joins pins 1 and 3; it is captioned `RY1 GENERAL ILUMINATION RELAY`, spelt so, and bracketed `POWER SUPPLY BOARD`. This sheet's pins 1 and 3 are the reverse of the Power Supply Board Schematic (below) and of the operator manual's coil-driver drawing (printed page 33), which both put the drive on pin 1 and +32 V on pin 3.

## Playfield Switch Wiring Diagram (printed page 52)

The sheet repeats the switch table with its own part numbers, then draws the matrix. `CN8` brings out `SWITCH DRIVE 2` to `SWITCH DRIVE 8` on pins 2, 3, 4, 5, 7, 8, 9 (wires `GRN-RED`, `GRN-ORG`, `GRN-YEL`, `GRN-BLK`, `GRN-BLU`, `GRN-VIO`, `GRN-GRY`); drive 1 is not drawn on this playfield sheet. `CN10` brings out `SWITCH RETURN 1` to `SWITCH RETURN 8` on pins 9, 8, 7, 6, 5, 3, 2, 1 (wires `WHT-BRN`, `WHT-RED`, `WHT-ORN`, `WHT-YEL`, `WHT-GRN`, `WHT-BLU`, `WHT-VIO`, `WHT-GRY`). The matrix draws `SW9` to `SW64`, each a switch in series with a diode, including `SW49` to `SW53` and `SW63`, `SW64`.

| Switch Number | Description | Part No. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | - |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08* | Launch Trigger | 180-5111-00 |
| 09 | Trough #1 Left | 180-5119-00 |
| 10 | Trough #2 | 180-5119-00 |
| 11 | Trough #3 | 180-5119-00 |
| 12 | Trough #4 | 180-5119-00 |
| 13 | Trough #5 | 180-5119-00 |
| 14 | Trough #6 | 180-5119-00 |
| 15 | Trough #7 Right | 180-5118-00 |
| 16 | Shooter Lane | 180-5100-01 |
| 17 | Drop Target C | 180-5092-01 |
| 18 | Drop Target R | 180-5092-01 |
| 19 | Drop Target A | 180-5092-01 |
| 20 | Drop Target N | 180-5092-01 |
| 21 | Drop Target E | 180-5092-01 |
| 22 | Left Lock Top | 180-5128-00 |
| 23 | Left Lock Bottom | 180-5128-00 |
| 24 | Single Left Rollover | 500-5706-00 |
| 25 | Right Stand-Up Top | 180-5130-00 |
| 26 | Right Stand-Up Middle | 180-5130-01 |
| 27 | Right Stand-Up Bottom | 180-5130-02 |
| 28 | Top Rollover Left | 500-5706-00 |
| 29 | Top Rollover Middle | 500-5706-00 |
| 30 | Top Rollover Right | 500-5707-00 |
| 31 | Right Scoop Assembly | 500-5057-00 |
| 32 | Animated Cat Target | 500-5738-08 |
| 33 | Left Turbo Bumper | 180-5015-01 |
| 34 | Bottom Turbo Bumper | 180-5015-01 |
| 35 | Right Turbo Bumper | 180-5015-01 |
| 36 | Left Slingshot | 180-5054-00 |
| 37 | Right Slingshot | 180-5054-00 |
| 38 | Right Scoop Rollover | 500-5707-00 |
| 39 | Left Captive Rollover | 500-5706-00 |
| 40 | Left Captive Target | 500-5738-08 |
| 41 | Left Return | 500-5706-00 |
| 42 | Right Return | 500-5707-00 |
| 43 | Left Outlane | 500-5706-00 |
| 44 | Right Outlane | 500-5707-00 |
| 45 | Left Ramp Exit | 180-5090-00 |
| 46 | Left Ramp Entrance | 180-5090-00 |
| 47 | VUK | 180-5116-00 |
| 48 | Ripper Kickback | 180-5167-00 |
| 49 | Not Used | - |
| 50 | Not Used | - |
| 51 | Not Used | - |
| 52 | Not Used | - |
| 53 | Not Used | - |
| 54 | Drop Target Bar (2) | 180-5129-00 |
| 55 | Right Captive Rollover | 500-5707-00 |
| 56 | Right Captive Tgt. | 500-5640-00 |
| 57 | Middle Scoop Left | 500-5116-00 |
| 58 | Middle Scoop Right | 500-5700-00 |
| 59 | Scoop Spinner | 180-5010-04 |
| 60 | Crane Left Limit | 500-5727-00 |
| 61 | Crane Right Limit | 500-5727-00 |
| 62 | Smart Missle | 515-5904-00 |
| 63 | Left Flip. Cab | 180-5048-01 |
| 64 | Right Flip. Cab | 180-5048-01 |

The names agree with the operator manual's part table (printed page 29, excerpt `switch-matrix`) except that this sheet spells 39 `Rollover` where the manual prints `Roilover`. Eight part numbers differ from the manual's: 32 (`500-5738-08` here, `180-5125-02` there), 40 (`500-5738-08`, `180-5114-08`), 48 (`180-5167-00`, `500-5707-00`), 56 (`500-5640-00`, `180-5114-08`), 57 (`500-5116-00`, `180-5116-00`), 60 and 61 (`500-5727-00`, `180-5093-00`) and 62 (`515-5904-00`, `180-0028-00`). The sheet prints no legend for the asterisk.

## Playfield Lamp Wiring Diagram (printed page 53)

| Lamp Number | Description |
| --- | --- |
| 01 | Find the Ripper |
| 02 | Grid:Last |
| 03 | Grid:Action |
| 04 | Grid:Hero |
| 05 | Grid:Super Crane |
| 06 | Left Turbo Bumper |
| 07 | Top Turbo Bumper |
| 08 | Right Turbo Bumper |
| 09 | Grid:Fast Scoring |
| 10 | Grid:Go to The Movies |
| 11 | Grid:Save Danny |
| 12 | Grid:Light Extra Ball |
| 13 | Grid:Cat Millions |
| 14 | Grid:To The Roof |
| 15 | Grid:Redeye |
| 16 | Grid:Big Mistake |
| 17 | C |
| 18 | R |
| 19 | A |
| 20 | N |
| 21 | E |
| 22 | Animated Cat Target |
| 23 | Left Ramp |
| 24 | Wild Card |
| 25 | Benedict's EyeTop |
| 26 | Benedict's Eye Middle |
| 27 | Benedict's Eye Bottom |
| 28 | Top Rollover Left |
| 29 | Top Rollover Middle |
| 30 | Top Rollover Right |
| 31 | Left Captive Ball |
| 32 | Right Captive Ball |
| 33 | Shield Left |
| 34 | Shield Left Center |
| 35 | Shield Right Center |
| 36 | Shield Right |
| 37 | More Time |
| 38 | Extra Ball |
| 39 | M-Ball |
| 40 | Return Lanes (2 Bulbs) |
| 41 | Spinner |
| 42 | Chicken |
| 43 | Outlanes (2 Bulbs) |
| 44 | The Roof |
| 45 | Jackpot |
| 46 | Ripper |
| 47 | Save Danny |
| 48 | Right Scoop |
| 49 | Shoot Again |
| 50 | Lock Bottom (Right) |
| 51 | Lock Top (Left) |
| 52 | Middle Scoop |
| 53 | Middle Scoop |
| 54 | Middle Scoop |
| 55 | Shoot the Crane |
| 56 | Middle Scoop |
| 57 | Smart Missle |
| 58 | R |
| 59 | I |
| 60 | P |
| 61 | P |
| 62 | E |
| 63 | R |
| 64 | Credit Button |

Under the table: `*Indicates Speaker or Backbox Lamp`; no row carries an asterisk. This list agrees word for word with the operator manual's lamp description list (printed page 31, excerpt `lamp-matrix`) except on 31 and 32, which the manual's list and its Lamp Matrix Chart print as `Captive Ball X2` and `Ticket`.

The drawing shows `CN7` pins 1, 2, 3, 4, 6, 7, 8, 9 as `LAMP DRIVE 1` to `LAMP DRIVE 8` (wires `YEL-BRN`, `YEL-RED`, `YEL-ORN`, `YEL-BLK`, `YEL-GRN`, `YEL-BLU`, `YEL-VIO`, `YEL-GRY`) and `CN6` pins 1, 2, 3, 5, 6, 7, 8, 9 as `LAMP RETURN 1` to `LAMP RETURN 8` (wires `RED-BRN`, `RED-BLK`, `RED-ORN`, `RED-YEL`, `RED-GRN`, `RED-BLU`, `RED-VIO`, `RED-GRY`), with the transistor list `LAMP DRIVE 1 Q71` ... `LAMP DRIVE 8 Q64` and `LAMP RETURN 1 Q72` ... `LAMP RETURN 8 Q79`. The matrix draws one socket per position, `LB1` to `LB64`. A separate block `G.I. LAMPS` draws two pairs of bulbs on connector `4M/F6` pins 1-4, wires `YEL`, `WHT-YEL`, `VIO`, `WHT-VIO`, `TO G.I. FUSES`.

## CPU Board Logic Diagram CN3 (printed page 56)

The page is `CPU Board Logic Diagram (Sheet 2 of 4)`, title block `CPU BOARD SHT 2 OF 4`. The connector is headed `CN3 TO CON. CN1 (MAS DIS. BD)`. Port B of the `6821` at `11B` (pins 10-17) and its `CA2` (pin 39) and `CB2` (pin 19) reach it through the `RA3 4.7K x 8` network and the `C147`-`C154`, `C155` and `C156` capacitors (printed `47OP`); `CA2` and `CB2` also have `4.7K` pull-ups `RA24-3` and `RA24-2` to `+5`. The table follows the drawing left to right.

| CN3 pin | Printed label | Port line |
| --- | --- | --- |
| 12 | N.C. | (none; the pin's line leads off to the left) |
| 9 | SEG.A | PB0 |
| 8 | SEG.B | PB1 |
| 7 | SEG.C | PB2 |
| 5 | SEG.D | PB3 |
| 4 | SEG.E | PB4 |
| 3 | SEG.F | PB5 |
| 2 | SEG.G | PB6 |
| 1 | (blank) | PB7 |
| 11 | N.C. | CA2 |
| 10 | N.C. | CB2 |
| 6 | KEY | (none) |

`BLANKING U-12G` is drawn joining the pin-12 line. The `SEG.` and `N.C.` labels name the display-board connector the heading names, not this game's loads; the Magnet Control Board connections (printed page 70, below) take pins 9, 8 and 7.

The same page draws `PA7` (pin 9) of the `6821` at `11B` running up to a link labelled `J8`: two open terminals joined by a dashed line, the upper terminal taken to ground. The pin-9 line is also pulled up to `+5` through `RA19-9` (`4.7K`). The page prints nothing else about `J8`.

## Power Supply Board Schematic (printed page 59)

The page's title block reads `DATA EAST PINBALL`, `POWER SUPPLY BOARD SCHEMATIC`, part no. `520-5047-02`, rev `A`, `PREPARED BY: CES INC.`. Its lower left corner draws the relay `RY1`, rated `24VDC/10A`: two changeover contacts and a coil, with each moving contact drawn resting on its upper fixed contact.

| RY1 terminal | Drawn as | Connected to |
| --- | --- | --- |
| 2 | upper fixed contact of the first changeover; the moving contact rests on it | terminal 1; `CN9X4` pins 1 and 3, which are joined |
| 4 | lower fixed contact of the first changeover | nothing (a short line) |
| 6 | moving contact of the first changeover | terminal 5; `CN8X9` pins 1-4, which are joined |
| 1 | upper fixed contact of the second changeover; the moving contact rests on it | terminal 2 |
| 3 | lower fixed contact of the second changeover | nothing (a short line) |
| 5 | moving contact of the second changeover | terminal 6 |
| 8 | coil | `CN7X5` pin 3, and the bar (cathode) end of diode `D1` `1N4001` |
| 7 | coil | `CN7X5` pin 1, and the triangle (anode) end of diode `D1` |

`CN9X4` pins 2 and 4 are joined and run straight to `CN8X9` pins 6-9, which are joined. `CN8X9` pin 5 is a short unconnected line, and the connector is captioned `GENERAL ILLUMINATION`. `CN7X5` pin 2 is a short unconnected line, and its pins 4 and 5 lead to other parts of the board. The sheet does not say where `CN9` is fed from. `CN8X9` matches the power-supply connector of the Coil/Flash Lamp sheet's General Illumination Lines (above) in its pin count and its unconnected pin 5 (`KEY` there). `CN7X5` pins 1 and 3 are the coil pins of that sheet's `P.S.CN7`, but with `D1`'s cathode on pin 3 this page puts the positive supply on pin 3 and the drive on pin 1: the reverse of that sheet, which prints `+ 32V` on pin 1 and drive 11 on pin 3 with its diode's cathode towards pin 1, and the same as the operator manual's coil-driver drawing (printed page 33), which runs drive 11's `BRN-ORG` to `CN7` pin 1 and joins pin 3 to the `CN3` pins 6-8 `+32V` line.

## PPB-1 board schematic: drive inputs (printed page 67)

The page, footed `PPD Board Servicing Diagrams`, prints the `PPB-1` board layout (`DATA EAST`, `REV A`, `520-5021-00`) beside its schematic, which is printed a quarter-turn on the sheet. The schematic draws the input header `J1` with fifteen pin numbers and no `J1-11`. For J1-1 to J1-8 it draws a diode and resistor in series to the right-set header `J9` and a second diode to the left-set header `J2`; for the other pins a resistor alone to `J9`. Every resistor carries a printed `3`; R9, R12 and R13 also carry `6.8`. `J2-10` is drawn on a short line that ends unconnected, and no `J2-3` is drawn.

| J1 pin | Right-set branch | J9 pin | Left-set diode | J2 pin |
| --- | --- | --- | --- | --- |
| J1-1 | D9, R1 | J9-5 | D1 | J2-9 |
| J1-2 | D10, R2 | J9-6 | D2 | J2-8 |
| J1-3 | D11, R3 | J9-7 | D3 | J2-7 |
| J1-4 | D12, R4 | J9-8 | D4 | J2-6 |
| J1-5 | D13, R5 | J9-9 | D5 | J2-5 |
| J1-6 | D14, R6 | J9-10 | D6 | J2-4 |
| J1-7 | D15, R7 | J9-11 | D7 | J2-2 |
| J1-8 | D16, R8 | J9-12 | D8 | J2-1 |
| J1-9 | R9 | J9-13 | (none) | (none) |
| J1-10 | R10 | J9-14 | (none) | (none) |
| J1-12 | R11 | J9-15 | (none) | (none) |
| J1-13 | R12 | J9-1 | (none) | (none) |
| J1-14 | R13 | J9-2 | (none) | (none) |
| J1-15 | R14 | J9-3 | (none) | (none) |

The J9 pins agree with the right-set returns the operator manual's coil-driver drawing prints for drives 1-8 (J9-5 to J9-12). Every left-set J2 pin is one lower than the pin the game's own drawings print for the same drive: the coil-driver drawing and the Coil/Flash Lamp sheet's left-set connector above both put drives 1-8 on pins 10, 9, 8, 7, 6, 5, 3 and 2.

## Magnet Control Board connections (printed page 70)

`Magnet Control Board 520-5068-00`.

| Connector pin | Signal | Wire | Other end |
| --- | --- | --- | --- |
| J1-9 | CLOCK | BRN-WHT | CPU CN1-7 |
| J1-8 | INPUT 3 | ORG-BLK | CPU CN3-7 |
| J1-7 | INPUT 1 | ORG-RED | CPU CN3-8 |
| J1-6 | INPUT 2 | ORG-BRN | CPU CN3-9 |
| J1-5 | CLR | GRY-BLK | CPU CN2-1 |
| J1-4 | + 5VDC | GRY | P.S.CN 6-7 |
| J1-3 | KEY | (none) | (none) |
| J1-2 | GROUND | BLK | P.S.CN4 |
| J1-1 | GROUND | BLK | P.S.CN4 |
| J2-1 | + 50VDC | VIO-YEL | PPB J7-3 |
| J2-2 | KEY | (none) | (none) |
| J2-3 | OUTPUT 1 | BLU-VIO | MAGNET 1 |
| J2-4 | OUTPUT 2 | BLU-GRY | MAGNET 2 |
| J2-5 | GND | BLK | P.S. CN4 |
| J2-6 | GND | BLK | P.S. CN4 |
| J2-7 | OUTPUT 3 | BLU-WHT | MAGNET 3 |

The sheet does not say where on the playfield `MAGNET 1`, `MAGNET 2` and `MAGNET 3` are.

## Magnet Controller Board schematic (printed page 71)

Title block: `MAGNET CONTROLLER BOARD`, part no. `520-5068-00`, prepared by `C.E.S. INC.`, rev. `C`, sheet 1 of 1. U1 is a `74HCT273`. Each J1 input passes a 100-ohm series resistor (`R1-R5 = 100`) and has a pull-up (`R6-R10 = 100K`) to +5V:

| J1 pin | Signal | Series resistor | Pull-up | U1 pin |
| --- | --- | --- | --- | --- |
| J1-5 | CLR (overbarred) | R1 | R10 | 1 CLR |
| J1-6 | IN 2 | R4 | R7 | 4 2D |
| J1-7 | IN 1 | R3 | R8 | 3 1D |
| J1-8 | IN 3 | R2 | R9 | 18 8D |
| J1-9 | CLK | R5 | R6 | 11 CP |

U1 inputs 3D-7D (pins 7, 8, 13, 14, 17) are tied to ground and outputs 3Q-7Q (pins 6, 9, 12, 15, 16) are marked `N.C.`. Outputs: 1Q (pin 2) through `R11 39K` to the gate of `Q1 P20N10`, whose drain is `J2-3 OUT 1`; 2Q (pin 5) through `R12 39K` to `Q2 P20N10`, drain `J2-4 OUT 2`; 8Q (pin 19) through `R13 39K` to `Q3 P20N10`, drain `J2-7 OUT 3`. Each MOSFET's source is grounded and each drain has a diode (`D1-D3 = 1N4934`) to `J2-1 +V`. `J2-5` and `J2-6` are `GROUND`. The board therefore latches the three CPU lines on the CLK edge and holds each magnet output at the latched level of its own input: IN 1 drives OUT 1, IN 2 drives OUT 2, IN 3 drives OUT 3.

## Ball Lock Assembly 500-5730-00 (printed page 73)

Title block: `BALL LOCK ASSEMBLY`, part no. `500-5730-00`, `DATA EAST PINBALL, INC.`, DWN `N.R.WURZ`, date `6-8-93`, scale `1:1`. Circled letters stand beside some rows: `(C)` at 7 and 14, `(B)` at 8, `(A)` at 15, and `(A) (D)` to the right of 11; the page does not say what the letters mean.

| Item | Part No. | Description | Qty |
| --- | --- | --- | --- |
| 1 | 515-5867-00 | BALL LOCK MTG BRKT ASSY | 1 |
| 2 | 530-5262-00 | PLUNGER, LOCK BALL | 1 |
| 3 | 535-5203-01 | COIL BRACKET | 2 |
| 4 | 545-5411-00 | COIL SLEEVE | 1 |
| 5 | 270-5005-0 | E-RING, 7/16 SHAFT | 1 |
| 6 | 545-5418-00 | NYLINER, 7/16 SHAFT | 1 |
| 7 | 232-5300-00 | #8-32 X 1/4 PPHW/SEMS | 4 |
| 8 | 180-5128-00 | ACTUATOR SWITCH | 2 |
| 9 | 237-5806-00 | #2-56 X 1/2 PPH | 4 |
| 10 | 244-5001-00 | #2 SPLIT LOCKWASHER | 4 |
| 11 | 090-5004-00 | COIL, 27-1500 | 1 |
| 12 | 036-5318-00 | BALL LOCK HARNESS | 1 |
| 13 | 112-5001-00 | DIODE | 2 |
| 14 | 266-5020-00 | SPRING | 1 |
| 15 | 535-6539-00 | SWITCH PROTECTOR | 2 |

Item 5's part number is printed `270-5005-0`, one digit short. The drawing shows two views of a vertical coil (11) whose plunger (2) stands up out of the top bracket, with the spring (14) around the plunger between the E-ring (5) and nyliner (6) and the coil top; the second view mounts the two actuator switches (8), each with a diode (13), beside the plunger on the mounting bracket, their actuator arms reaching over the top. The ball lock harness (12) is drawn as a connector. No ball is drawn, and the page does not say which way the plunger moves when the coil is energised.

## 5-Bank Drop Target Assembly 500-5621-05 (printed page 74)

Title block: `5-BANK DROP TRGT. ASSY. (ADJUSTABLE)`, part no. `500-5621-05`, `PARTEC # PB-1126`, DWN `BALCER`, date `12-02-92`.

| # | Description | Part # |
| --- | --- | --- |
| 1 | TRGT. END PLATE (2) | 535-6162-00 |
| 2 | TRGT. FRAME | 535-6159-03 |
| 3 | 8-32 X 3/8 (6) | 237-5879-00 |
| 4 | SPRING MTG. PLATE | 535-6510-05 |
| 5 | TARGET | 545-5048-01 |
| 6 | TRGT. RETAIN BRKT. | 535-5042-03 |
| 7 | 6-32 X 3/8 SHWHTCS TYPE 23 (6) | 237-5891-00 |
| 8 | TRGT. RESET SPRING | 265-5003-00 |
| 9 | COIL SUPPORT BRKT. | 535-6154-00 |
| 10 | (blank, printed as dashes) | (blank, printed as dashes) |
| 11 | 23-700 COIL | 090-5022-00 |
| 12 | COIL SLEEVE | 545-5031-00 |
| 13 | PLUNGER STOP BRKT. | 515-5088-00 |
| 14 | PLUNGER/LINK ASSY. | 515-5338-00 |
| 15 | TRGT. LIFT BRKT. | 535-6509-05 |
| 16 | TRGT. SHAFT | 530-5179-03 |
| 17 | E-RING (1/4) | 270-5002-00 |
| 18 | PIVOT SHAFT | 530-5180-03 |
| 19 | E-RING (1/8) | 270-5000-00 |
| 20 | SWITCH ASSY. | 180-5092-01 |
| 21 | SWITCH PLATE | 535-5045-00 |
| 22 | 6-32 X 1/2 | 237-5878-00 |
| 23 | IN 4004 DIODE | 112-5003-00 |
| 24 | PLUNGER LINK | 545-5062-00 |
| 25 | ADJ. BRKT. | 535-6508-00 |
| 26 | 8-32 X 7/8 (1) | 237-5890-00 |
| 27 | 8-32 NYLOC | 240-5102-00 |

Under the table: `*QUANTITY IS DESIGNATED BY BANK SIZE`. Row 7's description is printed much smaller than the others. In row 24 the digits `5062` are written over by hand. `IN 4004` is the print's spelling.

## Lock Ball Assembly 500-5684-01 (printed page 75)

The page, footed `Trough Assembly 75`, draws three parts: this assembly at the top, a `535-6606-01 DEFLECTOR` in the middle, and the six-ball switch assembly at the bottom. The top drawing is labelled `LOCK BALL ASSEMBLY 500-5684-01`.

| Item | Part No. | Description | Qty |
| --- | --- | --- | --- |
| 1 | 515-5817-01 | LOCK BALL BRKT ASSY | 1 |
| 2 | 515-5815-01 | LOCK BALL CAM ASSY | 1 |
| 3 | 530-5250-01 | PLUNGER,Ø7/16 X 2 1/4 LG | 1 |
| 4 | 545-5058-00 | LINK, LOCK BALL | 1 |
| 5 | 266-5036-01 | SPRING | 1 |
| 6 | 545-5400-00 | SPACER | 1 |
| 7 | 090-5034-00 | COIL, 25-1240 | 1 |
| 8 | 515-5088-00 | CORE STOP ASSY | 1 |
| 9 | 535-6658-00 | COIL RETAINING BRKT | 1 |
| 10 | 545-5411-00 | COIL SLEEVE | 1 |
| 11 | 545-5105-00 | RUBBER BUMPER | 1 |
| 12 | 270-5002-00 | E-RING, .25 SHAFT | 2 |
| 13 | 237-5898-00 | #6-32 HWH TC X .38 LG | 4 |
| 14 | 237-5606-00 | #8-32 PPH X 1" LG | 1 |
| 15 | 036-5301-01 | WIRING HARNESS | 1 |
| 16 | 270-5005-00 | E-RING, Ø.44 SHAFT | 1 |

The drawing lays the coil (7) horizontally, with the plunger (3), spring (5) and link (4) at its right end and the cam assembly (2) below the link.

## 6 Ball Switch Assembly 500-5683-01 (printed page 75)

The bottom drawing is labelled `6 BALL SWITCH ASSEMBLY 500-5683-01`; the page's title block reads `6 BALL OUT HOLE TROUGH ASSEMBLY`, DWN `T.V.S.`, date `8.6.93`, scale `1:1`, and its part-number box is cut off at the edge of the scan. The table is printed bottom-up, with its header row under item 1; it is transcribed here top-down.

| Item | Part No. | Description | Qty |
| --- | --- | --- | --- |
| 1 | 535-6621-01 | OUTHOLE MTG BRKT | 1 |
| 2 | 535-6622-01 | COIL MTG BRKT | 1 |
| 3 | 535-6623-00 | SWITCH MTG BRKT | 1 |
| 4 | 180-5118-00 | SWITCH, MINIATURE | 1 |
| 5 | 180-5119-00 | SWITCH, SUBMINIATURE | 12 |
| 6 | 515-5000-02 | PLUNGER ASSY | 1 |
| 7 | 545-5076-00 | COIL SLEEVE | 1 |
| 8 | 545-5105-00 | RUBBER BUMPER | 1 |
| 9 | 090-5001-00 | COIL, 23-800 | 1 |
| 10 | 237-5806-00 | #2-56 PPH X .5 LG | 12 |
| 11 | 244-5001-00 | #2 SPLIT LW | 12 |
| 12 | 237-5832-00 | #4-40 PPH X .62 LG | 2 |
| 13 | 232-5300-00 | #8-32 PPHW/SEM X .25 LG | 8 |
| 14 | 036-5301-00 | WIRE HARNESS | 1 |
| 15 | 535-5203-01 | COIL RETAINING BRKT | 1 |
| 16 | 266-5020-00 | SPRING | 1 |

The drawing shows six item-5 switches in a row under the sloped outhole bracket (1), where the table prints a quantity of 12, and one item-4 switch on the switch bracket (3) beside the top of the coil (9), which stands vertically under the low end of the row with its plunger (6) and spring (16).

## Crane Assembly (printed page 76)

Title block `CRANE ASSEMBLY`, `DATA EAST PINBALL, INC.`, `LAH MANUAL`. Callouts: `515-5856-00 TOP ASSY. (COMPLETE)`, `545-5419-00 CAB WINDOW`, `077-5100-00 LAMP SOCKET (2)`, `165-5000-89 LAMP (2)`, `237-5897-00 8-32 X 3/8 SHCS`, `515-5885-00 CAB & BOOM ASSY.`, `515-5889-00 COIL ASSY.` (drawn under the boom at the cab end), `232-5301-00 8/32 PPH SEMS`, `515-5857-00 BOTTOM ASSY. (COMPLETE)`, `270-5002-00 E-RING`, `545-5423-00 NYLINER #4L1-FF`, `530-5260-00 SHAFT`, `535-6687-00 SUPPORT BRKT.`, `PLAYFIELD`, `535-6686-00 MOTOR BRKT.`, `1/8 X 1/2 ROLL PIN`, `240-5104-00 8-32 KEPS NUT (2)`, `237-5858-00 8-32 X 5/8 HWH (2)`, `041-5027-00 MOTOR (CRANE)` and `130-5000-00 CAPACITOR (.1Z 500V)`. The motor hangs under the playfield on the motor bracket and turns the vertical shaft that carries the cab and boom above it; the two #89 lamps sit in the cab.
