"""Promote Star Trek Pro with reviewed normalized spatial placements."""

from __future__ import annotations

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import write_json, write_text

from curate_star_trek import CORE_SOURCE, PRO_KNOWLEDGE, PRO_MANUAL, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, build_pro


PARTIAL_PATH = ROOT / "machines/partial/stern/star-trek-pro-2013.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/star-trek-pro-2013.json"

ENTERPRISE_TABLE_SOURCE = "vpx-table.star-trek-enterprise-le-geometry"
ENTERPRISE_TABLE_SOURCE_RECORD = {
	"attribution": "The table authors credited by the table distribution",
	"id": ENTERPRISE_TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Star Trek Enterprise Limited Edition (Stern 2012).vpx (66,732,032 bytes), exact st_161hc table extracted with vpxtool git:v0.33.3. Used only for hidden trough-ball geometry: its drain is switch 18 and its four ball positions are switches 19-22, which are translated and mapped in order to physical Pro switches 18-21 by aligning the table's switch-22 trough-out with Pro BallRelease; no coordinate from its normalized frame is copied directly.",
	"original_filename": "Star Trek Enterprise Limited Edition (Stern 2012).vpx",
	"rights": "NOASSERTION",
	"sha256": "46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e",
	"uri": "external:pinmame-vpx-sources/stern/star-trek-premium-limited-edition-2013/source/Star Trek Enterprise Limited Edition (Stern 2012).vpx",
}

INPUT_POSITIONS = {
	1: [(0.578782, 0.138478)], 2: [(0.671218, 0.138478)], 4: [(0.757878, 0.144565)],
	7: [(0.788121, 0.605974)], 8: [(0.798888, 0.631463)], 9: [(0.808342, 0.657495)],
	10: [(0.102416, 0.482826)], 11: [(0.516468, 0.312082)], 12: [(0.229517, 0.531196)],
	13: [(0.134454, 0.305924)], 14: [(0.319853, 0.235272)],
	18: [(0.703727, 0.946296)], 19: [(0.749432, 0.933741)], 20: [(0.796670, 0.921846)],
	21: [(0.849790, 0.906658)], 22: [(0.895000, 0.908000)], 23: [(0.939863, 0.909891)],
	24: [(0.077731, 0.806522)], 25: [(0.149160, 0.790435)],
	26: [(0.242986, 0.774518)], 27: [(0.682742, 0.775298)],
	28: [(0.775998, 0.790978)], 29: [(0.851891, 0.809348)],
	30: [(0.581736, 0.214458)], 31: [(0.799698, 0.219893)], 32: [(0.675748, 0.290545)],
	33: [(0.500525, 0.297554)], 34: [(0.490021, 0.258207)],
	35: [(0.001576, 0.335054)], 36: [(0.202206, 0.062663)],
	37: [(0.808298, 0.239620)], 38: [(0.941702, 0.202228)],
	39: [(0.289259, 0.452677)], 40: [(0.293899, 0.478655)], 41: [(0.298363, 0.504959)],
	42: [(0.094844, 0.621680)], 43: [(0.090117, 0.648093)], 44: [(0.868172, 0.617935)],
	45: [(0.181548, 0.575738)], 46: [(0.298100, 0.347061)], 47: [(0.444547, 0.332966)],
	48: [(0.625131, 0.324235)], 49: [(0.633885, 0.413329)], 50: [(0.774991, 0.428872)],
	51: [(0.896534, 0.148261)], 52: [(0.067227, 0.236522)],
	81: [(0.621586, 0.888587)], 83: [(0.305935, 0.888587)],
}

SOLENOID_POSITIONS = {
	1: [(0.849790, 0.906658)], 2: [(0.938813, 0.911467)], 3: [(0.498950, 0.261848)],
	4: [(0.516468, 0.312082)], 5: [(0.516468, 0.312082)], 6: [(0.102416, 0.482826)],
	7: [(0.490809, 0.234511)], 9: [(0.581736, 0.214458)], 10: [(0.799698, 0.219893)],
	11: [(0.675748, 0.290545)], 12: [(0.850839, 0.517146)],
	13: [(0.242986, 0.774518)], 14: [(0.682742, 0.775298)],
	15: [(0.305935, 0.888587)], 16: [(0.621586, 0.888587)],
	17: [(0.248844, 0.277954)], 18: [(0.831574, 0.252564)],
	19: [(0.033482, 0.095380)], 20: [(0.756171, 0.117120)], 21: [(0.501536, 0.246117)],
	22: [(0.200000, 0.960000)], 23: [(0.335535, 0.238322)], 25: [(0.691504, 0.220796)],
	26: [(0.186737, 0.343828)], 27: [(0.265665, 0.463793)], 28: [(0.769132, 0.327344)],
	29: [(0.233390, 0.533342)], 30: [(0.876356, 0.480302)], 31: [(0.504202, 0.216957)],
	32: [(0.221113, 0.715870)],
}

