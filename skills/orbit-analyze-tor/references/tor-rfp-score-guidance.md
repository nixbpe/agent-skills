# TOR/RFP Score Guidance

Reference for Step 00 TOR/RFP clarity scoring. Use with [Step 00 contract](contract.md) when producing the canonical **TOR/RFP Clarity Score** section, whose Step 00 output alias is `TOR_RFP_Clarity_Score`, plus ambiguity triage, decision packets, and Step 01 handoff.

Normative precedence: this file expands the scoring criteria. If guidance conflicts with [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) or [Step 00 contract](contract.md), follow [กฎร่วมของ action](../SKILL.md#กฎที่ต้องอ่าน) for shared rules and the Step 00 command contract for output structure.

## Purpose

Score TOR/RFP readiness for estimation, not solution quality. The score measures how safely the team can convert source material into scope baseline, assumptions, scenarios, and downstream estimation artifacts.

Do not block every missing detail. Score the evidence, triage ambiguity, ask only high-impact questions, and convert medium/low gaps into assumptions, defaults, scenarios, or open items.

## Scoring Scale

| Score | Meaning | Evidence Standard | Treatment |
|---:|---|---|---|
| 5 | Clear / confirmed | Explicit TOR/RFP statement or approved artifact with owner, boundary, and acceptance implication | Use as baseline fact |
| 4 | Mostly clear | Requirement is stated but minor detail is missing; defensible default exists | Baseline with labelled assumption/default |
| 3 | Partially clear | Intent is visible but count, owner, boundary, priority, or acceptance detail is incomplete | Baseline only with assumption; map risk or open question |
| 2 | Weak / ambiguous | Topic is mentioned but implementation meaning, scope, or owner is unclear | Scenario, high-impact question, or discovery item |
| 1 | Missing / contradictory | No usable evidence, conflicting statements, or source/version uncertainty | Do not commit baseline; ask or mark discovery needed |

## Average Score Action

| Average | Confidence | Baseline Action | Required Handling |
|---:|---|---|---|
| 4.0-5.0 | High | Proceed as baseline with normal assumptions | Log minor assumptions only |
| 3.0 to <4.0 | Medium | Proceed with assumption log and risk mapping | Ask only top high-impact blockers |
| 2.0 to <3.0 | Low | Proceed only with explicit confidence note and scenario deltas | Separate baseline vs scenario; owner/needed-by required |
| <2.0 | Very Low | ROM or discovery-first only | Do not present as fixed baseline |

## 5W1H Completeness Cross-Check

Run 5W1H as an evidence check inside each clarity dimension before assigning the dimension score. 5W1H is not a separate score and must not become a 10th clarity dimension. Not every lens applies to every dimension; use only the relevant prompts listed under each dimension.

5W1H handling rules:

- If a 5W1H gap affects scope, MD, timeline, resource plan, risk, baseline, scenario, or contractual commitment, classify it as High ambiguity.
- If a 5W1H gap has a defensible benchmark or default, record it as `Assumption:` or `Default:` with owner, impact, confidence, fallback, and baseline treatment.
- If a 5W1H gap prevents understanding the estimation objective or scope boundary, lower the mapped dimension score and create a decision packet.
- Do not calculate a separate 5W1H average. The official score remains the arithmetic average of the 9 TOR/RFP clarity dimensions.

## Dimension Rubrics

### 1. Business Objective

5W1H evidence check:

- Who: sponsor, business owner, decision maker, success owner.
- Why: business goal, pain point, expected value, success criteria.
- What: target outcome, priority, constraint driver.
- When: business deadline if the objective is date-driven.

If Why is missing, maximum score is 3. If sponsor/owner is missing and affects approval or baseline commitment, create high-impact ambiguity.

| Score | Criteria |
|---:|---|
| 5 | Business goal, success criteria, priority, target outcome, and sponsor intent are explicit |
| 4 | Goal and priority are clear; success metric or measurable outcome is partly missing |
| 3 | General business intent exists but outcome, priority, or decision driver is vague |
| 2 | Multiple possible objectives or conflicting priorities appear without resolution |
| 1 | Objective is absent or source only lists activities/features without business goal |

Impact mapping: scope boundary, MVP decision, scenario choice, executive recommendation.

High-impact questions: objective priority, must-have outcome, success criteria, commitment driver.

Default handling: if objective is broad but usable, label assumption and keep confidence Medium/Low.

### 2. Scope Boundary

5W1H evidence check:

- Who: affected user groups, business owner, scope approver.
- What: in-scope, out-of-scope, modules, journeys, deliverables, exclusions.
- Where: channels, sites, environments, usage context.
- When: phase, MVP/core/full-scope timing, future-release boundary.
- Why: priority reason for inclusion/exclusion.

If What or phase boundary is unclear, maximum score is 3. If optional/MVP/budget-fit scope is mixed into baseline, create decision packet or scenario split.

| Score | Criteria |
|---:|---|
| 5 | In-scope/out-of-scope, phase, modules, channels, user journeys, and exclusions are explicit |
| 4 | Core scope is clear; optional/future items need minor classification |
| 3 | Main modules are listed but phase boundary, exclusions, or optional scope is incomplete |
| 2 | Scope mixes baseline, MVP, optional, budget-fit, and future phase without separation |
| 1 | No defensible boundary; baseline cannot be separated from wishlist or discovery |

Impact mapping: WBS completeness, baseline vs scenario, change-control triggers.

High-impact questions: full scope vs core, confirmed versus optional scope inclusion, MVP vs baseline, explicit exclusions.

Default handling: never silently convert optional/MVP/budget-fit scope into baseline.

### 3. Functional Inventory

5W1H evidence check:

- Who: actors executing each workflow and role-specific variants.
- What: features, screens, APIs, reports, business rules, CRUD/actions.
- How: workflow steps, approval flow, exception flow, validation rules.
- Where: channel or module where each function is used.
- When: event trigger, frequency, batch/real-time behavior if relevant.

If What inventory is broad capability wording without count/detail, maximum score is 3. If How changes effort materially, create high-impact ambiguity or scenario.

| Score | Criteria |
|---:|---|
| 5 | Features, workflows, screens, APIs, reports, business rules, and CRUD/approval behavior are enumerated |
| 4 | Feature list is clear; some counts or low-level rules require assumptions |
| 3 | Functional areas are known but screen/API/report counts or workflow depth are incomplete |
| 2 | Requirements are described as broad capabilities with unclear transaction flow or inventory |
| 1 | No usable functional inventory for FE/BE/QA estimation |

Impact mapping: FE/BE/QA MD, screen/API count, WBS coverage, test scope.

High-impact questions: number of screens/reports, workflow variants, approval levels, API exposure.

Default handling: use benchmark assumptions only when labelled and traceable; otherwise scenario/discovery.

### 4. Integration Clarity

5W1H evidence check:

- Who: source/target system owner, interface spec owner, test environment owner.
- What: systems, data objects, payload, API/file/message scope.
- How: protocol, auth, direction, error handling, retry/reconciliation pattern.
- When: frequency, trigger, cutover/dependency date.
- Where: environment, network boundary, endpoint/data residency context.

If system owner or interface pattern is missing, maximum score is 3. If protocol/direction is unclear and affects MD/risk, create `DEC-XX` with Type `Integration`.

| Score | Criteria |
|---:|---|
| 5 | Systems, direction, protocol, data objects, frequency, auth, ownership, test environment, and error handling are clear |
| 4 | Systems and protocol are clear; minor mapping or test detail is missing |
| 3 | Integration targets are known but protocol, owner, payload, or frequency is incomplete |
| 2 | External systems are mentioned without interface pattern or responsibility split |
| 1 | Integration existence is uncertain or contradictory |

Impact mapping: INT MD, BE/QA effort, dependency risk, contingency, schedule risk.

High-impact questions: real-time vs batch, API/file/message, owner of spec, environment availability, data contract.

Default handling: if unclear, create `DEC-XX` with Type `Integration`; do not assume real-time API as default without rationale.

### 5. Data & Migration

5W1H evidence check:

- Who: source data owner, cleansing owner, migration approver, reconciliation owner.
- What: entities, volume, data quality, mapping, historical scope.
- How: migration/import method, cleansing, reconciliation, rollback, cutover.
- When: migration window, trial run, freeze period, go-live cutover.
- Where: source/target systems, data location, retention/residency constraint.

If source, volume, or cleansing owner is missing, maximum score is 3. If cleansing/reconciliation responsibility is unclear, baseline must label assumption and keep cleansing as scenario delta.

| Score | Criteria |
|---:|---|
| 5 | Source systems, volume, entities, cleansing owner, mapping, migration method, reconciliation, rollback, and cutover are clear |
| 4 | Entities and source are clear; volume or reconciliation needs assumption |
| 3 | Migration/import need is known but volume, quality, or cleansing responsibility is incomplete |
| 2 | Data movement is implied but source, owner, or cutover scope is unclear |
| 1 | No reliable data/migration evidence despite likely dependency |

Impact mapping: DE/DBA/QA MD, cutover plan, contingency, P75/P90 risk driver.

High-impact questions: one-time vs recurring import, cleansing owner, volume, reconciliation criteria, rollback.

Default handling: baseline may assume client-provided cleansed data only if labelled and scenario delta exists for cleansing.

### 6. NFR

5W1H evidence check:

- Who: security/compliance owner, operations owner, performance acceptance owner.
- What: performance, availability, security, audit, compliance, backup, DR, monitoring.
- How: measurement method, test approach, control requirement, operational model.
- When: peak period, SLA window, backup/DR timing, support hours.
- Where: deployment environment, data residency, network/security boundary.
- Why: regulatory, contractual, operational, or user-experience driver.

If NFRs are generic adjectives without measurable target, maximum score is 3. If compliance/security scope may affect architecture or timeline, create high-impact ambiguity.

| Score | Criteria |
|---:|---|
| 5 | Performance, availability, security, audit, compliance, scalability, backup, DR, monitoring, and support NFRs are measurable |
| 4 | Major NFR categories are stated; some thresholds or measurements need assumptions |
| 3 | NFR topics are mentioned but thresholds, environment, or acceptance criteria are incomplete |
| 2 | NFRs are generic phrases such as secure, fast, scalable, compliant without measurable target |
| 1 | NFRs are absent or conflict with scope/timeline constraints |

Impact mapping: architecture complexity, DevOps/QA effort, security/performance scope, risk reserve.

High-impact questions: availability target, response time, concurrent users, audit logging, compliance, DR/RPO/RTO.

Default handling: generic NFRs become assumptions; formal performance/security testing is scenario unless confirmed.

### 7. Users & Roles

5W1H evidence check:

- Who: actor groups, approvers, admins, internal/external users, support users.
- What: permissions, role capabilities, workflow ownership, admin functions.
- How: approval hierarchy, delegation, RBAC/ABAC, segregation of duties.
- Where: channels, departments, locations, external portals.
- When: user lifecycle events, onboarding/offboarding, approval timing.

If role groups are listed but permissions/approval paths are unclear, maximum score is 3. If external users or approval workflow are implied, do not assume simple RBAC.

| Score | Criteria |
|---:|---|
| 5 | Actor groups, permissions, workflow ownership, approval hierarchy, user volume, and admin roles are clear |
| 4 | Main roles are clear; minor permission matrix or volume detail is missing |
| 3 | User groups are listed but permissions, approval paths, or volumes are incomplete |
| 2 | Users are broadly described without role-based behavior or ownership |
| 1 | No usable user/role evidence |

Impact mapping: screen complexity, RBAC, workflow variants, QA scenarios, UAT ownership.

High-impact questions: role matrix, approver levels, internal/external users, admin functions, user volume.

Default handling: do not assume simple RBAC if approval workflow or external users are implied.

### 8. Acceptance/UAT

5W1H evidence check:

- Who: UAT owner, sign-off authority, tester groups, defect decision owner.
- What: acceptance criteria, test scenarios, test data, severity rules, exit criteria.
- How: UAT process, defect triage, retest, sign-off, deployment acceptance.
- When: UAT cycles, entry/exit dates, sign-off deadline, hypercare transition.
- Where: UAT environment, test data source, user location/channel if relevant.

If UAT owner or acceptance criteria are missing, maximum score is 3. If acceptance ambiguity may extend defect cycles or support effort, create open item or risk.

| Score | Criteria |
|---:|---|
| 5 | Acceptance criteria, UAT owner, test cycles, defect severity, sign-off process, test data, and entry/exit criteria are clear |
| 4 | UAT owner and sign-off are clear; detailed criteria or data setup needs assumptions |
| 3 | UAT is expected but criteria, cycles, or owner are incomplete |
| 2 | Acceptance is generic and may expand defect/support effort |
| 1 | No acceptance/UAT evidence for delivery closure |

Impact mapping: QA MD, UAT support, defect cycle, timeline, warranty/handover readiness.

High-impact questions: UAT owner, number of cycles, acceptance criteria source, test data owner, sign-off authority.

Default handling: if unclear, assume standard SIT/UAT support and log risk for extended defect cycles.

### 9. Timeline Constraint

5W1H evidence check:

- Who: sponsor/date owner, dependency owner, approval/procurement owner.
- What: target milestones, fixed commitments, dependency gates, deliverables by date.
- When: kickoff, design, development, UAT, go-live, blackout, handover.
- How: phased release, parallel work, staffing compression, dependency management.
- Why: regulatory, business launch, contract, budget cycle, operational event.

If deadline is fixed but scope trade-off is unclear, maximum score is 3. If timeline is used as an effort cap, separate it as scenario or constraint, not reduced baseline effort.

| Score | Criteria |
|---:|---|
| 5 | Target dates, dependencies, blackout windows, procurement/approval gates, and go-live constraint are explicit |
| 4 | Target go-live is clear; intermediate gates or blackout detail needs assumptions |
| 3 | Desired timeline exists but dependency dates or feasibility constraints are incomplete |
| 2 | Timeline is aggressive/implicit without scope/resource trade-off clarity |
| 1 | No usable timeline or conflicting deadline statements |

Impact mapping: resource plan, staffing compression, critical path, phase/scenario recommendation.

High-impact questions: fixed vs target date, blackout, dependency readiness, procurement window, phased go-live acceptance.

Default handling: treat deadline as planning constraint, not effort reduction. Use scenario if scope must be cut to fit.

## Ambiguity Triage Rules

| Level | Trigger | Step 00 Action |
|---|---|---|
| High | Affects scope, MD, timeline, resource plan, risk, baseline, scenario, or contractual commitment | Ask as `DEC-XX` or Open_HighImpact; max 3-5 total |
| Medium | Affects sizing but defensible benchmark/default exists | Record `ASM-XX` or `Default:` with impact, owner, confidence, fallback |
| Low | Implementation detail with limited baseline effect | Record note/assumption; do not block Step 00 |

Use decision packets for finite high-impact ambiguity. Each packet must include context, options, baseline impact, and default/fallback. Ask packets through `Open_HighImpact` and the asking tool; once answered, record the outcome only in `### Decision_Outcomes`. Record the triage level on the `Applied_Defaults` row (`Triage Level`) instead of a separate triage table.

## Evidence Rules

| Evidence Type | Use As | Rule |
|---|---|---|
| TOR/RFP explicit text | Confirmed | Cite source/version or section when available |
| Approved meeting note / stakeholder answer | Confirmed | Mark source as approved artifact or stakeholder decision |
| Industry/default benchmark | Default | Label `Default:` with rationale and impact if false |
| Agent inference | Assumption | Label `Assumption:` with owner, confidence, baseline treatment |
| Conflicting statements | Open / Decision | Do not average away conflict; ask or scenario split |

## Output Compactness Rules

- Keep each dimension evidence/gap to one concise phrase.
- Keep estimate impact tied to downstream artifact: scope, WBS, FE/BE/QA, INT, migration, architecture, UAT, resource, risk, scenario.
- Average score must be the arithmetic average of all 9 dimensions. Classify the unrounded average and display one decimal place; a display rounded to 4.0 does not upgrade an average below 4.0. An explicitly excluded/not-applicable dimension scores 5 only when the source confirms its exclusion; source silence is not evidence of N/A.
- Do not include document-control noise, glossary, citation appendix, architecture options, WBS, effort sizing, resource plan, risk range, pricing, or rate card.
- If average is below 3.0, explicitly state confidence and whether output is baseline, ROM, scenario, or discovery-first.

## Step 00 Decision Flow

```text
Read TOR/RFP source
  -> run relevant 5W1H evidence check inside each dimension
  -> score each of 9 dimensions from evidence
  -> compute average and confidence/action
  -> list unclear items
  -> classify High / Medium / Low
  -> ask only top 3-5 high-impact finite decisions
  -> convert remaining gaps to assumptions/defaults/scenarios/open items
  -> produce Step01_Handoff
  -> stop at the review gate; only the router may authorize the next action
```

## Validation Checklist

| Check | Pass Rule |
|---|---|
| 5W1H checked per dimension | Relevant Who/What/When/Where/Why/How prompts are considered before assigning each dimension score |
| 9 dimensions scored | Every required dimension has score 1-5, evidence/gap, and estimate impact |
| Average mapped | Average maps to confidence/action table |
| Evidence labelled | Facts, defaults, assumptions, and stakeholder decisions are distinguishable |
| High-impact ambiguity handled | Top 3-5 blockers asked/logged with owner and needed-by |
| Medium/low gaps not over-asked | Defensible gaps converted to assumption/default/scenario/note |
| Baseline/scenario separated | Optional, MVP, budget-fit, and discovery items are not silently included |
| No commercial leakage | Budget is constraint context only; no rate card, pricing, or cost build-up |
