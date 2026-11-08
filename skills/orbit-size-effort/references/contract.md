# orbit-size-effort contract

Read the [action guide](../SKILL.md) and all its required principles before execution, including direct invocation. `output/` and input artifact paths resolve from the working project. Bundled guidance links resolve from this installed contract. Produce only this action's outputs and stop. Approval and continuous-mode authorization never bypass mandatory quality gates. The router alone may authorize the next action.

Read [role boundaries](../../principle-orbit-effort-accounting/references/roles.md) and [calibration guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md). Estimate and Review are one deliverable with matching revision, revision date, baseline scope, Approval State, and Approval Basis. Keep explicit companion links. A correction invalidates approval for the changed revision until both files pass the gate together. Inventory S/M/C and sizing L/M/H are different judgments, not an automatic conversion.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | Generate Step 04 raw effort sizing from approved Step 03 feature/subfeature, backlog, UI/API, integration, and WBS inventories. |
| Input | `output/step_03_03_wbs_baseline.md`, `output/step_03_02_backlog_inventory.md`, `output/step_03_01_feature_inventory.md`, approved architecture/integration artifact. |
| Output | **Two files** produced together and kept in sync before the Post-step Review Gate: (a) `output/step_04_sizing_estimate.md`: numeric sizing tables; (b) `output/step_04_sizing_review.md`: QA reconciliation, inventory cross-check, calibration, scope cuts, and arithmetic gate. |
| Prerequisite | Approved Step 03.3 WBS baseline. |
| Missing prerequisite | STOP and ask user to run/approve [orbit-build-wbs](../../orbit-build-wbs/references/contract.md) first. |
| Guidance | MUST apply [Estimation Calibration Guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md) in the Review file Calibration Pass; calibration validates the estimate only. Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน). |
| Next command | Hand off to [orbit-plan-resources](../../orbit-plan-resources/references/contract.md) with Raw MD by role, bucket totals, assumptions, dependencies, and open sizing risks. |
| In scope | Cx judgment, feature/subfeature sizing (SG1/SG2), integration sizing, non-dev sizing, sizing summary (Estimation file); QA reconciliation, inventory cross-check, calibration, scope-cut scenarios, arithmetic gate (Review file). |
| Out of scope | Phasing, timeline, duration, sprint, calendar, PM role/task, Step 05 adjusted effort, resource plan, Step 06 contingency/range/reserve, or any commercial output. |
| Baseline declaration | Declare Approved Baseline Scope before sizing: `SG1-only` or `SG1+SG2`, same value in both files. SG2-if-excluded and AFN are scenario-only unless the user explicitly says `re-baseline` (see [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน) for the general MVP/cap/budget-fit/scope-cut scenario rule). |
| Role coverage | Default columns are a starting schema. If approved WBS requires DE, DBA, Change, or a specialist, append role columns to applicable detail tables and every role summary/handoff before sizing; do not hide their work under BE or DevOps. Each row Total sums all participating role columns. Use UX/UI=UX and DevOps=DO consistently. |
| Unit & seniority | 1 MD = 8 hours; delivery team seniority 3-5 years unless explicitly changed. |
| Atomic subfeature | One baseline row per approved `FN-XX.NN`. `AFN-XX.NN` stays scenario-only until approved and promoted with an ID mapping. No grouped ranges (e.g. `FN-01.01..08`) and no high-level feature rows in baseline detail. |
| Surface tag | Carry forward the Surface tag (`SUR-XX`) from Step 03.1 onto every feature sub-header; multi-surface features keep comma-separated IDs. Include a Surface Rollup table inside §5 Sizing Summary showing MD per surface. |
| Cx judgment | Assign Cx (L/M/H) by judgment using Implementation Notes scope (screens, APIs, integrations, business rules, data, security) before assigning MD. Use the Complexity-to-MD Reference in the Appendix as range guidance. |
| QA basis | **QA MD = Test Case Count × MD/case benchmark** (default S=0.1, M=0.2, C=0.4 MD/case unless calibrated). Size by actual test scope: functional + regression + integration + UAT support cases. Do NOT derive QA from FE+BE. Per-row QA total in Estimation §1–§4 must equal Review §1 QA Reconciliation total and Estimation §5 Sizing Summary QA total. |
| Separation | Keep feature/subfeature sizing, integration sizing, and non-dev sizing separate. Shared work has one sizing owner and references from other rows. Do not repeat SA/BA, FE/BE API work, or QA cases across buckets. |
| Warranty | Included in Raw MD as a separate non-dev row by default. Excluded only if stated consistently everywhere. |
| Names & refs | Copy the short subfeature name, not its outcome narrative. Implementation Notes hold UI/API/INT refs, `[Cx]`, and S/M/C test counts. Add short names or incremental drivers only when refs do not explain the estimate. WBS refs stay in Step 03.3 `## 5.1`. |
| Arithmetic gate | Reconcile role totals, bucket totals, ROM, QA reconciliation, and handoff to the same Raw Grand Total before publishing. Any changed number triggers a full baseline correction sweep across both files. |

