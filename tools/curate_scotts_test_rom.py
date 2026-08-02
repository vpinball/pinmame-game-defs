"""Classify Scott's Test ROM as diagnostic software, not a physical game."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
DRIVER_ID = "scotest8"


def main() -> None:
	catalog = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
	driver = next(record for record in catalog["drivers"] if record["id"] == DRIVER_ID)
	driver_record = {
		"id": driver["id"],
		"description": driver["description"],
		"year": driver["year"],
		"manufacturer": driver["manufacturer"],
		"flags": driver["flags"],
	}
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 1,
		"machine": {
			"id": "diagnostic.scotts-test-rom-v8",
			"name": "Scott's Test ROM (version 8)",
			"manufacturer": "Scott Charles",
			"year": 2019,
			"kind": "diagnostic_software",
		},
		"coverage": {
			"status": "partial",
			"missing": [
				"input_enumeration",
				"input_semantics",
				"output_enumeration",
				"output_semantics",
				"display_inventory",
				"mechanism_inventory",
				"mechanism_behavior",
				"polarity",
				"recreation_notes",
				"provenance",
			],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "unknown",
				"semantic_naming": "unknown",
				"physical_wiring": "not_applicable",
				"mechanisms": "not_applicable",
				"variant_coverage": "validated",
				"recreation_knowledge": "candidate",
			},
		},
		"controller": {"platform": "pinmame.bally-by35", "inversion_applied_by_emulator": True},
		"drivers": [driver_record],
		"inputs": [],
		"outputs": [],
		"displays": [],
		"mechanisms": [],
		"relationships": [],
		"sources": [
			{
				"id": f"pinmame.catalog.{PINMAME_REVISION[:12]}",
				"kind": "pinmame_catalog",
				"uri": "https://github.com/vpinball/pinmame",
				"revision": PINMAME_REVISION,
				"locator": "PinmameGetGames: scotest8",
				"license": "BSD-3-Clause",
				"attribution": "PinMAME contributors",
			},
			{
				"id": f"pinmame.core.{PINMAME_REVISION[:12]}",
				"kind": "pinmame_core",
				"uri": "https://github.com/vpinball/pinmame",
				"revision": PINMAME_REVISION,
				"locator": "src/wpc/by35games.c:1992-2002; src/wpc/driver.c:338",
				"license": "BSD-3-Clause",
				"attribution": "PinMAME contributors",
			},
		],
		"knowledge": {"path": "knowledge/partial/diagnostic/scotts-test-rom-v8.md", "status": "partial"},
		"conflicts": [],
	}
	definition_path = ROOT / "machines/partial/diagnostic/scotts-test-rom-v8.json"
	definition_path.parent.mkdir(parents=True, exist_ok=True)
	definition_path.write_text(json.dumps(definition, indent=2, sort_keys=True) + "\n", encoding="utf-8")

	knowledge_path = ROOT / "knowledge/partial/diagnostic/scotts-test-rom-v8.md"
	knowledge_path.parent.mkdir(parents=True, exist_ok=True)
	knowledge_path.write_text(
		"""# Scott's Test ROM (version 8)

Coverage: **partial diagnostic-software classification; not a physical game definition**

## Classification

PinMAME declares `scotest8` under the explicit `Scott's Test ROM` section in `by35games.c`, and the public driver description is `Scott's Test ROM (version 8)`. It is diagnostic software targeting Bally AS-2518-17/35-era hardware, not a distinct playfield an author can recreate.

The catalog retains it because it is a supported PinMAME driver. It is excluded from the physical/virtual game completion denominator only because the definition positively classifies it as `diagnostic_software`; unknown records continue to count as games.

## Emulated hardware

PinMAME initializes it as generation `GEN_BY17`, with the `dispBy7` display layout, left-flipper switch handling, eight balls, and the Bally 50 sound board. It uses the generic `input_ports_by35` input ports and the `by35_mBY35_50S` machine configuration.

## Remaining diagnostic documentation

The software's complete test sequence, expected switch/output address coverage, display prompts, sound tests, and operator procedure have not yet been documented. Those omissions keep this record partial even though they do not affect physical-game coverage.

## Sources

- PinMAME `4ec52ff0ac133ac251681518aed2249e19fe26eb`, `src/wpc/by35games.c:1992-2002` and `src/wpc/driver.c:338`.
""",
		encoding="utf-8",
	)


if __name__ == "__main__":
	main()
