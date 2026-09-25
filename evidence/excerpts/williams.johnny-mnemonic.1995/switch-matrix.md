# Williams Johnny Mnemonic (1995) — Switch Matrix

Source: Williams *Johnny Mnemonic* operations manual (September 1995), IPDB machine 3683 file
`Williams_1995_Johnny_Mnemonic_English_Manual.pdf`, PDF page 102, printed page 2-34. Read from the
native 300 dpi render. The same grid is printed again on the unpaginated quick-reference sheet at
PDF page 141.

A switch symbol between the headers reads `White ─►|─ o/ o─ Green`: each switch sits in series with a
diode from the white row line to the green column line.

Column headers (column, wire, connector, receiver pin):

| Column | Wire | Connector | Pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

Row headers (row, wire, connector, pin): 1 `White-Brown J209-1 U18-11`; 2 `White-Red J209-2 U18-9`;
3 `White-Orange J209-3 U18-5`; 4 `White-Yellow J209-4 U18-7`; 5 `White-Green J209-5 U19-11`;
6 `White-Blue U209-7 U19-9` (the connector is printed `U209-7` in this cell, where every other row
prints `J209-n`); 7 `White-Violet J209-8 U19-5`; 8 `White-Gray J209-9 U19-7`.

Dedicated grounded switches (left block, one per row):

| Position | Wire | Connector | Printed function |
| --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | Normal Function `Srv Crdts`, Test Function `Escape` |
| D6 | Orange-Blue | J205-7 | Normal Function `Volume Dn`, Test Function `Down` |
| D7 | Orange-Violet | J205-8 | Normal Function `Volume Up`, Test Function `Up` |
| D8 | Orange-Gray | J205-9 | Normal Function `Begin Test`, Test Function `Enter` |

Matrix cells (number, printed label). `[shaded]` marks a cell printed with the grey fill that the
legend explains as `= OPTO, TYPICALLY CLOSED.`

| Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- |
| 11 BALL LAUNCH | 21 SLAM TILT | 31 TROUGH JAM [shaded] | 41 LEFT RAMP ENTER |
| 12 X HAND HOME | 22 COIN DOOR CLOSED | 32 TROUGH BALL 1 [shaded] | 42 LEFT RAMP MADE |
| 13 START BUTTON | 23 BUY-IN BUTTON | 33 TROUGH BALL 2 [shaded] | 43 DROP TARGET |
| 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH BALL 3 [shaded] | 44 LEFT JET BUMPER |
| 15 LEFT OUTLANE | 25 LEFT SLINGSHOT | 35 TROUGH BALL 4 [shaded] | 45 BOTTOM JET BUMPER |
| 16 LEFT RETURN LANE | 26 RIGHT SLINGSHOT | 36 BALL POPPER 1 [shaded] | 46 RIGHT JET BUMPER |
| 17 RIGHT RETURN LANE | 27 LEFT STANDUP TARGET | 37 Y HAND HOME | 47 CRAZY BOB'S |
| 18 RIGHT OUTLANE | 28 RIGHT STANDUP TARGET | 38 RIGHT RUBBER | 48 SPINNER |

| Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- |
| 51 CYBER MATRIX 11 | 61 CYBER MATRIX 12 | 71 CYBER MATRIX 13 | 81 NOT USED |
| 52 CYBER MATRIX 21 | 62 CYBER MATRIX 22 | 72 CYBER MATRIX 23 | 82 NOT USED |
| 53 CYBER MATRIX 31 | 63 CYPER MATRIX 32 (sic) | 73 CYBER MATRIX 33 | 83 NOT USED |
| 54 RIGHT RAMP ENTER | 64 LEFT JET LANE | 74 X HAND ENCODER A [shaded] | 84 NOT USED |
| 55 RIGHT RAMP MADE | 65 MIDDLE JET LANE | 75 X HAND ENCODER B [shaded] | 85 NOT USED |
| 56 LEFT LOOP | 66 RIGHT JET LANE | 76 Y HAND ENCODER B [shaded] | 86 NOT USED |
| 57 RIGHT LOOP | 67 RIGHT HAND CONTROL | 77 Y HAND ENCODER A [shaded] | 87 NOT USED |
| 58 INNER LOOP ENTRY | 68 LEFT HAND CONTROL | 78 SHOOTER LANE | 88 NOT USED |

Flipper grounded switches (right block):

| Position | Wire | Connector | Printed label | Shaded |
| --- | --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right Flipper E.O.S. | no |
| F2 | Blue-Violet | J905-1 | Lower Right Flipper Opto | yes |
| F3 | Black-Blue | J906-3 | Lower Left Flipper E.O.S. | no |
| F4 | Blue-Gray | J905-2 | Lower Left Flipper Opto | yes |
| F5 | Black-Violet | J906-4 | BALL IN HAND | no |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Opto | yes |
| F7 | Black-Gray | J906-5 | Upper Left Flipper E.O.S. | no |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto | yes |

Footer: `J2XX = CPU BOARD; J9XX = FLIPTRONIC II BOARD`.

Note: the printed order in column 7 is X encoder A (74), X encoder B (75), then Y encoder **B** (76)
before Y encoder **A** (77). The F6/F8 cells repeat the generic Fliptronic labels; the Switch
Locations parts list (printed 2-35) prints F6, F7 and F8 `Not Used`.
