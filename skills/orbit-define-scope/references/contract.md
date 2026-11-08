# Step 01 intake and scope contract

Read [the action guide](../SKILL.md) and all its required principles before applying this contract, including direct invocation. User input and `output/` paths are relative to the working project. Bundled reference links are relative to this installed skill. Do not assign SG1/SG2 or add Approved Baseline Scope before Step 03.1.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate Step 01 Intake & Scope from TOR/RFP input and Step 00 confirmation baseline. |
| Input | TOR/RFP text, file, requirement notes, customer brief, and `output/step_00_confirmation_baseline.md`. |
| Output | MUST create/update `output/step_01_intake_scope.md` using the embedded schema below. |
| Prerequisite | MUST read approved `output/step_00_confirmation_baseline.md` before producing Step 01 and consume its confirmed decisions, open items, defaults/assumptions, and `Step01_Handoff`. MUST NOT re-ask any confirmed Step 00 decision. MUST carry every `Open_HighImpact` item into Step 01 Open Questions with owner, impact, and needed-by. |
| Missing prerequisite | MUST reject Step 01 execution and ask user to run [orbit-analyze-tor](../../orbit-analyze-tor/references/contract.md) and obtain its approval first. |
| Template dependency | Embedded in this command. MUST NOT depend on external output template files. |
| Guidance | Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน). |
| Scope classification | MUST separate `In Scope (Confirmed)`, `In Scope (Needs Confirmation)`, and `Out of Scope`. SHOULD use MoSCoW priority for confirmed scope items. Core/Full/Phased/Excluded alternatives are decision aids only and stay scenario rows outside confirmed scope until approved or the user says `re-baseline`. |
| Scope alternatives | See `## 1.1` inclusion rule. |
| Assumptions | MUST be falsifiable with validation signal, disproof trigger, and needed-by timing. |
| Count | `Count` is item-count only; not MD, effort weight, screen count, or API count. |
| Stable IDs | `IS-XX`, `IS-UXX`, `OS-XX`, `ASM-XX`, `C-XX`, `OQ-XX`. `ASM-XX` is one namespace shared with Step 00: reuse the Step 00 ID when Step 01 validates or refines a Step 00 assumption, and continue numbering for new ones. |
| In scope | Intake metadata, goals/KPIs, scope classification, assumptions, constraints, open questions, Step 02 handoff. The `IS-XX` scope items are the requirement list; do not add a separate high-level requirement table. |
| Out of scope | MUST NOT redo Step 00 confirmation gate, create WBS, estimate MD/timeline, resource plan, architecture options, risk range, or any commercial output. Budget is a scope/timeline constraint only. |

## Question Triggers

Ask only when a new gap appears during scope structuring; confirmed Step 00 decisions are reused, and low-impact gaps become `Assumption:` or `Default:` rows.

| Condition | Decision |
|---|---|
| New high-impact delta appears during scope structuring | TRIGGER one delta question or list as Open Question if unresolved. |
| `Count` changes | MUST update category totals, risk exposure, traceability, and note downstream WBS/sizing/risk impact. |

Allowed values: Scope State=`Confirmed/Needs Confirmation/Out of Scope`; Priority=`Must/Should/Could/Won't`; Type=`FR/NFR/Support/Handover`; Confidence=`Low/Medium/High`; Count=item-count only.

## Execution Flow

1. Read `output/step_00_confirmation_baseline.md`; reject execution and ask the user to run Step 00 if it is missing, unreadable, or unapproved under the shared Approval Basis rule.
2. Check high-impact blockers: scope boundary clarity, unresolved Step 00 open items, integration/hosting/security/NFR defaults, and intake assumptions that materially affect Step 02. If unresolved, ask; otherwise state `No blocking confirmations; proceeding with approved baseline/defaults.`
3. If the scope boundary is unclear, list scope alternatives in §1.1 before final classification. Record not-doing/deferred treatment in §3.3 Out of Scope; §3.3 is the single owner of deferred/not-doing items for all later steps.
4. Classify scope, assumptions, and constraints with stable IDs; reconcile Scope Count totals.
5. Ask up to 3-5 highest-impact stakeholder-answerable Open Questions with finite choices in one asking-tool gate, then update confirmed scope, assumptions, Open Questions, Summary, and Handoff before publishing.
6. Write the artifact summary-first: `Step Summary` and `เรื่องที่ต้องตัดสินใจ` directly under the header, then the appendix sections. The Handoff Note MUST give Step 02 the scope basis, integrations, hosting/security/NFR defaults, and architecture-impacting gaps.
7. Stop at the Post-step Review Gate ; only the router may authorize a subsequent action after this action completes.

## Output Contract

Create/update `output/step_01_intake_scope.md` using this compact schema.

Reviewer layout per [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) Output Economy; no step-specific delta.

