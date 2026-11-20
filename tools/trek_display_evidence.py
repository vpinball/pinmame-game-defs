#!/usr/bin/env python3
"""Verify the retained Star Trek display comparison without exporting ROMs or frames."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

LIBRARY = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
SCENARIO = "0ecd54499f5c2bc675054052bd4c33f6c90fdd2741f698a59a549ce56b791936"
CASES = {
    "11a": {
        "archive": "4afb9a8cb8e5c38bfba222acf19af059e1d4f6f4c2d546549498824256b94184",
        "display": ("trekadsp.bin", "4251fa0568d2e869b44358471a3d4a4e88443954", b"DISPLAY: STARTREK A0.27"),
        "trace": "c587756cf32cea9bbe6acb6634a6c56433f56ab193c77c73c92eb2094b2e7195",
        "frames": ("954669a4f1a70bb961078f524e191710b181b84cf40eda4c4b0e64ee717c69da", "6dea27d4f12ff7804f7313cbc2d2beecaf01814b3256b03e50af4847e16d8eb0"),
    },
    "110": {
        "archive": "b33c2fdb6ee88b8a990e71149650855348324ab1e9caf0e5d86f3c369f58aca4",
        "display": ("trekdsp.106", "3262d6604d1dcd1dc738bc3f919a3319b783fd73", b"DISPLAY: STARTREK A1.06"),
        "trace": "6279e0088738fdc63cdef42de4baab066ced9ed0696fb8ae6e1d294f2dee5599",
        "frames": ("43cfe267080ece1fb85cbb7a6b908bf36e05bbb27d65566ee939f37e6a0ec5cc", "171d2772113a10f96a5275389b2436a94f5843fea821f3eb9d4d3d0bbfc743ce"),
    },
}
FRAME_NAMES = ("000-booted-display-0.pgm", "001-boot-and-observe-attract-display-display-0.pgm")
PRODUCTION = {
    "117": ("trekcpu.117", "96f343fcc7b0f39e0a8ec7df47cea433ad2c9119", "trekdspa.109", "d26126310b8b316ca161d4202645de8fb6359822"),
    "120": ("trekcpu.120", "abf68c358c50bdeb36714cca0a9848e398a6f9fc", "trekdsp.106", "3262d6604d1dcd1dc738bc3f919a3319b783fd73"),
    "200": ("trekcpuu.200", "0ebb16ab8b95f04a19fa4510e58c01493393d48c", "trekdspa.109", "d26126310b8b316ca161d4202645de8fb6359822"),
    "201": ("trekcpuu.201", "282c8181e60da6358ef320358575a538aa4abe8c", "trekdspa.109", "d26126310b8b316ca161d4202645de8fb6359822"),
}
SOUND = {"trek.u7": "11731170ed4f04dd8af05d8f79ad727b0e0104d7", "trek.u17": "905f34173db0e04eaf5236191186ea209b8a0a34", "trek.u21": "1f9bed9b06d5b19fbc0cc0bef2e493eb1a3f1aa4"}
LAMP_NAMES = {36: b"BACKBOX #5", 44: b"LEFT RAMP (GREEN)", 45: b"LEFT MILLION (RED)", 63: b"RIGHT MILLION (RED)", 64: b"RIGHT RAMP (GREEN)"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_ips(source: bytes, patch: bytes) -> bytes:
    require(patch[:5] == b"PATCH", "invalid IPS header")
    result = bytearray(source)
    pos = 5
    while patch[pos:pos + 3] != b"EOF":
        require(pos + 5 <= len(patch), "truncated IPS record")
        offset = int.from_bytes(patch[pos:pos + 3], "big")
        size = int.from_bytes(patch[pos + 3:pos + 5], "big")
        pos += 5
        if size:
            data = patch[pos:pos + size]
            require(len(data) == size, "truncated IPS data")
            pos += size
        else:
            require(pos + 3 <= len(patch), "truncated IPS RLE")
            count = int.from_bytes(patch[pos:pos + 2], "big")
            data = patch[pos + 2:pos + 3] * count
            pos += 3
        require(offset + len(data) <= len(result), "IPS extends input")
        result[offset:offset + len(data)] = data
    require(pos + 3 == len(patch), "unsupported IPS trailer")
    return bytes(result)


def verify_lamp_names(display: bytes) -> int:
    """Find the unique 64-entry bank-relative lamp table using five anchors."""
    def label(base: int, number: int) -> bytes:
        pos = base + (number - 1) * 2
        offset = 0x10000 + int.from_bytes(display[pos:pos + 2], "little")
        if not 0x14000 <= offset < 0x18000:
            return b""
        end = display.find(b"\0", offset, min(offset + 64, 0x18000))
        return display[offset:end] if end >= 0 else b""

    candidates = [base for base in range(0x14000, 0x18000 - 128 + 1)
                  if all(label(base, n) == name for n, name in LAMP_NAMES.items())]
    require(len(candidates) == 1, f"expected one 64-entry lamp table, found {len(candidates)}")
    base = candidates[0]
    labels = [label(base, n) for n in range(1, 65)]
    require(all(name and all(32 <= c < 127 for c in name) for name in labels), "invalid lamp table entries")
    return base


def verify(rom_root: Path, run_root: Path, patch_root: Path) -> None:
    cpus = []
    for suffix, case in CASES.items():
        archive = rom_root / f"trek_{suffix}.zip"
        require(sha256(archive) == case["archive"], f"archive changed: {archive}")
        with ZipFile(archive) as z:
            cpu = z.read("trekcpu.110")
            cpus.append(cpu)
            name, expected, version = case["display"]
            display = z.read(name)
            require(len(display) == 131072 and hashlib.sha1(display).hexdigest() == expected, f"display ROM changed: {name}")
            require(version in display and b"DOTMATRIXLIVES!!!" in display, f"display strings absent: {name}")
            print(f"{name}: 64-entry lamp table at {verify_lamp_names(display):#x}")
            for sound_name, sound_hash in SOUND.items():
                require(hashlib.sha1(z.read(sound_name)).hexdigest() == sound_hash, f"sound mismatch: {archive}/{sound_name}")
        require(hashlib.sha1(cpu).hexdigest() == "989d70e067cd322351768550549a4e2c8923132c", f"CPU changed: {archive}")
        trace_path = run_root / f"{suffix}-frames.json"
        require(sha256(trace_path) == case["trace"], f"trace changed: {trace_path}")
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        require(trace["game"] == f"trek_{suffix}" and trace["failure"] is None, "wrong or failed run")
        require(trace["library_sha256"] == LIBRARY and trace["scenario"]["sha256"] == SCENARIO, "wrong library or scenario")
        require(trace["dmd_event_summary"]["0"]["changed_frames"] > 0, "no display changes")
        require(len(trace["snapshots"]) == 2, "unexpected snapshots")
        for snapshot, filename, digest in zip(trace["snapshots"], FRAME_NAMES, case["frames"], strict=True):
            display = snapshot["displays"][0]
            require((display["layout"]["width"], display["layout"]["height"]) == (128, 16), "unexpected layout")
            frame = run_root / f"frames-{suffix}" / filename
            require(sha256(frame) == digest, f"frame changed: {frame}")
            data = frame.read_bytes()
            header, pixels = data.split(b"\n255\n", 1)
            require(header == b"P5\n128 16" and len(pixels) == 2048, "unexpected PGM")
            # The harness scales 0..3 input to grayscale; already-grayscale input is unchanged.
            raw_digest = hashlib.sha256(pixels).hexdigest()
            scaled_digest = hashlib.sha256(bytes(value // 85 for value in pixels)).hexdigest() if all(v % 85 == 0 for v in pixels) else ""
            require(display["pixel_sha256"] in (raw_digest, scaled_digest), "frame pixels do not match trace")
    require(cpus[0] == cpus[1], "CPU images differ")
    for suffix, (cpu_name, cpu_hash, display_name, display_hash) in PRODUCTION.items():
        with ZipFile(rom_root / f"trek_{suffix}.zip") as z:
            for name, expected in ((cpu_name, cpu_hash), (display_name, display_hash), *SOUND.items()):
                require(hashlib.sha1(z.read(name)).hexdigest() == expected, f"ROM mismatch: {suffix}/{name}")
    with ZipFile(rom_root / "trek_201.zip") as z:
        cpu, display = z.read("trekcpuu.201"), z.read("trekdspa.109")
    print(f"trekdspa.109: 64-entry lamp table at {verify_lamp_names(display):#x}")
    for suffix, patch_hash, cpu_hash in (
        ("300", "22fbb1c825f5e132b0b114b027f52f2cec3279967119d7a42031ea91147de745", "a453208a7640a39cb96947e8d3d3b2f71f85e613"),
        ("301", "4c7b5f10cd536aa7406b1d6764a3c897d2c79a3eefad5c625b297a8b15225a65", "f8dd222b5237cf4bd8bc00f32980d68d339032f9"),
    ):
        patch_archive = patch_root / f"patch-{suffix}.zip"
        require(sha256(patch_archive) == patch_hash, f"patch archive changed: {patch_archive}")
        with ZipFile(patch_archive) as z:
            modified_cpu = apply_ips(cpu, z.read(f"STARTREK-CPU-{suffix}-patch.ips"))
            modified_display = apply_ips(display, z.read("STARTREK-DISPLAY-300-patch.ips"))
        require(hashlib.sha1(modified_cpu).hexdigest() == cpu_hash, f"patched CPU mismatch: {suffix}")
        require(hashlib.sha1(modified_display).hexdigest() == "eebcc697b89bbe62b0450fdec6226a8396308f37", f"patched display mismatch: {suffix}")
        print(f"patched display {suffix}: 64-entry lamp table at {verify_lamp_names(modified_display):#x}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--patch-root", type=Path, required=True)
    args = parser.parse_args()
    verify(args.rom_root, args.run_root, args.patch_root)
    print("Star Trek display ROMs and retained frames verified")
