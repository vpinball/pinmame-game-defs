# The Sopranos — 2-Flipper Circuit Wiring Diagram

Transcribed from `Stern_2005_The_Sopranos_Service_Manual.pdf`, PDF page 129 (printed Section 5, Chapter 2, page 112,
"2-Flipper Circuit Wiring Diagram"), from the PDF text layer checked against a 158 dpi render (`flipper-circuit.webp`).

## Dedicated switch inputs

`DEDICATED SWITCH INPUTS (SWITCH TO GROUND)`, `CN6 CPU-SOUND BOARD (PARTIAL VIEW)`, pins 1, 2, 3, 4, 6, 12 with wires
GRY-BRN, GRY-RED, GRY-ORG, GRY-YEL and the BLK ground:

| Switch | Printed | Type |
| --- | --- | --- |
| DS-3 | RIGHT FLIPPER, IN CABINET, DEDICATED SWITCH | N.O. |
| DS-1 | LEFT FLIPPER, IN CABINET, DEDICATED SWITCH | N.O. |
| DS-4 | RIGHT E.O.S., ON ASSY., DEDICATED SWITCH | N.C. |
| DS-2 | LEFT E.O.S., ON ASSY., DEDICATED SWITCH | N.C. |

`NOTE: N.C. = Normally Closed  N.O. = Normally Open`. `The Outside LEFT FLIPPER BUTTON located on the Cabinet operates
the Left Flipper. The Outside RIGHT FLIPPER BUTTON located on the Cabinet operates the Right Flipper.`

## Drive

`I/O POWER DRIVER BOARD (PARTIAL VIEW)`: J16 `POWER OUT` pins 1, 11, 15; `Q13 Q14 Q15 Q16` MOS FET `STP20N10L`; J10
`VOLTAGE` pins 10, 2, 1 (`2 RED-YEL 50V DC`); J9 `HIGH CURRENT SOLENOIDS` pins 9, 8, 1 (`2 BLU-BLK`, ORG-GRY, ORG-VIO).

- `LOWER RIGHT FLIPPER 22-1080 COIL`: `3A SLO-BLO (Located under Playfield)`, `RED-YEL 50V DC`, `BLU-YEL`, `Coil Wrap: YEL-GRN`, control `ORG-VIO`.
- `LOWER LEFT FLIPPER 22-1080 COIL`: `3A SLO-BLO (Located under Playfield)`, `RED-YEL 50V DC`, `GRY-YEL`, `Coil Wrap: YEL-GRN`, control `ORG-GRY`.
- `The 3A 250v Slo-Blo Fuses are located under the playfield NEAR the Flipper Assembly, see previous page for locations.`

## Technical Overview (printed text)

`Our Flipper System uses one supply voltage (50v DC) for both kick & hold. Once the Game CPU detects a Flipper Cabinet
Switch closure (during game play) it applies a 40msec pulse to the gate of the Flipper MOS FET Drive Transistor
(STP-20N10L). If it continues to detect a Flipper Cabinet Switch closure (the player holding the button in) it will
continue to pulse the flipper drive transistor 1msec every 12msecs for the duration of the hold cycle.`

`The E.O.S. (End-Of-Stroke) Switch serves the same function as before as it prevents foldback when the player has the
flipper energized to capture balls. The E.O.S. Switch is a normally closed switch which opens approximately 1/16" when
the flipper is energized. The Game CPU will detect a switch closure if the flipper bat is forced back by a high velocity
shot or rebound on the playfield and will apply another 40msec pulse of 50v DC to the coil.`

## Related pages

The flipper assembly pages (PDF 101 left 500-6543-12, PDF 102 right 500-6543-02) list item 3 `Power (EOS / End-of-Stroke)
Switch 1 180-5149-00`; the switch parts page (PDF 83) lists `L-# Switch (End-of-Stroke), Stack (Blade) 2 180-5149-00,
Dedicated Switch Numbers DS-2 & DS-4`.
