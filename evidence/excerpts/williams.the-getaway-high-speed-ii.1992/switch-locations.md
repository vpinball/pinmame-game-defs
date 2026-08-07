# The Getaway: High Speed II — Switch Locations parts list

Transcribed from `Getaway_HSII_OPS.pdf`, PDF page 101, printed page 2-40, "Switch Locations".
Produced by rendering the retained PDF at 300 dpi with `pdftoppm` and reading the table directly
(the retained OCR text layer was not trusted for this table).

| Item | Switch No. | Switch Assy No. | Description |
| --- | --- | --- | --- |
| 11 | SW-1A-193 | A-15205-R | Upper Right Flipper * |
| 11 | SW-1A-193 | A-15205-R-2 | Lower Right Flipper * |
| 12 | SW-1A-193 | A-15205-L-2 | Left Flipper ** |
| 13 | --- | 20-9663-1 | Start Button |
| 14 | --- | 20-6502-A | Plumb Bob |
| 15 | 5647-12693-19 | A-12688L | Freeway Bot. |
| 16 | 5647-12693-19 | A-12688L | Freeway Top |
| 17 | 5647-12693-19 | A-12688R | Freeway Bot. |
| 18 | 5647-12693-19 | A-12688R | Freeway Top |
| 21 | --- | 20-1066 | Slam Tilt |
| 22 | --- | A-8630 | Coin Door Close |
| 23 | --- | (optional) | Tckt. Dispenser |
| 24 | --- | A-8630 | Always Closed |
| 25 | 5647-12693-19 | A-12688 | Left Outlane |
| 26 | 5647-12693-19 | A-12688 | L. Return Lane |
| 27 | 5467-12693-19 | A-12688 | R. Return Lane |
| 28 | 5647-12693-19 | A-12688 | R. Outlane |
| 31 | A-4834-H | A-8284-2 | L. Slingshot |
| 32 | A-4834-H | A-8284-2 | R. Slingshot |
| 33 | --- | A-15419 | Low Gear Shift |
| 34 | --- | A-15419 | High Gear Shift |
| 35 | | | Not Used |
| 36 | --- | A-14691-4 | Top Red |
| 37 | --- | A-14691-4 | Middle Red |
| 38 | --- | A-14691-4 | Bottom Red |
| 41 | --- | A-14691-6 | Top Yellow |
| 42 | --- | A-14691-6 | Middle Yellow |
| 43 | --- | A-14691-6 | Bottom Yellow |
| 44 | --- | A-14691-5 | R. Bank Bot. |
| 45 | --- | A-14691-5 | R. Bank Mid. |
| 46 | --- | A-14691-5 | R. Bank Top |
| 47 | | | Not Used |
| 48 | | | Not Used |
| 51 | --- | A-14691-2 | Top Green |
| 52 | --- | A-14691-2 | Middle Green |
| 53 | --- | A-14691-2 | Bottom Green |
| 54 | 5647-12001-00 | B-12576 | Ramp Down |
| 55 | 5647-12133-12 | A-10417 | Outhole |
| 56 | 5647-09557-00 | A-8925 | Left Trough |
| 57 | 5647-09557-00 | A-8925 | Center Trough |
| 58 | 5647-12693-08 | A-11680 | Right Trough |
| 61 | --- | B-12030-2 | Top Jet |
| 62 | --- | B-12030-2 | Left Jet |
| 63 | --- | B-12030-2 | Bottom Jet |
| 64 | | | Not Used |
| 65 | 5647-12693-21 | A-15103 | Made U/D Ramp |
| 66 | | | Not Used |
| 67 | 5647-12693-21 | A-15102 | Made L. Ramp |
| 68 | | | Not Used |
| 71 | 5647-12693-19 | A-12688 | Top Loop |
| 72 | 5647-12693-19 | A-12688 | Middle Loop |
| 73 | 5647-12693-19 | A-12688 | Bottom Loop |
| 74 | 5647-12693-21 | A-15103 | Top Lock |
| 75 | 5647-12693-21 | A-15103 | Middle Lock |
| 76 | 5447-12693-21 | A-15103 | Bottom Lock |
| 77 | --- | A-9381-R | Eject Hole |
| 78 | 5647-12693-19 | A-12688 | Shooter |
| 81 | A-14316 (Trans) | A-14315 (LED) | Opto 1 |
| 82 | A-14316 (Trans) | A-14315 (LED) | Opto 2 |
| 83 | A-14316 (Trans) | A-14315 (LED) | Opto 3 |
| 84 | A-14316 (Trans) | A-14315 (LED) | Opto Made Loop |
| 85 | A-14316 (Trans) | A-14315 (LED) | Enter Left Ramp |
| 86 | --- | A-14691-5 | Left Bank Bottom |
| 87 | --- | A-14691-5 | Left Bank Middle |
| 88 | --- | A-14691-5 | Left Bank Top |

Footnotes printed at the bottom of the page:
`** A-15058  Single Flipper Cabinet Switch`
`*A-15060  Double Flipper Cabinet Switch`

Item numbers 11/12 on this diagram are cabinet-button callouts, not switch-matrix addresses (matrix
11/12 are themselves printed "Not Used" on the Switch Matrix page, 3-4) — item 11 is the double
cabinet switch assembly that gangs both the lower-right and upper-right flipper leaf switches to one
button paddle (footnote *, A-15060), and item 12 is the single cabinet switch assembly for the lower
left flipper only (footnote **, A-15058). No third flipper-button item is printed anywhere on this
page, and there is no upper-left flipper leaf switch entry at all — the only two Assy Nos. under item
11 are `A-15205-R` (upper right) and `A-15205-R-2` (lower right); no `A-15205-L` (upper left) row
exists to pair with the printed `A-15205-L-2` (lower left) under item 12.

Addresses 81-85 are the only five rows on this page carrying a paired opto LED/phototransistor part
(`A-14316`/`A-14315`); every other row prints either a plain mechanical switch part, a button/tilt
part, or "Not Used". Address 23 (Ticket Dispenser) is explicitly marked `(optional)` with no switch or
assembly part number at all — no LED/phototransistor pair is printed for it, despite the Switch Matrix
page's grid cell naming the same address "Ticket Opto." (see switch-matrix.md).
