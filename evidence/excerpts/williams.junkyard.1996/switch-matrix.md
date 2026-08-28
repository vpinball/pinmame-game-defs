# Williams Junk Yard (1996) — Switch Matrix

Source: Williams Junk Yard Operations Manual.

- Primary copy: printed page 2-34 (`p-110.png`, 200dpi render)
- Repeated copy: printed page 3-2 (`p-118.png`, 200dpi render) — also carries the "SWITCH MATRIX CIRCUIT" schematic and explanatory paragraph below the table
- Repeated copy: fold-out reference card (`p-145.png`, 200dpi render) — printed directly below the LAMP MATRIX table

All three copies were compared cell-by-cell; **no textual differences were found** between them. Page 118 and page 145 render the opto shading pattern more legibly than page 110, so shading calls below are taken from those two (they agree with each other).

Header wiring legend (top of table, all three copies): `White ─┤⊢○—○─ Green` (a switch symbol between the White and Green wire-color labels).

Column header block (row under "Column \ Row"):

| Column | Wire color | CPU connector (J206) | CPU board pin (U20) |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-Yellow | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

Row header block (left of table, "Dedicated Grounded Switches" column) and the "Flipper Grounded Switches" column on the right are transcribed per-row below the main grid.

## Legend

Printed directly under the table on all three copies:

> `J2XX = CPU BOARD`   `[shaded box] = OPTO, TYPICALLY CLOSED`

A shaded (grey-hatched) table cell denotes an opto (photo-interrupter) switch that is typically closed. Shading calls below are noted per cell as **(OPTO)**.

## Full 8×8 switch matrix

Row/column intersection gives the switch address (first digit = column, second digit = row).

| Row \ Col | 1 (Green-Brown) | 2 (Green-Red) | 3 (Green-Orange) | 4 (Green-Yellow) | 5 (Green-Black) | 6 (Green-Blue) | 7 (Green-Violet) | 8 (Green-Gray) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1** (White-Brown, D1) | 11 TOASTER GUN | 21 SLAM TILT | 31 TROUGH EJECT **(OPTO)** | 41 PAST SPINNER | 51 LEFT SLING | 61 UPPER RIGHT 3 BANK BOTTOM | 71 RAMP ENTRY | 81 NOT USED |
| **2** (White-Red, D2) | 12 REBOUND SWITCH | 22 COIN DOOR CLOSED | 32 TROUGH BALL 1 **(OPTO)** | 42 IN THE SEWER | 52 RIGHT SLING | 62 UPPER RIGHT 3 BANK MIDDLE | 72 SCOOP DOWN | 82 NOT USED |
| **3** (White-Orange, D3) | 13 START BUTTON | 23 NOT USED | 33 TROUGH BALL 2 **(OPTO)** | 43 LOCK JAM | 53 CAR TARGET 4 | 63 UPPER RIGHT 3 BANK TOP | 73 SCOOP MADE | 83 NOT USED |
| **4** (White-Yellow, D4) | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH BALL 3 **(OPTO)** | 44 PAST CRANE | 54 CAR TARGET 5 (RIGHT) | 64 UPPER LEFT 3 BANK BOTTOM | 74 DOG ENTRY | 84 NOT USED |
| **5** (White-Green, D5) | 15 TOP LEFT CRANE | 25 NOT USED | 35 TROUGH BALL 4 **(OPTO)** | 45 RAMP EXIT | 55 NOT USED | 65 UPPER LEFT 3 BANK MIDDLE | 75 NOT USED | 85 NOT USED |
| **6** (White-Blue, D6) | 16 LEFT OUTLANE | 26 RIGHT RETURN LANE | 36 LOCK UP 2 **(OPTO)** | 46 CAR TARGET 1 (LEFT) | 56 LOWER LEFT 3 BANK BOTTOM | 66 UPPER LEFT 3 BANK TOP | 76 RIGHT 3 BANK BOTTOM | 86 NOT USED |
| **7** (White-Violet, D7) | 17 LEFT RETURN LANE | 27 RIGHT OUTLANE | 37 LOCK UP 1 **(OPTO)** | 47 CAR TARGET 2 | 57 LOWER LEFT 3 BANK MIDDLE | 67 BOWL ENTRY | 77 RIGHT 3 BANK MIDDLE | 87 NOT USED |
| **8** (White-Gray, D8) | 18 SHOOTER LANE | 28 CRANE DOWN | 38 TOP RIGHT CRANE | 48 CAR TARGET 3 | 58 LOWER LEFT 3 BANK TOP | 68 BOWL EXIT | 78 RIGHT 3 BANK TOP | 88 NOT USED |

