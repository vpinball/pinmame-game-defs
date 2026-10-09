# Demolition Man — Solenoid and Flashlamp Wiring

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF page 110
(printed page `DEMOLITION MAN 3-6`, titled `Solenoid Wiring`) and PDF page 111 (printed page `DEMOLITION MAN 3-7`,
titled `Flashlamp Wiring`). Both are block-wiring drawings: a dashed box for the driver board on the left holds the
connector (a vertical stack of pin-number boxes), each pin has a printed wire name running right, and the wire ends at a
labelled device box carrying `sol. N`. Read from the rendered pages (308 dpi 1-bit scans), not from the OCR text. Wire
names are written exactly as printed (`Violet-Brown`, not `Vio-Brn`); `Brown-Black` and `Red-Brn` are as printed.
The drawings show electrical grouping only; they do not place any device on the playfield, backbox or cabinet, except
that page 111 headings group the flashlamps as `PLAYFIELD FLASHLAMPS` and `BACKBOX FLASHLAMPS`. Pin numbers in each
connector box are exactly the ones printed, in the printed order, which skips numbers (for example `J127` shows `1 3 4 5 6
7 8`).

Image: `solenoid-flasher-wiring.webp` is the Flashlamp Wiring page (PDF page 111); the Solenoid Wiring page (PDF
page 110) is transcribed from its own render.

## Page 110: Solenoid Wiring

All connectors on this page sit inside one dashed box headed `Power Driver PCB`. The page carries no `Playfield`,
`Backbox` or `Cabinet` label.

### Supply wires

| Connector | Pin | Printed wire label | Goes to |
| --- | --- | --- | --- |
| J107 | 3 | Red-Brn, +50V | the common feed line above the row `Ball Release` ... `Knocker` (sol. 1, 2, 3, 4, 5, 7) |
| J107 | 2 | Red-Blk, +50V | the common feed line above the row `Left Slingshot` ... `Diverter Hold` (sol. 9, 10, 11, 12, 13, 14, 15) |
| J118 | 3 | Black, Ground | `DC Motor Control` J1 pin 4 |
| J118 | 2 | Gray-Yellow, +12 | a junction that feeds `Motor EMI PCB` J1 pin 3 and `DC Motor Control` J1 pin 5 |

The punctuation after the wire colour in these four labels (`Red-Brn, +50V`, `Red-Blk, +50V`, `Black, Ground`,
`Gray-Yellow, +12`) prints as a comma or period in the 1-bit scan; it is written as a comma here. The same applies to
`Red-White, +20V` on page 111.

### Motor wiring (J118 / J126)

| Connector | Pin | Printed wire label | Goes to | Device label | sol. |
| --- | --- | --- | --- | --- | --- |
| J126 | 2 | Black-Red | `Motor EMI PCB` J1 pin 1; its J2 pins 1 (Red wire) and 2 (Black wire) then go to the motor | Elevator Motor | sol. 18 |
| J126 | 3 | Black-Orange | `DC Motor Control` J1 pin 2 | Claw Motor Left / Claw Motor Right (one box) | sol. 19, sol. 20 |
| J126 | 4 | Black-Yellow | `DC Motor Control` J1 pin 1 | Claw Motor Left / Claw Motor Right (one box) | sol. 19, sol. 20 |

`Motor EMI PCB` J1 has pins `3` (top) and `1` (bottom); J2 has `1` and `2`. `DC Motor Control` J1 has pins `4`, `5`
(top) and `2`, `1` (bottom); its J2 has `1` and `4`, which carry the `Red` and `Black` wires to one device box printed
`Claw Motor Left` / `Claw Motor Right` / `sol. 19` / `sol. 20`. The drawing does not say which of the two wires
(`Black-Orange`, `Black-Yellow`) is the left motor and which the right.

### Low-power solenoids (J127, +50V via J107-2)

