# X-Men Limited Edition Magneto disc coil locations

Source: `XMenManual_042214-high-resolution.pdf`, PDF page 61, printed page 9. This excerpt is Limited Edition evidence and must not be used for the Pro playfield.

The factory drawing shows two Q19 `FLASH: DISC CLEAR` device symbols and two Q20 `FLASH: DISC BLUE` device symbols alternating around the Magneto disc. Q30 `MAGNETO SPOT LIGHT` is the numbered device symbol immediately left of the disc. The committed WebP is a tight native-resolution crop of those five symbols and the Q4 Magneto control point; no remote text balloon or leader endpoint was measured.

## Reproducible normalization

Render PDF page 61 at the embedded scan's native 302 dpi. The resulting page is 2531 by 3557 pixels. In that render, the factory playfield drawing frame is `left=128`, `top=427`, `right=1444`, `bottom=3382`. Device-symbol centers were read in the same full-page pixel coordinates:

| Output | Symbol | Pixel center | Normalized `(x, y)` |
| --- | --- | --- | --- |
| Q19 | clear, rear-left | `(698, 1457)` | `(0.433, 0.349)` |
| Q19 | clear, lower-right | `(991, 1775)` | `(0.656, 0.456)` |
| Q20 | blue, upper-right | `(1009, 1609)` | `(0.669, 0.400)` |
| Q20 | blue, lower-left | `(769, 1816)` | `(0.487, 0.470)` |
| Q30 | Magneto spotlight, left | `(616, 1683)` | `(0.371, 0.425)` |

Each coordinate uses `x = (pixel_x - 128) / (1444 - 128)` and `y = (pixel_y - 427) / (3382 - 427)`, then rounds to three decimals. The precision intentionally reflects the scanned drawing rather than implying exact VPX object geometry.

## Frame control

The Q4 Magneto symbol center measured from the same drawing is approximately `(804, 1597)`, or `(0.514, 0.396)` in the manual frame. The exact retained VPW table places the Magneto magnet effect at `(0.526786, 0.406147)`. The difference is about `0.013` in x and `0.010` in y, which confirms that the manual and VPX frames have the same orientation and scale while also quantifying the drafting/measurement tolerance. The Q19, Q20, and Q30 placements therefore preserve the factory layout and multiplicity but are not exact VPX emitter-object centers.
