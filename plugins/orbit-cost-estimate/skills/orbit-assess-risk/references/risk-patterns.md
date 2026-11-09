# Risk pattern examples

Optional Step 06 discovery reference. Read only when the TOR/dependency scan needs examples beyond the command's taxonomy. Patterns are candidates, not project facts; the [Step 06 contract](contract.md) owns eligibility, scoring, formulas, and final checks.

### Auto-Generation Guide — Canonical Patterns by Theme

When generating the Risk Register from a TOR, scan for these patterns. Each pattern maps to a canonical risk and is pre-classified under one of the two top-level themes; adapt the wording to the project. Internal-only patterns are listed separately and must NOT enter the Step 06 risk register. They remain Step 05 constraints.

#### Theme A — Integration / External Dependency

**A1. Data access risks**

| Field | Value |
|---|---|
| Trigger phrases | "integrate with internal systems", "credentials will be provided", "API keys / subscription / network access", "SharePoint / Azure Blob / external sources" |
| ID pattern | Allocate the next `RSK-XX`; prioritize only if it gates the approved critical path |
| Likelihood / Impact | High / High |
| Impact category | Timeline (ETL blocked) + Scope (manual fallback) |
| Mitigation | Data source checklist in week 1, hard deadline before sprint dev, sample data contingency |

**A2. External source coverage**

| Field | Value |
|---|---|
| Triggers | TOR mentions external / public web data; "subscription content"; vague external sources |
| Likelihood / Impact | Medium / Medium |
| Canonical risk | Limited by API/Subscription availability; web scraping is not feasible |
| Mitigation | Confirm list of external sources, set expectation, scope expansion = CR |

**A3. Cross-team dependency**

| Field | Value |
|---|---|
| Triggers | "AI Hub team will provide...", "Data Engineering team responsible for...", "Integration with team X" |
| Likelihood / Impact | High / High |
| Canonical risk | Other team slippage blocks integration |
| Mitigation | API contract sprint 1, SLA per dependency, mock APIs, integration test plan |

#### Theme B — Requirement Unconfirmed

**B1. Role / permission**

| Field | Value |
|---|---|
| Triggers | "Access control by user role", "Guardrails", "RBAC", "permission-based filtering", "Single Sign-On", "Active Directory" |
| Likelihood / Impact | High / High (compliance + scope) |
| Canonical risk | User role / permission mapping must be ready before dev |
| Mitigation | Workshop with IT/HR, initial role set, QA on access control before go-live |

**B2. Configuration ossification**

| Field | Value |
|---|---|
| Triggers | "Configurable rules", "priority order", "thresholds", "Initially configured at deployment" |
| Likelihood / Impact | Low / Medium |
| Canonical risk | Rule/priority changes after go-live require code change (not config) |
| Mitigation | Workshop initial rules, decision log + sign-off, CR for changes |

**B3. Data quality rules dependency**

| Field | Value |
|---|---|
| Triggers | "Filtering by quality threshold", "Deduplication / archival rules", "Rules to be defined by client" |
| Likelihood / Impact | Medium / High |
| Canonical risk | Rules engine waits on client-supplied rules |
| Mitigation | Ask for rule examples week 1, baseline default rules, config tool |

**B4. Content dependency**

| Field | Value |
|---|---|
| Triggers | "Prompt library", "starter questions", "FAQ content", "Content provided by client", "Training data to be supplied" |
| Likelihood / Impact | Assess from owner commitment, readiness evidence, and dependency dates; do not assume all content is late |
| Canonical risk | Feature is ready before its content, so users see empty states |
| Mitigation | Lock milestone for content draft, working session with SMEs, owner for maintenance |

**B5. UX flow TBC**

| Field | Value |
|---|---|
| Triggers | "TBC", "TBD", "to be agreed", "Feedback mechanism — details to be confirmed" |
| Likelihood / Impact | Low–Medium / Low–Medium |
| Canonical risk | Design rework if confirmation comes late |
| Mitigation | Confirm in sprint planning, prepare 2 design variants |

**B6. Threshold / numeric placeholder**

| Field | Value |
|---|---|
| Triggers | "(placeholder)", numeric values flagged as draft, "Confidence score threshold to be tuned" |
| Likelihood / Impact | Medium / Medium |
| Canonical risk | Threshold mismatch → wrong disclaimers / user trust loss |
| Mitigation | Tune in calibration phase, expose config |

**B7. Compliance / PII**

| Field | Value |
|---|---|
| Triggers | "Personal data", "employee data", "customer data", "PDPA", "GDPR", "HIPAA", "Audit logging" |
| Likelihood / Impact | Medium / High |
| Canonical risk | PII handling gaps → legal exposure |
| Mitigation | DPIA, data classification, audit logs from day 1, retention policy |

**B8. Performance / scale assumption (NFR)**

| Field | Value |
|---|---|
| Triggers | Numeric volume in TOR ("10,000 users", "1M documents"), "Real-time", "<2 seconds", performance SLA in penalties clause |
| Likelihood / Impact | Medium / High |
| Canonical risk | Volume / latency assumption may not hold under prod load |
| Mitigation | Load test plan, infra sizing review, observability + SLO |

#### Excluded — Internal Delivery (NOT Step 06 risks)

The following patterns are structural delivery-team concerns. Per the Risk eligibility rule in Fixed Baseline / Scope, they MUST be carried as Step 05 resource constraints or validity conditions, not as Step 06 risk-register items.

| Pattern | Triggers | Where it Belongs |
|---|---|---|
| Dev → QA handoff timing | Structural (any TOR); requirements drift makes dev late → QA squeezed | Step 05 resource constraint / validity note. Mitigation = requirement freeze date, parallel QA prep, timeline buffer. |
| Resource on-boarding | Structural (any TOR); resource availability tied to kickoff date | Step 05 resource constraint / staffing assumption. Mitigation = confirm kickoff date, lock allocation 2-4 weeks early, backup pool, onboarding plan. |
