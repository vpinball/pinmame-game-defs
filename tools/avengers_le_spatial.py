"""Conservative, manual-only spatial evidence for Avengers Limited Edition.

This module deliberately does not consume the locally available ``avs_170``
VPX table.  That table is a Pro table, and using its geometry for LE would
turn a useful rejection artifact into false evidence.  The coordinates below
are normalized playfield anchors reconciled to the LE manual's physical maps.
Where the manual only gives a grouped assembly, the assertion is intentionally
an assembly anchor and carries a note; it is not presented as an individual
sensor or emitter location. The upper-right-orbit address is deliberately
withheld: the manual's switch matrix grid says 58 while its physical
switch-location drawing marks the disputed coordinate 61, and the known-working
LE script drives 58 without a 61 handler.
"""

from __future__ import annotations

from copy import deepcopy


MANUAL_SOURCE = "manual.avengers-limited-edition"


def _provenance(*, status: str = "observed", refs: tuple[str, ...] = (MANUAL_SOURCE,)) -> dict:
    return {"status": status, "source_refs": list(refs)}


def _located(
    x: float,
    y: float,
    *,
    role: str = "sensor",
    note: str | None = None,
    quantity: int | None = None,
) -> dict:
    placement = {
        "id": "playfield",
        "role": role,
        "space": "playfield",
        "x": x,
        "y": y,
        "provenance": _provenance(),
    }
    physical = {}
    if note is not None:
        physical["notes"] = note
    if quantity is not None:
        physical["quantity"] = quantity
    result = {"spatial": {"placements": [placement], "status": "observed"}}
    if physical:
        result["physical"] = physical
    return result


def _located_many(
    coordinates: tuple[tuple[str, float, float], ...],
    *,
    note: str | None = None,
    quantity: int | None = None,
) -> dict:
    placements = [
        {
            "id": placement_id,
            "role": "emitter",
            "space": "playfield",
            "x": x,
            "y": y,
            "provenance": _provenance(),
        }
        for placement_id, x, y in coordinates
    ]
    result = {"spatial": {"placements": placements, "status": "observed"}}
    physical = {}
    if note is not None:
        physical["notes"] = note
    if quantity is not None:
        physical["quantity"] = quantity
    if physical:
        result["physical"] = physical
    return result


def _not_applicable(reason: str, *, role: str) -> dict:
    return {
        "spatial": {
            "status": "not_applicable",
            "reason": reason,
            "provenance": _provenance(status="validated"),
        },
        "roles": [role],
    }


# Directly readable LE switch-map anchors.  Paired optos use the physical
# assembly anchor because the manual does not separate their optical beams.
INPUT_POSITIONS: dict[int, tuple[float, float, str | None]] = {
    1: (0.116714, 0.546546, None),
    2: (0.116091, 0.519088, None),
    3: (0.116713, 0.492330, None),
    4: (0.117025, 0.464311, None),
    7: (0.128486, 0.296465, None),
    10: (0.676899, 0.117660, None),
    11: (0.763355, 0.117130, None),
    12: (0.848961, 0.115468, None),
    13: (0.660726, 0.344705, None),
    14: (0.604986, 0.322862, None),
    24: (0.041434, 0.755829, None),
    25: (0.119696, 0.737086, None),
    26: (0.223175, 0.714054, None),
    27: (0.682767, 0.718596, None),
    28: (0.771346, 0.738034, None),
    29: (0.866926, 0.754344, None),
    30: (0.678933, 0.213986, None),
    31: (0.880455, 0.192900, None),
    32: (0.803850, 0.297933, None),
    33: (0.152541, 0.086437, None),
    34: (0.919318, 0.412595, None),
    35: (0.846309, 0.523974, None),
    36: (0.847184, 0.559789, None),
    41: (0.393908, 0.220213, "Hulk wheel opto pair; manual gives the assembly, not separate beam centers"),
    42: (0.393908, 0.220213, "Hulk wheel opto pair; manual gives the assembly, not separate beam centers"),
    43: (0.136371, 0.215574, None),
    44: (0.728195, 0.369950, None),
    45: (0.536243, 0.379225, "Tesseract wheel opto pair; manual gives the assembly, not separate beam centers"),
    46: (0.536243, 0.379225, "Tesseract wheel opto pair; manual gives the assembly, not separate beam centers"),
    47: (0.097262, 0.058970, None),
    48: (0.937937, 0.163419, None),
    49: (0.866642, 0.610764, None),
    50: (0.867122, 0.583493, None),
    51: (0.867791, 0.556033, None),
    52: (0.299893, 0.259946, None),
    53: (0.358681, 0.269686, None),
    54: (0.417263, 0.279490, None),
    55: (0.477604, 0.289743, None),
    57: (0.334825, 0.193855, None),
    62: (0.267477, 0.279984, None),
    63: (0.217594, 0.106101, None),
    81: (0.623146, 0.846135, "Right flipper EOS assembly anchor"),
    83: (0.284495, 0.844890, "Left flipper EOS assembly anchor"),
}


