# Jack*Bot — Section 3 Boards, Wiring Diagrams and Circuit Text

Transcribed from `Williams_1995_Jack_Bot_English_Manual.pdf` (SHA-256
`8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`), Section Three (printed page `3-N` is PDF page
118+N). PDF pages and printed folios used:

| PDF page | Printed folio | Content transcribed here |
| --- | --- | --- |
| 121 | 3-3 | Dedicated Switches and Dedicated Switch Circuit (coin door / control switches) |
| 124 | 3-6 | Solenoid Wiring, Coils & Visor Motor |
| 125 | 3-7 | Flashlamps wiring |
| 128 | 3-10 | General Illumination Circuit and block diagram |
| 129 | 3-11 | Flipper Circuit Diagram (with the boxed Jack*Bot note) |
| 130 | 3-12 | Flipper Coil Circuit, Flipper End-of-Stroke Switch Circuit |
| 131 | 3-13 | Flipper Cabinet Switch Circuit |
| 132 | 3-14 | Flipper Opto Board Assembly A-17316 |
| 133 | 3-15 | Outhole Trough Block Diagram |
| 134 | 3-16 | Trough IR LED Board Assembly A-18617-1 |
| 135 | 3-17 | Trough IR Photo Transistor Board Assembly A-18618-1 |
| 136 | 3-18 | 7-Opto Switch Board and Bracket Assembly A-15595 (pin list) |
| 137 | 3-19 | 7-Opto Switch Board and Bracket Schematic A-15595 |
| 138 | 3-20 | Motor EMI w/Brake Board Assembly A-15340; Visor Motor Circuit |
| 139 | 3-21 | 3-Bank Opto Drop Target Board A-13609; Drop Target Circuit |
| 140 | 3-22 | Coin Door Interface Board A-17051-1 (pin list) |
| 141 | 3-23 | Coin Door Interface Board Schematic A-17051-1 |

The Solenoid/Flashlamp Table reprint on PDF 123 (`3-5`) is covered in `solenoid-flasher-table.md`. The Power Driver
Board connector list (PDF 146-148, `3-28` to `3-30`) is in `power-driver-board.md`. Read from the rendered pages (300 dpi
scan) by the curator, not from the OCR text; every crop was inspected at 0.9x to 1.7x. Drawings are described by their
printed labels; line routing that is not labelled is not asserted.

## Printed page 3-3 (PDF page 121): Dedicated Switches

Heading `DEDICATED SWITCHES`. Drawing: left box `CPU BOARD` with connector `J205` (pins 1, 2, 3, 4, 6, 7, 8, 9, 11), right
box `COIN DOOR INTERFACE BOARD` with connectors `J1` (pins 14, 13, 12, 17, 11, 10, 8, 9, 15) and `J3` (pins 4, 5, 6, 7, 8,
9, 11, 3); on the far right, switch symbols. Each wire line prints wire colour, `(U17-5)` and the switch name:

| CPU J205 pin | Printed wire | Chip pin | Switch | Interface board `J1` pin (drawing) | Interface board `J3` pin (drawing) |
| --- | --- | --- | --- | --- | --- |
| 1 | Orange-Brown | (U17-5) | D1 | 14 | 4 |
| 2 | Orange-Red | (U17-5) | D2 | 13 | 5 |
| 3 | Orange-Black | (U17-5) | D3 | 12 | 6 |
| 4 | Orange-Yellow | (U17-5) | D4 | 17 | (no connection or switch drawn; the wire stops at the J3 side with no pin number) |
| 6 | Orange-Green | (U17-5) | D5 | 11 | 7 |
| 7 | Orange-Blue | (U17-5) | D6 | 10 | 8 |
| 8 | Orange-Violet | (U17-5) | D7 | 8 | 9 |
| 9 | Orange-Gray | (U17-5) | D8 | 9 | 11 |
| 11 | Black | (none) | ground (a ground symbol is drawn on J205-11) | 15 | 3 |

(There is no J205 pin 5 on the drawing. Seven switch symbols are drawn on the right: for J3 pins 4, 5, 6, 7, 8, 9, 11; the
J3 pin 3 line is the common return joined to all switch symbols; the D4 line carries no switch.)

Lists under the drawing (verbatim):

```
Coin Acceptor Switches
D1 - Left Coin Chute
D2 - Center Coin Chute
D3 - Right Coin Chute
D4 - Fourth Coin Chute
```

```
Control Switches
D5 - Normal Function, Service Credits; Test Function, Escape
D6 - Normal Function, Volume Down; Test Function, Down
D7 - Normal Function, Volume Up; Test Function, Up
D8 - Normal Function, Begin Test; Test Function, Enter
```

Heading `DEDICATED SWITCH CIRCUIT`. Circuit drawing: CPU BOARD box with `+5V`, `LS374SC`, `74LS240` (output `C`), `10KΩ`,
`LM339` comparator (node `B` at its output, node `A` at its input), `+12V`, `1.2KΩ`, `1KΩ`, `1N4148`, `470pf`, label
`Dedicated Input`, connector `J205` (pin `X` for the switch line, pin `11` for ground), wire `Orange-XXX` and `Black`
to the `COIN DOOR INTERFACE BOARD` (`X` and `15`; then `X` and `3`) and a switch labelled `Coin Acceptor or Control
Switch`. Truth table as printed:

| SWITCH | A | B | C | |
| --- | --- | --- | --- | --- |
| OPEN | H | H | L | OFF |
| CLOSED | L | L | H | ON |

Text under the circuit (verbatim):

```
The dedicated switches operate similar in the matrix, except that instead of a column circuit there is a
direct tie to ground.  Therefore, the column side is constantly active (low).

When a switch closes, the row side (dedicated input) of the circuit activates.  The "+" input to the LM339
drops below +5V, therefore the output is low.  Since the row circuit (dedicated input) is tied directly to
ground through the switch, the switch is considered closed by the microprocessor.  When the switch
opens, the "+" input to the LM339 is above +5V, it output is high and the row is inactive.
```

## Printed page 3-6 (PDF page 124): Solenoid Wiring, Coils & Visor Motor

Headings: `SOLENOID WIRING` (centre) and `COILS & VISOR MOTOR` (italic, left). Drawing: left box `POWER DRIVER BOARD` with
connectors `J107`, `J118`, `J122`, `J127`, `J130`.

Power and motor lines at the top:

| Connector pin | Printed label | Goes to |
| --- | --- | --- |
| J107-2 | `RED-BRN, +50V` | the right-hand bus that feeds the common (+) end of the `J130` coil row (solenoids 1-8) |
| J107-3 | `RED-BLK, +50V` | the bus that feeds the common (+) end of the `J127` coil row (solenoids 9-14) |
| J118-2 | `GRY-YEL, +12V` | `MOTOR EMI BOARD` connector pin 3 |
| J122-4 | `BLU-YEL` | `MOTOR EMI BOARD` connector pin 1 |

`MOTOR EMI BOARD` (box): left connector pins `3` and `1`; right connector pin `1` → `RED` to the motor, pin `2` → `BLACK`
from the motor. The motor symbol is labelled `VISOR MOTOR SOL. 28`.

Coil boxes (each box prints its name and `SOL. N`), with the connector pin and wire colour that reaches it:

