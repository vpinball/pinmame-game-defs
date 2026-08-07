# World Cup Soccer (Bally/Midway, 1994) spatial review

Status: validated. Every switch and lamp address in this audit is fully placed or carries a controlled `not_applicable` record; the one gap is a single solenoid (34, Loop Gate) with no evidence of any kind for its playfield location, which keeps the machine record `partial` at `machines/partial/midway/world-cup-soccer-1994.json` alongside the unresolved Fliptronic opto-polarity conflict recorded separately below.

The matching source is the retained known-working `World Cup Soccer (Bally 1994) VPW v1.5.vpx` at SHA-256 `ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=2152.941`, and every canonical coordinate is x/952.941 and y/2152.941 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Midway operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries a genuine but unreliable OCR text layer on multi-column tables; every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md` and its per-table excerpts.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (the goalie's own independent sinusoidal simulator, or the trough-eject event) rather than from a Hit/Trigger event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- Lamp addresses with a printed bulb quantity of two (46, 47, 71, 78) are two genuinely separate playfield placements, not co-located brightness doubles: the manual prints a distinct assembly number for each bulb, and the retained table's second Light object for each address sits at a materially different coordinate.
- GI strings 0, 1, and 4 use the retained table's GILeft/GIRight/GITop emitter collections, matching the retained script's GIUpdate2 dispatch exactly. GI strings 2 and 3 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- The synthetic solenoid mirror at public address 51 (wcs_getSol's OR of solenoids 8 and 16) is declared virtual with a `virtual` spatial record so no duplicate diverter mechanism is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 36: Projected onto the trough eject Kicker (Trigger/Kicker sw31, table object center): the retained script's SolTrough handler fires sw31.kick and vpmTimer.PulseSw 36 in the same event (no separate playfield object represents Trough Stack), and pinned PinMAME's own sim ball-routing table (wcs_stateDef) places the 'Trough stack' state immediately after the 'Trough 1' eject state in the ball's path toward the shooter lane.
- Switch 43: Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center): the retained script's InitGoalie sets BP_goalkeeper.x=376/.y=280, matching this primitive's own position (374.4,281.5) almost exactly, and wcs_handleMech sets public switches 43/44 directly from the DC-motor position counter (mech_getPos(0)) rather than from a fixed playfield sensor object.
- Switch 44: Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center); see switch 43.
- Switch 48: Projected onto the shooter-lane switch/plunger position (Trigger.swPlunger, identical coordinates to Trigger.sw38): the retained script's GWalls_Hit handler (triggered when a ball strikes the goalie's 35-segment target-wall ring) pulses public switch 48 without a dedicated playfield sensor object of its own; the coordinate used here is the nearest fixed reference in the same script region rather than an invented target-wall centroid.

## Counts

- Placements: 194
- Located input addresses: 51
- Located output bindings: 98
- Outputs with no spatial key at all: 1
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 10
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 15

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit can place, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, two blockers keep this record `partial`: public switches 112/114 are printed opto interrupters that pinned PinMAME does not normalize (`conflict.flipper-cabinet-opto-not-normalized`, unresolved), and solenoid 34 has no evidence of any kind for its playfield location. The definition therefore carries a non-empty `conflicts` array, `coverage.dimensions.physical_wiring = "conflicted"`, and `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`, so promotion to `author_ready` is refused until a LibPinMAME harness trace resolves the polarity question and further evidence (a wiring diagram, a differently-authored VPX table, or a physical-machine inspection) resolves solenoid 34's location.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/midway/world-cup-soccer-1994/extracted-vpxtool.manifest.json`, SHA-256 `eab6beeaca073c66c01cacaee71d605f3629832062e56f67d92a31405d438032`, 2588 files, 773038506 bytes.
- Human transcription index of every printed table read from the rendered manual pages, SHA-256 `7055d31403f69bedd4dffa94aad45952c18e75065941e204338eb9a818690f75`.
