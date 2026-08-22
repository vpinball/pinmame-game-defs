"""Generate the reviewed X-Men Limited Edition spatial partial."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from curate_xmen import LE_KNOWLEDGE, build_le
from pinmame_game_defs.jsonio import write_json, write_text

TABLE_SOURCE = "vpx-table.x-men-le-vpw-1.0"
CORROBORATING_SOURCE = "vpx-table.x-men-le-v2.0.1"
CORROBORATING_TEST_SOURCE = "vpx-table.x-men-le-v2.2.7a-test"
MANUAL_SOURCE = "manual.x-men-pro-le.2012.high-resolution"
SCRIPT_SOURCE = "vpx.x-men-le-vpw-1.0.6"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"

CORROBORATING_GEOMETRY_OUTPUTS = {18, 22, 28, 29, 31}
MANUAL_DERIVED_GEOMETRY_OUTPUTS = {19, 20, 30}

TABLE_SOURCE_RECORD = {
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"uri": "external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) VPW v1.0.vpx",
	"original_filename": "X-Men LE (Stern 2012) VPW v1.0.vpx",
	"sha256": "332c0a822024e7e0701e3939bdde0c0e0e4026479ef86414f93887681b3fa22e",
	"locator": "Exact physical LE table found in the first requested VPX search location and retained byte-for-byte at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) VPW v1.0.vpx. vpxtool git:v0.33.3 extraction is retained at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/extraction/VPW_v1.0; candidate and review artifacts are retained at external:pinmame-review-artifacts/stern/x-men-limited-edition-2012. Canonical playfield bounds are left=0 top=0 right=952 bottom=2115. The embedded script is the VPW v1.0 implementation of the pinned LE v1.0.6 semantic mapping.",
	"license": "NOASSERTION",
	"attribution": "VPW table authors and local user-authorized source",
	"rights": "NOASSERTION",
}

CORROBORATING_TABLE_SOURCE_RECORDS = [
	{
		"id": "vpx-table.x-men-le-v2.0.1",
		"kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) v2.0.1.vpx",
		"original_filename": "X-Men LE (Stern 2012) v2.0.1.vpx",
		"sha256": "5b78b36d07ed2f06c5aad360deb04c67d8f31fce9770843a178aac1bd624f5a7",
		"locator": "Exact physical LE corroborating table found in the first requested VPX search location and retained byte-for-byte at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) v2.0.1.vpx; vpxtool git:v0.33.3 extraction is retained at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/extraction/v2.0.1 and review artifacts at external:pinmame-review-artifacts/stern/x-men-limited-edition-2012. Its canonical playfield bounds are left=0 top=0 right=952 bottom=2115.",
		"license": "NOASSERTION",
		"attribution": "Local user-authorized source",
		"rights": "NOASSERTION",
	},
	{
		"id": "vpx-table.x-men-le-v2.2.7a-test",
		"kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) v2.2.7a_TEST.vpx",
		"original_filename": "X-Men LE (Stern 2012) v2.2.7a_TEST.vpx",
		"sha256": "68a4ffd02b70cdba06377c51b6feffe6bd1b5d332917fe1fef0f89c52b0d730b",
		"locator": "Exact physical LE corroborating test table found in the first requested VPX search location and retained byte-for-byte at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/X-Men LE (Stern 2012) v2.2.7a_TEST.vpx; vpxtool git:v0.33.3 extraction is retained at external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/extraction/v2.2.7a_TEST and review artifacts at external:pinmame-review-artifacts/stern/x-men-limited-edition-2012. Its canonical playfield bounds are left=0 top=0 right=952 bottom=2115.",
		"license": "NOASSERTION",
		"attribution": "Local user-authorized source",
		"rights": "NOASSERTION",
	},
]


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(device: dict[str, object], role: str, positions: list[tuple[str, float, float]] | list[tuple[float, float]], source_refs: tuple[str, ...]) -> None:
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
			"provenance": provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# All points below are normalized from the exact VPW v1.0 LE table's 952 x
# 2115 playfield.  Wall/target points are drag-point centroids; the script is
# the authority for which public switch or coil uses each shared assembly.
INPUT_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.100904, 0.552531)], 2: [(0.113893, 0.528948)],
	4: [(0.233580, 0.562019)], 7: [(0.832983, 0.487234)], 8: [(0.832983, 0.525532)],
	11: [(0.084819, 0.388448)], 12: [(0.437556, 0.318400)], 13: [(0.179486, 0.205924)], 14: [(0.075417, 0.147665)],
	18: [(0.646125, 0.922217)], 19: [(0.719888, 0.898681)], 20: [(0.790850, 0.877247)],
	21: [(0.858076, 0.857914)], 22: [(0.858076, 0.857914)], 23: [(0.947528, 0.887323)],
	24: [(0.040627, 0.748208)], 25: [(0.121629, 0.719866)],
	26: [(0.213427, 0.720161)], 27: [(0.634191, 0.720606)],
	28: [(0.719549, 0.698139)], 29: [(0.854134, 0.738323)],
	30: [(0.087328, 0.350202)], 31: [(0.316005, 0.377159)], 32: [(0.152280, 0.434311)],
	33: [(0.786626, 0.702333)], 34: [(0.713607, 0.753937)], 35: [(0.926444, 0.376846)],
	36: [(0.358569, 0.427520)], 38: [(0.526723, 0.189076)], 39: [(0.526783, 0.165400)],
	40: [(0.526897, 0.141724)], 41: [(0.470056, 0.241957)], 42: [(0.590983, 0.241975)],
	47: [(0.697592, 0.173979)], 48: [(0.848210, 0.146190)], 49: [(0.945972, 0.168714)],
	50: [(0.437556, 0.318400)], 51: [(0.715157, 0.347220)], 52: [(0.819398, 0.247728)],
	53: [(0.526092, 0.204412)], 54: [(0.259913, 0.096516)], 55: [(0.290112, 0.135274)],
	56: [(0.715157, 0.347220)],
}

FLIPPER_INPUT_POSITIONS = {
	81: [(0.587091, 0.827754)], 83: [(0.258410, 0.827754)],
}

# Q6/Q7 use this derived/shared assembly anchor because the working script and
# center-lock mechanism tie both actuators to Trigger.sw53.center; it is not an
# exact actuator object coordinate.
CENTER_LOCK_ASSEMBLY_POSITION = INPUT_POSITIONS[53]

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "flipper.right.button", 84: "flipper.left.button", 86: "flipper.upper.button",
	-7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
}

LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	17: [(0.563601, 0.761632)], 18: [(0.519803, 0.780688)], 19: [(0.471590, 0.798827)],
	20: [(0.342718, 0.725513)], 21: [(0.305873, 0.688944)], 22: [(0.339136, 0.649526)],
	23: [(0.423552, 0.635050)], 24: [(0.504730, 0.650227)], 25: [(0.537914, 0.686988)],
	26: [(0.504287, 0.724727)], 27: [(0.419934, 0.739746)], 28: [(0.281828, 0.761631)],
	29: [(0.325836, 0.780816)], 30: [(0.373485, 0.798860)], 31: [(0.422557, 0.817990)],
	32: [(0.423152, 0.853380)], 33: [(0.045860, 0.678763)], 34: [(0.121108, 0.652181)],
	35: [(0.151743, 0.572861)], 36: [(0.167019, 0.544004)], 37: [(0.463607, 0.575456)],
	38: [(0.438905, 0.543037)], 41: [(0.150519, 0.435941)], 42: [(0.315990, 0.382277)],
	43: [(0.087960, 0.351304)], 45: [(0.318817, 0.521179)], 46: [(0.319257, 0.542968)],
	47: [(0.323573, 0.565199)], 48: [(0.329243, 0.588236)], 49: [(0.348360, 0.233212)],
	50: [(0.299413, 0.212053)], 51: [(0.240520, 0.188731)], 52: [(0.192139, 0.381207)],
	53: [(0.170456, 0.315069)], 54: [(0.143040, 0.279598)], 55: [(0.213888, 0.233916)],
	56: [(0.261934, 0.263367)], 57: [(0.388630, 0.181035)], 58: [(0.408718, 0.225636)],
	59: [(0.194525, 0.478190)], 60: [(0.461269, 0.281431)], 65: [(0.526911, 0.326655)],
	66: [(0.525844, 0.295079)], 67: [(0.526478, 0.259843)], 68: [(0.718870, 0.642198)],
	69: [(0.785783, 0.633371)], 70: [(0.860694, 0.678878)], 71: [(0.768503, 0.529222)],
	72: [(0.768488, 0.497582)], 73: [(0.777819, 0.266319)], 74: [(0.803386, 0.232139)],
	75: [(0.674542, 0.210821)], 76: [(0.653117, 0.248438)], 77: [(0.596823, 0.282332)],
	78: [(0.902282, 0.262311)], 79: [(0.869890, 0.298646)], 80: [(0.850123, 0.332182)],
}

GI_POSITIONS: list[tuple[str, float, float]] = [
	("white.01", 0.184503, 0.804470), ("white.02", 0.199428, 0.746927),
	("white.03", 0.681216, 0.798894), ("white.04", 0.645025, 0.745404),
	("white.05", 0.042065, 0.608527), ("white.06", 0.062602, 0.529685),
	("white.07", 0.855284, 0.598401), ("white.08", 0.876475, 0.532790),
	("white.09", 0.046405, 0.275203), ("white.10", 0.326345, 0.167374),
	("white.11", 0.616334, 0.089095), ("white.12", 0.941144, 0.061307),
	("red.01", 0.611013, 0.064455), ("red.02", 0.171177, 0.710282),
	("red.03", 0.675136, 0.708067), ("red.04", 0.040976, 0.513464),
	("red.05", 0.876226, 0.506039), ("red.06", 0.037924, 0.255623),
	("red.07", 0.657403, 0.130514), ("red.08", 0.936111, 0.014471),
	("red.09", 0.441899, 0.161794),
	("blue.01", 0.122942, 0.784854), ("blue.02", 0.760737, 0.772311),
	("blue.03", 0.036388, 0.544721), ("blue.04", 0.847637, 0.570817),
	("blue.05", 0.048667, 0.294000), ("blue.06", 0.361599, 0.117707),
	("blue.07", 0.854768, 0.021381), ("blue.08", 0.883100, 0.131839),
	("base.01", 0.190803, 0.658392), ("base.02", 0.600013, 0.739413),
]

SOLENOID_POSITIONS: dict[int, list[tuple[float, float] | tuple[str, float, float]]] = {
	1: [(0.858076, 0.857914)], 2: [(0.947521, 0.886879)], 3: [(0.233580, 0.562019)],
	4: [(0.526786, 0.406147)], 5: [(0.290112, 0.135274)], 6: CENTER_LOCK_ASSEMBLY_POSITION,
	7: CENTER_LOCK_ASSEMBLY_POSITION, 9: [(0.087328, 0.350202)], 10: [(0.316005, 0.377159)],
	11: [(0.152280, 0.434311)], 12: [(0.872687, 0.398011)], 13: [(0.213427, 0.720161)],
	14: [(0.634191, 0.720606)], 15: [(0.258410, 0.827754)], 16: [(0.587091, 0.827754)],
	17: [(0.063596, 0.303155), (0.063778, 0.601628)],
	18: [(0.951053, 0.309522)],
	19: [("clear.01", 0.433, 0.349), ("clear.02", 0.656, 0.456)],
	20: [("blue.01", 0.669, 0.400), ("blue.02", 0.487, 0.470)],
	21: [(0.343684, 0.433658)],
	22: [("f122a", 0.608390, 0.169829), ("f122b", 0.450827, 0.172193)], 23: [(0.526293, 0.404828)],
	25: [(0.189278, 0.383700)], 26: [(0.360405, 0.059397)],
	27: [(0.713607, 0.753937), (0.926444, 0.376846)], 28: [("f28a", 0.148958, 0.018409), ("f28b", 0.286423, 0.018409), ("f28c", 0.425408, 0.018409)],
	29: [("f29a", 0.559517, 0.018409), ("f29b", 0.699833, 0.018409), ("f29c", 0.837139, 0.018409)],
	30: [("spotlight", 0.371, 0.425)],
	31: [("f131a", 0.118833, 0.882520), ("f131b", 0.791374, 0.881999)],
	32: [(0.529075, 0.158083)], 51: [(0.389991, 0.476778)],
	52: [(0.437556, 0.318400)], 53: [(0.715157, 0.347220)], 57: [(0.437556, 0.318400)],
	58: [(0.715157, 0.347220)],
}

FLASHER_QUANTITIES = {17: 2, 18: 1, 19: 2, 20: 2, 21: 1, 22: 2, 25: 1, 28: 3, 29: 3, 30: 1, 31: 2, 32: 1}


def apply_spatial(definition: dict[str, object]) -> None:
	definition["machine"]["playfield"] = {
		"width": 952,
		"height": 2115,
		"units": "vpx",
		"provenance": provenance(TABLE_SOURCE),
	}
	for display in definition["displays"]:
		display["spatial"] = {
			"status": "not_applicable",
			"reason": "cabinet_or_service",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}

	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			coordinate_sources = (TABLE_SOURCE, MANUAL_SOURCE) if group == "pinmame.input.switch" and address == 22 else (TABLE_SOURCE,)
			located(device, "sensor", INPUT_POSITIONS[address], coordinate_sources)
		elif address in FLIPPER_INPUT_POSITIONS:
			located(device, "sensor", FLIPPER_INPUT_POSITIONS[address], (TABLE_SOURCE,))
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"X-Men LE input {group} {address} has no reviewed spatial disposition")

		if group == "pinmame.input.switch" and address in {18, 19, 20, 21}:
			device.setdefault("physical", {})["location"] = "Under-apron four-ball trough; exact table kicker center supplies the placement."
		elif group == "pinmame.input.switch" and address == 22:
			physical = device.setdefault("physical", {})
			physical["location"] = "Under-apron trough exit; upper stacking beam on the same dual-opto board assembly as switch 21."
			physical["notes"] = "The Stern page-b3 trough cut-away places switch 22 directly above switch 21 on the shared transmitter/receiver pair. Because that distinction is vertical, both sensors share the exact switch-21 table anchor in the normalized two-dimensional playfield plane."
		elif group == "pinmame.input.switch" and address in {12, 50}:
			device.setdefault("physical", {})["location"] = "Left Nightcrawler moving pop-up assembly; the exact table uses one wall assembly for the down and hit sensors."
		elif group == "pinmame.input.switch" and address in {51, 56}:
			device.setdefault("physical", {})["location"] = "Right Nightcrawler moving pop-up assembly; the exact table uses one wall assembly for the hit and down sensors."
		elif group == "pinmame.input.switch" and address in {34, 35}:
			device.setdefault("physical", {})["location"] = "Iceman motorized Ice Slide limit assembly; exact VPX triggers map Start to switch 35/away and End to switch 34/home."
		elif group == "pinmame.input.switch" and address in {38, 39, 40, 53}:
			device.setdefault("physical", {})["location"] = "Magneto four-level vertical lock occupancy optos, bottom-to-top 53/38/39/40."

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			not_applicable(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			not_applicable(device, "virtual", CORE_SOURCE)
		elif group == "pinmame.output.lamp" and address == 39:
			device["roles"] = ["cabinet.start"]
			device.setdefault("physical", {})["quantity"] = 1
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 8:
			device["roles"] = ["cabinet.shaker"]
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 24:
			device["roles"] = ["cabinet.coin-meter"]
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in {54, 55, 56}:
			device["roles"] = ["internal.gi.channel"]
			not_applicable(device, "internal_nonvisual", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			if address in MANUAL_DERIVED_GEOMETRY_OUTPUTS:
				coordinate_sources = (MANUAL_SOURCE,)
			elif address in CORROBORATING_GEOMETRY_OUTPUTS:
				coordinate_sources = (CORROBORATING_SOURCE,)
			elif address in {6, 7}:
				coordinate_sources = (TABLE_SOURCE, SCRIPT_SOURCE)
			else:
				coordinate_sources = (TABLE_SOURCE,)
			located(device, role, SOLENOID_POSITIONS[address], coordinate_sources)
			physical = device.setdefault("physical", {})
			if kind == "flasher":
				quantity = FLASHER_QUANTITIES[address]
				if len(SOLENOID_POSITIONS[address]) != quantity:
					raise ValueError(f"X-Men LE flasher F{address} socket reconciliation mismatch: expected {quantity}, got {len(SOLENOID_POSITIONS[address])}")
				physical["quantity"] = quantity
				if address in MANUAL_DERIVED_GEOMETRY_OUTPUTS:
					physical["notes"] = "Stern manual PDF pages 60-61 control the Limited Edition installed quantity and physical location. Placements are reproducibly measured page-61 numbered device-symbol centers normalized against the documented playfield frame and rounded to three decimals; they preserve the factory drawing's socket relationships but are not exact VPX emitter-object centers."
				else:
					physical["notes"] = "Stern manual PDF page 60 controls the installed quantity; each direct flasher placement is an exact table-object coordinate. Derived/shared assembly anchors are disclosed separately and are not exact actuator coordinates."
				if address == 19:
					physical["location"] = "Magneto rotating-disc clear flasher pair, at the two Q19 callouts on opposite sides of the disc."
				elif address == 20:
					physical["location"] = "Magneto rotating-disc blue flasher pair, alternating with the two Q19 clear flashers."
				elif address == 30:
					physical["location"] = "Magneto spotlight immediately left of the rotating disc on the factory coil-location drawing."
				elif address == 18:
					physical["location"] = "Right-side flasher assembly; one manual socket at the exact LE v2.0.1 Light.Flasherlight3 center (905.4027, 654.639). The paired Flasher.Flasherflash3 is a render layer, not a second socket."
				elif address == 22:
					physical["location"] = "Magneto left/right flasher pair; exact LE v2.0.1 Light.f122a and Light.f122b emitter centers provide two distinct physical assemblies."
					physical["notes"] += " Coordinates are the exact named Light.f122a/f122b centers, normalized from 952 x 2115; the prior Primitive.Target_004_*/Target_001_* lightmap recipients are not emitters."
				elif address == 28:
					physical["location"] = "Rear back-panel left flasher group; the three exact LE v2.0.1 Flasher.f28a/f28b/f28c polygon centroids are retained as three distinct socket assemblies."
					physical["notes"] += " Coordinates are disclosed centroids of the exact named four-point flasher polygons, normalized from 952 x 2115; all are in bounds."
				elif address == 29:
					physical["location"] = "Rear back-panel right flasher group; the three exact LE v2.0.1 Flasher.f29a/f29b/f29c polygon centroids are retained as three distinct socket assemblies."
					physical["notes"] += " Coordinates are disclosed centroids of the exact named four-point flasher polygons, normalized from 952 x 2115; all are in bounds."
				elif address == 31:
					physical["location"] = "Bottom-arch flasher pair; exact LE v2.0.1 Light.f131a and Light.f131b static-bulb centers provide two distinct in-bounds physical assemblies."
					physical["notes"] += " The in-bounds centers (113.12879, 1866.5297) and (753.3876, 1865.4272) replace the prior invented (0,1) boundary projection."
			if address in {6, 7}:
				physical["location"] = "Magneto four-level vertical lock, shared dual up-post/latch assembly."
				physical["notes"] = "Derived/shared assembly geometry: the working script and center-lock mechanism tie outputs 6 and 7 to the exact Trigger.sw53.center (0.526092, 0.204412) anchor. This is not an exact Q6/Q7 actuator object coordinate."
			elif address in {19, 20, 23} and kind != "flasher":
				physical["location"] = "Magneto spinning disc assembly; exact VPX Disc lightmap/turntable anchor."
			elif address == 26:
				physical["location"] = "Magneto orbit diverter assembly; exact VPX RampDiverter anchor."
			elif address == 27:
				physical["location"] = "Iceman motorized Ice Slide; two exact VPX limit-trigger anchors describe the moving assembly."
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			located(device, "emitter", LAMP_POSITIONS[address], (TABLE_SOURCE,))
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.gi" and address == 0:
			if len(GI_POSITIONS) != 31:
				raise ValueError(f"X-Men LE GI socket reconciliation mismatch: {len(GI_POSITIONS)}")
			located(device, "emitter", GI_POSITIONS, (TABLE_SOURCE,))
			device.setdefault("physical", {}).update({
				"quantity": 31,
				"location": "31 playfield GI sockets: 12 white, 9 red, 8 blue, and 2 base-GI sockets shown by the Stern LE maps and named by the exact table.",
				"notes": "Public GI 0 is the master supply. Public auxiliary outputs 54-56 are subtractive color channels, not additional physical emitters; their causal mapping remains in the recreation knowledge and mechanism record.",
			})
		else:
			raise ValueError(f"X-Men LE output {group} {address} ({kind}) has no reviewed spatial disposition")


def _assert_flasher_socket_contract(definition: dict[str, object]) -> None:
	outputs = {
		int(device["binding"]["device"]): device
		for device in definition["outputs"]
		if device["binding"]["group"] == "pinmame.output.solenoid"
	}
	for address, quantity in FLASHER_QUANTITIES.items():
		device = outputs[address]
		placements = device["spatial"]["placements"]
		if len(placements) != quantity:
			raise ValueError(f"X-Men LE F{address} requires {quantity} physical socket placements, got {len(placements)}")
		if any(not (0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1) for placement in placements):
			raise ValueError(f"X-Men LE F{address} has an out-of-bounds physical placement")
	if any(placement["x"] == 0 and placement["y"] == 1 for placement in outputs[31]["spatial"]["placements"]):
		raise ValueError("X-Men LE F31 cannot use an invented boundary projection")


def _assert_placement_provenance(definition: dict[str, object]) -> None:
	source_ids = {source["id"] for source in definition["sources"]}
	for collection in (definition["inputs"], definition["outputs"]):
		for device in collection:
			for placement in device.get("spatial", {}).get("placements", []):
				refs = placement["provenance"]["source_refs"]
				if not refs or any(ref not in source_ids for ref in refs):
					raise ValueError(f"{placement['id']} must name every source required to reproduce or license the placement")
	inputs = {int(device["binding"]["device"]): device for device in definition["inputs"] if device["binding"]["group"] == "pinmame.input.switch"}
	if set(inputs[22]["spatial"]["placements"][0]["provenance"]["source_refs"]) != {TABLE_SOURCE, MANUAL_SOURCE}:
		raise ValueError("X-Men LE switch 22 must name both the table coordinate and manual shared-opto derivation")
	outputs = {int(device["binding"]["device"]): device for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.solenoid"}
	for address in (6, 7):
		if set(outputs[address]["spatial"]["placements"][0]["provenance"]["source_refs"]) != {TABLE_SOURCE, SCRIPT_SOURCE}:
			raise ValueError(f"X-Men LE output {address} must name both the table anchor and working-script assembly derivation")


def _promote_when_spatially_complete(definition: dict[str, object]) -> None:
	if definition.get("conflicts"):
		raise ValueError("X-Men LE cannot be author-ready while unresolved conflicts remain")
	for collection_name in ("inputs", "outputs", "displays"):
		for device in definition[collection_name]:
			spatial = device.get("spatial")
			if not isinstance(spatial, dict) or spatial.get("status") not in {"validated", "not_applicable"}:
				raise ValueError(f"{device['id']} prevents X-Men LE author-ready promotion: spatial disposition is incomplete")
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"


SPATIAL_KNOWLEDGE_APPENDIX = """## Normalized spatial evidence

