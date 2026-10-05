from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location("curate_pinheck", ROOT / "tools" / "curate_pinheck.py")
CURATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CURATOR)
RUNTIME = load_json(ROOT / "tools" / "pinheck_runtime.json")
PROFILE = load_json(ROOT / "controllers" / "pinmame" / "pinheck.json")
GAMES = CURATOR.GAMES


def addresses(rules: list[dict]) -> set[int]:
	return {n for rule in rules for n in range(rule["minimum"], rule["maximum"] + 1)}


class PinheckDefinitionTests(unittest.TestCase):
	def test_curator_output_matches_the_committed_artifacts(self) -> None:
		for game in GAMES:
			for path, payload in CURATOR.artifacts(game).items():
				with self.subTest(path=path.as_posix()):
					self.assertEqual(payload, (ROOT / path).read_bytes().replace(b"\r\n", b"\n"))

	def test_catalog_maps_each_driver_to_its_curated_record(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		drivers = {driver["id"]: driver for driver in catalog["drivers"]}
		# PinMAME 97aa922b names each set after its code version and adds America's Most Haunted V22; the bare game names are gone.
		self.assertEqual({"amh": ["amh_023", "amh_022"], "dominos": ["dominos_006"], "rzspook": ["rzspook_026"], "jetsons": ["jetsons_004"]},
		                 {game: list(config["drivers"]) for game, config in GAMES.items()})
		for game, config in GAMES.items():
			with self.subTest(game=game):
				self.assertNotIn(game, drivers)
				definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
				self.assertEqual(list(config["drivers"]), [driver["id"] for driver in definition["drivers"]])
				for driver_id in config["drivers"]:
					self.assertEqual(config["machine"], drivers[driver_id]["machine_id"])
					self.assertEqual("pinheck", drivers[driver_id]["clone_of"])
					self.assertEqual(driver_id, drivers[driver_id]["root_driver"])
					self.assertFalse((ROOT / "machines" / "stubs" / f"{driver_id}.json").exists())

	def test_amh_v22_cites_its_retained_downloads(self) -> None:
		definition = load_json(ROOT / "machines" / "partial" / f"{GAMES['amh']['stem']}.json")
		sources = {source["id"]: source for source in definition["sources"]}
		v22 = next(driver for driver in definition["drivers"] if driver["id"] == "amh_022")
		excerpt = (ROOT / "evidence" / "excerpts" / GAMES["amh"]["machine"] / "rom-v22.md").read_bytes().decode()
		for part in ("card", "hex"):
			pinned = CURATOR.AMH_V22[part]
			with self.subTest(part=part):
				self.assertIn(pinned["id"], v22["variant_notes"])
				self.assertEqual(("rom_static_analysis", pinned["sha256"], pinned["url"]),
				                 tuple(sources[pinned["id"]][key] for key in ("kind", "sha256", "uri")))
				self.assertEqual(["evidence/excerpts/spooky-pinball.america-s-most-haunted.2014/rom-v22.md"],
				                 [e["path"] for e in sources[pinned["id"]]["excerpts"]])
				self.assertIn(f"| {pinned['crc']} | {pinned['sha1']} |", excerpt)
		self.assertIn("CODE REVISION: 22\n", excerpt)
		self.assertIn("DATE: 10/3/2015\n", excerpt)

	def test_every_profile_address_is_enumerated_once(self) -> None:
		groups = {group["id"]: addresses(group["address_rules"]) for group in PROFILE["groups"]}
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			for group, expected in groups.items():
				devices = [d["binding"]["device"] for d in definition["inputs"] + definition["outputs"] if d["binding"]["group"] == group]
				with self.subTest(game=game, group=group):
					self.assertEqual(len(devices), len(set(devices)))
					self.assertEqual(expected, set(devices))

	def test_the_rom_switch_grid_proves_the_matrix_and_cabinet_formulas(self) -> None:
		for game in GAMES:
			drawn = RUNTIME["games"][game]["runs"]["switch"]["grid"]["drawn_by_public"]
			with self.subTest(game=game):
				for n in range(64):
					self.assertEqual([f"matrix {n}"], drawn[str(CURATOR.public_number(n))])
				for address in (2, 7, 8, 94):
					self.assertEqual([f"cabinet {address if address < 9 else address - 82}"], drawn[str(address)])
				self.assertEqual(["cabinet 3"], drawn["112"])
				self.assertEqual(["cabinet 4"], drawn["114"])
				self.assertEqual([], drawn["98"])

	def test_solenoid_test_fires_exactly_coil_plus_one(self) -> None:
		for game in GAMES:
			with self.subTest(game=game):
				names = CURATOR.rom_coils(game)
				self.assertEqual(list(range(1, 25)), sorted(names))

	def test_lamp_test_numbers_every_matrix_lamp_and_gi_output(self) -> None:
		for game in GAMES:
			with self.subTest(game=game):
				lamps = CURATOR.rom_lamps(game)
				self.assertEqual(64, len(lamps))
				gi = CURATOR.rom_gi(game)
				self.assertEqual("PLAYFIELD GI #0" if game == "amh" else "PLAYFIELD GI GI = 1", gi[44])
				self.assertEqual("BACKBOX GI #0" if game == "amh" else "BACKBOX GI GI = 0", gi[32])

	def test_game_start_keeps_named_gi_steady_and_flashers_off(self) -> None:
		# The observed GI header mapping: chart pin k is public 25 + k (k < 8) or 29 + k.
		for game in ("dominos", "rzspook", "jetsons"):
			definition = load_json(ROOT / "machines" / "partial" / f"{GAMES[game]['stem']}.json")
			named = {d["binding"]["device"]: d["kind"] for d in definition["outputs"]
			         if d["id"].startswith("gi.") and d["availability"] == "used"}
			seconds = [step for step in RUNTIME["games"][game]["runs"]["game"]["steps"] if step["label"].startswith("Game second")]
			with self.subTest(game=game):
				self.assertTrue(any(kind == "gi" for kind in named.values()))
				self.assertTrue(any(kind == "flasher" for kind in named.values()))
				for address, kind in named.items():
					lit = [address in step["active_solenoids"] for step in seconds]
					if kind == "gi":
						self.assertTrue(all(lit), address)
					else:
						self.assertLess(sum(lit), len(lit), address)

	def test_switch_polarity_and_flipper_buttons(self) -> None:
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			inputs = {d["binding"]["device"]: d for d in definition["inputs"]}
			with self.subTest(game=game):
				self.assertTrue(all(d.get("normally_closed") is False for d in inputs.values() if d["availability"] == "used"))
				self.assertEqual(["flipper.lower.right.button"], inputs[112]["roles"])
				self.assertEqual(["flipper.lower.left.button"], inputs[114]["roles"])
				self.assertTrue(inputs[1]["initial_active"])
				self.assertTrue(all(inputs[address].get("initial_active") for address in config["trough"]))
				self.assertEqual({"platform": "pinmame.pinheck", "hardware_generation": "0x10000000000000",
				                  "inversion_applied_by_emulator": True}, definition["controller"])

	def test_records_stay_partial_with_explicit_blockers(self) -> None:
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			with self.subTest(game=game):
				self.assertEqual("partial", definition["coverage"]["status"])
				expected = ["input_semantics"] if game == "dominos" else []
				self.assertEqual([*expected, "mechanism_behavior", "output_semantics", "spatial_placement"], definition["coverage"]["missing"])
				self.assertEqual("partial", definition["knowledge"]["status"])
				unknown = [d for d in definition["outputs"] if d["availability"] == "unknown"]
				self.assertTrue(unknown)

	def test_amh_ghost_channels_follow_the_ghost_type_setting(self) -> None:
		steps = {step["label"]: step for step in RUNTIME["games"]["amh"]["runs"]["rgb"]["steps"]}
		ghost = lambda label: [a for a in steps[label]["active_solenoids"] if a >= 62]
		self.assertEqual("GHOST TYPE REV 1", steps["Item 10"]["displayed_text"])
		self.assertEqual("GHOST TYPE REV 2", steps["Enter on item 10"]["displayed_text"])
		for label, text, address in (("Item 01", "GHOST=RED", 62), ("Item 02", "GHOST=GREEN", 63), ("Item 03", "GHOST=BLUE", 64),
		                             ("Item 11", "GHOST=RED", 62), ("Item 12", "GHOST=GREEN", 64), ("Item 13", "GHOST=BLUE", 63)):
			with self.subTest(label=label):
				self.assertEqual(text, steps[label]["displayed_text"])
				self.assertEqual([address], ghost(label))
		definition = load_json(ROOT / "machines" / "partial" / f"{GAMES['amh']['stem']}.json")
		labels = {d["binding"]["device"]: d["label"] for d in definition["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
		self.assertEqual("Ghost green (REV 1) or blue (REV 2)", labels[63])
		self.assertEqual("Ghost blue (REV 1) or green (REV 2)", labels[64])

	def test_unnamed_servo_and_rgb_outputs_are_not_declared_unused_from_silence(self) -> None:
		definition = load_json(ROOT / "machines" / "partial" / f"{GAMES['jetsons']['stem']}.json")
		outputs = {d["binding"]["device"]: d for d in definition["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
		self.assertEqual("optional", outputs[57]["availability"])
		self.assertEqual("unknown", outputs[58]["availability"])
		self.assertNotIn("quantity", outputs[58]["physical"])
		self.assertNotIn("spatial", outputs[58])
		attract = RUNTIME["games"]["jetsons"]["runs"]["game"]["steps"][0]
		self.assertIn(58, attract["active_solenoids"])
		for address in (62, 63, 64):
			with self.subTest(address=address):
				self.assertEqual("unknown", outputs[address]["availability"])
				self.assertNotIn("spatial", outputs[address])

	def test_simulator_shooter_follows_the_manual_plunger_declaration(self) -> None:
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			shooter = next(d for d in definition["outputs"] if d["binding"] == {"group": "pinmame.output.solenoid", "device": 49})
			with self.subTest(game=game):
				self.assertEqual("used" if config["manual_plunger"] else "unused", shooter["availability"])
				self.assertEqual("virtual" if config["manual_plunger"] else "unused", shooter["spatial"]["reason"])

	def test_runtime_summary_refuses_missing_or_altered_frames(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("retained harness runs are not available")
		import shutil
		import tempfile
		import pinheck_runtime
		from build_external_evidence_manifest import write_manifest
		source = Path(review_root) / GAMES["jetsons"]["machine"] / pinheck_runtime.SESSION / "runtime" / "jetsons-rgb"
		with tempfile.TemporaryDirectory() as scratch:
			# The remanifested cases rebuild the manifest after the damage, so only the frame checks can catch it.
			for damage in ("missing", "altered", "remanifested", "transposed header"):
				run_dir = Path(scratch) / damage
				shutil.copytree(source, run_dir)
				pinheck_runtime.summarize(run_dir)
				frame = next((run_dir / "dmd").glob("*-item-01-display-0.ppm"))
				if damage == "missing":
					frame.unlink()
				elif damage == "transposed header":
					frame.write_bytes(frame.read_bytes().replace(b"P6\n128 64\n", b"P6\n64 128\n", 1))
					write_manifest(run_dir, "jetsons")
				else:
					data = bytearray(frame.read_bytes())
					data[-1] ^= 0xFF
					frame.write_bytes(bytes(data))
					if damage == "remanifested":
						write_manifest(run_dir, "jetsons")
				with self.subTest(damage=damage), self.assertRaises(ValueError):
					pinheck_runtime.summarize(run_dir)

	def test_runtime_summary_pins_and_verifies_the_starting_state(self) -> None:
		for game in GAMES:
			seed = RUNTIME["games"][game]["baseline_state"]
			with self.subTest(game=game):
				if game == "amh":
					self.assertIsNone(seed)
				else:
					self.assertIn(f"nvram/{game}.nv", [f["path"] for f in seed["files"]])
					excerpt = (ROOT / CURATOR.excerpt_dir(game) / "runtime-provenance.md").read_text(encoding="utf-8")
					self.assertIn(seed["manifest_sha256"], excerpt)
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("retained harness runs are not available")
		import shutil
		import tempfile
		import pinheck_runtime
		machine = GAMES["dominos"]["machine"]
		source = Path(review_root) / machine / pinheck_runtime.SESSION / "baseline-state"
		with tempfile.TemporaryDirectory() as scratch:
			for damage in ("missing", "altered"):
				root = Path(scratch) / damage
				seed_dir = root / machine / pinheck_runtime.SESSION / "baseline-state"
				shutil.copytree(source, seed_dir)
				self.assertEqual(RUNTIME["games"]["dominos"]["baseline_state"], pinheck_runtime.baseline_state(root, "dominos"))
				nvram = seed_dir / "nvram" / "dominos.nv"
				if damage == "missing":
					nvram.unlink()
				else:
					data = bytearray(nvram.read_bytes())
					data[0] ^= 0xFF
					nvram.write_bytes(bytes(data))
				with self.subTest(damage=damage), self.assertRaises(ValueError):
					pinheck_runtime.baseline_state(root, "dominos")

	def test_amh_places_every_used_device_from_the_lw_table_or_says_why_not(self) -> None:
		definition = load_json(ROOT / "machines" / "partial" / f"{GAMES['amh']['stem']}.json")
		devices = {(d["binding"]["group"], d["binding"]["device"]): d for d in definition["inputs"] + definition["outputs"]}
		placed = {key for key, d in devices.items() if d.get("spatial", {}).get("status") == "observed"}
		used = {key for key, d in devices.items() if d["availability"] in ("used", "optional") and d.get("spatial", {}).get("status") != "not_applicable"}
		self.assertEqual(used - placed, set(CURATOR.AMH_UNPLACED))
		self.assertEqual(len(CURATOR.AMH_PLACEMENTS["placements"]), len(placed))
		self.assertIn("spatial_placement", definition["coverage"]["missing"])
		for key in placed:
			for placement in devices[key]["spatial"]["placements"]:
				with self.subTest(device=devices[key]["id"]):
					self.assertEqual("observed", placement["provenance"]["status"])
					self.assertIn(CURATOR.AMH_TABLE_SOURCE, placement["provenance"]["source_refs"])
		# The top lanes follow the ROM, not the table's trigger names: the chart's 40 "O" is the left lane.
		lanes = {address: devices[("pinmame.input.switch", address)]["spatial"]["placements"][0]["x"] for address in (61, 62, 63)}
		self.assertLess(lanes[61], lanes[62])
		self.assertLess(lanes[62], lanes[63])
		steps = {step["label"]: step for step in RUNTIME["games"]["amh"]["runs"]["lanes"]["steps"]}
		self.assertEqual([51], [lamp for lamp in steps["Close 61"]["active_lamps"] if 51 <= lamp <= 53])
		self.assertEqual([51, 52], [lamp for lamp in steps["Close 62"]["active_lamps"] if 51 <= lamp <= 53])

	def test_photo_games_place_playfield_measurements_or_say_why_not(self) -> None:
		groups = {"switch": "pinmame.input.switch", "solenoid": "pinmame.output.solenoid", "lamp": "pinmame.output.lamp"}
		self.assertEqual({"rzspook", "jetsons", "dominos"}, set(CURATOR.PHOTO))
		for game, seed in CURATOR.PHOTO.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{GAMES[game]['stem']}.json")
			devices = {(d["binding"]["group"], d["binding"]["device"]): d for d in definition["inputs"] + definition["outputs"]}
			placed = {(groups[e["group"]], e["address"]) for e in seed["placements"]}
			listed = {(groups[e["group"]], e["address"]) for e in seed["unplaced"]}
			geometry = {ph["id"] for ph in seed["photos"] if ph["role"] == "geometry"}
			with self.subTest(game=game):
				self.assertFalse(placed & listed)
				used = {key for key, d in devices.items() if d["availability"] in ("used", "optional") and d.get("spatial", {}).get("status") != "not_applicable"}
				self.assertEqual(used, placed | listed)
				self.assertIn("spatial_placement", definition["coverage"]["missing"])
				self.assertEqual(1, len(geometry))
			for entry in seed["placements"]:
				item = devices[(groups[entry["group"]], entry["address"])]
				with self.subTest(game=game, device=item["id"]):
					placement = item["spatial"]["placements"][0]
					self.assertEqual("observed", item["spatial"]["status"])
					self.assertEqual((entry["x"], entry["y"]), (placement["x"], placement["y"]))
					# frame_px is rounded to whole pixels, the normalized value to three decimals.
					self.assertAlmostEqual(entry["frame_px"][0] / 952, entry["x"], delta=0.001)
					self.assertAlmostEqual(entry["frame_px"][1] / 2185, entry["y"], delta=0.001)
					self.assertIn(entry["confidence"], ("medium", "high"))
					self.assertTrue(entry["level"] == "playfield" or re.search(r"flipper|sling", entry["feature"], re.I))
					self.assertTrue(geometry <= set(placement["provenance"]["source_refs"]))

	def test_dominos_scoops_cite_the_close_up_they_were_read_on(self) -> None:
		# Both scoop holes were read on thread photo 011 as well as the geometry photo; their coils share the holes.
		placements = {(e["group"], e["address"]): e for e in CURATOR.PHOTO["dominos"]["placements"]}
		for key in (("switch", 25), ("switch", 48), ("solenoid", 9), ("solenoid", 13)):
			with self.subTest(device=key):
				self.assertIn("photo.dominos-pinside-011", placements[key]["photos"])

	def test_photo_evidence_matches_the_retained_files(self) -> None:
		manuals = os.environ.get("PINMAME_MANUALS_ROOT")
		review = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals and not review:
			self.skipTest("no evidence roots are set")
		import hashlib
		from build_external_evidence_manifest import check_manifest
		for game, seed in CURATOR.PHOTO.items():
			if manuals:
				# A configured root must hold every photograph: a missing file fails rather than skips.
				for photo in seed["photos"]:
					with self.subTest(game=game, photo=photo["id"]):
						data = (Path(manuals) / photo["local_path"]).read_bytes()
						self.assertEqual(photo["sha256"], hashlib.sha256(data).hexdigest())
						from PIL import Image
						with Image.open(Path(manuals) / photo["local_path"]) as image:
							self.assertEqual(photo["size_px"], list(image.size))
			if review:
				directory = Path(review) / GAMES[game]["machine"] / seed["measurement_dir"]
				with self.subTest(game=game, check="manifest"):
					self.assertEqual(seed["measurement_manifest_sha256"], check_manifest(directory, game))
				candidates = {(e["group"], e["address"]): e for e in json.loads((directory / seed["candidates_file"]).read_text(encoding="utf-8"))}
				for entry in seed["placements"]:
					measured = candidates[(entry["group"], entry["address"])]
					with self.subTest(game=game, device=f"{entry['group']} {entry['address']}"):
						self.assertEqual("placed", measured["status"])
						self.assertEqual(entry["frame_px"], [round(measured["x"]), round(measured["y"])])
						self.assertEqual((entry["x"], entry["y"]), (round(measured["x"] / 952, 3), round(measured["y"] / 2185, 3)))

	def test_amh_lw_table_extraction_and_coordinates(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		# A configured root must hold the retained table: a missing table fails rather than skips.
		import hashlib
		table = CURATOR.AMH_TABLE
		base = Path(root) / table["relative"]
		extraction = base / table["filename"].removesuffix(".vpx")
		self.assertTrue(extraction.is_dir(), f"retained LW extraction missing under {base}")
		for name, digest, size in ((table["filename"], table["sha256"], table["bytes"]), (table["obj"], table["obj_sha256"], table["obj_bytes"])):
			with self.subTest(artifact=name):
				data = (base / name).read_bytes()
				self.assertEqual((digest, size), (hashlib.sha256(data).hexdigest(), len(data)))
		paths = sorted((p for p in extraction.rglob("*") if p.is_file()), key=lambda p: p.relative_to(extraction).as_posix())
		manifest = {"format": "pinmame-vpx-extraction-manifest", "version": 1,
		            "files": [{"path": p.relative_to(extraction).as_posix(), "size": p.stat().st_size,
		                       "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
		self.assertEqual(canonical_bytes(manifest), (base / f"{table['filename'].removesuffix('.vpx')}.manifest.json").read_bytes())
		self.assertEqual((table["manifest_sha256"], table["file_count"], table["total_bytes"]),
		                 (hashlib.sha256(canonical_bytes(manifest)).hexdigest(), len(paths), sum(p.stat().st_size for p in paths)))
		self.assertEqual(table["script_sha256"], hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest())
		for entry in CURATOR.AMH_PLACEMENTS["placements"]:
			item = json.loads((extraction / "gameitems" / f"{entry['object_kind']}.{entry['object']}.json").read_text(encoding="utf-8"))
			item = item.get(entry["object_kind"], item)
			if entry["read_from"] == "drag_point_centroid":
				points = item["drag_points"]
				x, y = sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points)
			else:
				x, y = item[entry["read_from"]]["x"], item[entry["read_from"]]["y"]
			with self.subTest(object=entry["object"]):
				self.assertEqual((round(x, 6), round(y, 6)), (entry["x"], entry["y"]))
				self.assertTrue(0 <= entry["x"] <= table["width"] and 0 <= entry["y"] <= table["height"])

	def test_scenarios_are_generated(self) -> None:
		completed = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "pinheck_harness_scenarios.py"), "--check"],
		                           capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

	def test_runtime_summary_matches_the_retained_runs(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("retained harness runs are not available")
		import pinheck_runtime
		self.assertEqual((ROOT / "tools" / "pinheck_runtime.json").read_bytes(), pinheck_runtime.payload(Path(review_root)))


if __name__ == "__main__":
	unittest.main()
