# orbit-inventory-features contract

Read the [action guide](../SKILL.md) and all its required principles before execution, including direct invocation. `output/` and input artifact paths resolve from the working project. Bundled guidance links resolve from this installed contract. Produce only this action's outputs and stop. Approval and continuous-mode authorization never bypass mandatory quality gates. The router alone may authorize the next action.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate the canonical functional feature/module/subfeature inventory for Step 03 before backlog, UI/API inventory, and WBS. |
| Input | MUST use approved `output/step_01_intake_scope.md` and approved `output/step_02_architecture_constraints.md`; TOR/RFP may be consulted only for traceability when referenced by those outputs. |
| Output | MUST create/update `output/step_03_01_feature_inventory.md`. |
| Prerequisite | MUST read both Step 01 and Step 02 outputs before producing the Step 03.1 feature inventory. |
| Missing prerequisite | MUST reject Step 03.1 execution and ask user to run/approve Step 01 and Step 02 first. |
| Guidance | Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน). Surface IDs come from Step 02 §1.1 Surface Map. |
| Next command | SHOULD hand off to [orbit-build-backlog](../../orbit-build-backlog/references/contract.md). |
| In scope | Feature/module taxonomy, stakeholder-readable feature detail, subfeature decomposition, SG1/SG2 grouping basis, scope refs, INT refs, data sync assumptions, open feature assumptions. |
| Out of scope | MUST NOT create UI/API inventory, WBS, MD/timeline, resource plan, risk range, or any commercial output; MUST NOT invent scope, screens, or APIs. |
| Traceability | Every feature traces to a scope ref (`IS-XX`/approved artifact) or is labelled `Assumption:`; every known integration dependency references `INT-XX` or is marked N/A with reason. |
| Stable IDs | Assign stable `FN-XX` IDs and module names reused by later commands; keep `FN-XX`, `AFN-XX`, `IS-XX`, `IS-UXX`, `OS-XX`, `INT-XX`, `OQ-XX` stable. |
| Surface tag | Tag every `FN-XX` / `AFN-XX` with one or more `SUR-XX` from Step 02 §1.1 Surface Map (comma-separated for multi-surface, e.g. `SUR-01, SUR-02`). No untagged feature row; use the declared `Backend / Integration` surface ID for non-UI work; do not assume its numeric ID is SUR-04. |
| Feature detail | Each feature row includes stakeholder-readable detail explaining actor/action/data/context/outcome enough for stakeholder review. |
| Subfeatures | Each feature row shows its subfeature count; the subfeatures themselves are listed once, in the dedicated `## 1.2 Subfeature List by Feature` table with stable `FN-XX.NN` / `AFN-XX.NN` IDs. Every subfeature is atomic (one estimable outcome; split `manage X/Y/Z`, `create/update/delete`, `view/export/audit` when they drive different UI/API/INT/WBS work) and carries behavior type, primary actor/system, plain-language outcome, integration relationship, INT ref, acceptance/done evidence, and sizing readiness without becoming UI/API inventory. `## 1.2` owns outcome and acceptance text; later steps reference it by subfeature ID. |
| Functional-only | Feature list contains system capabilities only; architecture/NFR/support/handover/DevOps/governance delivery work goes to the moved-out section. |
| Enterprise completeness | Run the Enterprise Functional Completeness Check as a discovery/confirmation lens, not automatic scope. Classify each common capability as `Confirmed` (only when traced to TOR/RFP or approved artifact), `Assumption - Needs confirmation` (default for unsourced items), `Candidate - Out of baseline`, `Moved to NFR/WBS/Risk`, or `N/A`, and resolve it here to `FN-XX` / `AFN-XX` / `OQ-XX` / `OS-XX` / moved-out / `N/A`. Step 03.2 consumes this resolution and does not re-table it. |
| Authn/Authz boundary | Check identity provider, login method, SSO/MFA, role/permission source, role mapping, provisioning/deprovisioning, and audit evidence; never merge authentication and authorization assumptions silently. If unclear, create open assumptions with owner/impact. |
| Integration boundary | For every integration candidate capture direction, read/write/writeback, trigger/frequency, initial load/setup, source of truth, owner, failure/retry behavior, and reconciliation. |
| Data sync | If a source data platform / data sync exists, include estimation-only logical table and record-volume assumptions with ASM refs, owner, impact, baseline treatment, fallback, and needed-by; never present them as confirmed TOR facts. |
| Deferred items | Step 01 §3.3 owns deferred/not-doing items. §0.3 lists only new functional items found here, continuing the `OS-XX` numbering. |
| Approved Baseline Scope | Set once in Step 03.1 (`SG1-only` / `SG1+SG2` / TBD); Step 03.2/03.3 copy it unchanged unless the user explicitly says `re-baseline`. |

