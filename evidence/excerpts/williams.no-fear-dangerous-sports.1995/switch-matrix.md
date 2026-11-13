# No Fear: Dangerous Sports — Switch Matrix Table, Section 3 copy and dedicated switches

From `Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf` (operations manual 16-50025-101, April 1995, a 144-page scan without a text layer; SHA-256 `176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b`), PDF page 109 (printed 2-36, Switch Matrix Table with its dedicated and flipper grounded-switch columns and the opto shading), its Section 3 copy PDF page 115 (3-2, compared) and the DEDICATED SWITCHES drawing PDF page 116 (3-3). Transcribed from the 200 dpi renders by a delegated reader; the curator then checked the PDF page 109 table against the rendered page. Cells are kept as printed, including misspellings and abbreviations; `—` marks a cell that is blank on the page. `p-NNN` is the PDF page; the printed page number follows it.

## PDF p-109, printed 2-36, "Switch Matrix Table"

Header drawing: `WHITE` - diode - switch - `GREEN`. Footnote: `J2XX = CPU BOARD; J9XX = FLIPTRONIC II BOARD`. Legend: stippled box `= OPTO, TYPICALLY CLOSED`.

### Columns

| Col | Wire | Connector | IC pin |
|---|---|---|---|
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

### Rows

| Row | Wire | Connector | IC pin |
|---|---|---|---|
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

### Grid (columns 3 and 4 are opto-shaded)

| Row \ Col | 1 | 2 | 3 (shaded) | 4 (shaded) | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 11 BALL LAUNCH | 21 SLAM TILT | 31 TROUGH STACK | 41 RIGHT POPPER 1 | 51 DROP TARGET | 61 EJECT HOLE | 71 NOT USED | 81 NOT USED |
| 2 | 12 NOT USED | 22 COIN DOOR CLOSED | 32 TROUGH 1 (RIGHT) | 42 RIGHT POPPER 2 | 52 NOT USED | 62 LEFT LOOP | 72 NOT USED | 82 NOT USED |
| 3 | 13 START BUTTON | 23 BUY EXTRA BALL | 33 TROUGH 2 | 43 NOT USED | 53 NOT USED | 63 LEFT RAMP ENTER | 73 NOT USED | 83 NOT USED |
| 4 | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH 3 | 44 NOT USED | 54 LEFT WIREFORM | 64 LEFT RAMP MIDDLE | 74 NOT USED | 84 NOT USED |
| 5 | 15 SHOOTER LANE | 25 KICKBACK | 35 TROUGH 4 | 45 NOT USED | 55 INNER LOOP | 65 NOT USED | 75 NOT USED | 85 NOT USED |
| 6 | 16 SPINNER | 26 LEFT RETURN | 36 NOT USED | 46 LEFT MAGNET | 56 LIGHT KICKBACK BOTTOM | 66 RIGHT RAMP ENTER | 76 NOT USED | 86 NOT USED |
| 7 | 17 RIGHT OUTLANE | 27 LEFT SLINGSHOT | 37 CENTER TROUGH ENTER | 47 CENTER MAGNET | 57 LIGHT KICKBACK TOP | 67 RIGHT RAMP EXIT | 77 NOT USED | 87 NOT USED |
| 8 | 18 RIGHT RETRUN | 28 RIGHT SLINGSHOT | 38 LEFT TROUGH ENTER | 48 RIGHT MAGNET | 58 RIGHT LOOP | 68 NOT USED | 78 NOT USED | 88 NOT USED |

No blank cells. `RIGHT RETRUN` (cell 18) is a printed typo, kept.

### Opto shading ("OPTO, TYPICALLY CLOSED", stippled cells)

Shaded matrix cells: all 16 cells of columns 3 and 4: 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48. This includes cells printed NOT USED (36, 43, 44, 45) and the magnet cells 46, 47, 48. No cell in columns 1, 2, 5-8 is shaded.

### Dedicated grounded switches

| ID | Wire | Connector | Label as printed |
|---|---|---|---|
| D1 | Org-Brn | J205-1 | Left Coin Chute |
| D2 | Org-Red | J205-2 | Center Coin Chute |
| D3 | Org-Blk | J205-3 | Right Coin Chute |
| D4 | Org-Yel | J205-4 | 4th Coin Chute |
| D5 | Org-Grn | J205-6 | small labels: `Normal` / `Service Credit` ; `Test` / `Escape` |
| D6 | Org-Blu | J205-7 | small labels: `Normal` / `Volume Down` ; `Test` / `Down` |
| D7 | Org-Vio | J205-8 | small labels: `Normal` / `Volume Up` ; `Test` / `Up` |
| D8 | Org-Gry | J205-9 | small labels: `Normal` / `Begin Test` ; `Test` / `Enter` |

(No J205-5 printed.) In D5-D8 the `Normal` heading and its text sit at left, the `Test` heading and its text at right.

### Flipper grounded switches

