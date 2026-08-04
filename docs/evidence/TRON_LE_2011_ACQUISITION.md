# TRON: Legacy Limited Edition (Stern 2011) evidence inventory

This is the acquisition and extraction record for `stern.tron-legacy-limited-edition.2011`. No VPX/VPT source, script, manual, extraction, or cache artifact was deleted.

## Identity and acquisition order

The required source search order was followed. These portable logical roots name the searched locations without recording a host-specific filesystem mapping:

1. `logical:visual-pinball/Tables`
2. `logical:visual-pinball/Tables Archive`
3. VPU/VPF was not queried because an exact physical LE was already identified in the first location.

Selected exact table:

- Original filename: `VR Room Tron Legacy (Limited Edition) (Stern 2011) V11.vpx`
- Source size: 133,521,408 bytes
- Source and retained-cache SHA-256: `56ad2f5318c33dbc12f3aa2515a41d819eb8b95b2ffcd94ebe1044cec4281ae5`
- `vpxtool`: `git:v0.33.3`
- Identity: VPX Table Name `Tron Legacy LE`, IPDB `5707`, ROM name `trn_174h`, description explicitly identifies Disney TRON Legacy LE / Stern 2011.
- Retained exact cache: `external:pinmame-vpx-sources/stern/tron-legacy-limited-edition-2011/VR Room Tron Legacy (Limited Edition) (Stern 2011) V11.vpx`

Rejected or non-selected local candidates:

- `Tron Legacy (Stern 2011) (G5K 2.2).vpx` — exact LE identity, retained as a comparison candidate; SHA-256 `bb82ab027d4c75211a91df1ae0051580dba5c44b07512e469f7e1379e22eeee0`.
- `Tron Legacy (Stern 2011) VPW Mod 0.24.vpx` — exact LE identity, retained as a comparison candidate; SHA-256 `ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4`.
- `Tron Legacy (Stern 2011) (1.6, SSF, Lightmod 1.2, NPC).vpx` — archive duplicate of the G5K candidate, retained by source hash.
- `TRON Classic (Original 2018) Mod v1.02.vpx` — rejected re-theme; ROM name `panther7`, SHA-256 `a9c5740b540cc3f4152fe389edbff0ffe059e900de54fbead14f2600cb2591dc`.
- Pro/non-LE candidates were not promoted into this definition.

## Retained extraction and semantic evidence

Under `external:pinmame-vpx-sources/stern/tron-legacy-limited-edition-2011/`:

- `vpxtool-extract-v11/` — full read-only `vpxtool extract` tree, including `script.vbs`, `gamedata.json`, and game-item JSON.
- `tron-legacy-le-v11.vbs` — extracted script, SHA-256 `5e0a66c21d73e540738f6dfbcd966944c4269c3c0b17545b0cf1c21543c9ecec`.
- `candidate-scripts/` — extracted scripts from the selected V11, G5K 2.2, and VPW 0.24 candidates for comparison.

Controller semantics use the pinned known-working script `vpx.tron-legacy-le-vpm-1.1.4`, revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc`. The official Stern manual is physical truth: `Tron-Manual.pdf`, external SHA-256 `1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84`; LE switch/coils/lamps tables are pages 55/57/59 and their location maps are pages 56/58/60. Those pages were rendered and visually inspected at 150 and 300 DPI because the scan has no usable text layer.

The runtime boot/start evidence remains under `evidence/runtime/sam/tron-legacy-limited-edition-boot-start.json`, with raw run SHA-256 `92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f` and external ROM archive SHA-256 `7ae5392a3bf6f9a7d282bf3ca002eea00a84ffd8cf39ff9af2e77a75e0eac44b`.

## Spatial evidence and fail-closed boundaries

The retained candidate report is `evidence/vpx/tron-legacy-limited-edition-2011-v11-spatial-candidates.json`, SHA-256 `318297fb178098929d62078075f891ee301067cff58ad778f683b577f83b8ff4`. It contains 493 direct playfield candidate centers in the exact table frame, including the typed Primitive positions and Wall drag-point centroids used by the promoted definition. The deterministic LE curator promotes only script/manual-reconciled devices into canonical placements, using x left-to-right and y rear/backglass-to-apron.

The preserved Q19/Q25 source conflict is concrete: the official Stern manual (`manual.tron-legacy-pro-le.2011`, PDF page 57) maps Q19 to `FLASH: RIGHT DOMES (X2)` and Q25 to `FLASH: LEFT DOMES (X2)`, opposite the selected known-working V11 embedded script. V11 maps Q19 to `setlampmod 125`, whose LampMod 125 drives `Flasher5`/`Flasher6` left-dome anchors, and Q25 to `setlampMod 119`, whose LampMod 119 drives `Flasher1`/`Flasher2` right-dome anchors. The comparison VPW Mod 0.24 revision (`candidate-scripts/vpw-0.24.vbs`, script SHA-256 `ecea74df1775bd39cfd8838955adfefb544b5907d345223847369710fc4dac7d`; candidate VPX SHA-256 `ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4`) maps Q19 to its right-blue `Flasher5`/`Flasher6` pair and Q25 to its left-yellow `Flasher3`/`Flasher4` pair. The retained V11 embedded script remains the controller/behavior tie-breaker; the disagreement is preserved rather than reported as concordant.

Individual matrix switches, coils, lamps, flashers, GI emitters, RGB ramp multiplicities, moving assemblies, slingshot projections, trough contacts, EOS contacts, cabinet/service N/A records, and virtual/unused outputs are all retained in the author-ready definition. The VPX's render helpers and reflective/material objects are excluded. Where an exact table models an assembly rather than an internal physical contact, the definition keeps the controller device distinct and discloses the shared or manual-map regional anchor; it does not invent helper geometry.

Deterministic generator: `tools/curate_tron.py` writes the Pro partial/runtime evidence and delegates LE promotion to `tools/curate_tron_le_spatial.py`. The latter reads only the retained candidate report and pinned source hashes. Repository validation, focused/full tests, `vpxtool verify`, and regeneration hash checks are required before review.
