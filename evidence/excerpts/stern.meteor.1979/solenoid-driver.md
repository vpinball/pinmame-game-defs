Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 24-25: the Solenoid Driver / Voltage Regulator schematic 12B-432-S113 for METEOR. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) - Solenoid Driver / Voltage Regulator schematic

Pages: PDF page 24 (left half) and PDF page 25 (right half) of the manual renders form ONE drawing, "SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC for METEOR, SOLID STATE", drawing no. 12B-432-S113, DRN. J.J., date 8-21-79 (title block on PDF page 25). PDF page 24 carries the decoder U2 and the 15 decoder-driven cells (Q1-Q14 and Q16), PDF page 25 the flipper/continuous section and the regulators.


Printed notes (verbatim): "U1, U2 & U3 = CA3081"; "*SE9302 Substitute X44E198"; "Solenoid Test Display No. is Drive Transistor (Q) Position on SDU"; "SEE LEFT SIDE OF SCHEMATIC FOR SOLENOID PINS." (PDF page 25 top, arrows to the J2 pin column). Component annotation "(x15)" beside R5 120 ohm, CR2 1N4004, C1 .002, R6 330 ohm, R57 1.2K, Q2 SE9302 (the single cell is drawn, 15 identical cells are implied).

## Input connector J4 (B) -> decoder U2 (74L154)

