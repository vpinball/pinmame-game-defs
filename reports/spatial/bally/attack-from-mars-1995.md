# Attack From Mars (Bally, 1995) spatial review

Status: validated and promoted to `machines/author-ready/bally/attack-from-mars-1995.json`.

The matching source is the retained known-working `Attack from Mars 3.02.vpx` by JPSalas at SHA-256 `f4bd2ae0e456030d14ea2f6f8fcd45e0e4f72ff22235a908d17424f1e9441cbd`. A fresh `vpxtool` extraction produced the embedded script at SHA-256 `46992cf7854853bac592ab9b2b5f65d641727accec8405b7aff84fbc8e2aa139`; that embedded stream is the runtime and causality authority. `vpxtool` established exact playfield bounds `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded JPSalas script is the runtime address and causality authority; the Bally operators handbook is the physical inventory, quantity, polarity and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry; and the pinned LibPinMAME harness supplies runtime observation.
- The retained manual PDF is an image-only scan. Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/attack-from-mars-1995/manual-transcription.md`; no OCR text was treated as authority.
- Flasher representation in the retained table needs care. Solenoids 20, 21, 22, 23 and 28 have an ordinary `Light` object at the bulb. Solenoids 17, 18, 19, 25, 26 and 27 do not: the author draws each as a raised `flare_red` glare quad sitting at the bulb position plus one or two `flw` wall-glow quads pinned to the left rail at `pos_x -2.5`, the right rail at `pos_x 947.5` or the rear wall at `pos_y 10`. For those six the flare origin is the only coordinate the table offers for the bulb and is used as the anchor, which the projection list records device by device. The wall glows are light spill projected onto the cabinet, never sockets, and are excluded from both placement and multiplicity.
- Solenoid 19 Right Side High is the one flasher whose stored `pos_x`/`pos_y` is stale in the retained table, pointing at (71, 800) on the left. Its drag-point centroid, its own right-rail wall glow at the same y, the manual solenoid-location map and the fact that its printed assembly A-20549 is the right wire ramp all place it on the right, and the centroid is used.
- GI strings 0-2 use the table's `aGiLLights`, `aGiMLights` and `aGiTLights` arrays. The table pairs each bulb with a co-located halo light, so those 50 light objects reduce to 29 distinct emitter positions. The manual prints no per-string bulb count, so strings 01 and 02 take their asserted physical quantity from those deduplicated arrays. String 03 asserts no quantity at all: three further bulb lights sit at the jet-bumper centres outside the modulated collection and the evidence does not settle whether they are additional sockets on that string, so its fourteen placements are the emitters the string is observed to drive rather than a claimed socket inventory. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record with no asserted count.
- The sixteen saucer L.E.D.s at public lamp addresses 91-98 and 101-108 are not in the printed lamp matrix. They are shifted into board A-20670 by public solenoids 37 and 38, and the pinned harness observed every one of the sixteen lit across four attract phases, eight at a time, with solenoids 37, 38, 41 and 42 active alongside them.
- Solenoids 41, 42 and 43 are PinMAME's mirrors of auxiliary outputs 37, 38 and 39, and custom solenoids 51, 52 and 53 are second views of 33, 34 and 35/36. All six are declared virtual with a `virtual` spatial record so no duplicate device is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 31: Projected onto the retained trough-exit kicker BallRelease. The retained table models the trough as an abstract four-ball cvpmTrough with no per-position objects, so no per-ball coordinate is observable from it; the manual switch-location map places the whole trough under the apron with the eject opto outboard of Trough Ball 1.
- Switch 32: Projected onto the retained trough-exit kicker BallRelease; see switch 31. Trough Ball 1 is the position nearest the eject.
- Switch 33: Projected onto the retained trough-exit kicker BallRelease; see switch 31.
- Switch 34: Projected onto the retained trough-exit kicker BallRelease; see switch 31.
- Switch 35: Projected onto the retained trough-exit kicker BallRelease; see switch 31. Trough Ball 4 is the position furthest from the eject.
- Switch 66: Projected onto the retained backbank moving-target assembly. The position switch is under the playfield inside 3-bank motor assembly A-20572 and has no separate table object.
- Switch 67: Projected onto the retained backbank moving-target assembly. The position switch is under the playfield inside 3-bank motor assembly A-20572 and has no separate table object.
- Solenoid 1: Projected onto the retained shooter-lane trigger swPlunger. The retained table drives the auto plunger through cvpmImpulseP bound to that trigger and models no separate kicker object; the manual solenoid-location map places kicker bracket A-14525 at the back of the same shooter lane.
- Solenoid 17: Taken from the origin of the retained flasher object f17a. Solenoids 17, 18, 19, 25, 26 and 27 have no separate emitter object in the retained table: the author draws each as a raised flare quad at the bulb position plus one or two wall-glow quads projected onto the cabinet walls. The flare origin is the bulb position and is used as the anchor; the wall glows are excluded because they are light spill, not sockets.
- Solenoid 18: Taken from the origin of the retained flasher object f18a; see solenoid 17.
- Solenoid 19: Taken from the drag-point centroid of the retained flasher object f19a rather than its stored pos_x/pos_y, which the table author left at a stale (71, 800) on the left. This is the one flasher whose stored origin is wrong. The centroid, the matching f19b right-wall glow at the same y, the manual solenoid-location map, and the printed assembly A-20549 Right Wire Ramp all place Right Side High on the right of the playfield.
- Solenoid 25: Taken from the origin of the retained flasher object f25a; see solenoid 17.
- Solenoid 26: Taken from the origin of the retained flasher object f26a; see solenoid 17.
- Solenoid 27: Taken from the origin of the retained flasher object f27a; see solenoid 17.
- Solenoid 35: Projected onto the retained diverter blade primitive DivP. The retained table actuates the diverter through an invisible flipper object parked off the playfield at (0.843508, 0.984320), which is a physics helper and not the physical blade location.
- Solenoid 36: Projected onto the retained diverter blade primitive DivP; see solenoid 35. The hold winding acts on the same blade as the power winding.
- Solenoid 45: Projected onto the retained RightFlipper object; the power and hold windings are the two windings of the same FL-11629 coil on assembly A-15849-R-2.
- Solenoid 46: Projected onto the retained RightFlipper object; see solenoid 45.
- Solenoid 47: Projected onto the retained LeftFlipper object; the power and hold windings are the two windings of the same FL-11629 coil on assembly A-15849-L-2.
- Solenoid 48: Projected onto the retained LeftFlipper object; see solenoid 47.
- Lamp 91: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 92: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 93: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 94: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 95: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 96: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 97: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 98: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 101: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 102: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 103: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 104: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 105: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 106: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 107: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.
- Lamp 108: Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 share one assembly and the retained table models no individual L.E.D. objects, so every address takes the saucer assembly anchor.

## Counts

- Placements: 187
- Located input addresses: 44
- Located output bindings: 116
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 18
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `internal_nonvisual` record: 2
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 14

## Promotion decision

No authoring-critical placement, polarity, quantity, or semantic question remains unresolved, the definition carries no conflict records, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Promotion to `author_ready` is therefore justified.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/attack-from-mars-1995/extraction-manifest.json`, SHA-256 `f2d555ebcf2b9dc563178400d741350006f8627f197eea47e2f2379045dbeb5e`, 745 files, 17831547 bytes.
- Candidate geometry `external:pinmame-review-artifacts/attack-from-mars-1995/vpx-spatial-candidates.json`.
- Rendered manual pages `external:pinmame-manuals/rendered/bally.attack-from-mars.1995/`; the 14 pages that decided a canonical value are listed with their SHA-256 in the companion JSON report, so an empty or substituted render cache is an audit failure rather than an assumed source.
- Human transcription of every printed table read from those pages, SHA-256 `eecef9b72e309e581c07fd5ecc8c5b4f9d3808f5bf4a4a3fdf53891e10296733`.
- Harness runs and DMD captures `external:pinmame-review-artifacts/attack-from-mars-1995/harness/`.