Note: column 3 (Green-Orange) is shaded/opto for rows 1–7 (addresses 31, 32, 33, 34, 35, 36, 37) but **not** for row 8 (address 38, TOP RIGHT CRANE, which is an ordinary mechanical switch on the same column).

## Dedicated grounded switches (row headers, left of grid)

| Row | Label | Wire | Connector | Pin |
| --- | --- | --- | --- | --- |
| D1 | Orange-Brown / J205-1 / Left Coin Chute / U17-5 | White-Brown | J208-1 | U18-11 |
| D2 | Orange-Red / J205-2 / Center Coin Chute / U17-7 | White-Red | J208-2 | U18-9 |
| D3 | Orange-Black / J205-3 / Right Coin Chute / U17-11 | White-Orange | J208-3 | U18-5 |
| D4 | Orange-Yellow / J205-4 / 4th Coin Chute / U17-9 | White-Yellow | J208-4 | U18-7 |
| D5 | Orange-Green / J205-6 U16-9 — Normal Function: Srv Crdts / Test Function: Escape | White-Green | J208-5 | U19-11 |
| D6 | Orange-Blue / J205-7 U16-11 — Normal Function: Test / Test Function: Volume Dn Down | White-Blue | J208-7 | U19-9 |
| D7 | Orange-Violet / J205-8 U16-7 — Normal Function: Test / Test Function: Volume Up Up | White-Violet | J208-8 | U19-5 |
| D8 | Orange-Gray / J205-9 U16-5 — Normal Function: Test/Begin Test / Test Function: Enter | White-Gray | J208-9 | U19-7 |

These are the printed row-header labels, not additional matrix cells; D1–D4 are the four coin-chute switches, D5–D8 double as the four cabinet Test/Volume/Escape/Enter service buttons depending on Normal vs. Test mode.

## Flipper grounded switches (rightmost column)

| Address | Label | Wire | Connector | Shading |
| --- | --- | --- | --- | --- |
| F1 | Lower Right Flipper E.O.S. | Black-Green | J208-13 | not shaded |
| F2 | Lower Right Flipper Opto | Blue-Violet | J212-12 | **(OPTO)** |
| F3 | Lower Left Flipper E.O.S. | Black-Blue | J208-12 | not shaded |
| F4 | Lower Left Flipper Opto | Blue-Gray | J212-11 | **(OPTO)** |
| F5 | SPINNER | Black-Violet | J208-11 | not shaded |
| F6 | Upper Right Flipper Opto | Black-Yellow | J212-10 | **(OPTO)** |
| F7 | Upper Left Flipper E.O.S. | Black-Gray | J208-10 | not shaded |
| F8 | Upper Left Flipper Opto | Black-Blue | J212-9 | **(OPTO)** |

Note: F5 is printed "SPINNER", not a flipper E.O.S./opto label, despite sharing the Flipper Grounded Switches column with the other seven flipper contacts.

## Copy comparison

Pages 110 (2-34), 118 (3-2), and 145 (fold-out card) print byte-for-byte identical cell text, dedicated-switch headers, and flipper-column labels. Page 110 is a low-shading render at this resolution; pages 118 and 145 clearly show the grey opto hatching and independently agree on which cells are shaded (column 3 rows 1–7, plus flipper addresses F2/F4/F6/F8). No cross-copy disagreement was found.
