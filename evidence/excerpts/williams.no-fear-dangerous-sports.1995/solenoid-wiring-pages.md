# No Fear: Dangerous Sports — Solenoid, flashlamp and G.I. wiring pages

From `Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf` (operations manual 16-50025-101, April 1995, a 144-page scan without a text layer; SHA-256 `176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b`), PDF pages 119-123 (printed 3-6 to 3-10), the coil and flashlamp wiring drawings and the driver-circuit pages. Transcribed from the 200 dpi renders by a delegated reader and not yet checked line by line against the page by the curator. Cells are kept as printed, including misspellings and abbreviations; `—` marks a cell that is blank on the page. `p-NNN` is the PDF page; the printed page number follows it.

## PDF page 119 - printed 3-6 - "SOLENOID WIRING" (heading `COILS`)

A schematic of the Power Driver Board connectors J107, J127 and J130 feeding coil boxes. Printed text labels:

- Connector `J107`: pin `2` `RED-BRN, +50V`; pin `3` `RED-BLK, +50V`. The pin 3 line runs to a bus that feeds the six coils of J127; the pin 2 line runs to the bus that feeds the eight coils of J130.
- Connector `J127` (low-power group): pin 3 `BRN-RED` -> `RIGHT SLINGSHOT SOL. 10`; pin 4 `BRN-ORN` -> `LEFT SLINGSHOT SOL. 11`; pin 5 `BRN-YEL` -> `DROP TARGET UP SOL. 12`; pin 7 `BRN-BLU` -> `TROUGH SOL. 14`; pin 8 `BRN-VIO` -> `EJECT SOL. 15`; pin 9 `BRN-GRY` -> `SKULL MOUTH SOL. 16`.
- Connector `J130` (high-power group): pin 1 `VIO-BRN` -> `RIGHT POPPER SOL. 1`; pin 2 `VIO-RED` -> `AUTOPLUNGER SOL. 2`; pin 4 `VIO-ORG` -> `RIGHT MAGNET SOL. 3`; pin 5 `VIO-YEL` -> `KICKBACK SOL. 4`; pin 6 `VIO-GRN` -> `CENTER MAGNET SOL. 5`; pin 7 `VIO-BLU` -> `LEFT MAGNET SOL. 6`; pin 8 `VIO-BLK` -> `KNOCKER SOL. 7`; pin 9 `VIO-GRY` -> `DROP TARGET DOWN SOL. 8`.
- Box labels: `POWER DRIVER BOARD`, `COILS`. J130 has no pin 3 printed.

---

## PDF page 120 - printed 3-7 - flashlamp wiring (heading `FLASHLAMPS`; continuation of solenoid wiring)

Schematic with sections `PLAYFIELD` and `INSERT PANEL`. Printed labels:

- `J106` pin `5`: `RED-WHT, +20V FOR INSERT PANEL FLASHLAMPS`.
- `J107` pin `6`: `RED-WHT, +20V FOR PLAYFIELD FLASHLAMPS`.
- `J126` (playfield): pin 1 `BLK-BRN SOLENOID 17 FLIPPER RETURN FLASHLAMPS`; pin 2 `BLK-RED SOLENOID 18 SPINNER FLASHLAMP`; pin 3 `BLK-ORG SOLENOID 19 NO FEAR FLASHLAMP`; pin 4 `BLK-YEL SOLENOID 20 RIGHT RAMP FLASHLAMP`; pin 5 `BLU-GRN SOLENOID 21 SKULL FLASHLAMPS`; pin 7 `BLU-VIO SOLENOID 23 LEFT RAMP FLASHLAMP`; pin 8 `BLU-GRY SOLENOID 24 TOP LEFT FLASHLAMP`.
- `J122` (playfield): pin 1 `BLU-BRN SOLENOID 25 AUTOFIRE FLASHLAMPS`; pin 4 `BLU-YEL SOLENOID 28 RIGHT POPPER FLASHLAMP`.
- `J125` (insert panel): pin 5 `BLK-YEL SOLENOID 20 RIGHT RAMP FLASHLAMP`; pin 6 `BLU-GRN SOLENOID 21 SKULL FLASHLAMP`; pin 7 `BLU-BLK SOLENOID 22 INSERT EXPLODE FLASHLAMP`; pin 8 `BLU-VIO SOLENOID 23 LEFT RAMP FLASHLAMPS`.
- `J124` (insert panel): pin 2 `BLU-RED SOLENOID 26 TOP LEFT INSERT FLASHLAMP`; pin 3 `BLU-ORG SOLENOID 27 TOP RIGHT INSERT FLASHLAMP`.
- Bulb symbols drawn per drive line (counted from the drawing, not printed as numbers): playfield J126: sol 17 two, sol 18 one, sol 19 one, sol 20 one, sol 21 two, sol 23 one, sol 24 one; J122: sol 25 two, sol 28 one; insert panel J125: sol 20 two, sol 21 one, sol 22 one, sol 23 two; J124: sol 26 one, sol 27 one. (Bulb types are not printed on this page.)

