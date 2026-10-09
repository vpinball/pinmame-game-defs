# NBA Fastbreak (Bally, 1997) spatial blockers

Retained VPX SHA-256 `d4d242abc77c106d195310d6d8a66cd2d8c1ffadf9ec8ac8aacc588cc87cb912`; script `69537260b7bc976a136a8ea1a4bd63ce7e0c09f81c766eafcbb765e9cb0b1a31`; 2237-file extraction manifest `37bb4b83816dfdbd700b116035f026d71346292dda861b37bdb6057bab906ac1`; manual `c901d3301766fec9c55dea8d8be22e08cbdf1edfd1dee5c67716fa3f728ad551`.

Bounds: `left=0 top=0 right=964 bottom=2162`. Every canonical coordinate is x/964 and y/2162 rounded to at most six places (factory-drawing measurements to three).

## Placement status

- `validated`: 104 devices
- `observed`: 41 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 62
- used devices with no placement record: 2 (`gi.string-4`, `gi.string-5`)

## Projection classes

- **switch:** The retained table's collision object for the switch (trigger, target, kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are projected onto the trough's BallRelease kicker because the script derives them from a ball count; the five defender optos 51-55, which the table derives from its cvpmMech, are measured on the switch drawing, where each has its own leader.
- **lamp:** The script-driven Light's own centre (render doubles collapsed by the smallest falloff), validated where the lamp drawing marks the same insert; the In The Paint lamps 67, 68, 77 and 78, which the table draws only as Flupper domes, take the dome base. Lamp 61's two bulbs are both placed.
- **solenoid:** The object the solenoid callback moves (wall, gate, saucer kicker, magnet trigger, flipper, bumper, slingshot) or the Flupper dome base it lights, validated where the solenoid drawing's callout agrees. The defender motor lines 37/38, the shot clock lines 39/40 and the trophy insert flasher 22 have no table object and are measured on the drawing.
- **gi:** Per-string collections of the table's UpdateGI lights for strings 1-3, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs. Strings 4 and 5 have no table collection and no placement.
- **display:** The shot clock display at the midpoint of the table's two digit sprites on the backboard, observed.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 106 of the 119 table placements it checks ([seed](../../../tools/seeds/bally/nba-fastbreak-1997-callouts.json)); the rest keep their observed status:

- `device.left-ramp-diverter.effect`: callout 03 on 2-41, 0.079 normalized away.
- `device.loop-gate.effect`: callout 06 on 2-41, 0.101 normalized away.
- `device.pass-left-2.effect`: callout 16 on 2-41, 0.076 normalized away.
- `device.pass-left-3.effect`: callout 26 on 2-41, 0.087 normalized away.
- `device.pass-right-3.effect`: callout 27 on 2-41, 0.079 normalized away.
- `lamp.matrix-61.emitter.1`: callout 61 on 2-45, every callout of this label marks a nearer placement.
- `lamp.matrix-67.emitter`: callout 67 on 2-45, 0.108 normalized away.
- `lamp.matrix-77.emitter`: callout 77 on 2-45, 0.079 normalized away.
- `switch.matrix-25.sensor`: callout 25 on 2-43, 0.170 normalized away.
- `switch.matrix-41.sensor`: callout 41 on 2-43, 0.079 normalized away.
- `switch.matrix-42.sensor`: callout 42 on 2-43, 0.243 normalized away.
- `switch.matrix-64.sensor`: callout 64 on 2-43, 0.169 normalized away.
- `switch.matrix-67.sensor`: callout 67 on 2-43, 0.262 normalized away.

## Unresolved physical geometry

- General illumination strings 4 and 5 (public GI 3 and 4) are wired to playfield #44 bulbs, but neither the retained table nor any retained drawing or count locates them, so they have no placement.
- The GI placements of strings 1-3 rest on the retained table's own grouping; no factory drawing or bulb count locates GI bulbs, so they stay observed.
- Placements the drawings do not confirm keep their observed status; each such device's note says what the drawing showed.

## Promotion decision

partial: every fitted device has an observed or validated placement or a controlled not-applicable record except the always-on GI strings 4 and 5, and no general-illumination placement can be validated from any retained drawing or count.
