"""Promote the physical Rolling Stones Limited Edition with reviewed spatial evidence.

The source table is the exact LE VPX found in the local Tables Archive.  This
module deliberately keeps the Standard definition on the fail-closed path:
the Premium/LE-only magnets, posts, five-ball trough, and cabinet controls are
never copied into it. Promotion writes only the canonical repository definition
and knowledge outputs below; candidate extraction and overlay artifacts remain
explicit-output operations in the spatial CLI and are never written here.
"""

from __future__ import annotations

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import write_json, write_text

from curate_rolling_stones import LE_KNOWLEDGE, VPU_LE_SOURCE, build


PARTIAL_PATH = ROOT / "machines/partial/stern/the-rolling-stones-limited-edition-2011.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-rolling-stones-limited-edition-2011.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/the-rolling-stones-limited-edition-2011.md"

MANUAL_SOURCE = "manual.rolling-stones-standard-le.2011"
VPX_SOURCE = "vpx.rolling-stones-le-1.0.6i"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
VPX_TABLE_SOURCE = "vpx-table.rolling-stones-le-archive-2020"
TABLE_SHA256 = "da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10"
DIRECT_SOURCES = (MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE)


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(
	device: dict[str, object],
	role: str,
	positions: list[tuple[float, float]] | list[tuple[str, float, float]],
	source_refs: tuple[str, ...] = DIRECT_SOURCES,
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
	device["spatial"] = {
		"status": "not_applicable",
		"reason": reason,
		"provenance": _provenance(*source_refs),
	}


def _note(device: dict[str, object], text: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {text}".strip()


# Centers are normalized from the exact VPX's 1000 x 2000 playfield bounds.
# Where the table uses a named collision wall rather than a switch object, its
# wall/primitive center is the disclosed assembly projection.
INPUT_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.091, 0.5565)], 2: [(0.104, 0.524)], 3: [(0.117, 0.4905)],
	6: [(0.233, 0.109375)], 7: [(0.316, 0.099125)], 8: [(0.4005, 0.087375)], 9: [(0.4845, 0.077875)],
	10: [(0.859, 0.5645)], 11: [(0.846, 0.5295)], 12: [(0.834, 0.4975)],
	17: [(0.4105, 0.97175)], 18: [(0.4745, 0.9745)], 19: [(0.5385, 0.9775)], 20: [(0.601, 0.9805)],
	21: [(0.664, 0.979)],
	23: [(0.91225, 0.877062)], 24: [(0.092125, 0.755656)], 25: [(0.161625, 0.737156)],
	26: [(0.25922, 0.72851)], 27: [(0.66497, 0.73018)], 28: [(0.762625, 0.739156)], 29: [(0.832625, 0.758156)],
	30: [(0.2005, 0.170875)], 31: [(0.4495, 0.152375)], 32: [(0.3425, 0.230375)],
	33: [(0.727, 0.466625)], 34: [(0.6495, 0.448625)], 35: [(0.5675, 0.436125)],
	36: [(0.4675, 0.430125)], 37: [(0.3005, 0.442625)], 38: [(0.231875, 0.455875)], 39: [(0.3855, 0.432625)],
	41: [(0.181, 0.397875)], 42: [(0.246, 0.212125)], 43: [(0.243, 0.2165)],
	44: [(0.1095, 0.113)], 45: [(0.905, 0.08975)], 46: [(0.676, 0.184062)], 48: [(0.922, 0.155125)],
	50: [(0.91825, 0.598562)], 51: [(0.39875, 0.383063)], 53: [(0.6505, 0.224875)],
	54: [(0.268, 0.27)], 55: [(0.322, 0.2625)], 56: [(0.79125, 0.314063)], 57: [(0.66325, 0.295813)],
}

EOS_POSITIONS = {
	81: [(0.6175, 0.8415)], 83: [(0.3075, 0.8415)],
}
MICK_HIT_POSITIONS = [
	("home", 0.727, 0.466625), ("pos2", 0.6495, 0.448625), ("pos3", 0.5675, 0.436125),
	("pos4", 0.4675, 0.430125), ("park", 0.3855, 0.432625), ("pos6", 0.3005, 0.442625),
	("away", 0.231875, 0.455875),
]