## Execution Flow

1. Read approved `output/step_03_03_wbs_baseline.md` with the Step 03.2/03.1 inventories and approved architecture/integration artifact; STOP if the WBS baseline is missing. Confirm only high-impact blockers: Approved Baseline Scope, SG2/AFN treatment, estimation basis/seniority, warranty handling, page/API/INT count assumptions, QA test-case basis (default or project-specific), and sizing confidence. If none, state `No blocking confirmations; proceeding with approved baseline/defaults.`
2. Fill `Approved Inputs Consumed` with the WBS count from the Step 03.3 Step Summary and screen/API/INT counts from Step 03.2 `## 5`.
3. Size bottom-up: one row per atomic subfeature for SG1, then SG2 (or the SG1-only `N/A` statement), each under its feature sub-header (Surface tag) with the short subfeature name, Implementation Notes refs, Cx judgment first, then role MD; then integrations one row per system/capability; then non-dev activities from the Appendix catalog (no PM; warranty row by default).
4. Build the Sizing Summary by role and bucket, Surface Rollup, SG1-only baseline, Raw Grand Total, and ROM ±25%.
5. Produce the Review file: QA Reconciliation per row, Inventory Cross-Check against the Appendix benchmark, Calibration Pass per [calibration guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md), Scope Cut Opportunities as scenario-only, and Arithmetic Quality Gate with Correction Log.
6. Run the arithmetic gate across both files; sweep both files after any changed number.
7. Ask up to 5 highest-impact stakeholder-answerable open items with finite choices in one gate using the asking tool or chat fallback, then revise both files before publishing.
8. Fill Step Summary, Handoff Note — Step 05, and Internal Review; publish both files together and stop at the embedded Post-step Review Gate and stop; a subsequent action requires separate router authorization.

## Output Contract — File 1: Estimation

Create/update `output/step_04_sizing_estimate.md` using the schema below. Reconcile every total against the Review file before publishing. Record the actual MD unit, seniority, warranty treatment, and QA benchmarks in `Approved Inputs Consumed`. Replace default benchmark values when calibration changes them; retain the rationale and decision ref.

Keep Implementation Notes concise; do not copy inventory descriptions. Use `N/A — [reason]` for a dimension with no UI, API, or integration. Keep the complexity driver when refs alone do not explain MD. S/M/C test counts remain explicit; rates come from `Approved Inputs Consumed` unless a documented row-specific override applies.

