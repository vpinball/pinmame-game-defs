# Bally Elvira and the Party Monsters (1989) — ELVIRA Cabinet Wiring

Source: Bally Midway *Elvira and the Party Monsters* Operations and Parts Information Manual
16-2011-101, IPDB machine 782 file `Elvira_and_the_Partymonsters_OCR_searchable.pdf`, PDF page 94,
printed page 3-2. Read from the native 300 dpi render.

Switch-matrix wiring as drawn:

- CPU board `1J8`/`1P8`: pin 1 labelled `Sw & Col 1` on `GRN-BRN`, carried through `2P1`/`2J1` pin 18
  and `2J18`/`2P18` pin 1 to the cabinet switches; pin 9 labelled `Opto Col 9` on `GRN-GRY`, drawn to
  `2P1` pin 11 and no further on this page.
- CPU board `1J10`/`1P10` rows 1 to 8 on pins 9, 8, 7, 6, 5, 3, 2, 1 (`WHT-BRN` through `WHT-GRY`),
  through `2P1` pins 1-8; on `2P18` row 1 is drawn to pin 12 and rows 3 to 8 to pins 10, 9, 8, 7, 6, 5,
  while row 2 is drawn with no `2P18` pin number.
- Cabinet switches on the column-1 drive, each with its own diode: `7SW2` Plumb Bob Tilt (`7D2`),
  `7SW3` Credit (`7D3`), `7SW4` Right Coin Chute (`7D4`), `7SW5` Center Coin Chute (`7D5`),
  `7SW6` Left Coin Chute (`7D6`), `7SW7` Slam Tilt (`7D7`), `7SW8` High Score Reset (`7D8`), through
  `7P1`/`7J1` pins 5 and 8-12.

Diagnostic inputs as drawn: CPU board `1J14`/`1P14` pin 1 `Memory Protect` (`BLK-RED`, to switch
`7SW76` Memory Protect), pin 2 `Gnd` (`WHT`), pin 3 `ADVANCE` (`GRN`), pin 4 `AUTO/MANUAL` (`BLU`),
through `7P1`/`7J1` pins 13-15 to `7SW75` (ADVANCE) and `7SW74` (AUTO-UP / MANUAL-DOWN).

Flipper circuit as drawn:

- CPU board `1J19`/`1P19` pins 1 and 2, bracketed by one two-line label `Flipper Gnd`, on `ORN-VIO` and
  `ORN-GRY`, through `2P5` pins 5 and 4, `2J5` and `2J10`/`2P10` pins 7 and 8; `2P10-7` (`ORN-VIO`) runs
  to the right flipper button and `2P10-8` (`ORN-GRY`) to the left.
- `Left Flipper Button` and `Right Flipper Button`, each with a `0.1 µF` capacitor, on `2P10`.
- `Playfield Flipper Coils` on `2P8`/`2J8` pins 14 (`BLU-GRY`), 15 (`BLU-VIO`), 8 (`GRY-YEL`) and
  9 (`BLU-YEL`); `Flipper Power` from `5J12`/`5P12` pins 4 and 2 on `BLU-YEL` and `GRY-YEL` through
  `2P5`/`2J5` pins 2 and 3.
- The flipper buttons switch the coil return directly; no matrix switch number is printed anywhere
  in the flipper circuit.

General illumination as drawn: `5.9Vac from Xfmr` (`YEL`, `YEL-WHT`) on `2P6`/`2J6` pins 2 and 7,
through fuse `F2` `5A S-B`, to `2P10` pins 10 and 9 and `7P1`/`7J1` pins 1 and 2, labelled
`General Illumination: Coin Door`.

Audio as drawn: `11J2` audio out/in to the `7R1` 10 kΩ volume control and 47 Ω resistor (cable
`H-8527`); `11J9` to the cabinet bottom speaker on `7P9`/`7J9` and the backbox speaker assembly on
`6P5`/`6J5` through an 11 Ω resistor (cable `H-12299`).
