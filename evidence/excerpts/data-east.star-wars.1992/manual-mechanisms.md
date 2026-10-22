# Star Wars mechanism and contact evidence

Source: Data East operator's manual `Star_Wars_DE_OPS.pdf`, SHA-256
`dda489f3270e465dc285102a1d311d7538f58de9772542c78ba0fedc3c546ab0`,
and `starwars_schematics.pdf`, SHA-256
`e2a5dedc7e9529a449151f8b9a7ec8d94eda3054dc1022d1e987e1124f9714d1`.
Original URLs and attribution are in `manual-spatial.md`. Transcribed by the
primary curator, visually checked against native-resolution renders on
2026-10-22; OCR was a navigation aid. Copyright Data East, NOASSERTION.

## CPU jumper table — complete table

Schematics PDF 2, unnumbered CPU setup page, complete CPU JUMPER TABLE.
Repeated cells below are separately printed, not filled down by inference.

| Game | CPU version | ROM location | Installed | Removed |
| --- | --- | --- | --- | --- |
| Torpedo Alley | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Time Machine | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Playboy | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| ABC M.N. Football | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Robocop | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Phantom of the Opera | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Back to the Future | Ver 3 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| The Simpsons | Ver 3 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Checkpoint | Ver 3 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Teen. Mut. Ninja Turtles | Ver 3 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Batman | Ver 3 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Star Trek | Ver 3 | 5C | J1b,J3,J5,J5b,J6b,J7b,&J8 | J1a,J2,J4,J5a,J6a,&J7a |
| Hook | Ver 3 | 5C | J1b,J3,J5,J5b,J6b,J7b,&J8 | J1a,J2,J4,J5a,J6a,&J7a |
| Lethal Weapon 3 | Ver 3 | 5C | J1b,J3,J5,J5b,J6b,J7b,&J8 | J1a,J2,J4,J5a,J6a,&J7a |
| Star Wars | Ver 3 | 5C | J1b,J3,J5,J5b,J6b,J7b,&J8 | J1a,J2,J4,J5a,J6a,&J7a |

Footnotes: Version 1 has a 2K RAM, a 24-pin IC at 5D. Version 2 has an
8K RAM, a 28-pin IC at 5D.

Schematics PDF 10, printed p.54, complete PIA 11B PA7 jumper branch in
`cpu-j8-wiring.webp`: PA7 pin 9 goes to J8 to ground, with RA19-9 4.7K
pullup. Installed J8 therefore grounds PA7 (0). PinMAME's shared `pia2a_r`
supplies DIP 0 shifted to this bit. The W7 comment belongs to shared Williams
code; Germany/USA exists in S11_COMPORTS but not this game's DE_COMPORTS.
No country semantics are established for J8 here.

## Main coil wiring — complete drivers 9–16 drawing region

Operator PDF 31, printed p.29, lower drawing region, retained in
`motor-relay-wiring.webp`. This is a circuit drawing, not a separate printed
solenoid table. Every branch in that region is transcribed below, including
both explicit no-coil locations. The upper 1L–8L and 1R–8R branches are
transcribed in `manual-spatial.md`.

| CPU driver | Transistor | CPU connector pin (connector name not printed in this region) | Control wire | Complete load annotation / route |
| --- | --- | --- | --- | --- |
| 09 | Q30 | 1 | BRN-BLK | R2D2 DANCE, 23-800; RED supply |
| 10 | Q29 | 2 | BLK-RED | L/R COIL RELAY, P/O PPD BOARD (literal); J6 pins [9/3 unclear] and [7/4 unclear]; RED-WHT supply |
| 11 | Q28 | 4 | BRN-RED | GENERAL ILLUM. RELAY K-1, P.S. BOARD CN7-3 to CN7-1 |
| 12 | Q27 | 5 | BRN-YEL | RELAY BOARD #520-5010-00, J8 input; BAR TARGET MOTOR 515-5256-00 |
| 13 | Q26 | 6 | BRN-GRN | NO COIL AT THIS LOCATION |
| 14 | Q25 | 7 | [blank] | NO COIL AT THIS LOCATION |
| 15 | Q24 | 8 | BRN-VIO | RELAY BOARD #520-5010-00, J8 input; DEATH STAR 515-5570-00 / R2D2 MOTORS 515-5571-00 |
| 16 | Q23 | 9 | WHT-GRY | PPB BOARD J8-11, Q1 TIP 36C, J8-12 BRN-GRY; LASER KICK 23-800; YEL-VIO to PPB J7-3 +50 VDC |

