from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs import spatial
from pinmame_game_defs.jsonio import canonical_bytes


ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "transformers-pro-2011.json"
LE_PATH = ROOT / "machines" / "partial" / "stern" / "transformers-limited-edition-2011.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "transformers-pro-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "transformers-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def load_curator_module() -> object:
	spec = importlib.util.spec_from_file_location("curate_transformers_test", ROOT / "tools" / "curate_transformers.py")
	assert spec is not None and spec.loader is not None
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


class TransformersDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.le = load_json(LE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)

	def test_both_editions_are_fail_closed_for_spatial_retrofit(self) -> None:
		for definition in (self.pro, self.le):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			self.assertIn("spatial_placement", definition["coverage"]["missing"])
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "tf_180h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "tf_180h.md").exists())
		knowledge = (ROOT / self.le["knowledge"]["path"]).read_text(encoding="utf-8")
		self.assertIn("## Spatial retrofit blocker register", knowledge)
		self.assertIn("cannot be located from the Pro frame", knowledge)

	def test_editions_exhaustively_split_the_supported_driver_family(self) -> None:
		pro = {driver["id"] for driver in self.pro["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"tf_120", "tf_140", "tf_150", "tf_160", "tf_170", "tf_180"}, pro)
		self.assertEqual({"tf_088h", "tf_100h", "tf_120h", "tf_130h", "tf_140h", "tf_150h", "tf_180h"}, limited_edition)
		self.assertFalse(pro & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("tf_")}, pro | limited_edition)

	def test_complete_switch_and_dip_address_space_is_explicit(self) -> None:
		for definition in (self.pro, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Right ramp exit", bindings(self.pro, "inputs", "pinmame.input.switch")[14]["label"])
		self.assertEqual("unused", bindings(self.le, "inputs", "pinmame.input.switch")[14]["availability"])
		self.assertEqual("Right ramp exit", bindings(self.le, "inputs", "pinmame.input.switch")[52]["label"])
		self.assertEqual("Starscream left limit", bindings(self.le, "inputs", "pinmame.input.switch")[71]["label"])
		self.assertEqual("unused", bindings(self.pro, "inputs", "pinmame.input.switch")[71]["availability"])
		roles = {role for item in self.pro["inputs"] for role in item.get("roles", [])}
		self.assertTrue({"cabinet.start", "cabinet.coin.left", "cabinet.tilt", "service.back", "service.down", "service.up", "service.enter", "flipper.lower.left.button", "flipper.lower.right.button"} <= roles)

	def test_pro_main_outputs_resolve_the_shared_script_gate_exception(self) -> None:
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(outputs))
		self.assertEqual("unused", outputs[4]["availability"])
		self.assertIn("official Pro chart", outputs[4]["physical"]["notes"])
		self.assertEqual("Orbit control gate", outputs[5]["label"])
		self.assertEqual("Optimus Prime bash solenoid", outputs[12]["label"])
		self.assertEqual("Optimus Prime ramp motor relay", outputs[30]["label"])
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		le_outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual("J16-P4", le_outputs[24]["wiring"]["power_connection"])
		self.assertEqual(20, le_outputs[24]["wiring"]["nominal_voltage_v"])

	def test_le_auxiliary_board_serialization_is_explicit(self) -> None:
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(outputs))
		self.assertTrue(all(outputs[address]["availability"] == "unused" for address in set(range(51, 59)) | {65, 66}))
		self.assertEqual("Q41", outputs[59]["wiring"]["driver_transistor"])
		self.assertEqual("Q46", outputs[64]["wiring"]["driver_transistor"])
		self.assertEqual("Starscream platform motor", outputs[59]["label"])
		self.assertEqual("Optimus Prime bash solenoid", outputs[62]["label"])
		self.assertEqual("Ironhide mini-playfield left", outputs[63]["label"])

	def test_lamp_matrices_are_complete_and_edition_specific(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(pro))
		self.assertEqual(set(range(1, 81)), set(limited_edition))
		self.assertEqual({56} | set(range(63, 81)), {address for address, lamp in pro.items() if lamp["availability"] == "unused"})
		self.assertEqual(set(range(1, 17)) | {60}, {address for address, lamp in limited_edition.items() if lamp["availability"] == "unused"})
		self.assertEqual("Megatron bottom", pro[57]["label"])
		self.assertEqual("Ironhide mini-playfield 1", limited_edition[59]["label"])
		self.assertEqual("Start button", limited_edition[80]["label"])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_capture_complete_causality(self) -> None:
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertIn("four-position vertical mini-trough", pro["mechanism.megatron-lock"]["behavior"])
		self.assertEqual([["switch.optimus-ramp-down"], ["switch.optimus-ramp-up"]], [position["sensors"] for position in pro["mechanism.optimus-ramp"]["positions"]])
		self.assertEqual(["device.orbit-control-gate"], pro["mechanism.orbit-gate"]["actuators"])
		self.assertNotIn("mechanism.starscream", pro)
		self.assertEqual(["switch.starscream-left-limit", "switch.starscream-right-limit", "switch.starscream-target"], limited_edition["mechanism.starscream"]["sensors"])
		self.assertEqual("511-6979-00", limited_edition["mechanism.starscream"]["assembly_part_number"])
		self.assertEqual(4, len(limited_edition["mechanism.ironhide-mini-playfield"]["sensors"]))
		self.assertIn("does not physically travel through the cannon", limited_edition["mechanism.megatron-figure-and-cannon"]["behavior"])
		actuators = [actuator for mechanism in limited_edition.values() for actuator in mechanism["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))

	def test_source_and_exact_rom_hash_constants_are_pinned(self) -> None:
		pro_sources = {source["id"]: source for source in self.pro["sources"]}
		le_sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8", pro_sources["manual.transformers-pro-le.2011"]["sha256"])
		self.assertEqual("9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8", le_sources["manual.transformers-pro-le.2011"]["sha256"])
		self.assertEqual("987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b", pro_sources["vpx.transformers-pro-vpw-2.3.1"]["sha256"])
		self.assertEqual("8689f01315ad4f6b7001c7a99147093c64297631104610a7ac03e34152e8f352", self.pro_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("5f7c0caa85b1b5b8799e6cceef8e7d9ec7d9ddd63f0b8364ab5e9168c88443da", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("0ce389603bb0ccc237e71937ddadb8a5534f2499fdf610f6ec4087bdf29d22f4", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		for evidence in (self.pro_evidence, self.le_evidence):
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], evidence["runtime"]["observations"]["display_layouts_seen"])

	def test_every_runtime_observation_resolves_to_a_declared_output(self) -> None:
		for definition, evidence in ((self.pro, self.pro_evidence), (self.le, self.le_evidence)):
			groups = {
				"solenoid_addresses_seen": bindings(definition, "outputs", "pinmame.output.solenoid"),
				"lamp_addresses_seen": bindings(definition, "outputs", "pinmame.output.lamp"),
				"gi_addresses_seen": bindings(definition, "outputs", "pinmame.output.gi"),
			}
			for observation, declared in groups.items():
				self.assertFalse(set(evidence["runtime"]["observations"][observation]) - set(declared), observation)

	def test_bindings_and_semantic_ids_are_unique(self) -> None:
		for definition in (self.pro, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))

	def test_generator_build_is_deterministic_and_preserves_edition_boundary(self) -> None:
		curator = load_curator_module()
		pro = curator.fail_closed_spatial_partial(curator.build(False))
		limited_edition = curator.fail_closed_spatial_partial(curator.build(True))
		self.assertEqual(canonical_bytes(pro), canonical_bytes(curator.fail_closed_spatial_partial(curator.build(False))))
		self.assertEqual(canonical_bytes(limited_edition), canonical_bytes(curator.fail_closed_spatial_partial(curator.build(True))))
		self.assertEqual(2, pro["schema_version"])
		self.assertEqual(2, limited_edition["schema_version"])
		self.assertEqual("partial", limited_edition["coverage"]["status"])
		self.assertIn("spatial_placement", limited_edition["coverage"]["missing"])
		self.assertFalse(any("spatial" in device for device in limited_edition["inputs"] + limited_edition["outputs"]))
		self.assertEqual({driver["id"] for driver in self.pro["drivers"]}, {driver["id"] for driver in pro["drivers"]})
		self.assertEqual({driver["id"] for driver in self.le["drivers"]}, {driver["id"] for driver in limited_edition["drivers"]})

	def test_curator_source_path_shim_is_cwd_independent(self) -> None:
		environment = os.environ.copy()
		environment.pop("PYTHONPATH", None)
		environment["PYTHONNOUSERSITE"] = "1"
		with tempfile.TemporaryDirectory() as temporary:
			result = subprocess.run(
				[
					sys.executable,
					"-c",
					"""
import importlib.util
import sys
from pathlib import Path

curator_path = Path(sys.argv[1]).resolve()
repository_root = curator_path.parents[1]
source_root = repository_root / "src"

def is_repository_or_site_package_path(entry: str) -> bool:
    if not entry:
        return True
    path = Path(entry).resolve()
    return (
        path == repository_root
        or repository_root in path.parents
        or any(part.casefold() in {"site-packages", "dist-packages"} for part in path.parts)
    )

sys.path[:] = [entry for entry in sys.path if not is_repository_or_site_package_path(entry)]
assert "pinmame_game_defs" not in sys.modules
assert importlib.util.find_spec("pinmame_game_defs") is None

spec = importlib.util.spec_from_file_location("isolated_curate_transformers", curator_path)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

loaded = sys.modules["pinmame_game_defs"]
assert Path(loaded.__file__).resolve().is_relative_to(source_root)
assert str(source_root) in sys.path
""",
					str(ROOT / "tools" / "curate_transformers.py"),
				],
				cwd=temporary,
				env=environment,
				capture_output=True,
				text=True,
				check=False,
			)
		self.assertEqual(0, result.returncode, result.stderr)

	def test_generator_skips_removed_pending_editions_without_author_ready(self) -> None:
		curator = load_curator_module()
		original_pending_ids = tuple(curator.SPATIAL_RETROFIT_PENDING_MACHINE_IDS)
		original_spatial_pending_ids = tuple(spatial.SPATIAL_RETROFIT_PENDING_MACHINE_IDS)
		for limited_edition in (False, True):
			with self.subTest(edition="limited edition" if limited_edition else "pro"):
				filename = "transformers-limited-edition-2011.json" if limited_edition else "transformers-pro-2011.json"
				machine_id = "stern.transformers-limited-edition.2011" if limited_edition else "stern.transformers-pro.2011"
				knowledge_filename = filename.removesuffix(".json") + ".md"
				evidence_filename = "transformers-limited-edition-boot-start.json" if limited_edition else "transformers-pro-boot-start.json"
				with tempfile.TemporaryDirectory() as temporary:
					curator.ROOT = Path(temporary)
					removed_pending_ids = tuple(identifier for identifier in original_pending_ids if identifier != machine_id)
					curator.SPATIAL_RETROFIT_PENDING_MACHINE_IDS = removed_pending_ids
					spatial.SPATIAL_RETROFIT_PENDING_MACHINE_IDS = removed_pending_ids
					try:
						curator.main()
					finally:
						curator.SPATIAL_RETROFIT_PENDING_MACHINE_IDS = original_pending_ids
						spatial.SPATIAL_RETROFIT_PENDING_MACHINE_IDS = original_spatial_pending_ids
					self.assertFalse((curator.ROOT / "machines/partial/stern" / filename).exists())
					self.assertFalse((curator.ROOT / "knowledge/stern" / knowledge_filename).exists())
					self.assertTrue((curator.ROOT / "evidence/runtime/sam" / evidence_filename).exists())

	def test_generator_does_not_clobber_a_promoted_edition(self) -> None:
		curator = load_curator_module()
		for limited_edition in (False, True):
			with self.subTest(edition="limited edition" if limited_edition else "pro"):
				filename = "transformers-limited-edition-2011.json" if limited_edition else "transformers-pro-2011.json"
				knowledge_filename = filename.removesuffix(".json") + ".md"
				with tempfile.TemporaryDirectory() as temporary:
					curator.ROOT = Path(temporary)
					promoted_definition = curator.ROOT / "machines/author-ready/stern" / filename
					promoted_definition.parent.mkdir(parents=True)
					promoted_definition.write_text('{"promoted": true}\n', encoding="utf-8")
					promoted_knowledge = curator.ROOT / "knowledge/stern" / knowledge_filename
					promoted_knowledge.parent.mkdir(parents=True)
					promoted_knowledge.write_text("promoted spatial knowledge\n", encoding="utf-8")
					curator.main()
					self.assertEqual('{"promoted": true}\n', promoted_definition.read_text(encoding="utf-8"))
					self.assertEqual("promoted spatial knowledge\n", promoted_knowledge.read_text(encoding="utf-8"))
					self.assertFalse((curator.ROOT / "machines/partial/stern" / filename).exists())


if __name__ == "__main__":
	unittest.main()
