"""Literal excerpt parsing and fail-closed table integrity checks."""

from pathlib import Path
import unittest

import wwf_manual as manual


ROOT = Path(__file__).resolve().parent.parent
EXCERPTS = ROOT / "evidence/excerpts/data-east.wwf-royal-rumble.1994"


class ManualRowsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.switch_text = (EXCERPTS / "switches.md").read_text(encoding="utf-8")
        cls.lamp_text = (EXCERPTS / "lamps.md").read_text(encoding="utf-8")
        cls.coil_text = (EXCERPTS / "coils.md").read_text(encoding="utf-8")

    def test_exact_printed_address_sets(self):
        self.assertEqual(set(manual.switch_rows(ROOT)), set(range(1, 65)))
        self.assertEqual(set(manual.lamp_rows(ROOT)), set(range(1, 65)))
        self.assertEqual(set(manual.coil_rows(ROOT)), {
            "1L", "1R", "2L", "2R", "3L", "3R", "4L", "4R",
            "5L", "5R", "6L", "6R", "7L", "7R", "8L", "8R",
            "09", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21", "22",
        })
        flippers = manual.flipper_rows(ROOT)
        self.assertEqual(set(flippers), {"1", "2"})
        self.assertEqual([row["Flipper Coil"] for row in flippers["1"]],
                         ["Lwr. Rt. Flipper 22-1080", "Lwr. Lt. Flipper 22-1080"])
        self.assertEqual([row["Flipper Coil"] for row in flippers["2"]],
                         ["Upr. Rt. Flipper 25-1800", "Upr. Lt. Flipper 25-1800"])

    def test_literal_cells_and_shared_wiring(self):
        switches = manual.switch_rows(text=self.switch_text)
        self.assertEqual(switches[45], {
            "Address": "45", "Matrix label (p28)": "RT Rollover BOT",
            "Parts-list description (p29)": "Right Rollover Bottom (LT Hand",
            "Part No.": "180-5707-00",
        })
        self.assertEqual(switches[48]["Parts-list description (p29)"], "Not Used")
        self.assertEqual(switches[48]["Part No."], "---")
        self.assertEqual(manual.lamp_rows(text=self.lamp_text)[28], {
            "Address": "28", "Matrix label (p30)": "LT & RT Outlanes",
            "Location-table description (p31)": "Special (Left & Right Outlanes)",
        })
        coils = manual.coil_rows(text=self.coil_text)
        self.assertEqual(coils["1R"]["Description p33"], "Lower Playfield Flash; X3 P/F, X1 Insert")
        self.assertEqual(coils["3R"]["Description p33"], "Right Macho Madness Flash; X2 P/F, Insert X2")
        self.assertEqual(coils["14"]["Drive transistor"], "---")
        self.assertEqual(coils["16"]["Power line"], "---")
        self.assertEqual(coils["1L"]["Drive transistor"], coils["1R"]["Drive transistor"])
        self.assertEqual(coils["1L"]["Board"], coils["1R"]["Board"])
        flippers = manual.flipper_rows(text=self.coil_text)
        self.assertEqual(flippers["1"][0]["Flipper 50vDC Power"], flippers["2"][1]["Flipper 50vDC Power"])
        self.assertEqual(flippers["2"][0]["E.O.S."], "Not Used")
        headings = (
            (manual.switch_column_headings, self.switch_text, 6, "CPU connection", "CN8-7"),
            (manual.switch_row_headings, self.switch_text, 8, "Return wire", "WHT-GRY"),
            (manual.lamp_column_headings, self.lamp_text, 4, "18V drive wire", "YEL-BLK"),
            (manual.lamp_row_headings, self.lamp_text, 2, "GND return wire", "RED-BLK"),
        )
        for parser, text, key, field, value in headings:
            with self.subTest(parser=parser.__name__):
                result = parser(text=text)
                self.assertEqual(set(result), set(range(1, 9)))
                self.assertEqual(result[key][field], value)

    def test_duplicate_missing_and_malformed_rows_fail_closed(self):
        cases = (
            (manual.switch_rows, self.switch_text, "| 48 | Not Used | Not Used | --- |"),
            (manual.lamp_rows, self.lamp_text, "| 25 | Extra Ball | Extra Ball |"),
            (manual.coil_rows, self.coil_text, "| 14 | Not Used | --- | --- | --- | --- | --- | --- | --- | --- |"),
            (manual.switch_column_headings, self.switch_text, "| 1 | Q55 | GRN-BRN | CN8-1 |"),
            (manual.switch_row_headings, self.switch_text, "| 1 | WHT-BRN | CN10-9 |"),
            (manual.lamp_column_headings, self.lamp_text, "| 1 | Q71 | YEL-BRN | CN7-1 |"),
            (manual.lamp_row_headings, self.lamp_text, "| 1 | Q72 | RED-BRN | CN6-1 |"),
        )
        for parser, text, row in cases:
            self.assertEqual(text.count(row), 1)
            mutations = {
                "duplicate": text.replace(row, row + "\n" + row),
                "missing": text.replace(row + "\n", ""),
                "empty cell": text.replace(row, row.replace(" | ", " | | ", 1)),
                "missing delimiter": text.replace(row, row[:-1]),
            }
            for name, mutated in mutations.items():
                with self.subTest(parser=parser.__name__, mutation=name):
                    with self.assertRaises(ValueError):
                        parser(text=mutated)

    def test_flipper_duplicate_missing_and_malformed_fail_closed(self):
        row = next(line for line in self.coil_text.splitlines()
                   if line.startswith("| 1 | Lwr. Rt. Flipper"))
        mutations = (
            self.coil_text.replace(row, row + "\n" + row),
            self.coil_text.replace(row + "\n", ""),
            self.coil_text.replace(row, row.replace(" | BLU-VIO SSFB CN1-7 |", " |  |")),
            self.coil_text.replace(row, row[:-1]),
        )
        for mutated in mutations:
            with self.subTest(mutated=mutated != self.coil_text):
                with self.assertRaises(ValueError):
                    manual.flipper_rows(text=mutated)

    def test_missing_or_duplicate_table_and_bad_separator_fail(self):
        header = "| Address | Matrix label (p30) | Location-table description (p31) |"
        for text in (self.lamp_text.replace(header, "missing"),
                     self.lamp_text + "\n" + header + "\n",
                     self.lamp_text.replace(header + "\n| --- | --- | --- |",
                                            header + "\n| --- | -- | --- |")):
            with self.assertRaises(ValueError):
                manual.lamp_rows(text=text)


if __name__ == "__main__":
    unittest.main()
