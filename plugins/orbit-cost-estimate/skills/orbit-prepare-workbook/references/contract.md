# Generate Estimation Workbook

เอกสารนี้เป็น canonical schema ของ workbook ทั้ง Markdown และ Excel. [orbit-prepare-workbook](../SKILL.md) ทำเฉพาะ Step A แล้วหยุดที่ Markdown review gate. [orbit-export-workbook](../../orbit-export-workbook/SKILL.md) ทำ Step B เมื่อได้รับอนุญาตและใช้ schema นี้โดยไม่สร้างสำเนา. อ่าน principles ที่ระบุใน action ก่อนใช้ contract. ทุก `output/` เป็น path ใน working project. ตัวอย่างในคอลัมน์ Example value เป็นรูปแบบเท่านั้น ไม่ใช่ project evidence.

## 1. Contract

| Field | Rule |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose | Generate the estimation workbook from approved Step 01-06 artifacts. Reporting/export only; it does not introduce a new step or modify Step 06 baseline. |
| Outputs | TWO artifacts produced in order: (1) `output/estimation_workbook.md`: Markdown summary that mirrors §4 sheet-by-sheet with real rows; (2) `output/estimation_workbook.xlsx`: Excel workbook generated **from** the Markdown summary via the bundled [converter](../../orbit-export-workbook/scripts/md_to_workbook.py). |
| Generation workflow | Step A: orbit-prepare-workbook writes/refreshes `output/estimation_workbook.md` per §5 and stops. Step B: orbit-export-workbook runs the [converter contract](../../orbit-export-workbook/references/contract.md) to materialise the `.xlsx`. `generate both` / `continue to xlsx` authorizes the router to invoke Step B after Step A passes its mandatory gates; it does not make preparation run conversion. Re-run Step B whenever the Markdown summary changes. |
| Source of truth | Approved Step 01-06 outputs feed the Markdown summary; the Markdown summary feeds the `.xlsx`. The `.xlsx` MUST NOT contain content that is not present in the Markdown summary. Step 00 only for TOR/RFP clarity score, assumptions, and traceability already referenced downstream. |
| Approval | All Step 01-06 sources must be approved. Draft exception: only if user explicitly requests; watermark the Markdown summary header and `README` sheet with `DRAFT - source artifact not approved` and list unapproved artifacts. |
| Baseline lock | Do not change Step 04 Raw MD, Step 05 Adjusted MD, Step 06 contingency/range, or approved baseline scope (see [baseline and scenarios](../../principle-orbit-baseline-and-scenarios/SKILL.md)). Workbook-specific views that must not feed Delivery Baseline unless explicit re-baseline is recorded: scenario deltas, scope cuts, SG2-if-excluded, management reserve, MVP/cap/budget-fit views. |
| Commercial boundary | Follows [planning, not pricing](../../principle-orbit-planning-not-pricing/SKILL.md); see VAL-12 for where forbidden commercial terms may appear. |
| Formula-first | Express arithmetic totals, percentages, ranges, and mechanically derived checks as live formulas in BOTH artifacts. Source MD inputs, benchmark inputs, and evidence-based judgments remain sourced literals. Semantic atomicity, acceptance, and readiness are reviewed judgments, not provable by a cell-presence formula. Use concrete A1 references; the converter creates neither Excel Tables nor named ranges. |
| IDs | Carry the stable [evidence and traceability](../../principle-orbit-evidence-and-traceability/SKILL.md) IDs plus inventory IDs (`FN-`, `BI-`, `SCR-`, `API-`) and canonical `WBS ID` values such as `1.X.XX` / `2.X.XX`. Represent WBS through `WBS Ref` / coverage / mapping columns; no standalone `WBS` sheet unless explicitly requested. |
| Failure behavior | If Markdown generation fails, STOP and state the limitation. If `.xlsx` generation via the [converter](../../orbit-export-workbook/scripts/md_to_workbook.py) fails (missing dependency, schema mismatch, formula error), STOP, surface the script's error, and leave the Markdown summary intact. Do not silently substitute one artifact for the other. |

## 2. Required Source Artifacts

| Step | Artifact | Workbook Use |
| ------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 01 | `output/step_01_intake_scope.md` | Scope in/out (incl. `OS-XX` deferred items), baseline scope basis, assumptions, constraints, open questions, traceability seeds. |
| 02 | `output/step_02_architecture_constraints.md` | Architecture decisions, tech stack, constraints, NFRs, integration baseline, complexity drivers. |
| 03.1 | `output/step_03_01_feature_inventory.md` | Feature/subfeature inventory, SG grouping, enterprise completeness, data assumptions. |
| 03.2 | `output/step_03_02_backlog_inventory.md` | Backlog & subfeature coverage, UI screens, sitemap (if included), APIs, integration coverage, count summary. The workbook derives 5W1H from these plus Step 03.1 §1.2. |
| 03.3 | `output/step_03_03_wbs_baseline.md` | WBS refs/mapping, DoD/milestone deviations, exclusions, scope traceability, subfeature-to-WBS mapping. |
| 04 | `output/step_04_sizing_estimate.md` + `output/step_04_sizing_review.md` | Numeric sizing/Raw MD from estimate; QA reconciliation, calibration, cross-check, scope-cut scenarios, and arithmetic gate from companion review. |
| 05 | `output/step_05_resource_plan.md` | Adjusted MD, productivity inputs, PM derivation, resource matrix, timeline, critical path. |
| 06 | `output/step_06_risk_contingency.md` | Risk register, contingency, P25/P50/P75/P90 range, reserve, final planning baseline snapshot. |

## 3. Sheets (in order)

Create exactly these sheets unless the user explicitly requests additions. Names must be Excel-safe (≤31 chars).

| # | Sheet | Source | Purpose |
| --: | --------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 0 | `README` | 01-06 | Workbook control, source versions, sheet index, no-pricing rule, approved baseline scope, final planning snapshot, validation summary. |
| 1 | `Assumption Confirmation` | 01-06 | Assumptions, confirmations, decisions, open questions, owners, impact, due dates, fallback, baseline treatment. |
| 2 | `In-Out Scope` | 01 | In/out/scenario classification, SG, priority, owner, impact, traceability. |
| 3 | `Architecture` | 02 | Architecture baseline, tech stack, integration approach, NFRs, constraints, complexity drivers. |
| 4 | `Feature Inventory` | 03.1 | Atomic subfeature inventory with SG, behavior, actor, outcome, readiness, integration relationship. |
| 5 | `Backlog Inventory` | 03.2 + 03.3 refs | Backlog items, subfeature mapping, deferred/not-doing treatment, WBS coverage. |
| 6 | `UI API Inventory` | 03.2 + 03.3 refs | UI screens, APIs, 5W1H metadata, integration coverage, WBS coverage, complexity. |
| 7 | `Estimate Sizing` | 04 + 03.3 refs | Sizing detail + summary, Raw MD, role split, QA formula, calibration, scenario cuts. |
| 8 | `Timeline Resource` | 05 | Productivity inputs, Adjusted MD, resource matrix, task timeline, duration, critical path. |
| 9 | `Risk` | 06 | Risk register, contingency, P25/P50/P75/P90, Delivery Baseline, Management Reserve, Planning Total, triggers, final snapshot. |

## 4. Sheet Format Contract

All sheets: compact layout per §4.10, wrap long text. Default number formats: MD `0.0`, FTE `0.00`, percent `0.0%`, dates as date type, integers as integer. Use the table names declared in each subsection.

Every sub-section below uses one consistent column-spec layout:

| Col | Header | Description | Example value | Format guide |

Columns must be created in the order shown. Additional approved Step 04 roles require suffix columns in applicable sizing detail/summary tables and matching Step 05 resource rows; this preserves source effort and is not new scope. Other suffix columns require explicit request. Mechanically derived checks feed `tbl_validation_summary`; carry reviewed source judgments with evidence instead of claiming formula proof.

### 4.0 `README` — `tbl_readme_control` + `tbl_validation_summary`

