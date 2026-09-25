# Star Trek: The Next Generation — Solenoid/Flasher Location drawing (flasher callouts)

Read from `Star_Trek_TNG_OPS.pdf`, PDF page 97, printed page 2-45 ("SOLENOID / FLASHER LOCATION"), the
playfield drawing to the right of the parts list (the parts list itself is the separate
`solenoid-flasher-locations` excerpt). The page is one 2567x3617 1-bit scan at 308 dpi; pixel coordinates
are on the full page rendered with `pdftoppm -r 308 -gray` (2568x3617 px). The committed crop is the box
0.49,0.10,0.935,0.72, so crop pixel = page pixel - (1258, 362).

The drawing is the printed 2-41 lamp drawing's artwork at the same scale: its outer playfield-frame lines
sit (-5.25, +87.5) px from that page's (the frame-line pixels are listed in `lamp-locations-drawing`), and
the normalized values below use the printed 2-41 frame fit.

## Flasher callouts (only the flasher items are transcribed)

| Printed item | Public solenoid | Callouts | Where the leader ends | Page px | Normalized |
| --- | --- | --- | --- | --- | --- |
| 20 Jets Flasher | 20 | 1 | beside the jet bumpers, right of bumper 12 | balloon only | not measured |
| 21 Right Popper Flasher | 21 | 1 | short leader from the balloon over the right wall rails to a holder symbol; the holder outline (x 2239-2263) is open at the top where it meets the rail art, so its centre is taken over its lowest 30 px, above its lower end at y 1769 | 2251.0, 1755.0 | 0.902, 0.563 |
| 22 Middle Ramp Flasher | 22 | 1 | forked tail: two prongs ending in the wire-ramp art at the rear, no bulb symbol under either | 1680.0, 645.0 / 1715.0, 646.0 | 0.356, 0.053 / 0.389, 0.054 |
| 23 Shield Flashers | 23 | 3 | left, centre and right shield lens | 1688.75, 1706.0 / 1838.75, 1687.5 / 1988.75, 1722.5 | 0.362, 0.544 / 0.506, 0.534 / 0.650, 0.550 |
| 25 Exit Under Gnd. Flashers | 25 | 1 | short leader to a closed holder symbol beside the left wall rails (white interior x 1415-1434, y 1731-1760) | 1424.0, 1745.0 | 0.108, 0.563 |
| 26 Right Borg Flashers | 26 | 1 | the three-bulb board at the rear right | board | see lamp drawing |
| 27 Left Borg Flashers | 27 | 2 | upper and lower elongated bulb of the left Borg board | board | see lamp drawing |
| 28 Center Borg Flashers | 28 | 2 | upper leader: the round flash bulb at the top of the Borg arch; lower leader: the round symbol on the lower centre plate, which printed 2-25 shows is the kicker coil, so this is a leader endpoint rather than a bulb (both measured on printed 2-41, see `lamp-locations-drawing`) | 1868.0, 647.0 / 1865.0, 828.0 | 0.536, 0.053 / 0.533, 0.137 |
| 41 Romulan Flashers | 55 | 1 | leftmost rear corner, left of the left ramp | 1435.4, 803.1 | 0.120, 0.128 |
| 42 Right Ramp Flashers | 56 | 1 | balloon above the rear right corner; its line runs up to the printed label "(On Back Panel)", not into the playfield | label | not measured (back panel) |

The list beside the drawing (printed on the same page) marks 29-36 "see Flipper Circuits" and the five
G.I. circuits and the flippers "* Not Shown". Item 22's forked tail is the style item 26 uses for its two
bulbs, but the solenoid/flasher table prints a single #89 playfield bulb for 22, so neither prong is taken
as its socket. Item 28's page px are the printed 2-41 symbols moved by this page's offset. Transcribed by the
curator from the rendered page; leader endpoints are accurate to a few pixels (about 0.005 normalized).