| Coil box (printed) | Sol. | Connector pin | Printed wire |
| --- | --- | --- | --- |
| LEFT SLINGSHOT | SOL. 9 | J127-1 | BRN-BLK |
| RIGHT SLINGSHOT | SOL. 10 | J127-3 | BRN-RED |
| LOWER JET BUMPER | SOL. 11 | J127-4 | BRN-ORN |
| LEFT JET BUMPER | SOL. 12 | J127-5 | BRN-YEL |
| UPPER JET BUMPER | SOL. 13 | J127-6 | BRN-GRN |
| DROP RAMP | SOL. 14 | J127-7 | BRN-BLU |
| BALL RELEASE | SOL. 1 | J130-1 | VIO-BRN |
| NOT USED | SOL. 2 | J130-2 | VIO-RED |
| FAR LEFT EJECT | SOL. 3 | J130-4 | VIO-ORG |
| DROP TARGETS | SOL. 4 | J130-5 | VIO-YEL |
| RIGHT EJECT HOLE | SOL. 5 | J130-6 | VIO-GRN |
| RAISE RAMP | SOL. 6 | J130-7 | VIO-BLU |
| KNOCKER | SOL. 7 | J130-8 | VIO-BLK |
| LEFT EJECT HOLE | SOL. 8 | J130-9 | VIO-GRY |

(The `J127` pin box prints `1, 3, 4, 5, 6, 7` and the `J130` pin box prints `1, 2, 4, 5, 6, 7, 8, 9`; the key pins
`J127-2` and `J130-3` and the flashlamp pins `J127-8`, `J127-9` are not drawn on this page. Solenoids 15 and 16
(`J127-8`, `J127-9`) appear on `3-7`. The `NOT USED / SOL. 2` box is drawn connected like the others, on `J130-2`.)

Notes on this page: the Power Driver Board connector list (`3-29`) prints `J130-2 N/C`, while this drawing and the
Solenoid/Flashlamp Table give `J130-2` the wire `VIO-RED` for the unused solenoid 2.

## Printed page 3-7 (PDF page 125): Flashlamps

Heading `FLASHLAMPS` (italic). Drawing: `POWER DRIVER BOARD` box with `J107` (pin 6, `RED-WHT, +20V`) feeding a bus on the right
to which each lamp symbol is joined, and the drive lines below. Each line prints `wire colour`, `SOLENOID NN`, name and
a lamp symbol:

| Connector pin | Printed wire | Printed solenoid | Printed name |
| --- | --- | --- | --- |
| J127-8 | BRN-VIO | SOLENOID 15 | RIGHT VISOR FLSHRS |
| J127-9 | BRN-GRY | SOLENOID 16 | LEFT VISOR FLSHRS |
| J126-1 | BLK-BRN | SOLENOID 17 | CENTER VISOR FLSHR |
| J126-2 | BLK-RED | SOLENOID 18 | PINBOT FACE FLSHR |
| J126-3 | BLK-ORG | SOLENOID 19 | JET BUMPERS FLSHR |
| J126-4 | BLK-YEL | SOLENOID 20 | LOWER LEFT FLSHR |
| J126-5 | BLU-GRN | SOLENOID 21 | MIDDLE LEFT FLSHR |
| J126-6 | BLU-BLK | SOLENOID 22 | LOWER RIGHT FLSHR |
| J126-7 | BLU-VIO | SOLENOID 23 | BACK PANEL 1 (LEFT) FLSHR |
| J126-8 | BLU-GRY | SOLENOID 24 | BACK PANEL 2 FLSHR |
| J122-1 | BLU-BRN | SOLENOID 22 | BACK PANEL 3 FLSHR |
| J122-2 | BLU-RED | SOLENOID 23 | BACK PANEL 4 FLSHR |
| J122-3 | BLU-ORG | SOLENOID 24 | BACK PANEL 5 (RIGHT) FLSHR |

(13 lamp lines, one lamp symbol each.) Printed anomalies: the three `J122` lines print `SOLENOID 22`, `SOLENOID 23`, `SOLENOID
24`, repeating the numbers of `J126-6`, `J126-7`, `J126-8`; the wire colours (`BLU-BRN`, `BLU-RED`, `BLU-ORG`) and the
Solenoid/Flashlamp Table place them at solenoids 25, 26 and 27. The page prints the plural `FLSHRS` for the two visor
lines (15 and 16). The last lamp (`BACK PANEL 5`) ends the bus with no junction dot. Connector pin boxes drawn: `J127`
pins 8 and 9; `J126` pins 1-8; `J122` pins 1-3.

## Printed page 3-10 (PDF page 128): General Illumination Circuit

Heading `GENERAL ILLUMINATION CIRCUIT`. Circuit labels: box `POWER DRIVER BOARD`, `Drive`, `J113` (pin `X`), `LS374`,
node `A`, `560Ω`, `VCC`, `10K Ω`, transistor `2N5401`, node `B`, `51Ω`, node `C`, a triac, connector `J120` (pin `X` at the
top and `X` at the bottom), connector `J115` (pin `X` to ground and pin `X` through a fuse `S.B.`, label `Power`) and `G.I.
LIGHTS` (three lamps in parallel). Text (verbatim):

```
When point "A" toggles low, points, "B" and "C" are high.  This turns on the triac and the desired general
illumination string of lights.
```

Heading `BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT`. Boxes and labels: `Playfield or Backbox G.I. Lights.  Up to 18
bulbs per string.` (three lamps in parallel); `Power Driver Board` (containing a fuse) fed from `6.3 volt secondary`; `Power Driver
Board` containing `Triac Drivers` and `LS374 Latch`; `Power Driver Board` containing `Zero Cross Detection Circuit` fed
from `5 volt secondary`; `CPU Board` containing `Microprocessor`.

## Printed page 3-11 (PDF page 129): Flipper Circuit Diagram

Heading `FLIPPER CIRCUIT DIAGRAM`. Left: the `FLIPTRONIC II BOARD` (rotated text) with connectors `J907`, `J906`, `J902`, `J905`, `J901`,
a ribbon `J903` to `J202` on `CPU BOARD`; bottom: `POWER DRIVER BOARD` with `J114` (pins 1 2 3 4 5 7), `J104` (pins 2, 1), `J116`
(pin 2); right: coil boxes and `FLIPPER OPTO BOARDS`.

`J907` (pin box prints `4 8 1 6`) feeds four 50V lines, printed above the drawing:

```
RED-BLUE +50V
RED-GRAY +50V
RED-GREEN +50V
RED-VIOLET +50V
```

End-of-stroke switches (`END-OF-STROKE SWITCHES`), connector `J906`:

| J906 pin | Printed wire | Printed name | Switch |
| --- | --- | --- | --- |
| 5 | BLACK-GRAY | U. LEFT FLIPPER* | F7 |
| 3 | BLACK-BLUE | L. LEFT FLIPPER* | F3 |
| 4 | BLACK-VIOLET | U. RIGHT FLIPPER | F5 |
| 1 | BLACK-GREEN | L. RIGHT FLIPPER | F1 |
| 6 | ORANGE | GROUND | (common) |

(The asterisk is printed after `U. LEFT FLIPPER` and `L. LEFT FLIPPER`, not after `U. RIGHT FLIPPER`. Four switch symbols are
drawn, each drawn as an open contact.)

Coil drive lines, connector `J902` (rotated board label `FLIPTRONIC II BOARD`), each ends at a coil box:

| J902 pin | Printed wire | Function | Transistor | Coil box |
| --- | --- | --- | --- | --- |
| 6 | YELLOW-VIOLET | POWER | Q2 | UPPER RIGHT FLIPPER COIL* |
| 4 | ORANGE-VIOLET | HOLD | Q7 | UPPER RIGHT FLIPPER COIL* |
| 13 | YELLOW-GREEN | POWER | Q4 | LOWER RIGHT FLIPPER COIL |
| 11 | ORANGE-GREEN | HOLD | Q11 | LOWER RIGHT FLIPPER COIL |
| 3 | YELLOW-GRAY | POWER | Q1 | UPPER LEFT FLIPPER COIL* |
| 1 | ORANGE-GRAY | HOLD | Q5 | UPPER LEFT FLIPPER COIL* |
| 9 | YELLOW-BLUE | POWER | Q3 | LOWER LEFT FLIPPER COIL |
| 7 | ORANGE-BLUE | HOLD | Q9 | LOWER LEFT FLIPPER COIL |