# The Standard sibling discloses this manual-ordered trough-region projection
# for the downstream SW22 jam opto. The LE table has no SW22 object, so this is
# reused only as derived sibling/manual geometry, not as an exact VPX center.
SW22_POSITION = (0.727167, 0.982)
SW22_POSITION_SOURCES = (VPX_TABLE_SOURCE, MANUAL_SOURCE)

SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.664, 0.979)], 2: [(0.916, 0.92625)],
	3: [(0.640092, 0.242232)], 4: [(0.640092, 0.242232)],
	5: [(0.306, 0.5205)], 6: [(0.167, 0.071)], 7: [(0.622, 0.5205)],
	9: [(0.2005, 0.170875)], 10: [(0.4495, 0.152375)], 11: [(0.3425, 0.230375)],
	13: [(0.25922, 0.72851)], 14: [(0.66497, 0.73018)],
	15: [(0.3075, 0.8415)], 16: [(0.6175, 0.8415)],
	17: [(0.116842, 0.65142)], 18: [(0.466, 0.615)], 19: [(0.466, 0.615)],
	30: [(0.461978, 0.868472)], 32: [(0.815842, 0.65592)],
}

FLASHER_POSITIONS: dict[int, list[tuple[float, float]]] = {
	22: [(0.0925, 0.19925)], 23: [(0.7785, 0.15725)],
	25: [(0.6185, 0.18175)],
	26: [(0.3235, 0.1635)],
	27: [(0.2075, 0.21225)],
	28: [(0.3545, 0.25025)],
	29: [(0.1425, 0.87425), (0.8045, 0.87125)], 31: [(0.3245, 0.324875)],
}
FLASHER_QUANTITIES = {22: 1, 23: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 2, 31: 1}

LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	3: [(0.461625, 0.833656)], 4: [(0.0885, 0.69625)], 5: [(0.1625, 0.67225)], 6: [(0.76, 0.6745)], 7: [(0.834, 0.7005)],
	8: [(0.1515, 0.584313)], 9: [(0.166, 0.547813)], 10: [(0.18075, 0.511813)], 11: [(0.77725, 0.514625)],
	12: [(0.79225, 0.551125)], 13: [(0.80725, 0.587375)], 14: [(0.201, 0.424)], 15: [(0.182, 0.390125)], 16: [(0.166, 0.3535)],
	17: [(0.255, 0.37725)], 18: [(0.235, 0.343625)], 19: [(0.2185, 0.30775)], 20: [(0.536, 0.2635)],
	21: [(0.474, 0.40225)], 22: [(0.475, 0.320125)], 23: [(0.473, 0.28625)], 24: [(0.574, 0.39325)],
	25: [(0.578, 0.35675)], 26: [(0.594, 0.322625)], 27: [(0.611, 0.28575)], 28: [(0.664, 0.41475)],
	29: [(0.68, 0.380875)], 30: [(0.7005, 0.34575)], 31: [(0.2755, 0.60975)], 32: [(0.3465, 0.59525)],
	33: [(0.4225, 0.58775)], 34: [(0.4995, 0.58825)], 35: [(0.5755, 0.59575)], 36: [(0.6455, 0.61075)],
	37: [(0.657, 0.323875)], 38: [(0.7715, 0.340625)], 39: [(0.741125, 0.243781)], 40: [(0.759125, 0.210781)],
	41: [(0.803, 0.39275)], 42: [(0.828, 0.359125)], 43: [(0.854, 0.32525)], 44: [(0.220625, 0.068656)],
	45: [(0.296625, 0.058156)], 46: [(0.381625, 0.048656)], 47: [(0.460125, 0.038906)], 48: [(0.2415, 0.4865)],
	49: [(0.32, 0.47025)], 50: [(0.469, 0.46)], 51: [(0.5575, 0.46475)], 52: [(0.6335, 0.477)], 53: [(0.713, 0.496)],
	58: [(0.4605, 0.54975)], 60: [(0.202, 0.1795)], 61: [(0.451, 0.1605)], 62: [(0.346, 0.24)],
}

