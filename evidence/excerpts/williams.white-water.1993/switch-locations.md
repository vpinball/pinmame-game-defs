# White Water — Switch Locations (parts list)

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF page 104, printed
page 2-42 ("Switch Locations"). Transcribed from a 200 dpi render of the PDF
page; the retained PDF carries a text layer but the two-column layout
scrambles under `pdftotext -layout`, so this transcription is read from the
rendered page, not the OCR text.

Columns are `Sw. No. | Switch Part No. | Description` (left block) and
`Sw. No. | Opto Assy No. | Description` (right block, upper playfield). A
blank Switch Part No. with a populated assembly number in the Opto column is
the manual's opto-construction signature.

## Fliptronic (F1-F8) and cabinet start switch

| Sw. No. | Part No. | Description |
| --- | --- | --- |
| F1 | SW-1A-193 | Lwr Rt. Flipper EOS |
| F2 | 5490-12451-00 | Lwr Rt. Flipper Cab. |
| F3 | SW-1A-193 | Lwr Lt. Flipper EOS |
| F4 | 5490-12451-00 | Lwr Lt. Flipper Cab. |
| F5 | SW-1A-193 | Uppr. Rt. Flipper EOS |
| F6 | 5490-12451-00 | Uppr. Rt. Flipper Cab. |
| 13 | 20-9663-1 | Start Button |
| 14 | 20-9502-A | Plumb Bob Tilt |

F7 and F8 (Upper Left Flipper EOS/Button) are not printed on this page at
all — no row, no part number — confirming the upper-left flipper position is
unfitted on this machine, even though the Switch Matrix wiring page (below)
still prints the F7/F8 column template.

## Left/main-lower matrix block (columns 1-2 plus dedicated 15-18/21-24)

| Sw. No. | Part No. | Description |
| --- | --- | --- |
| 15 | 5647-12133-12 | Outhole |
| 16 | SW-11A-37 | Left Jet Bumper |
| 17 | SW-11A-37 | Right Jet Bumper |
| 18 | SW-11A-37 | Center Jet Bumper |
| 21 | SW-1A-117 | †Slam Tilt |
| 22 | 5643-09288-00 | †Coin Door Closed |
| 23 | Not Used | †Ticket Opto |
| 24 | A-8630 | †Always Closed |
| 25 | 5647-12693-19 | Left Outlane |
| 26 | 5647-12693-19 | Left Flipper Lane |
| 27 | 5647-12693-19 | Right Flipper Lane |
| 28 | 5647-12693-19 | Right Outlane |
| 31 | B-12912-10 | River "R2" |
| 32 | B-12912-10 | River "E" |
| 33 | B-12912-10 | River "V" |
| 34 | B-12912-10 | River "I" |
| 35 | B-12912-10 | River "R1" |
| 36 | B-12912-23 | 3-bank Top |
| 37 | B-12912-23 | 3-bank Center |
| 38 | B-12912-23 | 3-bank Lower |
| 51 | SW-1A-114 (kick) / SW-1A-120 (*score) | Left Sling |
| 52 | SW-1A-114 (kick) / SW-1A-120 (*score) | Right Sling |
| 53 | 5647-12693-04 | Ball Shooter |
| 54 | SW-1A-120 | Lower Jet Arena |
| 55 | SW-1A-120 | Right Jet Arena |
| 56 | A-14604-12 | Extra Ball |
| 57 | 5647-12693-21 | Canyon Main |
| 58 | 5647-12693-13 | Bigfoot Cave |

`*` The Score slingshot switches have diodes across them. `†` Not shown on
the location diagram (dedicated/cabinet switches).

## Upper-playfield block (columns 4/6/7/8, right side of the page)

| Sw. No. | Assy/Part No. | Description |
| --- | --- | --- |
| 41 | A-14604-11 | Light Lock Left |
| 42 | A-14604-11 | Light Lock Right |
| 43 | 5647-12693-19 | Left Loop |
| 44 | 5647-12693-19 | Right Loop |
| 45 | 5647-12693-19 | Secret Passage |
| 46 | 5647-12693-11 | Left Ramp Enter |
| 47 | 5647-12693-11 | Rapids Enter |
| 48 | 5647-12693-11 | Canyon Entrance |
| 61 | A-14315 (LED) / A-14316 (Trans) | Whirlpool Popper |
| 62 | A-14315 (LED) / A-14316 (Trans) | Whirlpool Exit |
| 63 | A-14315 (LED) / A-14316 (Trans) | Lockup Right |
| 64 | A-14315 (LED) / A-14316 (Trans) | Lockup Center |
| 65 | A-14315 (LED) / A-14316 (Trans) | Lockup Left |
| 66 | A-14315 (LED) / A-14316 (Trans) | Left Ramp Main |
| 67 | — | Not Used |
| 68 | A-14315 (LED) / A-14316 (Trans) | Disas. Drop Enter |
| 71 | 5647-12693-21 | Rapids Ramp Main |
| 72 | — | Not Used |
| 73 | B-12912-24 | Hot Foot Upper |
| 74 | B-12912-24 | Hot Foot Lower |
| 75 | 5647-12693-21 | Disas. Drop Main |
| 76 | 5647-12693-08 | Right Trough |
| 77 | 5647-09957-00 | Center Trough |
| 78 | 5647-09957-00 | Left Trough |
| 81 to 85 | — | Not Used |
| 86 | 5490-12451-00 | Bigfoot Opto 1 |
| 87 | 5490-12451-00 | Bigfoot Opto 2 |
| 88 | — | Not Used |

11, 12 are also printed "Not Used" in the left block (not separately
transcribed above; confirmed against the Switch Matrix wiring page, which
shows both as blank cells).

Every switch built from the "A-14315 (LED)" + "A-14316 (Trans)" pair, or from
the single part "5490-12451-00", is an opto/proximity construction with no
mechanical switch part. That set is exactly {61, 62, 63, 64, 65, 66, 68, 86,
87} plus the Fliptronic cabinet-button positions F2, F4, F6 (and the F7/F8
template, unfitted here). No other matrix address in this manual uses either
part number.
