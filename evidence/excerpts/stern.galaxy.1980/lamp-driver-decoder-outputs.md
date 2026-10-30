Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF page 30, drawing number `12B-431-S-114` (printed at the lower left), `LAMP DRIVER SCHEMATIC` `FOR GALAXY` (title block on PDF page 31, `DATE 10-11-79`); PDF page 30 is the left half of the sheet. The page is upright. It was read from crops at 500 to 1000 dpi, no rotation. The four decoder chips `U1` to `U4`, the J4 input pins and the notes are on this page.

The four decoder chips are labelled `U1`, `U2`, `U3` (printed `U3` in a bold hand that looks like `UB`) and `U4`, each with a part label beside it printed `MC14514B` (the last character of the label looks like `B`, `8` or `3` on different chips; no other part number is printed). Each chip's input pins, as printed on the chip's left side with the pin number outside and the pin name inside: `24` `VDD`, `2` `D1`, `3` `D2`, `21` `D3`, `22` `D4`, `23` `E`, `1` `ST`, `12` `VSS`. Lines feeding these pins are labelled `AD0` to `AD3` for `D1` to `D4`, and `PD0`, `PD1`, `PD2`, `PD3` for the `E` pin of `U1`, `U2`, `U3`, `U4` respectively; the `ST` pins join the common `STROBE` line.

Each output line has the chip pin number printed outside the chip (right of the body, hand written) and, beside the chip edge, a smaller output index (`0` to `14` for the 15 drawn outputs). On each line a resistor is printed with its designation and `2KΩ` (`ZKΩ` in the hand lettering), then a transistor symbol drawn with its `Q` label above it and the transistor type to its right: `2N5060` (printed `ZN5060`) or `MCR106-1` with a filled triangle (note 1: `INDICATES MCR106-1 TRANSISTOR`). The type is read as the one printed beside the same transistor symbol as the `Q` label. Output indices S0 to S14 follow the chip's output index. For `U3` and `U4` the outputs with pins 14, 13 and 16 (S12, S13, S14) are drawn above the S0 line instead of below S11. Output S15 is not drawn on any chip.

### U1 (MC14514B)

| Output | Chip pin | Resistor | SCR | Type |
| ---: | ---: | --- | --- | --- |
| S0 | 11 | R14 | Q14 | 2N5060 |
| S1 | 9 | R12 | Q12 | 2N5060 |
| S2 | 10 | R13 | Q13 | 2N5060 |
| S3 | 8 | R8 | Q8 | MCR106-1 (triangle) |
| S4 | 7 | R9 | Q9 | MCR106-1 (triangle) |
| S5 | 6 | R10 | Q10 | MCR106-1 (triangle) |
| S6 | 5 | R11 | Q11 | 2N5060 |
| S7 | 4 | R4 | Q4 | 2N5060 |
| S8 | 18 | R1 | Q1 | MCR106-1 (triangle) |
| S9 | 17 | R2 | Q2 | MCR106-1 (triangle) |
| S10 | 20 | R3 | Q3 | MCR106-1 (triangle) |
| S11 | 19 | R7 | Q7 | 2N5060 |
| S12 | 14 | R16 | Q16 | MCR106-1 (triangle) |
| S13 | 13 | R5 | Q5 | 2N5060 |
| S14 | 16 | R6 | Q6 | 2N5060 |

### U2 (MC14514B)

| Output | Chip pin | Resistor | SCR | Type |
| ---: | ---: | --- | --- | --- |
| S0 | 11 | R29 | Q29 | 2N5060 |
| S1 | 9 | R27 | Q27 | 2N5060 |
| S2 | 10 | R28 | Q28 | 2N5060 |
| S3 | 8 | R35 | Q35 | MCR106-1 (triangle) |
| S4 | 7 | R34 | Q34 | MCR106-1 (triangle) |
| S5 | 6 | R22 | Q22 | MCR106-1 (triangle) |
| S6 | 5 | R26 | Q26 | 2N5060 |
| S7 | 4 | R25 | Q25 | 2N5060 |
| S8 | 18 | R24 | Q24 | MCR106-1 (triangle) |
| S9 | 17 | R17 | Q17 | MCR106-1 (triangle) |
| S10 | 20 | R23 | Q23 | MCR106-1 (triangle) |
| S11 | 19 | R21 | Q21 | 2N5060 |
| S12 | 14 | R15 | Q15 | MCR106-1 (triangle) |
| S13 | 13 | R18 | Q18 | 2N5060 |
| S14 | 16 | R19 | Q19 | 2N5060 |

### U3 (MC14514B)