GI_POSITIONS = [
	("light38", 0.915, 0.254), ("light39", 0.923, 0.44), ("light37", 0.853, 0.075), ("light36", 0.305, 0.213),
	("light35", 0.097, 0.567), ("light34", 0.089, 0.357), ("light33", 0.461, 0.289), ("light4", 0.764, 0.7915),
	("light32", 0.657, 0.726), ("light31", 0.277, 0.723), ("light30", 0.911, 0.032), ("light29", 0.091, 0.041),
	("light27", 0.291, 0.255), ("light25", 0.826, 0.2295), ("light24", 0.848, 0.1475), ("light21", 0.718, 0.2015),
	("light19", 0.62, 0.1475), ("light18", 0.861, 0.5175), ("light17", 0.067, 0.5115),
	("light13", 0.877, 0.519), ("light16", 0.079, 0.535), ("light15", 0.087, 0.4355), ("light14", 0.072, 0.3665),
	("light12", 0.864, 0.4485), ("light11", 0.526, 0.0695), ("light10", 0.442, 0.0795), ("light9", 0.36, 0.0885),
	("light8", 0.274, 0.1005), ("light7", 0.19, 0.1105), ("light6", 0.166, 0.7915), ("light5", 0.254, 0.8175),
	("light3", 0.678, 0.8195), ("light2", 0.696, 0.7405), ("light28", 0.228, 0.7395), ("light41", 0.471, 0.363),
	("light40", 0.475, 0.645), ("light1", 0.253, 0.661375), ("light42", 0.673, 0.661375), ("light43", 0.21, 0.8095),
	("light45", 0.72, 0.8075),
]


def _by_binding(definition: dict[str, object], collection: str, group: str, address: int) -> dict[str, object]:
	for device in definition[collection]:
		binding = device["binding"]
		if binding["group"] == group and binding["device"] == address:
			return device
	raise KeyError(f"missing {collection} binding {group} {address}")


def _set_role(device: dict[str, object], role: str) -> None:
	roles = list(device.get("roles", []))
	if role not in roles:
		roles.append(role)
	device["roles"] = roles


def _apply_inputs(definition: dict[str, object]) -> None:
	for device in definition["inputs"]:
		binding = device["binding"]
		group = binding["group"]
		address = int(binding["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device.get("availability") == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address == 22:
			_set_role(device, "internal.trough-jam-opto")
			device.setdefault("physical", {})["location"] = "Downstream trough-jam opto at the five-ball trough/eject corridor."
			_set_role(device, "internal.trough")
			_located(device, "sensor", [SW22_POSITION], SW22_POSITION_SOURCES)
			_note(device, "The Standard sibling's manual-ordered trough-region projection is reused for the physically equivalent downstream LE SW22 jam opto. The exact LE table has no dedicated SW22 object; this is not an exact VPX coordinate and has practical uncertainty of about plus or minus 0.02 normalized x and 0.02 normalized y, so it must not be treated as a measured sensor center.")
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address])
			if address in {26, 27}:
				_note(device, "The exact table exposes the switch as a slingshot collision wall; this is the six-vertex wall-centroid assembly projection.")
			elif address in {33, 34, 35, 36, 37, 38, 39}:
				_note(device, "The exact table exposes the Moving Mick position as a named wall; this is the corresponding main-wall center. Paired render/collision layers are not enumerated as extra switches.")
		elif address == 71:
			_set_role(device, "internal.ball-detector")
			_not_applicable(device, "internal_nonvisual", MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)
		elif address in {82, 84}:
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
			_note(device, "The flipper button is a physical cabinet switch; it is not a playfield sensor and has no playfield placement.")
		elif address in EOS_POSITIONS:
			_located(device, "sensor", EOS_POSITIONS[address])
			_note(device, "The normally-closed EOS contact is located at the actual lower-flipper assembly center; this playfield point is not a claim that the leaf is surface-visible.")
		elif address in {85, 87}:
			_set_role(device, "internal.compatibility")
			_not_applicable(device, "virtual", VPX_SOURCE, CORE_SOURCE)
		elif address in {86, 88}:
			_set_role(device, "cabinet.post-button")
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, VPX_SOURCE)
		else:
			# Cabinet/service controls, tilt, and the remaining public software
			# states are useful records but have no normalized playfield point.
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		if address == 72:
			_located(device, "sensor", MICK_HIT_POSITIONS)
			_note(device, "One physical Moving Mick target-hit switch is shared by all seven sensed target positions; these are the seven exact collision-wall positions, not seven switches or render layers.")


