"""Pinned, side-effect-free PinMAME contract helper for Data East Star Wars.

The module intentionally reads only its adjacent committed JSON seed during normal operation.  It
does not discover a PinMAME checkout, inspect the environment, or regenerate a definition.  The
primary curator supplies the manual rows and retained-evidence references when integrating these
records into the physical-machine definition.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from pinmame_flipper_column import flipper_column_inputs


_SEED_PATH = Path(__file__).with_suffix(".json")
_SEED: dict[str, Any] = json.loads(_SEED_PATH.read_text(encoding="utf-8"))

PINMAME_REPOSITORY = _SEED["pinmame"]["repository"]
PINMAME_REVISION = _SEED["pinmame"]["revision"]

PINMAME_DEGAMES_SOURCE_ID = "pinmame.star-wars.1992.degames"
PINMAME_CORE_SOURCE_ID = "pinmame.star-wars.1992.core"
PINMAME_CORE_HEADER_SOURCE_ID = "pinmame.star-wars.1992.core-header"
PINMAME_S11_SOURCE_ID = "pinmame.star-wars.1992.s11"
PINMAME_S11_HEADER_SOURCE_ID = "pinmame.star-wars.1992.s11-header"
PINMAME_DEDMD_SOURCE_ID = "pinmame.star-wars.1992.dedmd"
PINMAME_DESOUND_SOURCE_ID = "pinmame.star-wars.1992.desound"
PINMAME_GEN_SOURCE_ID = "pinmame.star-wars.1992.gen"

PINMAME_SOURCE_IDS = (
    PINMAME_DEGAMES_SOURCE_ID,
    PINMAME_CORE_SOURCE_ID,
    PINMAME_CORE_HEADER_SOURCE_ID,
    PINMAME_S11_SOURCE_ID,
    PINMAME_S11_HEADER_SOURCE_ID,
    PINMAME_DEDMD_SOURCE_ID,
    PINMAME_DESOUND_SOURCE_ID,
    PINMAME_GEN_SOURCE_ID,
)

# These source IDs already exist in the Star Wars base definition.  They are constants so a
# caller using a successor manual or runtime record can replace them explicitly rather than the
# helper guessing a source location.
OPERATORS_MANUAL_SOURCE_ID = "manual.star-wars-1992.operators"
SCHEMATICS_MANUAL_SOURCE_ID = "manual.star-wars-1992.schematics"
VPW_SCRIPT_SOURCE_ID = "vpx-script.star-wars-1992.vpw-1-2-2"
DEFAULT_MANUAL_SOURCE_IDS = (OPERATORS_MANUAL_SOURCE_ID, SCHEMATICS_MANUAL_SOURCE_ID)
DEFAULT_RUNTIME_SOURCE_IDS = (VPW_SCRIPT_SOURCE_ID,)

INITIALIZER_DECLARATION = _SEED["initializer"]["declaration"]
FLIPPER_PAIR = (
    _SEED["initializer"]["flipper_switches"]["left"],
    _SEED["initializer"]["flipper_switches"]["right"],
)
MUX_RELAY_SOLENOID = _SEED["initializer"]["mux_relay_solenoid"]

SWITCH_ADDRESSES = (-7, -6, *range(1, 65), *range(81, 89))
MATRIX_SWITCH_ADDRESSES = tuple(range(1, 65))
FLIPPER_COLUMN_ADDRESSES = tuple(range(81, 89))
DIP_ADDRESSES = (0,)
SOLENOID_ADDRESSES = tuple(range(1, 65))
LAMP_ADDRESSES = tuple(range(1, 65))

FACTORY_UNUSED_MATRIX_SWITCHES = frozenset((8, 9, 18, 49, *range(52, 65)))
CABINET_MATRIX_SWITCHES = frozenset((1, 2, 3, 4, 5, 6, 7, 15, 16, 50, 51))
UNREACHABLE_FLIPPER_COLUMN_SWITCHES = frozenset((81, 83, 85, 86, 87, 88))
PHYSICAL_SOLENOID_CANDIDATES = frozenset((*range(1, 13), 15, 16, *range(17, 23), *range(25, 33)))

_INPUT_CORE_REFS = (
    PINMAME_DEGAMES_SOURCE_ID,
    PINMAME_CORE_SOURCE_ID,
    PINMAME_CORE_HEADER_SOURCE_ID,
    PINMAME_S11_SOURCE_ID,
    PINMAME_S11_HEADER_SOURCE_ID,
)
_OUTPUT_CORE_REFS = (
    PINMAME_DEGAMES_SOURCE_ID,
    PINMAME_CORE_SOURCE_ID,
    PINMAME_CORE_HEADER_SOURCE_ID,
    PINMAME_S11_SOURCE_ID,
)

_SOURCE_LOCATORS = {
    "src/wpc/degames.c": (
        "829-925: Star Wars comment, exact INITGAMES11 declaration, and all eleven "
        "DE_ROMSTARTx0/DE_DMD32ROM*/DE2S_SOUNDROM042 manifests"
    ),
    "src/wpc/core.c": (
        "1778-1858: core_updateSw flipper-column copies and synthetic outputs; 2186-2187: "
        "core_swSeq2m/core_m2swSeq; 2251 onward: core_getSol"
    ),
    "src/wpc/core.h": (
        "137-164: FLIP_SWNO/FLIP_SOL definitions; public switch and solenoid constants"
    ),
    "src/wpc/s11.c": (
        "372: country jumper read; 537-555, 558-579, and 618-623: Data East special-solenoid "
        "permutation/mux; 871-874 and 1188-1197: lamp/solenoid counts, printer and GI output typing"
    ),
    "src/wpc/s11.h": "30-44: DE_COMPORTS; 92-93: DE_SWADVANCE and DE_SWUPDN",
    "src/wpc/dedmd.h": "10-19: DE_DMD32ROM8x and DE_DMD32ROM44 DMD ROM layout macros",
    "src/wpc/desound.h": "90-97: DE2S_SOUNDROM042 sound-ROM layout macro",
    "src/wpc/gen.h": "25-28: GEN_DEDMD32 generation constant",
}
_SOURCE_IDS_BY_FILE = {
    "src/wpc/degames.c": PINMAME_DEGAMES_SOURCE_ID,
    "src/wpc/core.c": PINMAME_CORE_SOURCE_ID,
    "src/wpc/core.h": PINMAME_CORE_HEADER_SOURCE_ID,
    "src/wpc/s11.c": PINMAME_S11_SOURCE_ID,
    "src/wpc/s11.h": PINMAME_S11_HEADER_SOURCE_ID,
    "src/wpc/dedmd.h": PINMAME_DEDMD_SOURCE_ID,
    "src/wpc/desound.h": PINMAME_DESOUND_SOURCE_ID,
    "src/wpc/gen.h": PINMAME_GEN_SOURCE_ID,
}

_SCHEMA_OUTPUT_KINDS = frozenset({
    "coil", "flasher", "lamp", "rgb_lamp", "gi", "motor", "servo", "magnet", "relay",
    "control_signal", "virtual",
})
_PINMAME_ALIAS_NAMESPACE = {
    "pinmame.input.switch": "pinmame.switch",
    "pinmame.input.dip": "pinmame.dip",
    "pinmame.output.solenoid": "pinmame.coil",
    "pinmame.output.lamp": "pinmame.lamp",
}


def _assert_seed_contract() -> None:
    """Reject a hand-edited seed that no longer expresses the audited source contract."""
    initializer = _SEED["initializer"]
    if INITIALIZER_DECLARATION != "INITGAMES11(stwr,GEN_DEDMD32, de_128x32DMD, FLIP1516, SNDBRD_DE2S, SNDBRD_DEDMD32, 0)":
        raise RuntimeError("Star Wars seed does not contain the audited INITGAMES11 declaration")
    if FLIPPER_PAIR != (15, 16) or MUX_RELAY_SOLENOID != 10:
        raise RuntimeError("Star Wars seed does not contain the audited flipper/mux contract")
    if any(initializer[key] != 0 for key in ("custom_switch_columns", "lamp_columns", "custom_solenoids", "special_switch_solenoids")):
        raise RuntimeError("Star Wars seed must keep all audited custom counts at zero")
    if initializer["printer_line"]:
        raise RuntimeError("Star Wars seed must not enable the printer line")
    if len(_SEED["drivers"]) != 11 or {driver["id"] for driver in _SEED["drivers"]} != {
        "stwr_101", "stwr_102", "stwr_103", "stwr_104", "stwr_106", "stwr_107", "stwr_107s",
        "stwr_a046", "stwr_a14", "stwr_e12", "stwr_g11",
    }:
        raise RuntimeError("Star Wars seed must contain exactly the eleven audited drivers")


_assert_seed_contract()


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            raise ValueError("source references must be non-empty strings")
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _dedupe_aliases(aliases: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for alias in aliases:
        namespace = alias.get("namespace")
        value = alias.get("value")
        if not isinstance(namespace, str) or not isinstance(value, str) or not namespace or not value:
            raise ValueError("aliases must contain non-empty namespace and value strings")
        pair = (namespace, value)
        if pair not in seen:
            seen.add(pair)
            result.append({"namespace": namespace, "value": value})
    return result


def _base_index(records: Sequence[Mapping[str, Any]], groups: Iterable[str]) -> dict[tuple[str, int], dict[str, Any]]:
    """Index only the requested controller groups and fail rather than choose a duplicate."""
    wanted = set(groups)
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for original in records:
        if not isinstance(original, Mapping):
            raise ValueError("base records must be mappings")
        binding = original.get("binding")
        if not isinstance(binding, Mapping) or binding.get("group") not in wanted:
            continue
        group = binding["group"]
        address = binding.get("device")
        if not isinstance(address, int):
            raise ValueError(f"{group} base binding must use an integer device address")
        key = (group, address)
        if key in index:
            raise ValueError(f"duplicate base binding {group}:{address}")
        index[key] = deepcopy(dict(original))
    return index


def _record_from_base(
    index: Mapping[tuple[str, int], dict[str, Any]],
    *,
    group: str,
    address: int,
    default_id: str,
) -> dict[str, Any]:
    record = deepcopy(index.get((group, address), {}))
    record["id"] = record.get("id", default_id)
    record["binding"] = {"group": group, "device": address}
    aliases = record.get("aliases")
    if aliases is None:
        aliases = [{"namespace": _PINMAME_ALIAS_NAMESPACE[group], "value": str(address)}]
    record["aliases"] = _dedupe_aliases(aliases)
    return record


def _base_refs(record: Mapping[str, Any]) -> tuple[str, ...]:
    provenance = record.get("provenance")
    if not isinstance(provenance, Mapping):
        return ()
    refs = provenance.get("source_refs", ())
    if not isinstance(refs, Sequence) or isinstance(refs, str):
        raise ValueError("base provenance source_refs must be a sequence")
    return tuple(_dedupe(refs))


def _provenance(status: str, *refs: Iterable[str]) -> dict[str, Any]:
    return {"status": status, "source_refs": _dedupe(ref for group in refs for ref in group)}


def _not_applicable(reason: str, status: str, *refs: Iterable[str]) -> dict[str, Any]:
    return {"status": "not_applicable", "reason": reason, "provenance": _provenance(status, *refs)}


def _append_note(record: dict[str, Any], note: str, *, part: str | None = None) -> None:
    physical = deepcopy(record.get("physical", {}))
    if not isinstance(physical, dict):
        raise ValueError(f"{record['id']} physical metadata must be an object")
    previous = physical.get("notes")
    physical["notes"] = f"{previous} {note}" if previous and note not in previous else note if not previous else previous
    if part:
        physical["part_number"] = part
    record["physical"] = physical


def _static_note(record: dict[str, Any], note: str) -> None:
    record.pop("physical", None)
    _append_note(record, note)


def _rows(
    rows: Mapping[int, Mapping[str, Any]],
    *,
    name: str,
    required: Iterable[int],
    require_kind: bool = False,
    exact: bool = False,
) -> Mapping[int, Mapping[str, Any]]:
    if not isinstance(rows, Mapping):
        raise ValueError(f"{name} must be an address-to-row mapping")
    required_set = set(required)
    keys = set(rows)
    if not required_set.issubset(keys):
        missing = sorted(required_set - keys)
        raise ValueError(f"{name} is missing addresses {missing}")
    if exact and keys != required_set:
        raise ValueError(f"{name} must contain exactly addresses {sorted(required_set)}")
    for address in required_set:
        row = rows[address]
        if not isinstance(row, Mapping) or not isinstance(row.get("label"), str) or not row["label"].strip():
            raise ValueError(f"{name}[{address}] must provide a non-empty label")
        if require_kind:
            kind = row.get("kind")
            if kind not in _SCHEMA_OUTPUT_KINDS:
                raise ValueError(f"{name}[{address}] must provide a machine-schema output kind")
        part = row.get("part")
        if part is not None and (not isinstance(part, str) or not part.strip()):
            raise ValueError(f"{name}[{address}].part must be a non-empty string when provided")
    return rows


def _candidate_refs(
    record: Mapping[str, Any],
    core_refs: Iterable[str],
    manual_refs: Iterable[str],
    runtime_refs: Iterable[str] = (),
) -> tuple[str, ...]:
    return tuple(_dedupe((*core_refs, *manual_refs, *runtime_refs, *_base_refs(record))))


def _preserve_identity(record: dict[str, Any], base: Mapping[str, Any]) -> dict[str, Any]:
    """Keep a pre-existing stable ID and aliases after a shared helper built the row."""
    if base:
        record["id"] = base.get("id", record["id"])
        aliases = base.get("aliases")
        if aliases is not None:
            record["aliases"] = _dedupe_aliases(aliases)
    return record


def core_sources() -> list[dict[str, Any]]:
    """Return revision-pinned source records without touching a source checkout."""
    hashes = _SEED["pinmame"]["source_files"]
    return [
        {
            "id": _SOURCE_IDS_BY_FILE[relative],
            "kind": "pinmame_core",
            "uri": f"{PINMAME_REPOSITORY}/blob/{PINMAME_REVISION}/{relative}",
            "revision": PINMAME_REVISION,
            "sha256": hashes[relative],
            "locator": _SOURCE_LOCATORS[relative],
        }
        for relative in _SOURCE_IDS_BY_FILE
    ]


def driver_records(base_drivers: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return the eleven source-listed drivers with deliberately unresolved physical compatibility.

    ROM chip identities stay in the committed seed because the machine schema intentionally has no
    arbitrary ROM-manifest field.  The one-chip/two-chip DMD distinction is source evidence, not a
    real-board socket or compatibility conclusion.
    """
    base_by_id: dict[str, dict[str, Any]] = {}
    for driver in base_drivers:
        if not isinstance(driver, Mapping) or not isinstance(driver.get("id"), str):
            raise ValueError("base drivers must be mappings with string ids")
        driver_id = driver["id"]
        if driver_id in base_by_id:
            raise ValueError(f"duplicate base driver {driver_id}")
        base_by_id[driver_id] = deepcopy(dict(driver))

    records: list[dict[str, Any]] = []
    for source_driver in _SEED["drivers"]:
        record = deepcopy(base_by_id.get(source_driver["id"], {}))
        for key in ("id", "description", "year", "manufacturer", "flags"):
            record[key] = source_driver[key]
        if source_driver.get("root"):
            record.pop("clone_of", None)
            role = "This is PinMAME's source root for the audited Star Wars family."
        else:
            record["clone_of"] = source_driver["clone_of"]
            role = f"This source clone is rooted at {source_driver['clone_of']}."
        dmd = source_driver["roms"]["dmd"]
        record["physical_compatibility"] = "unknown"
        record["variant_notes"] = (
            f"{role} Pinned PinMAME {PINMAME_REVISION} records CPU, {dmd['macro']} DMD, and "
            "DE2 sound chips with CRC/SHA1 in tools/star_wars_pinmame.json. All eleven drivers "
            f"share {INITIALIZER_DECLARATION}. The source manifest establishes emulator routing only; "
            "physical ROM/socket compatibility remains unknown pending primary-source hardware evidence."
        )
        records.append(record)
    return records


