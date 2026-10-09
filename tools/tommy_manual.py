"""Parsers for the hand-transcribed The Who's Tommy Pinball Wizard manual excerpts.

The excerpts under ``evidence/excerpts/data-east.the-who-s-tommy-pinball-wizard.1994/`` are the single
source of the printed tables: this module reads their Markdown tables back into plain data, so the
definition cannot disagree with the transcription a reader can open. Every parsed value is a string
exactly as transcribed; the curator decides what each means.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCERPT_DIR = ROOT / "evidence/excerpts/data-east.the-who-s-tommy-pinball-wizard.1994"


def read_tables(path: Path) -> dict[str, list[dict[str, str]]]:
    """Every pipe table in ``path``, keyed by the nearest preceding ``##`` heading.

    A heading that carries two tables (the lamp-board and bulb tables share one) keys the second as
    ``<heading> #2``.
    """
    tables: dict[str, list[dict[str, str]]] = {}
    heading = ""
    header: list[str] | None = None
    key = ""
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
            key = heading
            count = 2
            while key in tables:
                key = f"{heading} #{count}"
                count += 1
            tables[key] = []
            continue
        if all(re.fullmatch(r"-+", cell) for cell in cells):
            continue
        if len(cells) != len(header):
            raise ValueError(f"{path.name}: ragged table row under {heading!r}: {line}")
        tables[key].append(dict(zip(header, cells)))
    return tables


def table(tables: dict[str, list[dict[str, str]]], prefix: str, nth: int = 1) -> list[dict[str, str]]:
    """The ``nth`` table under the one heading that starts with ``prefix``."""
    suffix = "" if nth == 1 else f" #{nth}"
    matches = [rows for heading, rows in tables.items() if heading.startswith(prefix) and heading.endswith(suffix) and (nth > 1 or not re.search(r" #\d+$", heading))]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one table under a heading starting {prefix!r}, found {len(matches)}")
    return matches[0]


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
            "description": row["Description"], "marker": number[len(number.rstrip("*")):],
            "part": None if part in {"--", "See Cabinet", "(blank)"} else part, "part_printed": part,
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
    location = {}
    for row in table(tables, "Lamp Matrix No."):
        number = row["No."]
        address = int(number.rstrip("*"))
        location[address] = {"description": row["Description"], "marker": number[len(number.rstrip("*")):]}
    if sorted(chart) != list(range(1, 65)) or sorted(location) != list(range(1, 65)):
        raise ValueError("lamp tables must cover addresses 1-64 exactly")
    return {"chart": chart, "location": location}


def coil_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "coil-drivers.md")
    index = {row["Coil"]: row["Name"] for row in table(tables, "Coil test index")}
    drivers = {row["Coil"]: row for row in table(tables, "Switched, CPU Controlled")}
    flippers = {row["Coil description"]: row for row in table(tables, "Flipper Solenoids")}
    schematic = {int(row["Drive"]): row for row in table(tables, "Coil chart schematic")}
    servo_input = {int(row["P2 pin"]): row for row in table(tables, "Coil chart schematic", 2)}
    servo_output = {int(row["P1 pin"]): row for row in table(tables, "Coil chart schematic", 3)}
    expected = [f"{n}{side}" for n in range(1, 9) for side in "LR"] + [f"{n:02d}" for n in range(9, 23)]
    if sorted(drivers) != sorted(expected) or sorted(index) != sorted(expected):
        raise ValueError("coil tables must cover 1L-8R and 09-22 exactly")
    if sorted(schematic) != list(range(1, 9)):
        raise ValueError("the coil chart schematic table must cover drives 1-8 exactly")
    return {"index": index, "drivers": drivers, "flippers": flippers, "schematic": schematic, "servo_input": servo_input, "servo_output": servo_output}


def assembly_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "bulbs-and-assemblies.md")
    assemblies = {row["Item"]: row for row in table(tables, "Playfield - Major Assemblies")}
    bulbs = table(tables, "Lamp Board Layouts & Lamp Bulb Part Numbers", 2)
    return {"assemblies": assemblies, "bulbs": bulbs}
