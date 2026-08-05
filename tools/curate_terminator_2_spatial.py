"""Apply the reviewed VPW geometry to the semantic Terminator 2 definition."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json, write_text
from pinmame_game_defs.registry import rebuild_catalog

import curate_terminator_2 as semantic


ROOT = semantic.ROOT
DEFINITION_PATH = ROOT / "machines/partial/williams/terminator-2-judgment-day-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/terminator-2-judgment-day-1991.md"
AUDIT_PATH = ROOT / "reports/spatial/williams/terminator-2-judgment-day-1991.json"
X_MAX = 964.0
Y_MAX = 2162.0


def point(x: float, y: float) -> tuple[float, float]:
	return round(x / X_MAX, 6), round(y / Y_MAX, 6)


def placement(device: dict[str, Any], object_name: str, xy: tuple[float, float], role: str, sources: tuple[str, ...] = (semantic.VPX_TABLE_SOURCE,)) -> dict[str, Any]:
	return {"id": f"{device['id']}.{role}.{semantic.slug(object_name)}", "role": role, "space": "playfield", "x": xy[0], "y": xy[1], "provenance": semantic.provenance(*sources)}


def located(device: dict[str, Any], objects: list[tuple[str, tuple[float, float]]], role: str, status: str = "validated", sources: tuple[str, ...] = (semantic.VPX_TABLE_SOURCE,)) -> None:
	device["spatial"] = {"status": status, "placements": [placement(device, name, xy, role, sources) for name, xy in objects]}


def not_applicable(device: dict[str, Any], reason: str, *sources: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": semantic.provenance(*sources)}


def add_note(device: dict[str, Any], text: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = f"{physical['notes']} {text}" if physical.get("notes") else text


INPUT_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	11: [("TriggerRF", point(607.21906, 1845.6969))], 12: [("TriggerLF", point(253.6183, 1846.6035))],
	15: [("Drain-to-BallRelease trough projection 1", point(592.37544, 1994.622))], 16: [("Drain-to-BallRelease trough projection 2", point(671.94506, 1960.7174))],
	17: [("Drain-to-BallRelease trough projection 3", point(751.51468, 1926.8128))], 18: [("Drain", point(433.2362, 2062.4312))],
	25: [("Trigger.sw25", point(50.719437, 1729.4485))],
	26: [("Trigger.sw26", point(118.22889, 1613.9412))], 27: [("Trigger.sw27", point(748.96356, 1613.7274))], 28: [("Trigger.sw28", point(815.3944, 1665.8789))],
	31: [("Kicker.sw31", point(865.5187, 919.1969))], 32: [("Primitive.T2_Gun assembly", point(865.51874, 1029.3837))], 33: [("Primitive.T2_Gun assembly", point(865.51874, 1029.3837))],
	36: [("HitTarget.sw36", point(425.02313, 660.554))], 37: [("HitTarget.sw37", point(467.14813, 700.679))], 38: [("HitTarget.sw38", point(511.39816, 738.179))],
	41: [("Bumper.Bumper1", point(464.7151, 398.11743))], 42: [("Bumper.Bumper2", point(539.35254, 587.8717))], 43: [("Bumper.Bumper3", point(690.91473, 451.42084))],
	44: [("Wall.LeftSlingshot drag-point centroid", point(198.959384, 1596.17412))], 45: [("Wall.RightSlingshot drag-point centroid", point(666.839608, 1590.44232))],
	46: [("HitTarget.sw46", point(763.21747, 1245.4951))], 47: [("HitTarget.sw47", point(763.09247, 1296.8701))], 48: [("HitTarget.sw48", point(763.09247, 1347.8701))],
	51: [("Kicker.sw51", point(52.74919, 961.93243))], 53: [("Trigger.sw53", point(55.627926, 315.2049))], 54: [("Trigger.sw54", point(70.66557, 150.56776))], 55: [("Kicker.sw55", point(741.06757, 70.96199))],
	56: [("Trigger.sw56", point(468.81967, 203.57411))], 57: [("Trigger.sw57", point(568.8115, 225.40366))], 58: [("Trigger.sw58", point(671.2108, 246.00197))],
	61: [("Gate.sw61", point(197.30371, 513.38696))], 62: [("Trigger.sw62", point(40.26606, 193.32352))], 63: [("Gate.sw63", point(756.97565, 627.8825))],
	64: [("Trigger.sw64", point(618.4057, 481.23264))], 65: [("Trigger.sw65", point(880.5173, 279.71756))], 66: [("Trigger.sw66", point(799.59924, 195.73581))],
	71: [("HitTarget.sw71", point(173.69376, 694.7722))], 72: [("HitTarget.sw72", point(183.5637, 747.14056))], 73: [("HitTarget.sw73", point(192.89772, 799.7795))], 74: [("HitTarget.sw74", point(202.12245, 852.956))], 75: [("HitTarget.sw75", point(211.54387, 907.3085))],
	76: [("Kicker.sw76", point(276.99594, 211.89403))], 77: [("HitTarget.sw77", point(290.89508, 298.64487))], 78: [("Kicker.sw78", point(904.33246, 1945.6531))],
}

EFFECT_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	1: [("Kicker.sw76", point(276.99594, 211.89403))], 2: [("Kicker.sw31", point(865.5187, 919.1969))], 3: [("Drain", point(433.2362, 2062.4312))], 4: [("Kicker.BallRelease", point(831.0843, 1892.9082))],
	5: [("Wall.RightSlingshot drag-point centroid", point(666.839608, 1590.44232))], 6: [("Wall.LeftSlingshot drag-point centroid", point(198.959384, 1596.17412))],
	8: [("Trigger.sw25 kickback assembly", point(50.719437, 1729.4485))], 9: [("Plunger1", point(50.694122, 1926.4977))], 10: [("Kicker.sw55", point(741.06757, 70.96199))],
	11: [("Primitive.T2_Gun", point(865.51874, 1029.3837))], 13: [("Bumper.Bumper1", point(464.7151, 398.11743))], 14: [("Bumper.Bumper2", point(539.35254, 587.8717))],
	15: [("Bumper.Bumper3", point(690.91473, 451.42084))], 16: [("Kicker.sw51", point(52.74919, 961.93243))], 28: [("HitTarget.sw77", point(290.89508, 298.64487))],
	46: [("TriggerRF", point(607.21906, 1845.6969))], 48: [("TriggerLF", point(253.6183, 1846.6035))],
}

LAMP_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	11: [("L11", point(287.39496, 1643.4208))], 12: [("L12", point(358.5831, 1606.2587))], 13: [("L13", point(430.1694, 1588.9508))], 14: [("L14", point(505.71988, 1606.4674))], 15: [("L15", point(570.69257, 1644.9978))], 16: [("L16", point(429.96292, 1918.5978))], 17: [("L17", point(436.8856, 1484.8107))],
	21: [("L21", point(50.183113, 1647.6917))], 22: [("L22a", point(50.288, 1536.8124)), ("L22b", point(816.0358, 1537.0868))], 23: [("L23", point(118.31302, 1467.4066))], 24: [("L24", point(749.2248, 1467.3746))], 25: [("L25", point(374.6901, 809.52014))], 26: [("L26", point(355.82285, 705.24164))], 27: [("L27", point(339.6643, 601.6882))], 28: [("L28", point(322.85495, 496.36966))],
	31: [("L31", point(254.28519, 734.0496))], 32: [("L32", point(263.2487, 783.1297))], 33: [("L33", point(277.42532, 831.569))], 34: [("L34", point(290.36966, 875.9949))], 35: [("L35", point(303.47177, 923.73987))], 36: [("L36", point(426.90973, 776.25714))], 37: [("L37", point(469.18896, 811.4169))], 38: [("L38", point(510.19342, 852.4468))],
	41: [("L41", point(150.76582, 939.15454))], 42: [("L42", point(177.86926, 1050.7529))], 43: [("L43", point(216.63107, 1137.259))], 44: [("L44", point(238.982, 1210.2062))], 45: [("L45", point(257.1247, 1280.9836))], 46: [("L46", point(280.75662, 1355.6615))], 47: [("L47", point(296.22644, 1435.5078))], 48: [("L48", point(315.97357, 1512.3365))],
	51: [("L51a", point(400.10486, 1401.8247)), ("L51b", point(467.63043, 1401.209))], 52: [("Primitive.L52 skull assembly projection", point(290.89508, 298.64487))],
	53: [("L53", point(679.52106, 1136.9258))], 54: [("L54", point(652.94305, 1210.1489))], 55: [("L55", point(625.4195, 1282.5437))], 56: [("L56", point(598.9009, 1359.3146))], 57: [("L57", point(569.5661, 1434.337))], 58: [("L58", point(541.4647, 1508.2344))],
	61: [("L61", point(315.07635, 1016.63745))], 62: [("L62", point(330.0013, 1081.9806))], 63: [("L63", point(344.0438, 1146.8193))], 64: [("L64", point(358.65793, 1210.6841))], 65: [("L65", point(374.3634, 1274.9163))], 66: [("L66", point(112.11431, 1207.7814))], 67: [("L67", point(162.73505, 1318.2964))], 68: [("L68", point(226.74431, 642.4249))],
	71: [("L71", point(614.18414, 1018.8931))], 72: [("L72", point(592.16174, 1083.2053))], 73: [("L73", point(569.44775, 1146.943))], 74: [("L74", point(547.6057, 1211.571))], 75: [("L75", point(525.92194, 1276.051))], 76: [("L76", point(742.40247, 1241.3405))], 77: [("L77", point(741.8852, 1292.462))], 78: [("L78", point(743.76636, 1346.3873))],
	81: [("L81", point(750.78827, 956.7337))], 82: [("L82", point(637.8953, 940.2964))], 83: [("L83", point(719.845, 1051.8195))], 85: [("L85", point(305.93045, 398.8359))], 86: [("L86", point(469.6026, 108.398186))], 87: [("L87", point(569.9467, 130.69623))], 88: [("L88", point(673.7177, 152.81792))],
}

FLASHER_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	17: [("F117", point(392.1405, 1747.9479)), ("F1172", point(469.02628, 1748.8044))], 18: [("F118", point(729.04016, 1755.8896))], 19: [("F119", point(142.0577, 1754.0991))], 20: [("F120", point(47.956024, 862.4682))], 21: [("F121", point(865.69476, 936.60376)), ("F121b", point(870.1298, 1124.9872))], 22: [("F122", point(765.19946, 634.2644))], 23: [("F123", point(121.169914, 280.81564))], 25: [("F125", point(175.05278, 751.1035))], 26: [("F126", point(216.68967, 326.0185)), ("F126a", point(169.21431, 199.84035))], 27: [("F127", point(370.31763, 306.4764)), ("F127a", point(381.96442, 250.69917))],
}

GI2_OBJECTS = {
	"B1": (464.7151, 398.11743), "B2": (539.35254, 587.8717), "B3": (690.91473, 451.42084), "B4": (0, 0), "B5": (0, 0), "B6": (0, 0),
	"GI_1": (0, 0), "GI_2": (0, 0), "GI_3": (0, 0), "GI_4": (0, 0), "GI_5": (0, 0), "GI_6": (0, 0), "GI_7": (0, 0), "GI_8": (0, 0), "GI_9": (0, 0), "GI_10": (0, 0), "GI_11": (0, 0), "GI_12": (0, 0), "GI_13": (0, 0), "GI_14": (0, 0), "GI_15": (467.59897, 634.80756), "GI_16": (532.62964, 681.36774), "GI_17": (417.48743, 192.5585), "GI_18": (527.64984, 213.36194), "GI_19": (626.28754, 237.39903), "GI_20": (724.4383, 256.91516), "GI_001": (724.08636, 261.08545), "GI_002": (421.00003, 204.00002),
}
GI3_OBJECTS = {f"GI_{index}": xy for index, xy in {21: (380.64868, 348.83136), 22: (380.77527, 434.00882), 23: (255.7749, 464.9249), 24: (161.63599, 332.33954), 25: (122.198, 344.06424), 26: (847.0285, 51.368774), 27: (898.23193, 51.709064), 28: (911.20154, 107.4986), 29: (911.3922, 717.6473), 30: (912.45087, 802.47614), 31: (909.7719, 893.68713), 32: (909.37305, 1171.214), 33: (761.3623, 675.28876), 34: (721.5083, 654.1311), 35: (98.1416, 234.78833), 37: (726.0364, 1750.8704), 38: (139.12, 1754.6527)}.items()}

# The first three are exact bumper centers; the remaining coordinates are
# exact named GI emitter objects.  The zero placeholders are intentionally
# excluded from canonical placements and make omissions conspicuous in the
# audit rather than silently turning unknown geometry into (0,0).
GI2_OBJECTS = {name: point(*xy) for name, xy in GI2_OBJECTS.items() if xy != (0, 0)}
GI3_OBJECTS = {name: point(*xy) for name, xy in GI3_OBJECTS.items()}


def _by_binding(definition: dict[str, Any], collection: str, group: str) -> dict[int, dict[str, Any]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def apply_spatial(definition: dict[str, Any]) -> None:
	switches = _by_binding(definition, "inputs", "pinmame.input.switch")
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = device["binding"]["group"]
		address = device["binding"]["device"]
		if group == "pinmame.input.dip":
			not_applicable(device, "dip_switch", semantic.CONTROLLER_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", semantic.MANUAL_SOURCE)
		elif address in {1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 21, 22, 23, 111, 113}:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
		elif address in {112, 114}:
			not_applicable(device, "internal_nonvisual", semantic.CORE_SOURCE)
		elif address == 34:
			device["roles"] = ["cabinet.grip-trigger"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.VPX_SCRIPT_SOURCE)
			add_note(device, "The physical trigger is on the cabinet gun grip; the working VPX maps PlungerKey directly to Controller.Switch(34), so it must not receive a playfield coordinate.")
		elif address in INPUT_POSITIONS:
			if address in {15, 16, 17, 32, 33, 44, 45}:
				located(device, INPUT_POSITIONS[address], "sensor", "observed", (semantic.MANUAL_SOURCE, semantic.VPX_TABLE_SOURCE, semantic.VPX_SCRIPT_SOURCE))
			else:
				located(device, INPUT_POSITIONS[address], "sensor")
			if address in {15, 16, 17}:
				device["roles"] = [*(device.get("roles") or []), "internal.trough"]
				add_note(device, "The exact VPX exposes Drain and BallRelease but no separate trough-contact objects. This is an ordered 40/60/80-percent projection between those anchors, consistent with the manual left/center/right map, with practical uncertainty of about plus or minus 0.03 normalized in both axes; it is not copied from perspective artwork.")
			elif address in {32, 33}:
				add_note(device, "The contact is internal to the moving cannon mechanism. The exact T2_Gun center is a shared assembly projection confirmed by the manual mechanism map and the working cvpmMech windows, not an invented leaf-contact center.")
			elif address in {44, 45}:
				add_note(device, "The switch is implicit in the exact named slingshot collision wall. The extractor's drag-point centroid is the physical assembly projection, not an invented internal leaf-contact center.")
		else:
			add_note(device, "Spatial blocker: used controller address retained, but the exact corresponding VPX sensor object is not promoted from nearby graphical geometry.")
	# Constant switch 24 is handled after the generic branch so its policy
	# reason remains explicit even though it is not an unused address.
	not_applicable(switches[24], "constant", semantic.MANUAL_SOURCE)

	gi = _by_binding(definition, "outputs", "pinmame.output.gi")
	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = device["binding"]["group"]
		address = device["binding"]["device"]
		if device["kind"] == "virtual":
			not_applicable(device, "virtual", semantic.CORE_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", semantic.MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address == 84:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 7:
			device["roles"] = ["cabinet.knocker"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.VPX_SCRIPT_SOURCE)
			add_note(device, "The knocker is an internal cabinet sound device; the working table models only its callback sound, so it has no normalized playfield coordinate.")
		elif group == "pinmame.output.solenoid" and address == 24:
			device["roles"] = ["backbox.flasher"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
			add_note(device, "The manual locates this flasher in the backglass/backbox, outside normalized playfield space; the working script has no callback for it.")
		elif group == "pinmame.output.lamp" and address == 52:
			located(device, LAMP_POSITIONS[address], "emitter", "observed", (semantic.MANUAL_SOURCE, semantic.VPX_TABLE_SOURCE, semantic.VPX_SCRIPT_SOURCE))
			add_note(device, "The working script drives the exact Primitive.L52 skull-eye mesh. That primitive has an object-space origin at (0,0), so the exact adjacent skull drop-target center is retained as a disclosed assembly projection rather than treating (0,0) as a lamp position.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			located(device, LAMP_POSITIONS[address], "emitter")
		elif group == "pinmame.output.solenoid" and address in FLASHER_POSITIONS:
			located(device, FLASHER_POSITIONS[address], "emitter")
			add_note(device, "Named retained VPX Light.F objects are direct table geometry; closely coincident render-layer duplicates are not promoted unless they are distinct named emitter centers.")
		elif group == "pinmame.output.solenoid" and address in EFFECT_POSITIONS:
			located(device, EFFECT_POSITIONS[address], "effect", "observed", (semantic.MANUAL_SOURCE, semantic.VPX_TABLE_SOURCE, semantic.VPX_SCRIPT_SOURCE))
			if address in {5, 6}:
				add_note(device, "The exact named slingshot-wall centroid is the physical actuator assembly projection; the manual and controller semantics preserve the right/left coil identity.")
			elif address == 8:
				add_note(device, "The exact left-outlane switch 25 center is the shared kickback assembly projection established by the manual and working SolAPlunger callback; it is not a claim about the under-playfield coil's internal center.")
			elif address in {13, 14, 15}:
				add_note(device, "The exact named bumper center is the shared pop-bumper coil/effect anchor; the matching working hit event proves the switch address.")
		elif group == "pinmame.output.gi" and address == 2:
			objects = [(name, xy) for name, xy in [*GI2_OBJECTS.items(), *GI3_OBJECTS.items()]]
			located(device, objects, "emitter", "conflicted")
			add_note(device, "The placement list is the retained script's Case 2 GI2/GI3 emitter group. Its physical five-string identity conflicts with the manual GI table; this is intentionally conflicted evidence, not a resolved five-channel mapping.")
		else:
			add_note(device, "Spatial blocker: exact playfield emitter/effect geometry is not proven for this controller channel by the retained VPX objects.")
	# The manual's GI 4 is explicitly unused; keep it separate from the
	# script's decorative Light2-Light5 branch.
	not_applicable(gi[3], "unused", semantic.MANUAL_SOURCE)


def audit_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs = sorted(device["binding"]["device"] for device in definition["inputs"] if device.get("spatial", {}).get("status") in {"validated", "observed", "conflicted"})
	located_outputs = sorted((device["binding"]["group"], device["binding"]["device"]) for device in definition["outputs"] if device.get("spatial", {}).get("status") in {"validated", "observed", "conflicted"})
	unresolved_inputs = sorted(device["binding"]["device"] for device in definition["inputs"] if device["binding"]["group"] == "pinmame.input.switch" and device["availability"] != "unused" and "spatial" not in device)
	unresolved_solenoids = sorted(device["binding"]["device"] for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.solenoid" and device["availability"] != "unused" and device["kind"] != "virtual" and "spatial" not in device)
	unresolved_lamps = sorted(device["binding"]["device"] for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.lamp" and device["availability"] != "unused" and "spatial" not in device)
	unresolved_gi = sorted(device["binding"]["device"] for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.gi" and device["availability"] != "unused" and "spatial" not in device)
	unresolved: list[dict[str, Any]] = []
	if unresolved_inputs:
		unresolved.append({"kind": "spatial", "scope": "used switches without a reviewed playfield placement or controlled non-playfield disposition", "addresses": unresolved_inputs})
	if unresolved_solenoids:
		unresolved.append({"kind": "spatial", "scope": "solenoid/effect geometry", "addresses": unresolved_solenoids})
	if unresolved_lamps:
		unresolved.append({"kind": "spatial", "scope": "lamp geometry", "addresses": unresolved_lamps, "group": "pinmame.output.lamp"})
	if unresolved_gi:
		unresolved.append({"kind": "spatial", "scope": "GI string geometry/routing", "addresses": unresolved_gi, "group": "pinmame.output.gi"})
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": definition["machine"]["id"], "status": "partial",
		"coordinate_convention": {"space": "playfield", "x": "x/964; 0=left, 1=right", "y": "y/2162; 0=rear/backglass, 1=apron/player", "source_bounds": {"left": 0, "top": 0, "right": 964, "bottom": 2162}},
		"extraction": {"source_ref": semantic.VPX_EXTRACTION_SOURCE, "manifest_uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json", "manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.", "manifest_sha256": semantic.EXTRACTION_MANIFEST_SHA256, "file_count": semantic.EXTRACTION_FILE_COUNT, "total_bytes": semantic.EXTRACTION_TOTAL_BYTES, "fail_closed": True},
		"source_hashes": {"table_sha256": semantic.TABLE_SHA256, "embedded_script_sha256": semantic.SCRIPT_SHA256, "manual_sha256": semantic.MANUAL_SHA256, "rom_sha256": semantic.ROM_SHA256},
		"resolved_input_addresses": located_inputs, "resolved_output_bindings": [{"group": group, "address": address} for group, address in located_outputs],
		"candidate_geometry": {"input_objects": sorted({name for objects in INPUT_POSITIONS.values() for name, _ in objects}), "effect_objects": sorted({name for objects in EFFECT_POSITIONS.values() for name, _ in objects}), "lamp_objects": sorted({name for objects in LAMP_POSITIONS.values() for name, _ in objects}), "flasher_objects": sorted({name for objects in FLASHER_POSITIONS.values() for name, _ in objects}), "gi_case_2_objects": sorted([*GI2_OBJECTS, *GI3_OBJECTS]), "excluded_graphical_objects": ["Light2", "Light3", "Light4", "Light5", "T2_Gun laser overlays"]},
		"unresolved": unresolved,
		"blockers": [
			"The working VPX models the three trough contacts as controller state inside one cvpmBallStack and exposes no separate sensor centers; the retained ordered projection has about +/-0.03 normalized practical uncertainty rather than exact hidden-seat coordinates.",
			"Manual GI 1-5 naming conflicts with the retained script's GI2/GI3 arrays and Case 3 Light2-Light5 branch; output 2 retains a conflicted direct group placement, while the remaining physical string placements stay unresolved.",
			"Solenoid 12 is Knock Down / SM1-26-600 in the early manual table but Not Used in the later electrical table; the retained script has no SolCallback(12).",
			"Later lamp schematic connector labels differ from the lamp matrix table; no connector pinout is manufactured.",
		],
	}


KNOWLEDGE = """# Terminator 2: Judgment Day (Williams, 1991)

