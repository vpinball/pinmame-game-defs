"""Derive compact Taxi evidence from successful, independently pinned raw runs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes
from run_pinmame_harness import SEGMENT_16_CHARACTERS

REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
HARNESS_REVISION = "409403c8afd22fcc3abdbd339f6517f2286a1882"
LIBRARY_SHA256 = "ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d"
ROM_SHA256 = "30f21e3aa2ed62e93d38953e410b0c92679f264b7252d0408aad1d3eb991c03c"
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = Path("evidence/runtime/system-11/taxi-l4-service.json")


DROP_SENSOR_LABELS = {
	27: "LOLA LEFT",
	28: "LOLA MIDDLE",
	29: "LOLA RIGHT",
	30: "PINBOT TOP",
	31: "PINBOT MIDDLE",
	32: "PINBOT BOTTOM",
}
ALPHA_DISPLAY_INDEX = 0
NUMERIC_DISPLAY_INDEX = 1
ALPHA_SEGMENT_POSITIONS = list(range(16))
NUMERIC_ADDRESS_POSITIONS = [4, 5]
SEVEN_SEGMENT_DIGITS = {
	0x00: " ",
	0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4",
	0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9",
}


def _segments(values: object, context: str) -> list[int]:
	if not isinstance(values, list) or any(type(value) is not int or not 0 <= value <= 0xFFFF for value in values):
		raise ValueError(f"{context} must contain only 16-bit integer segments")
	return list(values)


def alpha_text(segments: list[int]) -> str:
	"""Decode Taxi's alpha display without concealing unknown glyphs.

	Taxi uses an alternate seven-segment 1 (0x0006). Its alpha decimal is
	bit15: for example, HI. SCORE's 0xa209 is I (0x2209) plus the decimal.
	O/0 share a glyph in this ROM; the separate numeric display settles the
	diagnostic address. An unknown alpha pattern is evidence drift, not text.
	"""
	decoded: list[str] = []
	for value in _segments(segments, "Alpha display"):
		glyph = value & 0x7FFF
		character = {0x0006: "1"}.get(glyph, SEGMENT_16_CHARACTERS.get(glyph))
		if character is None:
			raise ValueError(f"Unrecognized alpha segment pattern 0x{glyph:04x}")
		decoded.append(character + ("." if value & 0x8000 else ""))
	return "".join(decoded)


def _normalized_alpha_text(segments: list[int]) -> str:
	"""Normalize only display whitespace before comparing a ROM label."""
	return " ".join(alpha_text(segments).split())


def numeric_text(segments: list[int], positions: list[int] = NUMERIC_ADDRESS_POSITIONS) -> str:
	"""Decode only explicitly selected System 11 numeric slots.

	Taxi's CORE_SEG8 low byte drives the numeric slots, while the high byte
	contains separate digits. Do not infer meanings for the other cells.
	"""
	values = _segments(segments, "Numeric display")
	if len(set(positions)) != len(positions) or any(type(position) is not int or position < 0 or position >= len(values) for position in positions):
		raise ValueError("Numeric display positions must be unique in-range indexes")
	decoded: list[str] = []
	for position in positions:
		value = values[position]
		if value & 0xFF00:
			raise ValueError(f"Numeric address position {position} contains high-byte segments")
		glyph = value & 0x7F
		character = SEVEN_SEGMENT_DIGITS.get(glyph)
		if character is None:
			raise ValueError(f"Unrecognized numeric segment pattern 0x{glyph:02x} at position {position}")
		decoded.append(character + ("." if value & 0x80 else ""))
	return "".join(decoded)


def _snapshot(run: dict, label: str) -> dict:
	matches = [item for item in run.get("snapshots", []) if isinstance(item, dict) and item.get("label") == label]
	if len(matches) != 1:
		raise ValueError(f"Expected exactly one runtime snapshot labelled {label!r}")
	return matches[0]


def _display_segments(snapshot: dict, display_index: int) -> list[int]:
	displays = snapshot.get("displays")
	if not isinstance(displays, list):
		raise ValueError(f"Snapshot {snapshot.get('label')!r} has no display list")
	matches = [display for display in displays if isinstance(display, dict) and display.get("index") == display_index]
	if len(matches) != 1:
		raise ValueError(f"Snapshot {snapshot.get('label')!r} must contain display {display_index} exactly once")
	return _segments(matches[0].get("segments"), f"Snapshot {snapshot.get('label')!r} display {display_index}")


def _response(snapshot: dict, display_index: int, positions: list[int], interpreted_text: str, diagnostic_address: int | None = None) -> dict:
	response = {
		"snapshot_label": snapshot["label"],
		"display_index": display_index,
		"segments": _display_segments(snapshot, display_index),
		"decoded_segment_positions": positions,
		"interpreted_text": interpreted_text,
	}
	if diagnostic_address is not None:
		response["diagnostic_address"] = diagnostic_address
	return response


def verify_drop_response(run: dict, address: int) -> dict:
	"""Verify and retain all ROM display responses for one Taxi drop sensor."""
	try:
		expected_label = DROP_SENSOR_LABELS[address]
	except KeyError as error:
		raise ValueError(f"No settled Taxi drop-response contract for switch {address}") from error

	active = _snapshot(run, f"switch {address} active stimulus")
	release = _snapshot(run, f"switch {address} release stimulus")
	active_alpha = _display_segments(active, ALPHA_DISPLAY_INDEX)
	release_alpha = _display_segments(release, ALPHA_DISPLAY_INDEX)
	if len(active_alpha) != 16 or len(release_alpha) != 16:
		raise ValueError(f"Drop sensor {address} alpha response must retain all 16 segment cells")
	active_label = _normalized_alpha_text(active_alpha)
	if active_label != expected_label:
		raise ValueError(f"Drop sensor {address} active alpha label {active_label!r} does not equal {expected_label!r}")
	release_label = _normalized_alpha_text(release_alpha)
	if release_label:
		raise ValueError(f"Drop sensor {address} release alpha label is stale: {release_label!r}")

	active_numeric = _display_segments(active, NUMERIC_DISPLAY_INDEX)
	release_numeric = _display_segments(release, NUMERIC_DISPLAY_INDEX)
	if len(active_numeric) != 16 or len(release_numeric) != 16:
		raise ValueError(f"Drop sensor {address} numeric response must retain all 16 segment cells")
	observed_text = numeric_text(active_numeric)
	if "." in observed_text:
		raise ValueError(f"Drop sensor {address} numeric diagnostic address unexpectedly has a decimal attribute: {observed_text!r}")
	if not observed_text.isdecimal():
		raise ValueError(f"Drop sensor {address} numeric diagnostic address is not digits: {observed_text!r}")
	observed_address = int(observed_text)
	if observed_address != address:
		raise ValueError(f"Drop sensor {address} observed numeric address {observed_address} does not equal the stimulated address")
	if [release_numeric[position] for position in NUMERIC_ADDRESS_POSITIONS] != [0, 0]:
		raise ValueError(f"Drop sensor {address} release numeric address is stale")

	return {
		"label": f"drop sensor {address}: ROM names public1 and clears public0",
		"input_kind": "switch",
		"input_address": address,
		"observed_switch_addresses": [],
		"host_stimulus_switch_addresses": [address],
		"result": "observed",
		"display_responses": [
			_response(active, ALPHA_DISPLAY_INDEX, ALPHA_SEGMENT_POSITIONS, active_label),
			_response(active, NUMERIC_DISPLAY_INDEX, NUMERIC_ADDRESS_POSITIONS, observed_text, observed_address),
			_response(release, ALPHA_DISPLAY_INDEX, ALPHA_SEGMENT_POSITIONS, release_label),
			_response(release, NUMERIC_DISPLAY_INDEX, NUMERIC_ADDRESS_POSITIONS, ""),
		],
	}


def _load_run(path: Path, scenario: Path) -> dict:
	run = json.loads(path.read_bytes())
	if run.get("failure") is not None or run.get("game") != "taxi_l4":
		raise ValueError(f"Not a successful Taxi L4 run: {path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"Wrong pinned emulator binary: {path}")
	if run.get("scenario", {}).get("sha256") != hashlib.sha256(scenario.read_bytes()).hexdigest():
		raise ValueError(f"Scenario identity drift: {path}")
	return run


def _checkpoints(run: dict) -> list[dict]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
		for step in run["steps"] if step["type"] == "pulse_until_display"]


def build(review_root: Path) -> dict:
	runtime = review_root / "taxi-1988/runtime"
	names = [("l4-init", "taxi-nvram-init"), ("l4-coil", "taxi-coil-test"),
		("l4-labels-v3", "taxi-service-labels")]
	runs = {name: _load_run(runtime / (name + ".json"), ROOT / "tools/harness-scenarios/system-11" / (scenario + ".json"))
		for name, scenario in names}
	coil, labels = runs["l4-coil"], runs["l4-labels-v3"]
	if _checkpoints(coil) != [{"matched_text": "COIL TEST", "after_service_pulses": 5}]:
		raise ValueError("Taxi coil diagnostic checkpoint drift")
	if [x["matched_text"] for x in _checkpoints(labels)] != ["SINGLE LAMPS", "SWITCH EDGES"]:
		raise ValueError("Taxi service label diagnostic checkpoint drift")
	coil_seen = sorted({x["number"] for x in coil["events"] if x["event"] == "solenoid" and x["state"]})
	lamp_seen = sorted({x["number"] for x in labels["events"] if x["event"] == "lamp" and x["state"]})
	if not (set(range(1, 23)) | set(range(25, 33))) <= set(coil_seen) or lamp_seen != list(range(1, 65)):
		raise ValueError("Taxi complete service output sweep is missing addresses")
	checks = [verify_drop_response(labels, address) for address in DROP_SENSOR_LABELS]
	for host, copied, synthetic, label in [(82, 57, [45, 46], "right"), (84, 58, [47, 48], "left")]:
		held = next(x for x in labels["snapshots"] if x["label"] == f"{label} cabinet flipper column stimulus (held)")
		states = {x["number"]: x["state"] for x in held["watched_switches"]}
		if states.get(copied) != 1 or not set(synthetic) <= set(held["active_solenoids"]):
			raise ValueError("Cabinet flipper copy/synthetic output did not answer host input")
		checks.append({"label": label + " cabinet input copy", "input_kind": "switch", "input_address": host,
			"observed_switch_addresses": [copied], "host_stimulus_switch_addresses": [host],
			"held_synthetic_solenoid_addresses": synthetic, "result": "observed"})
	raw_runs = []
	for name, scenario in names:
		run = runs[name]
		raw_runs.append({"name": name, "sha256": hashlib.sha256((runtime / (name + ".json")).read_bytes()).hexdigest(),
			"scenario_path": f"tools/harness-scenarios/system-11/{scenario}.json", "scenario_sha256": run["scenario"]["sha256"],
			"action_count": run["scenario"]["action_count"], "watch_switches": run["watch_switches"],
			"self_test_pulses": sum(x["after_service_pulses"] for x in _checkpoints(run)), "boot_wait_s": 0,
			"nvram_initialization": "Fresh empty state; one retained initialization scenario." if name == "l4-init" else
			"Fresh state; copied only l4-init-state/nvram/taxi_l4.nv from the separately hashed initialization run.",
			"snapshot_count": len(run["snapshots"]), "retained_from": f"taxi-1988/runtime/{name}.json"})
	return {"format": "pinmame-machine-evidence", "version": 1, "extractor": {"id": "taxi-runtime-evidence", "version": 2},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame-game-defs",
			"revision": HARNESS_REVISION, "path": "tools/run_pinmame_harness.py", "sha256": hashlib.sha256((ROOT / "tools/run_pinmame_harness.py").read_bytes()).hexdigest(), "license": "MIT", "quality": "full"},
		"driver_ids": ["taxi_l4"], "machine_ids": ["williams.taxi.1988"], "switches": [], "outputs": [], "states": [], "mechanisms": [],
		"recreation_notes": [],
		"runtime": {"game": "taxi_l4", "rom_archive_sha256": ROM_SHA256,
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": REVISION},
			"raw_runs": raw_runs, "command_template": "python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game taxi_l4 --rom-path <legal-ROM-root> --work-dir <fresh-state> --scenario <recorded-scenario> --boot-wait 0 --output <external-run>; each scenario deliberately stabilizes for8s; diagnostic states inherit only the retained initialization NVRAM.",
			"observations": {"service_language": "English", "solenoid_addresses_seen": coil_seen, "lamp_addresses_seen": lamp_seen,
				"display_indices_seen": [0, 1, 2, 3], "ordered_solenoid_on_sequence": [x["number"] for x in coil["events"] if x["event"] == "solenoid" and x["state"]],
				"runs": {"l4-coil": {"diagnostic_checkpoints": _checkpoints(coil), "solenoid_addresses_seen": coil_seen},
					"l4-labels-v3": {"diagnostic_checkpoints": _checkpoints(labels), "named_action_observations": checks,
						"limitation": "Static host stimuli; physical movement, socket population and prototype hardware are not measured."}}}}}


def check(review_root: Path) -> None:
	if (ROOT / EVIDENCE_PATH).read_bytes() != canonical_bytes(build(review_root)):
		raise ValueError("Taxi compact runtime evidence drift")


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("review_root", type=Path)
	args = parser.parse_args()
	check(args.review_root)
	print("Taxi compact runtime evidence matches the successful retained runs.")