| ID | Wire | Connector | Label as printed | Shading |
|---|---|---|---|---|
| F1 | Black-Green | J906-1 | Lower Right E.O.S. | none |
| F2 | Blue-Violet | J905-1 | Lower Right Opto | faint stipple |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S. | none |
| F4 | Blue-Gray | J905-2 | Lower Left Opto | stipple visible |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S. | none |
| F6 | Black-Yellow | J905-3 | Upper Right Opto | stipple visible |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. | none |
| F8 | Black-Blue | J905-5 | Upper Left Opto | stipple visible |

The four Opto flipper cells (F2, F4, F6, F8) carry stippling like the legend; F2's is faint. F3 and F8 both print Black-Blue.

---
## PDF p-115, printed 3-2, "SWITCH MATRIX" (Section 3 copy)

Same table as p-109: headers, wires, connectors, IC pins, every cell number and name, dedicated and flipper columns, legend and footnote are text-identical, including `RIGHT RETRUN` (18). Shading identical: all of columns 3 and 4 (31-38, 41-48); flipper Opto cells F2, F4, F6, F8 stippled. Dedicated labels identical (D5 `Normal Service Credit` / `Test Escape`, D6 `Normal Volume Down` / `Test Down`, D7 `Normal Volume Up` / `Test Up`, D8 `Normal Begin Test` / `Test Enter`).

Page also has the "SWITCH MATRIX CIRCUIT" schematic (parts printed: LS374SC, 74LS240, LM339, 10KΩ, 1.2KΩ, 1KΩ, 470pf, 1N4148, +12V, +5V, J207, J209, `Green-XXX`, `White-XXX`; tables `COLUMN | A | B`: INACTIVE H L OFF, ACTIVE L H ON; `ROW | C | D | E`: SWITCH OPEN H H L OFF, SWITCH CLOSED L L H ON) and explanatory text. Folio `3-2`.

---

## PDF p-116, printed 3-3, "DEDICATED SWITCHES"

Wiring drawing, CPU BOARD J205 to COIN DOOR INTERFACE BOARD J1 and J3:

| J205 | Wire | IC | Label | J1 | J3 |
|---|---|---|---|---|---|
| 1 | Orange-Brown | (U17-5) | D1 | 14 | 4 |
| 2 | Orange-Red | (U17-5) | D2 | 13 | 5 |
| 3 | Orange-Black | (U17-5) | D3 | 12 | 6 |
| 4 | Orange-Yellow | (U17-5) | D4 | 17 | — (no J3 pin or switch drawn) |
| 6 | Orange-Green | (U17-5) | D5 | 11 | 7 |
| 7 | Orange-Blue | (U17-5) | D6 | 10 | 8 |
| 8 | Orange-Vioiet (typo as printed) | (U17-5) | D7 | 8 | 9 |
| 9 | Orange-Gray | (U17-5) | D8 | 9 | 11 |
| 11 | Black (grounded) | | | 15 | 3 |

Switch symbols are drawn on J3 pins 4, 5, 6, 7, 8, 9, 11, returning to common ground J3-3.

Printed text under drawing:
- Coin Acceptor Switches: `D1 - Left Coin Chute`; `D2 - Center Coin Chute`; `D3 - Right Coin Chute`; `D4 - Fourth Coin Chute`
- Control Switches: `D5 - Normal Function, Service Credits; Test Function, Escape`; `D6 - Normal Function, Volume Down; Test Function, Down`; `D7 - Normal Function, Volume Up; Test Function, Up`; `D8 - Normal Function, Begin Test; Test Function, Enter`

"DEDICATED SWITCH CIRCUIT" schematic and text follow (table `SWITCH | A | B | C`: OPEN H H L OFF; CLOSED L L H ON). Folio `3-3`.

## Transcription notes

All matrix cell numbers and names were read clearly from 1.6-2.3x crops. Residual items:
1. p-109 / p-115 flipper F2 (`Lower Right Opto`): stippling faint compared with F4, F6, F8. Text itself certain.
5. p-107 cell 21 and p-109 cell 61 have a partly dropped last glyph in the number; read by position.
7. Opto-shaded set from visible stippling: columns 3 and 4 fully stippled in every row; none seen elsewhere in the 8x8 grid.
Printed anomalies kept literally (not disagreements):
- Lamp column 8 is J137-9 (no J137-8); lamp row 3 is J134-4 (no J134-3); switch column 8 is J207-9; dedicated D5 is J205-6 (no J205-5).
- Switch cell 18 `RIGHT RETRUN` on both p-109 and p-115.
- F3 and F8 both print wire Black-Blue.
- p-116 `Orange-Vioiet` typo. D4 (Orange-Yellow, J205-4, J1-17) has no J3 pin or switch drawn.

Section 2 copy against Section 3 copy:
- Switch matrix p-109 vs p-115: no disagreement in any cell number, cell name, wire colour, connector, IC pin, dedicated label, flipper label or shading.
- Dedicated switches (p-109 column vs p-116 diagram/text, different content rather than copies): wire names abbreviated on p-109 (Org-Brn) and full on p-116 (Orange-Brown); D4 `4th Coin Chute` (p-109) vs `Fourth Coin Chute` (p-116); D5 `Service Credit` (p-109) vs `Service Credits` (p-116). J205 pins 1,2,3,4,6,7,8,9 agree.