| Output | Chip pin | Resistor | SCR | Type |
| ---: | ---: | --- | --- | --- |
| S0 | 11 | R36 | Q36 | 2N5060 |
| S1 | 9 | R38 | Q38 | 2N5060 |
| S2 | 10 | R44 | Q44 | 2N5060 |
| S3 | 8 | R49 | Q49 | MCR106-1 (triangle) |
| S4 | 7 | R48 | Q48 | MCR106-1 (triangle) |
| S5 | 6 | R37 | Q37 | 2N5060 |
| S6 | 5 | R32 | Q32 | 2N5060 |
| S7 | 4 | R20 | Q20 | 2N5060 |
| S8 | 18 | R42 | Q42 | MCR106-1 (triangle) |
| S9 | 17 | R41 | Q41 | MCR106-1 (triangle) |
| S10 | 20 | R40 | Q40 | MCR106-1 (triangle) |
| S11 | 19 | R39 | Q39 | 2N5060 |
| S12 | 14 | R33 | Q33 | MCR106-1 (triangle) |
| S13 | 13 | R30 | Q30 | 2N5060 |
| S14 | 16 | R31 | Q31 | 2N5060 |

### U4 (MC14514B)

| Output | Chip pin | Resistor | SCR | Type |
| ---: | ---: | --- | --- | --- |
| S0 | 11 | R57 | Q57 | 2N5060 |
| S1 | 9 | R50 | Q50 | 2N5060 |
| S2 | 10 | R51 | Q51 | 2N5060 |
| S3 | 8 | R54 | Q54 | MCR106-1 (triangle) |
| S4 | 7 | R55 | Q55 | MCR106-1 (triangle) |
| S5 | 6 | R60 | Q60 | 2N5060 |
| S6 | 5 | R59 | Q59 | 2N5060 |
| S7 | 4 | R58 | Q58 | 2N5060 |
| S8 | 18 | R56 | Q56 | MCR106-1 (triangle) |
| S9 | 17 | R46 | Q46 | 2N5060 |
| S10 | 20 | R52 | Q52 | 2N5060 |
| S11 | 19 | R53 | Q53 | 2N5060 |
| S12 | 14 | R47 | Q47 | MCR106-1 (triangle) |
| S13 | 13 | R43 | Q43 | 2N5060 |
| S14 | 16 | R45 | Q45 | 2N5060 |

Reading notes. Many `Q` labels on the transistor symbols are partly overprinted or broken by the vertical line through them (for example `Q13`, `Q16`, `Q25`, `Q21`, `Q38`, `Q49`, `Q55`, `Q56`, `Q52`); each was read as the number carried by the SCR column of the connector blocks on PDF page 31 and by the resistor of the same line. The resistor label `R18` of U2 S13 is written over another figure; `R19` of U2 S14 and `R6` of U1 S14 are small but legible. Wherever the transistor type printed beside the symbol disagrees with the filled-triangle marks beside the J1/J2/J3 pins on PDF page 31, both are as printed: `Q5` is `2N5060` here but has a triangle on J2 pin 16 on page 31, and `Q21` is `2N5060` here but has a triangle on J1 pin 12 (J2 pin 12 has none).

### J4 inputs

The J4 connector is drawn at the left edge as a dashed box labelled `J4`; each signal enters through a `20KΩ` resistor (printed `ZOKΩ`) and a pin arrow.

| Signal | Pin | Resistor | Notes |
| --- | ---: | --- | --- |
| AD0 | 14 | R76 | the four `AD` lines together are labelled `LAMP ADDRESS` |
| AD1 | 15 | R77 | |
| AD2 | 16 | R78 | |
| AD3 | 17 | R79 | |
| PD0 | 7 | R74 | the four `PD` lines together are labelled `LAMP DATA` |
| PD1 | 6 | R73 | |
| PD2 | 5 | R72 | |
| PD3 | 4 | R71 | |
| (strobe, no signal name at the pin) | 1 or 2 | R75 | line labelled `STROBE`; the pin number is small and unclear, `1` or `2` |
| (no signal name) | 3 | | joins a test point `TP2` marked `+5V` and, through `R70` `2KΩ`, a point marked `TP3` `+5V` (the label is overprinted and reads `TP3`), with a capacitor `C1` `.01 MFD` to ground |
| (no signal name) | 2, 1 (or `11`) and 2 | | three lines tied together and joined to the test point `TP1` marked `GND` and to the ground symbol under `C1` (the middle pin number is faint and reads `1`, `11` or `|`) |
| (no signal name) | (none printed) | | a fourth line at the foot of J4 with no number, also tied to the ground line |

The upper rail above the chips carries a bus of resistors `R61` to `R69`, each labelled `2.2 MEG Ω`, joined to a line marked `+5V`; `R61` to `R65` feed the `AD0`..`PD3` lines of the chips' D inputs and `R66` to `R69` the other group, as drawn.

Notes, verbatim (hand lettered, under `NOTES:`):

1. `▲ INDICATES MCR106-1 TRANSISTOR.`
2. `THIS DOCUMENT FOR LDA-100 REV. A AND LDA-REV. B SINGLE SIDED P.C. BOARDS.`

The sheet also prints `DIETZGEN NO. 198M AGEPROOF` under the drawing number.