## Question Triggers

| Condition | Action |
|---|---|
| Scope item is Must/Should/core baseline | Put in SG1 unless approved grouping says otherwise. |
| Scope item is Could/optional/uncertain | Put in SG2 or Needs Confirmation; do not baseline silently. |
| Feature has integration dependency | Add `INT-XX` ref and downstream note for backlog/API mapping. |
| Feature uses external/source data | Add dataset/table/record assumptions in the Data Sync Assumptions section, labelled estimation-only. |
| Common enterprise capability is plausible but unsourced | Mark `Assumption - Needs confirmation` with owner/impact and keep out of confirmed baseline. If it is technical/NFR/delivery/support rather than product behavior, move it to `## 2` moved-out instead of creating a feature. |
| Multiple valid feature groupings exist | Compare business-flow-centric vs capability-centric grouping, select one, and document rationale before the final inventory. |
| Feature boundary is unclear | Add an Open Question or `Assumption:` with owner/impact; Open Questions hold only feature-boundary blockers or assumptions. |
| Subfeature describes multiple outcomes | Split into separate atomic subfeatures before handing off to Step 03.2. |
| User answer confirms or rejects an `AFN-XX` / Open Question | Promote to confirmed `FN-XX` by allocating a new ID and recording AFN-to-FN and subfeature mappings, or change treatment to AFN/deferred/not-doing without renumbering existing IDs, then run the correction sweep in Execution Flow step 6. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with approved baseline/defaults.` |

Allowed values: Behavior Type=`User-facing / Admin-facing / System/Background / Audit/Status / Validation / Config / Export / Integration`; Integration Relationship=`Direct` (the subfeature itself exchanges data/events with an external system) / `Shared` (relies on an integration owned by another row/module) / `No external integration`; Sizing Readiness=`Ready / Needs clarification`.

## Execution Flow

1. Read approved `output/step_01_intake_scope.md` and `output/step_02_architecture_constraints.md`; if either is missing or not approved, stop and ask to run/approve it. Confirm Approved Baseline Scope and SG grouping rule.
2. Feature framing (`## 0`): map scope items to features, record the grouping decision when boundaries are ambiguous, and record any new deferred/not-doing items. Rejected alternatives stay scenario/context, never baseline changes.
3. Run the Enterprise Functional Completeness Check (`## 0.4`) including the authn/authz and integration boundary checks; carry unsourced items into Open Questions with owner/impact.
4. Write `FN-XX` / `AFN-XX` rows with surface tags, one atomic subfeature table per feature (`## 1.2`); move non-functional/delivery items to `## 2`; add Data Sync Assumptions when a source system is in scope.
5. Ask up to 3-5 highest-impact stakeholder-answerable Open Questions / Assumptions with finite choices in one asking-tool gate, then apply AFN promotion/demotion from the answers.
6. Correction sweep: after any feature, AFN, SG, subfeature, INT, or count change, update Feature Inventory, Assumption-backed Functional Additions, Subfeature List, Open Questions, Data Sync Assumptions, Step Summary, Handoff, and Internal Review. Leave no stale AFN rows, FN counts, subfeature IDs, or Summary/Handoff numbers.
7. Publish the artifact with the embedded Post-step Review Gate and stop; only the router may authorize a subsequent action.

## Enterprise discovery reference

Discovery prompts only. The output records project evidence and resolution for each area, not this generic list. These prompts do not add baseline scope.

| Capability Area | Discovery Prompts |
|---|---|
| User / Account Lifecycle | user provisioning, deactivation, profile, password reset, delegated admin |
| Authentication | SSO, [enterprise IdP / SSO provider], MFA, login callback, session behavior |
| Authorization / RBAC | role source, function permission, data authorization, role mapping |
| Admin / Configuration | lookup values, workflow rules, notification templates, holidays/SLA, parameters, feature toggles |
| Audit / Activity History | who changed what/when, approval trail, exportable audit report |
| Notification | [email/SMS/chat/messaging platform], recipient matrix, templates, escalation, reminders |
| Data Import / Export | initial load, recurring import, export format, field selection, drag-and-drop, template reuse |
| Reporting / Dashboard | report list, filters, drill-down, scheduled reports, visualization, KPI definitions |
| Search / Filter / Sort | search criteria, pagination, saved filters, favorite views |
| Workflow / Approval | approval levels, delegation, escalation, reject/rework, SLA, approval history |
| User-visible Error / Retry | validation messages, failed transaction report, retry/resubmit, reconciliation screen |
| File Handling | upload/download, preview, file type/size, virus scan expectation, storage retention |
| Localization / Accessibility / Browser | language, timezone, date/number format, accessibility, supported browsers/devices |