Layout: control key-value block + validation summary block on the same sheet.

#### 4.0.1 `tbl_readme_control`

| Col | Header | Description | Example value | Format guide |
| ----- | ------------ | ---------------------------------- | ------------------------------------ | --------------------- |
| A | Field | Control field name | `Delivery Baseline` | text |
| B | Value | Field value (literal or formula) | `='Risk'!B20` (illustrative; resolve address from final layout) | text/number/formula |
| C | Source Ref | Source artifact / sheet / cell | `Risk!Snapshot` | text |
| D | Note | Clarification or assumption | `Locked 2026-05-21` | text |

Required `Field` rows: Workbook Name, Project Name, Version, Generated Date, Source Artifacts, Approved Baseline Scope, Approval State, Approval Basis, No-Pricing Rule, Raw MD, Adjusted MD, Delivery Baseline, Management Reserve, Planning Total, P25, P50, P75, P90, Confidence, Integration Count, External Risk Count, Top Risks, Re-estimation Triggers, Baseline-vs-Scenario Note, Validation Summary, Calculation Status.

Use these exact numeric control names with source references, not invented inputs or totals.

- `Working Days per Week`, `Focus Factor`, and `Delivery Weeks` define the common delivery horizon.
- For each source role, include `{role} Raw MD`, `{role} Rework Rate`, `{role} Buffer Rate`, `{role} Adjusted MD`, `{role} Warranty Adjusted MD`, and `{role} Delivery Adjusted MD`. Preserve sourced rework/buffer MD, `PM Base MD`, and warranty effort/horizon in additional control rows. Do not invent a role adjustment or treat PM Base MD as proof of calendar-derived PM.
- `{role} Average FTE` = `{role} Delivery Adjusted MD` ÷ (`Delivery Weeks` × `Working Days per Week` × `Focus Factor`). `Average FTE` is the sum of those demand-derived role values. Delivery demand excludes separately scheduled warranty.
- `{role} Allocation Average FTE` = that role's matrix `FTE-Weeks` ÷ `Delivery Weeks`. `Allocation Average FTE` uses total allocated FTE-Weeks over the same horizon. Keep these distinct from demand-derived Average FTE. Include them when the source reports allocation averages, and disclose any separate warranty horizon.
- Preserve `Recommended Contingency MD`, `Selected Commitment Uplift`, `Contingency MD`, and `Selected Delivery Basis` from Step 06. The last field contains the selected `P25`, `P50`, `P75`, or `P90` label with its decision evidence in Source Ref/Note.
- `Reserve Rate` and `Reserve Denominator` make reserve arithmetic explicit. The denominator is exactly `Delivery Baseline` or `Adjusted MD`, as approved. Step 06 normally uses Delivery Baseline. A different basis needs its source exception, not an export-time change.

Derive arithmetic with resolved cell references. Missing calculation inputs remain disclosed gaps, not zero defaults. Keep calibration/review evidence in notes referencing Step 04 Review.

#### 4.0.2 `tbl_validation_summary`

| Col | Header | Description | Example value | Format guide |
| ----- | ---------- | ------------------------ | --------------------------- | -------------- |
| A | Check ID | VAL identifier from §7 | `VAL-03` | text |
| B | Result | Pass / Warning / Fail | `Pass` | formula/text |
| C | Severity | High / Medium / Low | `High` | text |
| D | Note | Evidence or rationale | `QA within FE+BE cross-check for all rows` | text |

Roll up every applicable row check with `Fail > Warning > Pass`; a check for Fail alone loses Warning. `Validation Summary` in `tbl_readme_control` must show the highest unresolved result. In each affected validation row's Note, use `finding=<key>; row=<stable ID>; cell=<sheet!address>; expected=<value/rule>; actual=<value>; source=<artifact revision/section>; action=<next action>`. Use `rationale=<reason>` where no corrective action is required. Include the verifier finding key when available and an exact row ID or cell reference. Label unavailable evidence explicitly. Preserve these warnings in the final handoff. A rationale or approval does not turn an unresolved Warning into Pass.

### 4.1 `Assumption Confirmation` — `tbl_assumption_confirmation`

One row per assumption / decision / confirmation / open question. Qualify OQ IDs by originating step, such as `OQ-01(Step02)`. Consolidate refined ASM/DEC rows by their stable project-wide ID and cite the source delta. A closed item is not overdue merely because its old due date has passed.

Approval to use an assumption is not confirmation of its content. Preserve each source ASM ID, wording, owner, fallback, and evidence status. Keep `Assumption` in Status and record any authorized default in Fallback Default/notes, separately from Included baseline treatment. Change to `Confirmed` only with direct confirming evidence.

| Col | Header | Description | Example value | Format guide |
| ----- | --------------------- | ---------------------------------------------------------------------------- | ------------------------------------------- | -------------- |
| A | ID | Stable identifier (`ASM-` / `DEC-` / `OQ-`) | `ASM-02` | text |
| B | Statement | Plain-language assumption or decision | `Client provides cleansed migration data` | text |
| C | Type | Scope / Integration / Data / NFR / Timeline / Resource / Risk / Acceptance | `Integration` | text |
| D | Status | Confirmed / Assumption / Open / Excluded / Scenario / Draft | `Open` | text |
| E | Owner | Decision owner | `Business Owner` | text |
| F | Impact If Wrong | MD / timeline / scope / risk impact | `+30 MD migration; schedule risk` | text |
| G | Baseline Treatment | Included / Excluded / Scenario / Open / Discovery Needed | `Included` | text |
| H | Due Date | Date the decision is required | `2026-06-15` | date |
| I | Fallback Default | Default used if user says `use defaults` | `Assume client-cleansed data` | text |
| J | Workbook Treatment | Where it lands in the workbook | `In-Out Scope + Risk row` | text |
| K | Related Scope | Scope IDs | `IS-04, IS-07` | text |
| L | Related Integration | INT IDs | `INT-03` | text |
| M | Related Risk | Risk IDs | `RSK-08` | text |
| N | Status Check | Status value valid | `Pass` | formula |
| O | Due Date Check | Due Date present and not overdue | `Pass / Overdue` | formula |
| P | Owner Check | Owner populated | `Pass` | formula |

### 4.2 `In-Out Scope` — `tbl_in_out_scope`

One scope table with baseline / scenario / exclusion classification; conditionally highlight Scenario/Out rows.

| Col | Header | Description | Example value | Format guide |
| ----- | ----------------------------- | ------------------------------------------------ | --------------------------- | -------------- |
| A | Scope ID | Stable scope ID | `IS-01` | text |
| B | Scope Area | Module / capability area | `Authentication` | text |
| C | Description | Short scope description | `SSO + OTP for employees` | text |
| D | In/Out/Scenario | In / Out / Scenario / Discovery Needed | `In` | text |
| E | SG | SG1 / SG2 / N/A | `SG1` | text |
| F | Priority | Must / Should / Could / Won't / N/A | `Must` | text |
| G | Owner | Owner | `Business Owner` | text |
| H | Baseline Treatment | Included / Excluded / Scenario / Re-baseline | `Included` | text |
| I | Impact If Changed | Effect on MD / timeline / risk | `+15 MD if SG2 added` | text |
| J | Notes | Notes | `Apply Azure AD baseline` | text |
| K | Source | TOR/RFP/artifact ref | `TOR §3.2` | text |
| L | Related Assumption/Decision | ASM / DEC refs | `ASM-02` | text |
| M | Related Feature | FN refs | `FN-01` | text |
| N | Related WBS | WBS IDs | `1.2.03` | text |
| O | Related Risk | Risk IDs | `RSK-04` | text |
| P | Scope Status Check | In/Out/Scenario value valid | `Pass` | formula |
| Q | SG Check | SG present and valid | `Pass` | formula |
| R | Traceability Check | At least one downstream ref (Feature/WBS/Risk) | `Pass` | formula |

### 4.3 `Architecture` — `tbl_architecture`

Combined register; integration rows use `Category = Integration`.

