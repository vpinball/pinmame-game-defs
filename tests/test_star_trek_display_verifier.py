import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from trek_display_evidence import LAMP_NAMES, apply_ips, verify_lamp_names


def display_image(*tables):
    """Build bank-relative pointer tables that share a synthetic set of labels."""
    image = bytearray(0x20000)
    cursor = 0x14000
    for number in range(1, 65):
        name = LAMP_NAMES.get(number, f"LAMP {number}".encode("ascii"))
        image[cursor:cursor + len(name)] = name
        for table in tables:
            entry = table + 2 * (number - 1)
            image[entry:entry + 2] = (cursor - 0x10000).to_bytes(2, "little")
        cursor += len(name) + 1
    return image


class DisplayVerifierTests(unittest.TestCase):
    def test_ips_literal_and_run_length_records(self):
        literal = bytes.fromhex("00 00 01 00 02") + b"ab"
        repeated = bytes.fromhex("00 00 05 00 00 00 03") + b"z"
        self.assertEqual(apply_ips(b"01234567", b"PATCH" + literal + repeated + b"EOF"), b"0ab34zzz")

    def test_ips_rejects_truncated_records_and_trailer(self):
        for patch, error in (
            (b"PATCH\x00", "truncated IPS record"),
            (b"PATCH" + bytes.fromhex("00 00 00 00 02 41"), "truncated IPS data"),
            (b"PATCH" + bytes.fromhex("00 00 00 00 00 00 03"), "truncated IPS RLE"),
            (b"PATCHEOFextra", "unsupported IPS trailer"),
        ):
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                apply_ips(bytes(8), patch)

    def test_unique_table_including_last_legal_bank_offset(self):
        for table in (0x15000, 0x18000 - 128):
            with self.subTest(table=table):
                self.assertEqual(verify_lamp_names(display_image(table)), table)

    def test_missing_and_ambiguous_tables(self):
        for tables in ((), (0x15000, 0x16000)):
            with self.subTest(tables=tables), self.assertRaisesRegex(ValueError, f"found {len(tables)}"):
                verify_lamp_names(display_image(*tables))

    def test_invalid_non_anchor_label(self):
        table = 0x15000
        image = display_image(table)
        image[table:table + 2] = bytes(2)
        with self.assertRaisesRegex(ValueError, "invalid lamp table entries"):
            verify_lamp_names(image)