Cabinet flipper switch lines, connector `J905` (pin box `5 2 3 1 6`):

| J905 pin | Printed wire | Printed name | Switch |
| --- | --- | --- | --- |
| 5 | BLACK-BLUE | U. LEFT FLIPPER | F8 |
| 2 | BLUE-GRAY | L. LEFT FLIPPER | F4 |
| 3 | BLACK-YELLOW | U. RIGHT FLIPPER | F6 |
| 1 | BLUE-VIOLET | L. RIGHT FLIPPER | F2 |
| 6 | ORANGE | GROUND | (common) |

These go to the box `FLIPPER OPTO BOARDS`, which also receives `GRAY-YELLOW +12V` from `J116` (pin 2).

Power connections as printed: `J901` (pins 3 and 1) `WHITE-BLUE 50VAC` (two wires) from `J104` pins 2 and 1; a pin box (pins 4, 5, 1, 2,
unlabelled on this page; the Power Driver Board list `3-28` names it `J904`) with `BLACK GROUND` (pin 4), `BLACK GROUND` (pin 5),
`GRAY +5V` (pin 1), `GRAY-GREEN +12V` (pin 2) from `J114` pins 1-7; the ribbon `J903` goes to `J202` on the `CPU BOARD`.

Boxed note, bold, at the lower right (verbatim; line breaks as printed in the justified block):

```
*IN JACK•BOT, THE UPPER RIGHT E.O.S. SWITCH, (F5), IS USED AS THE VISOR CLOSED SWITCH, AND THE UPPER LEFT E.O.S. SWITCH, (F7), IS USED AS THE VISOR OPEN SWITCH.

THE UPPER RIGHT AND UPPER LEFT FLIPPERS ARE NOT USED.
```

The note is not drawn inside a border; it is a bold text block to the right of the board. The `•` is a bullet between `JACK`
and `BOT`. The asterisk marks the two upper-flipper coil boxes (`UPPER RIGHT FLIPPER COIL*`, `UPPER LEFT FLIPPER COIL*`) and the two
left EOS lines (`U. LEFT FLIPPER*` F7, `L. LEFT FLIPPER*` F3); the page does not explain why the lower left (F3) line carries one
and the upper right (F5) line does not.

## Printed page 3-12 (PDF page 130): Flipper Coil and End-of-Stroke Switch Circuits

Heading `FLIPPER COIL CIRCUIT`, two circuits: `LEFT FLIPPER CIRCUIT` and `RIGHT FLIPPER CIRCUIT`, each a `FLIPTRONIC II BOARD` box with
`J901` (pins 1, 2, 3, 5), bridge `BR1`, capacitor `C2`, two fuses, `J907`, `J902`, `J906` and a `PLAYFIELD` box.

Left flipper circuit as printed:

- `J901` pins 1, 2, 3, 5 into `BR1`; `C2`; fuses `F904` (to `J907` pins 4 and 5, wire `RED-BLUE`) and `F902` (to `J907` pins 8 and 9,
  wire `RED-GRAY`).
- `RED-BLUE` → `LOWER LEFT FLIPPER` coil; `RED-GRAY` → `UPPER LEFT FLIPPER` coil. Each coil drawn with two diodes and a winding.
- `J902` pin 9 `YELLOW-BLUE POWER`, pin 7 `ORANGE-BLUE HOLD` (lower left); pin 3 `YELLOW-GRAY POWER`, pin 1 `ORANGE-GRAY HOLD`
  (upper left).
- `J906` pin 3 `BLACK-BLUE` → `LOWER LEFT E.O.S. SWITCH` (return `ORANGE`); pin 6 ground (`ORANGE`); pin 5 `BLACK-GRAY` →
  `UPPER LEFT E.O.S. SWITCH` (return `ORANGE`).

Right flipper circuit as printed:

- `J901` pins 1, 2, 3, 5 into `BR1`; `C2`; fuses `F903` (to `J907` pins 1 and 2, wire `RED-GREEN`) and `F901` (to `J907` pins 6 and 7,
  wire `RED-VIOLET`).
- `RED-GREEN` → `LOWER RIGHT FLIPPER` coil; `RED-VIOLET` → `UPPER RIGHT FLIPPER` coil.
- `J902` pin 9 `YELLOW-GREEN POWER`, pin 7 `ORANGE-GREEN HOLD` (lower right); pin 3 `YELLOW-VIOLET POWER`, pin 1 `ORANGE-VIOLET HOLD`
  (upper right).
- `J906` pin 1 `BLACK-GREEN` → `LOWER RIGHT E.O.S. SWITCH`; pin 6 ground (`ORANGE`); pin 4 `BLACK-VIOLET` → `UPPER RIGHT E.O.S. SWITCH`.

Printed anomaly: this right flipper circuit prints `J902` pins `9, 7, 3, 1`, the same pin numbers as the left circuit; the
Flipper Circuit Diagram (`3-11`) and the Solenoid/Flashlamp Table print the right-side wires at `J902-13` / `J902-11` (lower right) and
`J902-6` / `J902-4` (upper right). Wire colours agree on every page.

Heading `FLIPPER END-OF-STROKE SWITCH CIRCUIT`. Left: legend

```
F1 LOWER RIGHT FLIPPER
F5 UPPER RIGHT FLIPPER
F3 LOWER LEFT FLIPPER
F7 UPPER LEFT FLIPPER
```

and the italic note (verbatim):

```
Note:
F5 is used as the Visor Closed
switch
F7 is used as the Visor Open
switch.
```

Drawing: `FLIPTRONIC II BOARD`, connector `J906`:

| J906 pin | Printed wire (chip pin) | Switch |
| --- | --- | --- |
| 1 | BLACK-GREEN (U4A-5) | F1 |
| 4 | BLACK-VIOLET (U6A-5) | F5 |
| 3 | BLACK-BLUE (U4C-9) | F3 |
| 5 | BLACK-GRAY (U6C-9) | F7 |
| 6 | ORANGE | (common ground) |

Below, a dedicated-input circuit: `FLIPTRONIC II BOARD`, `+5V`, `+12V`, `HCT244`, `10KΩ`, `1KΩ`, `LM339` (nodes `A`, `B`), `1N4004`, `J906`
(pin `X` and pin `6`), `BLACK-XXX`, `ORANGE`, `PLAYFIELD`, `Dedicated Input`. Truth table:

| SWITCH | A | B | |
| --- | --- | --- | --- |
| OPEN | H | H | OFF |
| CLOSED | L | L | ON |

Text (verbatim):

```
The flipper E.O.S. circuits operate similar to the dedicated switch circuit.  The circuits are active low and
tied to ground through the switch.

When a switch closes, the row side, (dedicated input), of the circuit activates.  The "+" input of the LM339
drops below +5V therefore its output is low.  Since the row (dedicated input), circuit is tied directly to
ground through the switch, the switch is considered closed by the microprocessor.  When the switch
opens, the "+" input to the LM339 is above +5V, its output is high and the row (dedicated input) is
inactive.
```

## Printed page 3-13 (PDF page 131): Flipper Cabinet Switch Circuit

Heading `FLIPPER CABINET SWITCH CIRCUIT`.

