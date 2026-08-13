# Williams No Good Gofers operations manual - Switch Matrix

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: the `SWITCH MATRIX` wiring table, printed twice - on printed page 2-51 (PDF page 111)
in Section 2 and again on printed page 3-1 (PDF page 116) at the head of Section 3. Both
printings carry identical cell text and identical opto shading. **The Section 2 printing has a
blank column-3 header cell**; the Section 3 printing carries the full header, so column 3's
wire colour, connector and receiver below are taken from the Section 3 copy. The accompanying
crop `switch-matrix.webp` is rendered from the Section 3 page for the same reason.

Transcribed by hand from 300 dpi `pdftoppm` renders of both pages.

Legend printed under the table: `J2XX = CPU BOARD` and a halftone swatch reading
`= OPTO, TYPICALLY CLOSED`. Header decoration above the table: `White --|>|--o--  o-- Green`.

## Drive columns (printed header)

| Column | Wire | CPU connector | Receiver |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-White | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

## Return rows (printed header)

| Row | Wire | CPU connector | Receiver |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | J208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

## Dedicated grounded switches (left-hand column of the printed table)

| Position | Wire | CPU connector | Receiver | Normal function | Test function |
| --- | --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | U17-5 | LEFT COIN CHUTE | - |
| D2 | Orange-Red | J205-2 | U17-7 | CENTER COIN CHUTE | - |
| D3 | Orange-Black | J205-3 | U17-11 | RIGHT COIN CHUTE | - |
| D4 | Orange-Yellow | J205-4 | U17-9 | 4TH COIN CHUTE | - |
| D5 | Orange-Green | J205-6 | U16-9 | Srv Crdts | Escape |
| D6 | Orange-Blue | J205-7 | U16-11 | Volume Dn | Down |
| D7 | Orange-Violet | J205-8 | U16-7 | Volume Up | Up |
| D8 | Orange-Gray | J205-9 | U16-5 | Begin Test | Enter |

## Matrix cells

Cells the printed table shades `OPTO, TYPICALLY CLOSED` are marked **[OPTO]**. The sweep below
covers every one of the sixty-four printed cells, not only the shaded ones.

