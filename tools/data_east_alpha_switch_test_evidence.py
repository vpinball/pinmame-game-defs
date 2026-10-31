"""Derive compact Data East alphanumeric Switch Test name evidence from retained raw harness runs.

Each document reads two successful runs of one committed scenario on the pinned LibPinMAME build (``run-a`` and ``run-b``
under the external review-artifacts root), checks that they ran that scenario and the pinned binary, decodes every held
reading from the raw sixteen-segment values, and writes the names the ROM printed for each probed public switch address. The
ROM archive digest it records is a constant; tests/test_data_east_alpha_switch_test_evidence.py compares it with the
archive in the configured ROM library when PINMAME_ROM_LIBRARY_ROOT is set.

The undated compact JSON documents are immutable archival baselines. Their source locators and checker notes describe the
earlier campaign, whose original raw runs are unavailable; this tool reproduces only the dated successor documents and compares
their readings with those baselines. Matching readings do not reproduce or independently authenticate the unavailable runs.

On the earlier 97aa922b build the alphanumeric Switch Test kept the last name on screen after a switch opened, so a reading
could belong to the previous closure. In two fresh runs per game on 46e1a01a, every 3-second probe showed a reading distinct
from its preceding reference and both runs agreed. As a conservative safeguard, each probe still follows a different named
reference closure, and the tool refuses unstable reference readings. A probe repeating the reference text has no name of its
own. Both runs must give the same readings.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes, write_json  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS, SEGMENT_16_DISPLAY_TYPES  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
SESSION = "ci-pr-sweep-20261031/pr47-reproduction"
RUNS = ("run-a", "run-b")
SCENARIO_DIRECTORY = ROOT / "tools/harness-scenarios/data-east"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/data-east"
TITLE = "SWITCH TEST"
ATTRIBUTION = (
	"Successor runs generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. "
	"The original compact readings are preserved, but their original raw traces are unavailable. "
	"Both successor runs reproduce those readings. The successor ROM archives differ from the original archives; their members match "
	"the pinned driver. Public switch writes are "
	"host stimuli, never ROM observations. Display text is decoded from the harness's raw sixteen-segment values; the ROM's font "
	"draws O and 0 alike, so a reading keeps the letter the harness table assigns."
)
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact UTF-8 bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF; it lists every file below source.path except manifest.json and "
	"manifest.sha256 as {path, sha256, size}, using sorted POSIX-relative paths."
)
RECORD_SCRIPT_SHA256 = "c85c17b48b359b87a8590712600de6f97f93881f3241b16fa6a2be3ef230eb8f"
RUNNER_SHA256 = "d49868dada8e2b58ca8e8540a1f3af002ff22e321dbc79ab18c72909a8e2d3ce"
NVRAM_NOTE = (
	"empty: this run's retained record.py created a new state directory, checked its initial entries, and recorded the result in "
	"preflight.json; the harness itself does not check that the state directory was empty"
)


@dataclass(frozen=True)
class Game:
	game: str
	machine_id: str
	slug: str
	output: str
	scenario: str
	reference: int
	alternate: int
	flipper_pair: tuple[int, int]
	flipper_macro: str
	rom_archive_sha256: str

	@property
	def probes(self) -> list[int]:
		return [address for address in range(9, 65) if address not in self.flipper_pair]

	@property
	def directory(self) -> str:
		return f"{SESSION}/{self.game}"


GAMES = {
	"lwar_a83": Game(
		game="lwar_a83",
		machine_id="data-east.laser-war.1987",
		slug="laser-war-1987",
		output="laser-war-lwar_a83-switch-test-names-2026-10-31.json",
		scenario="lwar-a83-switch-test-names",
		reference=9,
		alternate=13,
		flipper_pair=(46, 47),
		flipper_macro="FLIP4746",
		rom_archive_sha256="05a8823b54f42fadcc0efe801d727e58e2345a0b5ad205fcc49eda0456b87da1",
	),
	"ssvc_a26": Game(
		game="ssvc_a26",
		machine_id="data-east.secret-service.1988",
		slug="secret-service-1988",
		output="secret-service-ssvc_a26-switch-test-names-2026-10-31.json",
		scenario="ssvc-a26-switch-test-names",
		reference=17,
		alternate=9,
		flipper_pair=(30, 31),
		flipper_macro="FLIP3031",
		rom_archive_sha256="9d78757d36ae1900d76edb59e91a6166121d1c82a02cc15ce52b66b7d8e2b3a5",
	),
}

REFERENCE_LABEL = re.compile(r"^reference (\d+) before (\d+) \(held\)$")
PROBE_LABEL = re.compile(r"^announce switch (\d+) \(held\)$")


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path, game: Game) -> dict[str, Any]:
	if _sha256(directory / "record.py") != RECORD_SCRIPT_SHA256:
		raise ValueError(f"recording script changed: {directory}")
	preflight = json.loads((directory / "preflight.json").read_bytes())
	result = json.loads((directory / "result.json").read_bytes())
	if preflight.get("initial_state_entries") != [] or preflight.get("initial_state_manifest_sha256") != hashlib.sha256(b"[]").hexdigest():
		raise ValueError(f"initial state was not empty: {directory}")
	if result.get("exit_code") != 0 or result.get("timeout") is not False:
		raise ValueError(f"recorded run failed or timed out: {directory}")
	if (preflight.get("library_sha256") != LIBRARY_SHA256 or preflight.get("rom_archive_sha256") != game.rom_archive_sha256
			or preflight.get("runner_sha256") != RUNNER_SHA256):
		raise ValueError(f"recorded inputs differ from pinned inputs: {directory}")
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = SCENARIO_DIRECTORY / f"{game.scenario}.json"
	if run.get("failure") is not None or run.get("game") != game.game:
		raise ValueError(f"not a successful {game.game} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if (run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path)
			or preflight.get("scenario_sha256") != _sha256(scenario_path)):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0 or run.get("initial_switches") != []:
		raise ValueError(f"built-in mechanisms and initial switches must be off: {run_path}")
	return run


def _rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
	"""The player rows the Switch Test writes to: every sixteen-segment display, in index order."""
	rows = [item for item in snapshot["displays"] if item["layout"]["type"] & 0x1F in SEGMENT_16_DISPLAY_TYPES]
	if [item["index"] for item in rows] != [0, 1]:
		raise ValueError(f"snapshot {snapshot['label']!r} must carry exactly the two sixteen-segment rows 0 and 1")
	return sorted(rows, key=lambda item: item["index"])


def _decode(row: dict[str, Any]) -> str:
	text = "".join(SEGMENT_16_CHARACTERS.get(value, "?") for value in row["segments"])
	if "?" in text:
		raise ValueError(f"undecodable segment value in {row['segments']}")
	if row.get("text") != text:
		raise ValueError(f"recorded text {row.get('text')!r} differs from the decoded segments {text!r}")
	return text


def _reading(snapshot: dict[str, Any]) -> str:
	return re.sub(r"\s+", " ", " ".join(_decode(row) for row in _rows(snapshot))).strip()


def _responses(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
	return [
		{
			"decoded_segment_positions": list(range(len(row["segments"]))),
			"display_index": row["index"],
			"interpreted_text": _decode(row),
			"segments": row["segments"],
			"snapshot_label": snapshot["label"],
		}
		for row in _rows(snapshot)
	]


def _checkpoint(run: dict[str, Any]) -> dict[str, Any]:
	green = [step for step in run["steps"] if step["label"] == "toggle Green once"]
	black = [step for step in run["steps"] if step["label"] == "advance to Switch Test"]
	if len(green) != 1 or len(black) != 1 or black[0].get("matched_text") != TITLE:
		raise ValueError("the run did not reach the Switch Test title")
	return {"after_service_pulses": 1 + black[0]["pulses"], "matched_text": TITLE}


def derive(run: dict[str, Any], game: Game) -> tuple[dict[int, str], dict[str, Any]]:
	"""Readings per probed address, and the run's observation block."""
	references: dict[int, tuple[int, str]] = {}
	probes: dict[int, dict[str, Any]] = {}
	for snapshot in run["snapshots"]:
		if match := REFERENCE_LABEL.match(snapshot["label"]):
			references[int(match.group(2))] = (int(match.group(1)), _reading(snapshot))
		elif match := PROBE_LABEL.match(snapshot["label"]):
			probes[int(match.group(1))] = snapshot
	if sorted(probes) != game.probes or sorted(references) != game.probes:
		raise ValueError(f"{game.game}: the run does not probe exactly {game.probes}")
	for address, (reference, _) in references.items():
		if reference != (game.alternate if address == game.reference else game.reference):
			raise ValueError(f"{game.game}: probe {address} was preceded by the wrong reference {reference}")
	reference_texts = {
		reference: {text for (closed, text) in references.values() if closed == reference}
		for reference in (game.reference, game.alternate)
	}
	if any(len(texts) != 1 for texts in reference_texts.values()):
		raise ValueError(f"{game.game}: a reference closure read more than one text {reference_texts}; the readout is not address-driven")
	reference_names = {reference: next(iter(texts)) for reference, texts in reference_texts.items()}
	if not all(reference_names.values()) or reference_names[game.reference] == reference_names[game.alternate]:
		raise ValueError(f"{game.game}: the two reference closures must read two different non-empty names")

	readings: dict[int, str] = {}
	observations = []
	for address in game.probes:
		snapshot = probes[address]
		text = _reading(snapshot)
		reference, before = references[address]
		named = text != before and text != TITLE
		if named:
			readings[address] = text
		label = (
			f"Switch Test, public {address} held 3 s after a 3 s reference closure of public {reference}: the ROM shows {text}"
			if named
			else f"Switch Test, public {address} held 3 s after a 3 s reference closure of public {reference}: the display still shows {text}, so the ROM printed no name of its own"
		)
		observations.append({
			"display_responses": _responses(snapshot),
			"host_stimulus_switch_addresses": [address],
			"input_address": address,
			"input_kind": "switch",
			"label": label,
			"observed_switch_addresses": [],
			"result": "observed" if named else "no_matching_transition",
		})
	others = [address for address in game.probes if address != game.reference]
	note = (
		f"Every one of the {len(others)} reference closures of public {game.reference} read {reference_names[game.reference]} and the one "
		f"of public {game.alternate} (before probing {game.reference}) read {reference_names[game.alternate]}. "
		f"{len(readings)} of {len(game.probes)} probes printed a reading that differs from the reference before them."
	)
	block = {
		"diagnostic_checkpoints": [_checkpoint(run)],
		"limitation": (
			"A reading records the text the ROM prints while one public address is held; it does not prove that a switch is fitted at "
			f"that address. Public {game.flipper_pair[0]} and {game.flipper_pair[1]} were not probed because {game.flipper_macro} "
			"makes them driver-owned copies of the cabinet flipper buttons."
		),
		"named_action_observations": observations,
		"note": note,
	}
	return readings, block