CABINET_INPUT_ROLES = {
    -7: "cabinet.tilt",
    -6: "cabinet.slam-tilt",
    -5: "cabinet.ticket-notch",
    -3: "service.back",
    -2: "service.down",
    -1: "service.up",
    0: "service.enter",
    15: "cabinet.tournament-start",
    16: "cabinet.start",
    65: "cabinet.coin.left",
    66: "cabinet.coin.middle",
    67: "cabinet.coin.right",
    68: "cabinet.coin.aux",
    69: "cabinet.coin.fifth",
    82: "cabinet.flipper.right-button",
    84: "cabinet.flipper.left-button",
}


OUTPUT_POSITIONS: dict[int, tuple[float, float, str, str | None, int | None]] = {
    1: (0.860617, 0.869790, "effect", "Six-ball trough kicker assembly; manual does not separate the six trough contacts", 1),
    3: (0.393908, 0.220213, "effect", "Hulk wheel rotation motor assembly", 1),
    4: (0.393908, 0.220213, "effect", "Hulk wheel rotation motor assembly", 1),
    5: (0.267477, 0.279984, "effect", "Hulk eject assembly", 1),
    6: (0.116636, 0.518069, "effect", "Thor drop-target bank reset assembly", 1),
    7: (0.097262, 0.058970, "effect", "Left orbit gate assembly", 1),
    9: (0.678933, 0.213986, "effect", "Lower pop bumper assembly", 1),
    10: (0.861731, 0.191085, "effect", "Right pop bumper assembly", 1),
    11: (0.670839, 0.215243, "effect", "Left pop bumper assembly", 1),
    12: (0.867122, 0.583493, "effect", "Loki lock mechanism assembly", 1),
    13: (0.223175, 0.714054, "effect", "Left slingshot assembly", 1),
    14: (0.682767, 0.718596, "effect", "Right slingshot assembly", 1),
    15: (0.284495, 0.844890, "effect", "Left flipper assembly", 1),
    16: (0.623146, 0.846135, "effect", "Right flipper assembly", 1),
    18: (0.043766, 0.430000, "emitter", "Left side flasher assembly", 1),
    19: (0.954245, 0.490000, "emitter", "Right side flasher assembly", 1),
    21: (0.393908, 0.220213, "emitter", "Hulk flasher assembly", 1),
    25: (0.790702, 0.232974, "emitter", "Pop-bumper flasher assembly", 1),
    26: (0.536243, 0.379225, "emitter", "Tesseract flasher assembly", 1),
    51: (0.417263, 0.279490, "effect", "Center HULK bank reset assembly", 1),
    54: (0.393908, 0.220213, "effect", "Hulk magnet assembly", 1),
    56: (0.393908, 0.220213, "effect", "Hulk arms assembly", 1),
    57: (0.942910, 0.110962, "effect", "Right orbit gate assembly", 1),
}


