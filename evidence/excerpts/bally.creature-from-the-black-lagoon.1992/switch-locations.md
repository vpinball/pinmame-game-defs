# Creature from the Black Lagoon — Switch Locations parts list

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 101, printed page 2-41,
"SWITCH LOCATIONS". Read directly from a 300 dpi `pdftoppm` render; the retained scan carries a real
(Adobe Paper Capture) OCR text layer, but it garbles this table (e.g. "P-A-1-D", "SW-1A-1 14"), so the
rendered image is the source of record for every value below, not `pdftotext`.

| Item | Switch/Assembly No. | Where Used |
| --- | --- | --- |
| F1 | SW-1A-193 | *Right Flipper EOS |
| F2 | A-15894 | *Right Flipper Opto Board |
| F3 | SW-1A-193 | *Left Flipper EOS |
| F4 | A-15894 | *Left Flipper Opto Board |
| 11-12 | --- | Not Used |
| 13 | 20-9663-1 | Credit/Start Button |
| 14 | 20-6502-A | *Plumb Bob Tilt |
| 15 | 5647-12693-19 | Top Left Rollover |
| 16 | 5647-12693-21 | †Left Subway |
| 17 | 5647-12693-21 | †Center Subway |
| 18 | 5647-12693-36 | Center Shot |
| 21 | 27-1066 | *Slam Tilt |
| 22 | 5643-09288-00 | *Coin Door |
| 23-24 | --- | Not Used |
| 25 | 5647-12693-19 | P of P-A-I-D |
| 26 | 5647-12693-19 | A of P-A-I-D |
| 27 | 5647-12693-19 | I of P-A-I-D |
| 28 | 5647-12693-19 | D of P-A-I-D |
| 31-32 | --- | Not Used |
| 33 | SW-11A-37 | Bottom Jet |
| 34 | A-14231 (LED) / A-14232 (Trans.) | Right Popper |
| 35 | 5647-12693-26 | Right Ramp Enter |
| 36 | 5647-12693-21 | Left Ramp Enter |
| 37 | A-14231 (LED) / A-14232 (Trans.) | Lower Right Popper |
| 38 | 5647-12693-11 | †Ramp Up/Down |
| 41 | A-16206-2 | Cola |
| 42 | A-16206-2 | Hot Dog |
| 43 | A-16206-2 | Popcorn |
| 44 | A-16206-2 | Ice Cream |
| 45 | SW-11A-37 | Left Jet |
| 46 | SW-11A-37 | Right Jet |
| 47 | SW-1A-114 | Left Slingshot |
| 48 | SW-1A-114 | Right Slingshot |
| 51 | 5647-12693-19 | Left Out Lane |
| 52 | 5647-12693-19 | Left Return Lane |
| 53 | 5647-12693-19 | Start Combo |
| 54 | 5647-12693-19 | Right Out Lane |
| 55 | 5647-12133-12 | Outhole |
| 56 | 5647-12693-08 | Right Trough |
| 57 | 5647-09957-00 | Center Trough |
| 58 | 5647-09957-00 | Left Trough |
| 61 | 5647-12693-36 | Right Ramp Exit |
| 62 | 5647-12693-21 | Left Ramp Exit (lower) |
| 63 | 5647-12693-19 | Center Lane Exit |
| 64 | 5647-12693-21 | Upper Ramp |
| 65 | 5647-12693-21 | Bowl |
| 66 | 5647-12693-04 | Shooter |
| 67-88 | --- | Not Used |

Footnotes printed on the page: `* Not shown.` and `† Located on underside of playfield.`

Only two addresses in this list carry the two-row "assembly / opto-assembly" LED-plus-phototransistor
disclosure that the rest of this evidence set relies on for opto identity: **34** (`A-14231 (LED)` over
`A-14232 (Trans.)`, Right Popper) and **37** (same pair, Lower Right Popper). Every other populated
address prints a single ordinary switch part (`5647-12693-xx`, `SW-1A-xxx`, `SW-11A-37`, `20-`, `27-`,
`5643-`, or `A-16206-2`), including the two addresses PinMAME's inverted-switch mask also normalizes
(15 Top Left Rollover, 38 Ramp Up/Down) — neither prints an LED/Trans pair or any other opto-construction
marker, so their normally-closed polarity is recorded from the retained script's own inverted hit/unhit
handling (switch 15) and from the ramp mechanism's own position-sensor logic (switch 38), not from this
parts list. F1-F4 are the only Fliptronic flipper-block positions printed on this page; F5-F8 do not
appear at all (not even as a "Not Used" row), which is the basis of
`conflict.upper-flipper-switches-unconfirmed-fitment` recorded against the Switch Matrix wiring page
below.
