# Star Trek: The Next Generation — Lamps Locations drawing and measurement record

Read from `Star_Trek_TNG_OPS.pdf`, PDF page 93, printed page 2-41 ("LAMPS LOCATIONS"), the playfield
drawing to the right of the parts list. The page is one 2574x3622 1-bit scan embedded at 308 dpi; every
pixel coordinate below is on the full page rendered with `pdftoppm -r 308 -gray` (2574x3622 px). The
committed crop is the box 0.44,0.11,0.935,0.73 of that page, so crop pixel = page pixel - (1133, 398).

## What the drawing prints (read from the rendered page)

- Two callouts numbered `78`. One sits on the rear rail above the top lanes 31/32/33; its leader ends on
  the middle, narrower bulb of a three-bulb board (two larger outer bulbs, one narrow centre bulb). The
  other sits left of the Borg kicker bracket, beside inserts 74/64; its leader ends on the middle socket of
  a board that also carries one elongated bulb above and one below it.
- An inset outside the left playfield edge, drawn in elevation: a two-socket bracket with `53` on the upper
  socket and `26` on the lower one, and a second two-socket bracket with `85` on the upper socket and `86`
  on the lower one. A horizontal leader runs from each bracket into the playfield and ends on a small
  hatched square.
- `26` is also printed on the playfield insert in the centre of the ship-mode ring, so lamp 26 has two
  printed positions: that insert and the lower socket of the 53/26 bracket.
- The ring of seven ship-mode inserts is labelled 13 (left), 14 (lower left), 21, 22, 23 (top), `26`
  (right) and 18 (lower right). The right-hand `26` is a misprint: the parts list on the same page prints
  27 "Ship Mode 6" and no second 26 on the ring, and the retained table places lamp 27 there. The 13 and
  14 leaders end on the two inserts the retained table gives to l14 and l13 respectively; that disagreement
  is recorded as `conflict.ship-mode-1-2-insert-positions`.
- At the Borg kicker arch: a round flash bulb at the top of the arch, and a round symbol on the lower
  centre plate. Printed 2-45's two item-28 (Center Borg Flasher) leaders end on these two; printed 2-25
  shows the upper one as item 16's single vertical flash bulb and draws the Borg kicker coil end-on at the
  lower one's spot (DETAIL 1, wired BRN-GRY and VIO-ORG).

## Frame: page pixels to normalized playfield

An affine map `[x, y] = [px, py, 1] @ A` was fitted by least squares from the printed centre of 16 round
hatched inserts to the retained VPW Mod v1.0 table's `Light` object of the same lamp number, divided by the
table's own bounds (1093 x 2162):

| Lamp | Page px | Residual (x, y) |
| --- | --- | --- |
| 31 | 2007.5, 593.1 | 0.0017, 0.0022 |
| 32 | 2080.0, 568.0 | -0.0100, 0.0017 |
| 33 | 2186.3, 549.4 | 0.0093, 0.0036 |
| 83 | 2143.8, 871.3 | 0.0000, -0.0044 |
| 21 | 1730.0, 1676.7 | 0.0002, -0.0027 |
| 22 | 1838.3, 1650.0 | -0.0008, -0.0009 |
| 26 (centre insert) | 1840.0, 1783.3 | 0.0009, -0.0023 |
| 23 | 1946.0, 1679.0 | -0.0024, -0.0033 |
| 27 (printed `26`) | 2008.0, 1787.0 | 0.0012, -0.0021 |
| 18 | 1946.0, 1885.0 | -0.0022, -0.0036 |
| 37 | 1891.7, 2123.3 | -0.0015, 0.0002 |
| 38 | 1943.3, 2164.2 | -0.0034, 0.0041 |
| 34 | 1736.7, 2158.3 | 0.0041, 0.0032 |
| 35 | 1784.2, 2120.8 | -0.0007, 0.0003 |
| 36 | 1840.0, 2093.3 | 0.0009, 0.0015 |
| 17 | 1842.0, 2340.0 | 0.0027, 0.0025 |

