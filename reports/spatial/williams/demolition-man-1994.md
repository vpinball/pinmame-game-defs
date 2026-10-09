# Demolition Man (Williams, 1994) spatial blockers

Retained VPX SHA-256 `099c70add2201ea3e49c34c9f910e365bd88218d8bf755846ceee93bce82fbd3`; script `0af7e1f50985d5a36d7b3f74ac1254a9d54594189c92934072a8951e7bf75e12`; 1027-file extraction manifest `a72529f25cbcc1be65bfc8d2113a502e6e7b4c5c532d5c786a025ca835028676`; manual `faa0c6f426dcac85fbc9f167e7d3a8b78ac3269b8b65530fb3111e1811f88981`.

Bounds: `left=0 top=0 right=1093 bottom=2162`. Every canonical coordinate is x/1093 and y/2162 rounded to at most six places.

## Placement status

- `validated`: 108 devices
- `observed`: 40 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 60
- used devices with no placement record: 7

  - `device.claw-flasher`
  - `device.elevator-1-flasher`
  - `device.elevator-2-flasher`
  - `gi.string-1`
  - `lamp.matrix-71`
  - `lamp.matrix-72`
  - `lamp.matrix-73`

## Projection classes

- **switch:** The centre of the VPX object the retained script binds to each matrix switch (trigger, kicker, standup or slingshot wall drag-point centroid, bumper). Sensors the table does not model are projected onto their mechanism's object: the trough optos onto BallRelease, the claw position optos onto the Claw arm's pivot, the elevator index onto ElevatorKicker.
- **lamp:** The centre of the insert Light each lamp's NFadeLm call drives (not its 'b' halo double). Lamps 11, 82 and 83 place both bulbs; lamp 83's inner pair comes from l83/l83a, which the table's fader wrongly drives from lamp 82.
- **solenoid:** The kicker, slingshot wall, bumper or flipper the script fires; for flashers the script-driven Light at the flasher. The diverter's power winding and the claw motor lines and magnet are projected onto the mechanism they move.
- **gi:** The Light members of the collection UpdateGI drives for strings 1-4, with render doubles closer than 0.006 normalized collapsed; observed only, without a quantity.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 111 of the 127 table placements it checks ([seed](../../../tools/seeds/williams/demolition-man-1994-callouts.json)); the rest keep their observed status:

- `device.ball-release.effect`: callout 1 on pdf-103, 0.142 normalized away.
- `device.bottom-popper.effect`: callout 2 on pdf-103, 0.077 normalized away.
- `device.center-ramp-flasher.emitter`: callout 40 on pdf-103, 0.085 normalized away.
- `device.diverter-hold.effect`: callout 15 on pdf-103, no callout of this label on the drawing.
- `device.lower-rebound-flasher.emitter`: callout 38 on pdf-103, 0.076 normalized away.
- `device.right-ramp-upper-flasher.emitter`: callout 44 on pdf-103, 0.113 normalized away.
- `lamp.matrix-13.emitter`: callout 13 on pdf-99, no callout of this label on the drawing.
- `lamp.matrix-61.emitter`: callout 61 on pdf-99, 0.087 normalized away.
- `lamp.matrix-62.emitter`: callout 62 on pdf-99, 0.075 normalized away.
- `switch.matrix-46.sensor`: callout 46 on pdf-101, 0.103 normalized away.
- `switch.matrix-53.sensor`: callout 53 on pdf-101, 0.200 normalized away.
- `switch.matrix-54.sensor`: callout 54 on pdf-101, no callout of this label on the drawing.
- `switch.matrix-62.sensor`: callout 62 on pdf-101, no callout of this label on the drawing.
- `switch.matrix-72.sensor`: callout 72 on pdf-101, 0.076 normalized away.
- `switch.matrix-76.sensor`: callout 76 on pdf-101, no callout of this label on the drawing.
- `switch.matrix-77.sensor`: callout 77 on pdf-101, 0.129 normalized away.

## Unresolved physical geometry

- G.I. string 1 (Back Panel) has no placement: the table models none of its bulbs, and no factory drawing locates G.I. bulbs, so spatial_placement stays in coverage.missing.
- The G.I. placements of strings 2-5 rest on the table's own grouping; no drawing or per-string bulb count validates them.
- Lamps 71-73 (a stacked three-lamp bar on the lamp drawing) and the back-panel flashers 17, 55 and 56 have no placement: the table renders them only as Flasher sprites.
- The lamp drawing hides its jet bumpers under ramp linework, so its control fit rests on the three flipper pivots and the Cryoclaw pivot hub; its leave-one-out control error is large, and the leave-one-out callout fit carries the check.
- Hidden mechanism contacts (trough optos, claw position optos, elevator index, end-of-stroke switches) have whole-mechanism projections or none.

## Promotion decision

partial: every used device has a placement or a controlled not-applicable record except the back-panel G.I. string, three lamps and three back-panel flashers; the factory drawings validate most checked table placements, but the G.I. bulbs cannot be validated from any retained drawing or count.