def build_document(review_root: Path, game: Game) -> dict[str, Any]:
	session = review_root / game.directory
	readings_by_run: dict[str, dict[int, str]] = {}
	blocks: dict[str, dict[str, Any]] = {}
	raw_runs = []
	for name in RUNS:
		directory = session / name
		run = _load_run(directory, game)
		readings_by_run[name], blocks[name] = derive(run, game)
		raw_runs.append({
			"action_count": run["scenario"]["action_count"],
			"initial_switches": run["initial_switches"],
			"name": f"{game.scenario}-{name}",
			"nvram_initialization": NVRAM_NOTE,
			"retained_from": f"external:pinmame-review-artifacts/{game.directory}/{name}/run.json",
			"scenario_path": f"tools/harness-scenarios/data-east/{game.scenario}.json",
			"scenario_sha256": run["scenario"]["sha256"],
			"self_test_pulses": blocks[name]["diagnostic_checkpoints"][0]["after_service_pulses"],
			"sha256": _sha256(directory / "run.json"),
			"snapshot_count": len(run["snapshots"]),
			"watch_switches": run["watch_switches"],
		})
	first, second = (readings_by_run[name] for name in RUNS)
	if first != second:
		differing = sorted(address for address in set(first) | set(second) if first.get(address) != second.get(address))
		raise ValueError(f"{game.game}: the two runs disagree at {differing}")
	original = EVIDENCE_DIRECTORY / game.output.replace("-2026-10-31.json", ".json")
	if first != readings(json.loads(original.read_bytes())):
		raise ValueError(f"{game.game}: successor readings differ from the original compact evidence")
	# The second run is cited for its agreement; its per-probe responses repeat the first run's and are not duplicated here.
	second_block = {
		"diagnostic_checkpoints": blocks[RUNS[1]]["diagnostic_checkpoints"],
		"note": (
			f"Independent repeat from its own empty state directory. {blocks[RUNS[1]]['note']} Its reading at every probed address equals "
			f"{RUNS[0]}'s, checked by tools/data_east_alpha_switch_test_evidence.py from both raw runs."
		),
	}
	manifest_digest = manifests.check_manifest(session, game.game)
	command = (
		f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game.game} --rom-path <read-only-rom-root> "
		f"--work-dir <new-isolated-state> --scenario tools/harness-scenarios/data-east/{game.scenario}.json --output <external-run.json>, "
		f"run twice from separate empty state directories. The Green and Black service buttons are the only keyboard inputs; every probe "
		f"is a direct public switch write, held 3 s after a 3 s reference closure of public {game.reference} (public {game.alternate} "
		f"before probing {game.reference}). Each snapshot taken while a switch is held records the two sixteen-segment player rows."
	)
	return {
		"driver_ids": [game.game],
		"extractor": {"id": "tools/data_east_alpha_switch_test_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [game.machine_id],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": game.game,
			"observations": {"runs": {RUNS[0]: blocks[RUNS[0]], RUNS[1]: second_block}},
			"raw_runs": raw_runs,
			"rom_archive_sha256": game.rom_archive_sha256,
		},
		"source": {
			"attribution": ATTRIBUTION,
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": MANIFEST_ALGORITHM,
			"path": f"external:pinmame-review-artifacts/{game.directory}",
			"quality": "observed",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"sha256": manifest_digest,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def readings(document: dict[str, Any]) -> dict[int, str]:
	"""The ROM's name for each probed address, read back from a committed evidence document."""
	result = {}
	for item in document["runtime"]["observations"]["runs"][RUNS[0]]["named_action_observations"]:
		if item["result"] == "observed":
			text = " ".join(response["interpreted_text"] for response in item["display_responses"])
			result[item["input_address"]] = re.sub(r"\s+", " ", text).strip()
	return result


def write(review_root: Path) -> None:
	for game in GAMES.values():
		write_json(EVIDENCE_DIRECTORY / game.output, build_document(review_root, game))


def check(review_root: Path) -> None:
	for game in GAMES.values():
		path = EVIDENCE_DIRECTORY / game.output
		if not path.is_file() or path.read_bytes() != canonical_bytes(build_document(review_root, game)):
			raise ValueError(f"Data East alpha Switch Test evidence drift: {path}")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--review-root", type=Path, default=None)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--write", action="store_true")
	args = parser.parse_args()
	root = args.review_root or (Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT") else None)
	if root is None:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT or --review-root is required")
	if args.write:
		write(root)
	else:
		check(root)
		print("Data East alpha Switch Test evidence matches the retained runs.")


if __name__ == "__main__":
	main()