OUTPUT_MULTIPLE_POSITIONS = {
    20: (
        ("device.slingshot-flasher.left-emitter", 0.223175, 0.714054),
        ("device.slingshot-flasher.right-emitter", 0.682767, 0.718596),
    ),
}


INTERNAL_OUTPUT_ROLES = {
    17: "internal.gi-relay",
    23: "internal.bridge-relay",
    55: "internal.gi-relay",
    58: "internal.gi-relay",
}


CABINET_OUTPUT_ROLES = {
    8: "cabinet.shaker",
    24: "cabinet.coin-meter",
    27: "cabinet.rear-panel-flasher",
    28: "cabinet.rear-panel-flasher",
    29: "cabinet.rear-panel-flasher",
    30: "cabinet.rear-panel-flasher",
    31: "cabinet.rear-panel-flasher",
    32: "cabinet.rear-panel-flasher",
}


def _address(device: dict) -> int:
    return int(device["binding"]["device"])


def _apply(device: dict, annotation: dict) -> None:
    """Merge spatial metadata without discarding existing wiring/physical data."""

    spatial = annotation["spatial"]
    placements = spatial.get("placements")
    if isinstance(placements, list):
        for placement in placements:
            if placement.get("id") == "playfield":
                placement["id"] = f"{device['id']}.placement"
    device["spatial"] = spatial
    if "physical" in annotation:
        device.setdefault("physical", {}).update(annotation["physical"])
    if "roles" in annotation:
        roles = device.setdefault("roles", [])
        for role in annotation["roles"]:
            if role not in roles:
                roles.append(role)


def apply_spatial(definition: dict) -> dict:
    """Annotate the LE definition with only defensible spatial assertions."""

    result = deepcopy(definition)
    for device in result["inputs"]:
        address = _address(device)
        if device["kind"] == "dip_switch":
            _apply(device, _not_applicable("dip_switch", role="cabinet.dip-switch"))
        elif device.get("availability") == "unused":
            _apply(device, _not_applicable("unused", role="unused"))
        elif address in CABINET_INPUT_ROLES:
            _apply(device, _not_applicable("cabinet_or_service", role=CABINET_INPUT_ROLES[address]))
        elif address in INPUT_POSITIONS:
            x, y, note = INPUT_POSITIONS[address]
            _apply(device, _located(x, y, note=note))

    for device in result["outputs"]:
        address = _address(device)
        if device.get("availability") == "unused":
            _apply(device, _not_applicable("unused", role="unused"))
        elif device["kind"] == "virtual":
            _apply(device, _not_applicable("virtual", role="virtual"))
        elif device["kind"] != "lamp" and address in INTERNAL_OUTPUT_ROLES:
            _apply(device, _not_applicable("internal_nonvisual", role=INTERNAL_OUTPUT_ROLES[address]))
        elif device["kind"] != "lamp" and address in CABINET_OUTPUT_ROLES:
            _apply(device, _not_applicable("cabinet_or_service", role=CABINET_OUTPUT_ROLES[address]))
        elif device["kind"] != "lamp" and address in OUTPUT_MULTIPLE_POSITIONS:
            _apply(
                device,
                _located_many(
                    OUTPUT_MULTIPLE_POSITIONS[address],
                    note="Shared output has two physical slingshot emitters; both manual-map emitters are retained.",
                    quantity=2,
                ),
            )
        elif device["kind"] != "lamp" and address in OUTPUT_POSITIONS:
            x, y, role, note, quantity = OUTPUT_POSITIONS[address]
            _apply(device, _located(x, y, role=role, note=note, quantity=quantity))
        elif device["kind"] == "lamp" and address in (55, 56):
            _apply(device, _not_applicable("cabinet_or_service", role="cabinet.start-or-tournament"))

    return result