| Col | Header | Description | Example value | Format guide |
| ----- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------- |
| A | ID | Stable ID | `INT-03` | text |
| B | Category | Tech Stack / Integration / NFR / Constraint | `Integration` | text |
| C | Item | Tech-stack / integration / NFR / constraint label | `Microsoft Azure AD` | text |
| D | Description | Detail | `Real-time SSO authentication` | text |
| E | Complexity Impact | Low / Medium / High | `High` | text |
| F | Baseline Treatment | Included / Excluded / Scenario | `Included` | text |
| G | Owner | Decision / owner | `Architecture Lead` | text |
| H | Notes | Notes (incl. integration minima: Direction / Protocol / Trigger / R-W / Source of Truth / Failure-Retry / API Ref) | `Direction=Outbound; Protocol=OIDC; Trigger=Login; Source=Azure AD; Retry=manual` | text |
| I | Source | Source artifact ref | `Step 02 §4` | text |
| J | Related INT/NFR/DATA | Refs | `NFR-02, DATA-01` | text |
| K | Related WBS | WBS IDs | `2.3.05` | text |
| L | Related Risk | Risk IDs | `RSK-05` | text |
| M | Source Check | Source ref present | `Pass` | formula |
| N | Integration Coverage Check | Integration row mapped to INT inventory | `Pass` | formula |
| O | NFR Coverage Check | NFR row mapped to NFR list | `Pass` | formula |

### 4.4 `Feature Inventory` — `tbl_feature_inventory`

One row per atomic subfeature; repeat feature-level fields on each subfeature row for filtering.

| Col | Header | Description | Example value | Format guide |
| ----- | ---------------------------- | ------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| A | Feature ID | Feature reference | `FN-01` | text |
| B | Subfeature ID | Atomic subfeature ref | `FN-01.01` | text |
| C | Module | Feature group | `User Administration` | text |
| D | Feature | Feature title | `Authentication & Login (SSO + OTP)` | text |
| E | Feature Detail | Feature-level summary; **MAY BE EMPTY** when subfeature narratives (col F) already describe the feature | (empty) or short summary | text |
| F | Subfeature Name | Atomic action / capability | `เมื่อพนักงานคลิก login ระบบ redirect ไป Azure AD แล้วสร้าง session` | text |
| G | SG | SG1 / SG2 | `SG1` | text |
| H | Priority | Must / Should / Could / Won't | `Must` | text |
| I | Behavior Type | Copy Step 03.1 Behavior Type vocabulary | `User-facing` | text |
| J | Primary Actor/System | Actor or system | `Employee` | text |
| K | Outcome Description | Outcome statement | `Session created; role mapped` | text |
| L | Acceptance Evidence | Acceptance evidence from Step 03.1 §1.2 | `Step 03.1 FN-01.01 acceptance condition` | text |
| M | Integration Relationship | Direct / Shared / No external integration | `Direct` | text |
| N | Sizing Readiness | Ready / Needs clarification | `Ready` | text |
| O | INT Ref | INT IDs | `INT-03` | text |
| P | Scope Ref | Scope IDs | `IS-01` | text |
| Q | Blocker ID | Open ASM/DEC blocking sizing | `N/A` | text |
| R | Subfeature Atomicity Check | Reviewed atomicity verdict from Step 03.1, with evidence | `Pass` | sourced judgment |
| S | INT Ref Check | INT Ref resolves when relationship is Direct or Shared | `Pass` | formula |
| T | Sizing Readiness Check | Readiness consistent with Blocker ID | `Pass` | formula |

### 4.5 `Backlog Inventory` — `tbl_backlog_inventory`

One row per source backlog item / subfeature mapping. Deferred/not-doing items remain in `In-Out Scope` under OS IDs; do not invent BI IDs or active backlog rows for them. Highlight Missing WBS coverage.

| Col | Header | Description | Example value | Format guide |
| ----- | -------------------------------- | ------------------------------------------------- | -------------------------------------------- | -------------- |
| A | BI ID | Backlog item ID | `BI-014` | text |
| B | User Story / Enabler | Story or enabler title | `As an employee I can log in via SSO` | text |
| C | Stakeholder-Readable Detail | Plain-language detail | `Employee taps Login → Azure AD → session` | text |
| D | Type | Feature / Enabler / Tech Debt | `Feature` | text |
| E | Priority | Must / Should / Could / Won't | `Must` | text |
| F | Subfeature Name | Subfeature name | `SSO login flow` | text |
| G | Coverage Status | Complete / Partial / Missing / N/A | `Complete` | text |
| H | WBS Coverage Status | Covered / Missing / N/A | `Covered` | text |
| I | Deferred / Not Doing Treatment | Active, or `OS-XX` from Step 01 §3.3 / Step 03.1 §0.3 | `Active` | text |
| J | WBS Mapping Note | Why mapped that way | `BI maps to FE+BE+QA tasks` | text |
| K | Notes | Notes | `OTP variant follow-up` | text |
| L | FN Ref | Feature reference | `FN-01` | text |
| M | Subfeature Ref | Subfeature reference | `FN-01.01` | text |
| N | Scope Ref | Scope IDs | `IS-01` | text |
| O | WBS Ref | WBS IDs | `1.2.03` | text |
| P | Subfeature Coverage Check | Subfeature ref populated for active rows | `Pass` | formula |
| Q | WBS Coverage Check | WBS Coverage Status = Covered for baseline rows | `Pass / Warning` | formula |
| R | Deferred Treatment Check | Deferred rows excluded from baseline sizing | `Pass` | formula |

### 4.6 `UI API Inventory` — `tbl_ui_api_inventory`

A combined export of the source SCR/API inventory, optional sitemap, and integration coverage. Preserve source counts and IDs. Do not invent SCR rows for email templates, reusable components, or states absent from Step 03.2. Supplemental 5W1H, Sitemap, and Integration Coverage rows do not increase screen/API counts or sizing.

**Why combined:** a screen and the APIs it calls share the same traceability path (BI → Feature → Subfeature → WBS) and the same complexity drivers (Cx, Reuse, INT). Keeping them on one sheet lets reviewers spot orphans (an API with no UI consumer, a screen with no API), missing integration coverage, and 5W1H gaps in one place instead of across three sheets.

**Inventory Type cheat-sheet** — controls which downstream fields are required and which validation checks run:

| Inventory Type | Row represents | Own ID format | Mandatory fields beyond core metadata |
| ------------------------ | ------------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------- |
| `UI` | User-facing screen, page, modal, drawer, dialog, email template | `SCR-NNN` | Type/Method, Cx, Reuse, SCR Ref = own ID, FN Ref + Subfeature Ref, WBS Ref |
| `API` | Backend operation: REST endpoint, RPC call, event handler | `API-NNN` | Type/Method (HTTP verb), Cx, Reuse, API Ref = own ID, INT Ref if external |
| `UI 5W1H` | 5W1H elaboration for a UI row | `SCR-NNN.5W1H` | 5W1H Summary fully populated, SCR Ref = parent UI |
| `API 5W1H` | 5W1H elaboration for an API row | `API-NNN.5W1H` | 5W1H Summary fully populated, API Ref = parent API |
| `Sitemap` | Node in the screen sitemap (only when Step 03.2 §2.1 is included) | `SITE-NNN` | Name/Operation = node label; Notes = parent + position |
| `Integration Coverage` | One INT × one consumer (UI or API) confirming the integration is used | `INTCOV-NNN` | INT Ref + (SCR Ref or API Ref) + BI Ref |

**Columns:**