Coverage: **partial — complete semantic inventory and reviewed normalized coordinates are retained, but author-ready status is blocked by explicit spatial and source conflicts.** This is the physical Williams machine only. FreeWPC custom-ROM drivers and virtual/community rethemes are not claimed by the canonical definition.

## Evidence precedence and exact identity

The retained known-working VPW 0022 embedded script is the semantic controller authority. The Williams operations manual is the physical wiring, switch/coil/lamp, GI, and assembly authority. Pinned PinMAME revision `4ec52ff0ac13` controls public address routing, the WPC-DMD hardware generation (`0x4`), and the driver family. The retained table SHA-256 is `3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c`; its embedded script SHA-256 is `b5153ac46f6d4b58afb676c1f7bfdff17c6ffb953941daed8dd841c679f4e831`. The manual SHA-256 is `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`; the authorized external `t2_l8.zip` evidence SHA-256 is `4cdd95d435334c3bd6fe19556b410b558e67266b30e7fb767f52f4d14ed525b1`.

The canonical driver set is `t2_d2`, `t2_d3`, `t2_d4`, `t2_d6`, `t2_d8`, `t2_l2`, `t2_l2sp1`, `t2_l3`, `t2_l4`, `t2_l6`, `t2_l8`, `t2_l81`, `t2_l82`, `t2_l83`, `t2_l84`, `t2_p2f`, `t2_p2g`, `t2_f19`, `t2_f20`, and `t2_f32`. D-series ghost fixes, sound/attract/profanity revisions, and the L83/L84 physical-compatible MODs retain the same physical I/O. The FreeWPC records are alternative firmware for the stock physical T2 hardware; they remain controller variants of this machine and do not create a separate physical machine or community retheme entry.