MANUAL_PROJECTED_SOLENOIDS = {17, 18, 21, 22, 23, 25, 26, 27, 28, 30}

LAMP_POSITIONS = {
	4: (0.074711, 0.743166), 5: (0.148766, 0.726753), 7: (0.774028, 0.727296), 8: (0.850184, 0.746535),
	9: (0.460872, 0.736671), 10: (0.517069, 0.779280), 11: (0.573792, 0.821889), 12: (0.465074, 0.864063),
	13: (0.465993, 0.916101), 14: (0.355305, 0.821889), 15: (0.407826, 0.779280), 16: (0.464548, 0.821889),
	17: (0.460084, 0.698111), 18: (0.460084, 0.670285), 19: (0.460084, 0.643111), 20: (0.458246, 0.615285),
	21: (0.457195, 0.586264), 22: (0.456145, 0.558111), 23: (0.455095, 0.530285), 24: (0.454307, 0.502242),
	25: (0.210084, 0.653302), 26: (0.274947, 0.586128), 27: (0.820903, 0.458519),
	28: (0.683036, 0.449063), 29: (0.381828, 0.367106), 30: (0.518120, 0.363519),
	32: (0.269301, 0.698274), 33: (0.210084, 0.653302), 34: (0.274947, 0.586128),
	35: (0.820903, 0.458519), 36: (0.683036, 0.449063), 37: (0.381828, 0.367106),
	38: (0.518120, 0.363519), 40: (0.142069, 0.652133), 41: (0.210084, 0.653302),
	42: (0.274947, 0.586128), 43: (0.820903, 0.458519), 44: (0.683036, 0.449063),
	45: (0.381828, 0.367106), 46: (0.518120, 0.363519), 48: (0.146534, 0.623655),
	49: (0.319722, 0.636209), 50: (0.205095, 0.592894), 51: (0.135373, 0.585557),
	52: (0.106749, 0.536861), 53: (0.353466, 0.504633), 54: (0.346376, 0.477894),
	55: (0.341649, 0.452459), 56: (0.400604, 0.419796), 57: (0.326418, 0.355068),
	59: (0.446691, 0.353764), 60: (0.605436, 0.357948), 61: (0.589023, 0.393655),
	62: (0.531907, 0.415992), 63: (0.536371, 0.463600), 64: (0.543724, 0.511209),
	65: (0.577468, 0.100503), 66: (0.668592, 0.100503), 67: (0.757090, 0.106590),
	68: (0.620273, 0.433764), 69: (0.761029, 0.448872), 70: (0.658745, 0.501100),
	71: (0.783219, 0.507622), 72: (0.705751, 0.569905), 73: (0.638130, 0.586481),
	74: (0.738445, 0.610394), 75: (0.746849, 0.636372), 76: (0.756828, 0.662459),
	80: (0.919380, 0.583859),
}

GI_POSITIONS = [
	("newlighttest76", 0.767069, 0.841522), ("newlighttest77", 0.224790, 0.802391),
	("newlighttest78", 0.725840, 0.766957), ("newlighttest79", 0.702731, 0.803261),
	("newlighttest80", 0.037815, 0.631739), ("newlighttest81", 0.161239, 0.841522),
	("newlighttest82", 0.233718, 0.865652), ("newlighttest83", 0.694590, 0.865652),
	("newlighttest84", 0.538340, 0.136957), ("newlighttest85", 0.625525, 0.136522),
	("newlighttest86", 0.716387, 0.140652), ("newlighttest87", 0.807637, 0.154783),
	("newlighttest88", 0.827731, 0.611413), ("newlighttest89", 0.242122, 0.431957),
	("newlighttest90", 0.201681, 0.766087), ("gilight1", 0.850315, 0.516359),
	("gilight113", 0.305410, 0.887772), ("gilight114", 0.622111, 0.888207),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth",
	71: "cabinet.action", 82: "flipper.lower-right.button", 84: "flipper.lower-left.button", 86: "flipper.upper-right.button",
}

