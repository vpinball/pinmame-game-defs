# Safe Cracker — Solenoid, Flasher and General Illumination Wiring Pages

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`, Section 3, PDF pages 130-134 (printed pages `3-6` to `3-10`):
`SOLENOID WIRING` (3-6), `FLASHER WIRING` (3-7), `HIGH POWER SOLENOID CIRCUIT` and `LOW POWER SOLENOID CIRCUIT`
(both on 3-8), `SPECIAL (GENERAL PURPOSE) SOLENOID CIRCUIT` and `FLASHLAMP CIRCUIT` (both on 3-9) and
`GENERAL ILLUMINATION CIRCUIT` with `BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT` (both on 3-10). These pages are wiring
drawings: every printed label is listed per drawing, grouped as printed (top to bottom, left to right). Read from the
rendered pages (300 dpi scan), not from the OCR text. Wire-colour names on these drawings are spelled in full
(`Violet-Brown`), not abbreviated as in the Solenoid/Flasher Table (`Vio-Brn`). A routing statement such as "feeds Sol
n" was traced by eye along the drawn line and is only as reliable as that tracing; the printed labels themselves are
literal.

---

## PDF page 130, printed page 3-6 — SOLENOID WIRING

Title (bold, centred): `SOLENOID WIRING`. The drawing has a vertical bus line on the left (the Power Driver Board edge)
with connectors listed down the left side, power-feed labels along the top, and boxes for each solenoid. A dashed
horizontal line separates the upper box group, labelled `BACKBOX SOLENOIDS` (large thin-stroke text, right of centre),
from the lower groups, labelled `PLAYFIELD SOLENOIDS`. The left margin, level with the lower groups, prints
`Power / Driver / Board` (three lines, large thin text).

### Power feeds at the top (connector, pin, wire colour, voltage as printed)

Each line is a connector label on the left, a boxed pin number, then a wire-colour/voltage label printed above the line.

| Connector | Pin (boxed) | Label printed above the line |
| --- | --- | --- |
| J133 | 2 | `Red-Brown   +50V` |
| J133 | 3 | `Red-Black   +50V` |
| J133 | 1 | `Red-Orange +50V` |
| J135 | 2 | `Red-Brown   +50V` |
| J140 | 2 | `Gray-Yellow  +12V` |
| J138 | 2 | `Gray-Yellow  +12V` |

J133 is drawn as one tall box holding pins `2`, `3`, `1` in that order (top to bottom); J135, J140 and J138 are
single-pin boxes (`2`). Line weights on the page: the J133 pin 2, J133 pin 1 and J140 pin 2 lines are drawn heavy; the
J133 pin 3, J135 pin 2 and J138 pin 2 lines are drawn thin. The six lines run to the right, turn down in nested
rectangles at the right edge and end at the horizontal buses above the solenoid groups (traced by eye: J138 pin 2 to the
bus over Sol 37-40; J140 pin 2 to Sol 26; J135 pin 2 to the Sol 02 / Sol 04 bus; J133 pin 1 to the bus over Sol 25, 27, 28;
J133 pin 3 to the bus over Sol 09-16; J133 pin 2 to the bus over Sol 01-08).

### Backbox solenoids (upper group)

Boxes (text as printed, `Sol nn` on the last line of each box), left to right, top row:

- `AUX. LAMP ENABLE` / `Sol 37`
- `AUX. LAMP CLOCK` / `Sol 38`
- `AUX. LAMP DATA 1` / `Sol 39`
- `AUX. LAMP DATA 2` / `Sol 40`

The four boxes hang from one horizontal bus (connected with dots at three branch points) fed from the J138-2 feed.

Next row, right of centre:

- `TOP LIGHT & MOTOR` / `Sol 26` (printed in four lines: `TOP`, `LIGHT &`, `MOTOR`, `Sol 26`)
- `RIGHT TOKEN TUBE` / `Sol 02` (printed `RIGHT`, `TOKEN`, `TUBE`, `Sol 02`)
- `LEFT TOKEN TUBE` / `Sol 04` (printed `LEFT`, `TOKEN`, `TUBE`, `Sol 04`)

Sol 02 and Sol 04 hang from one bus joined by a dot (the J135 feed).

Connector blocks on the left for the backbox group:

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J110 | 1 | `Brown-White` | Sol 37 |
| J110 | 3 | `Orange-White` | Sol 38 |
| J110 | 4 | `Yellow-White` | Sol 39 |
| J110 | 5 | `Green-White` | Sol 40 |
| J109 | 2 | `Blue-Black` | Sol 26 |
| J118 | 2 | `Violet-Red` | Sol 02 |
| J118 | 5 | `Violet-Yellow` | Sol 04 |

The J110 connector box prints pins `1`, `3`, `4`, `5` (no pin 2); J118 prints pins `2` and `5`; J109 (backbox group) prints
pin `2`.

### Playfield solenoids

Group 1 (top of the playfield area), left to right: `TOP POPPER EJECT` / `Sol 25`; `BOTTOM L.` / `3-BANK` / `Sol 27`
(printed `BOTTOM L.`); `BOTTOM R.` / `3-BANK` / `Sol 28`. Box text for Sol 25 is printed in four lines: `TOP`,
`POPPER`, `EJECT`, `Sol 25`.

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J109 | 1 | `Blue-Green` | Sol 25 |
| J109 | 3 | `Blue-Violet` | Sol 27 |
| J109 | 4 | `Blue-Gray` | Sol 28 |

Group 2, left to right: `TROUGH EJECT` / `Sol 09`; `LEFT SLING` / `Sol 10`; `RIGHT SLING` / `Sol 11`; `LEFT JET` / `Sol 12`;
`RIGHT JET` / `Sol 13`; `TOP JET` / `Sol 14`; `TOP LEFT 3-BANK` / `Sol 15`; `TOP RIGHT 3-BANK` / `Sol 16`.

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J113 | 1 | `Brown-Black` | Sol 09 |
| J113 | 3 | `Brown-Red` | Sol 10 |
| J113 | 4 | `Brown-Orange` | Sol 11 |
| J113 | 5 | `Brown-Yellow` | Sol 12 |
| J113 | 6 | `Brown-Green` | Sol 13 |
| J113 | 7 | `Brown-Blue` | Sol 14 |
| J113 | 8 | `Brown-Violet` | Sol 15 |
| J113 | 9 | `Brown-Gray` | Sol 16 |

The J113 connector box prints pins `1`, `3`, `4`, `5`, `6`, `7`, `8`, `9` (no pin 2); the pin numbers 5-9 are printed rotated.

Group 3 (lowest), left to right: `BIG KICK` / `Sol 01`; `VARI TGT RESET` / `Sol 03`; `BANK KICK` / `Sol 05`; `TOP POPPER UP` /
`Sol 06` (printed `TOP`, `POPPER`, `UP`, `Sol 06`); `RAMP DIVERTER` / `Sol 07`; `KICKBACK (RAMP)` / `Sol 08`.

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J116 | 1 | `Violet-Brown` | Sol 01 |
| J116 | 4 | `Violet-Orange` | Sol 03 |
| J116 | 6 | `Violet-Green` | Sol 05 |
| J116 | 7 | `Violet-Blue` | Sol 06 |
| J116 | 8 | `Violet-Black` | Sol 07 |
| J116 | 9 | `Violet-Gray` | Sol 08 |

The J116 connector box prints pins `1`, `4`, `6`, `7`, `8`, `9`. The `Violet-Black` label is printed `Violet-B!ack` (the `l`
and `a` are damaged in the scan); read as `Violet-Black` [?]. The page carries no fuse, transistor or diode labels. Printed
folio: `3-6`.

---

## PDF page 131, printed page 3-7 — FLASHER WIRING

Title (bold): `FLASHER WIRING`. Left edge: the Power Driver Board vertical line with the label `POWER / DRIVER / BOARD` (three lines,
small capitals). A dashed horizontal line separates `INSERT FLASHERS` (above) from `PLAYFIELD FLASHERS` (below); both
labels are printed in large thin text right of centre.

### Power feeds at the top

| Connector | Pin (boxed) | Label printed above the line |
| --- | --- | --- |
| J133 | 6 | `Red-White      +20V` |
| J134 | 5 | `Red-White      +20V` |

The J133-6 line runs along the right edge to the bus over the playfield flashers (Sol 17-22); the J134-5 line runs to a bus
over the insert flashers (Sol 23, 24) (traced by eye).

### Insert flashers

Boxes: `LIGHT ROPE 1` / `Sol 23` and `LIGHT ROPE 2` / `Sol 24` (each printed `LIGHT`, `ROPE n`, `Sol nn`), hung from one bus with a
dot between them.

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J112 | 8 | `Blue-Orange` | Sol 23 |
| J112 | 9 | `Blue-Yellow` | Sol 24 |

### Playfield flashers

Boxes, left to right: `BACK LEFT` / `Sol 17`; `JETS & BACK R.` / `Sol 18`; `RIGHT MIDDLE` / `Sol 19`; `RIGHT BOTTOM` / `Sol 20`;
`LEFT MIDDLE` / `Sol 21`; `LEFT BOTTOM` / `Sol 22`.

| Connector | Pin | Wire colour printed | Goes to (traced) |
| --- | --- | --- | --- |
| J111 | 1 | `Black-Brown` | Sol 17 |
| J111 | 2 | `Black-Red` | Sol 18 |
| J111 | 3 | `Black-Orange` | Sol 19 |
| J111 | 4 | `Black-Yellow` | Sol 20 |
| J111 | 5 | `Blue-Brown` | Sol 21 |
| J111 | 6 | `Blue-Red` | Sol 22 |

The J111 connector box prints pins `1` to `6`. No transistor, fuse or diode labels are printed. Printed folio: `3-7`.

---

## PDF page 132, printed page 3-8 — HIGH POWER SOLENOID CIRCUIT and LOW POWER SOLENOID CIRCUIT

### HIGH POWER SOLENOID CIRCUIT (upper drawing)

The drawing is enclosed in a dashed outline; the left part is labelled `Drive` (upper left), then `POWER DRIVER BOARD`
(large thin text in the middle left), and the lower part is labelled `Power` (lower left). At the right outside the dashed
outline: `COIL` (large thin text) with a coil symbol.

Drive part: connector `J102` with box labelled `X`; `LS374` (rectangle); point label `A` (output of the LS374, large
thin letter) feeding resistor `470`; `4.7K` resistor from `VCC` (printed `o VCC`) to the base node; transistor `MPSD52` (PNP);
point label `B` (large thin letter at the transistor collector); `1N4004` diode in series; resistor `68`; resistor `2.7K` to
ground node; Darlington `TIP102` (label above it); resistor `220`; diode `1N4004` from `+50V` (printed `o +50V` at the top);
transistor `TIP36C`; point label `C` (large thin letter, beside the TIP36C collector node); no letter `D` is printed on the
diagram (the paragraph below refers to a point `D`). Output connector `J116` with box labelled `X`; the wire label beside it reads
`Violet-XXX`; the line continues to the coil.

Power part: connector `J128` with pins `9`, `8` (upper pair) and `6`, `5` (lower pair); fuse `F108`; bridge of four diodes
labelled `D22`, `D20` (top row) and `D19`, `D21` (bottom row), with the text `all P600D` inside the bridge and `-` and `+`
marks at the bridge sides; capacitor `100mf` / `100V` (printed `100mf` over `100V`); resistor `10K` / `1W` (printed `10K` over
`1W`) in series with an `LED` to ground; `o +50V` supply node; fuse `F102`; connector `J133` with a box labelled `2`; the wire
label beside it reads `Red-Brown`.

Paragraph printed under the drawing (verbatim):

```
The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of the 2N5401
transistor, is high. A high at point "B" causes point "C", the collector of the TIP102 transistor and point
"D", the emitter of the TIP36C transistor, to drop low. When point "D" is low, the coil is grounded through
the transistor and turns on. The coil shuts off when point "A" toggles high.
```

(The paragraph names a `2N5401` transistor and a point `D`; the drawing prints `MPSD52` for that transistor and shows no
letter `D` (the only letters on it are `A`, `B`, `C`). See the notes at the end.)

### LOW POWER SOLENOID CIRCUIT (lower drawing)

Same layout and labels: `Drive`, `J102` (box `X`), `LS374`, `A`, `470`, `4.7K`, `VCC`, `MPSD52`, `B`, `1N4004`, `68`, `2.7K`, `TIP102`,
`C`, `POWER DRIVER BOARD`, `Power`, `J128` pins `9`, `8` and `6`, `5`, fuse `F108`, diodes `D22`, `D20`, `D19`, `D21`, `all P600D`, capacitor
`100mf` / `100V`, `10K` / `1W`, `LED`, `+50V` (two nodes), fuse `F102`, `COIL`. Differences from the high-power drawing: there is
no `TIP36C` transistor and no `220` resistor; the `1N4004` diode runs from `+50V` down to the `TIP102` collector node, which
is labelled `C`, and that node goes directly to the output connector. Output connector `J113` with box `X`, wire label `Brown-XXX`. Supply connector
`J133` with a box labelled `3`; wire label beside it `Red-Black` (the `a` is printed damaged and looks like `c`, so the label
looks like `Red-Blcck`; read as `Red-Black` [?]).

Paragraph under the drawing (verbatim):

```
The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B", the collector of
the 2N5401 transistor, is high. A high at point "B" turns on the TIP102 transistor and causes point "C" to
drop low. When point "C" is low the coil is grounded through the transistor and turns on. The coil shuts
off when point "A" toggles high.
```

Printed folio: `3-8`. Neither drawing carries a part number for the coil or a solenoid number.

---

## PDF page 133, printed page 3-9 — SPECIAL (GENERAL PURPOSE) SOLENOID CIRCUIT and FLASHLAMP CIRCUIT

### SPECIAL (GENERAL PURPOSE) SOLENOID CIRCUIT (upper drawing)

Dashed outline; `Drive`, `POWER DRIVER BOARD`, `Power` labels as on page 132. Right side outside the outline: `FLASHER` /
`or` / `COIL` (printed on three lines) between a coil symbol and a lamp symbol, joined by two vertical lines that continue to
the output connector and to the supply connector.

Drive part: `J102` (box `X`), `LS374`, `A`, `470`, `4.7K`, `VCC`, `MPSD52`, `B`, `1N4004` (series diode), `68`, `2.7K`, `TIP102`, `C`, `1N4004`
(diode from the output node to the connector). Output connector `J109` printed as a two-pin box with two `X` marks
(upper `X` for the diode node, lower `X` for the `TIP102` collector node); wire label beside it `Blue-XXX`.

Power part: `J128` pins `9`, `8` and `6`, `5`; fuse `F108`; bridge with `D22`, `D20`, `D19`, `D21`, `all P600D`; capacitor `100mf` / `100V`;
`10K` / `1W`; `LED`; `o +50V`; fuse `F104`; connector `J133` with a box labelled `1`; wire label beside it `Red-White`.

Text under the drawing (verbatim):

```
The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B" the collector of
the 2N5401 transistor , is high. A high at point "B" causes a low at point "C". When point "C" is low, the
coil/flashlamp is grounded through the transistor and turns on. When point "A" toggles high the
coil/flashlamp turns off.
* Tieback diode is not used for flashlamp circuit.
```

(The line break after `the` and the space before the comma in `transistor , is high` are as printed. No `*` marker is
printed on the drawing itself.)

### FLASHLAMP CIRCUIT (lower drawing)

Title (bold): `FLASHLAMP CIRCUIT`. Dashed outline; `Drive`, `POWER DRIVER BOARD`, `Power`.

Drive part: `J102` (box `X`), `LS374`, `A`, `470`, `4.7K`, `VCC`, `MPSD52`, `B`, `1N4004`, `68`, `2.7K`, `TIP102`, `C`. Output connector `J111` (box `X`);
wire label `Black-XXX`; the line continues to a lamp symbol labelled `FLASHER` (large thin text).

Power part: `J128` with pins `3`, `4` (upper pair) and `1`, `2` (lower pair); fuse `F107`; bridge of four diodes labelled `D16`, `D15` (top)
and `D18`, `D17` (bottom) with `all P600D`; capacitor `10,000mf` / `35V` (printed `10,000mf` over `35V`); resistor `2K` in series with
`LED`; `o +20V`; resistor `0.12` / `10W` (printed `0.12` over `10W`); connector `J133` with a box labelled `6`; wire label beside it
`Red-White`.

Text under the drawing (verbatim):

```
The microprocessor toggles the output of the 74LS374. When point "A" is low, point "B" the collector of
the 2N5401 transistor, is high. Once point "B" is high, point "C" the collector of the TIP102 transistor is
low. When point "C" is low, the flashlamp is grounded through the transistor and turns on. When point
"A" toggles high, the current shuts off.
```

Printed folio: `3-9`.

---

## PDF page 134, printed page 3-10 — GENERAL ILLUMINATION CIRCUIT

### GENERAL ILLUMINATION CIRCUIT, Figure #1 (upper drawing)

Title (bold): `GENERAL ILLUMINATION CIRCUIT`. Dashed outline; `Drive`, `POWER DRIVER BOARD`, `Power`. Right side: `G.I. LIGHTS` (large
thin text) above three lamp symbols wired in parallel.

Drive part: `J102` (box `X`), `LS374`, point `A`, resistor `560`, `4.7K` from `VCC` (printed `VCC` with an overline), transistor `MPSD52`,
point `B`, resistor `51`, point `C`, triac `SC141`. Connector `J103` (upper box `X` to ground; lower box `X` through a fuse
labelled `S.B.`); output connector `J106` (tall box with an `X` at the top and an `X` at the bottom). Caption under the drawing
(bold): `Figure #1`.

