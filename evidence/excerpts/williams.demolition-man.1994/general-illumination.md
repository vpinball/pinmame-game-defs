# Demolition Man — General Illumination Circuit and G.I. Strings

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, two regions read
from the rendered pages (308 dpi 1-bit scan), not from the OCR text:

- PDF page 114, printed page `DEMOLITION MAN 3-10`, the `General Illumination Circuit` schematic and the
  `Block Diagram of General Illumination Circuit`, with the caption beneath them.
- PDF page 102, printed page `DEMOLITION MAN 2-46`, the `General Illumination` block at the bottom of the
  `SOLENOID/FLASHER TABLE` (the table's column headings are printed once, at the top of PDF page 102; the
  block itself prints no repeated headings). The `Flipper Circuits` block below it is transcribed in
  `flipper-circuits.md`. The G.I. strings also appear, as connector pins, on the Power Driver Board lists
  (`power-driver-board-connectors.md`, J119-J121).

The G.I. circuit is drawn once for the whole game, not per string. The Power Driver Board connector lists
(PDF pages 136-138) and this table are separate prints; where they agree they are not independent confirmation of
one another beyond being two prints of the same board's wiring.

## General Illumination Circuit schematic (PDF page 114, upper drawing)

Labels and values as printed, left to right inside the dashed `POWER DRIVER BOARD` outline:

- `J113` connector, feeding an `LS374` latch (label `LS374`); the latch output is point `A`.
- `A` goes through a `560Ω` resistor to the base of a `2N5401` transistor; a `10K Ω` resistor ties that node to `VCC`.
- The transistor output is point `B`, which goes through a `51 Ω` resistor to point `C`.
- The triac (a triac symbol, named only in the caption) is drawn between the top pin of connector `J120` (marked
  `X`) and the top pin of connector `J115` (marked `X`), which is tied to a ground symbol; point `C` feeds the triac
  gate. The bottom pin of `J115` (`X`) goes through a fuse symbol labelled `S.B` to the bottom pin of `J120` (`X`),
  with the label `Power` printed below. The pin numbers of `J113`, `J115` and `J120` are not printed (each pin is
  marked `X`).
- Outside the outline, from `J120`, the two leads go to three lamps in parallel labelled `G.I. Lights`.
- Labels also printed: `Drive` (above the latch/transistor stage), `POWER DRIVER BOARD`, `J120`, `J115`, `J113`.

Caption printed beneath the block diagram (PDF page 114): `When point "A" toggles low, then points "B" and "C"
are high.  This turns On the triac and the desired General Illumination string lights.`

## Block Diagram of General Illumination Circuit (PDF page 114, lower drawing)

- A `6.3 volt secondary` winding feeds, through a fuse in a box labelled `Power Driver Board`, a lamp box labelled
  `Playfield or Backbox. Up to 18 bulbs.` (three lamp symbols)
- The lamp box is in series with a second box labelled `Power Driver Board` containing `Triac Drivers` and an
  `LS374 Latch` on the return path to the winding.
- A `5 volt secondary` winding feeds a box labelled `Zero Cross Detection Circuit Power Driver Board`, which
  connects to a box labelled `Microprocessor CPU Board`; the CPU board connects to the `LS374 Latch`.

## G.I. block of the solenoid/flasher table (PDF page 102, printed 2-46)