## Output Contract

Create/update `output/step_03_01_feature_inventory.md` using this compact schema.

```markdown
# Step 03.1 - Functional Feature Inventory: [PROJECT_NAME]

**Source**: `output/step_01_intake_scope.md` [approved revision] + `output/step_02_architecture_constraints.md` [approved revision]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approved Baseline Scope**: [SG1-only/SG1+SG2/TBD]
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [บันทึกผู้อนุมัติ/วันที่หรือ workflow authorization ตามหลักการ explicit approval ที่โหลดจาก action guide]

## Step Summary

- Functional feature count: [N] total; SG1=[N], SG2=[N], assumptions=[N].
- Feature framing: selected grouping=[business-flow/capability/mixed/N/A], new deferred items=[N] (§0.3).
- Modules: [module list].
- Integration-linked features: [ชื่อความสามารถและระบบที่เชื่อมต่อ; refs อยู่ §1].
- Data sync assumption: [source/table count/record count or N/A].

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 03.1 Functional Feature Inventory**

Please review:
- Key outputs: functional feature list, subfeature list, SG1/SG2 grouping, moved-out non-functional/delivery items, scope refs, integration refs, data sync assumptions if applicable.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Scope / MD / Timeline / Risk / Scenario.

Reply options:
- `approve Step 03.1` = lock feature inventory and hand off to Step 03.2 without executing it.
- `revise Step 03.1: ...` = update feature inventory before proceeding.

## ภาคผนวก

## Baseline Consumed

No blocking confirmations; proceeding with approved baseline/defaults. If blocking confirmations exist, stop before creating this artifact and ask the gate questions instead.

## 0. Feature Framing & Clustering

Use this section to converge approved scope into stable feature boundaries before assigning final `FN-XX` IDs. Do not invent new scope; label alternatives as scenario/context only unless re-baselined.

### 0.1 Scope-to-Feature Map

Scope item text อยู่ใน Step 01 §3; ตารางนี้แสดงเฉพาะการ map IS → FN

| Source Ref | Mapped Feature / Treatment |
|---|---|
| IS-01 | [→ FN-XX list / Moved out → `## 2`, later mapped to Step 04 `ND-XX` (reason) / ambiguity note] |

### 0.2 Grouping Decision

Write `N/A — feature boundaries are explicit in approved scope` unless boundaries are ambiguous. Otherwise, in one short paragraph: grouping selected (business-flow / capability / mixed), the alternative rejected and why, and the complexity driver that set the boundary. Rejected alternatives stay context only.

### 0.3 New Deferred Functional Items

Only functional items not already in Step 01 §3.3. Continue the `OS-XX` numbering; write `N/A — none beyond Step 01 §3.3` otherwise.

| ID | Item | Reason | Treatment | Change Trigger |
|---|---|---|---|---|
| OS-XX | [ITEM] | [WHY_NOT_IN_FINAL_FN_LIST] | Not Doing / Deferred / Assumed Existing / Scenario | [WHAT_REOPENS_SCOPE] |

### 0.4 Enterprise Functional Completeness Check

Check every area against `Enterprise discovery reference`. Keep all 13 area rows; record project evidence, status, resolution, and owner/impact instead of generic discovery prompts. Give a reason for each `N/A`. Confirm baseline scope only from the TOR/RFP or an approved artifact. If the source is unclear, use `Assumption - Needs confirmation` and carry owner/impact into Open Questions.