DIRECT_PRO_SOURCES = (PRO_MANUAL, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)
REGISTERED_TROUGH_SOURCES = (*DIRECT_PRO_SOURCES, ENTERPRISE_TABLE_SOURCE)


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], source_refs: tuple[str, ...]) -> None:
	if len(positions) != 1:
		raise ValueError(f"Star Trek Pro reviewed placement must contain exactly one point: {device['id']}")
	x, y = positions[0]
	device["spatial"] = {
		"status": "validated",
		"placements": [{"id": f"{device['id']}.{role}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)}],
	}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def _located_gi(device: dict[str, object]) -> None:
	device["spatial"] = {
		"status": "validated",
		"placements": [
			{"id": f"{device['id']}.emitter.{name}", "role": "emitter", "space": "playfield", "x": x, "y": y, "provenance": _provenance(PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)}
			for name, x, y in GI_POSITIONS
		],
	}
	_append_note(device, "The known-working Pro table drives these exact 18 GILighting objects, so their centers preserve its authoring-light design. This is not a manual-verified physical socket inventory: newlighttest76-newlighttest90 are table GI references, while gilight1, gilight113, and gilight114 illuminate flipper-pivot regions and may be render abstractions rather than one-for-one sockets. Do not infer 18 physical bulbs. GI_Light and GI_LightOff are aggregate overlays; BloomLights, flashers, and the LE-only page-150 41-emitter GI drawing are excluded.")


def apply_spatial(definition: dict[str, object]) -> None:
	if any("spatial" in device for collection in (definition["inputs"], definition["outputs"]) for device in collection):
		raise ValueError("Star Trek Pro spatial curation requires an unspatialized base definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PRO_MANUAL)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL)
		elif address in INPUT_POSITIONS:
			sources = REGISTERED_TROUGH_SOURCES if address in {18, 19, 20, 21} else DIRECT_PRO_SOURCES
			_located(device, "sensor", INPUT_POSITIONS[address], sources)
			if address in {18, 19, 20, 21}:
				_append_note(device, "The manual proves the physical four-position trough order but groups switches 18-22 spatially. The older table's switch 18 is its drain, not a Pro trough position; its four ball positions 19-22 are translated into the canonical Pro frame and mapped in order to Pro switches 18-21 by aligning its switch-22 trough-out with Pro BallRelease at (0.849790, 0.906658).")
			elif address == 22:
				_append_note(device, "The manual requires the downstream trough-jam opto, but the exact Pro table does not model switch 22. This is an approximate regional marker on the short ejection corridor between Pro BallRelease and shooter-lane switch 23, not an exact sensor center; practical uncertainty is about plus or minus 0.045 normalized x and 0.02 normalized y.")
			elif address in {26, 27}:
				_append_note(device, "The sensor is implicit in the exact Pro slingshot collision-wall footprint; this assembly centroid has practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address in {81, 83}:
				_append_note(device, "The normally-closed EOS contact is implicit in the exact lower-flipper assembly; its flipper-center projection has practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		else:
			raise ValueError(f"Star Trek Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL)
		elif group == "pinmame.output.solenoid" and address in {8, 24}:
			device.setdefault("roles", ["cabinet.shaker" if address == 8 else "cabinet.coin-meter"])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			sources = (PRO_MANUAL,) if address in MANUAL_PROJECTED_SOLENOIDS else DIRECT_PRO_SOURCES
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], sources)
			device.setdefault("physical", {})["quantity"] = 1
			if address in {4, 5}:
				_append_note(device, "Outputs 4 and 5 move one physical memory-target assembly and intentionally share its exact Pro center; output 3 remains the adjacent magnet assembly.")
			elif address in {13, 14}:
				_append_note(device, "This is the exact slingshot wall centroid used as the coil assembly projection, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address in MANUAL_PROJECTED_SOLENOIDS and address != 22:
				_append_note(device, "The shared Pro/LE coil-location drawing on manual PDF page 74 establishes this physical point. Its coordinate is a calibrated drawing projection into the 952 by 2300 Pro frame, not a claim of sub-object precision; practical uncertainty is about plus or minus 0.04 normalized x and y.")
			if address == 22:
				_append_note(device, "The physical laser motor is beneath the lower-left apron. Page 74 supports only this approximate regional marker in the canonical frame, not a calibrated point; practical uncertainty is about plus or minus 0.08 normalized x and 0.04 normalized y. Full-table Laser render fields are effects and are excluded.")
			elif address == 25:
				_append_note(device, "Page 74 shows one Q25 pop-bumper flasher point between the three pop assemblies, so quantity is one rather than one emitter per bumper.")
			elif address in {19, 20, 29}:
				_append_note(device, "The proven Pro script establishes this physical flasher semantic and the corresponding exact Pro f119a/f120a/f129a object center supplies geometry; broad glow helpers are excluded.")
			elif address == 31:
				_append_note(device, "The proven Pro callback drives VengFlashGI for output 31. Its exact light center supplies this parent-relative rest-state ship-flasher point; decorative ship and bloom geometry are excluded.")
		elif group == "pinmame.output.lamp" and address == 3:
			device.setdefault("roles", ["cabinet.lighting"])
			device.setdefault("physical", {})["quantity"] = 1
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", [LAMP_POSITIONS[address]], DIRECT_PRO_SOURCES)
			device.setdefault("physical", {})["quantity"] = 1
			if kind == "rgb_lamp":
				_append_note(device, "This controller record is one color channel of a single physical RGB insert; all three channel records intentionally share one placement and must not be recreated as separate modules.")
			elif address == 80:
				_append_note(device, "The exact l80 object is the physical blue spotlight center. The overlapping f80 halo is a render helper and is excluded from physical quantity and placement.")
		elif group == "pinmame.output.gi" and address == 0:
			_located_gi(device)
		else:
			raise ValueError(f"Star Trek Pro output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Star Trek Pro knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PRO_KNOWLEDGE,
	"Coverage: **author-ready - physical inventory, public PinMAME bindings, lamp semantics, mechanisms, and edition differences validated**",
	"Coverage: **author-ready - physical inventory, public PinMAME bindings, lamp semantics, mechanisms, edition differences, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"Exact VPX playfield coordinates were observed during curation but have not yet been normalized and promoted into the definition.",
	"Every used playfield lamp has a normalized placement from the exact Pro table; the six RGB emblems intentionally co-locate their three controller channels at one physical module.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Center target, lock, and Vengeance\n",
	"## Spatial coordinate model\n\nEvery playfield input, actuator, flasher, lamp, and table-authored GI reference emitter uses player-view normalized coordinates: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. The exact 952 by 2300 working Pro table is the sole coordinate frame. Its script remains controller-causality ground truth, while the official manual establishes physical inventory. Manual pages 67 and 71 are explicitly LE/Premium switch/lamp drawings, pages 68-70 are Premium/LE RGB material, and page 150 is explicitly LE GI; none is used as Pro physical-location evidence. Page 74 is the shared main Q-output map and supplies drawing projections for outputs without defensible physical VPX objects; the below-apron Q22 laser coordinate is explicitly regional rather than calibrated.\n\nThe hidden trough switches 18-21 are the only geometry imported from another table. That table's switch 18 is its drain; its four ball positions 19-22 are translated into the Pro frame and mapped in order to Pro 18-21 by aligning its switch-22 trough-out with Pro BallRelease. The manual-required Pro jam opto 22 is absent from the exact Pro table and therefore receives a disclosed approximate marker between BallRelease and shooter-lane switch 23. Slingshot sensors/coils and lower-flipper EOS contacts use disclosed assembly projections. Cabinet, service, DIP, unused, optional cabinet hardware, and virtual devices never receive fake playfield points.\n\nPro GI is deliberately not the Premium/LE 41-emitter inventory. The known-working Pro table drives exactly 18 objects in its `GILighting` collection, and those centers preserve the table's authoring-light design. They are not a manual-verified count of physical sockets: three `gilight` objects illuminate flipper-pivot regions and may be render abstractions. Aggregate `GI_Light`/`GI_LightOff`, bloom objects, flashers, and the LE-only manual page-150 drawing are excluded. Manual page 74 likewise proves Q25 is one physical pop-bumper flasher point rather than three.\n\n## Center target, lock, and Vengeance\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `runtime.star-trek-pro.boot-start`: exact `st_161c` LibPinMAME run",
	"- `vpx-table.star-trek-enterprise-le-geometry`: exact `Star Trek Enterprise Limited Edition (Stern 2012).vpx`, SHA-256 `46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e`; used only to recover the hidden trough chain by local registration to the shared Pro trough-out anchor.\n- `runtime.star-trek-pro.boot-start`: exact `st_161c` LibPinMAME run",
)


def promote() -> None:
	definition = build_pro()
	definition["sources"].append(ENTERPRISE_TABLE_SOURCE_RECORD)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/star-trek-pro-2013.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
