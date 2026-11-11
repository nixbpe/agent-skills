#!/usr/bin/env python3
"""Read-only verification of one estimation workbook.

Default mode compares the reviewed Markdown with the delivered XLSX.
`--markdown-only` checks the Markdown alone before the review gate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from openpyxl import load_workbook
from openpyxl.formula.tokenizer import Tokenizer
import yaml

from md_to_workbook import (
    MdTable, _is_separator_row, _safe_sheet_name, _short_sheet_name,
    _split_md_table_row, _table_name_from_config, parse_markdown,
)

TOLERANCE = Decimal("0.000001")
SEVERITY = {"Pass": 0, "Warning": 1, "Fail": 2}
LIMITATIONS = [
    "Numeric and Markdown-to-XLSX checks only; not semantic approval, actor-permission, or upstream source proofs.",
    "Formula caches are observed in the delivered XLSX; their presence does not prove fresh recalculation.",
    "No Excel formula evaluator, dependency-graph proof, QA case reconstruction, or independent PM calendar derivation.",
    "Canonical controls only; unsupported or missing computation inputs remain Warning.",
    "Configured sheet/table presence is checked; this is not a complete canonical schema or visual-layout audit.",
    "Risk probability/impact derivation, recommended-contingency components, warranty schedule capacity and qualitative VAL rules require separate review.",
]

PREFLIGHT_LIMITATIONS = [
    "Markdown-only: no XLSX, formula result or cached value is read. Run the workbook verifier after export.",
    "Required rows, row widths, registry tables, formula-like literals and literal Warning/Fail disclosure only.",
    "Check cells written as formulas are deferred until recalculation; a clean preflight does not predict their result.",
    "No numeric reconciliation, A1 address resolution, semantic source review or visual-layout audit.",
]
SUMMARY_METADATA = {"Bucket", "Bucket Total", "% of Raw Grand Total",
                    "QA vs FE+BE Check", "Bucket Sum Check"}
RANGE_ROWS = ["Adjusted MD", "Recommended Contingency MD", "Selected Commitment Uplift",
              "Contingency MD", "Delivery Baseline", "Management Reserve", "Planning Total",
              "P25", "P50", "P75", "P90"]
# Labels the canonical contract requires and the workbook verifier looks up by exact text.
REQUIRED_ROWS = {
    "tbl_readme_control": ("Field", [
        "Workbook Name", "Project Name", "Version", "Generated Date", "Source Artifacts",
        "Approved Baseline Scope", "Approval State", "Approval Basis", "No-Pricing Rule",
        "Raw MD", "Adjusted MD", "Delivery Baseline", "Management Reserve", "Planning Total",
        "P25", "P50", "P75", "P90", "Confidence", "Integration Count", "External Risk Count",
        "Top Risks", "Re-estimation Triggers", "Baseline-vs-Scenario Note", "Validation Summary",
        "Calculation Status", "Working Days per Week", "Focus Factor", "Delivery Weeks",
        "PM Base MD", "Recommended Contingency MD", "Selected Commitment Uplift",
        "Contingency MD", "Selected Delivery Basis", "Reserve Rate", "Reserve Denominator"]),
    "tbl_sizing_summary": ("Bucket", ["SG1 Features", "SG2 Features", "Integration", "Non-Dev",
                                      "Raw Grand Total"]),
    "tbl_range_reserve": ("Category / Scenario", RANGE_ROWS),
    "tbl_final_snapshot": ("Field", RANGE_ROWS + ["Selected Delivery Basis", "Top Risks",
                                                  "Confidence", "Re-estimation Triggers"]),
}
ROLE_CONTROLS = ("Raw MD", "Rework Rate", "Buffer Rate", "Adjusted MD",
                 "Warranty Adjusted MD", "Delivery Adjusted MD")
KEY_COLUMNS = ("Subfeature ID", "ID", "INT ID", "ND ID", "#", "Bucket", "Field",
               "Category / Scenario", "Role")


def number(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    text = str(value).strip()
    if not re.fullmatch(r"[+-]?(?:\d+(?:,\d{3})*(?:\.\d*)?|\.\d+)\s*%?", text):
        return None
    try:
        result = Decimal(text.rstrip("%").strip().replace(",", ""))
        return result / 100 if text.endswith("%") else result
    except InvalidOperation:
        return None


def formula_tokens(expression):
    tokens = Tokenizer(expression).items
    result = []
    skip_close = False
    for index, token in enumerate(tokens):
        if skip_close:
            skip_close = False
            continue
        value = token.value
        if token.type == "FUNC" and value.upper() in {"TRUE(", "FALSE("}:
            if index + 1 < len(tokens) and tokens[index + 1].type == "FUNC" and tokens[index + 1].subtype == "CLOSE":
                result.append(("OPERAND", "LOGICAL", value[:-1].upper()))
                skip_close = True
                continue
        if token.type == "WHITE-SPACE":
            adjacent = tokens[max(0, index - 1):index] + tokens[index + 1:index + 2]
            if len(adjacent) != 2 or any(t.subtype != "RANGE" for t in adjacent):
                continue
            value = " "
        if token.subtype == "RANGE":
            # Recalculation can remove optional sheet quotes, but never string-literal quotes.
            value = re.sub(r"^'([^\W\d]\w*)'!", r"\1!", value)
            value = re.sub(r"(\$?[A-Z]{1,3}\$?\d+):\1$", r"\1", value, flags=re.IGNORECASE)
        result.append((token.type, token.subtype, value))
    return result


@dataclass
class Cell:
    table: str
    row: str
    column: str
    ref: str
    source: str
    actual: Any
    cached: Any
    data_type: str

    def evidence(self) -> dict:
        return {"table": self.table, "row": self.row, "column": self.column,
                "cell": self.ref, "source": self.source, "actual": self.actual,
                "cached": self.cached, "data_type": self.data_type}


@dataclass
class BoundTable:
    source: MdTable
    rows: list[dict[str, Cell]]


class Verification:
    def __init__(self):
        self.findings: dict[str, dict] = {}
        self.tables: dict[str, BoundTable] = {}

    def add(self, key, result, expected, actual, evidence=(), note=""):
        self.findings[key] = {"result": result, "expected": expected, "actual": actual,
                              "evidence": [c.evidence() if isinstance(c, Cell) else c for c in evidence],
                              "note": note}

    def compare(self, key, expected, cell):
        actual = number(cell.cached) if cell else None
        if expected is None or actual is None:
            self.add(key, "Warning", expected, actual, [cell] if cell else [],
                     "Required numeric input or result is missing or unsupported.")
        else:
            self.add(key, "Pass" if abs(expected - actual) <= TOLERANCE else "Fail",
                     expected, actual, [cell])

    def numeric(self, cell):
        if cell is None:
            return None
        # Literal inputs come from Markdown, never the renderer's coercion routine.
        return number(cell.cached) if cell.source.startswith("`=") else number(cell.source)

    def index(self, table, key, value):
        bound = self.tables.get(table)
        if not bound or key not in bound.source.header or value not in bound.source.header:
            self.add(f"INPUT/{table}", "Warning", f"{key}, {value}", None,
                     note="Required computation table or columns unavailable.")
            return {}
        result = {}
        for row in bound.rows:
            label = row[key].source
            if label in result:
                self.add(f"DUPLICATE/{table}/{label}", "Fail", "unique key", label, [row[key]])
            else:
                result[label] = row[value]
        return result


def raw_widths(path, verification):
    lines = path.read_text(encoding="utf-8").splitlines()
    fenced = False
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            fenced = not fenced
        if not fenced and "|" in lines[i] and i + 1 < len(lines) and _is_separator_row(_split_md_table_row(lines[i + 1].strip())):
            width = len(_split_md_table_row(lines[i].strip()))
            j = i + 1
            while j < len(lines) and lines[j].strip() and "|" in lines[j]:
                actual = len(_split_md_table_row(lines[j].strip()))
                if actual != width:
                    verification.add(f"SOURCE-WIDTH/{j + 1}", "Fail", width, actual,
                                     [{"file": str(path), "line": j + 1}],
                                     "Rejected before parse_markdown can pad or truncate this row.")
                j += 1
            i = j
        else:
            i += 1
    return not verification.findings


def check_registry(sections, registry, v):
    for entry in registry:
        matching = [s for s in sections if entry.get("heading", "") and entry["heading"] in s.heading]
        if len(matching) != 1:
            v.add(f"STRUCTURE/config/{entry.get('heading')}", "Fail", "one source section", len(matching))
            continue
        names = [t.table_name or _table_name_from_config(matching[0].heading, i, registry)
                 for i, t in enumerate(matching[0].tables)]
        required = [t["name"] for t in entry.get("tables", [])]
        v.add(f"STRUCTURE/tables/{entry['heading']}", "Pass" if names == required else "Fail", required, names)


def key_column(header):
    return next((h for h in KEY_COLUMNS if h in header), header[0])


def bind_source(sections, registry, v):
    """Bind Markdown rows without a workbook; only literal cells carry a value."""
    for section in sections:
        sheet_name = _safe_sheet_name(_short_sheet_name(section.heading, registry))
        if not section.tables:
            v.add(f"STRUCTURE/empty/{sheet_name}", "Fail", "at least one table", 0)
        for i, table in enumerate(section.tables):
            name = table.table_name or _table_name_from_config(section.heading, i, registry)
            name = name or f"{sheet_name}/table-{i + 1}"
            if name in v.tables:
                v.add(f"STRUCTURE/duplicate/{name}", "Fail", "unique table", name)
                continue
            if len(set(table.header)) != len(table.header):
                v.add(f"STRUCTURE/columns/{name}", "Fail", "unique headers", table.header)
                continue
            key = key_column(table.header)
            rows = []
            for offset, source in enumerate(table.rows, 1):
                row_key = source[table.header.index(key)]
                rows.append({
                    header: Cell(name, row_key, header, f"markdown:{name}/row {offset}/{header}", text, None,
                                 None if text.startswith("`=") else text,
                                 "f" if text.startswith("`=") else "s")
                    for header, text in zip(table.header, source)})
            v.tables[name] = BoundTable(table, rows)


def bind_tables(sections, cfg, formulas, cached, v):
    registry = cfg.get("sheets", []) or []
    expected_sheets = [_safe_sheet_name(_short_sheet_name(s.heading, registry)) for s in sections]
    v.add("STRUCTURE/sheet-order", "Pass" if expected_sheets == formulas.sheetnames else "Fail",
          expected_sheets, formulas.sheetnames)
    check_registry(sections, registry, v)
    for section, sheet_name in zip(sections, expected_sheets):
        if sheet_name not in formulas:
            continue
        ws, values = formulas[sheet_name], cached[sheet_name]
        cursor = 1
        if not section.tables:
            v.add(f"STRUCTURE/empty/{sheet_name}", "Fail", "at least one table", 0)
        for i, table in enumerate(section.tables):
            name = table.table_name or _table_name_from_config(section.heading, i, registry)
            name = name or f"{sheet_name}/table-{i + 1}"
            if name in v.tables:
                v.add(f"STRUCTURE/duplicate/{name}", "Fail", "unique table", name)
                continue
            header_row = next((r for r in range(cursor, ws.max_row + 1)
                               if [ws.cell(r, c).value for c in range(1, len(table.header) + 1)] == table.header), None)
            if header_row is None:
                v.add(f"STRUCTURE/header/{name}", "Fail", table.header, None,
                      [{"sheet": sheet_name, "starting_row": cursor}])
                continue
            v.add(f"STRUCTURE/header/{name}", "Pass", table.header, table.header,
                  [{"sheet": sheet_name, "row": header_row}])
            if len(set(table.header)) != len(table.header):
                v.add(f"STRUCTURE/columns/{name}", "Fail", "unique headers", table.header)
                continue
            rows = []
            for offset, source in enumerate(table.rows, 1):
                row = {}
                row_key = source[table.header.index(key_column(table.header))]
                for col, (header, text) in enumerate(zip(table.header, source), 1):
                    observed = ws.cell(header_row + offset, col)
                    cell = Cell(name, row_key, header, f"'{sheet_name}'!{observed.coordinate}",
                                text, observed.value, values.cell(observed.row, col).value, observed.data_type)
                    row[header] = cell
                    key = f"TRANSFER/{name}/{offset}/{header}"
                    identifier = header == "ID" or header.endswith(" ID") or (header == "#" and name == "tbl_task_timeline")
                    if identifier:
                        okay = observed.value == text and observed.data_type != "f" and isinstance(observed.value, str)
                        if not text and observed.value is None:
                            okay = True
                        v.add(key, "Pass" if okay else "Fail", text, observed.value, [cell], "Exact lexical identifier comparison.")
                    elif text.startswith("`=") and text.endswith("`"):
                        okay = observed.data_type == "f" and formula_tokens(observed.value) == formula_tokens(text[1:-1])
                        v.add(key, "Pass" if okay else "Fail", text[1:-1], observed.value, [cell])
                    elif number(text) is not None:
                        actual_number = number(cell.cached)
                        okay = isinstance(cell.cached, (int, float)) and not isinstance(cell.cached, bool)
                        okay = okay and actual_number is not None and abs(number(text) - actual_number) <= TOLERANCE
                        v.add(key, "Pass" if okay and observed.data_type != "f" else "Fail",
                              number(text), cell.cached, [cell])
                    elif header in {"Field", "Bucket", "SG", "Role", "Category / Scenario"}:
                        v.add(key, "Pass" if observed.value == text else "Fail", text, observed.value, [cell])
                rows.append(row)
            v.tables[name] = BoundTable(table, rows)
            cursor = header_row + len(table.rows) + 1
    for ws in formulas:
        for row in ws:
            for cell in row:
                value = cached[ws.title][cell.coordinate]
                ref = f"'{ws.title}'!{cell.coordinate}"
                if cell.data_type == "e" or value.data_type == "e":
                    v.add(f"FORMULA-ERROR/{ref}", "Fail", "no spreadsheet error", value.value,
                          [{"cell": ref, "formula": cell.value}])
                elif cell.data_type == "f" and value.value is None:
                    v.add(f"FORMULA-CACHE/{ref}", "Warning", "cached result", None,
                          [{"cell": ref, "formula": cell.value}], "Not recalculated or cache unavailable.")


def sum_numbers(values):
    values = list(values)
    return None if any(value is None for value in values) else sum(values, Decimal(0))


def verify_sizing(v, controls):
    summary = v.tables.get("tbl_sizing_summary")
    if not summary or "Bucket" not in summary.source.header or "Bucket Total" not in summary.source.header:
        v.add("VAL-01/inputs", "Warning", "canonical sizing summary", None)
        return {}
    roles = [header for header in summary.source.header if header not in SUMMARY_METADATA]
    bucket_names = ("SG1 Features", "SG2 Features", "Integration", "Non-Dev")
    sums = {bucket: {role: [] for role in roles} for bucket in bucket_names}
    groups = v.index("tbl_feature_inventory", "Subfeature ID", "SG")
    complete = True
    for table_name, bucket in (("tbl_sizing_features", None), ("tbl_sizing_integrations", "Integration"), ("tbl_sizing_non_dev", "Non-Dev")):
        table = v.tables.get(table_name)
        if table is None:
            v.add(f"VAL-01/inputs/{table_name}", "Warning", "detail table", None)
            complete = False
            continue
        detail_headers = table.source.header
        role_headers = [header for header in detail_headers
                        if header in roles or f"{header} Raw MD" in controls]
        omitted = [header for header in role_headers if header not in roles]
        if omitted:
            v.add(f"VAL-01/omitted-roles/{table_name}", "Fail", "every detail role in summary", omitted)
        for row in table.rows:
            first = next(iter(row.values()))
            selected = bucket
            if selected is None:
                identity = row.get("Subfeature ID")
                group = groups.get(identity.source) if identity else None
                selected = f"{group.source} Features" if group else None
                if selected not in sums:
                    v.add(f"VAL-02/SG/{first.row}", "Fail", "exact Subfeature ID mapped to SG1 or SG2", selected, [first])
                    complete = False
                    continue
            values = []
            for role in roles:
                amount = v.numeric(row[role]) if role in row else Decimal(0)
                sums[selected][role].append(amount)
                values.append(amount)
            v.compare(f"VAL-02/row/{table_name}/{first.row}", sum_numbers(values), row.get("Total"))
    indexed = {}
    for row in summary.rows:
        bucket = row["Bucket"].source
        if bucket in indexed:
            v.add(f"VAL-02/duplicate/{bucket}", "Fail", "one bucket", bucket, [row["Bucket"]])
        indexed[bucket] = row
    unexpected = set(indexed) - set(bucket_names) - {"Raw Grand Total"}
    if unexpected:
        v.add("VAL-02/unexpected-buckets", "Fail", list(bucket_names) + ["Raw Grand Total"], sorted(unexpected))
    totals = {}
    for bucket in (*bucket_names, "Raw Grand Total"):
        row = indexed.get(bucket, {})
        expectations = []
        for role in roles:
            inputs = sums[bucket][role] if bucket in sums else [x for b in sums.values() for x in b[role]]
            expected = sum_numbers(inputs) if complete else None
            expectations.append(expected)
            v.compare(f"VAL-01/{bucket}/{role}", expected, row.get(role))
            if bucket == "Raw Grand Total":
                totals[role] = expected
        v.compare(f"VAL-02/{bucket}/total", sum_numbers(expectations), row.get("Bucket Total"))
    v.compare("VAL-01/Raw MD", sum_numbers(totals.values()), controls.get("Raw MD"))
    return totals


def verify_adjusted(v, controls, raw):
    adjusted = {}
    for role, amount in raw.items():
        v.compare(f"VAL-04/{role}/Raw MD", amount, controls.get(f"{role} Raw MD"))
        rework = v.numeric(controls.get(f"{role} Rework Rate"))
        buffer = v.numeric(controls.get(f"{role} Buffer Rate"))
        expected = amount * (1 + rework + buffer) if None not in (amount, rework, buffer) else None
        if f"{role} Rework MD" in controls:
            v.compare(f"VAL-04/{role}/Rework MD", amount * rework if None not in (amount, rework) else None, controls[f"{role} Rework MD"])
        if f"{role} Buffer MD" in controls:
            v.compare(f"VAL-04/{role}/Buffer MD", amount * buffer if None not in (amount, buffer) else None, controls[f"{role} Buffer MD"])
        v.compare(f"VAL-04/{role}/Adjusted MD", expected, controls.get(f"{role} Adjusted MD"))
        adjusted[role] = expected
    pm = v.numeric(controls.get("PM Base MD"))
    if pm is None:
        v.add("VAL-04/PM Base MD", "Warning", "explicit PM Base MD, including zero", None)
    # PM base is added once; any PM detail is already part of the role sum.
    expected = sum_numbers([*adjusted.values(), pm])
    v.compare("VAL-04/Adjusted MD", expected, controls.get("Adjusted MD"))


def verify_ranges(v, controls):
    ranges = v.index("tbl_range_reserve", "Category / Scenario", "Effort MD")
    snapshot = v.index("tbl_final_snapshot", "Field", "Value")
    a = v.numeric(ranges.get("Adjusted MD"))
    c = v.numeric(ranges.get("Recommended Contingency MD"))
    if c is not None and c < 0:
        v.add("VAL-08/contingency-domain", "Fail", "non-negative Recommended Contingency MD",
              c, [ranges["Recommended Contingency MD"]])
    expected = {"Adjusted MD": a, "Recommended Contingency MD": c}
    if a is None or c is None:
        v.add("VAL-08/inputs", "Warning", "Adjusted MD and Recommended Contingency MD", [a, c])
    else:
        half = c * Decimal("0.5")
        step = max(half, a * Decimal("0.05"))
        expected.update({"P25": a + min(c, step), "P50": a + c, "P75": a + c + step,
                         "P90": a + c + step + max(half, a * Decimal("0.10"))})
    basis_cell = controls.get("Selected Delivery Basis")
    basis = basis_cell.cached if basis_cell else None
    baseline = expected.get(basis) if basis in ("P25", "P50", "P75", "P90") else None
    if baseline is None:
        v.add("VAL-08/Selected Delivery Basis", "Warning", "P25/P50/P75/P90", basis)
    expected["Delivery Baseline"] = baseline
    expected["Selected Commitment Uplift"] = baseline - expected["P50"] if baseline is not None else None
    expected["Contingency MD"] = baseline - a if baseline is not None else None
    rate = v.numeric(controls.get("Reserve Rate"))
    denominator_cell = controls.get("Reserve Denominator")
    denominator = denominator_cell.cached if denominator_cell else None
    reserve_base = {"Adjusted MD": a, "Delivery Baseline": baseline}.get(denominator)
    reserve = rate * reserve_base if None not in (rate, reserve_base) else None
    if reserve is None:
        v.add("VAL-07/reserve-policy", "Warning", "Reserve Rate and Reserve Denominator (Adjusted MD or Delivery Baseline)", [rate, denominator])
    expected["Management Reserve"] = reserve
    expected["Planning Total"] = baseline + reserve if None not in (baseline, reserve) else None
    for label, amount in expected.items():
        v.compare(f"VAL-08/range/{label}", amount, ranges.get(label))
        v.compare(f"DUPLICATE/snapshot/{label}", amount, snapshot.get(label))
        if label in ("Adjusted MD", "Delivery Baseline", "Management Reserve", "Planning Total", "P25", "P50", "P75", "P90") or label in controls:
            v.compare(f"DUPLICATE/README/{label}", amount, controls.get(label))
    selected = snapshot.get("Selected Delivery Basis")
    v.add("DUPLICATE/snapshot/Selected Delivery Basis", "Pass" if selected and selected.cached == basis and basis else "Fail",
          basis, selected.cached if selected else None, [selected] if selected else [])


def verify_capacity(v, controls, raw):
    table = v.tables.get("tbl_resource_matrix")
    days = v.numeric(controls.get("Working Days per Week"))
    focus = v.numeric(controls.get("Focus Factor"))
    horizon = v.numeric(controls.get("Delivery Weeks"))
    if not table or "Role" not in table.source.header:
        v.add("VAL-05/inputs", "Warning", "canonical resource matrix", None)
        return
    weeks = [h for h in table.source.header if re.fullmatch(r"W\d+", h)]
    if not weeks or days is None or focus is None or horizon is None:
        v.add("VAL-05/controls", "Warning", "weekly columns, Working Days per Week, Focus Factor, Delivery Weeks", [weeks, days, focus, horizon])
    if any(x is not None and x <= 0 for x in (days, focus, horizon)):
        v.add("VAL-05/control-domain", "Fail", "positive workdays, focus and horizon", [days, focus, horizon])
        return
    if horizon is not None:
        v.add("VAL-05/horizon", "Pass" if weeks == [f"W{i}" for i in range(1, int(horizon) + 1)] and horizon == int(horizon) else "Fail", horizon, weeks)
    role_rows = [r for r in table.rows if r["Role"].source != "Total FTE/week"]
    expected_roles = set(raw) | {field.removesuffix(" Delivery Adjusted MD") for field in controls
                                 if field.endswith(" Delivery Adjusted MD")}
    pm = v.numeric(controls.get("PM Base MD"))
    if "PM Adjusted MD" in controls or (pm is not None and pm > 0):
        expected_roles.add("PM")
    for role in sorted(expected_roles - set(raw) - {"PM"}):
        for field in ("Raw MD", "Adjusted MD", "Warranty Adjusted MD", "Delivery Adjusted MD"):
            v.compare(f"VAL-05/{role}/unused/{field}", Decimal(0), controls.get(f"{role} {field}"))
    actual_roles = [row["Role"].source for row in role_rows]
    v.add("VAL-05/role-coverage",
          "Pass" if sorted(actual_roles) == sorted(expected_roles) else "Fail",
          sorted(expected_roles), sorted(actual_roles))
    demand_values = [v.numeric(controls.get(f"{role} Delivery Adjusted MD"))
                     for role in sorted(expected_roles)]
    allocation_values = []
    for row in role_rows:
        role = row["Role"].source
        allocated = sum_numbers(v.numeric(row[w]) for w in weeks) if weeks else None
        allocation_values.append(allocated)
        nominal = allocated * days if None not in (allocated, days) else None
        effective = nominal * focus if None not in (nominal, focus) else None
        demand = v.numeric(controls.get(f"{role} Delivery Adjusted MD"))
        full = v.numeric(controls.get(f"{role} Adjusted MD"))
        warranty = v.numeric(controls.get(f"{role} Warranty Adjusted MD"))
        v.compare(f"VAL-05/{role}/delivery-separation", full - warranty if None not in (full, warranty) else None, controls.get(f"{role} Delivery Adjusted MD"))
        for label, expected in (("FTE-Weeks", allocated), ("MD", nominal), ("Effective MD", effective), ("Adjusted MD", demand)):
            v.compare(f"VAL-05/{role}/{label}", expected, row.get(label))
        denominator = days * focus * horizon if None not in (days, focus, horizon) else None
        average = demand / denominator if demand is not None and denominator else None
        v.compare(f"VAL-05/{role}/Average FTE", average, controls.get(f"{role} Average FTE"))
        if f"{role} Allocation Average FTE" in controls:
            v.compare(f"VAL-05/{role}/Allocation Average FTE", allocated / horizon if allocated is not None and horizon else None, controls[f"{role} Allocation Average FTE"])
        if demand is not None and demand > 0 and effective is not None:
            ratio = effective / demand
            v.compare(f"VAL-05/{role}/Coverage Ratio", ratio, row.get("Coverage Ratio"))
            v.add(f"VAL-05/{role}/coverage", "Pass" if Decimal("0.95") <= ratio <= Decimal("1.05") else "Warning", "95%-105% delivery coverage", ratio, [row["Role"]], "Capacity tolerance is independent of numeric equality tolerance.")
        elif demand == 0:
            v.add(f"VAL-05/{role}/coverage", "Pass" if effective == 0 else "Warning", "zero demand requires zero capacity or reviewed rationale", effective, [row["Role"]])
    totals = [r for r in table.rows if r["Role"].source == "Total FTE/week"]
    if len(totals) != 1:
        v.add("VAL-05/total-row", "Fail", "one Total FTE/week row", len(totals))
    else:
        total = totals[0]
        for week in weeks:
            v.compare(f"VAL-05/total/{week}", sum_numbers(v.numeric(r[week]) for r in role_rows), total.get(week))
        allocated = sum_numbers(allocation_values)
        demand = sum_numbers(demand_values)
        nominal = allocated * days if None not in (allocated, days) else None
        effective = nominal * focus if None not in (nominal, focus) else None
        for label, expected in (("FTE-Weeks", allocated), ("MD", nominal), ("Effective MD", effective), ("Adjusted MD", demand)):
            v.compare(f"VAL-05/total/{label}", expected, total.get(label))
        if demand is not None and demand > 0 and effective is not None:
            v.compare("VAL-05/total/Coverage Ratio", effective / demand, total.get("Coverage Ratio"))
    demand = sum_numbers(demand_values)
    denominator = days * focus * horizon if None not in (days, focus, horizon) else None
    v.compare("VAL-05/Average FTE", demand / denominator if demand is not None and denominator else None, controls.get("Average FTE"))
    if "Allocation Average FTE" in controls:
        allocation = sum_numbers(allocation_values)
        v.compare("VAL-05/Allocation Average FTE", allocation / horizon if allocation is not None and horizon else None, controls["Allocation Average FTE"])


def row_checks(v):
    """Record every Warning/Fail check cell; return how many check cells are formulas."""
    formulas = 0
    for name, table in v.tables.items():
        for row in table.rows:
            for header, cell in row.items():
                check = header.endswith(" Check") or (name == "tbl_validation_summary" and header == "Result")
                check = check or (name == "tbl_readme_control" and header == "Value" and row.get("Field") and row["Field"].source.endswith(" Check"))
                if not check:
                    continue
                formulas += cell.source.startswith("`=")
                if cell.cached in ("Warning", "Fail"):
                    rationale = " ".join(str(row[h].cached or "") for h in ("Note", "Notes", "Rationale") if h in row)
                    v.add(f"ROW-CHECK/{name}/{cell.row}/{header}", cell.cached, "Pass or disclosed unresolved finding", cell.cached, [cell], rationale)
    return formulas


def is_disclosed(key, finding, disclosures):
    refs = [e.get("cell") for e in finding["evidence"] if e.get("cell")]
    rows = [e.get("row") for e in finding["evidence"] if isinstance(e.get("row"), str) and e["row"]]
    owner = key.split("/", 1)[0]
    if owner in ("FORMULA-CACHE", "FORMULA-ERROR", "TRANSFER"):
        owner = "VAL-14"
    elif owner == "ROW-CHECK":
        owner = {
            "QA vs FE+BE Check": "VAL-03", "Bucket Sum Check": "VAL-02",
            "Range Formula Check": "VAL-08", "Reserve Separation Check": "VAL-07",
            "INT Coverage Check": "VAL-09", "WBS Coverage Check": "VAL-13",
        }.get(key.rsplit("/", 1)[-1], owner)
    for row in disclosures:
        if re.fullmatch(r"VAL-\d{2}", owner):
            check_id = row.get("Check ID")
            if not check_id or check_id.cached != owner:
                continue
        note = str(row["Note"].cached or "") if "Note" in row else ""
        status = row["Result"].cached if "Result" in row else None
        identity = key in note or any(ref in note for ref in refs) or any(re.search(r"(?<![\w.-])" + re.escape(label) + r"(?![\w.-])", note) for label in rows)
        rationale = re.search(r"(?:rationale|action)\s*=\s*([^;\n]+)", note, re.IGNORECASE)
        if identity and rationale and SEVERITY.get(status, -1) >= SEVERITY[finding["result"]]:
            return True
    return False


DISCLOSURE_RULE = "README validation row with identifier/cell, unresolved severity and rationale/action"


def verify_disclosure(v, controls):
    summary = v.tables.get("tbl_validation_summary")
    row_checks(v)
    unresolved = [(key, finding) for key, finding in v.findings.items() if finding["result"] != "Pass"]
    disclosures = summary.rows if summary else []
    for key, finding in unresolved:
        if key.startswith("ROW-CHECK/tbl_validation_summary/"):
            continue
        disclosed = is_disclosed(key, finding, disclosures)
        v.add(f"DISCLOSURE/{key}", "Pass" if disclosed else "Fail", DISCLOSURE_RULE, "disclosed" if disclosed else "missing disclosure", finding["evidence"])
    highest = max((SEVERITY[f["result"]] for f in v.findings.values()), default=0)
    status_cell = controls.get("Validation Summary")
    status = status_cell.cached if status_cell else None
    expected = next(name for name, rank in SEVERITY.items() if rank == highest)
    v.add("DISCLOSURE/Validation Summary", "Pass" if status == expected else "Fail", expected, status, [status_cell] if status_cell else [])


def check_required_rows(v, controls):
    required = {table: (key, list(labels)) for table, (key, labels) in REQUIRED_ROWS.items()}
    summary = v.tables.get("tbl_sizing_summary")
    if summary:
        roles = [h for h in summary.source.header if h not in SUMMARY_METADATA]
        required["tbl_readme_control"][1].extend(f"{role} {field}" for role in roles for field in ROLE_CONTROLS)
    for table, (key, labels) in required.items():
        bound = v.tables.get(table)
        if not bound or key not in bound.source.header:
            v.add(f"PREFLIGHT/table/{table}", "Fail", f"table with a {key} column", None)
            continue
        present = [row[key].source for row in bound.rows]
        missing = [label for label in labels if label not in present]
        for label in missing:
            close = difflib.get_close_matches(label, present, n=1, cutoff=0.6)
            v.add(f"PREFLIGHT/required-row/{table}/{label}", "Fail", label, close[0] if close else None,
                  note=f"Row label must match exactly; closest existing row is {close[0]!r}." if close
                  else "Required row is missing.")
        if not missing:
            v.add(f"PREFLIGHT/required-rows/{table}", "Pass", len(labels), len(labels))
    for field, allowed in (("Selected Delivery Basis", ("P25", "P50", "P75", "P90")),
                           ("Reserve Denominator", ("Adjusted MD", "Delivery Baseline"))):
        cell = controls.get(field)
        if cell is not None and cell.data_type != "f":
            v.add(f"PREFLIGHT/control/{field}", "Pass" if cell.source in allowed else "Fail",
                  list(allowed), cell.source, [cell])
    matrix = v.tables.get("tbl_resource_matrix")
    if matrix and "Role" in matrix.source.header:
        totals = sum(row["Role"].source == "Total FTE/week" for row in matrix.rows)
        v.add("PREFLIGHT/resource-total-row", "Pass" if totals == 1 else "Fail", "one Total FTE/week row", totals)


def check_formula_safety(v):
    for name, table in v.tables.items():
        for offset, row in enumerate(table.rows, 1):
            for header, cell in row.items():
                text = cell.source.strip()
                if not text or text == "-" or text.startswith("`") or number(text) is not None:
                    continue
                if text[0] in "=+-@" or text.startswith("'="):
                    v.add(f"FORMULA-SAFETY/{name}/{offset}/{header}", "Fail",
                          "backtick-wrapped formula, number, or text with a non-formula prefix", text[:80], [cell],
                          "Literal text starting with =, +, - or @ can become a spreadsheet formula.")


def check_literal_disclosure(v, controls):
    """Disclosure for literal Warning/Fail cells; formula-driven checks are deferred."""
    deferred = []
    formulas = row_checks(v)
    if formulas:
        deferred.append(f"{formulas} check cells are formulas; their results and disclosure are verified after recalculation.")
    summary = v.tables.get("tbl_validation_summary")
    disclosures = summary.rows if summary else []
    highest = 0
    for key, finding in list(v.findings.items()):
        if not key.startswith("ROW-CHECK/"):
            continue
        highest = max(highest, SEVERITY[finding["result"]])
        if key.startswith("ROW-CHECK/tbl_validation_summary/"):
            continue
        disclosed = is_disclosed(key, finding, disclosures)
        v.add(f"DISCLOSURE/{key}", "Pass" if disclosed else "Fail", DISCLOSURE_RULE, "disclosed" if disclosed else "missing disclosure", finding["evidence"])
    status_cell = controls.get("Validation Summary")
    if status_cell is None:
        return deferred
    if status_cell.data_type == "f":
        deferred.append("Validation Summary is a formula; its roll-up is verified after recalculation.")
        return deferred
    floor = next(name for name, rank in SEVERITY.items() if rank == highest)
    okay = SEVERITY.get(status_cell.source, -1) >= highest
    v.add("DISCLOSURE/Validation Summary", "Pass" if okay else "Fail", f"{floor} or higher", status_cell.source, [status_cell],
          "Lower bound from literal check cells only.")
    return deferred


def summarize(v):
    counts = {result: sum(f["result"] == result for f in v.findings.values()) for result in SEVERITY}
    return ("Fail" if counts["Fail"] else "Warning" if counts["Warning"] else "Pass"), counts


def identify(paths):
    return {name: {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for name, path in paths.items()}


def load_config(path):
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg, dict):
        raise ValueError("Config must be a mapping")
    return cfg


def preflight(input_path, config_path):
    paths = {"markdown": Path(input_path), "config": Path(config_path)}
    identities = identify(paths)
    v = Verification()
    deferred = []
    if raw_widths(paths["markdown"], v):
        registry = load_config(paths["config"]).get("sheets", []) or []
        sections = parse_markdown(paths["markdown"])
        if not sections:
            v.add("STRUCTURE/source", "Fail", "workbook sections", [])
        check_registry(sections, registry, v)
        bind_source(sections, registry, v)
        controls = v.index("tbl_readme_control", "Field", "Value")
        check_required_rows(v, controls)
        check_formula_safety(v)
        deferred = check_literal_disclosure(v, controls)
    status, counts = summarize(v)
    return {"mode": "markdown-only", "status": status, "inputs": identities, "counts": counts,
            "deferred": deferred, "coverage_limitations": PREFLIGHT_LIMITATIONS, "findings": v.findings}


def verify(input_path, workbook_path, config_path):
    paths = {"markdown": Path(input_path), "workbook": Path(workbook_path), "config": Path(config_path)}
    identities = identify(paths)
    v = Verification()
    if raw_widths(paths["markdown"], v):
        cfg = load_config(paths["config"])
        sections = parse_markdown(paths["markdown"])
        if not sections:
            v.add("STRUCTURE/source", "Fail", "workbook sections", [])
        formulas = load_workbook(paths["workbook"], data_only=False)
        cached = load_workbook(paths["workbook"], data_only=True)
        try:
            bind_tables(sections, cfg, formulas, cached, v)
            controls = v.index("tbl_readme_control", "Field", "Value")
            raw = verify_sizing(v, controls)
            verify_adjusted(v, controls, raw)
            verify_ranges(v, controls)
            verify_capacity(v, controls, raw)
            verify_disclosure(v, controls)
        finally:
            formulas.close()
            cached.close()
    status, counts = summarize(v)
    return {"mode": "workbook", "status": status, "inputs": identities, "numeric_tolerance_md": str(TOLERANCE),
            "counts": counts, "coverage_limitations": LIMITATIONS, "findings": v.findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--workbook", type=Path, help="Delivered XLSX; required unless --markdown-only.")
    parser.add_argument("--markdown-only", action="store_true",
                        help="Preflight the Markdown before the review gate; reads no workbook.")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.markdown_only == (args.workbook is not None):
        print("Pass exactly one of --workbook or --markdown-only", file=sys.stderr)
        return 3
    if args.output.resolve() in {p.resolve() for p in (args.input, args.workbook, args.config) if p}:
        print("Report output must not overwrite an input", file=sys.stderr)
        return 3
    try:
        report = (preflight(args.input, args.config) if args.markdown_only
                  else verify(args.input, args.workbook, args.config))
        code = SEVERITY[report["status"]]
    except Exception as exc:
        report = {"status": "Error", "error": f"{type(exc).__name__}: {exc}",
                  "coverage_limitations": PREFLIGHT_LIMITATIONS if args.markdown_only else LIMITATIONS}
        code = 3
    try:
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Cannot write verification report: {exc}", file=sys.stderr)
        return 3
    print(f"{report['status']}: {args.output}")
    return code


if __name__ == "__main__":
    sys.exit(main())
