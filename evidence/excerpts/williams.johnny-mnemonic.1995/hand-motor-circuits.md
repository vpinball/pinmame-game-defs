# Williams Johnny Mnemonic (1995) — Hand Motor Driver, Position Encoders and Hand Motors Circuit

Source: Williams *Johnny Mnemonic* operations manual (September 1995), IPDB machine 3683 file
`Williams_1995_Johnny_Mnemonic_English_Manual.pdf`, PDF pages 128 and 129, printed pages 3-20 and
3-21. Read from the native 300 dpi renders. One transcription, cited by two crops:
`dual-relay-motor-driver` (printed 3-20 connector list) and `hand-motors-circuit` (printed 3-21).

## Dual Relay Motor Driver Assembly A-20532 (printed 3-20), connector list as printed

| Pin | Printed text |
| --- | --- |
| J1-1 | Blue-Gray, sol. #24 Y Motor Enable, from Pwr Dvr Brd J126-8 |
| J1-2 | Blue-Gray, loop from J1-1 |
| J1-3 | Blue-Black, sol. #22 X Motor Enable, from Pwr Dvr Brd J126-6 |
| J1-4 | Blue-Black, loop from J1-3 |
| J1-5 | Blue Violet, sol. #23 Y Motor Direction, from Pwr Dvr Brd J126-7 |
| J1-6 | Blue-Violet, loop from J1-5 |
| J1-7 | Blue-Green, sol. #21 X Motor Direction, from Pwr Dvr Brd J126-5 |
| J1-8 | Blue-Green, loop from J1-7 |
| J1-9 | Key |
| J1-10 | Black, ground from Pwr Dvr Brd J118-3 |
| J1-11 | Red-White, +20V from Pwr Dvr Brd J107-6 |
| J2-1 | Blue-Green, to Load 1 (moves hand left & right) |
| J2-2 | Not Used |
| J2-3 | Key |
| J2-4 | Red-Green. to Load 1( moves hand left & right) |
| J3-1 | Red-Violet, to Load 2 (moves hand in & out) |
| J3-2 | Key |
| J3-3 | Not Used |
| J3-4 | Blue-Violet, to Load 2 (moves hand in & out) |

The schematic below the list labels J1 pins `EN2`, `EN1`, `DIR2`, `DIR1`, `KEY`, `GND` and `+20V`.
Each enable line drives a TIP102 Darlington (`Q1`, `Q2`) that feeds a load; each direction line
switches a `12V DPDT` relay (`RLY2` for load 2 on J3, `RLY1` for load 1 on J2), whose contacts reverse
the load connections. The parts list on printed 2-12 (PDF page 80) lists `RLY1, RLY2 Relay, 12VDC,
DPDT` and `Q1, Q2 Transistor, TIP102, NPN Darl.`

## Position Encoder Board Assembly A-20533 (printed 3-21, upper half)

| Load 1 (moves hand left and right) | Load 2 (moves hand in and out) |
| --- | --- |
| J1-1 Gray-Yellow, +12V | J1-1 Gray-Yellow, +12V |
| J1-2 Black, ground | J1-2 Black, ground |
| J1-3 Key | J1-3 Key |
| J1-4 Green-Violet, sw. col. 7 | J1-4 Green-Violet, sw. col. 7 |
| J1-5 White-Yellow, sw. row 4 | J1-5 White-Blue, sw. row 6 |
| J1-6 White-Green, sw. row 5 | J1-6 White-Violet, sw. row 7 |

The schematic draws two `SHARP GP1A52HR` slotted interrupters (`OPTO1`, `OPTO2`), each switching a
`2N3904` transistor (`Q1`, `Q2`) onto the switch-column line through diodes; `All diodes are 1N4148.`

## Hand Motors Circuit (printed 3-21, lower half)

- Power driver board `J126-8 BLU-GRY SOL. #24 Y MOTOR ENABLE`, `J126-6 BLU-BLK SOL. #22 X MOTOR
  ENABLE`, `J126-7 BLU-VIO SOL. #23 Y MOTOR DIRECTION`, `J126-5 BLU-GRN SOL. #21 X MOTOR DIRECTION`
  into dual relay motor driver board J1 pins 1, 3, 5, 7; `J107-6 RED-WHT +20V` to J1-11;
  `J118-3 GRY-YEL +12V` and `J118-2 BLK GROUND` to J1-10 and on to both encoder boards.
- Driver board `J2-1 BLU-GRN` and `J2-4 RED-GRN` to `LOAD 1 - X MOTOR Moves hand left & right`;
  `J3-1 RED-VIO` and `J3-4 BLU-VIO` to `LOAD 2 - Y MOTOR Moves hand in & out.`
- CPU board `J207-7 GRN-VIO COL. 7` to both encoder boards; `J209-5 WHT-YEL ROW 4` and `J209-6 WHT-GRN
  ROW 5` to the `LOAD 1 POSITION ENCODER BOARD`; `J209-7 WHT-BLU ROW 6` and `J209-8 WHT-VIO ROW 7` to
  the `LOAD 2 POSITION ENCODER BOARD`.

Switch column 7 rows 4-7 are matrix addresses 74-77, printed on the switch matrix as X Hand Encoder A,
X Hand Encoder B, Y Hand Encoder B and Y Hand Encoder A.
