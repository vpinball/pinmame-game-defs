# Black Rose — Switch Matrix

Transcribed from `Bally_1992_Black_Rose_Manual.pdf`, PDF page 107, printed page `BLACK ROSE 3-3`, the
`SWITCH MATRIX` page (matrix grid with column/row wiring headers, `Dedicated Switches` block, `Flipper Switches`
block and the `Switch Matrix Circuit` drawing). Read from the rendered page (300 dpi image-only scan), not from the
OCR text.

Column and row headers are printed as three stacked lines (IC pin, wire colours, connector pin). Matrix cell names
are printed wrapped over two to four lines; they are joined with single spaces below, otherwise unchanged. Every
matrix cell also carries its two-digit address printed in its lower-left corner (column digit then row digit) and a
small drawn switch symbol in its lower-right corner; the symbol is identical in all 64 cells. No cell is printed
blank. No cell is shaded, tinted or marked as an opto: the page is a bilevel scan and a pixel check of every cell
shows plain white backgrounds with no fill, hatching or legend marking. The only opto-named matrix cell is the
text `Ticket Opto` at 23. Connector numbering skips a pin in two places as printed: column 8 is `J206-9` (no
`J206-8` is printed), and the Dedicated Switches D5 line is `J205-6` (no `J205-5` is printed); the row connectors
run `J208-1` to `J208-5` and then `J208-7`, `J208-8`, `J208-9` (no `J208-6` is printed). The same wire
colour `Blk-Blu` is printed for both F3 and F8 in the Flipper Switches block. No `[?]` or `[illegible]` cells.

## (a) Column (drive) headers

| Column | Drive IC | Wire | Connector pin |
| --- | --- | --- | --- |
| 1 | U20-18 | Grn-Brn | J206-1 |
| 2 | U20-17 | Grn-Red | J206-2 |
| 3 | U20-16 | Grn-Org | J206-3 |
| 4 | U20-15 | Grn-Yel | J206-4 |
| 5 | U20-14 | Grn-Blk | J206-5 |
| 6 | U20-13 | Grn-Blu | J206-6 |
| 7 | U20-12 | Grn-Vio | J206-7 |
| 8 | U20-11 | Grn-Gry | J206-9 |

## (b) Row (return) headers

| Row | Return IC | Wire | Connector pin |
| --- | --- | --- | --- |
| 1 | U18-11 | Wht-Brn | J208-1 |
| 2 | U18-9 | Wht-Red | J208-2 |
| 3 | U18-5 | Wht-Org | J208-3 |
| 4 | U18-7 | Wht-Yel | J208-4 |
| 5 | U19-11 | Wht-Grn | J208-5 |
| 6 | U19-9 | Wht-Blu | J208-7 |
| 7 | U19-5 | Wht-Vio | J208-8 |
| 8 | U19-7 | Wht-Gry | J208-9 |

## (c) Matrix cells (address = column digit then row digit)

| Address | Printed name |
| --- | --- |
| 11 | Not Used |
| 12 | Not Used |
| 13 | Start Button |
| 14 | Plumb Bob Tilt |
| 15 | Outhole |
| 16 | Right Trough |
| 17 | Center Trough |
| 18 | Left Trough |
| 21 | Slam Tilt |
| 22 | Coin Door Closed |
| 23 | Ticket Opto |
| 24 | Always Closed |
| 25 | Shooter |
| 26 | Left Outlane |
| 27 | Left Return Lane |
| 28 | Left Sling |
| 31 | Bottom Standup Bottom |
| 32 | Bottom Standup Middle |
| 33 | Bottom Standup Top |
| 34 | Fire Button |
| 35 | Cannon Kicker |
| 36 | Right Outlane |
| 37 | Right Return Lane |
| 38 | Right Slingshot |
| 41 | Middle Standup Top |
| 42 | Middle Standup Middle |
| 43 | Middle Standup Bottom |
| 44 | Left Ramp Enter |
| 45 | Top Left Loop |
| 46 | Left Jet |
| 47 | Right Jet |
| 48 | Bottom Jet |
| 51 | Top Standup Bottom |
| 52 | Top Standup Middle |
| 53 | Top Standup Top |
| 54 | Ramp Down |
| 55 | Ball Popper |
| 56 | Right Ramp Made |
| 57 | Jet Bumpers Exit |
| 58 | Jet Bumper Enter |
| 61 | Subway Top |
| 62 | Backboard Ramp |
| 63 | Lockup 1 |
| 64 | Lockup 2 |
| 65 | Right Single Standup |
| 66 | Subway Bottom |
| 67 | Not Used |
| 68 | Not Used |
| 71 | Lockup Enter |
| 72 | Middle Ramp |
| 73 | Not Used |
| 74 | Not Used |
| 75 | Not Used |
| 76 | Right Ramp Enter |
| 77 | Not Used |
| 78 | Not Used |
| 81 | Not Used |
| 82 | Not Used |
| 83 | Not Used |
| 84 | Not Used |
| 85 | Not Used |
| 86 | Not Used |
| 87 | Not Used |
| 88 | Not Used |