```markdown
# Step 04 — Sizing Estimate: [PROJECT_NAME]

**Source**: `output/step_03_03_wbs_baseline.md` [approved revision] + `output/step_03_02_backlog_inventory.md` [approved revision]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Companion Review File**: `output/step_04_sizing_review.md`
**Approved Baseline Scope**: SG1-only / SG1+SG2
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [บันทึกผู้อนุมัติ/วันที่หรือ workflow authorization ตามหลักการ explicit approval ที่โหลดจาก action guide]

## Step Summary

- Scope basis: [SG1-only / SG1+SG2]. Raw MD by role and bucket, counts, and ROM are in the Handoff Note (canonical numeric block for Step 04); do not restate them here.
- Top roles: [role list]; QA sized from test cases × MD/case.
- Confidence: L/M/H.
- Review file status: `output/step_04_sizing_review.md` — reconciliation/calibration/arithmetic gate [Pass/Warning/Fail].
- Exclusions respected: no phasing/timeline/PM, no Step 05/06 outputs.

## Handoff Note — Step 05

- Raw MD by role (excluding PM).
- Bucket breakdown: SG1, SG2, Integration, Non-Dev, Raw Grand Total.
- ROM ±25% range and SA+BA share.
- Atomic subfeature row count (no grouped baseline ranges).
- Page/API/INT assumptions and names.
- QA basis: total test cases [N] (S/M/C split), MD/case used, reconciliation passed (see Review file §1).
- Integration count: `[N]` (from §3 Integrations); Architecture complexity: `[Low/Medium/High]` if carried from Step 02.
- Dependencies: INT, data, NFR, client/external readiness, user decisions.
- Warranty handling: [included/excluded].
- Approved baseline scope; scenarios are separate.
- Step 05 owns PM effort, phasing, duration, staffing, resource matrix.

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 04 Sizing**

Both `step_04_sizing_estimate.md` and `step_04_sizing_review.md` must be published together.

Reply options:
- `approve Step 04` = lock raw sizing baseline (both files) and hand off to Step 05 without executing it.
- `revise Step 04: ...` = update sizing before proceeding.

## ภาคผนวก

## Approved Inputs Consumed

| Input | Value | Note |
|---|---:|---|
| WBS Count | [N] | SG1=[N], SG2=[N] |
| Backlog Items | [N] | [SG split] |
| UI Pages / Screens | [N] | S=[N], M=[N], C=[N] |
| APIs | [N] | S=[N], M=[N], C=[N] |
| Integration Coverage | [X/Y] | Missing=[list/N/A] |
| MD Unit | Default: 8 hours per MD | [actual value; approved change ref if different] |
| Team Seniority | Assumption: 3-5 years | [ASM/DEC ref; actual basis and impact if different] |
| Warranty Handling | Included in Raw MD as separate row / Excluded with rationale | [ND row ref or exclusion rationale; matches Step 05] |
| QA MD/case Benchmark | S=0.1, M=0.2, C=0.4 | Adjusted=[Y/N + rationale] |
| Open Sizing Assumptions | [N] | [top items] |

## 1. Features — SG1

One row per atomic subfeature, grouped under one sub-header per feature. Module and surface appear once in the sub-header, not on every row.

### FN-XX [feature title] · [module] · [SUR-XX from Step 02 §1.1; comma-separated if multi-surface]

| Sub Feature ID | Sub Feature Name | Implementation Notes | UX/UI | BA | SA | FE | BE | QA | Total |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| FN-XX.NN | [short subfeature name from Step 03.1] | - [UI] SCR-XX<br>- [API] API-XX<br>- [INT] INT-XX<br>- [Cx] [L/M/H]; [driver if needed]; tests S/M/C=([N], [N], [N]) | [MD] | [MD] | [MD] | [MD] | [MD] | [MD] | =SUM(UX:QA) |

**SG1 Subtotal**: [N] MD

## 2. Features — SG2

If **Approved Baseline Scope = SG1-only**: write `N/A — SG2 is scenario/excluded from approved baseline`, set SG2 subtotal to `0 MD`, exclude all SG2/AFN values from Raw Grand Total, ROM, and Step 05 handoff.

Same sub-header and columns as Section 1.

**SG2 Subtotal**: [N] MD

## 3. Integrations

One row per integration system/capability.

| System/Capability | Description | Integration Count | Integration Complex | SA | FE | BE | QA | Total | Refs |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| [system name] | [usage description in Thai] | - [interface 1]<br>- [interface 2] | L / M / H | [MD] | [MD or 0] | [MD] | [MD] | =SUM(SA:QA) | INT-XX, API-XX, WBS 1.5.XX |

Note: FE is normally `0` unless integration UI work is explicitly included and not already sized in features. Record S/M/C test-case counts and benchmarks in Description for each integration row. QA covers happy path, retry/error, and reconciliation without repeating feature or non-dev cases.

**Integration Subtotal**: [N] MD

## 4. Non-Dev Activities

Cross-cutting only. No PM tasks. Include warranty only if baseline includes warranty.

| ND ID | Activity | Role | UX/UI | BA | SA | FE | BE | QA | DevOps | Total |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ND-XX | [activity] | [primary role] | [MD] | [MD] | [MD] | [MD] | [MD] | [MD or 0] | [MD] | =SUM(UX:DevOps) |
| ND-16 | Warranty Support | Support | [MD] | [MD] | [MD] | [MD] | [MD] | [MD] | [MD] | =SUM(UX:DevOps) |

Note: QA in non-dev rows is `0` when activity has no test scope. For non-zero QA, record S/M/C test-case counts and benchmarks in Activity. Count test design, execution, regression, and UAT support once under the documented MD/case basis; additional cycles need an explicit assumption. Warranty includes support/fix effort in the appropriate roles, not QA verification alone.

**Non-Dev Subtotal**: [N] MD

## 5. Sizing Summary

| Role | SG1 MD | SG2 MD | Integration MD | Non-Dev MD | Total MD | % |
|---|---:|---:|---:|---:|---:|---:|
| SA | [N] | [N] | [N] | [N] | [N] | [x%] |
| BA | [N] | [N] | [N] | [N] | [N] | [x%] |
| UX/UI | [N] | [N] | [N] | [N] | [N] | [x%] |
| FE | [N] | [N] | [N] | [N] | [N] | [x%] |
| BE | [N] | [N] | [N] | [N] | [N] | [x%] |
| QA | [N] | [N] | [N] | [N] | [N] | [x%] |
| DevOps | [N] | [N] | [N] | [N] | [N] | [x%] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[Raw Grand Total]** | **100%** |

**QA Reconciliation Check**: QA Summary total [N] = Review file §1 QA Reconciliation total [N] = Σ per-row QA in §1–§4.
**SG1-only baseline**: [N] MD = SG1 features + core Integration + core Non-Dev. Allocate shared work once; incremental SG2 integration/non-dev stays outside this core view.
**Raw Grand Total**: [N] MD
**ROM ±25%**: [N-low] to [N-high] MD

### Surface Rollup

Roll up §1+§2 feature MD only by Surface tag. Multi-surface features split MD evenly across tagged surfaces unless another allocation is justified. Integration and Non-Dev never enter this feature-only total. Feature counts per surface count memberships; the Total feature count is the distinct feature count, not the sum of memberships. MD and percentages must reconcile.

| SUR-ID | Surface Name | # Features | MD | % of Feature MD | Notes |
|---|---|---:|---:|---:|---|
| SUR-01 | [Internal Admin] | [N] | [N] | [x%] | [optional rationale] |
| SUR-02 | [Public Customer] | [N] | [N] | [x%] | [optional rationale] |
| SUR-03 | [Internal Dashboard] | [N] | [N] | [x%] | [optional rationale] |
| SUR-04 | [Backend / Integration] | [N] | [N] | [x%] | [optional rationale] |
| **Total** | — | **[N]** | **[Feature MD]** | **100%** | Matches §1+§2 subtotal |


```