| Capability Area | Source / Evidence | Status | Resolution | Owner / Impact if Wrong |
| --- | --- | --- | --- | --- |
| User / Account Lifecycle | [TOR/RFP ref / approved artifact / N/A] | Confirmed / Assumption - Needs confirmation / Candidate - Out of baseline / Moved to NFR/WBS/Risk / N/A | [FN-XX/AFN-XX/OQ-XX/OS-XX/Moved-out/N/A] | [OWNER + impact] |
| Authentication | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Authorization / RBAC | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Admin / Configuration | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Audit / Activity History | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Notification | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Data Import / Export | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Reporting / Dashboard | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Search / Filter / Sort | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Workflow / Approval | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| User-visible Error / Retry | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| File Handling | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |
| Localization / Accessibility / Browser | [REF] | [STATUS] | [TREATMENT] | [OWNER + impact] |

## 1. Functional Feature Inventory

| FN-ID | Module | Surface | Functional Feature | รายละเอียดเพิ่มเติม | SG | Priority | Scope Ref | INT Ref | Subfeatures |
|---|---|---|---|---|---|---|---|---|---:|
| FN-01 | [MODULE] | [SUR-XX or comma-separated; from Step 02 §1.1 Surface Map] | [FEATURE] | [stakeholder-readable detail: who uses it, what data/process it covers, why, and outcome] | SG1/SG2 | Must/Should/Could | [IS-XX] | [INT-XX/N/A — reason] | [N] (§1.2) |

## 1.1 Assumption-backed Functional Additions

N/A — use this section only when additional functional assumptions are needed to close a known scope gap. Keep these separate from confirmed `FN-XX` rows. `AFN-XX` items are scenario/excluded from Step 04 baseline unless explicitly approved before sizing lock.

| AFN-ID | Surface | Functional Addition | รายละเอียดเพิ่มเติม | SG | Priority | Basis | INT Ref | Subfeatures |
|---|---|---|---|---|---|---|---|---|
| AFN-01 | [SUR-XX] | [ASSUMED_FUNCTIONAL_ADDITION] | [stakeholder-readable detail + explicit assumption basis] | SG2 | Should/Could | [IS-XX; assumption] | [INT-XX/N/A] | [N] (§1.2) |

## 1.2 Subfeature List by Feature

### FN-01 [Feature Name]

| Subfeature ID | Subfeature Name | Behavior Type | Primary Actor/System | Outcome Description | Done Evidence / Acceptance Condition | Integration Relationship | INT Ref | Basis | Sizing Readiness |
|---|---|---|---|---|---|---|---|---|---|
| FN-01.01 | [ATOMIC_SUBFEATURE] | User-facing/Admin-facing/System/Background/Audit/Status/Validation/Config/Export/Integration | [role/system] | [Thai plain-language outcome: who/system does what, with what data, for what result; no internal IDs] | [observable result / report / status / data change / approval evidence] | Direct/Shared/No external integration | INT-XX/N/A — [reason] | [IS-XX/Assumption] | Ready / Needs clarification |
| FN-01.02 | [ATOMIC_SUBFEATURE] | [type] | [role/system] | [Thai plain-language outcome; no internal IDs] | [acceptance evidence] | Direct/Shared/No external integration | INT-XX/N/A — [reason] | [IS-XX/Assumption] | Ready / Needs clarification |

Repeat one subfeature table for every `FN-XX` and `AFN-XX`. Every feature must have at least one subfeature. Subfeatures must be granular enough for Step 03.2 backlog/UI/API/INT derivation and Step 04 atomic sizing, but must not become UI/API inventory yet.

## 2. Non-functional / Architecture / Delivery Items Moved Out

| Moved Area | Items | Downstream Handling |
|---|---|---|
| Architecture / Platform | [[cloud/platform]/env/CI-CD/IaC/network/etc. if present] | Step 03.3 WBS / Step 04 non-dev / Step 05 resource plan |
| NFR / Reliability | [performance/availability/backup/retention/etc. if present] | Step 02 NFR / Step 03.3 WBS / Step 04 non-dev / Step 06 risk |
| Security / Compliance Controls | [TLS/encryption/scans/secrets/[privacy law / data protection requirement, e.g. PDPA/GDPR if applicable]/etc. if present] | Step 02 constraints / Step 03.3 WBS / Step 04 non-dev |
| QA / Governance | [SIT/UAT/CAB/release evidence/etc. if present] | Step 03.3 WBS / Step 04 non-dev |
| Support / Handover | [Hypercare/Warranty/KT/runbook/source handover/etc. if present] | Step 03.3 WBS / Step 04 support activities / Step 05 PM |

