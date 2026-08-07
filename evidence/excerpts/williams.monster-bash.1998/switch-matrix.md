# Monster Bash — Switch Matrix (wiring)

Transcribed from `Williams_1998_Monster_Bash_English_Manual.pdf`, PDF page 119, printed page 2-51,
the `SWITCH MATRIX` table. The retained scan is image-only (`pdftotext` yields 158 bytes of form
feeds only), so this is read from the rendered page, not an OCR text layer. The accompanying crop is
the same region, rendered grayscale so the shaded opto cells stay visible.

Header: `White ---|>--o o--- Green`. Footer: `J2XX = CPU BOARD`; shaded cells `= OPTO, TYPICALLY
CLOSED`. The whole eight-by-eight block is transcribed, not only the addresses the definition names,
so an unshaded or unused cell is as visible as a shaded one.

## Dedicated grounded switches

| Public | Wire | Connector | Return IC | Normal function | Test function |
| --- | --- | --- | --- | --- | --- |
| 1 (D1) | Orange-Brown | J205-1 | U17-5 | LEFT COIN CHUTE | — |
| 2 (D2) | Orange-Red | J205-2 | U17-7 | CENTER COIN CHUTE | — |
| 3 (D3) | Orange-Black | J205-3 | U17-11 | RIGHT COIN CHUTE | — |
| 4 (D4) | Orange-Yellow | J205-4 | U17-9 | 4TH COIN CHUTE | — |
| 5 (D5) | Orange-Green | J205-6 | U16-9 | Service Credits | Escape |
| 6 (D6) | Orange-Blue | J205-7 | U16-11 | Volume Down | Down |
| 7 (D7) | Orange-Violet | J205-8 | U16-7 | Volume Up | Up |
| 8 (D8) | Orange-Gray | J205-9 | U16-5 | Begin Test | Enter |

## Matrix drive columns

| Column | Wire | Connector | Drive IC |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-White | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

## Matrix return rows

| Row | Wire | Connector | Return IC |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | J208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

## Flipper grounded switch wiring

| Printed | Wire | Connector | Matrix-page description |
| --- | --- | --- | --- |
| F1 | Black-Green | J208-13 | LOWER RIGHT FLIPPER E.O.S. |
| F2 | Blue-Violet | J212-12 | LOWER RIGHT FLIPPER OPTO (shaded opto) |
| F3 | Black-Blue | J208-12 | LOWER LEFT FLIPPER E.O.S. |
| F4 | Blue-Gray | J212-11 | LOWER LEFT FLIPPER OPTO (shaded opto) |
| F5 | Black-Violet | J208-11 | UPPER RIGHT FLIPPER E.O.S. |
| F6 | Black-Yellow | J212-10 | UPPER RIGHT FLIPPER OPTO (shaded opto) |
| F7 | Black-Gray | J208-10 | CENTER SPINNER. |
| F8 | Black-Blue | J212-9 | UPPER LEFT FLIPPER OPTO (shaded opto) |

## Which cells are shaded

Optos shaded "typically closed" on the matrix page: 31, 32, 33, 34, 35, 36 (column 3), 42, 43
(column 4), and 74, 75, 76, 77, 78 (column 7), plus F2, F4, F6, F8. This is the region the promotion
review depends on: pinned PinMAME's inverted-switch mask covers only columns 3 and 4 (`0x3f` on
column 3, `0x06` on column 4); column 7 is `0x00`, so the shading on 74-78 is not reproduced by the
emulator's own normalization. Every shaded cell above is shaded on the printed page; none is an
inference from the mask.

## Naming note

The parts list (printed 2-48) calls F2/F4/F6/F8 "… FLIPPER CABINET" while this matrix page (2-51)
calls the same positions "… FLIPPER OPTO". Both describe one device: assembly A-17316 is the Flipper
Opto PCB Assembly (printed 2-11), i.e. the cabinet flipper button implemented as an opto interrupter.
The matrix-page wording is the more precise physical description; the parts-list wording gives the
location.