## Output Contract — File 2: Review & Cross-Check

Create/update `output/step_04_sizing_review.md` using the schema below. Every detailed MD and total in this file must cite its source row or section in the Estimation file. Benchmark inputs and review findings cite their own source. Both files publish together.

```markdown
# Step 04 — Sizing Review & Cross-Check: [PROJECT_NAME]

**Companion Estimation File**: `output/step_04_sizing_estimate.md`
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approved Baseline Scope**: SG1-only / SG1+SG2
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [บันทึกผู้อนุมัติ/วันที่หรือ workflow authorization ตามหลักการ explicit approval ที่โหลดจาก action guide]

## 1. QA Reconciliation

Subtotals the test-case basis behind QA MD in Estimation file §1–§4 and proves they reconcile to Estimation file §5 Sizing Summary QA total. Per-subfeature test cases stay in the Estimation file `[Cx]` bullets; do not list them again here.

| Row Type | Group | Rows | Test Cases (S / M / C) | Total Cases | MD/case Avg | QA MD |
|---|---|---:|---|---:|---:|---:|
| Feature | [module] | [N subfeatures] | S=[N], M=[N], C=[N] | [N] | [0.1-0.4] | [MD] |
| Integration | INT-01..INT-XX | [N] | S=[N], M=[N], C=[N] | [N] | [0.1-0.4] | [MD] |
| Non-Dev | ND-XX [activity with test scope] | 1 | S=[N], M=[N], C=[N] | [N] | [0.1-0.4] | [MD] |
| **Total** | — | — | S=[N], M=[N], C=[N] | **[N]** | — | **[QA MD]** |

**QA Reconciliation Check**: Σ per-row QA in Estimation §1–§4 = QA total in this section = QA in Estimation §5 Sizing Summary.
**MD/case Adjustment**: [None / explain if benchmark adjusted with rationale and calibration evidence].

## 2. Inventory Cross-Check

Compare like-for-like scope, roles, and buckets. FE and BE rows compare only implementation represented by the screen/API inventory, excluding support, migration, and integration add-ons counted elsewhere. Apply screen reuse weights to the FE benchmark. Integration add-on covers incremental adapter/test work only. Overall must include the same approved QA, analysis, UX, and non-dev basis as Raw Grand Total; otherwise mark it `N/A — incomplete benchmark coverage`, compare the covered subtotals, and raise a final-check Warning. Delta = (Detailed MD − Cross-check MD) ÷ Cross-check MD; a zero denominator is N/A with reason.

| Basis | Count | MD Benchmark | Cross-check MD | Detailed MD (from Estimation) | Delta | Status | Note |
|---|---:|---|---:|---:|---:|---|---|
| FE by screen | [N] | S/M/C benchmark | [N] | [FE MD] | [x%] | Pass/Warning/Fail | [note] |
| BE by API | [N] | S/M/C benchmark | [N] | [BE MD] | [x%] | Pass/Warning/Fail | [note] |
| Integration add-on | [N] | INT benchmark | [N] | [INT MD] | [x%] | Pass/Warning/Fail | [note] |
| Overall | N/A | Cross-check vs detailed | [N] | [Raw Grand Total] | [x%] | Pass/Warning/Fail | Normal +15-30%; explain 0-15%; flag below 0% or above 30% per [calibration guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md) |

## 3. Calibration Pass

| Check | Benchmark | Result | Action | Related ASM/SCN/RSK |
|---|---|---|---|---|
| FE MD/screen | 1.5-6 normal; flag <1 or >10 | Pass/Warning/Fail | [explain] | [ref/N/A] |
| BE MD/API | 0.75-4 normal; flag <0.5 or >8 | Pass/Warning/Fail | [explain] | [ref/N/A] |
| QA MD/case | 0.1-0.4 normal; flag <0.05 or >0.6 | Pass/Warning/Fail | [explain] | [ref/N/A] |
| QA test-case coverage | Cases per screen 2-8 normal; per API 1-5 normal | Pass/Warning/Fail | [explain — under-coverage = missing scenarios; over = redundancy] | [ref/N/A] |
| QA vs FE+BE cross-check | QA total compared with FE+BE total; sanity check only, not a sizing formula | Pass/Warning | [explain any deviation from the test-case basis] | [ref/N/A] |
| Integration MD/type | Protocol, ownership, test complexity | Pass/Warning/Fail | [explain] | [ref/N/A] |
| Report/dashboard complexity | Query, aggregation, filters, access control, validation | Pass/Warning/Fail | [explain] | [ref/N/A] |
| Migration scope | Import, reconciliation, rollback | Pass/Warning/Fail | [explain] | [ref/N/A] |
| Similar-project benchmark | Historical reference if available | Pass/Warning/N/A | [explain] | [ref/N/A] |

## 4. Scope Cut Opportunities

| Item | Basis | MD Savable | Impact | Max Cut | Baseline Treatment | Refs |
|---|---|---:|---|---:|---|---|
| [item] | [approved baseline item / excluded SG2 or AFN] | [net removable baseline MD; 0 if already excluded] | [Thai impact] | [non-overlapping removable MD] | Scenario only; no silent re-baseline. | [refs] |

## 5. Arithmetic Quality Gate

| Check | Rule | Result | Note |
|---|---|---|---|
| Role totals | SG1 + SG2 + Integration + Non-Dev = role Total in Estimation §5 | Pass/Fail | [note] |
| Bucket totals | SG1 + SG2 + Integration + Non-Dev = Raw Grand Total | Pass/Fail | [note] |
| QA reconciliation | Per-row QA in Estimation §1–§4 = Review §1 QA Reconciliation total = Estimation §5 Summary QA | Pass/Fail | [note] |
| QA basis | Every QA value sourced from test-case count × MD/case (not FE+BE) | Pass/Fail | [note] |
| No phase/PM | No phasing, timeline, sprint, calendar, PM role/task in either file | Pass/Fail | [note] |
| Atomic subfeature | One row per subfeature in Estimation §1–§2; no range or grouped IDs | Pass/Fail | [note] |
| Warranty consistency | Included/excluded uniformly across both files | Pass/Fail | [note] |
| Summary/ROM/Handoff | All cite same Raw Grand Total | Pass/Fail | [note] |
| Inventory cross-check | Delta explained if warning/red | Pass/Fail | [note] |
| Calibration | Flagged items mapped to action/ASM/SCN/RSK | Pass/Fail | [note] |
| Baseline vs scenario | No silent merge of scope cuts/scenarios | Pass/Fail | [note] |
| SG1-only exclusion | SG2/AFN = 0 in Estimation totals when basis is SG1-only | Pass/Fail/N/A | [note] |
| Surface Rollup | Estimation §5 Surface Rollup total matches §1+§2 feature MD | Pass/Fail | [note] |

### Correction Log

| Item | From | To | Reason | Files Swept | Sweep Done |
|---|---:|---:|---|---|---|
| N/A | N/A | N/A | No correction required | N/A | N/A |

## 6. Open Questions / Assumptions

| ID | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [question] | [Thai impact] | [owner] | Before Step 05 / before baseline lock |

## 7. Internal Review

Render passing checks in one `Pass:` line and retain only Warning/Fail rows with evidence and action, per [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน).

QA basis/reconciliation, no phase/PM, warranty, arithmetic, and correction sweep are recorded in §5 Arithmetic Quality Gate and its Correction Log, not here.

| Check | Result | Note |
|---|---|---|
| Step 03.3 WBS consumed | Pass/Warning/Fail | [note] |
| Subfeature rows include Implementation Notes with UI/API/INT refs and `[Cx]` tests | Pass/Warning/Fail | [note] |
| Cx (L/M/H) assigned by judgment before MD | Pass/Warning/Fail | [note] |
| Feature / Integration / Non-Dev separated | Pass/Warning/Fail | [note] |
| Sub Feature Name matches Step 03.1 name | Pass/Warning/Fail | [note] |
| Step 05 handoff (in Estimation file) ready | Pass/Warning/Fail | [note] |
```

