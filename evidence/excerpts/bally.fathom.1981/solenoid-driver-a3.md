# Bally Fathom — A3 Solenoid Driver / Voltage Regulator schematic (W-1183-34c)

Source: `Bally_1981_Fathom_Schematics.pdf`, PDF page 7. Title block reads
`SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC` / `FATHOM` / `# 1233` / `W-1183-34c`, sheet `10`.
Transcribed by hand from a 400 dpi render, in three overlapping crops covering the decoder, the
driver stages, and the connector blocks.

Connector code printed on the sheet: `C -> ROUTE TO CABINET CONN`, `B -> ROUTE TO BACK BOX CONN`,
`P -> ROUTE TO PLAYFIELD CONN`. Note 7: `* INDICATES 'AID' TEST POINT`.

## Momentary decode

`J4 B` carries the momentary selector from the MPU, printed `MOMENTARY SOLENOID` /
`SOLENOID BANK SELECT` and annotated `LOW WHEN SELECTED`:

| J4-B pin | signal | U2 input |
| --- | --- | --- |
| 6 | PB0 | A (test point *23) |
| 5 | PB1 | B (*22) |
| 4 | PB2 | C (*21) |
| 3 | PB3 | D (*20) |
| 7 | CB2 | G2 (*19) |

`U2` is `74L154` `BINARY TO ONE OF SIXTEEN DECODER`, part `E 620-39`, pin 24 = Vcc, pin 18 = G1
(grounded), pin 12 = ground.

Each decoder output drives one pre-driver section of `U1`/`U3`/`U4` (`CA-3081`, `E681`) through a
1.2K resistor (`1.2K TYP. (X15)`, R57-R71), then a `1N4004` (CR1-CR16) into an `SE9302` power
transistor (`E585-34`, nineteen fitted, Q1-Q19) with a 330 ohm base resistor and a .002 uF snubber.

Decoder output to power transistor, read row by row (output label, U2 pin, series resistor,
pre-driver section, coupling diode, transistor):

| U2 output | U2 pin | R | pre-driver | CR | transistor |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | R57 | U1 3/2 | CR2 | Q2 |
| 1 | 2 | R58 | U1 1/16 | CR1 | Q1 |
| 2 | 3 | R59 | U1 14/13 | CR5 | Q5 |
| 3 | 4 | R60 | U1 12/11 | CR6 | Q6 |
| 4 | 5 | R61 | U1 9/10 | CR7 | Q7 |
| 5 | 6 | R62 | U1 4/6 | CR3 | Q3 |
| 6 | 7 | R63 | U1 7/8 | CR4 | Q4 |
| 7 | 8 | R64 | U3 1/16 | CR8 | Q8 |
| 8 | 9 | R65 | U3 12/11 | CR13 | Q13 |
| 9 | 10 | R66 | U3 14/13 | CR14 | Q14 |
| 10 | 11 | R67 | U3 2/3 | CR9 | Q9 |
| 11 | 13 | R68 | U3 7/8 | CR10 | Q10 |
| 12 | 14 | R69 | U3 9/10 | CR12 | Q12 |
| 13 | 15 | R70 | U3 4/6 | CR11 | Q11 |
| 14 | 16 | R71 | U4 7/8 | CR16 | Q16 |
| 15 | 17 | — | — | — | printed `OPEN` |

Fifteen driven outputs; output 15 is printed `OPEN`, which is the idle selector state. The fifteen
momentary transistors are therefore exactly Q1-Q14 and Q16, and Q15/Q17/Q18/Q19 are the four
continuous drivers below.

## Connector destinations, verbatim labels

`J2` pins, top to bottom as drawn, each with an arrow from a driver stage:

| J2 pin | printed function |
| --- | --- |
| 9 | `3 TOP DROP TARGET RESET OR 1ST GREEN IN LINE DROP TARGET` |
| 4 | `6 DROP TARGET RESET OR 2ND GREEN IN LINE DROP TARGET` |
| 10 | `3 MIDDLE DROP TARGET RESET OR 3RD GREEN IN LINE DROP TARGET` |
| 11 | `RIGHT INLINE DROP TARGET RESET` |
| 5 | `KNOCKER` |
| 6 | `N/U` |
| 12 | `N/U` |

`J3 B` pins 7 and 4 carry arrows but are printed with no function label at all.

`J1 P`:

| J1 pin | printed function |
| --- | --- |
| 5 | `OUTHOLE KICKER` |
| 2 | `N/U` |
| 3 | `N/U` |