Upper drawing: `LEFT FLIPPER OPTO BOARD` and `RIGHT FLIPPER OPTO BOARD` (each with connector `J1`, pins 6, 7, 3, 4, 2, 1 drawn), their
cable plugs (pins 6, 7, 3, 4, 2, 1), `POWER DRIVER BOARD` (`J116`, pin 2) and `FLIPTRONIC II BOARD` (`J905`, pins 6, 2, 5, 1, 3):

| Wire (printed) | Function (printed) | Switch | Left opto board plug | Right opto board plug | Fliptronic J905 pin |
| --- | --- | --- | --- | --- | --- |
| GRAY-YELLOW +12V | (from J116 pin 2) | | 6 (and 7 looped) | 6 (looped from the left board) | (J116-2) |
| ORANGE GROUND | | | 3 (and 4) | 3 (and 4) | 6 |
| BLUE-GRAY | L. LEFT FLIPPER | F4 | 2 | | 2 |
| BLACK-BLUE | U. LEFT FLIPPER | F8 | 1 | | 5 |
| BLUE-VIOLET | L. RIGHT FLIPPER | F2 | | 2 | 1 |
| BLACK-YELLOW | U. RIGHT FLIPPER | F6 | | 1 | 3 |

(The plug pins 6 and 7 / 3 and 4 are drawn as loops joined to the next board; which loop belongs to which wire is read from
the drawing and matches the pin lists on `3-14`.)

Middle drawing: `FLIPTRONIC II BOARD` `J905` with legend

```
F2 LOWER RIGHT FLIPPER
F6 UPPER RIGHT FLIPPER
F4 LOWER LEFT FLIPPER
F8 UPPER LEFT FLIPPER
```

and `FLIPPER OPTO BOARDS` (four opto symbols, resistors and `+12V`):

| J905 pin | Chip pin | Printed wire | Switch |
| --- | --- | --- | --- |
| 3 | (U4B-7) | BLACK-YELLOW | F6 |
| 1 | (U6B-7) | BLUE-VIOLET | F2 |
| 2 | (U4D-11) | BLUE-GRAY | F4 |
| 5 | (U6D-11) | BLACK-BLUE | F8 |
| 6 | | ORANGE | ground |

Lower drawing: a dedicated-input circuit (`FLIPTRONIC II BOARD`, `+5V`, `+12V`, `HCT244`, `10KΩ`, `1KΩ`, `LM339`, `1N4004`, `J905` pin
`X` and pin `5`, wires `BLUE-XXX` / `BLACK-XXX`, `ORANGE`) and a `FLIPPER OPTO BOARD` (`J1` pin `X` and `3` and `6`, an opto, `470Ω`),
with `POWER DRIVER BOARD J116` pin 2 `+12V` as `GRAY-YELLOW`.

Text (verbatim):

```
The flipper switch circuits operate similar to the dedicated switch circuit.  The circuits are active low and
tied to ground through the switch circuit.

When a switch closes, the row side (dedicated input) of the circuit activates.  The "+" input to the LM339
drops below +5V, therefore, its output is low.  Since the row, (dedicated input) circuit is tied directly to
ground through the switch, the switch is considered closed by the microprocessor.  When the switch
opens, the "+" input to the LM339 is above +5V, its output is high and the row, (dedicated Input) is
inactive.
```

## Printed page 3-14 (PDF page 132): Flipper Opto Board Assembly A-17316

Heading `Flipper Opto Board Assembly A-17316`. Drawing: board outline with two opto positions `OPTO1`, `OPTO2`, resistors `R1`, `R2`, and
connector `J1` with silkscreen `SW1`, `SW2`, `GND`, `GND`, `KEY`, `+12V`, `+12V`. Schematic: `R1 470 Ω` and `R2 470 Ω` feed two
LEDs, each facing a phototransistor `OPTO1`, `OPTO2`; connector `J1`:

| J1 pin | Schematic label |
| --- | --- |
| 7 | +12V |
| 6 | +12V |
| 5 | KEY |
| 1 | SW1 |
| 2 | SW2 |
| 3 | GND |
| 4 | GND |

Pin lists (verbatim):

| Left Flipper Opto Board Assembly | Text |
| --- | --- |
| J1-1 | Black-Blue from Fliptronic II Board J905-5 |
| J1-2 | Blue-Gray from Fliptronic II Board J905-2 |
| J1-3 | N/C |
| J1-4 | Orange from Fliptronic II Board J905-6 |
| J1-5 | N/C |
| J1-6 | Gray-Yellow from Power Driver Board J116-2 |
| J1-7 | Gray-Yellow from Power Driver Board J116-2 |

| Right Flipper Opto Board Assembly | Text |
| --- | --- |
| J1-1 | Black-Yellow from Fliptronic II Board J905-1 |
| J1-2 | Blue-Violet from Fliptronic II Board J905-3 |
| J1-3 | Orange from Fliptronic II Board J905-6 |
| J1-4 | Orange from Left Flipper Opto Board Assy J1-4 |
| J1-5 | N/C |
| J1-6 | Gray-Yellow from Left Flipper Opto Board Assy J1-6 |
| J1-7 | N/C |

