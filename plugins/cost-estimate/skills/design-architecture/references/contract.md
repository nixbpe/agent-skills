# Step 02 architecture contract

Read [the action guide](../SKILL.md) and all its required principles before applying this contract, including direct invocation. User input and `output/` paths are relative to the working project. Bundled reference links are relative to this installed skill. Do not assign SG1/SG2 or add Approved Baseline Scope before Step 03.1.

The optional architecture profile and its example are not project evidence. Read the profile only to assess an explicitly requested or proposed candidate. Adoption requires explicit project acceptance; continuous workflow authorization alone does not approve this stack. Missing NFR values remain Open or proposed labelled defaults until authorized. Do not automatically assume AWS, EKS, microservices, SLA, surfaces, or example scope.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate **Step 02 Architecture & Constraints** from approved Step 01 intake scope. |
| Input | `output/step_00_confirmation_baseline.md`, approved `output/step_01_intake_scope.md`, and TOR/RFP references when needed for traceability. |
| Output | MUST create/update `output/step_02_architecture_constraints.md`. |
| Prerequisite | MUST read `output/step_00_confirmation_baseline.md` and approved `output/step_01_intake_scope.md` before producing architecture. |
| Missing prerequisite | MUST reject execution if Step 00 is missing or Step 01 is missing/not approved, and ask user to run Step 00 then run/approve Step 01 before Step 02. |
| Guidance | Read [Architecture Baseline](architecture.md) as an optional reference, not an approved project stack. Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน). Budget-fit means architecture/scope trade-off only. |
| Scope discipline | MUST NOT add scope beyond approved Step 01; unclear items become `Assumption:`, `Default:`, or Open Question. |
| Decisions | Every architecture decision has rationale + effort impact (`L/M/H`). Options are 2-3 max with a recommendation. |
| Integration coverage | MUST check SSO/Auth, notification, payment, BI/reporting, file storage, master data, and TOR systems. |
| NFRs | See `## 4` for the required category list and labelling rule. |
| Surface taxonomy | Declare every surface once in §1.1 Surface Map with stable `SUR-XX` IDs. Default taxonomy: `Internal Admin` (พนักงาน/admin web), `Public Customer` (เว็บสาธารณะ/ลูกค้าภายนอก), `Internal Dashboard` (analytics/BI), `Backend / Integration` (no UI). Add project-specific surfaces (e.g., Mobile App, Kiosk, Partner Portal) only when needed. Step 03.1/03.2/04 must reference these IDs/labels. |
| Stable IDs | `OPT-XX`, `INT-XX`, `NFR-XX`, `TC-XX`, `DEC-XX`, `OQ-XX`, `SUR-XX`. |
| In scope | Current/target state, options, integrations, NFRs, constraints, environments, complexity score, decisions, Step 03 handoff. |
| Out of scope | MUST NOT add scope, create WBS/backlog, estimate MD/timeline, resource plan, risk range, or any commercial output. |

## Question Triggers

| Condition | Action |
|---|---|
| Scope has no architecture implication | Keep as trace only; do not create architecture work. |
| Integration confirmed by TOR/Step 01 | Reuse the `INT-XX` ID already assigned by Step 00's `Integration_Inventory`; missing protocol/volume/frequency becomes assumption. |
| Integration implied but unconfirmed | Mark `Assumption:` or Open; do not count as confirmed. |
| Hosting/deployment unclear | Present 2-3 options, recommend one, keep final model Open. |
| NFR threshold missing | Use `Default:` and state impact if client/TOR rejects it. |
| Option affects scope/MD/timeline materially | Flag effort impact and Open decision; do not change baseline silently. |

## Execution Flow

1. Read `output/step_00_confirmation_baseline.md` and approved `output/step_01_intake_scope.md`; reject execution if Step 00 is missing or Step 01 is missing/not approved.
2. Check high-impact blockers: hosting/deployment baseline, integration contract assumptions, security/compliance constraints, and unresolved architecture-impacting open questions. If unresolved, ask; otherwise state `No blocking confirmations; proceeding with approved baseline/defaults.`
3. Declare every surface in §1.1 Surface Map before mapping options, integrations, and NFRs.
4. Fill current→target (4 rows), options, integration map + coverage line, NFRs, constraints, environment, complexity score (6 weighted drivers; total/max/rating shown once), and decisions.
5. Ask up to 3-5 highest-impact stakeholder-answerable Open Architecture Questions with finite choices in one asking-tool gate, then update decisions, assumptions, integration/NFR rows, Summary, and Handoff before publishing.
6. Write the artifact summary-first: `Step Summary` and `เรื่องที่ต้องตัดสินใจ` directly under the header, then the appendix sections. The Handoff Note MUST give Step 03 architecture WBS candidates, `INT-XX` list with status, NFR work packages, and open questions.
7. Stop at the Post-step Review Gate ; only the router may authorize a subsequent action after this action completes.

## Output Contract

Create/update `output/step_02_architecture_constraints.md` using this compact schema.