Items such as monitoring/observability, backup/recovery/DR, security scan, performance test, training, KT, cutover, hypercare, warranty, support operations/managed services, rate card, pricing, commercial terms, and contractual penalty/liquidated damages must not become product features unless the TOR/RFP explicitly requires user-facing application behavior. Otherwise, classify them as moved-out items for WBS/NFR/risk/commercial workflows.

## Open Questions / Assumptions

| ID | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [QUESTION_OR_ASSUMPTION] | [WHY + IMPACT] | [OWNER] | Before Step 03.2 |

## Data Sync Assumptions - [SOURCE_SYSTEM]

Use this section when data sync/import from a source system is in scope. Mark the section **Assumption for estimation** and explicitly state that table/record counts are not confirmed TOR facts until the source owner provides an interface catalog.

### Inbound Logical Tables / Datasets

| Dataset ID | Logical Table / Dataset | Purpose in [PROJECT_NAME] | Estimated Tables | Record Assumption | Basis / Impact if Wrong |
|---|---|---|---:|---:|---|
| DS-01 | [DATASET] | [functional use] | [N] | [record estimate/range] | [basis + impact on API/sizing/performance] |

### Volume Baseline for Estimation

| Volume Item | Assumption | Use in Downstream Step |
|---|---:|---|
| Recommended inbound logical table count | [N] logical tables/datasets | Step 03.2 API inventory and Step 04 integration sizing |
| Full initial load / full snapshot | [N] records | Data sync, validation, reconciliation, performance test, storage sizing |
| Daily incremental sync | [N] records/day | Scheduled sync, retry, monitoring, operational load |
| Base formula | [formula] | Update estimate when source owner confirms real dimensions/volume |
| Internal staging/control tables | [N] tables, not counted as inbound source tables | Sync status, retry, error log, audit log, reconciliation; count in app/WBS design, not source sync table count |

## Handoff Note - Step 03.2

- Feature IDs/modules: [FN list or table ref].
- Feature framing source: `## 0` for selected boundaries and enterprise-check resolution; deferred/not-doing items are Step 01 §3.3 plus §0.3 (`OS-XX`).
- Scope refs: [IS/IS-U list].
- Integration refs: [INT list].
- Approved Baseline Scope: [SG1-only/SG1+SG2/TBD].
- Subfeature source: use `## 1.2 Subfeature List by Feature` as the primary decomposition input.
- Step 04 assumption source: use each subfeature's `Behavior Type`, `Primary Actor/System`, `Outcome Description`, `Integration Relationship`, and `INT Ref`; keep IDs in ref columns only, not narrative assumption text.
- Data sync assumption source: use `Data Sync Assumptions - [SOURCE_SYSTEM]` for draft data/API inventory; do not treat table/record counts as confirmed until source owner provides interface catalog.

## Internal Review

Render per [reviewer-first guidance](../../principle-orbit-reviewer-first/SKILL.md).

| Check | Result | Note |
|---|---|---|
| Approved inputs consumed | Pass/Warning/Fail | [NOTE] |
| Feature framing completed | Pass/Warning/Fail/N/A | Scope-to-feature map complete; grouping decision recorded when boundaries are ambiguous; new deferred items numbered as `OS-XX`. |
| No new scope invented | Pass/Warning/Fail | [NOTE] |
| Functional-only feature list | Pass/Warning/Fail | [NOTE] |
| Stakeholder-readable detail answers 5W1H implicitly | Pass/Warning/Fail | [NOTE] |
| Subfeatures included | Pass/Warning/Fail | [NOTE] |
| Atomic subfeature metadata complete | Pass/Warning/Fail | Behavior type, actor/system, outcome, acceptance evidence, integration relationship, INT ref, basis, and sizing readiness present for every subfeature. |
| No grouped subfeatures | Pass/Warning/Fail | No slash/comma/range combined subfeatures remain. |
| Features trace to scope refs | Pass/Warning/Fail | [NOTE] |
| INT refs carried forward | Pass/Warning/Fail | [NOTE] |
| Data sync assumptions separated from confirmed scope | Pass/Warning/Fail/N/A | [NOTE] |
| Enterprise completeness checked | Pass/Warning/Fail | Common enterprise capabilities were classified and resolved without silently adding unsourced baseline scope. |
| Step 03.2 handoff ready | Pass/Warning/Fail | [NOTE] |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope and Output Contract. Verify unique FN/AFN/subfeature IDs, resolved refs, and the correction sweep before handoff. Enterprise-check resolution and atomic metadata are checked in `Internal Review`, not a second checklist.
