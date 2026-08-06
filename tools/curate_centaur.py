#!/usr/bin/env python3
"""Deterministic curator for Bally Centaur (1981).

Regenerates ``machines/partial/bally/centaur-1981.json`` and its knowledge note from the
tables embedded below, so the artifact can be reproduced byte-for-byte and drift can be
detected. ``--check`` refuses drift and never writes; ``--regenerate`` writes.

The tables are the curated result of three evidence sources, in the priority the runbook
sets out: the Bally game #1239 manual for physical construction, the ROM's own solenoid
self test (captured by the LibPinMAME harness) for the printed-to-public solenoid mapping,
and pinned PinMAME for controller topology. The self-test mapping in particular must not be
"tidied" into an identity mapping - see ``knowledge/bally/centaur-1981.md``.

Zero-padded legacy aliases follow a rule and are derived rather than embedded; only the
handful of named legacy aliases (``s_*``, ``c_*``) are stored, because they cannot be
derived and consumers still resolve them.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "centaur-1981.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "centaur-1981.md"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "centaur-1981.json"

DATA = json.loads((Path(__file__).with_suffix(".json")).read_text(encoding="utf-8"))


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


def build_definition() -> dict:
	inputs = []
	for key, spec in sorted(DATA["switches"].items(), key=lambda item: int(item[0])):
		address = int(key)
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		numeric = spec.get("legacy_numeric", legacy_numeric(address))
		aliases += [{"namespace": "vpe-legacy.switch", "value": value} for value in numeric]
		aliases += [
			{"namespace": "vpe-legacy.switch", "value": value}
			for value in spec.get("legacy_names", [])
		]
		if "manual_address" in spec:
			aliases.append({"namespace": "manual.address", "value": spec["manual_address"]})
		item = {
			"aliases": aliases,
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"provenance": spec["provenance"],
		}
		if "normally_closed" in spec:
			item["normally_closed"] = spec["normally_closed"]
		if "physical" in spec:
			item["physical"] = spec["physical"]
		if "roles" in spec:
			item["roles"] = spec["roles"]
		if "spatial" in spec:
			item["spatial"] = spec["spatial"]
		inputs.append(item)

	for key, spec in sorted(DATA.get("dips", {}).items(), key=lambda item: int(item[0])):
		address = int(key)
		inputs.append({
			"aliases": [{"namespace": "pinmame.dip", "value": str(address)},
				{"namespace": "manual.address", "value": "S%d" % address}],
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": spec["id"],
			"kind": "dip_switch",
			"label": spec["label"],
			"physical": spec["physical"],
			"provenance": spec["provenance"],
			"spatial": {
				"provenance": {"source_refs": ["manual.bally.centaur.1981"], "status": "validated"},
				"reason": "dip_switch",
				"status": "not_applicable",
			},
		})

	outputs = []
	for key, spec in sorted(DATA["solenoids"].items(), key=lambda item: int(item[0])):
		address = int(key)
		aliases = [{"namespace": "pinmame.coil", "value": str(address)}]
		numeric = spec.get("legacy_numeric", legacy_numeric(address))
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in numeric]
		aliases += [
			{"namespace": "vpe-legacy.coil", "value": value}
			for value in spec.get("legacy_names", [])
		]
		if "self_test" in spec:
			aliases.append({"namespace": "manual.self-test", "value": spec["self_test"]})
		coil = {
			"aliases": aliases,
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": spec["physical"],
			"provenance": spec["provenance"],
		}
		if "roles" in spec:
			coil["roles"] = spec["roles"]
		if "spatial" in spec:
			coil["spatial"] = spec["spatial"]
		outputs.append(coil)

	for key, spec in sorted(DATA["lamps"].items(), key=lambda item: int(item[0])):
		address = int(key)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		if spec.get("legacy"):
			numeric = spec.get("legacy_numeric", legacy_numeric(address))
			aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in numeric]
		item = {
			"aliases": aliases,
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": spec["id"],
			"kind": spec.get("kind", "lamp"),
			"label": spec["label"],
			"provenance": spec["provenance"],
		}
		if "physical" in spec:
			item["physical"] = spec["physical"]
		if "roles" in spec:
			item["roles"] = spec["roles"]
		if "spatial" in spec:
			item["spatial"] = spec["spatial"]
		outputs.append(item)

	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))

	return {
		"conflicts": DATA["conflicts"],
		"controller": DATA["controller"],
		"coverage": DATA["coverage"],
		"displays": DATA["displays"],
		"drivers": DATA["drivers"],
		"format": "pinmame-machine-definition",
		"inputs": inputs,
		"knowledge": DATA["knowledge"],
		"machine": DATA["machine"],
		"mechanisms": DATA["mechanisms"],
		"outputs": outputs,
		"relationships": DATA["relationships"],
		"schema_version": 2,
		"sources": DATA["sources"],
	}


def build_knowledge() -> str:
	"""The knowledge note is curated prose, so it is stored verbatim and drift-checked."""
	return DATA["knowledge_note"]


def canonical(value: object) -> str:
	return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="fail on drift; never write")
	mode.add_argument("--regenerate", action="store_true", help="rewrite the artifact")
	args = parser.parse_args()

	if AUTHOR_READY_PATH.exists():
		print(
			f"refusing to curate while an author-ready artifact exists (preserved): {AUTHOR_READY_PATH}",
			file=sys.stderr,
		)
		return 1

	expected = canonical(build_definition())
	expected_note = build_knowledge()

	if args.check:
		drifted = False
		for path, want in ((DEFINITION_PATH, expected), (KNOWLEDGE_PATH, expected_note)):
			if not path.exists():
				print(f"missing artifact: {path}", file=sys.stderr)
				drifted = True
				continue
			if path.read_text(encoding="utf-8") != want:
				print(f"canonical content mismatch: {path}", file=sys.stderr)
				drifted = True
		if drifted:
			return 1
		print("Centaur definition and knowledge note match the deterministic curator.")
		return 0

	DEFINITION_PATH.parent.mkdir(parents=True, exist_ok=True)
	DEFINITION_PATH.write_text(expected, encoding="utf-8", newline="\n")
	KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
	KNOWLEDGE_PATH.write_text(expected_note, encoding="utf-8", newline="\n")
	for path in (DEFINITION_PATH, KNOWLEDGE_PATH):
		print(f"wrote {path.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
