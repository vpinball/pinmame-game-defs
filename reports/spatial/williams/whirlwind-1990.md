# Whirlwind (Williams, 1990) spatial review

Status: validated. The physical machine record itself remains `partial` at `machines/partial/williams/whirlwind-1990.json` because of the unresolved backglass-vs-playfield flasher mounting conflict and the unconfirmed opto polarity noted below; see the promotion decision.

The matching source is the retained known-working `Whirlwind (Williams 1990).vpx` at SHA-256 `105477078e68547c24167fc9ba99baeff24ec48ce16c46ec2530184a67f92e23`. The retained vpxtool extraction produced the embedded script at SHA-256 `e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology and the System 11 address-space rules; the retained table supplies geometry.
- System 11 has no separate GI address space: GI is simply two ordinary solenoid addresses (11, 16) whose per-game bulb-type metadata happens to be continuous AC GI bulbs, resolved from pinned PinMAME's own per-game MACHINE_INIT block rather than any fixed platform range.
- Switches 10-13 (outhole/trough) and 42 (right ramp down) have no dedicated VPX trigger object in the retained table; they are documented projections onto the nearest real mechanism object (the Drain/BallRelease kickers, and the Right Ramp's own up/down geometry) rather than invented coordinates.
- Eleven flasher addresses are implemented purely as backglass effects in the retained table even though the manual names them after playfield features; this is recorded as an unresolved first-class conflict and their spatial keys are omitted rather than guessed either way.
- GI address 11 has an empty light collection in the retained table; its spatial key is omitted rather than invented, matching the precedent set for Star Trek: The Next Generation's unresolved lamps.
- The three spinning discs are a pure motor mechanism (solenoid 41) with no position sensor, confirmed independently by both the retained script (no Controller.Switch call for any disc object) and the manual's own Wheels Drive Assembly parts list (no switch/opto part).
- The alphanumeric display is cabinet/backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 10: Projected onto the Drain kicker (Kicker.Drain, table object center): switch 10 (Outhole) has no dedicated VPX trigger object -- the retained script's cvpmBallStack helper (bsTrough.InitSw 10,11,12,13) manages it abstractly, and Drain is the physical object nearest the outhole funnel (Drain_Hit feeds the trough via bsTrough.addball).
- Switch 11: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center): switches 11-13 (Ball Trough #1-#3) have no individual VPX trigger objects -- the retained script's cvpmBallStack helper manages all three abstractly against the single BallRelease exit kicker (bsTrough.InitKick BallRelease,75,4), the trough mechanism's own retained object.
- Switch 12: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.
- Switch 13: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.
- Switch 42: Projected onto the Right Ramp's own retained geometry (the RightRampUp/RightRampDown shared entry endpoint, table object center): switch 42 (Right Ramp Down) has a real printed switch part (5647-12001-00) but no dedicated VPX trigger object -- the retained script instead sets Controller.Switch(42) directly from the same SolRightRampEntryLifter/SolRightRampEntryDown handlers that swap the ramp's up/down geometry, because the physical switch is mechanically slaved to the same ramp position those solenoids control.

## Counts

- Placements: 123
- Located input addresses: 46
- Located output bindings: 77
- Outputs with an intentionally omitted spatial key: 12
- Inputs with a controlled `cabinet_or_service` record: 13
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 8
- Outputs with a controlled `cabinet_or_service` record: 9
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `virtual` record: 15

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit locates. However, eleven flasher solenoid addresses (25-32, 37, 39, 40) are implemented purely as backglass effects in the retained table while the manual names them after playfield features -- an unresolved conflict recorded as `conflict.flasher-backglass-vs-playfield-mounting` -- and four opto switches (26-29) plus the flipper-lane-change opto pair (57, 58) have confirmed construction but no confirmed rest-state polarity, since pinned PinMAME declares no inverted-switch mask at all for this driver. The definition therefore carries a non-empty `conflicts` array and `coverage.missing = ["polarity", "spatial_placement", "unresolved_conflicts"]`, so promotion to `author_ready` is refused; the record stays `partial` until a second independent table, a photograph of an unrestored machine's playfield, or a manual wiring diagram settles the flasher-mounting question, and a LibPinMAME harness trace or a manual opto-polarity legend settles the rest-state question.

## Retained evidence

- Retained vpxtool extraction, 1881 files.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `af6d1a70eea94ac46baa6858fa220766eaf0dddaf90684179fc5687e51c0fbe6`.
- VPX script/geometry cross-reference, SHA-256 `dfe62e82674ca6ce91cc20fad8f1a648add5e3d278e677dfb34128f312f8020b`.