## Appendix — References

### Complexity-to-MD Reference

Range guidance only. The sizer picks Cx (L/M/H) by judgment from the Implementation Notes scope.

| Cx | SA | BA | UX/UI | FE | BE | Typical Test Cases / Row | Notes |
|---|---|---|---|---|---|---|---|
| L | 0.5-1 | 0.5-1 | 0.5-1 | 1-3 | 1-3 | 2-5 cases | Basic CRUD, simple page/API, no integration |
| M | 1-3 | 1-3 | 1-3 | 3-8 | 3-10 | 5-15 cases | Moderate rules, 1-2 integrations, approval |
| H | 3-8 | 3-8 | 3-8 | 5-15 | 5-15 | 10-30 cases | Complex rules, 3+ integrations, real-time |

QA MD per row = test case count × MD/case (default S=0.1, M=0.2, C=0.4).

### Non-Dev Activity Catalog

Use only when in delivery baseline. No PM tasks.

| ND ID | Activity | Boundary | QA Test Scope |
|---|---|---|---|
| ND-01 | Cross-module Requirement Workshop + Master FS orchestration | Cross-cutting only | None |
| ND-02 | Master ERD + Master OpenAPI + Data Dictionary | Whole-system only | None |
| ND-03 | UX/UI Design System | Cross-cutting design system | None |
| ND-04 | Environment & Monitoring | DevOps setup only | None |
| ND-05 | SIT Scenario Preparation | Cross-module test design support | SIT scenarios |
| ND-06 | UAT Support + Defect Triage Preparation | UAT support baseline only | UAT regression cases |
| ND-07 | Performance Test Support | Evidence support | Perf scenarios |
| ND-08 | Security Scan / VA / Pentest Support | Scan support and remediation evidence | Security test cases |
| ND-09 | DR/BCP / Backup-Recovery Evidence | Evidence support only | DR drill cases |
| ND-10 | Data Migration / Initial Load Support | Seed/load/reconciliation | Reconciliation cases |
| ND-11 | Master Data Seed / Reference Data Setup | Cross-module seed | None |
| ND-12 | Cutover / Go-Live Preparation | Release checklist support | Cutover dry-run cases |
| ND-13 | Training / User Manual / Admin Guide | Post-dev docs and material | None |
| ND-14 | Post Go-Live / Hypercare Support | Hypercare baseline if included | Issue replay cases |
| ND-15 | Change Management | Stakeholder comms/readiness if in baseline | None |
| ND-16 | Warranty Support | Separate row by default | Defect fix verification |