## Controller inventory

All 64 printed switch-matrix positions `11` through `88` are present, including printed Not Used positions. Cabinet/service inputs `1`-`8`, optional generic flipper inputs `111`-`118`, and DIP inputs `1`-`8` are explicit. All printed lamp addresses `11`-`88` are present, including lamp `18` Not Used and the optional cabinet start-button lamp `84`. Solenoids `1`-`28`, the two lower-flipper aliases `46`/`48`, five GI address slots `0`-`4`, and the 128x32 DMD are explicit. Public lamp addresses remain WPC matrix addresses; do not replace them with sequential 1-64 values.

The retained script callbacks are: 1 `SolSkull` (physical Ball Popper, opening the skull path from switch 76), 2 gun fire/kicker, 3 outhole, 4 trough ball release, 7 knocker, 8 left outer-lane kickback saver, 9 auto plunger, 10 top lock, 11 gun motor, 16 left lock, and 28 drop-target reset. Flashers 17-27 use the script's `SetLamp 117` through `SetLamp 127` mappings except 24, which has no retained callback. The manual's physical output names remain authoritative even when the script callback name is thematic.

The manual solenoid table's exact wire/connector/transistor/part-number data is retained on every physical solenoid output. High-power outputs 1-8 use J130, low-power outputs 9-16 use J127, flashers use the J126/J125/J122 branches shown on manual page 48, and drop-target reset 28 is J122-4/Q20/AE-26-1200. The two lower flippers are output 46 `Blu-Yel/J109-7/FL-11630` and output 48 `Gry-Yel/J109-5/FL-11630`. GI strings retain the printed rows: GI1 `Wht-Brn/J120-7/Q18/#555`, GI2 `Wht-Vio/J119-1/Q10/#555`, GI3 `Wht-Yel/J121-9/Q14/#555`, GI4 `Wht-Orn/J120-8/Q16` with no printed lamp part, and GI5 `Wht-Grn/J120-10/Q12/#555`. Lamp-matrix connector labels are not copied into output wiring because the later schematic disagrees with the matrix table.

