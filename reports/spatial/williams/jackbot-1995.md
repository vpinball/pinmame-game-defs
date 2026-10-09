# Jack•Bot (Williams, 1995) spatial blockers

Retained VPX SHA-256 `31b827ba75dc7bc9fab1b3df5c9ff0708b235eb46e64666a781d4721fce4260f`; script `8edd32cea57460f1d76b864e39b742bb3bc77c0c201816a72094e4476c516c8b`; 1603-file extraction manifest `8c76313b82c0c5850c94c5e1eab0f3f478091422a8f2fe7a4c1dcdb9b75bbea7`; manual `8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`.

Bounds: `left=0 top=0 right=952 bottom=1974`. Every canonical coordinate is x/952 and y/1974 rounded to at most six places (factory-drawing measurements to three).

## Placement status

- `validated`: 72 devices
- `observed`: 68 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 68
- used devices with no placement record: 0

## Projection classes

- **switch:** The retained table's collision object for the switch (trigger, target, drop-target wall, saucer kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are projected onto the trough's BallRelease kicker because the script derives them from a ball count. Switches with no live table object (the rubber switches 11, 12 and 66, the ramp-down switch 15 and the visor switches 115 and 117) are measured on the switch drawing.
- **lamp:** The script-driven Light's own centre (the smaller-falloff member of each render double), validated where the lamp drawing marks the same insert; the drawing's chest-matrix inset is not at playfield scale and checks nothing. The mini-playfield lamps 71-74 and the lamps 75 and 76, which the table draws without a Light, take the bulb or sign object the script drives.
- **solenoid:** The object the solenoid callback moves (saucer kicker, drop-target wall, flipper, bumper, slingshot), the flasher dome primitive or the Light the script fades, validated where the solenoid drawing's callout agrees. The ramp coils 6 and 14, the visor motor 28 and the visor flashers 15-17, for which the table has no usable object, are measured on the solenoid drawing; the back-panel flashers 23-27 sit on the table's back-panel domes and the drawing's back-panel strip is not at playfield scale.
- **gi:** Per-string collections of the table's UpdateGi lights for strings 1-4, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates G.I. bulbs. String 5 lights the backbox insert panel and is not placed.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 72 of the 77 table placements it checks ([seed](../../../tools/seeds/williams/jackbot-1995-callouts.json)); the rest keep their observed status:

- `lamp.matrix-67.emitter`: callout 67 on 2-35, 0.070 normalized away.
- `lamp.matrix-75.emitter`: callout 75 on 2-35, 0.111 normalized away.
- `lamp.matrix-76.emitter`: callout 76 on 2-35, 0.123 normalized away.
- `lamp.matrix-85.emitter`: callout 85 on 2-35, 0.071 normalized away.
- `switch.matrix-36.sensor`: callout 36 on 2-37, 0.074 normalized away.

## Unresolved physical geometry

- The G.I. placements of strings 1-4 rest on the retained table's own grouping; no factory drawing or bulb count locates G.I. bulbs, so they stay observed.
- Placements the drawings do not confirm keep their observed status; each such device's note says what the drawing showed.

## Promotion decision

partial: every fitted device has an observed or validated placement or a controlled not-applicable record, but no general-illumination placement can be validated from any retained drawing or count.
