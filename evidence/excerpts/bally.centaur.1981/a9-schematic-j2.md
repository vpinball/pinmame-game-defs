# Centaur — AS-2518-43 Auxiliary Lamp Driver A9, connector J2

Transcribed from `Bally_1981_Centaur_Installation_and_General_Game_Operation_Instructions_with_schematics_OCR_searchable.pdf`,
PDF page 51, drawing **W-1207-11**. The accompanying crop is the same region.

The board is generic Bally hardware, so its internal wiring is the same on every machine that
carries one; only the functions printed against the J2 pins are game-specific.

## Structure

Each lamp data line enables one MC14555B decoder half, and the two latched address bits select one
of its outputs:

| data line | decoder half |
| --- | --- |
| PD0 | U2A |
| PD1 | U2B |
| PD2 | U3A |
| PD3 | U3B |

**`Q3` is marked `N/U` on all four halves.** That is why latched address 3 reaches no bulb, and why
public lamps 68, 84, 100 and 116 are bare matrix positions rather than unused lamps.

## Decoder output to SCR to connector pin, with printed function

| half | output | resistor | SCR | J2 pin | printed function |
| --- | --- | --- | --- | --- | --- |
| U2A | Q0 | R14 | Q6 | 7 | TOP LEFT LANE |
| U2A | Q1 | R13 | Q5 | 6 | RIGHT SLINGSHOT |
| U2A | Q2 | R12 | Q4 | 5 | #1 CHAMBER (2) (FROM BOTTOM) |
| U2A | Q3 | — | — | — | N/U |
| U2B | Q0 | R9 | Q1 | 1 | TOP MIDDLE LANE |
| U2B | Q1 | R10 | Q2 | 2 | LEFT SLINGSHOT |
| U2B | Q2 | R11 | Q3 | 3 | #2 CHAMBER (2) |
| U2B | Q3 | — | — | — | N/U |
| U3A | Q0 | R20 | Q12 | 18 | TOP RIGHT LANE |
| U3A | Q1 | R19 | Q11 | 19 | RIGHT THUMPER BUMPER |
| U3A | Q2 | R18 | Q10 | 20 | #3 CHAMBER (2) |
| U3A | Q3 | — | — | — | N/U |
| U3B | Q0 | R15 | Q7 | 11 | *(blank on the sheet)* |
| U3B | Q1 | R16 | Q8 | 12 | LEFT THUMPER BUMPER |
| U3B | Q2 | R17 | Q9 | 17 | #4 CHAMBER (2) (TOP) |
| U3B | Q3 | — | — | — | N/U |

Other J2 pins: `4 KEY`, `8 GND`, `9 GND`, and `10`, `13`, `14`, `15`, `16` marked `N/U`.

## Two things this sheet settles

**The outer top lanes.** `J2-7` reads TOP **LEFT** LANE and `J2-18` reads TOP **RIGHT** LANE. With
`public = 64 + 16k + address + 1` that makes public 65 the left lane and public 97 the right. The
retained community table binds them the other way round; the same traced chain reproduces the
table's other nine auxiliary assignments exactly, so the two outer lanes are a binding mistake in
the table rather than a fault in the derivation.

**Pin 11 is deliberately blank.** It carries a real SCR and series resistor exactly like its eleven
siblings, but no function is printed against it — while the genuinely unused pins on the same sheet
(`10`, `13`, `14`, `15`, `16`) are all marked `N/U` explicitly. Bally distinguished "unused" from
"unlabelled" here. Nothing else in the retained evidence names it: the PinWiki lamp chart leaves the
same row blank, and none of the four retained community tables models the address. This is the one
device that keeps Centaur `partial`.