| Col | Header | Description | Example value | Format guide |
| ----- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------- |
| A | ID | Stable row identifier, formatted per Inventory Type (see cheat-sheet above). Unique across the entire sheet. | `SCR-014` | text |
| B | Inventory Type | Which lens the row represents. Drives which fields are required and which validation checks fire. One of `UI` / `API` / `UI 5W1H` / `API 5W1H` / `Sitemap` / `Integration Coverage`. | `UI` | text |
| C | Module | Functional module / capability group the artefact belongs to. Must match the Module value used in `Feature Inventory` so cross-sheet pivots reconcile. | `User Administration` | text |
| D | Name/Operation | Display name for `UI` rows (the title users see), operation name for `API` rows (e.g. `Login`, `GetUserProfile`), sitemap node label for `Sitemap` rows. Do NOT put IDs here — IDs live in column A. | `Login Page` | text |
| E | Stakeholder Detail | One-to-two-sentence plain-language description of what the artefact does FOR the user or consumer. Stakeholder-readable, no jargon. Reviewers use this to confirm the artefact is in-scope and well-understood. | `หน้าจอที่พนักงานใช้เข้าสู่ระบบด้วย SSO (Azure AD)` | text |
| F | Type/Method | `UI` rows: copy source screen type (`LIST`, `FORM-S`, `FORM-M`, `DETAIL`, `DASH`, `REPORT`, `CANVAS`, `MODAL`). `API` rows: HTTP method (`GET` / `POST` / `PUT` / `PATCH` / `DELETE`) or RPC verb. `Sitemap` / `Integration Coverage` / 5W1H: `N/A`. | `FORM-S` or `POST` | text |
| G | Cx | Complexity score that drives FE/BE sizing in Step 04. Copy the approved S/M/C value and rationale from Step 03.2. Do not re-score complexity during export. `N/A` for non-sizable rows (Sitemap, 5W1H, Integration Coverage). | `M` | text |
| H | Reuse | Reuse factor versus an already-built artefact in the same baseline. `1.0` = brand-new build, `0.3` = significant reuse with minor adjustments, `0` = identical reuse (count once, do NOT re-size in Step 04), `N/A` for non-sizable rows. | `0.3` | number 0.0 |
| I | 5W1H Summary | One-line summary in the order Who / What / When / Where / Why / How. Mandatory for `UI 5W1H` and `API 5W1H` rows; recommended on every `UI` / `API` row to anchor the artefact in real usage context. Empty for `Sitemap` / `Integration Coverage`. | `Employee / log in / business hours / web+mobile / access / SSO` | text |
| J | Coverage Status | Is the row's required metadata (Type/Method, Cx, Reuse, 5W1H, refs) fully populated for its Inventory Type? `Complete` / `Partial` / `Missing` / `N/A`. Used by reviewers to chase down incomplete rows before sizing. | `Complete` | text |
| K | WBS Coverage Status | Has the artefact been mapped to one or more WBS tasks in Step 03? `Covered` = WBS Ref populated and accepted; `Missing` = no WBS task yet (will block Step 04 sizing); `N/A` for non-sizable rows (Sitemap, 5W1H, Integration Coverage). | `Covered` | text |
| L | WBS Mapping Note | Free-text explaining how this artefact maps to its WBS task(s). Useful when one artefact spans multiple WBS items (e.g. a Page that triggers both an FE task and a separate BE task, or one API used by two WBS work packages). | `Page maps to FE-Login + BE-AuthCallback` | text |
| M | Notes | Anything else a reviewer needs to know: deferred variants, accessibility constraints, mobile-vs-desktop split, parking-lot questions, security/PII flags. | `Mobile variant deferred to phase 2` | text |
| N | BI Ref | Backlog Item IDs (`BI-NNN`) that drive this artefact (comma-separated when multiple). Used to traceability-check that every approved BI lands on at least one concrete UI/API row. | `BI-014, BI-017` | text |
| O | FN Ref | Feature IDs (`FN-NN`) the artefact covers (comma-separated). Must reconcile with `Feature Inventory`. | `FN-01` | text |
| P | Subfeature Ref | Atomic Subfeature IDs (`FN-NN.NN`); the leaf-level traceability anchor for sizing. | `FN-01.01` | text |
| Q | SCR Ref | Screen IDs the row references. For `UI` rows = own ID. For `API` rows = the screens that consume this API. For `UI 5W1H` rows = parent screen. For other types use as appropriate or `N/A`. | `SCR-014` | text |
| R | API Ref | API IDs the row references. For `API` rows = own ID. For `UI` rows = APIs the screen calls. For `API 5W1H` rows = parent API. For other types use as appropriate or `N/A`. | `API-021, API-022` | text |
| S | INT Ref | Integration IDs (`INT-NN`) the row triggers. **Mandatory** on any `API` row that calls an external system, and on every `Integration Coverage` row. Feeds VAL-09 (every `INT-` must appear in at least one inventory row). | `INT-03` | text |
| T | Scope Ref | Scope IDs (`IS-XX` / `IS-UXX` / `OS-XX`) the row supports. Confirms scope coverage flows from Step 01 down to concrete UI/API artefacts. | `IS-01` | text |
| U | WBS Ref | WBS IDs the row maps to (comma-separated). Mandatory for baseline-sizable artefacts (`UI`, `API`); `N/A` for non-sizable rows. Feeds VAL-13. | `1.2.03, 1.2.04` | text |
| V | Cx Check | Formula. Sizable rows (`UI` / `API`): `Cx ∈ {S, M, C}`. Non-sizable rows: `Cx = N/A`. Returns `Pass` / `Fail`. | `Pass` | formula |
| W | Reuse Check | Formula. Sizable rows: `Reuse ∈ {0, 0.3, 1.0}`. Non-sizable rows: `Reuse = N/A`. Returns `Pass` / `Fail`. | `Pass` | formula |
| X | INT Coverage Check | Formula. If `Inventory Type = API` AND the operation calls an external system, `INT Ref` must be populated; otherwise `N/A`. Returns `Pass` / `Warning`. Pairs with VAL-09. | `Pass / Warning` | formula |
| Y | WBS Coverage Check | Formula. For sizable types (`UI` / `API`): `WBS Coverage Status = Covered`; otherwise `N/A`. Returns `Pass` / `Fail`. Feeds VAL-13. | `Pass` | formula |

**Row-quality rules of thumb:**

- Every active baseline BI must have its source UI/API mapping or the explicit N/A reason from Step 03.2. A non-UI/non-API subfeature is not automatically an orphan.
- Every `INT-` in `Architecture` should appear in at least one `API` row's `INT Ref` OR in a dedicated `Integration Coverage` row.
- Every UI/API row should have either a matching UI/API 5W1H row or a fully populated 5W1H Summary cell. Pick one convention per project and keep it, so reviewers do not have to guess where the 5W1H lives.
- Derive Who from the specific operation. Distinguish the initiating user, administrator, service account, external system, and background worker. Copy the actor/system from the matching source operation or subfeature, not a generic actor across all rows. Cite the source revision, section and SCR/API/subfeature ID in existing Notes and 5W1H metadata. Missing or contradictory actor evidence is a finding, not permission to invent an actor.
- A UI row with Reuse=0 has no duplicate FE implementation MD. Preserve actual WBS/test/integration mapping and canonical SCR-ID; N/A is valid only when the source gives a reason. Reuse does not exclude the entire subfeature from sizing.
- `Sitemap` rows are organisational only; they MUST NOT carry Cx / Reuse / WBS Ref values. Their job is to give reviewers a tree view of how `UI` rows hang together.
- `Integration Coverage` rows are the auditable link between `Architecture` (INT inventory) and the consumers; do not double-size them, because they exist only for VAL-09 coverage.

### 4.7 `Estimate Sizing`

Four sub-tables: Features → Integrations → Non-Dev → Summary. Detail rows hold Raw MD only (no rework/buffer; those live in §4.8). Roles consistently ordered `UX/UI, BA, SA, FE, BE, QA, DevOps`; omit a role column only when the sub-table never sizes it.

#### 4.7.1 Features — `tbl_sizing_features`

One row per approved baseline atomic subfeature. Derive SG from `Feature Inventory` using exact subfeature-ID lookup for bucket formulas; do not infer SG from numbering. Scenario-only AFN/SG2 rows belong to `tbl_scenarios`, not baseline totals. Copy short subfeature names, not outcome prose.

