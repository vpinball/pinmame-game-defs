"""Parsers for the hand-transcribed Last Action Hero manual and schematic excerpts.

The excerpts under ``evidence/excerpts/data-east.last-action-hero.1993/`` are the single source of the
printed tables: this module reads their Markdown tables back into plain data, so the definition cannot
disagree with the transcription a reader can open. Every parsed value is a string exactly as transcribed;
the curator decides what each means.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCERPT_DIR = ROOT / "evidence/excerpts/data-east.last-action-hero.1993"


def read_tables(path: Path) -> dict[str, list[dict[str, str]]]:
    """Every pipe table in ``path``, keyed by the nearest preceding ``##`` heading."""
    tables: dict[str, list[dict[str, str]]] = {}
    heading = ""
    header: list[str] | None = None
    for raw in path.read_bytes().decode("utf-8").split("\n"):
        line = raw.rstrip("\r")
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            header = None
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            tables.setdefault(heading, [])
            continue
        if all(re.fullmatch(r"-+", cell) for cell in cells):
            continue
        if len(cells) != len(header):
            raise ValueError(f"{path.name}: ragged table row under {heading!r}: {line}")
        tables[heading].append(dict(zip(header, cells)))
    return tables


def table(tables: dict[str, list[dict[str, str]]], prefix: str) -> list[dict[str, str]]:
    matches = [rows for heading, rows in tables.items() if heading.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one table under a heading starting {prefix!r}, found {len(matches)}")
    return matches[0]


def _wire_cell(text: str) -> tuple[str, str]:
    """Split ``GRY-BRN CN-11`` style cells into (wire, rest)."""
    wire, _, rest = text.partition(" ")
    return wire, rest


def _matrix(path: Path, kind: str) -> dict:
    tables = read_tables(path)
    columns = {int(row["Column"]): row for row in table(tables, "Column drives")}
    rows = {int(row["Row"]): row for row in table(tables, "Row returns")}
    chart = {}
    for row in table(tables, f"{kind} Matrix Chart"):
        address = int(row["Addr"])
        column, line = int(row["Column"]), int(row["Row"])
        if address != (column - 1) * 8 + line:
            raise ValueError(f"{kind.lower()} {address} is not column-major position ({column}, {line})")
        returned = {"wire": rows[line]["Wire"], "connector": rows[line]["Connector"]}
        if "Return transistor" in rows[line]:
            returned["transistor"] = rows[line]["Return transistor"]
        chart[address] = {
            "printed": row["Printed cell"], "column": column, "row": line,
            "drive": {"transistor": columns[column]["Drive transistor"], "wire": columns[column]["Wire"], "connector": columns[column]["Connector"]},
            "return": returned,
        }
    if sorted(chart) != list(range(1, 65)):
        raise ValueError(f"{kind.lower()} chart must cover addresses 1-64 exactly")
    return {"chart": chart, "tables": tables}


def switch_data() -> dict:
    data = _matrix(EXCERPT_DIR / "switch-matrix.md", "Switch")
    parts = {}
    for row in table(data.pop("tables"), "Switch Matrix Locations"):
        number = row["Addr"]
        address = int(number.rstrip("*"))
        part = row["Part no."]
        parts[address] = {
            "description": row["Description"], "cabinet": number.endswith("*"),
            "part": None if part in {"-", "See Cabinet"} else part, "part_printed": part,
        }
    if sorted(parts) != list(range(1, 65)):
        raise ValueError("switch part table must cover addresses 1-64 exactly")
    data["parts"] = parts
    return data


def lamp_data() -> dict:
    data = _matrix(EXCERPT_DIR / "lamp-matrix.md", "Lamp")
    descriptions = {int(row["Addr"]): row["Description"] for row in table(data.pop("tables"), "Lamp Number")}
    if sorted(descriptions) != list(range(1, 65)):
        raise ValueError("lamp description list must cover addresses 1-64 exactly")
    data["descriptions"] = descriptions
    return data


def coil_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "coil-drivers.md")
    muxed = {int(row["Drive"]): row for row in table(tables, "Drives 1-8")}
    direct = {int(row["Drive"]): row for row in table(tables, "Drives 9-16")}
    auxiliary = {int(row["Coil number"]): row for row in table(tables, "CPU Controlled Auxiliary Solenoids")}
    flippers = {row["Coil description"]: row for row in table(tables, "Flipper Solenoids")}
    if sorted(muxed) != list(range(1, 9)) or sorted(direct) != list(range(9, 17)) or sorted(auxiliary) != list(range(17, 23)):
        raise ValueError("coil tables must cover drives 1-8, 9-16 and 17-22 exactly")
    if sorted(flippers) != ["Left Flipper", "Right Flipper"]:
        raise ValueError(f"flipper table must name exactly the two flippers, not {sorted(flippers)}")
    return {"muxed": muxed, "direct": direct, "auxiliary": auxiliary, "flippers": flippers}