`A = [[0.000960944, -0.000005200], [-0.000001677, 0.000462176], [-1.262913, -0.195541]]`, RMS residual
0.0047, largest single residual 0.010. Measured points are therefore rounded to three decimals.

## Measured points

| Point | What it is | Page px | Normalized |
| --- | --- | --- | --- |
| Lamp 78, right board | device symbol: centre bulb of the three-bulb board (top 78 leader) | 2131.5, 555.6 | 0.784, 0.050 |
| Lamp 78, left board | device symbol: middle socket of the left board (second 78 leader) | 1738.9, 719.8 | 0.407, 0.128 |
| Right board, left outer bulb | device symbol | 2100.6, 549.4 | 0.755, 0.047 |
| Right board, right outer bulb | device symbol | 2157.5, 549.4 | 0.809, 0.047 |
| Left board, upper bulb | device symbol | 1696.0, 658.1 | 0.366, 0.100 |
| Left board, lower bulb | device symbol | 1696.0, 780.5 | 0.366, 0.156 |
| 53/26 bracket leader | hatched square at the leader end | 1622.0, 826.0 | 0.294, 0.178 |
| 85/86 bracket leader | hatched square at the leader end | 1458.0, 1026.0 | 0.136, 0.271 |
| Borg arch, top flash bulb (flasher 28, upper) | device symbol | 1873.3, 559.5 | 0.536, 0.053 |
| Borg lower centre plate, round symbol (flasher 28, lower leader) | symbol printed 2-25 identifies as the kicker coil | 1870.0, 740.8 | 0.533, 0.137 |
| Ring insert under the printed 13 leader | device symbol (table: l14) | 1673.7, 1788.3 | 0.342, 0.622 |
| Ring insert under the printed 14 leader | device symbol (table: l13) | 1732.7, 1891.0 | 0.399, 0.669 |

### Left-side check

All 16 fit points lie between x 0.40 and 0.84. Nine left-side lamps that are not fit inputs check the
extrapolation; their printed insert centres were estimated visually, so they are good to a few pixels:

| Lamp | Page px | Residual (x, y) |
| --- | --- | --- |
| 11 | 1572.7, 1672.3 | -0.0021, -0.0003 |
| 12 | 1572.7, 1721.3 | 0.0008, -0.0003 |
| 15 | 1572.3, 1770.3 | -0.0010, -0.0005 |
| 51 | 1547.3, 2102.0 | 0.0126, 0.0078 |
| 61 | 1534.0, 1344.0 | 0.0161, -0.0011 |
| 62 | 1573.0, 1457.0 | 0.0145, -0.0045 |
| 63 | 1608.3, 1573.0 | 0.0106, -0.0027 |
| 67 | 1671.7, 1396.0 | 0.0020, -0.0045 |
| 68 | 1630.3, 1417.0 | 0.0078, -0.0034 |

The worst, 0.016 at lamp 61, is at the left rear; left-side points carry that much more uncertainty than the
fit points.

### Other pages drawn from the same artwork

Printed 2-37 (PDF 89) and 2-45 (PDF 97) reuse this drawing at the same scale. On each render the outer
playfield-frame lines were located as the darkest pixel column or row of the line (column darkness summed
over rows 400-2700, row darkness summed over the playfield width):

| Page | Left | Right | Top (outer) | Top (inner) |
| --- | --- | --- | --- | --- |
| printed 2-41 (PDF 93) | 1334.0 | 2347.5 | 449.0 | 470.0 |
| printed 2-45 (PDF 97) | 1329.0 | 2342.0 | 536.0 | 558.0 |
| printed 2-37 (PDF 89) | 813.5 | 1827.0 | 666.5 | 689.0 |

The page offset is the mean shift of the left and right lines (x) and of the two top lines (y): printed
2-45 sits at (-5.25, +87.5) px and printed 2-37 at (-520.5, +218.25) px from this page. A point read there
has its offset subtracted before the map above is applied.

Transcribed by the curator from the rendered page; the fit and every normalized value are reproduced by
`review-artifacts/star-trek-the-next-generation-1993/2026-09-25-spatial-measure.py` in the working root.