| Col | Header | Description | Example value | Format guide |
| ----- | ---------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------- |
| A | Feature ID | Feature reference | `FN-01` | text |
| B | Subfeature ID | Atomic subfeature reference | `FN-01.01` | text |
| C | Module | Feature group | `User Administration` | text |
| D | Feature Name | Short feature title | `Authentication & Login (SSO + OTP)` | text |
| E | Subfeature Name | User-visible action / capability | `เมื่อพนักงานคลิก login ระบบ redirect ไป Azure AD แล้วสร้าง session ให้อัตโนมัติ` | text |
| F | Implementation Notes | Bullets of UI Pages / Components / APIs / Workers / Backend Logic / Integrations. Render as real newline-separated bullets in Excel using `\n- `, not `<br>`. Wrapped row heights are estimated after final column widths, capped at 409pt. Inspect the rendered cells for clipping. | `- [UI] Login Page (SCR-014)\n- [API] Login (API-021)\n- [INT] Azure AD (INT-03)` | bullet list (newline-separated in cell) |
| G | UX/UI | UX/UI Raw MD | `0.5` | number 0.0 |
| H | BA | BA Raw MD | `1.0` | number 0.0 |
| I | SA | SA Raw MD | `1.0` | number 0.0 |
| J | FE | FE Raw MD | `3.0` | number 0.0 |
| K | BE | BE Raw MD | `3.0` | number 0.0 |
| L | QA | QA Raw MD from Step 04 (test cases × MD/case); VAL-03 cross-checks it against FE+BE | `12.0` | 0.0 |
| M | Total | Row total Raw MD | `=SUM(G2:L2)` | formula 0.0 |

#### 4.7.2 Integrations — `tbl_sizing_integrations`

One row per external integration; sizes only roles that participate.

| Col | Header | Description | Example value | Format guide |
| ----- | ------------------------ | ----------------------------- | ------------------------------------------ | -------------- |
| A | INT ID | Integration ID | `INT-03` | text |
| B | System / Capability | External system name | `Microsoft Azure AD` | text |
| C | Description | Usage purpose | `SSO authentication for employees` | text |
| D | Interface Count | Interfaces / endpoints used | `- Authorize<br/>- Token<br/>- UserInfo` | bullet list |
| E | Integration Complexity | Low / Medium / High | `Medium` | text |
| F | SA | SA Raw MD | `1.0` | number 0.0 |
| G | FE | FE Raw MD | `2.0` | number 0.0 |
| H | BE | BE Raw MD | `3.0` | number 0.0 |
| I | QA | QA Raw MD | `2.0` | number 0.0 |
| J | DevOps | DevOps MD only if present in approved integration sizing; otherwise 0 | `0.0` | number 0.0 |
| K | Total | Row total Raw MD | `=SUM(F2:J2)` | formula 0.0 |

#### 4.7.3 Non-Dev Activities — `tbl_sizing_non_dev`

Cross-cutting non-dev activities (workshops, FS orchestration, governance, etc.).

| Col | Header | Description | Example value | Format guide |
| ----- | ---------------- | ------------------------------------- | --------------------------------------------------------------- | -------------- |
| A | ND ID | Non-dev activity ID | `ND-01` | text |
| B | Activity | Activity description | `Cross-module Requirement Workshop + Master FS orchestration` | text |
| C | Roles Involved | Roles participating in the activity | `BA, SA, UX` | text |
| D | UX/UI | UX/UI Raw MD | `0.5` | number 0.0 |
| E | BA | BA Raw MD | `1.0` | number 0.0 |
| F | SA | SA Raw MD | `1.0` | number 0.0 |
| G | FE | FE Raw MD | `0.0` | number 0.0 |
| H | BE | BE Raw MD | `0.0` | number 0.0 |
| I | QA | QA Raw MD | `0.0` | number 0.0 |
| J | DevOps | DevOps Raw MD | `1.0` | number 0.0 |
| K | Total | Row total Raw MD | `=SUM(D2:J2)` | formula 0.0 |

#### 4.7.4 Summary — `tbl_sizing_summary`

QA cells derive from the documented S/M/C test-case counts and MD/case inputs in source Implementation Notes, integration descriptions, and non-dev activities. Include those inputs in the Markdown rows/notes and use weighted formulas; do not replace them with FE+BE percentages. Additional approved role columns must participate in row totals and Raw MD checks. Carry Surface IDs in Feature Detail, inventory Notes, and sizing Implementation Notes with a source reference. Keep Module labels unchanged so cross-sheet grouping remains consistent.

Bucket × role totals; every value formula-driven from the three detail tables.

| Col | Header | Description | Example value | Format guide |
| ----- | ---------------------- | ----------------------------------------------------------------------- | ---------------------- | ---------------------- |
| A | Bucket | SG1 Features / SG2 Features / Integration / Non-Dev / Raw Grand Total | `SG1 Features` | text |
| B | UX/UI | Bucket UX/UI Raw MD | `=SUMIFS(...)` | formula 0.0 |
| C | BA | Bucket BA Raw MD | `=SUMIFS(...)` | formula 0.0 |
| D | SA | Bucket SA Raw MD | `=SUMIFS(...)` | formula 0.0 |
| E | FE | Bucket FE Raw MD | `=SUMIFS(...)` | formula 0.0 |
| F | BE | Bucket BE Raw MD | `=SUMIFS(...)` | formula 0.0 |
| G | QA | Bucket QA Raw MD | `=SUMIFS(...)` | formula 0.0 |
| H | DevOps | Bucket DevOps Raw MD | `=SUMIFS(...)` | formula 0.0 |
| I | Bucket Total | Row total | `=SUM(B2:H2)` | formula 0.0 |
| J | % of Raw Grand Total | Bucket share of Raw Grand Total | `=I2/$I$6` (illustrative) | formula percent 0.0% |
| K | QA vs FE+BE Check | VAL-03 sanity check: QA vs FE+BE, Warning when deviating without rationale | `Pass / Warning` | formula |
| L | Bucket Sum Check | VAL-02 row-level check | `Pass / Fail` | formula |

Required `Bucket` rows: `SG1 Features`, `SG2 Features`, `Integration`, `Non-Dev`, `Raw Grand Total`.

### 4.8 `Timeline Resource`

Aligned to Step 05 (`output/step_05_resource_plan.md` §4 + §5). TWO tables share the same weekly columns. Only the resource matrix has an extra phase-band header row.
1. **Weekly Resource Matrix** — one row per role × week columns W1..Wn
2. **Task / Phase Timeline** — one row per task × the same week columns W1..Wn, with cells color-coded by phase band when active

Drop any separate Phase Band Map table. Phase bands appear ONLY as a merged header row above the week labels in the Excel header (e.g., `Foundation` spans W1-W2; `BUILD-MP1` spans W3-W7; etc.).

Title the sheet: `Step 05 — Timeline & Resource Matrix (Adjusted-effort plan [N] wk)`.

#### 4.8.1 Weekly Resource Matrix — `tbl_resource_matrix`

Wide layout with weeks as columns and roles as rows. The Excel header has TWO physical rows:
- Row 1 (merged cells): Phase Band labels spanning their week columns (Foundation / BUILD-MP1..MPn / QA / Go-Live / Hypercare). Each phase band cell is filled with its band color.
- Row 2: Column headers (`#`, `Role`, `W1`, `W2`, … `Wn`, `FTE-Weeks`, `MD`, `Effective MD`, `Adjusted MD`, `Coverage Ratio`).

Derive `defaults.phase_bands` from the Step 05 phase-band row. Include labels/week ranges/fills in the Markdown summary as configuration metadata, then pass a temporary project config to the CLI with `--config`. Do not rely on the renderer's built-in example week ranges or mutate the shared config. The resource matrix inserts one band row; the task timeline does not insert one in the current converter. Account for this in A1 formula addresses and disclose the layout limitation.

