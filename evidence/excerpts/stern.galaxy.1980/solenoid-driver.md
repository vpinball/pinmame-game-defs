Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF pages 26 and 27, drawing number `12B-432-S-114` (printed at the lower left of page 27 and at the top right of page 26), title block `STERN ELECTRONICS INC.`, `1725 DIVERSEY BLVD. CHICAGO 60614`, `SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC`, `FOR GALAXY, SOLID STATE`, `DRN. CW.`, `DATE 10-17-79`, `DIETZGEN NO. 198M AGEPROOF` below. The sheet is stored in two upright halves with an overlap strip: PDF page 27 carries the left half (the `74L154` decoder `U2`, the driver stages, and the `J2` and `J5` pin lists) and PDF page 26 carries the right half (the flipper circuits, the connector blocks and the voltage regulator; the title block is on page 26). Read from crops at 450 to 550 dpi, no rotation; the Q17-Q19 output routes were rechecked on a 220 dpi crop. The notes box at the right edge of page 26 (headed `NOTES`, items `1.`, `2.`, `3.`) is cut off by the page edge and its text is not on either page.

## Notes printed on page 27

`U1, U2 & U3 = CA3081`; `*SE9302 Substitute X44E198`; `Solenoid Test Display No. is Drive Transistor (Q) Position on SDU`. (Note that the drawing's chips are `U1`, `U3`, `U4` for the Darlington drivers and `U2` for the decoder; the note lists `U1, U2 & U3`.)

## Input and decoder (page 27, left)

- `J4` (letter `B` under it): pins `6` `[BLU-Y]`, `5` `[BLU-R]`, `4` `[O-B]`, `3` `[R-W]`, `7` `[BRN-R]`. Pins 6, 5, 4, 3 are labelled `PINS 3, 4, 5 & 6 MOMENTARY SOLENOID DATA`; pin 7 is labelled `PIN 7 SOLENOID BANK SELECT LOW WHEN SELECTED`. Pins 6, 5, 4, 3 feed decoder `U2` pins 23, 22, 21, 20 and pin 7 feeds `U2` pin 19; each of the four data lines has a pull-up `R1`, `R2`, `R3`, `R4` (`100K`) to `+5`, and the lines are marked on `U2` as pins `1`, `2`, `4` and `8` (the weights beside the pins; read as `1`, `2`, `4'`, `8`).
- `U2` is printed `74L154`, supply pin `24` to `+5`, pin `18` to ground, pin `17` unconnected at the lower end, `12` to ground at the foot.
- `U2` outputs carry the pin numbers `1` to `11` and `13` to `16` (no `12` drawn), each through a resistor `R57` to `R71` in order: pin 1 `R57`, 2 `R58`, 3 `R59`, 4 `R60`, 5 `R61`, 6 `R62`, 7 `R63`, 8 `R64`, 9 `R65`, 10 `R66`, 11 `R67`, 13 `R68`, 14 `R69`, 15 `R70`, 16 `R71`.
- Also printed above the first stage on page 27: `1.2K (x15)`, `120Ω (x15)` (`R5`), `.002 (x15)`, `330Ω (x15)` (`R6`), `1N4004 (x15)`, `SE9302 (x15)`, meaning the stage drawn at the top is the pattern repeated for the other transistors, and diode `CR2`.

## Drive stages

Each driver stage is drawn as: a `CA3081` Darlington section (`U1`, `U3` or `U4`, with the pin numbers beside the section), a resistor `R<n>` from the supply, a diode `CR<n>`, a capacitor `C<n>`, a resistor to ground and the power transistor `Q<n>`. The decoder's resistor line enters the section's base pin. As read from the drawing (the input line of each stage runs from the `U2` output line of the same row; the association of the output line to the stage is from the row it is printed in and the line it continues on, read at 450 dpi):

| U2 output pin | Input resistor | Darlington section and pins | Stage resistor, diode, capacitor, ground resistor | Transistor | Load connector pin (see next section) |
| ---: | --- | --- | --- | --- | --- |
| 1 | R57 | U1, 3 / 2 | R5, CR2, C1, R6 | Q2 | J2 4 |
| 2 | R58 | U1, 16 / 1 | R7, CR1, C15, R8 | Q1 | J2 9 |
| 3 | R59 | U1, 13 / 14 | R9, CR5, C2, R10 | Q5 | J2 10 |
| 4 | R60 | U1, 11 / 12 | R11, CR6, C16, R12 | Q6 | J2 11 |
| 5 | R61 | U1, 10 / 9 | R13, CR7, C3, R14 | Q7 | J2 12 |
| 6 | R62 | U1, 6 / 4 | R15, CR3, C17, R16 | Q3 | J2 5 |
| 7 | R63 | U1, 8 / 7 | R17, CR4, C4, R18 | Q4 | J1 5 |
| 8 | R64 | U3, 16 / 1 | R19, CR8, C18, R20 | Q8 | J5 10 |
| 9 | R65 | U3, 11 / 12 | R21, CR13, C5, R22 | Q13 | J5 12 |
| 10 | R66 | U3, 13 / 14 | R23, CR14, C19, R24 | Q14 | J5 11 |
| 11 | R67 | U3, 3 / 2 | R25, CR9, C6, R26 | Q9 | J5 9 |
| 13 | R68 | U3, 8 / 7 | R27, CR10, C20, R28 | Q10 | J5 15 |
| 14 | R69 | U3, 10 / 9 | R29, CR12, C7, R30 | Q12 | J5 13 |
| 15 | R70 | U3, 6 / 4 | R31, CR11, C21, R32 | Q11 | J5 14 |
| 16 | R71 | U4, 8 / 7 | R33, CR16, C8, R34 | Q16 | J5 8 |

Every drive transistor is labelled in the drawing with its `Q` number only; `Q2`, `Q15`, `Q17`, `Q18` and `Q19` also print the type `SE9302` with an asterisk (`*SE9302 Substitute X44E198`). The stage-to-pin column is obtained by following the collector line of each transistor across the sheet; the lines run orthogonally and cross many vertical buses, so each mapping is a reading of the line routes (not a printed label) and is flagged below for the four doubtful ones.

## Connectors and the load label printed at each pin

Printed lists beside the connectors; wire colours in brackets or parentheses as printed.

`J2` (list on page 27, lower left; letter `C` under `J2` on page 26): pin `9` `LEFT SLING-SHOT (PUR-W)`; pin `4` `RIGHT SLING-SHOT (-BRN-)`; pin `10` `TOP THUMPER (G-R)`; pin `11` `DR. TARG. RESET (GREY)`; pin `5` `KNOCKER (B-Y)`; pin `12` `BALL KICKER (Y-R)`. The connector box on both pages also shows an additional pin `6` with no label (see below). Page 26 prints `SEE LEFT SIDE OF SCHEMATIC FOR SOLENOID PINS.` with arrows to the `J2` pin column.

`J5` (list on pages 26 and 27): pin `10` `SAUCER (B-Y)`; pin `12` `DR. TARG. RED (O-B)` (printed `(0-B.)`, with the hyphen overwritten); pin `11` `DR. TARG. BLUE (-B-)`; pin `9` `OUT-HOLE (O-R)` (printed `(0-R)`); pin `15` `LOWER LEFT THUMPER (B-BLU)`; pin `13` `DR. TARG. YEL. (O-W)`; pin `14` `DR. TARG. BLACK (Y-BLUE)`; pin `8` `OPEN`.

`J1` (letter `P` under it; block with pins `5`, `2`, `3`): pin `5` is labelled `LOWER R. THUMPER (BRN-Y)`; pins `2` and `3` carry no label of their own and are drawn beside the same label as pin 5.

`J3` (letter `B`) on page 27: pins `7` and `4` with no label.

The list above gives only the labels printed at each pin; the `J1`, `J2`, `J3` and `J5` pin boxes on page 26 repeat those numbers. Routes read from the collector lines (page 27 and the overlap strip of page 26):

- `Q1` collector line goes to `J2` 9 and a vertical from it continues to `J1` 2.
- `Q2` collector (the stage at the top with the `(x15)` notation) goes to `J2` 4 and a vertical from it continues to `J1` 3.
- `Q3` collector goes to `J2` 5 and to `J3` 4.
- `Q4` collector goes to `J1` 5 (the line jogs down before reaching the pin).
- `Q5` to `J2` 10, `Q6` to `J2` 11, `Q7` to `J2` 12, `Q8` to `J5` 10, `Q9` to `J5` 9, `Q10` to `J5` 15, `Q11` to `J5` 14, `Q12` to `J5` 13, `Q13` to `J5` 12, `Q14` to `J5` 11.
- `Q16` collector goes to `J5` 8 (`OPEN`) and a vertical from that line also reaches `J2` 6 and `J3` 7, which have no load label.

## Flipper circuits and other stages (page 26)

- `J4` (letter `B`) on page 26: pin `8` `FLIPPER DISABLE` `PB6` `[BLU-W]`; pin `11` `PB4` `[Y-W]`; pin `10` `FB7` `[Y-R]` (printed `FB7`); pin `9` `PB5` `[BLU-O]` (printed `[BLU-O]` with a stray mark). Each input line has a 3.9K resistor to the `CA3081` section `U4`: `R37` (3.9K) for pin 8, `R40` (3.9K) for pin 11, `R43` (3.9K) for pin 10, `R46` (3.9K) for pin 9 (and `R47` printed `3.9K` with `CR19` for the last stage).
- Stage resistors and sections as printed: `Q15` with `R38` (120Ω), `CR15` (1N4004), `C11` (.002), `R39` (330Ω), `U4` pins 3 / 2; `Q17` with `R41` (120Ω), `CR17`, `C12` (.002), `R42` (330Ω), `U4` pins 10 / 9; `Q18` with `R44` (120Ω), `CR18`, `C13` (.002), `R45` (330Ω), `U4` pins 11 / 12; `Q19` with `R47` (3.9K), `CR19` (1N4004), `C14` (.002), `R48` (330Ω), `U4` pins 13 / 14. All four transistors print `SE9302` with an asterisk.
- Flipper switches: a two-pole drawing with `4` to `6` and `3` to `5`: `4` / `6` `LEFT FLIPPER SW`, `3` / `5` `RIGHT FLIPPER SW.`, a dashed mechanical link running to the relay contact `8` (`FLIPPER ENABLE RELAY`). `J2` pins: `2` `To LEFT [BLU] FLIPPER BUTTON`, `1` `To RIGHT [R] FLIPPER BUTTON`. `J1` pin `8` is labelled `To LEFT FLIPPER COIL [G] (16)` and `J1` pin `9` `To RIGHT FLIPPER COIL [O] (16)`.
- `FLIPPER ENABLE RELAY` coil: contact terminals `8` and `7`, diode `CR20` (`1N4004`) across the coil, `43VDC` printed at the foot; the coil's other end runs to `J3` pin `5` `TO A2J3-8 [Y-W]`. `Q15`'s collector line goes to the relay coil.
- `Q17`'s collector line goes to `J5` pin `7`; the wire colour `W-BLU` is printed above the line and `GEN. ILLUM RELAY` (bold, on two lines) to the right of the pin. The vertical that crosses this line has no junction dot on it.
- `Q18`'s collector line goes to `J2` pin `15` `N/U` (letter `C` under `J2`). A junction dot on this line starts a vertical that runs up to `J5` pin `3` `N/U` and down to `J3` pin `9` `N/U`, so Q18 reaches three pins, all marked `N/U`.
- `Q19`'s collector line goes to `J2` pin `8`, labelled `COIN LD.` on the line and `COIN LOCK-OUT [Y-W]` beside the pin.
- Other pins of this half: `J3` `24` `[W-O]` and `23` `[R-Y]` both on a ground symbol line labelled `+43V SOLENOID GND` (the `+` and digit are overprinted); `J3` `25` and `13`, the MPU group `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22` with the printed notes `GREY-R To MPU [W-G]` (14, 15), `A5J4-3 [B-G] LAMP DRIVER DISPLAYS A1J1-18 [G-W]` (16, 17), `GREY-G To MPU (B-R)` (18, 19), `DISPLAYS A1J1-11 [BRN-...]` (20, `[BRN-W]` as printed on the notes line), `TRANSFORMER [W-BLU] A2J3-16 [B-BLU]` (21, 22); `J3` `25` is joined by a dashed line to `[BRN-W]` and `A3J3-25`; `J3` `13` is `A3J3-25`; `J2` `7` `[Y-R]` and `J3` `8` `[R]` (`+185 VDC`).
- `J3` (letter `B`) pins on the voltage side: `11` `To MPU [R-G]`; `12` `UNREGULATED FROM A2J3-8 [O]`; `10` `To TRANSFORMER (BRIDGE & GND) A2J3-17 [W-BRN]`; `6` `FROM A2J3-4 BRIDGE RECTIFIER [GREY-BLU]` (the supply node `TP4` `+230 V`); `3` `FROM A2J3-18 TRANSFORMER BRIDGE GND. [W]`.
- Voltage regulator: `25A-LM-323 +5V REG`, test points `TP1` `+5 VDC`, `TP3`, `TP5` `11.9 VDC`, `TP6` `R36 120Ω`, `TP7` `R72 1.2K`, `TP2` `+185 VDC`; `+5V BUS LINE` with `C22` `.01 µfd` and `+5 VDC REG`; `R49` `100Ω 1/2W`, `R50` `4.7Ω`, `C23` `11,700 µf 20 WV`, `C24` `2 µf 20 WV`, `C25` `.1`; `C26` `160 µf 350 WV`, `R35` `100K 1W`; the high-voltage regulator uses `Q21` (`2N3584`) with `CR21` (`1N4004`) across it, `Q22` (`2N3440`), `Q23` (`2N3440`), `R51` `22K 1/2W`, `R52` `390Ω`, `R58` `8.2K`, `R55` `1.2K`, `R56` `82K 1/2W`, `RT1` `25K` marked `+185 Vdc ADJUST`, `VR1` `1N5275A`, `C28` `.01` `500 VDC`, with voltage labels `193 VDC` and `+140 VDC`.

## Uncertain readings

- The routing of the collector lines to the connector pins (the `Load connector pin` column) was traced by eye along crowded orthogonal lines; the doubtful ones are `Q4` to `J1` 5 (it crosses the `Q3` branch to `J3` 4), `Q2` to `J2` 4 (its line is the top rail of the sheet), the `J1` 2/3 and `J2` 6 / `J3` 7 side branches, and `Q16`'s line also reaching `J2` 6 / `J3` 7.
- The `U2` output to stage association (`Input resistor` column) is read from the rows of the drawing; the printed Darlington pin numbers beside each stage and the resistor `R57`..`R71` labels were read at 450 dpi.
