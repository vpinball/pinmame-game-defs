"""Build Breakshot's compact service-diagnostic evidence from the retained bsv103 harness runs.

The four runs (Switch Test, Solenoid Test, Lamp Test and a short gameplay check) stay outside Git
under the review-artifacts root. ``tools/seeds/capcom/breakshot-1996-service-readings.json`` pins,
for every DMD frame this record cites, the frame's pixel digest and the curator's literal reading of
it, and for every cited step the solenoid addresses that went active and those that only released.
This builder refuses to write unless each retained run still matches its committed scenario, each
cited frame's retained image still hashes to the pinned digest, and each cited step still fires and
releases the pinned addresses; it then writes
``evidence/runtime/capcom/breakshot-service-diagnostics.json``.

``--check`` compares the committed evidence with a fresh build; both need
``PINMAME_REVIEW_ARTIFACTS_ROOT``. ``check_seed_against_evidence`` needs no external root: it proves
the committed evidence carries exactly the seed's readings, digests and fired addresses.
``render_service_excerpt`` renders the seed's readings as the machine's service-test excerpt, and
``check_service_excerpt`` proves the committed excerpt is that rendering.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "tools/seeds/capcom/breakshot-1996-service-readings.json"
EVIDENCE_PATH = ROOT / "evidence/runtime/capcom/breakshot-service-diagnostics.json"
SERVICE_EXCERPT_PATH = ROOT / "evidence/excerpts/capcom.breakshot.1996/service-tests.md"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "7ce04ac647167a5fb15e0391099e8d0a52b93f91be467906c8d52d2eccb389b8"
COMMAND_TEMPLATE = (
	"python tools/run_pinmame_harness.py --library <release-libpinmame built from 46e1a01a> --game bsv103 "
	"--rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/capcom/bsv103-<name>.json "
	"--dmd-dir <external-frame-dir> --output <external-run.json>"
)
MANIFEST_ALGORITHM = (
	"SHA-256 of the compact JSON object mapping each raw_runs name to its run.json SHA-256 "
	"(keys sorted, separators ',' and ':')"
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def load_seed() -> dict[str, Any]:
	seed = load_json(SEED_PATH)
	if SEED_PATH.read_bytes() != canonical_bytes(seed):
		raise ValueError(f"{SEED_PATH} is not in canonical byte format")
	if seed.get("format") != "pinmame-service-readings" or seed.get("machine_id") != "capcom.breakshot.1996":
		raise ValueError("not the Breakshot service-readings seed")
	return seed


def _snapshot(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [snapshot for snapshot in run["snapshots"] if snapshot["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one snapshot labelled {label!r}, found {len(matches)}")
	return matches[0]


def _step(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [step for step in run["steps"] if step["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def frame_pixel_readings(run_dir: Path, display: dict[str, Any]) -> list[bytes]:
	"""The raw DMD pixels a retained PGM frame can stand for, as the harness hashed them.

	The harness writes each frame as ``P5``: scaled to 0-255 when every pixel fits the layout's depth,
	and unscaled when one does not. A stored frame whose values all lie on the scaled grid but whose
	maximum exceeds the depth can therefore be either, and the run's recorded digest tells them apart.
	The frame is found by its file name under the run's own ``dmd`` folder, so a moved
	review-artifacts root still resolves.
	"""
	path = run_dir / "dmd" / PureWindowsPath(display["artifact"]).name
	data = path.read_bytes()
	layout = display["layout"]
	header = f"P5\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
	if not data.startswith(header) or len(data) != len(header) + layout["width"] * layout["height"]:
		raise ValueError(f"{path}: not a {layout['width']}x{layout['height']} harness PGM frame")
	grey = data[len(header):]
	max_level = max((1 << max(int(layout.get("depth", 1)), 1)) - 1, 1)
	levels = {round(level * 255 / max_level): level for level in range(max_level + 1)}
	readings = [grey] if max(grey, default=0) > max_level else []
	if all(value in levels for value in grey):
		readings.append(bytes(levels[value] for value in grey))
	return readings


def frame_digest(run_dir: Path, snapshot: dict[str, Any]) -> str:
	"""Hash the retained frame itself and require it to be the frame run.json records."""
	display = snapshot["displays"][0]
	digests = {hashlib.sha256(pixels).hexdigest() for pixels in frame_pixel_readings(run_dir, display)}
	if display["pixel_sha256"] not in digests:
		raise ValueError(f"frame {snapshot['label']!r}: the retained image does not match the digest its run records")
	return display["pixel_sha256"]


def _fired(step: dict[str, Any]) -> list[int]:
	"""Solenoid addresses that went active during the step."""
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if any(state for state in t["states"])})


def _released(step: dict[str, Any]) -> list[int]:
	"""Solenoid addresses whose only change during the step was back to off."""
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if not any(state for state in t["states"])})


def load_runs(review_root: Path, seed: dict[str, Any]) -> dict[str, tuple[dict[str, Any], str]]:
	runs = {}
	for name, item in sorted(seed["runs"].items()):
		path = review_root / item["retained"] / "run.json"
		run = load_json(path)
		scenario = ROOT / item["scenario"]
		if run["game"] != seed["game"] or run["failure"] is not None:
			raise ValueError(f"{path}: not a completed {seed['game']} run")
		if run["scenario"]["sha256"] != _sha256(scenario):
			raise ValueError(f"{path}: ran a different scenario than {item['scenario']}")
		if run["library_sha256"] != LIBRARY_SHA256:
			raise ValueError(f"{path}: produced by an unpinned LibPinMAME build")
		runs[name] = (run, _sha256(path))
	return runs


def _check_frame(run: dict[str, Any], run_dir: Path, item: dict[str, Any], label: str) -> dict[str, Any]:
	snapshot = _snapshot(run, label)
	if frame_digest(run_dir, snapshot) != item["pixel_sha256"]:
		raise ValueError(f"frame {label!r} no longer has the pinned digest")
	return snapshot


def build(review_root: Path) -> bytes:
	seed = load_seed()
	runs = load_runs(review_root, seed)
	names = [f"bsv103-{n}" for n in ("switch-test", "solenoid-test", "lamp-test", "gameplay")]
	switch_run, solenoid_run, lamp_run, gameplay_run = (runs[name][0] for name in names)
	switch_dir, solenoid_dir, lamp_dir, gameplay_dir = (review_root / seed["runs"][name]["retained"] for name in names)
	snapshots = []
	for item in seed["switch_test"]:
		snapshot = _check_frame(switch_run, switch_dir, item, item["snapshot"])
		if item["reading"] is None:
			previous = switch_run["snapshots"][switch_run["snapshots"].index(snapshot) - 1]
			unchanged = frame_digest(switch_dir, previous) == item["pixel_sha256"]
			if unchanged != (item["display"] == "unchanged"):
				raise ValueError(f"switch {item['public']}: the recorded display change does not reproduce")
			text = ("no response: the frame is identical to the one before the switch closed" if unchanged else
			        "the name panel still names the previously tested switch; only the switch grid changes")
		else:
			text = item["reading"]
		snapshots.append({"label": f"switch test, public {item['public']} held: {item['snapshot']}", "display_index": 0,
		                  "pixel_sha256": item["pixel_sha256"], "nonzero_pixels": snapshot["displays"][0]["nonzero_pixels"],
		                  "interpreted_text": text, "active_solenoid_addresses": []})
	for item in seed["solenoid_test"]:
		snapshot = _check_frame(solenoid_run, solenoid_dir, item, item["snapshot"])
		if _fired(_step(solenoid_run, item["fire_step"])) != item["fired"]:
			raise ValueError(f"solenoid test S{item['public']:02d}: the fired addresses do not reproduce")
		snapshots.append({"label": f"solenoid test, S{item['public']:02d} selected: {item['snapshot']}; fired on {item['fire_step']}",
		                  "display_index": 0, "pixel_sha256": item["pixel_sha256"],
		                  "nonzero_pixels": snapshot["displays"][0]["nonzero_pixels"],
		                  "interpreted_text": item["reading"], "active_solenoid_addresses": item["fired"]})
	for item in seed["lamp_test"]:
		snapshot = _check_frame(lamp_run, lamp_dir, item, item["snapshot"])
		snapshots.append({"label": f"lamp test, public {item['public']}: {item['snapshot']}", "display_index": 0,
		                  "pixel_sha256": item["pixel_sha256"], "nonzero_pixels": snapshot["displays"][0]["nonzero_pixels"],
		                  "interpreted_text": item["reading"], "active_solenoid_addresses": []})
	actions = []
	scenario_actions = load_json(ROOT / seed["runs"]["bsv103-gameplay"]["scenario"])["actions"]
	by_label = {action["label"]: action for action in scenario_actions}
	for item in seed["gameplay"]:
		step = _step(gameplay_run, item["step"])
		_check_frame(gameplay_run, gameplay_dir, item, item["step"])
		if _fired(step) != item["fired"] or _released(step) != item["released"]:
			raise ValueError(f"gameplay step {item['step']!r}: the fired or released addresses do not reproduce")
		transitioned = sorted(set(item["fired"]) | set(item["released"]))
		action = by_label[item["step"]]
		if "switch" not in action:
			# The boot wait has no input; its frame and power-on pulses are a diagnostic snapshot.
			snapshots.append({"label": f"gameplay run: {item['step']}", "display_index": 0, "pixel_sha256": item["pixel_sha256"],
			                  "interpreted_text": item["reading"], "active_solenoid_addresses": item["fired"]})
			continue
		actions.append({"label": item["step"] + (f"; DMD: {item['reading']}" if "reading" in item else ""),
		                "input_kind": "switch", "input_address": action["switch"],
		                "host_stimulus_switch_addresses": [action["switch"]], "observed_switch_addresses": [],
		                "active_solenoid_addresses": item["fired"], "transitioned_solenoid_addresses": transitioned,
		                "result": "observed" if transitioned or "reading" in item else "no_matching_transition"})
	solenoids = sorted({n for _, item in [(0, i) for i in seed["solenoid_test"]] for n in item["fired"]} |
	                   {n for item in seed["gameplay"] for n in item["fired"]})
	layouts = sorted({json.dumps({k: d["layout"][k] for k in ("type", "width", "height", "depth")}, sort_keys=True)
	                  for run, _ in runs.values() for s in run["snapshots"] for d in s["displays"]})
	run_digests = {name: digest for name, (_, digest) in runs.items()}
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "tools/build_breakshot_runtime_evidence.py", "version": 1},
		"source": {
			"kind": "service_diagnostic",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"path": "external:pinmame-review-artifacts/breakshot-1996/harness-runs",
			"sha256": hashlib.sha256(json.dumps(run_digests, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
			"manifest_algorithm": MANIFEST_ALGORITHM,
			"license": "NOASSERTION",
			"attribution": "Capcom Coin-Op bsv103 service menu, executed locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
			"quality": "validated",
		},
		"driver_ids": ["bsv103"],
		"machine_ids": ["capcom.breakshot.1996"],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": "bsv103",
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"command_template": COMMAND_TEMPLATE,
			"raw_runs": [
				{
					"name": name,
					"sha256": digest,
					"scenario_path": seed["runs"][name]["scenario"],
					"scenario_sha256": run["scenario"]["sha256"],
					"action_count": run["scenario"]["action_count"],
					"watch_switches": run["watch_switches"],
					"self_test_pulses": 0,
					"nvram_initialization": "empty isolated state directory",
					"snapshot_count": len(run["snapshots"]),
					**({"initial_switches": [{"switch": s["switch"], "state": s["state"]} for s in run["initial_switches"]]} if run["initial_switches"] else {}),
				}
				for name, (run, digest) in sorted(runs.items())
			],
			"observations": {
				"service_language": "English",
				"display_indices_seen": [0],
				"display_layouts_seen": [json.loads(layout) for layout in layouts],
				"solenoid_addresses_seen": solenoids,
				"lamp_addresses_seen": [item["public"] for item in seed["lamp_test"]],
				"diagnostic_snapshots": snapshots,
				"runs": {"bsv103-gameplay": {"named_action_observations": actions}},
			},
		},
	}
	return canonical_bytes(evidence)


def check_seed_against_evidence() -> None:
	"""Without external roots: the committed evidence carries exactly the seed's pinned readings."""
	seed = load_seed()
	evidence = load_json(EVIDENCE_PATH)
	if EVIDENCE_PATH.read_bytes() != canonical_bytes(evidence):
		raise ValueError(f"{EVIDENCE_PATH} is not in canonical byte format")
	snapshots = evidence["runtime"]["observations"]["diagnostic_snapshots"]
	expected = ([(item["pixel_sha256"], item["reading"]) for item in seed["switch_test"] if item["reading"] is not None] +
	            [(item["pixel_sha256"], item["reading"]) for item in seed["solenoid_test"] + seed["lamp_test"]])
	actual = {(s["pixel_sha256"], s["interpreted_text"]) for s in snapshots}
	missing = [pair for pair in expected if pair not in actual]
	if missing:
		raise ValueError(f"evidence lacks pinned readings: {missing[:3]}")
	for item in seed["solenoid_test"]:
		if not any(s["pixel_sha256"] == item["pixel_sha256"] and s["active_solenoid_addresses"] == item["fired"] for s in snapshots):
			raise ValueError(f"evidence lacks the fired addresses of S{item['public']:02d}")
	actions = evidence["runtime"]["observations"]["runs"]["bsv103-gameplay"]["named_action_observations"]
	steps = {a["label"].split("; DMD: ")[0]: (a["active_solenoid_addresses"], a["transitioned_solenoid_addresses"]) for a in actions}
	steps.update({s["label"].removeprefix("gameplay run: "): (s["active_solenoid_addresses"], s["active_solenoid_addresses"])
	              for s in snapshots if s["label"].startswith("gameplay run: ")})
	if steps != {item["step"]: (item["fired"], sorted(set(item["fired"]) | set(item["released"]))) for item in seed["gameplay"]}:
		raise ValueError("evidence gameplay transitions differ from the seed")