The schema-v2 records retain direct coordinates when an exact LE VPX table object supplies them, explicitly disclosed shared-assembly anchors when the working script and mechanism justify reusing a table point, and measured factory-manual device-symbol centers where a table exposes only render proxies. The VPW v1.0 table supplies a canonical 952 by 2115 playfield extent and the normalized controller/device points; the exact LE v2.0.1 table supplies the named flasher geometry retained for F18, F22, F28, F29, and F31. Placement provenance names the coordinate source plus any manual or working-script source required to justify a shared anchor. The exact LE v2.2.7a_TEST table remains retained as corroborating evidence, but it is not incorrectly claimed as a coordinate source.

The official Stern manual PDF page 60 was visually verified at the root: F17 reads `FLASH: LEFT SIDE (X2)` and F18 reads `FLASH: RIGHT SIDE`, so F18 quantity is one. The complete flasher set contains 21 physical sockets. Page 61 places both F19 clear sockets and both F20 blue sockets as alternating pairs around the Magneto disc, and places the single F30 Magneto spotlight immediately left of the disc. A retained native-resolution crop and transcription record the full-page 2531 by 3557 render, playfield-frame corners, five device-symbol pixel centers, normalization formula, and three-decimal results. A Q4 control measurement lands within 0.014 normalized units of the exact VPW Magneto anchor, demonstrating that the manual and table frames agree while quantifying their drafting tolerance. The five placements retain only the Limited Edition manual as coordinate provenance, avoiding the retained tables' one-center disc lightmaps and unrelated F30 render proxy.

