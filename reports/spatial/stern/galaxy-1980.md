# Galaxy (Stern, 1980) spatial review

Status: incomplete. Every placement is `observed` and general illumination has none, so the machine record stays `partial` at `machines/partial/stern/galaxy-1980.json`.

The geometry source is the retained `Galaxy (Stern 1980).vpx` (bord, version 1.2) at SHA-256 `5c457aaea7ea8cab3bbe9900756cd90eaa0461413aeea9e3a5e756f21ede77fd`; its embedded script is byte-identical to the pinned known-working corpus script (SHA-256 `ac7e8751a2f26307a8d2ddd9a74c64af944b32aef8f2ddf896c1eab13d2856e4`). Exact playfield bounds are left 0, top 0, right 952, bottom 1974, and every canonical coordinate is x/952 and y/1974 rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.

## Evidence decisions

- The script's bindings choose each switch's and coil's object. Each lamp is placed on the bulb light (`L<n>a`) under the insert the script drives from its address, never on the insert overlay.
- The switch, lamp and solenoid assignments agree between the script, this game's lamp lists and the ROM; no table binding defect was found.

## Explicit projections

- pinmame.input.switch 4: Placed at the mean of the drop-target wall's own drag points, the target face the script drops; the leaf switch under the bank has no object.
- pinmame.input.switch 9: Placed at the mean of the drop-target wall's own drag points, the target face the script drops.
- pinmame.input.switch 10: Placed at the mean of the drop-target wall's own drag points, the target face the script drops.
- pinmame.input.switch 11: Placed at the mean of the drop-target wall's own drag points, the target face the script drops.
- pinmame.input.switch 15: Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position.
- pinmame.input.switch 16: Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position.
- pinmame.input.switch 18: One placement per star, on the two triggers the script binds to this address (sw18 left of centre, sw18a at the centre between the lower lanes).
- pinmame.input.switch 33: Placed on the table's Drain kicker, its ball-collection proxy for the out-hole; the out-hole switch itself is not modelled.
- pinmame.output.solenoid 1: Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 2: Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 4: Projected onto the 4-bank it resets: the mean of the table's own four drop-target walls. The reset coil sits under the bank and has no object.
- pinmame.output.solenoid 8: Placed on the saucer's switch trigger, the pocket the coil ejects from; the table's saucer has no separate kicker object.
- pinmame.output.solenoid 9: Projected onto the red drop target it knocks down: its own coil sits under that target and has no object.
- pinmame.output.solenoid 10: Projected onto the blue drop target it knocks down.
- pinmame.output.solenoid 11: Placed on the table's Drain kicker, the ball-collection proxy where the ball enters the out-hole; the out-hole coil is not modelled.
- pinmame.output.solenoid 13: Projected onto the yellow drop target it knocks down.
- pinmame.output.solenoid 14: Projected onto the black drop target it knocks down.
- physical.input.direct 1: Placed on the left flipper pivot: the end-of-stroke contact is mounted on its flipper assembly.
- physical.input.direct 2: Placed on the right flipper pivot: the end-of-stroke contact is mounted on its flipper assembly.

## Counts

- Placements: 94 (94 observed) on 92 records
- Records with a controlled `cabinet_or_service` record: 25
- Records with a controlled `dip_switch` record: 32
- Records with a controlled `internal_nonvisual` record: 1
- Records with a controlled `unused` record: 19
- Records with a controlled `virtual` record: 2
- Records with no spatial key: 1 (gi.general-illumination)

## Excluded table objects

- l<n> insert overlays, l<n>z and l27c glows: render helpers drawn over or under the inserts; every lamp is placed on its bulb light L<n>a (and L27b) instead
- GI1 collection lights, flashers and the VR backglass objects: render and general-illumination helpers; the general illumination has no bulb inventory in any retained source
- Gate1, Gate2: the two passive gates of the mechanism record, carrying no controller binding; Gate7 is a hidden gate in the shooter lane
- Drain: the table's ball-collection kicker, used only as the projection point of the out-hole switch and kicker

## Blockers

- Every placement is `observed`: the manual prints no lamp-location drawing, so nothing independent checks the lamp positions, and the switch and coil placements have not been through the factory location-drawing callout check (tools/drawing_callouts.py) against the manual's switch and solenoid drawings (PDF pages 17 and 19).
- General illumination has no placement: no retained source gives its bulb quantity or positions, and the table's GI light collection is render membership, not a socket count.

## Promotion decision

Promotion to `author_ready` is refused: every placement rests on one community table with no independent check, and general illumination has no placement. The record stays `partial` with `coverage.missing = ["spatial_placement"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/galaxy-1980/bord-1.2/Galaxy (Stern 1980)/manifest.json`, SHA-256 `ebdb7074712c2457cdad50a8e4bea5b9bfac641f59aae6cd10462edccc122446`, 1292 files, 123292884 bytes.
- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/galaxy-1980/bord-1.2-geometry.tsv`.
