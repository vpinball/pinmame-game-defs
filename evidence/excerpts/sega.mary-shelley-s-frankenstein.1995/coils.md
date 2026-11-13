# Mary Shelley's Frankenstein coils and flash lamps (manual and wiring sheets)

Sources:

- Manual: `Sega_1995_Mary_Shelley_s_Frankenstein_English_Manual_pages_1_66_which_excludes_schematics_OCR_searchable.pdf` (SHA-256 `2f752c431e3b2a4718180e52340c5394f36b41833a150464f04d52d442be8764`). PDF page 39 (printed page 35, "Game Diagnostics"): "Coil Locations" and "Flash Lamp Locations" drawings with a legend. PDF page 40 (printed page 36): "Switched, CPU Controlled Auxillary & Constant Power Solenoids" table and "Flipper Solenoids" table. PDF page 41 (printed page 37): the coil chart schematic (section 5 below). Page 38 (printed page 34) holds only flash lamp / coil test text (section 6).
- Schematics: `Sega_1995_Mary_Shelley_s_Frankenstein_English_Manual_pages_67_93_which_are_the_schematics_OCR_searchable.pdf` (SHA-256 `e4eeb409e321ea1eb3f9d30120e488db8b638a6d3d69f3c66c2c9ca7919bf883`). PDF page 6 (printed page 72, "Playfield Coil / Flashlamp Wiring Diagram", printed twice on the sheet) and PDF page 7 (printed page 73, "Playfield Special Coil Diagram").

Conventions: in the coil table each cell that is printed on two lines (for example `PPB` over `J 2-1`) is joined with one space; the description cells print a bold word on the first line (`Coil:` or `Flashlamp: X1 P/F, Insert X3`) and the name on the next; these are joined with one space. Spelling, capitalization, punctuation and spacing inside connector text (`J 2-1` against `J8-12`, `CN 12-1`) are as printed. Where one printed cell spans two rows (a merged cell) the value is written in the first row and the second row carries `[merged with row above]`; no value was repeated. A dash-and-dot pattern printed in a cell is written `— · —`. No other normalization was applied. Handwriting is only ever listed in its own section (4b).

## 1. Coil / flashlamp table (PDF page 40, top table)

Table title as printed: "Switched, CPU Controlled Auxillary & Constant Power Solenoids". Column headings as printed: `Coil No.`, `Coil or Flashlamp Description`, `Drive Trans-istor (D.T.)` (printed `Drive Trans-` / `istor (D.T.)`, hyphen of the line break joined), `On Which Board?`, `D.T. Control Line`, `D.T. Control Line Connect`, `Power Line`, `Power Line Connection`, `Power Description`, `Coil or Flash Type`. The table lies completely on this page. Shaded cells: none in this table. Rows 1L-8R are printed in L/R pairs (coil above flashlamp).

| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil or Flash Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1L | Coil: 6-Ball Assembly Lockout | Q46 | CPU | VIO-BRN | PPB J 2-1 | BRN | PPB J 6-1, 2 | 32v L | 25-1240 |
| 1R | Flashlamp: X1 P/F, Insert X3 Flash above "A-N-K" | [merged with row above] | [merged with row above] | BLK-BRN | PPB J 9-1 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 2L | Coil: Trough Up-Kicker (TRUK) | Q45 | CPU | VIO-RED | PPB J 2-2 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 2R | Flashlamp: X2 P/F, Insert X2 Flashes above "F-R" | [merged with row above] | [merged with row above] | BLK-RED | PPB J 9-2 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 3L | Coil: Auto Launch 50v | Q44/Q5 | CPU/PPB | VIO-ORN | PPB J 8-2 | YEL/VIO | PPB J 7-8 | 50v L | 24-940 |
| 3R | Flashlamp: X1 P/F, Insert X3 Flash above "I-N" | Q44 | CPU | BLK-ORN | PPB J 9-3 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 4L | Coil: Bottom Scoop Kick-Big | Q43 | CPU | VIO-YEL | PPB J 2-4 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 4R | Flashlamp: X4 P/F, Insert X0 Flashes by Pop Bumpers | [merged with row above] | [merged with row above] | BLK-YEL | PPB J 9-4 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 5L | Coil: Top Scoop Kick-Big | Q42/Q2 | CPU | VIO-GRN | PPB J 2-5 | YEL/VIO | PPB J 7-8 | 50v L | 23-800 |
| 5R | Flashlamp: X2 P/F, Insert X2 Flashes by Spinner | Q42 | CPU/PPB | BLK-GRN | PPB J 9-5 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 6L | Coil: Playfield Ball Eject | Q41 | PPB | VIO-BLU | PPB J 2-6 | BRN | PPB J 6-1, 2 | 32v L | 24-940 |
| 6R | Flashlamp: X3 P/F, Insert X1 Flashes Upper Left Corner | [merged with row above] | CPU | BLK-BLU | PPB J 9-6 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 7L | Coil: VUK 50v | Q40/Q4 | CPU | VIO-BLK | PPB J 8-4 | YEL/VIO | PPB J 7-8, 2 | 50v L | 24-940 |
| 7R | Flashlamp: X3 P/F, Insert X1 Flashes around VUK | [merged with row above] | [merged with row above] | BLK-VIO | PPB J 9-7 | ORN | PPB J 6-4, 5 | 32v R | Bulb #89 |
| 8L | Coil: Knocker 32v (In Cabinet) | Q39 | CPU | VIO-GRY | PPB J 2-8 | BRN | PPB J 6-1, 2 | 32v L | 23-800 |
| 8R | Flashlamp: X0 P/F, Insert X0 Not Used in this Game. | [merged with row above] | [merged with row above] | — · — | — · — | — · — | — · — | — · — | — · — |
| 09 | Coil: Ramp Trap Door Right | Q30 | CPU | BRN-BLK | CPU CN 12-1 | RED | PS CN 3-6,7 | 32v | 28-1050 |
| 10 | Coil: Located on PPB in Backbox Left & Right Relay | Q29 | CPU | BLK-RED | CPU CN 12-2 | RED | PS CN 6-7 | 32v | 24v DC 10A DPDT |
| 11 | Coil: Located on Power Supply Bd. G.I. Relay | Q28 | CPU | BRN-ORN | CPU CN 12-4 | RED | PS CN 3-6,7 | 32v | 24v DC 10A DPDT |
| 12 | Coil: Ramp Trap Door Left | Q27 | CPU | BRN-YEL | CPU CN 12-5 | RED | PS CN 3-6,7 | 32v | 28-1050 |
| 13 | Coil: Monster Arms | Q26 | CPU | BRN-GRN | CPU CN 12-6 | RED | PS CN 3-6,7 | 32v | 23-800 |
| 14 | Coil: Right Orbit Ball Diverter | Q25 | CPU | BRN-BLU | CPU CN 12-7 | RED | PS CN 3-6, 7 | 32v | 27-1400 |
| 15 | Flashlamp: X4 P/F, Insert X0 Flashes around VUK | Q24 | CPU | BRN-VIO | CPU CN 12-8 | RED | PS CN 3-6,7 | 32v | 27-1500 |
| 16 | Coil: Laser Kick 50v | Q23/Q1 | CPU/PPB | BRN-GRY | PPB J8-12 | VIO-YEL | PPB J 7-3 | 50v | 23-800 |
| 17 | Coil: Top Turbo Bumper | Q11 | CPU | BLU-BRN | CPU CN 19-7 | RED | PS CN 3-6 | 32v | 23-700 |
| 18 | Coil: Middle Left Turbo Bumper | Q9 | CPU | BLU-RED | CPU CN 19-4 | RED | PS CN 3-6 | 32v | 23-700 |
| 19 | Coil: Middle Right Turbo Bumper | Q8 | CPU | BLU-ORN | CPU CN 19-3 | RED | PS CN 3-6 | 32v | 23-700 |
| 20 | Coil: Bottom Turbo Bumper | Q10 | CPU | BLU-YEL | CPU CN 19-6 | RED | PS CN 6-6, 7 | 32v | 23-800 |
| 21 | Coil: Left Slingshot | Q12 | CPU | BLU-GRN | CPU CN 19-8 | RED | PS CN 6-6, 7 | 32v | 23-800 |
| 22 | Coil: Right Slingshot | Q13 | CPU | BLU-BLK | CPU CN 19-9 | RED | PS CN 6-6, 7 | 32v | 23-800 |

Row count: 30 rows (1L-8R = 16, 09-22 = 14). Notes on the printed table: the description of row 8L carries the parenthetical "(In Cabinet)" in a smaller type; the `Coil or Flash Type` cells of rows 10 and 11 are printed in smaller type on two lines (`24v DC` / `10A DPDT`); in rows 1L-8R the drive-transistor and board cells of one L/R pair are a single merged cell except where both rows carry their own value (3L/3R, 5L/5R, 6L/6R).