```markdown
# Step 01 - Intake & Scope: [PROJECT_NAME]

**Source**: [approved Step 00 path + revision; TOR/RFP ref]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [ตาม กฎ approval ที่โหลดจาก action SKILL.md]

## Step Summary

Scope rollup by channel or module, as grouped in the TOR. Counts are item counts from §3.4 and must reconcile to it.

| Channel / Module | In Scope | รอยืนยัน | ครอบคลุมอะไร |
|---|---:|---:|---|
| [CHANNEL_OR_MODULE] | [N] | [N] | [งานหลักแบบภาษาคน ไม่มี ID] |
| **รวม** | **[N]** | **[N]** | ไม่รวม [N] รายการ: [กลุ่มหลักที่ตัดออก] |

- ความชัดเจนของ scope: [ต่ำ/ปานกลาง/สูง] เพราะ [เหตุผลสั้น].
- สมมติฐานที่กระทบ MD มากที่สุด: [1-3 ข้อ แบบภาษาคน].
- ข้อจำกัดหลัก: [1-3 ข้อ].

### เรื่องที่ต้องตัดสินใจ

Only open items that need a Sponsor, Business Owner, or partner answer, at most 3, most MD-impacting first. Do not repeat an item already in Step 00's block unless it is still open; mark a carried item `(ต่อจาก Step 00)`. Write `ไม่มีเรื่องค้าง` when none.

| เรื่อง | ทางเลือก | ผลต่อ estimate | ภายใน |
|---|---|---|---|
| [คำถามภาษาคน ไม่มี ID] | [A / B] | [ขอบเขต/MD/เวลา/ความเสี่ยง] | [step หรือวันที่] |

---

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**Post-step Review Gate — Step 01 Intake & Scope**

Please review:
- Key outputs: Step Summary and เรื่องที่ต้องตัดสินใจ at the top; appendix holds scope in/out, assumptions, constraints, open questions, Step 02 handoff.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: None / Scope / MD / Timeline / Risk / Scenario.

Reply options:
- `approve Step 01` = lock this step and make it eligible for Step 02. This action stops here.
- `revise Step 01: ...` = update this step before proceeding.

## ภาคผนวก — สำหรับ step ถัดไป (ผู้บริหารข้ามได้)

## Step 00 Baseline Consumed

Use Step 00 `Step01_Handoff` as-is; do not restate it. List only the deltas Step 01 adds: [re-baseline or none; new optional or unconfirmed scope alternatives; new ASM IDs; new OQ IDs].

## 1. Project Intake

| Item | Detail | Source / Note |
|---|---|---|
| Project Name | [PROJECT_NAME] | [TOR/RFP_REF] |
| Sponsor | [SPONSOR_ORG_OR_ROLE] | [TOR/RFP_REF / Assumption] |
| Business Owner | [BUSINESS_OWNER] | [TOR/RFP_REF / TBD] |
| Product Owner | [PRODUCT_OWNER_OR_TBD] | [TOR/RFP_REF / TBD] |
| Target Go-Live | [DATE_OR_TBD] | [TOR/RFP_REF / Not specified] |
| Budget Guardrail | [BUDGET_OR_TBD] | Constraint only. [TOR/RFP_REF / Not specified] |
| Delivery Model | [FIXED_SCOPE / T&M / AGILE_PROJECT / WATERFALL / HYBRID] | [TOR/RFP_REF / Assumption] |
| Estimation Objective | [WHAT_TO_ESTIMATE] | [User request / Step 00] |

## 1.1 Scope Alternatives - Scenario Only Unless Approved

Include this section only when the scope boundary is unclear; otherwise write `N/A — scope boundary explicit in TOR/Step 00`. High-impact questions go to `## Open Questions` only.

| Option | Description | When to Choose | Baseline Impact |
|---|---|---|---|
| Core | [Minimum scope required for business outcome] | [Fixed timeline/budget guardrail pressure] | Baseline candidate / scenario until approved |
| Full | [All requested TOR scope] | [Full commitment] | Full-scope candidate if approved |
| Phased | [Core first, optional later] | [Risk/time reduction] | Scenario only unless re-baselined |
| Excluded | [Explicitly not included] | [Avoid ambiguity] | Out of baseline |

## 2. Business Goals & KPIs

List 3-5 business goals; mark missing targets TBD.

| Goal ID | Goal / KPI | Target / Measurement |
|---|---|---|
| G-01 | [GOAL + KPI] | [TARGET or TBD + measurement point] |

## 3. Scope Definition

### 3.1 In Scope (Confirmed)

| ID | Scope Item | Priority | Ref |
|---|---|---|---|
| IS-01 | [CONFIRMED_SCOPE_ITEM] | [Must/Should/Could] | [TOR/RFP_REF] |

### 3.2 In Scope (Needs Confirmation)

These items remain outside the committed baseline until a decision or approved assumption closes the gap. Give each an OQ/DEC/ASM link with treatment and needed-by; choosing a broader scope alternative later does not approve an unresolved item.