Columns, left to right, as the table prints them: `Sol. No.`, `Function`, `Solenoid Type`, `Voltage Connections`
(`Playfield`, `Backbox`, `Cabinet`), `Drive Transistor` (printed `Drive xister` in the table's heading), `Drive
Connections` (`Playfield`, `Backbox`, `Cabinet`), `Drive Wire Color`, `Solenoid Part No. Flashlamp Type`
(`Playfield`, `Backbox`). Blank cells are printed blank; the rows are numbered `01`-`05`, not with the solenoid
numbers. The heading above the block reads `General Illumination`.

| No. | Function | Type | V playfield | V backbox | V cabinet | Drive transistor | Drive playfield | Drive backbox | Drive cabinet | Drive wire color | Lamp playfield | Lamp backbox |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Back Panel G.I. | G.I. | J121-1 | J120-1 |  | Q18 | J121-7 | J120-7 |  | Wht-Brn | #44 | #555 |
| 02 | Upper Right G.I. | G.I. | J121-2 | J120-2 |  | Q10 | J121-8 | J120-8 |  | Wht-Org | #44 | #555 |
| 03 | Upper Left G.I. | G.I. | J121-3 | J120-3 |  | Q14 | J121-9 | J120-9 |  | Wht-Yel | #44 | #555 |
| 04 | Lower Right G.I. | G.I. | J121-5 | J120-5 |  | Q16 | J121-10 | J120-10 |  | Wht-Grn | #44 | #555 |
| 05 | Lower Left G.I. | G.I. | J121-6 | J120-6 | J119-3 | Q12 | J121-11 | J120-11 | J119-1 | Wht-Vio | #44 | #555 |

The `Note:` line printed directly above the heading (`*Note:  Controlled from the 8-Driver Board, not the Power
Driver Board`) belongs to the asterisked solenoids 37-44 above the block; it is not printed on the G.I. rows.
No G.I. row carries an asterisk.

## Cross-check against the Power Driver Board connector lists (PDF page 137)

| String | Return pins (voltage connection) | 6.8VAC feed pins (drive connection) | Wire colour on the list | Destination printed on the list |
| --- | --- | --- | --- | --- |
| 01 Back Panel | J121-1 Brown return, J120-1 Brown return | J121-7 White-Brown, J120-7 White-Brown | White-Brown | playfield (J121) and backbox (J120) |
| 02 Upper Right | J121-2 Orange return, J120-2 Orange return | J121-8 White-Orange, J120-8 White-Orange | White-Orange | playfield and backbox |
| 03 Upper Left | J121-3 Yellow return, J120-3 Yellow return | J121-9 White-Yellow, J120-9 White-Yellow | White-Yellow | playfield and backbox |
| 04 Lower Right | J121-5 Green return, J120-5 Green return | J121-10 White-Green, J120-10 White-Green | White-Green | playfield and backbox |
| 05 Lower Left | J121-6 Violet return, J120-6 Violet return, J119-3 Violet return | J121-11 White-Violet, J120-11 White-Violet, J119-1 White-Violet | White-Violet | playfield, backbox and `Coin Door Brd` (J119 to `J2-1` and `J2-2`) |

Differences and observations (each printed as stated; none is resolved here):

- The Power Driver Board list prints `J121-4 N/C` and `J120-4 N/C` for the unused pin between the Yellow and
  Green returns; the table's G.I. 03 and 04 rows skip pin 4 accordingly (`J121-3` then `J121-5`).
- Each string's wire colour on the Power Driver Board list is the same on J119, J120 and J121 (`White-Violet`
  is used on all three connectors for string 05); the wire colours are printed `White-Brown`, `White-Orange`,
  `White-Yellow`, `White-Green`, `White-Violet` on the connector lists and abbreviated `Wht-Brn`, `Wht-Org`,
  `Wht-Yel`, `Wht-Grn`, `Wht-Vio` in the table.
- Only string 05 (`Lower Left G.I.`) lists a cabinet connection (`J119-3`, `J119-1`). The Power Driver Board
  list prints J119 as `G.I. to Coin Door Brd`, and the table places J119-3 and J119-1 in the `Lower Left G.I.` row's cabinet cells, so the
  coin-door connection is listed under that string, not as a sixth string.
- The table lists no separate backbox/playfield transistor: one drive transistor per string (`Q18`, `Q10`,
  `Q14`, `Q16`, `Q12`) with the playfield and backbox drive connections in the same row.
- The coin-door interface board's own list (PDF page 130) labels the J119 destination pins `J2-3` (White-Violet,
  G.I. 6.8vac) and `J2-5` (Violet, G.I.); the Power Driver Board list labels them `J2-2` and `J2-1`. See the
  note in `power-driver-board-connectors.md`.
- Bulb types printed: `#44` (playfield column) and `#555` (backbox column) on every G.I. row. The page prints
  `Up to 18 bulbs` per string in the block diagram.
