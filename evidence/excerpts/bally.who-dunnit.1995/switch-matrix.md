# WHO dunnit — switch matrix and locations

Source: Bally *WHO dunnit* manual, PDF pages 126–127, printed 2-44–2-45, and PDF page 157, printed 3-25 Fliptronic II connector list. Transcribed and visually checked against the rendered pages on 2026-09-30. `O` means the cell carries the printed “Opto, Typically Closed” halftone. A dash means the manual prints “Not Used”; it does not stand for an omitted row. The unshaded 12, 25, 47 and 48 still have opto parts in the locations list, an omission of shading rather than an assertion that those contacts are mechanical.

| Column | Drive wire | CPU connector | Driver |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

| Row | Return wire | CPU connector | Receiver |
| --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

| Address | Printed label | Address | Printed label | Address | Printed label | Address | Printed label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | 3-BANK POSITION 2 | 21 | SLAM TILT | 31 O | TROUGH JAM | 41 O | TOP LEFT HOLE |
| 12 | SLOT INDEX LEFT | 22 | COIN DOOR CLOSED | 32 O | TROUGH 1 | 42 O | POST JETS |
| 13 | START BUTTON | 23 | BUY-IN BUTTON | 33 O | TROUGH 2 | 43 O | BACK RIGHT POPPER |
| 14 | PLUMB BOB TILT | 24 | ALWAYS CLOSED | 34 O | TROUGH 3 | 44 O | LOWER RIGHT POPPER |
| 15 | SHOOTER LANE | 25 | SLOT INDEX CENTER | 35 O | TROUGH 4 | 45 | NOT USED |
| 16 | RIGHT OUTLANE | 26 | LEFT INLANE | 36 O | ENTER RAMP | 46 | NOT USED |
| 17 | RIGHT INLANE | 27 | LEFT OUTLANE | 37 O | MADE RAMP LEFT | 47 | ENTER RIGHT HOLE |
| 18 | RIGHT LOOP | 28 | LEFT LOOP | 38 | NOT USED | 48 | SLOT INDEX RIGHT |
| 51 | LOCK UP 1 | 61 | LEFT SLING | 71 | TOP 2-BANK | 81 | NOT USED |
| 52 | TOP 4-BANK | 62 | RIGHT SLING | 72 | BOTTOM 2-BANK | 82 | NOT USED |
| 53 | 2ND 4-BANK | 63 | LEFT JET | 73 | 3-BANK POSITION UP | 83 | NOT USED |
| 54 | 3RD 4-BANK | 64 | BOTTOM JET | 74 | UP DOWN RAMP | 84 | NOT USED |
| 55 | BOTTOM 4-BANK | 65 | RIGHT JET | 75 | SCOOP CENTER | 85 | NOT USED |
| 56 | MYSTERY TARGET | 66 | LEFT 3-BANK | 76 | SCOOP RIGHT | 86 | NOT USED |
| 57 | LOWER RIGHT LOCK 2 | 67 | CENTER 3-BANK | 77 | SCOOP LEFT | 87 | NOT USED |
| 58 | RED | 68 | RIGHT 3-BANK | 78 | BLACK | 88 | NOT USED |

The printed shaded set is 31–37 and 41–44. The full locations list also identifies the unshaded 12, 25 and 48 as A-20511 slot-index assemblies and 47 as an A-16908/A-16909 LED/transistor pair. The visible switch-matrix halftone therefore omits four fitted optos. The `*` footnote means “Not Shown”; dagger means “Located Under Playfield.”

The dedicated grounded switches D1–D8 are left, center, right and fourth coin chutes, Service Credits/Escape, Volume Down/Down, Volume Up/Up, and Begin Test/Enter, respectively. Their wires/connectors are Orange-Brown J205-1, Orange-Red J205-2, Orange-Black J205-3, Orange-Yellow J205-4, Orange-Green J205-6, Orange-Blue J205-7, Orange-Violet J205-8, Orange-Gray J205-9. Fliptronic F1–F8 are lower right EOS, lower right cabinet opto, lower left EOS, lower left cabinet opto, spinner, and three printed Not Used positions. The matrix prints the first four Fliptronic wires/connectors as Black-Green J906-1, Black-Violet J905-1, Black-Blue J906-3 and Black-Gray J905-2; F5 is Black-Violet J906-4, F6 Black-Yellow J905-3, F7 Black-Gray J906-5, F8 Black-Blue J905-5.

The F4 Black-Gray/J905-2 reading above is a matrix claim. PDF 157 (3-25) independently prints **J905-2 Blue-Gray to left flipper opto** in the Fliptronic II connector list. The pin and device agree; this factory wire-colour difference remains unresolved in `conflict.left-flipper-opto-wire`. See [the retained connector excerpt](flipper-circuits.md). No physical colour is selected.

PDF 126's locations list prints F6/F7/F8 switch parts as literal `---`, each described **Not Used**. In the matrix F6 is Black-Yellow J905-3 Upper Right Flipper Opto (NOT USED), and F8 Black-Blue J905-5 Upper Left Flipper Opto (NOT USED). PDF 157 instead routes those individual pins to right/left flipper optos. Each belongs to its own public channel 116/118, not primary112/114. The auxiliary fitment/usage difference is preserved as unresolved; no actual fitted auxiliary part or always-mirrored physical relationship is inferred from the board list or keyboard synthesis.

The locations-table switch-part cells, compacted only where identical:

| Address(es) | Printed switch part(s) |
| --- | --- |
| 11, 73 | 5647-12693-06 |
| 12, 25, 48 | A-20511 |
| 13 | 20-9663-1 |
| 14 | 04-10346 |
| 15 | 5647-12693-62 |
| 16–17, 26–28 | 5647-12693-19 |
| 21 | A-17238 |
| 22 | 5643-09288-00 |
| 23 | 20-9663-18 |
| 24 | 5643-09112-00 |
| 31–35 | A-18617-1 LED and A-18618-1 transistor |
| 36–37, 41–44 | A-16908 LED and A-16909 transistor |
| 47 | A-16908 and A-16909 transistor; its first description is printed “Enter Right Hole” without the `(LED)` parenthetical |
| 38, 45–46, 81–88 | --- Not Used |
| 51 | 5647-12133-11 |
| 52–55 | A-20575-5 |
| 56 | A-17799-15 |
| 57 | 5647-12693-26 |
| 58 | A-18530-4 |
| 61–62 | SW-1A-114 (kicker), SW-1A-120 (score) |
| 63–65 | SW-11A-37 |
| 66 | SW-1A-197-1 |
| 67–68 | SW-1A-198-1 |
| 71–72 | A-20505-6 |
| 74 | 5647-12693-36 |
| 75–77 | 5647-12693-21 |
| 78 | A-16816-7 |
