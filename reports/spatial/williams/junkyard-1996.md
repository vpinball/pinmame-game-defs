# Junk Yard (Williams, 1996) spatial review

Status: validated spatial-report format; spatial coverage itself is `candidate`. The definition remains `partial` at `machines/partial/williams/junkyard-1996.json` because the past-crane opto polarity conflict is unresolved and several mechanism-internal sensors carry documented projections.

The matching source is the retained known-working `Junk Yard (Williams 1996).vpx` (v1.3 by mfuegemann) at SHA-256 `8ff2c1c8ae3457a4b88ff2207bc506d07435b049343301ded4dbf8e855bef07f`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `b583aed396fea3cf6e2f862fdb51989aa01a99e624bbae8b30e8aeba7eeb4033`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual (146 pages, 16-50052-101 FINAL) carries a usable OCR text layer but every printed table used here was read from 200 dpi renders and transcribed (by a vision-capable model worker) into `evidence/excerpts/williams.junkyard.1996/`, cross-checked across the repeated copies.
- The trough and lock/scoop multi-position sensors have no dedicated playfield trigger objects because the retained script's cvpmBallStack helpers model ball sensing purely as an internal switch array. Those addresses are explicit documented projections onto the real kicker object that carries the mechanism's exit/entry point.
- Switch 44 (Past Crane) is the single polarity disagreement: opto-constructed per the manual but not normalized by jyGameData's mask. Recorded as a first-class unresolved conflict.
- GI addresses 2-4 and flasher/insert-panel bulbs are backbox/cabinet circuits with controlled `not_applicable` spatial records.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable`.

## Counts

- Placements: 150
- Located input addresses: 48
- Located output bindings: 72
- Unresolved input addresses: [28, 42]
- Unresolved output bindings: 15, 19, 20, 21, 23, 24, 25, 26, 27, 28

## Promotion decision

Junk Yard is a deterministic partial. The past-crane opto polarity question and the trough/crane projections must be resolved before promotion; a LibPinMAME harness trace of the public idle state of switch 44 on a legal jy_11/jy_12 ROM is the concrete next step. Before any promotion, a vision-capable curator must also visually re-check the six manual transcriptions (recorded `reviewed: false` / `method: model`) against the rendered pages, since the manual-derived device labels and wiring rest on those unchecked transcriptions.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/junkyard-1996/extracted-vpxtool.manifest.json`, SHA-256 `bb9b127b90d2e892f18707933288e15a080819e7d27cefaf787ee04379adbdbc`, 1008 files, 299118752 bytes.
- Six manual transcriptions (switch matrix, switch locations, lamp matrix, lamp locations, solenoid/flasher table, solenoid locations) under `evidence/excerpts/williams.junkyard.1996/`.
