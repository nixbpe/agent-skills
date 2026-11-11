# Estimation Calibration Guidance

This reference defines mandatory sanity thresholds and calibration rules for Step 04 Sizing, Step 05 Resource Planning, and Step 06 Risk / Final Planning Baseline.

Use these thresholds to detect under-estimation, over-estimation, formula breaks, and baseline inconsistencies. They are guardrails, not automatic re-estimation formulas. When a check is outside threshold, explain the reason, map it to assumptions/risks/scenarios, or raise a review finding.

## Required Calibration Checks

Step 04 must include a calibration pass after bottom-up sizing. Calibration validates the estimate; it must not introduce pricing, rate cards, or commercial terms.

| Check | Purpose |
|---|---|
| FE MD/screen | Detect under/over-estimated UI effort |
| BE MD/API | Detect under/over-estimated backend effort |
| Integration MD/type | Check protocol, ownership, dependency, and test complexity |
| Report/dashboard complexity | Check data, query, access control, and validation effort |
| Migration volume and cleansing | Check import, reconciliation, rollback, and cutover effort |
| QA vs FE + BE cross-check | Sanity-check test-case-based QA against FE + BE; explain any deviation |
| Inventory cross-check | Compare detailed estimate with inventory-based benchmark |
| Similar-project benchmark | Use historical delivery data when available |

If detailed sizing is below inventory cross-check, explain why or raise a finding before approval. If benchmark variance is large because TOR/RFP is unclear, map the variance to assumptions, scenarios, or risks.

## Sanity Thresholds

| Check | Normal | Flag If | Step Usage |
|---|---|---|---|
| FE MD/screen avg | 1.5-6 | <1 or >10 | Step 04, Step 06 final check |
| BE MD/API avg | 0.75-4 | <0.5 or >8 | Step 04, Step 06 final check |
| Screen:API ratio | API count ÷ physical screen count = 2-4 | <1 or >5; N/A for no-UI systems | Step 03, Step 04, Step 06 final check |
| Detailed vs inventory cross-check | like-for-like detailed estimate +15-30% | Detailed below inventory cross-check or >30% delta | Step 04, Step 06 final check |
| QA cross-check | QA sized from test cases × MD/case, compared with FE + BE | Deviation without rationale in Step 04 Calibration Pass | Step 04, Step 06 final check |
| PM / Total | 10-15% of Adjusted MD including PM | Outside 10-15%, explain in Step 05 | Step 05, Step 06 final check |
| (SA+BA) / Total | 15-25% | <10% | Step 04, Step 05, Step 06 final check |

## Confidence Usage

| Confidence | Use |
|---|---|
| P25 Best | Best-case planning range; optimistic view only |
| P50 Most Likely | T&M and internal planning |
| P75 Conservative | Fixed-scope delivery commitment / resource baseline |
| P90 Worst | Risk reserve discussion |

Planning heuristic. These P labels express planning conservatism, not measured statistical coverage unless supported by a documented probabilistic model. Use the Step 06 formulas for range values and select P50/P75 explicitly; selected Delivery Contingency includes the commitment uplift above P50. Range defaults do not certify schedule feasibility.

Range terminology mapping: `Best = P25`, `Most Likely = P50`, `Conservative Commitment = P75`, and `Worst = P90`. Use this mapping when reconciling Step 06 range outputs and final planning baseline wording.

Step 06 must run the final planning baseline checks defined in the [verification principle](../../principle-verify-before-publish/SKILL.md) in addition to these calibration thresholds. Threshold checks do not replace scope, traceability, assumption, risk, contingency, and baseline/scenario consistency checks.

## Market Defaults

| Default | Rule |
|---|---|
| Working days | 22/month unless project calendar differs |
| Warranty | Assumption: candidate 6-12 months after hypercare with 0.25-0.5 FTE standby; confirm source/owner before commitment. Standby availability is not consumed MD unless reserved capacity is explicitly included. Size support/fix effort in Step 04 and schedule it separately from delivery in Step 05. |
| AMS and KT/BAU transition | Separate support/resource workflows after baseline |
| LD clauses | Commercial/risk discussion, not Step 00-06 pricing |

## Handling Out-of-Threshold Results

When a threshold is breached:

1. Confirm the scope basis before judging the number: SG1-only, SG1+SG2, scenario, or re-baseline.
2. Check whether inventory counts are complete and traceable to approved scope.
3. Check arithmetic before changing assumptions: role totals, bucket totals, QA cross-check, ROM, top driver percentages, scenario figures, and P75 baseline.
4. If the number is valid, document rationale and keep it.
5. If the number depends on unclear TOR/RFP facts, map it to an assumption, decision, scenario delta, or risk.
6. If the number cannot be justified, raise a finding before approval.

Benchmark coverage must match the detailed scope and roles. Do not compare FE+BE-only benchmark MD with Raw Grand Total including analysis, QA, support, and non-dev. Delta = (Detailed MD − Benchmark MD) ÷ Benchmark MD; zero benchmark is N/A, not zero variance.

Inventory cross-check interpretation: detailed estimates that are 0-15% above the inventory cross-check are not automatic failures, but they require an explanation because they sit below the normal calibration band. Detailed estimates below the inventory cross-check or more than 30% above it require explicit rationale, assumption/risk mapping, or a finding.

Do not silently adjust baseline numbers to fit these thresholds. Any baseline correction must sweep all summaries, handoffs, scenario tables, workbook sheets, and cross-step references.