## Mechanisms and physical assemblies

The three-ball trough initializes `bsTrough.InitSw 18,17,16,15`, with switch 18 as the outhole/exit and switches 17, 16, and 15 as the three stack seats, and sets `Balls=3`; BallRelease kicks at 90 degrees with strength 8. The shooter lane is switch 78 with a 0-degree/50-strength kick and variance 3. The left lock is switch 51 at 160/13; the top lock is switch 55 at 270/5 with variance 6. The single drop target is switch 77 reset by solenoid 28.

The cannon is a `cvpmMech` one-solenoid, reverse, non-linear mechanism driven by solenoid 11, length 240, steps 240. Home switch 33 is the 0-5 window and mark switch 32 is the 98-105 window. The retained firing callback kicks switch 31 by `-CurrentPos` with strength 45 and clears the loaded ball; the visual callback uses `CurrentPos=aNewPos/3`. Recreating the cannon requires a motorized traverse and loaded-ball/fire state, not the modern comparison script's keyframed or magnet device. The VPW table's `T2_Gun` primitive is a shared assembly anchor for the internal mark/home contacts, not a substitute for the manual's A-14507/A-14504/A-13892-2 physical assemblies. Switch 34 is the trigger on the cabinet gun grip; the working script maps `PlungerKey` directly to that controller switch, so it intentionally has no playfield coordinate.