| ID | Possible Scope Item | Rationale / Risk if Wrong | Owner |
|---|---|---|---|
| IS-U01 | [UNCLEAR_SCOPE_ITEM] | [RATIONALE + IMPACT] | [OWNER] |

### 3.3 Out of Scope

Single owner of deferred/not-doing items. Step 03.1 §0.3 adds only new functional items, continuing the `OS-XX` numbering; later steps cite `OS-XX` and never re-list them.

| ID | Out of Scope | Reason / TOR Ref | Treatment | Change Trigger |
|---|---|---|---|---|
| OS-01 | [OUT_OF_SCOPE_ITEM] | [TOR/RFP_REF / Commercial exclusion / Assumption] | Not Doing / Deferred / Assumed Existing / Scenario | [WHAT_REOPENS_SCOPE] |

### 3.4 Scope Count

| Category | Count | Note |
|---|---:|---|
| In Scope (Confirmed) | [COUNT_CONFIRMED_ITEMS] | Item-count only; not MD/screen/API/weight. |
| In Scope (Needs Confirmation) | [COUNT_NEEDS_CONFIRMATION_ITEMS] | Update downstream WBS/sizing/risk if this changes. |
| Out of Scope | [COUNT_OUT_OF_SCOPE_ITEMS] | Exclusion count protects baseline boundary. |
| Total Scope Items | [TOTAL_COUNT] | Must equal confirmed + needs-confirmation + out-of-scope item counts. |

## 4. Planning Basis

### Assumptions / Defaults

Rows that validate a Step 00 assumption keep its ID and start the Statement with `= Step 00 ASM-XX` plus only the Step 01 delta. New assumptions continue after the last Step 00 ID.

| ID | Statement | Validation Signal | Disproof Trigger | Impact if False | Owner | Needed By | Confidence | Baseline Treatment | Fallback Default |
|---|---|---|---|---|---|---|---|---|---|
| ASM-XX | = Step 00 ASM-XX: [DELTA] / Assumption: [ASSUMPTION_STATEMENT] | [WHAT_CONFIRMS_TRUE] | [WHAT_PROVES_FALSE] | [SCOPE/MD/TIMELINE/RISK_IMPACT] | [OWNER] | [STEP/DATE] | [Low/Medium/High] | Included / Excluded / Scenario / Open / Discovery Needed | [authorized fallback or Step 00 ref] |

## 5. Constraints

| ID | Constraint | Category | Impact |
|---|---|---|---|
| C-01 | [CONSTRAINT_FROM_TOR_OR_CLIENT_POLICY] | [Time/Budget Guardrail/Resource/Compliance/Technical/Contract] | [IMPACT_ON_DELIVERY] |

## Open Questions

A Step 00 item carried forward gets a new Step 01 `OQ-XX` ID and cites the originating `DEC-XX` in the Question or Why/Impact cell.

| ID | Question | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [STEP00_OPEN_OR_STEP01_DELTA_QUESTION; cite `DEC-XX` if carried from Step 00] | [WHY + IMPACT] | [OWNER] | [STEP/DATE] |

## Handoff Note - Step 02

- Approved Step 01 scope basis: [FULL_SCOPE / CORE_SCOPE / PHASE_1 / TBD].
- Known/expected integrations: [SYSTEM_A], [SYSTEM_B], or `N/A — [reason]`.
- Hosting baseline/default: [CLIENT_CLOUD / VENDOR_CLOUD / ON_PREM / HYBRID / TBD].
- Security defaults: [AUTH/RBAC/[privacy law or data protection requirement]/ENCRYPTION/AUDIT/SECRETS/WAF_DEFAULTS].
- NFR defaults if TOR is silent: [PERFORMANCE], [AVAILABILITY], [RETENTION], [RTO/RPO], [BROWSER/DEVICE].
- Architecture-impacting gaps: [API_SPEC], [PAYLOAD], [AUTH_METHOD], [DATA_VOLUME], [CONCURRENT_USERS], [RESPONSE_TIME], [DR_REQUIREMENT].
- Step 02 input artifact: `output/step_01_intake_scope.md`.

## Internal Review

Render per [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) Output Economy.

| Check | Result | Note |
|---|---|---|
| Step 00 consumed + no duplicate gate | [Pass/Warning/Fail] | [NOTE] |
| Scope separated + counts reconcile | [Pass/Warning/Fail] | Count is item-count only, not MD/screen/API/weight. |
| Scope alternatives and exclusions | [Pass/Warning/Fail] | Alternatives (if any) and Not Doing/Deferred items are scenario-labelled and not mixed into confirmed baseline. |
| Assumptions/constraints labelled | [Pass/Warning/Fail] | [NOTE] |
| Open questions carried forward | [Pass/Warning/Fail] | [NOTE] |
| Step 02 handoff ready | [Pass/Warning/Fail] | [NOTE] |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope and Output Contract. Verify artifact path/metadata, carried Step 00 open items, and reconciled scope counts. Shared approval and reviewer-layout checks follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน).