## 2. Flipper Solenoids table (PDF page 40, bottom table)

Column headings as printed: `SSFB No.`, `Flipper Coil`, `Cabinet Switch`, `Switch Drive`, `Switch Return`, `E.O.S.`, `GND`, `Flipper 50vDC Power`, `Flipper 8vAC Hold`, `Flipper Coil Output`. Each `SSFB No.` cell prints `SSFB` over `1`. Under each Flipper Coil name the cell prints the coil number `23-1100` and a line of wire colours.

| SSFB No. | Flipper Coil | Cabinet Switch | Switch Drive | Switch Return | E.O.S. | GND | Flipper 50vDC Power | Flipper 8vAC Hold | Flipper Coil Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SSFB 1 | Lwr. Rt. Flipper 23-1100 BLU/YEL ORN/VIO | BLU-VIO SSFB CN1-7 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-GRY CPU CN10-1 TO SSFB CN1-3 | BRN-VIO RT. EOS SW. TO CN1-1 | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-8, -9 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-7, -8 | 50v / 8vAC; Q2, Q3, / SR1; CN2-7, 8 |
| SSFB 1 | Lwr. Lt. Flipper 23-1100 GRY/YEL ORN/GRY | BLU-GRY SSFB CN1-11 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-VIO CPU CN10-2 TO SSFB CN1-5 | BRN-GRY LT. EOS SW. TO CN1-9 | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-8, -9 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-7, -8 | 50v / 8vAC; Q10, Q9, / SR2; CN2-4, 5 |
| SSFB 1 | Upr. Rt. Flipper 23-1100 BLU/YEL ORN/GRY | GRY-VIO SSFB CN1-12 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-GRY CPU CN10-2 TO SSFB CN1-10 | Not Used | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-8, -9 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-7, -8 | 50v / 8vAC; Q16, Q15, / SR3; CN2-1, 2 |

Row count: 3. The Flipper Coil Output cell is printed as a three-line cell: line 1 `50v` and `8vAC` separated by a vertical bar; line 2 `Q2, Q3,` bar `SR1` (rows 2 and 3 read `Q10, Q9,` bar `SR2` and `Q16, Q15,` bar `SR3`); line 3 `CN2-7, 8` (`CN2-4, 5`, `CN2-1, 2`). In the table above the bar-separated halves are written with ` / ` and the lines with `; `. The "Switch Return" cell of row 3 is printed `CPU CN10-2 TO SSFB CN1-10` (the same CN10-2 as row 2).

## 3. Coil and flash lamp location drawings (PDF page 39)

Page title area: left drawing titled "Coil Locations", right drawing titled "Flash Lamp Locations", lower right drawing titled "Backbox (Insert) Flash Lamps & G.I.s". Callouts are black discs with white labels. No coordinates are given; positions are described on each drawing (top = back of playfield, left/right as viewed).

### 3a. Legend table (lower left of page)

Printed in two columns of 11/11 entries. Label then text as printed:

| Label | Text as printed | Shading |
| --- | --- | --- |
| 1L | 6-Ball Ass'y Lockout | none |
| 1R | Flash above "A-N-K" | none |
| 2L | Ball Eject to Shooter Lane | none |
| 2R | Flashes above "F-R" | none |
| 3L | Auto Launch 50v | none |
| 3R | Flash above "I-N" | none |
| 4L | Bot. Scoop Kick-Big 50v | none |
| 4R | Flashes by Pop Bumpers | none |
| 5L | Top Scoop Kick-Big 50v | none |
| 5R | Flashes by Spinner | none |
| 6L | Playfield Ball Eject | none |
| 6R | Flashes Upper Left Corner | none |
| 7L | VUK 50v | none |
| 7R | Flashes around VUK | none |
| 8L | Knocker 32v | shaded |
| 8R | Not Used | shaded |
| 09 | Ramp Trap Door Right | none |
| 10 | Left/Right (A/B) Relay | shaded |
| 11 | G.I. Relay | shaded |
| 12 | Ramp Trap Door Left | none |
| 13 | Monster Arms | none |
| 14 | Right Orbit Ball Diverter | none |
| 15 | Flashes around VUK | none |
| 16 | Laser Kick 50v | none |
| 17 | Top Turbo Bumper | none |
| 18 | Mid. Left Turbo Bumper | none |
| 19 | Mid. Right | none |
| 20 | Bottom Turbo Bumper | none |
| 21 | Left Slingshot | none |
| 22 | Right Slingshot | none |

