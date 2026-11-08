# Step 00 TOR analysis contract

Read [the action guide](../SKILL.md) and all its required principles before applying this contract, including direct invocation. User input and `output/` paths are relative to the working project. Bundled reference links are relative to this installed skill. Do not assign SG1/SG2 or add Approved Baseline Scope before Step 03.1.

Docling is required only for non-text input. Use an available Docling installation or tool, preserve conversion provenance, and inspect the resulting text against the source. Do not invent conversion success or implement a replacement converter. If unavailable, failed, or unverifiable, stop and request a text source or explicit permission for a stated limitation. Such permission does not waive evidence or mandatory quality gates; unreadable requirements remain unresolved. Text input does not require Docling or a Converted Text Source field.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST clarify TOR/RFP uncertainty before Step 01 intake scope. |
| Input | TOR/RFP text, requirement notes, or customer brief. If the source is not already text (`.txt`, `.md`, or pasted text), MUST convert it with Docling first, save the converted text under `output/`, and analyze the converted text. If conversion cannot run or cannot be verified, STOP and ask for a text source or permission to proceed with a clearly marked limitation. |
| Output | MUST create or update `output/step_00_confirmation_baseline.md`. Record the original source in `Source` and `Step01_Handoff`; include converted text path/version only when conversion was attempted. |
| Guidance | MUST apply [TOR/RFP Score Guidance](tor-rfp-score-guidance.md) for clarity scoring, ambiguity triage, evidence rules, and output compactness. Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, and no-rate-card rules follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน). |
| Next command | SHOULD hand off to [orbit-define-scope](../../orbit-define-scope/references/contract.md). |
| In scope | Source/version, objective, deadline/budget guardrail, scope boundary, channels/users, integrations/protocols, hosting, security, compliance, data, NFR, support. Budget is constraint context only. |
| Out of scope | MUST NOT create WBS, effort sizing, resource plan, architecture options, risk range, or any commercial output. |

## Question Triggers

Ask in this priority order. Group related uncertainty into one decision. Everything else becomes `Assumption:` or `Default:` in `Applied_Defaults`.

| Condition | Decision |
|---|---|
| TOR/RFP source or version is unclear | TRIGGER: confirm baseline document. |
| Estimation objective is unclear | TRIGGER: scope only, scope+effort, resource/timeline/risk, or full workflow. |
| Scope boundary is unclear | TRIGGER: full scope, phase-core, MVP, optional, or undecided. Do not treat MVP, budget-fit, or phase-core as baseline unless explicitly confirmed. |
| Deadline, budget guardrail, or contract constraint is unclear | TRIGGER only if it affects scope boundary, scenario, timeline, or contractual commitment. |
| Channels, users, integrations/protocols, auth/security/compliance/privacy law, data migration, reporting/audit, acceptance, warranty, or handover is unclear | TRIGGER if impact is high; otherwise log as `Assumption:`. |
| Hosting/infrastructure is absent | Use project-provided approved architecture/defaults if accepted; otherwise log Open. Do not depend on a fixed stack template. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with Step 00 confirmation baseline.` |

## Execution Flow

1. Convert a non-text source with Docling; stop on failure per the Input rule.
2. Score the 9 clarity dimensions per kb guidance and compute the average.
3. List unclear items and triage High / Medium / Low. High goes to `Open_HighImpact`; Medium and Low go to `Applied_Defaults`.
4. Ask up to 5 highest-impact stakeholder-answerable High items with finite choices in one gate, using the asking tool or chat fallback. Update the artifact with decisions or authorized defaults. Do not leave a High item open without owner and needed-by.
5. Write the artifact summary-first: `Step Summary` and `เรื่องที่ต้องตัดสินใจ` directly under the header, then the appendix sections. `Step01_Handoff` keys MUST map to Step 01 pre-step confirmation inputs.
6. Stop at the Post-step Review Gate ; only the router may authorize a subsequent action after this action completes.

## Output Contract

Create/update `output/step_00_confirmation_baseline.md` with this schema. Replace placeholders, remove template rows, write `N/A — [reason]` for sections that do not apply, and keep rows concise for downstream agents.

Use the shared metadata schema in [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน). Include `Converted Text Source` only when conversion was attempted; record failures in `Source_Quality_Notes`. Step Summary is the canonical numeric block for Step 00.

```markdown
# Step 00 - TOR Clarification Baseline: [PROJECT_NAME]

