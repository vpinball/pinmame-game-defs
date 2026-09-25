# Cactus Canyon (Bally, 1998) spatial review

Status: validated. Every spatial dimension audited here is complete, and the physical machine record is `author_ready` at `machines/author-ready/bally/cactus-canyon-1998.json` -- no polarity conflict was found for this machine (see the opto sweep in the manual transcription).

The matching source is the retained known-working `Cactus Canyon (Bally 1998) VPW 1.0.2.vpx` at SHA-256 `2e93faec289ce517a30f7285187d9eedca4652417ea2744e381c04a2e94e371b`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `7b07f1492c5db71dd7acc33c8c5875cfbbe7a799092722b2372784149cd06313`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`, and every canonical coordinate is x/952 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a fresh OCR text layer, so every printed table used here was extracted with `pdftotext -layout` and then confirmed against the rendered page image; the transcription in `external:pinmame-review-artifacts/cactus-canyon-1998/manual-transcription.md` is the source of record whenever OCR and the rendered page disagree.
- The opto sweep checked both manual cues (matrix shading and a populated Opto Assembly Part Number with a blank Switch Part Number, cross-referenced against the board-assembly pages) column by column against ccGameData's inverted-switch mask and found full agreement: every physically normally-closed opto switch (31-37, 41-42, 71, 77, 78, plus the Fliptronic 112/114 button optos handled by WPC-95's own hardware inversion) is normalized by the emulator. No `conflict.*-opto-not-normalized` entry was needed.
- Switches 71/72 (Train Encoder/Home) and 77/78 (Mine Home/Encoder) have no dedicated playfield trigger object because on the physical-ROM (PROC=0) path the retained script registers VPinMAME cvpmMech objects for the train (home 72 at step 0, encoder 71 for 3 of every 14 of 613 steps) and the mine sign (home 77 at steps 0-1, encoder 78 for 2 of every 8 of 49 steps), so PinMAME drives them from mechanism position. All four are documented projections onto the Train or Mine mechanism's own retained table object.
- GI strings 0-2 use the retained table's LeftGI/RightGI/TopGI(+TopGI2) emitter collections, matching the retained script's `UpdateGI` dispatch exactly; each collection's members were clustered within 25px to collapse render-doubled Light objects into one placement per physical bulb, and each placement is the smallest-falloff-radius member's own center, never a cluster centroid. TopGI2 (light006, light007, light034) is switched on only when the table's VRRoom option is 0, so its members are desktop/cabinet-view duplicates of three TopGI bulbs; where one of them is the smaller-radius member of its cluster it carries that bulb's placement. GI strings 3 and 4 are backbox insert-panel/cabinet circuits and take a controlled `cabinet_or_service` record.
- Flasher emitters use the fitted playfield bulb's own retained object: the smallest-radius bulb Light of the address's script-bound collection, the Flasherbase primitive of the three Flupper domes (25, 27, 28), or for flasher 26 the spotlight primitive SpotP at the end of the printed 2-37 leader, the script-bound saloon glow being a visual effect. The second bulb of 24, 26, 27 and 28 sits on the backbox insert panel and has no playfield coordinate, the same treatment as the author-ready WPC-95 records. The f27r*/f28r* back-wall `F_refl` reflection sprites that an earlier pass placed for 27 and 28, and an x coordinate for 24 that matched no object, were replaced.
- Solenoids 41/42 are PinMAME's LPDC mirror of the physical train-motor drive lines 37/38 and are declared virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 71: Projected onto the Train mechanism's own retained table objects (Primitives Train and Train1, table object center): the retained script's Table1_Init registers a VPinMAME cvpmMech on the physical-ROM (PROC=0) path (script.vbs lines 191-203): Sol1 = 38 (forward), Sol2 = 37 (reverse), MType vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear, Length 570, Steps 613, .AddSw 72, 0, 0 (Train Home asserted at step 0 only) and .AddPulseSw 71, 14, 3 (Train Encoder asserted for 3 of every 14 steps, core.vbs mapping it to PinMAME's pulsed mech switch). PinMAME therefore drives 71 and 72 from the mechanism position; the sw71 Timer object is switched on only in the PROC=1 TrainF_PROC/TrainB_PROC handlers, which are out of scope; there is no separate playfield sensor object.
- Switch 72: Projected onto the Train mechanism's own retained table object (Primitive Train, table object center): the retained script's Table1_Init registers a VPinMAME cvpmMech on the physical-ROM (PROC=0) path (script.vbs lines 191-203): Sol1 = 38 (forward), Sol2 = 37 (reverse), MType vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear, Length 570, Steps 613, .AddSw 72, 0, 0 (Train Home asserted at step 0 only) and .AddPulseSw 71, 14, 3 (Train Encoder asserted for 3 of every 14 steps, core.vbs mapping it to PinMAME's pulsed mech switch). PinMAME therefore drives 71 and 72 from the mechanism position; the sw71 Timer object is switched on only in the PROC=1 TrainF_PROC/TrainB_PROC handlers, which are out of scope; recorded at the position of the mechanism whose travel it senses.
- Switch 77: Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): the retained script's Table1_Init registers a VPinMAME cvpmMech on the physical-ROM (PROC=0) path (script.vbs lines 176-187): Sol1 = 17, MType vpmMechOneSol + vpmMechReverse + vpmMechLinear, Length 100, Steps 49, .AddSw 77, 0, 1 (Mine Home asserted at steps 0-1) and .AddPulseSw 78, 8, 2 (Mine Encoder asserted for 2 of every 8 steps). PinMAME therefore drives 77 and 78 from the mechanism position; recorded at the position of the mechanism it senses.
- Switch 78: Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): the retained script's Table1_Init registers a VPinMAME cvpmMech on the physical-ROM (PROC=0) path (script.vbs lines 176-187): Sol1 = 17, MType vpmMechOneSol + vpmMechReverse + vpmMechLinear, Length 100, Steps 49, .AddSw 77, 0, 1 (Mine Home asserted at steps 0-1) and .AddPulseSw 78, 8, 2 (Mine Encoder asserted for 2 of every 8 steps). PinMAME therefore drives 77 and 78 from the mechanism position; recorded at the position of the mechanism it senses.

## Counts

- Placements: 182
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

No switch-polarity conflict, unnamed required address, or missing physical/controller variant remains for this machine, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Every fitted playfield device carries a placement taken from its own retained object or a documented projection onto its own mechanism, every backbox, cabinet, virtual and unused address carries a controlled `not_applicable` record, and insert-panel flasher bulbs are recorded as backbox hardware without a playfield coordinate. The record carries no conflict and is promoted to `author_ready`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/cactus-canyon-1998/extracted-vpxtool.manifest.json`, SHA-256 `a0f7c251d961e72d588951496cbafd73ff9836475c5bc006cc44e63906aaa8bb`, 1268 files, 139765398 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `68119b41c5bc5cada849c64ea0fc105262394eaaa71f0f5704f4c43b1efe2904`.
- Retained VPX geometry dump of every named object used by this definition, SHA-256 `2f4ae8806e56d6ab75b82d24481efaf28f8bb18e601981e029c2adc9837af8aa`.