Legend note printed beneath: "Note: Shaded areas not shown on Diagrams." and "G.I. = General Illumination Lamps". Legend rows: 30.

### 3b. Coil Locations drawing (left playfield drawing)

Callout labels on the drawing: 12, 9, 14, 7L, 13, 6L, 17, 5L, 19, 18, 20, 4L, 21, 22, 16, 2L, 1L, 3L (18 labels). The shaded legend rows (8L, 8R, 10, 11) and 15 are not drawn. The drawing was read for orientation only; no placement in the definition is taken from it.

### 3c. Flash Lamp Locations drawing (right playfield drawing)

Callout labels on the drawing, each with arrows to one or more flash lamp symbols: 7R, 6R, 15, 5R, 15, 4R, 1R, 2R, 3R (15 appears twice). The drawing was read for orientation only; no placement in the definition is taken from it.

### 3d. Backbox (Insert) Flash Lamps & G.I.s drawing (lower right of the page)

An outline of the backbox insert board with circles: double circles labelled with a flash lamp label, and small circles labelled `G.I.` (printed as a G over I inside the small circle). Counts as printed: labelled double circles are 1R (three: upper left, right centre, lower left), 2R (two: upper centre, left lower), 3R (three: upper left, upper right, lower centre), 5R (two: left, centre), 6R (one: upper centre), 7R (one: left centre); the small G.I. circles number about 33 (counted approximately). No other text on the drawing. The page caption reads "Backbox (Insert) Flash Lamps & G.I.s".

## 4. Schematics PDF page 6 (printed page 72): Playfield Coil / Flashlamp Wiring Diagram

The sheet is a yellow single page with the diagram titled "Playfield Coil / Flashlamp Wiring Diagram" and page number "72" printed twice at the bottom. All labels below are printed unless listed in section 4b.

### 4a. Printed content

**Coil blocks (top row, left to right).** Each block prints: name, coil part number, transistor, driver label, and a wire label from its lower terminal. All blocks share the BRN upper bus; the +50 and +32 supplies are noted below.

| Printed name | Coil part number | Transistor | Driver label | Wire label at the lower terminal |
| --- | --- | --- | --- | --- |
| LASER KICK | 23-800 | Q23 | 16 | BRN/GRY (thick line to J8 pin 10); upper terminal line VIO/YEL to "+50 PPB J7-3" |
| KNOCKER | 23-800 | Q39 | 8L | VIO/GRY |
| RIGHT VUK | 24-1240 | Q40 | 7L | VIO/BLK |
| PLFD EJECT | 26-1200 | Q41 | 6L | VIO/BLU |
| TOP SCOOP | 23-800 | Q42 | 5L | VIO/GRN |
| BOTTOM SCOOP | 23-800 | Q43 | 4L | VIO/YEL |
| AUTO LAUNCH | 24-940 | Q44 | 3L | VIO/ORG |
| TROUGH UP KICKER | 23-800 | Q45 | 2L | VIO/RED |
| 6 BALL LOCK OUT | 25-1240 | Q46 | 1L | VIO/BRN |

Supply labels on the top bus: "+50VDCL PPB J7-8\9" with wire `YEL/VIO` (to the upper terminals of Right VUK, Top Scoop and Auto Launch); "+32VL PPB J6-2/1" with wire `BRN` (to the Knocker, Plfd Eject, Bottom Scoop, Trough Up Kicker and 6 Ball Lock Out upper terminals); "+50 PPB J7-3" with wire `VIO/YEL` (Laser Kick). The coil lower-terminal wires run to the PPB J8 connector (pins printed `10 9`, `8 7`, `6 5`, `4 3`, `2 1`) and to the J2 connector (pins `1`-`10`). Additional wire labels between J8 and the coils, as printed: `VIO/GRN`, `WHT/BLU`, `WHT/VIO`, `WHT/ORG`, and `WHT/GRY` with a bracketed `CPU CN12-9` (small print), and the text `N.C.` with a bracketed `NOT USED` at J8 pins 6/5.

