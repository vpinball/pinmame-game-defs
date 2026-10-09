# Safe Cracker — Security CPU Board Connectors

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`: the `SECURITY CPU BOARD ASSEMBLY A-20119-90003` drawing (PDF page
152, printed folio `3-28`, upper part of the page) and the connector pin list, which begins under the drawing on PDF page 152
(`J201`-`J205`, left column `J201`-`J204`, right column `J205`) and continues on PDF page 153 (printed folio `3-29`,
`J206`-`J212`, two columns). The pin list is printed as plain text lines of the form `Jnnn-n <wire colour>, <function/destination>`
with the wire colour spelled out in full; each line is given here as one table row, with the text after the pin designator
kept literally in the `Printed text` column. Blank lines between connectors on the page are not rows. Read from the rendered
page (300 dpi scan), not from the OCR text. The list has no heading line of its own on either page.

## Printed page 3-28 (PDF page 152): board assembly drawing

Title lines: `SECURITY CPU BOARD ASSEMBLY` / `A-20119-90003`. The drawing is an unrotated portrait board outline. Printed labels and
their positions:

| Label as printed | Position / what it labels | Pin-number labels printed at the connector ends |
| --- | --- | --- |
| `I/O EXTEND` | Above the two-row header `J201` (top left) | `2` (upper row) and `1` (lower row) at the left end; 13 pin positions per row visible |
| `J201` | Below the `I/O EXTEND` header | |
| `TO I/O SOUND` | Above the two-row header `J202` (top, to the right of J201) | `2` and `1` at the left end; `34` and `33` at the right end |
| `J202` | Below the `TO I/O SOUND` header | |
| `B1` | Rotated label at the left side of the battery holder at top left | (three side-by-side cell holders drawn, each marked `+` at the top and `-` at the bottom; a `+` is also printed beside the top terminal of the first and second holders) |
| `POWER` | Rotated label beside the connector at the right middle | |
| `J210` | Rotated label by the `POWER` connector | `1` at one end, `7` at the other |
| `J211` | Rotated label beside the two-row header on the right | `34` and `33` at one end, `2` and `1` at the other |
| `TO PWR/DRV/FLIP PCB` | Rotated label beside the `J211` header | |
| `POWER` / `DIAG` / `BLANKING` | Three labels (rotated) along the left edge, each with a leader line to one of three round two-hole LED/indicator symbols (top to bottom: `BLANKING`, `DIAG`, `POWER`) | |
| `CABINET` | Above the long single-row header `J212` (bottom row, upper) | `13` at the left end, `1` at the right end |
| `J212` | Below that header | |
| `PLFD COL` | Above the header `J206` | `9` at the left end, `1` at the right end |
| `J206` | Below that header | |
| `PLFD ROWS` | Above the header `J208` | `14` at the left end, `1` at the right end |
| `J208` | Below that header | |
| `DIRECT SW INPUTS` | Below the header `J205` (lower row, left) | `12` at the left end, `1` at the right end |
| `J205` | Above the `DIRECT SW INPUTS` label | |
| `B.B. COL` | Below the header `J207` (lower row, middle) | `9` at the left end, `1` at the right end |
| `J207` | Above the `B.B. COL` label | |
| `B.B. ROWS` | Below the header `J209` (lower row, right) | `9` at the left end, `1` at the right end |
| `J209` | Above the `B.B. ROWS` label | |

Other drawing features: about six keyhole-shaped mounting-hole symbols and two plain round holes (counted from the overview, approximate); no DIP switch is drawn, no
jumpers are labelled, no ICs or IC designators are labelled, and there are no printed notes. Each of the single-row headers
J205-J209, J212 and J210 has one `*` marker at a pin position (the keyed pin); the pin list below names the `Key` pin of each.
The drawing shows connectors `J201`, `J202`, `J205`, `J206`, `J207`, `J208`, `J209`, `J210`, `J211`, `J212`; connectors `J203` and
`J204` appear in the pin list (`Not Used`) but are not drawn.

## Pin list on printed page 3-28 (PDF page 152)

Left column (single lines, no pin rows):

| Connector | Printed text |
| --- | --- |
| J201 | 26-Pin Ribbon Cable, Data to/from J602 |
| J202 | 34-Pin Ribbon Cable, Data to/from J601 |
| J203 | Not Used |
| J204 | Not Used |

Right column:

#### J205

| Pin | Printed text |
| --- | --- |
| J205-1 | Orange-Brown, Ded. Sw. Row 1, to Coin Door Bd. J1-8 |
| J205-2 | Orange-Red, Ded. Sw. Row 2, to Coin Door Bd. J1-7 |
| J205-3 | Orange-Black, Ded. Sw. Row 3, to Coin Door Bd. J1-6 |
| J205-4 | Orange-Yellow, Ded. Sw. Row 4, to Coin Door Bd. J1-5 |
| J205-5 | Not Used |
| J205-6 | Orange-Green, Ded. Sw. Row 5, to Coin Door Bd. J1-4 |
| J205-7 | Orange-Blue, Ded. Sw. Row 6, to Coin Door Bd. J1-3 |
| J205-8 | Orange-Violet, Ded. Sw. Row 7, to Coin Door Bd. J1-2 |
| J205-9 | Orange-Gray, Ded. Sw. Row 8, to Coin Door Bd. J1-1 |
| J205-10 | Black, Ground, to Coin Door Bd. J1-10 |
| J205-11 | Key |
| J205-12 | Orange-White, Sw. Enable, to Coin Door Bd. J1-11 |

## Printed page 3-29 (PDF page 153)

### Left column

#### J206

| Pin | Printed text |
| --- | --- |
| J206-1 | Green-Brown, Sw. Col. 1, to Playfield Sw. |
| J206-2 | Green-Red, Sw. Col. 2, to Playfield Sw. |
| J206-3 | Green-Orange, Sw. Col. 3, to Playfield Sw. |
| J206-4 | Green-Yellow, Sw. Col. 4, to Playfield Sw. |
| J206-5 | Green-Black, Sw. Col. 5, to Playfield Sw. |
| J206-6 | Green-Blue, Sw. Col. 6, to Playfield Sw. |
| J206-7 | Green-Violet, Sw. Col. 7, to Playfield Sw. |
| J206-8 | Key |
| J206-9 | Green-Gray, Sw. Col. 8, to Playfield Sw. |

#### J207

| Pin | Printed text |
| --- | --- |
| J207-1 | Not Used |
| J207-2 | Not Used |
| J207-3 | Not Used |
| J207-4 | Not Used |
| J207-5 | Not Used |
| J207-6 | Not Used |
| J207-7 | Not Used |
| J207-8 | Key |
| J207-9 | Green-Gray, Sw. Col. 8, to Backbox Sw. |

#### J208

| Pin | Printed text |
| --- | --- |
| J208-1 | White-Brown, Sw. Row 1, to Playfield Sw. |
| J208-2 | White-Red, Sw. Row 2, to Playfield Sw. |
| J208-3 | White-Orange, Sw. Row 3, to Playfield Sw. |
| J208-4 | White-Yellow, Sw. Row 4, to Playfield Sw. |
| J208-5 | White-Green, Sw. Row 5, to Playfield Sw. |
| J208-6 | Key |
| J208-7 | White-Blue, Sw. Row 6, to Playfield Sw. |
| J208-8 | White-Violet, Sw. Row 7, to Playfield Sw. |
| J208-9 | White-Gray, Sw. Row 8, to Playfield Sw. |
| J208-10 | Not Used |
| J208-11 | Black-Violet, F5, to Upr Right E.O.S. Sw. |
| J208-12 | Black-Blue, F3, to Lwr Left E.O.S. Sw. |
| J208-13 | Black-Green, F1, to Lwr Right E.O.S. Sw. |
| J208-14 | Orange, Ground to E.O.S. Sw. |

### Right column

#### J209

| Pin | Printed text |
| --- | --- |
| J209-1 | White-Brown, Sw. Row 1, to Backbox Sw. |
| J209-2 | White-Red, Sw. Row 2, to Backbox Sw. |
| J209-3 | Not Used |
| J209-4 | Not Used |
| J209-5 | Not Used |
| J209-6 | Key |
| J209-7 | Not Used |
| J209-8 | Not Used |
| J209-9 | Not Used |

#### J210

| Pin | Printed text |
| --- | --- |
| J210-1 | Black, Ground, to/from J101-7, J606-1 |
| J210-2 | Key |
| J210-3 | Black, Ground, to/from J101-5, J606-3 |
| J210-4 | Gray, +5V, to/from J101-4, J606-4 |
| J210-5 | Gray, +5V, to/from J101-3, J606-5 |
| J210-6 | Gray-Green, +12V, to/from J101-2, J606-6 |
| J210-7 | Gray-Green, +12V, to/from J101-1, J606-7 |

#### J211

Printed as a single line: `J211 34-Pin Ribbon Cable, Data to/from J102`

#### J212

| Pin | Printed text |
| --- | --- |
| J212-1 | Green-Brown, Sw. Col. 1, to Coin Door Board J3-1 |
| J212-2 | Green-Red, Sw. Col. 2, to Coin Door Board J3-2 |
| J212-3 | Not Used |
| J212-4 | White-Brown, Sw. Row 1, to Coin Door Board J3-3 |
| J212-5 | Key |
| J212-6 | White-Red, Sw. Row 2, to Coin Door Board J3-4 |
| J212-7 | White-Orange, Sw. Row 3, to Coin Door Board J3-5 |
| J212-8 | White-Yellow, Sw. Row 4, to Coin Door Board J3-6 |
| J212-9 | Black-Blue, F8, Coin Door Board J13-2 |
| J212-10 | Black-Yellow, F6, to Right Flipper Opto Board J1-1 |
| J212-11 | Blue-Gray, F4, to Left Flipper Opto Board J1-2 |
| J212-12 | Blue-Violet, F2, to Right Flipper Opto Board J1-2 |
| J212-13 | Orange, Ground to Right Flipper Opto Board J1-4 |

## Row counts

Pin rows: J205 12, J206 9, J207 9, J208 14, J209 9, J210 7, J212 13 = 73 pin rows. Whole-connector lines: J201, J202, J211 (ribbon
cables) and J203, J204 (`Not Used`). Connectors J201-J212 each appear once, in ascending order; no pin is skipped or printed twice
within a connector.

## Observations on the printed text

- `J205` (`DIRECT SW INPUTS`) carries dedicated-switch rows 1-8 (`Ded. Sw. Row 1` ... `Row 8`) to Coin Door Bd. `J1-8` ... `J1-1` (row
  1 on `J1-8`, descending), with `J205-5` skipped as `Not Used` between rows 4 and 5, a `Black, Ground` on `J205-10` and an
  `Orange-White, Sw. Enable` on `J205-12`.
- Switch columns: `J206-1` ... `J206-7` carry `Sw. Col. 1` ... `7` and `J206-9` carries `Sw. Col. 8` to the playfield (`J206-8` is `Key`); `J207-9`
  carries `Sw. Col. 8` (same wire colour `Green-Gray`) `to Backbox Sw.`, and `J207-1` ... `J207-7` are `Not Used`.
- Switch rows: `J208` carries `Sw. Row 1` ... `8` to the playfield (`J208-6` is `Key`; rows 6-8 on pins 7-9), `J209` carries only
  `Sw. Row 1` and `Sw. Row 2` `to Backbox Sw.` (pins 1, 2), `J212` carries `Sw. Col. 1`, `Sw. Col. 2` and `Sw. Row 1` ... `Row 4` to the Coin Door
  Board `J3-1` ... `J3-6`.
- `J208-11`/`-12`/`-13` and `J212-9`/`-10`/`-11`/`-12` carry signals printed as `F1` ... `F8` (`F5`/`F3`/`F1` on `J208-11`/`-12`/`-13` to Upper
  Right, Lower Left and Lower Right `E.O.S. Sw.`; `F8`, `F6`, `F4`, `F2` on `J212-9`, `-10`, `-11`, `-12`). The designators
  `F2`, `F4`, `F6`, `F8` appear on `J212` and `F1`, `F3`, `F5` on `J208`; none of `F7` is printed. `J212-12` and `J212-11` both read `J1-2` on
  different boards (`Right Flipper Opto Board J1-2` and `Left Flipper Opto Board J1-2`). `J212-9` is printed `Coin Door Board J13-2`
  (without `to`), while the other J212 lines print `to`.
- `J208-14` reads `Orange, Ground to E.O.S. Sw.` and `J212-13` `Orange, Ground to Right Flipper Opto Board J1-4`.
- `J210` mirrors the Power Driver Board `J101`: `J210-1` to `J101-7`/`J606-1`, `J210-3` to `J101-5`/`J606-3`, `J210-4` to `J101-4`/`J606-4`, `J210-5` to `J101-3`/`J606-5`, `J210-6` to
  `J101-2`/`J606-6`, `J210-7` to `J101-1`/`J606-7`, with `to/from` wording (the Power Driver Board list prints `to J210-n, J606-n` for its side).
- `J201` is described as a `26-Pin Ribbon Cable` to `J602`; `J202` as a `34-Pin Ribbon Cable` to `J601`; `J211` as a `34-Pin Ribbon Cable` to `J102` (the Power
  Driver Board `J102`, also `34-Pin Ribbon Cable ... to/from CPU J211`).
- The drawing labels `J201` `I/O EXTEND` and `J202` `TO I/O SOUND`; the pin list does not repeat those names but gives the J602/J601
  destinations.

## Reading uncertainties

- The three indicator symbols along the left edge (labels `BLANKING`, `DIAG`, `POWER`) were read at native resolution; the order
  top to bottom is `BLANKING`, `DIAG`, `POWER`; their LED designators (if any) are not printed.
- The pin-count end labels (e.g. `13` on `J212`, `14` on `J208`) were read from native-resolution crops of the drawing; the positions
  of the key `*` markers were not transcribed (the pin list names every `Key` pin).
- No `[?]` readings in the pin-list text.
