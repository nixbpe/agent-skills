# Risk and final planning baseline contract

Read the [action guide](../SKILL.md) and every principle it requires before executing this contract, including direct invocation. `output/` paths resolve from the working project. Bundled Markdown links resolve from this installed skill. Examples and template rows are not project evidence. Preserve mandatory quality gates; approval cannot bypass a failed gate. Produce only this action’s artifact and stop.

Step 06 is a proposed final planning baseline until recorded approval. Evaluate all 23 final checks individually as Pass / Warning / Fail with evidence and any required action. Never replace the table with a blanket pass. There is no separate baseline-review action.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate the final Step 06 planning baseline, including risk, contingency, range, reserve, and internal consistency review from approved Step 05 adjusted effort/resource plan. |
| Input | `output/step_05_resource_plan.md`, `output/step_04_sizing_estimate.md`, approved Step 03 artifacts, approved architecture/integration constraints, Step 04 companion review, and Step 00/01 assumption/decision logs. |
| Output | MUST create/update `output/step_06_risk_contingency.md`. |
| Prerequisite | MUST read approved Step 05 resource plan before producing risk/contingency. |
| Missing prerequisite | MUST reject Step 06 execution and ask user to run/approve [orbit-plan-resources](../../orbit-plan-resources/references/contract.md) first. |
| Guidance | MUST apply [Estimation Calibration Guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md) for sanity thresholds, confidence usage, and out-of-threshold handling, and this contract’s §5 Cross-step Consistency Check for the 23 Required Final Checks. Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by this action](../SKILL.md#กฎที่ต้องอ่าน). |
| Next command | N/A — Step 06 is the final planning baseline step. |
| In scope | External risk register, contingency basis, P25/P50/P75/P90 baseline scenarios, management reserve, re-estimation triggers, cross-step consistency check, findings, final planning baseline snapshot. |
| Out of scope | MUST NOT change Step 04 Raw MD, Step 05 Adjusted MD/duration, resource plan, or approved baseline scope, and MUST NOT produce any commercial output. |
| Upstream immutability | Adjusted MD and duration come from Step 05. If Adjusted MD or the resource plan is inconsistent, STOP and ask to revise Step 05 or Step 04, or record a finding; never fix upstream numbers silently. |
| Risk sources | Risk items reference approved artifacts and Step 00-05 assumptions/dependencies; every unconfirmed high-impact assumption becomes a potential risk or validity condition. |
| Risk eligibility | Include only uncertainties outside the delivery team's direct control: external dependency, stakeholder decision, customer readiness, vendor/3rd-party readiness, regulatory, data/API owner, environment, procurement, or contractual. Internal factors (inability to find staff, capacity gap, key-person replacement, ramp-up, scarce internal skill, PM allocation, productivity shortfall, vendor staffing under team control) stay Step 05 resource constraints or validity conditions, unless they depend on an external approval, vendor, customer, or contractual decision. |
| Risk taxonomy | Exactly two top-level themes: Theme A `Integration / External Dependency` (external technical readiness/contracts) and Theme B `Requirement Unconfirmed` (stakeholder decisions and requirement details), with boundaries and owner patterns per the Risk Taxonomy Reference. One uncertainty appears in one risk only; do not mix requirement uncertainty into integration risks. |
| Critical workflow | If critical workflow / approval process / decision routing / state model details are unconfirmed, create a standalone Requirement Unconfirmed risk covering levels/states, routing conditions, approve/reject decisions, route back/resubmit, cancel/withdraw, delegate/expire, SLA/escalation, notification, and audit requirement. Owner: Business Owner / [Product Owner], with Process Owner, Security/Compliance, and IT/SA as supporting stakeholders. |
| Risk writing | Each risk states cause + impact and a self-contained mitigation/decision needed, understandable without lookup IDs. |
| Scoring | P×I on a 1-5 scale with probability mapping 1=10%, 2=30%, 3=50%, 4=70%, 5=90%; Expected MD = Prob % × Effort Impact MD; bands per the Risk Band Reference. |
| Contingency | Effort-based, never a flat unexplained percentage: Expected External Risk MD + adjustments from the Contingency Adjustment Reference, validated against the risk band guideline. Every adjustment MUST map to named requirement, integration, data, NFR, assumption, decision, risk, or scenario IDs; remove any adjustment without a driver. |
| Baseline and reserve | Delivery Baseline = Adjusted MD + Contingency MD; Planning Total = Delivery Baseline + Management Reserve. Management Reserve is sponsor-controlled for unknown-unknowns and stays separate unless explicitly released. P75 is the recommended delivery commitment view and excludes Management Reserve unless explicitly stated. Contingency/Reserve MD excludes warranty/hypercare effort already carried in Step 04/05. |
| Scenario range | P25/P50/P75/P90 are risk ranges for approved baseline scope only (Scenario Formula Reference), not cap/MVP/scope-cut views. If the user asks for MVP, budget cap, target date, or scope cut, add a brief separate scenario note only if requested; preserve the baseline unless explicitly re-baselined. |

## Question Triggers

Before execution, check high-impact blockers: approved Adjusted MD/resource plan, risk appetite, contingency approach, baseline vs scenario intent, P50/P75 usage, management reserve treatment, and sign-off audience expectations.

| Condition | Action |
|---|---|
| Risk appetite unclear | TRIGGER question, or use the labelled default from the Management Reserve Reference. |
| Contingency approach unclear | TRIGGER question on whether P50 or P75 is the planning/commitment basis; default P50 internal, P75 fixed-scope commitment. |
| Adjusted MD/resource plan inconsistent | STOP and ask to revise Step 05 or Step 04; do not fix numbers silently. |
| Risk expected MD outside guideline band | Explain the adjustment and reconcile against the risk band. |
| Management reserve requested as delivery effort | Keep separate unless the sponsor explicitly approves release into the delivery baseline. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with approved baseline/defaults.` |

## Execution Flow

1. Read the approved Step 05 resource plan (plus Step 04 estimate, Step 03 artifacts, and architecture/integration constraints); reject Step 06 if Step 05 is missing or unapproved. Record Adjusted MD, duration, peak/average FTE, critical path, Step 05 resource constraints (context only), and open assumptions.
2. Resolve Question Triggers in one gate, or state the no-blocking sentence.
3. Scan approved artifacts and Step 00-05 assumptions using the Risk Taxonomy Reference; consult optional risk patterns only when needed. Triage candidates with the quick 1-3 matrix, apply "When NOT to add a risk", then promote only applicable external risks into Theme A / Theme B with 1-5 P×I scores per the Scoring Reconciliation.
4. Compute Expected MD per risk, the Contingency Basis with adjustments, the Ambiguity-to-Contingency Mapping, and the Risk Band Validation.
5. Compute P25/P50/P75/P90 from the Scenario Formula Reference, then Delivery Baseline, Management Reserve (Management Reserve Reference), and Planning Total.
6. Define Re-estimation Triggers (external trigger, threshold, action, SLA, owner).
7. Run the Cross-step Consistency Check (the 23 Required Final Checks) and record Findings `F-XX` with severity H/M/L, recommendation, and impact, or `No critical findings`. Upstream inconsistencies become findings or revision requests, never silent fixes.
8. Ask up to 5 highest-impact remaining stakeholder-answerable open items with finite choices in one gate using the asking tool or chat fallback, then update the risk register, contingency/reserve treatment, scenarios, Summary, and Final Planning Baseline Snapshot. Any changed planning number requires a baseline correction sweep.
9. Publish the artifact with Step Summary and Final Planning Baseline Snapshot; stop at the Post-step Review Gate. Continuous mode does not apply beyond Step 06.

## Reference Tables

### Risk Band Reference

| Risk Band | Score | Guideline % |
|---|---|---|
| Low | 1-6 | 5-10% |
| Medium | 7-14 | 10-20% |
| High | 15-25 | 20-35% |

### Contingency Adjustment Reference

| Factor | Adjustment |
|---|---|
| Total Expected External Risk MD | Base from external risk register |
| Unquantified named uncertainty | 0-10% only with affected workstream, driver ID, and rationale; unknown-unknowns belong to Management Reserve |
| Customer / SME Readiness | 0-5% of Adjusted MD only for residual impact not already in Expected MD |
| Scope Confirmation Clarity | 0-5% of Adjusted MD only for residual impact not already in Expected MD |
| 3rd Party / Integration / Data Owner Risk | 0-5% of Adjusted MD only for residual impact not already in Expected MD |

### Scenario Formula Reference

Planning heuristic, not statistically validated percentiles. Use these formulas consistently and disclose any exception with rationale. All percentages are applied to Step 05 Adjusted MD and all ranges remain within approved baseline scope. Recommended Contingency must be non-negative. P25 caps its allowance at Recommended Contingency so a low-risk estimate cannot have P25 > P50.

Select P50 for internal planning or P75 for conservative commitment. Selected Commitment Uplift = selected range effort − P50. Delivery Contingency = Recommended Contingency + Selected Commitment Uplift. Delivery Baseline = Adjusted MD + Delivery Contingency = selected range effort. Management Reserve is calculated on that selected Delivery Baseline, not automatically on P50.

| Scenario | Formula | Usage |
|---|---|---|
| P25 Best | `Adjusted MD + min(Recommended Contingency MD, max(0.5 × Recommended Contingency MD, 5% × Adjusted MD))` | Optimistic internal view. |
| P50 Most Likely | `Adjusted MD + Recommended Contingency MD` | Internal planning / T&M staffing baseline. |
| P75 Conservative | `P50 + max(0.5 × Recommended Contingency MD, 5% × Adjusted MD)` | Fixed-scope delivery commitment / planning baseline; excludes Management Reserve. |
| P90 Worst | `P75 + max(0.5 × Recommended Contingency MD, 10% × Adjusted MD)` | Sponsor reserve discussion. |

### Management Reserve Reference

| Risk Appetite / Context | Default Reserve | Rule |
|---|---:|---|
| Low risk appetite / fixed-scope commitment | 10% of Delivery Baseline | Sponsor-controlled; not delivery team effort unless released. |
| Medium risk appetite / normal enterprise delivery | 7.5% of Delivery Baseline | Default when risk appetite is unclear and user allows defaults. |
| High risk appetite / T&M planning | 5% of Delivery Baseline | Keep visible but separate from delivery baseline. |
| Explicit sponsor policy | [policy %] | Use policy and cite source. |

## Risk Taxonomy

### Risk Taxonomy Reference

Use this reference to structure the Step 06 risk register. Include only applicable risks and keep the two top-level themes distinct (see Fixed Baseline/Scope `Risk taxonomy` row for the no-duplication rule).

| Top-Level Theme | Typical Risk Topic | Boundary Rule | Default Owner Pattern |
|---|---|---|---|
| Integration / External Dependency | [external data platform] integration contract/readiness | Technical integration contract, payload, writeback, sandbox, test data, readiness window. | [external data platform owner] / Architecture |
| Integration / External Dependency | Authentication/Authorization integration readiness | [enterprise IdP / SSO provider] and [identity/role source system] technical contracts, claims, role/data-scope source, test users, security evidence. Do not include critical workflow business routing here. | [identity/security owner] / [authorization source system owner] |
| Integration / External Dependency | Notification provider readiness | Provider, sender policy/domain, template integration, recipient source, retry/delivery/audit integration policy. Do not duplicate workflow notification requirement details. | [client IT / notification provider] / Business Owner |
| Integration / External Dependency | [client cloud landing zone/environment] / CAB / release readiness | Environment access, monitoring access, CAB/release calendar, production approval, security readiness. | [client infrastructure owner] / CAB / Security |
| Requirement Unconfirmed | Critical workflow / approval process / decision routing / state model details | Levels/states, routing conditions, approve/reject or equivalent decisions, route back/resubmit, cancel/withdraw, delegate/expire, SLA/escalation, notification, audit requirement. | Business Owner / [Product Owner] |
| Requirement Unconfirmed | [critical business rule/calculation] | Hierarchy, rounding, override, versioning, exception handling, ownership, approval treatment. | Business Owner / SME / Data Owner |
| Requirement Unconfirmed | [reporting/KPI definition] | KPI formula, aggregation level, chart/list behavior, filter/export expectation, threshold interpretation. | Business Owner / Data Owner / [Product Owner] |
| Requirement Unconfirmed | Data volume / NFR thresholds | Historical period, row volume, concurrency, export size, retention volume, performance/security thresholds. | Data Owner / Architecture / Security |
| Requirement Unconfirmed | Audit/retention/rollback/compliance lifecycle | Log detail, retention period, rollback evidence, lifecycle ownership, compliance evidence. Do not duplicate approval-flow business routing. | Business Owner / Compliance / Security |
| Requirement Unconfirmed | Contractual baseline boundary | Scope lock and warranty/support expectation boundary. Do not duplicate workflow or audit/compliance risks. | Sponsor / Procurement / Business Owner |

### Auto-Generation Guide — Canonical Patterns by Theme

Scan the approved TOR and dependencies using `Risk Taxonomy Reference`. Read [Risk pattern examples](risk-patterns.md) only when additional discovery prompts are needed; never create risks merely to fill a pattern list.

### Scoring Reconciliation (1-3 quick triage → 1-5 P×I baseline)

The canonical-pattern triage above uses a 1-3 Low/Medium/High shortcut for fast classification. The Step 06 risk register itself MUST use the 1-5 P×I scoring per the Scoring rule in Fixed Baseline / Scope. Map as follows when promoting a triaged pattern into the register:

| 1-3 Shortcut | 1-5 P / I Equivalent | Probability % |
|---|---|---|
| Low (1) | 1-2 | 10-30% |
| Medium (2) | 3 | 50% |
| High (3) | 4-5 | 70-90% |

Quick triage matrix (used to decide whether to include a candidate before scoring on 1-5):

| Likelihood × Impact | Low (1) | Medium (2) | High (3) |
|---|---|---|---|
| **Low (1)**    | 1 → Low | 2 → Low | 3 → Medium |
| **Medium (2)** | 2 → Low | 4 → Medium | 6 → High |
| **High (3)**   | 3 → Medium | 6 → High | 9 → High |

After triage, set explicit P and I values on the 1-5 scale, compute Score = P × I, and apply the official Risk Band Reference (Low 1-6 / Medium 7-14 / High 15-25).

### When NOT to add a risk

- Risks not anchored in the TOR, e.g. "team morale risk" or "office relocation risk".
- Risks that duplicate another. Collapse them into one.
- Risks whose only mitigation is "monitor", which is not a mitigation.
- "Risk of failure" is too generic; decompose it to a specific cause.
- Internal delivery management factors — see Risk eligibility (Fixed Baseline/Scope) and the Excluded — Internal Delivery table.
- Duplicate monetary or effort allowances. Keep named risks visible even when funded by contingency; count their impact only once.

## Output Contract

Create/update `output/step_06_risk_contingency.md` using this schema. Replace placeholders, write `N/A — [reason]` for sections that do not apply, and reconcile every number to the Step 05 adjusted baseline.

```markdown
# Step 06 - Risk, Contingency & Planning Baseline: [PROJECT_NAME]

**Source**: `output/step_05_resource_plan.md` [approved revision] + `output/step_04_sizing_estimate.md` [approved revision]
**Approved Baseline Scope**: SG1-only / SG1+SG2 / TBD
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [ผู้อนุมัติ/วันที่ หรือ authorization/วันที่ ตาม explicit-approval principle]

## Step Summary

- External risk counts are in the Final Planning Baseline Snapshot.
- Risk taxonomy: exactly two themes, Integration / External Dependency and Requirement Unconfirmed.
- Scope basis: [SG1-only / SG1+SG2]. Contingency, P25-P90, Delivery Baseline, Management Reserve and Planning Total are in the Final Planning Baseline Snapshot (canonical numeric block for Step 06); do not restate them here.
- Key validity condition: [condition]; confidence is in the Snapshot.

## Final Planning Baseline Snapshot

- Version: [VERSION]; Date: [DATE_YYYY-MM-DD]; Approved Scope: [SG1-only/SG1+SG2/TBD].
- Raw MD: [N] (Step 04, unchanged); Duration: [N] weeks/months; Peak/Avg FTE: [N] / [N] (from Step 05).
- Integration Count: [N]; Risk Count: [N] total (High=[N], Medium=[N], Low=[N]).
- Selected Delivery Basis: [P50/P75 + decision source]. Recommended Contingency [N] + Selected Commitment Uplift [N] = delivery Contingency [N].
- Delivery Baseline: Adjusted MD [N] + delivery Contingency [N] = [N]; Management Reserve [N] remains separate; Planning Total = Delivery Baseline + Management Reserve = [N].
- P75 Planning Baseline: [N] MD, excluding Management Reserve unless explicitly released.
- Range: P25=[N], P50=[N], P75=[N], P90=[N].
- Top risks: [ชื่อสั้นพร้อมผลกระทบ; IDs อยู่ §1].
- Risk themes: [Integration / External Dependency count] and [Requirement Unconfirmed count].
- Confidence: [L/M/H].
- Re-estimation triggers: [summary].
- Baseline vs scenario note: [no cap scenario / scenario kept separate].

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 06 Risk, Contingency & Planning Baseline**

Please review:
- Key outputs: external risk register, contingency basis, scenario range, delivery baseline, management reserve, cross-step consistency check, findings, re-estimation triggers.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: Risk / MD / Timeline / Scenario.

Reply options:
- `approve Step 06` = lock the final planning baseline and complete the workflow.
- `revise Step 06: ...` = update risk/contingency before proceeding.

## ภาคผนวก

## Approved Inputs Consumed

| Input | Value | Note |
|---|---:|---|
| Raw MD | [N] | From Step 04, unchanged |
| Adjusted MD | [N] | From Step 05 |
| Duration | [N] | From Step 05 planning baseline |
| Peak / Average FTE | [N] / [N] | From Step 05 |
| Critical Path | [text] | From Step 05 |
| Integration Count | [N] | From Step 04 §3 / Step 02 handoff |
| Step 05 Resource Constraints | [summary/N/A] | Carry as context only; do not count as Step 06 risks unless driven by external party/customer/vendor decision. |
| Open Assumptions | [N] | From Step 03-05 |

## 1. External Risk Register

Only include risks caused by external parties, stakeholder decisions, customer readiness, vendor/3rd-party readiness, regulator/compliance, integration/data owners, environments/access, procurement/contract, or external timeline dependencies. Do not include internal delivery staffing/resource availability issues.

Risk register must use exactly two top-level themes. Use `### Theme A: Integration / External Dependency` for external technical readiness/contracts, and `### Theme B: Requirement Unconfirmed` for stakeholder decisions and requirement details. If critical workflow / approval process / decision routing / state model details are not confirmed, create a standalone Requirement Unconfirmed risk.

### Theme A: Integration / External Dependency

| Risk ID | External Cause / ความเสี่ยง | Top-Level Theme | P | I | Score | Band | Prob % | Effort Impact MD | Expected MD | Owner | Mitigation / Decision Needed |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|
| RSK-01 | [stakeholder-readable cause + impact, e.g. external integration contract/readiness not confirmed] | Integration / External Dependency | [1-5] | [1-5] | [P×I] | Low/Medium/High | [10/30/50/70/90%] | [N] | [prob × impact MD] | [external owner] | [stakeholder-readable action/decision/date] |

### Theme B: Requirement Unconfirmed

| Risk ID | External Cause / ความเสี่ยง | Top-Level Theme | P | I | Score | Band | Prob % | Effort Impact MD | Expected MD | Owner | Mitigation / Decision Needed |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|
| RSK-05 | [stakeholder-readable cause + impact, e.g. critical workflow / approval process / decision routing / state model not confirmed: levels/states, routing conditions, approve/reject or equivalent decisions, route back/resubmit, cancel/withdraw, delegate/expire, SLA/escalation, notification, audit requirement] | Requirement Unconfirmed | [1-5] | [1-5] | [P×I] | Low/Medium/High | [10/30/50/70/90%] | [N] | [prob × impact MD] | Business Owner / [Product Owner] | Run workflow decision workshop; include Process Owner, Security/Compliance, and IT/SA as supporting stakeholders. |

| **Total** |  |  |  |  |  |  |  | **[N]** | **[N]** |  | Expected MD = Prob % × Effort Impact MD for external risks only. |

## 2. Contingency Basis

| Item | Formula / Basis | MD | % of Adjusted MD | Rationale |
|---|---|---:|---:|---|
| Total Expected External Risk MD | Sum(Expected Risk MD) | [N] | [x%] | From external risk register only. |
| Unquantified named uncertainty | Adjusted MD × [x% or 0] | [N] | [x%] | [driver ID + workstream + residual impact not already counted] |
| Customer / SME Readiness Adjustment | Adjusted MD × [x%] | [N] | [x%] | [rationale] |
| Scope Confirmation Adjustment | Adjusted MD × [x%] | [N] | [x%] | [rationale] |
| 3rd Party / Integration / Data Owner Adjustment | Adjusted MD × [x%] | [N] | [x%] | [rationale] |
| **Recommended Contingency** | Expected External Risk MD + Adjustment MD | **[N]** | **[x%]** | Validate against risk band. |

### Ambiguity-to-Contingency Mapping

| Driver ID | Ambiguity / Risk Driver | Affected Workstream | Related Risk | Treatment | MD / Range Impact | Baseline Classification |
|---|---|---|---|---|---:|---|
| ASM/DEC/RSK-XX | [uncertainty driver] | Integration / Data / NFR / UAT / Timeline | RSK-XX | Delivery contingency / Management reserve / Scenario delta / Discovery | [N] | Delivery Baseline / Management Reserve / Scenario Delta |

### Risk Band Validation

| Metric | Value | Result | Note |
|---|---:|---|---|
| Highest Risk Band | Low/Medium/High | Pass/Warning | [note] |
| Risk Count by Band | High=[N] / Medium=[N] / Low=[N] | Pass/Warning | [note] |
| Guideline % | [range] | Pass/Warning | [note] |
| Recommended Contingency % | [x%] | Pass/Warning | [note] |

## 3. Scenario Range

Baseline risk scenarios below apply to approved baseline scope only. Duration changes are scenario assumptions with named critical-path drivers, not automatic -5%/+10%/+25% rules. Keep Step 05 duration unchanged as the base. A proposed commitment duration or extra capacity needs an upstream Step 05 revision before sign-off.

Formula source: use `Scenario Formula Reference`. `P75 Planning Baseline` excludes Management Reserve; `Planning Total` is reported separately as Delivery Baseline + Management Reserve.

| Scenario | Confidence | Scope | Duration | Effort Formula | Effort MD | Usage |
|---|---|---|---|---|---:|---|
| Best | P25 | Approved baseline scope, low risk realization | [Step 05 base + justified scenario delta] | `Adjusted MD + min(Recommended Contingency, max(0.5 × Recommended Contingency, 5% × Adjusted MD))` | [N] | Optimistic internal view |
| Most Likely | P50 | Approved baseline scope, normal risk realization | Step 05 base | `Adjusted MD + Recommended Contingency` | [N] | Internal planning / T&M staffing baseline |
| Conservative | P75 | Approved baseline scope, conservative risk allowance | [base + justified scenario delta] | `P50 + max(0.5 × Recommended Contingency, 5% × Adjusted MD)` | [N] | Fixed-scope delivery commitment; excludes Management Reserve |
| Worst | P90 | Approved baseline scope, higher risk allowance | [base + justified scenario delta] | `P75 + max(0.5 × Recommended Contingency, 10% × Adjusted MD)` | [N] | Sponsor reserve discussion |

## 4. Delivery Baseline / Management Reserve

Selected delivery basis: [P50 / P75 + decision source]. Reconcile the selected commitment to §3. Do not call P50 the Delivery Baseline while presenting P75 as the same commitment.

| Category | MD / Duration | % | Note |
|---|---:|---:|---|
| Adjusted Effort (Step 05) | [N] MD | [x%] | Source of truth from Step 05 |
| Recommended Contingency | [N] MD | [% of Adjusted MD] | P50 expected-risk allowance from §2 |
| Selected Commitment Uplift | [N] MD | [% of Adjusted MD] | Selected range effort − P50; 0 when P50 selected |
| Contingency | [N] MD | [% of Adjusted MD] | Recommended Contingency + Selected Commitment Uplift |
| **Delivery Baseline** | **[N] MD / [Step 05 duration; feasibility finding if uplift unstaffed]** | **[% of Adjusted MD]** | Adjusted + delivery Contingency = selected range effort |
| Management Reserve | [N] MD | [% of Delivery Baseline] | Sponsor-controlled unknown-unknowns; separate from P75; no automatic schedule conversion |
| **Planning Total** | **[N] MD** | **[% of Adjusted MD]** | Delivery Baseline + Management Reserve; reserve does not automatically add calendar duration |

## 5. Cross-step Consistency Check

| Check | Result | Note |
|---|---|---|
| Scope in/out clear from approved baseline | Pass/Warning/Fail | [note] |
| Scope maps to WBS | Pass/Warning/Fail | [note] |
| Assumptions documented | Pass/Warning/Fail | [note] |
| Architecture constraints captured | Pass/Warning/Fail | [note] |
| Integrations identified and sized | Pass/Warning/Fail | [note] |
| Intake scope and architecture baseline approved or clearly assumed | Pass/Warning/Fail | [note] |
| WBS complete | Pass/Warning/Fail | [note] |
| Sizing method and complexity scoring complete | Pass/Warning/Fail | [note] |
| Effort and resource plan trace Step 04 -> 05 -> 06 | Pass/Warning/Fail | [note] |
| Team plan feasible | Pass/Warning/Fail | [note] |
| Resource baseline complete | Pass/Warning/Fail | [note] |
| Risk register complete | Pass/Warning/Fail | [note] |
| Contingency has effort/schedule rationale | Pass/Warning/Fail | [note] |
| Best / Most Likely / Worst range complete | Pass/Warning/Fail | [note] |
| Numbers consistent across steps | Pass/Warning/Fail | [note] |
| Screen count vs scope reconciled | Pass/Warning/Fail | [note] |
| API count vs integration reconciled | Pass/Warning/Fail | [note] |
| Inventory cross-check vs detailed estimate delta <=30% | Pass/Warning/Fail | [note] |
| TOR/RFP clarity score reflected in confidence | Pass/Warning/Fail | [note] |
| High-impact ambiguity triaged, decided, or mapped | Pass/Warning/Fail | [note] |
| Baseline and scenario deltas separated | Pass/Warning/Fail | [note] |
| Assumption and decision due dates not overdue without findings | Pass/Warning/Fail | [note] |
| Contingency maps to named ambiguity, risk, requirement, assumption, or decision IDs | Pass/Warning/Fail | [note] |

## Findings

| Finding ID | Severity | Finding | Recommendation | Baseline Impact |
|---|---|---|---|---|
| F-01 / No critical findings | H/M/L | [issue or No critical findings] | [recommendation/N/A] | Scope / MD / Timeline / Resource / Risk / Scenario / N/A |

## 6. Re-estimation Triggers

| Trigger | Threshold | Action | SLA | Owner |
|---|---|---|---|---|
| Customer-confirmed scope growth | >10% or any contractual scope change | Re-estimate | 5 days | PM / BA / Sponsor |
| Customer / 3rd-party decision delay | >2 weeks, missed approval-flow/formula/KPI/design sign-off, or impacts critical path | Re-baseline impact assessment | 3 days | PM / Sponsor / External Owner |
| New external integration | Any | Impact assessment | Immediate | SA / Integration Owner |
| External environment/API/data readiness slips | Any critical dependency | Re-plan affected phase | 3-5 days | PM / External Owner |
| High-impact external assumption invalid | Any | Re-estimate affected scope | 3-5 days | PM / Owner |

## Open Questions / Assumptions

| ID | Related Risk | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|---|
| OQ-01 | RSK-XX | [question/assumption] | [stakeholder-readable why/impact] | [owner] | Before baseline sign-off |

## Verification Fallback

Record the verification method, checked values, and limitations. Recompute arithmetic independently from source rows. Excel formula text or a successful file write does not prove recalculated results. If no Excel-compatible calculation engine or required validator is available, label results `Not recalculated` or `Not verified`, show the independent numeric reconciliation, and keep affected checks Warning/Fail. An unstaffed selected contingency requires a Step 05 capacity revision or an explicit feasibility finding; do not label that plan ready for commitment.

## Internal Review

The §5 Cross-step Consistency Check (23 Required Final Checks) is the final internal consistency review and stays row by row. This section covers only the Step 06-specific checks below (contingency rationale and ID mapping are §5 checks 13 and 23), rendered per [reviewer-first guidance](../../principle-orbit-reviewer-first/SKILL.md) (one `Pass:` line; rows only for Warning/Fail).

| Check | Result | Note |
|---|---|---|
| Step 05 consumed without changing Adjusted MD | Pass/Warning/Fail | [note] |
| Risk register grouped by exactly two themes | Pass/Warning/Fail | [note] |
| Risk register includes external risks only | Pass/Warning/Fail | [note] |
| Critical workflow risk explicit if unconfirmed | Pass/Warning/Fail | [note] |
| Risk descriptions are stakeholder-readable/self-contained | Pass/Warning/Fail | [note] |
| P25/P50/P75/P90 are baseline risk scenarios | Pass/Warning/Fail | [note] |
| Delivery Baseline / Reserve / Planning Total reconcile | Pass/Warning/Fail | [note] |
| Final planning baseline ready | Pass/Warning/Fail | [note] |


```

## Validation Checklist

Evaluate the full `## 5. Cross-step Consistency Check` and the Step 06-specific `Internal Review` against the Fixed Baseline / Scope and Output Contract. All 23 final checks, findings, selected commitment feasibility, and verification limitations must be recorded before sign-off.
