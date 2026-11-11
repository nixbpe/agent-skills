# Illustrative APO architecture inventory

Project-specific example only. Do not adopt its IDs, events, identity systems, SG grouping, or counts into another project. The [architecture reference](../architecture.md) and approved project artifacts control any use of this example.

## Workflow notification example

| Event | Trigger | Primary Recipient | Architecture Handling |
|---|---|---|---|
| Submitted / Request Created | Request enters approval workflow | First-level approver | Send workflow notification with request ID and action link |
| Pending Next Approval | Workflow moves to next approval level | Next approver | Resolve current approver from routing matrix before sending |
| Approved by Level | Approver approves an intermediate level | Requester / next approver | Record approval event and send status transition notification |
| Final Approved | Final approval level completes | Requester / owner | Send completion notification and close workflow notification chain |
| Rejected | Approver rejects with reason | Requester | Include reject reason and route-back context where applicable |
| Route Back / Return for Revision | Request is returned for correction | Requester | Include required action and resubmit link |
| Resubmitted | Requester resubmits after correction | Relevant approver | Restart or continue routing according to approved workflow rule |
| Cancelled / Withdrawn | Requester or authorized user cancels request | Requester / current approver | Notify affected participants and stop pending reminders |
| Delegated / Reassigned / Expired | Approval ownership changes or expires | Delegate / original approver / admin | Notify new owner and keep reassignment audit trail |
| Reminder / SLA Breach | No action within configured threshold | Current approver / escalation owner | Scheduled worker sends reminder and records reminder log |

Illustrative APO non-workflow notification events: sync failure notification for transfer/retry failure uses INT-03 in that example only; admin-managed notification template/recipient configuration is SG2/assumption-backed unless explicitly re-baselined.

## A7. Sitemap / Menu Baseline

Illustrative APO inventory only. The SCR/INT IDs, identity providers, authorization system, SG grouping, and counts below must not carry into another project's estimate. Derive its inventory from approved Step 03.1 scope. This example includes 25 SG1 and 5 SG2 screens; the 30-screen total is not an SG1-only baseline.

Example UI inventory contains 30 screens after removing Favorite View Manager and standalone Export & Reports pages: S=0, M=23, C=7. Forecast export is an action available from the current forecast view across SCR-03 and SCR-05 to SCR-09, not a separate menu/page. Login is Microsoft Entra ID / Azure AD Login only. Screens marked as SG2/assumption-backed remain optional unless explicitly re-baselined.

```text
APO Web Application
├── 1. Authentication
│   └── SCR-31 Microsoft Entra ID / Azure AD Login
│       └── Rule: Microsoft IdP authentication only; no local username/password login; IdP setup excluded; OR-PIS remains function/data authorization boundary
│
├── 2. Dashboard / Forecast View
│   ├── SCR-03 Monthly Forecast Browser
│   ├── SCR-05 Sales Office Forecast View
│   ├── SCR-06 Sales Group Forecast View
│   ├── SCR-07 Plant Forecast View
│   ├── SCR-08 Material Group Forecast View
│   └── SCR-09 Material Number Forecast View
│   └── Action: Export forecast data from the current forecast view across SCR-03 and SCR-05 to SCR-09
│
├── 3. Forecast Adjustment
│   ├── SCR-10 Forecast Edit Workspace
│   └── SCR-11 Allocation Preview
│
├── 4. Approval Workflow
│   ├── SCR-13 Submit Approval Request
│   ├── SCR-14 Approval Inbox and Decision
│   ├── SCR-15 Workflow Resubmit
│   ├── SCR-16 Workflow Cancel / Withdraw
│   ├── SCR-17 Delegation / Expiry Rule
│   └── SCR-18 Workflow Status / SLA Monitor
│
├── 5. Data Integration & Operations
│   ├── SCR-01 Manual Transfer Console
│   ├── SCR-02 Sync Status and History
│   ├── SCR-27 Writeback Status and Reconciliation
│   ├── SCR-35 Reference Data Review (SG2)
│   └── SCR-37 Data Reconciliation Summary (SG2)
│
├── 6. Audit & Version Control
│   ├── SCR-28 Audit Log Search
│   ├── SCR-29 Version History
│   ├── SCR-30 Version Rollback
│   └── SCR-39 Extended Business Activity Audit (SG2)
│
├── 7. User / Access Administration
│   ├── SCR-32 User Profile Status Review
│   ├── SCR-33 Role Data-scope Mapping Admin
│   └── SCR-34 Provision / Deactivation Evidence
│
└── 8. System Configuration
    ├── SCR-12 Approval Rule Admin
    ├── SCR-36 Forecast Cycle Control (SG2)
    └── SCR-38 Admin Configuration Console (SG2)
```

SG2 / optional-assumption screens in this sitemap: SCR-35 Reference Data Review, SCR-36 Forecast Cycle Control, SCR-37 Data Reconciliation Summary, SCR-38 Admin Configuration Console, SCR-39 Extended Business Activity Audit.