| Col | Header | Description | Example value | Format guide |
| ----- | --------------- | ------------------------------------------------------------------- | ------------------- | ----------------- |
| A | # | Numeric row sequence | `1` | number integer |
| B | Role | Role name (PM, UX/UI, BA, SA, FE, BE, DevOps, QA, Change) | `PM` | text |
| C… | W1, W2 … Wn | One column per calendar week; FTE allocation for the role | `1.0` / `0.5` | number 0.00 |
| X1 | FTE-Weeks | Sum of FTE allocations across all weeks for the role | `=SUM(C3:L3)` (illustrative ten-week row) | formula 0.00 |
| X2 | MD | Nominal delivery MD = FTE-Weeks × sourced working days/week | `=M3*5` (illustrative) | formula 0.0 |
| X3 | Effective MD | Nominal delivery MD × sourced Focus Factor | [concrete formula] | formula 0.0 |
| X4 | Adjusted MD | Delivery portion of role Adjusted MD from README control rows, excluding separately scheduled warranty | [concrete formula] | formula 0.0 |
| X5 | Coverage Ratio | Effective MD ÷ Adjusted MD; N/A if no demand | [concrete formula] | formula percent 0.0% |

Last row = **Total FTE/week** (column B bold), each `W1..Wn` cell = `=SUM(role rows in that week)`, FTE-Weeks total = `=SUM(FTE-Weeks col)`, MD total = `=SUM(MD col)`.

Notes:
- FTE-Weeks = sum of per-week FTE values across active weeks.
- MD = FTE-Weeks × WORK_DAYS_PER_WEEK (default 5 → multiplier 5).
- MD is nominal calendar-derived. Effective MD and Coverage Ratio make VAL-05 auditable; check every role and the total, not only the grand total. Source warranty schedule effort/capacity in README control rows and check combined delivery + warranty against full Adjusted MD. Do not include warranty twice.
- Keep unused roles with all-zero week cells (e.g., Change=0) so the matrix stays auditable.

#### 4.8.2 Task / Phase Timeline — `tbl_task_timeline`

Wide-layout Gantt sharing the same W1..Wn columns as §4.8.1. Active week cells are color-filled (no `■` text; fill color encodes phase/task class). In the Markdown summary, write the literal cell text `active` (case-insensitive) to mark an active week — the script fills that cell and removes the text; leave the cell empty for an inactive week. This differs from [resource planning contract](../../orbit-plan-resources/references/contract.md)'s own `■` legend, which describes that artifact, not this sheet — do not write `■` here. Sub-task numbering (`3.1`, `3.2`, …) decomposes parents. When BUILD splits, list each Mini-Phase as its own row.

| Col | Header | Description | Example value | Format guide |
| ----- | ------------------ | --------------------------------------------------------------------------------------------------- | -------------------------------------- | ---------------- |
| A | # | Row number (supports sub-tasks `2.1`, `3.1`) | `2.1` | text |
| B | Task / Phase | Task or phase name | `BUILD-MP1: Auth + Platform` | text |
| C… | W1, W2 … Wn | One column per calendar week; cell filled (no text) if task active in that week, blank otherwise | (fill only) | fill |

Required default task rows (per Step 05 §5):

| # | Task / Phase | Fill color (suggested) |
| ---: | --- | --- |
| (header) | Requirement and Design | light blue `#DDEBF7` |
| 1 | Foundation & POC | medium blue `#9DC3E6` |
| 2 | Develop (BUILD) | light blue (parent) |
| 2.1+ | BUILD-MP1..MPn: [feature group] | light blue per MP |
| 3 | Infrastructure | beige `#FFE699` |
| 3.1 | Setup DEV Environment | yellow `#FFF2CC` |
| 3.2 | Setup SIT Environment | yellow `#FFF2CC` |
| 3.3 | Setup UAT Environment | yellow `#FFF2CC` |
| 3.4 | Setup PROD Environment | yellow `#FFF2CC` |
| 4 | SIT | light green `#C6E0B4` |
| 5 | UAT | light green `#C6E0B4` |
| 6 | NFT (Performance + Security) | grey `#808080` |
| 7 | Regression Test | light peach `#FCE4D6` |
| 8 | CAB (Change Approval Board) | light grey `#D9D9D9` |
| 9 | CUT — Cutover Weekend | orange `#F4B084` |
| 10 | Hypercare ([N] wk) | light green `#C6E0B4` (or `N/A — excluded` if hypercare excluded in Step 04; warranty is independent) |

Phase Band header colors above the sprint columns (applied to §4.8.1 row 1 + matching task rows in §4.8.2):
- Foundation: light navy `#D9E1F2`
- BUILD / BUILD-MP*: medium blue `#9DC3E6` / light blue `#BDD7EE`
- QA: light grey `#E7E6E6`
- Go-Live: orange `#F4B084`
- Hypercare: light green `#C6E0B4`

Footer note in the sheet: `FTE-Weeks = sum of FTE per role across delivery weeks. MD is nominal; Effective MD = MD × Focus Factor. Delivery plus separate warranty capacity reconciles to Adjusted MD within 95-105% by role.`

### 4.9 `Risk`

Four sub-tables + snapshot block. Risk score integer; conditionally highlight High risks and failed checks.

#### 4.9.1 Risk Register — `tbl_risk_register`

| Col | Header | Description | Example value | Format guide |
| ----- | ------------------------------ | -------------------------------------------------------------- | --------------------------------------------- | ----------------- |
| A | Risk ID | Stable ID | `RSK-04` | text |
| B | External Cause / Risk | Risk statement | `CRM sandbox availability delay` | text |
| C | Top-Level Theme | Exact Step 06 theme label | `Integration / External Dependency` | text |
| D | Band | Low / Medium / High from Score | `=IF(E2>=15,"High",IF(E2>=7,"Medium","Low"))` | formula/text |
| E | Score | `P × I` | `=F2*G2` | formula integer |
| F | P | Probability score 1-5 | `4` | number integer |
| G | I | Impact score 1-5 | `4` | number integer |
| H | Prob % | Derived from P using 10/30/50/70/90% | `=CHOOSE(F2,10%,30%,50%,70%,90%)` | formula percent 0.0% |
| I | Effort Impact MD | MD if risk realizes | `15.0` | number 0.0 |
| J | Expected MD | `Prob % × Effort Impact MD` | `=H2*I2` | formula 0.0 |
| K | Owner | External decision/dependency owner | `Client Integration Owner` | text |
| L | Mitigation / Decision Needed | Mitigation plan | `Request sandbox by W2` | text |
| M | Contingency Treatment | Delivery Baseline / Management Reserve / Scenario Delta | `Delivery Baseline` | text |
| N | Baseline Classification | Included / Excluded / Scenario | `Included` | text |
| O | Related Refs | REQ / INT / NFR / DATA / ASM / DEC / SCN / WBS / Step05 refs | `INT-03, WBS 1.2.03` | text |
| P | Risk Formula Check | Score and Expected MD formulas valid | `Pass` | formula |
| Q | Contingency Mapping Check | Mapped to named driver (ASM / DEC / SCN / RSK) | `Pass / Fail` | formula |

#### 4.9.2 Range & Reserve — `tbl_range_reserve`

| Col | Header | Description | Example value | Format guide |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------- | ---------------------- |
| A | Category / Scenario | Adjusted MD / Contingency / Delivery Baseline / Management Reserve / Planning Total / P25 / P50 / P75 / P90 | `P75` | text |
| B | Effort MD | Effort value | [resolved A1 formula] | formula 0.0 |
| C | Percent of Adjusted MD | `Effort MD / Adjusted MD` | `=B2/$B$2` (illustrative) | formula percent 0.0% |
| D | Confidence | Confidence level | `75%` | percent 0.0% |
| E | Scope | Baseline / Scenario label | `Baseline` | text |
| F | Duration | Calendar duration if applicable | `10 weeks` | text |
| G | Usage | Purpose label | `Recommended planning baseline` | text |
| H | Includes Contingency | Y / N | `Y` | text |
| I | Includes Management Reserve | Y / N | `N` | text |
| J | Notes | Notes | `Reserve held by sponsor` | text |
| K | Formula | Formula matching Step 06; no statistical σ claim | `P75 = P50 + max(0.5 × Recommended Contingency, 5% × Adjusted MD)` | text |
| L | Range Formula Check | VAL-08 check | `Pass` | formula |
| M | Reserve Separation Check | Reserve not double-counted | `Pass` | formula |

