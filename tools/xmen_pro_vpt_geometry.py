"""Recover bounded coordinate fields from the exact X-Men Pro VP9 compound streams.

7-Zip extracts the compound container without interpreting its images. This reader
interprets BIFF framing, names, centers and drag points, plus the specifically
reviewed wr3 figure fields. Other records remain opaque; this is deliberately
not a full VPT parser or physical-socket resolver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import struct
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(ROOT / "src"))
from pinmame_game_defs.jsonio import write_json
from build_external_evidence_manifest import check_manifest

SOURCE_SHA256 = "00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8"
SCRIPT_SHA256 = "90cd88f121798f7c91ba738713c2aae99784751637380beb864ee3e2bcde25cb"
RAW_MANIFEST_SHA256 = "a10a88327cc1133e613b440c432448a47d45e3dcbf79b40ae5f7cf0cb951c386"
FIGURE_PNG_SHA256 = "321e5c738da86722547b45d8363258888cf9285022db76e24be35b91aa86197c"
TYPE_NAMES = {0: "Surface", 1: "Flipper", 2: "Timer", 3: "Plunger", 5: "Bumper", 6: "Trigger", 7: "Light", 8: "Kicker", 9: "Decal", 10: "Gate", 11: "Spinner", 12: "Ramp", 19: "Primitive", 20: "Flasher"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def figure_image(raw_root: Path) -> bytes:
    """Recover only Image52's declared PNG payload, excluding BIFF ENDB trailers."""
    data = (raw_root / "GameStg/Image52").read_bytes()
    if sha256(data) != "7c8ebdf0bcef23e1c3b37df647ac779984f535ddd378ff78ba0dae30ae7113f4":
        raise ValueError("wrong exact figure image stream")
    # This legacy nested image container is not a general framed-image parser.
    # The reviewed DATA tag is at192, after the literal magneto/magneto2 names.
    size = struct.unpack_from("<I", data, 188)[0]
    payload = data[196:192+size]
    if data[192:196] != b"DATA" or sha256(payload) != FIGURE_PNG_SHA256:
        raise ValueError("figure PNG payload drift")
    return payload


def records(data: bytes, start: int = 4):
    """Yield framed records including nested drag-point records, refusing overruns."""
    offset = start
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError(f"truncated BIFF header at {offset}")
        size = struct.unpack_from("<I", data, offset)[0]
        end = offset + 4 + size
        if size < 4 or end > len(data):
            raise ValueError(f"invalid BIFF size {size} at {offset}")
        tag = data[offset + 4:offset + 8].decode("ascii")
        if not all("A" <= c <= "Z" or "0" <= c <= "9" or c == "\x00" for c in tag):
            raise ValueError(f"invalid BIFF tag {tag!r}")
        yield tag, offset, data[offset + 8:end]
        if tag == "CODE":
            # Script payload has its own length, outside the CODE record.
            return
        offset = end


def point(payload: bytes) -> list[float]:
    if len(payload) != 8:
        raise ValueError("a 2D coordinate must contain exactly two binary32 values")
    result = list(struct.unpack("<ff", payload))
    if not all(math.isfinite(value) for value in result):
        raise ValueError("non-finite coordinate")
    return result


def item(data: bytes, stream: str) -> dict:
    if len(data) < 4:
        raise ValueError("missing object type")
    type_code = struct.unpack_from("<I", data)[0]
    if type_code not in TYPE_NAMES:
        raise ValueError(f"unsupported object type {type_code}")
    result = {"stream": stream, "sha256": sha256(data), "type": TYPE_NAMES[type_code]}
    if type_code == 9:
        # VP9 decals embed an unframed font payload. None is a selected anchor.
        return {**result, "excluded": "unsupported VP9 decal/font payload"}
    parsed = list(records(data))
    if not parsed or parsed[-1][0] != "ENDB" or parsed[-1][1] + 8 != len(data):
        raise ValueError(f"{stream}: missing final ENDB")
    names = [payload for tag, _, payload in parsed if tag == "NAME"]
    if len(names) != 1 or len(names[0]) < 4:
        raise ValueError(f"{stream}: expected exactly one explicit NAME")
    length = struct.unpack_from("<I", names[0])[0]
    if length != len(names[0]) - 4 or length % 2:
        raise ValueError(f"{stream}: malformed UTF-16 NAME")
    result["name"] = names[0][4:].decode("utf-16-le")
    if not result["name"] or "\x00" in result["name"]:
        raise ValueError(f"{stream}: empty or terminated NAME")
    centers = []
    points = []
    in_points = False
    pending_point = False
    fields = {}
    for tag, offset, payload in parsed:
        if tag == "DPNT":
            if payload or pending_point:
                raise ValueError(f"{stream}: malformed drag-point boundary")
            in_points = pending_point = True
        elif tag == "VCEN":
            value = point(payload)
            if in_points:
                if not pending_point:
                    raise ValueError(f"{stream}: duplicate drag-point center")
                points.append(value)
                pending_point = False
            else:
                centers.append(value)
        elif not in_points and tag in {"FLAX", "FLAY", "TMIN"}:
            if tag in fields or len(payload) != 4:
                raise ValueError(f"{stream}: duplicate/malformed {tag}")
            fields[tag] = struct.unpack("<i" if tag == "TMIN" else "<f", payload)[0]
    if pending_point or len(centers) > 1:
        raise ValueError(f"{stream}: incomplete/duplicate coordinate")
    if type_code == 20:
        if not all(tag in fields for tag in ("FLAX", "FLAY")):
            raise ValueError(f"{stream}: missing flasher sprite center")
        result["center"] = [fields["FLAX"], fields["FLAY"]]
        result["coordinate_role"] = "render sprite only; never a physical socket"
    elif centers:
        result["center"] = centers[0]
    if points:
        result["drag_points"] = points
    if "TMIN" in fields:
        result["timer_interval"] = fields["TMIN"]
    if type_code == 12 and result["name"] == "wr3":
        # This exact reviewed Ramp renders the figure photograph. Reading these
        # fields does not make other Ramps, or their centroids, physical anchors.
        wanted = {"HTBT", "HTTP", "WDBT", "WDTP", "CLDR", "RVIS", "IMAG"}
        billboard = {}
        for tag, _, payload in parsed:
            if tag not in wanted:
                continue
            if tag in billboard:
                raise ValueError(f"{stream}: duplicate figure field {tag}")
            if tag == "IMAG":
                if len(payload) < 4 or struct.unpack_from("<I", payload)[0] != len(payload)-4:
                    raise ValueError(f"{stream}: malformed figure image name")
                value = payload[4:].decode("ascii")
            else:
                if len(payload) != 4:
                    raise ValueError(f"{stream}: malformed figure field {tag}")
                value = struct.unpack("<i" if tag in {"CLDR", "RVIS"} else "<f", payload)[0]
                if not math.isfinite(value):
                    raise ValueError(f"{stream}: nonfinite figure field {tag}")
            billboard[tag] = value
        if set(billboard) != wanted:
            raise ValueError(f"{stream}: incomplete reviewed figure fields")
        result["reviewed_figure_fields"] = billboard
    return result