Both motor relay drawings separately print the same topology: RED relay-coil
supply from the 32V supply branch; NO COIL terminal WHT-RED from BR2, 28 VAC;
NC marked NC; COMM marked GND. The motor is between WHT-RED 28 VAC and
WHT-RED from GND/COMM. Output 15 switches both named motors together. CPU
connector pin 3 is omitted by the printed connector; it is not an inferred load.
Supply board CN3-5 is ORG, +32V; the CN7 box prints 6/7/8 and +32V,
with no wire colour printed at pin 7. The L/R coil relay is
the PPB multiplexer, distinct from the power-supply GI relay printed K-1.

## CPU Controlled Auxiliary Solenoids — complete table

Operator PDF 30, printed p.28. Repeated RED / PS CN3-8 cells are separately
printed. These printed coil numbers agree with the retained stwr_103 ROM coil
test and the Data East PIA permutation; they are not inferred from row order.

| Coil | Description | Control line CPU to coil | Power line PS to coil | Transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Top Turbo Bumper | BLU-BRN / CPU CN19-7 | RED / PS CN3-8 | Q11 | 23-800 |
| 18 | Left Turbo Bumper | BLU-RED / CPU CN19-4 | RED / PS CN3-8 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN / CPU CN19-3 | RED / PS CN3-8 | Q8 | 23-800 |
| 20 | Bottom Turbo Bumper | BLU-YEL / CPU CN19-6 | RED / PS CN3-8 | Q10 | 23-800 |
| 21 | Left Slingshot | BLU-GRN / CPU CN19-8 | RED / PS CN3-8 | Q12 | 23-800 |
| 22 | Right Slingshot | BLU-BLK / CPU CN19-9 | RED / PS CN3-8 | Q13 | 23-800 |

## Flipper Solenoids — complete table

Same page. Power-input cell is merged across both rows and is repeated here
explicitly. The left switch connector's last glyph is indistinct (0/6 in the
scan); it is not completed from a sibling game's wiring.

| Description / part | CPU to coil ground | Switch to flipper PCB ground | Power lines PCB to coil | Type | Power input to flipper PCB |
| --- | --- | --- | --- | --- | --- |
| Left Flipper / 090-5032-00 | ORN-GRY / CPU CN19-2 | BLU-GRY / CN1-[0/6 unclear] | GRY-YEL / CN2-1,2 | 22-1080 | BLK-WHT 50VDC; GRY, GRY-GRN 6VAC (merged cell) |
| Right Flipper / 090-5032-00 | ORN-VIO / CPU CN19-1 | BLU-VIO / CN1-1 | BLK-WHT / CN1-1 | 22-1080 | BLK-WHT 50VDC; GRY, GRY-GRN 6VAC (merged cell) |

The physical winding table does not identify PinMAME's fabricated power/hold
outputs 45-48 as separate physical windings. Those outputs are duplicate logical
states on this initializer, not winding telemetry.

## Playfield — Major Assemblies: complete table

Operator PDF 33, printed p.31. The drawing's numbered arrows identify instances;
table captions are transcribed here in full. Two scoop assembly captions name
the same generic assembly; the drawing and script distinguish left from right.

| Item | Description | Part |
| --- | --- | --- |
| 1 | Ball Feed Assy.(Trough) | 500-5012-01 |
| 2 | Outhole Assy. | 500-5082-00 |
| 3 | Super VUK | 500-5116-04 |
| 4 | Sling Shot Assy | 500-5226-00 |
| 5 | Turbo Bumper Assy. | 500-5227-01 |
| 6 | 3 Bank Drop Target Assy. | 500-5621-03 |
| 7 | Ball Launch Assy. | 500-5477-01 |
| 8 | R2D2 Unit | 500-5484-00 |
| 9 | Flipper Assy. Right | 500-5606-73 |
| 10 | Flipper Assy Left | 500-5606-74 |
| 11 | Underchute Ramp | 500-5612-00 |
| 12 | Ball Kicker Assy.(Scoop) | 500-5468-02 |
| 13 | Ball Kicker Assy.(Scoop) | 500-5468-00 |
| 14 | Bottom Arch Assy. | 545-5302-04 |
| 15 | Loop Ramp | 515-5682-00 |
| 16 | VUK Wire Ramp | 535-6339-00 |
| 17 | Metal Ramp | 500-5609-00 |
| 18 | Level (Horizontal) | 670-5000-00 |
| 19 | Level (Vertical) | 670-5001-00 |
| 20 | 2 Bank S.U. Switch Assy. | 500-5615-06 |
| 21 | Single S.U. Switch Assy. | 500-5625-06 |
| 22 | Up-Down Target Assy. | 500-5618-00 |
| 23 | Kick Back Assembly | 500-5080-00 |