**J8 transistor stage (PPB).** Five transistors, each printed: Q1 TIP 36C with R-19 220 ohm and D21 1N4004 (J8 pins 10, 9); Q2 TIP 36C with R-18 220 and D20 1N4004 (pins 8, 7); Q3 TIP 36C with R-17 220 and D19 1N4004 (pins 6, 5, KEY printed beside); Q4 TIP 36C with R-16 220 and D18 1N4004 (pins 4, 3); Q5 TIP 36C with R-15 220 and D17 1N4004 (pins 2, 1). (The printed unit is the ohm sign; `R-19 220 Ω`.) The J8 pin text is as printed: `10 9`, `8 7`, `6 5` , `4 3`, `2 1`.

**PPB J2 connector** pins as printed (left to right): 1 (printed `N.C.` beneath), 2, 3, 4 (printed `KEY` beneath), 5, 6, 7, 8, 9, 10. The J2 lines run to rows tagged `1R`-`8R` at the J1 side; reading of which J2 pin feeds which row, by tracing the drawn lines: pin 10 to 1R; pin 9 to 2R; pin 8 to 3R; pin 7 to 4R; pin 6 to 5R; pin 5 to 6R; pin 3 to 7R; pin 2 to 8R [?trace of J2 pin-to-row lines]. Each of rows 1R-8R prints a resistor and a diode pair: 1R R-1/D9/D1, 2R R-2/D10/D2, 3R R-3/D11/D3, 4R R-4/D12/D4, 5R R-5/D13/D5, 6R R-6/D14/D6, 7R R-7/D15/D7, 8R R8/D16/D8.

**PPB J1 to CPU CN11 (wires and "SOL. DRIVE" labels as printed)**

| J1 pin | Wire | CN11 pin | Label printed |
| --- | --- | --- | --- |
| 1 | GRY/BRN | 1 | SOL. DRIVE 1 Q46 |
| 2 | GRY/RED | 3 | SOL. DRIVE 2 Q45 |
| 3 | GRY/ORG | 4 | SOL. DRIVE 3 Q44 |
| 4 | GRY/YEL | 5 | SOL. DRIVE 4 Q43 |
| 5 | GRY/GRN | 6 | SOL. DRIVE 5 Q42 |
| 6 | GRY/BLU | 7 | SOL. DRIVE 6 Q41 |
| 7 | GRY/VIO | 8 | SOL. DRIVE 7 Q40 |
| 8 | GRY/BLK | 9 | SOL. DRIVE 8 Q39 |

(Rows 9-14 of J1 are printed `9 R9`, `10 R10`, `11 R11`, `12 R12`, `13 R13`, `14 R14`, with the lead tags `9`, `12`, `13`, `14`, `15`, `16` at the left of the resistors R9-R14; these J1 pins 9-14 connect to CN12 as below.) The bracket to the right reads "C.P.U. BOARD".

**CPU CN12 (J1 pins 9-14 and CPU CN12), as printed**

| CN12 pin | Wire | Label printed |
| --- | --- | --- |
| 1 | BRN/BLK | SOL. DRIVE 9 Q30 |
| 2 | BLK/RED | SOL. DRIVE 10 Q29 |
| 4 | BRN/YEL | SOL. DRIVE 11 Q28 |
| 5 | (joined to the pin 4 line by a drawn tie; no separate wire label) | SOL. DRIVE 12 Q27 |
| 6 | BRN/GRN | SOL. DRIVE 13 Q26 |
| 7 | BRN/BLU | SOL. DRIVE 14 Q25 |
| 8 | BRN/VIO | SOL. DRIVE 15 Q24 |
| 9 | WHT/GRY | SOL. DRIVE 16 Q23 |

Pin 3 of CN12 is not drawn. A vertical wire label `BRN/ORG` runs from the CN12 area down to P.S. CN7 pin 3.

**Playfield coils on the left (Q30, Q27, Q26, Q25 at CPU CN 12)**, as printed:

| Name | Part number | Wire to supply | CN12 pin | Wire to CN12 | Transistor |
| --- | --- | --- | --- | --- | --- |
| RIGHT TRAP DOOR | 28-1050 | RED 9 | 1 | BRN/BLK | Q30 |
| LEFT TRAP DOOR | 28-1050 | RED 12 | 5 | BRN/YEL | Q27 |
| MONSTER ARMS | 23-800 | RED 14 | 6 | BRN/GRN | Q26 |
| DIVERTER | 27-1400 | RED 14 | 7 | BRN/BLU | Q25 |

