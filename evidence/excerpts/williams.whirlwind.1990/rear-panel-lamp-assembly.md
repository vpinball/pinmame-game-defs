# Whirlwind — D-13356 rear-panel lamp assembly

Source: Williams **Red Parts Catalog 16-9190-B**, printed page **5-37**,
“Unique Assemblies - cont'd / WHIRLWIND (574) / Back Panel Lamp Assembly
D-13356”. The publisher's retained page is
<https://www.planetarypinball.com/reference/partsmanuals/WMS_Parts_Red_16-9190-B/files/assets/mobile/page0473_i2.jpg>.
Acquired 2026-11-06T23:48:17.811073Z, 89,720 bytes, 1050×1358 pixels,
SHA-256 `9b6351d58ed5405a776d9f585ea1c5852cde6aa1b9ee4b08d5ada840836b8338`.
Williams Electronics Games, Inc.; rights/license NOASSERTION.

Method: manual transcription and visual inspection by repository curator. Read the
native raster, rotated 270 degrees counter-clockwise, rather than its poor
SEO text layer. Punctuation and spacing are normalized; values, designators
and parenthesized quantities below preserve the printed cells.

## Complete printed parts table

| Item | Part Number | Part Design. | Description |
|---|---|---|---|
| 1 | 5768-12583-00 | blank | GI & Flash Lamp PCB |
| 2 | 24-8768 | L6 thru L10 | Twist Socket (4) |
| 3 | 24-8768 | L6 thru L10 | #555 Bulb 6.3V .25A (4) |
| 4 | 24-8803 | L1 thru L5 | Lamp Socket (5) |
| 5 | 24-8802 | L1 thru L5 | #906 Bulb 13V .69A (5) |
| 6 | 5791-10871-03 | J2 | 3H SPL Sq. Pin .156 |
| 7 | 5791-10871-06 | J1 | 6H SPL Sq. Pin .156 |

The table prints **24-8768** for both the twist socket and bulb; that is a
literal reading, not a correction of the operations manual's socket part
24-8767. It also prints **(4)** twice for the inclusive range **L6 thru L10**.

## Drawing and physical inventory

The complete front elevation draws **five large sockets, LMP1–LMP5**, in
one row and **five smaller sockets, LMP6–LMP10**, in the other. Its side
elevation distinguishes the two bulb sizes and the two headers. These are
physical socket symbols, not callout balloons. The table identifies their
bulbs as #906 and #555 respectively. The diagram therefore contains ten
positions, despite the table's two parenthesized `(4)` quantities. The
catalog's printed 1-11 index calls D-13356 a “9-Lamp PCB Assembly”; that
index total repeats the parts-table arithmetic and disagrees with the
drawn ten sockets.

Independent physical corroboration is Andrew Burch's original-board repair
photo in [Whirlwind Repair & Service Log #1](https://www.enteryourinitials.com/2017/03/07/whirlwind-repair-service-log-1/),
<http://www.enteryourinitials.com/images/whirlwind/whirlwind_rear_storm_lamp_board_dirty.jpg>.
Reacquired by public HTTP GET at 2026-11-07T00:01:46.584758Z, 54,552 bytes,
SHA-256 `e6892411527eb8a56c0b8b747ccb00113bf80eb4ee9ee44146ca20f64fd895ea`,
independently matching the earlier retained original. Its native 600×450
image shows the following socket labels and bulb sizes.
The board is rotated relative to the catalog; **the partial globe at the
left edge is LMP10, a GI bulb**, rather than an extra #906 flasher.

| Photo centre, native pixels | Silkscreen / physical observation |
|---|---|
| (10,267), partly clipped globe | LMP10, small GI |
| (122,277) | LMP5, large #906 |
| (147,218) | LMP9, small GI |
| (307,200) | LMP4, large #906 |
| (353,144) | LMP8, empty GI socket position |
| (445,141) | LMP3, large #906 |
| (494,83) | LMP7, small GI |
| (535,104) | LMP2, large #906 |
| (580,85) | LMP1, large #906 |
| (575,55) | LMP6, small GI |

The repairer explicitly replaces the missing GI twist socket. The complete
LMP1–LMP10 pattern in this photograph corroborates the factory elevation:
**five #906 flasher positions and five #555 GI positions**. A different
owner's KLOV prose says six #555 plus five flashers; the drawing and actual
silkscreened socket pattern govern the physical inventory instead.

The operations manual's solenoid table separately prints three bulbs for
left lightning, one for middle thunder and two for right thunder. Its sum
of six disagrees with this board. The independently retained December 1989
operator's handbook 16-574-103, PDF 8/printed 8, explicitly prints **two** for
left lightning, **one** for middle thunder and **two** for right thunder.
Its complete literal table is in `handbook-solenoids.md`. That second
factory count agrees with the full elevation and actual socket pattern,
resolving the operations table's three-left-bulb entry as an erratum.
The five positions serve the left, middle and right groups in that order.
The separately reviewed `rear-panel-placement.md` records the subsequent
PCB-to-panel registration and the accepted, explicitly limited projections.

## Portable drawing derivation

The original JPEG is retained unchanged under the run's `primary-red-parts`
folder. PyMuPDF 1.28.2 `convert_to_pdf` wrapped its existing JPEG stream as
one PDF page without resampling; wrapper SHA-256
`ebd2a2eef166271ae8f5e3614fccd06d836a48bbb1f48fbf6970532df61e254e`.
The official `tools/render_excerpt_image.py` then produced the tight
front/side elevation crop, excluding the printed parts table:

`page0473_i2-wrapper.pdf page 1, crop box 0.219,0.075,0.486,0.858, scanned page rendered at its native resolution (embedded image xref 3, 1050px across 10.94in), rendered at 96 dpi, grayscale, rotated 270 degrees counter-clockwise, 1065x282 WebP quality 65`

The crop was reopened and checked against the unchanged native JPEG.
