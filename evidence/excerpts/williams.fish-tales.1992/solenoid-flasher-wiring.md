# Fish Tales — Solenoid Table (wiring)

Transcribed from `Fish_Tales_OPS.pdf`, PDF page 102, printed page 3-8, the `Solenoid Table`
(identical duplicate present, unnumbered, at PDF page 2 — see `manual-transcription.md`). Read from
the rendered page and independently cross-checked against a 400 dpi lossless crop for every cell,
not the OCR text layer.

Header: Sol. No. | Function | Solenoid Type | Wire Color | Connections (Playfield-Insert-Hood) |
Driver Trnstr | Solenoid Part Number/Flashlamp Type.

| Sol. | Function | Type | Wire | Connections | Driver | Part / Flashlamp |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Ball Shooter | High Power | Vio-Brn | J130-1 | Q82 | AE-23-800 |
| 02 | Catapult | High Power | Vio-Red | J130-2 | Q80 | AL-23-800 |
| 03 | Ball Popper | High Power | Vio-Org | J130-4 | Q78 | AE-24-900 |
| 04 | Left Sling | High Power | Vio-Yel | J130-5 | Q76 | AE-27-1200 |
| 05 | Right Sling | High Power | Vio-Grn | J130-6 | Q64 | AE-27-1200 |
| 06 | Left Gate | High Power | Vio-Blu | J130-7 | Q66 | A-14406 |
| 07 | Knocker | High Power | Vio-Blk | J130-8 | Q68 | AE-23-800 |
| 08 | Backbox Fish | High Power | Vio-Gry | J130-9 | Q70 | AE-23-800 |
| 09 | Outhole | Low Power | Brn-Blk | J127-1 | Q58 | AE-27-1200 |
| 10 | Ball Release | Low Power | Brn-Red | J127-3 | Q56 | AE-26-1200 |
| 11 | Eject Hole | Low Power | Brn-Org | J127-4 | Q54 | AE-26-1200 |
| 12 | Drop Target Up | Low Power | Brn-Yel | J127-5 | Q52 | AE-26-1200 |
| 13 | Drop Target Down | Low Power | Brn-Grn | J127-6 | Q50 | SM1-26-600 |
| 14 | Left Jet Bumper | Low Power | Brn-Blu | J127-7 | Q48 | AE-26-1200 |
| 15 | Center Jet Bumper | Low Power | Brn-Vio | J127-8 | Q46 | AE-26-1200 |
| 16 | Right Jet Bumper | Low Power | Brn-Gry | J127-9 | Q44 | AE-26-1200 |
| 17 | Jackpot Flasher | Flasher | Blk-Brn | J126-1 | Q42 | 1PL #906 |
| 18 | Super Jackpot Flasher | Flasher | Blk-Red | J126-2 | Q40 | 1PL #906 |
| 19 | Instant Multi-ball Flasher | Flasher | Blk-Org | J126-3, J125-3 | Q38 | 1PL #906 / 2 IB #906 |
| 20 | Light Extra Ball Flasher | Flasher | Blk-Yel | J126-4, J125-5 | Q36 | 1PL #906 / 2 IB #906 |
| 21 | Rock the Boat Flasher | Flasher | Blu-Grn | J126-5, J125-6 | Q28 | 1PL #906 / 2 IB #906 |
| 22 | Video Mode Flasher | Flasher | Blu-Blk | J126-6, J125-7 | Q30 | 1PL #906 / 2 IB #906 |
| 23 | Hold Bonus Flasher | Flasher | Blu-Vio | J126-7, J125-8 | Q34 | 1PL #906 / 1 IB #906 |
| 24 | Not Used | Flasher | Blu-Gry | — | Q32 | — |
| 25 | Reel Flasher | Flasher | Blu-Brn | J122-1, J124-1, J124-1 | Q26 | 1PL #89/1HD #906 / 2 IB #906 |
| 26 | Top Left Flasher | Flasher | Blu-Red | J122-2 | Q24 | 1PL #89/1PL #906 |
| 27 | Casters Club Flasher | Flasher | Blu-Org | J122-3, J124-3 | Q22 | 1PL #89 / 1 IB #906 |
| 28 | Reel Motor | Low Power | Blu-Yel | J122-4 | Q20 | 14-7967 |

**Two verified anomalies, transcribed exactly as printed and not corrected:**

* Row 25's Connections cell prints the token `J124-1` twice (`J122-1  J124-1  J124-1`). Verified
  against a 400 dpi lossless crop. This may correspond to the three separate bulb populations the
  Solenoid/Flasher Locations page lists for the same address (playfield #89, backbox insert #906,
  hood #906 — see `solenoid-flasher-locations.md`), or may be a source printing error; not resolved
  here.
* Row 05's driver transistor reads `Q64`, breaking the otherwise strictly-descending-by-2 pattern of
  the surrounding rows (`Q82, Q80, Q78, Q76, Q64, Q66, Q68, Q70` for rows 01-08). Verified against
  the same crop; transcribed as printed rather than corrected to a hypothetical `Q74`.

## General Illumination (same page)

| Addr | Function | Wire | Connections (Playfield-Insert-Cabinet-Hood) | Driver | Bulb |
| --- | --- | --- | --- | --- | --- |
| 01 | Backbox G.I. | Wht-Brn | J121-7 | Q18 | #555 |
| 02 | Backbox G.I. / Hood | Wht-Org | J121-8, J120-8 | Q10 | #555 |
| 03 | Playfield G.I. | Wht-Yel | J120-9 | Q14 | #44 |
| 04 | Backbox G.I. | Wht-Grn | J121-10 | Q16 | #555 |
| 05 | Playfield G.I. / Coin Door | Wht-Vio | J120-11, J119-1 | Q12 | #44 |

## Flipper Circuits (same page)

| Flipper circuit | Wire | Playfield connector | Pwr | Hold | Coil |
| --- | --- | --- | --- | --- | --- |
| Lower Right Flipper | Blu-Yel | J907-8, 9 | Q4 | Q11 | FL-11629 |
| Lower Left Flipper | Gry-Yel | J907-6, 7 | Q3 | Q9 | FL-11629 |

No row for an upper-right or upper-left flipper circuit is printed anywhere on this page — not even
a "NOT USED" placeholder, matching the complete absence of Fliptronic F5-F8 rows on the Switch
Locations page (`switch-locations.md`).

## Printed 3-9 — Solenoid Wiring (block diagram)

PDF page 103. A connector block/schematic diagram, not a row table, tracing Power Driver Board
connectors J119, J122, J124, J125, J126, J127, J130 out to their named coil/flasher boxes. It
confirms the same 28 solenoid addresses and the same GI connector pins as the Solenoid Table above,
with no additional addresses. One detail not visible in the row table: connector J119 pin 2 supplies
"Gray-Yellow +12V (playfield)" directly into the Reel(1)/Top Left(2)/Casters Club(1) flasher block
and separately into the Reel Motor block — i.e. solenoids 25, 26, 27, and 28 share one +12V supply
tap distinct from the +50V/+20V taps used by the rest of the page.
