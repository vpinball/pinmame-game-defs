"""Promote Star Trek Premium / Limited Edition with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import write_json, write_text

from curate_star_trek import CORE_SOURCE, PREMIUM_KNOWLEDGE, PREMIUM_MANUAL, VPX_SOURCE, build_premium


PARTIAL_PATH = ROOT / "machines/partial/stern/star-trek-premium-limited-edition-2013.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/star-trek-premium-limited-edition-2013.json"

NEO_TABLE_SOURCE = "vpx-table.star-trek-le-neo-real-1.0.2-geometry"
NEO_TABLE_SOURCE_RECORD = {
	"attribution": "Neo and the table authors credited by the table distribution",
	"id": NEO_TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Star Trek LE Neo real Mod 1.0.2.vpx (191,655,936 bytes), exact st_161h table extracted with vpxtool git:v0.33.3. Its 952 by 2300 playfield bounds are the sole normalized coordinate frame. Object geometry is accepted only after reconciliation with the official manual and proven v1.10 script. Neo's manual-matching 18-21 trough initialization and switch-22 ejection pulse are accepted; its upper-flipper coupling and Vengeance simplifications are explicitly rejected.",
	"original_filename": "Star Trek LE Neo real Mod 1.0.2.vpx",
	"rights": "NOASSERTION",
	"sha256": "f7edee3cbcebff1a078496b7ef7dcef7368158a61b48934f2241792a70bc233c",
	"uri": "external:pinmame-vpx-sources/stern/star-trek-premium-limited-edition-2013/source/Star Trek LE Neo real Mod 1.0.2.vpx",
}

ENTERPRISE_TABLE_SOURCE = "vpx-table.star-trek-enterprise-le-geometry"
ENTERPRISE_TABLE_SOURCE_RECORD = {
	"attribution": "The table authors credited by the table distribution",
	"id": ENTERPRISE_TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Star Trek Enterprise Limited Edition (Stern 2012).vpx (66,732,032 bytes), exact st_161hc table extracted with vpxtool git:v0.33.3. Only geometry absent from the canonical Neo table is used: its switch 18 is a drain and is rejected, while its four ball positions 19-22 are translated and mapped in order to physical Premium/LE trough switches 18-21 by aligning the table's switch-22 trough-out with Neo BallRelease. Lamp 51 and Vengeance bulb meshes use separate local registrations; no coordinate from this table's normalized frame is copied directly.",
	"original_filename": "Star Trek Enterprise Limited Edition (Stern 2012).vpx",
	"rights": "NOASSERTION",
	"sha256": "46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e",
	"uri": "external:pinmame-vpx-sources/stern/star-trek-premium-limited-edition-2013/source/Star Trek Enterprise Limited Edition (Stern 2012).vpx",
}

INPUT_POSITIONS = {
	1: [(0.578782, 0.138478)], 2: [(0.671218, 0.138478)], 4: [(0.757878, 0.144565)],
	7: [(0.794118, 0.605543)], 8: [(0.804622, 0.630978)], 9: [(0.814076, 0.657283)],
	10: [(0.102416, 0.482826)], 11: [(0.516282, 0.312283)], 12: [(0.229517, 0.531196)],
	13: [(0.134454, 0.305924)], 14: [(0.319853, 0.235272)],
	18: [(0.703727, 0.946296)], 19: [(0.749432, 0.933741)], 20: [(0.796670, 0.921846)],
	21: [(0.849790, 0.906658)], 22: [(0.895000, 0.908000)], 23: [(0.939863, 0.909891)],
	24: [(0.077731, 0.834990)], 25: [(0.149160, 0.790435)],
	26: [(0.242986, 0.774518)], 27: [(0.682742, 0.775298)],
	28: [(0.775998, 0.790978)], 29: [(0.851891, 0.809348)],
	30: [(0.581736, 0.214458)], 31: [(0.799698, 0.219893)], 32: [(0.675748, 0.290545)],
	33: [(0.500525, 0.297554)], 34: [(0.490021, 0.258207)],
	35: [(0.001576, 0.335054)], 36: [(0.202206, 0.062663)],
	37: [(0.808298, 0.239620)], 38: [(0.941702, 0.202228)],
	39: [(0.283088, 0.452935)], 40: [(0.287815, 0.479022)], 41: [(0.292542, 0.505326)],
	42: [(0.088761, 0.621630)], 43: [(0.083771, 0.647935)], 44: [(0.868172, 0.617935)],
	45: [(0.178046, 0.573152)], 46: [(0.287815, 0.345543)], 47: [(0.442752, 0.330109)],
	48: [(0.628267, 0.319965)], 49: [(0.636029, 0.410761)], 50: [(0.776786, 0.425978)],
	51: [(0.896534, 0.148261)], 52: [(0.067227, 0.236522)], 53: [(0.500865, 0.237365)],
	81: [(0.621586, 0.888587)], 83: [(0.305935, 0.888587)],
}

SOLENOID_POSITIONS = {
	1: [(0.849790, 0.906658)], 2: [(0.938813, 0.911467)], 3: [(0.498950, 0.261848)],
	4: [(0.516282, 0.312283)], 5: [(0.516282, 0.312283)], 6: [(0.102416, 0.482826)],
	7: [(0.493561, 0.234511)], 9: [(0.581736, 0.214458)], 10: [(0.799698, 0.219893)],
	11: [(0.675748, 0.290545)], 12: [(0.850839, 0.517146)],
	13: [(0.242986, 0.774518)], 14: [(0.682742, 0.775298)],
	15: [(0.305935, 0.888587)], 16: [(0.621586, 0.888587)],
	17: [(0.248844, 0.277954)], 18: [(0.831574, 0.252564)],
	19: [(0.033892, 0.112326)], 20: [(0.756171, 0.117120)], 21: [(0.501536, 0.246117)],
	22: [(0.200000, 0.960000)], 23: [(0.335535, 0.238322)], 25: [(0.691504, 0.220796)],
	26: [(0.186737, 0.343828)], 27: [(0.265665, 0.463793)], 28: [(0.769132, 0.327344)],
	29: [(0.235294, 0.539783)], 30: [(0.876356, 0.480302)], 31: [(0.502101, 0.247048)],
	32: [(0.221113, 0.715870)], 51: [(0.530593, 0.097323)], 52: [(0.813682, 0.115584)],
	53: [(0.500865, 0.237365)], 54: [(0.074562, 0.880015)], 55: [(0.103108, 0.480360)],
	56: [(0.500865, 0.237365)], 59: [(0.707983, 0.718261)],
}

PHYSICAL_LAMP_POSITIONS: dict[int, list[tuple[str, float, float]]] = {
	1: [("module", 0.381828, 0.367106)], 2: [("module", 0.326418, 0.355068)],
	3: [("module", 0.400604, 0.419796)], 4: [("module", 0.446691, 0.353764)],
	5: [("module", 0.518120, 0.363519)], 6: [("module", 0.533774, 0.415992)],
	7: [("module", 0.589023, 0.393655)], 8: [("module", 0.605436, 0.357948)],
	9: [("module", 0.820903, 0.458519)], 10: [("module", 0.783219, 0.507622)],
	11: [("module", 0.761029, 0.448872)], 12: [("module", 0.683036, 0.449063)],
	13: [("module", 0.658745, 0.501100)], 14: [("module", 0.620273, 0.433764)],
	15: [("module", 0.638130, 0.586481)], 16: [("module", 0.705751, 0.569905)],
	17: [("module", 0.106749, 0.536861)], 18: [("module", 0.135373, 0.585557)],
	19: [("module", 0.146534, 0.623655)], 20: [("module", 0.274947, 0.586128)],
	21: [("module", 0.205095, 0.592894)], 22: [("module", 0.319722, 0.636209)],
	23: [("module", 0.142069, 0.652133)], 24: [("module", 0.210084, 0.653302)],
	25: [("module", 0.269301, 0.698274)], 26: [("module", 0.076067, 0.787265)],
	27: [("module", 0.074711, 0.743166)], 28: [("module", 0.148766, 0.726753)],
	29: [("module", 0.353466, 0.504633)], 30: [("module", 0.346376, 0.477894)],
	31: [("module", 0.341649, 0.452459)], 32: [("module", 0.536371, 0.463600)],
	33: [("module", 0.543724, 0.511209)], 34: [("module", 0.465993, 0.916101)],
	35: [("module", 0.465074, 0.864063)], 36: [("module", 0.573792, 0.821889)],
	37: [("module", 0.464548, 0.821889)], 38: [("module", 0.355305, 0.821889)],
	39: [("module", 0.517069, 0.779280)], 40: [("module", 0.460872, 0.736671)],
	41: [("module", 0.407826, 0.779280)], 42: [("module", 0.460084, 0.698111)],
	43: [("module", 0.460084, 0.670285)], 44: [("module", 0.460084, 0.643111)],
	45: [("module", 0.458246, 0.615285)], 46: [("module", 0.457195, 0.586264)],
	47: [("module", 0.456145, 0.558111)], 48: [("module", 0.455095, 0.530285)],
	49: [("module", 0.454307, 0.502242)], 50: [("module", 0.172320, 0.182543)],
	51: [("assembly", 0.897124, 0.517279)],
	52: [("module", 0.137099, 0.162618)], 53: [("module", 0.577468, 0.100503)],
	54: [("module", 0.668592, 0.100503)], 55: [("module", 0.757090, 0.106590)],
	56: [("saucer", 0.500865, 0.224407)],
	57: [("nacelle.left", 0.377191, 0.172295), ("nacelle.right", 0.624474, 0.172295)],
	58: [("module", 0.738445, 0.610394)], 59: [("module", 0.746849, 0.636372)],
	60: [("module", 0.756828, 0.662459)], 61: [("module", 0.774028, 0.727296)],
	62: [("module", 0.850184, 0.746535)],
	63: [("assembly", 0.143749, 0.888266)],
	64: [("assembly", 0.771201, 0.888266)],
	70: [("chaser", 0.104114, 0.296557)],
	71: [("chaser", 0.093751, 0.275397)],
	72: [("chaser", 0.092369, 0.251377)],
	73: [("chaser", 0.092369, 0.228881)],
	74: [("chaser", 0.092369, 0.201430)],
	75: [("chaser", 0.097282, 0.176012)],
	76: [("chaser", 0.111087, 0.151356)],
	77: [("chaser", 0.125825, 0.125684)],
}

# The official page-152 underside drawing is rotated into player view. Its 31
# labeled socket centers are projected through the inner playfield outline;
# x therefore inverts the drawing's vertical axis and y follows its horizontal
# axis. The two GI3 symbols embedded in the illustrated pop-bumper assemblies
# are excluded here and replaced below by the three exact VPX pop centers.
GI_SOCKET_POSITIONS: list[tuple[str, float, float]] = [
	("socket-01", 0.945055, 0.042629),
	("socket-02", 0.887912, 0.425933),
	("socket-03", 0.874725, 0.188632),
	("socket-04", 0.829304, 0.084902),
	("socket-06", 0.819780, 0.632682),
	("socket-07", 0.810256, 0.601066),
	("socket-08", 0.786813, 0.280284),
	("socket-09", 0.750916, 0.861456),
	("socket-10", 0.740659, 0.070693),
	("socket-11", 0.720147, 0.772291),
	("socket-13", 0.684249, 0.884902),
	("socket-14", 0.679853, 0.818828),
	("socket-15", 0.632967, 0.060391),
	("socket-16", 0.547253, 0.064298),
	("socket-17", 0.442491, 0.132504),
	("socket-18", 0.412454, 0.083126),
	("socket-19", 0.262271, 0.434458),
	("socket-20", 0.262271, 0.466785),
	("socket-21", 0.257875, 0.021314),
	("socket-22", 0.227839, 0.245471),
	("socket-23", 0.213187, 0.819893),
	("socket-24", 0.207326, 0.877087),
	("socket-25", 0.184615, 0.130728),
	("socket-26", 0.172161, 0.768028),
	("socket-27", 0.147253, 0.859325),
	("socket-28", 0.126740, 0.202131),
	("socket-29", 0.095238, 0.058259),
	("socket-30", 0.059341, 0.023446),
	("socket-31", 0.051282, 0.619538),
	("socket-32", 0.038095, 0.299467),
	("socket-33", 0.033700, 0.558437),
]

GI_POP_POSITIONS: list[tuple[str, float, float]] = [
	("pop.left", 0.581736, 0.214458),
	("pop.right", 0.799698, 0.219893),
	("pop.bottom", 0.675748, 0.290545),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth",
	71: "cabinet.action", 82: "cabinet.flipper", 84: "cabinet.flipper", 86: "cabinet.flipper",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.solenoid", 60): "cabinet.backbox",
	("pinmame.output.solenoid", 61): "cabinet.backbox",
	("pinmame.output.solenoid", 62): "cabinet.backbox",
	("pinmame.output.solenoid", 63): "cabinet.backbox",
	("pinmame.output.solenoid", 64): "cabinet.backbox",
}

BACKBOX_FLASHER_QUANTITIES = {60: 2, 61: 2, 62: 1, 63: 1, 64: 1}
DIRECT_NEO_SOURCES = (PREMIUM_MANUAL, VPX_SOURCE, NEO_TABLE_SOURCE)
REGISTERED_ENTERPRISE_SOURCES = (PREMIUM_MANUAL, VPX_SOURCE, NEO_TABLE_SOURCE, ENTERPRISE_TABLE_SOURCE)
REGISTERED_ENTERPRISE_INPUTS = {18, 19, 20, 21}


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


def _manual_lamp_number(device: dict[str, object]) -> int:
	for alias in device.get("aliases", []):
		if alias.get("namespace") == "manual.address":
			return int(alias["value"])
	raise ValueError(f"Used Star Trek lamp {device['id']} has no manual diagnostic address")


def _lamp_quantity(physical_number: int) -> int:
	if physical_number in {51, 57, 63, 64, 78} or 79 <= physical_number <= 100:
		return 2
	return 1


def _located_gi(device: dict[str, object]) -> None:
	placements = []
	for suffix, x, y in GI_SOCKET_POSITIONS:
		placements.append({"id": f"{device['id']}.emitter.{suffix}", "role": "emitter", "space": "playfield", "x": x, "y": y, "provenance": _provenance(PREMIUM_MANUAL)})
	for suffix, x, y in GI_POP_POSITIONS:
		placements.append({"id": f"{device['id']}.emitter.{suffix}", "role": "emitter", "space": "playfield", "x": x, "y": y, "provenance": _provenance(PREMIUM_MANUAL, NEO_TABLE_SOURCE)})
	device["spatial"] = {"status": "validated", "placements": placements}
	device.setdefault("physical", {})["quantity"] = 41
	_append_note(device, "The official page-152 drawing establishes 27 wedge-base sockets, four bayonet sockets, and three illuminated pop-bumper assemblies: 34 playfield emitters total on physical GI0/GI1/GI3 wiring regions. Individual base and wiring-region assignments are not asserted in placement IDs because the drawing does not support a fully reliable per-socket transcription. Its separate backbox inset proves four white GI3, two blue GI1, and one red GI0 bayonet, bringing the physical aggregate to 41 emitters behind PinMAME's one GI-0 transport channel. The 31 drawn socket centers are calibrated manual projections: their socket identity and physical region are validated, but the drawing does not support a quantified per-socket positional tolerance and the six-decimal values must not be read as sub-object measurement precision. The three pop points are canonical Neo assembly centers. The seven backbox fixtures are inventoried here but intentionally have no playfield-space placement. All VPX bloom, reflection, and Laser* helpers are excluded.")


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed spatial disposition to every physical input and output."""
	if any("spatial" in device for collection in (definition["inputs"], definition["outputs"]) for device in collection):
		raise ValueError("Star Trek Premium spatial curation requires an unspatialized base definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PREMIUM_MANUAL)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PREMIUM_MANUAL)
		elif address in INPUT_POSITIONS:
			sources = REGISTERED_ENTERPRISE_SOURCES if address in REGISTERED_ENTERPRISE_INPUTS else DIRECT_NEO_SOURCES
			_located(device, "sensor", INPUT_POSITIONS[address], sources)
			if address in {18, 19, 20, 21}:
				_append_note(device, "The official manual and exact Neo table prove the physical four-position trough order and initial 18-21 occupancy. The older table's switch 18 is its drain and is rejected; its four ball positions 19-22 are translated into the canonical Neo frame and mapped in order to physical switches 18-21 by aligning its switch-22 trough-out with Neo BallRelease at (0.849790, 0.906658). Do not reproduce v1.10's virtual switch-18 drain and 19-22 ball chain.")
			elif address == 22:
				_append_note(device, "The official manual requires the downstream trough-jam opto and the exact Neo script pulses switch 22 on ejection, but Neo does not model a direct sensor object. This is an approximate regional marker on the short corridor between Neo BallRelease and shooter-lane switch 23, not an exact sensor center; practical uncertainty is about plus or minus 0.045 normalized x and 0.02 normalized y.")
			elif address == 11:
				_append_note(device, "The manual establishes the single memory target. This is the canonical Neo visible sw11p target center; its overlapping DropTrigger is the controller sensor and the adjacent center-lock magnet remains a separate assembly.")
			elif address in {26, 27}:
				_append_note(device, "The sensor is implicit in the canonical Neo slingshot collision-wall footprint; this is its assembly centroid with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address == 53:
				_append_note(device, "The crash opto is part of the moving Vengeance latch assembly. This is the canonical Neo ship-parent rest anchor used as a manual-confirmed sensor projection, with practical uncertainty of about plus or minus 0.03 normalized x and y.")
			elif address in {81, 83}:
				_append_note(device, "The normally-closed EOS contact is implicit in the exact lower-flipper assembly; the flipper center is an assembly projection with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PREMIUM_MANUAL)
		else:
			raise ValueError(f"Star Trek Premium input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PREMIUM_MANUAL)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			if address in BACKBOX_FLASHER_QUANTITIES:
				device.setdefault("physical", {})["quantity"] = BACKBOX_FLASHER_QUANTITIES[address]
				_append_note(device, "The official LE backbox drawing establishes this physical fixture count; it is intentionally excluded from normalized playfield space.")
			_not_applicable(device, "cabinet_or_service", PREMIUM_MANUAL)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			if address == 22:
				sources = (PREMIUM_MANUAL,)
			else:
				sources = DIRECT_NEO_SOURCES
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], sources)
			device.setdefault("physical", {})["quantity"] = len(SOLENOID_POSITIONS[address])
			if address in {4, 5}:
				_append_note(device, "Outputs 4 and 5 raise and lower one physical memory-target assembly and intentionally share the canonical Neo sw11p target center; this is distinct from output 3's adjacent Magnet2 center.")
			elif address in {13, 14}:
				_append_note(device, "This is the exact slingshot wall centroid used as the manual-confirmed coil assembly projection, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address == 22:
				_append_note(device, "The service drawing places the physical laser motor beneath the lower-left apron. It supports only this approximate regional marker in the canonical frame, not a calibrated point; practical uncertainty is about plus or minus 0.08 normalized x and 0.04 normalized y. Full-table laser render fields are not physical motor locations.")
			elif address in {53, 56}:
				_append_note(device, "The Vengeance dive/shake actuator and latch belong to one moving ship assembly and intentionally share its canonical Neo rest-state parent anchor. This is a manual-confirmed assembly projection, not a claim that the distinct internal actuators occupy the same point; practical uncertainty is about plus or minus 0.04 normalized x and y.")
			elif address in {6, 55}:
				_append_note(device, "The eject coil and unsensed rotating VUK/deflector perform distinct operations at one physical scoop: output 6 uses the eject mouth while output 55 uses the exact rotating Scoop primitive pivot.")
			elif address in {19, 20}:
				_append_note(device, "The proven v1.10 script establishes the physical ramp-cap semantics; the corresponding canonical Neo f119a/f120a cap center supplies geometry. Broad wall-glow and ramp-transmission helpers are excluded.")
			elif address == 31:
				_append_note(device, "The proven v1.10 script establishes output 31's Vengeance-flasher semantics through its F31/F31a render helpers. The Neo table maps the same output to VengFlashGI, whose light center supplies this rest-state parent-relative assembly point; the broad F31/F31a bloom geometry is excluded.")
		elif group == "pinmame.output.lamp":
			physical_number = _manual_lamp_number(device)
			physical = device.setdefault("physical", {})
			physical["quantity"] = _lamp_quantity(physical_number)
			if physical_number in PHYSICAL_LAMP_POSITIONS:
				positions = PHYSICAL_LAMP_POSITIONS[physical_number]
				sources = REGISTERED_ENTERPRISE_SOURCES if physical_number in {51, 56, 57} else DIRECT_NEO_SOURCES
				_located(device, "emitter", positions, sources)
				if 1 <= physical_number <= 49 or physical_number in {52, 53, 54, 55, 58, 59, 60, 61, 62, 63, 64}:
					_append_note(device, "This controller record is one color channel of the physical RGB module; all channel records intentionally share the same physical placement list and must not be recreated as separate modules.")
				if physical_number == 51:
					_append_note(device, "The manual proves two blue Enterprise emitters. The older geometry exposes only one composite light/model anchor, so quantity remains two but there is one assembly placement, never an invented bulb separation. The anchor is translated into the canonical Neo frame by the local upper-right-flipper correspondence; practical uncertainty is about plus or minus 0.03 normalized x and y.")
				elif physical_number == 57:
					_append_note(device, "The two nacelle centers are derived from the two connected components of the exact L57_NacelleBulbs mesh after applying the older table's 180-degree ship transform. A local ship-parent translation registers them into the canonical Neo frame. They are rest-state parent-relative points and move with Vengeance.")
				elif physical_number == 56:
					_append_note(device, "This saucer bulb point is locally registered from the older bulb mesh to the canonical Neo ship parent. It is rest-state and parent-relative, so it transforms with Vengeance.")
				elif physical_number in {63, 64}:
					_append_note(device, "The manual proves two physical apron emitters, while Neo exposes one composite light footprint. Quantity remains two but the definition records one canonical assembly center and does not invent separate bulb points; practical uncertainty is about plus or minus 0.03 normalized x and y.")
				elif 70 <= physical_number <= 77:
					_append_note(device, "The manual proves one physical warp-chaser lamp for this diagnostic number. The proven v1.10 script establishes the output semantics, and the canonical Neo l70-l77 physical lamp object supplies the point. v1.10's two beam segments and WarpAmbient bloom are render helpers and are excluded from physical quantity.")
			elif physical_number in {65, 66, 67, 68, 69, 78} or 79 <= physical_number <= 100:
				device.setdefault("roles", ["cabinet.lighting"])
				_not_applicable(device, "cabinet_or_service", PREMIUM_MANUAL)
				if physical_number in {66, 67, 68}:
					_append_note(device, "Physical lamps 66-68 are the red, green, and blue channels of one cabinet Fire-button assembly, not three separately placed buttons.")
			else:
				raise ValueError(f"Star Trek Premium physical lamp {physical_number} has no reviewed spatial disposition")
		elif group == "pinmame.output.gi" and address == 0:
			_located_gi(device)
		else:
			raise ValueError(f"Star Trek Premium output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Star Trek Premium knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PREMIUM_KNOWLEDGE,
	"Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**",
	"Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, recreation behavior, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nEvery physical playfield input, actuator, lamp, and GI socket has a normalized player-view placement: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. The 952 by 2300 Neo table is the sole normalized coordinate frame. Direct Neo object centers are accepted only after reconciliation with the official manual and proven v1.10 script. Geometry absent from Neo is never copied from another normalized table frame: trough switches 18-21 are locally registered by the shared direct-Neo switch-22 trough-out anchor, lamp 51 by the shared upper-right flipper, and Vengeance bulb-mesh points by the shared ship parent. Slingshot sensors/coils, the Vengeance crash opto, EOS contacts, laser motor, composite multi-bulb assemblies, and GI sockets use explicitly disclosed assembly or drawing projections. Cabinet, service, backbox fixtures, virtual, unpopulated, unused, and DIP devices are outside playfield space.\n\nThe lamp audit preserves physical multiplicity that render geometry can both hide and exaggerate. Lamp 51 has two Enterprise emitters but only one defensible composite assembly anchor; lamps 63 and 64 likewise each have two apron emitters represented by one composite Neo assembly center. No false bulb separation is invented. Lamp 57 has two separately recoverable Vengeance nacelle centers. The manual proves one physical lamp for each warp-chaser number 70-77; v1.10's paired beam segments and WarpAmbient object are render helpers, while Neo's direct l70-l77 lamp objects supply one canonical point per output. Cabinet Enterprise and every cabinet phaser output also retain the manual's ×2 physical quantity even though they have no playfield coordinate.\n\nThe moving Vengeance is one spatial assembly with separate causality: output 53 supplies PWM dive/shake motion, output 56 controls the latch/return, switch 53 reports the crash/latch state, output 7 returns the captive ball, output 31 flashes the ship, and lamps 56/57 illuminate the saucer and two nacelles. The v1.10 script proves output 31's Vengeance semantics through F31/F31a, while Neo maps that same output to VengFlashGI and supplies the canonical assembly anchor. Their points are canonical-frame, parent-relative rest-state placements; co-located assembly anchors do not collapse them into one device or claim identical internal actuator locations. The broad F31/F31a bloom geometry is a render helper and is not used as output 31's physical position. The left eject and output-55 rotating VUK likewise belong to one scoop but use separate Neo eject-mouth and rotating-pivot points, with no invented position switch.\n\nThe page-152 GI drawing proves 34 playfield emitters: 31 sockets plus three illuminated pop-bumper assemblies. Its separate backbox inset proves seven additional physical GI lamps. The aggregate output therefore keeps quantity 41, but only the 34 playfield emitters receive playfield-space placements; the backbox row is not misrepresented at y=0. The 31 drawing-derived socket centers preserve validated identity and physical region, but the drawing does not support a quantified per-socket positional tolerance; their six-decimal projected values are not claims of sub-object measurement precision. The official coil-location drawing places the unsensed laser motor beneath the lower-left apron; its coordinate remains a disclosed manual projection and the broad Laser render fields are effects, not motor locations. The auxiliary drawing proves two Q42 speaker-panel flashers, two Q43 backbox flashers, and one each on Q44-Q46. Those quantities remain in the definition while all seven fixtures stay outside normalized playfield space.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"Geometry absent from Neo is never copied from another normalized table frame: trough switches 18-21 are locally registered by the shared direct-Neo switch-22 trough-out anchor, lamp 51 by the shared upper-right flipper, and Vengeance bulb-mesh points by the shared ship parent.",
	"Geometry absent from Neo is never copied from another normalized table frame: the donor table's switch 18 drain is rejected, its four ball positions 19-22 are locally registered and mapped in order to physical Premium/LE switches 18-21, lamp 51 is registered by the shared upper-right flipper, and Vengeance bulb-mesh points by the shared ship parent. The manual-required jam opto 22 is absent as a direct Neo sensor and receives a disclosed approximate point on the ejection corridor.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"The official coil-location drawing places the unsensed laser motor beneath the lower-left apron; its coordinate remains a disclosed manual projection and the broad Laser render fields are effects, not motor locations.",
	"The official coil-location drawing places the unsensed laser motor beneath the lower-left apron; its coordinate is a disclosed approximate region rather than a calibrated point, and the broad Laser render fields are effects, not motor locations.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `manual.star-trek-premium-le`: official Stern `Star-Trek-LE-Manual.pdf`, SHA-256 `ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d`; I/O and wiring tables on PDF pages 68-77, 114-119, and 153-155.",
	"- `manual.star-trek-premium-le`: official Stern `Star-Trek-LE-Manual.pdf`, SHA-256 `ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d`; I/O and physical location drawings on PDF pages 68-77, wiring on 114-119 and 153-155, and the physical GI/socket drawing on PDF page 152.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `vpx.star-trek-le-1.10`: known-working script",
	"- `vpx-table.star-trek-le-neo-real-1.0.2-geometry`: exact `Star Trek LE Neo real Mod 1.0.2.vpx`, 191,655,936 bytes, SHA-256 `f7edee3cbcebff1a078496b7ef7dcef7368158a61b48934f2241792a70bc233c`; retained externally under `pinmame-vpx-sources/stern/star-trek-premium-limited-edition-2013/source` and used as the sole normalized geometry frame after semantic reconciliation.\n- `vpx-table.star-trek-enterprise-le-geometry`: exact `Star Trek Enterprise Limited Edition (Stern 2012).vpx`, 66,732,032 bytes, SHA-256 `46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e`; retained beside the Neo table and used only for missing geometry that is locally registered into the Neo frame by a shared physical anchor.\n- `vpx.star-trek-le-1.10`: known-working script",
)


def promote() -> None:
	definition = build_premium()
	definition["sources"].extend([NEO_TABLE_SOURCE_RECORD, ENTERPRISE_TABLE_SOURCE_RECORD])
	manual_source = next(source for source in definition["sources"] if source["id"] == PREMIUM_MANUAL)
	manual_source["locator"] = "Star-Trek-LE-Manual.pdf, PDF pages 68-77, 114-119, 152-155"
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/star-trek-premium-limited-edition-2013.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