| J4 pin | Wire colour (printed) | Goes to U2 pin | Small weight digit printed beside U2 pin | Printed function |
| --- | --- | --- | --- | --- |
| 6 | [BLU-Y] | 23 | 1 | "PINS 3, 4, 5 & 6 MOMENTARY SOLENOID DATA" |
| 5 | [BLU-R] | 22 | 2 | same |
| 4 | [O-B] | 21 | 4 (printed 4') | same |
| 3 | [R-W] | 20 | 8 | same |
| 7 | [BRN-R] | 19 | (blank) | "PIN 7 SOLENOID BANK SELECT LOW WHEN SELECTED" |
| (none) | (blank) | 18 | (blank) | tied to ground symbol |
| (none) | (blank) | 12 | (blank) | ground (printed "12" at bottom of U2) |

R1 100K, R2 100K, R3 100K, R4 100K pull-ups to +5: R1 on J4-3 line (U2-20), R2 on J4-4 (U2-21), R3 on J4-5 (U2-22), R4 on J4-6 (U2-23). The J4-7 (U2-19) line has no pull-up drawn.

## Decoder output -> input CA3081 section -> driver transistor

Each decoder output pin goes through R57..R71 (printed R57 ... R71 in pin order below) to a CA3081 stage (U1, U3 or U4), then CR (1N4004), C (.002) and a Q (SE9302). Each Q cell has a diode CRn, a .002 capacitor Cn from base-side node to collector, a 330 ohm base resistor Rn and a 120 ohm resistor.

| U2 out pin | Resistor | CA3081 unit and pin | Drive transistor | Diode / cap in cell |
| --- | --- | --- | --- | --- |
| 1 | R57 | U1 pin 3 (out 2) | Q2 | CR2 / C1 |
| 2 | R58 | U1 pin 16 (out 1) | Q1 | CR1 / C15 |
| 3 | R59 | U1 pin 13 (out 14) | Q5 | CR5 / C2 |
| 4 | R60 | U1 pin 11 (out 12) | Q6 | CR6 / C16 |
| 5 | R61 | U1 pin 10 (out 9) | Q7 | CR7 / C3 |
| 6 | R62 | U1 pin 6 (out 4) | Q3 | CR3 / C17 |
| 7 | R63 | U1 pin 8 (out 7) | Q4 | CR4 / C4 |
| 8 | R64 | U3 pin 16 (out 1) | Q8 | CR8 / C18 |
| 9 | R65 | U3 pin 11 (out 12) | Q13 | CR13 / C5 |
| 10 | R66 | U3 pin 13 (out 14) | Q14 | CR14 / C19 |
| 11 | R67 | U3 pin 3 (out 2) | Q9 | CR9 / C6 |
| 12 | (not drawn; U2 pin 12 is ground) | - | - | - |
| 13 | R68 | U3 pin 8 (out 7) | Q10 | CR10 / C20 |
| 14 | R69 | U3 pin 10 (out 9) | Q12 | CR12 / C7 |
| 15 | R70 | U3 pin 6 (out 4) | Q11 | CR11 / C21 |
| 16 | R71 | U4 pin 8 (out 7) | Q16 | CR16 / C8 |
| 17 | (blank; pin drawn with a bare line, no resistor) | - | - | - |

U2 pin numbering printed 1-11 then 13-17 (no pin 12 output). (74L154: pin n -> Y(n-1) for n<=11, 13-17 -> Y11-Y15.)

## Driver transistor -> load connector, pin, wire colour, load name

Wire colours are those printed in the J2/J5 legends (left column of PDF page 24 for J2, right of the J5 column on PDF page 24/PDF page 25). Transistor collector routing was traced on the 300 dpi renders; where one collector reaches more than one pin that is stated.

| Driver | Collector goes to (connector-pin) | Wire colour (printed) | Load name (printed) | Notes |
| --- | --- | --- | --- | --- |
| Q1 | J2-9; same net also reaches J1-2 | (PUR-W) | CENTER THUMPER | J2 legend PDF page 24 lower left |
| Q2 | J2-4; same net also reaches J1-3 | (BRN) | LEFT SLING-SHOT | |
| Q3 | J2-5; same net also reaches J3-4 | (B-Y) | KNOCKER | |
| Q4 | J1-5 (drawn on J1, P) | (BRN-Y) | LEFT BOTTOM DROP TARGET | label printed beside J1 on PDF page 25 |
| Q5 | J2-10 | (G-R) | LEFT TOP DROP TARGET | |
| Q6 | J2-11 | (GREY) | "M" TARGET | |
| Q7 | J2-12 | (Y-B) | M"E"T TARGET (printed `M"E"T TARGET` in the J2 legend) | the playfield coil sheet prints (Y-W) |
| Q8 | J5-10 | (B-Y) | "T" TARGET | |
| Q9 | J5-9 | (O-R) | MET"E" TARGET | |
| Q10 | J5-15 | (B-BLU) | "O" TARGET | |
| Q11 | J5-14 | (Y-BLU) | "R" TARGET | |
| Q12 | J5-13 | (O-W) | METEOR DROP TARGET | |
| Q13 | J5-12 | (O-B) | RT. DROP TARGET | |
| Q14 | J5-11 | (-B-) struck through / illegible (see uncertain) | RT. SLING-SHOT | |
| Q15 | relay coil (see continuous section) | - | FLIPPER ENABLE RELAY | driven by PB6 |
| Q16 | J5-8; same net also reaches J2-6 and J3-7 | (R-B) | OUT-HOLE | |
| Q17 | J5-7 | N/U | N/U | PB4 |
| Q18 | J2-15, also J5-3 and J3-9 | N/U | N/U | PB7 |
| Q19 | J2-8 | [Y-W] | COIN LOCK-OUT (net labelled "COIN LD.") | PB5 |

Driver cells Q1..Q14 and Q16 are the decoder-driven momentary cells. There is NO Q15 on the decoder; the label Q15 belongs to the flipper-disable stage.

## Continuous-solenoid / relay section (PDF page 25 upper)

PIA port B bits drive four more stages through U4 (CA3081). Each stage: PBn line with a 3.9K pull-up (R37, R40, R43, R46) to +5, a 120 ohm (R38, R41, R44, R47 - note R47 is printed 3.9K ohm), CR 1N4004 (CR15, CR17, CR18, CR19), 330 ohm (R39, R42, R45, R48), .002 cap (C11, C12, C13, C14) and an SE9302 transistor.

| J4 pin | Wire colour | PB bit label | U4 pin | Driver | Load |
| --- | --- | --- | --- | --- | --- |
| 8 | [BLU-W] | "FLIPPER DISABLE" PB6 | 3 (out 2) | Q15 SE9302 | FLIPPER ENABLE RELAY coil (relay terminals 8 and 7) |
| 11 | [Y-W] | PB4 | 10 (out 9) | Q17 SE9302 | J5-7 N/U |
| 10 | [Y-R] | PB7 | 11 (out 12) | Q18 SE9302 | J2-15 N/U (same net J5-3, J3-9 N/U) |
| 9 | [BLU-O] (printed "[BLU-O7"/"BLU-07", see uncertain) | PB5 | 13 (out 14) | Q19 SE9302 | J2-8 COIN LOCK-OUT [Y-W], line labelled "COIN LD." |

### Flipper wiring as drawn (PDF page 25 top right)
- Flipper enable relay: coil between terminal 8 (Q15 collector, dot) and terminal 7 (to the "43 VDC" line); CR20 1N4004 across the coil. Relay terminal 7/43VDC line also runs to J3-5 "TO A2J3-8 [Y-W]" (J3 labelled B in the drawing).
- Relay contacts (dashed mechanical link from coil to contact armature at terminal 8): terminal 4 / terminal 6 "LEFT FLIPPER SW." and terminal 3 / terminal 5 "RIGHT FLIPPER SW." - the left contact pair: terminal 4 goes to J1-8 "TO LEFT FLIPPER COIL [G] (16)"; terminal 3 goes to J1-9 "TO RIGHT FLIPPER COIL [O] (16)". Terminal 6 -> J2-2 "TO LEFT [BLU] FLIPPER BUTTON"; terminal 5 -> J2-1 "TO RIGHT [R] FLIPPER BUTTON" (J2 shown with label C).
- Fuse: none drawn on this sheet. E.O.S. switches: none drawn on this sheet.
- "(16)" printed after each flipper coil lead is the wire gauge/ID as printed; not interpreted.
- J5-7 "N/U" (box), J5-3 "N/U", J2-15 "N/U", J3-9 "N/U" are boxes/pins drawn with "N/U" text.
- Lock-out: "COIN LOCK-OUT [Y-W]" at J2-8. Solenoid ground: "+43V SOLENOID GND" line goes to J3-24 [W-O] and J3-23 [R-Y].

### Regulator section (PDF page 25 lower)
- +5V regulator: 25A-LM-323 "+5V REG" (pin 2 output, pin 3 (CASE)), R49 100 ohm 1/2 W, R50 4.7 ohm, C25 .1, C24 2uf 20WV, C23 11,700 uf 20 WV, C22 .01 uf; TP1 +5 VDC, TP5 11.9 VDC, TP6 R36 120 ohm, TP7 R72 1.2K, TP3. "+5 V BUS LINE" arrow.
- Outputs on J3 (B): 25 -> [BRN-W] to A3J3-25? (a bracketed [BRN-W] dashed line between J3-25 and J3-13 labelled "A3J3-25"), 13, 14 "GREY-R TO MPU [W-G]", 15, 16 "A5J4-3 LAMP DRIVER DISPLAYS A1J1-18 [B-G] [G-W]" (as printed "ASJ4- 3 [B-G] LAMP DRIVER DISPLAYS A1J1-18 [G-W]"), 17, 18-22 "GREY-G TO MPU (B-R)", "DISPLAYS A1J1-11 [BRN]", "TRANSFORMER A2J3-16 [B-BLU]" with "[W-BLU]". J2 (C) pin 7 [Y-R]. J3 (B) pin 8 [R].
- High voltage regulator: TP4 +230 V (from J3-6 "FROM A2J3-4 BRIDGE RECTIFIER [GREY-BLU]", J3-3 "FROM A2J3-18 TRANSFORMER BRIDGE GND. [W]"), C26 160 uf 350 WV, R35 100K 1W, Q21 2N3584 with CR21 1N4004, Q22 2N3440, Q23 2N3440, R51 22K 1/2 W, R52 390 ohm, R58 8.2K, RT1 25K "+185 Vdc ADJUST", R56 82K 1/2 W, R55 1.2K, C28 .01 (500V?), VR1 1N5275A, "+193 VDC" node, "+140 VDC" node, TP2 "+185 VDC" output to J3-8 [R].
- J3 (B) pins 11 "TO MPU [R-G]", 12 "UNREGULATED FROM A2J3-8 [O]", 10 "TO TRANSFORMER (BRIDGE & GND) A2J3-17 [W-BRN]"; C23 11,700 uf across.

## Uncertain readings
- J5-11 RT. SLING-SHOT wire colour printed "(-B-)" with a strike-through over it, text overlaps the next legend line ("MET"E" TARGET"). Best reading: (B) with an overstrike, possibly a hand correction. The playfield sheet (PDF page 36) prints A3J5-11 (O-W).
- J4-9 colour printed "[BLU-O7" - best reading [BLU-O] (blue-orange).
- which collector nets reach J1-2, J1-3, J2-6, J3-4, J3-7 (these pins have no legend text). Best reading from line tracing: J1-2 = Q1 net, J1-3 = Q2 net, J3-4 = Q3 net (with J2-5), J2-6 and J3-7 = Q16 net (with J5-8). These are not printed with labels.
- PDF page 25 regulator/J3-C pin annotations: handwriting partly cut off at the page edge; the "[BRN-W]" bracketed text beside J3-25/13.
- U2 output 17: no resistor drawn - treated as unused/blank.
- small digits beside U2 input pins (1, 2, 4', 8) are read as binary weights.
