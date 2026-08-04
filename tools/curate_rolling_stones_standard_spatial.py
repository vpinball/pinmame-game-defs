"""Promote the physical Stern The Rolling Stones Standard/Pro (2011) retrofit."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text

from curate_rolling_stones import build, STANDARD_KNOWLEDGE


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/the-rolling-stones-standard-2011.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-rolling-stones-standard-2011.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/the-rolling-stones-standard-2011.md"

TABLE_SOURCE = "vpx-table.rolling-stones-le-bound-shared-geometry"
SCRIPT_SOURCE = "vpx.rolling-stones-le-1.0.6i"
MANUAL_SOURCE = "manual.rolling-stones-standard-le.2011"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
VPU_SOURCE = "vpuniverse.rolling-stones-balutito-mod-2-0-24384"

TABLE_SOURCE_RECORD = {
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"uri": "external:pinmame-vpx-sources/stern/the-rolling-stones-standard-2011/source/local-tables-archive/The Rolling Stones (Stern 2011).vpx",
	"sha256": "da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10",
	"locator": "The Rolling Stones (Stern 2011).vpx, 56,029,184 bytes, archived local fallback and extracted with vpxtool git:v0.33.3. Its embedded rsn_110h controller and LE-only magnets, up/down posts, fifth ball, top shooter switch, and detector are rejected. Only objects proven common by the official Standard/Premium service inventory are used for normalized geometry, after semantic reconciliation against the known-working script.",
	"original_filename": "The Rolling Stones (Stern 2011).vpx",
	"known_working": False,
	"license": "NOASSERTION",
	"attribution": "Table authors credited in the embedded VPX script; source retained externally",
	"rights": "NOASSERTION",
}

VPU_SOURCE_RECORD = {
	"id": VPU_SOURCE,
	"kind": "human_review",
	"uri": "https://vpuniverse.com/files/file/24384-rolling-stones-the-stern-2011-balutitomod-20/",
	"locator": "Authenticated VPUniverse metadata page for Rolling Stones, The (Stern 2011) Balutito(MOD) 2.0; the page identifies ROM Name rsn_110h, so this candidate is explicitly disqualified as an exact Standard table and is not used for Standard geometry or bindings.",
	"license": "NOASSERTION",
	"attribution": "VPUniverse, balutito, and capnclaw",
	"acquired_at": "2026-08-04T00:00:00Z",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], *source_refs: str) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{device['id']}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": _provenance(*source_refs),
			}
		)
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	if not isinstance(physical, dict):
		physical = {}
		device["physical"] = physical
	previous = physical.get("notes")
	physical["notes"] = f"{previous} {note}" if isinstance(previous, str) and previous else note


# All values are x/1000 and y/2000 from the archived table's playfield bounds.
# Wall centroids and the moving Mick walls are kept as explicit reviewed points.
# Flasher Light.F<n>/F<n>a/F<n>pf entries are synchronized render layers, not
# independent physical sockets, and are collapsed to one manual-backed anchor.
INPUT_POSITIONS = {
	1: [(0.091000, 0.556500)], 2: [(0.104000, 0.524000)], 3: [(0.117000, 0.490500)],
	6: [(0.233000, 0.109375)], 7: [(0.316000, 0.099125)], 8: [(0.400500, 0.087375)], 9: [(0.484500, 0.077875)],
	10: [(0.859000, 0.564500)], 11: [(0.846000, 0.529500)], 12: [(0.834000, 0.497500)],
	23: [(0.912250, 0.877062)], 24: [(0.092125, 0.755656)], 25: [(0.161625, 0.737156)],
	26: [(0.259220, 0.728510)], 27: [(0.664970, 0.730180)], 28: [(0.762625, 0.739156)], 29: [(0.832625, 0.758156)],
	30: [(0.200500, 0.170875)], 31: [(0.449500, 0.152375)], 32: [(0.342500, 0.230375)],
	33: [(0.727000, 0.466625)], 34: [(0.649500, 0.448625)], 35: [(0.567500, 0.436125)], 36: [(0.467500, 0.430125)],
	37: [(0.300500, 0.442625)], 38: [(0.231875, 0.455875)], 39: [(0.385500, 0.432625)],
	41: [(0.181000, 0.397875)], 42: [(0.246000, 0.212125)], 43: [(0.243000, 0.216500)], 44: [(0.109500, 0.113000)],
	45: [(0.905000, 0.089750)], 46: [(0.676000, 0.184062)], 48: [(0.922000, 0.155125)],
	51: [(0.398750, 0.383063)], 53: [(0.650500, 0.224875)], 54: [(0.268000, 0.270000)], 55: [(0.322000, 0.262500)],
	56: [(0.791250, 0.314063)], 57: [(0.663250, 0.295813)],
	72: [(0.727000, 0.466625), (0.649500, 0.448625), (0.567500, 0.436125), (0.467500, 0.430125), (0.385500, 0.432625), (0.300500, 0.442625), (0.231875, 0.455875)],
}

TROUGH_POSITIONS = {
	18: [(0.474500, 0.974500)],
	19: [(0.538500, 0.977500)],
	20: [(0.601000, 0.980500)],
	21: [(0.664000, 0.979000)],
	# The manual's Standard switch-location drawing establishes a distinct
	# downstream jam-opto position. The LE table exposes only Kicker.SW21, so
	# this is a disclosed ordered trough-region projection, not a VPX object.
	22: [(0.727167, 0.982000)],
}

EOS_POSITIONS = {81: [(0.617500, 0.841500)], 83: [(0.307500, 0.841500)]}
FLIPPER_BUTTON_ADDRESSES = {82, 84}

BUMPERS = {30: (0.200500, 0.170875), 31: (0.449500, 0.152375), 32: (0.342500, 0.230375)}
SLINGS = {26: (0.259216, 0.728511), 27: (0.664974, 0.730178)}
FLIPPERS = {15: (0.307500, 0.841500), 16: (0.617500, 0.841500)}
MICK_PIVOT = (0.466000, 0.615000)

OUTPUT_POSITIONS = {
	1: [(0.664000, 0.979000)], 2: [(0.916000, 0.926250)], 3: [(0.640092, 0.242232)], 4: [(0.640092, 0.242232)], 6: [(0.167000, 0.071000)],
	9: [BUMPERS[30]], 10: [BUMPERS[31]], 11: [BUMPERS[32]], 13: [SLINGS[26]], 14: [SLINGS[27]],
	15: [FLIPPERS[15]], 16: [FLIPPERS[16]], 18: [MICK_PIVOT], 19: [MICK_PIVOT],
	22: [(0.092500, 0.199250)], 23: [(0.778500, 0.157250)],
	25: [(0.618500, 0.181750)],
	26: [(0.323500, 0.163500)], 27: [(0.207500, 0.212250)],
	28: [(0.354500, 0.250250)], 31: [(0.324500, 0.324875)],
}

FLASHER_ANCHOR_NOTES = {
	25: "Manual PDF page 55 lists one Q25/Ronnie flasher circuit. The retained F25, F25a, and F25pf entries are synchronized LE render layers for that one physical assembly; only the F25 assembly anchor is retained and physical quantity is one.",
	27: "Manual PDF page 55 lists one Q27/Charlie flasher circuit. The retained F27, F27a, and F27pf entries are synchronized LE render layers for that one physical assembly; only the F27 assembly anchor is retained and physical quantity is one.",
	28: "Manual PDF page 55 lists one Q28/Keith flasher circuit. The retained F28, F28a, and F28pf entries are synchronized LE render layers for that one physical assembly; only the F28 assembly anchor is retained and physical quantity is one.",
}

# The L<n> objects are the script's controller-addressed inserts. Light20 is
# the only physical lamp location absent as L20 in this archived VPX; its exact
# center is retained from the common table model and reconciled to the manual's
# lamp-20 inventory, without treating the VPX GI/render membership as semantic.
LAMP_POSITIONS = {
	3: (0.461625, 0.833656), 4: (0.088500, 0.696250), 5: (0.162500, 0.672250), 6: (0.760000, 0.674500), 7: (0.834000, 0.700500),
	8: (0.151500, 0.584313), 9: (0.166000, 0.547813), 10: (0.180750, 0.511813), 11: (0.777250, 0.514625), 12: (0.792250, 0.551125), 13: (0.807250, 0.587375),
	14: (0.201000, 0.424000), 15: (0.182000, 0.390125), 16: (0.166000, 0.353500), 17: (0.255000, 0.377250), 18: (0.235000, 0.343625), 19: (0.218500, 0.307750),
	20: (0.536000, 0.263500), 21: (0.474000, 0.402250), 22: (0.475000, 0.320125), 23: (0.473000, 0.286250), 24: (0.574000, 0.393250), 25: (0.578000, 0.356750), 26: (0.594000, 0.322625), 27: (0.611000, 0.285750), 28: (0.664000, 0.414750), 29: (0.680000, 0.380875), 30: (0.700500, 0.345750),
	31: (0.275500, 0.609750), 32: (0.346500, 0.595250), 33: (0.422500, 0.587750), 34: (0.499500, 0.588250), 35: (0.575500, 0.595750), 36: (0.645500, 0.610750), 37: (0.657000, 0.323875), 38: (0.771500, 0.340625), 39: (0.741125, 0.243781), 40: (0.759125, 0.210781), 41: (0.803000, 0.392750), 42: (0.828000, 0.359125), 43: (0.854000, 0.325250), 44: (0.220625, 0.068656), 45: (0.296625, 0.058156), 46: (0.381625, 0.048656), 47: (0.460125, 0.038906), 48: (0.241500, 0.486500), 49: (0.320000, 0.470250), 50: (0.469000, 0.460000), 51: (0.557500, 0.464750), 52: (0.633500, 0.477000), 53: (0.713000, 0.496000),
	58: (0.460500, 0.549750), 60: (0.202000, 0.179500), 61: (0.451000, 0.160500), 62: (0.346000, 0.240000),
}

GI_POSITIONS = [
	(0.915000, 0.254000), (0.923000, 0.440000), (0.853000, 0.075000), (0.305000, 0.213000), (0.097000, 0.567000), (0.089000, 0.357000), (0.461000, 0.289000), (0.764000, 0.791500), (0.657000, 0.726000), (0.277000, 0.723000), (0.911000, 0.032000), (0.091000, 0.041000), (0.291000, 0.255000), (0.826000, 0.229500), (0.848000, 0.147500), (0.718000, 0.201500), (0.620000, 0.147500), (0.861000, 0.517500), (0.067000, 0.511500), (0.877000, 0.519000), (0.079000, 0.535000), (0.087000, 0.435500), (0.072000, 0.366500), (0.864000, 0.448500), (0.526000, 0.069500), (0.442000, 0.079500), (0.360000, 0.088500), (0.274000, 0.100500), (0.190000, 0.110500), (0.166000, 0.791500), (0.254000, 0.817500), (0.678000, 0.819500), (0.696000, 0.740500), (0.228000, 0.739500), (0.471000, 0.363000), (0.475000, 0.645000), (0.253000, 0.661375), (0.673000, 0.661375), (0.210000, 0.809500), (0.720000, 0.807500),
]


def apply_spatial(definition: dict[str, object]) -> None:
	if len(GI_POSITIONS) != 40:
		raise ValueError("Rolling Stones Standard GI map must contain 40 individual common emitters after reconciling matrix lamp 20")
	for device in definition["inputs"]:  # type: ignore[index]
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in FLIPPER_BUTTON_ADDRESSES:
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif address in TROUGH_POSITIONS:
			_located(device, "sensor", TROUGH_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
			device["roles"] = [*(device.get("roles") or []), "internal.trough"]
			if address == 22:
				_append_note(device, "The official Standard switch-location drawing identifies SW22 as the downstream trough-jam opto. The retained LE script and table extraction expose no SW22 object, so this distinct point is a disclosed trough-region projection from the manual's ordered geometry, with practical uncertainty of about plus or minus 0.02 normalized x and 0.02 normalized y; it is not copied from SW21.")
		elif address in EOS_POSITIONS:
			_located(device, "sensor", EOS_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
			_append_note(device, "The normally-closed EOS contact has no standalone VPX render object; this is the accepted hidden-switch convention and a disclosed projection to the exact lower-flipper assembly center, not a cabinet control.")
		elif address in INPUT_POSITIONS and INPUT_POSITIONS[address]:
			_located(device, "sensor", INPUT_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
		elif group == "pinmame.input.switch" and (address in {15, 16, 65, 66, 67, 68, 69} or address <= 0):
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Rolling Stones Standard input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:  # type: ignore[index]
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif (group, address) == ("pinmame.output.solenoid", 8):
			device["roles"] = ["cabinet.shaker"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif (group, address) == ("pinmame.output.solenoid", 24):
			device["roles"] = ["cabinet.coin-meter"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in {20, 21}:
			device["roles"] = ["cabinet.rear-panel-flasher"]
			device.setdefault("physical", {})["quantity"] = 1
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, TABLE_SOURCE)
		elif group == "pinmame.output.solenoid" and address in OUTPUT_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", OUTPUT_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
			if len(OUTPUT_POSITIONS[address]) > 1:
				device.setdefault("physical", {})["quantity"] = len(OUTPUT_POSITIONS[address])
			if address in FLASHER_ANCHOR_NOTES:
				device.setdefault("physical", {})["quantity"] = 1
				_append_note(device, FLASHER_ANCHOR_NOTES[address])
		elif group == "pinmame.output.lamp" and address in {1, 2}:
			device["roles"] = ["cabinet.start" if address == 1 else "cabinet.tournament"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", [LAMP_POSITIONS[address]], TABLE_SOURCE, MANUAL_SOURCE)
			device.setdefault("physical", {})["quantity"] = 1
			if address == 20:
				_append_note(device, "The official lamp matrix chart identifies one physical lamp-20 socket at this center. The VPX Light20 object is also in the GI render collection at the same coordinate, so it is reconciled to this matrix lamp and excluded from the GI socket count.")
		elif group == "pinmame.output.gi" and address == 0:
			_located(device, "emitter", GI_POSITIONS, TABLE_SOURCE, MANUAL_SOURCE)
			device.setdefault("physical", {})["quantity"] = len(GI_POSITIONS)
			_append_note(device, "The 40 retained GI emitters are the common physical GI objects after excluding VPX Light20, which is reconciled to matrix lamp 20 at the same physical/object coordinate; render-collection membership is not an additional socket.")
		else:
			raise ValueError(f"Rolling Stones Standard output {group} {address} ({kind}) has no reviewed spatial disposition")

	for display in definition["displays"]:  # type: ignore[index]
		display["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": _provenance(CORE_SOURCE, MANUAL_SOURCE)}


def _knowledge() -> str:
	text = STANDARD_KNOWLEDGE.replace(
		"Coverage: **partial — normalized spatial placements pending.**",
		"Coverage: **author-ready - complete physical inventory, PinMAME bindings, mechanism causality, normalized spatial placements, wiring, and edition boundary validated**",
	)
	return text.rstrip() + """