### GENERAL ILLUMINATION CIRCUIT, Figure #2 (second drawing)

Dashed outline; `J103` (upper box `X` to ground, lower box `X`), a bridge of four diodes labelled `all P600D`, `J106` (tall box with
an `X` at the top and an `X` at the bottom), `POWER DRIVER BOARD`, `G.I. LIGHTS` with three lamp symbols in parallel. Caption
under the drawing (bold): `Figure #2`.

Text under the figures (verbatim):

```
There are five general illumination strings; three like figure #1 and two like figure #2. When point "A"
toggles low, points, "B" and "C" are high. This turns on the triac and the desired general illumination
string of lights.
```

### BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT

Title (bold): `BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT`. Boxes and labels, left to right and top to bottom:

- `Playfield or Backbox / G.I. Lights.  Up to / 18 bulbs per string.` (dashed box holding three lamp symbols in parallel);
- `Power Driver / Board` (dashed box holding a fuse symbol), fed from a transformer winding labelled `6.3 volt secondary`;
- upper right dashed box holding a bridge of four diodes labelled `all P600D`;
- the word `OR` between the upper right box and the box below it;
- `Power Driver Board` (dashed box) holding two boxes, `Triac / Drivers` and `LS374 / Latch`;
- `Power Driver Board` (dashed box, lower middle) holding `Zero Cross Detection / Circuit`, fed from a second transformer
  winding labelled `5 volt secondary`;
