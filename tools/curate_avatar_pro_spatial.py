"""Curate the Stern Avatar Pro 2010 definition without promoting unproven geometry."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial

from curate_avatar import (
	CORE_SOURCE,
	PRO_KNOWLEDGE,
	MANUAL_SOURCE,
	PRO_ROM_SOURCE,
	PRO_RUNTIME_SOURCE,
	VPX_SOURCE,
	VPX_TABLE_SOURCE,
	build,
)

PRO_MANUAL = MANUAL_SOURCE


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/avatar-pro-2010.json"

ARCHIVE_TABLE_SOURCE = "vpx-table.avatar-pro.archive-080116a-geometry"

# Exact VPX centers are taken from direct named objects in the selected archive
# extraction, whose normalized candidates match the independently retained VPU
# extraction. Polygon-derived target and slingshot centers are withheld.
INPUT_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.186581, 0.707801)],
	2: [(0.090089, 0.525258)], 3: [(0.101497, 0.496883)], 4: [(0.112097, 0.469522)], 5: [(0.124633, 0.441681)],
	9: [(0.128414, 0.328960)], 10: [(0.102416, 0.082506)], 11: [(0.340902, 0.060967)],
	12: [(0.431239, 0.061913)], 13: [(0.518423, 0.067114)], 14: [(0.339811, 0.266371)],
	17: [(0.453127, 0.260051)],
	24: [(0.047966, 0.743852)], 25: [(0.120071, 0.702405)],
	28: [(0.799874, 0.714500)], 29: [(0.884150, 0.747728)],
	30: [(0.310465, 0.142791)], 31: [(0.575565, 0.133134)], 32: [(0.443293, 0.214691)],
	35: [(0.889747, 0.069832)], 36: [(0.730655, 0.175925)], 37: [(0.612371, 0.263978)], 38: [(0.752508, 0.276196)],
	39: [(0.774160, 0.376832)], 40: [(0.836774, 0.422809)],
	42: [(0.598280, 0.318706)], 43: [(0.652836, 0.324586)], 44: [(0.707458, 0.330496)],
	52: [(0.941477, 0.167447)],
	83: [(0.320378, 0.831324)], 81: [(0.663720, 0.829669)],
}

# The manual and retained table establish the public jam opto 22 and shooter 23
# anchors; the known-working script corroborates their controller semantics.
# The four trough contacts remain physical/script evidence only because the
# retained geometry has no one-to-one physical switch crosswalk for them.
TROUGH_POSITIONS = {
	22: [(0.848214, 0.871661)], 23: [(0.949580, 0.881560)],
}

SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.848214, 0.871661)], 2: [(0.951090, 0.977482)], 3: [(0.621849, 0.385057)],
	9: [(0.310465, 0.142791)], 10: [(0.575565, 0.133134)], 11: [(0.443293, 0.214691)],
	15: [(0.320378, 0.831324)], 16: [(0.663720, 0.829669)],
	28: [(0.779945, 0.232257), (0.631835, 0.214576)],
	29: [(0.064306, 0.395730)], 32: [(0.963465, 0.553650)],
}

FLASHER_QUANTITIES = {
	20: 1, 21: 2, 22: 1, 23: 1, 26: 1,
	28: 2, 29: 1, 32: 1,
}
BLOCKED_INPUTS = {18, 19, 20, 21, 45, 46, 57, 58}
CONFLICTED_INPUT_POSITIONS = {7, 8, 26, 27}
BLOCKED_FLASHERS = {20, 21, 22, 23, 26}
CONFLICTED_MECHANISM_OUTPUTS = {6, 7}
CONFLICTED_PLAYFIELD_OUTPUTS = {17, 18}
CONFLICTED_FLASHERS = {25, 30, 31}
INTERNAL_NONVISUAL_OUTPUTS = {5, 13, 19}

SPATIAL_CONFLICTS = [
	{
		"id": "conflict.pro-le-target-and-sling-spatial",
		"path": "inputs[pinmame.input.switch:7|8|26|27],outputs[pinmame.output.solenoid:17|18]",
		"description": "The retained Pro table offers polygon-derived target and slingshot centers, but the reviewed Limited Edition record either disagrees materially or explicitly rejects the corresponding manually calibrated points. No polygon centroid is promoted as a physical switch or actuator placement until the cross-edition object mapping is reconciled. Resolution path: an overhead photograph or measured survey of an unrestored Pro playfield locating the two slingshot assemblies and the right standup bank, scaled against the retained manual's own to-scale playfield-underside plan on PDF page 26 (printed 'p 7', Main Playfield Bottom - Miscellaneous Parts and Brackets), whose slingshot footprints PDF page 6 already ties to LEFT SW. 26, RIGHT SW. 27 and coils Q17/Q18; or a second, independently authored known-working Pro recreation whose object centers do not descend from the single archive/VPU table lineage retained here. Unresolved.",
		"source_refs": [PRO_MANUAL, ARCHIVE_TABLE_SOURCE, VPX_SOURCE],
	},
	{
		"id": "conflict.pro-le-mechanism-spatial",
		"path": "outputs[pinmame.output.solenoid:5|6|7|13|19]",
		"description": "The Pro candidate projected relay, motor, and Link lockup channels onto shared mechanism or target anchors that the Limited Edition review rejects or places differently. Internal relay/motor loads are nonvisual and Q6/Q7 remain unlocated until the mechanism crosswalk is reconciled. Resolution path: the Link lockup assembly drawing from a complete Stern Avatar parts book, since the retained 55-page copy is a selection whose own pages cross-reference sections it does not contain (PDF page 26 points at 'the Yellow Pages, PCBs, Pages y 42 - y 43' and 'the Blue Pages, Page b 23'); or an underside photograph of an unrestored Pro playfield locating the Q6 LINK LOCKUP UP and Q7 LINK LOCKUP LATCH coils against the three 511-5249-xx relay/connector assemblies that same page already marks as item 2. Unresolved.",
		"source_refs": [PRO_MANUAL, ARCHIVE_TABLE_SOURCE, VPX_SOURCE],
	},
	{
		"id": "conflict.pro-le-flasher-quantity",
		"path": "outputs[pinmame.output.solenoid:25|30|31]",
		"description": "Q25/Q30/Q31 physical quantities inferred from Pro render objects contradict the reviewed Limited Edition record derived from the same manual. Near-co-located helper objects do not prove separate physical emitters, so quantities and placements remain withheld. Resolution path: a photograph or socket survey of an unrestored Pro playfield recording how many #89 sockets Q25, Q30 and Q31 each feed and where they sit, read against the Pro Coils Detailed Chart Table on PDF page 36 (printed 'y 2'), whose own multiplier column prints LEFT SIDE BLUE (X2) at Q30 and RIGHT SIDE BLUE (X2) at Q31 and no multiplier at Q25 POP BUMPER FLASH; the retained 55-page extract contains no flash-lamp location drawing, so a complete Stern Avatar parts book would also serve. Unresolved.",
		"source_refs": [PRO_MANUAL, ARCHIVE_TABLE_SOURCE, VPX_SOURCE],
	},
]

LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	3: [(0.490606, 0.871016)], 4: [(0.489311, 0.803019)], 5: [(0.490046, 0.775875)],
	6: [(0.490108, 0.748433)], 7: [(0.490320, 0.721313)], 8: [(0.491633, 0.694519)], 9: [(0.490593, 0.666413)],
	10: [(0.204757, 0.458810)], 11: [(0.197404, 0.486528)], 12: [(0.190051, 0.514483)], 13: [(0.183092, 0.542734)],
	14: [(0.881488, 0.671041)], 15: [(0.796750, 0.645379)], 16: [(0.718503, 0.598145)],
	17: [(0.186950, 0.658666)], 18: [(0.120206, 0.653066)], 19: [(0.048361, 0.691689)],
	21: [(0.794232, 0.563551)], 22: [(0.784566, 0.535861)], 23: [(0.205179, 0.261519)], 24: [(0.302713, 0.636794)],
	26: [(0.227358, 0.590894)], 27: [(0.546577, 0.531511)], 28: [(0.651375, 0.534054)], 29: [(0.448355, 0.489142)],
	30: [(0.568368, 0.486411)], 31: [(0.686702, 0.491590)], 32: [(0.767487, 0.501427)], 33: [(0.802111, 0.457354)],
	34: [(0.728551, 0.437536)], 35: [(0.651247, 0.435080)], 36: [(0.596263, 0.436781)], 37: [(0.549382, 0.424034)],
	38: [(0.424333, 0.443473)], 39: [(0.186908, 0.410505)], 40: [(0.343304, 0.460807)], 41: [(0.312156, 0.416686)],
	42: [(0.157942, 0.371003)], 43: [(0.392223, 0.379691)], 47: [(0.273348, 0.354630)], 48: [(0.463374, 0.291765)],
	49: [(0.473082, 0.348597)], 50: [(0.479694, 0.392849)], 51: [(0.681430, 0.273536)], 52: [(0.182784, 0.227682)],
	53: [(0.710730, 0.214331)], 54: [(0.361170, 0.095972)], 55: [(0.427346, 0.104674)], 56: [(0.503360, 0.103347)],
	57: [(0.381010, 0.624996)], 58: [(0.452981, 0.616932)], 59: [(0.530136, 0.616860)],
	60: [(0.305714, 0.141477)], 61: [(0.574984, 0.135021)], 62: [(0.448272, 0.216258)], 63: [(0.605783, 0.625215)], 64: [(0.681766, 0.636594)],
}

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament-start", 16: "cabinet.start", 65: "cabinet.coin.left", 66: "cabinet.coin.center",
	67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 84: "flipper.lower.left.button",
	82: "flipper.lower.right.button", -7: "cabinet.tilt",
	-6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}
CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker", ("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start", ("pinmame.output.lamp", 2): "cabinet.tournament",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]] | list[tuple[str, float, float]], source_refs: tuple[str, ...]) -> None:
	placements: list[dict[str, object]] = []
	for index, position in enumerate(positions, start=1):
		if len(position) == 3:
			suffix, x, y = position
			placement_suffix = f".{suffix}"
		else:
			x, y = position
			placement_suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{device['id']}.{role}{placement_suffix}", "role": role, "space": "playfield", "x": x, "y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def _located_sources(*refs: str) -> tuple[str, ...]:
	return tuple(refs)


def apply_spatial(definition: dict[str, object]) -> None:
	if any("spatial" in device for device in [*definition["inputs"], *definition["outputs"]]):
		raise ValueError("Avatar Pro spatial curation requires a fresh build(False) definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PRO_MANUAL)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL, VPX_SOURCE)
		elif address in BLOCKED_INPUTS:
			_append_note(device, "Spatial placement is intentionally withheld: the working script and manual establish the switch identity/order, but the retained geometry has no one-to-one physical switch object or defensible endpoint crosswalk.")
		elif address in CONFLICTED_INPUT_POSITIONS:
			_append_note(device, "Spatial placement is intentionally withheld because the retained Pro polygon-derived center conflicts with or is explicitly rejected by the reviewed Limited Edition record. A physical target or sling crosswalk is required before promotion.")
		elif address in TROUGH_POSITIONS:
			_located(device, "sensor", TROUGH_POSITIONS[address], _located_sources(PRO_MANUAL, ARCHIVE_TABLE_SOURCE, VPX_SOURCE))
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], _located_sources(ARCHIVE_TABLE_SOURCE, VPX_SOURCE))
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		else:
			raise ValueError(f"Avatar Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE, PRO_RUNTIME_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL, PRO_ROM_SOURCE)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		elif group == "pinmame.output.solenoid" and address in INTERNAL_NONVISUAL_OUTPUTS:
			_not_applicable(device, "internal_nonvisual", PRO_MANUAL, VPX_SOURCE)
			_append_note(device, "This relay or motor is an internal mechanism load. Its previously shared assembly or target point is rejected as a device location and is not a playfield effect placement.")
		elif group == "pinmame.output.solenoid" and address in CONFLICTED_MECHANISM_OUTPUTS:
			_append_note(device, "Spatial placement is intentionally withheld because the Pro and Limited Edition review records disagree between the Link lockup switch anchor and captive-ball assembly anchor; neither point is promoted until the shared mechanism crosswalk is reconciled.")
		elif group == "pinmame.output.solenoid" and address in CONFLICTED_PLAYFIELD_OUTPUTS:
			_append_note(device, "Spatial placement is intentionally withheld because the retained polygon-derived sling center is explicitly rejected by the reviewed Limited Edition record. No actuator point is promoted until the physical sling crosswalk is reconciled.")
		elif group == "pinmame.output.solenoid" and address in BLOCKED_FLASHERS:
			device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			_append_note(device, "Spatial placement is intentionally withheld. The manual establishes the physical flasher and multiplicity, but Q20/Q22/Q23 are rendered through Link helper passes, Q21 is a two-bulb backpanel assembly outside playfield space, and Q26 has no defensible one-to-one physical anchor in the retained candidate.")
		elif group == "pinmame.output.solenoid" and address in CONFLICTED_FLASHERS:
			device.setdefault("physical", {}).pop("quantity", None)
			_append_note(device, "Spatial placement and physical quantity are intentionally withheld. Q25/Q30/Q31 conflict with the same-manual Limited Edition record, and Q30/Q31 expose near-co-located render objects that do not prove separate physical #89 emitters.")
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			sources = _located_sources(PRO_MANUAL, ARCHIVE_TABLE_SOURCE, VPX_SOURCE)
			_located(device, role, SOLENOID_POSITIONS[address], sources)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address == 28:
				_append_note(device, "The manual multiplicity is preserved as two separate physical #89 flasher emitters; the two well-separated exact f28 table centers are used after script/manual reconciliation.")
			elif address in {29, 32}:
				_append_note(device, "The manual calls out one physical flasher. The two same-channel table helper objects are render passes of that one emitter and are represented by their center average.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], _located_sources(ARCHIVE_TABLE_SOURCE, VPX_SOURCE))
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.gi" and address == 0:
			device.setdefault("physical", {})["quantity"] = 37
			_append_note(device, "Spatial placement is intentionally withheld. The official Pro GI wiring drawing proves 27 playfield sockets plus 10 backpanel sockets on circuits BRN, YELLOW, GREEN, and VIOLET, but the 23 generic VPX GI render-pool objects have no one-to-one manual/physical crosswalk. Manual multiplicity proves quantity, not those object locations; render helpers and evenly spaced manual points are not physical sockets.")
		else:
			raise ValueError(f"Avatar Pro output {group} {address} ({kind}) has no reviewed spatial disposition")

	for display in definition["displays"]:
		display["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": _provenance(CORE_SOURCE, PRO_RUNTIME_SOURCE)}


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Avatar Pro knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)

# The previous promotion text is intentionally replaced by this fail-closed
# review note. Keep the source-specific semantic reconciliation explicit: the
# geometry table and the known-working script are byte-distinct artifacts.
SPATIAL_KNOWLEDGE = fail_closed_spatial_knowledge("stern.avatar-pro.2010", PRO_KNOWLEDGE)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Pro versus Limited Edition\n",
	"## Spatial evidence and blockers\n\nThe canonical coordinate space is normalized VPX/player view: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron end. This record remains schema-v2 partial because the exact table supplies candidate geometry, not a complete physical crosswalk. Exact direct table objects are retained only where their physical object identity, Pro edition identity, and manual/script semantics are reconciled. Cabinet/service, virtual, unused, DIP, and display devices are controlled non-playfield records.\n\nThe known-working `avr_200` script is the semantic/causality authority at SHA-256 `8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29`. The selected archive and authenticated VPU table embed a different, byte-distinct script at SHA-256 `0fa91c9232c2eca200c1598c759bd7b1dee742ccc63fb0de87105a062de4b4bd`. They reconcile on the `avr_200` identity, four-ball `InitSw` order/initial count, captive-ball switch 39, AMP/Link mechanism identities, and endpoint semantics used by this definition, but they are not byte-identical: the embedded table has additional Q9-Q11 and Q20-Q32 render callbacks and different switch/animation/audio implementation, while the known-working script carries explicit Q3/Q8/Q17-Q19 callbacks and different collision handling. The embedded script therefore remains geometry-only and never supplies a known-working implication.\n\nExplicit spatial blockers retained as physical evidence but without coordinates include trough switches 18-21, AMP bank endpoints 45/46, AMP suit endpoints 57/58, Link lockup coils Q6/Q7, the internal Q13 direction relay, Q20-Q23 and Q26 flasher helpers, and Q25/Q30/Q31. Q6/Q7 disagree with the Limited Edition record's captive-ball anchor; Q25/Q30/Q31 quantities conflict with that same-manual record, while Q30/Q31's near-co-located table objects look like render layers rather than separate bulbs. Those facts remain visible instead of being silently reconciled. GI-0 retains the manual-proven quantity of 27 playfield plus 10 backpanel sockets; the 23 generic render-pool GI objects, four hand-placed playfield points, and ten evenly spaced backpanel points are all excluded because they do not establish physical socket locations.\n\nThe retained direct lamp objects are one physical emitter per used matrix address, with Pro-unused lamp addresses and all cabinet/service controls kept as controlled non-playfield records. Q21 and Q28 retain only manual-reconciled multiplicity; Q29/Q32 collapse paired render passes to one emitter. No Limited Edition-only detector, transporter, marching leg, or bottom-arch mechanism is projected onto Pro.\n\n## Pro versus Limited Edition\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `runtime.avatar-pro.boot-start`: corrected callback-state harness evidence SHA-256 `d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7`.\n",
	"- `vpx-table.avatar-pro.archive-080116a-geometry`: selected exact archive `Avatar.vpx`, SHA-256 `aaff981437470f8c4edf6b2902e7a6d78db19d826a04d9662e3bcb812dd9740d`; embedded `avr_200` script SHA-256 `0fa91c9232c2eca200c1598c759bd7b1dee742ccc63fb0de87105a062de4b4bd`, byte-distinct from the known-working semantic script SHA-256 `8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29`; geometry-only evidence with semantic differences reconciled above.\n- `runtime.avatar-pro.boot-start`: corrected callback-state harness evidence SHA-256 `d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7`.\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"Explicit spatial blockers retained as physical evidence but without coordinates include trough switches 18-21, AMP bank endpoints 45/46, AMP suit endpoints 57/58, Link lockup coils Q6/Q7, the internal Q13 direction relay, Q20-Q23 and Q26 flasher helpers, and Q25/Q30/Q31.",
	"Explicit spatial blockers retained as physical evidence but without coordinates include trough switches 18-21, AMP bank endpoints 45/46, AMP suit endpoints 57/58, polygon-derived target and sling candidates at switches 7/8/26/27 and Q17/Q18, Link lockup coils Q6/Q7, internal relay/motor loads Q5/Q13/Q19, Q20-Q23 and Q26 flasher helpers, and Q25/Q30/Q31.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"Those facts remain visible instead of being silently reconciled.",
	"Those facts remain visible in structured unresolved-conflict records instead of being silently reconciled.",
)


def build_curated_definition() -> dict[str, object]:
	"""Build the exact fail-closed Pro artifact without writing repository state."""
	definition = build(False)
	definition["sources"].append({
		"id": ARCHIVE_TABLE_SOURCE,
		"kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/stern/avatar-pro-2010/inventory/archive/Avatar.vpx",
		"sha256": "aaff981437470f8c4edf6b2902e7a6d78db19d826a04d9662e3bcb812dd9740d",
		"known_working": False,
		"original_filename": "Avatar.vpx",
		"locator": "Exact edition-matched archive table, VPX conversion 080116a, cGameName avr_200; embedded script SHA-256 0fa91c9232c2eca200c1598c759bd7b1dee742ccc63fb0de87105a062de4b4bd is byte-distinct from the known-working semantic script SHA-256 8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29. Retained only for exact candidate geometry after limited semantic reconciliation; authenticated VPU geometry has the same embedded script hash and normalized candidate payload.",
		"license": "NOASSERTION",
		"attribution": "Table authors credited in the retained VPX table; archive copy retained for review",
		"rights": "NOASSERTION",
	})
	# Conflicts have to be attached before the downgrade, not after: the
	# downgrade is what rewrites `coverage.missing`, and it can only add
	# `unresolved_conflicts` for conflicts it can see.
	definition["conflicts"] = SPATIAL_CONFLICTS
	definition = fail_closed_spatial_partial(definition)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	apply_spatial(definition)
	return definition


def curate() -> None:
	definition = build_curated_definition()
	write_json(PARTIAL_PATH, definition)
	write_text(ROOT / "knowledge/stern/avatar-pro-2010.md", SPATIAL_KNOWLEDGE)


if __name__ == "__main__":
	curate()
