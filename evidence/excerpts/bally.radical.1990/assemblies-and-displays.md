# Radical construction and display tables

Source: Bally / Midway *Radical!* Operator Handbook 16-2015-101, April 1990,
SHA256 `a5085eb4c9088f3cba48949dba9f30a72c8aa3f30208d4f65150cc6e1f777cb6`.
IPDB machine 1904: https://www.ipdb.org/machine.cgi?id=1904;
direct file https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf.
Manufacturer copyright; no redistribution license established. Factual table transcriptions only.
Manually read and visually reviewed by primary curator, 2026-11-06, against retained page renders.
Line wrapping and spacing are normalized; `[blank]` is a visibly empty cell, not an inferred value.
Hyphens in part numbers are preserved. The right display scan clips the left edge of descriptions;
`[clipped]` marks the missing portion. No sibling board completes those cells.

## PDF 76, printed 2-22: 3-Bank Drop Target Assembly, C-11223-4

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | 03-8033 | Plain Target |
| 2 | B-13271 | 3-Bank Target Sub-assembly |
| 3 | 10-364 | Target Retractor Spring |
| 4 | C-13205-1 | 3-Bank Target Opto assembly |
| 5 | 20-8712-18 | “E” Ring, 3/16” Shaft |
| 6 | 20-8712-25 | “E” Ring, 1/4” Shaft |
| 7 | 10-392 | Compression Spring |
| 8 | 4408-01119-00 | Nut, 8-32 ESN |
| 9 | A-11397 | Stop Bracket Assembly |
| 10 | AE-26-1200 | Coil Assembly |
| 11 | 01-8413 | Coil Mounting Bracket |
| 12 | A-11389 | Plunger & Reset Plate Assembly |
| a) | 02-3972-1 | Plunger |
| b) | 01-8408 | 3-Bank Reset Plate |
| c) | 4410-01132-00 | Nut, 10-32 ESN |
| 13 | 03-7066-4 | Coil Tubing |
| 14 | 4700-00016-00 | Flatwasher, .13 x 7/16 x 17 ga. |
| 15 | 4008-01016-10 | Mach. Screw, 8-32 x 5/8 P-RH |
| 16 | 4700-00072-00 | Flatwasher, 17/64 x 1/2 x 21 ga. |
| 17 | 23-6626 | Rubber Grommet |

The drawing shows three independently retracting target blades and their shared reset plate,
coil/plunger and opto board. It supplies topology, not a measured travel time or sensor polarity.

## PDF 77, printed 2-23: 3-Bank Drop Target Opto Board, C-13205-1

| Part No. | Ckt Designation | Description |
| --- | --- | --- |
| 5768-12546-00 | [blank] | 3-Bank Opto Board |
| 5490-10159-00 | Opto 1 - Opto3 | Opto Interrupter, MDL, S/G |
| 5010-08930-00 | R1, R3, R5 | Resistor, C.F., 470 Ω, 1/2w, 5% |
| 5010-09162-00 | R8 | Resistor, C.F., 100KΩ, 1/4w, 5% |
| 5010-09234-00 | R2, R4, R6 | Resistor, C.F., 27KΩ, 1/4w, 5% |
| 5010-08774-00 | R7 | Resistor, C.F., 22KΩ, 1/4w, 5% |
| 5043-08980-00 | B | Capacitor, .01μfd., +80, -20% |
| 5370-12272-00 | U1 | I.C., Quad. Comp., LM339 |
| 5791-12548-07 | J1 | 7 pin header R/A lock Sq. .100 |
| 5070-09054-00 | D1, D2, D3 | Diode, 1N4004, 1.0A |

The board drawing labels Opto1, Opto2, Opto3 and marks R9-R11 “Not Installed”.
This is positive opto construction evidence for both banks named C-11223-4 in the switch inventory;
the switch matrix's lack of opto shading does not change it. Electrical normal state is derived
separately from the System 11 read path and the working drop-target script.

## PDF 71, printed 2-17: Standup Target Assemblies (Including Diode)

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | B-11696-4 | Standup Target (Red) |
| 2 | B-13900-4 | Standup Target (Red) |

## PDF 71, printed 2-17: Ball Trough Switches

| Part No. | Description |
| --- | --- |
| B-13623 | Switch Plate Assembly |
| A-5844-44 | Switch Wire & Bracket Assy |
| B-13622 | Switch Mounting Plate Sub-Assy |
| RM-21-03 | #10 Tubing |
| 4004-01060-08 | MS 4-40 x 1/2 SL-PH-S |
| 4005-01005-02 | MS 5-40 x 1/8 P-PH |
| 5070-06258-00 | Diode, 1N4001, 1A |
| 5647-09957-00 | μSwitch E21-50H |
| 5825-09373-00 | #4 Solder Lug-bent |
| A-11680 | Ball Trough Switch, Right |
| 01-8652 | Mounting Bracket |
| 5647-12073-08 | Submin. Switch |
| 5070-06258-00 | Diode, 1N4001, 1.0A |
| A-8645 | Switch Wire & Bracket Assy |

