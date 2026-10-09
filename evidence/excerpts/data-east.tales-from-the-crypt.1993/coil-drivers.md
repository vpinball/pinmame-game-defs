# Tales from the Crypt (Data East 1993) - Coil drivers, the Left/Right relay and the Special Coil Wiring Diagram

Transcribed by hand from native-resolution renders of printed pages 32 and 33 (PDF 36 and 37) of the GameEx-hosted scan `Data_East_1993_Tales_from_the_Crypt_Manual.pdf`. The scan has no text layer, so every cell was read from the render; OCR text was used only to locate the pages. Page 33 is a schematic: its pin numbers were read from 400-700 dpi crops of the drawing, and where a drawing label is internally inconsistent (below) the label is transcribed as printed.

Printed page 32 states: `Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.` The page also names the Flash Lamp test (all flash lamps fire randomly), the Automatic Test (ALL COILS) and the Select Coil test.

## Drives 1-8, switched between a left set (coil) and a right set (flash lamps) by the relay

Every drive follows one pattern on the drawing: CPU board `SIDE L nn` and `SIDE R nn` outputs share one `TIP 122` transistor, and the CN-11 pin feeds the PPB board input, where one diode and one diode-resistor branch separate the left (coil) path from the right (flash lamp) path. The left coil wire leaves the PPB board at `J2` and the right-set return leaves at `J9`; the coil's other end returns to a `+VL` pin of the PPB board, and the flash lamps take `+32 VR` through an `ORG` wire from PPB `J6` pins 4,5 and return through the `J9` wire. The coil and its flash lamps therefore share only the CPU-to-PPB wire and the transistor: the `J2` wire is the coil's, the `J9` wire the flash lamps'.

| Drive | Transistor | CN-11 pin | CPU to PPB wire | PPB input | Coil wire (to coil) | Return wire | Left coil | Coil type | Right set |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Q46 | 1 | GRY-BRN | J1-1 | VIO-BRN (J2-10) | BLK-BRN (J9-5) | 6 Ball Ass'y Lockout | 25-1240 | (2) PLFD (1) BACK PANEL (1) INSERT (4) 89 |
| 2 | Q45 | 3 | GRY-RED | J1-2 | VIO-RED (J2-9) | BLK-RED (J9-6) | Ball Release | 23-800 | (3) PLFD (1) INSERT (4) 89 |
| 3 | Q44 | 4 | GRY-ORN | J2-3 (header printed J2) | WHT-ORG (J2-8), then Q5 on the PPB booster board, then VIO-ORG | BLK-ORG (J9-7) | Ball Launch | 23-800 | (2) PLFD (2) INSERT (4) 89 |
| 4 | Q43 | 5 | GRY-YEL | J1-4 | VIO-YEL (J2-7) | BLK-YEL (J9-8) | Drop Target | 23-800 | (2) PLFD (1) BACK PANEL (1) INSERT (4) 89 |
| 5 | Q42 | 6 | GRY-GRN | J2-5 (header printed J2) | VIO/GRN (J2-6) | BLK-GRN (J9-9) | Scoop | 23-800 | (3) PLFD (1) INSERT (4) 89 |
| 6 | Q41 | 7 | GRY-BLU | J1-6 | WHT/BLU (J2-5), then Q3 on the PPB booster board, then VIO-BLU | BLK-BLU (J9-10) | Left VUK | 23-800 | (2) PLFD (1) BACK PANEL (1) INSERT (4) 89 |
| 7 | Q40 | 8 | GRY-VIO | J1-7 | VIO-BLK (J2-3) | BLK-VIO (J9-11) | Top VUK | 23-800 | (3) PLFD (1) BACK PANEL (4) 89 |
| 8 | Q39 | 9 | GRY-BLK | J1-8 | VIO-GRY (J2-2) | BLK-GRY (J9-12) | Knocker | 23-800 | (2) PLFD (1) BACK PANEL (1) INSERT (4) 89 |

Power pins as drawn: drives 1, 2, 4 and 7 return their coil to `+32 VL` on J6-3; drive 5 to `+32 VL` on J7-3; drives 3 and 6 pass through the Q5 / Q3 `TIP 36C` booster and return to `+50 VL` on J7-8,9 (the coil wire is `YEL-VIO`); drive 8 returns to `+32 VL` on J7-8,9. On drives 1, 2, 4, 5, 7 and 8 the wire from the coil to that `+32 VL` pin is labelled `BRN`. Every right set takes `+32 VR` through an `ORG` wire on J6 pins 4,5. The three-letter location words are the drawing's: PLFD (playfield), BACK PANEL, INSERT (the right-hand backbox drawing on printed page 32 places the eight inserts in the backbox, and the bulb table on printed page 39 lists eight `#89` bulbs `On Backbox`).

