# Bally Indianapolis 500 (1995) — Switch Matrix

Source: *Indianapolis 500 Operators Handbook*, 16-10140, July 1995, `Indianapolis_500_OPS.pdf`
PDF page 6, printed page 4, table titled **SWITCH MATRIX**. Read from the native 300 dpi render.

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
| 11 | BALL LAUNCH | 21 | SLAM TILT | 31 | THREE BANK CENTER | 41 | TOP TROUGH [opto] |
| 12 | NOT USED | 22 | COIN DOOR CLOSED | 32 | THREE BANK LOWER | 42 | TROUGH 1 (RIGHT) [opto] |
| 13 | START BUTTON | 23 | BUY-IN BUTTON | 33 | NOT USED | 43 | TROUGH 2 [opto] |
| 14 | PLUMB BOB TILT | 24 | ALWAYS CLOSED | 34 | RIGHT FLIPPER WRENCH | 44 | TROUGH 3 [opto] |
| 15 | LEFT OUTLANE | 25 | SHOOTER LANE | 35 | LEFT RAMP ENTER | 45 | TROUGH 4 (LEFT) [opto] |
| 16 | LEFT FLIPPER LANE | 26 | LEFT SLING-SHOT | 36 | LEFT RAMP MADE | 46 | LEFT RAMP STANDUP |
| 17 | RIGHT FLIPPER LANE | 27 | RIGHT SLING-SHOT | 37 | LEFT LOOP | 47 | TURBO WRENCH |
| 18 | RIGHT OUTLANE | 28 | THREE BANK UPPER | 38 | RIGHT LOOP | 48 | JET BUMPER WRENCH |

| No. | Label | No. | Label | No. | Label | No. | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | LEFT LANE | 61 | UPPER POPPER [opto] | 71 | NOT USED | 81 | NOT USED |
| 52 | CENTER LANE | 62 | TURBO POPPER [opto] | 72 | LEFT JET | 82 | NOT USED |
| 53 | RIGHT LANE | 63 | TURBO BALL SENSE [opto] | 73 | RIGHT JET | 83 | NOT USED |
| 54 | TEN POINT | 64 | UPPER EJECT | 74 | CENTER JET | 84 | NOT USED |
| 55 | LEFT RAMP WRENCH | 65 | LOWER KICKER | 75 | RIGHT RAMP ENTER | 85 | NOT USED |
| 56 | LEFT LIGHTUP [opto] | 66 | TURBO INDEX | 76 | RIGHT RAMP MADE | 86 | NOT USED |
| 57 | CENTER LIGHTUP [opto] | 67 | NOT USED | 77 | NOT USED | 87 | NOT USED |
| 58 | RIGHT LIGHTUP [opto] | 68 | NOT USED | 78 | NOT USED | 88 | NOT USED |

Cell 66 `TURBO INDEX` is printed **without** the opto shading. It is the only turbo-mechanism
switch in column 6 rows 1-3/6 that is unshaded.

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
| F7 | Black-Gray | J906-5 | Upper Left Flipper EOS (NOT USED) |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto (NOT USED) [opto] |

Printing notes, preserved literally: F5 repeats F2's wire colour `Black-Violet`, F7 repeats F4's
`Black-Gray` and F8 repeats F3's `Black-Blue`; they are on different connectors (J906 vs J905).
