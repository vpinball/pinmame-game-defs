from __future__ import annotations

import copy
import re
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import _validate_curator_placeholder_digests, _validate_python_line_endings, _validate_runtime_observations, validate_controller_profile, validate_machine, validate_repository


ROOT = Path(__file__).resolve().parents[1]
PRE_FLIPTRONIC_WPC_GENERATIONS = {"0x1", "0x2", "0x4"}


class RepositoryValidationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.transformers = load_json(ROOT / "machines" / "partial" / "stern" / "transformers-limited-edition-2011.json")

	def author_ready_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		definition["coverage"]["status"] = "author_ready"
		definition["coverage"]["missing"] = []
		definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
		return definition

	def shared_rgb_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		definition["coverage"]["status"] = "partial"
		definition["coverage"]["missing"] = ["spatial_placement"]
		template = next(output for output in definition["outputs"] if output["kind"] == "lamp")
		for address, channel in ((900, "blue"), (901, "green"), (902, "red")):
			output = copy.deepcopy(template)
			output["id"] = f"lamp.test-rgb-{address}"
			output["label"] = f"Test RGB {channel}"
			output["availability"] = "used"
			output["binding"] = {"group": "test.rgb", "device": address}
			output["physical"] = {
				"quantity": 2,
				"shared_emitter_group": "rgb.test",
				"emitter_channel": channel,
				"co_located_addresses": [900, 901, 902],
				"shared_physical_quantity": 2,
				"notes": "Three independently controlled channels on one physical RGB emitter group.",
			}
			output["spatial"] = {
				"status": "observed",
				"placements": [
					{
						"id": f"lamp.test-rgb-{address}.emitter",
						"role": "emitter",
						"space": "playfield",
						"x": 0.5,
						"y": 0.5,
						"provenance": copy.deepcopy(template["provenance"]),
					}
				],
			}
			definition["outputs"].append(output)
		return definition

	def test_repository_is_valid(self) -> None:
		self.assertEqual([], validate_repository(ROOT))

	def test_curator_placeholder_digest_guard_rejects_literal_and_expression(self) -> None:
		for placeholder in ('"' + ('0' * 64) + '"', '"0" * 64'):
			with self.subTest(placeholder=placeholder), tempfile.TemporaryDirectory() as temporary_directory:
				root = Path(temporary_directory)
				(root / "tools").mkdir()
				(root / "tools" / "curate_fixture.py").write_text(f"SHA256 = {placeholder}\n", encoding="utf-8")
				errors: list[str] = []
				_validate_curator_placeholder_digests(root, errors)
				self.assertEqual(["tools/curate_fixture.py: contains an all-zero SHA-256 placeholder"], errors)

	def test_generated_json_placeholder_digest_guard_rejects_zero_values(self) -> None:
		for relative_path in ("catalog/fixture.json", "controllers/fixture.json", "machines/partial/fixture.json"):
			with self.subTest(relative_path=relative_path), tempfile.TemporaryDirectory() as temporary_directory:
				root = Path(temporary_directory)
				path = root / relative_path
				path.parent.mkdir(parents=True)
				path.write_text('{"sources":[{"sha256":"' + ('0' * 64) + '"}]}\n', encoding="utf-8")
				errors: list[str] = []
				_validate_curator_placeholder_digests(root, errors)
				self.assertEqual([f"{relative_path} $.sources[0].sha256: contains an all-zero SHA-256 placeholder"], errors)

	def test_knowledge_placeholder_digest_guard_rejects_zero_values(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			root = Path(temporary_directory)
			path = root / "knowledge/fixture.md"
			path.parent.mkdir(parents=True)
			path.write_text(f"Retained artifact SHA-256: {('0' * 64)}\n", encoding="utf-8")
			errors: list[str] = []
			_validate_curator_placeholder_digests(root, errors)
			self.assertEqual(["knowledge/fixture.md: contains an all-zero SHA-256 placeholder"], errors)

	def test_python_line_ending_guard_rejects_crlf(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			root = Path(temporary_directory)
			(root / "tests").mkdir()
			(root / "tests" / "test_fixture.py").write_bytes(b"pass\r\n")
			errors: list[str] = []
			_validate_python_line_endings(root, errors)
			self.assertEqual(["tests/test_fixture.py: Python sources must use LF line endings"], errors)

	def test_author_ready_display_na_provenance_has_core_and_physical_manual_evidence(self) -> None:
		checked = []
		display_count = 0
		for path in sorted((ROOT / "machines" / "author-ready").rglob("*.json")):
			definition = load_json(path)
			if definition.get("coverage", {}).get("status") != "author_ready":
				continue
			for display in definition.get("displays", []):
				spatial = display.get("spatial")
				display_count += 1
				self.assertIsNotNone(spatial, path.as_posix())
				self.assertEqual("not_applicable", spatial.get("status"), path.as_posix())
				self.assertEqual("cabinet_or_service", spatial.get("reason"), path.as_posix())
				sources = {source["id"]: source for source in definition["sources"]}
				refs = spatial["provenance"]["source_refs"]
				self.assertTrue(any(sources[ref].get("kind") == "pinmame_core" for ref in refs), path.as_posix())
				self.assertTrue(any(sources[ref].get("kind") in {"manual", "human_review"} for ref in refs), path.as_posix())
				checked.append(path)
		self.assertGreater(display_count, 0)
		self.assertEqual(display_count, len(checked))

	def test_author_ready_driver_must_match_containing_physical_definition(self) -> None:
		definition = self.author_ready_fixture()
		definition["drivers"][0]["physical_compatibility"] = "different"
		errors = validate_machine(definition)
		self.assertTrue(any("physically compatible with the containing machine definition" in error for error in errors))

	def display_override_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		driver = definition["drivers"][0]
		driver["physical_compatibility"] = "compatible"
		driver["display_overrides"] = [
			{
				"target": definition["displays"][0]["id"],
				"width": definition["displays"][0].get("width", 128) + 1,
				"provenance": {"status": "validated", "source_refs": [definition["sources"][0]["id"]]},
			}
		]
		return definition

	def test_display_override_accepts_a_canonical_display_target(self) -> None:
		self.assertEqual([], validate_machine(self.display_override_fixture()))

	def test_display_override_rejects_invalid_targets_and_duplicate_targets(self) -> None:
		definition = self.display_override_fixture()
		definition["drivers"][0]["display_overrides"].append(
			{
				"target": definition["displays"][0]["id"],
				"controller_index": 9,
				"provenance": {"status": "validated", "source_refs": [definition["sources"][0]["id"]]},
			}
		)
		for override in definition["drivers"][0]["display_overrides"]:
			override["target"] = "display.not-declared"
		errors = validate_machine(definition)
		self.assertTrue(any("must resolve to a canonical display ID" in error for error in errors))
		self.assertTrue(any("duplicate display override target" in error for error in errors))

	def test_display_override_requires_resolved_validated_provenance_and_nonidentical_driver(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		override["provenance"]["source_refs"] = ["missing.source"]
		definition["drivers"][0]["physical_compatibility"] = "identical"
		errors = validate_machine(definition)
		self.assertTrue(any("unknown source reference 'missing.source'" in error for error in errors))
		self.assertTrue(any("physically identical drivers cannot carry display overrides" in error for error in errors))
		definition = self.author_ready_fixture()
		definition["drivers"][0]["physical_compatibility"] = "compatible"
		definition["drivers"][0]["display_overrides"] = [
			{
				"target": definition["displays"][0]["id"],
				"width": definition["displays"][0].get("width", 128),
				"provenance": {"status": "candidate", "source_refs": [definition["sources"][0]["id"]]},
			}
		]
		errors = validate_machine(definition)
		self.assertTrue(any("author-ready display override provenance must be validated" in error for error in errors))

	def test_display_override_schema_requires_a_dimension_and_rejects_extra_fields(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		del override["width"]
		override["unexpected"] = True
		errors = validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "fixture")
		self.assertTrue(any("is not valid under any of the given schemas" in error for error in errors))
		self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

	def test_segment_start_is_valid_only_for_segment_displays(self) -> None:
		definition = self.display_override_fixture()
		display = definition["displays"][0]
		override = definition["drivers"][0]["display_overrides"][0]
		display["segment_start"] = 2
		override["segment_start"] = 1
		errors = validate_machine(definition)
		self.assertTrue(any("segment_start: is only valid for segment displays" in error for error in errors))
		display["kind"] = "segment"
		del display["height"]
		self.assertEqual([], validate_machine(definition))

	def test_author_ready_segment_displays_require_index_start_and_width(self) -> None:
		definition = self.author_ready_fixture()
		display = definition["displays"][0]
		display["kind"] = "segment"
		del display["height"]
		display["segment_start"] = 2
		errors = validate_machine(definition)
		self.assertTrue(any("segment displays require controller_index, segment_start, and width" in error for error in errors))
		display["controller_index"] = 0
		errors = validate_machine(definition)
		self.assertFalse(any("segment displays require" in error for error in errors))

	def test_display_override_must_change_a_canonical_value(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		override["width"] = definition["displays"][0]["width"]
		errors = validate_machine(definition)
		self.assertTrue(any("must change at least one canonical display value" in error for error in errors))

	def test_virtual_machine_records_and_virtual_only_drivers_are_rejected(self) -> None:
		definition = self.author_ready_fixture()
		definition["machine"]["kind"] = "virtual_pinball"
		definition["drivers"][0]["id"] = "che_cho"
		errors = validate_machine(definition)
		self.assertTrue(any("outside the physical-machine scope" in error and "$.machine.kind" in error for error in errors))
		self.assertTrue(any("outside the physical-machine scope" in error and "$.drivers[0].id" in error for error in errors))

	def test_mechanism_actuator_can_have_only_one_owner(self) -> None:
		definition = self.author_ready_fixture()
		actuator = definition["mechanisms"][0]["actuators"][0]
		definition["mechanisms"][1]["actuators"].append(actuator)
		errors = validate_machine(definition)
		self.assertTrue(any("is already owned" in error for error in errors))

	def test_physical_solenoid_connection_can_have_only_one_owner(self) -> None:
		definition = self.author_ready_fixture()
		physical_outputs = [output for output in definition["outputs"] if output["binding"]["group"] == "pinmame.output.solenoid" and output.get("kind") != "virtual" and output.get("availability") in {"used", "optional"} and output.get("wiring", {}).get("control_connection")]
		physical_outputs[1]["wiring"]["board"] = physical_outputs[0]["wiring"]["board"]
		physical_outputs[1]["wiring"]["control_connection"] = physical_outputs[0]["wiring"]["control_connection"]
		errors = validate_machine(definition)
		self.assertTrue(any("duplicates physical output connection" in error for error in errors))

	def test_shared_rgb_emitter_metadata_is_atomic_and_cross_checked(self) -> None:
		definition = self.shared_rgb_fixture()
		self.assertEqual([], validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "shared-rgb"))
		self.assertFalse(any("shared RGB emitter" in error for error in validate_machine(definition)))

		cases = (
			("missing field", lambda value: value["outputs"][-1]["physical"].pop("shared_physical_quantity"), "metadata fields must appear together"),
			("missing sibling", lambda value: value["outputs"][-1]["physical"].update({"co_located_addresses": [900, 901, 999]}), "not present in the same output group"),
			("own address omitted", lambda value: value["outputs"][-3]["physical"].update({"co_located_addresses": [901, 902]}), "own address must be included"),
			("address disagreement", lambda value: value["outputs"][-2]["physical"].update({"co_located_addresses": [900, 901]}), "agree on the complete address set"),
			("group disagreement", lambda value: value["outputs"][-2]["physical"].update({"shared_emitter_group": "rgb.other"}), "agree on shared emitter group identity"),
			("quantity disagreement", lambda value: value["outputs"][-2]["physical"].update({"quantity": 3, "shared_physical_quantity": 3}), "agree on the shared physical quantity"),
			("quantity mismatch", lambda value: value["outputs"][-2]["physical"].update({"quantity": 3}), "must equal shared_physical_quantity"),
			("channel set", lambda value: value["outputs"][-2]["physical"].update({"emitter_channel": "blue"}), "unique exact blue/green/red set"),
			("coordinate mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"x": 0.6}), "equivalent coordinates, roles, and coordinate space"),
			("role mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"role": "effect"}), "equivalent coordinates, roles, and coordinate space"),
			("space mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"space": "backglass"}), "equivalent coordinates, roles, and coordinate space"),
		)
		for name, mutate, expected in cases:
			with self.subTest(name=name):
				invalid = self.shared_rgb_fixture()
				mutate(invalid)
				self.assertTrue(any(expected in error for error in validate_machine(invalid)), name)
		missing = self.shared_rgb_fixture()
		missing["outputs"][-1]["physical"].pop("shared_physical_quantity")
		self.assertTrue(validate_against_schema(missing, ROOT / "schemas" / "machine.schema.json", "shared-rgb-missing-field"))

	def test_author_ready_sam_requires_one_unwired_virtual_game_on_output(self) -> None:
		definition = self.author_ready_fixture()
		definition["outputs"] = [output for output in definition["outputs"] if output["binding"] != {"device": 33, "group": "pinmame.output.solenoid"}]
		self.assertTrue(any("must declare public solenoid 33 exactly once" in error for error in validate_machine(definition)))
		definition = self.author_ready_fixture()
		game_on = next(output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"})
		game_on["kind"] = "coil"
		game_on["wiring"] = {"board": "invented"}
		errors = validate_machine(definition)
		self.assertTrue(any("never a physical device" in error for error in errors))
		self.assertTrue(any("cannot have physical wiring" in error for error in errors))

	def test_runtime_observations_must_map_to_author_ready_outputs(self) -> None:
		definition = self.author_ready_fixture()
		evidence = {"machine_ids": [definition["machine"]["id"]], "runtime": {"observations": {"solenoid_addresses_seen": [999]}}}
		errors: list[str] = []
		_validate_runtime_observations(evidence, "evidence/test.json", {definition["machine"]["id"]: definition}, errors)
		self.assertTrue(any("address 999 is not declared" in error for error in errors))

	def test_current_sam_partials_retain_consistent_game_on_semantics(self) -> None:
		for path in (ROOT / "machines" / "partial" / "stern").rglob("*.json"):
			definition = load_json(path)
			if definition.get("controller", {}).get("platform") != "pinmame.sam":
				continue
			matches = [output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"}]
			self.assertEqual(1, len(matches), path.as_posix())
			self.assertEqual("virtual", matches[0]["kind"], path.as_posix())
			self.assertNotIn("wiring", matches[0], path.as_posix())

	def test_constant_zero_virtual_wpc_state_channels_are_unused(self) -> None:
		checked: list[str] = []
		for path in sorted((ROOT / "machines").rglob("*.json")):
			definition = load_json(path)
			if not definition.get("controller", {}).get("platform", "").startswith("pinmame.wpc"):
				continue
			channels = [output for output in definition["outputs"] if output["binding"] == {"device": 32, "group": "pinmame.output.solenoid"}]
			if definition["coverage"]["dimensions"].get("address_enumeration") == "validated":
				self.assertTrue(channels, f"{path.as_posix()}: validated WPC address enumeration omits public channel 32")
			if not channels:
				continue
			self.assertEqual(1, len(channels), path.as_posix())
			channel = channels[0]
			self.assertEqual("virtual", channel["kind"], path.as_posix())
			self.assertEqual("unused", channel["availability"], path.as_posix())
			self.assertEqual(["internal.unused.wpc-output"], channel["roles"], path.as_posix())
			self.assertEqual("virtual", channel["spatial"]["reason"], path.as_posix())
			self.assertIn("zero", channel["physical"]["notes"].lower(), path.as_posix())
			self.assertNotIn("once a fast-flip address is configured", channel["physical"]["notes"].lower(), path.as_posix())
			for address in (29, 30, 31):
				state = [output for output in definition["outputs"] if output["binding"] == {"device": address, "group": "pinmame.output.solenoid"}]
				self.assertEqual(1, len(state), f"{path.as_posix()}: missing WPC state channel {address}")
				self.assertEqual("used", state[0]["availability"], f"{path.as_posix()}:{address}")
				self.assertEqual(["internal.wpc-state"], state[0]["roles"], f"{path.as_posix()}:{address}")
				if address == 31 and definition["controller"].get("hardware_generation") in PRE_FLIPTRONIC_WPC_GENERATIONS:
					self.assertEqual("relay", state[0]["kind"], f"{path.as_posix()}:{address}")
					self.assertEqual("cabinet_or_service", state[0]["spatial"]["reason"], f"{path.as_posix()}:{address}")
				else:
					self.assertEqual("virtual", state[0]["kind"], f"{path.as_posix()}:{address}")
					self.assertEqual("virtual", state[0]["spatial"]["reason"], f"{path.as_posix()}:{address}")
			checked.append(definition["machine"]["id"])
		self.assertGreaterEqual(len(checked), 20)

	def test_optional_playfield_extent_is_accepted_constrained_and_never_required(self) -> None:
		# The playfield block exists only so a consumer can render normalized placements at the
		# right aspect ratio. It must stay optional, so every already-published definition that
		# omits it keeps validating, and it must reject nonsense rather than silently carry it.
		definition = load_json(ROOT / "machines" / "partial" / "williams" / "monster-bash-1998.json")
		self.assertNotIn("playfield", definition["machine"])
		self.assertEqual([], validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "no-playfield"))

		accepted = copy.deepcopy(definition)
		accepted["machine"]["playfield"] = {"width": 952.0, "height": 2162.0, "units": "vpx"}
		self.assertEqual([], validate_against_schema(accepted, ROOT / "schemas" / "machine.schema.json", "playfield"))

		for label, block in (
			("zero width", {"width": 0, "height": 2162.0, "units": "vpx"}),
			("negative height", {"width": 952.0, "height": -1, "units": "vpx"}),
			("unknown units", {"width": 952.0, "height": 2162.0, "units": "furlong"}),
			("missing height", {"width": 952.0, "units": "vpx"}),
			("extra key", {"width": 952.0, "height": 2162.0, "units": "vpx", "depth": 5}),
		):
			rejected = copy.deepcopy(definition)
			rejected["machine"]["playfield"] = block
			self.assertNotEqual([], validate_against_schema(rejected, ROOT / "schemas" / "machine.schema.json", label), label)

	def test_controller_plugin_routes_match_pinmame_contract(self) -> None:
		expected = {
			"pinmame.input.switch": 1,
			"pinmame.output.solenoid": 1,
			"pinmame.output.gi": 256,
			"pinmame.output.lamp": 512,
		}
		for path in sorted((ROOT / "controllers" / "pinmame").glob("*.json")):
			profile = load_json(path)
			groups = {group["id"]: group for group in profile["groups"]}
			for group_id, expected_group_id in expected.items():
				plugin = groups.get(group_id, {}).get("transports", {}).get("controller_plugin")
				if plugin is not None:
					self.assertEqual(expected_group_id, plugin["group_id"], f"{path.name}:{group_id}")
			if path.name == "sam.json":
				self.assertEqual({}, groups["physical.output.ticket"]["transports"])
			self.assertEqual("https://github.com/vpinball/pinmame", profile["sources"][-1]["uri"])

		invalid = copy.deepcopy(load_json(ROOT / "controllers" / "pinmame" / "data-east.json"))
		solenoid = next(group for group in invalid["groups"] if group["id"] == "pinmame.output.solenoid")
		solenoid["transports"]["controller_plugin"]["group_id"] = 256
		self.assertTrue(
			any("requires 1, got 256" in error for error in validate_controller_profile(invalid))
		)
		invalid["groups"][0]["id"] = []
		self.assertIsInstance(validate_controller_profile(invalid), list)

	def test_controller_notes_format_requires_notes(self) -> None:
		profile = copy.deepcopy(load_json(ROOT / "controllers" / "pinmame" / "capcom.json"))
		group = profile["groups"][0]
		group.pop("notes")
		group["notes_format"] = "markdown"
		errors = validate_against_schema(profile, ROOT / "schemas" / "controller.schema.json", "controller-notes-format")
		self.assertTrue(any("notes" in error for error in errors), errors)

	def test_controller_markdown_notes_follow_the_rendering_contract(self) -> None:
		profiles = [load_json(path) for path in sorted((ROOT / "controllers" / "pinmame").glob("*.json"))]
		groups = [group for profile in profiles for group in profile["groups"]]
		self.assertEqual(12, len(profiles))
		self.assertEqual(38, sum(group.get("notes_format") == "markdown" for group in groups))
		self.assertEqual(9, sum("notes" in group and "notes_format" not in group for group in groups))
		self.assertEqual(9, sum("notes" not in group for group in groups))
		for group in groups:
			if group.get("notes_format") != "markdown":
				continue
			notes = group["notes"]
			with self.subTest(group=group["id"]):
				self.assertNotRegex(notes, r"<[A-Za-z][^>]*>")
				headings = re.findall(r"(?m)^(#{1,6})\s+", notes)
				self.assertTrue(all(len(heading) >= 4 for heading in headings), notes)
				self.assertRegex(notes, r"(?m)(^####\s|^\|.+\|$|^[-*]\s|\*\*.+?\*\*|`[^`]+`)")

	def test_capcom_flasher_ranges_match_pinned_source(self) -> None:
		profile = load_json(ROOT / "controllers" / "pinmame" / "capcom.json")
		notes = next(group["notes"] for group in profile["groups"] if group["id"] == "pinmame.output.solenoid")
		for table_row in (
			"| `abv` | Airborne | `20-27` |",
			"| `bbb` | Big Bang Bar | `21-26` |",
			"| `bsv` | Breakshot | `28-32` |",
			"| `ffv` | Flipper Football | `28-32` |",
			"| `kpb` | Kingpin | `18-19`, `21-31` |",
			"| `pmv` | Pinball Magic | `21-31` |",
		):
			self.assertIn(table_row, notes)
		self.assertIn("alternative plunger range at `27-31`", notes)
		self.assertIn("Kingpin's two ranges are explicitly provisional", notes)

	def test_capcom_breakshot_switch_exception_is_documented(self) -> None:
		profile = load_json(ROOT / "controllers" / "pinmame" / "capcom.json")
		notes = next(group["notes"] for group in profile["groups"] if group["id"] == "pinmame.input.switch")
		self.assertIn("When `HAS_SWITCH_BOARD` is true", notes)
		self.assertIn("`src/wpc/capcom.h`", notes)
		self.assertNotIn("capcoms.h", notes)
		self.assertIn("internal switch column 0 (`src/wpc/capcom.h`)", notes)
		self.assertNotIn("also calls this 'switch column 9'", notes)
		self.assertIn("low nibble (bits 0-3)", notes)
		self.assertIn("public addresses 29-32", notes)
		self.assertIn("lamp-column-strobed switch matrix", notes)


if __name__ == "__main__":
	unittest.main()