- `CPU Board` (dashed box) holding `Microprocessor`, joined by lines to the Zero Cross Detection Circuit and to the `LS374 / Latch`.

Printed folio: `3-10`. No fuse or connector number is given in the block diagram; the connector `S.B.` fuse of Figure #1 is the
only fuse label on the page.

---

## Notes and reading uncertainties

- `[?]` Page 130: the `Violet-Black` label is printed `Violet-B!ack` (damaged glyphs); read as `Violet-Black`. Its pin (J116-8)
  and destination (Sol 07) agree with the Solenoid/Flasher Table.
- `[?]` Page 132, low-power drawing: the label beside J133 pin 3 is printed `Red-Black` with the `a` glyph damaged
  (`Red-Blcck` look); read as `Red-Black`, which matches `Red-Black` on page 130 for J133 pin 3.
- Page 132, high-power drawing: the paragraph speaks of a point `D` (the emitter of the TIP36C) but the diagram prints no
  letter `D`; the letters printed on the drawing are `A`, `B`, `C` only.
- Printed anomalies worth noting (not reading uncertainties): (a) the J133 pin 1 supply is labelled `Red-Orange +50V` on page 130
  but `Red-White` on the special-solenoid circuit (page 133), where the J133 pin-1 wire shares the `Red-White` label with the
  flasher supply J133 pin 6 on pages 131 and 133; (b) the `HIGH POWER` and `LOW POWER` circuit paragraphs and the
  `Flashlamp` paragraph name the transistor `2N5401` while every drawing prints `MPSD52`; (c) the special-solenoid
  circuit prints fuse `F104` on its +50V branch, whereas the high and low power circuits print `F102` there; (d) the page-130
  `J110` and `J113` connector boxes omit pin 2, as the Solenoid/Flasher Table does; (e) the page-130 feeds `J138-2` and `J140-2`
  are `Gray-Yellow +12V` (the Solenoid/Flasher Table prints no wire colour or voltage for those connections).
- All connector/pin/wire pairs on page 130 (J109, J110, J113, J116, J118) and page 131 (J111, J112) agree with the
  `Drive Playfield`/`Drive Backbox` pins and the colours of the Solenoid/Flasher Table (the table abbreviates, e.g.
  `Vio-Brn` for `Violet-Brown`). The voltage connector pins printed on page 130 (`J133-1`, `-2`, `-3`, `J135-2`, `J138-2`,
  `J140-2`) and page 131 (`J133-6`, `J134-5`) also agree with the table.
