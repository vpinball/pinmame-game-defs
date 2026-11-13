---
source: pinball_robowar_gottlieb_instruction_manual_2_of_2.pdf
source_sha256: f96ce0b20bebce7fdd085809e00c2eef6cc044957ec3942353f48fd053debb83
locator: PDF pages 16 and 15; printed folios 46 and 45; "TRANSFORMER PANEL/CABINET SCHEMATIC/WIRING DIAGRAM", drawing E-25888 (title block on folio 45; folio 46 is the right-hand continuation and carries no title block; folio 46 page header is cut to "C DIAGRAMS, PARTS LISTS")
method: Visual transcription from the 600 dpi native page render, checked against Windows OCR
transcribed_by: curator transcription
reviewed: false
status: the coin door, 1A7 diode board, A1J5, flipper button, knocker and A3J5 sections were checked against the rendered page; the power, transformer and fuse sections remain a draft; uncertain readings are marked
---

# Gottlieb Robo-War (game #714) - Transformer panel / cabinet schematic and wiring diagram

Folio 45 (PDF page 15) is the left half and folio 46 (PDF page 16) the right half of one drawing; lines that leave folio 45 on the right edge re-enter folio 46 at the left edge. Folio 46 is transcribed first because it carries the cabinet switches and loads.

## Title block (folio 45)

| Field | Printed |
| --- | --- |
| Company | Premier Technology |
| TITLE | TRANSFORMER PANEL/CABINET SCHEMATIC/WIRING DIAGRAM |
| DRAWN | handwritten initials (best reading "G.P.D."; uncertain) |
| APPROVED | handwritten initials "R.H.M." |
| DATE | APR-2-88 |
| Drawing number | E-25888 |

Also printed (folio 45, lower right): "A12 TRANSFORMER PANEL MA-1111 USED WITH SYSTEM 80B". No game number or revision letter is printed in this block.

## Printed notes (folio 45)

NOTES:

1. PRIMARY POWER FUSE VALUES; 110V AC, 5AMP SLO-BLO; 220V AC, 2.5AMP SLO-BLO
2. [boxed XXX] INDICATES WIRE COLOR.
3. A12J7 SHOWN IN 110V AC OPERATION.

Symbols legend: circuit-ground symbol = "CIRCUIT GROUND"; hatched ground symbol = "EARTH GROUND".

