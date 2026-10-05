# ROM-map inputs

Bulk tables that `tools/curate_rom_maps.py` reads. Each was transcribed once from contributor evidence that is retained outside Git, and the curator pins each one by SHA-256. Edit a table only together with its pin and its source record.

| File | Transcribed from | Retained at (working root) |
| --- | --- | --- |
| `lethal-weapon-3-1992.sound-commands.json` | `docs/TR_SOUND_MAP.csv`, the Total Recall project's own sound-command map and labels | `review-artifacts/lethal-weapon-3-rom-state-2026-10-03/` |
| `attack-from-mars-1995.dcs-commands.json` | the DCS opcode table in `knowledge/bally/attack-from-mars-1995.md`: contributor runtime annotations and group only | (in this repository) |
| `attack-from-mars-1995.game-adjustments.json` | `rammap/afm_adjustments_named.json`, read out of the ROM's own adjustment descriptors and menu strings | `review-artifacts/attack-from-mars-rom-state-2026-09-05/` |
| `attack-from-mars-1995.mode-replay.json` | `rammap/afm_modes.json`, the contributor's mode-replay recipes | `review-artifacts/attack-from-mars-rom-state-2026-09-05/` |

The AFM table deliberately leaves out the sample file names from the community altsound package that the knowledge note's table quotes. That package is not retained, and its author and redistribution terms are not established. None of these tables copies Pinball Memory Maps content, so they stay under this repository's MIT licence.