---

## PDF page 121 - printed 3-8 - "HIGH POWER SOLENOID CIRCUIT" and "LOW POWER SOLENOID CIRCUIT"

Two driver-circuit schematics (not interpreted). Printed labels and text:

- High power: `POWER DRIVER BOARD`, `Drive`, `J113` -> `LS374` -> `A` -> 470 ohm -> `2N5401` (4.7K ohm to `VCC`) -> `B` -> 68 ohm -> `TIP102` (collector `C`, 2.7K ohm) -> `TIP36C` (220 ohm; `1N4004` to `+50V`); output `J130`, `COIL`, wire label `Violet-XXX`; return `Red-Brown` via `J107` and fuse `F105`; power section `J102` pins `9`, `8`, `6`, `5`, fuse `F112`, bridge `BR3`, `100mf 50V`, `10K` ohm, label `Power`.
- Low power: same drive chain with `TIP102` only; output `J127`, `COIL`, wire label `Brown-XXX`; return `Red-Black` via `J107` and fuse `F104`; power section `J102` pins `9`, `8`, `6`, `5`, `F112`, `BR3`, `100mf 50V`, `10K`.
- Text under high power: "The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of the 2N5401 transistor, is high. A high at point "B" causes point "C", the collector of the TIP102 transistor and point "D", the emitter of the TIP36C transistor, to drop low. When point "D" is low, the coil is grounded through the transistor and turns on. The coil shuts off when point "A" toggles high."
- Text under low power: "The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of the 2N5401 transistor, is high. A high at point "B" turns on the TIP102 transistor and causes point "C" to drop low. When point "C" is low the coil is grounded through the transistor and turns on. The coil shuts off when point "A" toggles high."

## PDF page 122 - printed 3-9 - "FLASHLAMP CIRCUIT" and "SPECIAL (GENERAL PURPOSE) SOLENOID CIRCUIT"

- Flashlamp: `J113` -> `LS374` -> `A` -> 470 ohm -> `2N5401` -> `B` -> 68 ohm -> `TIP102` (collector `C`, 2.7K ohm); output `J12X`, `FLASHLAMP`, wire label `Black-XXX`; supply `Red-White` via `J106 or J107`; power section `J102` pins `3`, `4`, `.`(damaged), `2`, fuse `F111`, bridge `BR4`, `15,000mf`, `1.5K` ohm with an LED symbol.
- Special (general purpose): same drive chain, `TIP102`, `1N4004` tieback; output `J12X`, label `FLASHLAMP or COIL`, wire label `Blue-XXX`; supply `Red-White` via `J106 or J107` and fuse `F103`; power section `J102` pins `9`, `8`, `6`, `5`, fuse `F112`, bridge `BR3`, `100mf 50V`, `10K`.
- Texts: flashlamp - "...point "C" the collector of the TIP102 transistor is low. When point "C" is low, the flashlamp is grounded through the transistor and turns on. When point "A" toggles high, the current shuts off."; special - "...When point "C" is low, the coil/flashlamp is grounded through the transistor and turns on. When point "A" toggles high the coil/flashlamp turns off."; footnote `* Tieback diode is not used for flashlamp circuit.`

---

## PDF page 123 - printed 3-10 - "GENERAL ILLUMINATION CIRCUIT" and "BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT"

The page is generic; it carries **no per-string wire colours, no connector pins for individual strings, no location labels per string**. Everything printed:

- Circuit: `POWER DRIVER BOARD`, `Drive`, `J113` -> `LS374` -> `A` -> 560 ohm -> `2N5401` (10K ohm to `VCC`) -> `B` -> 51 ohm -> `C` -> triac; `J115` (two `X` pins, one to ground, one via fuse `S.B.` to `J120`); `J120` (two `X` pins) -> `G.I. LIGHTS` (three bulbs in parallel); label `Power`.
- Text: "When point "A" toggles low, points, "B" and "C" are high. This turns on the triac and the desired general illumination string of lights."
- Block diagram: `6.3 volt secondary` -> `Power Driver Board` (fuse) -> `Playfield or Backbox G.I. Lights. Up to 18 bulbs per string` -> `Power Driver Board` (`Triac Drivers`, `LS374 Latch`); `5 volt secondary` -> `Power Driver Board` `Zero Cross Detection Circuit` -> `CPU Board` `Microprocessor`.

---
