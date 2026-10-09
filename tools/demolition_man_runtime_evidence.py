"""Derive the compact Demolition Man runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism setting, and writes the derived
observations beside the other runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's visual reading
of that snapshot's retained DMD frame; its ``pixel_sha256`` pins the frame. The tool refuses a raw run whose transitions no
longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.demolition-man.1994"
GAME = "dm_lx4"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "63759f135cb709df5908c8014b851822ba09fd16a9e6858d9e39d7255c7364f9"
HARNESS_DIRECTORY = "demolition-man-1994/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-dcs"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-dcs"
IDENTIFICATION = "DEMOLITION MAN / 50028 REV. LX-4"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The run directory's manifest (tools/build_external_evidence_manifest.py) lists the raw "
	"trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM restored its factory settings before the "
	"scenario left the message loop with Escape"
)
# Retained run directory -> (SHA-256 of its manifest.json, built-in mechanisms mask the run used).
RUNS = {
	"dm-switch-edges": ("ca903257e8890b79c313d4bb3db86c2ba47e6db17bdff12d5c08cedf4927d7ae", 0),
	"dm-claw-test": ("c3a0d368fcc6ea55c3b4ac805f8902756a436b434eaca0d9c656233d37c1b6c9", 0),
	"dm-claw-functions": ("b1cb3e242488672b986e8a638b3031c70f2a93112df926bf089bfd8551ddc7fc", 15),
	"dm-solenoid-test": ("2a09a0d212be553c3ae65d21c23bc2342ea703b2bd0f3f0de56723b7510670bf", 15),
	"dm-flasher-test": ("5e60cadcb7ac33529df660c8941570a80f16de7d1b1cf9b749aefa8f4f531954", 15),
	"dm-gi-test": ("34ddde17974ff0dee923ee188e18397dec42190648add8552e1e1f25303a5be5", 15),
	"dm-flipper-coil-test": ("5690840bd7640e2099a2ff4c4183eb19cb311369433ffc7df0b1ff70d47bcc94", 15),
	"dm-single-lamps": ("082da2b0ad8e260f02dd94c147e23d7c9075876cef205205c2875f44911afacd", 15),
}

# --- T.1 SWITCH EDGES: the name on the ROM's top display line while it reads the switch as active ---------------------
EDGE_NAMES = {
	11: "BALL LAUNCH", 12: "L. HANDLE BUTTON", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "LEFT OUTLANE", 16: "LEFT INLANE",
	17: "RIGHT INLANE", 18: "RIGHT OUTLANE", 21: "SLAM TILT", 23: "BUY-IN BUTTON", 24: "ALWAYS CLOSED", 25: "CLAW RIGHT",
	26: "CLAW LEFT", 27: "SHOOTER LANE", 28: "NOT USED", 31: "TROUGH 1 (RIGHT)", 32: "TROUGH 2", 33: "TROUGH 3", 34: "TROUGH 4",
	35: "TROUGH 5 (LEFT)", 36: "TROUGH JAM", 37: "NOT USED", 38: "STANDUP 5", 41: "LEFT SLING", 42: "RIGHT SLING", 43: "LEFT JET",
	44: "TOP SLING", 45: "RIGHT JET", 46: "R. RAMP ENTER", 47: "R. RAMP EXIT", 48: "RIGHT LOOP", 51: "L. RAMP ENTER",
	52: "L. RAMP EXIT", 53: "CENTER RAMP", 54: "UPPER REBOUND", 55: "LEFT LOOP", 56: "STANDUP 2", 57: "STANDUP 3", 58: "STANDUP 4",
	61: "SIDE RAMP ENTER", 62: "SIDE RAMP EXIT", 63: "(M)TL ROLLOVER", 64: "M(T)L ROLLOVER", 65: "MT(L) ROLLOVER", 66: "EJECT",
	67: "ELEVATOR INDEX", 68: "NOT USED", 71: "CAR CRASH 1", 72: "CAR CRASH 2", 73: "TOP POPPER", 74: "ELEVATOR HOLD",
	75: "NOT USED", 76: "BOTTOM POPPER", 77: "EYEBALL STANDUP", 78: "STANDUP 1", 81: 'CLAW "CAPT. SIM."', 82: 'CLAW "SUP. JETS"',
	83: 'CLAW "PR. BREAK"', 84: 'CLAW "FREEZE"', 85: 'CLAW "ACMAG"', 86: "UL. FLIPPER GATE", 87: "CAR CR. STANDUP", 88: "LOWER REBOUND",
}
# The one swept switch the ROM names on the falling edge: 24 (Always Closed) is named when public 24 goes to 0.
NAMED_AT_ZERO = frozenset({24})
EDGE_MATRIX = tuple(sorted(address for address in EDGE_NAMES))
# Fliptronic buttons: the ROM fires a flipper and names the synthesized end-of-stroke switch.
FLIPPER_BUTTONS = {
	112: ("R FLIPPER EOS", "F1", (45, 46)), 114: ("UL FLIPPER EOS", "F7", (35, 36, 47, 48)),
	116: ("R FLIPPER EOS", "F1", (45, 46)), 118: ("UL FLIPPER EOS", "F7", (35, 36, 47, 48)),
}
# End-of-stroke addresses: a host write raises no name (PinMAME rewrites 111, 113 and 117 from the coil state; 115 reads back but the ROM ignores it).
FLIPPER_EOS = (111, 113, 115, 117)

# --- T.4 SOLENOID TEST: (address, step label whose snapshot is read, ROM text) --------------------------------------
T4 = (
	(1, "Enter (start T.4)", "BALL RELEASE / T.4 01 REPEAT / VIO-BRN RED-BRN"),
	(2, "T.4 after Up 1", "BOTTOM POPPER / T.4 02 REPEAT / VIO-RED RED-BRN"),
	(3, "T.4 after Up 2", "AUTO PLUNGER / T.4 03 REPEAT / VIO-ORN RED-BRN"),
	(4, "T.4 after Up 3", "TOP POPPER / T.4 04 REPEAT / VIO-YEL RED-BRN"),
	(5, "T.4 after Up 4", "DIVERTER POWER / T.4 05 REPEAT / VIO-GRN RED-BRN"),
	(6, "T.4 after Up 5", "NOT USED / T.4 06 REPEAT / VIO-BLU RED-BRN"),
	(7, "T.4 after Up 6", "KNOCKER / T.4 07 REPEAT / VIO-BLK RED-BRN"),
	(8, "T.4 after Up 7", "NOT USED / T.4 08 REPEAT / VIO-GRY RED-BLK"),
	(9, "T.4 after Up 8", "LEFT SLING / T.4 09 REPEAT / BRN-BLK RED-BLK"),
	(10, "T.4 Up 9", "RIGHT SLING / T.4 10 REPEAT / BRN-RED RED-BLK"),
	(11, "T.4 after Up 10", "LEFT JET / T.4 11 REPEAT / BRN-ORN RED-BLK"),
	(12, "T.4 after Up 11", "TOP SLING / T.4 12 REPEAT / BRN-YEL RED-BLK"),
	(13, "T.4 after Up 12", "RIGHT JET / T.4 13 REPEAT / BRN-GRN RED-BLK"),
	(14, "T.4 after Up 13", "EJECT / T.4 14 REPEAT / BRN-BLU RED-BLK"),
	(15, "T.4 after Up 14", "DIVERTER HOLD / T.4 15 REPEAT / BRN-VIO RED-BLK"),
	(16, "T.4 after Up 15", "NOT USED / T.4 16 REPEAT / BRN-GRY RED-BLK"),
	(33, "T.4 after Up 16", "CLAW MAGNET / T.4 33 REPEAT / YEL-VIO RED-VIO"),
	(34, "T.4 after Up 17", "NOT USED / T.4 34 REPEAT / ORN-VIO RED-VIO"),
)
# Step whose transitions prove the pulse: the Enter that starts the test for the first driver, then each Up press.
T4_PULSE_STEP = {address: ("Enter (start T.4)" if index == 0 else f"T.4 Up {index}") for index, (address, _, _) in enumerate(T4)}

# --- T.5 FLASHER TEST -----------------------------------------------------------------------------------------------
T5 = (
	(17, "Enter (start T.5)", "CLAW FLASHER / T.5 17 REPEAT / BLK-BRN RED-WHT"),
	(21, "T.5 Up 1", "JETS FLASHER / T.5 21 REPEAT / BLU-GRN RED-WHT"),
	(22, "T.5 Up 2", "SIDE RAMP / T.5 22 REPEAT / BLU-BLK RED-WHT"),
	(23, "T.5 Up 3", "LEFT RAMP UPPER / T.5 23 REPEAT / BLU-VIO RED-WHT"),
	(24, "T.5 Up 4", "LEFT RAMP LOWER / T.5 24 REPEAT / BLU-GRY RED-WHT"),
	(25, "T.5 Up 5", "CAR CRASH CENTER / T.5 25 REPEAT / BLU-BRN RED-WHT"),
	(26, "T.5 Up 6", "CAR CRASH LOWER / T.5 26 REPEAT / BLU-RED RED-WHT"),
	(27, "T.5 Up 7", "RIGHT RAMP / T.5 27 REPEAT / BLU-ORN RED-WHT"),
	(28, "T.5 Up 8", "EJECT FLASHER / T.5 28 REPEAT / BLU-YEL RED-WHT"),
	(51, "T.5 Up 9", "CAR CRASH UPPER / T.5 37 REPEAT / BRN-WHT RED-WHT"),
	(52, "T.5 Up 10", "LOWER REBOUND / T.5 38 REPEAT / BLK-WHT RED-WHT"),
	(53, "T.5 Up 11", "EYEBALL FLASHER / T.5 39 REPEAT / ORN-WHT RED-WHT"),
	(54, "T.5 Up 12", "CENTER RAMP / T.5 40 REPEAT / YEL-WHT RED-WHT"),
	(55, "T.5 Up 13", "ELEVATOR FLASH 2 / T.5 41 REPEAT / GRN-WHT RED-WHT"),
	(56, "T.5 Up 14", "ELEVATOR FLASH 1 / T.5 42 REPEAT / BLU-WHT RED-WHT"),
	(57, "T.5 Up 15", "DIVERTER FLASHER / T.5 43 REPEAT / VIO-WHT RED-WHT"),
	(58, "T.5 Up 16", "RIGHT RAMP UPPER / T.5 44 REPEAT / GRY-WHT RED-WHT"),
)

# --- T.6 GEN'L. ILLUM.: (public string, step label, ROM text) -------------------------------------------------------
T6 = (
	((0, 1, 2, 3, 4), "T.6 Up 1", "ALL ILLUMINATION / T.6 BRIGHT=2 STOP"),
	((0,), "T.6 Up 9", "BACK PANEL / T.6 BRIGHT=2 STOP / WHT-BRN BRN"),
	((1,), "T.6 Up 17", "UPPER RIGHT / T.6 BRIGHT=2 STOP / WHT-ORN ORN"),
	((2,), "T.6 Up 25", "UPPER LEFT / T.6 BRIGHT=2 STOP / WHT-YEL YEL"),
	((3,), "T.6 Up 33", "LOWER RIGHT / T.6 BRIGHT=2 STOP / WHT-GRN GRN"),
	((4,), "T.6 Up 41", "LOWER LEFT / T.6 BRIGHT=2 STOP / WHT-VIO VIO"),
)

# --- T.12 FLIPPER COIL: (public outputs pulsed, step label, ROM text) -----------------------------------------------
T12 = (
	((45,), "Enter (start T.12)", "R. FLIP. POWER / T.12 01 REPEAT / BLU-VIO BLU-YEL"),
	((46,), "T.12 Up 1", "R. FLIP. HOLD / T.12 02 REPEAT / ORN-GRN BLU-YEL"),
	((47,), "T.12 Up 2", "L. FLIP. POWER / T.12 03 REPEAT / BLU-GRY GRY-YEL"),
	((48,), "T.12 Up 3", "L. FLIP. HOLD / T.12 04 REPEAT / ORN-BLU GRY-YEL"),
	((35,), "T.12 Up 4", "U.L. FLIP. POWER / T.12 07 REPEAT / BLK-BLU GRY-YEL"),
	((36,), "T.12 Up 5", "U.L. FLIP. HOLD / T.12 08 REPEAT / ORN-GRY GRY-YEL"),
)

# --- T.8 SINGLE LAMPS: public lamp -> the name the ROM prints (frame taken while the Up press is held) ---------------
LAMP_NAMES = {
	11: "BALL SAVE", 12: '"FORTRESS MB"', 13: '"MUSEUM MB"', 14: '"CRYOPRISON MB"', 15: '"WASTELAND MB"', 16: '"SHOOT AGAIN"',
	17: '"ACCESS CLAW"', 18: 'L. RAMP "EXPLODE"', 21: 'R. RAMP "JACKPOT"', 22: 'R. LOOP "EXPLODE"', 23: '"LITE QU. FREEZE"',
	24: '"FREEZE" 4 (R)', 25: '"CLAW READY"', 26: '"FREEZE" 3', 27: '"FREEZE" 2', 28: '"FREEZE" 1 (L)', 31: 'R. LOOP "JACKPOT"',
	32: "STANDUP 5", 33: "R. RAMP ARROW", 34: 'L. RAMP "JACKPOT"', 35: 'L. LOOP "JACKPOT"', 36: "CAR CRASH TOP", 37: "STANDUP 1",
	38: "CAR CRASH CENTER", 41: 'R. RAMP "EXPLODE"', 42: "R. RAMP CAR CHASE", 43: '"QUICK FREEZE"', 44: "L. RAMP CAR CHASE",
	45: '"EXTRA BALL"', 46: '"START M. BALL"', 47: "CAR CRASH BOTTOM", 48: 'L. LOOP "EXPLODE"', 51: "UNDERG. ARROW",
	52: 'UNDERG. "JACKPOT"', 53: "STANDUP 2", 54: "L. RAMP ARROW", 55: 'S. RAMP "JACKPOT"', 56: "S. RAMP ARROW",
	57: "L. LOOP ARROW", 58: 'C. RAMP "JACKPOT"', 61: 'CLAW "CAPT. SIM."', 62: 'CLAW "SUP. JETS"', 63: 'CLAW "PR. BREAK"',
	64: 'CLAW "FREEZE"', 65: 'CLAW "ACMAG"', 66: "(M)TL ROLLOVER", 67: "M(T)L ROLLOVERR", 68: "MT(L) ROLLOVER",
	71: '"SUPER JACKPOT"', 72: '"COMPUTER"', 73: '"DEMO. TIME"', 74: "NOT USED", 75: "NOT USED", 76: "STANDUP 4", 77: "STANDUP 3",
	78: '"RETINA SCAN"', 81: "C. RAMP MIDDLE", 82: "C. RAMP OUTER (2)", 83: "C. RAMP INNER (2)", 84: "C. RAMP ARROW",
	85: "R. LOOP ARROW", 86: "BUY-IN BUTTON", 87: '"LAUNCH BALL"', 88: "START BUTTON",
}
LAMP_ORDER = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))

# --- T.14 CLAW TEST -------------------------------------------------------------------------------------------------
CLAW_BOXES = {25: "CLAW R. SW.", 26: "CLAW L. SW.", 67: "ELEV. INDEX", 74: "ELEV. HOLD"}
CLAW_FUNCTIONS = (
	(1, "AUTO RUN", (18,)),
	(2, "CLAW LEFT", ()),
	(3, "CLAW RIGHT", (19, 20)),
	(4, "RUN ELEVATOR", (18,)),
	(5, "PARK ELEVATOR", (18,)),
	(6, "MAGNET ON", (33,)),
)


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(review_root: Path, name: str) -> dict[str, Any]:
	directory = review_root / HARNESS_DIRECTORY / name
	manifest_sha, mechanics = RUNS[name]
	if _sha256(directory / "manifest.json") != manifest_sha:
		raise ValueError(f"retained run manifest drift: {directory}")
	manifest = json.loads((directory / "manifest.json").read_bytes())
	if manifest.get("format") != "pinmame-external-evidence-manifest" or manifest.get("game") != GAME:
		raise ValueError(f"not a Demolition Man run manifest: {directory}")
	listed = {entry["path"] for entry in manifest["files"]}
	if not {"run.json", "scenario.json"} <= listed:
		raise ValueError(f"run manifest omits the trace or the scenario: {directory}")
	for entry in manifest["files"]:
		target = directory / entry["path"]
		if not target.is_file() or target.stat().st_size != entry["size"] or _sha256(target) != entry["sha256"]:
			raise ValueError(f"retained run file missing or changed: {target}")
	run = json.loads((directory / "run.json").read_bytes())
	run["_directory"] = directory
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{name}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Demolition Man {GAME} run: {directory}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {directory}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {directory}")
	if run.get("handle_mechanics") != mechanics:
		raise ValueError(f"run {name} must use --handle-mechanics {mechanics}")
	return run


def _snapshot(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["snapshots"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one snapshot labelled {label!r}, found {len(matches)}")
	return matches[0]


def _step(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["steps"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def _risen(step: dict[str, Any], channel: str = "solenoids") -> set[int]:
	"""Addresses whose recorded transitions during the step include an active state."""
	return {item["number"] for item in step["transitions"][channel] if any(item["states"])}


def _frame_matches(run: dict[str, Any], display: dict[str, Any]) -> bool:
	"""Whether the retained PGM frame reproduces the snapshot's pixel SHA-256.

	run_pinmame_harness.py hashes the raw levels and writes them to the PGM unchanged when any exceeds the layout's depth
	(as this DMD's 0-254 levels do), or scaled to 0-255 (level * 255 / max_level) otherwise; either encoding is accepted.
	"""
	path = run["_directory"] / display["artifact"].replace("\\", "/").split("/", 1)[1]
	layout = display["layout"]
	header = f"P5\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
	data = path.read_bytes()
	if not data.startswith(header) or len(data) != len(header) + layout["width"] * layout["height"]:
		raise ValueError(f"unexpected DMD frame file: {path}")
	payload = data[len(header):]
	max_level = max((1 << max(int(layout.get("depth", 1)), 1)) - 1, 1)
	candidates = {hashlib.sha256(payload).hexdigest(), hashlib.sha256(bytes(round(value * max_level / 255) for value in payload)).hexdigest()}
	return display["pixel_sha256"] in candidates


def _diagnostic(run: dict[str, Any], label: str, text: str) -> dict[str, Any]:
	snapshot = _snapshot(run, label)
	displays = [item for item in snapshot["displays"] if item["index"] == 0]
	if len(displays) != 1:
		raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
	if not _frame_matches(run, displays[0]):
		raise ValueError(f"retained DMD frame of snapshot {label!r} does not reproduce its pixel SHA-256")
	return {
		"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
		"display_index": 0,
		"interpreted_text": text,
		"label": label,
		"nonzero_pixels": displays[0]["nonzero_pixels"],
		"pixel_sha256": displays[0]["pixel_sha256"],
	}


def _frame_rows(review_root: Path, run: dict[str, Any], label: str, rows: slice, columns: slice) -> bytes:
	"""Pixels of a region of the labelled snapshot's retained PGM frame (128x32, one byte per pixel after the header)."""
	artifact = _snapshot(run, label)["displays"][0]["artifact"].replace("\\", "/")
	data = (review_root / HARNESS_DIRECTORY / artifact).read_bytes()
	pixels = data[len(b"P5\n128 32\n255\n"):]
	if len(pixels) != 128 * 32:
		raise ValueError(f"unexpected frame size for {label!r}")
	return b"".join(pixels[row * 128 + columns.start: row * 128 + columns.stop] for row in range(rows.start, rows.stop))


def _same_top_line(review_root: Path, run: dict[str, Any], label: str, reference: str) -> bool:
	"""True when the labelled frame's top text line (rows 0-9, right of the switch grid) equals the reference frame's."""
	region = (slice(0, 10), slice(32, 128))
	return _frame_rows(review_root, run, label, *region) == _frame_rows(review_root, run, reference, *region)


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _observation(label: str, stimulus: list[int], input_address: int, transitioned: list[int]) -> dict[str, Any]:
	record = {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": stimulus,
		"input_address": input_address,
		"input_kind": "switch",
		"label": label,
		"observed_switch_addresses": [],
		"result": "observed",
		"transitioned_solenoid_addresses": transitioned,
	}
	return record


def _command(name: str, mechanics: int, detail: str) -> str:
	return (
		f"python tools/run_pinmame_harness.py --library <libpinmame> --game {GAME} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		f"--handle-mechanics {mechanics} --scenario {SCENARIO_DIRECTORY}/{name}.json --dmd-dir <external-dmd-dir> --output <external-run.json>. "
		+ detail
	)


def _document(review_root: Path, name: str, run: dict[str, Any], observations: dict[str, Any], detail: str) -> dict[str, Any]:
	manifest_sha, mechanics = RUNS[name]
	run_sha = _sha256(review_root / HARNESS_DIRECTORY / name / "run.json")
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/demolition_man_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": _command(name, mechanics, detail),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": name,
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{name}/run.json",
					"scenario_path": f"{SCENARIO_DIRECTORY}/{name}.json",
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"sha256": run_sha,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": f"{ATTRIBUTION} Exact external directory manifest {name}/manifest.json SHA-256 {manifest_sha}.",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{name}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"sha256": run_sha,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def build_edges(review_root: Path) -> dict[str, Any]:
	name = "dm-switch-edges"
	run = _load_run(review_root, name)
	idle = "T.1 started, every swept switch at public 0"
	snapshots = [
		_diagnostic(run, "Enter 4 (towards MAIN MENU)", "MAIN MENU / B. BOOKKEEPING"),
		_diagnostic(run, idle, "SWITCH EDGES / T1"),
	]
	named = []
	for address in EDGE_MATRIX:
		level = 0 if address in NAMED_AT_ZERO else 1
		named_label, other_label = f"{address} -> {level}", f"{address} -> {1 - level}"
		if _same_top_line(review_root, run, named_label, idle) or not _same_top_line(review_root, run, other_label, idle):
			raise ValueError(f"T.1 must name public {address} at {level} only")
		snapshots.append(_diagnostic(run, named_label, f"{EDGE_NAMES[address]} / T1 LAST SW {address}"))
		named.append(_observation(f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is {level} and clears it at {1 - level}", [address], address, []))
	for address, (text, printed, coils) in FLIPPER_BUTTONS.items():
		rising = _risen(_step(run, f"{address} -> 1"))
		if not set(coils) <= rising:
			raise ValueError(f"the ROM did not fire {coils} for public {address}: {sorted(rising)}")
		snapshots.append(_diagnostic(run, f"{address} -> 1", f"{text} / T1 LAST SW {printed}"))
		named.append(_observation(
			f"T.1 with host public {address} set to 1: the ROM fires public {', '.join(str(coil) for coil in coils)} and names {printed} ({text}) from the synthesized end-of-stroke bit",
			[address], address, sorted(rising),
		))
	for address in FLIPPER_EOS:
		step = _step(run, f"{address} -> 1")
		if _risen(step) or not _same_top_line(review_root, run, f"{address} -> 1", f"{address} -> 0") or not _same_top_line(review_root, run, f"{address} -> 1", idle):
			raise ValueError(f"a host write to end-of-stroke address {address} must change nothing the ROM shows")
		named.append(_observation(
			f"T.1 with host public {address} set to 1 and back: the ROM names nothing and fires nothing (host read-back {step['observed_state']})",
			[address], address, [],
		))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Built-in mechanisms stay disabled, so the power-up report adds CLAW MOTOR ERROR screens and four Enters reach the main menu. "
		"Each set_switch holds one public level for 1.5 s; the snapshot after it records the ROM's T.1 display. The ROM names a switch on "
		"its top line while it reads the switch as active."
	)
	return _document(review_root, name, run, observations, detail)


def build_claw_test(review_root: Path) -> dict[str, Any]:
	name = "dm-claw-test"
	run = _load_run(review_root, name)
	idle = "T.14 started, every claw switch at public 0"
	snapshots = [_diagnostic(run, idle, "CLAW TEST / AUTO RUN / no box marked")]
	named = []
	for address, box in CLAW_BOXES.items():
		frame = lambda label: _snapshot(run, label)["displays"][0]["pixel_sha256"]
		if frame(f"{address} -> 1") == frame(idle) or frame(f"{address} -> 0") != frame(idle):
			raise ValueError(f"T.14 must mark {box} only while public {address} is 1")
		snapshots.append(_diagnostic(run, f"{address} -> 1", f"CLAW TEST / AUTO RUN / X in the {box} box"))
		named.append(_observation(f"T.14 marks the {box} box (activated, blocked) while host public {address} is 1 and clears it at 0", [address], address, []))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Built-in mechanisms stay disabled (four Enters reach the main menu). T.14 draws an X in the box of each claw or elevator opto "
		"the ROM reads as activated (blocked); each opto is driven to public 1 and back to 0 for 2 s. The scenario then holds Enter on "
		"the test's functions, which stop at ELEVATOR ERROR without the simulated elevator; dm-claw-functions repeats them."
	)
	return _document(review_root, name, run, observations, detail)


def build_claw_functions(review_root: Path) -> dict[str, Any]:
	name = "dm-claw-functions"
	run = _load_run(review_root, name)
	snapshots = []
	named = []
	for index, text, outputs in CLAW_FUNCTIONS:
		risen = _risen(_step(run, f"hold Enter on function {index}"))
		if risen != set(outputs):
			raise ValueError(f"T.14 {text} drove {sorted(risen)}, not {sorted(outputs)}")
		snapshots.append(_diagnostic(run, f"hold Enter on function {index} (held)", f"CLAW TEST / {text} (inverted while running)"))
		named.append(_observation(f"T.14 {text} held for 3 s: the ROM drives public {sorted(outputs) if outputs else 'nothing (the claw already rests at its left switch)'}", [8], 8, sorted(outputs)))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Built-in mechanisms 0-3 are enabled so PinMAME's claw and elevator model reports 25, 26, 67 and 74; two Enters reach the main "
		"menu. Each claw-test function runs only while Enter is held (3 s); the run records the outputs the ROM drives meanwhile. "
		"CLAW RIGHT drives 19 and 20 together (the ROM pulses both lines); the smoothed solenoid states do not show the duty split."
	)
	return _document(review_root, name, run, observations, detail)


