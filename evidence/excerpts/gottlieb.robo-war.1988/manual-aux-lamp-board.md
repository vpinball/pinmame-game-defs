---
source: pinball_robowar_gottlieb_instruction_manual_2_of_2.pdf
source_sha256: f96ce0b20bebce7fdd085809e00c2eef6cc044957ec3942353f48fd053debb83
locator: PDF page 13; printed folio 43; "AUXILIARY LAMP DRIVER BOARD (A11) COMPONENT LOCATION", "AUXILIARY LAMP DRIVER BOARD (A11) PARTS LIST" and schematic title block "AUX. LAMP DRIVER BOARD (1A11)", Premier Technology, drawing E-21594, dated 8AUG86
method: Visual transcription from the 600 dpi native page render, checked against Windows OCR
transcribed_by: curator transcription
reviewed: true
status: curator transcription checked against the rendered page, with the 1A11P1 and U3 regions compared on a full-resolution crop; uncertain readings are marked
---

# Auxiliary Lamp Driver Board (A11)

## Schematic notes (as printed)

NOTE:
1. ALL TRANSISTORS ARE 2N6043.
2. ALL RESISTORS ARE +/-5%, 1/4W.

## Input connector 1A11P1

| Pin | As drawn |
| --- | --- |
| 1 | "( NOT USED )" - a line from this pin runs right and down to the junction of R1 (3K to +5V) and U1 pin 1 |
| 4 | +5V DC (with C4 47UF 10V to ground; also supplies the +5V rail) |
| 2 | ground |

Pin 3 is not drawn on the schematic (only pins 1, 4, 2 are shown).

## Sequencing logic as drawn

- U5 LM555M timer: pins 4 and 8 to +5V (C2 .01UF to ground at the +5V), pin 1 ground; R12 3K from +5V to pin 7; R13 680K from pin 7 to the junction of pins 2 and 6; C1 0.1UF from that junction to ground. Output pin 3 goes to U1 pin 2.
- U1 7400N quad NAND (pin 14 +5V, pin 7 ground): pin 1 from the R1 3K pull-up / 1A11P1 pin 1 node, pin 2 from U5 pin 3; output pin 3 goes to U3 pin 14. The other three gates (inputs 4/5, 9/10, 12/13; outputs 6, 8, 11) are drawn with no connections to other circuitry.
- U3 SN7490N decade counter: pin 14 from U1 pin 3; pin 5 +5V (C3 .01UF to ground); pins 2, 3, 6, 7 tied to ground; pin 10 drawn beside the ground bracket. Output pin 12 is wired to pin 1 and to U4 pin 15; pin 9 goes to U4 pin 14; pin 8 goes to U4 pin 13; pin 11 goes to U4 pin 12.
- U4 SN7442N BCD-to-decimal decoder: pin 16 +5V, pin 8 ground; inputs 15, 14, 13, 12 from U3 as above. Outputs drawn: pins 1, 2, 3, 4, 5 go to U2 inverter inputs 1, 3, 5, 9, 11; pins 6, 7, 9, 10, 11 go to U6 inverter inputs 1, 3, 5, 9, 11.
- U2 and U6 SN7405N hex inverters (pin 14 +5V, pin 7 ground each): the sixth-pair inverter (input 13, output 12) is drawn unused on each.

## Output positions (1A11P2, 10 positions)

Each inverter output (pins 2, 4, 6, 8, 10) has a 620 pull-up resistor to +5V and drives the base of a 2N6043 transistor; each transistor's emitter is grounded and its collector goes to the connector pin.

| Output (1A11P2 pin) | Transistor | Base resistor / pull-up | Driven by |
| --- | --- | --- | --- |
| 1 | Q1 | R2 620 | U2 pin 2 (input pin 1, from U4 pin 1) |
| 2 | Q2 | R3 620 | U2 pin 4 (input pin 3, from U4 pin 2) |
| 3 | Q3 | R4 620 | U2 pin 6 (input pin 5, from U4 pin 3) |
| 4 | Q4 | R5 620 | U2 pin 8 (input pin 9, from U4 pin 4) |
| 5 | Q5 | R6 620 | U2 pin 10 (input pin 11, from U4 pin 5) |
| 6 | Q6 | R7 620 | U6 pin 2 (input pin 1, from U4 pin 6) |
| 7 | Q7 | R8 620 | U6 pin 4 (input pin 3, from U4 pin 7) |
| 8 | Q8 | R9 620 | U6 pin 6 (input pin 5, from U4 pin 9) |
| 9 | Q9 | R10 620 | U6 pin 8 (input pin 9, from U4 pin 10) |
| 10 | Q10 | R11 620 | U6 pin 10 (input pin 11, from U4 pin 11) |

No lamp names or lamp numbers are printed on this page. Supply/relay inputs: only 1A11P1 pin 4 (+5V DC) and pin 2 (ground); no other supply or relay input is drawn.

## Component location (as printed)

Board outline with R1, U1, U2 across the top row, U3, U4 below, U5, U6 lower row, C1, C2, C3, C4, R13, R12; connector A11P1 (4 pins, pin 1 marked) on the left edge; resistors R2-R11 in a column beside transistors Q1-Q10 (drawn as rounded outlines) with connector A11P2 (10 positions, pin 1 marked at the top) on the right edge.

## AUXILIARY LAMP DRIVER BOARD (A11) PARTS LIST

| REFERENCE | DESCRIPTION | PART NUMBER |
| --- | --- | --- |
| **[blank]** | Auxiliary Lamp Driver Assembly | MA-866 |
| C1 | Capacitor, .1 MFD, 100V Ceramic Radial Lead | XO-626 |
| C2-C3 | Capacitor, .01 MFD, 100V Radial Lead | XO-202 |
| C4 | Capacitor, 47 MFD, 10V Electrolytic Radial Lead | XO-227 |
| Q1-Q10 | Transistor, 2N6043 NPN Darlington | XO-303 |
| R1, R12 | Resistor, 3K Ohm, 5%, 1/4 W | XO-23 |
| R2-R11 | Resistor, 620K Ohm, 5%, 1/4 W | XO-4 |
| R13 | Resistor, 680K Ohm, 5%, 1/4 W | XO-669 |
| U1 | I.C. 2-Input NAND, 7400 | XO-420 |
| U2, U6 | I.C. Inverter, 7405 | XO-403 |
| U3 | I.C. Decade Counter, 7490 | XO-425 |
| U4 | I.C. Decoder, 7442 | XO-426 |
| U5 | I.C. Timer, NE555 | XO-631 |
| P2 | 10 Position Connector | XO-531 |
| P1 | 4 Position Connector | XO-532 |

## Uncertain readings

- R2-R11 are "620" on the schematic and "620K Ohm" on the parts list (as printed); the discrepancy is recorded, not resolved.
- U5 is "LM555M" on the schematic and "NE555" on the parts list.
- The U3 pin 10 connection: the schematic joins pins 2, 3, 6 and 7 to the ground symbol and prints pin 10 beside them with no line drawn to it.
- U3 pin 12 meets a junction dot that runs to U3 pin 1 and to U4 pin 15.
- The line from 1A11P1 pin 1, labelled "( NOT USED )", ends at a junction dot on the R1 / U1 pin 1 node. With nothing on that pin, R1 holds U1 pin 1 high and the gate passes the U5 clock to U3.
- On the component-location drawing R2-R11 sit in one column beside Q1-Q10 in the order printed there; the drawing does not pair each resistor with a transistor.