The drawing prints the coil's name above each coil symbol: `6 BALL ASS'Y LOCKOUT 25-1240`, `BALL RELEASE 23-800`, `BALL LAUNCH 23-800`, `DROP TARGET 23-800`, `SCOOP 23-800`, `LEFT VUK 23-800`, `TOP VUK 23-800` and `KNOCKER 23-800`.

## Drives 9-16, direct on CN-12 (not affected by the relay)

| Drive | Transistor | CN-12 pin | Wire | Device as drawn |
| --- | --- | --- | --- | --- |
| 9 | Q30 | 1 | BRN/BLK | DIVERTER 27-1400 (power wire RED) |
| 10 | Q29 | 2 | BLK-RED | L/R COIL RELAY (power wire RED/WHT to PS board CN3-5, +32V) |
| 11 | Q28 | 4 | BRN-ORG | GENERAL ILLUM. RELAY, contact K-1 on the PS board (CN7 pins 1 and 3) |
| 12 | Q27 | 5 | (BRN/YEL) N.C. | NO COIL AT THIS LOCATION (RED) N.C. |
| 13 | Q26 | 6 | (BRN/GRN) N.C. | NO COIL AT THIS LOCATION (RED) N.C. |
| 14 | Q25 | 7 | (BRN/BLU) N.C. | NO COIL AT THIS LOCATION (RED) N.C. |
| 15 | Q24 | 8 | BRN-VIO | A relay whose COMM / N.O. / N.C. contacts switch a 26 VAC feed to a load drawn as an AC source symbol (power wire RED); the drawing's contact labels are only partly legible and name no load |
| 16 | Q23 | 9 | WHT/GRY | Cabinet shaker motor: `TIP 36C` Q4 through D18 `1N4004` and R16 `220`, output BRN/GRY to the Shaker Motor Board J1-P6/7, motor `12VDC`, board fed 9VAC from PS CN1 through three `1N5404` diodes and `2.5A` fuses |

CN-12 pin 3 is not drawn. On drives 12-14 the drawing prints each wire colour in parentheses followed by `N.C.` and draws the wire ending unconnected beside the `NO COIL AT THIS LOCATION` balloon: the `N.C.` marks a wire with nothing on it, not a contact.

## CPU Controlled Auxiliary Solenoids (printed table)

| Coil number | Coil description | Control line (CPU to coil) | Power line (PS to coil) | Drive transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 20 | Left Slingshot | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Laser Kickback (See Schematic) | WHT-VIO CPU CN19-9 | VIO-YEL PPB J7-3 | Q13 | 23-800 |

## Flipper Solenoids (printed as its own unnumbered table)

The printed headings are `Coil Description`, `Flipper GND CPU to Flip. Sw. to Flip. PCB`, `Power Line FlipPC to Coil`, `Coil Type` and `Power Input To Flip. PCB`. The upper-right row's power-input cell is printed as three dashes.

| Coil description | Assembly | CPU to flipper switch | Flipper switch to Flip. PCB | Power line, Flip. PCB to coil | Coil type | Power input to Flip. PCB |
| --- | --- | --- | --- | --- | --- | --- |
| Left Flipper | 090-5032-00 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-10 | GRY-YEL CN2-1,2 | 22-1080 | BLK-WHT 50VDC |
| Right Fliper Lwr. | 090-5032-00 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-7 | BLU-YEL CN2-4,5 | 22-1080 | GRY/GRY-GRN 8VAC |
| Right Flipper Upr. | 090-5044-00 | ORN-VIO CPU CN19-1 | GRY-VIO CN1-12 | BLK-YEL CN2-1,2 | 25-1800 | --- |

`Fliper` in the second row is the print's own spelling. The lower and upper right flippers share the `ORN-VIO CPU CN19-1` flipper-ground line.

## Drawing: Flash Lamp / Coil Tests location diagram (printed page 32)

The playfield drawing is annotated with boxed labels: left-set coil callouts `1L` through `7L` (no `8L` appears), right-set flash-lamp callouts `1R` through `8R` (several repeat, and `7R` and `8R` share one box at the centre ring), the numbers `17`, `18` and `19` at the three turbo bumpers, `20` and `21` at the two slingshots, `22` at the lower left, and a boxed `15` right of centre. A second drawing, `Backbox Flash Lamps`, shows the backbox flash-lamp sockets labelled `1R`, `5R 8R`, `2R 4R`, `3R 3R` and `6R`.

## Bulb quantities named in this page

The right-hand drawings give four `#89` bulbs for every drive, so thirty-two `#89` flash lamps in all (19 playfield, 5 back panel, 8 insert). The Lamp Bulbs & Sockets table on printed page 39 lists thirty-one `#89` bulbs: 4 lay-down on the backpanel and 1 stand-up straight-leg on the backpanel, 7 + 11 on the playfield and 8 on the backbox. The one-bulb disagreement is in the playfield count (19 by the drive drawings, 18 by the parts table).
