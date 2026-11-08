#!/usr/bin/env python3
"""
md_to_workbook.py — Reusable Markdown → Excel converter for estimation workbooks.

Project-agnostic: reads a Markdown file structured per
[workbook contract](../../orbit-prepare-workbook/references/contract.md) §5 and produces a styled .xlsx
per §4 + §4.10. No project-specific content baked into the script.

CLI:
    python scripts/md_to_workbook.py \
      --input  output/estimation_workbook.md \
      --output output/estimation_workbook.xlsx \
      [--config scripts/workbook_config.yaml] \
      [--strict]

Module API:
    from scripts.md_to_workbook import convert
    convert(input_path, output_path, config_path=None, strict=False)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from markdown_it import MarkdownIt
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet


# ---------------------------------------------------------------------------
# Exit codes (per command contract §6.6)
# ---------------------------------------------------------------------------
EXIT_OK = 0
EXIT_PARSE_ERROR = 2
EXIT_SCHEMA_MISMATCH = 3
EXIT_FORMULA_ERROR = 4
EXIT_IO_ERROR = 5


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------
@dataclass
class MdTable:
    """Represents a single parsed Markdown table."""
    header: list[str]
    rows: list[list[str]]
    table_name: str | None = None  # backticked tbl_* name, if found in nearest H3


@dataclass
class MdSection:
    """One H2 section, optionally containing H3 sub-sections each with one table."""
    heading: str  # full H2 text, e.g. "Sheet 7 — Estimate Sizing"
    tables: list[MdTable] = field(default_factory=list)


def _strip_inline_md(text: str) -> str:
    """Strip simple inline markdown decorations from cell text.

    Skips italic stripping inside backticked code/formula cells so that
    Excel formulas like `=F3*G3` keep their multiplication operator.
    """
    text = text.strip()
    # Preserve formula text verbatim
    if text.startswith("`") and text.endswith("`"):
        inner = text.strip("`")
        if inner.startswith("="):
            return text  # leave formula backticks intact for downstream coerce
        return inner
    # Remove **bold** markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    # Italic *xxx* — only strip when content is short and contains no whitespace
    # AND no math/formula characters, to avoid eating Excel * operators.
    def _maybe_italic(m: re.Match) -> str:
        inner = m.group(1)
        if any(ch in inner for ch in "()=+/<>"):
            return m.group(0)
        return inner
    text = re.sub(r"(?<!\*)\*([^*\s][^*]*?[^*\s]|\S)\*(?!\*)", _maybe_italic, text)
    return text


def _split_md_table_row(line: str) -> list[str]:
    """Split a Markdown table row into cells, handling escaped pipes."""
    # Replace escaped pipes with placeholder, split, then restore.
    placeholder = ""
    safe = line.replace("\\|", placeholder)
    parts = [p.strip() for p in safe.split("|")]
    # Drop leading/trailing empties from outer pipes.
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.replace(placeholder, "|") for p in parts]


def _is_separator_row(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-+:?", c.strip()) for c in cells if c.strip() != "")


def parse_markdown(md_path: Path) -> list[MdSection]:
    """Parse the Markdown file into ordered H2 sections containing tables.

    The walker is lightweight and tolerant:
      - H2 ("## ...") starts a new section
      - H3 ("### ...") captures the next table; the backticked `tbl_*` name in the
        H3 line is recorded as the table name
      - Tables under an H2 (no preceding H3) inherit no explicit table name
    """
    if not md_path.is_file():
        raise FileNotFoundError(f"Markdown input not found: {md_path}")

    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    sections: list[MdSection] = []
    current_section: MdSection | None = None
    pending_table_name: str | None = None

    i = 0
    in_code_fence = False
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Skip fenced code blocks entirely.
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            i += 1
            continue
        if in_code_fence:
            i += 1
            continue

        # H2: new section
        if stripped.startswith("## ") and not stripped.startswith("### "):
            current_section = MdSection(heading=stripped[3:].strip())
            sections.append(current_section)
            pending_table_name = None
            i += 1
            continue

        # H3: capture pending table name (look for backticked tbl_*)
        if stripped.startswith("### "):
            heading_text = stripped[4:].strip()
            m = re.search(r"`(tbl_[A-Za-z0-9_]+)`", heading_text)
            pending_table_name = m.group(1) if m else None
            i += 1
            continue

        # Markdown table detection: line containing pipes, next line is separator
        if "|" in stripped and i + 1 < len(lines):
            sep_cells = _split_md_table_row(lines[i + 1].strip())
            if _is_separator_row(sep_cells):
                header = [_strip_inline_md(c) for c in _split_md_table_row(stripped)]
                rows: list[list[str]] = []
                j = i + 2
                while j < len(lines):
                    nxt = lines[j].rstrip()
                    if not nxt.strip() or "|" not in nxt:
                        break
                    row_cells = [_strip_inline_md(c) for c in _split_md_table_row(nxt.strip())]
                    # Pad/truncate to header length
                    if len(row_cells) < len(header):
                        row_cells += [""] * (len(header) - len(row_cells))
                    elif len(row_cells) > len(header):
                        row_cells = row_cells[: len(header)]
                    rows.append(row_cells)
                    j += 1
                table = MdTable(header=header, rows=rows, table_name=pending_table_name)
                if current_section is not None:
                    current_section.tables.append(table)
                pending_table_name = None
                i = j
                continue

        i += 1

    return sections


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
def load_config(config_path: Path | None) -> dict[str, Any]:
    if config_path is None:
        return {}
    if not config_path.is_file():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _defaults(cfg: dict[str, Any]) -> dict[str, Any]:
    return cfg.get("defaults", {}) or {}


# ---------------------------------------------------------------------------
# Cell value classification
# ---------------------------------------------------------------------------
_NUMBER_RE = re.compile(r"^-?\d{1,3}(,\d{3})*(\.\d+)?$|^-?\d+(\.\d+)?$")
_PERCENT_RE = re.compile(r"^-?\d+(\.\d+)?\s*%$")


def _is_formula(text: str) -> bool:
    s = text.strip()
    return s.startswith("`=") and s.endswith("`")


def _strip_formula(text: str) -> str:
    return text.strip().strip("`")


def _coerce_value(text: str, header: str, integer_headers: list[str]) -> Any:
    """Convert a cell string into a Python value (str, int, float, or formula)."""
    s = text.strip()
    if s == "" or s == "-" or s.lower() in {"n/a", "na"}:
        return s
    # Escaped leading '=' for literal text starting with '='
    if s.startswith("'="):
        return s[1:]
    if _is_formula(s):
        return _strip_formula(s)
    # Percent literal "12.5%"
    if _PERCENT_RE.fullmatch(s):
        try:
            return float(s.rstrip("%").strip()) / 100.0
        except ValueError:
            return s
    # Plain number (strip thousand separators)
    if _NUMBER_RE.fullmatch(s):
        try:
            v = float(s.replace(",", ""))
            if header in integer_headers or v.is_integer() and header in integer_headers:
                return int(v)
            return v
        except ValueError:
            return s
    return s


def _number_format_for(header: str, defaults: dict[str, Any]) -> str | None:
    nf_map: dict[str, str] = defaults.get("number_format", {}) or {}
    integer_headers: list[str] = defaults.get("integer_headers", []) or []
    if header in integer_headers:
        return "0"
    # First-match-wins on keyword
    for kw, fmt in nf_map.items():
        if kw and kw in header:
            return fmt
    return None


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
THIN = Side(style="thin", color="BFBFBF")
THICK_BOTTOM = Side(style="medium", color="1F4E78")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_TOP_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_RIGHT_MIDDLE = Alignment(horizontal="right", vertical="center", wrap_text=False)
ALIGN_CENTER_MIDDLE = Alignment(horizontal="center", vertical="center", wrap_text=False)


# ---------------------------------------------------------------------------
# Column width recipes (R2) — header pattern → width in characters
# ---------------------------------------------------------------------------
_WEEK_COL_RE = re.compile(r"^W\d+$", re.IGNORECASE)
_SPRINT_COL_RE = re.compile(r"^S\d+$", re.IGNORECASE)


def _column_width_for_header(header: str) -> int:
    """Return Excel column width (in characters) based on header pattern.

    Recipes follow the R2 spec — case-insensitive substring matching. Default
    fallback is 12. Bullet columns are handled separately (cap at 50).
    """
    h = (header or "").strip()
    if not h:
        return 12
    lower = h.lower()

    # Exact short single-letter / sequence headers
    if h in ("#", "Seq", "No") or lower in {"#", "seq", "no"}:
        return 4
    # Week columns: W1, W2, ... — short
    if _WEEK_COL_RE.fullmatch(h) or _SPRINT_COL_RE.fullmatch(h):
        return 4

    # Exact one-char short codes
    if h in ("P", "I"):
        return 10

    # Specific IDs (exact-name matches first, then contains 'ID')
    id_exact = {
        "Feature ID", "Subfeature ID", "BI ID", "SCR ID", "API ID",
        "INT ID", "ND ID", "Risk ID", "Scenario ID", "Scope ID",
    }
    if h in id_exact or "id" in lower.split() or lower.endswith(" id") or lower.startswith("id ") or " id" in (" " + lower + " "):
        # broad ID match by token
        if " id" in (" " + lower):
            return 12
    if "id" == lower or lower.endswith("id") and len(h) <= 18:
        return 12

    # Module exact
    if h == "Module" or lower == "module":
        return 16

    # Feature / Feature Name exact
    if h in ("Feature", "Feature Name") or lower in {"feature", "feature name"}:
        return 24

    # Long-text columns
    long_text_keys = (
        "subfeature name", "statement", "description",
        "stakeholder detail", "user story",
    )
    if any(k in lower for k in long_text_keys):
        return 40

    # Wider bullet/notes columns
    wide_text_keys = (
        "implementation notes", "notes", "interface count", "mitigation",
        "wbs mapping note", "external cause",
    )
    if any(k in lower for k in wide_text_keys):
        return 50

    # Role MD columns (exact short codes) — first to avoid grabbing 'PM' from 'Impact'
    role_md = {
        "UX/UI", "BA", "SA", "FE", "BE", "QA", "DevOps", "Change", "PM", "Total",
    }
    if h in role_md:
        return 6

    # Short status / classification headers
    short_class_keys = (
        "sg", "priority", "cx", "type", "status", "owner", "method",
        "reuse", "severity", "band",
    )
    if any(lower == k or lower.startswith(k + " ") or lower.endswith(" " + k) for k in short_class_keys):
        return 10
    if lower in short_class_keys:
        return 10

    # Check column
    if "check" in lower:
        return 8

    # Coverage / percent / probability
    pct_keys = ("coverage ratio", "percent of adjusted md", "prob %")
    if any(k in lower for k in pct_keys) or lower.endswith("%") or " %" in lower:
        return 8

    # Generic numeric headers — MD / FTE / Score (when not role-exact)
    numeric_keys = ("md", "fte", "score", "sprint-fte", "fte-weeks")
    if any(k == lower or k in lower.split() for k in numeric_keys):
        return 8
    if any(k in lower for k in ("md", "fte", "score")):
        # broader numeric heuristic
        return 8

    # Refs / source / cross-refs
    ref_keys = (
        "refs", "related refs", "source", "source ref",
        "int ref", "wbs ref", "bi ref", "fn ref", "scr ref",
        "api ref", "scope ref",
    )
    if any(k in lower for k in ref_keys):
        return 18

    # Contains 'ID' anywhere (catch-all)
    if "id" in lower and len(h) <= 24:
        return 12

    return 12


def _cell_alignment(header: str, value: Any, *, col_idx: int) -> Alignment:
    """Pick the right Alignment object based on header pattern and value (R3).

    - Header containing 'Check'/'Status'/'Result'/'Band' → center + middle
    - col_idx == 1 (the leading '#'/'Seq' column) → center + middle
    - ID columns → center + middle
    - Numeric headers (MD/FTE/%/Score/Sprint-FTE/FTE-Weeks/integer) → right + middle
    - Default text → left + top + wrap=True
    """
    h = (header or "").strip()
    lower = h.lower()

    # First column (#/Seq/No) → center + middle
    if col_idx == 1 or h in ("#", "Seq", "No"):
        return ALIGN_CENTER_MIDDLE

    # Status-style columns
    status_words = ("check", "status", "result", "band")
    if any(w in lower for w in status_words):
        return ALIGN_CENTER_MIDDLE

    # ID columns — by exact ID names or 'id' token
    id_exact = {
        "Feature ID", "Subfeature ID", "BI ID", "SCR ID", "API ID",
        "INT ID", "ND ID", "Risk ID", "Scenario ID", "Scope ID",
    }
    if h in id_exact or lower.endswith(" id") or lower == "id":
        return ALIGN_CENTER_MIDDLE

    # Numeric headers
    numeric_keys = (
        "md", "fte", "score", "sprint-fte", "fte-weeks",
        "coverage ratio", "percent", "prob %", "%",
    )
    if any(k in lower for k in numeric_keys):
        return ALIGN_RIGHT_MIDDLE

    # Week / sprint columns are numeric
    if _WEEK_COL_RE.fullmatch(h) or _SPRINT_COL_RE.fullmatch(h):
        return ALIGN_RIGHT_MIDDLE

    # Numeric python values → right + middle
    if isinstance(value, (int, float)):
        return ALIGN_RIGHT_MIDDLE

    return ALIGN_TOP_WRAP


def _is_bullet_header(header: str, defaults: dict[str, Any]) -> bool:
    keywords = defaults.get("bullet_header_keywords", []) or []
    return any(k in header for k in keywords)


def _is_status_header(header: str, defaults: dict[str, Any]) -> bool:
    keywords = defaults.get("status_header_keywords", []) or []
    return any(k in header for k in keywords)


def _is_numeric_header(header: str, defaults: dict[str, Any]) -> bool:
    nf = _number_format_for(header, defaults)
    return nf is not None


def _normalize_bullets(text: str) -> str:
    """Convert <br> / <br/> and literal `\\n` to real newlines so wrap_text
    renders bullet lists. Markdown table cells cannot embed real newlines, so
    upstream generators use either `<br>` HTML breaks or a literal two-char
    backslash-n token. Both are normalized to actual line feeds here."""
    if not isinstance(text, str):
        return text
    s = re.sub(r"<\s*br\s*/?\s*>", "\n", text, flags=re.IGNORECASE)
    # Convert literal two-char sequence "\\n" (backslash + n) to a real newline.
    s = s.replace("\\n", "\n")
    return s


def _apply_table_styling(
    ws: Worksheet,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    header: list[str],
    defaults: dict[str, Any],
    *,
    is_sub_table: bool,
) -> None:
    """Apply header fill, banding, conditional formatting, and column-level formats."""
    header_fill_hex = (
        defaults.get("sub_header_fill", "2E75B6")
        if is_sub_table
        else defaults.get("header_fill", "1F4E78")
    )
    header_font_color = (
        defaults.get("sub_header_font_color", "FFFFFF")
        if is_sub_table
        else defaults.get("header_font_color", "FFFFFF")
    )
    # alt_fill removed — user directive: all-white cells with black borders, no row banding
    pass_fill = defaults.get("pass_fill", "C6EFCE")
    pass_font = defaults.get("pass_font", "006100")
    warning_fill = defaults.get("warning_fill", "FFEB9C")
    warning_font = defaults.get("warning_font", "9C5700")
    fail_fill = defaults.get("fail_fill", "FFC7CE")
    fail_font = defaults.get("fail_font", "9C0006")

    header_pf = PatternFill("solid", fgColor=header_fill_hex)
    header_font = Font(name="Calibri", size=11, bold=True, color=header_font_color)
    body_font = Font(name="Calibri", size=10)

    # All-white-with-black-borders style (replaces alternating row banding).
    # Use thin black borders on every cell side so the table reads as a static grid.
    THIN_BLACK = Side(style="thin", color="000000")
    CELL_BORDER = Border(left=THIN_BLACK, right=THIN_BLACK, top=THIN_BLACK, bottom=THIN_BLACK)

    # Header row — center + middle, bold, white on #1F4E78 (R3) + black border on all sides
    for c in range(start_col, end_col + 1):
        cell = ws.cell(row=start_row, column=c)
        cell.fill = header_pf
        cell.font = header_font
        cell.alignment = ALIGN_CENTER_MIDDLE
        cell.border = CELL_BORDER
    # R1: header row height 18pt (was 26pt)
    ws.row_dimensions[start_row].height = 18

    # Data rows
    # R2: header-pattern-based widths replace auto-fit logic.
    # Bullet columns still cap at 50 (was 60).
    bullet_cap = 50

    for col_offset, hdr in enumerate(header):
        col_idx = start_col + col_offset
        col_letter = get_column_letter(col_idx)
        is_bullet = _is_bullet_header(hdr, defaults)
        is_status = _is_status_header(hdr, defaults)
        nf = _number_format_for(hdr, defaults)

        # Per-column data formatting — all-white cells with black borders (no banding)
        for r in range(start_row + 1, end_row + 1):
            cell = ws.cell(row=r, column=col_idx)
            cell.font = body_font
            cell.alignment = _cell_alignment(hdr, cell.value, col_idx=col_idx)
            if nf:
                cell.number_format = nf
            cell.border = CELL_BORDER

        # R2: width recipe per header pattern; bullet columns cap at 50.
        # On multi-table sheets (e.g. Sheet 7 Estimate Sizing), later tables
        # share column letters with earlier tables — use max-wins so a wider
        # earlier column (e.g. 'Subfeature Name' = 40) isn't shrunk by a later
        # role-MD header (e.g. 'BA' = 6).
        recipe_w = _column_width_for_header(hdr)
        if is_bullet:
            target_w = min(bullet_cap, max(recipe_w, 30))
        else:
            target_w = recipe_w
        # openpyxl's default ColumnDimension.width is 13.0 even when unset, so
        # a direct max-wins check against `.width` would never shrink from the
        # default. Track explicitly-set columns on the worksheet so multi-table
        # sheets (where later headers share column letters) only grow widths.
        col_dim = ws.column_dimensions[col_letter]
        seen = getattr(ws, "_width_set_cols", None)
        if seen is None:
            seen = set()
            ws._width_set_cols = seen  # type: ignore[attr-defined]
        if col_letter not in seen:
            col_dim.width = target_w
            seen.add(col_letter)
        elif target_w > (col_dim.width or 0):
            col_dim.width = target_w

        # Conditional formatting for status columns
        if is_status and end_row >= start_row + 1:
            data_range = f"{col_letter}{start_row + 1}:{col_letter}{end_row}"
            try:
                ws.conditional_formatting.add(
                    data_range,
                    CellIsRule(
                        operator="equal",
                        formula=['"Pass"'],
                        fill=PatternFill("solid", fgColor=pass_fill),
                        font=Font(color=pass_font, bold=True),
                    ),
                )
                ws.conditional_formatting.add(
                    data_range,
                    CellIsRule(
                        operator="equal",
                        formula=['"Warning"'],
                        fill=PatternFill("solid", fgColor=warning_fill),
                        font=Font(color=warning_font, bold=True),
                    ),
                )
                ws.conditional_formatting.add(
                    data_range,
                    CellIsRule(
                        operator="equal",
                        formula=['"Fail"'],
                        fill=PatternFill("solid", fgColor=fail_fill),
                        font=Font(color=fail_font, bold=True),
                    ),
                )
                ws.conditional_formatting.add(
                    data_range,
                    CellIsRule(
                        operator="equal",
                        formula=['"Overdue"'],
                        fill=PatternFill("solid", fgColor=fail_fill),
                        font=Font(color=fail_font, bold=True),
                    ),
                )
            except Exception:
                # Conditional-format range collision — skip silently
                pass


def _maybe_bold_high_impact(
    ws: Worksheet,
    start_row: int,
    end_row: int,
    header: list[str],
    defaults: dict[str, Any],
) -> None:
    """Bold + border-top rows whose 'Field' column matches high-impact names."""
    high_impact = set(defaults.get("high_impact_field_names", []) or [])
    if not high_impact or "Field" not in header:
        return
    field_idx = header.index("Field")
    for r in range(start_row + 1, end_row + 1):
        v = ws.cell(row=r, column=field_idx + 1).value
        if isinstance(v, str) and v.strip() in high_impact:
            for c in range(1, len(header) + 1):
                cell = ws.cell(row=r, column=c)
                cell.font = Font(name="Calibri", size=11, bold=True)
                cell.border = Border(top=THIN)


def _set_tab_color(ws: Worksheet, sheet_name: str, defaults: dict[str, Any]) -> None:
    tab_colors: dict[str, str] = defaults.get("tab_colors", {}) or {}
    for kw, color in tab_colors.items():
        if kw and kw in sheet_name:
            ws.sheet_properties.tabColor = color
            return


def _safe_sheet_name(name: str) -> str:
    cleaned = re.sub(r'[\\/*?:\[\]]', "-", name)
    return cleaned[:31] if len(cleaned) > 31 else cleaned


def _short_sheet_name(heading: str, cfg_sheets: list[dict[str, Any]]) -> str:
    for entry in cfg_sheets:
        h = entry.get("heading", "")
        if h and h in heading:
            return entry.get("short_name", heading)
    # Fallback: take text after em-dash if present.
    if " — " in heading:
        return heading.split(" — ", 1)[1].strip()
    return heading


def _table_name_from_config(
    section_heading: str,
    table_index: int,
    cfg_sheets: list[dict[str, Any]],
) -> str | None:
    for entry in cfg_sheets:
        h = entry.get("heading", "")
        if h and h in section_heading:
            tables = entry.get("tables", []) or []
            if 0 <= table_index < len(tables):
                return tables[table_index].get("name")
    return None


# ---------------------------------------------------------------------------
# Sheet 8 §4.8 — sprint-based timeline helpers (resource matrix + task Gantt)
# ---------------------------------------------------------------------------

# Phase band metadata: ordered ranges of week header tokens (W1..W48) →
# (band label shown in merged header, fill color). Project-agnostic in code
# even though the labels and ranges are Step 05 conventions.
#
# Weekly mapping (per the Step 05 §4 `Phase Band` row):
#   W1-W2  Foundation        (light navy)
#   W3-W7  BUILD-MP1         (light blue)
#   W8-W12 BUILD-MP2         (light blue)
#   W13-W17 BUILD-MP3        (light blue)
#   W18-W22 BUILD-MP4        (light blue)
#   W23    QA P1             (light grey)
#   W24    Go-Live P1        (orange)
#   W25-W30 BUILD-MP5        (medium blue)
#   W31-W38 BUILD-MP6        (medium blue)
#   W39-W42 BUILD-MP7        (medium blue)
#   W43-W45 QA P2            (light grey)
#   W46    Go-Live P2        (orange)
#   W47-W48 Hypercare        (light green)
_PHASE_BAND_RANGES: tuple[tuple[str, range, str], ...] = (
    ("Foundation", range(1, 3), "D9E1F2"),
    ("BUILD-MP1", range(3, 8), "BDD7EE"),
    ("BUILD-MP2", range(8, 13), "BDD7EE"),
    ("BUILD-MP3", range(13, 18), "BDD7EE"),
    ("BUILD-MP4", range(18, 23), "BDD7EE"),
    ("QA P1", range(23, 24), "E7E6E6"),
    ("Go-Live P1", range(24, 25), "F4B084"),
    ("BUILD-MP5", range(25, 31), "9DC3E6"),
    ("BUILD-MP6", range(31, 39), "9DC3E6"),
    ("BUILD-MP7", range(39, 43), "9DC3E6"),
    ("QA P2", range(43, 46), "E7E6E6"),
    ("Go-Live P2", range(46, 47), "F4B084"),
    ("Hypercare", range(47, 49), "C6E0B4"),
)

# Derive _PHASE_BANDS as ((tokens, label, fill), ...) using "W<n>" tokens so
# legacy lookup code keeps working.
_PHASE_BANDS: tuple[tuple[tuple[str, ...], str, str], ...] = tuple(
    (tuple(f"W{n}" for n in rng), label, fill_hex)
    for label, rng, fill_hex in _PHASE_BAND_RANGES
)

# Task-class fill lookup: keyword (lowercase) → hex fill. First-match wins.
_TASK_CLASS_COLORS: tuple[tuple[str, str], ...] = (
    ("requirement", "DDEBF7"),
    ("foundation", "9DC3E6"),
    ("build-mp", "BDD7EE"),
    ("develop", "BDD7EE"),
    ("build", "BDD7EE"),
    ("setup", "FFF2CC"),
    ("infrastructure", "FFE699"),
    ("hypercare", "C6E0B4"),
    ("sit", "C6E0B4"),
    ("uat", "C6E0B4"),
    ("nft", "808080"),
    ("regression", "FCE4D6"),
    ("cab", "D9D9D9"),
    ("cut", "F4B084"),
)


def _phase_bands_from_defaults(defaults: dict[str, Any] | None):
    """Return phase bands from config `defaults.phase_bands` (list of
    {label, weeks: "W1-W4" | "W38", fill}) or the built-in default tuple.
    Keeps the converter project-agnostic: projects override bands via YAML."""
    pb = (defaults or {}).get("phase_bands")
    if not pb:
        return _PHASE_BANDS
    out = []
    for e in pb:
        rng = str(e.get("weeks", "")).strip()
        m = re.fullmatch(r"([WwSs])(\d+)(?:\s*-\s*[WwSs]?(\d+))?", rng)
        if not m:
            continue
        prefix = m.group(1).upper(); a = int(m.group(2)); b = int(m.group(3) or a)
        out.append((tuple(f"{prefix}{n}" for n in range(a, b + 1)), str(e.get("label", "")), str(e.get("fill", "BDD7EE"))))
    return tuple(out) if out else _PHASE_BANDS


def _task_class_colors_from_defaults(defaults: dict[str, Any] | None):
    """Merge config `defaults.task_class_colors` (list of [keyword, hex]) in front
    of the built-in keyword→color table (config wins on first match)."""
    extra = (defaults or {}).get("task_class_colors") or []
    merged: list[tuple[str, str]] = []
    for item in extra:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            merged.append((str(item[0]).lower(), str(item[1])))
        elif isinstance(item, dict):
            merged.append((str(item.get("keyword", "")).lower(), str(item.get("fill", ""))))
    return tuple(merged) + _TASK_CLASS_COLORS


def _write_phase_band_header(ws: Worksheet, header: list[str], row: int, bands=None) -> None:
    """Emit a merged Phase Band header row above the sprint column headers.

    Walks the table header looking for sprint tokens (S0..Sn) and merges each
    contiguous band per `_PHASE_BANDS`. Non-sprint columns receive no band cell.
    """
    # Map week/sprint token → column index (1-based) for fast lookup.
    period_cols: dict[str, int] = {}
    for c_idx, hdr in enumerate(header, start=1):
        token = hdr.strip()
        if re.fullmatch(r"[WS]\d+", token, flags=re.IGNORECASE):
            period_cols[token.upper()] = c_idx

    for tokens, label, fill_hex in (bands or _PHASE_BANDS):
        cols = [period_cols[t] for t in tokens if t in period_cols]
        if not cols:
            continue
        start_c, end_c = min(cols), max(cols)
        cell = ws.cell(row=row, column=start_c, value=label)
        cell.font = Font(name="Calibri", size=10, bold=True, color="1F4E78")
        cell.fill = PatternFill("solid", fgColor=fill_hex)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if end_c > start_c:
            ws.merge_cells(start_row=row, start_column=start_c, end_row=row, end_column=end_c)
            # Ensure merged tail cells inherit fill (openpyxl quirk)
            for c in range(start_c + 1, end_c + 1):
                ws.cell(row=row, column=c).fill = PatternFill("solid", fgColor=fill_hex)
    ws.row_dimensions[row].height = 18


def _apply_resource_heatmap(
    ws: Worksheet,
    *,
    header: list[str],
    data_start_row: int,
    data_end_row: int,
    start_col: int,
    end_col: int,
) -> None:
    """3-color heatmap on the weekly FTE cells of tbl_resource_matrix.

    Range = role rows (excluding Total) × week columns (W1..Wn, excluding the
    trailing FTE-Weeks and MD summary columns). Uses ColorScaleRule (white →
    yellow → red) so light load reads cool, heavy load reads hot.
    """
    if data_end_row < data_start_row:
        return
    # Identify week-column indexes (header matches Wxx pattern, 1-based col).
    week_col_re = re.compile(r"^[Ww]\d+$")
    week_cols = [c + start_col for c, h in enumerate(header) if week_col_re.match(h.strip())]
    if not week_cols:
        return
    first_week_col = min(week_cols)
    last_week_col = max(week_cols)
    first_letter = get_column_letter(first_week_col)
    last_letter = get_column_letter(last_week_col)
    rng = f"{first_letter}{data_start_row}:{last_letter}{data_end_row}"
    try:
        from openpyxl.formatting.rule import ColorScaleRule
        rule = ColorScaleRule(
            start_type="num", start_value=0, start_color="FFFFFFFF",
            mid_type="num", mid_value=2.0, mid_color="FFFFEB9C",
            end_type="num", end_value=4.0, end_color="FFF8696B",
        )
        ws.conditional_formatting.add(rng, rule)
    except Exception:
        # Skip silently if openpyxl rejects the rule (older versions, etc.).
        pass


def _row_task_label(row: list[str], header: list[str]) -> str:
    """Find the Task / Phase column value in a row (case-insensitive substring)."""
    for c_idx, hdr in enumerate(header):
        h = hdr.strip().lower()
        if "task" in h or "phase" in h:
            if c_idx < len(row):
                return row[c_idx]
    # Fallback: 2nd column (since 1st is "#")
    return row[1] if len(row) > 1 else ""


def _task_class_color(label: str, colors=None) -> str | None:
    """Resolve a task-class fill color from a task label using keyword match."""
    s = (label or "").lower()
    for kw, color in (colors or _TASK_CLASS_COLORS):
        if kw in s:
            return color
    return None


# ---------------------------------------------------------------------------
# Worksheet writing
# ---------------------------------------------------------------------------
def _write_table(
    ws: Worksheet,
    table: MdTable,
    table_name: str,
    start_row: int,
    defaults: dict[str, Any],
    *,
    is_sub_table: bool,
    title: str | None = None,
) -> int:
    """Write one MdTable to ws starting at start_row; return next free row.

    Special handling per command §4.8 (Sheet 8):
    - `tbl_resource_matrix`: insert a merged "Phase Band" row above the column
      headers; spans + band fill colors are derived from the sprint header text
      (S0..S10). The row pushes the rest of the table down by 1.
    - `tbl_task_timeline`: rendered as a Gantt — body cells whose text is the
      literal token "active" (case-insensitive) are cleared and filled with the
      row's task-class color based on a keyword lookup against the Task / Phase
      column. Empty cells stay blank.
    Both behaviors are gated strictly on table_name so the converter remains
    project-agnostic for other sheets/tables.
    """
    integer_headers = defaults.get("integer_headers", []) or []

    # R1: drop the per-table title block (saves vertical space). Keep the
    # parameter for API compatibility but ignore the value.
    _ = title

    # Sheet 8 §4.8.1 — Phase Band merged header row above sprint columns
    if table_name == "tbl_resource_matrix":
        _write_phase_band_header(ws, header=table.header, row=start_row, bands=_phase_bands_from_defaults(defaults))
        start_row += 1
    task_colors = _task_class_colors_from_defaults(defaults)

    # Header
    for c, hdr in enumerate(table.header, start=1):
        ws.cell(row=start_row, column=c, value=hdr)

    # Body
    # R1: keep default Excel row height (~15pt) — do not auto-expand even for
    # bullet rows; rely on wrap_text + column widths instead.
    row_height_bullet = None
    # Sheet 8 §4.8.2 — collect active-cell fills for the task timeline Gantt.
    # We defer applying fills until AFTER _apply_table_styling (which sets
    # banding/alt_fill) so the task-class color wins.
    is_task_timeline = table_name == "tbl_task_timeline"
    task_fill_jobs: list[tuple[int, int, str]] = []
    for r_offset, row in enumerate(table.rows, start=1):
        excel_row = start_row + r_offset
        has_bullets = False
        # Resolve task-class color for this row (lookup against task / phase column)
        row_fill_hex = (
            _task_class_color(_row_task_label(row, table.header), task_colors) if is_task_timeline else None
        )
        for c, val in enumerate(row, start=1):
            hdr = table.header[c - 1] if c - 1 < len(table.header) else ""
            normalized = _normalize_bullets(val) if isinstance(val, str) else val
            if isinstance(normalized, str) and "\n" in normalized:
                has_bullets = True
            cell_value = _coerce_value(normalized, hdr, integer_headers) if isinstance(normalized, str) else normalized
            # Sheet 8 §4.8.2: literal "active" → fill-only Gantt cell
            if (
                is_task_timeline
                and isinstance(cell_value, str)
                and cell_value.strip().lower() == "active"
            ):
                ws.cell(row=excel_row, column=c, value=None)
                if row_fill_hex:
                    task_fill_jobs.append((excel_row, c, row_fill_hex))
            else:
                ws.cell(row=excel_row, column=c, value=cell_value)
        if has_bullets and row_height_bullet is not None:
            ws.row_dimensions[excel_row].height = row_height_bullet

    end_row = start_row + len(table.rows)
    end_col = len(table.header)

    # Style
    _apply_table_styling(
        ws,
        start_row=start_row,
        end_row=end_row,
        start_col=1,
        end_col=end_col,
        header=table.header,
        defaults=defaults,
        is_sub_table=is_sub_table,
    )

    # NOTE: Excel Table objects intentionally omitted.
    #
    # OOXML Excel Tables (ListObjects) always carry an <autoFilter> element.
    # Earlier attempts to suppress filter dropdowns by setting tbl.autoFilter=None
    # after _initialise_columns() produced invalid table XML, which Excel detected
    # and "repaired" on open — wiping all 18 tables.
    #
    # The visual styling (header fill, black borders, conditional formatting,
    # heatmap, task-timeline color cells) is applied at the cell level above and
    # does NOT depend on the Table object. The named "tbl_*" identity is kept only
    # in markdown for the contract; the workbook reads as styled ranges.
    table_name = re.sub(r"\W", "_", table_name)
    _ = ref = f"A{start_row}:{get_column_letter(end_col)}{end_row}"  # noqa: F841
    # Ensure no sheet-level auto_filter is left over.
    ws.auto_filter.ref = None

    _maybe_bold_high_impact(ws, start_row, end_row, table.header, defaults)

    # Apply task-class fills last so they override banding/alt_fill (§4.8.2).
    for row_i, col_i, fill_hex in task_fill_jobs:
        ws.cell(row=row_i, column=col_i).fill = PatternFill("solid", fgColor=fill_hex)

    # Heatmap on resource matrix — FTE intensity per role × week.
    # Skip header rows + Total FTE row + FTE-Weeks/MD trailing columns.
    if table_name == "tbl_resource_matrix":
        _apply_resource_heatmap(
            ws,
            header=table.header,
            data_start_row=start_row + 1,  # first role row (after column header)
            data_end_row=end_row - 1,      # exclude Total FTE/week row
            start_col=1,                   # tables start at col A in _write_table
            end_col=end_col,
        )

    return end_row + 2  # leave a one-row spacer


def write_workbook(
    sections: list[MdSection],
    output_path: Path,
    cfg: dict[str, Any],
    *,
    strict: bool = False,
) -> None:
    defaults = _defaults(cfg)
    cfg_sheets: list[dict[str, Any]] = cfg.get("sheets", []) or []

    wb = Workbook()
    # Remove default empty sheet — we'll add explicitly.
    default_sheet = wb.active
    wb.remove(default_sheet)

    for section in sections:
        sheet_name = _safe_sheet_name(_short_sheet_name(section.heading, cfg_sheets))
        if not section.tables:
            if strict:
                raise ValueError(f"Section '{section.heading}' has no tables")
            continue
        ws = wb.create_sheet(title=sheet_name)
        ws.sheet_view.showGridLines = False
        _set_tab_color(ws, section.heading, defaults)

        # R1: drop per-table title block. All tables (first + sub) start with
        # column header on their own row. Row numbers for the first table still
        # match markdown-time references (header=row 1, first data=row 2),
        # except for tbl_resource_matrix which gets a phase-band row inserted.
        next_row = 1
        for idx, table in enumerate(section.tables):
            # Resolve table name: prefer explicit H3 backtick, fallback to config registry
            table_name = (
                table.table_name
                or _table_name_from_config(section.heading, idx, cfg_sheets)
                or f"tbl_{sheet_name.lower().replace(' ', '_')}_{idx + 1}"
            )
            is_sub = len(section.tables) > 1
            next_row = _write_table(
                ws,
                table,
                table_name=table_name,
                start_row=next_row,
                defaults=defaults,
                is_sub_table=is_sub,
                title=None,
            )

        # R1: do not freeze panes — leave ws.freeze_panes at its default (None).

        # Print setup polish
        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.print_options.horizontalCentered = True
        ws.print_title_rows = "1:2"

    # Atomic write
    tmp_dir = output_path.parent
    tmp_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".xlsx_tmp_", suffix=".xlsx", dir=str(tmp_dir))
    os.close(fd)
    try:
        wb.save(tmp_path)
        os.replace(tmp_path, output_path)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def convert(
    input_path: str | Path,
    output_path: str | Path,
    config_path: str | Path | None = None,
    strict: bool = False,
) -> None:
    """Convert a Markdown estimation workbook to an .xlsx file."""
    in_p = Path(input_path)
    out_p = Path(output_path)
    cfg_p = Path(config_path) if config_path else None

    sections = parse_markdown(in_p)
    cfg = load_config(cfg_p) if cfg_p else {}
    write_workbook(sections, out_p, cfg, strict=strict)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="md_to_workbook",
        description="Convert estimation Markdown summary to styled Excel workbook.",
    )
    p.add_argument("--input", required=True, help="Markdown input path")
    p.add_argument("--output", required=True, help="Excel (.xlsx) output path")
    p.add_argument(
        "--config",
        default="scripts/workbook_config.yaml",
        help="YAML config path (default: scripts/workbook_config.yaml)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail on unknown headers or missing required tables.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    # Ensure markdown-it-py available; not used yet for parsing (custom walker)
    # but reserved per command contract §6.4 step 1.
    _ = MarkdownIt
    args = _build_arg_parser().parse_args(argv)
    in_p = Path(args.input)
    out_p = Path(args.output)
    cfg_p = Path(args.config) if args.config else None

    try:
        sections = parse_markdown(in_p)
    except FileNotFoundError as exc:
        print(f"[md_to_workbook] {exc}", file=sys.stderr)
        return EXIT_PARSE_ERROR
    except Exception as exc:
        print(f"[md_to_workbook] Markdown parse error: {exc}", file=sys.stderr)
        return EXIT_PARSE_ERROR

    try:
        cfg = load_config(cfg_p) if cfg_p else {}
    except FileNotFoundError as exc:
        print(f"[md_to_workbook] {exc}", file=sys.stderr)
        return EXIT_SCHEMA_MISMATCH

    try:
        write_workbook(sections, out_p, cfg, strict=args.strict)
    except ValueError as exc:
        print(f"[md_to_workbook] Schema mismatch: {exc}", file=sys.stderr)
        return EXIT_SCHEMA_MISMATCH
    except OSError as exc:
        print(f"[md_to_workbook] I/O error: {exc}", file=sys.stderr)
        return EXIT_IO_ERROR
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"[md_to_workbook] Formula/write error: {exc}", file=sys.stderr)
        return EXIT_FORMULA_ERROR

    print(f"[md_to_workbook] Wrote {out_p} ({len(sections)} sheets)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
