"""Decode the switch and coil name tables from a user-supplied System 11 game ROM.

Williams System 11B game ROMs keep the text their service tests print as fixed 16-byte entries,
one per public address, in the U26 program ROM. A byte with bit 7 set is the character in its
low seven bits followed by the display's period segment, and the ROM font codes ``o`` and ``p``
for ``-`` and ``/`` (the coil test displays the stored ``JACKPTpSUN FLASH`` entry as
``JACKPT/SUN FLASH``). This tool locates both tables by their first entries, decodes every entry
in address order, and prints JSON. No ROM bytes are written anywhere.

    python tools/s11_rom_name_tables.py --rom <game.zip> [--member <u26 file>] \
        --switch-anchor "  PLUMB  TILT   " --switch-count 58 \
        --coil-anchor "    OUTHOLE     " --coil-next "CAPT" --coil-count 30

The switch table runs in public switch order from address 1. The coil table follows the ROM's
own coil-test order, in which each switched A-side entry is followed by its C-side partner, so
its entries are returned in table order with no address attached; pair them with a coil-test
run to assign public addresses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

ENTRY_BYTES = 16
SYMBOLS = {"o": "-", "p": "/"}


def decode_entry(raw: bytes) -> str:
	text = []
	for value in raw:
		if value >= 0x80:
			text.append(SYMBOLS.get(chr(value & 0x7F), chr(value & 0x7F)) + ".")
		elif 32 <= value < 127:
			text.append(SYMBOLS.get(chr(value), chr(value)))
		else:
			text.append(f"<{value:02x}>")
	return "".join(text)


def _table(rom: bytes, start: int, count: int) -> list[dict[str, Any]]:
	entries = []
	for index in range(count):
		raw = rom[start + index * ENTRY_BYTES:start + (index + 1) * ENTRY_BYTES]
		entries.append({"index": index + 1, "offset": f"0x{start + index * ENTRY_BYTES:04x}", "raw_hex": raw.hex(), "text": decode_entry(raw).strip()})
	return entries


def find_coil_table(rom: bytes, anchor: bytes, following: bytes) -> int:
	position = rom.find(anchor)
	while position >= 0:
		if rom[position + ENTRY_BYTES:position + ENTRY_BYTES + len(following)] == following:
			return position
		position = rom.find(anchor, position + 1)
	raise RuntimeError("coil table anchor not found")


def decode(rom_zip: Path, member: str | None, switch_anchor: str, switch_count: int, coil_anchor: str, coil_next: str, coil_count: int) -> dict[str, Any]:
	with zipfile.ZipFile(rom_zip) as archive:
		names = archive.namelist()
		if member is None:
			candidates = [name for name in names if "u26" in name.casefold()]
			if len(candidates) != 1:
				raise RuntimeError(f"cannot choose the U26 program ROM among {names}")
			member = candidates[0]
		rom = archive.read(member)
	switch_start = rom.find(switch_anchor.encode("latin-1"))
	if switch_start < 0:
		raise RuntimeError("switch table anchor not found")
	coil_start = find_coil_table(rom, coil_anchor.encode("latin-1"), coil_next.encode("latin-1"))
	return {
		"rom_archive": rom_zip.name,
		"rom_archive_sha256": hashlib.sha256(rom_zip.read_bytes()).hexdigest(),
		"member": member,
		"member_sha256": hashlib.sha256(rom).hexdigest(),
		"member_size": len(rom),
		"switch_table": {"start": f"0x{switch_start:04x}", "entries": _table(rom, switch_start, switch_count)},
		"coil_table": {"start": f"0x{coil_start:04x}", "entries": _table(rom, coil_start, coil_count)},
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--rom", type=Path, required=True)
	parser.add_argument("--member")
	parser.add_argument("--switch-anchor", required=True)
	parser.add_argument("--switch-count", type=int, required=True)
	parser.add_argument("--coil-anchor", required=True)
	parser.add_argument("--coil-next", required=True)
	parser.add_argument("--coil-count", type=int, required=True)
	args = parser.parse_args()
	result = decode(args.rom, args.member, args.switch_anchor, args.switch_count, args.coil_anchor, args.coil_next, args.coil_count)
	print(json.dumps(result, indent=1))


if __name__ == "__main__":
	main()