Supply label at the far left: "+32 VDC PS CN3-7/6" with wire label `RED`. Wire numbers `9`, `12`, `14`, `14` are printed as shown beside each RED wire.

**Flasher groups.** Each group prints a title line, a bulb type line and a wire label; the bulbs sit on a common return bus. Groups labelled in the lower region, with the "+32VDCR PPB J6-4/5" `ORG` supply labels at the top of each row:

| Group label (right of the bulbs) | Printed title | Bulbs and type lines | Return wire |
| --- | --- | --- | --- |
| 1R | (1) LOWER 3 BANK S.U.(3)INSERT | (4) NO.89 | BLK/BRN |
| 2R | (2) LEFT BOTTOM PLFD(2)INSERT | (4) NO.89 | BLK/RED |
| 3R | (1) RIGHT BOTTOM PLFD(3)INSERT | (4) NO.89 | BLK/ORG |
| 4R | (4) TURBO BUMPERS | (4) NO. 89 | BLK/YEL |
| 5R | (2) RIGHT MID PLFD(2)INSERT | (4) NO. 89 | BLK/GRN |
| 6R | (3) LEFT TOP PLFD(1)INSERT | (3) NO.89 / (1) NO.906 | BLK/BLU |
| 7R | (3) RIGHT TOP PLFD(1)INSERT | (4) NO.89 | BLK/VIO |
| 8R | (4) NOT USED | (none printed) | BLK/GRY |
| (no group label; at the left) | (4) UPPER RIGHT PLAYFIELD | (4) NO. 89 | wire `BRN/VIO` with the text `(TO Q24)`; supply `ORG 15` from "+32VDCR PPBJ6-4/5" |

The upper-right-playfield group sits at the lower left beside the coil list and its supply wire is printed `ORG` with the number `15`. The R-groups' upper supply labels read "+ 32VDCR PPB J6-4/5" and `ORG` (printed over 3R and 7R).

**General illumination lines block (left, labelled "GENERAL ILLUMINATION LINES").** "POWER SUPPLY BOARD CN 8" connector pins, as printed: 1 `BRN`, 2 `YEL`, 3 `GRN`, 4 `VIO`, 5 `KEY` under the bracket "6.3 VAC OUTPUT TO BULBS"; pins 6, 7, 8, 9 under the bracket "6.3 VAC OUTPUT TO FUSES" (no wire labels printed for 6-9 on the CN8 side). PPB J5 pins, as printed: 9 `WHT/VIO`, 8 `KEY`, 7 `WHT/GRN`, 6 `WHT/YEL`, 5 `WHT/BRN` under "6.3 VAC OUTPUT TO BULBS"; 1 `WHT/BRN`, 2 `WHT/YEL`, 3 `WHT/GRN`, 4 `WHT/VIO` on the fuse side. Fuses F4, F3, F2, F1 each "5 AMP SLO BLO" (the text "5 AMP SLO BLO" is printed once to the right of the four fuses).

**J4 / BR1 (50 V supply).** J4 pins 5, 4, 3, 2, 1 on the "48 VAC" side: pin 5 `BLK/YEL`, pin 3 `BLK/YEL`, pin 2 `KEY` (pins 4 and 1 unlabelled); F5 "5 AMP SLO BLO"; bridge BR1; C1 "100µf 250V"; C2 "0.1µf"; R20 "802K 5W". J3: pins 4, 3, 2, 1 each `BLK` with the bracket label `GND`.

**PPB J9 connector (bottom, labelled J9), as printed** pin number then label: 11 `N.C.`; 10 `N.C.`; 9 `N.C.`; 8 `N.C.` (diagonal tag `R8`); 7 `BLK/VIO` (tag `R7`); 6 `BLK/BLU` (`R6`); 5 `BLK/GRN` (`R5`); 4 `BLK/YEL` (`R4`); 3 `BLK/ORG` (`R3`); 2 `BLK/RED` (`R2`); 1 `BLK/BRN` (`R1`); `KEY`; 14 `N.C.`; 13 `BRN/VIO`; 12 `N.C.`. The tags `R1`-`R8` and `11`, `10`, `9`, `14`, `13`, `12` are printed on diagonal leader lines above the connector.