The four ball-position switches 18-21 use exact table kicker centers. The manual's page-b3 trough cut-away proves switch 22 is the upper stacking beam on the same dual-opto transmitter/receiver assembly as switch 21. Because the physical distinction is vertical, outside the normalized x/y plane, switch 22 shares the exact switch-21 table anchor and its placement provenance names both the table coordinate and the manual derivation. Outputs Q6/Q7 similarly share the exact `Trigger.sw53.center` anchor only as derived assembly geometry; their placement provenance names both the table anchor and the working script that ties both actuators to the center-lock assembly. This is not an exact actuator object coordinate. F22 uses the exact v2.0.1 `Light.f122a` `(0.608390, 0.169829)` and `Light.f122b` `(0.450827, 0.172193)` emitter centers; the prior `Primitive.Target_004_*`/`Target_001_*` lightmap recipients are excluded. Cabinet/service inputs, the start-button lamp, shaker, coin meter, unused channels, the DIP bank, GI dim control outputs 54-56, and virtual output 33 remain explicitly controlled non-playfield records. The Pro table and archive `xmn_151` table are excluded from LE spatial evidence. With every installed LE playfield device now assigned or explicitly non-spatial, the definition is author-ready.
"""


def generate(root: Path = ROOT) -> None:
	partial_path = root / "machines/partial/stern/x-men-limited-edition-2012.json"
	author_ready_path = root / "machines/author-ready/stern/x-men-limited-edition-2012.json"
	legacy_path = root / "machines/partial/stern/x-men-le-2012.json"
	if legacy_path.exists():
		raise RuntimeError(
			f"Refusing to regenerate {author_ready_path}: legacy X-Men LE definition exists at {legacy_path}; "
			"resolve the duplicate canonical definition explicitly before curating again."
		)
	if partial_path.exists():
		raise RuntimeError(
			f"Refusing to regenerate {author_ready_path}: a partial canonical definition exists at {partial_path}; "
			"treat it as a deliberate demotion and resolve the evidence gap explicitly before promoting again."
		)
	definition = build_le()
	for replacement in [TABLE_SOURCE_RECORD, *CORROBORATING_TABLE_SOURCE_RECORDS]:
		for index, source in enumerate(definition["sources"]):
			if source["id"] == replacement["id"]:
				definition["sources"][index] = replacement
				break
		else:
			definition["sources"].append(replacement)
	definition["schema_version"] = 2
	apply_spatial(definition)
	_assert_flasher_socket_contract(definition)
	_assert_placement_provenance(definition)
	_promote_when_spatially_complete(definition)
	write_json(author_ready_path, definition)
	write_text(root / "knowledge/stern/x-men-limited-edition-2012.md", LE_KNOWLEDGE.rstrip() + "\n\n" + SPATIAL_KNOWLEDGE_APPENDIX.rstrip() + "\n")


def check(root: Path = ROOT) -> None:
	partial_path = root / "machines/partial/stern/x-men-limited-edition-2012.json"
	if partial_path.exists():
		raise RuntimeError(f"Refusing X-Men LE author-ready check while a partial canonical definition exists at {partial_path}")
	with tempfile.TemporaryDirectory() as temporary:
		expected_root = Path(temporary)
		generate(expected_root)
		for relative_path in (
			Path("machines/author-ready/stern/x-men-limited-edition-2012.json"),
			Path("knowledge/stern/x-men-limited-edition-2012.md"),
		):
			actual_path = root / relative_path
			expected_path = expected_root / relative_path
			if not actual_path.is_file() or actual_path.read_bytes() != expected_path.read_bytes():
				raise RuntimeError(f"X-Men LE generated artifact drift: {relative_path.as_posix()}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="reconstruct and compare the canonical LE artifacts without writing")
	arguments = parser.parse_args()
	if arguments.check:
		check()
	else:
		generate()