Reviewer layout per [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) Output Economy; step-specific delta: no tool/stack names beyond the architecture style and hosting.

```markdown
# Step 02 - Architecture & Constraints: [PROJECT_NAME]

**Source**: `output/step_01_intake_scope.md` [approved revision] + [TOR/RFP ref]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [ตาม กฎ approval ที่โหลดจาก action SKILL.md]

## Step Summary

| หัวข้อ | สรุป |
|---|---|
| สถาปัตยกรรมที่แนะนำ | [รูปแบบ + hosting ในหนึ่งประโยค]; ไม่เลือก [ทางเลือกหลักที่ตัดทิ้ง] เพราะ [เหตุผลสั้น] |
| ความซับซ้อน | [Low/Medium/High] ([PCT]%): [2-4 driver หลักแบบภาษาคน] |
| ตัวขับ effort หลัก | [2-3 เรื่อง เช่น integration, NFR ที่เข้มที่สุด, security gate] |
| ใช้ค่า default แทน | [จำนวน] เรื่องที่ลูกค้ายังไม่ยืนยัน: [รายการแบบภาษาคน] |

### เรื่องที่ต้องตัดสินใจ

Only open architecture items that need a client, Sponsor, or partner answer, at most 3, most MD-impacting first. Do not repeat an item already in the Step 00 or Step 01 block; list those in one `ยังค้างจาก Step 00/01:` line under the table. Write `ไม่มีเรื่องค้าง` when none.

| เรื่อง | ทางเลือก | ผลต่อ estimate | ภายใน |
|---|---|---|---|
| [คำถามภาษาคน ไม่มี ID] | [A (ปัจจุบัน) / B] | [ขอบเขต/MD/เวลา/ความเสี่ยง] | [step, milestone หรือวันที่] |

---

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**Post-step Review Gate — Step 02 Architecture & Constraints**

Please review:
- Key outputs: Step Summary and เรื่องที่ต้องตัดสินใจ at the top; appendix holds options, integration map, NFRs, constraints, complexity score, decisions, Step 03 handoff.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Scope / MD / Timeline / Risk / Scenario.

Reply options:
- `approve Step 02` = lock this step and make it eligible for Step 03.1. This action stops here.
- `revise Step 02: ...` = update this step before proceeding.

## ภาคผนวก — สำหรับ step ถัดไป (ผู้บริหารข้ามได้)

## Prerequisites Consumed

Step 00 baseline: [Pass/Warning/Fail] — [one-line facts/defaults used].  
Step 01 scope: [Pass/Warning/Fail] — [scope basis + open architecture gaps].

## 1. Current → Target State

| Area | Current→Target Summary | Basis | Effort Impact |
|---|---|---|---|
| Business Process | [CURRENT → TARGET in one phrase] | [TOR/Step01/Assumption] | [L/M/H] |
| Application | [CURRENT → TARGET in one phrase] | [TOR/Step01/Assumption] | [L/M/H] |
| Data | [CURRENT → TARGET in one phrase] | [TOR/Step01/Assumption] | [L/M/H] |
| Infrastructure | [CURRENT → TARGET in one phrase] | [TOR/Step01/Assumption] | [L/M/H] |

## 1.1 Surface Map

Declare every user-facing and backend surface the platform will serve. Step 03/04 tag each feature/screen/API/WBS with one or more Surface IDs from this table.

| SUR-ID | Surface Name | Type | Primary Actor | Channel | Access Mode | Notes |
|---|---|---|---|---|---|---|
| SUR-01 | [e.g., Internal Admin] | Internal Web | [Admin/Staff role] | Web browser | SSO (Azure AD/OIDC) | [CRUD master, workflow, audit, report] |
| SUR-02 | [e.g., Public Customer] | Public Web | [External customer/tenant] | Web browser | OTP/email or public | [search, booking, request] |
| SUR-03 | [e.g., Internal Dashboard] | Internal Web | [Strategic/exec] | Web (embed Power BI?) | SSO | [analytics/BI] |
| SUR-04 | [e.g., Backend / Integration] | Non-UI | System / scheduled | API / event | Service-to-service | [integration, batch, scheduled] |

Defaults: Tax/PDPA-related screens belong to `Internal Admin` unless TOR says public. Power BI/embedded analytics belong to `Internal Dashboard`. Integrations and scheduled jobs belong to `Backend / Integration`. A feature can span multiple surfaces (write as comma-separated SUR-IDs in Step 03.1/04).

## 2. Architecture Options

| OPT-ID | Option Summary | Trade-off (Pros/Cons) | Effort Impact | Decision |
|---|---|---|---|---|
| OPT-01 | [OPTION] | [PROS / CONS] | [L/M/H] | [Recommended/Open/Rejected + why] |

## 3. Integration Map

| INT-ID | System / Capability | Dir / Protocol | Vol / Cx / Freq | Basis | State |
|---|---|---|---|---|---|
| INT-01 | [SYSTEM] | [In/Out/Both / protocol] | [L/M/H or TBD] / [L/M/H] / [freq] | [Step 00 Integration_Inventory + only the ASM/DEC/gap that adds direction or protocol] | [Confirmed/Assumption/Open] |

Requirement refs per INT live in Step 00 `Integration_Inventory`; do not copy them into `Basis`.

Coverage: SSO/Auth=[INT/N/A/Assumption]; Notification=[INT/N/A/Assumption]; Payment=[INT/N/A/Assumption]; BI/Reporting=[INT/N/A/Assumption]; File Storage=[INT/N/A/Assumption]; Master Data=[INT/N/A/Assumption]; TOR Systems=[covered list].

## 4. NFRs

Cover Performance, Availability, Security, Scalability, Retention, and [privacy law / data protection requirement] at minimum. Missing values use labelled `Default:` with impact if false.

| NFR-ID | Category | Target / `Default:` | Basis | Impact if False |
|---|---|---|---|---|
| NFR-01 | Performance | [TARGET or `Default:`] | [TOR/Assumption/Default] | [IMPACT] |

## 5. Technical Constraints

| TC-ID | Constraint | Why | Effort Impact | Mitigation |
|---|---|---|---|---|
| TC-01 | [CONSTRAINT] | [C-XX from Step 01 when it restates a Step 01 constraint; then NFR/TOR ref] | [L/M/H] | [MITIGATION] |

## 6. Environment & Release

Cite the §1 row, DEC or NFR ID that already states a baseline, and write only what it does not cover.

| Area | Baseline / Default | Open Gap |
|---|---|---|
| Env Stack | [DEV/SIT/UAT/PROD/etc.] | [gap/N/A] |
| Hosting / Cloud | [baseline/TBD] | [gap/N/A] |
| Release & CI/CD | [baseline/TBD] | [gap/N/A] |
| Security + DR/BCP + Client Devices | [baseline] | [gap/N/A] |

## 7. Architecture Complexity Score

| Driver | Weight | Rating 0-3 | Rationale |
|---|---:|---:|---|
| Integration Count | 5 | [0-3] | [WHY] |
| Legacy Coupling | 4 | [0-3] | [WHY] |
| Security/Compliance | 4 | [0-3] | [WHY] |
| Data Migration Volume | 3 | [0-3] | [WHY] |
| NFR Stringency | 3 | [0-3] | [WHY] |
| Multi-tenancy | 3 | [0-3] | [WHY] |

Score: `[TOTAL] / 66 = [PCT]%` → **[Low/Medium/High]**. Formula: `Σ(weight × rating)`. Default thresholds use the unrounded percentage: Low <33%, Medium 33% to <67%, High ≥67%. Ratings are 0=absent, 1=limited, 2=moderate, 3=high; justify each with project evidence. Show the headline result in Step Summary and the calculation here.

## 8. Decisions & Open Items

### Decisions

List `Open` and spec-pending rows first, then `Recommended` rows.

| DEC-ID | Decision | Why | Effort Impact | Owner | State | Baseline Treatment | Needed By | Fallback Default |
|---|---|---|---|---|---|---|---|---|
| DEC-XX | [DECISION] | [RATIONALE + source] | [L/M/H + impact if wrong] | [OWNER] | [Approved/Recommended/Open/Rejected] | Included / Excluded / Scenario / Open / Discovery Needed | [step/date] | [authorized default / N/A — resolved] |

### Open Architecture Questions

Do not restate a Step 01 open question. When an architecture question refines one, start the Question with `= OQ-XX(Step01):` and write only the architecture detail it adds. `Needed By` names a real upcoming trigger; if a needed-by gate has passed while the item remains open, retain the original date, flag it overdue, and record an owner-approved revised date with impact. Do not hide overdue decisions by moving their dates.

| ID | Question | Why It Matters | Impact if Unresolved | Owner | Needed By |
|---|---|---|---|---|---|
| OQ-01 | [ARCHITECTURE_GAP] | [WHY] | [IMPACT] | [OWNER] | Before Step 03 |

## Handoff Note - Step 03

- Architecture-derived WBS candidates: [env setup], [CI/CD], [migration], [security], [DR], [observability].
- Integration work packages: [INT-XX list with status].
- NFR work packages: [performance], [security], [DR/BCP], [retention], [compliance].
- Architecture-impacting open questions: [OQ list].

## Internal Review

Render per [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) Output Economy.

| Check | Result | Note |
|---|---|---|
| Step 01 consumed + no new scope | [Pass/Warning/Fail] | [NOTE] |
| Surface Map declared + every TOR-implied surface covered | [Pass/Warning/Fail] | [NOTE] |
| Integrations + coverage complete | [Pass/Warning/Fail] | [NOTE] |
| NFRs/constraints sourced or default-labelled | [Pass/Warning/Fail] | [NOTE] |
| Decisions include rationale + effort impact | [Pass/Warning/Fail] | [NOTE] |
| Complexity score + Step 03 handoff complete | [Pass/Warning/Fail] | [NOTE] |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope and Output Contract, including Surface Map, INT/NFR coverage, decision ownership, and complexity thresholds. Shared approval and reviewer-layout checks follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน).
