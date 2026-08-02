"""Normalize the PinMAME SAM game-on state and legacy ticket-service bindings.

SAM exposes synthetic public solenoid 33 for game-on/fast-flip state. Older imported
definitions confused the service manual's optional ticket identities 33-35 with that
LibPinMAME address. Physical ticket functions remain documented in an untransported
controller group while public solenoid 33 is represented exactly once as virtual.
"""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]


def _ticket_service_output(output: dict[str, object]) -> bool:
	binding = output.get("binding")
	if not isinstance(binding, dict) or binding.get("group") != "pinmame.output.solenoid" or binding.get("device") not in {33, 34, 35}:
		return False
	label = str(output.get("label", "")).casefold()
	return "ticket" in label or "switched ground" in label


def _move_ticket_service_output(output: dict[str, object]) -> None:
	binding = output["binding"]
	assert isinstance(binding, dict)
	binding["group"] = "physical.output.ticket"
	address = int(binding["device"])
	aliases = output.get("aliases")
	if not isinstance(aliases, list):
		aliases = []
	aliases = [alias for alias in aliases if isinstance(alias, dict) and alias.get("namespace") not in {"pinmame.solenoid", "vpe-legacy.coil"}]
	if not any(alias.get("namespace") == "manual.service-output" and alias.get("value") == str(address) for alias in aliases):
		aliases.append({"namespace": "manual.service-output", "value": str(address)})
	output["aliases"] = aliases


def _game_on_output(core_source: str) -> dict[str, object]:
	return {
		"id": "virtual.game-on",
		"label": "PinMAME SAM game-on state",
		"kind": "virtual",
		"binding": {"group": "pinmame.output.solenoid", "device": 33},
		"aliases": [{"namespace": "pinmame.solenoid", "value": "33"}],
		"availability": "used",
		"physical": {"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."},
		"provenance": {"status": "validated", "source_refs": [core_source]},
	}


def normalize_definition(path: Path) -> bool:
	definition = load_json(path)
	if definition.get("coverage", {}).get("status") != "author_ready" or definition.get("controller", {}).get("platform") != "pinmame.sam":
		return False
	outputs = definition.get("outputs")
	if not isinstance(outputs, list):
		raise ValueError(f"{path}: author-ready SAM definition has no output inventory")
	for output in outputs:
		if isinstance(output, dict) and _ticket_service_output(output):
			_move_ticket_service_output(output)
	game_on = [output for output in outputs if isinstance(output, dict) and output.get("binding") == {"group": "pinmame.output.solenoid", "device": 33}]
	if len(game_on) > 1:
		raise ValueError(f"{path}: multiple public SAM solenoid-33 definitions")
	if game_on:
		if game_on[0].get("kind") != "virtual":
			raise ValueError(f"{path}: public SAM solenoid 33 is still physical after ticket migration")
	else:
		core_sources = [source.get("id") for source in definition.get("sources", []) if isinstance(source, dict) and source.get("kind") == "pinmame_core"]
		if len(core_sources) != 1:
			raise ValueError(f"{path}: expected one PinMAME core source")
		insert_at = max((index for index, output in enumerate(outputs) if isinstance(output, dict) and output.get("binding", {}).get("group") == "pinmame.output.solenoid"), default=-1) + 1
		outputs.insert(insert_at, _game_on_output(str(core_sources[0])))
	write_json(path, definition)
	return True


def main() -> None:
	count = sum(normalize_definition(path) for path in sorted((ROOT / "machines" / "author-ready").rglob("*.json")))
	print(f"Normalized {count} author-ready SAM definitions.")


if __name__ == "__main__":
	main()
