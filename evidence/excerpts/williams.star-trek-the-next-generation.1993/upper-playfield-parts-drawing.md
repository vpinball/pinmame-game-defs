# Star Trek: The Next Generation — Upper Playfield Parts Locations (items 21-26b)

Read from `Star_Trek_TNG_OPS.pdf`, PDF pages 88-89, printed pages 2-36 (parts list) and 2-37 (drawing),
both titled "UPPER PLAYFIELD PARTS LOCATONS" (sic). Page 89 is one 2581x3627 1-bit scan at 308 dpi; pixel
coordinates are on the full page rendered with `pdftoppm -r 308 -gray`. The committed crop is the page-89
box 0.30,0.17,0.46,0.39, the rear-left corner around callouts 21 and 22, so crop pixel is about page pixel
- (774, 617).

## Parts list rows used (printed 2-36, as printed)

| Item | Part Number | Description |
| --- | --- | --- |
| 21 | A-17484 | Romulan Ship |
| 22 | A-17330 | 2-lamp PCB |
| 23 | A-14690-6 | Yellow Standup Target |
| 24 | 03-8994 | Klingon Ship |
| 24a) | 12-7150 | Klingon Ship Support Wire |
| 25 | A-16959 | Switch Gate Assembly |
| 26 | A-16811 | Plastic Ramp |
| 26a) | 01-11635 | Flap |
| 26b) | A-17272 | 2-lamp PCB |

Printed 2-41 gives A-17330 as lamp 53's assembly and A-17272 as lamp 85's.

## Drawing (printed 2-37)

Callout 22 sits against the left side of the left ramp, below callout 21 (Romulan Ship, rear left corner);
its leader ends on a small bracket left of the ramp at page px 960, 1000. This drawing is the printed 2-41
artwork at the same scale with its outer playfield-frame lines at (-520.5, +218.25) px from that page's;
subtracting the offset and applying the printed 2-41 frame fit (see `lamp-locations-drawing`) puts the
callout-22 target at normalized 0.158, 0.158, reading accuracy about 0.02 because the leader tip merges with
the bracket art. Callout 26 points at the plastic ramp itself, not at its 2-lamp PCB, so it fixes no lamp
position.

Transcribed by the curator from the rendered pages.