The manual mechanism map and assembly pages identify the A-8039-3 outhole/trough, C-9638 shooter, A-14525 right kickback, B-11873 left kickback, C-13174-L/R lower flipper assemblies, B-12665 kicker arms with B-13935 coils, A-14507 gun-kicker assembly, A-14504 cannon platform, A-13892-2 motor regulator, ball eject assemblies, A-14501 ball popper, A-14615 single-bank drop target, and lamp boards A-K. These relationships are retained as physical authoring knowledge; ambiguous manual assembly naming is not silently relabeled.

## Printed conflicts and script boundaries

Solenoid 12 is deliberately optional/conflicted: the early solenoid/location list says Knock Down / SM1-26-600, while the later electrical table says Not Used; the retained script has no `SolCallback(12)`. The later lamp schematic connector labels differ from the lamp matrix table; matrix address/name identity is retained without invented connector wiring. The manual names five GI strings as GI 1 Top Insert, GI 2 Left Playfield, GI 3 Right Playfield, GI 4 Not Used, and GI 5 Bottom Insert. The retained script instead toggles `GI2` (B1-B6 plus named GI objects 1-20/001/002) and `GI3` (named GI objects 21-35) for Case 2, has a separate Case 3 `Light2`-`Light5` branch, no Case 1 behavior, and exits on Case 4. Decorative Light2-Light5 and laser overlays are not promoted as physical GI or cannon emitters. The spatial audit retains the exact Case 2 object centers as conflicted evidence and leaves the other string routing unresolved.

