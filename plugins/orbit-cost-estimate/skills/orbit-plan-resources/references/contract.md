# Resource planning contract

Read the [action guide](../SKILL.md) and every principle it requires before executing this contract, including direct invocation. `output/` paths resolve from the working project. Bundled Markdown links resolve from this installed skill. Examples and template rows are not project evidence. Preserve mandatory quality gates; approval cannot bypass a failed gate. Produce only this action’s artifact and stop.

## Fixed Baseline / Scope

| Area | Rule |
|---|---|
| Purpose | MUST generate Step 05 resource planning from approved Step 04 Raw MD. Raw MD is immutable input: do not overwrite, re-size, or re-estimate effort. |
| Input | Approved `output/step_04_sizing_estimate.md` and `output/step_04_sizing_review.md` together, approved Step 03 WBS/counts, Step 04 bucket breakdown, feature/subfeature basis, dependencies, and sizing assumptions. |
| Output | MUST create/update `output/step_05_resource_plan.md`. |
| Prerequisite | MUST read both approved Step 04 estimate and companion review before resource planning. |
| Missing prerequisite | MUST reject Step 05 execution and ask user to run/approve [orbit-size-effort](../../orbit-size-effort/references/contract.md) first. |
| Guidance | MUST apply [Estimation Calibration Guidance](../../principle-orbit-effort-accounting/references/estimation-calibration.md) for PM/Total and (SA+BA)/Total sanity checks and [Role Boundary Guidance](../../principle-orbit-effort-accounting/references/roles.md) for role ownership. Gate limits, asking tool, `Assumption:`/`Default:` labelling, language, baseline/scenario separation, and no-rate-card rules follow [shared principles loaded by this action](../SKILL.md#กฎที่ต้องอ่าน). |
| Next command | SHOULD hand off to [orbit-assess-risk](../../orbit-assess-risk/references/contract.md). |
| In scope | Productivity inputs, adjusted effort, feature/backlog analysis & prioritization, weekly resource matrix, weekly project timeline, resource constraints, Step 06 handoff. |
| Out of scope | MUST NOT change Step 04 Raw MD, re-size scope, or produce Step 06 contingency, P25/P50/P75/P90 range, management reserve, planning total, or any commercial output. |
| Productivity | Apply focus factor, rework, and buffer by project type from the Productivity Reference; role-level rework/buffer treatment is in the Rework Applicability Reference. |
| Capacity constants | Define once and reuse the constants and formulas in the Productivity Reference; the matrix reconciles Effective MD, not Nominal MD. |
| PM MD | Owned by Step 05 and calendar/resource-derived; Step 04 has no PM role and MUST NOT be used as a PM baseline. Cross-check against 10-15% of adjusted delivery total; if outside, record rationale/treatment. Do not force PM by percentage or revise Step 04 to fit. |
| Reconciliation | Weekly delivery matrix plus separate warranty schedule Effective MD by role MUST reconcile to Adjusted MD (not Step 04 Raw Grand Total) within 95-105%. Outside the band, adjust allocation/duration or flag the plan as infeasible before publishing. |
| Backlog prioritization | Produce Feature/Backlog Analysis & Prioritization before the resource matrix, ranking by dependency, critical path, sizing, business priority, and risk (Backlog Prioritization Reference). Timeline and mini-phasing MUST consume this ranking; critical-path features are sequenced first. |
| Phase bands | Week columns `W1...Wn` MUST be grouped under named phase bands (Foundation / BUILD / QA / Go-Live / Hypercare or project-specific equivalents) via the `Phase Band` row at the top of the §4 matrix; reuse the same bands in the timeline. When BUILD is split, label sub-bands `BUILD-MP1`, `BUILD-MP2`, ... in that row. QA band covers the §5 SIT+UAT+NFT+Regression rows; Go-Live band covers the §5 CAB+CUT rows. |
| Mini-phasing | Thresholds and required MP fields are in the Mini-Phasing Reference; apply them to §3.2/§4/§5. |
| Timeline | Planning duration/timeline derives from weekly capacity, the prioritized backlog, and dependencies, never from re-sizing. One weekly Gantt only, with week columns matching the resource matrix; no separate sprint timeline. |
| Resource constraints | Capture capacity gaps or staffing constraints as notes in the weekly matrix and the Handoff Note; they are not a risk register. |
| Warranty | Carry Step 04 warranty handling consistently; do not double-count with Step 06 reserve. |

## Question Triggers

Before execution, check high-impact blockers: approved Raw MD, project type/productivity factor, target duration/go-live, staffing constraints, delivery model, PM derivation basis, and warranty/hypercare resource handling.

| Condition | Action |
|---|---|
| Project type unclear | TRIGGER question; default to Integration-Heavy only if Step 04 handoff confirms 3+ external integrations and user allows defaults. |
| Target duration/go-live exists | Reverse-plan from TOR Go-Live and flag gaps. |
| Target duration absent | Propose planning duration from capacity/resource feasibility and label it as an assumption. |
| Staffing constraint exists | Reflect in weekly resource matrix constraints/notes; do not change Raw MD. |
| Feature dependencies form a long critical path | Sequence critical-path features first in the backlog and place them in early mini-phases. |
| PM or matrix coverage outside its band | Flag, record rationale/treatment, and adjust allocation/duration; never revise Step 04 to fit. |
| No blocking uncertainty remains | MUST state `No blocking confirmations; proceeding with approved baseline/defaults.` |

## Execution Flow

1. Read both approved Step 04 files; reject Step 05 if either is missing, unapproved, inconsistent, or has a failed mandatory arithmetic gate. Record Raw MD by role, bucket breakdown, feature/subfeature basis, warranty handling, dependencies, and integration count/architecture complexity.
2. Resolve Question Triggers in one gate, or state the no-blocking sentence.
3. Set productivity inputs and capacity constants once.
4. Compute Adjusted MD by role = Raw MD + applicable rework + applicable buffer; derive PM MD from calendar/resource governance and run the PM/Total sanity check (see Fixed Baseline).
5. Produce the prioritized backlog, critical path, and mini-phase decision from the Backlog Prioritization and Mini-Phasing References.
6. Build one delivery-week resource matrix with its `Phase Band` row and a separate warranty schedule if needed. Reconcile Effective MD to delivery Adjusted MD, then combined delivery + warranty to full Adjusted MD within 95-105% by role.
7. Build the weekly Gantt aligned to the matrix and its phase bands; record resource constraints as matrix notes and in the Handoff Note.
8. Ask up to 5 highest-impact remaining stakeholder-answerable open items with finite choices in one gate using the asking tool or chat fallback, then update productivity inputs, adjusted effort, matrix, Summary, and Handoff. Any changed Adjusted MD requires a baseline correction sweep.
9. Publish the artifact with the Step 06 handoff payload (see Handoff Note); stop at the Post-step Review Gate. Only the router may authorize a separate next action under continuous mode; this action never executes Step 06.

## Productivity Reference

| Project Type | Focus | Rework | Buffer | Notes |
|---|---:|---:|---:|---|
| Greenfield | 80% | 10% | 10% | New build with moderate dependency. |
| Migration/Modernization | 75% | 15% | 12% | Existing system/data/process migration complexity. |
| Integration-Heavy (3+ ext.) | 70% | 18% | 15% | Multiple external dependencies or heavy enterprise integration. |

Capacity constants and formulas (define once, reuse everywhere):

- `WORK_DAYS_PER_MONTH = 22` (regional/project calendar default; project calendar may override) and `WORK_DAYS_PER_WEEK = 5`.
- `EFFECTIVE_MD_PER_FTE_WEEK = WORK_DAYS_PER_WEEK × Focus Factor`; Effective MD/Person-Month = `WORK_DAYS_PER_MONTH × Focus Factor`.
- `FTE-Weeks` = sum of weekly FTE allocations for the role; `Nominal MD = FTE-Weeks × WORK_DAYS_PER_WEEK`; `Effective MD = Nominal MD × Focus Factor`.
- `Rework MD = Raw MD × applicable rework rate`; `Buffer MD = Raw MD × applicable buffer rate`. Both use Raw MD, not compounded values. Focus affects capacity only, not Adjusted MD.
- `PM Base MD = base governance PM FTE-Weeks × WORK_DAYS_PER_WEEK × Focus Factor`, plus separately approved PM buffer. Record the base allocation before buffer; final matrix PM allocation must cover base plus buffer without feeding back into PM Base MD. PM Base MD is governance effort, not rework. Include PM Base MD as a separate addition in total reconciliation.
- Use dated calendar working days when known. Otherwise, calendar months = weeks × WORK_DAYS_PER_WEEK ÷ WORK_DAYS_PER_MONTH; do not mix this with four-week month approximations.
- Average FTE = `Adjusted MD ÷ (Weeks × EFFECTIVE_MD_PER_FTE_WEEK)` using demand and weeks from the same delivery/support horizon. Do not substitute matrix allocation. `Allocated average FTE = FTE-Weeks ÷ Weeks` is a separate capacity measure; label it explicitly even when coverage passes. Average FTE rounded up is only a staffing lower bound. Headcount must also cover peak role allocation, skills, leave, and dependency timing. Round people up; fractional FTE cells represent partial allocation, not fractional people.

## Rework Applicability Reference

| Role | Default Rework Treatment | Buffer Treatment | Note |
|---|---|---|---|
| SA | 0% rework | Apply selected buffer | Discovery/design changes are handled as assumptions or Step 04 revision, not automatic rework. |
| BA | 0% rework | Apply selected buffer | Same as SA. |
| UX | 0% rework | Apply selected buffer | Apply rework only if UX iteration scope is explicitly approved. |
| FE | Apply selected rework | Apply selected buffer | Dev role. |
| BE | Apply selected rework | Apply selected buffer | Dev role. |
| QA | 0% rework by default | Apply selected buffer | QA effort already validates reworked build; use rework only with explicit rationale. |
| DevOps | 0% rework by default | Apply selected buffer | Use rework only for unstable infra/release pipeline assumption. |
| PM | Created in Step 05 from calendar/resource governance need | Buffer optional only if approved | Step 04 has no PM baseline; PM is not a Step 04 revision trigger by itself. |
| Change | 0% rework | Apply selected buffer if in baseline | Change activities are not dev rework. |

## Backlog Prioritization Reference

Apply these criteria in order when sequencing the feature/backlog. Ties broken by the next-lower criterion.

| Order | Criterion | Rule |
|---:|---|---|
| 1 | Dependency | Predecessors MUST precede dependents (infra/foundation features first; integrations after producer services). |
| 2 | Critical-path contribution | Features on the longest dependency chain set the duration floor; protect them with priority allocation and early start. |
| 3 | Sizing weight | Large features (high MD) start earlier so they fit; small follow-ups backfill. |
| 4 | Business priority | MoSCoW (Must > Should > Could > Won't) or sponsor rank when supplied. |
| 5 | Risk / unknowns | Pull high-risk, integration-heavy, or discovery-required features forward for early validation. |

## Mini-Phasing Reference

| BUILD Calendar Duration | Mini-Phasing Treatment | Notes |
|---|---|---|
| ≤ 4 weeks (~1 month) | Single BUILD phase | Mini-phasing optional and must be justified if used. |
| > 4 weeks and ≤ 8 weeks | 2 mini-phases (`MP1`, `MP2`), typically 3-4 weeks each | Each MP delivers a coherent feature group with internal demo/SIT-light. |
| > 8 weeks and ≤ 12 weeks | 3 mini-phases | Align MPs to prioritized backlog tranches; protect critical path in MP1-MP2. |
| > 12 weeks | 4+ mini-phases (typically 3-4 weeks each; shorter final MP justified) | Rolling SIT may overlap MPs; reflect in matrix phase bands. |

Use 3-4 weeks as a target, not a duration floor. Shorten the final mini-phase or justify overlap when necessary to fit the approved BUILD duration. Do not extend a five-week BUILD merely to fit two three-week phases.

Each mini-phase must list: feature group (from prioritized backlog), week range, gate/demo, dependency to next MP, and roles staffed.

## Output Contract

Create/update `output/step_05_resource_plan.md` using this schema. Replace placeholders, write `N/A — [reason]` for sections that do not apply, and reconcile all capacity totals.

Use `Rework Applicability Reference` to select each role's rework rate. `[r%]` refers to the selected rework percentage in §1. Record the effective numeric rate in `Rework Rule`. For an approved exception, replace the rate and Rework MD. Record the approval ref and rationale in Note. PM has zero Rework MD; governance effort remains in PM Base MD.

```markdown
# Step 05 - Resource Plan: [PROJECT_NAME]

**Source**: `output/step_04_sizing_estimate.md` + `output/step_04_sizing_review.md` [approved paired revision]
**Version**: [VERSION], [DATE_YYYY-MM-DD]
**Approved Baseline Scope**: SG1-only / SG1+SG2 / TBD
**Approval State**: Draft / Approved / Needs Revision
**Approval Basis**: [ผู้อนุมัติ/วันที่ หรือ authorization/วันที่ ตาม explicit-approval principle]

## Step Summary

- Scope basis: [SG1-only / SG1+SG2]. Adjusted MD, duration, FTE and coverage are in the Handoff Note (canonical numeric block for Step 05); do not restate them here.
- Productivity profile: [project type + factors].
- Critical path and resource constraints: see Handoff Note; do not repeat them here.

## Handoff Note - Step 06

- Effort: Raw [N] MD (Step 04, unchanged) → Adjusted [N] MD; Adjusted MD by role: [role list]; PM [N] MD = [x%].
- Duration through hypercare: [N] weeks / [N] months; BUILD [N] weeks; warranty horizon: [N or N/A]. Delivery Person-Months [N] (`delivery Adjusted MD ÷ (WORK_DAYS_PER_MONTH × Focus Factor)`); warranty demand/capacity is reported separately.
- Weekly resource baseline: [week count and phase bands]; Average FTE [N] (`delivery Adjusted MD ÷ (delivery weeks × EFFECTIVE_MD_PER_FTE_WEEK)`); allocated average FTE [N] (`delivery FTE-Weeks ÷ delivery weeks`); peak allocated FTE [N] from the matrix `Total FTE/week` row; coverage [x%]. State the delivery horizon; report warranty separately.
- Prioritized backlog and critical path: [top critical-path features, critical-path MD, MP groupings].
- Mini-phasing: [MP count, week ranges, feature groups, gates] or `N/A — BUILD ≤ 4 wk`.
- Resource constraints: [constraints from matrix notes/N/A].
- Key assumptions: [top assumptions].
- Warranty/hypercare handling: [summary].

**เปลี่ยนจากรอบก่อน:** [ครั้งแรก / สิ่งที่เปลี่ยนและผลต่อ baseline; ไม่คัดลอกรายละเอียด]
**ข้อพบที่ต้องรับทราบ:** [นำ Warning/Fail จาก review มาสรุปพร้อมผลกระทบ หรือ ไม่มี; อ้างส่วนภาคผนวก]

**ประเด็นที่ต้องตัดสินใจ:** [ไม่เกิน 3 ประเด็นสำคัญและผลต่อ baseline หรือ ไม่มี; อ้าง Open Questions ในภาคผนวก]

**Post-step Review Gate — Step 05 Resource Planning**

Please review:
- Key outputs: productivity inputs, adjusted effort, feature/backlog prioritization, weekly resource matrix, weekly project timeline (with mini-phases if BUILD > 4 wk), resource constraints.
- Assumptions to confirm: [อ้างประเด็นที่ต้องตัดสินใจด้านบน; ไม่เขียนซ้ำ].
- Baseline impact: MD / Timeline / Resource / Risk.

Reply options:
- `approve Step 05` = lock resource plan and make it available to Step 06 risk/contingency. Stop this action; the router may authorize the next action separately.
- `revise Step 05: ...` = update resource plan before proceeding.

## ภาคผนวก

## Approved Inputs Consumed

| Input | Value | Note |
|---|---:|---|
| Raw Grand Total MD | [N] | From Step 04 |
| Raw MD by Role | [summary] | From Step 04 Sizing Summary |
| Bucket Breakdown | [summary] | SG1/SG2/Integration/Non-Dev from Step 04 Sizing Summary |
| Feature/Subfeature Basis | [summary] | Feature/subfeature rows, page/API/INT assumptions, and count/complexity basis from Step 04 |
| Warranty Handling | Included / Excluded | Must match Step 04 |
| Key Dependencies | [N] | INT, client/external/operational readiness, NFR, staffing assumptions |
| Integration Count / Architecture Cx | [N] / [Low/Medium/High] | Required for project type default; from Step 04/Step 02 handoff |

## 1. Productivity Inputs

| Project Type | Focus Factor | Rework | Buffer | Effective MD / FTE-Week | Rationale |
|---|---:|---:|---:|---:|---|
| [Greenfield/Migration/Integration-Heavy] | [x%] | [x%] | [x%] | `[5 × focus]` | [why selected] |

Capacity constants: `WORK_DAYS_PER_MONTH` = [22 or project calendar]; `WORK_DAYS_PER_WEEK` = [5]; `EFFECTIVE_MD_PER_FTE_WEEK` = [N] (`WORK_DAYS_PER_WEEK × Focus Factor`).

## 2. Adjusted Effort

Carry every Step 04 role unchanged, including approved DE/DBA/specialists. Change has Raw MD only if it is a distinct role in Step 04; otherwise keep its zero row and do not duplicate Change activity effort already allocated to BA/SA. Total Adjusted MD = Raw MD + rework + buffer + PM Base MD. The PM row's Adjusted MD includes PM Base MD even though its Raw MD and Rework MD are zero.

Rework MD = Raw MD × effective rate. Note records any approved rate override.

| Role | Raw MD | Rework Rule | Rework MD | Buffer MD | Adjusted MD | Note |
|---|---:|---|---:|---:|---:|---|
| SA | [N] | 0% | 0 | [N] | [N] | [note] |
| BA | [N] | 0% | 0 | [N] | [N] | [note] |
| UX | [N] | 0% | 0 | [N] | [N] | [note] |
| FE | [N] | [r%] | [N] | [N] | [N] | [note] |
| BE | [N] | [r%] | [N] | [N] | [N] | [note] |
| QA | [N] | 0% | 0 | [N] | [N] | [note] |
| DevOps | [N] | 0% | 0 | [N] | [N] | [note] |
| PM | 0 | 0% | 0 | [N/0] | [PM Base MD + approved PM buffer] | PM Base MD from derivation below; not sourced from Step 04. |
| Change | [N] | 0% | 0 | [N] | [N] | [note] |
| **Total** | **[Raw MD]** |  | **[N]** | **[N]** | **[Adjusted MD]** |  |

**PM Derivation**: PM Base MD = [N] MD calendar-derived ([PM FTE-Weeks × working days/week × focus]); Adjusted PM MD = PM Base MD + approved PM buffer = [N] MD = [x%] of Adjusted Total vs 10-15% benchmark → Pass/Warning. [If outside range, explain governance intensity, duration, or delivery model; do not mutate Step 04.]

## 3. Feature/Backlog Analysis & Prioritization

Sequence the WBS features into delivery order before laying out the resource matrix and timeline. Inputs: Step 03 WBS, Step 04 sizing, Step 02 dependencies/integrations. Apply the criteria from the Backlog Prioritization Reference (dependency → critical path → sizing → business priority → risk).

### 3.1 Prioritized Backlog

| # | Feature / Backlog Item | WBS Ref | Size (MD) | Predecessors | On Critical Path | Business Priority | Risk | Sequence | Mini-Phase | Notes |
|---:|---|---|---:|---|---|---|---|---:|---|---|
| 1 | [Feature] | [WBS-XX] | [N] | [list / none] | Y/N | Must / Should / Could | Low / Med / High | 1 | MP1 / N-A | [why this position] |
| 2 | [Feature] | [WBS-XX] | [N] | [list / none] | Y/N | Must / Should / Could | Low / Med / High | 2 | MP1 / MP2 / ... | [note] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 3.2 Mini-Phase Plan (only when BUILD > 4 weeks; otherwise mark `N/A — BUILD ≤ 4 wk`)

| Mini-Phase | Week Range | Feature Group (from §3.1) | Internal Gate / Demo | Handoff to Next MP | Roles Staffed | Notes |
|---|---|---|---|---|---|---|
| MP1 | W[ ] - W[ ] | [features] | Demo + SIT-light | [artifacts/criteria] | [roles] | Critical-path features prioritized |
| MP2 | W[ ] - W[ ] | [features] | Demo + SIT-light | [artifacts/criteria] | [roles] | [note] |
| ... | ... | ... | ... | ... | ... | ... |

## 4. Weekly Resource Matrix

Use one resource matrix only. Columns are calendar weeks (`W1...Wn`) grouped under named phase bands (Foundation / BUILD / QA / Go-Live / Hypercare, or project-specific equivalents) by the `Phase Band` row at the top of the matrix. When BUILD is split into mini-phases, label its sub-bands `BUILD-MP1`, `BUILD-MP2`, ...; if BUILD ≤ 4 weeks, use a single `BUILD` band. FTE cells may use decimals (e.g., `0.5`) for partial allocation; headcount remains whole-person planning unless explicitly stated as allocation. The matrix Adjusted MD column contains delivery-only demand; the separate warranty schedule owns warranty demand.

Title the matrix with the planning summary, e.g.: `Step 05 — Timeline & Resource Matrix (Adjusted-effort plan [N] wk)`. Step 06 selects the risk-range commitment basis; do not label Step 05 as P75.

| # | Role | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | ... | Wn | FTE-Weeks | Nominal MD | Effective MD | Adjusted MD | Coverage Ratio | Constraint / Note |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
|  | Phase Band | Foundation | Foundation | BUILD-MP1 | BUILD-MP1 | BUILD-MP1 | BUILD-MP2 | BUILD-MP2 | BUILD-MP2 | ... | [band] |  |  |  |  |  |  |
| 1 | PM | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | `[FTE-Weeks × WORK_DAYS_PER_WEEK]` | `[nominal × focus]` | [N] | `[effective/adjusted]` | Pass/Warning + constraint if any |
| 2 | UX/UI | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 3 | BA | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 4 | SA | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 5 | FE | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 6 | BE | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 7 | DevOps | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 8 | QA | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| 9 | Change | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | [FTE] | ... | [FTE] | [sum] | [N] | [N] | [N] | [%] | [note] |
| **Total FTE/week** |  | [sum] | [sum] | [sum] | [sum] | [sum] | [sum] | [sum] | [sum] | ... | [sum] | **[FTE-Weeks total]** | **[Nominal MD total]** | **[Effective MD total]** | **[Adjusted Total]** | **[x%]** | 95-105% target |

Notes:
- `FTE-Weeks` = sum of weekly FTE allocations across active weeks for the role.
- `Nominal MD` = `FTE-Weeks × WORK_DAYS_PER_WEEK` (default WORK_DAYS_PER_WEEK=5).
- `Effective MD` = `Nominal MD × Focus Factor`; reconcile it to the delivery portion of Adjusted MD within 95-105%, then check combined delivery + warranty capacity against full Adjusted MD.
- Retain unused roles with `0` FTE-Weeks. For zero Adjusted MD, Coverage Ratio is `N/A — no demand`; non-zero allocation needs a reason. Show both per-role and total coverage.
- Delivery weeks through hypercare and warranty weeks are distinct horizons. Report demand-based Average FTE, allocated average FTE, and peak allocated FTE with their horizon. Do not dilute delivery averages with standby warranty weeks or replace demand with Effective MD.

### Warranty Resource Schedule

If warranty is included, show its post-hypercare calendar horizon, role allocations, Effective MD, and coverage against the warranty portion of Step 04/05 effort. Use a separate support schedule rather than hundreds of delivery-week columns. Delivery matrix plus warranty schedule must reconcile to total Adjusted MD by role; neither may include the other's effort. If excluded, write `N/A — warranty excluded in Step 04`. Standby availability is not consumed MD unless the approved assumption explicitly reserves that capacity.

## 5. Project Timeline (Weekly Gantt)

Express phases and tasks as a Gantt across week columns and phase bands that match the Weekly Resource Matrix. Mark each active week cell with `■` (or shaded equivalent in exports); leave inactive cells blank. Use sub-task numbering (`3.1`, `3.2`, ...) to decompose a parent task. When BUILD is split, list each Mini-Phase as its own row referencing the feature group from §3.2.

| # | Task / Phase | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | ... | Wn | Start Week | End Week | Duration (Weeks) | Critical? | Dependencies | Key Deliverable |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|
|  | Requirement and Design | ■ | ■ | ■ |  |  |  |  |  |  |  | W1 | W3 | 3 | Y/N | PO/SME availability | FS/UX baseline |
| 1 | Foundation & POC | ■ | ■ |  |  |  |  |  |  |  |  | W1 | W2 | 2 | Y/N | Contract/PO/PMO readiness | Foundation + POC validated |
| 2 | Develop (BUILD) |  |  | ■ | ■ | ■ | ■ | ■ | ■ |  |  | W3 | W8 | 6 | Y/N | Design/API readiness | Build complete for agreed scope |
| 2.1 | BUILD-MP1: [feature group] |  |  | ■ | ■ | ■ |  |  |  |  |  | W3 | W5 | 3 | Y/N | Design/API + MP1 backlog | MP1 demo + SIT-light passed |
| 2.2 | BUILD-MP2: [feature group] |  |  |  |  |  | ■ | ■ | ■ |  |  | W6 | W8 | 3 | Y/N | MP1 handoff | MP2 demo + SIT-light passed |
| 3 | Infrastructure | ■ | ■ | ■ | ■ |  |  |  |  |  |  | W1 | W4 | 4 | Y/N | Cloud/network/security approvals | All environments ready |
| 3.1 | Setup DEV Environment | ■ |  |  |  |  |  |  |  |  |  | W1 | W1 | 1 | Y/N | Infra account/access | DEV ready |
| 3.2 | Setup SIT Environment |  | ■ |  |  |  |  |  |  |  |  | W2 | W2 | 1 | Y/N | DEV ready | SIT ready |
| 3.3 | Setup UAT Environment |  |  | ■ |  |  |  |  |  |  |  | W3 | W3 | 1 | Y/N | SIT ready | UAT ready |
| 3.4 | Setup PROD Environment |  |  |  | ■ |  |  |  |  |  |  | W4 | W4 | 1 | Y/N | UAT ready / security signoff | PROD ready |
| 4 | SIT |  |  |  |  |  | ■ | ■ | ■ | ■ |  | W6 | W9 | 4 | Y/N | INT owner/sandbox/payload/test data | SIT evidence |
| 5 | UAT |  |  |  |  |  |  |  |  | ■ | ■ | W9 | W10 | 2 | Y/N | Client acceptance criteria/users/env | UAT signoff |
| 6 | NFT (Performance + Security) |  |  |  |  |  |  | ■ | ■ | ■ |  | W7 | W9 | 3 | Y/N | NFT scope/test data/env | NFT + security evidence |
| 7 | Regression Test |  |  |  |  |  |  |  |  | ■ | ■ | W9 | W10 | 2 | Y/N | Stable build / regression pack | Regression evidence |
| 8 | CAB (Change Approval Board) |  |  |  |  |  |  |  |  |  | ■ | W10 | W10 | 1 | Y/N | UAT + NFT signoff | CAB approval |
| 9 | CUT — Cutover Weekend |  |  |  |  |  |  |  |  |  | ■ | W10 | W10 | 1 | Y/N | CAB approval / release window | Production cutover |
| 10 | Hypercare ([N] wk) |  |  |  |  |  |  |  |  |  |  | W[ ] | W[ ] | [N] | Y/N | Go-live | Hypercare closure (or `N/A — hypercare excluded in Step 04`; warranty exclusion alone does not exclude hypercare) |

Legend: `■` = active week cell; blank = inactive. Sub-task rows (`2.1`, `2.2`, `3.1`–`3.4`) decompose their parent. The Develop row MUST be decomposed into `BUILD-MPn` rows whenever BUILD calendar duration > 4 weeks. Week columns must equal the Weekly Resource Matrix; do not introduce a separate sprint timeline.

## Open Questions / Assumptions

| ID | Item | Why / Impact | Owner | Needed By |
|---|---|---|---|---|
| OQ-01 | [question/assumption] | [stakeholder-readable why/impact] | [owner] | Before Step 06 / final resource baseline |

## Internal Review

Render per [reviewer-first guidance](../../principle-orbit-reviewer-first/SKILL.md).

| Check | Result | Note |
|---|---|---|
| Step 04 Raw MD consumed without change | Pass/Warning/Fail | [note] |
| Productivity rules applied | Pass/Warning/Fail | [note] |
| PM derivation completed | Pass/Warning/Fail | [note] |
| Feature/backlog prioritization produced | Pass/Warning/Fail | Sequence applies dependency → critical path → sizing → business priority → risk. |
| Mini-phasing rule applied | Pass/Warning/Fail | If BUILD > 4 wk, split into `MP1...MPn` (typically 3-4 wk each; shorter final MP justified) with feature group + gate; else `N/A — BUILD ≤ 4 wk`. |
| Weekly resource matrix reconciles to Adjusted MD | Pass/Warning/Fail | Delivery capacity matches delivery demand; delivery + warranty capacity matches full Adjusted MD by role within 95-105%. `Phase Band` covers every delivery week. |
| Project timeline aligns to weekly matrix | Pass/Warning/Fail | Week columns and phase bands match the matrix; BUILD decomposed into `MP` rows when split; no separate sprint timeline. |
| Step 06 handoff ready | Pass/Warning/Fail | Average FTE uses same-horizon Adjusted demand and capacity constants. Allocated average FTE uses FTE-Weeks/weeks and has a separate label. Handoff figures reconcile to their owning tables. |


```

## Validation Checklist

Evaluate `Internal Review` against the Fixed Baseline / Scope, reference formulas, and Output Contract. Check Adjusted Effort arithmetic and per-role delivery + warranty coverage. Source immutability, PM derivation, mini-phasing, timeline alignment, and Step 06 exclusions are checked once against those sections.
