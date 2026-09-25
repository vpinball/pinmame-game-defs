# Tales of the Arabian Nights — Power Driver Board G.I. connectors

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, read from the pages rendered
at their native 300 dpi. The committed crop is the J105/J106 block of PDF page 156 (printed 3-26),
the load-bearing region; the other quoted lines are disclosed below with their own page numbers.

## Power Driver Board Assembly A-20028 connector list (PDF page 156, printed 3-26)

Complete J104, J105 and J106 blocks, in printed order and spelling (including the printed "inset
panel" typo on J105-11):

| Pin | Printed text |
| --- | --- |
| J104-1 | Violet, return, G.I. to Coin Door Board J2-3 |
| J104-2 | Key |
| J104-3 | White-Violet, 6.8Vac, G.I. to Coin Door BrdJ2-5 |
| J105-1 | N/C |
| J105-2 | N/C |
| J105-3 | N/C |
| J105-4 | Key |
| J105-5 | Green, return, G.I. to insert panel |
| J105-6 | Violet, return, G.I. to insert panel |
| J105-7 | N/C |
| J105-8 | N/C |
| J105-9 | N/C |
| J105-10 | White-Green, 6.8Vac, G.I. to insert panel |
| J105-11 | White-Violet, 6.8Vac, G.I. to inset panel |
| J106-1 | Brown, return, G.I. to playfield |
| J106-2 | Orange, return, G.I. to playfield |
| J106-3 | Yellow, return, G.I. to playfield |
| J106-4 | Key |
| J106-5 | N/C |
| J106-6 | N/C |
| J106-7 | White-Brown, 6.8Vac, G.I. to playfield |
| J106-8 | White-Orange, 6.8Vac, G.I. to playfield |
| J106-9 | White-Yellow, 6.8Vac, G.I. to playfield |
| J106-10 | N/C |
| J106-11 | N/C |

The J104 lines sit in the left column of the same page, outside the committed crop.

## Coin Door Interface Board A-20580 (PDF page 152, printed 3-22)

- `J2-3 White-Violet, G.I. 6.8vac from Power Driver J104-1`
- `J2-5 Violet, G.I. from Power Driver Board J104-3`
- `J5-1 Violet, G.I. return to coin door`
- `J5-2 White-Violet, G.I. 6.8vac to coin door`

(The two pages swap the wire colours on J104-1 and J104-3: the power-driver page prints J104-1 Violet
and J104-3 White-Violet, the coin-door page the reverse. Both agree that the White-Violet / Violet
pair of string 05 is carried through the coin-door board to the coin door.)

## General Illumination Circuit (PDF page 140, printed 3-10)

Printed under the two circuit figures: "There are five general illumination strings; three like
figure #1 and two like figure #2." Figure #1 is the triac (SC141) string switched by the LS374 latch;
figure #2 is the always-on string fed through P600D diodes with no switching element. The block
diagram's lamp box reads "Playfield or Backbox G.I. Lights. Up to 18 bulbs per string."

## Reading

Pin by pin, transistor-row order and wire colour, `J106-1..3`/`J106-7..9` are printed strings 01-03
(Q5/Q4/Q3, Wht-Brn/Wht-Org/Wht-Yel) and go to the playfield; `J105-5/6`/`J105-10/11` are strings
04-05 (Q2/Q1, Wht-Grn/Wht-Vio) and go to the insert panel; `J104` carries string 05 on to the coin
door. This is the evidence that the General Illumination rows of printed page 2-40
(`general-illumination.md`) list their connectors under the wrong location columns.
