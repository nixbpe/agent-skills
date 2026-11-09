---
name: delivery-deliver-change
description: Deliver one explicitly requested issue or capability change through implementation, review, and authorized publication without merging or starting follow-up work.
disable-model-invocation: true
---

# Deliver one requested change

## When to use

Use this skill only for an explicit request to deliver one issue or capability change. It can take an authorized change to merge-ready and an unmerged PR when publication is authorized. Invoking it does not grant commit, push, PR creation, merge, or deployment permission.

Use accepted issue criteria directly. Do not require a new feature record, acceptance document, or technical specification for routine work. An index can locate sources but cannot authorize implementation.

## Inputs

Obtain the issue URL or number, or the explicit requested capability change. Identify its accepted outcomes, contracts, dependencies, and non-goals. Record the current workspace, requested stop state, and separate permissions for implementation and each publication operation.

An open product decision, deferred work, or a dependency that has not reached its required state blocks the affected implementation. Do not reinterpret the requested behavior to avoid that gate.

## Required reading

Read every listed file completely before acting. Recover truncated reads and resolve links from their containing document.

- Read the [authority principle](../principle-delivery-authority/SKILL.md).
- Read the [owned writes principle](../principle-delivery-owned-writes/SKILL.md).
- Read the [source and evidence principle](../principle-delivery-source-evidence/SKILL.md).
- Read the [trust boundaries principle](../principle-delivery-trust-boundaries/SKILL.md).
- Read the [project context contract](../delivery-coordinate-work/references/project-context.md).
- Read [Git safety](references/git-safety.md).
- Read the [coordination skill](../delivery-coordinate-work/SKILL.md) and [assignment and handoff contract](../delivery-coordinate-work/references/assignment-and-handoff.md).
- Read the [implementation skill](../delivery-implement-change/SKILL.md) and [static review skill](../delivery-review-change/SKILL.md).

Read the source criteria, repository instructions, relevant existing code, quality commands, and PR template before implementation. The reviewer loads its own required reading and receives inspection evidence from an authorized owner.

## Steps

1. Confirm one accepted source and its requested behavior. Preserve its contracts. Return scope or contract changes to the user before implementing them. Record the requested completion state without treating it as publication authority.
2. Establish owned paths and the integration owner. Follow Git safety for the workspace and branch. Relay only permissions actually granted to each owner. Keep `COMMIT_MODE: none` when no commit permission exists. The main session may implement only when project role policy permits.
3. Implement the complete behavior, affected callers, tests, required runtime smoke checks, accessibility obligations, and criterion-linked proof. Use coordination only where ownership or role boundaries require it. Do not invent a release manifest for ordinary implementation.
4. Stop all writers before final integration checks. Obtain independent static review for code changes and resolve in-scope findings under the project's severity mapping. Keep source labels unchanged. Blocking or unclassified findings prevent readiness.
5. Run the project's required focused checks and full local quality gates through authorized worker operations. Preserve failed or unverified results. Diagnose failures and use the applicable bounded repair procedure rather than weakening checks or skipping required behavior.
6. If commit, push, and PR creation are each authorized, apply the canonical Git gates and publish one PR. If authority is absent, stop before that operation and report the completed local work and exact permission needed. Do not erase authorized implementation progress merely because publication is unavailable.
7. Use the repository's PR template. Cite the source, delivered behavior, risks, per-criterion proof, and gate results for the exact head SHA. For a request without an issue, identify the requested change and use `Closes: none` where required. Keep detailed handoffs outside the PR body.
8. Wait with finite timeouts for required PR CI and review conditions on the published head. A pending or timed-out check remains unverified. Report merge-ready only after every required condition passes on that head.

If the assignment explicitly requires separate PRs or dependency merge gates, finish the first merge-ready PR, identify the next authorized unit, and stop. Do not merge or start dependent follow-up work.

## Verification

Require the accepted behavior, required proof, independent review, and local gates to match the delivered source. After publication, require the PR gates and review to match the current head. A source change invalidates stale review or execution claims according to their scope. Bound release evidence additionally follows the immutable candidate rules.

Use `observed pass`, `observed fail`, and `not verified`. A local success does not prove remote CI passed. Passing CI does not prove an omitted local or manual requirement. Loading this skill never replaces an approval record.

## Output and stop conditions

Return the delivered behavior, source identity, review result, local verification, CI state, and remaining permissions or blockers. Include a commit SHA and PR URL only when they exist. State whether the PR remains unmerged and whether dependent work has started.

Stop at the requested authorized state. Report a publication block separately from implementation status. Never claim merge-ready while required findings, gates, or evidence remain unresolved. Release qualification, merge, deployment, and dependent work require separate scope and authorization.
