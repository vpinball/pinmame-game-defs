# Big Bang Bar — Location of Switches & Optos

Transcribed from `Capcom_1996_Big_Bang_Bar_Manual.pdf`, PDF page 87, printed page 83
("Location of Switches & Optos"). Rendered at 300 dpi first, then re-rendered at 600 dpi
in overlapping crops and read visually in full, including every "UNUSED" row; the OCR text
layer was never trusted (Adobe Paper Capture, noisy on dense multi-column tables). PDF page
number = printed page number + 4 (empirically verified against the printed footer on this
page and several neighboring pages).

## Left table — cabinet switches (Ref. 1-18)

Columns: `REF. NO. | DESCRIPTION | SWITCH PART NUMBER`. No opto columns on this table.
Footnotes printed at the bottom of the right table (apply to both): `* NOTE: SWITCH IS
LOCATED IN CABINET.` `** NOTE: NOT SERVICED SEPARATELY.`

| Ref. No. | Description | Switch Part Number |
| --- | --- | --- |
| *1 | COIN DOOR-CHUTE 1 | ** |
| *2 | COIN DOOR-CHUTE 2 | ** |
| *3 | COIN DOOR-CHUTE 3 | ** |
| *4 | COIN DOOR-CHUTE 4 | ** |
| *5 | LEFT FLIPPER BUTTON | SW00127 |
| *6 | RIGHT FLIPPER BUTTON | SW00127 |
| *7 | "START" BUTTON | SW00130 |
| *8 | COIN DOOR OPEN (MODE) | SW00132 |
| *9 | COIN DOOR - SLAM TILT | SW00121 |
| *10 | TILT BOB | A-00065-1 |
| 11-14 | UNUSED | (blacked-out cell, no part number) |
| 15 | TOKEN DISPENSE | (blank) |
| 16 | TICKET DISPENSE | (blank) |
| 17 | 4-BANK MERCURY | SW00106 |
| 18 | 4-BANK VENUS | SW00106 |

Ref. 17/18 print on this same physical page block (a page-layout column split, not a
hardware distinction) despite being genuine playfield switch-matrix positions: they are the
first two members of the 4-Bank drop-target bank, matched exactly by the retained
known-working script's `sol4Bank` reset handler (`DTRaise 17/18/19/20`, the last two of
which print on the right/matrix table below) and by pinned PinMAME's `cc_m2sw` address
arithmetic, which places column 1 (public 17-24) immediately after the 16 cabinet
addresses.

Cross-reference: the companion schematic sheet "DIAGRAM, CABINET SWITCHES, LAMPS & COIN
DOOR WIRING" (sheet 6 of 12, `Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf`)
independently prints a small legend naming switches 5-10 (`5 LEFT FLIPPER`, `6 RIGHT
FLIPPER`, `7 START`, `8 COIN DOOR OPEN`, `10 TILT BOB`), matching this table exactly with
zero disagreement.

## Right table — playfield/matrix switches (Ref. 19-80)

Columns: `REF. NO. | DESCRIPTION | SWITCH PART NUMBER | OPTO RECEIVER P/N | OPTO XMTR. P/N`.

**Scan-quality note:** for every row on this table, the `OPTO RECEIVER P/N` and `OPTO XMTR.
P/N` columns render as a solid black/heavily-noised region in the scan, **except** rows
36-39 (the trough switches), where `A0015604-4R` (receiver) and `A0015702-4R` (transmitter)
print clearly on a clean background — the identical part-number pair the Opto Boards page
(printed page 76) documents for its Receiver/Transmitter board pair. The black region covers
unused rows and ordinary mechanical-switch rows identically, so it is read here as a
print/scan artifact (dirty glass or toner defect over that column band) rather than a
deliberate "shaded = opto" convention; the possibility that it is masking further real opto
part numbers cannot be excluded from this scan alone. Under this reading, only 36-39 are
positively documented as opto by part number on this table.

