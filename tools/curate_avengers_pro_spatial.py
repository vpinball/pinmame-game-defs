"""Promote the reviewed Stern Avengers Pro spatial definition."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text

from curate_avengers import CORE_SOURCE, PRO_KNOWLEDGE, PRO_MANUAL, PRO_RUNTIME, PRO_SCRIPT, build


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/avengers-pro-2012.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/avengers-pro-2012.json"

TABLE_SOURCE = "vpx-table.avengers-pro-archive-45de3964"
TABLE_SHA256 = "45de396493ddf562f06baa6950a5b3b46d7803f4aca1ed1df4ad7f45a6a4c5df"
TABLE_SOURCE_RECORD = {
	"attribution": "The Visual Pinball table archive and credited table authors",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"license": "NOASSERTION",
	"locator": "Avengers (Pro), The (Stern 2012).vpx; ROM avs_170; SHA-256 prefix 45de3964; 81,530,880 bytes; exact playfield bounds 0,0 through 952,2115; read-only extraction/candidate audit in pinmame-review-artifacts/stern.avengers-le/extracted/03-archive-pro and spatial-candidates-03-archive-pro.json",
	"original_filename": "Avengers (Pro), The (Stern 2012).vpx",
	"sha256": TABLE_SHA256,
	"uri": "local-evidence://vpx-table/stern.avengers-pro-archive-45de3964",
}

DIRECT_SOURCES = (TABLE_SOURCE, PRO_SCRIPT, PRO_MANUAL)
MANUAL_MAP_SOURCES = (PRO_MANUAL,)


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], source_refs: tuple[str, ...] = DIRECT_SOURCES) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{device['id']}.{role}{suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


# Coordinates are normalized from the exact plain Pro table's 952 by 2115 frame.
# Values are deliberately limited to exact object centers or disclosed assembly
# centroids; no WIP HD/MOD geometry is used.
INPUT_POSITIONS = {
	1: [(0.116714, 0.546546)], 2: [(0.116091, 0.519088)], 3: [(0.116713, 0.492330)], 4: [(0.117025, 0.464311)],
	7: [(0.128486, 0.296465)], 10: [(0.676899, 0.117660)], 11: [(0.763355, 0.117130)], 12: [(0.848961, 0.115468)],
	13: [(0.660726, 0.344705)], 14: [(0.604986, 0.322862)], 23: [(0.935335, 0.896396)],
	24: [(0.041434, 0.755829)], 25: [(0.119696, 0.737086)], 26: [(0.223175, 0.714054)], 27: [(0.682767, 0.718596)],
	28: [(0.771346, 0.738034)], 29: [(0.866926, 0.754344)], 30: [(0.678933, 0.213986)], 31: [(0.880455, 0.192900)],
	32: [(0.803850, 0.297933)], 33: [(0.152541, 0.086437)], 34: [(0.919318, 0.412595)], 35: [(0.846309, 0.523974)],
	36: [(0.847184, 0.559789)], 43: [(0.136371, 0.215574)], 44: [(0.728195, 0.369950)], 47: [(0.097262, 0.058970)],
	48: [(0.937937, 0.163419)], 49: [(0.866642, 0.610764)], 50: [(0.867122, 0.583493)], 51: [(0.867791, 0.556033)],
	52: [(0.299893, 0.259946)], 53: [(0.358681, 0.269686)], 54: [(0.417263, 0.279490)], 55: [(0.477604, 0.289743)],
	57: [(0.334825, 0.193855)], 61: [(0.942910, 0.110962)], 62: [(0.267477, 0.279984)], 63: [(0.217594, 0.106101)],
	81: [(0.623146, 0.846135)], 83: [(0.284495, 0.844890)],
}

TROUGH_SENSOR_POSITIONS = {
	# The exact table supplies only the BallRelease and Drain endpoints. The
	# four physical switches are disclosed projections along that trough path,
	# in the script's 18 -> 21 physical order; switch 22 is downstream on the
	# short release-to-shooter corridor.
	18: [(0.532206, 0.948554)], 19: [(0.641676, 0.922299)], 20: [(0.751147, 0.896045)],
	21: [(0.860617, 0.869790)], 22: [(0.898000, 0.883000)],
}

ASSEMBLY_SENSOR_POSITIONS = {
	41: [(0.393908, 0.220213)], 42: [(0.393908, 0.220213)],
	45: [(0.536243, 0.379225)], 46: [(0.536243, 0.379225)],
}

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start", 65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right",
	68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 82: "cabinet.flipper.right-button", 84: "cabinet.flipper.left-button",
}

# Matrix-lamp centers are exact Light.lN or Primitive.LN object centers from the
# archive extraction. Lamps 71/73/75 use their dedicated on-playfield bulb-cover
# primitives; the unrelated S118a Q18 helper and off-playfield Flasher71/73/75
# glow planes are deliberately excluded.
LAMP_POSITIONS = {
	3: (0.448982, 0.869953), 4: (0.041343, 0.718277), 5: (0.102902, 0.684418), 6: (0.787327, 0.688207), 7: (0.862619, 0.722056),
	8: (0.459021, 0.672538), 9: (0.523214, 0.694577), 10: (0.536752, 0.733216), 11: (0.449334, 0.757750), 12: (0.378431, 0.734661),
	13: (0.362616, 0.694787), 14: (0.187010, 0.548254), 15: (0.187212, 0.520438), 16: (0.185925, 0.493213), 17: (0.181550, 0.466554),
	18: (0.158719, 0.423933), 19: (0.140941, 0.393540), 20: (0.115172, 0.358659), 21: (0.097649, 0.329581), 22: (0.068840, 0.269989),
	23: (0.146981, 0.318566), 24: (0.260823, 0.417813), 25: (0.244782, 0.386170), 26: (0.226309, 0.354972), 27: (0.203975, 0.324292),
	28: (0.181066, 0.280911), 29: (0.256124, 0.179963), 30: (0.242459, 0.144390), 31: (0.599872, 0.575723), 32: (0.615315, 0.549568),
	33: (0.631677, 0.522870), 34: (0.646394, 0.496295), 35: (0.668395, 0.463435), 36: (0.694420, 0.421050), 37: (0.793707, 0.559691),
	38: (0.793970, 0.522811), 39: (0.330451, 0.337752), 41: (0.436612, 0.404443), 42: (0.466854, 0.419810), 43: (0.506465, 0.430349),
	44: (0.552037, 0.431525), 45: (0.593635, 0.426097), 46: (0.624849, 0.411064), 47: (0.513765, 0.318160), 48: (0.351206, 0.291225),
	49: (0.408212, 0.300670), 50: (0.461527, 0.309884), 51: (0.594237, 0.343509), 52: (0.623753, 0.360062), 53: (0.913885, 0.283463),
	54: (0.887157, 0.316193), 55: (0.866374, 0.346498), 57: (0.817829, 0.405617), 58: (0.877640, 0.432393), 60: (0.670839, 0.215243),
	61: (0.861731, 0.191085), 62: (0.791645, 0.295190), 63: (0.642495, 0.060272), 65: (0.769506, 0.084596), 66: (0.847011, 0.084439),
	67: (0.763950, 0.056133), 68: (0.845619, 0.062308), 69: (0.373011, 0.378637), 70: (0.689373, 0.083878),
	71: (0.157235, 0.068047), 73: (0.156911, 0.068193), 75: (0.163438, 0.067535), 78: (0.842577, 0.377052),
}

OUTPUT_POSITIONS = {
	2: [(0.934212, 0.970157)], 3: [(0.401261, 0.172400)], 4: [(0.401261, 0.172400)], 5: [(0.267477, 0.279984)],
	6: [(0.388360, 0.274716)], 7: [(0.613044, 0.063949)], 9: [(0.678933, 0.213986)], 10: [(0.880455, 0.192900)],
	11: [(0.803850, 0.297933)], 13: [(0.223175, 0.714054)], 14: [(0.682767, 0.718596)],
	15: [(0.284495, 0.844890)], 16: [(0.623146, 0.846135)], 17: [(0.400735, 0.114775)],
	20: [(0.707750, 0.735671), (0.197012, 0.728527)],
	22: [(0.866642, 0.610764)], 23: [(0.393908, 0.220213)], 25: [(0.790702, 0.232974)],
	26: [(0.536243, 0.379225)],
}

# The official Pro coil-test map is a physical-location schematic rather than
# an exact XY drawing. These are its stated approximate Y anchors: Q18=.43,
# Q12=.47, and Q19=.49. The exact plain-Pro VPX objects instead land at
# y=.182622 (S118p), .264379 (RampControlGate), and .355755 (S119a/b). That
# three-item vertical disagreement is localized: nearby Q17/Q21/Q23/Q26 and
# the surrounding physical map reconcile. The manual map therefore controls
# these placements; no unrecorded interpolation is used.
MANUAL_COIL_MAP_POSITIONS = {
	12: [(0.057307, 0.47)],
	18: [(0.043766, 0.43)],
	19: [(0.954245, 0.49)],
	21: [(0.374000, 0.252000)],
}

TROUGH_COIL_POSITION = [(0.860617, 0.869790)]

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker", ("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start", ("pinmame.output.lamp", 2): "cabinet.tournament-start",
}


def apply_spatial(definition: dict[str, object]) -> None:
	if any("spatial" in device for device in [*definition["inputs"], *definition["outputs"]]):
		raise ValueError("Avengers Pro spatial promotion requires a fresh build(False) definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PRO_MANUAL)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL, PRO_SCRIPT)
		elif address in TROUGH_SENSOR_POSITIONS:
			_located(device, "sensor", TROUGH_SENSOR_POSITIONS[address])
			if address in {18, 19, 20, 21}:
				_append_note(device, "The manual switch map page 12 groups switches 18-22 at the trough. The exact table provides Kicker.Drain at (0.532206,0.948554), Kicker.BallRelease at (0.860617,0.869790), and Primitive.Apron as the apron boundary, but no individual trough contact objects; this is a disclosed assembly projection along the physical 18-to-21 path, not an exact switch-leaf center. The working script fixes the physical order through bsTrough.InitSw 0,21,20,19,18 and initializes four balls on 18-21.")
			else:
				_append_note(device, "The manual switch map page 12 leads switches 18-22 into the trough assembly, while the exact table provides Kicker.BallRelease, Kicker.Drain, and Primitive.Apron rather than a modeled jam contact. This is a disclosed downstream jam-sensor projection on the release-to-shooter corridor, not an exact switch-leaf center; the four-ball stack semantics remain the working script's 18-21 order.")
		elif address in ASSEMBLY_SENSOR_POSITIONS:
			_located(device, "sensor", ASSEMBLY_SENSOR_POSITIONS[address])
			if address in {41, 42}:
				_append_note(device, "The manual switch map page 12 places switches 41/42 on the Hulk assembly and the working script uses them as opposed wheel optos. The exact HulkMag/Hulk body assembly anchor is used as a disclosed projection for the hidden opto pair; it is not an internal opto-leaf coordinate.")
			else:
				_append_note(device, "The manual switch map page 12 places switches 45/46 on the Tesseract assembly and the working script uses them as opposed wheel optos. The exact Primitive.TessBase/cube assembly center is used as a disclosed projection for the hidden opto pair; it is not an internal opto-leaf coordinate.")
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address])
			if address in {30, 31}:
				_append_note(device, "The official Pro switch map fixes switch 30 at the left pop and switch 31 at the right pop. The exact table's left Bumper1 at x=.678933 is scripted as sw31 and its right Bumper2 at x=.880455 as sw30; this VPX controller-name/address anomaly is documented but not propagated into physical placement. The PinMAME address is unchanged.")
			elif address in {26, 27}:
				_append_note(device, "The exact slingshot-wall polygon centroid is used as the physical switch assembly projection; the manual and script control the left/right address semantics.")
			elif address in {81, 83}:
				_append_note(device, "The EOS contact is implicit in the exact lower-flipper assembly; the flipper center is the disclosed assembly anchor, not a claim about the hidden contact leaf.")
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		else:
			raise ValueError(f"Avengers Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", PRO_SCRIPT, PRO_RUNTIME)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL, PRO_SCRIPT)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL, PRO_SCRIPT)
		elif group == "pinmame.output.solenoid" and address == 1:
			_located(device, "effect", TROUGH_COIL_POSITION)
			device.setdefault("physical", {})["quantity"] = 1
			_append_note(device, "The official Pro coil map page 15 places Q1 in the ball trough. The exact Kicker.BallRelease anchor at (0.860617,0.869790), bounded by Kicker.Drain and the Primitive.Apron assembly, is used as a disclosed under-apron trough-kicker projection; it is not a claim about the hidden coil center.")
		elif group == "pinmame.output.solenoid" and address in MANUAL_COIL_MAP_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			_located(device, role, MANUAL_COIL_MAP_POSITIONS[address], MANUAL_MAP_SOURCES)
			device.setdefault("physical", {})["quantity"] = len(MANUAL_COIL_MAP_POSITIONS[address])
			if address == 12:
				_append_note(device, "The official Pro coil-test map locates Q12 (left ramp control gate) at y≈.47. The exact archive's named RampControlGate wall is at y=.264379, a vertically displaced VPX model of this physical assembly; the manual map controls this physical placement.")
			elif address == 18:
				_append_note(device, "The official Pro coil-test map locates Q18 (left-side #89 flasher) at y≈.43. The exact archive maps Q18 to S118p/S118a at y=.182622; that isolated vertical VPX placement is rejected in favor of the manual physical map. S118a remains a render helper, not a second bulb.")
			elif address == 19:
				_append_note(device, "The official Pro coil-test map locates Q19 (right-side #89 flasher) at y≈.49. The exact archive maps Q19 to S119a/S119b at y=.355755; that isolated vertical VPX placement is rejected in favor of the manual physical map. S119a/S119b remain collapsed to one physical bulb.")
			elif address == 21:
				_append_note(device, "The official Pro coil-location map page 15 places Q21 on the Hulk assembly at about (0.374,0.252), between Q17/Q3-Q4 and Q23/Q6. The exact VPX S121/S121a glow-helper centroid (0.663449,0.238199) is a conflicting rendered proxy and is deliberately not used for this physical placement; provenance is manual-map only.")
		elif group == "pinmame.output.solenoid" and address in OUTPUT_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			_located(device, role, OUTPUT_POSITIONS[address])
			device.setdefault("physical", {})["quantity"] = len(OUTPUT_POSITIONS[address])
			if address in {3, 4}:
				_append_note(device, "Outputs 3 and 4 are opposite-direction motor callbacks for the one visible Hulk rotation assembly and intentionally share one anchor.")
			elif address == 6:
				_append_note(device, "The reset coil acts on the complete four-target HULK bank; the target-center centroid is an assembly projection, not a claim that the hidden coil sits on the playfield surface.")
			elif address == 20:
				_append_note(device, "The manual explicitly marks Q20 SLINGSHOT (X2). The exact archive's S120p1/S120p2 dome centers are retained as the two physical #906 flashers; S120a-d are illumination helpers.")
			elif address == 21:
				_append_note(device, "The manual proves one Hulk #906 flasher. The exact archive maps Q21 to S121/S121a, two broad illumination helpers for that one spotlight; their disclosed centroid is retained as the physical assembly projection rather than counting two bulbs.")
			elif address == 22:
				_append_note(device, "The manual and script prove the Loki retaining-post actuator. Its point is the exact Loki opto-stack assembly anchor; the hidden post coil is not assigned a fabricated internal coordinate.")
			elif address == 25:
				_append_note(device, "The manual proves one pop-bumper #89 flasher at Q25. The exact archive maps SetLamp 125 to the single S125 emitter; the three nearby bumper centers are not additional lamps.")
			elif address in {9, 10}:
				_append_note(device, "The official Pro coil map fixes Q9 at the left pop and Q10 at the right pop. The archive Bumper1/Bumper2 centers provide the matching geometry, but its working script reverses their switch callbacks (Bumper1→sw31 and Bumper2→sw30); this controller-name/address anomaly does not change Q9/Q10 physical placement.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", [LAMP_POSITIONS[address]])
			device.setdefault("physical", {})["quantity"] = 1
			if address in {71, 73, 75}:
				_append_note(device, f"The manual groups lamps 71, 73, and 75 in one left-side location callout. This socket retains the exact table's dedicated on-playfield L{address} bulb-cover primitive; the unrelated S118a Q18 helper and off-playfield Flasher{address} glow plane are excluded.")
		elif group == "pinmame.output.solenoid" and 27 <= address <= 32:
			device.setdefault("roles", ["cabinet.rear-panel"])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL, PRO_SCRIPT)
			_append_note(device, "The official Pro coil chart identifies this as a backpanel flasher. It is outside playfield space and therefore has no XY placement.")
		elif group == "pinmame.output.gi" and address == 0:
			gi_positions = [
				(0.755797, 0.803354), (0.215181, 0.823107), (0.690015, 0.823290), (0.148133, 0.801950),
				(0.685224, 0.749593), (0.228330, 0.747632), (0.198452, 0.698599), (0.717593, 0.698319),
				(0.862974, 0.604426), (0.113796, 0.599196), (0.931032, 0.488616), (0.055145, 0.558351),
				(0.051825, 0.489114), (0.050719, 0.425854), (0.045186, 0.356617), (0.789938, 0.342670),
				(0.704729, 0.267954), (0.953717, 0.361100), (0.813177, 0.022387), (0.952610, 0.031353),
				(0.273148, 0.087141), (0.513284, 0.098598), (0.050719, 0.022885),
				(0.628484, 0.123762), (0.715354, 0.123264), (0.804989, 0.124509), (0.891859, 0.123762),
			]
			_located(device, "emitter", gi_positions)
			device.setdefault("physical", {})["quantity"] = len(gi_positions)
			_append_note(device, "The exact table's 50 GI render helpers collapse to 27 reviewed playfield anchors: 23 paired GI bulbs plus four lane-guide bulbs. Rear-panel/service lighting is not assigned fake playfield coordinates; all physical GI sockets still share PinMAME GI address 0.")
		else:
			raise ValueError(f"Avengers Pro output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Avengers Pro knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PRO_KNOWLEDGE,
	"Coverage: **author-ready - complete Pro I/O, wiring, mechanisms, initial state, and controller bindings validated**",
	"Coverage: **author-ready - complete Pro I/O, wiring, mechanisms, initial state, controller bindings, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nAll located records use the exact plain Pro table's 952 by 2115 player-view frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the apron. The working Pro script establishes causality and semantic addresses; the official Pro manual establishes physical inventory and multiplicity; the exact table is used only for reconciled geometry. Cabinet, service, backpanel, virtual, unused, DIP, trough/interior optos, and other off-playfield records are explicit N/A dispositions with no fabricated XY. Paired GI render layers and unrelated VPX bloom/render helpers are collapsed or excluded; lock lamps 71/73/75 retain the three dedicated on-playfield L71/L73/L75 bulb-cover primitive centers rather than the unrelated Q18 S118a helper or off-playfield glow planes.\n\nThe official maps override two explicitly recorded VPX anomalies. First, the physical switch/coil maps put 30/Q9 left, 31/Q10 right, and 32/Q11 bottom; the exact table's Bumper1 at x=.678933 is scripted to sw31 and Bumper2 at x=.880455 to sw30. The controller bindings stay as scripted, but the physical XY assignments follow the manual. Second, the official coil-test map puts Q18 left flasher at y≈.43, Q12 left ramp gate at y≈.47, and Q19 right flasher at y≈.49. The archive's named S118p/S118a, RampControlGate, and S119a/S119b objects instead land at y=.182622/.264379/.355755. Adjacent mapped assemblies reconcile, so these three isolated vertical VPX placements are rejected; the manual-map approximate anchors are retained without inventing sub-map precision.\n\nThe Pro topology remains four trough balls on 18-21 plus jam 22, matrix shooter 23, center HULK reset 6, ramp gate 12, Hulk arms 17, Loki 22, magnet 23, and right orbit 61. No LE bridge, auxiliary board, six-ball trough, or LE-only mechanism is introduced.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `manual.avengers-pro`: official Stern `Avengers-Pro-Manual.pdf`, SHA-256 `fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031`; switch chart PDF page 13, coil chart page 16, lamp chart page 19, location maps, and model-specific assembly drawings.",
	"- `manual.avengers-pro`: official Stern `Avengers-Pro-Manual.pdf`, SHA-256 `fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031`; switch chart PDF page 13, coil chart page 16, lamp chart page 19, location maps, and model-specific assembly drawings.\n- `vpx-table.avengers-pro-archive-45de3964`: exact plain Pro table `Avengers (Pro), The (Stern 2012).vpx` for ROM `avs_170`, SHA-256 `45de396493ddf562f06baa6950a5b3b46d7803f4aca1ed1df4ad7f45a6a4c5df`; bounds 0,0 through 952,2115; read-only extraction and candidate report `03-archive-pro`.",
)
SPATIAL_KNOWLEDGE = SPATIAL_KNOWLEDGE.replace(
	"Cabinet, service, backpanel, virtual, unused, DIP, trough/interior optos, and other off-playfield records",
	"Cabinet, service, backpanel, virtual, unused, DIP, and other off-playfield records",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"The Pro topology remains four trough balls on 18-21 plus jam 22, matrix shooter 23, center HULK reset 6, ramp gate 12, Hulk arms 17, Loki 22, magnet 23, and right orbit 61. No LE bridge, auxiliary board, six-ball trough, or LE-only mechanism is introduced.\n\n## Sources\n",
	"The Pro topology remains four trough balls on 18-21 plus jam 22, matrix shooter 23, center HULK reset 6, ramp gate 12, Hulk arms 17, Loki 22, magnet 23, and right orbit 61. No LE bridge, auxiliary board, six-ball trough, or LE-only mechanism is introduced.\n\nQ21 is a manual-map assembly projection at about (0.374,0.252) on Hulk, between the Q17/Q3-Q4 and Q23/Q6 callouts on manual page 15. The VPX S121/S121a centroid at (0.663449,0.238199) is a conflicting render proxy, so it is rejected rather than silently retained; Q21's placement provenance is manual-only.\n\nThe four trough sensors and jam sensor are disclosed assembly projections. The exact table's Kicker.Drain and Kicker.BallRelease provide the trough endpoints, Primitive.Apron identifies the apron boundary, and the working script supplies the 18-to-21 physical order and four-ball inventory. Q1 uses the BallRelease assembly anchor. Switches 41/42 use the Hulk assembly anchor and 45/46 use the Tesseract base anchor; these points describe assemblies, not hidden contact leaves.\n\n## Sources\n",
)


def promote() -> None:
	definition = build(False)
	definition["sources"].append(TABLE_SOURCE_RECORD)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/avengers-pro-2012.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
