---
source: pinball_robowar_gottlieb_instruction_manual_1_of_2.pdf
source_sha256: c887ba2af6229371753d6a062a7a94eb5fd51cafdaed4c6ae49fabe1a5af2fef
locator: PDF pages 30-32; printed folio 26-28; "X. WIRING AND SCHEMATIC DIAGRAMS, PARTS LISTS" - "DRIVER BOARD (A3) COMPONENT LOCATION", "DRIVER BOARD (A3) PARTS LIST" (folio 26) and the DRIVER BOARD (A3) schematic across folios 27 and 28 (Premier Technology title block "DRIVER BOARD (A3)", drawing E-20915, dated 12-12-80)
method: Visual transcription from the 600 dpi native page render, checked against Windows OCR
transcribed_by: curator transcription
reviewed: false
status: folio 28 (latches Z10-Z12 with their lamp outputs L36-L51, the Z13 sound outputs and every solenoid driver row) was checked against the rendered page; folios 26 and 27 remain a draft; uncertain readings are marked
---

# Driver Board (A3)

The schematic is one drawing split across two pages: folio 27 carries the left and middle part (latches Z1-Z9) and folio 28 carries the right part (latches Z10-Z12, hex inverter Z13 and the solenoid drivers). The page seam cuts off the right edge of folio 27 and the left edge of folio 28; the cut labels are noted below.

## Component location (folio 26)

Printed board edge connectors: J1 (top edge, long), J2 (bottom right), J3 (bottom, long), J4 (bottom left), J5 and J6 (left edge). Components located as printed: Q1-Q4 and Q5-Q12 at the right edge in two columns (Q1, Q2, Q3, Q4 on a vertical strip; Q5-Q12 as round-can outlines), Q13-Q32 in the centre columns, Q33-Q44 lower left centre (round-can outlines for Q33-Q44 and Q37-Q40), Q45-Q52 in two vertical stacks (Q45, Q49, Q46, Q50 and Q48, Q52, Q47, Q51), Q53 (TO-220 style, top left, with CR1), Q54, Q55, Q56 (top left strip), Q57, Q61, Q63 (small strips), Q58, Q62, Q64 (large metal-can, mounted with screws), Q59, Q60 (TO-220 style), ICs Z1-Z12 in two rows across the top and middle, Z13 top left. Capacitors C1-C19, resistors R1-R61 and diodes CR1-CR6 are located as labelled. The letters "C B E" are printed beside Q54 (lead-order marking for the strip transistors).

## Driver Board (A3) Parts List (folio 26)

| REFERENCE | DESCRIPTION | PART NUMBER |
| --- | --- | --- |
| **[blank]** | DRIVER BOARD | MA-295 |
| C1 | Capacitor, 10 mfd, 10V Tantalum | XO-209 |
| C2-C19 | Capacitor, 01 mfd, 50V Ceramic | XO-229 |
| CR1-CR6 | Diode-Silicon 1N4148 | XO-261 |
| R1-R53, R61, R55, R56, R58, R59 | Resistor, 1.0K ohm, 5%, 1/4W | XO-5 |
| R54, R57, R60 | Resistor, 91 ohm, 5%, 1W | XO-158 |
| Q1-Q4, Q13-Q32, Q45-Q52, Q54-Q57, Q61, Q63 | Transistor, NPN, Darlington MPS-U45 | XO-306 |
| Q5-Q12, Q33-Q44 | Transistor, NPN, Darlington MPS-A13 | XO-304 |
| Q53, Q59, Q60 | Transistor, NPN, Darlington 2N6043 | XO-303 |
| Q58, Q62, Q64 | Transistor, NPN, 2N3055 | XO-301 |
| Z1-Z12 | IC-Quad "D" Latch Flip Flop SN74175N | XO-410 |
| Z13 | IC-Hex Inverter SN7404N | XO-402 |
| **[blank]** | Insulator-Thermalloy 43-03-4 | XO-512 |