| Ref. | Description | Switch Part Number | Opto Receiver P/N | Opto Xmtr. P/N |
| --- | --- | --- | --- | --- |
| 19 | 4-BANK PYTHOS | SW00106 | — | — |
| 20 | 4-BANK MARS | SW00106 | — | — |
| 21 | RAMP STAND-UP LEFT | A-00583-FGT | — | — |
| 22 | RAMP STAND-UP RIGHT | A-00583-FGT | — | — |
| 23 | RAMP STAND-UP SIDE | A-00585-FGT | — | — |
| 24 | RAMP ENTRANCE | SW00117 | — | — |
| 25 | SPINNER | SW00107 | — | — |
| 26 | OUTER ORBIT LEFT | SW00111 | — | — |
| 27 | INNER ORBIT LEFT | SW00111 | — | — |
| 28 | ROLLOVER "B" | SW00111 | — | — |
| 29 | ROLLOVER "A" | SW00111 | — | — |
| 30 | ROLLOVER "R" | SW00111 | — | — |
| 31 | TUBE ENTRANCE | SW00142 | — | — |
| 32 | RAMP EXIT | SW00117 | — | — |
| 33 | LEFT FLIPPER E.O.S. | SW00127 | — | — |
| 34 | RIGHT FLIPPER E.O.S. | SW00127 | — | — |
| 35 | OUTHOLE | SW00113 | — | — |
| 36 | TROUGH 1 BALL | — (blank; no mechanical switch) | A0015604-4R | A0015702-4R |
| 37 | TROUGH 2 BALLS | — | A0015604-4R | A0015702-4R |
| 38 | TROUGH 3 BALLS | — | A0015604-4R | A0015702-4R |
| 39 | TROUGH 4 BALLS | — | A0015604-4R | A0015702-4R |
| 40 | UNUSED | — | — | — |
| 41 | LEFT SLINGSHOT | SW00138 | — | — |
| 42 | RIGHT SLINGSHOT | SW00138 | — | — |
| 43 | SHOOTER LANE | SW00112 | — | — |
| 44 | OUTLINED LEFT [sic; almost certainly "OUTLANE LEFT" — see note below] | SW00111 | — | — |
| 45 | INLANE LEFT | SW00111 | — | — |
| 46 | LOWER LOCK 1 BALL | SW00142 | — | — |
| 47 | LOWER LOCK 2 BALLS | SW00142 | — | — |
| 48 | LOWER LOCK 3 BALLS | SW00142 | — | — |
| 49 | 3-BANK URANUS | SW00106 | — | — |
| 50 | 3-BANK NEPTUNE | SW00106 | — | — |
| 51 | 3-BANK PLUTO | SW00106 | — | — |
| 52 | 3-BANK STAND-UP LEFT | SW00141 | — | — |
| 53 | 3-BANK STAND-UP RIGHT | SW00141 | — | — |
| 54 | STAR BUMPER LEFT | SW00126 | — | — |
| 55 | STAR BUMPER RIGHT | SW00126 | — | — |
| 56 | STAR BUMPER MIDDLE | SW00126 | — | — |
| 57 | ALIEN MOTOR | — (blank) | — | — |
| 58 | 1-BANK | SW00106 | — | — |
| 59 | INNER ORBIT RIGHT | SW00111 | — | — |
| 60 | OUTER ORBIT RIGHT | SW00111 | — | — |
| 61 | ALIEN LOCK LEFT | SW00146 | — | — |
| 62 | ALIEN LOCK RIGHT | SW00146 | — | — |
| 63-64 | UNUSED | — | — | — |
| 65 | INLANE RIGHT | SW00111 | — | — |
| 66 | OUTLANE RIGHT | SW00111 | — | — |
| 67 | EJECT HOLE | SW00139 | — | — |
| 68 | U.R. FLIPPER E.O.S. | SW00127 | — | — |
| 69 | ISLAND ENTRANCE | SW00142 | — | — |
| 70 | ISLAND EXIT LEFT | A-00578-L | — | — |
| 71 | ISLAND EXIT RIGHT | A-00578-R | — | — |
| 72-76 | UNUSED | — | — | — |
| 77 | CAPTIVE BOTTOM LEFT | SW00111 | — | — |
| 78 | CAPTIVE TOP LEFT | SW00111 | — | — |
| 79 | CAPTIVE BOTTOM RIGHT | SW00111 | — | — |
| 80 | CAPTIVE TOP RIGHT | SW00111 | — | — |

Note on Ref. 44 "OUTLINED LEFT": read identically twice at 600 dpi. Given Ref. 45 is
"INLANE LEFT" and Ref. 65/66 are "INLANE RIGHT"/"OUTLANE RIGHT" (the mirrored right-side
pair), "OUTLINED LEFT" is almost certainly a typesetting slip for "OUTLANE LEFT" — recorded
verbatim; the correction is an inference, not asserted as the manual's intended text.

Small-numbers check: 16 cabinet positions (incl. unused 11-14) + 64 playfield/matrix
positions (Ref. 19-80) minus the seven explicit "UNUSED" positions (40, 63-64, 72-76) = 57
real playfield switches, consistent with the pinned PinMAME driver comment describing 16
cabinet switches and a 64-position playfield matrix (8x8).