def inputs(
    base_inputs: Sequence[Mapping[str, Any]],
    switch_rows: Mapping[int, Mapping[str, Any]],
    *,
    manual_source_refs: Iterable[str] = DEFAULT_MANUAL_SOURCE_IDS,
    runtime_source_refs: Iterable[str] = DEFAULT_RUNTIME_SOURCE_IDS,
) -> list[dict[str, Any]]:
    """Build exactly -7/-6, matrix 1-64, flipper-column 81-88, and country DIP 0.

    ``switch_rows`` is the primary curator's full factory transcription, keyed by matrix address,
    with ``label`` and ``part`` entries.  Existing records retain their semantic IDs and aliases;
    new records receive the stable IDs named by this helper.  This function deliberately omits
    ``normally_closed``: the physical contact construction remains a primary-curator decision.
    """
    switch_rows = _rows(switch_rows, name="switch_rows", required=MATRIX_SWITCH_ADDRESSES, exact=True)
    manual_refs = tuple(_dedupe(manual_source_refs))
    runtime_refs = tuple(_dedupe(runtime_source_refs))
    index = _base_index(base_inputs, ("pinmame.input.switch", "pinmame.input.dip"))
    records: list[dict[str, Any]] = []

    for address, label, default_id in ((-7, "Black Advance", "switch.advance"), (-6, "Green Up/Down", "switch.up-down")):
        record = _record_from_base(index, group="pinmame.input.switch", address=address, default_id=default_id)
        refs = _candidate_refs(record, _INPUT_CORE_REFS, manual_refs)
        record.update({
            "label": label,
            "kind": "switch",
            "availability": "used",
            "provenance": _provenance("observed", refs),
        })
        record.pop("normally_closed", None)
        _append_note(
            record,
            f"Data East service input {address}: {label}. It is a cabinet/service button, not a matrix switch; "
            "the primary curator retains physical construction and service-panel details.",
        )
        record["physical"]["location"] = "cabinet/service panel"
        record["physical"]["switch_type"] = "button"
        record["spatial"] = _not_applicable("cabinet_or_service", "observed", refs)
        records.append(record)

    for address in MATRIX_SWITCH_ADDRESSES:
        row = switch_rows[address]
        record = _record_from_base(
            index,
            group="pinmame.input.switch",
            address=address,
            default_id=f"switch.matrix-{address}",
        )
        record.update({"label": row["label"], "kind": "switch"})
        record.pop("normally_closed", None)
        part = row.get("part")
        if part == "-":
            part = None

        if address in FACTORY_UNUSED_MATRIX_SWITCHES:
            refs = _candidate_refs(record, _INPUT_CORE_REFS, manual_refs)
            record["availability"] = "unused"
            record["provenance"] = _provenance("validated", refs)
            _static_note(
                record,
                f"Factory matrix row {address} is explicitly Not Used. The exact initializer has no custom switch columns; "
                "there is no fitted controller input to place or model.",
            )
            record["spatial"] = _not_applicable("unused", "validated", refs)
        else:
            refs = _candidate_refs(record, _INPUT_CORE_REFS, manual_refs, runtime_refs)
            record["availability"] = "used"
            record["provenance"] = _provenance("observed", refs)
            note = (
                f"Factory matrix row {address}: {row['label']}. The exact initializer uses the standard Data East "
                "8x8 public matrix; this helper records an observed physical candidate only."
            )
            if address == 15:
                note += " FLIP1516 maps this left cabinet contact from flipper-column button 84 on every core_updateSw; do not drive matrix 15 directly."
            elif address == 16:
                note += " FLIP1516 maps this right cabinet contact from flipper-column button 82 on every core_updateSw; do not drive matrix 16 directly."
            _append_note(record, note, part=part)
            if address in CABINET_MATRIX_SWITCHES:
                record["physical"]["location"] = "cabinet"
                record["spatial"] = _not_applicable("cabinet_or_service", "observed", refs)
        records.append(record)

    flipper_records = flipper_column_inputs(
        flip_swno=FLIPPER_PAIR,
        flip_swno_text="FLIP1516 (FLIP_SWNO(15,16))",
        core_refs=_INPUT_CORE_REFS,
        button_refs=tuple(_dedupe((*manual_refs, *runtime_refs))),
        button_notes={
            "left": "The exact initializer declares only the lower left matrix copy at 15; no upper flipper input is declared.",
            "right": "The exact initializer declares only the lower right matrix copy at 16; no upper flipper input is declared.",
        },
        unused_notes={
            address: "FLIP1516 sets no FLIP_SOL, FLIP_EOS, or upper FLIP_SW bit, so this exact initializer cannot route the position to the ROM."
            for address in UNREACHABLE_FLIPPER_COLUMN_SWITCHES
        },
        unused_note_refs=_INPUT_CORE_REFS,
    )
    for record in flipper_records:
        address = record["binding"]["device"]
        base = index.get(("pinmame.input.switch", address), {})
        _preserve_identity(record, base)
        record.pop("normally_closed", None)
        if address in (82, 84):
            refs = _candidate_refs(base or record, _INPUT_CORE_REFS, manual_refs, runtime_refs)
            record["provenance"] = _provenance("observed", refs)
            record["spatial"] = _not_applicable("cabinet_or_service", "observed", refs)
        else:
            refs = _candidate_refs(base or record, _INPUT_CORE_REFS, ())
            record["provenance"] = _provenance("validated", refs)
            record["spatial"] = _not_applicable("unused", "validated", refs)
        records.append(record)

    dip = _record_from_base(index, group="pinmame.input.dip", address=0, default_id="dip.country-jumper")
    refs = _candidate_refs(dip, (PINMAME_S11_SOURCE_ID, PINMAME_S11_HEADER_SOURCE_ID), manual_refs)
    dip.update({
        "label": "CPU Jumper J8 (PIA 11B PA7)",
        "kind": "dip_switch",
        "availability": "used",
        "provenance": _provenance("observed", refs),
    })
    dip.pop("normally_closed", None)
    _append_note(
        dip,
        "The game's CPU sheet labels the PIA 11B PA7 ground jumper J8, factory installed (DIP 0 = 0). "
        "pia2a_r reads core_getDip(0) << 7. Its shared Williams W7 comment and S11 Germany/USA labels "
        "do not describe this Data East input: DE_COMPORTS declares no Country DIP. No country meaning is asserted. "
        "This is not an operator-DIP bank.",
    )
    dip["physical"]["location"] = "CPU board J8, PIA 11B PA7"
    dip["physical"]["switch_type"] = "dip"
    dip["spatial"] = _not_applicable("dip_switch", "observed", refs)
    records.append(dip)
    return records


