# Black Rose — Solenoid Wiring

Transcribed from `Bally_1992_Black_Rose_Manual.pdf`, PDF page 112, printed page `BLACK ROSE 3-8`, the
`SOLENOID WIRING` drawing. The page is a wiring drawing: the Power Driver Board connectors run down the left edge (the words `Power Driver Board` are printed vertically in the left margin) and each connector pin has a labelled wire running to a labelled box (the coil or flasher, with its name and `Sol NN`). Read from the rendered page (300 dpi image-only scan), not from the OCR text.

Wire colours are printed in full words (`Violet-Brown`, `Black-Orange`, `Blue-Gray`) on this page, unlike the abbreviated colours in the Solenoid/Flasher Table. Connector pin numbers are the numbers printed inside each connector's box, top to bottom, exactly as printed; note the printed pin sequences skip numbers (J123 prints 1, 3, 4, 5; J126 prints 1, 3, 4, 5, 6, 7, 8, 9; J127 prints 1, 3, 4, 6, 7, 8; J130 prints 4, 1, 2, 5, 6, 7, 8, 9; J107 prints 3, 2, 6 and, at the bottom, 6). The pin in each row is the pin whose box edge aligns with that wire label. Every wire-to-block pairing was followed along the drawn line. The Blocks are drawn in four groups (top to bottom): J123 flashers 25-28; J126 flashers 17-24; J127 coils 9-11, 13-15; J130 coils 1-8. Each block also has a second line drawn from its top to a common supply bus; the bus labels are the `J107` wires listed at the end. No notes, legends or footnotes are printed on the page. Solenoids 12 and 16 (Not Used), the G.I. strings and the flipper circuits are not drawn on this page. No connector `J125` appears on this page.

## Flashers and coils by Power Driver Board connector

| Connector | Printed pin | Wire label | Block label (as printed) | Sol |
| --- | --- | --- | --- | --- |
| J123 | 1 | Blue-Brown | Top Popper Flasher | Sol 25 |
| J123 | 3 | Blue-Red | Cannon Flasher | Sol 26 |
| J123 | 4 | Blue-Orange | Fire Button Flasher | Sol 27 |
| J123 | 5 | Blue-Yellow | Right Sword Flasher | Sol 28 |
| J126 | 1 | Black-Brown | Left Bottom Flasher | Sol 17 |
| J126 | 3 | Black-Red | Left Top Flasher | Sol 18 |
| J126 | 4 | Black-Orange | Right Bottom Flasher | Sol 19 |
| J126 | 5 | Black-Yellow | Right Top Flasher | Sol 20 |
| J126 | 6 | Blue-Green | Right Ramp Flasher | Sol 21 |
| J126 | 7 | Blue-Black | Left Ramp Flasher | Sol 22 |
| J126 | 8 | Blue-Violet | Locker Open Flasher | Sol 23 |
| J126 | 9 | Blue-Gray | Left Sword Flasher | Sol 24 |
| J127 | 1 | Brown-Black | Left Ball Lockup | Sol 9 |
| J127 | 3 | Brown-Red | Ramp Up | Sol 10 |
| J127 | 4 | Brown-Orange | Ramp Down | Sol 11 |
| J127 | 6 | Brown-Green | Left Jet Bumper | Sol 13 |
| J127 | 7 | Brown-Blue | Right Jet Bumper | Sol 14 |
| J127 | 8 | Brown-Violet | Bottom Jet Bumper | Sol 15 |
| J130 | 4 | Violet-Orange | Cannon Motor | Sol 3 |
| J130 | 1 | Violet-Brown | Ball Popper | Sol 1 |
| J130 | 2 | Violet-Red | Outhole | Sol 2 |
| J130 | 5 | Violet-Yellow | Ball Release | Sol 4 |
| J130 | 6 | Violet-Green | Right Slingshot | Sol 5 |
| J130 | 7 | Violet-Blue | Left Slingshot | Sol 6 |
| J130 | 8 | Violet-Black | Knocker | Sol 7 |
| J130 | 9 | Violet-Gray | Cannon Kicker | Sol 8 |

## Supply / common wires at connector J107

| Connector | Printed pin | Wire label | Where it goes |
| --- | --- | --- | --- |
| J107 (top) | 3 | Violet-Yellow | Runs right across the top of the page and down the right edge (no block label on the line) |
| J107 (top) | 2 | Violet-Orange | Runs right across the top of the page and down the right edge (no block label on the line) |
| J107 (top) | 6 | Red-White | Feeds the common line above flashers 25-28 and the common lines of flashers 17-24 |
| J107 (lower) | 6 | Red-White | Ends at the Cannon Motor (Sol 3) block only |

The coil group Sol 1, 2, 4, 5, 6, 7, 8 has its own common line above its blocks, separate from the lower Red-White wire, which reaches it from the right-hand vertical supply line; the common bus that feeds the J127 coil group (Sol 9, 10, 11, 13, 14, 15) is likewise a drawn line from the right-hand vertical supply line. Neither common line carries a label of its own; the only labelled supply wires are the J107 wires above. The drawing does not name a supply voltage anywhere. (Corrected after the curator re-read the page: an earlier reading had the lower Red-White wire also feeding the Sol 1-8 common line, which the drawing does not show.)

## Comparison of this page with the Solenoid/Flasher Table (PDF page 109) and Locations list (PDF page 101)

See the report accompanying these files; summary: block names, Sol numbers and wire colours agree with the table for every drawn block. The connector pin numbers on J123 (26-28) and J126 (18-24) differ from the table's pin numbers, and the table's `J125` connector does not appear on the wiring page.