**Source**: [TOR/RFP name + version/date, one line]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Converted Text Source**: [converted path + tool + revision; Failed: SQ-XX]
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [ตาม กฎ approval ที่โหลดจาก action SKILL.md]

## Step Summary

| หัวข้อ | สรุป |
|---|---|
| เอกสารตั้งต้น | [ยืนยันแล้ว/ยังไม่ยืนยัน + ชื่อและ version] |
| ความชัดเจนของ TOR | [N.N/5 + ระดับ]; ต่ำสุดคือ [มิติ] [N/5] เพราะ [เหตุผลสั้น] |
| ขอบเขตที่ตั้งใจ | [channel/module, จำนวน requirement, สิ่งที่ไม่รวม ในหนึ่งบรรทัด] |
| มติที่ปิดแล้ว | [จำนวน]: [มติแต่ละข้อแบบสั้น คั่นด้วย ·] |
| สมมติฐานที่ใช้ | [จำนวน] ข้อ; ที่กระทบ MD มากที่สุดคือ [1-3 ข้อ แบบภาษาคน] |
| ความเสี่ยงหลัก | [1-2 เรื่อง] |

### เรื่องที่ต้องตัดสินใจ

Only items still open that need a Sponsor, Business Owner, or partner answer, at most 3, most MD-impacting first. Write `ไม่มีเรื่องค้าง` when none.

| เรื่อง | ทางเลือก | ผลต่อ estimate | ภายใน |
|---|---|---|---|
| [คำถามภาษาคน ไม่มี ID] | [A / B] | [ขอบเขต/MD/เวลา/ความเสี่ยง] | [step หรือวันที่] |

---

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**Post-step Review Gate — Step 00 TOR Clarification Baseline**

Please review:
- Key outputs: Step Summary and เรื่องที่ต้องตัดสินใจ at the top; appendix holds confirmed decisions, clarity score, defaults/assumptions, Step 01 handoff.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Scope / MD / Timeline / Resource / Risk / Scenario.

Reply options:
- `approve Step 00` = lock this confirmation baseline and make it eligible for Step 01. This action stops here.
- `revise Step 00: ...` = update confirmation baseline before proceeding.

## ภาคผนวก — สำหรับ step ถัดไป (ผู้บริหารข้ามได้)

## Confirmed_Decisions

| ID | Area | Decision | Source |
|---|---|---|---|
| [REQ/INT/NFR/DATA]-XX | [AREA] | [FACT_FROM_SOURCE] | [TOR/RFP_REF or approved artifact] |

Source facts belong here. Stakeholder decisions use `DEC-XX` in `Decision_Outcomes`.

## TOR_RFP_Clarity_Score

| Dimension | Score 1-5 | Evidence / Gap | Estimate Impact |
|---|---:|---|---|
| Business Objective | [N] | [evidence/gap] | [scope/MVP impact] |
| Scope Boundary | [N] | [evidence/gap] | [WBS impact] |
| Functional Inventory | [N] | [evidence/gap] | [FE/BE/QA impact] |
| Integration Clarity | [N] | [evidence/gap] | [INT/risk impact] |
| Data & Migration | [N] | [evidence/gap] | [migration impact] |
| NFR | [N] | [evidence/gap] | [architecture impact] |
| Users & Roles | [N] | [evidence/gap] | [permission/workflow impact] |
| Acceptance/UAT | [N] | [evidence/gap] | [QA/UAT impact] |
| Timeline Constraint | [N] | [evidence/gap] | [resource/schedule impact] |
| **Average** | **[N.N]** | [Clear/Moderate/High/Insufficient] | [baseline action] |

## Open_HighImpact