def schematic_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "schematic-book.md")
    switch_sheet = {int(row["Switch Number"].rstrip("*")): row for row in table(tables, "Playfield Switch Wiring Diagram")}
    lamp_sheet = {int(row["Lamp Number"]): row["Description"] for row in table(tables, "Playfield Lamp Wiring Diagram")}
    magnet_pins = {row["Connector pin"]: row for row in table(tables, "Magnet Control Board connections")}
    latch = {row["J1 pin"]: row for row in table(tables, "Magnet Controller Board schematic")}
    if sorted(switch_sheet) != list(range(1, 65)) or sorted(lamp_sheet) != list(range(1, 65)):
        raise ValueError("schematic switch and lamp sheets must cover addresses 1-64 exactly")
    coil_sheet = {row["Position"]: row for row in table(tables, "Coil/Flash Lamp sheet: left-set coils")}
    boosters = {row["Transistor"]: row for row in table(tables, "Coil/Flash Lamp sheet: J8 boosters")}
    flash_groups = {row["Group"]: row for row in table(tables, "Coil/Flash Lamp sheet: right-set flash lamp groups")}
    cn3 = {row["CN3 pin"]: row for row in table(tables, "CPU Board Logic Diagram CN3")}
    ppb_inputs = {row["J1 pin"]: row for row in table(tables, "PPB-1 board schematic: drive inputs")}
    if [f"J1-{n}" for n in range(1, 9)] != list(ppb_inputs)[:8]:
        raise ValueError("the PPB-1 input table must open with J1-1 to J1-8 in order")
    if sorted(coil_sheet) != sorted([f"{n}L" for n in range(1, 9)] + ["SOL 22"]):
        raise ValueError(f"the coil sheet must draw 1L-8L and SOL 22 exactly, not {sorted(coil_sheet)}")
    if sorted(boosters) != [f"Q{n}" for n in range(1, 6)] or sorted(flash_groups) != [f"{n}R" for n in range(1, 9)]:
        raise ValueError("the coil sheet must draw boosters Q1-Q5 and flash groups 1R-8R exactly")
    if sorted(cn3, key=int) != [str(n) for n in range(1, 13)]:
        raise ValueError("the CN3 table must cover pins 1-12 exactly")
    assemblies = {}
    for key, prefix in (
        ("ball_lock", "Ball Lock Assembly 500-5730-00"), ("drop_targets", "5-Bank Drop Target Assembly 500-5621-05"),
        ("lockout", "Lock Ball Assembly 500-5684-01"), ("trough", "6 Ball Switch Assembly 500-5683-01"),
    ):
        rows = table(tables, prefix)
        number = "#" if "#" in rows[0] else "Item"
        assemblies[key] = {row[number]: row for row in rows}
        if sorted(assemblies[key], key=int) != [str(n) for n in range(1, len(rows) + 1)]:
            raise ValueError(f"{prefix}: items must run 1-{len(rows)} without a gap")
    return {
        "switches": switch_sheet, "lamps": lamp_sheet, "magnet_pins": magnet_pins, "latch": latch,
        "coil_sheet": coil_sheet, "boosters": boosters, "flash_groups": flash_groups, "cn3": cn3, "ppb_inputs": ppb_inputs,
        "assemblies": assemblies,
    }


def parts_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "cabinet-and-assemblies.md")
    cabinet = {row["Item"]: row for row in table(tables, "Cabinet Parts Illustration")}
    assemblies = {row["Item"].rstrip("."): row for row in table(tables, "Playfield - Major Assemblies")}
    bulbs = {row["Item"]: row for row in table(tables, "Lamp Bulb Part Numbers")}
    diagnostic = {row["CN14 pin"]: row for row in table(tables, "Cabinet Wiring Diagram: diagnostic switches")}
    return {"cabinet": cabinet, "assemblies": assemblies, "bulbs": bulbs, "diagnostic_switches": diagnostic}
