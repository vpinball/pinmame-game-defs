# Tales of the Arabian Nights (Williams, 1996) spatial review

Status: conflicted. Every switch, solenoid, and lamp address that the retained table can support is located and validated, but two GI addresses have no supporting VPX object and a third carries a genuine manual-versus-script wiring disagreement, so the physical machine record stays `partial` at `machines/partial/williams/tales-of-the-arabian-nights-1996.json`.

The matching source is the retained known-working `Tales of the Arabian Nights (Williams 1996).vpx` at SHA-256 `487375925e6f44998cd416b6d28983f08144d2bfe7a1432ac9ad16af7b23fec0`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `c4a742f2188c9e3dcba70a7717d5b8985bbd1d913cc05c17df3b2f9d341b876b`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2164`, and every canonical coordinate is x/952 and y/2164 (not 2162) rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries a genuine OCR text layer, but `pdftotext -layout` badly garbles the multi-column switch/solenoid/lamp tables. Every printed table used here was re-verified visually against the 300 dpi rendered pages and transcribed into `external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/manual-transcription.md`.
- Two switches (31, 42) and two mechanism-driven switches (56, 57) have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (trough ball-release event, Genie figure rock angle, Spinning Lamp Unit disc rotation) rather than from a discrete Hit event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- This retained table is smaller and older than the VPW mods used for several other curated WPC games (944 files, no VPW authorship). Its object set does not support a validated playfield placement for GI addresses 3 and 4, so those two devices are left spatially unresolved rather than assigned a fabricated coordinate.
- GI address 2 carries a first-class unresolved conflict: the manual documents it as backbox-only but the retained script binds only that address to a playfield-wide dimming effect. The manual's physical wiring controls this device's spatial classification (not_applicable/cabinet_or_service).
- Solenoids 16 and 17 (Left Eject Flasher, Inlane Flashers) print two playfield bulbs each, but the retained table models only one Light object per address; one placement is recorded and the quantity gap is disclosed in `physical.notes` rather than fabricating a second coordinate.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 31: Projected onto the trough Ball 1 kicker position (sw32): the retained script's ball-release handler (SolRelease) kicks the ball resting on switch 32 and pulses trough-eject opto 31 in the same event (vpmTimer.PulseSw 31), and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.
- Switch 42: Projected onto the Genie figure (Primitive GenieP, table object center): public switch 42 (Genie Target) is set from UpdateGenie's rocking-angle threshold (GenieAngle > 4.5) on the figure itself, not from a discrete trigger-hit event on either physical target blade.
- Switch 56: Projected onto the Spinning Lamp Unit disc center (Primitive LampPr/LampPr1/LampPr3, table object center at raw (510, 840)): SpinnerBallTimer_Timer pulses public switch 56 (Lamp Spin CCW) whenever the disc's simulated rotation crosses a position threshold while spinning counter-clockwise; there is no fixed sensor object.
- Switch 57: Projected onto the Spinning Lamp Unit disc center; see switch 56. SpinnerBallTimer_Timer pulses public switch 57 (Lamp Spin CW) at the same thresholds while the disc spins clockwise.

## Unresolved (no fabricated placement)

- pinmame.output.gi address 3: no VPX object bound to this playfield GI address in the retained extraction
- pinmame.output.gi address 4: no VPX object bound to this playfield GI address in the retained extraction

## Counts

- Placements: 146
- Located input addresses: 42
- Located output bindings: 98
- Unresolved output bindings: 2
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 20
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `virtual` record: 28

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for switches, solenoids, lamps, or the flipper pair. GI address 2 carries a first-class, unresolved conflict between the manual's physical wiring and the retained script's runtime binding (`conflict.gi-string-3-playfield-binding`), and GI addresses 3 and 4 -- the manual's genuine playfield strings -- have no VPX object to validate a placement from in this retained (non-VPW) table. The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"` / `coverage.dimensions.spatial_placement = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]` until a LibPinMAME harness trace against a legal totan_14 ROM observes which GI address the ROM actually varies during attract-mode playfield dimming.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/extracted-vpxtool.manifest.json`, SHA-256 `761846f3369203502a9083c19e46a0da046893a46df43abc734a53c61b19a04d`, 944 files, 128702095 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `fd33e241ed3715c93213ced0f051df1a72a1d042eb9dda0536273eb3b84ac176`.