Printed as "R1-R53, R61," with a continuation line "R55, R56, R58, R59" (the wrap line lists R55, R56, R58, R59 again after the range R1-R53, as printed). The description cells for R54/R57/R60 read "91 ohm" (the decimal point is not distinct in the scan; the schematic prints "9.1, 5%, 1W" on R54, R57 and R60).

Printed note on folio 26:

1. JUMPER WIRES REPLACED DIODES CR2, CR3 AND CR4 FOR SYSTEM 80A AND 80B GAMES.
2. TRANSISTOR TYPES MPS-U45 AND NSD-U45 ARE INTERCHANGEABLE.

(Folio 28 prints the same notes as note 4 and note 5, with "NDS-U45" in note 5.)

## Schematic notes (folio 28)

NOTE: UNLESS OTHERWISE INDICATED;
1. RESISTORS ARE 1000 OHM, +/-5%, 1/4W.
2. CAPACITORS ARE .01UF, +/-20%, 50V.
3. INTEGRATED CIRCUITS ARE SN74175N.
4. JUMPER WIRES REPLACED DIODES CR2, CR3 AND CR4 FOR SYSTEM 80A AND 80B GAMES.
5. TRANSISTOR TYPES MPS-U45 AND NDS-U45 ARE INTERCHANGEABLE.

## Latch inputs (as drawn)

Every SN74175N latch Z1-Z12 has D1 (pin 4), D2 (pin 5), D3 (pin 12), D4 (pin 13) wired to the four common data lines coming in from the left edge of the schematic (labels cut at the seam: "D1", "D2", "D3", "D4" and a line labelled ending "OL" at the top). The latches' outputs Q1-Q4 are pins 2, 7, 10, 15 (each through a 1K series resistor to the base of one transistor). Pin 16 is +5V; pin 1 (CL) is tied to +5V, with a decoupling capacitor on the +5V pin as drawn; pin 8 is ground. The clock (CK) pin 9 of each latch is fed from the A3J1 strobe pins below, each with a capacitor to ground:

| Latch | CK (pin 9) from | Capacitor at CK |
| --- | --- | --- |
| Z1 | strobe line labelled "S1" (label cut at the seam; A3J1 pin C on folio 26's right strip, label begins "DS") | C3 |
| Z2 | strobe line labelled "S2" (cut), A3J1 pin 3 | C4 |
| Z3 | strobe line labelled "S3" (cut), A3J1 pin E | C5 |
| Z4 | strobe line labelled "S4" (cut), A3J1 pin D | C7 |
| Z5 | strobe line labelled "S5" (cut), A3J1 pin H | C9 |
| Z6 | DS6, A3J1 pin F | C10 |
| Z7 | DS7, A3J1 pin K | C11 |
| Z8 | DS8, A3J1 pin J | C13 |
| Z9 | DS9, A3J1 pin M | C15 |
| Z10 | DS10, A3J1 pin L | capacitor drawn, designator not printed (C16 not shown at this position) |
| Z11 | DS11, A3J1 pin N | C17 |
| Z12 | DS12, A3J1 pin P | C19 |

The data lines on A3J1 (cut by the seam on folio 26/27, shown at the right edge of folio 26 as pins 7, 6, 4, 5 with labels beginning "LD") are: pin 7, pin 6, pin 4, pin 5. The strip fragment on folio 26 reads, top to bottom: 7 "LD...", 6 "LD...", 4 "LD...", 5 "LD...", C "DS...", 3 "DS...", E "DS...", D "DS...", H "DS...". The mapping of pins 7/6/4/5 to D1-D4 and of the cut labels to DS1-DS5 is by position and is not fully legible (see Uncertain readings). Capacitors C2, C6, C8, C12, C14, C18 appear as decoupling capacitors beside the +5V/CL pins of Z1, Z4, Z5, Z8, Z10, Z12 (positions as drawn; C1 is the 10UF 10V on the +5V source).

## A3J1 (from A1J4 control board) pins as drawn

Folio 27: F (DS6), K (DS7), J (DS8), M (DS9), 2 and B (+5V DC (SOURCE) with C1 10UF 10V), 1 and A (ground), W, 19 (index key pins). Folio 28: L (DS10), N (DS11), P (DS12); and the solenoid/sound input column: B-bar (overline), A-bar (overline), Z, Y, 21, 24, 23, 22, X, T, S, R, U.

## Lamp driver outputs

Each lamp driver is one transistor (collector to the output pin, emitter to the common line that ends at a LAMP GND pin). Output pins are on A3J2, A3J3, A3J4 and A3J5 as drawn (the same connector designator A3J3 appears for several separate pin columns; each column is listed with its pins).

| Lamp driver | Latch / output pin | Resistor | Transistor | Transistor type | Output connector pin | Label printed beside pin |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Z1 Q1 (pin 2) | R1 | Q1 | MPS-U45 | A3J3 pin A (printed with overline) | L0 GAME OVER RELAY (PLAYFIELD) |
| L1 | Z1 Q2 (pin 7) | R2 | Q2 | MPS-U45 | A3J3 pin B (printed with overline) | L1 TILT RELAY (PLAYFIELD) |
| L2 | Z1 Q3 (pin 10) | R3 | Q3 | MPS-U45 | A3J5 pin 2 | L2 |
| L3 | Z1 Q4 (pin 15) | R4 | Q4 | MPS-U45 | A3J3 pin C (printed with overline) and also A3J2 pin 1 (the collector line of Q4 is drawn to both) | L3 SHOOT AGAIN (PLAYFIELD) at A3J3-C; "L3" at A3J2-1 |
| L4 | Z2 Q1 (pin 2) | R5 | Q5 | MPS-A13 | A3J2 pin 2 | L4 SOUND 16 |
| L5 | Z2 Q2 (pin 7) | R6 | Q6 | MPS-A13 | A3J2 pin 3 | L5 |
| L6 | Z2 Q3 (pin 10) | R7 | Q7 | MPS-A13 | A3J2 pin 5 | L6 |
| L7 | Z2 Q4 (pin 15) | R8 | Q8 | MPS-A13 | A3J2 pin 4 | L7 |
| L8 | Z3 Q1 (pin 2) | R9 | Q9 | MPS-A13 | A3J2 pin 10 | L8 |
| L9 | Z3 Q2 (pin 7) | R10 | Q10 | MPS-A13 | A3J2 pin 9 | L9 |
| L10 | Z3 Q3 (pin 10) | R11 | Q11 | MPS-A13 | A3J2 pin 7 | L10 |
| L11 | Z3 Q4 (pin 15) | R12 | Q12 | MPS-A13 | A3J2 pin 8 | L11 |
| (ground) | common emitter line of Q1-Q12 | | | | A3J2 pin 6 | LAMP GND. |
| L12 | Z4 Q1 (pin 2) | R13 | Q13 | MPS-U45 | A3J3 pin 25 | L12 |
| L13 | Z4 Q2 (pin 7) | R14 | Q14 | MPS-U45 | A3J3 pin 24 | L13 |
| L14 | Z4 Q3 (pin 10) | R15 | Q15 | MPS-U45 | A3J3 pin 22 | L14 |
| L15 | Z4 Q4 (pin 15) | R16 | Q16 | MPS-U45 | A3J3 pin 23 | L15 |
| L16 | Z5 Q1 (pin 2) | R17 | Q17 | MPS-U45 | A3J3 pin 13 | L16 |
| L17 | Z5 Q2 (pin 7) | R18 | Q18 | MPS-U45 | A3J3 pin 14 | L17 |
| L18 | Z5 Q3 (pin 10) | R19 | Q19 | MPS-U45 | A3J3 pin 16 | L18 |
| L19 | Z5 Q4 (pin 15) | R20 | Q20 | MPS-U45 | A3J3 pin 15 | L19 |
| (ground) | common emitter line of Q13-Q20 | | | | A3J3 pin Z | LAMP GND. |
| L20 | Z6 Q1 (pin 2) | R21 | Q21 | MPS-U45 | A3J3 pin 21 | ".20" (label cut at the seam, reads L20) |
| L21 | Z6 Q2 (pin 7) | R22 | Q22 | MPS-U45 | A3J3 pin 20 | ".21" (cut) |
| L22 | Z6 Q3 (pin 10) | R23 | Q23 | MPS-U45 | A3J3 pin 18 | ".22" (cut) |
| L23 | Z6 Q4 (pin 15) | R24 | Q24 | MPS-U45 | A3J3 pin 19 | ".23" (cut) |
| L24 | Z7 Q1 (pin 2) | R25 | Q25 | MPS-U45 | A3J3 pin 9 | ".24" (cut) |
| L25 | Z7 Q2 (pin 7) | R26 | Q26 | MPS-U45 | A3J3 pin 10 | ".25" (cut) |
| L26 | Z7 Q3 (pin 10) | R27 | Q27 | MPS-U45 | A3J3 pin 12 | ".26" (cut) |
| L27 | Z7 Q4 (pin 15) | R28 | Q28 | MPS-U45 | A3J3 pin 11 | ".27" (cut) |
| (ground) | common emitter line of Q21-Q28 | | | | A3J3 pin 17 | "AMP GND." (cut; reads LAMP GND.) |
| L28 | Z8 Q1 (pin 2) | R29 | Q29 | MPS-U45 | A3J3 pin Y | ".28" (cut) |
| L29 | Z8 Q2 (pin 7) | R30 | Q30 | MPS-U45 | A3J3 pin X | ".29" (cut) |
| L30 | Z8 Q3 (pin 10) | R31 | Q31 | MPS-U45 | A3J3 pin V | ".30" (cut) |
| L31 | Z8 Q4 (pin 15) | R32 | Q32 | MPS-U45 | A3J3 pin W | ".31" (cut) |
| L32 | Z9 Q1 (pin 2) | R33 | Q33 | MPS-A13 | A3J3 pin 5 | ".32" (cut) |
| L33 | Z9 Q2 (pin 7) | R34 | Q34 | MPS-A13 | A3J3 pin 6 | ".33" (cut) |
| L34 | Z9 Q3 (pin 10) | R35 | Q35 | MPS-A13 | A3J3 pin K | ".34" (cut) |
| L35 | Z9 Q4 (pin 15) | R36 | Q36 | MPS-A13 | A3J3 pin 7 | ".35" (cut) |
| (ground) | common emitter line of Q29-Q36 | | | | A3J3 pin U | "AMP GND." (cut; reads LAMP GND.) |
| L36 | Z10 Q1 (pin 2) | R37 | Q37 | MPS-A13 | A3J4 pin 1 | L36 |
| L37 | Z10 Q2 (pin 7) | R38 | Q38 | MPS-A13 | A3J4 pin 2 | L37 |
| L38 | Z10 Q3 (pin 10) | R39 | Q39 | MPS-A13 | A3J4 pin 4 | L38 |
| L39 | Z10 Q4 (pin 15) | R40 | Q40 | MPS-A13 | A3J4 pin 3 | L39 |
| (ground) | common emitter line of Q37-Q40 | | | | A3J4 pin 5 | LAMP GND. |
| L40 | Z11 Q1 (pin 2) | R41 | Q41 | MPS-A13 | A3J3 pin 4 | L40 (printed "1.40" in the scan) |
| L41 | Z11 Q2 (pin 7) | R42 | Q42 | MPS-A13 | A3J3 pin 3 | L41 (printed "1.41") |
| L42 | Z11 Q3 (pin 10) | R43 | Q43 | MPS-A13 | A3J3 pin T | L42 |
| L43 | Z11 Q4 (pin 15) | R44 | Q44 | MPS-A13 | A3J3 pin 2 | L43 |
| (ground) | common emitter line of Q41-Q44 | | | | A3J3 pin S | LAMP GND. |
| L44 | Z12 Q1 (pin 2) | R45 | Q45 | MPS-U45 | A3J3 pin D | L44 |
| L45 | Z12 Q2 (pin 7) | R46 | Q46 | MPS-U45 | A3J3 pin F | L45 |
| L46 | Z12 Q3 (pin 10) | R47 | Q47 | MPS-U45 | A3J3 pin P | L46 |
| L47 | Z12 Q4 (pin 15) | R48 | Q48 | MPS-U45 | A3J3 pin M | L47 |
| L48 | Z12 Q1-bar (pin 3) | R49 | Q49 | MPS-U45 | A3J3 pin E | L48 |
| L49 | Z12 Q2-bar (pin 6) | R50 | Q50 | MPS-U45 | A3J3 pin H | L49 |
| L50 | Z12 Q3-bar (pin 11) | R51 | Q51 | MPS-U45 | A3J3 pin R | L50 |
| L51 | Z12 Q4-bar (pin 14) | R52 | Q52 | MPS-U45 | A3J3 pin N | L51 |
| (ground) | common emitter line of Q45-Q52 | | | | A3J3 pin C | LAMP GND. |
| (supply) | | | | | A3J3 pin B | +5V DC (arrow out) |
| (ground) | | | | | A3J3 pins 1 and A | ground symbol (tied together, not labelled) |

### What is drawn for L48-L51 and Q49-Q52

Z12 is drawn tall with its D1-D4 inputs (pins 4, 5, 12, 13) at the top and, separately at the bottom, four extra outputs labelled Q1-bar (pin 3), Q2-bar (pin 6), Q3-bar (pin 11), Q4-bar (pin 14) with resistors R49, R50, R51, R52 to transistors Q49, Q50, Q51, Q52 (all MPS-U45). Z12's ordinary Q1-Q4 outputs (pins 2, 7, 10, 15) drive Q45-Q48 (L44-L47). The Q-bar outputs drive Q49-Q52, whose collectors go to A3J3 pins E, H, R, N, labelled L48, L49, L50, L51 respectively. Q49-Q52 therefore all have an output connector pin and a printed label; none is drawn unlabelled or without a pin. L48-L51 share the Z12 clock line DS12 (CK pin 9) and the D1-D4 data lines with L44-L47. The component-location drawing places Q49-Q52 in the two vertical stacks beside Q45-Q48.

### Lamp drivers with a transistor but no output pin / unlabelled

On this schematic every lamp transistor Q1-Q52 is drawn with a connector pin. The only items without a transistor of their own are the LAMP GND pins and the extra A3J2 pin 1, which carries the same net as the L3 transistor Q4's collector (A3J3 pin C-bar). No drawn lamp transistor lacks a pin. The printed label beside pin A3J2-1 is "L3", the same label as at A3J3 pin C-bar.

## Sound outputs (Z13 hex inverter SN7404N, as drawn)

A3J1 pins B-bar, A-bar, Z, Y (each with its line drawn into Z13 input pins 1, 3, 5, 9) feed four inverters of Z13 (Z13 pin 14 +5V, pin 7 ground). The inverter outputs are pins 2, 4, 6, 8, which go to A3J5:

| Z13 input (from A3J1) | Z13 output pin | A3J5 pin | Label |
| --- | --- | --- | --- |
| pin 1 (A3J1 B-bar) | 2 | 6 | SOUND 1 |
| pin 3 (A3J1 A-bar) | 4 | 5 | SOUND 2 |
| pin 5 (A3J1 Z) | 6 | 1 | SOUND 4 |
| pin 9 (A3J1 Y) | 8 | 7 | SOUND 8 |

## Solenoid drivers

| Solenoid | A3J1 input pin | Input path | Driver transistors | Output connector pin | Solenoid-ground pin |
| --- | --- | --- | --- | --- | --- |
| SOLENOID 8 | 21 | CR1 (1N4148) | Q53 (2N6043) | A3J5 pin 8 | A3J5 pin 3 (SOLENOID GND.) |
| SOLENOID 3 | 24 | jumper wire drawn in place of a diode (SEE NOTE 4) | Q54 (MPS-U45) | A3J6 pin 3 | A3J6 pin 4 (SOLENOID GND.) |
| SOLENOID 4 | 23 | jumper wire (SEE NOTE 4) | Q55 (MPS-U45) | A3J6 pin 2 | A3J6 pin 4 |
| SOLENOID 7 | 22 | jumper wire (SEE NOTE 4) | Q56 (MPS-U45) | A3J6 pin 1 | A3J6 pin 4 |
| SOLENOID 2 | X | R53 (1K) | Q57 (MPS-U45, collector load R54 9.1 5% 1W to +5V, R55 to ground) driving Q58 (2N3055) | A3J4 pin 13 | A3J4 pin 10 (SOLENOID GND.) |
| SOLENOID 9 | T | CR5 (1N4148) | Q59 (2N6043) | A3J4 pin 8 | A3J4 pin 9 (SOLENOID GND.) |
| SOLENOID 1 | S | CR6 (1N4148) | Q60 (2N6043) | A3J4 pin 7 | A3J4 pin 9 (shared with Q59) |
| SOLENOID 5 | R | R56 (1K) | Q61 (MPS-U45, R57 9.1 5% 1W to +5V, R58 to ground) driving Q62 (2N3055) | A3J4 pin 6 | A3J4 pin 14 (SOLENOID GND.) |
| SOLENOID 6 | U | R59 (1K) | Q63 (MPS-U45, R60 9.1 5% 1W to +5V, R61 to ground) driving Q64 (2N3055) | A3J4 pin 12 | A3J4 pin 11 (SOLENOID GND.) |

A3J4 pin 15 is drawn tied to ground (ground symbol). The three jumper wires on A3J1 24/23/22 are drawn as loops and labelled "SEE NOTE 4" (note 4: jumper wires replaced diodes CR2, CR3 and CR4 for System 80A and 80B games). The Q59 / Q60 emitter returns meet at A3J4 pin 9 as one drawn line.

## Uncertain readings

- The strobe/data labels at the left seam of folio 27 are cut ("D1", "D2", "D3", "D4", "S1".."S5", and a line ending "OL"); the A3J1 pin letters for Z1-Z5 are read from the right strip of folio 26 (7, 6, 4, 5, C, 3, E, D, H) whose printed labels begin "LD" and "DS" but are cut off at the page edge. The assignment of pins 7/6/4/5 to D1-D4 and C/3/E/D/H to the strobes S1-S5 is by vertical position and not fully legible (?).
- Labels L20-L35 and the "LAMP GND." at pins 17 and U are read from the right edge of folio 27 and left edge of folio 28 where the page seam cuts the first character; they read ".20" ... ".35" and "AMP GND." (?). They follow the unbroken sequence from L19 and L36.
- The overlines on A3J3 pins A, B, C and on A3J1 B and A (folio 28) are printed as an overbar over the letter; whether the overbar is part of the pin designator is not stated.
- Folio 28 labels "L40" and "L41" print as "1.40" and "1.41" in the scan (?).
- The resistor value R54/R57/R60: the parts list reads "91 ohm" and the schematic "9.1"; the printed decimal point is not distinct on the parts list (?).
- The capacitor designator at Z10's CK is not printed (a capacitor symbol is drawn without a designator; C16 is located elsewhere on the component-location drawing) (?).
- The Q4/L3 collector also appears wired to A3J2 pin 1; the printed junction dot is at the Q4 collector line, the wire passes down to A3J2-1.