The modern comparison script is not semantic authority. Its four-position trough, pulsed 62/64, virtual devices, and keyframed/magnet cannon are excluded. The g5k script is corroborating only where it agrees with the retained VPW behavior.

## Normalized playfield geometry

The exact coordinate convention is `x=raw_x/964`, `y=raw_y/2162`, with x=0 left and x=1 right, y=0 rear/backglass and y=1 apron/player. Placements name their exact retained VPX object and use the `vpx-table.t2-vpw-0022` source. The extraction contains 548 retained files totaling 132,477,924 bytes. Its retained `extracted-vpxtool.manifest.json` lists every sorted relative POSIX path with byte size and SHA-256; canonical JSON bytes hash to `f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9`. The curator recomputes and verifies the complete manifest before regeneration and whenever the evidence root is configured during `--check`.

Lamp, switch, flasher, cannon, trough, lock, shooter, popper, bumper, slingshot, ramp-entry, and lower-flipper positions with exact named table objects or disclosed assembly projections are retained in the definition. Switches 41-43 and outputs 13-15 share the exact three bumper centers. Switches 44/45 and outputs 6/5 use the extractor's exact left/right slingshot-wall drag-point centroids. Gates `sw61` and `sw63` locate the two ramp-entry switches. The left-outlane switch 25 anchors kickback output 8. Cabinet grip switch 34, knocker output 7, backglass flasher 24, start-button lamp 84, and the DMD are controlled non-playfield records rather than fake playfield points. Lamp 52 drives the exact object-space `Primitive.L52` skull-eye mesh; because that primitive reports `(0,0)`, its coordinate is an observed projection to the adjacent exact skull drop-target center and says so explicitly.

