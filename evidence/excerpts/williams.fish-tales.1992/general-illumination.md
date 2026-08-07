# Fish Tales — General Illumination (locations and wiring)

Combines the General Illumination sections of two printed pages: the Solenoid/Flasher Locations
parts list (PDF page 92, printed 2-44) and the Solenoid Table wiring page (PDF page 102, printed
3-8, with an identical unnumbered duplicate at PDF page 2). Read from the rendered pages, not the
OCR text layer.

## Locations (printed 2-44)

| Item | Bulb | Assy | Description |
| --- | --- | --- | --- |
| 01 | 24-8768 | — | *Backbox G.I. #555 |
| 02 | 24-8768 | — | *Backbox & Hood G.I. #555 |
| 03 | 24-6549 | — | *Playfield G.I. #44 |
| 04 | 24-8768 | — | *Backbox G.I. #555 |
| 05 | 24-6549 | — | *Playfield & Coin Door G.I. #44 |

`*` = "Not Shown" on the printed playfield map. None of the five rows has an assembly number; all
are described purely as bulb runs.

## Wiring (printed 3-8)

| Addr | Function | Wire | Connections (Playfield-Insert-Cabinet-Hood) | Driver | Bulb |
| --- | --- | --- | --- | --- | --- |
| 01 | Backbox G.I. | Wht-Brn | J121-7 | Q18 | #555 |
| 02 | Backbox G.I. / Hood | Wht-Org | J121-8, J120-8 | Q10 | #555 |
| 03 | Playfield G.I. | Wht-Yel | J120-9 | Q14 | #44 |
| 04 | Backbox G.I. | Wht-Grn | J121-10 | Q16 | #555 |
| 05 | Playfield G.I. / Coin Door | Wht-Vio | J120-11, J119-1 | Q12 | #44 |

Both pages agree exactly on the zone breakdown for all five addresses. Of the five GI strings, only
two (03 and 05) reach the playfield at all:

* **03 "Playfield G.I."** is playfield-only (#44 bulbs, single connector J120-9).
* **05 "Playfield & Coin Door G.I."** reaches both the playfield and the coin door (#44 bulbs, two
  connectors J120-11 and J119-1) — the only GI string with a coin-door/cabinet leg.
* **01 "Backbox G.I."** and **04 "Backbox G.I."** are backbox-only (#555 bulbs, single connectors).
* **02 "Backbox G.I. / Hood"** reaches both the backbox and the hood (#555 bulbs, two connectors
  J121-8 and J120-8) but never the playfield.

No GI string is marked with any brightness/dimming footnote or asterisk beyond the blanket "Not
Shown" mark that applies to all five rows equally on the Locations page — unlike some other WPC
manuals in this project, this page carries no "these strings do not dim" style footnote at all.

## Printed 3-9 — Solenoid Wiring block diagram cross-check

The block/schematic diagram on PDF page 103 (printed 3-9) traces the same five GI connector pins
(within the Power Driver Board's J119/J120/J121 connector group) with no additional GI addresses and
no contradiction of the zone breakdown above.
