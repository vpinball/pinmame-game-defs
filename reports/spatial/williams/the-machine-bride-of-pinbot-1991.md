# The Machine: Bride of Pinbot (Williams, 1991) spatial review

Status: author_ready.

Geometry comes from the retained known-working VPW 1.0.3 table (SHA-256 `041c49cff7ff206f570fbac4cfad01d075c8f2c6d8a09f27cdf78c68b3a60270`), whose embedded script (SHA-256 `b7624ad6d6f7cc807d55c2d83748239d7847a31f52d2314ebc1f318b55a4a3a7`) is the runtime authority. Exact bounds are `left=0 top=0 right=952 bottom=2162`; every coordinate is x/952 and y/2162 at six fractional places. The Williams operations manual (16-50002-101, March 1991) is the physical authority.

## Evidence decisions

- Jet-bumper switches follow the manual (both switch pages and the drawing), pinned bop.c names, and the ROM's switch-test names, not the retained script's permuted Bumper1/2/3 pulses.
- Helmet lamps follow the manual's helmet test (first lamp lower left, Up moves clockwise) combined with the ROM's single-lamp order (108 first, then 107 ... 101, 98 ... 91); the retained table's l91-l108 naming runs the opposite way round.
- Flasher domes 21-24 follow the manual's solenoid-locations drawing (21 left of the head, 22 right, 24 lower left, 23 lower right) and the retained script's SetRedDome1/2/4/3 bindings.
- Backbox insert lamps 71-85 and G.I. strings 0 and 3 take controlled `cabinet_or_service` records; the insert bulbs of flashers 18, 19, and 21-24 are counted in each flasher's quantity without a playfield placement.
- The helmet data and clock lines (25, 26) and the head motor relay (27) are `internal_nonvisual`.

## Explicit projections

- pinmame.input.switch 67: Face Position rides the head drive; the switch-locations drawing (2-41) prints it in the dashed drive housing about 0.1 further toward the rear, but no retained table object models it, so it is anchored at the head assembly's centre (Face primitive), which the head motor (28) shares.
- pinmame.output.solenoid 28: Head Motor placed at the centre of the head it rotates (Face primitive).
- pinmame.output.solenoid 8: Head Mouth Kicker placed on the retained TWKicker1 kicker-arm primitive behind the mouth opening.
- pinmame.output.solenoid 15: Head Left Eye Kicker placed on the retained TWKicker2 kicker-arm primitive behind the left eye opening.
- pinmame.output.solenoid 16: Head Right Eye Kicker placed on the retained TWKicker3 kicker-arm primitive behind the right eye opening.
- pinmame.output.gi 1: The helmet-light supply string is placed at the sixteen helmet bulb sockets it powers, shared with lamps 91-108.

## Counts

- Placements: 166
- Located input addresses: 41
- Located output bindings: 94
- Unresolved records: 0
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 22
- Outputs with a controlled `cabinet_or_service` record: 17
- Outputs with a controlled `internal_nonvisual` record: 3
- Outputs with a controlled `virtual` record: 21

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool.manifest.json`, SHA-256 `4090ee6bb9a55da0dc8aff6c6fecf92150e9aa0187ffe51b16f0a7e728749fd2`, 4084 files, 300991426 bytes.
- Manual SHA-256 `28b580b38af835cc8efa100d0b44f504684dce756ea7079ca9a042f34aa5c3b9`; committed excerpts under `evidence/excerpts/williams.the-machine-bride-of-pinbot.1991/`.
- Runtime evidence `evidence/runtime/wpc-alpha/bride-of-pinbot-head-helmet-and-service-names.json`.