The three physical trough contacts are retained as an ordered 40/60/80-percent projection between the exact drain and ball-release anchors, consistent with the manual left/center/right map and carrying about plus or minus 0.03 normalized practical uncertainty. Their behavior and address order are complete, but the working table exposes only the cvpmBallStack rather than exact hidden contact seats. The remaining spatial blockers are optional/conflicted solenoid 12 and the unresolved GI 1/2/5 physical-string routing. The separate solenoid 12, GI-routing, and lamp-connector evidence conflicts also remain author-critical. The definition must remain partial until those exact facts are resolved by retained evidence.
"""


def expected(root: Path) -> tuple[dict[str, Any], str, dict[str, Any]]:
	definition = semantic.build_semantic()
	apply_spatial(definition)
	return definition, KNOWLEDGE.rstrip() + "\n", audit_report(definition)


def check(root: Path = ROOT) -> None:
	source_root = semantic.configured_vpx_sources_root(required=False)
	if source_root is not None:
		semantic.verify_extraction_manifest(source_root)
	definition, knowledge, audit = expected(root)
	actual_definition = definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	actual_knowledge = root / KNOWLEDGE_PATH.relative_to(ROOT)
	actual_audit = root / AUDIT_PATH.relative_to(ROOT)
	if not actual_definition.is_file() or actual_definition.read_bytes() != canonical_bytes(definition):
		raise SystemExit(f"T2 curator check failed: {actual_definition} is not deterministic output")
	if not actual_knowledge.is_file() or actual_knowledge.read_text(encoding="utf-8") != knowledge:
		raise SystemExit(f"T2 curator check failed: {actual_knowledge} is not deterministic output")
	if not actual_audit.is_file() or actual_audit.read_bytes() != canonical_bytes(audit):
		raise SystemExit(f"T2 curator check failed: {actual_audit} is not deterministic output")
	verified_suffix = " and configured extraction manifest" if source_root is not None else ""
	print(f"T2 curator check: deterministic canonical definition, knowledge, and spatial audit{verified_suffix}")


def generate(root: Path = ROOT) -> None:
	source_root = semantic.configured_vpx_sources_root(required=True)
	assert source_root is not None
	semantic.verify_extraction_manifest(source_root)
	definition, knowledge, audit = expected(root)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), knowledge)
	write_json(root / AUDIT_PATH.relative_to(ROOT), audit)
	rebuild_catalog(root)
	print("T2 curator regeneration: definition, knowledge, spatial audit, and catalog rebuilt")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	if args.check:
		check()
	else:
		generate()


if __name__ == "__main__":
	main()