#### 4.9.3 Scenarios — `tbl_scenarios`

| Col | Header | Description | Example value | Format guide |
| ----- | --------------------------- | ---------------------------------------- | -------------------------------------- | -------------- |
| A | Scenario ID | Scenario ID | `SCN-DATA-CLEANSING` | text |
| B | Scenario Name | Name | `Data cleansing in-scope` | text |
| C | Description | Detail | `Vendor handles full data cleansing` | text |
| D | MD Delta | +/- MD vs baseline | `+25.0` | number 0.0 |
| E | Duration Delta | +/- weeks vs baseline | `+2 weeks` | text |
| F | Risk Impact | Impact summary | `Adds reconciliation risk` | text |
| G | Baseline Treatment | Scenario / Re-baseline / Exclusion | `Scenario` | text |
| H | Re-baseline Trigger | Trigger | `Client approves cleansing scope` | text |
| I | Notes | Notes | `Do not merge with baseline` | text |
| J | Source | Source artifact ref | `Step 04 Review §4` | text |
| K | Related Refs | Scope / Assumption / Risk refs | `IS-04, ASM-02, RSK-08` | text |
| L | Scenario Separation Check | Scenario not feeding Delivery Baseline | `Pass` | formula |

#### 4.9.4 Final Snapshot Block — `tbl_final_snapshot`

Key-value block; same layout as `tbl_readme_control` but locked to the Step 06 final planning baseline.

| Col | Header | Description | Example value | Format guide |
| ----- | ------------ | --------------------------- | -------------------------------- | --------------------- |
| A | Field | Snapshot field | `Delivery Baseline` | text |
| B | Value | Value | `=B2+B5` (illustrative) | formula/number/text |
| C | Source Ref | Source artifact / formula | `Adjusted MD + Contingency MD` | text |
| D | Note | Clarification | `Locked 2026-05-21` | text |

Required `Field` rows: Adjusted MD, Recommended Contingency MD, Selected Commitment Uplift, Contingency MD, Selected Delivery Basis, Delivery Baseline, Management Reserve, Planning Total, P25, P50, P75, P90, Top Risks, Confidence, Re-estimation Triggers.

In `tbl_range_reserve`, preserve the expected-risk subtotal and every named Step 06 adjustment as separate rows so Recommended Contingency is derivable. Selected delivery Contingency = Recommended Contingency + Selected Commitment Uplift. If P75 is selected, Delivery Baseline must equal P75. Never double-count uplift or reserve.

Key formulas: `Score = P × I`; `Expected MD = Prob % × Effort Impact MD`; `Delivery Baseline = Adjusted MD + Contingency MD`; `Planning Total = Delivery Baseline + Management Reserve`.

### 4.10 Style Polish (applies to all sheets)

Apply the formatting below, then inspect the actual rendered workbook. Width-based row-height estimates are not a guarantee of readable layout. Tables are static reports. Follow the Filters and Freeze panes rules below.