### Inventory MD Benchmark (cross-check only)

| Area | S | M | C | Formula |
|---|---:|---:|---:|---|
| FE by page/screen | 1.5 | 3.5 | 6 | `Σ(page count × MD benchmark)` |
| BE by API | 0.75 | 2 | 4 | `Σ(API count × MD benchmark)` |
| QA by test case | 0.1 | 0.2 | 0.4 | `Σ(test case count × MD/case)`; adjust with calibration evidence |
| Integration add-on | 2 | 5 | 10 | Per confirmed `INT-XX` cluster; avoid double-count with API rows |

## Validation Checklist

Gate, asking-tool, labelling, language, and scenario-separation checks follow [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน); calibration thresholds follow [calibration guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md). Baseline declaration, atomic subfeature, surface-tag carry-forward, names/refs, Cx judgment, QA basis, arithmetic, no-phase/PM, warranty, and cross-check/calibration are recorded in the Fixed Baseline/Scope table and the §5 Arithmetic Quality Gate; not repeated here. Step 04-specific checks:

- **Prerequisite and two-file output**: Step 03.3 WBS baseline consumed; both `step_04_sizing_estimate.md` and `step_04_sizing_review.md` exist, reference each other, and carry the same Approved Baseline Scope and a matching `Approval State`.
- **Step 05 handoff**: Estimation file Handoff includes raw MD by role, buckets, atomic basis, QA basis, assumptions, dependencies, and warranty.
