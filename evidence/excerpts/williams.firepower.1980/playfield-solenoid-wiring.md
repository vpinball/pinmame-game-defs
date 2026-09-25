# Williams Firepower (game 497) — Playfield Solenoid Wiring Diagram

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 25, printed page 25, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 300 dpi render.

Heading, verbatim: `PLAYFIELD SOLENOIDS WIRING DIAGRAM`; caption `Playfield Solenoid Wiring Diagram`.

## Coils, each drawn with a diode across it

| Coil | Printed name | Diode | 8J3/8P3 drive pin |
| --- | --- | --- | --- |
| 8L1 | BALL RELEASE | 8D129 | 17 |
| 8L4 | LEFT EJECT HOLE | 8D132 | 20 |
| 8L5 | RIGHT EJECT HOLE | 8D133 | 21 |
| 8L6 | UPPER RIGHT EJECT HOLE | 8D135 | 22 |
| 8L7 | LEFT BALL SAVER KICKER | 8D136 | 23 |
| 8L8 | BALL RAMP | 8D136 | 24 |
| 8L17 | TOP LEFT JET BUMPER | 8D137 | 11 |
| 8L18 | BOTTOM LEFT JET BUMPER | 8D138 | 12 |
| 8L19 | TOP RIGHT JET BUMPER | 8D139 | 13 |
| 8L20 | BOTTOM RIGHT JET BUMPER | 8D140 | 14 |
| 8L21 | RIGHT KICKER | 8D143 | 15 |
| 8L22 | LEFT KICKER | 8D144 | 16 |

The diode label `8D136` is printed on both 8L7 and 8L8. 8J3/8P3 pins 18 and 19 are drawn with
their wires ending in `N/C`. Pins 1 and 2 carry the coil supply and ground; the harness list below
names them `SOL. B+` and `GRD.`

## Special switches

Six playfield switches are drawn between the ground line and 8J3/8P3 pins 5-10, each with a
22 uF capacitor and a 100 ohm resistor in series across it:

| Switch | Printed name | Capacitor | Resistor | 8J3/8P3 pin |
| --- | --- | --- | --- | --- |
| 8SW65 | TOP LEFT JET BUMPER | 8C1 22 | 8R1 100 | 5 |
| 8SW66 | BOTTOM LEFT JET BUMPER | 8C2 22 | 8R2 100 | 6 |
| 8SW67 | TOP RIGHT JET BUMPER | 8C3 22 | 8R3 100 | 7 |
| 8SW68 | BOTTOM RIGHT JET BUMPER | 8C4 22 | 8R4 100 | 8 |
| 8SW69 | RIGHT KICKER | 8C5 22 | 8R5 100 | 9 |
| 8SW70 | LEFT KICKER | 8C6 22 | 8R6 100 | 10 |

## Flash lamps

`8B65 TYPE 89` and `8B66 TYPE 89`, labelled together `FLASH LAMPS`, drawn one above the other on
one vertical line fed from the solenoid-supply side; below them `8R7 1 1/2W`, and `8R8 330 2W`
from the junction below the lamps to the special-switch ground line. A separate lead leaves this
circuit as `6P2 6J2` to `2J9-5`, `Q43`, `SOL. 15`, `BRN-VIO`.

## Flippers

`8L24` (`LEFT FLIPPER`) with diode `8D146`, and `8L25` (`RIGHT FLIPPER`) with diode `8D148`. Each
coil is drawn with a tap and a switch across part of the winding. Their supply comes on `8J2/8P2`
pins 23 and 24 (`BLU`) from `3P3-4` and `3P3-5`, `FLIPPER B+ FROM POWER SUPPLY`; their returns go on
`8J3/8P3` pins 4 (left, `BLU-GRY`) and 3 (right, `BLU-VIO`) to `7P1-10` and `7P1-8`.

## Harness connectors (driver board side)

| Driver board | Transistor | Wire | Label |
| --- | --- | --- | --- |
| 2J11-9 | Q23 | GRY-GRN | SOL. 5 |
| 2J11-3 | Q25 | GRY-BLU | SOL. 6 |
| 2J11-2 | Q27 | GRY-VIO | SOL. 7 |
| 2J11-8 | Q21 | GRY-YEL | SOL. 4 |
| 2J11-7 | Q19 | GRY-ORN | SOL. 3 |
| 2J11-5 | Q17 | GRY-RED | SOL. 2 |
| 2J11-4 | Q15 | GRY-BRN | SOL. 1 |
| 2J11-1 | Q29 | GRY-BLK | SOL. 8 |
| 3J3-6 (power supply) | -- | RED | SOL. B+ |
| 3J3-3 (power supply) | -- | BLK | GRD. |
| 2J12-7 | Q2 | BLU-BRN | SOL. 17 |
| 2J12-4 | Q4 | BLU-RED | SOL. 18 |
| 2J12-3 | Q6 | BLU-ORG | SOL. 19 |
| 2J12-6 | Q8 | BLU-YEL | SOL. 20 |
| 2J12-8 | Q10 | BLU-GRN | SOL. 21 |
| 2J12-9 | Q12 | BLU-BLK | SOL. 22 |
| 2J12-1 | -- | ORG-VIO | printed `LEFT FLIPPER` |
| 2J12-2 | -- | ORG-GRY | printed `RIGHT FLIPPER` |
| 2J13-5 | -- | ORG-BRN | SOL. 17 SPEC. SW |
| 2J13-3 | -- | ORG-RED | SOL. 18 SPEC. SW |
| 2J13-2 | -- | ORG-BLK | SOL. 19 SPEC. SW |
| 2J13-4 | -- | ORG-YEL | SOL. 20 SPEC. SW |
| 2J13-8 | -- | ORG-GRN | SOL. 21 SPEC. SW |
| 2J13-9 | -- | ORG-BLU | SOL. 22 SPEC. SW |

Inside the dashed `PART OF DRIVER BOARD` box, 2J12 pins 1 and 2 are joined and run through the
contact of relay `Z1` (coil and contact drawn in a dashed sub-box) to ground. On this sheet the
labels beside 2P12-1 and 2P12-2 read `LEFT FLIPPER` and `RIGHT FLIPPER`; the cabinet wiring
diagram (page 24) and Table 3 note 2 of the instruction booklet both put the right flipper button
on `ORN-VIO 2P12-1, 7P1-7` and the left on `ORN-GRY 2P12-2, 7P1-9`. Both leads end on the same Z1
contact, so the two labels here are transposed without any electrical consequence.

A `PART OF CABINET` dashed box draws the `RIGHT FLIPPER BUTTON` across `7J1`/`7P1` pins 9 and 10
and the `LEFT FLIPPER BUTTON` across pins 8 and 7. That matches the sheet's transposed 2P12 labels
but not its own coil side, where `7P1-10` `BLU-GRY` runs to `8P3-4` and `8L24 LEFT FLIPPER` and
`7P1-8` `BLU-VIO` to `8P3-3` and `8L25 RIGHT FLIPPER`; as drawn, the right button would fire the
left coil. The cabinet wiring diagram (see `cabinet-wiring.md`) draws the right button `7SW72` on
7P1-7/7P1-8 and the left button `7SW73` on 7P1-9/7P1-10, which is self-consistent, agrees with
Table 3, and is followed here.