## Contact construction and matrix connectors

Schematics PDF 6, printed p.50, complete playfield switch drawing region:
columns 2-8 contain SW9-SW64 in eight rows. Every drawn contact is normally
open, in series with its diode; no opto construction is shown. SW41/SW42 are
also drawn open. Their closure at a cam endpoint is an actuated state, not a
normally-closed construction. The unused positions are drawn as generic
contacts but the parts chart explicitly marks them Not Used: this does not
establish fitted hardware there.

| Drive column | CN8 pin | Wire | Switch range |
| --- | --- | --- | --- |
| 2 | 2 | GRN-RED | 9-16 |
| 3 | 3 | GRN-ORG | 17-24 |
| 4 | 4 | GRN-YEL | 25-32 |
| 5 | 5 | GRN-BLK | 33-40 |
| 6 | 7 | GRN-BLU | 41-48 |
| 7 | 8 | GRN-VIO | 49-56 |
| 8 | 9 | GRN-GRY | 57-64 |

| Return row | CN10 pin | Wire |
| --- | --- | --- |
| 1 | 9 | WHT-BRN |
| 2 | 8 | WHT-RED |
| 3 | 7 | WHT-ORN |
| 4 | 6 | WHT-YEL |
| 5 | 5 | WHT-GRN |
| 6 | 3 | WHT-BLU |
| 7 | 2 | WHT-VIO |
| 8 | 1 | WHT-GRY |

Schematics PDF 9-10, printed pp.53-54, CPU logic drawing service-input
subcircuit: CN14-4 UP/DOWN, CN14-3 ADVANCE, CN14-1 MEM PROT, CN14-2 GND.
UP/DOWN and ADVANCE have 4.7K pullups R8/R5 and 470-ohm R7/R6 input filters,
C83/C82 .01 to ground, through LS02 1B/1F. These are service circuits, not
matrix contacts. PinMAME s11_irqline presents Black Advance to PIA2 CA1
complemented and Green Up/Down to CB1 directly. Public 1 is the button's down
position, as s11's own diagnostic status labels say; the circuit's internal
logic level must not be reapplied by a consumer. The green push-on/push-off
direction selector is a maintained control: 0 forward/up, 1 reverse/down.

Operator PDF 7, printed p.3: installation uses three balls, approximately
6.5-degree playfield pitch, and explicitly says there is no ball-roll tilt.
Closing the plumb tilt triggers tilt warnings/tilt; closing slam tilt ends the
current games. PDF 26, printed p.24: Active Switch Test names closed switches
and removes the name on release. Together with the unmasked, uninverted matrix
read path and the retained ROM's active-at-1 screens, this establishes normally
open contacts for the used matrix inputs, including cabinet contacts.

Operator PDF 25, printed p.23, Bar Motor diagnostic: UP and DOWN closures occur
just before the corresponding travel limit; both must never be ON together.
Use that diagnostic to test the two ends. The retained recreation maps them to
41 and 42 and makes the bar target non-collidable when the bar is lowered.

## Factory flasher discrepancy retained

Operator PDF 31, printed p.29, coil wiring sheet, 6R branch prints (2) PLFD,
(2) INSERT, (4) NO.89. Separate schematic PDF 4, printed p.48, prints the same
location labels but (3) NO.89. The complete eight-bank annotations of the latter
sheet are in `manual-spatial.md`. The ROM labels both 4R and 8R FOUR playfield
flashers; its strings are software descriptions, not a physical socket count.
The definition retains the unresolved physical-count conflict.