## (d) Dedicated Switches

Printed on the left of the page under the heading `Dedicated Switches`. Each entry has three stacked header lines
(IC pin, wire colours, connector pin), a name, a label `D1` to `D8` printed above or beside a switch symbol, and all
eight switches share one ground line on the right. For D5 to D8 the printed column headings `Normal Function` and
`Test Function` appear above the two names; the first name is the Normal Function and the second is the Test
Function. The printed names wrap over lines (`Volume Down` is printed `Volume` / `Down`, `Volume Up` is printed
`Volume` / `Up`, `Begin Test` is printed `Begin` / `Test`); they are joined with spaces here. The `Test Function`
for D6 prints as `Down` and for D7 as `Up`, with no `Volume` word.

| Label | IC | Wire | Connector pin | Name (D1-D4) | Normal Function (D5-D8) | Test Function (D5-D8) |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | U17-5 | Org-Brn | J205-1 | Left Coin Chute | | |
| D2 | U17-7 | Org-Red | J205-2 | Center Coin Chute | | |
| D3 | U17-11 | Org-Blk | J205-3 | Right Coin Chute | | |
| D4 | U17-9 | Org-Yel | J205-4 | 4th Coin Chute | | |
| D5 | U16-9 | Org-Grn | J205-6 | | Service Credits | Escape |
| D6 | U16-11 | Org-Blu | J205-7 | | Volume Down | Down |
| D7 | U16-7 | Org-Vio | J205-8 | | Volume Up | Up |
| D8 | U16-5 | Org-Gry | J205-9 | | Begin Test | Enter |

(Blank cells in this table mean the item has no such printed name: D1-D4 carry a single name with no Normal/Test
headings, and D5-D8 carry the two function names instead.)

## (e) Flipper Switches

Printed on the right of the page under the heading `Flipper Switches`. Each entry has three stacked header lines
(IC pin, wire colours, connector pin), a name, and a label `F1` to `F8` above a switch symbol. The four `End of
Stroke` switches (F1, F3, F5, F7) join one ground line and the four `Opto` switches (F2, F4, F6, F8) join a second
ground line. The name for F7 is printed `Upper Left` / `Flipper End of Stroke` with the final letters touching the
vertical ground line; it reads `Stroke`. Names that wrap are joined with spaces.

| Label | IC | Wire | Connector pin | Printed name |
| --- | --- | --- | --- | --- |
| F1 | U4A-5 | Blk-Grn | J906-1 | Right Flipper End of Stroke |
| F2 | U4B-7 | Blu-Vio | J905-1 | Right Flipper Opto |
| F3 | U4C-9 | Blk-Blu | J906-3 | Left Flipper End of Stroke |
| F4 | U4D-11 | Blu-Gry | J905-2 | Left Flipper Opto |
| F5 | U6A-5 | Blk-Vio | J906-4 | Upper Right Flipper End of Stroke |
| F6 | U6B-7 | Blk-Yel | J905-3 | Upper Right Flipper Opto |
| F7 | U6C-9 | Blk-Gry | J906-5 | Upper Left Flipper End of Stroke |
| F8 | U6D-11 | Blk-Blu | J905-5 | Upper Left Flipper Opto |

## (f) Switch Matrix Circuit drawing

Titled `Switch Matrix Circuit`, two schematic fragments side by side with example labels `COLUMN (example)` and
`ROW (example)`, both inside `CPU Board` outlines joined through connector `J206` (column side) and `J208` (row
side) to a dashed `Playfield` box.

- Column side: `LS 374SC` latch output drives an inverter `ULN-2803` (point `B` is labelled at the inverter
  output and point `A` at the `J206` connector side of the 1K/470 pf node); a `1K` resistor pulls the line to `+12V`, a `470 pf` capacitor goes
  to ground; the line leaves via `J206` as `GRN-XXX` to the switch.
- Playfield box: a single switch in series with a diode, between wire `GRN-XXX` and wire `WHT-XXX`.
- Row side: from `J208` through a `1N4148` diode to node `C`; node `C` has a `1.2K` resistor to `+12V` and a
  `470 pf` capacitor to ground; a `1K` resistor connects `C` to the `+` input of an `LM339` comparator, whose `-`
  input is tied to `+5V`; output node `D` has a `10K` pull-up to `+5V` and goes to a `74LS240` buffer whose output
  is node `E`.

Truth tables as printed (`H` = high, `L` = low):

| Column | A | B | |
| --- | --- | --- | --- |
| Inactive | H | L | Off |
| Active | L | H | On |

| Switch | C | D | E | |
| --- | --- | --- | --- | --- |
| Open | H | H | L | Off |
| Closed | L | L | H | On |

Explanatory text printed below the circuit, verbatim (two paragraphs):

The microprocessor is constantly strobing the column side of the switch. When point "A" on the column circuit toggles low the column side is active.

When a switch closes the row side of the circuit activates. The "+" input to the LM339 drops below +5V causing its output to go low. Corresponding row and column switches must be  low at the same time, for the switch to be considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is inactive.

(The scan prints two spaces between `must be` and `low`; kept.)