## Normalized spatial retrofit

Coordinates use the global playfield space: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron end. The archived VPX was searched after both local table folders and before the authenticated web sources, retained externally, and extracted with vpxtool `git:v0.33.3`. It is explicitly LE-bound (`rsn_110h`), so its controller bindings and LE-only geometry are not promoted into this Standard definition.

The exact VPX centers are used only for hardware reconciled as common by the official Stern manual and the known-working script: target banks, lanes, ramps/orbits, spinner, pops, slings, flippers, center lock, controlled gate, common Mick travel, addressed inserts, and one assembly anchor for each named flasher circuit. The F25/F25a/F25pf, F27/F27a/F27pf, and F28/F28a/F28pf entries are synchronized render layers, not three physical sockets per circuit. The 40 retained GI emitters exclude VPX Light20 because that object shares the physical/object coordinate of matrix lamp 20; it is one physical device, not two sockets. The manual remains authoritative for Standard multiplicity and excludes the LE magnets, three up/down posts, fifth/ceramic ball, detector 71, top shooter switch 50, and LE-only cabinet controls.

The cabinet controls/meters/shaker, rear-panel flashers, unused channels, and DMD are explicit controlled non-playfield dispositions. The four trough ball-position contacts use the reviewed ordered trough geometry; SW22 is a distinct manual-backed trough-jam projection because the LE table/script has no SW22 object. The flipper EOS contacts use the accepted hidden-switch convention and are disclosed projections to their lower-flipper assemblies, while cabinet buttons 82/84 remain cabinet/service N/A. The shared Moving Mick hit switch carries seven endpoint placements because one physical sensor follows the moving target, and the seven position switches retain their individual detents. No Standard placement is inferred from LE-only hardware.

## Spatial evidence

- `vpx-table.rolling-stones-le-bound-shared-geometry`: retained VPX SHA-256 `da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10`; candidate packet retained under the external review-artifact directory.
- `vpx.rolling-stones-le-1.0.6i`: known-working script SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`; semantic and causality authority only.
- `manual.rolling-stones-standard-le.2011`: official Stern manual SHA-256 `1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf`; physical inventory, multiplicity, wiring, and Standard/LE boundary authority.
- `vpuniverse.rolling-stones-balutito-mod-2-0-24384`: authenticated VPUniverse metadata identifies `rsn_110h`; it is explicitly disqualified as an exact Standard table and contributes no Standard geometry or bindings.
"""


def promote() -> None:
	definition = build(False)
	definition["sources"].append(TABLE_SOURCE_RECORD)  # type: ignore[index]
	definition["sources"].append(VPU_SOURCE_RECORD)  # type: ignore[index]
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"  # type: ignore[index]
	definition["coverage"]["status"] = "author_ready"  # type: ignore[index]
	definition["coverage"]["missing"] = []  # type: ignore[index]
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"  # type: ignore[index]
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(KNOWLEDGE_PATH, _knowledge())
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