def recover(raw_root: Path) -> dict:
    if any(part.startswith(".incoming-") for part in raw_root.parts):
        raise ValueError("diagnostic incoming trees are not evidence")
    manifest_digest = check_manifest(raw_root, "xmn_151")
    if manifest_digest != RAW_MANIFEST_SHA256:
        raise ValueError("raw stream manifest differs from the exact retained VPT extraction")
    game = (raw_root / "GameStg/GameData").read_bytes()
    values = {}
    script = None
    for tag, offset, payload in records(game, 0):
        if tag in {"LEFT", "RGHT", "TOPX", "BOTM", "SEDT"}:
            if tag in values or len(payload) != 4:
                raise ValueError(f"duplicate/malformed GameData {tag}")
            values[tag] = struct.unpack("<I" if tag == "SEDT" else "<f", payload)[0]
        elif tag == "CODE":
            length = struct.unpack_from("<I", game, offset + 8)[0]
            script = game[offset + 12:offset + 12 + length]
            if len(script) != length or sha256(script) != SCRIPT_SHA256:
                raise ValueError("embedded script differs from exact known-working VPT")
    if values != {"LEFT": 0.0, "TOPX": 0.0, "RGHT": 959.0, "BOTM": 2162.0, "SEDT": 1702} or script is None:
        raise ValueError("unexpected bounds, item count or missing script")
    expected = {f"GameItem{n}" for n in range(values["SEDT"])}
    if {p.name for p in (raw_root / "GameStg").glob("GameItem*")} != expected:
        raise ValueError("missing or extra numbered object stream")
    items = [item((raw_root / f"GameStg/GameItem{n}").read_bytes(), f"GameStg/GameItem{n}") for n in range(values["SEDT"])]
    names = [row["name"].casefold() for row in items if "name" in row]
    if len(set(names)) != len(names):
        raise ValueError("ambiguous case-insensitive object names")
    text = "\n".join(line.split("'", 1)[0] for line in script.decode("windows-1252").splitlines())
    lamp_bindings = [{"address": int(n), "objects": [first, second]} for n, first, second in re.findall(r"(?im)^\s*FadeL\s+(\d+)\s*,\s*(\w+)\s*,\s*(\w+)\s*$", text)]
    return {
        "format": "x-men-pro-vpt-coordinate-fields", "version": 1,
        "source_sha256": SOURCE_SHA256, "script_sha256": SCRIPT_SHA256,
        "raw_manifest_sha256": manifest_digest,
        "bounds": {"left": 0.0, "top": 0.0, "right": 959.0, "bottom": 2162.0},
        "scope": "BIFF framing, explicit NAME/VCEN/FLAX/FLAY/TMIN and DPNT/VCEN; exact wr3 only also reads IMAG/HTBT/HTTP/WDBT/WDTP/CLDR/RVIS for the reviewed figure billboard. All other payloads are opaque. Three unsupported decals are retained and excluded. No socket, mesh, wiring or complete VPT semantic interpretation.",
        "script_fade_l_bindings": lamp_bindings,
        "items": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--names", nargs="+", help="retain only these exact, reviewed object names")
    args = parser.parse_args()
    recovered = recover(args.raw_root)
    if args.names:
        selected = set(args.names)
        found = {row.get("name") for row in recovered["items"]} & selected
        if found != selected:
            raise ValueError(f"missing selected names: {sorted(selected - found)}")
        recovered["extracted_item_count"] = len(recovered["items"])
        recovered["items"] = [row for row in recovered["items"] if row.get("name") in selected]
    write_json(args.output, recovered)


if __name__ == "__main__":
    main()