The diagram labels the upper assembly 5647-12073-00 MICROSWITCH, whereas the list's
right-switch row says 5647-12073-08. Both readings are preserved. The two trough contacts are
distinct from the outhole contact; a ball stack's first InitSw argument is not another trough sensor.

## PDF 73, printed 2-19: Diverter Assembly (Right Ball Gate), B-13496-1

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | B-13493 | Mounting Bracket Assy |
| 2 | AE-26-1500 | Coil Assembly |
| 3 | A-10821 | Flipper Stop Bracket Assy |
| 4 | 03-7066 | Coil Tubing |
| 5 | 01-8413 | Bracket Coil Tubing |
| 6 | 4010-01008-06 | Mach. Screw, 10-32 x 3/8 |
| 7 | 4701-00004-00 | Lockwasher, #10 Split |
| 8 | A-13494 | Diverter Shaft & Paddle |
| a) | 02-4444 | Shaft |
| b) | 03-8388 | Diverter |
| c) | 20-8716-1 | Roll Pin, 3/32 x 1/2 |
| d) | 20-8712-25 | “E”-Ring, 1/4” Shaft |
| 9 | A-13278 | Plunger Assembly |
| a) | 02-4241 | Coil Plunger |
| b) | 10-389 | Spring |
| c) | 20-8712-43 | “E”-Ring, 7/16” Shaft |
| d) | 20-8716-5 | Roll Pin, 1/8 x 7/16 |
| 10 | A-13279 | Drive Arm Assembly |
| 11 | C-13811 | Funnel Gate Assembly |

Items 8-11 and their lettered children appear under “Associated Parts”, not a separate assembly.

## PDF 73, printed 2-19: Diverter Assembly (Bowtie), C-13809

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | B-13808 | Plunger Assembly |
| 2 | B-11660 | Main Frame Sub-assembly |
| 3 | 03-8090 | Flat Cam |
| 4 | 01-8639 | Coil Support Bracket |
| 5 | A-10821 | Flipper Stop Bracket Assembly |
| 6 | 5070-06258-00 | Diode, 1N4001 |
| 7 | 10-406 | Compression Spring |
| 8 | [blank] | Extension Spring |
| 9 | 10-392 | Compression Spring |
| 10 | 5647-12073-06 | Mini Microswitch |
| 11 | AE-23-800 | Coil Assembly |
| 12 | 4701-00024-00 | Split Lock Washer #2 |
| 13 | 4700-00103-00 | Flat Washer #12 |
| 14 | 20-8712-25 | E-Retaining Ring |
| 15 | 20-7890-7 | Nylined Bearing |
| 16 | 4010-01008-06 | M.S. #10-32 P-PH |
| 17 | 4701-00004-00 | Split Lock Washer #10 |
| 18 | 4700-00021-00 | Flat Washer .203 x .437 x .032 |
| 19 | 03-8403 | Diverter Plastic |
| 20 | B-13629 | Diverter Shaft Assembly |

Items 19-20 appear under “Associated Parts (Not Shown)”. The switch inventory identifies switch 20
as p/o B-13629; the coil table identifies 07A as Ball Diverter. The mechanism has a physical
microswitch even though the VPX script supplies its state from a toggled wall.

## PDF 64, printed 2-10: Bally Left Display Board D-12706

