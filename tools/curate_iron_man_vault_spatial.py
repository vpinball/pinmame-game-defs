"""Promote Iron Man Pro Vault Edition with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text

from curate_iron_man import (
	CORE_SOURCE,
	FLASHER_QUANTITIES,
	VE_KNOWLEDGE,
	VE_MANUAL_SOURCE,
	VPX_SOURCE,
	build,
)


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/iron-man-vault-edition-2014.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/iron-man-vault-edition-2014.json"

TABLE_SOURCE = "vpx-table.iron-man-vault-vpw-1.0-geometry"
TABLE_SOURCE_RECORD = {
	"attribution": "VPW and the table authors credited by the table distribution",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx (245,182,464 bytes), exact im_185ve table extracted with vpxtool git:v0.33.3. Coordinates are accepted only where the embedded table geometry reconciles with the official 2014 physical maps and the pinned known-working sidecar script; VLM light-map, reflection, transmission, room, and VR helpers are excluded from physical counts. Lspot1/Lspot2 are retained as the two manual-listed above-playfield #555 GI sources after table-script reconciliation.",
	"original_filename": "Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
	"rights": "NOASSERTION",
	"sha256": "c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b",
	"uri": "external:pinmame-vpx-sources/stern/iron-man-vault-edition-2014/source/Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
}

INPUT_POSITIONS = {
	1: [(0.446429, 0.421130)], 3: [(0.446429, 0.421130)],
	4: [(0.370877, 0.412615)], 5: [(0.446429, 0.421130)], 6: [(0.521849, 0.412727)],
	7: [(0.089296, 0.139839)], 9: [(0.915127, 0.118325)], 10: [(0.199666, 0.224694)],
	11: [(0.164480, 0.433348)], 12: [(0.337684, 0.123937)], 13: [(0.453782, 0.155941)],
	14: [(0.838126, 0.454476)],
	18: [(0.646125, 0.927991)], 19: [(0.719888, 0.905518)],
	20: [(0.790850, 0.885051)], 21: [(0.858076, 0.866591)],
	22: [(0.930439, 0.845121)], 23: [(0.945733, 0.897573)],
	24: [(0.054345, 0.752864)], 25: [(0.145032, 0.718155)],
	26: [(0.275550, 0.726973)], 27: [(0.702914, 0.732205)],
	28: [(0.792639, 0.728542)], 29: [(0.876559, 0.759536)],
	30: [(0.567145, 0.173122)], 31: [(0.838245, 0.192110)], 32: [(0.668140, 0.254110)],
	33: [(0.117614, 0.482093)], 34: [(0.110518, 0.505808)], 35: [(0.103434, 0.529427)],
	36: [(0.096652, 0.552395)], 37: [(0.915480, 0.092892)], 38: [(0.707853, 0.122112)],
	39: [(0.797932, 0.129558)], 40: [(0.840225, 0.547131)], 41: [(0.840827, 0.570595)],
	42: [(0.840827, 0.594878)], 43: [(0.829368, 0.273845)], 44: [(0.206582, 0.336515)],
	45: [(0.412771, 0.254448)], 46: [(0.522313, 0.228940)], 47: [(0.600139, 0.301277)],
	48: [(0.676092, 0.310694)], 49: [(0.056488, 0.128980)], 50: [(0.666794, 0.399863)],
	81: [(0.658435, 0.835666)], 83: [(0.324865, 0.835666)],
}

SOLENOID_POSITIONS = {
	1: [(0.858076, 0.866591)], 2: [(0.942805, 0.978764)],
	3: [(0.448439, 0.490866)], 4: [(0.606800, 0.349757)],
	5: [(0.199666, 0.224694)], 6: [(0.522771, 0.066365)],
	9: [(0.567145, 0.173122)], 10: [(0.838245, 0.192110)], 11: [(0.668140, 0.254110)],
	12: [(0.612599, 0.121511)], 15: [(0.324865, 0.835666)], 16: [(0.658435, 0.835666)],
	17: [(0.275550, 0.726973)], 18: [(0.702914, 0.732205)], 19: [(0.446429, 0.421130)],
	20: [(0.696930, 0.203680)], 21: [(0.163340, 0.115124)],
	22: [(0.272424, 0.324770), (0.272424, 0.324770)], 23: [(0.462841, 0.220480)],
	25: [(0.364695, 0.378792), (0.531241, 0.378792)], 26: [(0.706933, 0.127314)],
	27: [(0.145118, 0.192556), (0.205913, 0.233077), (0.250067, 0.180066)],
	28: [(0.447072, 0.407742), (0.447072, 0.407742), (0.447072, 0.407742)],
	29: [(0.589444, 0.280486), (0.737121, 0.288520)],
	30: [(0.410511, 0.720898), (0.563715, 0.721215)],
	31: [(0.055666, 0.542583), (0.054880, 0.614537)],
	32: [(0.954307, 0.578104)],
}

LAMP_POSITIONS = {
	3: [(0.509335, 0.903753)], 4: [(0.055376, 0.709021)], 5: [(0.142070, 0.664381)],
	6: [(0.790312, 0.668090)], 7: [(0.874750, 0.692585)], 8: [(0.335529, 0.195620)],
	9: [(0.455559, 0.158431)], 10: [(0.459757, 0.198117)], 11: [(0.466105, 0.251706)],
	12: [(0.516745, 0.284824)], 13: [(0.444013, 0.303307)], 14: [(0.329336, 0.155594)],
	15: [(0.125811, 0.356210)], 16: [(0.154389, 0.396445)], 17: [(0.202533, 0.501237)],
	18: [(0.195840, 0.528556)], 19: [(0.189705, 0.555518)], 20: [(0.182324, 0.582240)],
	21: [(0.257362, 0.305465)], 22: [(0.347391, 0.264034)], 23: [(0.354412, 0.288954)],
	24: [(0.361897, 0.313884)], 25: [(0.368878, 0.338768)], 26: [(0.809762, 0.306471)],
	27: [(0.299417, 0.365126)], 28: [(0.574095, 0.519833)], 29: [(0.527652, 0.533234)],
	30: [(0.475298, 0.540142)], 31: [(0.420636, 0.540544)], 32: [(0.368645, 0.533055)],
	33: [(0.322103, 0.519879)], 34: [(0.899184, 0.340538)], 35: [(0.867446, 0.389405)],
	36: [(0.755753, 0.566286)], 37: [(0.757651, 0.593262)], 38: [(0.759124, 0.620528)],
	39: [(0.730043, 0.418090)], 40: [(0.713940, 0.442110)], 41: [(0.697342, 0.466193)],
	42: [(0.681093, 0.490139)], 43: [(0.246638, 0.384514)], 44: [(0.307791, 0.675986)],
	45: [(0.397580, 0.645894)], 46: [(0.492771, 0.628880)], 47: [(0.589158, 0.646064)],
	48: [(0.678978, 0.676255)], 49: [(0.493237, 0.741274)], 50: [(0.493051, 0.780912)],
	51: [(0.493289, 0.814080)], 52: [(0.493526, 0.842484)], 53: [(0.493532, 0.869662)],
	54: [(0.092444, 0.307706)], 55: [(0.484716, 0.681680), (0.484376, 0.707115)], 56: [(0.781901, 0.343919)],
	57: [(0.673381, 0.161408)], 58: [(0.749880, 0.164839)], 59: [(0.615541, 0.448343)],
	60: [(0.564409, 0.173177)], 61: [(0.836661, 0.192040)], 62: [(0.665708, 0.253966)],
	63: [(0.840803, 0.429852)],
}

# The exact VPW collection contains 31 giNNN objects and two Lspot sources. The
# manual count/geography and table history identify gi024/gi027/gi030/gi031 as
# rear-wall render pools. The two Lspot objects are the manual's above-playfield
# #555 bulbs; nearby gi004/gi014 are their separated under-playfield halo passes,
# not two additional sockets. The 25 remaining giNNN sources plus both Lspots
# reconcile exactly to manual circuits B=10, Y=7, and V=10.
GI_PLAYFIELD_POSITIONS = [
	("brown.01", 0.072786, 0.100092), ("brown.02", 0.226237, 0.129580),
	("brown.03", 0.174595, 0.269730), ("brown.04", 0.191563, 0.297950),
	("brown.05", 0.056556, 0.368024), ("brown.06", 0.060244, 0.428270),
	("brown.07", 0.056556, 0.476467), ("brown.08", 0.505841, 0.143334),
	("brown.09", 0.406246, 0.119791), ("brown.10", 0.215770, 0.169017),
	("yellow.01", 0.235689, 0.807358), ("yellow.02", 0.265568, 0.759737),
	("yellow.above-playfield-555", 0.230629, 0.685078), ("yellow.04", 0.051391, 0.532590),
	("yellow.05", 0.083114, 0.595690), ("yellow.06", 0.069097, 0.617252),
	("yellow.07", 0.153200, 0.782766),
	("violet.01", 0.734911, 0.813779), ("violet.02", 0.793996, 0.795586),
	("violet.03", 0.721216, 0.759737), ("violet.above-playfield-555", 0.743541, 0.692584),
	("violet.05", 0.885767, 0.592306), ("violet.06", 0.885766, 0.553705),
	("violet.07", 0.753585, 0.112835), ("violet.08", 0.665194, 0.118721),
	("violet.09", 0.876094, 0.228866), ("violet.10", 0.842934, 0.129627),
]

# The manual proves ten sockets in one rear-panel row. Its perspective sketch
# labels the row but does not expose ten independently measurable centers, so
# these are an explicit equal-spacing projection across the usable panel width.
GI_REAR_PANEL_POSITIONS = [
	("green.01", 0.090000, 0.000000), ("green.02", 0.181000, 0.000000),
	("green.03", 0.272000, 0.000000), ("green.04", 0.363000, 0.000000),
	("green.05", 0.454000, 0.000000), ("green.06", 0.546000, 0.000000),
	("green.07", 0.637000, 0.000000), ("green.08", 0.728000, 0.000000),
	("green.09", 0.819000, 0.000000), ("green.10", 0.910000, 0.000000),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 69: "cabinet.coin.fifth",
	82: "flipper.lower.right.button", 84: "flipper.lower.left.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
}

INTERNAL_OUTPUT_ROLES = {
	("pinmame.output.lamp", 73): "internal.load",
	("pinmame.output.lamp", 79): "internal.load",
	("pinmame.output.lamp", 80): "internal.load",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(
	device: dict[str, object],
	role: str,
	positions: list[tuple[float, float]] | list[tuple[str, float, float]],
	source_refs: tuple[str, ...],
) -> None:
	placements = []
	for index, position in enumerate(positions, start=1):
		if len(position) == 3:
			suffix, x, y = position
			placement_suffix = f".{suffix}"
		else:
			x, y = position
			placement_suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{device['id']}.{role}{placement_suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _set_placement_sources(device: dict[str, object], index: int, *source_refs: str) -> None:
	device["spatial"]["placements"][index]["provenance"] = _provenance(*source_refs)


def apply_spatial(
	definition: dict[str, object],
	*,
	geometry_source: str = TABLE_SOURCE,
	manual_source: str = VE_MANUAL_SOURCE,
	projection_source: str = VE_MANUAL_SOURCE,
	product_label: str = "Iron Man Vault",
	preserve_existing_gi_construction: bool = False,
) -> None:
	"""Apply one reviewed shared-layout disposition without changing edition construction."""
	if len(GI_PLAYFIELD_POSITIONS) != 27 or len(GI_REAR_PANEL_POSITIONS) != 10:
		raise ValueError("Iron Man Vault GI map must contain 27 playfield and ten rear-panel placements")
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", manual_source)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], (geometry_source,))
			if address == 22:
				device.setdefault("physical", {})["notes"] = "The exact VPW omits a sw22 object. This approximate jam-opto anchor is the six-decimal least-squares continuation of the exact consecutive sw18-sw21 trough-sensor centers; it preserves trough order without claiming a directly measured switch center. Practical uncertainty is about plus or minus 0.02 normalized x and y."
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", manual_source)
		else:
			raise ValueError(f"{product_label} input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "cabinet_or_service", manual_source)
		elif (group, address) in INTERNAL_OUTPUT_ROLES:
			device.setdefault("roles", [INTERNAL_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "internal_nonvisual", manual_source)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], (geometry_source,))
			physical = device.setdefault("physical", {})
			if kind == "flasher":
				physical["quantity"] = FLASHER_QUANTITIES[address]
			if address in {22, 28}:
				physical["notes"] += " Each manual-listed physical module retains an individual placement ID at the shared assembly/cluster anchor because the exact VPW table collapses the modules into one light pool; the co-located projection does not claim recoverable separation, and VLM fanout is not extra hardware."
			elif address == 27:
				_set_placement_sources(device, 2, projection_source)
				physical["notes"] += " Two emitter points come directly from l127a/l127b; the third is a calibrated projection from the official location-map callout because l127r is only a co-located render pass. Manual-projected anchors have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y."
			elif address == 30:
				for index in range(len(SOLENOID_POSITIONS[address])):
					_set_placement_sources(device, index, projection_source)
				physical["notes"] += " The two physical placements are calibrated approximate anchors from the official location-map callouts; exact VPW object l130 is one collapsed light pool between them, while its VLM fanout is not extra hardware. Manual-projected anchors have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y."
			elif address == 31:
				for index in range(len(SOLENOID_POSITIONS[address])):
					_set_placement_sources(device, index, projection_source)
				physical["notes"] += " Both physical placements are calibrated approximate anchors from the separately marked Q31 callouts in the official location map; exact VPW object l131 is one collapsed light pool between them. Manual-projected anchors have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y."
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], (geometry_source,))
			device.setdefault("physical", {}).setdefault("quantity", 1)
			if address == 55:
				for index in range(len(LAMP_POSITIONS[address])):
					_set_placement_sources(device, index, projection_source)
				device["physical"]["notes"] += " Both manual-listed emitters retain individual placement IDs at calibrated approximate anchors from the two separately printed callouts; exact VPW objects l55/l55r are co-located render passes that collapse the physical separation into one light pool. Manual-projected anchors have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y."
		elif group == "pinmame.output.gi" and address == 0:
			_located(device, "emitter", [*GI_PLAYFIELD_POSITIONS, *GI_REAR_PANEL_POSITIONS], (geometry_source,))
			for index in range(len(GI_PLAYFIELD_POSITIONS), len(GI_PLAYFIELD_POSITIONS) + len(GI_REAR_PANEL_POSITIONS)):
				_set_placement_sources(device, index, projection_source)
			physical = device.setdefault("physical", {})
			if preserve_existing_gi_construction:
				construction_notes = str(physical.get("notes", "")).strip()
				spatial_notes = "The shared 2D frame uses exact Lspot1/Lspot2 source centers for placement IDs yellow.above-playfield-555 and violet.above-playfield-555. Nearby gi004/gi014 are separated halo/render passes, not additional placement points. The other 25 playfield points are exact reconciled giNNN objects. VPW gi024/gi027/gi030/gi031 are four rear-wall render pools, not physical sockets; the rear-row anchors are explicit evenly spaced projections at y=0 from the reviewed shared layout rather than independently measurable centers. These geometry notes do not transfer Vault bulb inventory, circuit counts, or cabinet construction to the original edition."
				physical["notes"] = " ".join(part for part in (construction_notes, spatial_notes) if part)
			else:
				spatial_notes = "The manual fixes playfield circuits B/Y/V at 10/7/10 and rear circuit G at 10. The playfield inventory is 25 under-playfield #44 bulbs plus two above-playfield #555 bulbs: placement IDs yellow.above-playfield-555 and violet.above-playfield-555 use exact Lspot1/Lspot2 source centers. Nearby gi004/gi014 are separated halo/render passes for those spot bulbs, not additional sockets; VPW's changelog says the spotlight bulbs were separated and its ball-shadow code treats Lspot1/Lspot2 as the light sources. The other 25 playfield points are exact reconciled giNNN objects. VPW gi024/gi027/gi030/gi031 are four rear-wall render pools, not physical sockets. Ten rear #44 sockets are projected as an explicitly documented evenly spaced y=0 row because the perspective drawing proves the row/count but not ten exact centers. The US cabinet's two #555 coin-door bulbs intentionally have no playfield coordinate; European cabinets use three instead, for a total physical quantity of 40 rather than 39."
				physical.update({
					"quantity": 39,
					"location": "27 playfield bulbs, 10 rear-panel bulbs, and two US coin-door bulbs; European cabinets use three coin-door bulbs",
					"notes": spatial_notes,
				})
		else:
			raise ValueError(f"{product_label} output {group} {address} ({kind}) has no reviewed spatial disposition")


def promote() -> None:
	definition = build(True)
	if not any(source["id"] == TABLE_SOURCE for source in definition["sources"]):
		definition["sources"].append(TABLE_SOURCE_RECORD)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/iron-man-vault-edition-2014.md", VE_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
