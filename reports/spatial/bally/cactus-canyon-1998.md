# Cactus Canyon (Bally, 1998) spatial review

Status: validated. Every spatial dimension audited here is complete except two flasher addresses (24, 26) whose second documented bulb has no independently resolvable coordinate; the physical machine record stays `partial` at `machines/partial/bally/cactus-canyon-1998.json` for that reason alone -- no polarity conflict was found for this machine (see the opto sweep in the manual transcription).

The matching source is the retained known-working `Cactus Canyon (Bally 1998) VPW 1.0.2.vpx` at SHA-256 `2e93faec289ce517a30f7285187d9eedca4652417ea2744e381c04a2e94e371b`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `7b07f1492c5db71dd7acc33c8c5875cfbbe7a799092722b2372784149cd06313`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a fresh OCR text layer, so every printed table used here was extracted with `pdftotext -layout` and then confirmed against the rendered page image; the transcription in `external:pinmame-review-artifacts/cactus-canyon-1998/manual-transcription.md` is the source of record whenever OCR and the rendered page disagree.
- The opto sweep checked both manual cues (matrix shading and a populated Opto Assembly Part Number with a blank Switch Part Number, cross-referenced against the board-assembly pages) column by column against ccGameData's inverted-switch mask and found full agreement: every physically normally-closed opto switch (31-37, 41-42, 71, 77, 78, plus the Fliptronic 112/114 button optos handled by WPC-95's own hardware inversion) is normalized by the emulator. No `conflict.*-opto-not-normalized` entry was needed.
- Switches 71/72 (Train Encoder/Home) and 77/78 (Mine Home/Encoder) have no dedicated playfield trigger object because the retained script's PROC=0 (physical ROM) path either drives them from a Timer object tied to mechanism motion (71) or does not set them at all (72, 77, 78 -- only the PROC=1 community P-ROC path does). All four are documented projections onto the Train or Mine mechanism's own retained table object.
- GI strings 0-2 use the retained table's LeftGI/RightGI/TopGI(+TopGI2) emitter collections, matching the retained script's `UpdateGI` dispatch exactly; each collection's members were clustered within 25px to collapse render-doubled Light objects into one placement per physical bulb. GI strings 3 and 4 are backbox insert-panel/cabinet circuits and take a controlled `cabinet_or_service` record.
- Solenoids 41/42 are PinMAME's LPDC mirror of the physical train-motor drive lines 37/38 and are declared virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 71: Projected onto the Train mechanism's own retained table objects (Primitives Train and Train1, table object center): the retained script's sw71 object is a VPX Timer, not a Hit trigger, and its sw71_Timer handler pulses public switch 71 once per encoder step while the Train primitive is in motion ("Dozer - Encoder Pulse which runs with Train Mech."); there is no separate playfield sensor object.
- Switch 72: Projected onto the Train mechanism's own retained table object (Primitive Train, table object center): the retained script's PROC=0 TrainF/TrainB handlers never set Controller.Switch(72) at all (only the PROC=1 Polly_Timer path does), so there is no VPX object of any kind bound to this address under the physical ROM's normal operating path; the manual and PinMAME's own switch matrix are the only evidence this switch exists, at the position of the mechanism whose motion it senses.
- Switch 77: Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): like switch 72, the retained script's PROC=0 MoveMine/MineTimer_Timer handlers never set Controller.Switch(77) (only the PROC=1 Sw15_Timer path does); the manual and PinMAME are the only evidence for this address, recorded at the position of the mechanism it senses.
- Switch 78: Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): the retained script's PROC=0 path has no object bound to public switch 78 either (only the PROC=1 sw15b_Timer path pulses it, "Dozer - Encoder Pulse which runs with Mine Mech."); recorded at the position of the mechanism it senses.

## Counts

- Placements: 184
- Located input addresses: 50
- Located output bindings: 97
- Inputs with a controlled `cabinet_or_service` record: 12
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 15
- Outputs with a controlled `cabinet_or_service` record: 3
- Outputs with a controlled `unused` record: 7
- Outputs with a controlled `virtual` record: 26

## Promotion decision

No switch-polarity conflict, unnamed required address, or missing physical/controller variant remains for this machine, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, flasher addresses 24 and 26 each document two fitted bulbs (playfield plus insert-panel) on the printed Solenoid/Flasher Locations page, and the retained table's Light-object evidence for both addresses cannot be split into two independently resolvable coordinates -- inventing a second coordinate is explicitly forbidden, so each keeps exactly one placement. `coverage.missing` is `["spatial_placement"]` and `coverage.dimensions.spatial_placement = "candidate"`, so promotion to `author_ready` is refused; the record stays `partial` until a second distinguishable insert-panel bulb position is found (a higher-resolution table revision, a playfield photograph, or a runtime harness trace that separately drives the two physical lamps).

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/cactus-canyon-1998/extracted-vpxtool.manifest.json`, SHA-256 `a0f7c251d961e72d588951496cbafd73ff9836475c5bc006cc44e63906aaa8bb`, 1268 files, 139765398 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `68119b41c5bc5cada849c64ea0fc105262394eaaa71f0f5704f4c43b1efe2904`.
- Retained VPX geometry dump of every named object used by this definition, SHA-256 `2f4ae8806e56d6ab75b82d24481efaf28f8bb18e601981e029c2adc9837af8aa`.
