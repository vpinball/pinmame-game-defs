#!/usr/bin/env python3
"""Verify Star Trek's seven pinned CPU images without retaining ROM bytes.

Run with --rom-root <existing ROM zip folder> --patch-root <retained patched
images folder>. CPU addresses are file offsets for these 64 KiB images. The
byte-pattern scan is a bounded check, not a 6800 control-flow analysis.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


IMAGES = {
    "110": ("989d70e067cd322351768550549a4e2c8923132c", 0xB970),
    "117": ("96f343fcc7b0f39e0a8ec7df47cea433ad2c9119", 0xB9E2),
    "120": ("abf68c358c50bdeb36714cca0a9848e398a6f9fc", 0xBC4C),
    "200": ("0ebb16ab8b95f04a19fa4510e58c01493393d48c", 0xBD0F),
    "201": ("282c8181e60da6358ef320358575a538aa4abe8c", 0xBD47),
    "300": ("a453208a7640a39cb96947e8d3d3b2f71f85e613", 0xBD47),
    "301": ("f8dd222b5237cf4bd8bc00f32980d68d339032f9", 0xBD47),
}

# MC6800 instruction encodings, composed as instructions rather than ROM
# disassembly bytes. Operands $108F/$1091 and $2802 are CPU addresses.
OP = {"ldab_ix": 0xE6, "inx": 0x08, "ldaa_ix": 0xA6, "coma": 0x43,
      "tst_ext": 0x7D, "bne": 0x26, "staa_ext": 0xB7, "stab_ext": 0xF7,
      "ldx_imm": 0xCE, "ldab_ext": 0xF6, "aslb": 0x58, "jsr_ext": 0xBD,
      "ldx_ix": 0xEE}

EXPECTED = (
    ((0,), (1,)), ((4, 2, 1), (1, 1, 1)), ((7, 0), (1, 1)),
    ((5, 2), (1, 1)), ((0, 1, 2, 3, 4, 5, 6, 7), (1,) * 8),
    ((7, 0, 7, 0, 7, 0), (4, 1, 2, 1, 2, 1)),
    ((1, 2, 4, 4, 2, 1), (1,) * 6), ((1, 2, 4), (1, 1, 1)),
)


def image_for(revision, rom_root, patch_root):
    if revision in ("300", "301"):
        return (patch_root / f"trekcpuu.{revision}").read_bytes()
    with zipfile.ZipFile(rom_root / f"trek_{revision}.zip") as archive:
        candidates = [name for name in archive.namelist() if "cpu" in name.lower()]
        if len(candidates) != 1:
            raise ValueError(f"{revision}: expected exactly one CPU member, found {candidates}")
        return archive.read(candidates[0])


def analyze(data, expected_table=None):
    if len(data) != 65536:
        raise ValueError("CPU image must contain 65536 bytes")
    signature = bytes((OP["ldab_ix"], 0, OP["inx"], OP["ldaa_ix"], 0,
                       OP["coma"], OP["tst_ext"], 0x10, 0x91, OP["bne"], 3,
                       OP["staa_ext"], 0x28, 0x02))
    hits = [pos for pos in range(0x4000, len(data) - len(signature) + 1)
            if data.startswith(signature, pos)]
    if len(hits) != 1:
        raise ValueError(f"expected one chase routine, found {len(hits)}")
    pos = hits[0]
    # LDX #table; LDAB $108F; ASLB; JSR <revision-specific>; LDX 0,X.
    if (pos < 12 or data[pos - 12] != OP["ldx_imm"] or
            data[pos - 9:pos - 5] != bytes((OP["ldab_ext"], 0x10, 0x8F, OP["aslb"])) or
            data[pos - 5] != OP["jsr_ext"] or
            data[pos - 2:pos] != bytes((OP["ldx_ix"], 0))):
        raise ValueError("unexpected table dispatch")
    table = int.from_bytes(data[pos - 11:pos - 9], "big")
    if expected_table is not None and table != expected_table:
        raise ValueError(f"unexpected dispatch table: {table:04X}")
    if not 0x4000 <= table <= len(data) - 16:
        raise ValueError("pointer table is outside mapped ROM")
    patterns = []
    for index in range(8):
        pointer = int.from_bytes(data[table + 2 * index:table + 2 * index + 2], "big")
        if not 0x4000 <= pointer < len(data):
            raise ValueError(f"pattern {index}: pointer outside mapped ROM")
        count = data[pointer]
        if not count or pointer + 1 + 2 * count > len(data):
            raise ValueError(f"pattern {index}: invalid length")
        masks = tuple(data[pointer + 1:pointer + 1 + 2 * count:2])
        delays = tuple(data[pointer + 2:pointer + 1 + 2 * count:2])
        if (masks, delays) != EXPECTED[index]:
            raise ValueError(f"pattern {index}: unexpected values")
        patterns.append({"index": index, "address": f"{pointer:04X}",
                         "masks": masks, "delays": delays})
    # A raw extended-store opcode scan can include data and misses other
    # addressing modes; publish locations only, without claiming completeness.
    stores = [f"{i:04X}" for i in range(0x4000, len(data) - 2)
              if data[i] in (OP["staa_ext"], OP["stab_ext"])
              and data[i + 1:i + 3] == bytes((0x28, 0x02))]
    return {"routine": f"{pos:04X}", "table": f"{table:04X}",
            "patterns": patterns, "possible_extended_stores": stores}


def verify_stores(data, result):
    """Check the instruction contexts of the 11 bounded scan hits."""
    sites = [int(value, 16) for value in result["possible_extended_stores"]]
    if len(sites) != 11:
        raise ValueError("unexpected number of possible extended stores")
    if any(data[pos] != OP["stab_ext"] for pos in sites[:3]):
        raise ValueError("unexpected boot-store instructions")
    # Immediate accumulator A loads immediately preceding output stores.
    for pos, value in zip((sites[3], *sites[5:10]), (255, 255, 248, 255, 255, 255)):
        if data[pos - 2:pos] != bytes((0x86, value)):
            raise ValueError("unexpected fixed-value store")
    if data[sites[4] - 2:sites[4]] != bytes((OP["ldaa_ix"], 0)):
        raise ValueError("unexpected service-test indexed load")
    if tuple(data[sites[5] - 6:sites[5] - 2]) != (254, 253, 251, 255):
        raise ValueError("unexpected service-test data")
    if sites[10] != int(result["routine"], 16) + 11:
        raise ValueError("unexpected chase store")


def verify(rom_root, patch_root):
    result = {}
    for revision, (expected_sha1, table) in IMAGES.items():
        data = image_for(revision, rom_root, patch_root)
        if hashlib.sha1(data).hexdigest() != expected_sha1:
            raise ValueError(f"{revision}: CPU image SHA-1 does not match pinned driver")
        result[revision] = analyze(data, table)
        verify_stores(data, result[revision])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom-root", required=True, type=Path)
    parser.add_argument("--patch-root", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.rom_root, args.patch_root), indent=2))


if __name__ == "__main__":
    main()