def _walk(run: dict[str, Any], rows: tuple, pulse_step: dict[int, str] | None, label_format: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
	snapshots, named = [], []
	for index, (address, label, text) in enumerate(rows):
		step_label = pulse_step[address] if pulse_step else label
		risen = _risen(_step(run, step_label))
		if address not in risen:
			raise ValueError(f"{step_label} did not pulse public {address}: {sorted(risen)}")
		snapshots.append(_diagnostic(run, label, text))
		named.append(_observation(label_format.format(address=address, text=text.split(" / ")[0]), [8 if index == 0 else 7], 8 if index == 0 else 7, [address]))
	return snapshots, named


def build_solenoids(review_root: Path) -> dict[str, Any]:
	name = "dm-solenoid-test"
	run = _load_run(review_root, name)
	snapshots, named = _walk(run, T4, T4_PULSE_STEP, "T.4 SOLENOID TEST selects public {address} ({text}): the ROM pulses it repeatedly")
	walk = set().union(*(_risen(step) for step in run["steps"] if step["label"].startswith("T.4 ")))
	if {17, 18, 19, 20} & walk:
		raise ValueError("T.4 must not pulse the flasher and motor drivers 17-20")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Each Up press selects the next driver; in REPEAT mode the ROM pulses it until the next press. The walk covers 1-16, 33 and 34 "
		"and then returns to 1; it never selects 17-20, which T.5 and T.14 drive."
	)
	return _document(review_root, name, run, observations, detail)