Printed anomalies: the right board's `J1-1` is listed as `Black-Yellow from Fliptronic II Board J905-1` and `J1-2` as `Blue-Violet from
Fliptronic II Board J905-3`, whereas `3-13` and `3-11` print `Black-Yellow` at `J905-3` and `Blue-Violet` at `J905-1`; the left board
agrees with `3-13`. On the right board `J1-3` is `Orange from ... J905-6` and `J1-4` `Orange from Left Flipper Opto Board`, the
silkscreen calls `3`/`4` `GND`. The silkscreen / schematic place `SW1` on `J1-1` and `SW2` on `J1-2`: so on the left board `J1-1`
(`Black-Blue`, F8, upper left) is `SW1` and `J1-2` (`Blue-Gray`, F4, lower left) is `SW2`; on the right board `J1-1` (`Black-Yellow`,
F6, upper right) is `SW1` and `J1-2` (`Blue-Violet`, F2, lower right) is `SW2`. The page does not say which of `OPTO1`/`OPTO2` is on
which of `SW1`/`SW2` beyond the schematic, which draws `OPTO1` on `SW1` and `OPTO2` on `SW2`.

## Printed page 3-15 (PDF page 133): Outhole Trough Block Diagram

Heading `Outhole Trough Block Diagram`. Four boxes on the left joined to the `7-OPTO SWITCH BOARD` on the right.

`TROUGH IR LED BOARD (GREEN BOARD)`, connector `J1`, to the 7-Opto board `J1`:

| Trough LED board J1 pin | Printed wire | Label | 7-Opto board J1 pin |
| --- | --- | --- | --- |
| 9 | BLK | GROUND | 10 |
| 7 | GRY-BRN | LED 1 | 8 |
| 6 | GRY-RED | LED 2 | 7 |
| 5 | GRY-ORG | LED 3 | 6 |
| 4 | GRY-BLK | LED 4 | 5 |
| 3 | GRY-GRN | LED 5 | 3 |

`TROUGH IR PHOTO TRANSISTOR BOARD (BLUE BOARD)`, connector `J1`, to the 7-Opto board `J2`:

| Photo transistor board J1 pin | Printed wire | Label | 7-Opto board J2 pin |
| --- | --- | --- | --- |
| 1 | GRY-YEL | +12v | 10 |
| 3 | ORG-BRN | PHOTO TRANSISTOR 1 | 7 |
| 4 | ORG-RED | PHOTO TRANSISTOR 2 | 6 |
| 5 | ORG-BLK | PHOTO TRANSISTOR 3 | 5 |
| 6 | ORG-YEL | PHOTO TRANSISTOR 4 | 4 |
| 7 | ORG-GRN | PHOTO TRANSISTOR 5 | 3 |

Power and CPU lines to the 7-Opto board `J3`:

| Source | Printed wire | Label | 7-Opto board J3 pin |
| --- | --- | --- | --- |
| POWER DRIVER BOARD J118-2 | GRY-YEL | +12V | 2 |
| POWER DRIVER BOARD J118-3 | BLK | GND | 3 |
| CPU BOARD J209-1 | WHT-BRN | SW. ROW 1 | 5 |
| CPU BOARD J209-2 | WHT-RED | SW. ROW 2 | 6 |
| CPU BOARD J209-3 | WHT-ORG | SW. ROW 3 | 7 |
| CPU BOARD J209-4 | WHT-YEL | SW. ROW 4 | 8 |
| CPU BOARD J209-5 | WHT-GRN | SW. ROW 5 | 9 |
| CPU BOARD J207-3 | GRN-ORG | SW. COL. 3 | 12 |

(The drawing also shows the `J113` ribbon from the Power Driver Board to `J211` on the CPU Board.)

Lower drawing: `TROUGH IR LED BOARD` (note `REPEATED FOR ALL FIVE LEDS.`, labels `GRY-GRN LED5`, `GRY-BLK LED4`, `GRY-ORG LED3`, `GRY-RED LED2`,
`GRY-BRN LED1`, `BLK, GND`), `TROUGH IR PHOTO TRANSISTOR BOARD` (note `REPEATED FOR ALL FIVE PHOTO TRANSISTORS.`, labels `GRY-YEL, +12V`,
`ORG-BRN PHOTO TRANSISTOR1` through `ORG-GRN PHOTO TRANSISTOR5`) and the `7-OPTO SWITCH BOARD`. Text (verbatim):

```
IN THE OUTHOLE TROUGH CIRCUIT, THE BALL ROLLS BETWEEN THE TROUGH IR LED BOARD AND THE TROUGH IR PHOTO TRANSISTOR BOARD AND BREAKS THE BEAM.  WHEN THE BEAM IS BROKEN, THE SWITCH IS READ AS MADE.
```

(The text is printed in a narrow block with line breaks; the sentence is continuous.)

## Printed page 3-16 (PDF page 134): Trough IR LED Board Assembly A-18617-1

Heading `Trough IR LED Board Assembly (transmitter-green board) A-18617-1`. Board layout with `LED1` to `LED7` and connector `J1` (pins 9 to 1). Schematic with
seven LEDs and the connector `J1` labels:

| J1 pin | Schematic label |
| --- | --- |
| 1 | Ball 6 |
| 2 | Ball 5 |
| 3 | Ball 4 |
| 4 | Ball 3 |
| 5 | Ball 2 |
| 6 | Ball 1 |
| 7 | Jam Ball |
| 8 | Key |
| 9 | Common |

LED labels on the schematic: `LED7 (Ball 6)`, `LED6 (Ball 5)`, `LED5 (Ball 4)`, `LED4 (Ball 3)`, `LED3 (Ball 2)`, `LED2 (Ball 1)`, `LED1 (Jam Ball)`.

Pin list (verbatim):

| Pin | Text |
| --- | --- |
| J1-1 | N/C |
| J1-2 | N/C |
| J1-3 | Gray-Green, LED5, to 7-Opto Switch Board J1-3 |
| J1-4 | Gray-Black, LED4, to 7-Opto Switch Board J1-5 |
| J1-5 | Gray-Orange, LED3, to 7-Opto Switch Board J1-6 |
| J1-6 | Gray-Red, LED2, to 7-Opto Switch Board J1-7 |
| J1-7 | Gray-Brown, LED1, to 7-Opto Switch Board J1-8 |
| J1-8 | Key |
| J1-9 | Black, ground, to 7-Opto Switch Board J1-10 |

Observation: the schematic labels give `J1-4` = `Ball 3` (LED4) and `J1-3` = `Ball 4` (LED5); the pin list wires those to LED4 and LED5.
Pins 1 and 2 (`Ball 6`, `Ball 5`: LED7, LED6) are listed `N/C`.

## Printed page 3-17 (PDF page 135): Trough IR Photo Transistor Board Assembly A-18618-1

Heading `Trough IR Photo Transistor Board Assembly (receiver-blue board) A-18618-1`. Board layout `Q1` to `Q7` and connector `J1` (pins 9 to 1). Schematic labels:
`Q1 (Jam Ball)`, `Q2 (Ball 1)`, `Q3 (Ball 2)`, `Q4 (Ball 3)`, `Q5 (Ball 4)`, `Q6 (Ball 5)`, `Q7 (Ball 6)`. Connector `J1` labels:

| J1 pin | Schematic label |
| --- | --- |
| 1 | Common |
| 2 | Key |
| 3 | Jam Ball |
| 4 | Ball 1 |
| 5 | Ball 2 |
| 6 | Ball 3 |
| 7 | Ball 4 |
| 8 | Ball 5 |
| 9 | Ball 6 |

Pin list (verbatim):

| Pin | Text |
| --- | --- |
| J1-1 | Gray-Yellow, +12V, to 7-Opto Switch Board J2-10 |
| J1-2 | Key |
| J1-3 | Orange-Brown, Photo Transistor 1, to 7-Opto Switch Board J2-7 |
| J1-4 | Orange-Red, Photo Transistor 2, to 7-Opto Switch Board J2-6 |
| J1-5 | Orange-Black, Photo Transistor 3, to 7-Opto Switch Board J2-5 |
| J1-6 | Orange-Yellow, Photo Transistor 4, to 7-Opto Switch Board J2-4 |
| J1-7 | Orange-Green, Photo Transistor  5, to 7-Opto Switch Board J2-3 |
| J1-8 | N/C |
| J1-9 | N/C |

(`Photo Transistor  5` prints two spaces. `J1-1` is labelled `Common` on the schematic but wired `+12V` in the list.)

## Printed pages 3-18 and 3-19 (PDF pages 136, 137): 7-Opto Switch Board and Bracket Assembly A-15595

Heading `7-Opto Switch Board and Bracket Assembly A-15595` (`3-18`) and `7-Opto Switch Board and Bracket Schematic A-15595` (`3-19`).
Board layout on `3-18`: connectors `J1` (10 pins, pin 4 key), `J2` (10 pins), `J3` (12 pins), resistors `R1` to `R29`, `C1`-`C3`, `U1`, `U2`, diodes `D1`-`D9`, `LED1`.

Pin list as printed (`3-18`):

| Pin | Text |
| --- | --- |
| J1-1 | N/C |
| J1-2 | N/C |
| J1-3 | Gray-Green, (LED 5), to Trough IR LED Trough board J1-3 |
| J1-4 | Key |
| J1-5 | Gray-Black, (LED 4), to Trough IR LED Trough board J1-4 |
| J1-6 | Gray-Orange, (LED 3), to Trough IR LED Trough board J1-5 |
| J1-7 | Gray-Red, (LED 2), to Trough IR LED Trough board J1-6 |
| J1-8 | Gray-Brown, (LED 1), to Trough IR LED Trough board J1-7 |
| J1-9 | N/C |
| J1-10 | Black, Ground, to Trough IR LED Trough board J1-9 |
| J2-1 | N/C |
| J2-2 | N/C |
| J2-3 | Orange-Green, (Photo Transistor 5), to Trough IR Photo Transistor Trough board J1-7 |
| J2-4 | Orange-Yellow, (Photo Transistor 4), to Trough IR Photo Transistor Trough board J1-6 |
| J2-5 | Orange-Black, (Photo Transistor 3), to Trough IR Photo Transistor Trough board J1-5 |
| J2-6 | Orange-Red, (Photo Transistor 2), to Trough IR Photo Transistor Trough board J1-4 |
| J2-7 | Orange-Brown, (Photo Transistor 1), to Trough IR Photo Transistor Trough board J1-3 |
| J2-8 | Key |
| J2-9 | N/C |
| J2-10 | Gray-Yellow, +12V, to Trough IR Photo Transistor Trough board J1-1 |
| J3-1 | N/C |
| J3-2 | Gray-Yellow, +12V, from Power Driver board J118-2 |
| J3-3 | Black, Ground, from Power Driver board J118-3 |
| J3-4 | Key |
| J3-5 | White-Brown, switch row 1, from CPU board J209-1 |
| J3-6 | White-Red, switch row 2, from CPU board J209-2 |
| J3-7 | White-Orange, switch row 3, from CPU board J209-3 |
| J3-8 | White-Yellow, switch row 4, from CPU board J209-4 |
| J3-9 | White-Green, switch row 5, from CPU board J209-5 |
| J3-10 | N/C |
| J3-11 | N/C |
| J3-12 | Green-Orange, switch column 3, from CPU board J207-3 |

(`J3-10` prints with a mis-struck glyph, `J3-1D`-like, in the scan; the pin number follows the sequence `J3-9`, `J3-11`.)

Schematic labels (`3-19`), connector by connector:

- `J2`: pin 10 `+12V`, pin 9 `+12V`, pin 8 `KEY`, pin 7 `E1 OPTO1`, pin 6 `E2 OPTO2`, pin 5 `E3 OPTO3`, pin 4 `E4 OPTO4`, pin 3 `E5 OPTO5`, pin 2 `E6 OPTO6`,
  pin 1 `E7 OPTO7`.
- `J1`: pin 9 `CATHODE GND`, pin 10 `CATHODE GND`, pin 4 `KEY`, pin 8 `ANODE LED1` (`R15`), pin 7 `ANODE LED2` (`R16`), pin 6 `ANODE LED3` (`R17`),
  pin 5 `ANODE LED4` (`R18`), pin 3 `ANODE LED5` (`R19`), pin 2 `ANODE LED6` (`R20`), pin 1 `ANODE LED7` (`R21`), each resistor `2W OR 1/2W` to `+12V VCC`.
- `J3`: pin 1 `+12V`, pin 2 `+12V`, pin 3 `GND`, pin 4 `KEY`, pin 5 `R1`, pin 6 `R2`, pin 7 `R3`, pin 8 `R4`, pin 9 `R5`, pin 10 `R6`, pin 11 `R7`, pin 12 `COL.`.
- Seven `LM339` comparator channels (`U1A`-`U1D`, `U2A`-`U2D`; eight outputs drawn with diodes `D1`-`D8`, `D9` on the column line) with `2KΩ` / `100KΩ` / `22KΩ` / `10KΩ` resistors,
  `LED1` with `R29 1.2KΩ`, `C1 100mf`, `C2`, `C3`.

Opto-to-row mapping: the pin lists connect only the trough optos 1-5 (`J2-7` to `J2-3`, `E1` to `E5`) and switch rows 1-5 (`J3-5` to `J3-9`) plus
column 3 (`J3-12`). The schematic names the row outputs `R1` to `R7` (on `J3-5` to `J3-11`) and the opto inputs `E1` to `E7` (on `J2-7` to `J2-1`),
and the comparator wiring between them is not traced here (the crossing lines in the lower half are not resolved at this scan resolution);
by name only, `Ex` goes to `Rx`. `E6`/`E7` (`J2-2`, `J2-1`) and `R6`/`R7` (`J3-10`, `J3-11`) have no external wire in the pin lists
(`N/C`), and `LED6`/`LED7` (`J1-2`, `J1-1`) are `N/C` as well.

## Printed page 3-20 (PDF page 138): Motor EMI w/Brake Board Assembly A-15340 and Visor Motor Circuit

Heading `Motor EMI w/Brake Board Assembly A-15340`. Board layout: `L1`, `R1`, `Q1`, `D1`, `C1`, `L2`, connectors `J1` (3 pins) and `J2` (2 pins).
Schematic labels: `J1` pin 3 (to node joined to `R1 2.2KΩ`, the collector of `Q1 TIP102` and `L1 4.7MH` → `J2` pin 1), `J1` pin 2 `KEY`, `J1` pin 1 (to `D1 1N4004`
and the emitter of `Q1` via `L2 4.7MH` → `J2` pin 2).

Pin list (verbatim):

| Pin | Text |
| --- | --- |
| J1-1 | Blue-Yellow, Visor Motor, solenoid 28 drive, from Power Driver board J122-4 |
| J1-2 | N/C |
| J1-3 | Gray-Yellow, +12V, from Power Driver board J118-2 |
| J2-1 | Red, to Visor Motor |
| J2-2 | Black, from Visor Motor |

Heading `VISOR MOTOR CIRCUIT`. Drawing labels: `POWER DRIVER BOARD` (`J118` pin 2 `GRY-YEL, +12V`; `J122` pin 4 `BLU-YEL`; `J113`), `MOTOR EMI BOARD` (left pins 3 and 1; right pins 1 and 2),
`RED` (pin 1) and `BLACK` (pin 2) to the motor symbol labelled `VISOR MOTOR SOL. 28`; `J211` / `CPU BOARD` / `J202`; `FLIPTRONIC II BOARD` with `J903` and `J906`:

| J906 pin | Printed label |
| --- | --- |
| 4 | BLK-VIO, VISOR CLOSED SW. (F5) |
| 5 | BLK-GRY, VISOR OPEN SW. (F7) |
| 6 | ORANGE, GROUND |

The two switches are drawn as open contact symbols.

## Printed page 3-21 (PDF page 139): 3-Bank Opto Drop Target Board A-13609 and Drop Target Circuit

Heading `3-Bank Opto Drop Target Board A-13609`. Board layout: `OPTO 1`, `OPTO 2`, `OPTO 3`, `D1`, `LED 1`, `R1`-`R4`, connector `J1`. Pin list (verbatim, printed
`Broad` for `Board`):

| Pin | Text |
| --- | --- |
| J1-1 | White-Blue, sw. row 6, from CPU J209-7 |
| J1-2 | White-Violet, sw. row 7, from CPU J209-8 |
| J1-3 | White-Gray, sw. row 8, from CPU J209-9 |
| J1-4 | Green-Brown, sw. col. 1, from CPU J207-1 |
| J1-5 | Key |
| J1-6 | Black, ground, from Power Driver Broad J113-3 |
| J1-7 | Gray-Yellow, +12V, from Power Driver Broad J113-2 |

Schematic labels (`J1` at the right): pin 1 `ROW 6`, pin 2 `ROW 7`, pin 3 `ROW 8`, pin 5 `KEY`, pin 4 `COL. 1` (through diode `D1`), pin 7 `+12VDC`,
pin 6 `GND`. Three photo-coupler channels: `OPTO 3` (LED with `R4`) → `ROW 6` (pin 1); `OPTO 2` (LED with `R3`) → `ROW 7` (pin 2); `OPTO 1` (LED with `R1`) → `ROW 8` (pin 3);
the three transistor emitters join the `COL. 1` line (pin 4) through `D1`. `LED 1` with `R2` is a power indicator on `+12VDC`.

Heading `DROP TARGET CIRCUIT`. Drawing: `POWER DRIVER BOARD` `J118` pin 2 `GRY-YEL, +12V` and pin 3 `BLK, GROUND` to the `3-BANK OPTO DROP TARGET BOARD`
`J1` pins 7 and 6; the `J113` ribbon to `J211`; `CPU BOARD` `J207` pin 1 `GRN-BRN, SW. COL. 1` to `J1` pin 4; `J209` pin 7 `WHT-BLU, SW. ROW 6` to `J1` pin 1,
pin 8 `WHT-VIO, SW. ROW 7` to `J1` pin 2, pin 9 `WHT-GRY, SW. ROW 8` to `J1` pin 3.

Matrix result: the three optos read in switch column 1, rows 6, 7 and 8; `OPTO 3` (leftmost on the board and in the drawing) is row 6, `OPTO 2` row 7, `OPTO 1` row 8.
The page prints no switch numbers and does not say which physical target is `OPTO 1`, `OPTO 2` or `OPTO 3`. (WPC numbers a switch as column-digit then row-digit, which would
make these 16, 17 and 18; that is the curator's inference, not printed here.)

## Printed page 3-22 (PDF page 140): Coin Door Interface Board A-17051-1

Heading `Coin Door Interface Board A-17051-1`. Board layout shows connectors `J1` (11 pins), `J2` (5), `J3` (12), `J4` (labelled; `NRI`), `J5` (13 pins), `J6` (15),
`J7` (11), `J8` (3), `J9` (5), diodes `D1`-`D11`, `SW5`. Pin lists, left column then right column, as printed:

| Pin | Text |
| --- | --- |
| J1-1 | Orange-Gray, ded. switch row 8 form CPU J205-9 |
| J1-2 | Orange-Violet, ded. switch row 7 from CPU J205-8 |
| J1-3 | Orange-Blue, ded. switch row 6 from CPU J205-7 |
| J1-4 | Orange-Green, ded. switch row 5 from CPU J205-6 |
| J1-5 | Orange-Yellow, ded. switch row 4 from CPU J205-4 |
| J1-6 | Orange-Black, ded. switch row 3 from CPU J205-3 |
| J1-7 | Orange-Red, ded. switch row  2 from CPU J205-2 |
| J1-8 | Orange-Brown, ded. switch row  1 from CPU J205-1 |
| J1-9 | Key |
| J1-10 | Black, ground from CPU J205-10 |
| J1-11 | Orange-White, switch enable from CPU J205-12 |
| J2-1 | Black, ground from Power Driver Board J116-3 |
| J2-2 | Gray-Yellow, +12vac for Power Driver Board J116-2 |
| J2-3 | Violet, G.I. from Power Driver Board J119-3 |
| J2-4 | Key |
| J2-5 | White-Violet, G.I. 6.8vac from Power Driver J119-1 |
| J3-1 | Green-Brown, switch column. 1 from CPU J212-1 |
| J3-2 | Green-Red, switch column 2 from CPU J212-2 |
| J3-3 | White-Brown, switch row 1 from CPU J212-4 |
| J3-4 | White-Red, switch row 2 from CPU J212-6 |
| J3-5 | White-Orange, switch row 3 from CPU J212-7 |
| J3-6 | White-Yellow, switch row 4 from CPU J212-8 |
| J3-7 | Key |
| J3-8 | Yellow-Gray, lamp col. 8 from Power Driver J136-3 |
| J3-9 | Red-Blue, lamp row 6 from Power Driver J135-7 |
| J3-10 | Red-Violet, lamp row 7 from Power Driver J135-8 |
| J3-11 | Red-Gray, lamp row 8 from Power Driver J135-9 |
| J4 | Not Used |
| J5-1 | Violet, G.I. return to coin door |
| J5-2 | White-Violet, G.I. 6.8vac to coin door |
| J5-3 | Black, ground to coin door |
| J5-4 | Orange-Brown, ded. switch row 1 to coin door |
| J5-5 | Orange-Red, ded. switch row 2 to coin door |
| J5-6 | Orange-Black, ded. switch row 3 to coin door |
| J5-7 | Orange-Green, ded. switch row 5 to coin door |
| J5-8 | Orange-Blue, ded. switch row 6 to coin door |
| J5-9 | Orange-Violet, ded. switch row 7 to coin door |
| J5-10 | Key |
| J5-11 | Orange-Gray, ded. switch row 8 to coin door |
| J5-12 | Green-Red, switch column 2 to coin door Slam Tilt |
| J5-13 | White-Brown, switch row 1 to coin door Slam Tilt |
| J6 | Not Used |
| J7-1 | Yellow-Gray, lamp column 8 to cabinet |
| J7-2 | N/C |
| J7-3 | Red-Violet, lamp row 7 to cabinet |
| J7-4 | Red-Gray, lamp row 8 to cabinet |
| J7-5 | Key |
| J7-6 | Green-Brown, switch column 1 to cabinet |
| J7-7 | Green-Red, switch column 2 to cabinet |
| J7-8 | White-Orange, switch row 3 to cabinet |
| J7-9 | N/C |
| J7-10 | N/C |
| J7-11 | White-Orange, switch row 3 to cabinet |
| J8-1 | White, switch row to cabinet Slam Tilt |
| J8-2 | Key |
| J8-3 | Green, switch column to cabinet Slam Tilt |
| J9-1 | White-Yellow, switch row 4 to Plumb Bob Tilt |
| J9-2 | Key |
| J9-3 | Green-Brown, switch column 1 to Plumb Bob Tilt |
| J9-4 | White-Red, switch row 2 to Interlock Switch |
| J9-5 | Green-Red, switch column 2 to Interlock Switch |

(Rows: J1 11, J2 5, J3 11, J4 1, J5 13, J6 1, J7 11, J8 3, J9 5 = 61 lines.) Printed anomalies: `J1-1` `form` for `from`; `J2-2` prints
`+12vac` (every other 12 volt line is `+12V`); `J3-1` `column.` with a stray period; `J3` lists 11 pins while the schematic on `3-23`
draws 12 (`J3-12 N/C`); `J7-8` and `J7-11` both print `White-Orange, switch row 3 to cabinet`; `J8-1` and `J8-3` print `switch row` and `switch
column` without a number; `J5` has no dedicated switch row 4 line (`J1-5` carries row 4, but `J5` skips from row 3 (`J5-6`) to row 5 (`J5-7`)).
`J1-10` ground is `CPU J205-10` here but `J205` pin `11` on the Dedicated Switches drawing (`3-3`).

## Printed page 3-23 (PDF page 141): Coin Door Interface Board Schematic A-17051-1

Heading `Coin Door Interface Board Schematic A-17051-1`. Connector labels as printed on the schematic (generic board names; the game wiring names are in `3-22`):

| Connector | Pin: label |
| --- | --- |
| `J1  DEDICATED IN` | 1 `DIG. SW.4`, 2 `DIG. SW.3`, 3 `DIG. SW.2`, 4 `DIG. SW.1`, 5 `COIN4`, 6 `RT. COIN3`, 7 `CN. COIN2`, 8 `LT. COIN1`, 9 `KEY`, 10 `GND`, 11 `ENABLE` |
| `J2  POWER IN` | 5 `6.3VAC`, 4 `KEY`, 3 `6.3VAC`, 2 `+12V`, 1 `GND` |
| `J3  SWITCH/LAMP IN` | 1 `SW. COL.1`, 2 `SW. COL.2`, 3 `SW. ROW1`, 4 `SW. ROW2`, 5 `SW. ROW3`, 6 `SW. ROW4`, 7 `KEY`, 8 `LP. COL.1`, 9 `LP. ROW1`, 10 `LP. ROW2`, 11 `LP. ROW3`, 12 `N/C` |
| `J4  NRI` | 1 `GND`, 2 `+12V`, 3 `N/C`, 4 `N/C`, 5 `N/C`, 6 `ENABLE`, 7 `COIN1`, 8 `COIN2`, 9 `COIN3`, 10 `COIN4` |
| `J5  COIN DOOR` | 13 `SLAM SW. ROW1`, 12 `SLAM SW. COL.1`, 11 `SW.4`, 10 `KEY`, 9 `SW.3`, 8 `SW.2`, 7 `SW.1`, 6 `RT. COIN3`, 5 `CN. COIN2`, 4 `LT. COIN1`, 3 `GND`, 2 `G.I. LAMP`, 1 `G.I. LAMP` |
| `J6  ECA COIN DOOR` | 15 `COIN1`, 14 `COIN2`, 13 `COIN3`, 12 `SELECT`, 11 `COIN 7/8EN`, 10 `COIN 5/6EN`, 9 `COIN4 EN`, 8 `COIN3 EN`, 7 `COIN2 EN`, 6 `COIN1 EN`, 5 `COIN4`, 4 `+12V`, 3 `GND`, 2 `KEY`, 1 `GND` |
| `J7  CABINET` | 1 `LP. COL.1`, 2 `LP. ROW1`, 3 `LP. ROW2`, 4 `LP. ROW3`, 5 `KEY`, 6 `SW. COL.1`, 7 `SW. COL.2`, 8 `SW. ROW3`, 9 `SW. ROW2`, 10 `SW. ROW1`, 11 `SW. ROW3` |
| `J8  SLAM` | 3 `SLAM`, 2 `KEY`, 1 `SLAM` |
| `J9  PLUMB BOB/COIN DOOR` | 1 `PLUMB BOB`, 2 `KEY`, 3 `PLUMB BOB`, 4 `MEM. PROTECT`, 5 `MEM. PROTECT` |

Other labels: an eight-position DIP switch with positions numbered `1`-`8` on one side and `9`-`16` on the other, diodes `D1`-`D11` (`D1`, `D2` in the `J3` switch lines; `D3`, `D4` to the lamp lines; `D5`-`D7` in the
lamp lines to `J7`; `D8`-`D11` in the switch lines to `J7`), and the printed note `NOTE: ALL DIODES ARE 1N4004`.

Differences between the schematic and the `3-22` pin list: `J1` `DIG. SW.4`-`1` sit on the pins that `3-22` names dedicated switch rows 8-5, and `COIN4` to `COIN1` on rows 4-1; `J5` `SW.1`-`SW.4` are the
rows 5, 6, 7, 8 pins (`J5-7`, `J5-8`, `J5-9`, `J5-11`); `J7` pins 1-4 are generic `LP.` names where `3-22` prints lamp column 8, `N/C`, lamp row 7 and lamp row 8; `J9-4`/`J9-5` are `MEM. PROTECT` on
the schematic and `Interlock Switch` row 2 / column 2 in the pin list; `J2` pins 3 and 5 are `6.3VAC` here and `G.I.` `Violet` / `White-Violet 6.8vac` in the list; `J3` pins 8-11 are `LP. COL.1`, `LP. ROW1`-`3` here and
lamp column 8 / rows 6-8 in the list.

## Summary of what the visor, visor switches and drop target pages show

- Visor motor: solenoid 28 (Gen. Purpose in the table, drive transistor `Q20`, `J122-4` `BLU-YEL`, part `14-8023`, assembly `A-20100`) drives one DC motor through the Motor EMI w/Brake Board A-15340: `+12V` on
  `J1-3`, the transistor drive on `J1-1`, motor leads `J2-1` Red and `J2-2` Black. There is one drive line only (no separate direction or enable line is printed) and the board holds a transistor `Q1 TIP102`
  with a diode `D1 1N4004` across the motor side (a brake).
- Visor position: the Jack*Bot note on `3-11` and `3-12` / `3-20` says the upper-right end-of-stroke switch F5 (`J906-4`, `BLACK-VIOLET`, `BLK-VIO`) is the visor closed switch and the upper-left F7
  (`J906-5`, `BLACK-GRAY`, `BLK-GRY`) is the visor open switch; both are wired as normal flipper EOS dedicated inputs to the Fliptronic II board with `ORANGE` ground (`J906-6`), drawn as open contacts. The upper
  flippers themselves are not used (their coil drive lines `Q2`/`Q7` and `Q1`/`Q5` are drawn but listed `NOT USED`). The upper flipper cabinet buttons F6 and F8 are the opto switches on the flipper opto boards.
- Visor flashers: solenoids 15 and 16 (right and left visor flashers, listed Low Power in the table) and 17 (centre visor flasher).
- Drop targets: three optos on board A-13609 read in switch column 1, rows 6, 7 and 8 (`OPTO 3` row 6, `OPTO 2` row 7, `OPTO 1` row 8), powered `+12V` and `GND` from the Power Driver Board
  `J113`-labelled connector (this page prints `J113-2` and `J113-3` where the drawing on the same page prints `J118-2`, `J118-3`). The bank is reset by solenoid 4 `DROP TARGETS` (`J130-5`, `VIO-YEL`).
  Solenoid 14 `DROP RAMP` is a separate coil; the page does not link it to the target circuit.

## Typos and anomalies as printed (collected)

- `3-7`: `J122` flashlamp lines print `SOLENOID 22, 23, 24` (should match solenoids 25-27 by table); `RIGHT VISOR FLSHRS` and `LEFT VISOR FLSHRS` plural.
- `3-12`: right flipper circuit prints `J902` pins `9, 7, 3, 1` instead of `13, 11, 6, 4`.
- `3-14`: right flipper opto board `J1-1` and `J1-2` list `J905-1` and `J905-3` (swapped against `3-13`).
- `3-16`/`3-17`: `J1-1` is `Common` on the receiver schematic but `+12V` in the list; the receiver and transmitter use different pin orders.
- `3-18`: `J3-10` glyph mis-struck; `J1`/`J2` lists say `Trough board` after the board name.
- `3-21`: `Broad` for `Board` twice; the connector is `J113` in the pin list and `J118` in the drawing.
- `3-22`: `form` for `from`; `+12vac`; `column.`; duplicate `J7-8`/`J7-11`; unnumbered `J8` rows/columns.
- `3-3`: `J205-11` ground vs `J205-10` in `3-22`; the drawing's `J1`/`J3` pin numbers (14, 13, 12, 17, 11, 10, 8, 9, 15 and 4-11, 3) match neither `J1` nor `J3` of A-17051-1 but the `J3` numbers equal the `J5` coin door pins.
- `3-6`: `J130-2` drawn wired to solenoid 2 (`VIO-RED`) while the Power Driver list prints `J130-2 N/C`.

## Uncertain readings

- `3-3` (121): J1 pins 14/13/12/17/11/10/8/9/15 read from the diagram at 1.0x; legible but the connector label `J1` there does not match A-17051-1's `J1`.
- `3-13` (131): the pin numbers on the cable plugs of the two flipper opto boards (pins 6, 7, 3, 4 looped) are read from a thin drawing and the pairing of loops was inferred from `3-14`'s pin list.
- `3-19` (137): comparator-to-row routing not traced; by-name mapping only.
- `3-18` (136): `J3-10` pin number glyph is distorted in the scan.
- `3-6` (124): which bus line of `J107` feeds which coil row was read from the drawing routing (line from `J107-2` runs to the far right and down to the `J130` row; line from `J107-3` runs to the `J127` row).
