# The Sopranos (Stern, 2005) spatial blockers

Retained VPX SHA-256 `9bbc98d47888c28843cf17aa7f8ce5d04671da86ee1e76ddb1f2cd330b30162c`; script `56262b8bb13d295504abe54f0f586a5e6d288cb4f4b55963889d13c7ba57de08`; 1441-file extraction manifest `7e2a9c25d8f694b6f6cf24b375f9d95b6450f4a1463ba245a0487a93395dc091`; manual `4765c79a9fac44d14e4330477ffb4ab4d7af259499a3b5d1156adf83d75b0c88`.

Bounds: `left=0 top=0 right=952 bottom=2300`. Every canonical coordinate is x/952 and y/2300 rounded to at most six places.

## Placement status

- `validated`: 112 devices
- `observed`: 24 devices
- `candidate`: 8 devices
- controlled `not_applicable` records: 71
- used devices with no placement record: 0


## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, gate, spinner, hit target, kicker, slingshot wall, bumper). The trough switches and the stacking opto, which the table does not model, are projected onto the release kicker BallRelease; the safe limit onto the midpoint of the two safe-door walls; each end-of-stroke contact onto its flipper.
- **lamp:** The centre of the insert Light each lamp's NFadeL call drives. The five Episodes lamps 73-77, which the table stacks at one point, are drawing-measured candidates.
- **solenoid:** The kicker, slingshot wall, bumper, flipper, post wall or gate the script fires, and for flashers the script-driven Light. The auto launch is placed on the shooter-lane trigger its impulse plunger uses; the drop-target coils on the target; the safe and safe-latch coils on the safe door; the fish jaw and fish flasher on the jaw primitive; the Bada Bing! relay on the dancers' midpoint. The UK AUX posts are drawing-measured candidates.
- **gi:** The 33 Light members of the table's GI collection; observed only, without per-string assignment.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 114 of the 121 table placements it checks ([seed](../../../tools/seeds/stern/the-sopranos-2005-callouts.json)); the rest keep their observed status:

- `device.q12-left-slingshot.effect`: callout 12 on pdf-9, 0.080 normalized away.
- `device.q13-right-slingshot.effect`: callout 13 on pdf-9, 0.084 normalized away.
- `device.q15-left-flipper.effect`: callout 15 on pdf-9, 0.130 normalized away.
- `device.q16-right-flipper.effect`: callout 16 on pdf-9, 0.111 normalized away.
- `device.q31-playfield-left-and-right-flashers-x2.emitter`: callout 31 on pdf-9, 0.124 normalized away.
- `device.q6-right-control-gate.effect`: callout 6 on pdf-9, 0.079 normalized away.
- `switch.33-right-orbit.sensor`: callout 33 on pdf-6, 0.089 normalized away.

## Unresolved physical geometry

- The trough switches 11-15 and the safe limit 10 are not modelled by the table; their placements are projections onto mechanism objects and stay observed.
- The five Episodes lamps 73-77 share one table point; their drawing-measured placements are candidates.
- The UK AUX posts 33-35 are not in the US table; their drawing-measured placements are candidates.
- The flipper and slingshot coils, the Q31 left flasher, the second Q29 dome and other placements listed below fail the callout limit or have no callout, and stay observed.
- The G.I. drawing is a mirrored bottom view without reliable controls, so the 33 G.I. placements stay observed although their count matches.

## Promotion decision

partial: every used device has a placement or a controlled not-applicable record, but projections, candidates and placements the drawings do not confirm keep spatial_placement in coverage.missing.
