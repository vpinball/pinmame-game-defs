"""Read literal cells from the retained WWF Royal Rumble manual excerpts.

Each function accepts a repository ``root`` or an injected excerpt ``text``.
Rows are dictionaries keyed by the exact Markdown column headings, including
the address cell. Switch and lamp rows and wiring headings map integer printed
addresses to rows; coil rows map printed string numbers (including leading
zeroes) to rows. Flipper rows map the printed SSFB number as a string to a
list of rows in source order, since each number occurs twice. Cell padding is
removed; the cell contents are otherwise unchanged. These are manual values,
not public addresses or interpreted device properties.
"""

from pathlib import Path
import re


_EXCERPTS = Path("evidence/excerpts/data-east.wwf-royal-rumble.1994")
_ROOT = Path(__file__).resolve().parent.parent

_SWITCH = ("Address", "Matrix label (p28)", "Parts-list description (p29)", "Part No.")
_LAMP = ("Address", "Matrix label (p30)", "Location-table description (p31)")
_COIL = ("Coil No.", "Description p33", "Drive transistor", "Board", "D.T. control line", "Control connect", "Power line", "Power connection", "Power description", "Coil or flash type")
_FLIPPER = ("SSFB No.", "Flipper Coil", "Cabinet Switch", "Switch Drive", "Switch Return", "E.O.S.", "GND", "Flipper 50vDC Power", "Flipper 8vAC Hold", "Coil Output 50v", "Coil Output 8vAC")
_SWITCH_COLUMN = ("Column", "Drive transistor", "Drive wire", "CPU connection")
_SWITCH_ROW = ("Row", "Return wire", "CPU connection")
_LAMP_COLUMN = ("Column", "Transistor", "18V drive wire", "Connection")
_LAMP_ROW = ("Row", "Transistor", "GND return wire", "Connection")


def _source(filename, root, text):
    if text is not None:
        return text
    try:
        return ((Path(root) if root is not None else _ROOT) / _EXCERPTS / filename).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Cannot read {filename}") from exc


def _cells(line, count):
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError(f"Malformed table line: {line!r}")
    cells = tuple(cell.strip() for cell in line[1:-1].split("|"))
    if len(cells) != count or any(not cell for cell in cells):
        raise ValueError(f"Missing or extra table cell: {line!r}")
    return cells


def _table(text, headings):
    lines = text.splitlines()
    header = "| " + " | ".join(headings) + " |"
    matches = [i for i, line in enumerate(lines) if line.strip() == header]
    if len(matches) != 1:
        raise ValueError(f"Expected one table header: {headings[0]}")
    start = matches[0] + 1
    if start >= len(lines):
        raise ValueError("Missing table separator")
    separator = _cells(lines[start], len(headings))
    if any(not re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        raise ValueError("Malformed table separator")
    rows = []
    for line in lines[start + 1:]:
        if not line.strip():
            break
        rows.append(dict(zip(headings, _cells(line, len(headings)))))
    if not rows:
        raise ValueError("Missing table rows")
    return rows


def _unique(rows, field, expected, convert):
    result = {}
    for row in rows:
        raw = row[field]
        if raw not in expected:
            raise ValueError(f"Unexpected {field}: {raw!r}")
        key = convert(raw)
        if key in result:
            raise ValueError(f"Duplicate {field}: {raw!r}")
        result[key] = row
    if set(result) != {convert(value) for value in expected}:
        raise ValueError(f"Incomplete {field} table")
    return result


def _matrix(filename, headings, expected, root, text):
    rows = _table(_source(filename, root, text), headings)
    return _unique(rows, headings[0], {str(n) for n in expected}, int)


def switch_rows(root=None, *, text=None):
    """Return {printed address: {exact heading: literal cell}} for switches 1–64."""
    return _matrix("switches.md", _SWITCH, range(1, 65), root, text)


def lamp_rows(root=None, *, text=None):
    """Return {printed address: {exact heading: literal cell}} for lamps 1–64."""
    return _matrix("lamps.md", _LAMP, range(1, 65), root, text)


def coil_rows(root=None, *, text=None):
    """Return {printed coil number: {exact heading: literal cell}}."""
    rows = _table(_source("coils.md", root, text), _COIL)
    expected = {f"{n}{side}" for n in range(1, 9) for side in "LR"}
    expected.update(f"{n:02}" for n in range(9, 23))
    return _unique(rows, "Coil No.", expected, str)


def flipper_rows(root=None, *, text=None):
    """Return {printed SSFB number: [literal row dictionaries in source order]}."""
    rows = _table(_source("coils.md", root, text), _FLIPPER)
    # The printed number alone is not unique. Validate the four literal row
    # identifiers so duplicate or missing rows cannot masquerade as a pair.
    expected = {
        ("1", "Lwr. Rt. Flipper 22-1080"),
        ("1", "Lwr. Lt. Flipper 22-1080"),
        ("2", "Upr. Rt. Flipper 25-1800"),
        ("2", "Upr. Lt. Flipper 25-1800"),
    }
    seen = set()
    result = {}
    for row in rows:
        identity = (row["SSFB No."], row["Flipper Coil"])
        if identity not in expected or identity in seen:
            raise ValueError(f"Unexpected or duplicate flipper row: {identity!r}")
        seen.add(identity)
        result.setdefault(identity[0], []).append(row)
    if seen != expected:
        raise ValueError("Incomplete flipper table")
    return result


def switch_column_headings(root=None, *, text=None):
    """Return {column number: {exact heading: literal shared cell}}."""
    return _matrix("switches.md", _SWITCH_COLUMN, range(1, 9), root, text)


def switch_row_headings(root=None, *, text=None):
    """Return {row number: {exact heading: literal shared cell}}."""
    return _matrix("switches.md", _SWITCH_ROW, range(1, 9), root, text)


def lamp_column_headings(root=None, *, text=None):
    """Return {column number: {exact heading: literal shared cell}}."""
    return _matrix("lamps.md", _LAMP_COLUMN, range(1, 9), root, text)


def lamp_row_headings(root=None, *, text=None):
    """Return {row number: {exact heading: literal shared cell}}."""
    return _matrix("lamps.md", _LAMP_ROW, range(1, 9), root, text)
