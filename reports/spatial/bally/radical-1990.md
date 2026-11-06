# bally.radical.1990 spatial evidence

Coverage: **partial**. Every located placement remains **observed**.

x=0 left, x=1 right; y=0 rear/backglass, y=1 apron/player.

Placements: 153; omitted device spatial records: 4.

## Evidence and transformation

Exact hashes, every selected VPX object and source coordinate, diagram pixels, six controls and affine coefficients are retained in `tools/seeds/bally/radical-1990-spatial.json`. Full extraction integrity is checked separately. VPX normalization uses the shared helper against bounds 0,0,952,1974. The manual lamp-location drawing is projected through `tools/drawing_callouts.py` and rounded to 0.001; these are insert-center projections and no socket survey is claimed. The maximum control leave-one-out error is 0.014408 normalized. All extrapolated measurements stay observed. The 0.07 callout convention is only a cross-check limit; it does not promote these projections.

## Projection classes

- Matrix lamps: center of each numbered illuminated insert in the manual drawing, projected to the playfield plane.
- Lock sensors: their own script-bound ball kickers, not separate switch bodies.
- Bowtie sensor: vertex mean of its own mechanism wall, not a measured microswitch.
- Sling scoring contacts: own rubber-wall vertex means, not leaf-contact bodies.
- Coils: effect anchors on their own mechanism/ball path; no under-playfield coil location is asserted.
- GI: one bulb-mesh light per exact center; retain the smallest falloff-radius render double, then lexical name.
- Flashers 9/25..32: the callback-bound VPW dome bases, whose origins were checked against actual exported world-mesh bounds; independent Bumper controls verify that coordinate plane.
- Flasher 16: the factory's own numbered symbol on PDF 84, projected by a separate six-control fit (maximum leave-one-out error 0.008251), explicitly extrapolated and observed. The table's bulbless glow is not the coordinate source.
- Middle Man 27: midpoint of the distinct factory-marked horizontal actuator blade on PDF 82, projected by that page's own six-control fit (maximum leave-one-out error 0.006349), explicitly extrapolated and observed; no precise contact-body center is claimed.

## Remaining evidence

- All placements remain observed. The lamp drawing provides insert-center projections, not socket centers; measurements outside its six-control convex hull are extrapolated. Table geometry and manual drawings are potentially related evidence, not independent factory measurements.
- The 39 modeled playfield GI bulb centers are table observations. No own-machine wiring or complete GI socket diagram assigns/counts every physical emitter; the fitted count and completeness remain unproved.
- Flasher16 now has an observed factory-symbol projection from its own solenoid-location drawing; the point is extrapolated and not independently surveyed. Other playfield flashers use the VPW dome bases; backbox emitters sharing these circuits do not receive invented playfield coordinates.
- The table's Drain kicker is a ball-disposal helper, not an outhole sensor/coil center. Trough switches 11 and 12 and the outhole switch 10 / coil 1 lack defensible table coordinates. A measured underside/location drawing or physical survey is needed.
- Middle Man 27 now has an observed factory-actuator projection onto its own horizontal blade on the switch-location drawing. This point is extrapolated and does not claim the hidden microswitch body center or independent placement validation.

## Omitted spatial records

- `switch.outhole-10`: `pinmame.input.switch` 10
- `switch.trough-1-right-11`: `pinmame.input.switch` 11
- `switch.trough-2-left-12`: `pinmame.input.switch` 12
- `output.outhole-1`: `pinmame.output.solenoid` 1

Remain partial; no author-ready promotion is justified.
