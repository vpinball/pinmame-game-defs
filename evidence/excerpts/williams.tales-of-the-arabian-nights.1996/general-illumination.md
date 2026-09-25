# Tales of the Arabian Nights — General Illumination

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, PDF page 122, printed page
2-40, the General Illumination block printed on the same page as the Solenoid/Flasher Table (see
`solenoid-flasher-wiring.md`). The retained PDF carries a genuine OCR text layer, but the layout
extraction badly garbles multi-column tables, so every cell below was read from the page rendered at
its native 300 dpi. The committed crop shows only the five GI rows; the column headers are printed
once, at the top of the page, and are visible in the `solenoid-flasher-wiring.webp` crop.

The page's column headers, left to right, read literally: Sol. No. | Function | Solenoid Type |
Voltage Connections (Playfield, Backbox, Cabinet) | Drive Xistor | Voltage Connections (Playfield,
Backbox, Cabinet) | Drive Wire Color | Solenoid Part Number / Flashlamp Type (Playfield, Backbox).
Printed page 2-40 repeats "Voltage Connections" over the second connector group; that group is the
drive side (it follows the Drive Xistor column, and the two reprints of this table on PDF pages 2 and
135 head it "Drive Connections"), and the Flipper Circuits sub-table lower on this same page prints
"Drive Connections" over its own connector column. The transcription below labels that second group
"Drive". Each cell is recorded under the column it is printed in; a dash is a genuinely blank printed
cell.

| No. | Function | Type | Voltage PF | Voltage BB | Voltage Cab | Xistor | Drive PF | Drive BB | Drive Cab | Wire | Lamp PF | Lamp BB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | ILLUMINATION STRING 1 | G.I. | — | J106-1 | — | Q5 | — | J106-7 | — | Wht-Brn | #44 | — |
| 02 | ILLUMINATION STRING 2 | G.I. | — | J106-2 | — | Q4 | — | J106-8 | — | Wht-Org | #44 | — |
| 03 | ILLUMINATION STRING 3 | G.I. | — | J106-3 | — | Q3 | — | J106-9 | — | Wht-Yel | #44 | — |
| 04 | \*ILLUMINATION STRING 4 | G.I. | J105-5 | — | — | Q2 | J105-10 | — | — | Wht-Grn | — | #555 |
| 05 | \*ILLUMINATION STRING 5 | G.I. | J105-6 | — | J104-3 | Q1 | J105-11 | — | J104-1 | Wht-Vio | — | #555 |

Footnotes printed at the bottom of the page: "J1XX = POWER DRIVER BOARD", "24-6549 = #44 BULB; 24-8704
= #89 BULB; 24-8768 = #555 BULB; 24-8802 = #906 BULB" and "\*THESE G.I. STRINGS DO NOT BRIGHTEN AND
DIM, THEY ARE ALWAYS ON." The asterisk is printed on strings 04 and 05 only.

## The page contradicts itself

The connector cells and the bulb cells of the same five rows place each string on opposite sides of
the machine:

- Strings 01-03 carry their connectors (`J106-x`) in the **Backbox** connection columns, but their
  `#44` bulb in the **Playfield** flashlamp column.
- Strings 04-05 carry their connectors (`J105-x`) in the **Playfield** connection columns, but their
  `#555` bulb in the **Backbox** flashlamp column.

The same table is printed three times in this manual: here on 2-40 (PDF 122), in the unnumbered front
matter (PDF 2), and in Section 3 (printed 3-5, PDF 135). All three copies carry the same G.I. column
placement, so they are reprints of one table rather than independent sources, and the misprint is
present in each.

Elsewhere on the same page the location columns are used correctly. The Knocker (07) prints `J133-2`
and `J116-8` under Backbox, and the insert-panel companions of flashers 16 and 25-27 print `J134-5`
and `J114-5` / `J108-1..3` under Backbox. The continuation of the Power Driver Board connector list
names those pins for the same locations (read from the rendered pages; the knocker is a backbox coil,
not an insert-panel device):

- Printed 3-27 (PDF 157): `J108-1 Blue-Brown, solenoid 25 drive to insert panel flasher`, `J108-2
  Blue-Red, solenoid 26 drive to insert panel flasher`, `J108-3 Blue-Orange, solenoid 27 drive to
  insert panel flasher`, `J114-5 Brown-Gray, solenoid 16 drive to insert panel flasher`, and
  `J116-8 Violet-Black, solenoid 7 drive to backbox coil`.
- Printed 3-28 (PDF 158): `J134-5 Red-White, +20V to insert panel flasher`. (The same block prints
  its key pin as `J135-4 Key` between `J134-3` and `J134-5`, a typo for J134-4, kept literally.)

## What decides it

The same manual's Power Driver Board Assembly A-20028 connector list (PDF page 156, printed 3-26)
names the pins these rows print, and it names them for the opposite location from the 2-40
connector columns:

- `J106-1/2/3` "Brown/Orange/Yellow, return, G.I. to playfield" and `J106-7/8/9` "White-Brown/
  White-Orange/White-Yellow, 6.8Vac, G.I. to playfield": strings 01-03 by pin, transistor-row order
  and wire colour.
- `J105-5/6` "Green/Violet, return, G.I. to insert panel" and `J105-10/11` "White-Green/White-Violet,
  6.8Vac, G.I. to insert panel": strings 04-05.
- `J104-1/3` "G.I. to Coin Door Board J2-3/J2-5": the cabinet branch of string 05.

The board list agrees with the 2-40 bulb columns and with the always-on footnote (the General
Illumination Circuit page, printed 3-10, draws three triac-switched strings and two always-on
strings). So the connector numbers on 2-40 are right and match the board; what is misprinted is the
**location column** they were entered under for these five rows. Strings 01-03 (public GI 0-2) are
the dimmable playfield strings; strings 04-05 (public GI 3-4) are the always-on backbox insert-panel
strings, and string 05 also feeds the coin-door lamps through `J104`.
