# Export workbook contract

## Scope and prerequisites

This action converts the reviewed `output/estimation_workbook.md` to `output/estimation_workbook.xlsx`. It does not author a second planning baseline or replace Markdown preparation. Load the [canonical workbook contract](../../orbit-prepare-workbook/references/contract.md), especially §2 source approval, §3 sheet order, all §4 schemas, §5 Markdown syntax and safety, and §7 VAL-01 through VAL-14. Load the principles listed in [the action guide](../SKILL.md) even on direct invocation.

Require explicit `continue to xlsx`, `generate both`, or an equivalent export request for the identified Markdown revision. Preserve upstream approvals and any explicitly authorized draft watermark. A conversion request does not approve missing source artifacts or waive mandatory gates. If source values, table rows, or formulas need substantive revision, stop and return the finding for preparation and renewed review. Do not silently repair the baseline during export.

The converter only emits tables. Any Markdown prose that must appear in Excel, including warnings, source revisions, approval basis, no-pricing rules, Calculation Status, phase-band provenance and draft notices, must also be represented in the appropriate control or note cells before conversion. The `.xlsx` cannot introduce content absent from the Markdown.

## Bundled runtime and paths

- [md_to_workbook.py](../scripts/md_to_workbook.py) converts workbook Markdown to XLSX.
- [requirements.txt](../scripts/requirements.txt) requires `openpyxl>=3.1`, `pyyaml>=6.0`, and `markdown-it-py>=3.0` in the selected Python environment. Use Python 3.10 or newer.
- [workbook_config.yaml](../scripts/workbook_config.yaml) provides sheet mappings and formatting defaults. It is a template, not approved project phase-band evidence.

Resolve `EXPORT_SKILL` to the installed directory containing this action's `SKILL.md`. Run from the user's working project, not the installed skill directory. The following variables are runtime paths to resolve, not literal placeholders to leave in the command.

```bash
python3 -m pip install -r "$EXPORT_SKILL/scripts/requirements.txt"
python3 "$EXPORT_SKILL/scripts/md_to_workbook.py" \
  --input output/estimation_workbook.md \
  --output output/estimation_workbook.xlsx \
  --config output/workbook_config.yaml \
  --strict
```

Use an existing suitable environment or a project virtual environment. Do not mutate the shared installation or install globally without authorization.

## Project-specific configuration

Copy the bundled config to working-project `output/workbook_config.yaml`, preserving the sheet/table registry and format defaults. Derive `defaults.phase_bands` from the approved Step 05 phase-band row and the reviewed Markdown configuration metadata. Each band has `label`, `weeks` and `fill`; supported week syntax includes `W1-W4` and `W5`. Resolve actual labels, inclusive ranges and six-digit hex fills. Do not copy those illustrative weeks as project facts.

Validate that bands are nonempty, syntactically valid, non-overlapping and cover the intended weekly columns with the approved labels. An empty or wholly invalid `phase_bands` list silently falls back to the converter's fixed 48-week example bands. Never use that fallback for an unrelated project. If the source contains no usable band definition, stop for its approved treatment rather than inventing phases. Optional `defaults.task_class_colors` entries accept `[keyword, hex]` pairs or `{keyword, fill}` mappings and precede the built-in keyword colors. Record any project override in the Markdown.

Always pass `--config` explicitly. The public CLI retains the relative default `scripts/workbook_config.yaml`, resolved from the current working directory. It is not relative to the installed script. The module API `convert(input_path, output_path, config_path=None, strict=False)` has no automatic config default. Pass the project config explicitly to the API too. Do not rewrite shared script constants or shared configuration for a reporting task.

## CLI and conversion behavior

| Flag | Required | Default | Actual behavior |
| --- | --- | --- | --- |
| `--input` | Yes | None | Markdown input path. |
| `--output` | Yes | None | Target `.xlsx`; writes a temporary file in the target directory and replaces the destination only after successful save. |
| `--config` | No | `scripts/workbook_config.yaml` | YAML formatting defaults and sheet/table registry, relative to working directory. |
| `--strict` | No | Off | Rejects an H2 section with zero tables. It does not validate all required sheets, headers, formulas or semantic rules, despite broader CLI help wording. |

The custom line-walker reads H2 headings as sheets and H3 backticked `tbl_*` names as table identities. `markdown-it-py` is imported but not used for parsing. Fenced code is skipped. Header text drives formats. The parser pads short rows and truncates long rows, so independently check Markdown row widths before conversion. An H2 without tables is skipped without `--strict`.