| Description | QTY. | DESIGNATION NO. | PART NUMBER |
| --- | --- | --- | --- |
| Axial Cap., 0.01mfd. 50v. +80, -20% | 6 | B (Bypass Cap) | 5043-08980-00 |
| Axial Cap., 0.1mfd. 50v. +80, -20% | 1 | C1 | 5043-08996-00 |
| Axial Cap., 10mfd. 25v. ±20% | 1 | C2 | 5040-09343-00 |
| Zener, 1N4740, 10v | 2 | D1, D2 | 5075-09135-00 |
| Display, 16-Character A/N | 1 | DSPL1 | 5670-12308-00 |
| 9-Pin Header, Right Angle, .156 | 2 | J1, J2 | 5791-10869-09 |
| 26-Pin Header, Right Angle, .100 | 1 | J3 | 5791-10851-00 |
| 6-Pin Header, Right Angle, .156 | 1 | J7 | 5791-10869-06 |
| Resistor, 18KΩ, 1/4w, 5% | 25 | R1-R8, R21-R37 | 5010-08773-00 |
| Resistor, 100KΩ, 1/4w, 5% | 32 | R38, R40, R42, R44, R46, R48, R50, R52, R54, R55-R61, R63, R65, R67, R69, R71, R73, R75-R83, R85 | 5010-09162-00 |
| Resistor, 10KΩ, 1/2w, 5% | 9 | R39, R41, R43, R47, R53, R66, R70, R72, R84 | 5010-08981-00 |
| Resistor, 1MΩ, 1/4w, 5% | 1 | R86 | 5010-10258-00 |
| Resistor, 8.2KΩ, 1/2w, 5% | 7 | R45, R49, R51, R62, R64, R68, R74 | 5010-10927-00 |
| I.C. 4049 | 3 | U1-U3 | 5310-08975-00 |
| I.C. 4001 | [blank] | U6, U7, U10, U11 | 5310-09882-00 |
| I.C. 7180, Catode Driver | 2 | U8, U9 | 5680-08969-00 |
| I.C. 6118, Anode Driver | 2 | U12, U13 | 5680-08968-00 |
| Bally-Hi-Display PCB | 1 | [blank] | 5768-12408-00 |
| Support Display5 | [blank] | S (Support) | 03-8088-1 |

The final description prints the digit 5 adjacent to “Display”; it is not silently moved into the
quantity column. The display module's own quantity is clearly one.

## PDF 65, printed 2-11: Bally Right Display Board D-12502-1

| Description (left edge clipped) | QTY. | DESIGNATION NO. | PART NUMBER |
| --- | --- | --- | --- |
| [clipped] Cap., 0.01mfd. 50v. +80, -20% | 9 | B (Bypass Cap) | 5043-08980-00 |
| [clipped] Cap., 0.1mfd. 50v. +80, -20% | 1 | C1 | 5043-08996-00 |
| [clipped] Cap., 10mfd. 25v. ±20% | 1 | C2 | 5040-09343-00 |
| [clipped] 1N4740, 10v | 2 | D1, D2 | 5075-09135-00 |
| [clipped] 16-Character A/N | 1 | DSPL1 | 5670-12308-00 |
| [clipped] Header, Right Angle, .156 | 3 | J1, J2, J5 | 5791-10869-09 |
| [clipped] Header, Right Angle, .100 | 1 | J3 | 5791-10851-00 |
| [clipped] Header, Right Angle, .156 | 1 | J7 | 5791-10869-06 |
| [clipped] 18KΩ, 1/4w, 5% | 25 | R1-R8, R21-R37 | 5010-08773-00 |
| [clipped] 100KΩ, 1/4w, 5% | 32 | R38, R40, R42, R44, R46, R48, R50, R52, R54-R61, R63, R65, R67, R69, R71, R73, R75-R83, R85 | 5010-09162-00 |
| [clipped] 1MΩ, 1/4w, 5% | 1 | R86 | 5010-10258-00 |
| [clipped] 8.2KΩ, 1/2w, 5% | 7 | R45, R49, R51, R62, R64, R68, R74 | 5010-10927-00 |
| [clipped] 0Ω | 2 | W3, W4 | 5010-09534-00 |
| [clipped] 4049 | 3 | U1-U3 | 5310-08975-00 |
| [clipped] 4001 | 4 | U6, U7, U10, U11 | 5310-09882-00 |
| [clipped] 7180, Catode Driver | 2 | U8, U9 | 5680-08969-00 |
| [clipped] 6118, Anode Driver | 2 | U12, U13 | 5680-08968-00 |
| [clipped] Lo-Display PCB | 1 | [blank] | 5768-12378-00 |
| [clipped] Display | 5 | S (Support) | 03-8088-1 |
| [clipped] I.D. Label | 1 | [blank] | 16-8850-251 |

Physical display inventory is two sixteen-character alphanumeric modules, one per board. Four
player-score designations do not imply four display modules. PinMAME's third, 128x32 rendered
display is a virtual presentation of these segments, not a fitted DMD.

## PDF 50, printed 1-44: problem-analysis prose (paraphrase)

The manual says the machine normally uses two balls. A missing-ball report can result from
trough switches 11/12 or shooter switch 14. A ball found elsewhere is returned through the outhole.
After prolonged operation, unactuated switches can generate a report (90 balls or about 30 games);
the program can compensate for disabled switches. The operator checks Switch Levels and Switch
Edges and tests with a ball, rather than interpreting a host-injected state as physical operation.
This paragraph is a summary, not a verbatim transcription.