def render_service_excerpt(seed: dict[str, Any]) -> bytes:
	"""The committed service-test excerpt: every reading the seed pins, in test order."""
	lines = [
		"# Breakshot — ROM service tests (bsv103)",
		"",
		"Read from the ROM's own service menu, run on LibPinMAME by the four retained harness runs the seed",
		"`tools/seeds/capcom/breakshot-1996-service-readings.json` names. Each row pairs the public address the",
		"step drove or that changed with the 128x32 DMD frame shown at that step. The text is literal, with ` / `",
		"between display lines; `Frame` is the first 16 hex digits of the frame's pixel SHA-256 (the seed and",
		f"`evidence/runtime/capcom/breakshot-service-diagnostics.json` carry the full digests). {seed['read_by']['method'][0].upper()}{seed['read_by']['method'][1:]}.",
		"",
		"## Switch Test",
		"",
		"Each public switch held at 1 on its own while the test was showing. `unchanged` means the frame equals the",
		"previous step's; `name panel unchanged` means only the switch grid changed and the test named nothing.",
		"",
		"| Public | Display | Frame |",
		"| ---: | --- | --- |",
	]
	for item in seed["switch_test"]:
		text = item["reading"] if item["reading"] is not None else item["display"].replace("_", " ")
		lines.append(f"| {item['public']} | {text} | `{item['pixel_sha256'][:16]}` |")
	lines += [
		"",
		"## Solenoid Test",
		"",
		"Each coil selected with the right flipper button and fired with Start. `Fired` lists the public solenoid",
		"addresses that went active on the fire step.",
		"",
		"| Public | Display | Fired | Frame |",
		"| ---: | --- | --- | --- |",
	]
	for item in seed["solenoid_test"]:
		fired = ", ".join(str(n) for n in item["fired"])
		lines.append(f"| {item['public']} | {item['reading']} | {fired} | `{item['pixel_sha256'][:16]}` |")
	lines += [
		"",
		"## Lamp Test",
		"",
		"The single-lamp walk; at each step only the listed public lamp was lit.",
		"",
		"| Public | Display | Frame |",
		"| ---: | --- | --- |",
	]
	for item in seed["lamp_test"]:
		lines.append(f"| {item['public']} | {item['reading']} | `{item['pixel_sha256'][:16]}` |")
	lines += [
		"",
		"## Gameplay check",
		"",
		"A short game on fresh state: boot, coins, Start, the shooter lane, both drop banks, the tilt bob and the",
		"slam tilt. `Fired` lists the public solenoid addresses that went active during the step and `Released`",
		"those whose only change was back to off; a dash means none.",
		"",
		"| Step | Display | Fired | Released | Frame |",
		"| --- | --- | --- | --- | --- |",
	]
	for item in seed["gameplay"]:
		fired = ", ".join(str(n) for n in item["fired"]) or "-"
		released = ", ".join(str(n) for n in item["released"]) or "-"
		lines.append(f"| {item['step']} | {item.get('reading', '')} | {fired} | {released} | `{item['pixel_sha256'][:16]}` |")
	return ("\n".join(lines) + "\n").encode("utf-8")


def check_service_excerpt() -> None:
	if not SERVICE_EXCERPT_PATH.is_file() or SERVICE_EXCERPT_PATH.read_bytes() != render_service_excerpt(load_seed()):
		raise ValueError(f"{SERVICE_EXCERPT_PATH} differs from the seed's rendering")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--write", action="store_true")
	args = parser.parse_args()
	root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	try:
		if not root:
			raise ValueError("PINMAME_REVIEW_ARTIFACTS_ROOT is required to read the retained runs")
		payload = build(Path(root))
		if args.write:
			EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
			EVIDENCE_PATH.write_bytes(payload)
			SERVICE_EXCERPT_PATH.write_bytes(render_service_excerpt(load_seed()))
			print(f"Wrote {EVIDENCE_PATH} and {SERVICE_EXCERPT_PATH}")
		elif not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != payload:
			raise ValueError(f"{EVIDENCE_PATH} differs from a fresh build")
		else:
			check_seed_against_evidence()
			check_service_excerpt()
			print("Breakshot runtime evidence matches the retained runs")
	except (OSError, ValueError, KeyError) as exc:
		parser.exit(1, f"{exc}\n")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