def _apply_outputs(definition: dict[str, object]) -> None:
	for device in definition["outputs"]:
		binding = device["binding"]
		group = binding["group"]
		address = int(binding["device"])
		kind = device["kind"]
		if group == "pinmame.output.gi":
			_located(device, "emitter", GI_POSITIONS)
			device.setdefault("physical", {})["quantity"] = len(GI_POSITIONS)
			_note(device, "GI 0 is the aggregate controller callback. The 40 placements are the individual physical GI sockets represented by the exact table's GI collection after excluding Light20, which is reconciled to matrix lamp 20 at the same physical/object coordinate; FGI render layers are deliberately excluded.")
		elif kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device.get("availability") == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in {8, 24}:
			_set_role(device, "cabinet.shaker" if address == 8 else "cabinet.coin-meter")
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif group == "pinmame.output.solenoid" and address in {20, 21}:
			_set_role(device, "cabinet.rear-panel-flasher")
			device.setdefault("physical", {})["quantity"] = 1
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, VPX_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "effect", SOLENOID_POSITIONS[address])
			if address in {3, 4}:
				_note(device, "Both callbacks act on the two center-lock barriers; the shared lock-barrier centroid is the exact VPX assembly projection, not two fabricated coil centers.")
			elif address in {18, 19}:
				_note(device, "The relay effect is represented at the exact Moving Mick parent pivot. The VPX motor relay is causal control for the moving assembly, not a surface coil.")
			elif address in {5, 7}:
				_note(device, "The magnet trigger center is the exact VPX Magnet1/Magnet2 playfield point; magnetic response remains ceramic-ball dependent.")
			elif address in {17, 30, 32}:
				_note(device, "The post actuator is represented at the exact named post wall center; the raised post endpoint and ball effect remain mechanism behavior, not duplicate emitters.")
		elif group == "pinmame.output.solenoid" and address in FLASHER_POSITIONS:
			_located(device, "emitter", FLASHER_POSITIONS[address])
			device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address in {22, 23}:
				_note(device, "The exact VPX contains paired render layers at this callback; one physical flasher emitter is retained.")
			elif address in {25, 27, 28}:
				band = {25: "Ronnie/F25", 27: "Charlie/F27", 28: "Keith/F28"}[address]
				_note(device, f"Manual PDF page 55 lists one {band} flasher circuit and no multiplier; only F29 is marked X2. The retained F{address}, F{address}a, and F{address}pf objects are synchronized VPX render layers for that one physical assembly; only the primary F{address} anchor is retained and physical quantity is one.")
			elif address == 29:
				_note(device, "The official coil chart explicitly says X2. One left and one right bottom-arch emitter are retained; *_a/*_b render duplicates are excluded.")
		elif group == "pinmame.output.lamp" and address in {1, 2}:
			_set_role(device, "cabinet.start-lamp" if address == 1 else "cabinet.tournament-lamp")
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address])
			device.setdefault("physical", {})["quantity"] = 1
			if address == 20:
				_note(device, "Manual lamp-map address 20 is reconciled to the exact table's Light20 center even though the known script does not bind a separate L20 callback; this is the physical matrix location, not a new render layer.")
		elif group == "pinmame.output.lamp":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		else:
			raise ValueError(f"unreviewed LE output {group} {address} ({kind})")


def _exact_table_source() -> dict[str, object]:
	return {
		"id": VPX_TABLE_SOURCE,
		"kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/stern/the-rolling-stones-limited-edition-2011/source/local-tables-archive/The Rolling Stones (Stern 2011).vpx",
		"sha256": TABLE_SHA256,
		"locator": "Exact edition-matched VPX selected from the ordered local search: Tables (no exact match), then Tables Archive. Embedded cGameName=rsn_110h. vpxtool v0.33.3 extraction yielded 176 deterministic centered candidates from 1000x2000 bounds; the source and analysis/spatial-candidates.json are retained externally.",
		"license": "NOASSERTION",
		"attribution": "VPX table authors credited in the embedded script",
		"original_filename": "The Rolling Stones (Stern 2011).vpx",
		"rights": "NOASSERTION",
		"known_working": True,
	}