def _physical_solenoid_kind(address: int, row: Mapping[str, Any]) -> str:
    forced = {8: "coil", 10: "relay", 11: "gi", 12: "motor", 15: "motor", 16: "coil"}
    expected = forced.get(address)
    if expected is not None and row["kind"] != expected:
        raise ValueError(f"coil_rows[{address}].kind must be {expected!r} for the audited Star Wars contract")
    return expected or row["kind"]


def _static_solenoid(address: int) -> tuple[str, str, str, str, tuple[str, ...]]:
    if address in (13, 14):
        return (
            f"Factory Driver {address} (No Load Fitted)", "virtual", "unused", "unused",
            (PINMAME_DEGAMES_SOURCE_ID, PINMAME_S11_SOURCE_ID),
        )
    if address == 23:
        return (
            "Game On / Flipper and Switched-Solenoid Enable", "control_signal", "used", "virtual",
            (PINMAME_CORE_SOURCE_ID, PINMAME_CORE_HEADER_SOURCE_ID, PINMAME_S11_SOURCE_ID),
        )
    if address == 24:
        return ("Reserved Solenoid 24", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    if 33 <= address <= 36:
        return (f"Unused Upper-Flipper Output {address}", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    if 37 <= address <= 44:
        return (f"Unused Printer-Line Output {address}", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    if address in (45, 46):
        return (
            f"Synthetic Right Flipper {'Power' if address == 45 else 'Hold'} State", "virtual", "used", "virtual",
            (PINMAME_CORE_SOURCE_ID, PINMAME_CORE_HEADER_SOURCE_ID),
        )
    if address in (47, 48):
        return (
            f"Synthetic Left Flipper {'Power' if address == 47 else 'Hold'} State", "virtual", "used", "virtual",
            (PINMAME_CORE_SOURCE_ID, PINMAME_CORE_HEADER_SOURCE_ID),
        )
    if address == 49:
        return ("Unavailable Simulator Shooter State", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    if address == 50:
        return ("Reserved Solenoid 50", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    if 51 <= address <= 64:
        return (f"Unused Custom Solenoid {address}", "virtual", "unused", "unused", _OUTPUT_CORE_REFS)
    raise ValueError(f"no static-solenoid description for {address}")


def _static_solenoid_note(address: int) -> str:
    if address in (13, 14):
        return (
            f"Factory schematic evidence identifies driver {address} as having no fitted load. A ROM coil-cycle test may still pulse "
            "the controllable driver; that does not make a physical device fit. This is not inferred from a VPW comment."
        )
    if address == 23:
        return "S11_GAMEONSOL / CORE_SSFLIPENSOL gates cabinet flippers and switched special solenoids; it is a meaningful virtual enable state, not a playfield coil."
    if 33 <= address <= 36:
        return "The generic upper-flipper public range is always zero for this exact Data East initializer."
    if 37 <= address <= 44:
        return "gameSpecific1 is zero in the exact initializer, so no S11_PRINTERLINE byte is published here."
    if address in (45, 46, 47, 48):
        side = "right" if address in (45, 46) else "left"
        button = 82 if side == "right" else 84
        return f"core_updateSw synthesizes this state from lower-{side} flipper-column button {button}; it is not an independent board driver or a physical winding identity."
    if address == 49:
        return "The cross-platform simulator shooter state is unavailable because this exact game has no simData."
    if address in (24, 50):
        return "This address is a reserved public controller gap and does not publish meaningful state."
    if 51 <= address <= 64:
        return "custSol is zero and the driver has no custom getter, so this public custom-solenoid address is constant zero."
    raise ValueError(f"no static-solenoid note for {address}")


def outputs(
    base_outputs: Sequence[Mapping[str, Any]],
    lamp_rows: Mapping[int, Mapping[str, Any]],
    coil_rows: Mapping[int, Mapping[str, Any]],
    *,
    manual_source_refs: Iterable[str] = DEFAULT_MANUAL_SOURCE_IDS,
    runtime_source_refs: Iterable[str] = DEFAULT_RUNTIME_SOURCE_IDS,
) -> list[dict[str, Any]]:
    """Build exactly solenoids 1-64 and lamps 1-64 from the committed controller contract.

    Physical candidates deliberately remain ``observed``.  Only core-proven virtual/unused slots
    are ``validated`` here; fitment, wiring, polarity, quantities, and playfield placement remain
    primary-curator work.  The output does not create a GI group: GI is solenoid 11.
    """
    lamp_rows = _rows(lamp_rows, name="lamp_rows", required=LAMP_ADDRESSES, exact=True)
    coil_rows = _rows(
        coil_rows,
        name="coil_rows",
        required=PHYSICAL_SOLENOID_CANDIDATES,
        require_kind=True,
    )
    if any(not isinstance(address, int) or address not in SOLENOID_ADDRESSES for address in coil_rows):
        raise ValueError("coil_rows may contain only public solenoid addresses 1-64")
    manual_refs = tuple(_dedupe(manual_source_refs))
    runtime_refs = tuple(_dedupe(runtime_source_refs))
    index = _base_index(base_outputs, ("pinmame.output.solenoid", "pinmame.output.lamp"))
    legacy_lamp_111_aliases = _dedupe_aliases(
        alias
        for original in base_outputs
        if isinstance(original, Mapping)
        and isinstance(original.get("binding"), Mapping)
        and original["binding"].get("group") == "pinmame.output.lamp"
        and original["binding"].get("device") == 111
        for alias in original.get("aliases", ())
        if isinstance(alias, Mapping) and alias.get("namespace") == "vpe-legacy.lamp"
    )

    records: list[dict[str, Any]] = []
    for address in SOLENOID_ADDRESSES:
        record = _record_from_base(
            index,
            group="pinmame.output.solenoid",
            address=address,
            default_id=f"solenoid.{address}",
        )
        if address in PHYSICAL_SOLENOID_CANDIDATES:
            row = coil_rows[address]
            refs = _candidate_refs(record, _OUTPUT_CORE_REFS, manual_refs, runtime_refs)
            record.update({
                "label": row["label"],
                "kind": _physical_solenoid_kind(address, row),
                "availability": "used",
                "provenance": _provenance("observed", refs),
            })
            note = (
                f"Public solenoid {address}: {row['label']}. Its machine-specific physical fitment, polarity, wiring, "
                "quantity, and spatial metadata remain an observed primary-curator candidate."
            )
            if address == 8:
                note += " The factory schematic identifies this output as the cabinet knocker."
            elif address == 10:
                note += " The exact INITGAMES11 data assigns K1 mux relay control to this real relay binding."
            elif address == 11:
                note += (
                    " This is the active-inverted AC GI relay on its real pinmame.output.solenoid binding; "
                    "the retained script treats it inverted. There is no PinMAME GI group."
                )
            elif 25 <= address <= 32:
                note += " K1 selects this C-side alias of A-side driver %d; it is not an independent transistor." % (address - 24)
            _append_note(record, note, part=row.get("part"))
            if address == 11 and legacy_lamp_111_aliases:
                record["aliases"] = _dedupe_aliases([*record["aliases"], *legacy_lamp_111_aliases])
                _append_note(
                    record,
                    "Only vpe-legacy.lamp aliases formerly attached to invalid lamp 111 are retained here. Lampz111 is a table-local visual collection, not a PinMAME lamp or GI address.",
                )
            elif address == 11:
                _append_note(
                    record,
                    "Lampz111 is a table-local visual collection, not a PinMAME lamp or GI address; no native lamp 111 binding is emitted.",
                )
            records.append(record)
            continue

        label, kind, availability, reason, static_refs = _static_solenoid(address)
        refs = tuple(_dedupe((*static_refs, *(manual_refs if address in (13, 14) else ()), *_base_refs(record))))
        record.update({
            "label": label,
            "kind": kind,
            "availability": availability,
            "provenance": _provenance("validated", refs),
        })
        _static_note(record, _static_solenoid_note(address))
        record["spatial"] = _not_applicable(reason, "validated", refs)
        records.append(record)

    for address in LAMP_ADDRESSES:
        row = lamp_rows[address]
        record = _record_from_base(
            index,
            group="pinmame.output.lamp",
            address=address,
            default_id=f"lamp.matrix-{address}",
        )
        record.update({"label": row["label"], "kind": "lamp"})
        part = row.get("part")
        if part == "-":
            part = None
        if address == 17:
            refs = _candidate_refs(record, (PINMAME_DEGAMES_SOURCE_ID, PINMAME_S11_SOURCE_ID), manual_refs)
            record.update({"availability": "unused", "provenance": _provenance("validated", refs)})
            _static_note(record, "Factory lamp row 17 is explicitly Not Used; the exact initializer publishes no additional lamp columns.")
            record["spatial"] = _not_applicable("unused", "validated", refs)
        else:
            refs = _candidate_refs(record, (PINMAME_DEGAMES_SOURCE_ID, PINMAME_S11_SOURCE_ID), manual_refs, runtime_refs)
            record.update({"availability": "used", "provenance": _provenance("observed", refs)})
            note = f"Factory lamp row {address}: {row['label']}. This remains an observed physical candidate pending primary curation of fitment, quantity, wiring, and placement."
            if address == 25:
                note += " This is the cabinet credit-button lamp, not a playfield coordinate."
            elif address in (29, 30):
                note += " This is a physical Death Star sphere lamp, not a virtual controller row."
            _append_note(record, note, part=part)
            if address == 25:
                record["physical"]["location"] = "cabinet credit button"
                record["spatial"] = _not_applicable("cabinet_or_service", "observed", refs)
        records.append(record)
    return records


def verify_source_checkout(source_checkout: str | Path) -> dict[str, str]:
    """Optionally verify a caller-selected PinMAME checkout against the committed seed.

    Normal helper functions never call this.  It deliberately accepts no default checkout path, so
    source verification cannot become an implicit external dependency or a regeneration step.
    """
    root = Path(source_checkout)
    if not root.is_dir():
        raise ValueError(f"source checkout is not a directory: {root}")
    actual_hashes: dict[str, str] = {}
    for relative, expected in _SEED["pinmame"]["source_files"].items():
        path = root / relative
        if not path.is_file():
            raise ValueError(f"source checkout is missing {relative}")
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"{relative} SHA-256 is {actual}, expected {expected} for {PINMAME_REVISION}")
        actual_hashes[relative] = actual

    degames = (root / "src/wpc/degames.c").read_text(encoding="utf-8")
    if INITIALIZER_DECLARATION not in degames:
        raise ValueError("degames.c does not contain the seeded exact Star Wars INITGAMES11 declaration")
    for driver in _SEED["drivers"]:
        marker = f"DE_ROMSTARTx0({driver['id']},"
        start = degames.find(marker)
        end = degames.find("DE_ROMEND", start)
        if start < 0 or end < 0:
            raise ValueError(f"degames.c does not contain a complete manifest for {driver['id']}")
        manifest = degames[start:end]
        for section in ("cpu", "dmd", "sound"):
            chips = [driver["roms"][section]] if section == "cpu" else driver["roms"][section]["chips"]
            for chip in chips:
                if chip["name"] not in manifest or f"CRC({chip['crc32']})" not in manifest or f"SHA1({chip['sha1']})" not in manifest:
                    raise ValueError(f"degames.c manifest for {driver['id']} disagrees with seed chip {chip['name']}")
    return actual_hashes
