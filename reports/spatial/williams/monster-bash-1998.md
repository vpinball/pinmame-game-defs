# Monster Bash (Williams, 1998) spatial review

Status: validated. Every spatial dimension audited here is complete, but the physical machine record itself remains `partial` at `machines/partial/williams/monster-bash-1998.json` because of an unresolved switch-polarity conflict outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Monster Bash (Williams 1998) VPWmod v1.0.vpx` at SHA-256 `bef48b75b072c3fc8b4803639cc65f54144db6ff7e9476f6ea6b1fc23bc68c8d`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `b043d07c74693ce5c713a9edc1529413f3c2ec4420b63488085cd45e4fe413e8`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF is an image-only scan (`pdftotext` yields 158 bytes of form feeds only). Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/monster-bash-1998/manual-transcription.md`.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (Dracula motor step counter, Frankenstein figure rotation, Up/Down Bank target Z height) rather than from a Hit/Trigger event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- GIbot member `light11` sits at normalized x=1.087804, outside the retained table's 0..1 playfield bounds, and is excluded as a table modeling anomaly; GI address 0's physical quantity is 34, not the collection's raw 35 members.
- Flasher addresses 18-26 (excluding 17) each drive at least one playfield bulb; only the playfield bulb receives a coordinate. Address 17 (Wolfman Flashers) has zero playfield bulbs -- both fitted lamps are on the back panel and insert panel -- so it takes a `cabinet_or_service` record with role `cabinet.insert-panel`.
- GI strings 0-2 use the retained table's GIBot/GITopRight+GIBumpers/GITopLeft emitter collections, matching the retained script's `UpdateGi` dispatch exactly. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- Solenoids 41/42 are PinMAME's LPDC mirror of physical Dracula-motor drive lines 37/38 and are declared virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 25: Projected onto the rotating Dracula figure (Primitive Drac, table object center): DracTargets_Hit fires public switch 25 from a 47-segment target-wall ring that surrounds Drac and only one segment is active at a time (indexed from Drac.RotZ), so there is no single fixed target object.
- Switch 31: Projected onto the trough Ball 1 kicker position (sw32): the retained script's ball-release handler kicks the ball resting on switch 32 and pulses switch 31 (RandomSoundBallRelease sw32: vpmTimer.PulseSw 31) in the same event, and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.
- Switch 74: Projected onto the rotating Dracula figure (Primitive Drac, table object center): the five position optos 74-78 are printed on the A-21402 Defender Switch Board Assembly inside the Dracula mechanism and PinMAME's mb_mech reads them from a single 90-step motor-position counter, not five separate playfield objects.
- Switch 75: Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.
- Switch 76: Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.
- Switch 77: Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.
- Switch 78: Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.
- Switch 81: Projected onto the Up/Down Bank target assembly (Primitive frankytargets, table object center): the retained script sets public switches 81/82 directly from frankytargets.z threshold crossings rather than from a separate playfield sensor object.
- Switch 82: Projected onto the Up/Down Bank target assembly (Primitive frankytargets, table object center); see switch 81.
- Switch 83: Projected onto the Frankenstein figure (Primitive franky, table object center): the retained script sets public switches 83/84 directly from franky.rotx threshold crossings rather than from a separate playfield sensor object.
- Switch 84: Projected onto the Frankenstein figure (Primitive franky, table object center); see switch 83.
- Switch 87: Projected onto the centroid of the retained table's fhitwall collision wall, the hit surface raised while the Frankenstein figure is in striking position (public switch 87 is set from franky.rotx thresholds in the same handlers as switches 83/84, not from a Hit event on a fixed object).

## Counts

- Placements: 243
- Located input addresses: 55
- Located output bindings: 95
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 7
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 7
- Outputs with a controlled `virtual` record: 12

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, public switches 74-78 (Dracula Position 5 through 1) are printed normally-closed opto interrupters on the A-21402 Defender Switch Board Assembly that pinned PinMAME's mbGameData inverted-switch mask does not normalize (column 7 is 0x00, unlike columns 3 and 4), while PinMAME's own mb_mech[2] table asserts them at their step ranges in what reads as the opposite sense -- an unresolved polarity conflict recorded as `conflict.dracula-position-opto-not-normalized`. The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["polarity", "unresolved_conflicts"]` until a LibPinMAME harness trace against a legal mb_10 or mb_106b ROM observes the true idle public state of 74-78.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/monster-bash-1998/extracted-vpxtool.manifest.json`, SHA-256 `1361d166539823e12aedc983e95c0d1b0789dab291de4fd9a23f9aa830ec57ea`, 2153 files, 199010658 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `a5d8d4a1936fe379ed855227a1d73d3a26d95438f75e0c60f3b11e1080d84bfc`.
