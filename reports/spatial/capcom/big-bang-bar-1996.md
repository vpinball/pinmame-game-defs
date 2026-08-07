# Big Bang Bar (Capcom, 1996) spatial review

Status: validated. This audit is complete for every address it covers, but the physical machine record itself remains `partial` at `machines/partial/capcom/big-bang-bar-1996.json` because of unresolved conflicts and output-semantics gaps outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Big Bang Bar (Capcom 1996) VPW v1.0.vpx` at SHA-256 `7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5`. The retained extraction produced the embedded script at SHA-256 `db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Capcom operators manual and its companion schematic set are the physical inventory, quantity, polarity, wiring, and device-identity authority (the schematic's own per-device "DEVICE # & DESCRIPTION" table on sheet 7 is the single most authoritative solenoid source found); pinned PinMAME source owns controller topology and per-game hardware metadata; the retained table supplies geometry.
- The manual is an Adobe Paper Capture OCR'd scan whose text layer is unreliable on dense multi-column tables; every printed table used here was read from rendered page images at 200-600 dpi and transcribed into `external:pinmame-review-artifacts/big-bang-bar/manual-transcription.md` and its companion solenoid/schematic document.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (the Alien rotating mechanism's 32-step motor counter) or reuses a table object that also serves another role (kickers, slingshot walls, bumpers). Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- Two Light objects (lamp addresses 2 and 62) sit outside the retained table's 0..1 normalized playfield bounds and are excluded as a table-modeling anomaly.
- Three used lamp addresses (3, 38, 125) and two solenoid addresses' mechanism geometry (14, 15) have no resolvable coordinate in the retained table; their `spatial` key is omitted entirely rather than an invented status or coordinate.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 25: Projected onto the Spinner table object's own center (Spinner.sw25); a physical spinner has no separate fixed sensor position.
- Switch 33: Projected onto the LeftFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolLFlipper with no separate sensor object.
- Switch 34: Projected onto the RightFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolRFlipper with no separate sensor object.
- Switch 35: Projected onto the same Kicker object as the Outhole coil (solenoid 1): the manual's Switch Locations table names Ref.35 "Outhole" and the retained script kicks the ball resting on this object from Sub SolTrough.
- Switch 41: Projected onto the Wall.LeftSlingShot object's own drag-point centroid; resolved via the retained script's LeftSlingShot_Slingshot event sub rather than a differently-named sw41 object.
- Switch 42: Projected onto the Wall.RightSlingShot object's own drag-point centroid; resolved via the retained script's RightSlingShot_Slingshot event sub rather than a differently-named sw42 object.
- Switch 54: Projected onto the Bumper2 table object's own center; resolved via the retained script's Bumper2_Hit event sub, which pulses this switch.
- Switch 55: Projected onto the Bumper3 table object's own center; resolved via the retained script's Bumper3_Hit event sub.
- Switch 56: Projected onto the Bumper1 table object's own center; resolved via the retained script's Bumper1_Hit event sub.
- Switch 57: Projected onto the rotating Alien mechanism's own anchor (Primitive Alien1_BM_Lit_Room): the retained script's ALockTimer_timer reads a single 0-31 motor-position counter and toggles this one opto through a repeating home/quarter/half/three-quarter-turn notch pattern, not a fixed playfield sensor object -- the same pattern established for Monster Bash's Dracula-position optos.
- Switch 68: Projected onto the RightFlipper table object's own center, the same object switch 34 projects onto: the retained script sets both switches together inside Sub SolRFlipper with no separate Upper Right Flipper EOS sensor object modeled.

## Counts

- Placements: 194
- Located input addresses: 56
- Located output bindings: 131
- Unresolved input addresses (used, no coordinate): 0
- Unresolved output bindings (used, no coordinate): 10
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `unused` record: 8
- Inputs with a controlled `virtual` record: 2
- Outputs with a controlled `cabinet_or_service` record: 2
- Outputs with a controlled `no_physical_device` record: 3
- Outputs with a controlled `unused` record: 24
- Outputs with a controlled `virtual` record: 17

## Promotion decision

No authoring-critical placement question remains silently unresolved: every address this audit covers is either a validated placement, a controlled `not_applicable` record, or an explicitly named unresolved gap. However, four first-class conflicts remain open (flipper mirror address left/right naming, the address-35 Eject Hole mirror mislabeled as an upper-left flipper, solenoid 22's shared bulb-vs-coil device construction, and the ramp-diverter geometry inconsistency), and three output devices (the inferred Bumper 1/2/3 solenoid correspondence) rest on ordering evidence rather than a confirmed wiring page. The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["polarity", "output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts", "recreation_notes"]`. This curation pass was also run without the mandatory independent high-tier cross-provider review described in `docs/INSTRUCTIONS.md`, which alone would keep `recreation_notes` in `coverage.missing` even if every other gap were closed.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/capcom/big-bang-bar-1996/extracted-vpxtool.manifest.json`, SHA-256 `8b1b7c6f35b98b0fecf1d88ac0746d81599fd8006189d58998c255de62fc2e90`, 2874 files, 1091052346 bytes.
- Human transcription of every printed switch/lamp table, SHA-256 `3e503420d32c307f409edaa57c80d6f4bfa9f01d90cd0e47dbc6ddc755188994`, and its companion solenoid/schematic transcription, SHA-256 `b996714bd9cd3811481ab0eb0ccce071c3d019819844eaffffaf5318e28c4bd5`.
- VPX object-geometry notes, SHA-256 `e1339971328d98e365b6574733b08f8dc1849814806bb2973019482c93468ac5`.
