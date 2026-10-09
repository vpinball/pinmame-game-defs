"""Decode the lamp, switch and coil name tables from every locally available Pin-Bot game ROM.

Pin-Bot's System 11A service text lives in the 32 KiB U27 program ROM as fixed 14-byte entries:
seven characters for the player 1 display followed by seven for the player 2 display, which is how
the Single Lamps, Switch Levels and Coil tests print them. A byte with bit 7 set is the character in
its low seven bits followed by the display's period segment (``SW.``, ``D.T.``). Three tables sit
back to back:

* the lamp table, 64 entries in public lamp order, ending where the switch table begins;
* the switch table, 64 entries in public switch order, whose first entry is `` PLUMB  TILT  ``;
* the coil table, which starts directly after the switch table in the ROM's own coil-test order:
  sixteen entries alternating each switched A-side load with its C-side partner, then one entry
  per controlled and special solenoid, each followed by a blank 14-byte entry.

Each table is located by its anchor text in every set rather than by an offset carried over from
another set, and each anchor is checked (the lamp table must begin with ``GAME OVER`` and the coil
table with ``OUTHOLE``). No ROM bytes are written; only decoded text, offsets and hashes.

    python tools/pinbot_rom_name_tables.py --roms <vpinmame-roms> --out <dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

ENTRY_BYTES = 14
HALF = 7
SETS = ("pb_l5", "pb_l5h", "pb_l3", "pb_l2", "pb_l1", "pb_p4", "pb_j1", "pb_j2", "pb_j3", "pb_j5")
LAMP_COUNT = 64
SWITCH_COUNT = 64
# Sixteen A/C entries, then eight controlled and six special solenoids, each with a blank spacer.
COIL_WINDOW = 16 + 2 * 14


def decode_text(raw: bytes) -> str:
	text = []
	for value in raw:
		if value >= 0x80:
			text.append(chr(value & 0x7F) + ".")
		elif 32 <= value < 127:
			text.append(chr(value))
		else:
			text.append(f"<{value:02x}>")
	return "".join(text)


def decode_entry(raw: bytes) -> dict[str, str]:
	top, bottom = decode_text(raw[:HALF]), decode_text(raw[HALF:])
	return {"player_1": top, "player_2": bottom, "text": " ".join(part for part in (top.strip(), bottom.strip()) if part)}


def table(rom: bytes, start: int, count: int) -> list[dict[str, Any]]:
	entries = []
	for index in range(count):
		offset = start + index * ENTRY_BYTES
		entry = decode_entry(rom[offset:offset + ENTRY_BYTES])
		entries.append({"index": index + 1, "offset": f"0x{offset:04x}", **entry})
	return entries


def program_member(archive: zipfile.ZipFile) -> str:
	candidates = [name for name in archive.namelist() if "u27" in name.casefold()]
	if len(candidates) != 1:
		raise RuntimeError(f"cannot choose the U27 program ROM among {archive.namelist()}")
	return candidates[0]


def decode_set(rom_zip: Path) -> dict[str, Any]:
	with zipfile.ZipFile(rom_zip) as archive:
		member = program_member(archive)
		rom = archive.read(member)
	switch_start = rom.find(b" PLUMB  TILT  ")
	if switch_start < 0:
		raise RuntimeError(f"{rom_zip.name}: switch table anchor not found")
	lamp_start = switch_start - LAMP_COUNT * ENTRY_BYTES
	coil_start = switch_start + SWITCH_COUNT * ENTRY_BYTES
	if decode_entry(rom[lamp_start:lamp_start + ENTRY_BYTES])["text"] != "GAME OVER":
		raise RuntimeError(f"{rom_zip.name}: lamp table does not end at the switch table")
	if decode_entry(rom[coil_start:coil_start + ENTRY_BYTES])["text"] != "OUTHOLE":
		raise RuntimeError(f"{rom_zip.name}: coil table does not follow the switch table")
	return {
		"rom_archive": rom_zip.name,
		"rom_archive_sha256": hashlib.sha256(rom_zip.read_bytes()).hexdigest(),
		"member": member,
		"member_sha256": hashlib.sha256(rom).hexdigest(),
		"member_size": len(rom),
		"lamp_table": {"start": f"0x{lamp_start:04x}", "entries": table(rom, lamp_start, LAMP_COUNT)},
		"switch_table": {"start": f"0x{switch_start:04x}", "entries": table(rom, switch_start, SWITCH_COUNT)},
		"coil_table": {"start": f"0x{coil_start:04x}", "entries": table(rom, coil_start, COIL_WINDOW)},
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--roms", type=Path, required=True, help="read-only ROM archive directory")
	parser.add_argument("--out", type=Path, required=True, help="external output directory")
	args = parser.parse_args()
	args.out.mkdir(parents=True, exist_ok=True)
	summary = {}
	for name in SETS:
		rom_zip = args.roms / f"{name}.zip"
		if not rom_zip.is_file():
			summary[name] = "not in the local ROM corpus"
			continue
		result = decode_set(rom_zip)
		(args.out / f"{name}.json").write_bytes((json.dumps(result, indent=1) + "\n").encode("utf-8"))
		summary[name] = {"member": result["member"], "member_sha256": result["member_sha256"], "switch_table": result["switch_table"]["start"]}
	print(json.dumps(summary, indent=1))


if __name__ == "__main__":
	main()
