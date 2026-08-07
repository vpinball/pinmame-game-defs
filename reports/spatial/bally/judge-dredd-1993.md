# Judge Dredd (Bally, 1993) spatial review

Status: partial. The physical machine record lives at `machines/partial/bally/judge-dredd-1993.json` and stays `partial`: five addresses have no placement and four unresolved conflicts remain. See the promotion decision below.

The matching source is the retained known-working `Judge Dredd (Bally 1993) VPW v1.1.vpx` at SHA-256 `61f6844d947cc788f81a9ed91e108bd800bd3172abd125ad2ecfb51f6d55be06`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `817427aed72dc68a5e96a6a50614e8ab822d9d6d98c6033757ef245eda5b6d32`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=1093 bottom=2162` — this is a wide-body Superpin, so every canonical coordinate is x/1093 and y/2162, rounded to at most six fractional places, and the 952 divisor that standard-width WPC games use would stretch every x by about 15 percent.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries an Adobe Paper Capture OCR layer, but its output for every multi-column table in Sections 2 and 3 is scrambled. Every printed table used here was read from 300-600 dpi renders and transcribed by hand into `evidence/excerpts/bally.judge-dredd.1993/`.
- Which switch-matrix cells carry the "Opto, Typically Closed" halftone was settled by a mechanical connected-component sweep of all 64 cells at 600 dpi, not by eye, and the result was cross-checked against the switch-locations parts list's independent LED/phototransistor disclosure. The two agree cell for cell.
- Lamp bindings come from the retained script's `Lampz.MassAssign` table, which assigns the primary `L<nn>` Light plus co-located glow and flare doubles per address. Only the primary object supplies a coordinate. Addresses 38, 87 and 88 have no assignment at all, matching the manual, which prints them as cabinet button lamps with a blank bulb number.
- Lamp 61 is printed `Extra Ball (2)` and drawn twice in the manual's location diagram; the retained table models it as two Lights far apart on the playfield, so it takes two placements. Lamp 83 is also printed with a quantity of two, but its single retained Light is the midpoint of the two printed positions and is therefore excluded rather than used.
- Flasher placements match the manual's own playfield bulb counts address by address: one each for 17-20, two each for 21, 22, 24, 25 and 27, one each for 23 and 26, and none for 28, which the printed table gives blank Playfield columns and three backbox bulbs.
- Several switches have no dedicated playfield object because the retained script and pinned PinMAME both derive their public state from a mechanism's own continuous position (the globe rotation counter, the crane arm counter) or from another device's event (the trough eject). Those are explicit documented projections onto the real table object that carries the underlying mechanism, never a centroid of other devices.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 18: Three physical standup targets share the one matrix address. The manual's own location diagram draws the 18 callout three times against a single `A-14227-15` part number, and the retained script instantiates three separate hit targets (sw18, sw18a, sw18b) that all report the same public switch. Each of the three retained objects supplies one placement rather than one being chosen or the three being averaged.
- Switch 61: Projected onto the rotating Deadworld disc (Primitive DW_Disc, table object center). The manual marks item 61 `*Not Shown` in the parts list yet draws its callout inside the disc outline at the hub, and pinned PinMAME reads it as the ball-resting-on-the-globe state in jd_stateDef's "Planet" step rather than from a fixed playfield sensor.
- Switch 71: Projected onto the crane assembly (Primitive Crane, table object center). The manual marks item 71 `†Located Under Playfield`, and the retained script asserts public switch 71 from the crane arm's own rotation angle inside Crane_X_Timer rather than from a playfield trigger.
- Switch 77: Projected onto the rotating Deadworld disc (Primitive DW_Disc, table object center). The manual marks item 77 `*Not Shown` and draws its callout at the disc hub beside 61; the retained script asserts public switch 77 when the disc's own rotation angle brings a loaded slot under the crane (FWTimer_Timer), and pinned PinMAME's jd_handleMech does the same from a 0-100 globe-position counter. It is an angular position sensor, not a playfield location.
- Switch 87: Projected onto the trough eject position (Kicker sw86). The retained script's trough handler kicks the ball resting at Trough 6 and pulses public switch 87 in the same event (Sub JDTrough: sw86.kick 37,30 then vpmTimer.PulseSw 87), and the manual's location diagram draws 87 immediately outboard of 86 at the eject end of the trough.
- Solenoid 1: Projected onto the crane assembly (Primitive Crane, table object center). The Globe Magnet is carried on the end of the crane arm and has no fixed playfield position; the manual draws its callout on the crane assembly at the left of the globe.
- Solenoid 4: Projected onto the crane assembly (Primitive Crane, table object center); the Globe Arm motor drives that assembly and the manual draws its callout on it. Same anchor as solenoid 1, which is mounted on the same arm.
- Solenoid 5: Projected onto the "J" drop target (Primitive sw54prim), the left-hand end of the five-target JUDGE bank that this coil resets. The manual marks item 05 `†Located Under Playfield` and draws its callout at that end of the bank. The coil is part of the bank's own mechanism; it is not placed at a centroid of the five targets.
- Solenoid 10: Projected onto the "D" drop target (Primitive sw56prim), the single target this coil pulls down. The manual marks item 10 `†Located Under Playfield` and the retained script's TripDrop handler drops exactly that target.
- Solenoid 13: Projected onto the trough eject position (Kicker sw86), the ball position this coil ejects from; the manual draws item 13 at the eject end of the trough.

## Counts

- Placements: 162
- Located input addresses: 45
- Located output bindings: 96
- Inputs with a controlled `cabinet_or_service` record: 21
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `internal_nonvisual` record: 4
- Inputs with a controlled `unused` record: 6
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 2
- Outputs with a controlled `virtual` record: 15
- Inputs with no spatial record at all: 3
- Outputs with no spatial record at all: 2

## Unresolved

- pinmame.output.lamp 83: Two printed bulbs, and the only retained object is their midpoint.
- pinmame.output.gi 4: No playfield emitter in the retained table's collection for this address.
- pinmame.input.switch 28: Fitment unresolved; see conflict.l1-era-switch-fitment.
- pinmame.input.switch 32: Fitment unresolved; see conflict.l1-era-switch-fitment.
- pinmame.input.switch 65: Fitment unresolved; see conflict.l1-era-switch-fitment.

## Promotion decision

Promotion to `author_ready` is refused. Five addresses have no placement — lamp 83, GI 4 and switch positions 28, 32 and 65 — and the definition carries four unresolved conflicts: three printed opto cells that pinned PinMAME does not normalize, five drop-target switches that it does normalize with no opto evidence behind them, three switch addresses whose fitment the manual contradicts itself about, and a general-illumination string order on which the manual and the retained known-working script disagree outright. `coverage.status` stays `partial` with `coverage.missing = ["polarity", "spatial_placement", "unresolved_conflicts"]`. The cheapest route to closing three of the four is a LibPinMAME gameplay-harness trace against a legal jd_l1 and jd_l7 ROM: the idle public state of 61/71/77 and 54-58 settles the two polarity conflicts, driving each GI address in turn settles the string order, and comparing what the two ROMs read at 28, 32 and 65 settles the fitment question.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/judge-dredd-1993/extracted-vpxtool.manifest.json`, SHA-256 `8eaa44e94e08384f9fd0f77b1d237539d73f2c79bb716fa51eb78197268d81d2`, 1840 files, 419225172 bytes.
- Manual reading record, SHA-256 `78b62d0f8a3a2b1b4a2b1e29bdcbd0aa2e3b6c76eb5a2c19e6a1cd9a4dfd8e01`, with the rendered page cache at `external:pinmame-manuals/rendered/bally.judge-dredd.1993/`.