| Aspect | Rule |
| --- | --- |
| Header row | Fill `#1F4E78`, white bold configured font at 10pt, centered, wrapped, border bottom 1px. Rotate a header 90° when its longest word cannot fit the fixed width; keep the exact header text. |
| Sub-table header (when stacked) | Fill `#2E75B6`, white bold configured font at 10pt, centered, with the same wrap/rotation rule |
| Font | `defaults.font_name`, default `Noto Sans Thai`. Confirm the font is installed in the rendering environment and supports all source glyphs. |
| Header height | Minimum 18pt. Estimate wrapped height after final column widths, capped at 409pt. |
| Data rows | Configured font at 10pt, minimum 15pt. Estimate wrapped height after final column widths, capped at 409pt. Text top-aligned with wrap; numeric cells middle-right-aligned. |
| Row fill | **All-white** background on every data row (no alternating banding). Visual separation comes from black cell borders, not fill color. |
| Cell borders | Thin black border on all 4 sides of every header and data cell within tables (header + body). Non-table areas have no borders. |
| Text alignment | Text → left + wrap; Numbers (MD/FTE/%/integer) → right with wrapping for text results; Status (Pass/Warning/Fail/Y/N) → center; sequence and ID headers → center. A text field in the first column remains left-wrapped. |
| MD / FTE / % cells | Right-aligned with number formats from the [export runtime contract](../../orbit-export-workbook/references/contract.md#cli-and-conversion-behavior) and its explicit project config |
| Status cells (Pass/Warning/Fail) | Conditional formatting: Pass=green `#C6EFCE`, Warning=amber `#FFEB9C`, Fail=red `#FFC7CE` |
| Resource matrix heatmap | `tbl_resource_matrix` weekly FTE cells (W1..Wn × role rows, excluding Total row + summary cols) get a 3-color ColorScale: 0=white, 2.0=`#FFEB9C` (warm yellow), 4.0=`#F8696B` (red). Light load = cool, heavy load = hot. |
| High-impact cells (Raw MD, Adjusted, Delivery Baseline, Planning Total, P90) | Bold; no font-size bump; border-top thin |
| Bullet cells (Implementation Notes, Interface Count) | Real newlines with wrap_text=True. Height estimate uses final widths and line breaks, capped at 409pt. Check clipping, Thai line breaks and font substitution in the rendered workbook. |
| Column widths | Fixed per-keyword widths — see the column width recipes below. |
| Filters | **NO auto-filter** on any Excel Table |
| Freeze panes | **NO freeze panes** on any sheet |
| Title block | **DROP per-table title block** — sheet name in tab; table identity from header context only (compact layout) |
| Sheet tab color | README=`#1F4E78`; Sizing/Risk=`#C00000` (highlight); Timeline=`#2E75B6`; others=default |
| No gridlines outside tables | Hide gridlines on non-table areas |
| Print setup | Landscape, fit to 1 page wide. Repeat headers only on single-table sheets, using both rows for a resource matrix. Stacked tables must not repeat another table's header. Rotate narrow phase labels instead of widening the fixed week columns. Inspect actual print pages. |

#### Column width recipes (per header keyword, in characters)

| Header pattern | Width |
| --- | ---: |
| `#` / `Seq` / `No` | 4 |
| ID columns (`Feature ID`, `Subfeature ID`, `BI ID`, `SCR ID`, `API ID`, `INT ID`, `ND ID`, `Risk ID`, `Scenario ID`, `Scope ID`) | 12 |
| `Module` | 16 |
| `Feature` / `Feature Name` | 24 |
| `Subfeature Name` / `Statement` / `Description` / `Stakeholder Detail` / `User Story` | 40 |
| `Implementation Notes` / `Notes` / `Interface Count` / `Mitigation` / `WBS Mapping Note` | 50 |
| `SG` / `Priority` / `Cx` / `Type` / `Status` / `Owner` (short labels) | 10 |
| Role MD columns (`UX/UI`, `BA`, `SA`, `FE`, `BE`, `QA`, `DevOps`, `Change`, `PM`, `Total`) | 6 |
| `MD` / `FTE` / `Score` numeric columns | 8 |
| Week columns (`W1`, `W2`, … `Wn`) | 4 |
| `Coverage Ratio` / `Percent of Adjusted MD` / `Prob %` | 8 |
| `Refs` / `Related Refs` / `Source` / `Source Ref` | 18 |
| `Check` columns (formula) | 8 |
| Default fallback | 12 |

## 5. Markdown Summary File — `output/estimation_workbook.md`

This file is produced FIRST and is the single source from which the `.xlsx` is generated. It is human-reviewable and must contain every row that will appear in the workbook (not placeholders).

### 5.1 File header

```markdown
# Estimation Workbook Summary — [PROJECT_NAME]

- Generated: YYYY-MM-DD
- Source artifacts: Step 01-06 (list versions/paths)
- Approved Baseline Scope: SG1-only / SG1+SG2 / TBD
- Approval State: Draft / Approved / Needs Revision
- No-Pricing Rule: enforced
- Target .xlsx: `output/estimation_workbook.xlsx`
- Generator script: [resolved installed orbit-export-workbook/scripts/md_to_workbook.py path]
```

### 5.2 Section-per-sheet layout

One H2 section per sheet, in the order defined in §3. The H2 heading MUST encode the sheet index and sheet name so config can match it. Table names belong in H3 sub-headings or the config registry:

```markdown
## Sheet 7 — Estimate Sizing
```

Optional short description (one paragraph) right after the heading, then one or more Markdown tables per the column-specs in §4. Tables MUST use the exact `Header` row text from §4 (used as the lookup key for column format/type).

### 5.3 Sub-tables (sheets with multiple `tbl_*`)

For sheets containing multiple tables (`README`, `Estimate Sizing`, `Timeline Resource`, `Risk`), use H3 sub-headings that contain the `tbl_*` name in backticks. The script keys off the backticked table name, so heading text around it can vary:

```markdown
### 7.1 Features — `tbl_sizing_features`

| Feature ID | Subfeature ID | Module | ... |
| --- | --- | --- | --- |
| FN-01 | FN-01.01 | User Administration | ... |

### 7.2 Integrations — `tbl_sizing_integrations`

| INT ID | System / Capability | ... |
| --- | --- | --- |
| INT-03 | Microsoft Azure AD | ... |
```

### 5.4 Formula cells

Formulas appear as backtick-wrapped, leading-`=` Excel expressions. Use valid A1 references with row numbers, such as `=SUM(G2:L2)`, and quoted sheet names such as `='Estimate Sizing'!M2`. Formula examples in §4 are schematic; resolve addresses after computing final row layout. Names such as `Raw_Grand_Total` and `tbl_*` are not defined Excel names. Do not emit unresolved symbols, `...`, whole-column sums that include their own subtotal, or structured table references.

The converter writes formula text but does not calculate formulas or cached results. Recalculate with Excel/LibreOffice and inspect results when available. Otherwise record `Not recalculated` and independent numeric reconciliations; never claim formula checks passed from file creation alone.

The current converter removes the apostrophe from literal `'=...`, so openpyxl can still treat it as a formula. Do not rely on that escape for untrusted text. If source text starts with `=`, `+`, `-`, or `@`, stop for safe literal handling or use a labelled textual rendering with a non-formula prefix. Never silently execute source text as a formula.

### 5.5 Required content per sheet

Every sheet listed in §3 must be fully populated per its §4 column spec — no `...` placeholders.

### 5.6 Stop and review gate

After writing/refreshing `output/estimation_workbook.md`, STOP and present the review gate. Offer `approve workbook Markdown`, `revise workbook Markdown: ...`, `continue to xlsx`, and `stop` using the available ask tool, or numbered chat options when unavailable. Record the reviewed revision and approval basis. `generate both` / `continue to xlsx` may authorize the router to invoke the separate export action after all mandatory gates pass. Preparation never invokes conversion itself. Re-running Step B without changing the Markdown is idempotent.

## 6. Excel Generation Script

The [export contract](../../orbit-export-workbook/references/contract.md) owns the runtime CLI, module API, configuration, exit codes, verification, and failure behavior. The bundled [converter](../../orbit-export-workbook/scripts/md_to_workbook.py), [configuration](../../orbit-export-workbook/scripts/workbook_config.yaml), and [requirements](../../orbit-export-workbook/scripts/requirements.txt) belong to that action. Preparation does not run them.

Section 4 owns all sheet schemas and layout; §5 owns Markdown syntax; §7 owns VAL-01 through VAL-14. Export consumes these sections unchanged. Resolve installed script paths independently of the working-project output paths. Always pass the project-specific config explicitly, with phase bands derived from the approved Step 05 source and recorded in the Markdown.

## 7. Validation Rules

The Markdown author writes formulas for mechanical checks and sourced verdicts for semantic checks. The converter only writes/styles those cells. The separate [verifier](../../orbit-export-workbook/references/contract.md#independent-workbook-verifier) compares parsed input rows with actual formulas and cached values from the delivered XLSX. It is not a formula engine or a semantic source reviewer. Run it after final recalculation, or report missing caches as warnings when recalculation is unavailable.

Keep independent semantic review against approved Step 01-06 detail rows. Check operation-specific actors, source identity, assumptions, exclusions, integration meaning, atomicity, acceptance and readiness. A populated cell or author-written `Pass` is not independent evidence. Report implemented numeric coverage and uncovered checks separately. Apply the warning disclosure and roll-up rule in §4.0.2.

| ID | Rule |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| VAL-01 | For every role, including approved extra roles, compare each SG1 Features, SG2 Features, Integration and Non-Dev summary cell against its matching detail rows. Derive feature SG by exact subfeature-ID lookup. Reconcile each role's Raw Grand Total too. A matching grand total cannot hide a swapped role or bucket. |
| VAL-02 | Bucket totals SG1 + SG2 + Integration + Non-Dev = Raw Grand Total. |
| VAL-03 | QA vs FE + BE cross-check per applicable detail row and summary total; QA is sized from test cases in Step 04, and deviation without rationale returns Warning. |
| VAL-04 | Step 05 Adjusted MD = Raw MD + applicable rework + applicable buffer + Step 05-derived PM. |
| VAL-05 | Compare effective capacity and delivery demand for every role and total over the same Delivery Weeks horizon, within 95-105%, else Warning. Reconcile separately scheduled warranty to full Adjusted MD. Check demand-derived Average FTE independently of allocation averages. |
| VAL-06 | Delivery Baseline = Adjusted MD + Contingency MD. |
| VAL-07 | Planning Total = Delivery Baseline + Management Reserve. |
| VAL-08 | Check every risk row's Score = P × I, Prob % mapping of P = 1/2/3/4/5 to 10/30/50/70/90%, and Expected MD = Prob % × Effort Impact MD. Check each P25/P50/P75/P90 equation against the Step 06 Scenario Formula Reference, then ordering separately. Reconcile Recommended Contingency to expected-risk subtotal plus named adjustments, selected uplift to selected range minus P50, and reserve to its sourced rate and denominator. An ordered range alone is not a formula pass. Preserve approved exception rationale and the unresolved discrepancy status. |
| VAL-09 | Every baseline INT ID resolves in Architecture, has UI/API coverage and sizing, and maps to Risk only if an applicable uncertainty exists; explicit N/A reasons are allowed. A mention on any one sheet is not full coverage. |
| VAL-10 | Every baseline subfeature traces through Feature Inventory, Backlog Inventory, WBS mapping and Estimate Sizing; UI/API mapping has source refs or explicit N/A reason. Preserve non-UI capabilities. |
| VAL-11 | Baseline and scenario deltas remain separate; scenarios do not feed Delivery Baseline formulas unless re-baseline is recorded. |
| VAL-12 | Forbidden commercial terms do not appear as workbook output (fields, calculations, values, pricing tables, commercial deliverables). They may appear only in no-pricing guardrails, validation labels, or remediation notes. |
| VAL-13 | Every baseline `BI-XX`, `SCR-XX`, `API-XX`, `INT-XX`, and atomic subfeature has WBS reference coverage or explicit `N/A — [reason]`. |
| VAL-14 | Formula-first mechanical checks use valid resolved A1 addresses and produce no circular/undefined references. Recalculated values match independent numeric checks, or README records Not recalculated with warnings. |

For VAL-08, let A be Step 05 Adjusted MD and C be non-negative Recommended Contingency MD. Independently compute P25 = A + min(C, max(0.5 × C, 0.05 × A)), P50 = A + C, P75 = P50 + max(0.5 × C, 0.05 × A), and P90 = P75 + max(0.5 × C, 0.10 × A). Then check P25 ≤ P50 ≤ P75 ≤ P90. Compare each actual cell with its own expected result, not only the adjacent range values. Use the approved Step 06 exception if one exists and disclose the deviation. These are planning heuristics, not statistically validated percentiles.
