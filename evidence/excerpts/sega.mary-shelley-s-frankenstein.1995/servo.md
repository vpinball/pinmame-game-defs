# Mary Shelley's Frankenstein creature head servo and CPU auxiliary connectors

Sources: schematics `Sega_1995_Mary_Shelley_s_Frankenstein_English_Manual_pages_67_93_which_are_the_schematics_OCR_searchable.pdf` (SHA-256 `e4eeb409e321ea1eb3f9d30120e488db8b638a6d3d69f3c66c2c9ca7919bf883`). PDF page 5 (printed page 71, "Backbox Wiring Diagram"), the CPU board connector block CN1-CN3, read on a 300 ppi crop of the retained page render; PDF page 27 (printed page 93, "Creature Head Motion Servo Board" / "Theory of Operation"), read from the rendered page and its text layer. PDF page 4 (printed page 70, "Cabinet Wiring Diagram") for the shaker motor board line.

Conventions: pin, label and wire text as printed; the wire colour of each pin is printed at the right end of its line.

## CPU CN1, CN2 and CN3 (PDF page 5)

| Connector | Pin | Label printed at the left | Wire printed at the right |
| --- | --- | --- | --- |
| CN1 | 1 | [none] | N.C. |
| CN1 | 2 | [none] | N.C. |
| CN1 | 3 | [none] | N.C. |
| CN1 | 4 | [none] | N.C. |
| CN1 | 5 | PRINTER STROBE | VIO |
| CN1 | 6 | PRINTER CONTROL | VIO/WHT |
| CN1 | 7 | MAGNETS | BRN/WHT |
| CN1 | 8 | [none] | KEY |
| CN1 | 9 | SERVO ENABLE | RED/WHT |
| CN2 | 1 | ENABLE | GRY/BLK |
| CN2 | 2-6 | N.C. | N.C. |
| CN2 | 7 | KEY | KEY |
| CN2 | 8-9 | N.C. | N.C. |
| CN3 | 1 | DATA LINE TO PRINTER | ORG/GRY |
| CN3 | 2 | DATA LINE TO PRINTER | ORG/VIO |
| CN3 | 3 | DATA LINE TO PRINTER | ORG/BLU |
| CN3 | 4 | DATA LINE TO PRINTER | ORG/GRN |
| CN3 | 5 | DATA LINE TO PRINTER | ORG/YEL |
| CN3 | 6 | KEY | KEY |
| CN3 | 7 | DATA LINE TO PRINTER | ORG/BLK |
| CN3 | 8 | DATA LINE TO PRINTER | ORG/RED |
| CN3 | 9 | DATA LINE TO PRINTER | ORG/BRN |
| CN3 | 10 | CB2 METER STROBE | GRY/RED |
| CN3 | 11 | CA2 PRINTER BUSY | ORG/WHT |
| CN3 | 12 | N.C. | [none] |

No line on this sheet runs from CN1, CN2 or CN3 to the servo board; the sheet does not say which CPU lines carry the servo clock and data.

## Creature Head Motion Servo Board (PDF page 27)

Printed text, as read:

> "Serial Data is clocked out of the Main CPU Board to the Monster Head Motion Servo Board at 125 BPS. The data is accompanied by a Transition-Sensitive Clock (both rising and falling transitions) and an Active-High Enable. The CPU sends 8-bit Data Words to the Servo Board to trigger pre-recorded routines stored in the Micro-Controller on the Servo Board itself."

> "Since the clock is Transition-Sensitive, there are only 4 pulses on the clock for each 8-bit Data Word as shown:"

> "Data is sampled a fraction of a second after each transistion to insure a stable read of the Data State." (sic, "transistion")

> "The signal to the Servo Motor consists of a short pulse of +5v ranging in duration from .3 to 1.7 milliseconds, repeating every 16.3ms. The duration of the short pulse determines the Servo's position - at 1 millisecond the Servo is centered. On power-up, the Servo Board will blink it's LED a few times and then send centering signals to all 4 of it's Servo's until it receives a command code from the CPU. (Note: Only Servo Output #1 is being used for the Creature.)"

Waveform captions: "Clock (Ref. Servo Bd. CN1-2)", "Data (Ref. Servo Bd. CN1-3)", "Enable (Ref. Servo Bd. CN1-4)", "Output to Servo Motor". Board caption: "Monster Head Motion Board, PN. 520-5113-00". Side note: "Only Servo Output #1 is being used for the Creature". The schematic draws the board's CN1 inputs and four servo outputs.

## Cabinet Wiring Diagram (PDF page 4)

A box labelled `SHAKER MOTOR BD` with connector `J1` is drawn beside the coin-door block; its line is labelled `BRN/GRY` `PPB J8` `12` `SOLENOID DRIVE 16`. The Coil table (manual PDF 40) and the ROM give driver 16 as the Laser Kick 50v; the sheet is the platform's common cabinet drawing.

## Uncertain readings

- CN1-CN3 wire colours were read on a reduced crop; the labels are certain, the slash-separated colour pairs are the best reading.
