from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

from openpyxl import Workbook
import yaml


ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "plugins/orbit-cost-estimate/skills/orbit-export-workbook/scripts/verify_workbook.py"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


class Formula:
    def __init__(self, expression, cache):
        self.expression = expression
        self.cache = cache


class WorkbookFixture:
    def __init__(self, root):
        self.root = root
        self.markdown = root / "workbook.md"
        self.workbook = root / "final.xlsx"
        self.config = root / "project.yaml"
        self.report = root / "report.json"
        self.tables = {}
        self.positions = {}
        controls = [
            ["Raw MD", 5], ["Adjusted MD", 5], ["PM Base MD", 0],
            ["Selected Delivery Basis", "P50"], ["Reserve Rate", 0.1],
            ["Reserve Denominator", "Delivery Baseline"],
            ["Working Days per Week", 5], ["Focus Factor", 1], ["Delivery Weeks", 1],
            ["Average FTE", 1], ["Validation Summary", "Pass"],
            ["Calculation Status", "Recalculated"],
        ]
        for role, amount, average in (("FE", 3, 0.6), ("BE", 2, 0.4)):
            controls.extend([[f"{role} {field}", value] for field, value in (
                ("Raw MD", amount), ("Rework Rate", 0), ("Buffer Rate", 0),
                ("Adjusted MD", amount), ("Warranty Adjusted MD", 0),
                ("Delivery Adjusted MD", amount), ("Average FTE", average),
            )])
        ranges = [
            ["Adjusted MD", 5], ["Recommended Contingency MD", 1],
            ["Selected Commitment Uplift", 0], ["Contingency MD", 1],
            ["Delivery Baseline", 6], ["Management Reserve", 0.6],
            ["Planning Total", 6.6], ["P25", 5.5], ["P50", 6], ["P75", 6.5], ["P90", 7],
        ]
        controls.extend([row[:] for row in ranges if row[0] != "Adjusted MD"])
        self.add("README", "tbl_readme_control", ["Field", "Value", "Source Ref", "Note"], [r + ["fixture", ""] for r in controls])
        self.add("README", "tbl_validation_summary", ["Check ID", "Result", "Severity", "Note"], [["VAL-01", "Pass", "High", "Independent numeric evidence"]])
        self.add("Features", "tbl_feature_inventory", ["Subfeature ID", "SG"], [["FN-01.01", "SG1"]])
        self.add("Sizing", "tbl_sizing_features", ["Subfeature ID", "FE", "BE", "Total"], [["FN-01.01", 3, 2, Formula("=SUM(B2:C2)", 5)]])
        self.add("Sizing", "tbl_sizing_integrations", ["INT ID", "FE", "BE", "Total"], [])
        self.add("Sizing", "tbl_sizing_non_dev", ["ND ID", "FE", "BE", "Total"], [])
        self.add("Sizing", "tbl_sizing_summary", ["Bucket", "FE", "BE", "Bucket Total", "QA vs FE+BE Check"], [
            ["SG1 Features", Formula("=B2", 3), Formula("=C2", 2), 5, "Pass"],
            ["SG2 Features", 0, 0, 0, "Pass"], ["Integration", 0, 0, 0, "Pass"],
            ["Non-Dev", 0, 0, 0, "Pass"], ["Raw Grand Total", 3, 2, 5, "Pass"],
        ])
        self.add("Timeline", "tbl_resource_matrix", ["#", "Role", "W1", "FTE-Weeks", "MD", "Effective MD", "Adjusted MD", "Coverage Ratio"], [
            [1, "FE", 0.6, 0.6, 3, 3, 3, 1], [2, "BE", 0.4, 0.4, 2, 2, 2, 1],
            [3, "Total FTE/week", 1, 1, 5, 5, 5, 1],
        ])
        self.add("Timeline", "tbl_task_timeline", ["#", "Task / Phase", "W1"], [
            ["3.1", "Setup DEV Environment", "active"],
            ["3.10", "Setup UAT Environment", "active"], ["001", "Foundation", ""],
        ])
        self.add("Risk", "tbl_range_reserve", ["Category / Scenario", "Effort MD"], ranges)
        self.add("Risk", "tbl_final_snapshot", ["Field", "Value", "Source Ref", "Note"],
                 [row[:] + ["fixture", ""] for row in ranges] + [["Selected Delivery Basis", "P50", "fixture", ""]])

    def add(self, sheet, name, headers, rows):
        self.tables[name] = (sheet, headers, rows)

    def set_value(self, table, key, header, value):
        _, headers, rows = self.tables[table]
        next(row for row in rows if row[0] == key)[headers.index(header)] = value

    def write(self):
        workbook = Workbook()
        workbook.remove(workbook.active)
        source = []
        registry = []
        caches = []
        previous = None
        for name, (sheet, headers, rows) in self.tables.items():
            if sheet != previous:
                ws = workbook.create_sheet(sheet)
                source.extend([f"## {sheet}", ""])
                registry.append({"heading": sheet, "short_name": sheet, "tables": []})
                cursor = 1
                previous = sheet
            registry[-1]["tables"].append({"name": name})
            if name == "tbl_resource_matrix":
                ws.cell(cursor, 3, "Delivery")
                cursor += 1
            source.extend([f"### `{name}`", "", "| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"])
            for col, header in enumerate(headers, 1):
                ws.cell(cursor, col, header)
            for offset, row in enumerate(rows, 1):
                md_row = []
                for col, item in enumerate(row, 1):
                    cell = ws.cell(cursor + offset, col)
                    self.positions[(name, str(row[0]), headers[col - 1])] = (sheet, cell.coordinate)
                    if isinstance(item, Formula):
                        md_row.append(f"`{item.expression}`")
                        cell.value = item.expression
                        caches.append((sheet, cell.coordinate, item.cache))
                    else:
                        md_row.append(str(item))
                        cell.value = None if item == "active" else item
                source.append("| " + " | ".join(md_row) + " |")
            source.append("")
            cursor += len(rows) + 2
        self.markdown.write_text("\n".join(source), encoding="utf-8")
        self.config.write_text(yaml.safe_dump({"sheets": registry}), encoding="utf-8")
        workbook.save(self.workbook)
        workbook.close()
        for sheet, address, value in caches:
            if value is not None:
                self.mutate_xml(sheet, address, value, cache=True)

    def mutate_xml(self, sheet, address, value, cache=False, error=False):
        sheet_names = list(dict.fromkeys(t[0] for t in self.tables.values()))
        member = f"xl/worksheets/sheet{sheet_names.index(sheet) + 1}.xml"
        with ZipFile(self.workbook) as archive:
            files = {name: archive.read(name) for name in archive.namelist()}
        xml = ET.fromstring(files[member])
        cell = xml.find(f".//s:c[@r='{address}']", NS)
        if not cache:
            for child in list(cell):
                cell.remove(child)
        cell.set("t", "e" if error else "n")
        cached = cell.find("s:v", NS)
        if cached is None:
            cached = ET.SubElement(cell, f"{{{NS['s']}}}v")
        cached.text = str(value)
        files[member] = ET.tostring(xml, encoding="utf-8", xml_declaration=True)
        with ZipFile(self.workbook, "w", ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)

    def run(self, markdown_only=False):
        mode = ["--markdown-only"] if markdown_only else ["--workbook", str(self.workbook)]
        result = subprocess.run([sys.executable, str(VERIFIER), "--input", str(self.markdown),
                                 *mode, "--config", str(self.config),
                                 "--output", str(self.report)], capture_output=True, text=True)
        if not self.report.exists():
            raise AssertionError(result.stdout + result.stderr)
        return result.returncode, json.loads(self.report.read_text(encoding="utf-8"))

    def complete_required_rows(self):
        controls = self.tables["tbl_readme_control"][2]
        present = {row[0] for row in controls}
        for field in ("Workbook Name", "Project Name", "Version", "Generated Date", "Source Artifacts",
                      "Approved Baseline Scope", "Approval State", "Approval Basis", "No-Pricing Rule",
                      "Confidence", "Integration Count", "External Risk Count", "Top Risks",
                      "Re-estimation Triggers", "Baseline-vs-Scenario Note"):
            if field not in present:
                controls.append([field, "fixture value", "fixture", ""])
        snapshot = self.tables["tbl_final_snapshot"][2]
        for field in ("Top Risks", "Confidence", "Re-estimation Triggers"):
            snapshot.append([field, "fixture value", "fixture", ""])

    def preflight(self):
        self.write()
        self.workbook.unlink()
        return self.run(markdown_only=True)


class WorkbookVerificationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="orbit-verification-test-")
        self.addCleanup(self.directory.cleanup)
        self.fixture = WorkbookFixture(Path(self.directory.name))

    def test_appended_specialist_role_is_included_in_all_totals(self):
        for name in ("tbl_sizing_features", "tbl_sizing_integrations",
                     "tbl_sizing_non_dev", "tbl_sizing_summary"):
            _, headers, rows = self.fixture.tables[name]
            index = headers.index("BE")
            headers.pop(index)
            headers.append("DBA")
            for row in rows:
                row.append(row.pop(index))
        self.fixture.set_value("tbl_sizing_features", "FN-01.01", "Total",
                               Formula("=SUM(B2,D2)", 5))
        self.fixture.set_value("tbl_sizing_summary", "SG1 Features", "DBA",
                               Formula("=D2", 2))
        _, headers, rows = self.fixture.tables["tbl_sizing_features"]
        for header, value in (("WBS Ref", "1.1.01"), ("Test Case Count", 5),
                              ("QA MD/Case", 0.1), ("QA Reconciliation", 0),
                              ("Atomicity Check", "Pass"), ("Acceptance Check", "Pass")):
            headers.append(header)
            for row in rows:
                row.append(value)
        for row in self.fixture.tables["tbl_readme_control"][2]:
            if row[0].startswith("BE "):
                row[0] = "DBA " + row[0][3:]
        for row in self.fixture.tables["tbl_resource_matrix"][2]:
            if row[1] == "BE":
                row[1] = "DBA"
        self.fixture.tables["tbl_resource_matrix"][2].insert(2, [4, "Change", 0, 0, 0, 0, 0, 0])
        for field in ("Raw MD", "Adjusted MD", "Warranty Adjusted MD",
                      "Delivery Adjusted MD", "Average FTE"):
            self.fixture.tables["tbl_readme_control"][2].append([
                f"Change {field}", 0, "Unused role retained for review", ""])
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (0, "Pass"), report)
        self.assertEqual(report["findings"]["VAL-01/Raw Grand Total/DBA"]["expected"], "2")
        self.assertEqual(report["findings"]["VAL-04/Adjusted MD"]["expected"], "5")
        self.assertEqual(report["findings"]["VAL-05/Average FTE"]["expected"], "1")

    def test_missing_resource_role_cannot_reduce_demand(self):
        _, _, rows = self.fixture.tables["tbl_resource_matrix"]
        rows[:] = [row for row in rows if row[1] != "BE"]
        rows[-1][:] = [3, "Total FTE/week", 0.6, 0.6, 3, 3, 3, 1]
        self.fixture.set_value("tbl_readme_control", "Average FTE", "Value", 0.6)
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2, report)
        self.assertEqual(report["findings"]["VAL-05/role-coverage"]["result"], "Fail")
        self.assertEqual(report["findings"]["VAL-05/Average FTE"]["expected"], "1")

    def test_synchronized_negative_contingency_is_rejected(self):
        values = {"Recommended Contingency MD": -1, "Contingency MD": -1,
                  "P25": 4, "P50": 4, "P75": 4.25, "P90": 4.75,
                  "Delivery Baseline": 4, "Management Reserve": 0.4, "Planning Total": 4.4}
        for table, column in (("tbl_range_reserve", "Effort MD"),
                              ("tbl_final_snapshot", "Value"), ("tbl_readme_control", "Value")):
            for field, value in values.items():
                self.fixture.set_value(table, field, column, value)
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2, report)
        self.assertEqual(report["findings"]["VAL-08/contingency-domain"]["result"], "Fail")

    def test_capacity_warning_requires_its_own_validation_row(self):
        _, _, rows = self.fixture.tables["tbl_resource_matrix"]
        rows[0][:] = [1, "FE", 0.7, 0.7, 3.5, 3.5, 3, 3.5 / 3]
        rows[-1][:] = [3, "Total FTE/week", 1.1, 1.1, 5.5, 5.5, 5, 1.1]
        self.fixture.set_value("tbl_readme_control", "Validation Summary", "Value", "Warning")
        self.fixture.set_value("tbl_validation_summary", "VAL-01", "Result", "Warning")
        self.fixture.set_value("tbl_validation_summary", "VAL-01", "Note",
                               "finding=VAL-05/FE/coverage; rationale=Reviewed staffing slack")
        self.fixture.tables["tbl_validation_summary"][2].append(["VAL-05", "Pass", "High", ""])
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2, report)
        self.assertEqual(report["findings"]["DISCLOSURE/VAL-05/FE/coverage"]["result"], "Fail")
        self.assertEqual(report["findings"]["DISCLOSURE/Validation Summary"]["expected"], "Fail")
        self.assertEqual(report["findings"]["DISCLOSURE/Validation Summary"]["result"], "Fail")

    def test_failed_readme_summary_cannot_return_pass(self):
        self.fixture.set_value("tbl_readme_control", "Validation Summary", "Value", "Fail")
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (2, "Fail"))

    def test_minimal_valid_artifact_checks_literal_and_cached_inputs(self):
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (0, "Pass"), report)
        self.assertEqual(float(report["findings"]["VAL-08/range/P90"]["expected"]), 7)
        self.assertEqual(report["findings"]["VAL-01/SG1 Features/FE"]["actual"], "3")
        self.assertEqual(report["findings"]["VAL-05/Average FTE"]["actual"], "1")

    def test_recalculation_sheet_quotes_preserve_formula_meaning(self):
        self.fixture.set_value("tbl_sizing_summary", "SG1 Features", "FE",
                               Formula('=IF("FALSE"="FALSE",IF(FALSE,0,SUM(\'Sizing\'!B2:B2)),0)', 3))
        self.fixture.write()
        _, address = self.fixture.positions[("tbl_sizing_summary", "SG1 Features", "FE")]
        member = "xl/worksheets/sheet3.xml"
        cases = (
            ('IF("FALSE"="FALSE",IF(FALSE(),0,SUM(Sizing!B2)),0)', "Pass"),
            ('IF("FALSE"="FALSE",IF(FALSE(),0,SUM(Sizing!C2)),0)', "Fail"),
            ('IF("FALSE"="FALSE",IF(TRUE(),0,SUM(Sizing!B2)),0)', "Fail"),
            ('IF("TRUE"="FALSE",IF(FALSE(),0,SUM(Sizing!B2)),0)', "Fail"),
        )
        for expression, expected in cases:
            with ZipFile(self.fixture.workbook) as archive:
                files = {name: archive.read(name) for name in archive.namelist()}
            tree = ET.fromstring(files[member])
            tree.find(f".//s:c[@r='{address}']/s:f", NS).text = expression
            files[member] = ET.tostring(tree, encoding="utf-8", xml_declaration=True)
            with ZipFile(self.fixture.workbook, "w", ZIP_DEFLATED) as archive:
                for name, data in files.items():
                    archive.writestr(name, data)
            _, report = self.fixture.run()
            self.assertEqual(report["findings"]["TRANSFER/tbl_sizing_summary/1/FE"]["result"],
                             expected)

    def test_wrong_monotonic_ranges_fail_even_when_markdown_agrees(self):
        for table, column in (("tbl_range_reserve", "Effort MD"), ("tbl_final_snapshot", "Value"), ("tbl_readme_control", "Value")):
            self.fixture.set_value(table, "P75", column, 7.5)
            self.fixture.set_value(table, "P90", column, 8.5)
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-08/range/P75"]["result"], "Fail")
        self.assertEqual(float(report["findings"]["VAL-08/range/P90"]["expected"]), 7)
        self.assertEqual(report["findings"]["VAL-08/range/P90"]["result"], "Fail")

    def test_offset_cached_role_errors_cannot_hide_in_grand_total(self):
        self.fixture.write()
        for role, value in (("FE", 4), ("BE", 1)):
            sheet, cell = self.fixture.positions[("tbl_sizing_summary", "SG1 Features", role)]
            self.fixture.mutate_xml(sheet, cell, value, cache=True)
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-01/SG1 Features/FE"]["result"], "Fail")
        self.assertEqual(report["findings"]["VAL-01/SG1 Features/BE"]["result"], "Fail")
        self.assertEqual(report["findings"]["VAL-02/SG1 Features/total"]["result"], "Pass")

    def test_task_coercion_and_leading_zero_loss_fail(self):
        self.fixture.write()
        for task, actual in (("3.1", 3), ("3.10", 3.1), ("001", 1)):
            sheet, cell = self.fixture.positions[("tbl_task_timeline", task, "#")]
            self.fixture.mutate_xml(sheet, cell, actual)
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        for index in (1, 2, 3):
            self.assertEqual(report["findings"][f"TRANSFER/tbl_task_timeline/{index}/#"]["result"], "Fail")

    def test_hidden_warning_fails_all_pass_validation_summary(self):
        self.fixture.set_value("tbl_sizing_summary", "Non-Dev", "QA vs FE+BE Check", "Warning")
        self.fixture.write()
        code, report = self.fixture.run()
        key = "ROW-CHECK/tbl_sizing_summary/Non-Dev/QA vs FE+BE Check"
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"][key]["result"], "Warning")
        self.assertEqual(report["findings"][f"DISCLOSURE/{key}"]["result"], "Fail")
        self.assertEqual(report["findings"]["DISCLOSURE/Validation Summary"]["result"], "Fail")

    def test_disclosed_allowed_warning_remains_warning(self):
        self.fixture.set_value("tbl_sizing_summary", "Non-Dev", "QA vs FE+BE Check", "Warning")
        self.fixture.set_value("tbl_readme_control", "Validation Summary", "Value", "Warning")
        self.fixture.tables["tbl_validation_summary"][2].append([
            "VAL-03", "Warning", "High",
            "row=Non-Dev; rationale=Reviewed exception for non-development QA effort"])
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (1, "Warning"), report)
        self.assertEqual(report["findings"]["DISCLOSURE/ROW-CHECK/tbl_sizing_summary/Non-Dev/QA vs FE+BE Check"]["result"], "Pass")

    def test_missing_cache_is_never_pass(self):
        self.fixture.set_value("tbl_sizing_features", "FN-01.01", "Total", Formula("=SUM(B2:C2)", None))
        self.fixture.set_value("tbl_readme_control", "Calculation Status", "Value", "Not recalculated")
        self.fixture.set_value("tbl_readme_control", "Validation Summary", "Value", "Warning")
        for check in ("VAL-02", "VAL-14"):
            self.fixture.tables["tbl_validation_summary"][2].append([
                check, "Warning", "High",
                "cell='Sizing'!D2; action=Recalculate this formula before publication"])
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (1, "Warning"), report)
        self.assertEqual(report["findings"]["FORMULA-CACHE/'Sizing'!D2"]["result"], "Warning")
        self.assertEqual(report["findings"]["VAL-02/row/tbl_sizing_features/FN-01.01"]["result"], "Warning")

    def test_raw_row_width_rejected_before_tolerant_parser(self):
        self.fixture.write()
        source = self.fixture.markdown.read_text(encoding="utf-8")
        self.fixture.markdown.write_text(source.replace("| FN-01.01 | SG1 |", "| FN-01.01 | SG1 | discarded |"), encoding="utf-8")
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["counts"]["Fail"], 1)
        self.assertEqual(next(iter(report["findings"].values()))["actual"], 3)
        self.assertTrue(next(iter(report["findings"])).startswith("SOURCE-WIDTH/"))

    def test_numeric_literal_transfer_and_formula_error_fail(self):
        self.fixture.write()
        sheet, cell = self.fixture.positions[("tbl_sizing_features", "FN-01.01", "FE")]
        self.fixture.mutate_xml(sheet, cell, 30)
        sheet, cell = self.fixture.positions[("tbl_sizing_features", "FN-01.01", "Total")]
        self.fixture.mutate_xml(sheet, cell, "#DIV/0!", cache=True, error=True)
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["TRANSFER/tbl_sizing_features/1/FE"]["result"], "Fail")
        self.assertEqual(report["findings"]["FORMULA-ERROR/'Sizing'!D2"]["result"], "Fail")

    def test_capacity_slack_does_not_define_average_fte(self):
        self.fixture.set_value("tbl_readme_control", "FE Average FTE", "Value", 0.7)
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-05/FE/Average FTE"]["expected"], "0.6")
        self.assertEqual(report["findings"]["VAL-05/FE/Average FTE"]["result"], "Fail")

    def test_missing_control_is_explicit_and_disclosable(self):
        _, _, rows = self.fixture.tables["tbl_readme_control"]
        rows[:] = [row for row in rows if row[0] != "Delivery Weeks"]
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-05/controls"]["result"], "Warning")
        self.assertEqual(report["findings"]["VAL-05/FE/Average FTE"]["result"], "Warning")

    def test_bucket_membership_uses_exact_inventory_lookup(self):
        self.fixture.set_value("tbl_feature_inventory", "FN-01.01", "SG", "SG2")
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-01/SG1 Features/FE"]["expected"], "0")
        self.assertEqual(report["findings"]["VAL-01/SG2 Features/FE"]["expected"], "3")
        self.assertEqual(report["findings"]["VAL-01/Raw Grand Total/FE"]["result"], "Pass")

    def test_reserve_cannot_be_folded_into_delivery_baseline(self):
        for table, column in (("tbl_range_reserve", "Effort MD"), ("tbl_final_snapshot", "Value"), ("tbl_readme_control", "Value")):
            self.fixture.set_value(table, "Delivery Baseline", column, 6.6)
        self.fixture.write()
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["VAL-08/range/Delivery Baseline"]["expected"], "6")
        self.assertEqual(report["findings"]["DUPLICATE/snapshot/Delivery Baseline"]["result"], "Fail")

    def test_required_table_header_must_exist_in_actual_file(self):
        self.fixture.write()
        self.fixture.mutate_xml("Features", "A1", 42)
        code, report = self.fixture.run()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["STRUCTURE/header/tbl_feature_inventory"]["result"], "Fail")

    def test_preflight_passes_complete_markdown_without_a_workbook(self):
        self.fixture.complete_required_rows()
        code, report = self.fixture.preflight()
        failures = {k: f for k, f in report["findings"].items() if f["result"] != "Pass"}
        self.assertEqual((code, report["mode"], failures), (0, "markdown-only", {}))
        self.assertEqual(set(report["inputs"]), {"markdown", "config"})

    def test_preflight_rejects_range_label_the_workbook_verifier_cannot_find(self):
        self.fixture.complete_required_rows()
        self.fixture.set_value("tbl_range_reserve", "Recommended Contingency MD", "Category / Scenario", "Recommended Contingency")
        code, report = self.fixture.preflight()
        finding = report["findings"]["PREFLIGHT/required-row/tbl_range_reserve/Recommended Contingency MD"]
        self.assertEqual((code, finding["result"], finding["actual"]), (2, "Fail", "Recommended Contingency"))

    def test_preflight_requires_role_controls_for_every_summary_role(self):
        self.fixture.complete_required_rows()
        controls = self.fixture.tables["tbl_readme_control"][2]
        controls[:] = [row for row in controls if row[0] != "BE Buffer Rate"]
        code, report = self.fixture.preflight()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["PREFLIGHT/required-row/tbl_readme_control/BE Buffer Rate"]["result"], "Fail")

    def test_preflight_literal_warning_needs_disclosure_and_summary_rollup(self):
        self.fixture.complete_required_rows()
        self.fixture.set_value("tbl_sizing_summary", "Non-Dev", "QA vs FE+BE Check", "Warning")
        code, report = self.fixture.preflight()
        self.assertEqual(code, 2)
        self.assertEqual(report["findings"]["DISCLOSURE/ROW-CHECK/tbl_sizing_summary/Non-Dev/QA vs FE+BE Check"]["result"], "Fail")
        self.assertEqual(report["findings"]["DISCLOSURE/Validation Summary"]["result"], "Fail")
        self.fixture.tables["tbl_validation_summary"][2].append(
            ["VAL-03", "Warning", "Medium", "finding=VAL-03; row=Non-Dev; rationale=QA sized from test cases"])
        self.fixture.set_value("tbl_readme_control", "Validation Summary", "Value", "Warning")
        code, report = self.fixture.preflight()
        failed = [k for k, f in report["findings"].items() if f["result"] == "Fail"]
        self.assertEqual((code, failed), (1, []))

    def test_preflight_defers_formula_checks_instead_of_passing_them(self):
        self.fixture.complete_required_rows()
        self.fixture.set_value("tbl_sizing_summary", "Non-Dev", "QA vs FE+BE Check", Formula('=IF(B5>0,"Warning","Pass")', "Warning"))
        code, report = self.fixture.preflight()
        self.assertEqual(code, 0)
        self.assertIn("1 check cells are formulas", report["deferred"][0])
        self.assertNotIn("ROW-CHECK/tbl_sizing_summary/Non-Dev/QA vs FE+BE Check", report["findings"])

    def test_preflight_rejects_formula_like_literal_text(self):
        self.fixture.complete_required_rows()
        self.fixture.set_value("tbl_readme_control", "Project Name", "Note", "=HYPERLINK(1)")
        self.fixture.set_value("tbl_readme_control", "Version", "Note", "- trailing bullet")
        self.fixture.set_value("tbl_readme_control", "Raw MD", "Note", "-4")
        code, report = self.fixture.preflight()
        unsafe = sorted(f["actual"] for k, f in report["findings"].items() if k.startswith("FORMULA-SAFETY/"))
        self.assertEqual((code, unsafe), (2, ["- trailing bullet", "=HYPERLINK(1)"]))

    def test_mode_requires_exactly_one_of_workbook_or_markdown_only(self):
        self.fixture.write()
        base = [sys.executable, str(VERIFIER), "--input", str(self.fixture.markdown),
                "--config", str(self.fixture.config), "--output", str(self.fixture.report)]
        for extra in ([], ["--markdown-only", "--workbook", str(self.fixture.workbook)]):
            result = subprocess.run(base + extra, capture_output=True, text=True)
            self.assertEqual(result.returncode, 3)
            self.assertFalse(self.fixture.report.exists())

    def test_input_error_has_separate_exit(self):
        self.fixture.write()
        self.fixture.workbook.unlink()
        code, report = self.fixture.run()
        self.assertEqual((code, report["status"]), (3, "Error"))
        self.assertIn("FileNotFoundError", report["error"])


if __name__ == "__main__":
    unittest.main()
