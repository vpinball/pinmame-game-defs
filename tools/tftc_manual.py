"""Parsers for the hand-transcribed Tales from the Crypt manual excerpts.

The excerpts under ``evidence/excerpts/data-east.tales-from-the-crypt.1993/`` are the single source of
the printed tables: this module reads their Markdown tables back into plain data, so the definition
cannot disagree with the transcription a reader can open. Every parsed value is a string exactly as
transcribed; the curator decides what each means.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCERPT_DIR = ROOT / "evidence/excerpts/data-east.tales-from-the-crypt.1993"


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


def switch_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "switch-matrix.md")
    columns = {int(row["Column"]): row for row in table(tables, "Column drives")}
    rows = {int(row["Row"]): row for row in table(tables, "Row returns")}
    chart = {}
    for row in table(tables, "Switch Matrix Chart"):
        address = int(row["Addr"])
        column, line = int(row["Column"]), int(row["Row"])
        if address != (column - 1) * 8 + line:
            raise ValueError(f"switch {address} is not column-major position ({column}, {line})")
        chart[address] = {
            "printed": row["Printed cell"], "column": column, "row": line,
            "drive": {"transistor": columns[column]["Drive transistor"], "wire": columns[column]["Wire"], "connector": columns[column]["Connector"]},
            "return": {"wire": rows[line]["Wire"], "connector": rows[line]["Connector"]},
        }
    parts = {}
    for row in table(tables, "Switch Matrix Locations"):
        number = row["Addr"]
        address = int(number.rstrip("*"))
        part = row["Part no."]
        parts[address] = {
            "description": row["Description"], "cabinet": number.endswith("*"),
            "part": None if part in {"--", "See Cabinet"} else part, "part_printed": part,
        }
    if sorted(chart) != list(range(1, 65)) or sorted(parts) != list(range(1, 65)):
        raise ValueError("switch tables must cover addresses 1-64 exactly")
    return {"chart": chart, "parts": parts}


def lamp_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "lamp-matrix.md")
    columns = {int(row["Column"]): row for row in table(tables, "Column drives")}
    rows = {int(row["Row"]): row for row in table(tables, "Row returns")}
    chart = {}
    for row in table(tables, "Lamp Matrix Chart"):
        address = int(row["Addr"])
        column, line = int(row["Column"]), int(row["Row"])
        if address != (column - 1) * 8 + line:
            raise ValueError(f"lamp {address} is not column-major position ({column}, {line})")
        chart[address] = {
            "printed": row["Printed cell"], "column": column, "row": line,
            "drive": {"transistor": columns[column]["Drive transistor"], "wire": columns[column]["Wire"], "connector": columns[column]["Connector"]},
            "return": {"transistor": rows[line]["Return transistor"], "wire": rows[line]["Wire"], "connector": rows[line]["Connector"]},
        }
    location: dict[str, str] = {}
    for row in table(tables, "Lamp Matrix No."):
        location[row["No."]] = row["Description"]
    if sorted(chart) != list(range(1, 65)):
        raise ValueError("lamp chart must cover addresses 1-64 exactly")
    return {"chart": chart, "location": location}


def coil_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "coil-drivers.md")
    muxed = {}
    for row in table(tables, "Drives 1-8"):
        muxed[int(row["Drive"])] = row
    direct = {int(row["Drive"]): row for row in table(tables, "Drives 9-16")}
    auxiliary = {int(row["Coil number"]): row for row in table(tables, "CPU Controlled Auxiliary Solenoids")}
    flippers = {row["Coil description"]: row for row in table(tables, "Flipper Solenoids")}
    if sorted(muxed) != list(range(1, 9)) or sorted(direct) != list(range(9, 17)) or sorted(auxiliary) != list(range(17, 23)):
        raise ValueError("coil tables must cover drives 1-8, 9-16 and 17-22 exactly")
    return {"muxed": muxed, "direct": direct, "auxiliary": auxiliary, "flippers": flippers}


def bulb_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "bulbs-and-assemblies.md")
    bulbs = table(tables, "Lamp Bulbs & Sockets")
    assemblies = {row["Item"]: row for row in table(tables, "Playfield - Major Assemblies")}
    return {"bulbs": bulbs, "assemblies": assemblies}