def _spatial_knowledge() -> str:
	anchor = "Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, and recreation behavior validated**"
	if LE_KNOWLEDGE.count(anchor) != 1:
		raise ValueError("Rolling Stones LE knowledge coverage anchor changed")
	text = LE_KNOWLEDGE.replace(anchor, "Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, recreation behavior, and normalized spatial placements validated**", 1)
	spatial = """## Normalized spatial model and reconciliation

Coordinates use the global player-view playfield frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron. Exact VPX centers were normalized from its 1000 x 2000 bounds after reconciling the known-working script's callback names with the official manual's physical inventory. Named walls and moving primitives are represented by their main collision/assembly center. Paired render layers are never promoted as separate hardware.

Every used physical switch has a sensor placement, including the manual-ordered derived projection for SW22 and all seven positions of the one shared Moving Mick hit switch 72. Every used physical coil, magnet, relay, and post effect has an effect placement; moving endpoints remain explicit in the mechanism inventory. Matrix lamps, flashers, and all 40 individual GI collection emitters have emitter placements. Light20 is excluded from GI because it is the same physical/object center as matrix lamp 20. The two rear-panel flashers, cabinet lamps, shaker, coin meter, tilts/service controls, virtual compatibility states, unused channels, DIP switches, and internal magnetic detector are explicit controlled non-playfield N/A records. The aggregate DMD remains a display record without a playfield coordinate in the base schema. The exact VPX's F25/F25a/F25pf, F27/F27a/F27pf, and F28/F28a/F28pf objects are synchronized render layers collapsed to one physical socket per manual circuit; manual page 55 marks only F29 X2, while F25/F27/F28 have no multiplier; output 29 retains that manual-proven X2 multiplicity.

SW22 reuses the committed Standard sibling's `(0.727167, 0.982)` manual-ordered trough-region projection because the manual establishes the same downstream jam-opto arrangement for LE/Premium and the exact LE table supplies no competing SW22 object. This is a derived physical-equivalence marker with practical uncertainty of about plus or minus 0.02 normalized x and 0.02 normalized y, never an exact VPX coordinate.

The official manual remains authoritative for LE/Premium multiplicity and edition boundary. The exact table is authoritative for edition-matched geometry only after that semantic reconciliation. The Standard definition intentionally remains spatially fail-closed and receives none of these LE coordinates.

"""
	if text.count("## Sources\n") != 1:
		raise ValueError("Rolling Stones LE knowledge sources anchor changed")
	text = text.replace("## Sources\n", spatial + "## Sources\n", 1)
	text = text.replace(
		"- `vpx.rolling-stones-le-1.0.6i`: known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`.",
		"- `vpx.rolling-stones-le-1.0.6i`: known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`; semantic and causality ground truth.",
		1,
	)
	text = text.replace(
		"- `runtime.rolling-stones-limited-edition.boot-start`: exact `rsn_110h` harness, SHA-256 `81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c`.",
		f"- `{VPU_LE_SOURCE}`: authenticated VPUniverse metadata page identifies ROM Name `rsn_110h`; identity evidence only, with no table artifact downloaded or hashed.\n- `vpx-table.rolling-stones-le-archive-2020`: exact archive VPX, SHA-256 `da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10`; embedded `rsn_110h`, exact 1000x2000 geometry, and retained 176-point candidate extraction.\n- `runtime.rolling-stones-limited-edition.boot-start`: exact `rsn_110h` harness, SHA-256 `81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c`.",
		1,
	)
	return text


def promote() -> None:
	definition = build(True)
	definition["schema_version"] = 2
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	definition["sources"].append(_exact_table_source())
	_apply_inputs(definition)
	_apply_outputs(definition)
	write_json(AUTHOR_READY_PATH, definition)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()
	write_text(KNOWLEDGE_PATH, _spatial_knowledge())


if __name__ == "__main__":
	promote()
