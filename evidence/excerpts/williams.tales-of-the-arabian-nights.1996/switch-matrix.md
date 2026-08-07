# Tales of the Arabian Nights — Switch Matrix

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, PDF page 120, printed page
2-38, the SWITCH MATRIX table. The retained PDF carries a genuine OCR text layer, but the layout
extraction badly garbles multi-column tables (columns interleave, numbers shift rows), so this was
re-verified against the 300 dpi rendered page image, which is the source of record. The accompanying
crop is the same region, rendered grayscale so the shaded opto cells stay visible.

Legend: shaded cell = "OPTO, TYPICALLY CLOSED". `J2XX = CPU BOARD`. Address = `column * 10 + row`.

| Row \ Column | 1 (Green-Brn, J206-1/U20-18) | 2 (Green-Red, J206-2/U20-17) | 3 (Green-Org, J206-3/U20-16) | 4 (Green-Yel, J206-4/U20-15) | 5 (Green-Blk, J206-5/U20-14) | 6 (Green-Blu, J206-6/U20-13) | 7 (Green-Vio, J206-7/U20-12) | 8 (Green-Gry, J206-9/U20-11) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (D1 Orange-Brn/White-Brn) | 11 HAREM PASSAGE | 21 SLAM TILT | 31 TROUGH EJECT (opto) | 41 RAMP MADE LEFT | 51 LEFT SLING | 61 LEFT STANDUPS | 71 NOT USED | 81 NOT USED |
| 2 (D2 Orange-Red/White-Red) | 12 VANISH TUNNEL | 22 COIN DOOR CLOSED | 32 TROUGH BALL 1 (opto) | 42 GENIE TARGET | 52 RIGHT SLING | 62 RIGHT STANDUPS | 72 NOT USED | 82 NOT USED |
| 3 (D3 Orange-Blk/White-Org) | 13 START BUTTON | 23 GENIE STANDUP TARGET | 33 TROUGH BALL 2 (opto) | 43 LEFT LOOP | 53 LEFT JET | 63 TOP SKILL | 73 NOT USED | 83 NOT USED |
| 4 (D4 Orange-Yel/White-Yel) | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH BALL 3 (opto) | 44 INNER LOOP LEFT | 54 RIGHT JET | 64 MIDDLE SKILL | 74 NOT USED | 84 NOT USED |
| 5 (D5 Orange-Grn/White-Grn) | 15 RAMP ENTER | 25 BAZAAR EJECT | 35 TROUGH BALL 4 (opto) | 45 INNER LOOP RIGHT | 55 MIDDLE JET | 65 BOTTOM SKILL | 75 NOT USED | 85 NOT USED |
| 6 (D6 Orange-Blu/White-Blu) | 16 LEFT OUTLANE | 26 LEFT INLANE | 36 LEFT CAGE OPTO (opto) | 46 MINI STANDUPS | 56 LAMP SPIN CCW | 66 LOCK 1 (BOTTOM) | 76 NOT USED | 86 NOT USED |
| 7 (D7 Orange-Vio/White-Vio) | 17 RIGHT INLANE | 27 RIGHT OUTLANE | 37 RIGHT CAGE OPTO (opto) | 47 RAMP MADE RIGHT | 57 LAMP SPIN CW | 67 LOCK 2 (MIDDLE) | 77 NOT USED | 87 NOT USED |
| 8 (D8 Orange-Gry/White-Gry) | 18 BALL SHOOTER | 28 LEFT WIRE MAKE | 38 LEFT EJECT (not opto) | 48 RIGHT CAPTIVE BALL | 58 LEFT CAPTIVE BALL | 68 LOCK 3 (TOP) | 78 NOT USED | 88 NOT USED |

Dedicated grounded switches D1-D8 (left column): D1 Left Coin Chute, D2 Center Coin Chute, D3 Right
Coin Chute, D4 4th Coin Chute, D5 Srv Crdts/Escape, D6 Volume Dn/Down, D7 Volume Up/Up, D8 Begin
Test/Enter.

## Flipper grounded switches (rightmost column, all printed grounded, address = `110 + Fn`)

| Printed | Wire / connector | Description | Shaded (opto)? |
| --- | --- | --- | --- |
| F1 | Black-Green, J208-13 | Lower Right Flipper E.O.S. | No |
| F2 | Blue-Violet, J212-12 | Lower Right Flipper Opto | Yes |
| F3 | Black-Blue, J208-12 | Lower Left Flipper E.O.S. | No |
| F4 | Blue-Gray, J212-11 | Lower Left Flipper Opto | Yes |
| F5 | Black-Violet, J208-11 | Upper Right Flipper E.O.S. | No |
| F6 | Black-Yellow, J212-10 | Upper Right Flipper Opto | Yes |
| F7 | Black-Gray, J208-10 | Upper Left Flipper E.O.S. | No |
| F8 | Black-Blue, J212-9 | Upper Left Flipper Opto | Yes |
