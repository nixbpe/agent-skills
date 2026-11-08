# orbit-build-wbs contract

Read the [action guide](../SKILL.md) and all its required principles before execution, including direct invocation. `output/` and input artifact paths resolve from the working project. Bundled guidance links resolve from this installed contract. Produce only this action's outputs and stop. Approval and continuous-mode authorization never bypass mandatory quality gates. The router alone may authorize the next action.

Read [role boundaries](../../principle-orbit-effort-accounting/references/roles.md) before assigning owners.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate final Step 03 WBS dev and non-dev tasks from approved backlog/inventory. |
| Input | `output/step_03_02_backlog_inventory.md` (controlling input), with Step 03.1 feature inventory and architecture/integration artifacts as supporting traceability only when referenced by Step 03.2. |
| Output | MUST create/update `output/step_03_03_wbs_baseline.md`. |
| Prerequisite | MUST read approved Step 03.2 backlog/inventory before producing WBS. |
| Missing prerequisite | MUST reject Step 03.3 execution and ask user to run/approve [orbit-build-backlog](../../orbit-build-backlog/references/contract.md) first. |
| Guidance | Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by the action guide](../SKILL.md#กฎที่ต้องอ่าน). |
| Next command | SHOULD hand off to [orbit-size-effort](../../orbit-size-effort/references/contract.md). |
| In scope | Dev WBS, non-dev WBS, DoD, milestones, exclusions/hand-offs, scope traceability, Step 04 handoff. |
| Out of scope | MUST NOT estimate MD/timeline, resource plan, risk range, or any commercial output. MUST NOT add unapproved features. |
| Coverage | Include dev and non-dev work: analysis, UX, FE, BE, integration, testing, DevOps, migration, training/docs, PM, change management. |
| Traceability | Every approved scope item, backlog item, screen/API, integration, and atomic subfeature from Step 03.2 maps to WBS or explicit `N/A — [reason]`; feature-level-only traceability is not enough for Step 04. Every `INT-XX` has at least one integration WBS/API mapping or Missing flag. Missing mapping is a warning, never hidden. |
| One owner per fact | The one-row-per-subfeature mapping (`## 5.1`) adds only BI-ID, WBS Ref, and WBS coverage. SG and SCR/API/INT refs stay in Step 03.2 `## 1`; outcome/acceptance/readiness stay in Step 03.1 `## 1.2`; deferred items stay in Step 01 §3.3 / Step 03.1 §0.3 (`OS-XX`). Do not copy them into Step 03.3. |
| Estimability | Work packages must be man-day estimable but MUST NOT include MD values or numeric sizing proxies such as days, points, t-shirt size, or capacity percentage. |
| WBS domains and numbering | SG1 uses `1.X.XX` with domains `1.1 Analysis`, `1.2 UX`, `1.3 FE`, `1.4 BE`, `1.5 Integration`, `1.6 Testing`, `1.7 DevOps`, `1.8 Migration`, `1.9 Training/Docs`, `1.10 PM`, `1.11 Change Mgmt`; SG2 mirrors the same domain numbers as `2.1`-`2.11` using `2.X.XX`. Copy baseline mode unchanged from prior steps and tag SG2, cap, MVP, scope-cut, or core-only views shown for scenario as `Scenario-only` unless explicit `re-baseline` is logged. |
| DoD and milestones | The Default DoD and Milestones below apply unless the TOR or an approved decision changes them; the artifact records deviations only. Milestones are sequence/checkpoint outputs, not duration or timeline estimates. |
| Stable IDs | Keep `WBS ID`, `BI-XX`, `SCR-XX`, `API-XX`, `INT-XX`, `FN-XX` stable for downstream agents. |

## Mapping Rules

Confirm before execution only high-impact blockers: approved Step 03.2 artifact, unchanged baseline mode, missing integration coverage, screen/API count flags, and WBS grouping assumptions. Mapping decisions:

| Condition | Decision |
|---|---|
| BI/SCR/API has delivery work | Map to WBS in the correct domain. |
| Atomic subfeature has delivery work | Add/verify one row in `Subfeature-to-WBS Mapping for Step 04` with WBS refs across analysis/UX/FE/BE/INT/test as applicable. |
| Atomic subfeature has acceptance/readiness blocker | Carry blocker into mapping, open questions, and Step 04 handoff; do not mark semantic coverage complete silently. |
| Work is cross-cutting/non-dev | Map to analysis/testing/DevOps/migration/docs/PM/change WBS. |
| Item belongs to SG2 | Use `2.X.XX`; do not mix with SG1 baseline silently. If shown for scenario only, tag `Scenario-only` and do not present as committed baseline. |
| Integration coverage missing | Flag in traceability and Step 04 handoff. |
| WBS not estimable | Split into smaller work packages. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with approved baseline/defaults.` |

## Default DoD and Milestones

| Area | Default DoD |
|---|---|
| Analysis / Design | FS, UX flow, API contract, and data model reviewed and signed off by BA/SA and Product Owner. |
| Development | Code merged with peer review, unit tests pass, deployed to SIT, no open Critical/High defects in scope. |
| Testing | SIT and UAT cases executed, Critical/High defects closed, UAT sign-off recorded. |
| DevOps / Docs | Environments provisioned via pipeline, release notes, runbook, and user/admin guides delivered. |

Milestone sequence: M0 Kickoff → M1 Scope Freeze → M2 Design → M3 Dev → M4 SIT → M5 UAT → M6 Go-Live → M7 Hypercare End → M8 Warranty End.

## Execution Flow

1. Read approved `output/step_03_02_backlog_inventory.md`; reject execution if missing. Resolve the blockers listed under Mapping Rules or state the no-blocking sentence.
2. Carry forward the selected feature grouping and blockers from Step 03.2 into `Backlog / Inventory Consumed`; cite deferred items by `OS-XX` only.
3. Build dev and non-dev WBS by domain with SG numbering; split any package that is not estimable.
4. Record DoD and milestone deviations from the defaults (or `Default applies`); exclusions/hand-offs for Training, Hypercare/Warranty, Hardware/License, Change Management plus TOR-specific items; and cite deferred `OS-XX` items as having no WBS.
5. Complete scope traceability and the one-row-per-subfeature mapping; flag missing INT coverage and blockers in traceability and Step 04 handoff.
6. Ask up to 5 highest-impact stakeholder-answerable open items with finite choices in one gate using the asking tool or chat fallback, then update WBS mappings, exclusions/hand-offs, Summary, and Handoff before publishing.
7. Fill Step Summary, Handoff Note - Step 04 (WBS IDs by SG, INT coverage, non-dev activities), and Internal Review.
8. Stop at the embedded Post-step Review Gate and stop; a subsequent action requires separate router authorization.

## Output Contract

Create/update `output/step_03_03_wbs_baseline.md` using this compact schema.

```markdown
# Step 03.3 - WBS Baseline: [PROJECT_NAME]

**Source**: `output/step_03_02_backlog_inventory.md` [approved revision] (controlling) + supporting refs from Step 03.1/architecture only when referenced by Step 03.2
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approved Baseline Scope**: SG1-only / SG1+SG2 / TBD
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [บันทึกผู้อนุมัติ/วันที่หรือ workflow authorization ตามหลักการ explicit approval ที่โหลดจาก action guide]

## Step Summary

- WBS count: [N] total; SG1=[N], SG2=[N].
- Coverage: scope/backlog/screens/APIs/INT status [summary].
- Atomic subfeature WBS coverage: [Complete/Partial/Missing]; missing=[subfeature list/N/A].
- Blockers carried: [ชื่อประเด็นจาก Step 03.2 §1 หรือ N/A; IDs อยู่ Open Questions].
- Deferred/not-doing items: [ชื่อกลุ่มงาน/N/A; refs อยู่ §4]; no WBS.
- Non-dev included: [analysis/testing/devops/migration/docs/PM/change status].

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 03.3 WBS Baseline**

Please review:
- Key outputs: WBS, DoD/milestone deviations, exclusions/hand-offs, traceability, Step 04 handoff.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Scope / MD / Timeline / Risk / Scenario.

Reply options:
- `approve Step 03.3` = lock WBS baseline and hand off to Step 04 sizing without executing it.
- `revise Step 03.3: ...` = update WBS before proceeding.

## ภาคผนวก

## Backlog / Inventory Consumed

Backlog=[N BI]; Screens=[N]; APIs=[N]; INT coverage=[X/Y]; Approved Baseline Scope=[SG1-only/SG1+SG2/TBD]; Open gaps=[list/N/A].

| Carry-forward Item | Value | Note |
|---|---|---|
| Feature grouping basis | [selected grouping from Step 03.1 via Step 03.2 or N/A] | Preserve selected boundaries; do not use rejected alternatives. |
| Deferred/not-doing items | [OS-XX list or N/A] | Owned by Step 01 §3.3 + Step 03.1 §0.3; no WBS unless re-baselined. |
| Acceptance/readiness blockers | [N] | Carry to subfeature mapping, open questions, and Step 04 handoff. |

## 1. WBS

Keep scenario-only AFN/SG2 packages separate and labelled. Approval of this artifact does not promote unresolved scope into the baseline. PM WBS packages are sized in Step 05, not Step 04. Every non-PM package, including approved DE/DBA or specialist work, must have a Step 04 sizing owner.

### 1.1 Feature Work Packages

Describe each per-feature domain package once, then list the WBS IDs per feature in a matrix. Screen/API content per package comes from Step 03.2 `## 1` through the BI-ID mapping in `## 5.1`. Shared screen/API implementation has one owning WBS package; dependent subfeatures reference it rather than recreating it.

| Domain | Description | Deliverable | Owner Role | Dependency |
|---|---|---|---|---|
| 1.1 Analysis & FS | [template description] | [deliverable] | BA/SA | [dep] |
| 1.2 UX/UI | [template description] | [deliverable] | UX | [dep] |
| 1.3 FE | [template description] | [deliverable] | FE | [dep] |
| 1.4 BE | [template description] | [deliverable] | BE | [dep] |
| 1.6 Test | [template description] | [deliverable] | QA | [dep] |

| FN | Feature | Surface | SG1 Subfeatures | 1.1 Analysis & FS | 1.2 UX/UI | 1.3 FE | 1.4 BE | 1.6 Test | Scope Ref |
|---|---|---|---:|---|---|---|---|---|---|
| FN-XX | [feature name] | SUR-XX | [N] | 1.1.XX | 1.2.XX / N/A — no UI | 1.3.XX / N/A — no UI | 1.4.XX / N/A — no BE | 1.6.XX | IS-XX |

### 1.2 Integration, Non-dev, PM and SG2 Work Packages

| WBS ID | Work Package | Description | Deliverable | Owner Role | Dependency | Scope / Backlog Ref |
|---|---|---|---|---|---|---|
| 1.5.01 | [Integration / non-dev / PM / SG2 WP] | [description] | [deliverable] | [role] | [dep/N/A] | INT/ND/IS refs |

## 2. Definition of Done

Default DoD applies (see command). Deviations: [area + changed criterion + TOR/decision ref, or `None`].

## 3. Milestones

Default milestone sequence M0-M8 applies (see command). Deviations: [added/removed checkpoint + reason, or `None`]. No dates or durations in Step 03.3.

## 4. Exclusions & Hand-offs

| Item | Status / Owner | Note |
|---|---|---|
| Training | [In/Out/Hand-off] | [NOTE] |
| Hypercare / Warranty | [In/Out/Hand-off] | [NOTE; if In, map hypercare and warranty separately to WBS and count each effort once in Step 04 support rows] |
| Hardware / License | [In/Out/Hand-off] | [NOTE] |
| Change Management | [In/Out/Hand-off] | [NOTE] |
| Deferred functional items | Out (no WBS) | `OS-XX` list from Step 01 §3.3 / Step 03.1 §0.3, or N/A |

## 5. Scope Traceability Check

List Scope (`IS-XX`) and `INT-XX` rows only. Do not list SCR/API rows here; prove them with one coverage line computed from `## 5.1`.

| Ref Type | Ref ID | WBS ID(s) | Status | Note |
|---|---|---|---|---|
| Scope/INT | [REF] | [WBS IDs] | Covered/Missing/N/A | [NOTE; `N/A — [reason]` when not mapped] |

Screen/API coverage: [N]/[N] SCR and [N]/[N] API referenced by Step 03.2 `## 1` BI rows whose `## 5.1` row has a WBS Ref.

## 5.1 Subfeature-to-WBS Mapping for Step 04

This table is the primary Step 04 WBS source. It must have one row per atomic subfeature from Step 03.2. Do not use grouped feature rows as a substitute. SG และ SCR/API/INT refs อยู่ที่ Step 03.2 §1 (ผ่าน BI-ID); outcome/acceptance/readiness อยู่ที่ Step 03.1 §1.2.

| Subfeature | BI-ID | WBS Ref | WBS Coverage Status | Note |
|---|---|---|---|---|
| FN-XX.NN [subfeature name] | BI-XX | 1.X.XX, 1.X.XX / N/A — [reason] | Complete/Partial/Missing/N/A | [gap; note blocker ID when an inventory default was applied] |

## Open Questions / Assumptions

| ID | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [QUESTION_OR_ASSUMPTION] | [WHY + IMPACT] | [OWNER] | Before Step 04 |

## Handoff Note - Step 04

- WBS IDs by SG: [SG1 list], [SG2 list].
- INT IDs + coverage: [INT list/status].
- Non-dev activities: [list].
- Screen/API/INT refs and counts: Step 03.2 `## 1` and `## 5` (not repeated here).
- WBS refs source: use `## 5.1 Subfeature-to-WBS Mapping for Step 04`; every Step 04 atomic sizing row must be able to pull WBS refs from this table.
- Outcome/acceptance source: Step 03.1 `## 1.2 Subfeature List by Feature`.
- Readiness/blocker source: Step 03.1 `## 1.2` `Sizing Readiness` and Step 03.2 `## 1` `Blocker ID`.
- Deferred/not-doing source: `OS-XX` in Step 01 §3.3 / Step 03.1 §0.3; do not include these in Step 04 baseline sizing unless re-baselined.

## Internal Review

Render per [reviewer-first guidance](../../principle-orbit-reviewer-first/SKILL.md).

| Check | Result | Note |
|---|---|---|
| Step 03.2 consumed | Pass/Warning/Fail | [NOTE] |
| Dev + non-dev WBS complete | Pass/Warning/Fail | [NOTE] |
| WBS packages are estimable | Pass/Warning/Fail | No MD values included. |
| No numeric sizing proxies | Pass/Warning/Fail | No days, points, t-shirt size, capacity %, or pseudo-estimate appears in WBS descriptions. |
| Traceability complete | Pass/Warning/Fail | [NOTE] |
| Atomic subfeature WBS mapping complete | Pass/Warning/Fail | Every subfeature from Step 03.2 has WBS refs or explicit `N/A — [reason]`. |
| Subfeature refs resolve | Pass/Warning/Fail | Every `## 5.1` BI-ID resolves to Step 03.2 `## 1`; no Step 03.1/03.2 fields are copied. |
| Deferred items excluded | Pass/Warning/Fail/N/A | `OS-XX` items are listed in `## 4` as Out and have no WBS rows. |
| INT coverage carried forward | Pass/Warning/Fail | [NOTE] |
| Step 04 handoff ready | Pass/Warning/Fail | [NOTE] |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope, Mapping Rules, and Output Contract. Verify unique WBS IDs, resolved refs, SG numbering, and every atomic subfeature's WBS mapping. Keep scenario/deferred treatment unchanged.
