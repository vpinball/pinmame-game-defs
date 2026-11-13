from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_robo_war as curator  # noqa: E402
import drawing_callouts  # noqa: E402
from build_external_evidence_manifest import write_manifest  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

EXCERPTS = ROOT / "evidence/excerpts" / curator.MACHINE_ID
SCENARIOS = ROOT / "tools/harness-scenarios/gts80/robo-war-1988"


class RoboWarDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(curator.PARTIAL)
		cls.devices = {(d["binding"]["group"].rsplit(".", 1)[-1], d["binding"]["device"]): d for d in cls.definition["inputs"] + cls.definition["outputs"]}
		cls.by_id = {d["id"]: d for d in cls.definition["inputs"] + cls.definition["outputs"]}
		cls.sources = {s["id"]: s for s in cls.definition["sources"]}

	def test_identity_variants_and_unique_catalog_claim(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("Robo-War", "Gottlieb", 1988, "714", 1975, "GryK3-MQrWk"),
		                 (machine["name"], machine["manufacturer"], machine["year"], machine["model_number"], machine["ipdb_id"], machine["opdb_id"]))
		expected = {"robowars", "robowarf", "robowffp", "robowrfp"}
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual(expected, set(drivers))
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in drivers.values()))
		self.assertTrue(all(drivers[d]["clone_of"] == "robowars" for d in expected - {"robowars"}))
		self.assertEqual("pinmame.gts80b", self.definition["controller"]["platform"])
		claimants = []
		for path in (ROOT / "machines").rglob("*.json"):
			record = load_json(path)
			if expected & {d["id"] for d in record.get("drivers", [])}:
				claimants.append(record["machine"]["id"])
		self.assertEqual([curator.MACHINE_ID], claimants)

	def test_complete_ranges_and_unused_cells_are_proved_by_the_matrix_sheet(self) -> None:
		for group, addresses in curator.EXPECTED.items():
			self.assertEqual(addresses, {n for (g, n) in self.devices if g == group.rsplit(".", 1)[-1]}, group)
		blank = {10 * s + r for s in range(3) for r in range(8)} - {6, 7, 16, 17, 27}
		for number in sorted(blank | {32, 34, 67, 77}):
			cell = self.devices["switch", number]
			self.assertEqual(("switch", "unused", "unused"), (cell["kind"], cell["availability"], cell["spatial"]["reason"]), number)
			self.assertNotIn("normally_closed", cell)
			self.assertIn("not fitment evidence", cell["physical"]["notes"])
		cabinet = {7: "service.button", 17: "cabinet.coin", 27: "cabinet.coin", 37: "cabinet.coin", 47: "cabinet.start", 57: "cabinet.tilt"}
		for number, role in cabinet.items():
			cell = self.devices["switch", number]
			self.assertEqual("used", cell["availability"])
			self.assertEqual([role], cell["roles"])
			self.assertFalse(cell["normally_closed"])
			if number != 57:
				self.assertEqual("cabinet_or_service", cell["spatial"]["reason"])
		# The tilt address also carries the playboard contact, which no table object places.
		tilt = self.devices["switch", 57]
		self.assertEqual(3, tilt["physical"]["quantity"])
		self.assertNotIn("spatial", tilt)
		self.assertIn("switch.tilt", load_json(curator.AUDIT)["missing_spatial_ids"])
		self.assertTrue(any("switch 57" in blocker for blocker in load_json(curator.AUDIT_SEED)["blockers"]))
		for number in set(range(30, 77)) - {32, 34, 37, 47, 57, 67} - {38, 39, 48, 49, 58, 59, 68, 69}:
			cell = self.devices["switch", number]
			self.assertEqual("used", cell["availability"], number)
			self.assertFalse(cell["normally_closed"], number)

	def test_flipper_buttons_copies_and_slam_polarity(self) -> None:
		for copy_address, button in ((6, 114), (16, 112)):
			copy_cell = self.devices["switch", copy_address]
			self.assertEqual("virtual", copy_cell["kind"])
			self.assertIn(str(button), copy_cell["physical"]["notes"])
			self.assertFalse(self.devices["switch", button]["normally_closed"])
			# Folio 49 fits the advance pushbuttons apart from the flipper switch assemblies.
			self.assertIn("item 26", self.devices["switch", button]["physical"]["notes"])
			self.assertNotIn("same button", self.devices["switch", button]["physical"]["notes"])
		self.assertEqual(["flipper.lower.left.button"], self.devices["switch", 114]["roles"])
		self.assertEqual(["flipper.lower.right.button"], self.devices["switch", 112]["roles"])
		for number in (111, 113, 115, 116, 117, 118):
			self.assertEqual(("virtual", "unused"), (self.devices["switch", number]["kind"], self.devices["switch", number]["availability"]))
		slam = self.devices["switch", -1]
		self.assertTrue(slam["normally_closed"])
		self.assertFalse(slam["initial_active"])
		self.assertTrue(self.devices["switch", 56]["initial_active"])
		self.assertEqual("used", self.devices["switch", 46]["availability"])
		self.assertIn("RIGHT FLIPPER SWITCH", self.devices["switch", 46]["physical"]["notes"])
		# Lamps 23-26 were all lit when the probe pulsed 46, so it shows no rotation.
		self.assertIn("shows no rotation", self.devices["switch", 46]["physical"]["notes"])
		for number in range(45, 49):
			self.assertEqual("virtual", self.devices["solenoid", number]["kind"])

	def test_dip_banks_and_unread_sound_inputs(self) -> None:
		for number in range(1, 33):
			dip = self.devices["dip", number]
			self.assertEqual(("dip_switch", "used"), (dip["kind"], dip["availability"]))
			self.assertTrue(dip["label"].endswith(f"(S{number})"))
		self.assertIn("Balls per Game", self.devices["dip", 25]["label"])
		for number in range(33, 43):
			dip = self.devices["dip", number]
			self.assertEqual(("virtual", "unused"), (dip["kind"], dip["availability"]))
			self.assertIn("rom.robo-war-sound-dip-scan", dip["provenance"]["source_refs"])

	def test_relays_coils_on_lamp_drivers_and_the_s_multiplex(self) -> None:
		for number, label in ((0, "Q"), (1, "T"), (12, "S"), (13, "A")):
			relay = self.devices["lamp", number]
			self.assertEqual("relay", relay["kind"])
			self.assertTrue(relay["label"].endswith(label) or f" {label}" in relay["label"], relay["label"])
			self.assertEqual("internal_nonvisual", relay["spatial"]["reason"])
			# The relay test holds Q on while it pulses the others, so none is energized alone.
			self.assertNotIn("alone", relay["physical"]["notes"])
		self.assertIn("holds it on into the solenoid test", self.devices["lamp", 0]["physical"]["notes"])
		self.assertEqual(("coil", "16570"), (self.devices["lamp", 2]["kind"], self.devices["lamp", 2]["physical"]["part_number"]))
		self.assertEqual(("coil", "17875"), (self.devices["lamp", 14]["kind"], self.devices["lamp", 14]["physical"]["part_number"]))
		self.assertEqual("control_signal", self.devices["lamp", 4]["kind"])
		gated = {r["destination"] for r in self.definition["relationships"] if r["source"] == "relay.switching-s"}
		self.assertEqual({self.devices["solenoid", n]["id"] for n in (1, 2, 3, 5, 6)}, gated)
		self.assertTrue(all(r["kind"] == "relay_gated" for r in self.definition["relationships"] if r["source"] == "relay.switching-s"))
		inverted = [r for r in self.definition["relationships"] if r["kind"] == "inverted"]
		self.assertEqual([("relay.tilt-t", "gi.playboard-illumination")], [(r["source"], r["destination"]) for r in inverted])
		for number in (1, 2, 5, 6):
			coil = self.devices["solenoid", number]
			self.assertEqual("coil", coil["kind"])
			self.assertIn("Dome", coil["label"])
			self.assertIn("lamp 12 = 0", coil["physical"]["notes"])
		self.assertEqual(("flasher", "flasher"), (self.devices["solenoid", 4]["kind"], self.devices["solenoid", 7]["kind"]))
		self.assertEqual(["cabinet.knocker"], self.devices["solenoid", 8]["roles"])

	def test_lamp_driver_provisions_without_loads_stay_unused_and_mirrors_stay_virtual(self) -> None:
		for number in range(48, 52):
			lamp = self.devices["lamp", number]
			self.assertEqual(("lamp", "unused"), (lamp["kind"], lamp["availability"]))
			self.assertIn(f"complement of lamp {number - 4}", lamp["physical"]["notes"])
			self.assertIn("E-25887", lamp["physical"]["notes"])
		for number in range(52, 61):
			self.assertEqual(("virtual", "used"), (self.devices["lamp", number]["kind"], self.devices["lamp", number]["availability"]))
		for number in range(61, 64):
			self.assertEqual(("virtual", "unused"), (self.devices["lamp", number]["kind"], self.devices["lamp", number]["availability"]))
		for number in range(15, 19):
			lamp = self.devices["lamp", number]
			self.assertEqual(2, lamp["physical"]["quantity"])
			placements = lamp["spatial"]["placements"]
			# Both bulbs under the one oval insert are projected onto its centre and never validated.
			self.assertEqual(2, len(placements))
			self.assertEqual(1, len({(p["x"], p["y"]) for p in placements}))
			self.assertEqual({"observed"}, {p["provenance"]["status"] for p in placements})
		# No table light shows a bulb, so every lamp is a projection and none is validated.
		lamps = [d for d in self.definition["outputs"] if d["binding"]["group"] == "pinmame.output.lamp" and d["kind"] == "lamp" and "placements" in d.get("spatial", {})]
		self.assertEqual(41, len(lamps))
		for lamp in lamps:
			self.assertEqual({"observed"}, {p["provenance"]["status"] for p in lamp["spatial"]["placements"]}, lamp["id"])
			self.assertIn("projected", lamp["physical"]["notes"], lamp["id"])
		for number, bumper in ((45, "Bumper1"), (46, "Bumper2"), (47, "Bumper3")):
			self.assertEqual([f"{self.devices['lamp', number]['id']}.{bumper.lower()}"], [p["id"] for p in self.devices["lamp", number]["spatial"]["placements"]])
		self.assertIn("l5a, a bulb-mode glow light", self.devices["lamp", 5]["physical"]["notes"])
		self.assertIn("LEFT OUT ROLLOVER, SPECIAL", self.devices["lamp", 37]["physical"]["notes"])
		self.assertEqual("Left Return Rollover Special", self.devices["lamp", 37]["label"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			for ref in mechanism["actuators"] + mechanism["sensors"]:
				self.assertIn(ref, self.by_id, mechanism["id"])
		self.assertEqual(["coil.stargate-ramp"], mechanisms["mech.stargate-ramp"]["actuators"])
		self.assertEqual({"coil.outhole", "coil.ball-release"}, set(mechanisms["mech.ball-transport"]["actuators"]))
		self.assertEqual([], mechanisms["mech.flippers"]["actuators"])
		self.assertEqual([], mechanisms["mech.pop-bumpers"]["actuators"])
		banks = {m["id"]: len(m["sensors"]) for m in mechanisms.values() if m["kind"] == "drop_target_bank"}
		self.assertEqual({"mech.alpha-one": 1, "mech.alpha-two": 2, "mech.alpha-three": 3, "mech.top-bank": 4}, banks)

	def test_partial_gate_rejects_cosmetic_promotion(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], unresolved_conflicts(self.definition))
		promoted = copy.deepcopy(self.definition)
		promoted["coverage"].update(status="author_ready", missing=[])
		promoted["coverage"]["dimensions"] = {k: "validated" for k in promoted["coverage"]["dimensions"]}
		self.assertTrue(any("spatial" in error for error in validate_machine(promoted, ROOT)))
		with patch.object(curator, "load_json", side_effect=lambda path: promoted if path == curator.SEED else load_json(path)):
			with self.assertRaisesRegex(ValueError, "cannot authorize promotion"):
				curator.build()

	def test_every_excerpt_is_cited_and_pinned(self) -> None:
		cited = {excerpt["path"] for source in self.definition["sources"] for excerpt in source.get("excerpts", [])}
		self.assertEqual({p.relative_to(ROOT).as_posix() for p in EXCERPTS.iterdir()}, cited)
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], curator.digest(ROOT / excerpt["path"]), excerpt["path"])
		for source in ("manual.robo-war-part-1", "manual.robo-war-part-2", "vpx.robo-war"):
			self.assertTrue(self.sources[source]["license"])
			self.assertTrue(self.sources[source]["attribution"])
		self.assertFalse(self.sources["vpx.robo-war"]["known_working"])

	def test_committed_scenarios_match_the_recorded_raw_run_pins(self) -> None:
		summary = load_json(EXCERPTS / "runtime-observations.txt")
		self.assertEqual({"robo-war-service-sweep.json", "robo-war-gameplay-probe.json"}, {p.name for p in SCENARIOS.glob("*.json")})
		for run in summary["runs"].values():
			self.assertIsNone(run["failure"])
			path = ROOT / run["scenario"]["path"]
			self.assertNotIn(b"\r", path.read_bytes())
			self.assertEqual(run["scenario"]["sha256"], curator.digest(path))
		self.assertEqual(self.sources["runtime.robo-war-service-sweep"]["sha256"], summary["runs"]["service_sweep"]["raw_run_sha256"])
		self.assertEqual(self.sources["runtime.robo-war-gameplay-probe"]["sha256"], summary["runs"]["gameplay_probe"]["raw_run_sha256"])

	def test_s_released_pulses_are_only_resets_and_the_hole_kick(self) -> None:
		pulses = load_json(EXCERPTS / "runtime-observations.txt")["gameplay_probe"]["s_multiplexed_pulses"]
		released = pulses["pulses_with_relay_s_released"]
		self.assertEqual({1: 5, 2: 5, 3: 1, 5: 5, 6: 5}, {n: sum(p["solenoid"] == n for p in released) for n in (1, 2, 3, 5, 6)})
		self.assertEqual(["solenoid 3 kicks the hole"], [p["step"] for p in released if p["solenoid"] == 3])
		allowed = ("boot", "ball release", "completes", "resets", "both balls in trough")
		for pulse in released:
			self.assertTrue(any(word in pulse["step"] for word in allowed) or pulse["solenoid"] == 3, pulse)

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load_json(curator.CALLOUT_SEED)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		self.assertEqual(curator.digest(curator.CALLOUT_SEED), self.sources[curator.CALLOUTS]["sha256"])
		checked = 0
		for device in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (device.get("spatial") or {}).get("placements") or []:
				decision = decisions["placements"].get(placement["id"])
				status = placement["provenance"]["status"]
				if decision is None:
					self.assertEqual("observed", status, placement["id"])
					continue
				checked += 1
				self.assertEqual("validated" if decision["agrees"] else "observed", status, placement["id"])
				self.assertEqual(decision["agrees"], curator.CALLOUTS in placement["provenance"]["source_refs"], placement["id"])
		self.assertEqual(len(seed["checks"]), checked)
		self.assertEqual(["switch.outhole.drain", "switch.right-flipper-switch.rightflipper", "switch.shooter-lane-rollover.shooterlane"],
		                 sorted(pid for pid, d in decisions["placements"].items() if not d["agrees"]))
		audit = load_json(curator.AUDIT)
		self.assertEqual(curator.callout_check(self.definition), audit["drawing_callout_check"])
		self.assertEqual(curator.digest(curator.AUDIT_SEED), audit["source_seed_sha256"])
		# Flashers sharing a coil output, the leader-less SOL.4 and SOL.7 labels, the projected
		# lamps and the misprinted second SW 42 are never checked.
		excluded = [("solenoid", n) for n in (1, 2, 3, 4, 5, 6, 7)] + [("lamp", n) for n in [3, *range(5, 12), *range(15, 48)]]
		for key in excluded:
			for placement in self.devices[key]["spatial"]["placements"]:
				self.assertIn(placement["id"], seed["excluded_checks"])
				self.assertNotIn(placement["id"], seed["checks"])
		self.assertIn("leader", seed["excluded_checks"]["flasher.left-side.lpf"])
		self.assertIn("leader", seed["excluded_checks"]["flasher.right-side.rpf"])
		self.assertIn("switch.left-drop-target.alpha1", seed["excluded_checks"])
		page = seed["pages"]["folio-48"]
		self.assertGreaterEqual(len(page["controls"]), 5)
		self.assertNotIn("model", json.dumps(seed["read_by"]).lower())

	def test_knowledge_note_carries_the_computed_callout_sentence(self) -> None:
		note = curator.NOTE.read_text(encoding="utf-8")
		self.assertNotIn("{CALLOUT_CHECK}", note)
		check = load_json(curator.AUDIT)["drawing_callout_check"]
		self.assertIn(f"validates {check['validated']} of the {check['checked']} table placements", note)
		self.assertIn("each with a note on its device: switches 36, 46, 66.", note)


class RoboWarCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_refuses_incomplete_inventory(self) -> None:
		self.assertEqual(curator.PARTIAL.read_bytes(), canonical_bytes(curator.build()))
		first = curator.artifacts()
		self.assertEqual(first, curator.artifacts())
		for path, expected in first.items():
			self.assertEqual(expected, path.read_bytes(), str(path))
		seed = load_json(curator.SEED)
		incomplete = copy.deepcopy(seed)
		incomplete["inputs"] = [d for d in incomplete["inputs"] if d["binding"] != {"group": "pinmame.input.switch", "device": 0}]
		with patch.object(curator, "load_json", side_effect=lambda path: incomplete if path == curator.SEED else load_json(path)):
			with self.assertRaisesRegex(ValueError, "Incomplete controller address inventory"):
				curator.build()
		unpinned = copy.deepcopy(seed)
		next(s for s in unpinned["sources"] if s["id"] == curator.CALLOUTS)["sha256"] = "0" * 64
		with patch.object(curator, "load_json", side_effect=lambda path: unpinned if path == curator.SEED else load_json(path)):
			with self.assertRaisesRegex(ValueError, "does not pin the committed callout seed"):
				curator.build()

	def test_excerpt_and_external_guards_reject_missing_or_changed_bytes(self) -> None:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			file = root / "fact.txt"
			file.write_bytes(b"actual fact\n")
			digest = curator.digest(file)
			definition = {"sources": [{"excerpts": [{"path": "fact.txt", "sha256": digest}]}]}
			with patch.object(curator, "ROOT", root):
				curator.verify_excerpts(definition)
				file.write_bytes(b"100 tokens truncated\n")
				truncated = {"sources": [{"excerpts": [{"path": "fact.txt", "sha256": curator.digest(file)}]}]}
				with self.assertRaisesRegex(ValueError, "Truncated source excerpt"):
					curator.verify_excerpts(truncated)
				file.write_bytes(b"changed\n")
				with self.assertRaisesRegex(ValueError, "changed excerpt"):
					curator.verify_excerpts(definition)
				file.unlink()
				with self.assertRaisesRegex(ValueError, "Missing"):
					curator.verify_excerpts(definition)
			artifact = {"environment": "ROBO_WAR_TEST_EVIDENCE", "relative_path": "fact.txt", "sha256": digest}
			with patch.dict(os.environ, {"ROBO_WAR_TEST_EVIDENCE": str(root)}):
				with self.assertRaisesRegex(ValueError, "Missing retained"):
					curator.verify_external({"retained_artifacts": [artifact]})
				file.write_bytes(b"wrong root bytes\n")
				with self.assertRaisesRegex(ValueError, "Changed retained"):
					curator.verify_external({"retained_artifacts": [artifact]})
				manifest = write_manifest(root, curator.GAME)
				directory = {"environment": "ROBO_WAR_TEST_EVIDENCE", "relative_path": ".", "sha256": manifest, "directory_manifest": True}
				curator.verify_external({"retained_artifacts": [directory]})
				file.write_bytes(b"manifest drift\n")
				with self.assertRaisesRegex(ValueError, "manifest content is stale"):
					curator.verify_external({"retained_artifacts": [directory]})

	def test_check_refuses_drift_and_regeneration_refuses_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			file = root / "canonical.txt"
			file.write_bytes(b"drift\n")
			ready = root / "ready.json"
			with patch.object(curator, "READY", ready), patch.object(curator, "artifacts", return_value={file: b"expected\n"}), patch.object(sys, "argv", ["curator", "--check"]):
				with self.assertRaisesRegex(ValueError, "Curator drift"):
					curator.main()
				self.assertEqual(b"drift\n", file.read_bytes())
			ready.write_bytes(b"promoted\n")
			with patch.object(curator, "READY", ready), patch.object(sys, "argv", ["curator", "--regenerate"]):
				with self.assertRaisesRegex(ValueError, "author-ready artifact"):
					curator.main()
				self.assertEqual(b"promoted\n", ready.read_bytes())


class RoboWarRetainedEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(curator.PARTIAL)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
	def test_retained_extraction_reproduces_every_placement(self) -> None:
		curator.verify_external(load_json(curator.AUDIT_SEED))
		extracted = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "gottlieb/robo-war-1988/full-extraction-vpxtool"
		bounds = load_json(extracted / "gamedata.json")
		self.assertEqual((0, 0, 1024, 2240), tuple(round(bounds[k]) for k in ("left", "top", "right", "bottom")))
		points = {}
		for file in (extracted / "gameitems").glob("*.json"):
			body = next(iter(load_json(file).values()))
			point = next((body[k] for k in ("center", "pos", "position", "vCenter") if isinstance(body.get(k), dict) and "x" in body[k]), None)
			if point is None and body.get("drag_points"):
				drag = body["drag_points"]
				point = {axis: sum(p[axis] for p in drag) / len(drag) for axis in ("x", "y")}
			if point is not None:
				points[body.get("name", "").lower()] = (point["x"], point["y"])
		mapping = (EXCERPTS / "spatial-mapping.txt").read_text(encoding="utf-8")
		groups: dict[str, list[str]] = {}
		for line in mapping.splitlines():
			cells = [c.strip() for c in line.strip("|").split("|")]
			if len(cells) == 7 and cells[0].count(".") >= 2 and not cells[2].startswith("="):
				groups.setdefault(cells[0], []).append(cells[2].lower())
		placements = {p["id"]: p for d in self.definition["inputs"] + self.definition["outputs"] for p in (d.get("spatial") or {}).get("placements", [])}
		self.assertEqual(set(placements), set(groups))
		for pid, names in groups.items():
			x = sum(points[n][0] for n in names) / len(names)
			y = sum(points[n][1] for n in names) / len(names)
			self.assertEqual((round(x / 1024, 6), round(y / 2240, 6)), (placements[pid]["x"], placements[pid]["y"]), pid)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts not configured")
	def test_drawing_callout_renders_and_reads_are_retained(self) -> None:
		seed = load_json(curator.CALLOUT_SEED)
		roots = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertGreaterEqual(drawing_callouts.verify_retained(seed, ROOT, None, roots), 10)
		reads = load_json(roots / seed["retained_artifacts"]["directory"] / "reads.json")
		self.assertEqual([r["pixel"] for r in reads["reads"]], [r["pixel"] for r in seed["pages"]["folio-48"]["reads"]])
		self.assertEqual([c["pixel"] for c in reads["controls"]], [c["pixel"] for c in seed["pages"]["folio-48"]["controls"]])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts not configured")
	def test_raw_gameplay_run_recomputes_the_s_multiplex_summary(self) -> None:
		roots = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		raw = roots / "gottlieb.robo-war.1988/session-20261113/harness/gameplay-probe.json"
		summary = load_json(EXCERPTS / "runtime-observations.txt")
		self.assertEqual(summary["runs"]["gameplay_probe"]["raw_run_sha256"], hashlib.sha256(raw.read_bytes()).hexdigest())
		run = json.loads(raw.read_text(encoding="utf-8"))
		state, counts = 0, {}
		for event in run["events"]:
			if event["event"] == "lamp" and event["number"] == 12:
				state = event["state"]
			if event["event"] == "solenoid" and event["state"] == 1 and event["number"] in (1, 2, 3, 5, 6):
				key = f"solenoid {event['number']} with lamp 12 = {state}"
				counts[key] = counts.get(key, 0) + 1
		self.assertEqual(summary["gameplay_probe"]["s_multiplexed_pulses"]["count_by_relay_s_state"], counts)


if __name__ == "__main__":
	unittest.main()