**PPB J7 connector (printed pins 9 to 1, left to right):** 9 `YEL/VIO`; 8 `YEL/VIO`; 7 `N.U.`; 6 `N.U.`; 5 `BLK/WHT`; 4 `KEY`; 3 `VIO/YEL`; 2 `BLK/WHT`; 1 `BLK/WHT`. Group labels under it: "+50VDCL (NORMALLY CLOSED)" under pins 9/8; "+50VDCR (NORMALLY OPEN)" under pins 7/6; "FLIPPER +50DC" under pins 5, 3, 2, 1.

**PPB J6 connector (printed pins 9 to 1, left to right):** 9 (connected, no wire text on the pin); 8 `KEY`; 7 `RED/WHT`; 6 (no label); 5 `ORG`; 4 `ORG`; 3 `BRN`; 2 `BRN`; 1 `BRN`. Group labels: "+32VR FLASHERS" under pins 5/4; "+32VL COILS" under pins 3, 2, 1; "+32V FROM P.S. CN3 PIN5" at the left of J6.

**K1 relay (dashed box, label `K1`).** Contacts and fuses printed: F8 "4 AMP SLO BLO", F9 "5 AMP SLO BLO", F7 "3 AMP SLO BLO", F6 "5 AMP SLO BLO"; the coil is printed `SOL` with diode `D22`. **A/B RELAY note (upper right), printed in three lines:** "A/B RELAY" / "NORMALLY CLOSED SIDE ="N.C." ="L"EFT ="A" SIDE" / "NORMALLY OPEN SIDE ="N.O." ="R"IGHT ="B" SIDE" / "N.U. MEANS "NOT USED"".

**General Illumination relay (right).** "+ 32V" feeds P.S. CN7 pin 1; pin 2 `KEY`; pin 3 joined via wire `BRN/ORG`; the relay block is printed `SOL I` / `RY1` / `GENERAL ILLUMINATION RELAY`, with the bracket "POWER SUPPLY BOARD". A diode is drawn across the relay coil.

**Printed boxes:** "PPB" (dashed box in the centre), "CPU CN 12" (box at the left lower), "CN11" and "CN12" (boxes at the right).

### 4b. Handwritten annotations (not printed; transcribed separately)

| Handwritten text (best reading) | Location on the sheet |
| --- | --- |
| `50V-DC` | above the BR1 bridge / C1 line, upper centre-left |
| `Q24-CPU` and `122` (below it) | lower left, under the upper-right-playfield flasher group wire `(TO Q24)` |
| `Sol. Dr. 15` (read as `Sol. Dr.15`) | lower left, above and right of the `(TO Q24)` label, near the J9 BRN/VIO line |
| `J6` | left of the PPB J6 connector, beside pin 9 |
| `Q29` | below the J6 connector, left of the "+32VR FLASHERS" label |
| `122` and `Q46` | left of the `BLK/BRN` return wire of group 1R |
| `Q 45-122` (read as `Q45-122`) | below the 2R group, above `BLK/RED` |
| `122` and `Q44 - CPU` | below the 3R group |
| `122` and `Q43` | below the 4R group |
| `122` and `Q42` | below the 5R group, near `BLK/GRN` |
| `122` and `Q41` | below the 6R group, near `BLK/BLU` |
| `122` and `Q40` | below the 7R group, near `BLK/VIO` |
| `122` and `Q39` | below the 8R group, near `BLK/GRY` |
| `NOT USED` with a large curly brace | right of the 8R group (brace encloses the 8R group) |

The handwritten notes that read "122" and a Q number are each a number written above a Q label, as printed in the position described.

## 5. Manual PDF page 41 (printed page 37): coil chart schematic

