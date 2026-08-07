# Cactus Canyon — Switch Matrix

Transcribed from `Cactus_Canyon_Manual.pdf`, PDF page 101, printed page 2-43, the SWITCH MATRIX
table. The retained PDF carries an OCR text layer, but it is garbled on this dense tabular page, so
this is confirmed against the rendered page, which is the source of record. The accompanying crop is
the same region, rendered grayscale so the shaded opto cells stay visible.

Address = column x 10 + row. Shaded cells ("OPTO, TYPICALLY CLOSED" per the page legend) are marked
`[OPTO]` below; this shading covers only column 3 plus the four Flipper-Opto rows (F2/F4/F6/F8) in
the separate Fliptronic block — it is not exhaustive of every opto address the manual documents (see
`switch-locations.md` for the full two-cue sweep).

| Row (return) | Col1 Green-Brown | Col2 Green-Red | Col3 Green-Orange [OPTO col] | Col4 Green-White | Col5 Green-Black | Col6 Green-Blue | Col7 Green-Violet | Col8 Green-Gray |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 NOT USED | 21 SLAM TILT | 31 TROUGH EJECT `[OPTO]` | 41 MINE POPPER | 51 LEFT SLINGSHOT | 61 DROP #1 LEFT | 71 TRAIN ENCODER | 81 NOT USED |
| 2 | 12 NOT USED | 22 COIN DOOR CLOSED | 32 TROUGH BALL 1 `[OPTO]` | 42 SALOON POPPER | 52 RIGHT SLINGSHOT | 62 DROP #2 LEFT CENTER | 72 TRAIN HOME | 82 CENTER RAMP ENTER |
| 3 | 13 START BUTTON | 23 NOT USED | 33 TROUGH BALL 2 `[OPTO]` | 43 NOT USED | 53 LEFT JET BUMPER | 63 DROP #3 RIGHT CENTER | 73 SALOON GATE | 83 LEFT RAMP MAKE |
| 4 | 14 PLUMB BOB TILT | 24 ALWAYS CLOSED | 34 TROUGH BALL 3 `[OPTO]` | 44 TOP RIGHT STANDUP | 54 RIGHT JET BUMPER | 64 DROP #4 RIGHT | 74 NOT USED | 84 CENTER RAMP MAKE |
| 5 | 15 MINE ENTRANCE | 25 NOT USED | 35 TROUGH BALL 4 `[OPTO]` | 45 NOT USED | 55 BOTTOM JET BUMPER | 65 RIGHT RAMP MAKE | 75 SALOON BART TOY | 85 LEFT RAMP ENTER |
| 6 | 16 LEFT OUTLANE | 26 LEFT RETURN LANE | 36 LEFT LOOP BOTTOM `[OPTO]` | 46 BEER MUG SWITCH | 56 RIGHT LOOP TOP | 66 RIGHT RAMP ENTER | 76 NOT USED | 86 TOP LEFT STANDUP |
| 7 | 17 RIGHT RETURN LANE | 27 RIGHT OUTLANE | 37 RIGHT LOOP BOTTOM `[OPTO]` | 47 LEFT BONUS 'X' LANE | 57 RIGHT BONUS 'X' LANE | 67 SKILL BOWL | 77 MINE HOME | 87 BOTTOM LEFT STANDUP |
| 8 | 18 SHOOTER LANE | 28 BOTTOM RIGHT STANDUP | 38 NOT USED `[OPTO]` | 48 JET EXIT | 58 LEFT LOOP TOP | 68 BOTTOM RIGHT RAMP | 78 MINE ENCODER | 88 NOT USED |

Dedicated grounded switches (D1-D8, coin door column, address 1-8): 1 Left Coin Chute, 2 Center Coin
Chute, 3 Right Coin Chute, 4 4th Coin Chute, 5 Srv Crdts/Escape (normal function/test function), 6
Volume Dn/Down, 7 Volume Up/Up, 8 Begin Test/Enter. (Rows 5-8 double as service-menu navigation, per
the manual's row labels "Normal Function"/"Test Function".)

## Flipper grounded switches (Fliptronic column, printed F1-F8)

| Printed | Wire | Description | Shaded opto? |
| --- | --- | --- | --- |
| F1 | Black-Green J208-13 | LOWER RIGHT FLIPPER E.O.S. | no |
| F2 | Blue-Violet J212-12 | LOWER RIGHT FLIPPER OPTO | yes |
| F3 | Black-Blue J208-12 | LOWER LEFT FLIPPER E.O.S. | no |
| F4 | Blue-Gray J212-11 | LOWER LEFT FLIPPER OPTO | yes |
| F5 | Black-Violet J208-11 | UPPER RIGHT FLIPPER E.O.S. | no |
| F6 | Blue-Yellow J212-10 | UPPER RIGHT FLIPPER OPTO | yes (unfitted — this machine has no upper flippers) |
| F7 | Black-Gray J208-10 | UPPER LEFT FLIPPER E.O.S. | no |
| F8 | Black-Blue J212-9 | UPPER LEFT FLIPPER OPTO | yes (unfitted — this machine has no upper flippers) |