Tables become styled cell ranges, not Excel Tables or named ranges. Multiple tables stack with one blank row between them. A resource matrix adds one phase-band row above its header. The task timeline does not add that row. Account for both cases in concrete A1 addresses. `active` cells in the task timeline become fill-only cells; the keyword color must resolve for the intended task. No filters or freeze panes are created. Long text wraps at fixed row heights and can be clipped. Print setup repeats rows `1:2`, which must be reviewed per sheet.

Number formats come from the config. Default header conventions are MD `0.0`, FTE `0.00`, percent or Ratio `0.0%`, Date `yyyy-mm-dd`, and configured Score/P/I/Start Week/End Week/Duration Weeks/Seq integer headers. All sheet schemas and remaining visual requirements stay in canonical §4; do not maintain a duplicate schema here.

## Formula safety and calculation status

Backtick-wrapped leading-`=` expressions become formula text. The converter neither calculates formulas nor supplies cached results. It does not validate dependency graphs, circular references, undefined names or semantic correctness. Use resolved A1 references with quoted sheet names. There are no defined `tbl_*` names or structured-reference tables. Do not emit unresolved symbols, schematic `...` formulas or self-including subtotal ranges.

The converter removes the apostrophe from literal `'=...`; openpyxl can then treat it as a formula. Do not rely on apostrophe escaping for untrusted text. Check source strings beginning with `=`, `+`, `-` or `@` separately from intentionally authored formulas and numeric inputs. Stop for safe literal handling, or use an explicit non-formula textual prefix in the reviewed Markdown. Do not execute untrusted source text as formulas.

When Excel or LibreOffice is available, recalculate the actual output and inspect cached values and formula errors. Independently reconcile source totals and all VAL-01 through VAL-14. When no calculation engine is available, put `Not recalculated` in both Markdown and the README control table, list independent numeric reconciliations and unresolved formula warnings, then convert that representation. File creation alone is not a formula-check pass. Metadata or status changes must remain synchronized with Markdown; rerun conversion when Markdown changes, and recalculate the delivered file again if claiming recalculated status.

## Verification before publication

1. Check approved source revisions and reviewed Markdown identity. Compare exact sheet count/order, H2/H3 names, headers, row widths, IDs, populated rows and any authorized additions against canonical §3-§5 before invoking the converter.
2. Review the explicit project config, source-derived phase bands, role coverage and address layout. Preserve scenario separation, QA test-case inputs, additional approved roles, PM derivation, warranty and reserve treatment.
3. Run conversion and retain the command, config path/revision, input revision, exit code and diagnostics as conversion provenance. Do not insert conversion success provenance before the attempt.
4. Open the resulting workbook. Inspect sheets, formulas, actual row coordinates, cell types, phase bands, timeline fills, status formatting, clipped text and meaningful print headers. A success log or a valid ZIP alone is not verification.
5. Recalculate when available, inspect formula errors and computed results, and evaluate every VAL check with source evidence. Preserve `Not recalculated` and warnings otherwise. Do not infer semantic atomicity or acceptance from populated cells.
6. Report the actual file path, source revision, calculation engine/status, verification performed and remaining warnings. Stop for review. Do not invoke another action.

## Errors and exit codes

| Exit | Actual meaning |
| --- | --- |
| `0` | Workbook saved. This does not mean source approval, schema completeness or formula correctness passed. |
| `2` | Missing Markdown or Markdown parse error. Argument parsing can also exit with `2`. |
| `3` | Missing config, or `ValueError` during writing, including empty H2 sections with `--strict`. |
| `4` | Other workbook-write exception, including formula/write errors. |
| `5` | `OSError` during workbook writing. |

Parse errors have generic diagnostics, not file+line localization. Write errors do not provide reliable sheet+cell localization. Missing Python dependencies can fail during import before these handlers run. Malformed or unreadable YAML and invalid config shapes can fail outside the documented handlers. Surface the real exit code and stderr; do not recategorize these as successful conversion.

On any failure, stop, report the error, preserve the reviewed Markdown and explain whether an existing `.xlsx` is stale. The atomic save prevents a half-written destination but does not prove that an older destination represents the current Markdown. Never claim an old workbook as the new result, silently substitute Markdown for Excel, or bypass a mandatory quality gate.
