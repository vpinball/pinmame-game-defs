# Cactus Canyon — Saloon flasher (26) location

Measured on `Cactus_Canyon_Manual.pdf`, PDF page 95, printed page 2-37: the playfield drawing that
carries the numbered solenoid/flasher callouts listed on printed page 2-36 (see
`solenoid-flasher-locations.md`). The committed crop covers the upper right of the playfield, from
the right ramp to the right side rail, with the callout balloons 27, 36/33, 26, 38/37 and 04 at its
right edge.

## What the drawing shows

Balloon **26** (SALOON FLASHER - PLAYFIELD on printed 2-36) sits at the right edge beside the
right ramp. Its leader runs left and ends at a small bracket just inside the right ramp's inner
wall, below the saloon building outline. The leader does not end on the saloon building itself.

## Measurement

- Full-page render: PDF page 95 at the scan's native 200 dpi, 1551 x 2143 pixels.
- Playfield frame on that render: x 375-1164, y 254-2019 (outer playfield outline). Under this
  frame, jet bumper 13's circle and the flasher domes at callouts 25 and 27 land on their own drawn
  circles.
- The leader of balloon 26 ends at pixel (1020, 610). In the committed crop, which starts at page
  pixel (698, 214), that is about (322, 396).
- Normalized: x = (1020 - 375) / 789 = 0.8175, y = (610 - 254) / 1765 = 0.2017 (x = 0 left,
  y = 0 rear).
- The retained table's decorative spotlight primitive `SpotP` is at (0.800694, 0.216224), about
  0.022 from that endpoint. The script-bound `F26` lights (`Light56`/`Light57`, about (0.76, 0.19))
  sit on the saloon building instead.

The measurement is at the drawing's precision (a leader endpoint on a 200 dpi scan), so it is used to
choose between retained-table objects, not as a coordinate of its own.
