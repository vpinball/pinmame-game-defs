# Bally Fathom — A9 Auxiliary Lamp Driver schematic (W-1207-9) and parts list

Two sources are transcribed here because they describe the same board.

## Component parts list

Source: `Bally_1981_Fathom_English_Manual.pdf`, PDF page 37. Heading `AS-2518-52 AUXILIARY LAMP
DRIVER` and `A9: AUXILIARY LAMP DRIVER COMPONENT PARTS LIST`.

| item | qty | reference | Bally part | description |
| --- | --- | --- | --- | --- |
| 1 | 1 | A9 | AS-2518-52 | Auxiliary Lamp Driver, Complete |
| 2 | 1 | U1 | E-620-134 | Quad Flip Flop |
| 3 | 4 | U2 thru U5 | E-620-108 | BCD to Decimal Decoder |
| 4 | 28 | Q1 thru Q28 | E-585-29 | S.C.R. |
| 5 | 28 | R10 thru R37 | E-105-237 | Resistor, 2K ohm, 1/4 w, 5% |
| 6 | 8 | R1-4, R6-9 | E-105-242 | Resistor, 20K ohm, 1/4 w, 5% |
| 7 | 1 | R5 | E-105-173 | Resistor, 2.2M, 1/4 W, 5% |
| 8 | 1 | C1 | E-586-85 | Capacitor, .01 uf, 25 V, +-20% |
| 9 | 1 | J1 | E-736-15 | Connector, KK 156 15 Pin |
| 10 | 1 | J2 | E-736-18 | Connector, KK156 18 Pin |
| 11 | 2 | J3 | E-736-10 | Connector, KK 156 10 Pin |
| 12 | 2 | TP1, TP2 | P-5399 | Test Point |
| 13 | 25 | — | M-1777-126 | Jumper |

**This is not the AS-2518-43 board that Bally Centaur and Bally Kiss carry.** The -52 has four
decoders and twenty-eight SCRs where the -43 has two decoders and twelve, so the Centaur/Kiss
decoder-half-to-SCR derivation does not transfer to this machine.

## Schematic

Source: `Bally_1981_Fathom_Schematics.pdf`, PDF page 6. Title block reads `AUXILIARY LAMP DRIVER A9`
/ `FATHOM` / `, 1233` / `W-I207-9`, sheet `9`. Notes printed on the sheet:

1. `ALL RESISTORS ARE 1/4 W. +-5%.`
2. `VOLTAGES SHOWN ARE FOR GAME UP CONDITIONS.`
3. `* INDICATES "AID" TEST POINT`
4. `SCR'S ARE MCR-106-1, (E-585 29).`
5. `PREFIX ALL REFERENCE DESIGNATIONS WITH "A9".`

`J1` (15 pin) carries the second lamp strobe from the MPU and the four lamp data lines. Printed
pin-to-signal, with the harness destinations from the small table at the left of the sheet:

| A9 J1 pin | signal | goes to | wire |
| --- | --- | --- | --- |
| 1 | `AD1` | `A5J4-15` | 13 |
| 2 | `AD0` | `A5J4-14` | 32 |
| 3 | `LAMP STROBE` | `A4J1-8` | 90 |
| 4 | `AD2` | `A5J4-16` | 45 |
| 5 | `N/U` | — | — |
| 6 | `KEY` | — | — |
| 7 | `PD1` | `A5J4-6` | 23 |
| 8 | `PD0` | `A5J4-7` | 63 |
| 9 | `PD2` | `A5J4-5` | 71 |
| 10 | `PD3` | `A5J4-4` | 74 |
| 11 | — | `A5J4-3` | 84 |
| 12 | `N/U` | — | — |
| 13 | `GND` | — | — |
| 14 | `GND` | — | — |
| 15 | `GND` | `A5J4-11` | 58 |

The left-hand table is headed `A9 J1` / `TO` and its foot reads `TO W-1187-`.

`U1` is `MC14175B` (`E-620-134`), a quad flip-flop clocked by `LAMP STROBE` on pin 9 (`CLK.`). Its
data inputs D0/D1/D2 take AD0/AD1/AD2 and its outputs Q0 (pin 2), Q1 (pin 7) and Q2 (pin 10) feed
the `A`, `B` and `C` inputs of all four decoders. D3 (pin 13) is not driven from J1; it sits on R5
(2.2M) to ground, so **only three latched address bits reach this board** and the fourth lamp
address bit is ignored here.

`U2` through `U5` are `MC14028B` (`E-620-108`) `(X4)`. Each decoder's `D` input (pin 11) is driven
through one 20K resistor from one lamp data line: `PD0 -> U2` (R6), `PD1 -> U3` (R7), `PD2 -> U4`
(R8), `PD3 -> U5` (R9). Each decoder uses seven outputs, 0 through 6, and its output 7 (chip pin 4)
is printed `N/U`:

| decoder output | chip pin | U2 (PD0) | U3 (PD1) | U4 (PD2) | U5 (PD3) |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | R10 -> Q1 | R17 -> Q8 | R24 -> Q15 | R31 -> Q22 |
| 1 | 14 | R11 -> Q2 | R18 -> Q9 | R25 -> Q16 | R32 -> Q23 |
| 2 | 2 | R12 -> Q3 | R19 -> Q10 | R26 -> Q17 | R33 -> Q24 |
| 3 | 15 | R13 -> Q4 | R20 -> Q11 | R27 -> Q18 | R34 -> Q25 |
| 4 | 1 | R14 -> Q5 | R21 -> Q12 | R28 -> Q19 | R35 -> Q26 |
| 5 | 6 | R15 -> Q6 | R22 -> Q13 | R29 -> Q20 | R36 -> Q27 |
| 6 | 7 | R16 -> Q7 | R23 -> Q14 | R30 -> Q21 | R37 -> Q28 |
| 7 | 4 | `N/U` | `N/U` | `N/U` | `N/U` |

Twenty-eight SCRs, matching the parts list.

Only seven of the twenty-eight SCR outputs carry a printed function on this sheet. Each is the
decoder output 0 or output 1 of its chip, and each is annotated beside the connector pin it drives:

| SCR | decoder output | connector pin | printed function |
| --- | --- | --- | --- |
| Q1 | U2 output 0 | `J2-7` | `#1 SCAN ROLLOVER BUTTON` |
| Q2 | U2 output 1 | `J2-8` | `#5 BACKSCAN AND 1ST LEFT LANE SCAN` |
| Q8 | U3 output 0 | `J2-14` | `#2 SCAN ROLLOVER BUTTON` |
| Q9 | U3 output 1 | `J2-11` | `#6 BACK SCAN AND 2ND LEFT LANE SCAN` |
| Q15 | U4 output 0 | `J3-8` | `#3 SCAN ROLLOVER BUTTON` |
| Q16 | U4 output 1 | `J3-3` | `#7 BACK SCAN AND 3RD LEFT LANE SCAN` |
| Q22 | U5 output 0 | `J3-15` | `#4 BACK SCAN` |

The remaining twenty-one SCRs reach `J2`/`J3` pins that this sheet leaves without a function label.
The right-hand harness blocks are headed `A9 J2` (`TO PANEL W-1192-30`) and `A9 J3` (`TO INSERT`),
and their own pin columns carry only wire numbers, `N/U` and `KEY` entries, not functions. Two
further captions on the sheet: `TOP (LOOKING AT BACKSIDE OF INSERT)` and, at the harness blocks,
`TO PANEL W-1192-30` and `TO INSERT`.