| Addr | Column/Row | Description | Shaded |
| --- | --- | --- | --- |
| 11 | 1/1 | NOT USED | |
| 12 | 1/2 | LEFT RAMP MAKE | |
| 13 | 1/3 | START BUTTON | |
| 14 | 1/4 | PLUMB BOB TILT | |
| 15 | 1/5 | CENTER RAMP MAKE | |
| 16 | 1/6 | LEFT OUTLANE | |
| 17 | 1/7 | RIGHT IN-LANE | |
| 18 | 1/8 | SHOOTER GROOVE | |
| 21 | 2/1 | SLAM TILT | |
| 22 | 2/2 | COIN DOOR CLOSED | |
| 23 | 2/3 | JET ADVANCE STANDUP | |
| 24 | 2/4 | ALWAYS CLOSED | |
| 25 | 2/5 | UNDERGROUND PASS | |
| 26 | 2/6 | LEFT IN-LANE | |
| 27 | 2/7 | RIGHT OUTLANE | |
| 28 | 2/8 | KICKBACK | |
| 31 | 3/1 | TROUGH EJECT | **[OPTO]** |
| 32 | 3/2 | TROUGH BALL 1 | **[OPTO]** |
| 33 | 3/3 | TROUGH BALL 2 | **[OPTO]** |
| 34 | 3/4 | TROUGH BALL 3 | **[OPTO]** |
| 35 | 3/5 | TROUGH BALL 4 | **[OPTO]** |
| 36 | 3/6 | TROUGH BALL 5 | **[OPTO]** |
| 37 | 3/7 | TROUGH BALL 6 | **[OPTO]** |
| 38 | 3/8 | JET POPPER | **[OPTO]** |
| 41 | 4/1 | LEFT GOFER DOWN | **[OPTO]** |
| 42 | 4/2 | RIGHT GOFER DOWN | **[OPTO]** |
| 43 | 4/3 | NOT USED | |
| 44 | 4/4 | PUTT OUT POPPER | **[OPTO]** |
| 45 | 4/5 | RIGHT POPPER JAM | **[OPTO]** |
| 46 | 4/6 | RIGHT POPPER | **[OPTO]** |
| 47 | 4/7 | LEFT RAMP DOWN | |
| 48 | 4/8 | RIGHT RAMP DOWN | |
| 51 | 5/1 | LEFT SLINGSHOT | |
| 52 | 5/2 | RIGHT SLINGSHOT | |
| 53 | 5/3 | TOP JET BUMPER | |
| 54 | 5/4 | MIDDLE JET BUMPER | |
| 55 | 5/5 | BOTTOM JET BUMPER | |
| 56 | 5/6 | TOP SKILL SHOT | |
| 57 | 5/7 | MIDDLE SKILL SHOT | |
| 58 | 5/8 | LOWER SKILL SHOT | |
| 61 | 6/1 | LEFT SPINNER | |
| 62 | 6/2 | RIGHT SPINNER | |
| 63 | 6/3 | INNER WHEEL OPTO | **[OPTO]** |
| 64 | 6/4 | OUTER WHEEL OPTO | **[OPTO]** |
| 65 | 6/5 | LEFT GOFER 1 | |
| 66 | 6/6 | LEFT GOFER 2 | |
| 67 | 6/7 | BEHIND LEFT GOFER | |
| 68 | 6/8 | HOLE-IN-ONE MADE | |
| 71 | 7/1 | LEFT CART PATH | |
| 72 | 7/2 | RIGHT CART PATH | |
| 73 | 7/3 | RIGHT RAMP MAKE | |
| 74 | 7/4 | GOLF CART | |
| 75 | 7/5 | RIGHT GOFER 1 | |
| 76 | 7/6 | RIGHT GOFER 2 | |
| 77 | 7/7 | ADVANCE TRAP VALUE | |
| 78 | 7/8 | SAND TRAP EJECT | |
| 81 | 8/1 | K-I-C-K ADVANCE | |
| 82 | 8/2 | (K)ICK | |
| 83 | 8/3 | K(I)CK | |
| 84 | 8/4 | KI(C)K | |
| 85 | 8/5 | KIC(K) | |
| 86 | 8/6 | CAPTIVE BALL | |
| 87 | 8/7 | NOT USED | |
| 88 | 8/8 | NOT USED | |

Note: cell 73 is printed `RIGHT RAMP MAKE` on the matrix page while the switch-locations parts
list on 2-49 prints `RIGHT RAMP MADE` for the same item. Both are recorded; the parts list is
taken as the authoritative label.

The shaded set is exactly `{31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 44, 45, 46, 63, 64}` -
fifteen addresses - swept cell by cell across all sixty-four positions of this printing.

## Flipper grounded switches (right-hand column of the printed table)

| Position | Wire | Connector | Description | Shaded |
| --- | --- | --- | --- | --- |
| F1 | BLACK-GREEN | J208-13 | LOWER RIGHT FLIPPER E.O.S. | |
| F2 | BLUE-VIOLET | J212-12 | LOWER RIGHT FLIPPER OPTO | **[OPTO]** |
| F3 | BLACK-BLUE | J208-12 | LOWER LEFT FLIPPER E.O.S. | |
| F4 | BLUE-GRAY | J212-11 | LOWER LEFT FLIPPER OPTO | **[OPTO]** |
| F5 | BLACK-VIOLET | J208-11 | UPPER RIGHT FLIPPER E.O.S. | |
| F6 | BLACK-YELLOW | J212-10 | UPPER RIGHT FLIPPER OPTO | **[OPTO]** |
| F7 | BLACK-GRAY | J208-10 | UPPER LEFT FLIPPER E.O.S. | |
| F8 | BLACK-BLUE | J212-9 | UPPER LEFT FLIPPER OPTO | **[OPTO]** |

Note: `BLACK-BLUE` is printed for both F3 and F8. Preserved verbatim; the same duplicate
appears on other Williams WPC-95 manuals using this table template, and the two positions are
on different connectors (J208-12 and J212-9).

Page footers: `2-51` (Section 2 printing) and `3-1` (Section 3 printing).
