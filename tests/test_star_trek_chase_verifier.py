import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import verify_star_trek_chase as chase


def fixture():
    """Construct a synthetic program and table, not a copy of a ROM."""
    data = bytearray(65536)
    table, routine = 0x5000, 0x4100
    op = chase.OP
    data[routine - 12:routine] = bytes((op["ldx_imm"], 0x50, 0,
        op["ldab_ext"], 0x10, 0x8F, op["aslb"], op["jsr_ext"], 0x40, 0x20,
        op["ldx_ix"], 0))
    data[routine:routine + 14] = bytes((op["ldab_ix"], 0, op["inx"],
        op["ldaa_ix"], 0, op["coma"], op["tst_ext"], 0x10, 0x91,
        op["bne"], 3, op["staa_ext"], 0x28, 2))
    pointer = 0x5100
    for index, (masks, delays) in enumerate(chase.EXPECTED):
        data[table + 2 * index:table + 2 * index + 2] = pointer.to_bytes(2, "big")
        data[pointer] = len(masks)
        for offset, (mask, delay) in enumerate(zip(masks, delays)):
            data[pointer + 1 + 2 * offset:pointer + 3 + 2 * offset] = bytes((mask, delay))
        pointer += 1 + 2 * len(masks)
    return data


class ChaseVerifierTests(unittest.TestCase):
    def test_reads_eight_patterns_and_maps_output_address(self):
        result = chase.analyze(fixture(), 0x5000)
        self.assertEqual(result["routine"], "4100")
        self.assertEqual(result["table"], "5000")
        self.assertEqual([tuple(p["masks"]) for p in result["patterns"]],
                         [masks for masks, _ in chase.EXPECTED])
        self.assertEqual(result["possible_extended_stores"], ["410B"])

    def test_rejects_mutated_mask_delay_dispatch_and_pointer(self):
        mutations = ((0x5101, 8), (0x5102, 0), (0x40F7, 0), (0x5000, 0))
        for address, value in mutations:
            with self.subTest(address=address):
                data = fixture()
                data[address] = value
                with self.assertRaises(ValueError):
                    chase.analyze(data, 0x5000)

    def test_rejects_missing_or_duplicate_routine_and_wrong_size(self):
        data = fixture()
        with self.assertRaises(ValueError):
            chase.analyze(data[:-1])
        changed = data.copy()
        changed[0x4100] = 0
        with self.assertRaises(ValueError):
            chase.analyze(changed)
        changed = data.copy()
        changed[0x4200:0x420E] = data[0x4100:0x410E]
        with self.assertRaises(ValueError):
            chase.analyze(changed)

    def test_extended_store_context_and_service_table_guard(self):
        data = fixture()
        sites = list(range(0x4020, 0x40C0, 0x10))
        for index, pos in enumerate(sites):
            data[pos:pos + 3] = bytes((chase.OP["stab_ext"] if index < 3
                                       else chase.OP["staa_ext"], 0x28, 2))
        for pos, value in zip((sites[3], *sites[5:]), (255, 255, 248, 255, 255, 255)):
            data[pos - 2:pos] = bytes((0x86, value))
        data[sites[4] - 2:sites[4]] = bytes((chase.OP["ldaa_ix"], 0))
        data[sites[5] - 6:sites[5] - 2] = bytes((254, 253, 251, 255))
        result = chase.analyze(data, 0x5000)
        chase.verify_stores(data, result)
        data[sites[5] - 3] = 0
        with self.assertRaisesRegex(ValueError, "service-test data"):
            chase.verify_stores(data, result)

    def test_rejects_ambiguous_archive_and_unpinned_cpu(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(root / "trek_110.zip", "w") as archive:
                archive.writestr("firstcpu", b"x")
                archive.writestr("secondCPU", b"y")
            with self.assertRaises(ValueError):
                chase.image_for("110", root, root)
            with zipfile.ZipFile(root / "trek_110.zip", "w") as archive:
                archive.writestr("cpu", bytes(fixture()))
            with self.assertRaisesRegex(ValueError, "SHA-1"):
                chase.verify(root, root)


if __name__ == "__main__":
    unittest.main()