| Connector | Pin | Printed wire label | Device label | sol. |
| --- | --- | --- | --- | --- |
| J127 | 1 | Brown-Black | Left Slingshot | sol. 9 |
| J127 | 3 | Brown-Red | Right Slingshot | sol. 10 |
| J127 | 4 | Brown-Orange | Left Jet Bumper | sol. 11 |
| J127 | 5 | Brown-Yellow | Top Slingshot | sol. 12 |
| J127 | 6 | Brown-Green | Right Jet Bumper | sol. 13 |
| J127 | 7 | Brown-Blue | Ball Eject | sol. 14 |
| J127 | 8 | Brown-Violet | Diverter Hold | sol. 15 |

### High-power solenoids (J130, +50V via J107-3)

| Connector | Pin | Printed wire label | Device label | sol. |
| --- | --- | --- | --- | --- |
| J130 | 1 | Violet-Brown | Ball Release | sol. 1 |
| J130 | 2 | Violet-Red | Bottom Plunger | sol. 2 |
| J130 | 4 | Violet-Orange | Auto Plunger | sol. 3 |
| J130 | 5 | Violet-Yellow | Top Popper | sol. 4 |
| J130 | 6 | Violet-Green | Diverter Power | sol. 5 |
| J130 | 8 | Violet-Black | Knocker | sol. 7 |

Each device box prints its label over `sol. N` in the lower part of the box. No box for sol. 6 or 8, or for sol. 16, is
drawn.

## Page 111: Flashlamp Wiring

Page 111 has two halves separated by a dotted rule: the upper half is headed (right-aligned, italic bold)
`PLAYFIELD FLASHLAMPS` and the lower half `BACKBOX FLASHLAMPS`. The upper half draws two dashed boards, `Power Driver PCB`
(connectors `J107`, `J126`, `J122`) and `8-Driver PCB` (connectors `J4`, `J3`); the lower half draws one dashed board,
`Power Driver PCB` (connectors `J106`, `J125`, `J124`).

### Playfield flashlamps

| Connector | Pin | Printed wire label | Device label | sol. |
| --- | --- | --- | --- | --- |
| J107 | 6 | Red-White, +20V | common feed line over all playfield flashlamp boxes (sol. 17, 21, 22, 23, 24, 25, 26, 27, 28, 37, 38, 39, 40, 41, 42, 43, 44) | |
| J126 | 1 | Black-Brown | Claw Flasher | sol. 17 |
| J126 | 5 | Blue-Green | Jet Flasher | sol. 21 |
| J126 | 6 | Blue-Black | Side Ramp Flasher | sol. 22 |
| J126 | 7 | Blue-Violet | Left Ramp Upper Flasher | sol. 23 |
| J126 | 8 | Blue-Gray | Left Ramp Lower Flasher | sol. 24 |
| J122 | 1 | Blue-Brown | Car Chase Center Flasher | sol. 25 |
| J122 | 2 | Blue-Red | Car Chase Lower Flasher | sol. 26 |
| J122 | 3 | Blue-Orange | Right Ramp Flasher | sol. 27 |
| J122 | 4 | Blue-Yellow | Eject Flasher | sol. 28 |
| J4 (8-Driver PCB) | 2 | Brown-White | Car Chase Upper Flasher | sol. 37 |
| J4 (8-Driver PCB) | 4 | Black-White | Lower Rebound Flasher | sol. 38 |
| J4 (8-Driver PCB) | 5 | Orange-White | Eyeball Flasher | sol. 39 |
| J4 (8-Driver PCB) | 6 | Yellow-White | Center Ramp Flasher | sol. 40 |
| J3 (8-Driver PCB) | 2 | Green-White | Elevator 2 Flasher | sol. 41 |
| J3 (8-Driver PCB) | 3 | Blue-White | Elevator 1 Flasher | sol. 42 |
| J3 (8-Driver PCB) | 4 | Violet-White | Diverter Flasher | sol. 43 |
| J3 (8-Driver PCB) | 5 | Gray-White | Rt. Ramp Upper Flasher | sol. 44 |

