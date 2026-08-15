from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "revenge-from-mars-1999.json"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "p2k.json"
EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "operations-manual-service-tables.md"
POLARITY_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "operations-manual-switch-polarity.md"
LOCATION_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "operations-manual-location-maps.md"
AFTERMARKET_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "mypinballs-opto-expansion-install.md"
UPDATE_LOG_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "mypinballs-code-update-log.md"
MECHANISM_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "operations-manual-mechanism-assemblies.md"
LOCK_DIVERTER_EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "pinside-lock-diverter-service-observation.md"
STOCK_RUNTIME_PATH = ROOT / "evidence" / "runtime" / "p2k" / "revenge-from-mars-stock-ball-serve.json"
DEBUG_RUNTIME_PATH = ROOT / "evidence" / "runtime" / "p2k" / "revenge-from-mars-debug-ball-cycle.json"
SERVICE_RUNTIME_PATH = ROOT / "evidence" / "runtime" / "p2k" / "revenge-from-mars-solenoid-service-test.json"
SERVICE_SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "pinball-2000" / "rfm-solenoid-service-test.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "revenge-from-mars-1999.json"
LOCATION_IMAGES = {
	"lamp-locations-matrix-a.webp": "212a2bfc3d3e0a78c04210fb601692c77b7bc76fd44c2a41ca7ed2dab7e7a7cb",
	"lamp-locations-matrix-b.webp": "c8a9acc6c349db286d05f681a3182a373d6bd0f607eec927c21c143d45061b87",
	"playfield-switch-locations.webp": "3c55555ed5637207efe17e992b26c09662f0986d633367555ebe94dc66b1e221",
	"solenoid-flasher-locations.webp": "d9b66fa87bb5cd85f0ee5098fc76040fd489fb87d852ccf8613c55a7308862ca",
	"aftermarket-six-ball-trough.webp": "af9c94880b4ac4cc43306ca8b8d7d59b3613e79a31fa9ef8b44a83157ff4336a",
	"aftermarket-three-ball-lock.webp": "f738eaf5371e08fd1c4bc8404b1aa5ebf79bb9e95b027308616df5f81b1934e0",
}
FACTORY_LOCATION_IMAGES = {
	"lamp-locations-matrix-a.webp",
	"lamp-locations-matrix-b.webp",
	"playfield-switch-locations.webp",
	"solenoid-flasher-locations.webp",
}
MECHANISM_IMAGES = {
	"mechanism-auto-fire-assembly.webp": "16a2385e6d47b2068f29513d344a43ac69754ea4dd4ee7424fb582c519615fe2",
	"mechanism-ball-trough-assembly.webp": "f1ef59b0f2809c98dfe1b5c8edf4d3fc016d48d879da6be9ce24016591e44f2b",
	"mechanism-right-flipper-assembly.webp": "fc8ad6422bd497b883706246ec95538daadfb0a0b971c9d709ebd06326d8bd3f",
	"mechanism-left-flipper-assembly.webp": "bb00de9caa76132e9620c5893c41b0535df1b86967e9cc4e5ae96d8c2110f31e",
	"mechanism-slingshot-kicker-assembly.webp": "58f88b77854a0f18d631ec1ec7606689f45b87477e337c0bc612c4da8d8bb6f7",
	"mechanism-skip-ramp-assembly.webp": "c3760e1d669e77cbfec0cd6490c8a9fd6ec56f9f427a09c8d2a4c094393caa6f",
	"mechanism-right-popper-assembly.webp": "66236d2c1d05e38a04461252a0246996a58040881458597dc20856dd8d1d762c",
	"mechanism-drop-target-assembly.webp": "8e863fb2401f323d41971b4c8338e44990ee1c61973380428e301bcb48965109",
	"mechanism-right-lockup-assembly.webp": "eb7166541f50ec9dfb84bff4ed37e97e430d4d2b52ed63b9ea5f8908445eee42",
	"mechanism-lock-diverter-assembly.webp": "0c44970314fdb17fc5e097e3670d56af01b3345f302d12280d3897b64464c8e6",
	"mechanism-ball-gate-assembly.webp": "acae05724e5ec4c119c9590779f5a12e748d4d852cc28ff5d403283ea0cfa78d",
	"mechanism-jet-exit-post-assembly.webp": "e2d0119958c6ad4e8ee416aaf68bfbb36123361224c5393fe58c465d79d20025",
	"mechanism-ball-catcher-assembly.webp": "c6994f7baedccfc6f38bf11aaa74bc4f49210dd71ddd280467f428e325b35590",
	"mechanism-martian-assembly.webp": "34208a13c91759a01ace00fce2d3574724f8d4d19ace4809012ece1b8d31b961",
	"mechanism-jet-coil-assembly.webp": "3601a63bb575dff4f135a549c4d7135767624666ea0f1842f69e6d923c57346a",
	"mechanism-jet-bumper-b9414-6-assembly.webp": "4a0d13c3fb045167f688a3972f78fbdc79b5192c4ff25f8e43c4b856ef940045",
	"mechanism-jet-bumper-b13123-2-assembly.webp": "d871a51a91c9c8c4ab9e70e83ec9e534f84fda269dbd3c5cf2d391639f0f5f78",
}
RFM_DRIVERS = {
	"rfm_120", "rfm_140", "rfm_150", "rfm_160", "rfm_180", "rfm_190", "rfm_191", "rfm_195",
	"rfm_200", "rfm_210", "rfm_222", "rfm_223", "rfm_224", "rfm_250", "rfm_260",
}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class RevengeFromMarsDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.controller = load_json(CONTROLLER_PATH)
		cls.spatial_report = load_json(SPATIAL_REPORT_PATH)

	def test_identity_controller_and_driver_family(self) -> None:
		self.assertEqual(
			{"id": "bally.revenge-from-mars.1999", "name": "Revenge from Mars", "manufacturer": "Bally", "year": 1999, "kind": "physical_pinball", "model_number": "50070", "ipdb_id": 4446},
			self.definition["machine"],
		)
		self.assertEqual("pinmame.p2k", self.definition["controller"]["platform"])
		self.assertEqual("0x8000000000000", self.definition["controller"]["hardware_generation"])
		self.assertEqual(RFM_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})

	def test_curator_is_deterministic_and_matches_the_committed_outputs(self) -> None:
		import curate_revenge_from_mars as curator

		first = curator.expected_files()
		second = curator.expected_files()
		self.assertEqual(first, second)
		for path, expected in first.items():
			self.assertEqual(expected, path.read_text(encoding="utf-8"), path)

	def test_controller_exposes_only_the_p2k_public_ranges(self) -> None:
		groups = {group["id"]: group for group in self.controller["groups"]}
		self.assertEqual({"pinmame.input.switch", "pinmame.output.solenoid", "pinmame.output.lamp"}, set(groups))
		self.assertEqual([{"minimum": 0, "maximum": 127}], groups["pinmame.output.lamp"]["address_rules"])
		self.assertEqual(
			[{"minimum": 1, "maximum": 32}, {"minimum": 45, "maximum": 48}, {"minimum": 51, "maximum": 62}],
			groups["pinmame.output.solenoid"]["address_rules"],
		)
		polarity_notes = groups["pinmame.input.switch"]["notes"]
		for token in ("mixed raw public levels", "active-low", "active-high", "exactly as delivered"):
			self.assertIn(token, polarity_notes)

	def test_all_switch_driver_and_lamp_positions_are_explicit(self) -> None:
		inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]}
		expected_inputs = {column * 10 + row for column in range(1, 9) for row in range(1, 9)} | set(range(91, 99)) | set(range(101, 109)) | set(range(111, 119))
		self.assertEqual(expected_inputs, set(inputs))
		self.assertEqual(88, len(inputs))
		self.assertEqual({53, 54, 55, 56}, {address for address, item in inputs.items() if item["availability"] == "optional"})
		self.assertEqual({41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56}, {address for address, item in inputs.items() if item.get("normally_closed")})
		self.assertTrue(all(item["normally_closed"] is False for item in inputs.values() if item["availability"] == "used" and item["binding"]["device"] not in {41, 42, 43, 44, 45, 46, 47, 51, 52}))
		self.assertTrue(all("normally_closed" not in item for item in inputs.values() if item["availability"] == "unused"))
		self.assertTrue(all("active-low" in inputs[address]["physical"]["notes"] for address in {41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56}))
		self.assertTrue(all("active-high" in item["physical"]["notes"] for item in inputs.values() if item["availability"] == "used" and item["binding"]["device"] not in {41, 42, 43, 44, 45, 46, 47, 51, 52}))
		expected_manual_types = {15: "microswitch", 38: "microswitch", 63: "leaf", 64: "leaf", 65: "leaf", 75: "microswitch", 105: "leaf", 106: "leaf"}
		self.assertEqual(expected_manual_types, {address: inputs[address]["physical"]["switch_type"] for address in expected_manual_types})
		self.assertEqual({61: "unknown", 62: "unknown"}, {address: inputs[address]["physical"]["switch_type"] for address in (61, 62)})
		expected_manual_parts = {15: "5647-12693-31", 38: "5647-12693-07", 63: "A-16443-1", 64: "A-16443-1", 65: "A-16443-1", 75: "5647-12693-11", 105: "SW-1A-194", 106: "SW-1A-194"}
		self.assertEqual(expected_manual_parts, {address: inputs[address]["physical"]["part_number"] for address in expected_manual_parts})
		expected_manual_assemblies = {15: "A-15211-1", 38: "A-22989", 63: "A-12030-3", 64: "A-12030-3", 65: "A-12030-3", 75: "A-22992", 105: "A-23004-R-2", 106: "A-23001-L-2"}
		self.assertEqual(expected_manual_assemblies, {address: inputs[address]["physical"]["assembly_part_number"] for address in expected_manual_assemblies})

		solenoids = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		self.assertEqual(set(range(1, 33)) | set(range(45, 49)) | set(range(51, 63)), set(solenoids))
		self.assertEqual("Right Flipper Power", solenoids[45]["label"])
		self.assertEqual("Lock Diverter Power", solenoids[51]["label"])
		self.assertEqual("Ticket Dispenser (Optional)", solenoids[62]["label"])
		for address in range(29, 33):
			self.assertEqual("used", solenoids[address]["availability"])
			self.assertEqual("virtual", solenoids[address]["kind"])
			self.assertEqual("virtual", solenoids[address]["spatial"]["reason"])
			self.assertIn(f"register 0x0D at public address {address}", solenoids[address]["physical"]["notes"])
			self.assertIn("runtime.rfm.stock-ball-serve", solenoids[address]["provenance"]["source_refs"])
			self.assertNotIn("manual.rfm.operations-1999", solenoids[address]["provenance"]["source_refs"])
			self.assertNotIn("manual.rfm.operations-1999", solenoids[address]["spatial"]["provenance"]["source_refs"])
		self.assertIn("service-diagnostic.rfm.solenoid-test", solenoids[29]["provenance"]["source_refs"])
		self.assertNotIn("service-diagnostic.rfm.solenoid-test", solenoids[31]["provenance"]["source_refs"])

		lamps = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual(set(range(128)), set(lamps))
		self.assertEqual("Start Button", lamps[2]["label"])
		self.assertEqual("Right Slingshot Spotlight", lamps[15]["label"])
		self.assertEqual("Left Slingshot Spotlight", lamps[31]["label"])
		self.assertEqual("11A", next(alias["value"] for alias in lamps[0]["aliases"] if alias["namespace"] == "manual.address"))
		self.assertEqual("88B", next(alias["value"] for alias in lamps[127]["aliases"] if alias["namespace"] == "manual.address"))

	def test_video_contract_preserves_the_line_doubled_export(self) -> None:
		self.assertEqual(
			[{"id": "display.pinball-2000-video", "label": "Pinball 2000 reflected playfield video", "kind": "video", "controller_index": 0, "width": 640, "height": 480, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": ["pinmame.core.8371478a7640", "manual.rfm.operations-1999", "runtime.rfm.stock-ball-serve"]}}, "provenance": {"status": "validated", "source_refs": ["pinmame.core.8371478a7640", "manual.rfm.operations-1999", "runtime.rfm.stock-ball-serve"]}}],
			self.definition["displays"],
		)

	def test_factory_location_drawings_validate_stock_spatial_placement(self) -> None:
		self.assertEqual(["variant_differences"], self.definition["coverage"]["missing"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["variant_coverage"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["mechanisms"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertTrue(all("spatial" in item for item in self.definition["inputs"] + self.definition["outputs"]))
		self.assertEqual(49, sum(item["spatial"]["status"] == "validated" for item in self.definition["inputs"]))
		self.assertEqual(143, sum(item["spatial"]["status"] == "validated" for item in self.definition["outputs"]))

		inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]}
		self.assertEqual((0.9, 0.08, "sensor"), self._placement(inputs[11]))
		self.assertEqual(self._placement(inputs[31]), self._placement(inputs[32]))
		self.assertIn("prints address 31 twice", inputs[31]["physical"]["notes"])
		self.assertEqual("internal_nonvisual", inputs[105]["spatial"]["reason"])
		self.assertEqual("internal_nonvisual", inputs[106]["spatial"]["reason"])
		aftermarket_positions = {53: (0.34, 0.97, "sensor"), 54: (0.26, 0.97, "sensor"), 55: (0.695, 0.185, "sensor"), 56: (0.695, 0.165, "sensor")}
		for address, expected_position in aftermarket_positions.items():
			self.assertEqual("optional", inputs[address]["availability"])
			self.assertEqual("validated", inputs[address]["spatial"]["status"])
			self.assertEqual(expected_position, self._placement(inputs[address]))
			self.assertEqual(["manual.rfm.operations-1999", "manual.rfm.mypinballs-opto-expansion-v2"], inputs[address]["spatial"]["placements"][0]["provenance"]["source_refs"])
			self.assertIn("reviewed", inputs[address]["physical"]["notes"])

		outputs = {(item["binding"]["group"], item["binding"]["device"]): item for item in self.definition["outputs"]}
		self.assertEqual((0.5, 0.86, "emitter"), self._placement(outputs[("pinmame.output.lamp", 68)]))
		self.assertEqual((0.5, 0.43, "emitter"), self._placement(outputs[("pinmame.output.solenoid", 17)]))
		self.assertEqual((0.65, 0.82, "effect"), self._placement(outputs[("pinmame.output.solenoid", 45)]))
		self.assertEqual(self._placement(outputs[("pinmame.output.solenoid", 45)]), self._placement(outputs[("pinmame.output.solenoid", 46)]))

	def test_matrix_b_lower_cluster_follows_the_drawing_depth(self) -> None:
		lamps = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual((0.574, 0.62, "emitter"), self._placement(lamps[26]))
		self.assertEqual((0.4, 0.66, "emitter"), self._placement(lamps[58]))
		self.assertEqual((0.4, 0.58, "emitter"), self._placement(lamps[60]))
		self.assertEqual((0.22, 0.73, "emitter"), self._placement(lamps[15]))
		self.assertEqual((0.78, 0.73, "emitter"), self._placement(lamps[31]))
		rim = {42, 43, 44, 45, 46, 59, 60, 61, 62}
		weapons = {26, 27, 28}
		wedges = {25, 29, 30, 41, 58}
		arc = {8, 10, 12, 14, 24, 40, 56, 57}
		front = {9, 11, 13}
		depth = lambda addresses: [self._placement(lamps[address])[1] for address in addresses]
		self.assertLess(max(depth(rim)), min(depth(weapons)))
		self.assertLess(max(depth(weapons)), min(depth(wedges)))
		self.assertLess(max(depth(wedges)), min(depth(arc)))
		self.assertLess(max(depth(arc)), min(depth(front)))
		coordinates: dict[tuple[float, float], int] = {}
		for address, lamp in lamps.items():
			if lamp["spatial"]["status"] == "not_applicable":
				continue
			x, y, _ = self._placement(lamp)
			self.assertNotIn((x, y), coordinates, f"lamp {address} duplicates lamp {coordinates.get((x, y))}")
			coordinates[(x, y)] = address

	@staticmethod
	def _placement(item: dict[str, object]) -> tuple[float, float, str]:
		placement = item["spatial"]["placements"][0]
		return placement["x"], placement["y"], placement["role"]

	def test_manual_and_rejected_vpx_are_content_locked(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.rfm.operations-1999"]
		aftermarket = sources["manual.rfm.mypinballs-opto-expansion-v2"]
		update_log = sources["service-bulletin.rfm.mypinballs-code-updates"]
		diverter_review = sources["human-review.rfm.pinside-lock-diverter"]
		self.assertEqual("6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df", manual["sha256"])
		self.assertEqual("00a744e1cc6507c328b22f33fc4f3aa6f8ec4826dce0a8874493023ee8d48fbf", aftermarket["sha256"])
		self.assertEqual("https://www.mypinballs.com/software/rfm/code_updates.jsp", update_log["uri"])
		self.assertEqual("2026-08-15T17:11:46Z", update_log["acquired_at"])
		self.assertEqual("https://pinside.com/pinball/forum/topic/rfm-diverter-closes-but-doesnt-open-fully", diverter_review["uri"])
		self.assertEqual("2026-08-15T20:40:35Z", diverter_review["acquired_at"])
		self.assertEqual("9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be", sources["vpx-table.attack-and-revenge-v600-rejected"]["sha256"])
		self.assertFalse(sources["vpx-table.attack-and-revenge-v600-rejected"]["known_working"])
		self.assertIn("cGameName=afm_113b", sources["vpx-table.attack-and-revenge-v600-rejected"]["locator"])
		self.assertEqual("e283b2b47f41ebe5c5464d2cda49df531d069dc57db8e91f29c12c9ef90c663b", hashlib.sha256(EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("ebeaa81f508e100314320e2014e86f0cff8bfc8726e5c47d103f0499047db88a", hashlib.sha256(POLARITY_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("7977b64e33308e8ee163a197d6c2426f9ce236e85cfcf47bcede5dd003776815", hashlib.sha256(LOCATION_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("4d4622669b0bd622d132d5c1543ec22651cefb5446051141c4e1c4f92da6040d", hashlib.sha256(AFTERMARKET_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("bc85edefe9b568bcc020ce9f6e1d79f0c05a7f4691cb7cbf16533e85ee0e0895", hashlib.sha256(UPDATE_LOG_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("9922331222bec6dae27b8dee7e646d0c52c2f61d6862b0842cda2ee921918038", hashlib.sha256(MECHANISM_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual("e78b555ab28f737321d9aaa988d88761fc94dc1769272e3ad77c06e7223ef22d", hashlib.sha256(LOCK_DIVERTER_EXCERPT_PATH.read_bytes()).hexdigest())
		self.assertEqual(23, len(manual["excerpts"]))
		self.assertEqual(21, sum("image" in excerpt for excerpt in manual["excerpts"]))
		self.assertEqual(2, len(aftermarket["excerpts"]))
		self.assertEqual(1, len(update_log["excerpts"]))
		for filename, expected_sha256 in LOCATION_IMAGES.items():
			image_path = LOCATION_EXCERPT_PATH.parent / filename
			self.assertLess(image_path.stat().st_size, 1_500_000 if filename in FACTORY_LOCATION_IMAGES else 100_000)
			self.assertEqual(expected_sha256, hashlib.sha256(image_path.read_bytes()).hexdigest())
		for filename, expected_sha256 in MECHANISM_IMAGES.items():
			image_path = MECHANISM_EXCERPT_PATH.parent / filename
			self.assertLess(image_path.stat().st_size, 100_000)
			self.assertEqual(expected_sha256, hashlib.sha256(image_path.read_bytes()).hexdigest())

	def test_spatial_report_preserves_projection_and_remaining_blockers(self) -> None:
		self.assertEqual("pinmame-spatial-blockers", self.spatial_report["format"])
		self.assertEqual("bally.revenge-from-mars.1999", self.spatial_report["machine_id"])
		self.assertEqual("stock_spatial_validated_machine_partial", self.spatial_report["status"])
		self.assertEqual(192, self.spatial_report["placement_count"])
		self.assertNotIn("no_physical_device", self.spatial_report["not_applicable_inputs"])
		self.assertEqual([105, 106], self.spatial_report["not_applicable_inputs"]["internal_nonvisual"])
		self.assertNotIn(105, self.spatial_report["not_applicable_inputs"]["cabinet_or_service"])
		self.assertNotIn(106, self.spatial_report["not_applicable_inputs"]["cabinet_or_service"])
		shared_effect = next(item["detail"] for item in self.spatial_report["projection_classes"] if item["class"] == "shared_mechanism_effect")
		for public_pair in ("45/46", "47/48", "51/52", "53/54", "6/7"):
			self.assertIn(public_pair, shared_effect)
		self.assertEqual(6, len(self.spatial_report["evidence"]))
		self.assertEqual(4, sum("projection_review_frame" in evidence for evidence in self.spatial_report["evidence"]))
		self.assertEqual("remain_partial", self.spatial_report["promotion_decision"]["decision"])
		self.assertEqual(["variant_differences"], self.spatial_report["promotion_decision"]["coverage_missing"])
		self.assertEqual(["variant-prism-factory-pairing"], [item["id"] for item in self.spatial_report["unresolved_blockers"]])
		self.assertIn("unchecked assumption", self.spatial_report["unresolved_blockers"][0]["blocker"])
		self.assertNotIn("description", self.spatial_report["unresolved_blockers"][0])

	def test_firmware_hardware_contract_is_explicit(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("compatible", drivers["rfm_222"]["physical_compatibility"])
		self.assertIn("six balls", drivers["rfm_222"]["variant_notes"])
		self.assertIn("also released as 2.30", drivers["rfm_222"]["variant_notes"])
		self.assertEqual("different", drivers["rfm_260"]["physical_compatibility"])
		for token in ("requires", "53-54", "55-56", "three physical"):
			self.assertIn(token, drivers["rfm_260"]["variant_notes"])
		for driver in drivers.values():
			self.assertIn("revision-1 Prism banks", driver["variant_notes"])
			self.assertIn("shipping pairing unverified", driver["variant_notes"])
			self.assertIn("does not change gameplay", driver["variant_notes"])

	def test_runtime_evidence_pins_release_debug_and_service_cycles(self) -> None:
		stock = load_json(STOCK_RUNTIME_PATH)
		debug = load_json(DEBUG_RUNTIME_PATH)
		service = load_json(SERVICE_RUNTIME_PATH)
		self.assertEqual("deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c", stock["runtime"]["emulator"]["sha256"])
		self.assertEqual("a236d6b7d16efe9c56425affb6c59872c78d801ce106a0bc1af697237c5c8060", stock["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("642645d81cdc10189c6592e4e1407b399e19ef7ec6f3eae2bf42dda78bedb3f7", stock["runtime"]["raw_runs"][0]["scenario_sha256"])
		self.assertEqual([{"depth": 24, "height": 480, "type": 15, "width": 640}], stock["runtime"]["observations"]["display_layouts_seen"])
		self.assertEqual("057ead79397dce64cdd6798dbb8d1042b9224304c3fd7c3daa43aae2875a494c", debug["runtime"]["emulator"]["sha256"])
		self.assertEqual("3c77df07b1127aa4784ff939f7b8eb31021cdb34903a87b5f7f3f3c341c315d9", debug["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("f7df41e0c3ba6afd9aa36066fc57d52ea5a3f49ef1ec52b1b1c9b27c63589a85", debug["runtime"]["raw_runs"][0]["scenario_sha256"])
		for observation in stock["runtime"]["observations"]["named_action_observations"]:
			self.assertEqual([], observation["observed_switch_addresses"])
			self.assertTrue(observation["host_stimulus_switch_addresses"])
		self.assertTrue({5, 29, 30, 31, 32}.issubset(stock["runtime"]["observations"]["solenoid_addresses_seen"]))
		for observation in debug["runtime"]["observations"]["runs"]["debug-ball-cycle-02"]["named_action_observations"]:
			self.assertTrue(observation["observed_switch_addresses"])
			self.assertTrue(observation["host_stimulus_switch_addresses"])
		note = debug["runtime"]["observations"]["runs"]["debug-ball-cycle-02"]["note"]
		for token in ("42-45", "driver 9", "switch 18", "driver 15", "modeled drain"):
			self.assertIn(token, note)
		self.assertEqual("deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c", service["runtime"]["emulator"]["sha256"])
		self.assertEqual("47df7e4c1139f14e227334d2d87b809cc78c66ed5c0f334b31bc6a435d654afc", service["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("ebd7d68968d6c953d8921cc23588bb4f3831a2e0913de39601b19f9833a62635", service["runtime"]["raw_runs"][0]["scenario_sha256"])
		self.assertEqual("ebd7d68968d6c953d8921cc23588bb4f3831a2e0913de39601b19f9833a62635", hashlib.sha256(SERVICE_SCENARIO_PATH.read_bytes()).hexdigest())
		observations = service["runtime"]["observations"]["named_action_observations"]
		transitioned = {address for item in observations for address in item["transitioned_solenoid_addresses"]}
		self.assertEqual({1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 45, 46, 47, 48, 51, 52, 53, 54}, transitioned)
		left_gate = next(item for item in observations if "output 5" in item["label"])
		self.assertEqual("no_matching_transition", left_gate["result"])
		self.assertEqual([], left_gate["transitioned_solenoid_addresses"])
		self.assertTrue({29, 30, 32}.issubset(service["runtime"]["observations"]["solenoid_addresses_seen"]))
		self.assertTrue(all(item["result"] == "observed" for item in observations if item is not left_gate))
		self.assertTrue(all(item["observed_switch_addresses"] == [] for item in observations))

	def test_mechanisms_are_complete_and_use_retained_runtime_provenance(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(16, len(mechanisms))
		self.assertTrue(all(item["provenance"]["status"] == "validated" for item in mechanisms.values()))
		self.assertNotIn("service-diagnostic.rfm.solenoid-test", mechanisms["mechanism.ball-catcher"]["provenance"]["source_refs"])
		self.assertTrue(all("manual.rfm.operations-1999" in item["provenance"]["source_refs"] for item in mechanisms.values()))
		for identifier in ("mechanism.ball-trough", "mechanism.auto-plunger"):
			self.assertIn("runtime.rfm.stock-ball-serve", mechanisms[identifier]["provenance"]["source_refs"])
			self.assertIn("runtime.rfm.debug-ball-cycle", mechanisms[identifier]["provenance"]["source_refs"])
		self.assertIn("service-bulletin.rfm.mypinballs-code-updates", mechanisms["mechanism.right-lockup"]["provenance"]["source_refs"])
		trough_positions = [position for position in mechanisms["mechanism.ball-trough"]["positions"] if position["id"].startswith("position.trough-ball-")]
		self.assertEqual(["Ball 1", "Ball 2", "Ball 3", "Ball 4"], [position["label"] for position in trough_positions])
		self.assertEqual(4, len({position["description"] for position in trough_positions}))
		for index, position in enumerate(trough_positions, start=1):
			self.assertIn(f"Ball {index}", position["description"])
		self.assertEqual(["Down", "Up"], [position["label"] for position in mechanisms["mechanism.jet-exit-post"]["positions"]])
		self.assertIn("raising the post", mechanisms["mechanism.jet-exit-post"]["behavior"])
		self.assertEqual(["Closed", "Open"], [position["label"] for position in mechanisms["mechanism.lock-diverter"]["positions"]])
		self.assertIn("human-review.rfm.pinside-lock-diverter", mechanisms["mechanism.lock-diverter"]["provenance"]["source_refs"])
		self.assertIn("power winding that pulls", mechanisms["mechanism.lock-diverter"]["behavior"])
		self.assertEqual(["Down", "Up"], [position["label"] for position in mechanisms["mechanism.left-martian"]["positions"]])
		self.assertEqual(["Down", "Up"], [position["label"] for position in mechanisms["mechanism.right-martian"]["positions"]])
		self.assertEqual(["Closed", "Open"], [position["label"] for position in mechanisms["mechanism.left-gate"]["positions"]])
		self.assertIn("without an output-5 callback", mechanisms["mechanism.left-gate"]["behavior"])
		self.assertIn("production serve/launch trace records public output 5", mechanisms["mechanism.left-gate"]["behavior"])
		self.assertEqual(["Ready", "Deflected"], [position["label"] for position in mechanisms["mechanism.ball-catcher"]["positions"]])
		self.assertEqual(["switch.75.center-deflector-panel"], mechanisms["mechanism.ball-catcher"]["sensors"])
		self.assertTrue({"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.flippers"} <= mechanisms.keys())

	def test_only_resolved_manual_lamp_disagreement_is_retained(self) -> None:
		self.assertEqual(1, len(self.definition["conflicts"]))
		conflict = self.definition["conflicts"][0]
		self.assertEqual("ignored", conflict["status"])
		self.assertIn("18B", conflict["description"])
		self.assertIn("28B", conflict["description"])


if __name__ == "__main__":
	unittest.main()
