# Bally The Shadow (1994) — Switch Matrix

Source: *The Shadow* Operations Manual 16-50032-101, November 1994 (`Manual_Bally_1994_The_Shadow.pdf`,
IPDB 2528), PDF page 135, printed page 2-40, table titled **SWITCH MATRIX**. Read from the native
300 dpi render.

Header diagram as printed: `White —▶|—o/ o— Green`. Footnote as printed:
`J2XX = CPU Board; J9XX = Fliptronic II Board;` followed by a shaded swatch `= Opto, Typically Closed`.

## Column header (drive)

| Column | Wire | Connector | Driver |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

## Row header (return)

| Row | Wire | Connector | Receiver |
| --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

## Matrix cells (`[opto]` marks a cell printed with the opto shading)

| No. | Label | No. | Label | No. | Label | No. | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | GUN TRIGGER | 21 | SLAM TILT | 31 | LEFT RAMP ENTER [opto] | 41 | TROUGH 1 [opto] |
| 12 | RIGHT PHURBA CONTROL | 22 | COIN DOOR CLOSED | 32 | RIGHT RAMP ENTER [opto] | 42 | TROUGH 2 [opto] |
| 13 | START BUTTON | 23 | BUY-IN BUTTON | 33 | INNER SANCTUM [opto] | 43 | TROUGH 3 [opto] |
| 14 | PLUMB BOB TILT | 24 | ALWAYS CLOSED | 34 | LEFT PHURBA CONTROL | 44 | TROUGH 4 [opto] |
| 15 | RIGHT OUTLANE | 25 | (M)ONGOL TARGET | 35 | LEFT RUBBER | 45 | TROUGH 5 [opto] |
| 16 | RIGHT RETURN LANE | 26 | M(O)NGOL TARGET | 36 | MINI KICKER [opto] | 46 | TOP TROUGH [opto] |
| 17 | LEFT RETURN LANE | 27 | MONGO(L) TARGET | 37 | MINI LIMIT LEFT [opto] | 47 | INNER LOOP ENTER [opto] |
| 18 | LEFT OUTLANE | 28 | MONG(O)L TARGET | 38 | MINI LIMIT RIGHT [opto] | 48 | SHOOTER |

| No. | Label | No. | Label | No. | Label | No. | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | WALL TARGET DOWN | 61 | LEFT SLINGSHOT | 71 | MINI LEFT STANDUP 1 | 81 | MINI RIGHT STANDUP 4 |
| 52 | MO(N)GOL TARGET | 62 | RIGHT SLINGSHOT | 72 | MINI LEFT STANDUP 2 | 82 | MINI RIGHT STANDUP 3 |
| 53 | MON(G)OL TARGET | 63 | LOCKUP RIGHT | 73 | MINI LEFT STANDUP 3 | 83 | NOT USED |
| 54 | LEFT LOOP ENTER | 64 | LOCKUP MIDDLE | 74 | MINI LEFT STANDUP 4 | 84 | MINI RIGHT STANDUP 1 |
| 55 | BATTLE DROP DOWN | 65 | LOCKUP LEFT | 75 | LEFT RAMP LEFT MADE | 85 | MINI DROP LEFT [opto] |
| 56 | CENTER STANDUP | 66 | LEFT EJECT | 76 | LEFT RAMP RIGHT MADE | 86 | MINI DROP MIDDLE LEFT [opto] |
| 57 | RIGHT LOOP ENTER | 67 | RIGHT EJECT | 77 | RIGHT RAMP LEFT MADE | 87 | MINI DROP MIDDLE RIGHT [opto] |
| 58 | MINI EXIT TUBE | 68 | POPPER | 78 | RIGHT RAMP RIGHT MADE | 88 | MINI DROP RIGHT [opto] |

Cell 48 `SHOOTER` is printed **without** the opto shading; every other cell in column 4 is shaded.
The whole of column 3 is shaded except 34 `LEFT PHURBA CONTROL` and 35 `LEFT RUBBER`.

## Dedicated Grounded Switches (left block)

| Position | Wire | Connector | Printed function |
| --- | --- | --- | --- |
| (1) D1 | Orange-Brown | J205-1 | Left Coin Chute |
| (2) D2 | Orange-Red | J205-2 | Center Coin Chute |
| (3) D3 | Orange-Black | J205-3 | Right Coin Chute |
| (4) D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| (5) D5 | Orange-Green | J205-6 | Normal Function `Ser Credits`, Test Function `Esc` |
| (6) D6 | Orange-Blue | J205-7 | Normal Function `Vol Down`, Test Function `Down` |
| (7) D7 | Orange-Violet | J205-8 | Normal Function `Vol Up`, Test Function `Up` |
| (8) D8 | Orange-Gray | J205-9 | Normal Function `Begin Test`, Test Function `Enter` |

## Flipper Grounded Switches (right block; `[opto]` = printed shaded)

| Position | Wire | Connector | Printed function |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Right Flipper EOS |
| F2 | Black-Violet | J905-1 | Right Flipper Opto [opto] |
| F3 | Black-Blue | J906-3 | Left Flipper EOS |
| F4 | Black-Gray | J905-2 | Left Flipper Opto [opto] |
| F5 | Black-Violet | J906-4 | Upper Right Flipper EOS |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Opto [opto] |
| F7 | Black-Gray | J906-5 | Upper Left Flipper EOS |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto [opto] |

Printing notes, preserved literally: F5 repeats F2's wire colour `Black-Violet`, F7 repeats F4's
`Black-Gray` and F8 repeats F3's `Black-Blue`; they are on different connectors (J906 vs J905). This
page prints F7 and F8 with their generic Fliptronic names and no `NOT USED`; the switch locations list
on the same page prints both `Not Used` with no part number.