| ID | Area | Question / Context | Options | Baseline Impact | Fallback Default | Owner | Needed By |
|---|---|---|---|---|---|---|---|
| DEC-XX | [area] | [what TOR says + unclear point] | A) [choice] B) [choice] C) [scenario/exclude] | [scope/MD/timeline/risk] | [default if `use defaults`] | [owner] | [step/date] |

Once a packet is answered at the gate, delete its row here and record the result once in `### Decision_Outcomes`. Do not repeat decided packets in `Confirmed_Decisions`, a triage table, or the Handoff; point to the DEC ID instead.

### Decision_Outcomes (Step 00 gate, [date])

| DEC ID | Decision | Source | Impact if Wrong | Baseline Treatment | Scenario Created | Owner | Needed By | Fallback Default |
|---|---|---|---|---|---|---|---|---|
| DEC-XX | [decision incl. key detail] | [stakeholder + date / authorized default] | [scope/MD/timeline/risk] | Included / Excluded / Scenario / Discovery Needed | `SCN-XX` / N/A — [reason] | [owner] | [step/date or closed date] | [default / N/A — resolved] |

## Applied_Defaults

Ambiguity triage is recorded here as `Triage Level`, not in a separate table. Medium/Low gaps that have no A-row go in `### Other Triaged Gaps`. Do not restate a `Confirmed_Decisions` or `Decision_Outcomes` fact as an ASM row; when an existing ASM ID must stay for traceability, write the Statement as `= [Q/DEC ID]` plus only the delta.

| ID | Statement | Rationale + Impact if False | Baseline Treatment | Owner | Confidence | Due | Triage Level |
|---|---|---|---|---|---|---|---|
| ASM-XX | Assumption: / Default: [STATEMENT] | [RATIONALE + IMPACT] | Included / Excluded / Scenario / Open | [OWNER] | L/M/H | [step/date] | High → Default/Scenario/Risk / Medium / Low / — |

### Other Triaged Gaps (no A-row)

| ID | Area | Ambiguity | Level | Action | Owner | Needed By |
|---|---|---|---|---|---|---|
| [ASM-/LOW- ID] | [area] | [gap] | Medium/Low | [assumption/default/note] | [owner] | [step] |

## Optional Compact Sections

Include `Integration_Inventory` whenever integrations are identified, including assumed/open ones; write `N/A — no integrations identified` otherwise. Include the other sections only when the source needs them, and keep them to counts and pointers: `Requirement_Inventory_Snapshot` (rows per channel/sheet, ID ranges; ID defects point to SQ-XX), `Integration_Inventory` (ID / System / Requirement Ref / Status; direction and pattern belong to Step 02 §3; this is the single owner of the integration list, so `Confirmed_Decisions` and `Step01_Handoff` cite the INT range instead of re-listing systems), `Source_Quality_Notes` (SQ-XX findings with recommended fix, including source-conversion limitations).

## Step01_Handoff

| Key | Value |
|---|---|
| Source/version baseline | [original source + converted text path or N/A] |
| Estimation objective | [VALUE] |
| Scope boundary intent | [VALUE] |
| Confirmed channels/user groups | [VALUE] |
| Confirmed/expected integrations | [VALUE] |
| Hosting/infrastructure baseline | [VALUE] |
| High-impact open items | [VALUE] |
| Clarity score / confidence | [pointer to Step Summary + TOR_RFP_Clarity_Score; confidence/action] |
| Baseline assumptions and scenario deltas | [VALUE] |

## Handoff Note - Step 01

- Use `Step01_Handoff` as the Step 01 input baseline and carry every `Open_HighImpact` item as a Step 01 Open Question with owner/needed-by.
- Preserve baseline vs scenario separation from Step 00 in Step 01 scope classification.

## Readiness_Check

Pass: [list the checks that passed in one line: source/text, clarity + triage, high-impact items asked/logged, defaults labelled, Step 01 handoff]. รายการที่ไม่ Pass:

| Check | Result | Note |
|---|---|---|
| [check] | Warning/Fail | [evidence + action] |


```

## Validation Checklist

Evaluate `Readiness_Check` against the Fixed Baseline / Scope and Output Contract, including source conversion, high-impact decisions, and Step01_Handoff. Shared approval and reviewer-layout checks follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน).
