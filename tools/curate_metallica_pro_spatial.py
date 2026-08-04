"""Promote Metallica Pro with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import write_json, write_text

from curate_metallica import MANUAL_SOURCE, PRO_KNOWLEDGE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, build_pro


PARTIAL_PATH = ROOT / "machines/partial/stern/metallica-pro-2013.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/metallica-pro-2013.json"

DIRECT_SOURCES = (MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)

INPUT_POSITIONS = {
	1: [(0.192622, 0.706385)], 3: [(0.058042, 0.485628)], 4: [(0.061027, 0.395224)],
	7: [(0.125398, 0.493647)], 9: [(0.125398, 0.461457)],
	18: [(0.569000, 0.942000)], 19: [(0.673000, 0.911000)],
	20: [(0.777000, 0.880000)], 21: [(0.880999, 0.848817)],
	22: [(0.912000, 0.866000)], 23: [(0.943795, 0.882111)],
	24: [(0.056944, 0.745679)], 25: [(0.126209, 0.706625)],
	26: [(0.285308, 0.719582)], 27: [(0.700483, 0.718992)],
	28: [(0.794538, 0.719753)], 29: [(0.877994, 0.751659)],
	30: [(0.606898, 0.134432)], 31: [(0.834438, 0.162904)], 32: [(0.663003, 0.227110)],
	35: [(0.451658, 0.126653)], 36: [(0.180727, 0.331676)], 37: [(0.300979, 0.319332)],
	40: [(0.670013, 0.377491)], 41: [(0.799694, 0.387416)], 42: [(0.562600, 0.291522)],
	43: [(0.086134, 0.110087)], 44: [(0.705021, 0.090748)], 45: [(0.792619, 0.096228)],
	46: [(0.913485, 0.087972)], 47: [(0.595942, 0.138131)], 50: [(0.057566, 0.156594)],
	51: [(0.819515, 0.566214)], 52: [(0.144206, 0.215798)], 53: [(0.452005, 0.147618)],
	54: [(0.655057, 0.311576)], 60: [(0.245216, 0.334421)], 61: [(0.227346, 0.302730)],
	62: [(0.207345, 0.271382)], 81: [(0.661138, 0.827442)], 83: [(0.327191, 0.827442)],
}

SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.880999, 0.848817)], 2: [(0.943795, 0.882111)],
	3: [(0.185704, 0.230417)], 4: [(0.449163, 0.232118)],
	5: [(0.655057, 0.311576)], 6: [(0.861799, 0.532281)], 7: [(0.543838, 0.032898)],
	9: [(0.606898, 0.134432)], 10: [(0.834438, 0.162904)], 11: [(0.663003, 0.227110)],
	12: [(0.226638, 0.302844)], 13: [(0.285308, 0.719582)], 14: [(0.700483, 0.718992)],
	15: [(0.327191, 0.827442)], 16: [(0.661138, 0.827442)], 18: [(0.453048, 0.068002)],
	19: [(0.157826, 0.181397)], 20: [(0.655057, 0.311576)], 23: [(0.316735, 0.213299)],
	25: [(0.709144, 0.174457)], 26: [(0.149081, 0.137218), (0.187283, 0.121217)],
	27: [(0.382952, 0.100703), (0.514331, 0.103164)],
	28: [(0.277645, 0.183622), (0.540323, 0.227521)], 29: [(0.743026, 0.371360)],
	30: [(0.566351, 0.298320)], 31: [(0.477140, 0.439421), (0.499807, 0.463906)],
	32: [(0.452660, 0.291458)],
}

FLASHER_QUANTITIES = {19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 25: 1, 26: 2, 27: 2, 28: 2, 29: 1, 30: 1, 31: 2, 32: 1}

LAMP_POSITIONS = {
	4: [(0.521718, 0.875450), (0.467148, 0.875275)], 5: [(0.419984, 0.808515)],
	6: [(0.469123, 0.808516)], 7: [(0.518865, 0.808423)], 8: [(0.568191, 0.808516)],
	9: [(0.607377, 0.767861)], 10: [(0.536961, 0.767861)],
	11: [(0.466000, 0.767861)], 12: [(0.378275, 0.738007)],
	13: [(0.380298, 0.692141)], 14: [(0.435614, 0.685521)], 15: [(0.493117, 0.683329)],
	16: [(0.550414, 0.685356)], 17: [(0.605973, 0.692180)], 18: [(0.056188, 0.695430)],
	19: [(0.125658, 0.662782)], 20: [(0.191980, 0.657847)], 21: [(0.144827, 0.609336)],
	22: [(0.196474, 0.604735)], 23: [(0.217678, 0.583327)], 24: [(0.140313, 0.574201)],
	25: [(0.872838, 0.677647)], 26: [(0.789322, 0.653130)],
	27: [(0.795649, 0.594801), (0.741847, 0.579357)], 29: [(0.761745, 0.521721)],
	30: [(0.637837, 0.524199)], 31: [(0.637197, 0.490049)],
	32: [(0.758248, 0.486786)], 33: [(0.814055, 0.448501)],
	34: [(0.689641, 0.449351)], 35: [(0.767078, 0.423779)], 36: [(0.843447, 0.401964)],
	37: [(0.719523, 0.404905)], 38: [(0.654207, 0.406774)], 40: [(0.338482, 0.498186)],
	41: [(0.342713, 0.463963)], 42: [(0.216232, 0.524721)],
	43: [(0.216814, 0.502501)], 44: [(0.218850, 0.480345)], 45: [(0.219868, 0.458125)],
	46: [(0.295957, 0.423065)], 47: [(0.172632, 0.412660)],
	48: [(0.173198, 0.378365)], 49: [(0.208365, 0.360898)],
	50: [(0.269373, 0.376841)], 51: [(0.305875, 0.349507)], 52: [(0.388962, 0.382303)],
	53: [(0.398406, 0.348492)], 54: [(0.357244, 0.304615)],
	55: [(0.335446, 0.259271)], 56: [(0.453368, 0.300659)], 57: [(0.122413, 0.337619)],
	58: [(0.091846, 0.292417)], 60: [(0.605796, 0.134046)],
	61: [(0.833528, 0.163147)], 62: [(0.663593, 0.227011)], 63: [(0.700288, 0.134540)],
	64: [(0.755111, 0.133865)], 65: [(0.675381, 0.281633)], 67: [(0.481339, 0.477447)],
	68: [(0.493948, 0.450955)], 69: [(0.494849, 0.430687)],
	70: [(0.832678, 0.536147)], 71: [(0.854755, 0.542141)], 73: [(0.405409, 0.169696)],
	75: [(0.450550, 0.158693)], 78: [(0.495557, 0.169874)],
}

LAMP_COLLAPSE_NOTES = {
	9: "The exact table also has a render-helper at (0.590614, 0.738007). The retained anchor is the closer approximation to the single manual socket (about 11 px residual in the fitted manual frame); the physical center remains approximate.",
	10: "The exact table also has a render-helper at (0.520199, 0.738007). The retained anchor is the closer approximation to the single manual socket (about 11 px residual in the fitted manual frame); the physical center remains approximate.",
	11: "The exact table also has a render-helper at (0.449237, 0.738007). The retained anchor is the closer approximation to the single manual socket (about 13 px residual in the fitted manual frame); the physical center remains approximate.",
	12: "The exact table also has a render-helper at (0.395038, 0.767861). The two candidates are effectively tied against the single manual socket (about 20-22 px residual in the fitted manual frame); the retained physical center is approximate.",
	31: "The exact table also has a render-helper at (0.681305, 0.496421). The retained anchor is the closer approximation to the single manual socket (about 13 px residual in the fitted manual frame); the physical center remains approximate.",
	32: "The exact table also has a render-helper at (0.804273, 0.493312). The retained anchor is the closer approximation to the single manual socket (about 3 px residual in the fitted manual frame); the physical center remains approximate.",
	41: "The exact table also has a render-helper at (0.299123, 0.469031). The retained anchor is the closer approximation to the single manual socket (about 15 px residual in the fitted manual frame); the physical center remains approximate.",
	48: "The exact table also has a render-helper at (0.129117, 0.384794). The retained anchor is the closer approximation to the single manual socket (about 14 px residual in the fitted manual frame); the physical center remains approximate.",
	53: "The exact table also has a render-helper at (0.352244, 0.352590). The retained anchor is the closer approximation to the single manual socket (about 9 px residual in the fitted manual frame); the physical center remains approximate.",
	60: "The exact table also has a nearly coincident low-intensity glow helper at (0.605796, 0.138894). The retained high-intensity bumper-light center is an approximate physical anchor.",
	61: "The exact table also has a nearly coincident low-intensity glow helper at (0.833528, 0.167994). The retained high-intensity bumper-light center is an approximate physical anchor.",
	62: "The exact table also has a nearly coincident low-intensity glow helper at (0.663593, 0.231858). The retained high-intensity bumper-light center is an approximate physical anchor.",
	70: "The exact table also has a render-helper at (0.784896, 0.560651) on the ramp artwork. The retained anchor matches the single round feature beside the manual leader line; the physical center remains approximate.",
	71: "The exact table also has a render-helper at (0.816798, 0.569438) on the ramp artwork. The retained anchor matches the single round feature beside the manual leader line; the physical center remains approximate.",
}

GI_POSITIONS: list[tuple[str, float, float]] = [
	("vpx.gi001", 0.155263, 0.773626), ("vpx.gi002", 0.890853, 0.619416),
	("vpx.gi003", 0.241164, 0.798294), ("vpx.gi004", 0.736578, 0.806712),
	("vpx.gi005", 0.877738, 0.578412), ("vpx.gi006", 0.798825, 0.785881),
	("vpx.gi007", 0.269725, 0.749700), ("vpx.gi008", 0.704210, 0.752989),
	("vpx.gi009", 0.236111, 0.709682), ("vpx.gi010", 0.750272, 0.710231),
	("vpx.gi011", 0.030480, 0.639774), ("vpx.gi012", 0.038350, 0.293697),
	("vpx.gi013", 0.029825, 0.600936), ("vpx.gi014", 0.282297, 0.278682),
	("vpx.gi015", 0.267870, 0.250961), ("vpx.gi016", 0.876426, 0.196097),
	("vpx.gi017", 0.131469, 0.120442), ("vpx.gi018", 0.185243, 0.093876),
	("vpx.gi019", 0.940692, 0.060958), ("vpx.gi020", 0.869869, 0.026307),
	("vpx.gi021", 0.056711, 0.071353), ("vpx.gi022", 0.138027, 0.042477),
	("vpx.gi023", 0.838392, 0.099652), ("vpx.gi024", 0.753141, 0.081171),
	("vpx.gi025", 0.662645, 0.087524), ("vpx.gi026", 0.577394, 0.073086),
	("vpx.gi027", 0.350497, 0.136035), ("vpx.gi028", 0.313774, 0.064423),
	("vpx.gi029", 0.113108, 0.419596), ("vpx.gi040", 0.856770, 0.479800),
	("vpx.gi060001", 0.126114, 0.908417), ("vpx.gi062", 0.796817, 0.908287),
	("vpx.gi063", 0.477828, 0.931914),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "service.ticket",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament", 16: "cabinet.start", 65: "cabinet.coin.left",
	66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth",
	69: "cabinet.coin.fifth", 82: "flipper.lower.right.button", 84: "flipper.lower.left.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 21): "cabinet.rear-panel",
	("pinmame.output.solenoid", 22): "cabinet.rear-panel",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("physical.output.ticket", 33): "service.ticket",
	("physical.output.ticket", 34): "service.ticket",
	("physical.output.ticket", 35): "service.ticket",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]] | list[tuple[str, float, float]], source_refs: tuple[str, ...]) -> None:
	placements = []
	for index, position in enumerate(positions, start=1):
		if len(position) == 3:
			suffix, x, y = position
			placement_suffix = f".{suffix}"
		else:
			x, y = position
			placement_suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{placement_suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed spatial disposition to every physical input and output."""
	if any("spatial" in device for collection in (definition["inputs"], definition["outputs"]) for device in collection):
		raise ValueError("Metallica Pro spatial curation requires an unspatialized base definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			if address == 81:
				device["roles"] = ["flipper.lower.right.eos"]
			elif address == 83:
				device["roles"] = ["flipper.lower.left.eos"]
			_located(device, "sensor", INPUT_POSITIONS[address], DIRECT_SOURCES)
			if address in {18, 19, 20, 21}:
				_append_note(device, "The working table models the four-ball trough as one stack rather than four geometry objects. This manual-confirmed point is a disclosed assembly projection along the trough path; switch 21 terminates at the exact BallRelease eject anchor.")
			elif address == 22:
				_append_note(device, "The proven script pulses this downstream jam opto during trough ejection but exposes no separate object. This is a disclosed regional projection between the exact eject and shooter-lane anchors, with practical uncertainty of about plus or minus 0.04 normalized x and 0.03 normalized y.")
			elif address in {26, 27}:
				_append_note(device, "The switch is implicit in the exact VPX slingshot collision wall. This point is the wall polygon centroid, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address in {60, 61, 62}:
				_append_note(device, "This is the exact visible target center; the normally-closed under-playfield contact follows the moving target at the same assembly position.")
			elif address in {81, 83}:
				_append_note(device, "The normally-closed EOS contact is implicit in the exact lower-flipper assembly; this is its assembly center, with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Metallica Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", PRO_VPX_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			if group == "pinmame.output.solenoid" and address in {21, 22}:
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
				_append_note(device, "The Pro coil chart and location map prove one physical bulb on this side of the rear panel; it is outside normalized playfield space.")
			elif group == "pinmame.output.solenoid" and address == 24:
				_append_note(device, "The official Pro chart defines optional output 24 as a coin meter. The known-working VPX uses a knocker sound effect for this callback, which is cabinet feedback emulation and does not add a physical knocker to the machine definition.")
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], DIRECT_SOURCES)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address in {13, 14}:
				_append_note(device, "This exact VPX slingshot-wall polygon centroid is the manual-confirmed coil assembly projection, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address == 18:
				_append_note(device, "The exact Head1 rest-state pivot supplies the Electric Chair/Sparky step-up assembly point. It is a moving parent-relative coordinate, not an internal coil center.")
			elif address == 20:
				_append_note(device, "The official Pro map proves one snake flasher. The table's two callback glow objects sit at the slings and conflict with that physical geometry, so this manual-confirmed snake-eject assembly anchor is used instead of preserving the render error.")
			elif address == 30:
				_append_note(device, "The official Pro chart proves one captive-ball flasher. The table spreads three glow objects across that area; the central f30a point is retained as one composite physical anchor rather than inventing three bulbs.")
			elif address == 12:
				_append_note(device, "The reset coil acts on the complete three-target bank. This point is the centroid of exact target centers 60-62, not a claim that the under-playfield reset coil sits on the playfield surface.")
		elif group == "pinmame.output.lamp" and 1 <= address <= 80:
			if address not in LAMP_POSITIONS:
				raise ValueError(f"Used Metallica Pro standard lamp {address} has no reviewed position")
			_located(device, "emitter", LAMP_POSITIONS[address], DIRECT_SOURCES)
			device.setdefault("physical", {})["quantity"] = len(LAMP_POSITIONS[address])
			if len(LAMP_POSITIONS[address]) > 1:
				_append_note(device, "The official Pro lamp-location map and exact table both prove the listed physical multiplicity for this one matrix output.")
			elif address in LAMP_COLLAPSE_NOTES:
				_append_note(device, LAMP_COLLAPSE_NOTES[address])
		elif group == "pinmame.output.gi" and address == 0:
			_located(device, "emitter", GI_POSITIONS, DIRECT_SOURCES)
			device.setdefault("physical", {})["quantity"] = 39
			_append_note(device, "The exact table's 64 ordinary-GI render lights collapse to 33 distinct playfield anchors after paired glow layers are deduplicated. The official GI map additionally proves six back-panel sockets outside playfield space; quantity remains 39 without fabricated back-panel coordinates.")
		else:
			raise ValueError(f"Metallica Pro output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Metallica Pro knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PRO_KNOWLEDGE,
	"Coverage: **author-ready - complete physical I/O, mechanisms, variant split, wiring, and recreation behavior validated**",
	"Coverage: **author-ready - complete physical I/O, mechanisms, variant split, wiring, recreation behavior, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nEvery physical playfield sensor, actuator, controlled lamp, flasher, and ordinary-GI anchor uses one normalized player-view frame from the exact 952 by 2162 JP table: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. The working script establishes controller causality and the official manual confirms physical inventory and multiplicity. Cabinet, service, rear-panel, virtual, DIP, and unused records never receive fake playfield points. Trough contacts, the shooter-path jam opto, slingshot contacts/coils, EOS contacts, and drop-bank reset are explicitly disclosed as assembly or regional projections.\n\nPhysical lighting multiplicity follows the Pro service maps rather than the count of VPX glow helpers. Only matrix outputs 4 and 27 drive two physical lamps. For outputs 9-12, 31, 32, 41, 48, 53, 60-62, 70, and 71, one of two VPX render objects is retained as the approximate physical socket anchor; every affected record discloses the discarded helper and residual uncertainty. Flashers 26, 27, 28, and 31 are pairs; every other playfield flasher is one bulb. The two VPX glow objects driven by snake flasher 20 occupy the slings and conflict with the official physical map, so the definition uses a disclosed snake-assembly projection. Captive-ball flasher 30 is one physical bulb represented by three overlapping/spread glow helpers, so only its central composite anchor is retained. Rear-panel outputs 21/22 each drive one off-playfield bulb. Ordinary GI has 33 deduplicated exact playfield anchors plus six manual-proven rear-panel sockets; all 39 are retained in physical quantity without invented rear-panel coordinates.\n\nOutput 24 is physically the optional coin meter on the Pro wiring chart. JP's callback plays a knocker sound as cabinet feedback, but that render/audio choice is not evidence for a physical knocker. The Pro mechanism topology otherwise stays intentionally simpler than Premium/LE: the grave marker and snake are static, the captive ball is passive, there is no coffin lock/magnet processor, and decorative VPX spinners remain non-scoring.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; Pro service tables on PDF pages 119-129.",
	"- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; ordinary-GI physical map on PDF page 114 and Pro coil/flasher chart, coil location, lamp matrix, and lamp location on pages 119, 120, 122, and 123.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `vpx-table.metallica-pro-jps-6.0.0`: VPForums table, SHA-256 `837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118`; downloaded archive SHA-256 `5fafb136ed9f76ad32dcc035bd72c4dadd856562778f9fae53d7e1bcc9396ff0`.",
	"- `vpx-table.metallica-pro-jps-6.0.0`: exact known-working `JP's Metallica Pro (Stern 2013) v600.vpx`, SHA-256 `837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118`; downloaded archive SHA-256 `5fafb136ed9f76ad32dcc035bd72c4dadd856562778f9fae53d7e1bcc9396ff0`, retained externally under `pinmame-vpx-sources/stern/metallica-pro-2013/source`, and extracted read-only with vpxtool git:v0.33.3 for the sole normalized geometry frame.",
)


def promote() -> None:
	definition = build_pro()
	table_source = next(source for source in definition["sources"] if source["id"] == PRO_VPX_TABLE_SOURCE)
	table_source["known_working"] = True
	table_source["uri"] = "external:pinmame-vpx-sources/stern/metallica-pro-2013/source/JP's Metallica Pro (Stern 2013) v600.vpx"
	table_source["locator"] = "JP's Metallica Pro (Stern 2013) v600.vpx (32,940,032 bytes); exact mtl_180 Pro table extracted with vpxtool git:v0.33.3; its 952 by 2162 bounds are the sole normalized coordinate frame after script/manual reconciliation"
	manual_source = next(source for source in definition["sources"] if source["id"] == MANUAL_SOURCE)
	manual_source["locator"] = "MTLAB1-compressed.pdf: ordinary-GI physical map on PDF page 114; Pro coil/flasher chart and location map on pages 119-120; Pro lamp matrix and physical location map on pages 122-123; related service sheets through page 129"
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/metallica-pro-2013.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
