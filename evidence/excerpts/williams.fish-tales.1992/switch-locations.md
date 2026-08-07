# Fish Tales — Switch Locations

Transcribed from `Fish_Tales_OPS.pdf`, PDF page 91, printed page 2-43, the `Switch Locations` table.
Read from the rendered page and cross-checked against a 400 dpi crop where legibility mattered; the
manual carries an OCR text layer (Adobe Acrobat Paper Capture) but it was used only to help locate
this page, never to settle a cell value. `*` marks "The Score slingshot switches have diodes across
them." `†` marks "Not Shown" on the printed playfield map.

## Fliptronic column

| Item | Switch No. | Switch Assy No. | Description |
| --- | --- | --- | --- |
| F1 | SW-1A-193 | A-15205-R-2 | †Rt. Flipper EOS |
| F2 | SW-1A-191 | A-15058 | Rt. Flipper Cabinet |
| F3 | SW-1A-193 | A-15205-L-2 | Lt. Flipper EOS |
| F4 | SW-1A-191 | A-15058 | †Lt. Flipper Cabinet |

There is no F5, F6, F7, or F8 row anywhere on this page — not even a "NOT USED" placeholder row.
The table has exactly four Fliptronic rows in total. See `boards-and-assemblies.md` for the generic
Fliptronic II board circuit diagrams, which do print wiring for a full complement of four flippers
regardless of fitment, and for the game-specific parts pages that corroborate this table's silence
on upper-flipper positions.

## Matrix switches

| Item | Switch No. | Switch Assy No. | Description |
| --- | --- | --- | --- |
| 13 | ----- | 20-9663-1 | Start Button |
| 14 | ----- | 20-6502-A | Plumb Bob Tilt |
| 15 | 5647-12133-12 | A-10417 | Outhole |
| 16 | 5647-12693-08 | A-11680 | Trough 1 |
| 17 | 5647-09957-00 | B-8925 | Trough 2 |
| 18 | 5647-09957-00 | B-8925 | Trough 3 |
| 21 | SW-1A-117 | A-15487 | Slam Tilt |
| 22 | ----- | A-8630 | Coin Door Closed |
| 23 | *(blank)* | Not Used | Ticket Opto |
| 24 | ----- | A-8630 | †Always Closed |
| 25 | 5647-12693-19 | A-12688 | Left Outlane |
| 26 | 5647-12693-19 | A-12688 | Left Return Lane |
| 27 | ----- | A-15741 | Left Standup Tgt 1 |
| 28 | ----- | A-15741 | Left Standup Tgt 2 |
| 31 | 20-9713-07 | A-15130 | Cast |
| 32 | 5647-12693-21 | A-15055 | Left Boat Exit |
| 33 | 5647-12693-21 | A-15055 | Right Boat Exit |
| 34 | 5647-12133-00 | A-12010 | Spinner |
| 35 | 5647-12693-17 | A-15404 | Reel Entry |
| 36 | 5647-12693-12 | A-14947 | Catapult |
| 37 | A-14315 (LED) / A-14316 (Trans) | ----- | Reel 1 |
| 38 | A-14315 (LED) / A-14316 (Trans) | ----- | Reel 2 |
| 41 | A-14691-5 | ----- | Captive Ball |
| 42 | 5647-12693-18 | A-12687 | Right Boat Entry |
| 43 | 5647-12693-19 | A-12688-1 | Left Boat Entry |
| 44 | 5647-12693-19 | A-12688-1 | Letter (L)IE |
| 45 | 5647-12693-19 | A-12688 | Letter L(I)E |
| 46 | 5647-12693-19 | A-12688 | Letter Ll(E) |
| 47 | SW-1A-167-1 | A-11658-1 | Ball Popper |
| 48 | 5647-12693-31 | A-15211 | Drop Target |
| 51 | SW-11A-37 | B-12029-2 | Left Jet Bumper |
| 52 | SW-11A-37 | B-12029-2 | Center Jet Bumper |
| 53 | SW-11A-37 | B-12029-2 | Right Jet Bumper |
| 54 | ----- | A-15741 | Right Standup Tgt 1 |
| 55 | ----- | A-15741 | Right Standup Tgt 2 |
| 56 | 5647-12693-19 | A-12688 | Ball Shooter |
| 57 | SW-1A-114 (Kick) / SW-1A-120-1 (Score)* | A-8284-2 | Left Slingshot |
| 58 | SW-1A-114 (Kick) / SW-1A-120-1 (Score)* | A-8284-2 | Right Slingshot |
| 61 | ----- | A-15658-6 | Extra Ball |
| 62 | 5647-12693-18 | A-12687 | Top Right Loop |
| 63 | 5647-12133-11 | A-0381-R | Top Eject Hole |
| 64 | 5647-12693-19 | A-12688 | Top Left Loop |
| 65 | 5647-12693-19 | A-12688 | Right Return |
| 66 | 5647-12693-19 | A-12688 | Right Outlane |

No rows are printed for 11, 12, 67, 68, or 71-88, matching the Switch Matrix legend
(`switch-matrix.md`), which labels all of these "Not Used."

## Opto sweep result

Only two addresses carry any opto-construction marking on this page: 37 and 38 (Reel 1/Reel 2),
via the `(LED)`/`(Trans)` notation in the Switch No. column in place of a normal part number. No
other row in either the Fliptronic block or the matrix block carries a comparable marking. This is
corroborated by the Fish Reel Unit Assembly parts page (`A-14945`, see `boards-and-assemblies.md`),
which lists exactly two "Opto Photo/Trans Assy." (`A-14316`) and two "Opto LED Assembly" (`A-14315`)
items — one opto pair per switch address. Switches 47 (Ball Popper, `SW-1A-167-1`) and 48
(Drop Target, `5647-12693-31`) — the two addresses pinned PinMAME's inverted-switch mask actually
normalizes — carry no opto marking at all here; 48's part number cross-checks exactly against the
1-Bank Drop Target Assembly's own Mini Micro Switch item.

## The 23 / 24 naming point

Item 23's Switch No. cell is blank and its Switch Assy No. cell literally reads "Not Used", with
description "Ticket Opto" — this manual documents address 23 as an unfitted, vestigial position.
Item 24 has a real assembly number (`A-8630`, the same generic normally-closed part also used for
item 22 "Coin Door Closed") and description "Always Closed" — a populated, described switch. This
bears directly on whether address 24 should be treated as the driver's `swNotUsed` scaffolding
symbol or as real fitted hardware; reported here as printed, not resolved.
