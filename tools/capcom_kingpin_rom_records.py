"""Decode Capcom Kingpin's diagnostic I/O name records from a user-supplied program ROM.

The kpb105 program ROM (``u1hu1l.bin``, loaded at CPU address 0x10000000) carries one
contiguous table of fixed-layout records that the service menu uses to name every lamp,
switch, and coil. Each record is big-endian::

    type:u8  length:u8  number:u16  name_pointer:u32  payload[length - 8]

``type`` is 1 for a lamp, 2 for a switch, and 3 for a coil. ``number`` is the ROM's own
internal index; this module converts it to the PinMAME public address:

* lamp  ``n``: ``64 * ((n & 15) >> 3) + (7 - (n & 7)) * 8 + (n >> 4) + 1``
* switch ``n``: derived from pinned ``capcom.c`` ``io_r``, which returns switch word ``k`` (1-4) as
  ``swMatrix[k + 4] << 8 | swMatrix[k]``. The ROM numbers the bits of that word from the high byte, so
  ROM column ``c = n >> 3`` (2-9) is PinMAME internal column ``c // 2 + 4`` when even and ``c // 2`` when
  odd; ROM column 0 is the cabinet byte in internal column 0. The public address is ``cc_m2sw`` =
  ``9 + (n & 7) + internal_column * 8``.
* coil ``n``: the ROM's 32 coil bits map to public 1-8 (``n`` 15..8), 9-16 (31..24), 17-24 (7..0) and
  25-32 (23..16). This conversion is not derived from source; it is established by the Solenoid
  Test walk, in which every displayed S-number fires the public address this function returns.

For switches, bit 1 of payload byte 14 is set on exactly the records the service menu treats
as optos. The lamp conversion is likewise confirmed by the Lamp Test walk, and the switch
conversion by the Switch Test, whose printed number equals the returned public address.

No ROM bytes are written anywhere; the command prints the decoded table.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

ROM_BASE = 0x10000000
RECORD_TYPES = {1: "lamp", 2: "switch", 3: "coil"}
# ROM switch column -> PinMAME internal switch column (cc_m2sw input), from io_r's word layout.
SWITCH_COLUMN = {0: 0, **{column: column // 2 + (4 if column % 2 == 0 else 0) for column in range(2, 10)}}
COIL_BYTE_BASE = {1: 0, 3: 8, 0: 16, 2: 24}
OPTO_FLAG_OFFSET = 14
OPTO_FLAG_MASK = 0x02


def lamp_public(number: int) -> int:
	return 64 * ((number & 15) >> 3) + (7 - (number & 7)) * 8 + (number >> 4) + 1


def switch_public(number: int) -> int:
	column, row = divmod(number, 8)
	return 9 + row + SWITCH_COLUMN[column] * 8


def coil_public(number: int) -> int:
	byte, bit = divmod(number, 8)
	return COIL_BYTE_BASE[byte] + (7 - bit) + 1


def _name(rom: bytes, pointer: int) -> str | None:
	offset = pointer - ROM_BASE
	if not 0 <= offset < len(rom):
		return None
	end = rom.find(b"\0", offset, offset + 64)
	if end < 0:
		return None
	text = rom[offset:end]
	return text.decode("ascii") if text and all(32 <= byte < 127 for byte in text) else None


def decode(rom: bytes) -> list[dict[str, object]]:
	"""Return the first run of at least 100 well-formed records, starting with a lamp."""
	for start in range(0, len(rom) - 16, 2):
		if rom[start] != 1 or rom[start + 1] != 12:
			continue
		records: list[dict[str, object]] = []
		offset = start
		while offset + 8 <= len(rom):
			kind, length = rom[offset], rom[offset + 1]
			if kind not in RECORD_TYPES or length < 8:
				break
			number = struct.unpack(">H", rom[offset + 2:offset + 4])[0]
			name = _name(rom, struct.unpack(">I", rom[offset + 4:offset + 8])[0])
			if name is None:
				break
			payload = rom[offset + 8:offset + length]
			records.append({"offset": offset, "type": RECORD_TYPES[kind], "number": number, "name": name, "payload": payload.hex()})
			offset += length
		if len(records) >= 100:
			for record in records:
				number = int(record["number"])
				if record["type"] == "lamp":
					record["public"] = lamp_public(number)
				elif record["type"] == "switch":
					payload = bytes.fromhex(str(record["payload"]))
					record["public"] = switch_public(number)
					record["opto_flag"] = bool(len(payload) > OPTO_FLAG_OFFSET and payload[OPTO_FLAG_OFFSET] & OPTO_FLAG_MASK)
				else:
					record["public"] = coil_public(number)
			return records
	return []


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("program_rom", type=Path, help="kpb105 u1hu1l.bin (read-only)")
	args = parser.parse_args(argv)
	records = decode(args.program_rom.read_bytes())
	if not records:
		print("no Kingpin I/O record table found", file=sys.stderr)
		return 1
	json.dump(records, sys.stdout, indent=1)
	print()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
