# Medieval Madness (Williams, 1997) spatial review

Status: validated and promoted to `machines/author-ready/williams/medieval-madness-1997.json`.

The matching source is the retained known-working `Medieval Madness (Williams 1997) VPW v1.0.vpx` at SHA-256 `9a05a555d03aca3d48d73b3e6566220b27fde46aa5d2517a08faacdbc58bcab9`. A fresh `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `cdc5590888d810a44b772ec327789362cd27dd7a6c58870bc148b2d87a0f90f8`; that embedded stream is the runtime and causality authority. `vpxtool` established exact playfield bounds `left=0 top=0 right=952.941 bottom=2164.706`, and every canonical coordinate is x/952.941 and y/2164.706 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- All four retained manual PDFs are image-only scans. Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/medieval-madness-1997/manual-transcription.md`; the retained OCR text is a search index only.
- Direct table object centres cover every visible sensor, effect, and emitter. Lightmap (`LM_*`), baked-mesh (`BM_*`), virtual-reality (`VR_*`, `VRBG*`), ball-routing helper (`ramptrigger*`), physics-blocker, and standup render primitives are excluded from physical multiplicity.
- Flasher addresses 17-20 drive a playfield flasher plus a separate backbox insert-panel flasher; only the playfield bulb receives a coordinate and the physical quantity stays two. Addresses 21-25 have two playfield emitters each, and the manual's Note 2 back-panel bulbs for 22 and 25 are the rear-edge pair in the table.
- GI strings 0-2 use the table's GIB/GIM/GIT emitter arrays; the manual prints no per-string bulb count, so the physical quantity is taken from those arrays. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- Solenoids 33-36 are troll actuators wired to Fliptronic upper-flipper circuits, and solenoid 41 is PinMAME's mirror of LPDC output 37. The mirror is declared virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 31: Projected onto the trough-exit ball position: the retained script's SolBallRelease pulses switch 31 and kicks the same trough-exit ball, and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.
- Switch 56: Projected onto the retained drawbridge door assembly; the manual marks switch 56 as a hidden (dashed) position inside the drawbridge mechanism.
- Switch 57: Projected onto the retained drawbridge door assembly; the manual marks switch 57 as a hidden (dashed) position inside the drawbridge mechanism.
- Switch 74: Projected onto the left troll strike surface; the physical position switch is under the playfield inside troll assembly A-22034.
- Switch 75: Projected onto the right troll strike surface; the physical position switch is under the playfield inside troll assembly A-22034.

## Counts

- Placements: 181
- Located input addresses: 44
- Located output bindings: 101
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 18
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `virtual` record: 13

## Promotion decision

No authoring-critical placement, polarity, quantity, or semantic question remains unresolved, the definition carries no conflict records, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Promotion to `author_ready` is therefore justified.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/medieval-madness-1997/extracted-vpxtool.manifest.json`, SHA-256 `2f5a08bb9ce459a90934b3999e6ee96b15b4885f5a07dee8681c1f2b3ca50442`, 2793 files, 1073881024 bytes.
- Candidate geometry `external:pinmame-review-artifacts/medieval-madness-1997/vpx-spatial-candidates.json`.
- Rendered manual pages `external:pinmame-manuals/rendered/williams.medieval-madness.1997/`; the 24 pages that decided a canonical value are listed with their SHA-256 in the companion JSON report, so an empty or substituted render cache is an audit failure rather than an assumed source.
- Human transcription of every printed table read from those pages, SHA-256 `b0905ec59747532ca146ba4e0a6e66b384f28ad2528617b29bfed64221f9d4d2`.
- Harness runs and DMD captures `external:pinmame-review-artifacts/medieval-madness-1997/harness/`.
