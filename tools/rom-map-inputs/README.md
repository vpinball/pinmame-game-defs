# ROM-map inputs

Bulk tables that `tools/curate_rom_maps.py` reads. Each was transcribed or deterministically extracted from contributor evidence retained outside Git, and the curator pins each one by SHA-256. Edit a table only together with its pin and its source record.

| File | Transcribed from | Retained at (working root) |
| --- | --- | --- |
| `lethal-weapon-3-1992.sound-commands.json` | `docs/TR_SOUND_MAP.csv`, the Total Recall project's own sound-command map and labels | `review-artifacts/lethal-weapon-3-rom-state-2026-10-03/` |
| `lethal-weapon-3-1992.sound-observations.json` | command membership extracted from the 14 retained `rec/*/meta.json` sound streams; each run carries its ROM, path and manifest-verified metadata hash | `review-artifacts/lethal-weapon-3-rom-state-2026-10-03/` |
| `attack-from-mars-1995.dcs-commands.json` | the DCS opcode table in `knowledge/bally/attack-from-mars-1995.md`: contributor runtime annotations and group only | (in this repository) |
| `attack-from-mars-1995.game-adjustments.json` | `rammap/afm_adjustments_named.json`, read out of the ROM's own adjustment descriptors and menu strings | `review-artifacts/attack-from-mars-rom-state-2026-09-05/` |
| `attack-from-mars-1995.mode-replay.json` | `rammap/afm_modes.json`, the contributor's mode-replay recipes | `review-artifacts/attack-from-mars-rom-state-2026-09-05/` |

The AFM table deliberately leaves out the sample file names from the community altsound package that the knowledge note's table quotes. That package is not retained, and its author and redistribution terms are not established. None of these tables copies Pinball Memory Maps content, so they stay under this repository's MIT licence.

Reproduce the LW3 observations with `python -B tools/curate_rom_maps.py --extract-lw3-sound-observations <evidence-root>`. The extractor verifies the exact retained `MANIFEST.sha256`, its recording inventory and every metadata hash before reading command index 1 from each sound-stream entry. It writes only the compact observations input; normal `--regenerate` and `--check` use repository inputs exclusively. `tests/test_rom_maps.py` recomputes it when the external evidence is available.

An emitted command proves its presence on the recording's CPU ROM, not its semantic label. Only source-reported observed labels with a supporting retained emission receive observed/rig evidence, with ROM scope derived from those recordings. Reported bindings without a retained emission stay candidate with their original grade preserved in the note; unverified labels stay candidate even when their command was recorded. Shared sound-ROM bytes do not establish the same CPU-trigger behavior.