A schematic page without a table; it repeats, in the manual's own drawing, the PPB/CPU wiring of each coil pair. Visible printed labels, as read at low resolution: sections `1-L\R` through `8-L\R`, each showing "P/O CPU BOARD" with "SIDE L 01 ... TIP 122 ... Q46 ... SIDE R 01", `CN-11`, "P/O PPB BOARD", `J1`, `J2`, `J9`, a diode and resistor pair (D1/D9-R1, D2/D10-R2, D3/D11-R3, D4/D12-R4, D5/D13-R5, D6/D14-R6, D7/D15-R7, D8/D16-R8), coil labels `6 BALL LOCK OUT 25-1240`, `TROUGH UP KICKER 23-800`, `BALL LAUNCH 24-940`, `BOTTOM SCOOP 23-800`, `TOP SCOOP 23-800`, `EJECT 26-1200`, `RIGHT VUK 25-1240`, `KNOCKER 23-800`; wire labels `GRY-BRN`, `VIO-BRN`, `BLK-BRN`, `BRN`, `ORG` (and equivalents for each pair); bulb group notes `(1) SUPER MODE PLFD (3) INSERT (4) 89`, `(2) LEFT BOTTOM PLFD (2) INSERT (4) 89`, `(1) RIGHT BOTTOM PLFD (3) INSERT (4) 89`, `(4) TURBO BUMPERS (4) 89`, `(2) RIGHT MID PLFD (2) INSERT (4) 89`, `(3) TOP LEFT PLFD (1) INSERT (4) 89`, `(3) TOP RIGHT PLFD (1) INSERT (4) 89`, `NOT USED`; and the lower block "P/O CPU BOARD CN-12" with `09 Q30 BRN/BLK` TRAP DOOR RAMP RIGHT 28-1050, `10 Q29 BLK-RED` L/R COIL RELAY, `11 Q28 BRN-ORG`, `12 Q27 BRN/YEL` TRAP DOOR RAMP LEFT 28-1050, `13 Q26 BRN/GRN` MONSTER ARM 23-800, `14 Q25 BRN/BLU` DIVERTER 27-1400, `15 Q24 BRN/VIO` (4) UPPER RIGHT PLAYFIELD, `16 Q23 WHT/GRY` LASER KICK 23-800, and "P/O PS BOARD CN3 +32V", `CN7`, `K-1`, "GENERAL ILLUM. RELAY". Page number printed `37` ("Game Diagnostics"). This page was read only for orientation; it carries `Q5`, `Q2`, `Q4`, `Q1` helper-transistor boxes labelled "P/O PPB BOARD" on rows 3, 5, 7 and 16.

## 6. Test-page text relevant to coils (PDF page 38, printed page 34)

> "Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right Relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils."

## 7. Schematics PDF page 7 (printed page 73): Playfield Special Coil Diagram

Page title printed at the bottom right: "Playfield Special Coil Diagram" with page number `73`. All labels as printed:

Supply: a `RED` wire from "CN 3" pin `6` ("POWER SUPPLY" bracket) to the common top bus of the six coils.

| Coil label | Printed name | Part number | Lower terminal wire | CN 19 line |
| --- | --- | --- | --- | --- |
| SP6 | RIGHT SLINGSHOT | 23-800 | BLU/BLK | pin 9: "SW.SOL DRIVE 6Q13" |
| SP5 | LEFT SLINGSHOT | 23-800 | (none printed at the coil; routes to CN 19) `BLU-GRN` | pin 8: "SW.SOL DRIVE 5Q12" |
| SP4 | TOP TURBO BUMPER | 23-700 | `BLU-BRN` | pin 7: "SW.SOL DRIVE 4Q11" |
| SP3 | BOTTOM TURBO BUMPER | 23-700 | `BLU-YEL` | pin 6: "SW.SOL DRIVE 3Q10" |
| SP2 | LEFT TURBO BUMPER | 23-700 | `BLU-RED` | pin 4: "SW.SO. DRIVE 2Q9" |
| SP1 | RIGHT TURBO BUMPER | 23-700 | `BLU-ORG` | pin 3: "SW.SOL DRIVE 1Q8" |

Connector labelled `CN 19` with six pins numbered 3, 4, 6, 7, 8, 9 (pins as printed beside each line: `3`, `4`, `6`, `7`, `8`, `9`). Wire labels along the lines: `BLU-ORG`, `BLU-RED`, `BLU-YEL`, `BLU-BRN`, `BLU-GRN`, `BLU/BLK` (printed with a slash, unlike the others, and also printed vertically on the SP6 drop as `BLU/BLK`). The connector label `CN 3` appears at the top right.

Each coil is drawn with a diode across it. The coil labels `SP1` to `SP6` are printed beside the coils (SP1 at the right end, SP6 at the left end). Rows: 6 coils, 6 CN 19 pins.

## Uncertain readings

- Section 4a, J2 pin-to-row mapping: `[?pin 10 to 1R, 9 to 2R, 8 to 3R, 7 to 4R, 6 to 5R, 5 to 6R, 3 to 7R, 2 to 8R]` was read by tracing drawn lines on the diagram, not from a printed label.
- Section 3d: the count of G.I. circles on the backbox insert drawing (about 33) is an approximate count.
- Section 5: the page 41 labels were read at low resolution and are listed for orientation only.
