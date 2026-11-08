from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "skills/orbit-export-workbook/scripts/md_to_workbook.py"


class WorkbookExportTests(unittest.TestCase):
    def test_identifiers_survive_integer_config_without_changing_effort(self):
        with tempfile.TemporaryDirectory(prefix="orbit-export-test-") as directory:
            root = Path(directory)
            markdown = root / "source.md"
            config = root / "config.yaml"
            target = root / "result.xlsx"
            markdown.write_text(
                "## Timeline\n\n### `tbl_task_timeline`\n\n"
                "| # | Task / Phase | MD | W1 |\n"
                "| --- | --- | --- | --- |\n"
                "| 3.1 | Setup DEV Environment | 1.25 | active |\n"
                "| 3.10 | Setup UAT Environment | 2.5 | active |\n"
                "| 001 | เตรียมข้อมูล | `=SUM(C2:C3)` | |\n",
                encoding="utf-8",
            )
            config.write_text(
                "defaults:\n  integer_headers: ['#']\n"
                "  number_format: {MD: '0.00'}\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(EXPORT), "--input", str(markdown),
                 "--output", str(target), "--config", str(config), "--strict"],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            workbook = load_workbook(target)
            self.addCleanup(workbook.close)
            sheet = workbook["Timeline"]
            self.assertEqual([sheet[f"A{row}"].value for row in (2, 3, 4)],
                             ["3.1", "3.10", "001"])
            self.assertEqual([sheet[f"C{row}"].value for row in (2, 3, 4)],
                             [1.25, 2.5, "=SUM(C2:C3)"])
            self.assertEqual(sheet["B4"].value, "เตรียมข้อมูล")
            self.assertIsNone(sheet["D2"].value)
            self.assertEqual(sheet["D2"].fill.patternType, "solid")


if __name__ == "__main__":
    unittest.main()
