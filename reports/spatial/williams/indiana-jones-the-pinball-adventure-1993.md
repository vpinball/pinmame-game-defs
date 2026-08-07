# Indiana Jones: The Pinball Adventure (Williams, 1993) spatial review

Status: validated. Every spatial dimension audited here is complete, but the physical machine record itself remains `partial` at `machines/partial/williams/indiana-jones-the-pinball-adventure-1993.json` because of two unresolved switch-polarity conflicts outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Indiana Jones The Pinball Adventure (Williams 1993) VPWmod v1.0.vpx` at SHA-256 `03451b7951242d204f9f79ab91f108d3c8aa203039f2ca867b24f4f47668c250`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `926e7a90d89602b003ac93757ee23c6ae916bb382112be28f82388381490bb7a`; that embedded stream is the runtime and causality authority. This is a WIDE-BODY table: exact playfield bounds are `left=0 top=0 right=1093 bottom=2162`, and every canonical coordinate is x/1093 and y/2162 rounded to at most six fractional places -- not the 952-wide divisor every other curated WPC game uses.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a Paper Capture OCR text layer that scrambles/duplicates table cells under `pdftotext -layout`. Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/indiana-jones-the-pinball-adventure-1993/manual-transcription.md`.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (idol motor angle, Path of Adventure linear tilt counter) or because the trough's own ball-stack class has no per-position object. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- The Path of Adventure insert lamps (71-75, 81-85) share one raw local-space Primitive coordinate because they are children of the tilting mini-playfield group; each is projected onto the playfield-fixed switch or trigger object at the same lane position instead of using that shared placeholder.
- gi060 and gi061 are Light objects that belong to no active GI collection (`GiTopSides`/`GiBotSides` are both declared empty in `collections.json`) and are excluded as orphaned table-modeling objects.
- GI addresses 0 (Top Playfield) and 1 (Bottom Playfield) use the retained table's own GITop/GIBumpers and GiBot emitter collections; every one of their 34 and 32 members has an individually transcribed and validated placement.

## Explicit projections

- pinmame.input.switch 81: Projected onto the retained "Ballrelease" kicker (trough exit / Ball Release coil position): cvpmTrough's own construction (.InitSwitches Array(86,85,84,83,82,81), .InitExit BallRelease,70,15) has no individual playfield object per ball position, only the shared exit kicker.
- pinmame.input.switch 82: Projected onto the retained "Ballrelease" kicker; see switch 81.
- pinmame.input.switch 83: Projected onto the retained "Ballrelease" kicker; see switch 81.
- pinmame.input.switch 84: Projected onto the retained "Ballrelease" kicker; see switch 81.
- pinmame.input.switch 85: Projected onto the retained "Ballrelease" kicker; see switch 81.
- pinmame.input.switch 86: Projected onto the retained "Ballrelease" kicker; see switch 81.
- pinmame.input.switch 87: Projected onto the retained "Ballrelease" kicker (trough exit): the retained script pulses this switch from SolBallRelease whenever bsTrough.Balls is nonzero (relationship.ball-release-top-trough-pulse), not from a distinct Top Trough playfield object.
- pinmame.input.switch 121: Projected onto the rotating idol figure (Primitive totem, table object center): the retained script's UpdateIdol_timer sets Controller.Switch(121/122/123) directly from a 360-degree motor-position counter (60-degree sextants), not from three separate playfield objects.
- pinmame.input.switch 122: Projected onto the rotating idol figure (Primitive totem, table object center); see switch 121.
- pinmame.input.switch 123: Projected onto the rotating idol figure (Primitive totem, table object center); see switch 121.
- pinmame.input.switch 124: Projected onto the tilting mini-playfield assembly (Primitive minipf, table object center): the retained script's POAMech (vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear, .AddSw 124,0,0) sets this switch from the mechanism's own 9-step linear position counter, not from a separate playfield sensor object.
- pinmame.input.switch 125: Projected onto the tilting mini-playfield assembly (Primitive minipf, table object center); see switch 124.
- pinmame.output.lamp 71: Projected onto the Mini Top Left switch/trigger object (table object center): the mini-playfield insert lamp has no distinct retained-table object -- the script drives it through `DisableLighting Li71on, 600,` against a Primitive that shares a single raw local coordinate with every other mini-playfield insert lamp because it is a child of the tilting mini-playfield group.
- pinmame.output.lamp 72: Projected onto the Mini Top Right switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 73: Projected onto the Mini Middle Top Left switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 74: Projected onto the Mini Middle Top Right switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 75: Projected onto the retained "EnterPoA" trigger, the Path of Adventure entrance sensor immediately behind the Top Post; the "Mini Top Arrow" insert marks the entrance and has no distinct lamp object of its own; see lamp 71.
- pinmame.output.lamp 81: Projected onto the Mini Middle Bottom Left switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 82: Projected onto the Mini Middle Bottom Right switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 83: Projected onto the Mini Bottom Left switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 84: Projected onto the Mini Bottom Right switch/trigger object (table object center); see lamp 71.
- pinmame.output.lamp 85: Projected onto the retained "ExitPoA" trigger, the Path of Adventure exit sensor; the "Mini Bottom Arrow" insert marks the exit and has no distinct lamp object of its own; see lamp 71.

## Counts

- Placements: 240
- Located input addresses: 65
- Located output bindings: 107
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 4
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `virtual` record: 16

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, public switch 71 (Captive Ball Front) and switches 121-123 (Wheel Position 1-3) are printed normally-closed opto interrupters per the manual's own board schematics that pinned PinMAME's ijGameData inverted-switch mask does not normalize, unlike their opto column neighbors (72/73 and 124/125 respectively) -- two unresolved polarity conflicts recorded as `conflict.captive-ball-front-opto-not-normalized` and `conflict.wheel-position-opto-not-normalized`. The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["polarity", "unresolved_conflicts"]` until a LibPinMAME harness trace against a legal ij_l7 ROM observes the true idle and transition public state of all four addresses.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool.manifest.json`, SHA-256 `438995cdc586b0ba83f6e683b9e0576530517f6e0a5afa86f2dd1236d5bbfb40`, 2027 files, 362116168 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `5a083e87ffc8aa0237d72b98848fa58d4450f848e25535e5ae4a945d6015c8f3`.
