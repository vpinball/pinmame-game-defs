# Black Rose (Bally, 1992) spatial blockers

Retained VPX SHA-256 `41f965d27c1615841d39f0b83922e09e37e2fe6bad54318fd6bf18b08c1b1a8e`; script `c860e49c2b8be296ce73a64b5e9715245e290b3c2a799f24640234534f799f25`; 1715-file extraction manifest `6bcef73e07d14a8452b900476d320e0c26fff5d81395166afb283e17c4956a94`; manual `63c80f33ae9570c6c9575b198f7b2d73634750f0395c7280782bf7e91437cc90`.

Bounds: `left=0 top=0 right=952 bottom=2162`. Every canonical coordinate is x/952.0 and y/2162.0 rounded to at most six places (factory-drawing measurements to three).

## Placement status

- `validated`: 106 devices
- `observed`: 27 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 73
- used devices with no placement record: 1

## Projection classes

- **switch:** Exact VPX collision object the retained script binds to the matrix switch (trigger, target, kicker, gate, bumper or slingshot wall), observed, and validated where the factory drawing's own callout agrees within the limit. The trough switches 16-18 and the Ramp Down switch 54 have no table object and are measured on the switch drawing; the cannon kicker switch 35 uses the cannon's CannonKicker kicker.
- **lamp:** Exact VPX Light centre for each lamp's playfield bulb, observed, validated where the lamp drawing's callout agrees; 11 and 86 place both of their bulbs. The backbox insert lamps 78 and 87 and the Credit button lamp 88 are controlled not-applicable records.
- **solenoid:** Named VPX mechanism anchor or visible effect object for each coil, and the script-driven bulb Light for each flasher with render doubles collapsed, observed, validated where the solenoid/flasher drawing's own callout agrees; the ramp-lift coils 10 and 11 have no table object and are measured on the drawing. Flipper windings print no callout and keep their table placements observed. The cannon motor (3) and the lockup coil (9) project onto the cannon disc and the first lockup kicker.
- **gi:** Per-string collections of table GI lights for the three playfield strings, collapsed where bulbs are stacked and without the jet-bumper glow helpers, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 109 of the 117 table placements it checks ([seed](../../../tools/seeds/bally/black-rose-1992-callouts.json)); the rest keep their observed status:

- `device.cannon-kicker.effect`: callout 8 on pdf-101, 0.074 normalized away.
- `device.outhole.effect`: callout 2 on pdf-101, 0.232 normalized away.
- `switch.matrix-15.sensor`: callout 15 on pdf-100, 0.118 normalized away.
- `switch.matrix-56.sensor`: callout 56 on pdf-100, 0.115 normalized away.
- `switch.matrix-61.sensor`: callout 61 on pdf-100, 0.133 normalized away.
- `switch.matrix-62.sensor`: callout 62 on pdf-100, 0.117 normalized away.
- `switch.matrix-66.sensor`: callout 66 on pdf-100, 0.290 normalized away.
- `switch.matrix-72.sensor`: callout 72 on pdf-100, 0.183 normalized away.

## Unresolved physical geometry

- The general-illumination bulb coordinates of the three playfield strings rest on the retained table's own grouping; no factory drawing or bulb count locates them, so their placements stay observed and spatial_placement stays in coverage.missing.
- The two Top Popper flashers (solenoid 25) sit on the back panel behind the Broadside popper; the drawing prints their balloons without leaders above the playfield's top edge and the table models them only as glow lights, so solenoid 25 has no placement.
- Hidden mechanism parts (the trough switches, the ramp-lift coils and the Ramp Down switch, the cannon motor and its catapult) are placed at the mechanism they belong to, not at a measured contact centre.

## Promotion decision

partial: every used device has a placement or a controlled not-applicable record except the Top Popper flashers, and the factory drawings validate most table placements, but the general-illumination bulbs cannot be validated from any retained drawing or count.
