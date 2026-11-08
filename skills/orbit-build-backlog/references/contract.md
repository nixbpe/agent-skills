# orbit-build-backlog contract

Read the [action guide](../SKILL.md) and all its required principles before execution, including direct invocation. `output/` and input artifact paths resolve from the working project. Bundled guidance links resolve from this installed contract. Produce only this action's outputs and stop. Approval and continuous-mode authorization never bypass mandatory quality gates. The router alone may authorize the next action.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST expand Step 03.1 features into backlog items, UI pages with in-page activity, optional sitemap/navigation grouping, and backend API/integration inventory. |
| Input | MUST use approved `output/step_03_01_feature_inventory.md` as the controlling source of feature, subfeature, scope, architecture, and integration context; do not derive new baseline scope, feature boundaries, or integration context from Step 01/02/TOR except to verify traceability when cited by Step 03.1. |
| Output | MUST create/update `output/step_03_02_backlog_inventory.md`. |
| Prerequisite | MUST read approved `output/step_03_01_feature_inventory.md` before producing backlog/inventory. |
| Missing prerequisite | MUST reject Step 03.2 execution and ask user to run/approve Step 03.1 first. |
| Guidance | Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน). Surface IDs come from Step 02 §1.1 Surface Map. |
| Next command | SHOULD hand off to [orbit-build-wbs](../../orbit-build-wbs/references/contract.md). |
| In scope | `BI-XX` with subfeature coverage, UI Page Inventory including in-page activities, optional sitemap/navigation grouping, API inventory, integration coverage, count summary, complexity rationale, source data assumptions. |
| Out of scope | MUST NOT create WBS tasks, estimate MD/timeline, resource plan, risk range, or any commercial output; MUST NOT invent unapproved features. |
| Traceability | Every backlog item traces to `FN-XX` and a scope ref. Every backlog, UI, API, and integration mapping carries an atomic `Subfeature Ref` / `Subfeature Name` from Step 03.1; never collapse mappings back to feature level. |
| Stable IDs | Keep `BI-XX`, `SCR-XX`, `API-XX`, `INT-XX`, `FN-XX` stable. |
| Surface tag | Tag every `SCR-XX` and `API-XX` with one or more `SUR-XX` from Step 02 §1.1 Surface Map. Screens belong to the surface that hosts them; APIs belong to the surface(s) that call them (multi-surface when shared). Use the declared `Backend / Integration` surface ID for system-to-system APIs and scheduled jobs; do not assume SUR-04 exists. |
| One owner per fact | Outcome and acceptance text lives only in Step 03.1 `## 1.2`. Step 03.2 rows carry IDs and refs; do not copy outcome, acceptance, or user-story text. API rows keep a short `Stakeholder-Readable Detail` because it describes the operation, which Step 03.1 does not. |
| Coverage matrix | `## 1. Backlog & Subfeature Coverage Matrix` has exactly one row per atomic `FN-XX.NN` / `AFN-XX.NN` (one `BI-XX` each), carrying blocker status plus screen/API/INT refs. Behavior type, actor, and sizing readiness stay in Step 03.1 `## 1.2`. `Inventory Coverage` = `Partial` when a default was applied for a subfeature whose Step 03.1 readiness is `Needs clarification`; do not mark it `Complete` without a resolved assumption. |
| UI inventory | Each `SCR-XX` is one semantic page, screen, work surface, or independently operated modal (split dimension views, lifecycle states, approval worklists, audit/config and governance pages only when they require distinct layouts or behavior; do not count every status, filter value, or responsive variant as a new screen, and never count a menu or capability group as one screen) with in-page activities used for complexity. The sitemap (`## 2.1`) is optional: include it when the TOR or reviewer needs a menu view; when included it lists every `SCR-XX` exactly once and is an information-architecture assumption, not final UX/wireframe/approved menu. |
| API inventory | Cover `CRUD / BIZ / INTG / BATCH / FILE / RT` types; map INTG APIs to `INT-XX`; every `INT-XX` has coverage status Covered/Missing/N/A (coverage may come from any API type carrying an `INT Ref`). |
| 5W1H | Not produced in Step 03.2; every cell would repeat an inventory column. The workbook `UI API Inventory` sheet carries a `5W1H Summary` per row (see [workbook-only 5W1H contract](../../orbit-prepare-workbook/references/contract.md)). |
| Enterprise candidate resolution | Consume the Step 03.1 `## 0.4` resolution; do not re-table it. Items resolved to `FN-XX`/`AFN-XX` appear through `## 1`; `OQ-XX` items stay in Open Questions; `OS-XX` and moved-out items create no BI/SCR/API rows. Unsourced common capabilities stay `Needs confirmation`; never convert them into baseline backlog silently. |
| Boundary preservation | Keep authentication provider, login/session, authorization/role source, function permission, and data authorization separate in coverage/API/INT mapping; preserve integration direction, read/write/writeback, trigger/frequency, initial load/setup, failure/retry, owner, and reconciliation assumptions from Step 03.1. |
| Source data assumptions | Carry Step 03.1 table/record assumptions into Countable Summary and open assumptions as estimation-only; keep separate from confirmed TOR facts. |
| Complexity rationale | Add concise rationale for any `C` label not obvious from activity/API wording. |
| Counts | Counts are inventory counts only, never MD/effort. |
| Baseline mode | Copy Approved Baseline Scope from Step 03.1 unchanged and keep deferred/not-doing items (`OS-XX` in Step 01 §3.3 and Step 03.1 §0.3) out of BI/SCR/API rows; only an explicit user `re-baseline` changes either. |