def build_flashers(review_root: Path) -> dict[str, Any]:
	name = "dm-flasher-test"
	run = _load_run(review_root, name)
	snapshots, named = _walk(run, T5, None, "T.5 FLASHER TEST selects public {address} ({text}): the ROM pulses it repeatedly")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Each Up press selects the next flasher. The ROM prints the manual's numbers 37-44 for the auxiliary 8-driver flashers while it "
		"pulses public 51-58, which is PinMAME's dm_getSol custom-output range (CORE_CUSTSOLNO 1-8, WPC_EXTBOARD1 bits 0-7)."
	)
	return _document(review_root, name, run, observations, detail)


def build_gi(review_root: Path) -> dict[str, Any]:
	name = "dm-gi-test"
	run = _load_run(review_root, name)
	snapshots, named = [], []
	for strings, label, text in T6:
		risen = _risen(_step(run, label), "gis")
		if risen != set(strings):
			raise ValueError(f"T.6 {label} changed {sorted(risen)}, not {sorted(strings)}")
		snapshots.append(_diagnostic(run, label, text))
		named.append(_observation(f"T.6 {text.split(' / ')[0]}: the ROM steps the brightness of public G.I. {', '.join(str(item) for item in strings)}", [7], 7, []))
	gis = sorted({event["number"] for event in run["events"] if event["event"] == "gi"})
	observations = {"diagnostic_snapshots": snapshots, "gi_addresses_seen": gis, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Up raises the selected brightness one step and, past BRIGHT=8, moves to the next selection (ALL ILLUMINATION, then each "
		"string in order); the run records which public G.I. outputs change at each press."
	)
	return _document(review_root, name, run, observations, detail)


def build_flippers(review_root: Path) -> dict[str, Any]:
	name = "dm-flipper-coil-test"
	run = _load_run(review_root, name)
	snapshots, named = [], []
	for index, (outputs, label, text) in enumerate(T12):
		risen = _risen(_step(run, label))
		if not set(outputs) <= risen:
			raise ValueError(f"T.12 {label} did not pulse {outputs}: {sorted(risen)}")
		snapshots.append(_diagnostic(run, label, text))
		named.append(_observation(f"T.12 FLIPPER COIL selects {text.split(' / ')[0]}: the ROM pulses public {outputs[0]}", [8 if index == 0 else 7], 8 if index == 0 else 7, list(outputs)))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	detail = (
		"Each Up press selects the next winding; the ROM numbers them 01-04, 07 and 08 (the Fliptronic positions) and skips the upper "
		"right pair, whose power line drives the claw magnet. A step can also show the previous winding's last pulse."
	)
	return _document(review_root, name, run, observations, detail)


def build_lamps(review_root: Path) -> dict[str, Any]:
	name = "dm-single-lamps"
	run = _load_run(review_root, name)
	snapshots, named = [], []
	for index, address in enumerate(LAMP_ORDER):
		position = (index + 63) % 64 + 1
		label = f"T.8 Up {position}"
		lit = _risen(_step(run, label), "lamps")
		if address not in lit:
			raise ValueError(f"{label} did not light public lamp {address}: {sorted(lit)}")
		snapshots.append(_diagnostic(run, f"{label} (held)", f"{LAMP_NAMES[address]} / T.8 {index + 1:02d} LAMP {address}"))
		named.append(_observation(f"T.8 SINGLE LAMPS selects lamp {index + 1:02d} ({LAMP_NAMES[address]}): the ROM lights public lamp {address}", [7], 7, []))
	lamps = sorted({event["number"] for event in run["events"] if event["event"] == "lamp" and event["state"]})
	observations = {
		"diagnostic_snapshots": snapshots,
		"lamp_addresses_seen": lamps,
		"named_action_observations": named,
		"named_output_addresses": {f"lamp-{index + 1:02d}": address for index, address in enumerate(LAMP_ORDER)},
		"solenoid_addresses_seen": _seen(run),
	}
	detail = (
		"T.8 starts on lamp 01 (public 11); each Up press selects the next lamp in column-row order and the frame taken while the press "
		"is held shows its name (the name blinks). Press 64 wraps back to public 11, which is where the walk reads lamp 11."
	)
	return _document(review_root, name, run, observations, detail)


BUILDERS = {
	"demolition-man-dm-lx4-switch-edges.json": build_edges,
	"demolition-man-dm-lx4-claw-test.json": build_claw_test,
	"demolition-man-dm-lx4-claw-functions.json": build_claw_functions,
	"demolition-man-dm-lx4-solenoid-test.json": build_solenoids,
	"demolition-man-dm-lx4-flasher-test.json": build_flashers,
	"demolition-man-dm-lx4-gi-test.json": build_gi,
	"demolition-man-dm-lx4-flipper-coil-test.json": build_flippers,
	"demolition-man-dm-lx4-single-lamps.json": build_lamps,
}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="refuse drift instead of writing")
	args = parser.parse_args()
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required")
	review_root = Path(value)
	for filename, builder in BUILDERS.items():
		document = builder(review_root)
		path = EVIDENCE_DIRECTORY / filename
		if args.check:
			if not path.is_file() or path.read_bytes() != canonical_bytes(document):
				raise SystemExit(f"runtime evidence drift: {path}")
		else:
			write_json(path, document)
	print("checked" if args.check else "written", len(BUILDERS))


if __name__ == "__main__":
	main()
