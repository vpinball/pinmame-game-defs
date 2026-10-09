# Safe Cracker — Power Driver Board Connectors

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`: the `POWER DRIVER BOARD ASSEMBLY A-20028` drawing (PDF page 148,
printed folio `3-24`) and its connector pin list, which runs over three printed pages: `3-25` (PDF page 149, two text
columns; J101-J115), `3-26` (PDF page 150, two text columns; J116-J133) and `3-27` (PDF page 151, left column only;
J134-J141). The pages print the pin list as plain text lines of the form `Jnnn-n <wire colour>, <function/destination>`,
with the wire colour spelled out in full (for example `Gray-Green`, `Blue-Violet`) and no column separators. Each line is
given here as one table row, with the printed text after the pin designator kept literally in the `Printed text` column.
Blank lines between connectors on the page are not rows. Read from the rendered page (300 dpi scan), not from the OCR
text. The pages carry no heading above the pin list (no `Power Driver Board Continued...` line); page 150 has the left
column `J116`-`J124` and the right column `J125`-`J133`; page 149 has the left column `J101`-`J108` and the right column
`J109`-`J115`.

## Printed page 3-24 (PDF page 148): board assembly drawing

Title lines: `POWER DRIVER BOARD ASSEMBLY` / `A-20028`. The page is a rotated board-outline drawing (landscape board shown on a
portrait page; the board edge has four notches on the right side). It carries no part values, only designators and
pin-number end labels. Folio: `3-24`.

Connector designators printed, with the highest pin number labelled at the connector end (the drawing is rotated, so the 1 end and the high end are at the top or bottom; only the end labels are printed, not every pin number):

| Connector | Pin count (end labels) |
| --- | --- |
| J101 | 7 ... 1 |
| J102 | 34/33 and 2/1 (two-row header) |
| J103 | 12 ... 1 |
| J104 | 3 ... 1 |
| J105 | 11 |
| J106 | 11 |
| J107 | 5 |
| J108 | 5 |
| J109 | 9 |
| J110 | 5 |
| J111 | 13 |
| J112 | 9 |
| J113 | 9 |
| J114 | 5 |
| J115 | 5 |
| J116 | 9 |
| J117 | 5 |
| J118 | 5 |
| J119 | 9 |
| J120 | 13 |
| J121 | 9 |
| J122 | 3 |
| J123 | 9 |
| J124 | 9 |
| J125 | 9 |
| J126 | 9 |
| J127 | 5 |
| J128 | 9 |
| J129 | 7 |
| J130 | 5 |
| J131 | 5 |
| J132 | 3 |
| J133 | 6 |
| J134 | 5 |
| J135 | 3 |
| J136 | 4 |
| J137 | 4 |
| J138 | 4 |
| J139 | 5 |
| J140 | 4 |
| J141 | 4 |

The drawing also shows one `*` marker at one pin position of most connectors (the keyed pin); the star positions were not transcribed because the printed pin list below names the `Key` pin of each connector. J102 is a two-row 34-pin header printed with `34`/`33` at one end and `2`/`1` at the other.

Fuses printed (rotated labels, drawn as fuse-holder outlines): `F101` (alone near J140/J141), `F102`, `F103`, `F104` (a
group of three near J134/J135 and LED103/LED104), `F105`, `F106`, `F107`, `F108`, `F109` (a group of five near J129/J128),
`F110`, `F111`, `F112`, `F113`, `F114` (a group of five near J103), `F115`, `F116`, `F117`, `F118` (a group of four near
J119/J121). That is 18 fuses, F101-F118. No fuse ratings are printed.

LEDs printed: `LED100`, `LED101`, `LED102`, `LED103`, `LED104`, `LED105` (circles with rotated labels). No colours or
functions are printed.

Other printed labels: none. The drawing has no printed notes, no part numbers other than `A-20028`, and no pin function
labels.

## Printed page 3-25 (PDF page 149)

### Left column

#### J101

| Pin | Printed text |
| --- | --- |
| J101-1 | Gray-Green, +12V to J210-7, J606-7 |
| J101-2 | Gray-Green, +12V to J210-6, J606-6 |
| J101-3 | Gray, +5V to J210-5, J606-5 |
| J101-4 | Gray, +5V to J210-4, J606-4 |
| J101-5 | Black, Ground to J210-3, J606-3 |
| J101-6 | Key |
| J101-7 | Black, Ground to J210-1, J606-1 |

#### J102

Printed as a single line (no pin rows): `J102 34-Pin Ribbon Cable, Data to/from CPU J211`

#### J103

| Pin | Printed text |
| --- | --- |
| J103-1 | Yellow-White, 6.8VAC from Xformer Secondary |
| J103-2 | White-Brown, 6.8VAC from Xformer Secondary |
| J103-3 | White-Brown, 6.8VAC from Xformer Secondary |
| J103-4 | White-Orange, 6.8VAC from Xformer Secondary |
| J103-5 | White-Yellow, 6.8VAC from Xformer Secondary |
| J103-6 | White-Yellow, 6.8VAC from Xformer Secondary |
| J103-7 | Orange, 6.8VAC from Xformer Secondary |
| J103-8 | Not Used |
| J103-9 | Key |
| J103-10 | Green, 6.8VAC from Xformer Secondary |
| J103-11 | Not Used |
| J103-12 | Not Used |

#### J104

Printed as a single line: `J104 Not Used`

#### J105

| Pin | Printed text |
| --- | --- |
| J105-1 | Brown, Return, G.I. to Coin Door Board J2-5 |
| J105-2 | Not Used |
| J105-3 | Yellow, Return, G.I. to Playfield |
| J105-4 | Key |
| J105-5 | Not Used |
| J105-6 | Not Used |
| J105-7 | White-Brown, 6.8VAC, G.I. to Coin Door Bd. J2-3 |
| J105-8 | Not Used |
| J105-9 | White-Yellow, 6.8VAC, G.I. to Playfield |
| J105-10 | Not Used |
| J105-11 | Not Used |

#### J106

| Pin | Printed text |
| --- | --- |
| J106-1 | Brown, Return G.I. to Insert Panel |
| J106-2 | Not Used |
| J106-3 | Yellow, Return G.I. to Insert Panel |
| J106-4 | Key |
| J106-5 | Not Used |
| J106-6 | Not Used |
| J106-7 | White-Brown, 6.8VAC, G.I. to Insert Panel |
| J106-8 | White-Orange, 6.8VAC, G.I. to Insert Panel |
| J106-9 | White-Yellow, 6.8VAC, G.I. to Insert Panel |
| J106-10 | White-Green, 6.8VAC, G.I. to Insert Panel |
| J106-11 | White-Violet, 6.8VAC, G.I. to Insert Panel |

#### J107, J108

Printed as single lines: `J107 Not Used` and `J108 Not Used`

### Right column

#### J109

| Pin | Printed text |
| --- | --- |
| J109-1 | Blue-Green, Solenoid 25 to Playfield Coil |
| J109-2 | Blue-Black, Solenoid 26 to Backbox Motor |
| J109-3 | Blue-Violet, Solenoid 27 to Playfield Coil |
| J109-4 | Blue-Gray, Solenoid 28 to Playfield Coil |
| J109-5 | Red-Orange Tieback Diode to Sol. 25, 27, 28 |
| J109-6 | Not Used |
| J109-7 | Key |
| J109-8 | Red-Orange Tieback Diode to Sol. 25, 27, 28 |
| J109-9 | Red-Orange Tieback Diode to Sol. 25, 27, 28 |

#### J110

| Pin | Printed text |
| --- | --- |
| J110-1 | Brown-White to Solenoid 37 to Insert |
| J110-2 | Key |
| J110-3 | Orange-White to Solenoid 38 to Insert |
| J110-4 | Yellow-White to Solenoid 39 to Insert |
| J110-5 | Green-White to Solenoid 40 to Insert |

#### J111

| Pin | Printed text |
| --- | --- |
| J111-1 | Black-Brown, Solenoid 17 to Playfield Flasher |
| J111-2 | Black-Red, Solenoid 18 to Playfield Flasher |
| J111-3 | Black-Orange, Solenoid 19 to Playfield Flasher |
| J111-4 | Black-Yellow, Solenoid 20 to Playfield Flasher |
| J111-5 | Blue-Brown, Solenoid 21 to Playfield Flasher |
| J111-6 | Blue-Red, Solenoid 22 to Playfield Flasher |
| J111-7 | Not Used |
| J111-8 | Not Used |
| J111-9 | Key |
| J111-10 | Not Used |
| J111-11 | Not Used |
| J111-12 | Not Used |
| J111-13 | Not Used |

#### J112

| Pin | Printed text |
| --- | --- |
| J112-1 | Not Used |
| J112-2 | Not Used |
| J112-3 | Not Used |
| J112-4 | Key |
| J112-5 | Not Used |
| J112-6 | Not Used |
| J112-7 | Not Used |
| J112-8 | Blue-Orange, Solenoid 23 to Insert Flasher |
| J112-9 | Blue-Yellow, Solenoid 24 to Insert Flasher |

#### J113

| Pin | Printed text |
| --- | --- |
| J113-1 | Brown-Black, Solenoid 9 Drive to Playfield Coil |
| J113-2 | Key |
| J113-3 | Brown-Red, Solenoid 10 to Playfield Coil |
| J113-4 | Brown-Orange, Solenoid 11 to Playfield Coil |
| J113-5 | Brown-Yellow, Solenoid 12 to Playfield Coil |
| J113-6 | Brown-Green, Solenoid 13 to Playfield Coil |
| J113-7 | Brown-Blue, Solenoid 14 to Playfield Coil |
| J113-8 | Brown-Violet, Solenoid 15 to Playfield Coil |
| J113-9 | Brown-Gray, Solenoid 16 to Playfield Coil |

#### J114, J115

Printed as single lines: `J114 Not Used` and `J115 Not Used`

## Printed page 3-26 (PDF page 150)

### Left column

#### J116

| Pin | Printed text |
| --- | --- |
| J116-1 | Violet-Brown, Solenoid 1 to Playfield Coil |
| J116-2 | Not Used |
| J116-3 | Key |
| J116-4 | Violet-Orange, Solenoid 3 to Playfield Coil |
| J116-5 | Not Used |
| J116-6 | Violet-Green, Solenoid 5 to Playfield Coil |
| J116-7 | Violet-Blue, Solenoid 6 to Playfield Coil |
| J116-8 | Violet-Black, Solenoid 7 to Playfield Coil |
| J116-9 | Violet-Gray, Solenoid 8 to Playfield Coil |

#### J117

Printed as a single line: `J117 Not Used`

#### J118

| Pin | Printed text |
| --- | --- |
| J118-1 | Not Used |
| J118-2 | Violet-Red Solenoid 2 to Backbox Coil |
| J118-3 | Not Used |
| J118-4 | Key |
| J118-5 | Violet-Yellow Solenoid 4 to Backbox Coil |

#### J119

| Pin | Printed text |
| --- | --- |
| J119-1 | Red-Green, +50V to Lower Right Flipper Coil |
| J119-2 | Red-Green, Loop End from J119-1 |
| J119-3 | Key |
| J119-4 | Red-Blue, +50V to Lower Left Flipper |
| J119-5 | Red-Blue, Loop End from J119-4 |
| J119-6 | Red-Violet, +50V to Upper Right Flipper Coil |
| J119-7 | Red-Violet, Loop End from J119-6 |
| J119-8 | Red-Gray, +50V to Playfield Coil 35 & 36 |
| J119-9 | Red-Gray, Loop End from J119-8 |

#### J120

| Pin | Printed text |
| --- | --- |
| J120-1 | Orange-Gray, Holding, Playfield Coil 36 |
| J120-2 | Not Used |
| J120-3 | Yellow-Gray, Power, Playfield Coil 35 |
| J120-4 | Orange-Violet, Holding, Upr Right Flipper Coil |
| J120-5 | Not Used |
| J120-6 | Yellow-Violet, Power, Upr Right Flipper Coil |
| J120-7 | Orange-Blue, Holding, Lower Left Flipper Coil |
| J120-8 | Not Used |
| J120-9 | Yellow-Blue, Power, Lower Left Flipper Coil |
| J120-10 | Key |
| J120-11 | Orange-Green, Holding, Lwr Right Flipper Coil |
| J120-12 | Not Used |
| J120-13 | Yellow-Green, Power, Lower Right Flipper Coil |

#### J121

| Pin | Printed text |
| --- | --- |
| J121-1 | Yellow-Brown, Lamp Col. 1 to Playfield |
| J121-2 | Yellow-Red, Lamp Col. 2 to Playfield |
| J121-3 | Yellow-Orange, Lamp Col. 3 to Playfield |
| J121-4 | Yellow-Black, Lamp Col. 4 to Playfield |
| J121-5 | Yellow-Green, Lamp Col. 5 to Playfield |
| J121-6 | Yellow-Blue, Lamp Col. 6 to Playfield |
| J121-7 | Yellow-Violet, Lamp Col. 7 to Playfield |
| J121-8 | Key |
| J121-9 | Yellow-Gray, Lamp Col. 8 to Playfield |

#### J122

| Pin | Printed text |
| --- | --- |
| J122-1 | Key |
| J122-2 | Not Used |
| J122-3 | Yellow-Gray, Lamp Col 8 to Coin Door Bd. J3-9 |

#### J123, J124

Printed as single lines: `J123 Not Used` and `J124 Not Used`

### Right column

#### J125

| Pin | Printed text |
| --- | --- |
| J125-1 | Red-Brown, Lamp Row 1 to Playfield |
| J125-2 | Red-Black, Lamp Row 2 to Playfield |
| J125-3 | Key |
| J125-4 | Red-Orange, Lamp Row 3 to Playfield |
| J125-5 | Red-Yellow, Lamp Row 4 to Playfield |
| J125-6 | Red-Green, Lamp Row 5 to Playfield |
| J125-7 | Red-Blue, Lamp Row 6 to Playfield |
| J125-8 | Red-Violet, Lamp Row 7 to Playfield |
| J125-9 | Red-Gray, Lamp Row 8 to Playfield |

#### J126

| Pin | Printed text |
| --- | --- |
| J126-1 | Not Used |
| J126-2 | Not Used |
| J126-3 | Key |
| J126-4 | Not Used |
| J126-5 | Not Used |
| J126-6 | Not Used |
| J126-7 | Red-Blue, Lamp Row 6 to Coin Door Bd. J3-10 |
| J126-8 | Red-Violet, Lamp Row 7 to Coin Door Bd. J3-11 |
| J126-9 | Red-Gray, Lamp Row 8 to Coin Door Bd. J3-12 |

#### J127

| Pin | Printed text |
| --- | --- |
| J127-1 | White-Green, 9.8VAC from Xformer Secondary |
| J127-2 | White-Green, 9.8VAC Loop End from J127-1 |
| J127-3 | White-Green, 9.8VAC from Xformer Secondary |
| J127-4 | Key |
| J127-5 | White-Green, 9.8VAC Loop End from J127-3 |

#### J128

| Pin | Printed text |
| --- | --- |
| J128-1 | White-Red, 16VAC Loop End from J128-2 |
| J128-2 | White-Red, 16VAC from Xformer Secondary |
| J128-3 | White-Red, 16VAC Loop End from J128-4 |
| J128-4 | White-Red, 16VAC from Xformer Secondary |
| J128-5 | Black-Yellow, 16VAC Loop End from J128-6 |
| J128-6 | Black-Yellow, 16VAC from Xformer Secondary |
| J128-7 | Key |
| J128-8 | Black-Yellow, 16VAC Loop End from J128-9 |
| J128-9 | Black-Yellow, 16VAC from Xformer Secondary |

#### J129

| Pin | Printed text |
| --- | --- |
| J129-1 | Red, 9VAC from Xformer Secondary |
| J129-2 | Red, 9VAC from Xformer Secondary |
| J129-3 | Key |
| J129-4 | Blue-White, 13VAC from Xformer Secondary |
| J129-5 | Blue-White, 13VAC Loop End from J129-4 |
| J129-6 | Blue-White, 13VAC from Xformer Secondary |
| J129-7 | Blue-White, 13VAC Loop End from J129-6 |

#### J130, J131, J132

Printed as single lines: `J130 Not Used`, `J131 Not Used`, `J132 Not Used`

#### J133

| Pin | Printed text |
| --- | --- |
| J133-1 | Red-Orange, +50V to Playfield Coils |
| J133-2 | Red-Brown, +50V to Playfield Coils |
| J133-3 | Red-Black, +50V to Playfield Coils |
| J133-4 | Key |
| J133-5 | Not Used |
| J133-6 | Red-White, +20V to Playfield Flashlamps |

## Printed page 3-27 (PDF page 151)

Only the left column is printed; the right half of the page is empty.

#### J134

| Pin | Printed text |
| --- | --- |
| J134-1 | Not Used |
| J134-2 | Not Used |
| J134-3 | Not Used |
| J134-4 | Key |
| J134-5 | Red-White, +20VDC to Insert Flashlamps |

#### J135

| Pin | Printed text |
| --- | --- |
| J135-1 | Not Used |
| J135-2 | Red-Brown +50V to Backbox Coils |
| J135-3 | Not Used |

#### J136, J137

Printed as single lines: `J136 Not Used` and `J137 Not Used`

#### J138

| Pin | Printed text |
| --- | --- |
| J138-1 | Key |
| J138-2 | Gray-Yellow, +12V to Backbox Coils |
| J138-3 | Black, Ground to Backbox Coils |
| J138-4 | Not Used |

#### J139

| Pin | Printed text |
| --- | --- |
| J139-1 | Key |
| J139-2 | Gray-Yellow +12V to Coin Door Bd. J2-2 |
| J139-3 | Black Ground to Coin Door Bd. J2-1 |
| J139-4 | Not Used |
| J139-5 | Black-White to Coin Door Bd. J2-7 |

#### J140

| Pin | Printed text |
| --- | --- |
| J140-1 | Key |
| J140-2 | Gray-Yellow, +12V to Backbox Motor |
| J140-3 | Not Used |
| J140-4 | Not Used |

#### J141

| Pin | Printed text |
| --- | --- |
| J141-1 | Key |
| J141-2 | Gray-Yellow, +12V to Playfield Switches |
| J141-3 | Black, Ground to playfield Switches |
| J141-4 | Not Used |

## Row counts

Pin rows transcribed: J101 7, J103 12, J105 11, J106 11, J109 9, J110 5, J111 13, J112 9, J113 9, J116 9, J118 5, J119 9,
J120 13, J121 9, J122 3, J125 9, J126 9, J127 5, J128 9, J129 7, J133 6, J134 5, J135 3, J138 4, J139 5, J140 4, J141 4 =
223 pin rows. Whole-connector lines (no pin rows): `J102` (a one-line description), and `Not Used` for J104, J107, J108,
J114, J115, J117, J123, J124, J130, J131, J132, J136, J137. Every connector J101-J141 appears exactly once in the list, in
ascending order; no pin number is skipped or printed twice within a connector, and every connector's pin rows run from
pin 1 to the pin count shown on the drawing.

## Observations on the printed text

- Lamp matrix connectors. Lamp columns 1-7 are on `J121-1` ... `J121-7` and column 8 on `J121-9` (`J121-8` is `Key`); column 8
  is also printed on `J122-3` (`Yellow-Gray, Lamp Col 8 to Coin Door Bd. J3-9`, the same wire colour as `J121-9`). Lamp rows 1-5 are
  `J125-1`, `J125-2`, `J125-4` ... `J125-6` and rows 6-8 `J125-7` ... `J125-9` (`J125-3` is `Key`); rows 6, 7 and 8 also appear on
  `J126-7`, `J126-8` and `J126-9` to the Coin Door Board `J3-10`, `J3-11`, `J3-12`, with the same wire colours (`Red-Blue`,
  `Red-Violet`, `Red-Gray`) as `J125-7`, `J125-8`, `J125-9`.
- `J123 Not Used` and `J124 Not Used` are printed although the board drawing shows nine-pin connectors J123 and J124.
- Wire colours repeated on several pins: `J103-2` and `J103-3` (`White-Brown`), `J103-5` and `J103-6` (`White-Yellow`), `J109-5`,
  `J109-8` and `J109-9` (`Red-Orange Tieback Diode to Sol. 25, 27, 28`, the same text on three pins), `J127-1` and
  `J127-3` plus their loop ends (`White-Green`), `J129-1` and `J129-2` (`Red`), `J133-1`/`-2`/`-3` (three different `Red-` colours,
  all `+50V to Playfield Coils`), `J135-2` (`Red-Brown`, same colour as `J133-2`).
- Solenoid numbers on the list: 1, 3, 5, 6, 7, 8 on `J116` (pins 1, 4, 6, 7, 8, 9); 2 and 4 on `J118` (pins 2 and 5, `to Backbox Coil`);
  9-16 on `J113` (pins 1, 3-9); 17-22 on `J111` (pins 1-6); 23 and 24 on `J112` (pins 8, 9, `to Insert Flasher`); 25-28 on `J109`
  (pins 1-4; 26 is `to Backbox Motor`); 35 and 36 on `J119`/`J120` (`Playfield Coil 35 & 36`); 37-40 on `J110` (pins 1, 3, 4, 5, `to Insert`).
  No solenoid 29, 30, 31, 32, 33 or 34 is printed on any connector in this list.
- Flipper circuits on `J119`/`J120`: `+50V` to Lower Right (`J119-1`), Lower Left (`J119-4`), Upper Right (`J119-6`) and `Playfield Coil
  35 & 36` (`J119-8`); each with a `Loop End` pin. `J120` has `Holding` and `Power` pins for Playfield Coil 36 (`Holding`, `J120-1`) and
  Playfield Coil 35 (`Power`, `J120-3`; no `Holding` pin for 35), Upper Right (`J120-4` Holding / `J120-6` Power), Lower Left
  (`J120-7` Holding / `J120-9` Power) and Lower Right (`J120-11` Holding / `J120-13` Power). No Upper Left flipper appears. The
  `J119-1` line prints `Flipper Coil`, the `J119-4` line prints only `Lower Left Flipper` (no `Coil`). `J120-4`/`J120-6` use `Upr`;
  `J120-11` uses `Lwr`.
- Line formatting varies: `J110-*` lines have no comma after the wire colour and no function word (`Brown-White to Solenoid 37 to
  Insert`); `J118-2`/`J118-5` have no comma; `J135-2`, `J139-2`, `J139-3`, `J139-5` have no comma; `J141-3` prints `playfield` in lower case.
- `J141-4` is printed as `J1.41-4 Not Used` on page 3-27 (a stray dot after the `1`); transcribed as `J141-4`.
- `J103` uses six `6.8VAC` wire colours (`Yellow-White`, `White-Brown`, `White-Orange`, `White-Yellow`, `Orange`, `Green`) and pins 8, 11
  and 12 are `Not Used`.
- `J105-1` and `J105-7` go to the Coin Door Board `J2-5` and `J2-3`; `J105-3`, `J105-9` go to the Playfield; `J106` carries the Insert Panel G.I.
  returns and the five `6.8VAC` feeds, so the insert panel G.I. is on `J106` and the playfield / coin door G.I. on `J105`.
- Voltages printed: `+12V`, `+5V`, `+50V`, `+20V` / `+20VDC`, `6.8VAC`, `9.8VAC`, `16VAC`, `9VAC`, `13VAC`.

## Reading uncertainties

- Pin-count end labels on the drawing were read from a 1511-px downsampled overview of the whole page (the labels are large); the pin counts agree with the highest pin number in the printed list for every connector that has list rows.
- No `[?]` readings in the pin list text itself; all pin-list lines were read from native-resolution tiles.