The device boxes are drawn in four rows (17, 21, 22, 23, 24 / 25, 26, 27, 28 / 37, 38, 39, 40 / 41, 42, 43, 44), each row on
a branch of the `J107` pin 6 feed. The `Red-White, +20V` label is printed above the first branch. Device box labels
are printed on several lines (for example `Left Ramp` / `Upper` / `Flasher` / `sol. 23`).

### Backbox flashlamps

| Connector | Pin | Printed wire label | Device label | sol. |
| --- | --- | --- | --- | --- |
| J106 | 5 | Red-White, +20V | common feed line over all backbox flashlamp boxes (sol. 17, 21, 22, 23, 24, 25, 26, 27, 28) | |
| J125 | 1 | Black-Brown | Claw Flasher | sol. 17 |
| J125 | 6 | Blue-Green | Jet Flasher | sol. 21 |
| J125 | 7 | Blue-Black | Side Ramp Flasher | sol. 22 |
| J125 | 8 | Blue-Violet | Left Ramp Upper Flasher | sol. 23 |
| J125 | 9 | Blue-Gray | Left Ramp Lower Flasher | sol. 24 |
| J124 | 1 | Blue-Brown | Car Chase Center Flasher | sol. 25 |
| J124 | 2 | Blue-Red | Car Chase Lower Flasher | sol. 26 |
| J124 | 3 | Blue-Orange | Right Ramp Flasher | sol. 27 |
| J124 | 5 | Blue-Yellow | Eject Flasher | sol. 28 |

No backbox flashlamp is drawn for sol. 37-44. The page shows no flipper, coil, general-illumination, magnet or motor wiring,
and no Cryoclaw, cabinet or apron labelling.

## Comparison with the Solenoid/Flasher Table (PDF page 102, reprinted on page 109)

Every connector and pin below matches the table; the differences found are listed after.

Matches checked cell by cell: voltage connectors `J107-3` (Sol. 01-05, 07), `J107-2` (09-15), `J107-6` (17, 21-28, 37-44),
`J106-5` (backbox feed, 17, 21-28), `J118-2` (18-20); drive connectors `J130-1/2/4/5/6/8` (01-05, 07), `J127-1/3/4/5/6/7/8`
(09-15), `J126-1` to `J126-8` (17-24), `J122-1` to `J122-4` (25-28), `J125-1/6/7/8/9` (backbox 17, 21-24), `J124-1/2/3/5`
(backbox 25-28), `J4-2/4/5/6` (37-40), `J3-2/3/4/5` (41-44); drive wire colours (`Vio-*`, `Brn-*`, `Blk-*`, `Blu-*`, `*-Wht`) against
the printed wire names above.

Differences and disagreements:

- Sol. 02 is `Bottom Popper` in the table and the location page, `Bottom Plunger` on the Solenoid Wiring drawing.
- The table puts the Knocker (Sol. 07) voltage (`J107-3`), drive (`J130-8`) and part in its Backbox columns; the Solenoid
  Wiring drawing wires it from the same `J107` pin 3 and `J130` pin 8 as the other high-power solenoids and does not
  mark it as backbox.
- The table lists a `Cabinet` column for voltage and drive connections (`J119-3` and `J119-1` for General Illumination 05
  only); neither wiring page shows `J119`, `J120`, `J121`, `J907` or `J902`, so general illumination and flipper circuits
  are not corroborated on these pages.
- The table lists Sol. 41-44 as 8-driver rows (`J3`); the drawing agrees and places 41-44 in the playfield half only.
- The drawings give the J126 pin-to-device assignment for the motors through `Black-Red` (Elevator Motor), `Black-Orange`
  and `Black-Yellow` (one shared claw motor box); the table's separate rows `Claw Motor Left` (`J126-3`, `Blk-Org`) and
  `Claw Motor Right` (`J126-4`, `Blk-Yel`) are consistent in pin and colour but the drawing does not name which wire is
  left and which right.
- Neither drawing places a device on the Cryoclaw, the cabinet or the apron; the table's Backbox columns for 17 and 21-28
  correspond to the drawing's `BACKBOX FLASHLAMPS` half (same connectors `J106`, `J125`, `J124`).
