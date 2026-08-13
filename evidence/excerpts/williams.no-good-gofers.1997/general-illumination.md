# Williams No Good Gofers operations manual - General illumination destinations

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: PDF page 144, printed page 3-30, the `Power Driver Board Assembly A-20028`
interboard-wiring list, connectors J104, J105 and J106 in full. Transcribed by hand from a
300 dpi `pdftoppm` render. Every pin of all three connectors is reproduced, including the
pins marked `N/C`, because which pins are *not* connected is what fixes the string-to-panel
assignment.

The general-illumination rows of printed pages 2-44 and 2-53 are transcribed in
`solenoid-flasher-locations.md` and `solenoid-flasher-wiring.md`; this file carries the
destination evidence those two pages do not.

## J104 (coin door)

| Pin | Wire | Description |
| --- | --- | --- |
| J104-1 | WHT-VIO | 6.8VAC for G.I. to Coin Door brd J2-5. |
| J104-2 | KEY | |
| J104-3 | VIO | Return for G.I. to Coin Door board J2-3. |

## J105

| Pin | Wire | Description |
| --- | --- | --- |
| J105-1 | N/C | |
| J105-2 | N/C | |
| J105-3 | YEL | Return for G.I. to insert panel. |
| J105-4 | KEY | |
| J105-5 | GRN | Return for G.I. to insert panel. |
| J105-6 | VIO | Return for G.I. to insert panel. |
| J105-7 | N/C | |
| J105-8 | N/C | |
| J105-9 | WHT-YEL | 6.8VAC for G.I. to insert panel. |
| J105-10 | WHT-GRN | 6.8VAC for G.I. to insert panel. |
| J105-11 | WHT-VIO | 6.8VAC for G.I. to insert panel. |

## J106

| Pin | Wire | Description |
| --- | --- | --- |
| J106-1 | BRN | Return for G.I. to playfield. |
| J106-2 | ORG | Return for G.I. to playfield. |
| J106-3 | YEL | Return for G.I. to playfield. |
| J106-4 | KEY | |
| J106-5 | N/C | |
| J106-6 | N/C | |
| J106-7 | WHT-BRN | 6.8VAC for G.I. to playfield. |
| J106-8 | WHT-ORG | 6.8VAC for G.I. to playfield. |
| J106-9 | WHT-YEL | 6.8VAC for G.I. to playfield. |
| J106-10 | N/C | |
| J106-11 | N/C | |

Page footer: `3-30`.

## What the three tables together say

Each general-illumination string is uniquely identified by its own drive wire colour, and that
colour appears in both the Solenoid/Flasher Table on 2-53 and this wiring list. Matching them
gives, without relying on either page's connector *designators*:

| Public GI address | Printed item | Drive wire | Destination per 3-30 | Bulbs per 2-44 |
| --- | --- | --- | --- | --- |
| 0 | 01 LEFT SIDE STRING | WHT-BRN | playfield (J106-7 / return J106-1 BRN) | #555, #545 |
| 1 | 02 RIGHT SIDE STRING | WHT-ORG | playfield (J106-8 / return J106-2 ORG) | #555, #545 |
| 2 | 03 GOFER SPOTLIGHT | WHT-YEL | playfield (J106-9 / return J106-3 YEL) **and** insert panel (J105-9 / return J105-3 YEL) | #44 playfield plus #555, #545 insert |
| 3 | 04 ILLUMINATION STRING 4 | WHT-GRN | insert panel (J105-10 / return J105-5 GRN) | #44 |
| 4 | 05 ILLUMINATION STRING 5 | WHT-VIO | insert panel (J105-11 / return J105-6 VIO) **and** coin door (J104-1 / return J104-3 VIO) | #44 |

The pin *numbers* printed for the general-illumination block on 2-53 match this list exactly -
1/7, 2/8, 3/9 for the three playfield strings and 5/10, 6/11 for the two insert-panel strings.
Only the connector *designators* are transposed: 2-53 prints `J105` where 3-30 lists those
pins on `J106`, and vice versa. The 3-30 list is internally corroborated because it also
records which pins carry nothing (`J105-1`, `J105-2`, `J105-7`, `J105-8`, `J106-5`, `J106-6`,
`J106-10`, `J106-11` are all `N/C`), so the pins 2-53 attributes to `J105-1/7` and `J105-2/8`
carry no wire at all under the designators 2-53 prints. The wire colours, the placement of
strings 01-03 under 2-53's own *Playfield* voltage/drive sub-columns, the footnote asterisk
appearing only on strings 04 and 05, and string 05's coin-door branch all agree with 3-30's
destinations.
