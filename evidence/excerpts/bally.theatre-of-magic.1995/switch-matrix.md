# Theatre of Magic — Switch Matrix

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 118, printed page 2-42, the SWITCH MATRIX
table. The retained PDF carries a Paper Capture OCR text layer, but per project policy every table
was verified against a 300 dpi render of the page regardless of the text layer's presence. The
accompanying crop is the same region, rendered grayscale so the shaded opto cells stay visible.

Columns 1-8 headers: 1 Green-Brown/J207-1/U20-18, 2 Green-Red/J207-2/U20-17, 3
Green-Orange/J207-3/U20-16, 4 Green-Yellow/J207-4/U20-15, 5 Green-Black/J207-5/U20-14, 6
Green-Blue/J207-6/U20-13, 7 Green-Violet/J207-7/U20-12, 8 Green-Gray/J207-9/U20-11. Rows 1-8 headers:
1 White-Brown/J209-1/U18-11 ... 8 White-Gray/J209-9/U19-7. Dedicated column (left of the matrix,
printed D1-D8) uses Orange-* wires to J205-*.

Shaded cells ("OPTO, TYPICALLY CLOSED"): column 3 rows 1-6 (addresses 31-36) and column 5 rows 5-8
(addresses 55-58). No other cell is shaded, including column 3 rows 7-8 (37, 38) and column 4 (41-48,
the Lock/Eddy row).

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 21 | Slam Tilt | 31 | Trough Jam (opto) | 41 | Lock 1 |
| 51 | Left Bank Target | 61 | Left Sling | 71 | Center Ramp Exit | 81 | Loop Right |
| 12 | Not Used | 22 | Coin Door Closed | 32 | Trough 1 (opto) | 42 | Lock 2 |
| 52 | Captive Ball Rest | 62 | Right Sling | 72 | Not Used | 82 | Center Ramp Targets |
| 13 | Start Button | 23 | Buy-In | 33 | Trough 2 (opto) | 43 | Lock 3 |
| 53 | Right Lane Enter | 63 | Bottom Jet | 73 | Right Ramp Exit | 83 | Vanish Lock 1 |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Trough 3 (opto) | 44 | Popper |
| 54 | Left Lane Enter | 64 | Middle Jet | 74 | Right Ramp Exit 2 | 84 | Vanish Lock 2 |
| 15 | Shooter Lane | 25 | Left Outlane | 35 | Trough 4 (opto) | 45 | Left Drain Eddy |
| 55 | Cube Position 4 (opto) | 65 | Top Jet | 75 | Center Ramp Enter | 85 | Trunk Hit (eddy) |
| 16 | Not Used | 26 | Left Return Lane | 36 | Subway Opto (opto) | 46 | Not Used |
| 56 | Cube Position 1 (opto) | 66 | Top Lane 1 | 76 | Right Ramp Enter | 86 | Right Lane Exit |
| 17 | Not Used | 27 | Right Return Lane | 37 | Spinner | 47 | Subway Micro |
| 57 | Cube Position 2 (opto) | 67 | Top Lane 2 | 77 | Captive Ball Top | 87 | Left Lane Exit |
| 18 | Not Used | 28 | Right Outlane | 38 | Right Lower Target | 48 | Right Drain Eddy |
| 58 | Cube Position 3 (opto) | 68 | Not Used | 78 | Loop Left | 88 | Not Used |

## Dedicated (grounded) switches D1-D8, printed left of the matrix

| Printed | Wire | Connection | Function |
| --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | Service Credits (normal) / Escape (test) |
| D6 | Orange-Blue | J205-7 | Volume Down (normal) / Down (test) |
| D7 | Orange-Violet | J205-8 | Volume Up (normal) / Up (test) |
| D8 | Orange-Gray | J205-9 | Begin Test (normal) / Enter (test) |

## Flipper Grounded Switches column (rightmost), printed F1-F8

| Printed | Wire | Connector | Description |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Right Flipper EOS |
| F2 (shaded) | Black-Violet | J905-1 | Right Flipper Opto |
| F3 | Black-Blue | J906-3 | Left Flipper EOS |
| F4 (shaded) | Black-Gray | J905-2 | Left Flipper Opto |
| F5 | Black-Violet | J906-4 | Upper Right Flipper EOS |
| F6 (shaded) | Black-Yellow | J905-3 | Upper Right Flipper Opto |
| F7 | Black-Gray | J906-5 | Upper Left Flipper EOS |
| F8 (shaded) | Black-Blue | J905-5 | Upper Left Flipper Opto |

`J2XX = CPU Board; J9XX = Fliptronic II Board`.