COLOR CODE (printed on both folios' conventions; box on folio 45): 0 BLACK, 1 BROWN, 2 RED, 3 ORANGE, 4 YELLOW, 5 GREEN, 6 BLUE, 7 VIOLET, 8 GRAY, 9 WHITE.

## FUSE DESIGNATIONS (folio 45 table, as printed)

| Fuse | Printed designation |
| --- | --- |
| F1 | SOUND POWER SUPPLY (A6) |
| F2 | POWER SUPPLY (A2) |
| F3 | DISPLAYS (32V AC) |
| F4 | SOLENOIDS (+24V DC) |
| F5 | CONTROLLED LAMPS |
| F6 | PLAYFIELD ILLUMINATION |
| F7 | LIGHTBOX ILLUMINATION |
| F8 | PRIMARY POWER (SEE NOTE 1) |
| F9 | DISPLAY FILAMENT (6.2V AC) |
| F9A | DISPLAY FILAMENT (6.2V AC) |
| **[blank]** | **[blank]** (an empty row is printed between F9A and F20) |
| F20 | LINE INPUT (SEE TABLE) |

## Fuse ratings printed on the schematic

| Fuse | Printed rating | Where printed |
| --- | --- | --- |
| F20 | "SEE TABLE": F20, LINE INPUT FUSE; 110V AC, 8AMP, SLO-BLO; 220V AC, 4AMP, SLO-BLO | MA-941 line filter/fuse assembly, wire 766 to 788 |
| F8 | "SEE NOTE 1" | on wire 722 after A12P7 pin 3 |
| F9 | 1A | wire 155, 6.2V AC (DISPLAY FILAMENT ... text runs off the page edge) |
| F9A | 1A ("F9A, 1A") | wire 166, 6.2V AC RETURN (DISPLAY FI... text runs off the page edge) |
| F3 | 1/4A SLO-BLO | wire 177, 32V AC |
| F1 | 1/2A | wire 655, 12V AC |
| F2 | 6-1/4A SLO-BLO | wire 211 to 233, 11V AC |
| F4 | 8A SLO-BLO | wire 266 to 188, 27V AC |
| F6 | 5A SLO-BLO | wire 088 to 066, 6.3V AC |
| F5 | 10A SLO-BLO | wire 300 to 311, 8V AC |
| F7 | 1/2A SLO-BLO | 115V AC to lightbox (A12P8 pin 2) |

## Folio 46: coin door (A10J1 / A10P1)

Connector `A10J1 | A10P1`, pins listed in drawn order top to bottom. A dashed box around the left side is labelled "P/O FRONT DOOR" (coin chute lamps) and encloses the switches and lamps on the A10J1 side. Wire boxes appear on both the J1 side and the P1 side.

| A10 pin | Wire box (J1 side) | Wire box (P1 side) | Printed label / switch at J1 side | Contact symbol drawn | Other end printed |
| --- | --- | --- | --- | --- | --- |
| 12 | `9` | `9` | SLAM SW. (switch connects pin 12 to pin 10) | normally closed (parallel plates with a diagonal slash drawn through them) | P1 side wire `9` goes to "GND" arrow to `1A18J1` |
| 10 | `700` | `700` | other end of SLAM SW. | (see pin 12) | continues to A1J5 pin 10 "SLAM SW." wire 700 |
| 3 | **[blank]** | `255` "+6V DC" | none | n/a | wire 255 +6V DC (route not fully traced) |
| 4 | `411` | `411` | LEFT COIN SW. | normally open (two parallel plates) | wire 411 continues to A1J5 pin 3 "STROBE 1" |
| 5 | `422` | `422` | RIGHT COIN SW. | normally open | wire 422 continues to A1J5 pin 4 "STROBE 2" |
| 6 | `433` | `433` | CENTER COIN SW. | normally open | wire 433 continues to A1J5 pin 5 "STROBE 3" |
| 11 | **[blank]** | `688` "+5V DC" | none | n/a | +5V DC |
| 9 | `533` | `533` | other side of CENTER COIN SW. | (see pin 6) | continues to 1A7J1 pin 4 "CENTER COIN SW. RETURN" |
| 8 | `522` | `522` | other side of RIGHT COIN SW. | (see pin 5) | continues to 1A7J1 pin 3 "RIGHT COIN SW. RETURN" |
| 7 | `511` | `511` | other side of LEFT COIN SW. | (see pin 4) | continues to 1A7J1 pin 2 "LEFT COIN SW. RETURN" |
| 2 | `066` | `066` | COIN CHUTE LAMPS (three lamps drawn in parallel) | lamp symbols | wire 066 on P1 side |
| 1 | `000` | `000` | other side of the three COIN CHUTE LAMPS | lamp symbols | wire 000 on P1 side |

Label printed under the lamp group: "P/O FRONT DOOR". Above the lamps: "COIN CHUTE LAMPS". There is no fuse or lamp part number printed on these lamps.

## Folio 46: A1J5 (to A1 control board)

Connector label `A1J5`; "TO A1 CONTROL BOARD".

| A1J5 pin | Printed signal | Wire box |
| --- | --- | --- |
| 10 | SLAM SW. | `700` |
| 3 | STROBE 1 | `411` |
| 4 | STROBE 2 | `422` |
| 5 | STROBE 3 | `433` |
| 8 | RETURN 6 | `666` |
| 1 | RETURN 7 | `677` |
| 7 | STROBE 5 | `455` |
| 6 | STROBE 4 | `444` |
| 2 | STROBE 0 | `400` |

## Folio 46: 1A7 diode board (1A7J1 / 1A7P1) - cabinet button, tilt and coin-return switches

Printed label: "1A7 DIODE BOARD 1N270 (8)". Dashed box encloses the diode side (1A7P1). Eight diodes are drawn (triangles) in the P1 side on pins 4, 3, 2, 1, 5, 6, 9, 10; pins 8 and 17 are drawn without a diode.

| 1A7 pin | Wire box | Printed label | Contact symbol drawn | Switch other terminal runs to (as drawn) | Diode drawn on P1 side |
| --- | --- | --- | --- | --- | --- |
| 4 | `533` | CENTER COIN SW. RETURN | n/a (line to A10J1 pin 9) | A10J1 pin 9 | yes |
| 3 | `522` | RIGHT COIN SW. RETURN | n/a (line to A10J1 pin 8) | A10J1 pin 8 | yes |
| 2 | `511` | LEFT COIN SW. RETURN | n/a (line to A10J1 pin 7) | A10J1 pin 7 | yes |
| 1 | `500` | PLAY/TEST SW. | normally open (two parallel plates) | STROBE 0 (`400`, A1J5 pin 2) | yes |
| 5 | `544` | REPLAY BUTTON | normally open | STROBE 4 (`444`, A1J5 pin 6) | yes |
| 6 | `555` | PLUMB BOB TILT SW. | normally open | STROBE 5 (`455`, A1J5 pin 7) | yes |
| 8 | `677` | (label "BALL ROLL TILT SW." is printed just above this line; see below) | none on this line | RETURN 7 (`677`, A1J5 pin 1): the line leaves J1 pin 8 to the left and runs down to RETURN 7 | no diode drawn |
| 9 | `300` | LEFT ADVANCE BUTTON | normally open | STROBE 0 (`400`, A1J5 pin 2, shared node with PLAY/TEST SW.) | yes |
| 10 | `311` | RIGHT ADVANCE BUTTON | normally open | STROBE 1 (`411`, A1J5 pin 3) | yes |
| 17 | `666` | (no switch label; wire only) | none | RETURN 6 (`666`, A1J5 pin 8) | no diode drawn |

BALL ROLL TILT SW. is drawn as a second normally open contact directly below PLUMB BOB TILT SW., with a bracket line from each of its terminals up to a dot on each terminal of the plumb-bob contact: the two tilt contacts are in parallel between STROBE 5 (`455`) and wire `555` (1A7 pin 6). Its label sits on the row whose wire box is `677`, but no contact is drawn on the pin 8 line itself.

On the P1 side as drawn: the diode outputs of pins 4, 3, 2, 1, 5 and 6 and the direct line of pin 8 are joined on one vertical line, so they leave the board on pin 8 and wire `677` to RETURN 7 (A1J5 pin 1). The diode outputs of pins 9 and 10 and the direct line of pin 17 are joined on a second vertical line, so they leave on pin 17 and wire `666` to RETURN 6 (A1J5 pin 8). Triangles are drawn pointing toward the connector (left). Dashed arrow from the label "1A7 DIODE BOARD 1N270 (8)" points at the dashed box.

## Folio 46: flipper cabinet switches (A9J1, to playboard A9P1)

Connector `A9J1`; brace label "TO PLAYBOARD A9P1".

| A9J1 pin | Wire box | Printed label | Contact symbol drawn | Other end printed |
| --- | --- | --- | --- | --- |
| 2 | `044` | RIGHT FLIPPER SW. RETURN | normally open (two parallel plates) | `9` "GND" arrow to `2A18J2` |
| 1 | `033` | LEFT FLIPPER SW. RETURN | normally open | `9` "GND" arrow to `2A18J2` |
| 6 | `877` | L2 | none | goes to A3J5 pin 2 "L2" `877` |
| 5 | `500` | SOUND 16 | none | goes to A6J1 pin 9 "SOUND 16" `500` |

No flipper end-of-stroke (EOS) contact, flipper coil or flipper coil connector pin is drawn on either folio. No other cabinet switch (for example a start/credit button) is drawn beyond those listed in this file.

## Folio 46: knocker (A10J3 / A10P3)

| Pin | Wire box | Printed label |
| --- | --- | --- |
| 2 | `888` (both sides) | line from knocker; P3 side continues to A3J5 pin 8 "KNOCKER (SOL.8)" `888` |
| 1 | `222` (both sides) | other end of the coil; P3 side wire `222` loops to the left side of the page (route not traced further) |

"KNOCKER ASSY." (dashed box) contains a coil labelled `5195` with a diode labelled `1N4004` drawn in parallel across the coil.

## Folio 46: speaker and volume control

- SPEAKER #1, 4Ω, 15W, 6-1/2" (terminals marked "-" and "+").
- "-" terminal: wire box `9` "GND" arrow to `1A18J1`.
- "+" terminal: runs to the VOLUME CONTROL 100Ω, 2W wiper; a branch with wire box `022` labelled "TO SPEAKERS #2 AND #3".
- VOLUME CONTROL 100Ω, 2W: one end to wire box `9` "GND" arrow to `1A18J1`, other end runs up and right to the audio supply lines.

## Folio 46: A3J5 (to A3 master driver board)

| A3J5 pin | Printed signal | Wire box |
| --- | --- | --- |
| 2 | L2 | `877` |
| 7 | SOUND 8 | `744` |
| 1 | SOUND 4 | `733` |
| 5 | SOUND 2 | `722` |
| 6 | SOUND 1 | `711` |
| 8 | KNOCKER (SOL. 8) | `888` |
| 3 | GND | `9` (arrow to `1A18J1`) |

## Folio 46: A6J1 and A6J2 (to A6 sound board)

| Connector / pin | Printed signal | Wire box |
| --- | --- | --- |
| A6J1 pin 10 | RESET (overbar) | `300` |
| A6J1 pin 9 | SOUND 16 | `500` |
| A6J1 pin 6 | SOUND 1 | `711` |
| A6J1 pin 3 | SOUND 2 | `722` |
| A6J1 pin 2 | SOUND 4 | `733` |
| A6J1 pin 1 | SOUND 8 | `744` |
| A6J2 pin 9 | AUDIO OUT | `566` |
| A6J2 pin 3 | -12V DC REG. | `533` |
| A6J2 pin 4 | +12V DC REG. | `544` |
| A6J2 pin 1 | DC GND (arrow to `1A18J1`) | `9` |
| A6J2 pin 2 | DC GND | `9` |
| A6J2 pin 8 | ANALOG GND | `9` |
| A6J2 pin 5 | +5V DC | `688` |

## Folio 46: A5J1 (to A5 aux. power supply)

| A5J1 pin | Printed signal | Wire box |
| --- | --- | --- |
| 1 | +12V DC | `200` |
| 9 | +24V DC | `222` |
| 6 | 12V AC | `633` |
| 7 | 12V AC RETURN | `644` |
| 4 | AUDIO OUT | `011` |
| 3 | ANALOG GND | `9` |
| 8 | DC GND (arrow to `1A18J1`) | `9` |
| 10 | +12V DC REG. | `544` |
| 5 | -12V DC REG. | `533` |
| 2 | AUDIO IN | `566` |

## Folio 46: A2 +5V power supply (located in lightbox), A1J1, A10P2

A2 box label: "A2 +5V POWER SUPPLY ( LOCATED IN LIGHTBOX )".

| Connector / pin | Printed signal | Wire box |
| --- | --- | --- |
| A2J1 / J1 pin 2 | GND (arrow to `2A18J1`) | `9` |
| A2J1 / J1 pin 4 | (arrow in) | `200` |
| A2J1 / J1 pin 5 | (arrow in) | `200` |
| A2J1 / J1 pin 6 | +12V DC | `200` |
| J2 / A2J2 pin 3 | +5V DC (SOURCE) | `688` |
| J2 / A2J2 pin 1 | +5V DC (SOURCE), to A1J1 pin 1 | `688` |
| J2 / A2J2 pin 2 | +5V DC (SOURCE), to A1J1 pin 2 | `688` |
| J2 / A2J2 pin 4 | +5V DC (SOURCE) | `688` |
| J2 / A2J2 pin 5 | +5V DC (SOURCE) | `688` |
| A1J1 pin 1 | (from A2J2 pin 1) | `688` |
| A1J1 pin 2 | (from A2J2 pin 2) | `688` |
| A1J1 pin 4 | GND (arrow to `2A18J1`) | `9` |
| A1J1 pin 5 | GND (arrow to `2A18J1`) | `9` |
| A10P2 pin 7 | +5V DC | `688` |
| A10P2 pin 3 | 6.2V AC | `122` |
| A10P2 pin 4 | Vco | `133` |
| A10P2 pin 5 | 6.2V AC RETURN | `144` |
| A10P2 pin 1 | 32V AC | `100` |
| A10P2 pin 9 | GND (arrow to `1A18J1`) | `9` |
| A10P2 pin 6 | RESET (overbar) | `300` |
| A10P2 pin 2 | (no label printed; line runs to A12P2 pin 7 "32V AC RETURN" `111`) | **[blank]** |

A10P2 brace label: "TO 1A4J1 (DISPLAY) VIA A10J2".

## Folio 46: A12J2 / A12P2 (transformer panel connector)

Wire codes are the same on both sides of the connector unless noted. Pins listed in drawn order top to bottom.

| Pin | Wire box | Printed signal (P2 side) |
| --- | --- | --- |
| 8 | `122` | 6.2V AC |
| 9 | `133` | Vco |
| 10 | `144` | 6.2V AC RETURN |
| 6 | `100` | 32V AC |
| 7 | `111` | 32V AC RETURN |
| 11 | `633` | 12V AC |
| 12 | `644` | 12V AC RETURN |
| 4 | `200` | +12V DC |
| 5 | `200` | +12V DC |
| 3 | `222` | +24V DC |
| 15 | `222` | **[blank]** (no signal label printed) |
| 13 | `000` | 6.3V AC RETURN |
| 2 | `255` | +6V DC |
| 14 | `066` | 6.3V AC |

Other labels on the left edge of folio 46 adjacent to A12J2: "...LAMENT)" (end of the display-filament label from folio 45), "R2 ... 5W,WW" (end of the R1/R2 label), "C1 ... 10,000UF 25V", wire `9` "GND" arrow to `2A18J3`.

## Folio 46: A12J1 (to playboard) and ground connector banks

A12J1 (brace label "TO PLAYBOARD"), pins listed in drawn order:

| A12J1 pin | Wire box |
| --- | --- |
| 3 | `222` |
| 2 | `066` |
| 5 | `188` |
| 4 | `255` |
| 6 | `288` |
| 1 | `000` |

Connector banks drawn on the left edge, with no switches or loads: `1A18P3` and `1A18P2` (grouped by the same brace "TO PLAYBOARD"); `1A18P1 | 1A18J1` (eight pins on the P1 side tied to a common line, eight output arrows on the J1 side); `2A18P3 | 2A18J3` (output arrows labelled "TO C1 (NEG. SIDE)", "TO +12V DC BRIDGE", "TO +24V DC BRIDGE", "TO +6V DC BRIDGE"); `2A18P2 | 2A18J2` (two arrows, plus six lines to A9J2 pins 1-6); `2A18P1 | 2A18J1` (six lines to A9J2 pins 7-12 and three output arrows). A9J2 is labelled "GROUNDS TO A3 DRIVER VIA A9P2" (pins 1, 2, 3, 4, 5, 6, then 7, 8, 9, 10, 11, 12). An earth-ground symbol and a circuit-ground symbol are drawn at the far left on the common ground line.

## Folio 45: AC input, line filter, ON-OFF switch, A12J7 / A12P7

- AC INPUT POWER 110V AC 50Hz/60Hz (North American plug drawn); AC INPUT POWER 220V AC 50Hz/60Hz (European plug drawn).
- Cord conductors labelled BLACK, GREEN (to earth ground), WHITE.
- `MA-941 LINE FILTER/FUSE ASSEMBLY`: P/O A12J6 / P/O A12P6 pin 3 wire `766` through fuse `F20` ("SEE TABLE") to wire `788` (with a small boxed `6` blue and `5` green tag arrows), then the LINE FILTER block; pin 4 wire `777` (boxed `1` brown tag arrow, boxed `5` tag, "NOT USED IN ALL GAMES." printed beside the ground branch); output side P/O A12P6 pin 1 wire `700` (boxed `6` tag) and pin 2 wire `711` (boxed `1` tag), to P/O A12J6 pins 1 and 2 wires `700` and `711`.
- ON-OFF-SW. (dashed box, two-pole switch, earth ground at its dashed box): each pole has boxed `0` (black) wires in and out; poles feed `722` (A12J7 pin 3) and `733` (A12J7 pin 4). Wire `700` returns to A12J7 pin 1 ("110V AC") and wire `711` to A12J7 pin 2 ("110V AC RETURN").
- A12J7 / A12P7 (pins as drawn): 3 `722` then fuse `F8` ("SEE NOTE 1"); 4 `733`; 1 `700` BLACK to SERVICE OUTLET; 2 `711` WHITE to SERVICE OUTLET (GREEN to earth ground); 9 wire box `9` (J7 side) and `777` (P7 side); 5 `9` (J7) and `777` (P7); 6 RED (110V AC); 7 GREEN (100V AC); 8 `9` (J7 side), VIOLET (COMMON); 10 ORANGE (110V AC); 11 YELLOW (100V AC); 12 `788` (COMMON), BROWN labelled at the junction with a tag.
- JUMPER 1 (J1) drawn between A12J7 pins 5 and 6; JUMPER 2 (J2) from pin 9 round to pin 10; JUMPER 3 (J3) from pin 8 to pin 12 (as drawn on the J7 side).
- A12J9 "TO LIGHTBOX A12P9": pin 2 `822`, pin 1 `811`. A12J8 / A12P8: pin 2 `822` then "115V AC" fuse `F7` 1/2A SLO-BLO; pin 1 `811` (J8 side) and `6` (P8 side) "115V AC COMMON".

### POWER INPUT OPTIONS table (A12J7 wiring view, as printed)

Pin-number grid (wiring view): row 1: 1 2 3 4; row 2: 5 6 7 8; row 3: 9 10 11 12.

Jumper grids (rows 1 to 3 as printed; top row printed in faint dotted digits 1 2 3 4 for every grid):

| Option | Row 2 (pins 5-8) | Row 3 (pins 9-12) |
| --- | --- | --- |
| 100V AC INPUT JUMPERS | J1, 6 (faint), J1, J3 | J2, 10 (faint), J2, J3 |
| 110V AC INPUT JUMPERS | J1, J1, 7 (faint), J3 | J2, J2, 11 (faint), J3 |
| 200V AC INPUT JUMPERS | J1, 6 (faint), J1, J2 | 9 (faint), 10 (faint), J2, 12 (faint) |
| 210V AC INPUT JUMPERS | J1, 6 (faint), J1, J2 | 9 (faint), J2, 11 (faint), 12 (faint) |
| 220V AC INPUT JUMPERS | J1, J1, 7 (faint), J2 | 9 (faint), J2, 11 (faint), 12 (faint) |

## Folio 45: transformer 24634 and rectifier circuits

Transformer dashed box labelled `24634`. Secondary taps with wire boxes as printed (tap number as printed beside the winding end where legible):

| Tap | Wire box | Fuse | Printed signal |
| --- | --- | --- | --- |
| 5 | `155` | F9 1A | 6.2V AC (DISPLAY FILAMENT ... text runs off the page) |
| 7 | `133` | none | Vco |
| 9 | `166` | F9A, 1A | 6.2V AC RETURN (DISPLAY FI... text runs off the page) |
| 1 | `177` | F3 1/4A SLO-BLO | 32V AC |
| 2 | `111` | none | 32V AC RETURN |
| 3 | `655` | F1 1/2A | 12V AC |
| 4 | `644` | none | 12V AC RETURN |
| 15 | `211` | F2 6-1/4A SLO-BLO, then `233` | 11V AC (then R1 and R2 in parallel, bridge EL-42, +12V DC) |
| 16 | `244` | none | 11V AC RETURN |
| 10 | `266` | F4 8A SLO-BLO, then `188` | 27V AC (bridge EL-42, +24V DC) |
| 11 | `288` | none | 27V AC RETURN |
| 12 | `000` | none | 6.3V AC RETURN |
| 13 | `088` | F6 5A SLO-BLO, then `066` | 6.3V AC |
| 14 | `300` | F5 10A SLO-BLO, then `311` | 8V AC (bridge EL-42, +6V DC) |
| (tap number not legible) | `6` (blue) | F7 1/2A SLO-BLO (on `822`) | 115V AC / 115V AC COMMON to lightbox |

Rectifier and parts labels: bridges labelled `EL-42` (three); R1 and R2 "EACH 0.33Ω, 10%, 5W,WW" (continued on folio 46 as "5W,WW"); capacitor C1 "10,000UF 25V" (+ and - marked); each bridge negative returns to wire box `9` "GND" arrows to `2A18J3`. Earth ground symbol at the transformer shield.

## Uncertain readings

- DRAWN initials in the title block ("G.P.D.") are handwritten; best reading only.
- 1A7 board: the P1-side buses, the parallel tilt contacts and the strobe of every cabinet switch were re-traced on a full-resolution crop of the 600 dpi render (PDF page 16, region x 2900-4700, y 4400-6100). The strobe line of RIGHT ADVANCE BUTTON leaves the crop at the top and was followed on the whole-page render to STROBE 1 (`411`); it is the least certain trace on the sheet.
- A10P1 pin 3 `255` +6V DC and pin 11 `688` +5V DC: pin numbers read directly, but where the lines go was not fully traced.
- A10P3 pin 1 wire `222`: onward routing not traced.
- A10P2 pin 6 RESET `300`: the route to A6J1 pin 10 is by trace and not certain.
- J2 / A2J2 pins 4 and 5 `688` onward routing not traced.
- Folio 45 jumper tables: faint digits are drawn in a dotted font and were read as unused pin numbers; the jumper positions J1/J2/J3 are in bold.
- The pin-count of ground banks 1A18P3, 1A18P2, 1A18P1 and 2A18P3 was not counted exactly (about 8 or 9 pins each).
- Transformer tap numbers on folio 45 are read where legible; the tap for the `6` / `6` secondary is not legible. Tap-number readings 5, 7, 9, 1, 2, 3, 4, 15, 16, 10, 11, 12, 13, 14 follow the vertical order on the page.
- Wire color words (RED, GREEN, etc.) and the boxed single digits near the line filter were transcribed as printed.
