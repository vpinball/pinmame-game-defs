"""Promote Spider-Man Vault Edition with reviewed normalized spatial placements."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/spider-man-vault-edition-2016.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/spider-man-vault-edition-2016.json"
EXCERPT_ROOT = ROOT / "evidence/excerpts/stern.spider-man-vault-edition.2016"

TABLE_SOURCE = "vpx-table.spider-man-ve-2.2"
SCRIPT_SOURCE = "vpx.spider-man-ve-2.2"
MANUAL_SOURCE = "manual.spider-man-ve.500-55a0-01"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"

TABLE_SOURCE_RECORD = {
	"attribution": "Table recreation by Alessio; fixes by DjRobX and credited table contributors",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Spider-Man_VE_2.2.vpx (85,819,392 bytes); ROM smanve_101; verified and extracted with vpxtool git:v0.33.3; normalized gameitem geometry and collection membership reviewed against manual pages 14, 16, 18, 40-46, 55, and 64-66",
	"original_filename": "Spider-Man_VE_2.2.vpx",
	"rights": "NOASSERTION",
	"sha256": "b258efeecc3dcbffd7dae79c52fdd39bba8c9a82e918034f170ab75c90764f11",
	"uri": "local-evidence://stern/spider-man-vault-edition-2016/Spider-Man_VE_2.2.vpx",
}


def _manual_excerpts() -> list[dict[str, object]]:
	"""Return the retained, visually checked manual transcriptions for this machine."""
	entries = [
		("switch-locations", "excerpt.spider-man-ve.switch-locations", "PDF page 15, section 1.12 SWITCH LOCATIONS"),
		("lamp-locations", "excerpt.spider-man-ve.lamp-locations", "PDF page 17, section 1.13 LAMP LOCATIONS"),
		("coil-locations-bottom", "excerpt.spider-man-ve.coil-locations-bottom", "PDF page 19, section 1.14 COILS & FLASH LAMP LOCATIONS, underside view"),
		("coil-locations-top", "excerpt.spider-man-ve.coil-locations-top", "PDF page 19, section 1.14 COILS & FLASH LAMP LOCATIONS, upper-playfield/backbox view"),
		("coils-detailed-chart", "excerpt.spider-man-ve.coils-detailed-chart", "PDF page 52, COILS DETAILED CHART TABLE"),
		("gi-circuit-layout", "excerpt.spider-man-ve.gi-circuit-layout", "PDF page 55, PLAYFIELD WIRING, GI circuit layout"),
		("trough-opto-pcb", "excerpt.spider-man-ve.trough-opto-pcb", "PDF page 64, THROUGH UP-KICKER DUAL OPTO PCBS"),
		("trough-opto-led1", "excerpt.spider-man-ve.trough-opto-led1", "PDF page 65, OPTO TROUBLESHOOTING and LED1 alignment/test"),
		("trough-opto-led2", "excerpt.spider-man-ve.trough-opto-led2", "PDF page 66, LED2 alignment/test"),
	]
	result = []
	for stem, excerpt_id, locator in entries:
		markdown = EXCERPT_ROOT / f"{stem}.md"
		image = EXCERPT_ROOT / f"{stem}.webp"
		if not markdown.is_file() or not image.is_file():
			raise FileNotFoundError(f"Spider-Man VE excerpt is missing: {markdown} or {image}")
		result.append({
			"id": excerpt_id,
			"locator": locator,
			"path": str(markdown.relative_to(ROOT)).replace("\\", "/"),
			"sha256": hashlib.sha256(markdown.read_bytes()).hexdigest(),
			"image": str(image.relative_to(ROOT)).replace("\\", "/"),
			"image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
			"image_derivation": {
				"switch-locations": "SpiderMan_VE_web.pdf page 15, crop box 0.04,0.17,0.5,0.92, scanned page rendered at its native resolution (embedded image xref 263, 496px across 4.95in), rendered at 100 dpi, grayscale, 392x827 WebP quality 45",
				"lamp-locations": "SpiderMan_VE_web.pdf page 17, crop box 0.06,0.18,0.5,0.93, scanned page rendered at its native resolution (embedded image xref 308, 288px across 2.87in), rendered at 100 dpi, grayscale, 376x829 WebP quality 45",
				"coil-locations-bottom": "SpiderMan_VE_web.pdf page 19, crop box 0.05,0.18,0.52,0.93, scanned page rendered at its native resolution (embedded image xref 394, 558px across 5.57in), rendered at 100 dpi, grayscale, 401x827 WebP quality 45",
				"coil-locations-top": "SpiderMan_VE_web.pdf page 19, crop box 0.55,0.15,0.96,0.64, scanned page rendered at its native resolution (embedded image xref 396, 334px across 3.34in), rendered at 100 dpi, grayscale, 350x540 WebP quality 45",
				"coils-detailed-chart": "SpiderMan_VE_web.pdf page 52, crop box 0.04,0.03,0.97,0.95, born-digital page rendered for legibility (smallest type in region 5.2pt, targeting 11px glyphs), rendered at 98 dpi, capped to 1000px wide, grayscale, rotated 90 degrees counter-clockwise, 766x1001 WebP quality 40",
				"gi-circuit-layout": "SpiderMan_VE_web.pdf page 55, crop box 0.04,0.15,0.43,0.92, born-digital page rendered for legibility (smallest type in region 1.1pt, targeting 11px glyphs), rendered at 211 dpi, capped to 700px wide, grayscale, 701x1789 WebP quality 30",
				"trough-opto-pcb": "SpiderMan_VE_web.pdf page 64, crop box 0.04,0.08,0.96,0.94, born-digital page rendered for legibility (smallest type in region 2.8pt, targeting 11px glyphs), rendered at 115 dpi, capped to 900px wide, grayscale, 901x1090 WebP quality 45",
				"trough-opto-led1": "SpiderMan_VE_web.pdf page 65, crop box 0.04,0.08,0.96,0.94, born-digital page rendered for legibility (smallest type in region 4.8pt, targeting 11px glyphs), rendered at 102 dpi, capped to 800px wide, grayscale, 801x968 WebP quality 35",
				"trough-opto-led2": "SpiderMan_VE_web.pdf page 66, crop box 0.04,0.08,0.96,0.94, scanned page rendered at its native resolution (embedded image xref 1467, 701px across 7.00in), rendered at 100 dpi, grayscale, 784x948 WebP quality 45",
		}[stem],
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		})
	return result


INPUT_POSITIONS = {
	1: [(0.138028, 0.582658)], 2: [(0.140301, 0.557399)], 3: [(0.142894, 0.531917)],
	4: [(0.145811, 0.506891)], 5: [(0.148405, 0.481268)], 6: [(0.271422, 0.392656)],
	7: [(0.169544, 0.410954)], 8: [(0.063550, 0.155792)],
	9: [(0.442017, 0.318489)], 10: [(0.500630, 0.319680)], 11: [(0.558421, 0.320720)],
	12: [(0.421551, 0.216664)], 13: [(0.551265, 0.216422)], 14: [(0.095156, 0.613533)],
	18: [(0.560000, 0.940000)], 19: [(0.635000, 0.922000)], 20: [(0.710000, 0.904000)],
	21: [(0.785000, 0.886000)], 22: [(0.840000, 0.870000)],
	23: [(0.937040, 0.884368)], 24: [(0.060924, 0.762064)], 25: [(0.132222, 0.742553)],
	26: [(0.227998, 0.728366)], 27: [(0.675814, 0.728070)], 28: [(0.771928, 0.741430)],
	29: [(0.844407, 0.761170)], 30: [(0.630252, 0.161466)], 31: [(0.824842, 0.156619)],
	32: [(0.744748, 0.240898)], 33: [(0.627363, 0.087123)], 34: [(0.716255, 0.083570)],
	35: [(0.805804, 0.082270)], 36: [(0.796376, 0.283365)], 37: [(0.938813, 0.097289)],
	38: [(0.938813, 0.166083)], 39: [(0.788012, 0.539657)], 40: [(0.782694, 0.566182)],
	41: [(0.777048, 0.591548)], 42: [(0.493960, 0.202600)], 43: [(0.139673, 0.094164)],
	44: [(0.633403, 0.241608)], 45: [(0.940126, 0.189835)], 46: [(0.871586, 0.563593)],
	47: [(0.317752, 0.214657)], 48: [(0.050158, 0.287234)],
	49: [(0.501990, 0.312554)], 50: [(0.501990, 0.312554)],
	53: [(0.447596, 0.151773)], 54: [(0.447596, 0.151773)],
	57: [(0.743558, 0.313044)], 58: [(0.743558, 0.313044)], 59: [(0.493260, 0.121585)],
	63: [(0.755252, 0.349291)], 81: [(0.621301, 0.845924)], 83: [(0.289980, 0.846515)],
}

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "cabinet.flipper", 84: "cabinet.flipper",
	-7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 6): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.knocker",
	("physical.output.ticket", 33): "service.ticket",
	("physical.output.ticket", 34): "service.ticket",
	("physical.output.ticket", 35): "service.ticket",
}

SOLENOID_POSITIONS = {
	1: [(0.856749, 0.864243)], 2: [(0.937040, 0.884368)], 3: [(0.717991, 0.391437)],
	4: [(0.796376, 0.283365)], 5: [(0.743558, 0.313044)], 7: [(0.579549, 0.042961)],
	8: [(0.866752, 0.041624)], 9: [(0.630252, 0.161466)], 10: [(0.824842, 0.156619)],
	11: [(0.744748, 0.240898)], 12: [(0.493260, 0.121585)], 13: [(0.447596, 0.151773)],
	14: [(0.855358, 0.460841)], 15: [(0.289980, 0.846515)], 16: [(0.621301, 0.845924)],
	17: [(0.227998, 0.728366)], 18: [(0.675814, 0.728070)], 20: [(0.501990, 0.312554)],
	21: [(0.541627, 0.180524)], 22: [(0.352488, 0.059662)],
	23: [(0.609638, 0.203251), (0.357931, 0.135461)],
	25: [(0.296350, 0.039657), (0.148897, 0.066785)], 26: [(0.488905, 0.216992)],
	27: [(0.447596, 0.151773)],
	28: [(0.136924, 0.589677)],
	29: [(0.098214, 0.044681)], 30: [(0.877626, 0.041844)],
	31: [(0.630252, 0.161466), (0.824842, 0.156619), (0.744748, 0.240898)],
}

LAMP_POSITIONS = {
	3: [(0.452558, 0.852246)], 4: [(0.451212, 0.650561)], 5: [(0.515653, 0.676879)],
	6: [(0.592025, 0.695842)], 7: [(0.552382, 0.731333)], 8: [(0.542467, 0.770891)],
	9: [(0.451694, 0.765786)], 10: [(0.363356, 0.770118)], 11: [(0.350938, 0.731373)],
	12: [(0.312513, 0.695952)], 13: [(0.388754, 0.678063)], 14: [(0.452219, 0.716705)],
	15: [(0.876332, 0.343947)], 16: [(0.900048, 0.292532)], 17: [(0.208439, 0.474764)],
	18: [(0.205618, 0.502231)], 19: [(0.203777, 0.529201)], 20: [(0.201346, 0.556300)],
	21: [(0.198477, 0.583549)], 22: [(0.294624, 0.496885)], 23: [(0.292504, 0.529505)],
	24: [(0.289015, 0.561652)], 25: [(0.076723, 0.207137)], 26: [(0.094969, 0.259396)],
	27: [(0.120299, 0.310429)], 28: [(0.298872, 0.423733)], 29: [(0.397713, 0.422867)],
	30: [(0.413404, 0.476387)], 31: [(0.434224, 0.528320)], 32: [(0.193819, 0.439891)],
	33: [(0.566892, 0.455609)], 34: [(0.537628, 0.507835)], 35: [(0.510010, 0.560689)],
	36: [(0.675896, 0.455227)], 37: [(0.637005, 0.508614)], 38: [(0.611222, 0.542575)],
	39: [(0.586476, 0.575648)], 40: [(0.562058, 0.608564)], 41: [(0.058323, 0.686783)],
	42: [(0.135134, 0.674861)], 43: [(0.769902, 0.674848)], 44: [(0.848176, 0.686618)],
	45: [(0.392921, 0.378880)], 46: [(0.466413, 0.398428)], 47: [(0.539203, 0.417992)],
	48: [(0.709719, 0.557570)], 49: [(0.442551, 0.254368)], 50: [(0.493037, 0.219736)],
	51: [(0.542631, 0.254483)], 52: [(0.444246, 0.350064)], 53: [(0.497965, 0.350960)],
	54: [(0.554385, 0.352148)], 57: [(0.633021, 0.048447)], 58: [(0.721716, 0.045133)],
	59: [(0.809527, 0.042058)], 60: [(0.630515, 0.161348)], 61: [(0.825893, 0.156856)],
	62: [(0.742910, 0.241726)], 63: [(0.703425, 0.584499)], 64: [(0.697127, 0.611798)],
	65: [(0.321550, 0.457836)],
	66: [(0.245206, 0.000000)], 67: [(0.245206, 0.000000)], 68: [(0.244652, 0.000000)],
	69: [(0.590365, 0.000000)], 70: [(0.590365, 0.000000)], 71: [(0.589259, 0.000000)],
	72: [(0.873729, 0.506938)], 74: [(0.419687, 0.232565)], 75: [(0.246717, 0.252778)],
	76: [(0.172138, 0.669090)], 77: [(0.855830, 0.418203)], 78: [(0.919889, 0.238910)],
}

# Measured from the color-coded physical bulb markers on manual page 55. The
# playfield drawing was normalized against its x=154..582 and y=343..1307 pixel
# outline, with y reversed because the underside drawing has the rear/top edge at
# its bottom. The separately captioned rear-panel drawing is a rear view, so its
# measured x positions are mirrored into player view and projected to y=0.
# The two coin-door bulbs are cabinet hardware and remain quantity-only metadata.
GI_POSITIONS: list[tuple[str, float, float]] = [
	("brown.01", 0.220561, 0.818672), ("brown.02", 0.153738, 0.798963),
	("brown.03", 0.209346, 0.752905), ("brown.04", 0.184346, 0.722822),
	("brown.05", 0.044159, 0.608817), ("brown.06", 0.053738, 0.547095),
	("brown.07", 0.107944, 0.459544), ("brown.08", 0.230374, 0.366494),
	("yellow.01", 0.693692, 0.823755), ("yellow.02", 0.759112, 0.805083),
	("yellow.03", 0.699533, 0.754772), ("yellow.04", 0.726402, 0.723133),
	("yellow.05", 0.833879, 0.564419), ("yellow.06", 0.689252, 0.268672),
	("yellow.07", 0.656542, 0.221992), ("yellow.08", 0.684346, 0.085166),
	("yellow.09", 0.592056, 0.082573), ("yellow.10", 0.766355, 0.080913),
	("yellow.11", 0.845561, 0.077905),
	("violet.01", 0.050000, 0.338589), ("violet.02", 0.044159, 0.275311),
	("violet.03", 0.178738, 0.249378), ("violet.04", 0.248131, 0.251245),
	("violet.05", 0.377103, 0.207573), ("violet.06", 0.228738, 0.200622),
	("violet.07", 0.150000, 0.181535), ("violet.08", 0.367523, 0.156846),
	("violet.09", 0.215421, 0.149689), ("violet.10", 0.061215, 0.039938),
	("violet.11", 0.226636, 0.023029), ("violet.12", 0.378738, 0.017946),
	("violet.13", 0.478972, 0.016909),
	("green.01", 0.090187, 0.000000), ("green.02", 0.181075, 0.000000),
	("green.03", 0.272430, 0.000000), ("green.04", 0.363551, 0.000000),
	("green.05", 0.455140, 0.000000), ("green.06", 0.542056, 0.000000),
	("green.07", 0.632243, 0.000000), ("green.08", 0.724533, 0.000000),
	("green.09", 0.815888, 0.000000), ("green.10", 0.907009, 0.000000),
]


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


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply a reviewed disposition to every input and output, failing closed."""
	located_sources = (TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], located_sources)
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Spider-Man VE input {group} {address} has no reviewed spatial disposition")

		if group == "pinmame.input.switch" and address in {18, 19, 20, 21, 22}:
			device.setdefault("physical", {})["location"] = "Under-apron four-ball trough assembly 500-6318-24-ND"
		if group == "pinmame.input.switch" and address in {49, 50}:
			device.setdefault("physical", {})["location"] = "Motorized Sandman three-bank assembly 500-7056-01 / 500-7057-01"
		if group == "pinmame.input.switch" and address in {53, 54}:
			device.setdefault("physical", {})["location"] = "Sandman moving-gate assembly 500-7061-00"
		if group == "pinmame.input.switch" and address in {57, 58}:
			device.setdefault("physical", {})["location"] = "Doc Ock moving-gate assembly 500-7061-00"

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if group == "pinmame.output.solenoid" and address == 19:
			device["id"] = "output.green-goblin-shake"
			device["label"] = "Green Goblin shake coil"
			device["availability"] = "used"
			physical = device.setdefault("physical", {})
			physical["location"] = "Green Goblin toy mount 511-5302-05"
			physical["notes"] = "The physical VE manual installs and wires this Q19 coil. The known-working VPX leaves SolCallback(19) disabled, so its digital toy animation is intentionally incomplete evidence rather than proof that the physical output is unused."
			_located(device, "effect", [(0.136924, 0.589677)], (TABLE_SOURCE, MANUAL_SOURCE))
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif group == "pinmame.output.lamp" and address in {1, 2}:
			device["roles"] = [{1: "cabinet.start", 2: "cabinet.tournament"}[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], located_sources)
			physical = device.setdefault("physical", {})
			if address == 5:
				physical.setdefault("location", "Doc Ock moving-gate assembly 500-7061-00")
			elif address == 13:
				physical.setdefault("location", "Sandman moving-gate assembly 500-7061-00")
			elif address == 20:
				physical.setdefault("location", "Motorized Sandman three-bank assembly 500-7056-01 / 500-7057-01")
			elif address == 27:
				physical.setdefault("location", "Sandman dome on the upper playfield assembly")
				physical.setdefault("notes", "The broad VPX FlashGiallo helper is outside the canonical table bounds; the physical LED is placed at the manual-defined Sandman dome assembly.")
			elif address == 28:
				physical.setdefault("location", "Green Goblin toy mount 511-5302-05")
				physical["notes"] = "Two 113-5034-08 LED flashers are installed inside the single drilled Green Goblin toy. The normalized point locates that shared three-dimensional assembly; the manual does not expose separate playfield-plane coordinates, and the working VPX combines their light into one broad FlasherGoblin overlay."
			elif address in {29, 30}:
				physical.setdefault("location", "Rear back-panel flasher assembly")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], located_sources)
			device.setdefault("physical", {}).setdefault("quantity", 1)
			if address in range(66, 72):
				device["physical"].setdefault("location", "Rear back panel; projected onto the y=0 boundary")
		elif group == "pinmame.output.gi" and address == 0:
			expected_circuits = {"brown": 8, "yellow": 11, "violet": 13, "green": 10}
			actual_circuits = {
				circuit: sum(suffix.startswith(f"{circuit}.") for suffix, _, _ in GI_POSITIONS)
				for circuit in expected_circuits
			}
			if actual_circuits != expected_circuits or len(GI_POSITIONS) != 42:
				raise ValueError(f"Spider-Man VE GI circuit reconciliation mismatch: {actual_circuits!r}")
			_located(device, "emitter", GI_POSITIONS, (MANUAL_SOURCE,))
			device.setdefault("physical", {}).update({
				"quantity": 44,
				"location": "32 playfield bulbs, 10 rear back-panel bulbs, and 2 coin-door bulbs on four fused GI circuits",
				"notes": "The 32 playfield placements are measured from the circuit-colored bulb markers in the manual page-55 underside diagram, normalized in player view. The manual's circuit-4 prose says upper right, but its violet markers are on the upper left; the plotted physical markers are used because the brown/yellow marker regions independently validate the diagram orientation. The 10 individually measured rear-panel markers come from a separately captioned rear view, so x is mirrored into player view before projection to y=0. Two additional green/white-circuit bulbs are inside/on the coin door and intentionally have no playfield coordinate.",
			})
		else:
			raise ValueError(f"Spider-Man VE output {group} {address} ({kind}) has no reviewed spatial disposition")


def promote() -> None:
	input_path = PARTIAL_PATH if PARTIAL_PATH.exists() else AUTHOR_READY_PATH
	definition = load_json(input_path)
	if not any(source["id"] == TABLE_SOURCE for source in definition["sources"]):
		definition["sources"].append(TABLE_SOURCE_RECORD)
	manual_source = next(source for source in definition["sources"] if source["id"] == MANUAL_SOURCE)
	manual_source["excerpts"] = _manual_excerpts()
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	for display in definition["displays"]:
		display["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, MANUAL_SOURCE]}}
	write_json(AUTHOR_READY_PATH, definition)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