`J5`:

| J5 pin | printed function |
| --- | --- |
| 10 | `LEFT THUMPER BUMPER` |
| 12 | `BOTTOM THUMPER BUMPER` |
| 11 | `RIGHT THUMPER BUMPER` |
| 9 | `LEFT SLINGSHOT` |
| 15 | `RIGHT SLINGSHOT` |
| 13 | `TOP SAUCER OR 1ST BLUE IN LINE DROP TARGET` |
| 14 | `RIGHT SAUCER OR 2ND BLUE IN LINE DROP TARGET` |
| 8 | `3RD BLUE IN LINE DROP TARGET` |

Five of these destinations are printed as one output serving either of two coils
(`... OR ...`). That is the Solenoid Expander relay: see `playfield-wiring.md`, where the two
alternative coils on each of those five wires are drawn with a ganged relay contact between them.

Driver-stage to connector-pin lines that could be followed unambiguously on the retained scan
(straight horizontal runs with no crossing):

- Q9 (output 10) -> J5-9 `LEFT SLINGSHOT`
- Q10 (output 11) -> J5-15 `RIGHT SLINGSHOT`
- Q12 (output 12) -> J5-13 `TOP SAUCER OR 1ST BLUE IN LINE DROP TARGET`
- Q11 (output 13) -> J5-14 `RIGHT SAUCER OR 2ND BLUE IN LINE DROP TARGET`
- Q16 (output 14) -> J5-8 `3RD BLUE IN LINE DROP TARGET`

The remaining ten driver outputs reach their pins through nested staircase routing that the retained
scan does not resolve line by line. Those ten were instead established from the ROM's own solenoid
self test; see `../../../reports/spatial/bally/fathom-1981.md` and the retained harness run.

## Continuous outputs

The four continuous outputs are separate driver stages fed from four further MPU PIA1:B lines, each
through a 3.9K/120 ohm pair, a 1N4004 and an SE9302:

| J4-B pin | printed signal | printed name | transistor | destination |
| --- | --- | --- | --- | --- |
| 8 | `PB6` | `FLIPPER DISABLE` / `CONT 1` | Q15 | `K1` `FLIPPER ENABLE RLY`, out to `J3 B` pin 5 `TO A2J3-8, A8J1-9`, 43 VDC |
| 11 | `PB4` | `CONT 2` | Q17 | `J5` pin 7 `N/U`, `J2 C` pin 15 `N/U` |
| 10 | `PB7` | `CONT 3` | Q18 | `J2 C` pin 15 `N/U` |
| 9 | `PB5` | `COIN LOCK OUT` / `CONT 4` | Q19 | `J3 B` pin 8 `COIN LOCKOUT` |

`CONT 2` and `CONT 3` reach nothing but pins printed `N/U`. `CONT 3` is PB7, which the playfield
wiring diagram shows is also the sixth switch-column strobe `ST 5` at `A4J4-8`.

## Flipper section

Printed at the top right of the sheet: coils `LEFT FLIPPER`, `RIGHT FLIPPER`, `UPPER RIGHT FLIPPER`
and `OUTHOLE KICKER` sit on the 43 VDC bus behind the K1 flipper-enable relay contacts, fed from
`A2J1-7 +43 VDC` through a `1A S.B.` fuse. Flipper coil outputs go to `J1` pins 8 (`TO LEFT FLIPPER
COIL`) and 9 (`TO RIGHT FLIPPER COIL`); the cabinet flipper buttons come in on `J2 C` pin 2 (`TO
LEFT FLIPPER BUTTON`) and pin 1 (`TO RIGHT FLIPPER BUTTON`). There is no driver-board momentary
output for any flipper coil; the relay gates the whole flipper bus.

## Other blocks on the sheet

`+5VDC REGULATOR` (Q20, `E-710` / `LAS1405` / `78H05KC` / `LM323K`) and `+190 VDC REGULATOR`
(Q21 `2N3584`, Q22/Q23 `2N3440`, VR1 `1N5275A`, RT1 25K `+190 VDC ADJUST`, fuse `3/16 A 8 AG`
`E-133-29`), feeding `J3 B` pin 8 `+190 VDC TO DISPLAYS`. `J2 C` pin 7 is `SELF TEST GRD RETURN`.
`LAST NUMBER USED` block: `R72`, `C29`, `Q23`, `CR21`, `VR1`, with `N/U C9, C10` and `N/U Q20`.