def spatial_audit(definition: dict) -> dict:
    """Return a deterministic review artifact for the generated LE subset."""

    located_inputs = sorted(
        device["id"]
        for device in definition["inputs"]
        if device.get("spatial", {}).get("status") in {"observed", "validated", "candidate"}
    )
    located_outputs = sorted(
        device["id"]
        for device in definition["outputs"]
        if device.get("spatial", {}).get("status") in {"observed", "validated", "candidate"}
    )
    unresolved_inputs = sorted(
        device["id"]
        for device in definition["inputs"]
        if "spatial" not in device
    )
    unresolved_outputs = sorted(
        device["id"]
        for device in definition["outputs"]
        if "spatial" not in device
    )
    return {
        "format": "pinmame-spatial-blockers",
        "version": 1,
        "machine_id": definition["machine"]["id"],
        "coordinate_space": "playfield",
        "coordinate_convention": {"x": "left_to_right", "y": "rear_to_apron"},
        "evidence_policy": "manual-only; disputed upper-right-orbit address withheld; no Pro geometry is promoted to LE",
        "manual": {
            "source_id": MANUAL_SOURCE,
            "sha256": "4687ae0ed0ac249411deff3b0284d5c13d8fab154e430e95b6bd9f7bb82dca62",
            "pages": [63, 64, 66, 68, 117],
        },
        "promoted": {
            "inputs": located_inputs,
            "outputs": located_outputs,
        },
        "rejected_candidates": [
            {
                "organized_path": "pinmame-vpx-sources/stern/avengers-limited-edition-2012/Avengers (Stern 2012)-WIP HD neo Hulk rascalV2.vpx",
                "sha256": "1972c6bc5c032f8a2eeac30cb89c88479bc38d9f77e33bbc0893ae48795018a6",
                "rom": "avs_170",
                "disposition": "rejected_edition_mismatch",
                "reason": "The VPX script/table is Pro-family evidence; it is not the physical Limited Edition machine and cannot supply LE coordinates.",
            }
        ],
        "unresolved_blockers": [
            {
                "devices": {"inputs": [58, 61]},
                "blocker": "Unresolved LE upper-right-orbit address mapping: the official physical switch-location drawing marks the disputed coordinate as switch 61, the same manual's switch matrix grid identifies switch 58 as RIGHT ORBIT, and the known-working LE VPX script drives sw58 without a sw61 handler. Neither address receives a spatial placement or an unused classification.",
            },
            {"devices": {"inputs": [8, 9]}, "blocker": "Bridge down/up endpoint placement is not separated by a trustworthy LE spatial record."},
            {"devices": {"inputs": [17, 18, 19, 20, 21, 22, 23]}, "blocker": "Six-ball trough contacts and jam switch are grouped in the manual; individual switch centers and the jam geometry remain unlocated."},
            {"devices": {"inputs": [86]}, "blocker": "Shooter-lane switch placement is not yet reconciled to a normalized LE map coordinate."},
            {"devices": {"outputs": unresolved_outputs}, "blocker": "Used physical output placement remains missing for these addresses; no Pro coordinate was projected."},
            {"devices": {"outputs": [0]}, "blocker": "RGB GI requires physical per-emitter multiplicity and color/location reconciliation; the current schema cannot treat the relay as the emitter set."},
            {"devices": {"display": ["display.dmd"]}, "blocker": "Schema v2 has no display spatial-placement field, so DMD location cannot be recorded without a schema extension."},
            {"devices": {"outputs": [45, 46, 47, 57, 58, 59, 60, 61]}, "blocker": "LE lock lamps 45-47 and Tesseract lamps 57-61 are grouped on the LE lamp map; individual emitter locations and multiplicity are not yet reconciled."},
            {"devices": {"inputs": unresolved_inputs}, "blocker": "Remaining physical inputs lack a manual-reconciled placement or controlled non-playfield N/A assertion."},
        ],
    }