## Question Triggers

| Condition | Action |
|---|---|
| Feature has user interaction | Create `BI-XX` and one `SCR-XX` per distinct page/screen/state/modal; set Cx from the action rules. |
| Every `SCR-XX` (when the sitemap is included) | Add it to the sitemap group of its menu (note modal/error/state pages and SG2 screens in the group's Notes). |
| Feature needs a backend operation | Create an API row with type and Cx. |
| Feature maps to `INT-XX` | Create/mark the INTG API and coverage status. |
| API supports multiple feature flows or subfeatures | Reuse one API row, note `Multi-consumer` in Stakeholder-Readable Detail, list all `BI Ref` / `Subfeature Ref` values, and describe the shared outcome instead of inflating the count. |
| Step 03.1 subfeature has `Needs clarification` readiness | Keep it in the coverage matrix, set its Blocker ID, and do not mark coverage complete. |
| Subfeature has no direct screen/API/INT | Keep it in the coverage matrix and mark the missing dimension N/A with reason instead of dropping it. |
| Step 03.1 enterprise item resolved to `OQ-XX` / `OS-XX` / moved-out | Keep as open question / trace by `OS-XX` / carry into handoff notes only. Create BI/SCR/API rows only for items resolved to `FN-XX`/`AFN-XX`. |
| Source data assumptions exist | Add dataset/volume metrics to Countable Summary and open assumption rows for confirmation. |
| API or screen is unclear | Mark `Assumption:` or Open Question; do not silently omit. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with approved baseline/defaults.` |

## Coding Reference

| Field | Values |
|---|---|
| Screen types | `LIST / FORM-S / FORM-M / DETAIL / DASH / REPORT / CANVAS / MODAL` |
| Screen Cx | `S=≤2 actions`; `M=3-5 actions/conditional/upload/filter`; `C=6+ actions/realtime/drag-drop/state machine` |
| Reuse | `1.0=unique`, `0.3=variant`, `0=exact reuse` |
| API types | `CRUD / BIZ / INTG(ref INT-XX) / BATCH / FILE / RT(WS/SSE)` |
| API Cx | `S=single entity`; `M=multi-entity/1 ext/validation`; `C=multi-system/async+callback` |
| Integration relationship | `Direct` = the subfeature/API itself exchanges data/events with an external system; `Shared` = relies on an integration owned by another module/API; `No external integration` = application-internal only |
| Screen:API ratio | Normal 1:2-1:4; flag if <1:1 or >1:5 |

## Execution Flow

1. Read approved `output/step_03_01_feature_inventory.md`; if missing or not approved, stop and ask to run/approve Step 03.1. Confirm unchanged baseline mode, feature boundary questions, and integration list readiness. Consume feature framing, selected grouping rationale, deferred/not-doing items, atomic subfeatures, and data sync assumptions before writing rows.
2. Confirm every Step 03.1 `## 0.4` item has a resolution; items resolved to `FN-XX`/`AFN-XX` must reach `## 1`.
3. Derive the Backlog & Subfeature Coverage Matrix (`## 1`, one `BI-XX` per atomic subfeature).
4. Build UI Page Inventory and the optional Sitemap (`## 2` to `## 2.1`); Backend API & Integration Inventory and the Integration Coverage line (`## 3` to `## 4`); and Countable Summary with complexity rationale (`## 5`).
5. Traceability completeness gate: every Step 03.1 confirmed feature and atomic subfeature appears in the Backlog & Coverage Matrix with UI/API/INT refs or explicit N/A; unresolved assumptions stay visible as Open Questions.
6. Ask up to 5 highest-impact stakeholder-answerable Open Questions / Assumptions with finite choices in one gate using the asking tool or chat fallback, then update BI/SCR/API/INT rows and counts.
7. Sync sweep after any screen or API addition/removal/split/merge: Backlog & Coverage Matrix refs, UI Page Inventory, Sitemap (if included), Backend API Inventory, Integration Coverage, Countable Summary, Screen:API ratio, Step Summary, Handoff, and Internal Review use one consistent number set.
8. Publish the artifact with the embedded Post-step Review Gate and stop; only the router may authorize a subsequent action.

## Output Contract

Create/update `output/step_03_02_backlog_inventory.md` using this compact schema.

```markdown
# Step 03.2 - Backlog & Inventory: [PROJECT_NAME]

**Source**: `output/step_03_01_feature_inventory.md` [approved revision]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approved Baseline Scope**: [SG1-only/SG1+SG2/TBD; copy unchanged from Step 03.1]
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [บันทึกผู้อนุมัติ/วันที่หรือ workflow authorization ตามหลักการ explicit approval ที่โหลดจาก action guide]

## Step Summary

- Backlog items: [N]; UI screens: [N]; APIs: [N].
- Feature framing: selected grouping=[basis/N/A]; deferred/not-doing items=[ชื่อกลุ่มงาน/N/A; refs อยู่ Feature Baseline Consumed] (no BI/SCR/API rows).
- Integration coverage: [X/Y] covered; missing=[ชื่อระบบ/N/A; refs อยู่ §4].
- Subfeature coverage: [Complete/Partial/Missing]; every atomic subfeature has screen/API/INT refs or explicit N/A.
- Screen complexity split: S=[N], M=[N], C=[N]; API complexity split: S=[N], M=[N], C=[N].
- Screen:API ratio: [ratio] with status [Normal/Flag].

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 03.2 Backlog & Inventory**

Please review:
- Key outputs: backlog & subfeature coverage, UI pages/in-page activities, sitemap (if included), backend APIs, integration coverage, count summary.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Scope / MD / Timeline / Risk / Scenario.

Reply options:
- `approve Step 03.2` = lock backlog/inventory and hand off to Step 03.3 without executing it.
- `revise Step 03.2: ...` = update backlog/inventory before proceeding.

## ภาคผนวก

## Feature Baseline Consumed

No blocking confirmations; proceeding with approved baseline/defaults. [Or list blocking confirmations if any]

| Baseline Item | Value | Note |
|---|---:|---|
| Confirmed/derived functional features | [N] | [FN list] |
| Assumption-backed additions | [N] | [AFN list or N/A] |
| Approved Baseline Scope | [SG1-only/SG1+SG2/TBD] | Do not re-baseline silently |
| Integration refs | [N] | [INT list] |
| Data sync assumption | [table/record assumptions or N/A] | Assumption for estimation only; pending source owner catalog |
| Feature grouping basis | [selected grouping from Step 03.1 §0.2 or N/A] | Use this to avoid splitting backlog across rejected feature boundaries. |
| Deferred/not-doing items | [OS-XX list or N/A] | Owned by Step 01 §3.3 + Step 03.1 §0.3; no BI/SCR/API rows unless re-baselined. |

## 1. Backlog & Subfeature Coverage Matrix

หนึ่งแถวต่อ atomic subfeature (1 BI ต่อ subfeature). Outcome, acceptance, behavior type, actor และ sizing readiness อยู่ที่ Step 03.1 §1.2; ตารางนี้เก็บเฉพาะ ref, blocker และ coverage สำหรับ Step 03.3/04

| BI-ID | Subfeature | SG | Type | Priority | Blocker ID | Screen Ref | API Ref | Integration Relationship | INT Ref | Scope Ref | Inventory Coverage | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BI-01 | FN-XX.NN [subfeature name] | SG1/SG2 | Feature/Enabler | Must/Should/Could | [OQ-XX/ASM-XX/N/A] | SCR-XX/N/A — [reason] | API-XX/N/A — [reason] | Direct/Shared/No external integration | INT-XX/N/A — [reason] | IS-XX | Complete/Partial/Missing | [gap/assumption] |

## 2. UI Page Inventory

| SCR-ID | Module | Surface | Page / Screen | Type | In-page Activities | Cx | Reuse | BI Ref | FN Ref | Subfeature Ref | Scope Ref |
|---|---|---|---|---|---|---|---:|---|---|---|---|
| SCR-01 | [MODULE] | [SUR-XX from Step 02 §1.1] | [PAGE] | [TYPE] | [actions/activity list] | S/M/C | 1.0/0.3/0 | BI-XX | FN-XX | FN-XX.NN | IS-XX |

## 2.1 Sitemap / Navigation Structure

Optional. Write `N/A — menu view not required` when not needed. Sitemap นี้เป็น **information architecture assumption** สำหรับจัดกลุ่ม UI inventory ให้เห็น menu/navigation และใช้ประกอบ Step 03.3 WBS เท่านั้น ไม่ใช่ final UX design หรือ wireframe. ทุก `SCR-XX` อยู่ในตารางนี้ครั้งเดียว

| Menu Level 1 | Menu Level 2 / Page Group | Screen Refs | Primary User | Notes |
|---|---|---|---|---|
| [MENU] | [PAGE_GROUP] | SCR-XX, SCR-YY | [ROLE list] | [modal/state: SCR list; SG2: SCR list; or Assumption IA] |

## 3. Backend API & Integration Inventory

| API-ID | Module | Surface | API / Operation | Stakeholder-Readable Detail | Method | Type | Cx | Integration Relationship | INT Ref | BI Ref | FN Ref | Subfeature Ref | Scope Ref |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API-01 | [MODULE] | [SUR-XX — which surface(s) consume this API] | [OPERATION] | [stakeholder-readable detail describing system behavior, data, and integration/use] | GET/POST/etc. | CRUD/BIZ/INTG/BATCH/FILE/RT | S/M/C | Direct/Shared/No external integration | INT-XX/N/A — [reason] | BI-XX | FN-XX | FN-XX.NN | IS-XX |

## 4. Integration Coverage

One line computed from the `INT Ref` column in `## 3` (any API type counts): `INT-01=Covered (API-XX, API-YY); INT-02=Missing — [reason]; INT-03=N/A — [reason]`.

## 5. Countable Summary

Show the approved baseline and scenario-only counts separately, including shared screens/APIs once. Copy headline counts to Step Summary with this section as their calculation source. A shared artifact is baseline if at least one approved baseline subfeature needs it; only incremental optional work belongs to SG2/scenario. Exact reuse must reference its canonical SCR-ID; it avoids duplicate FE sizing but does not remove required integration or test work. API reuse is not independently discounted without an approved sizing rationale.

| Metric | Value | Note |
|---|---:|---|
| Total UI Screens | [N] | S=[N], M=[N], C=[N] |
| Weighted Screen Equivalent | [N] | Σ(screen reuse factor); may be fractional, not a unique-screen count |
| Total APIs | [N] | S=[N], M=[N], C=[N] |
| Total INTG APIs | [N] | API IDs; additional integration-linked APIs may use BATCH/FILE/BIZ/CRUD types with INT refs |
| Integration Coverage | [X/Y] | covered integration refs |
| Screen:API Ratio | [1:N or N/A — no UI] | API count ÷ physical screen count for the same scope; use N/A for non-UI systems |
| Source Data Datasets | [N or N/A] | Assumption for estimation only if applicable |
| Source Data Volume | [N or N/A] | Assumption for estimation only if applicable |

### Complexity Rationale for C-labelled Inventory

| Area | C-labelled Items | Rationale |
|---|---|---|
| UI Screens | [SCR list] | [Why C is justified under screen Cx rules] |
| APIs | [API list] | [Why C is justified under API Cx rules] |

## Open Questions / Assumptions

| ID | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [QUESTION_OR_ASSUMPTION] | [WHY + IMPACT] | [OWNER] | Before Step 03.3 |

## Handoff Note - Step 03.3

- Coverage source: `## 1` (one `BI-XX` per subfeature with SCR/API/INT refs and Blocker ID); counts in `## 5`.
- Approved Baseline Scope: [SG1-only/SG1+SG2/TBD; copy unchanged from Step 03.1].
- Coverage gaps and blockers: [INT missing list, Blocker IDs, or N/A].
- Scope caution: deferred items `OS-XX` get no WBS unless re-baselined; [assumption-backed features, source data volumes, discovery items, or N/A].

## Internal Review

Render per [reviewer-first guidance](../../principle-orbit-reviewer-first/SKILL.md).

| Check | Result | Note |
|---|---|---|
| Step 03.1 features consumed | Pass/Warning/Fail | [NOTE] |
| Feature framing carried forward | Pass/Warning/Fail/N/A | Selected grouping and boundary assumptions from Step 03.1 are reflected or marked N/A. |
| BI items trace to FN/scope | Pass/Warning/Fail | [NOTE] |
| Atomic subfeature coverage complete | Pass/Warning/Fail | Every Step 03.1 subfeature appears exactly once in the coverage matrix. |
| Blockers preserved | Pass/Warning/Fail | Every Step 03.1 `Needs clarification` subfeature has a Blocker ID in `## 1`; acceptance and readiness stay in Step 03.1 §1.2. |
| UI pages include activities/Cx/reuse | Pass/Warning/Fail | [NOTE: include sitemap coverage if the sitemap is included] |
| APIs include type/Cx/INT refs | Pass/Warning/Fail | [NOTE] |
| Integration coverage complete | Pass/Warning/Fail | [NOTE] |
| Count semantics | Pass/Warning/Fail | Counts are inventory only; no MD/effort/cost/timeline. |
| Deferred items excluded | Pass/Warning/Fail/N/A | `OS-XX` items from Step 01 §3.3 / Step 03.1 §0.3 have no BI/SCR/API rows unless re-baselined. |
| SG immutability | Pass/Warning/Fail | Approved Baseline Scope copied from Step 03.1 unless re-baseline logged. |
| Step 03.3 handoff ready | Pass/Warning/Fail | [NOTE] |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope, Coding Reference, and Output Contract. Verify unique BI/SCR/API IDs, resolved refs, exact atomic coverage, and the count sync sweep. Preserve the approved baseline mode and source N/A reasons.
