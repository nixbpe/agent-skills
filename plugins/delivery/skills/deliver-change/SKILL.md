---
name: deliver-change
description: Deliver one explicitly requested issue or capability change through implementation, review, and authorized publication without merging or starting follow-up work.
disable-model-invocation: true
---

# Deliver one requested change

## When to use

Use this skill only for an explicit request to deliver one issue or capability change. It can take an authorized change to merge-ready and an unmerged PR when publication is authorized.

Use accepted issue criteria directly. Do not require a new feature record, acceptance document, or technical specification for routine work. An index can locate sources but cannot authorize implementation.

## Inputs

Obtain the issue URL or number, or the explicit requested capability change. Identify its accepted outcomes, contracts, dependencies, and non-goals. Record the current workspace, requested stop state, and separate permissions for implementation and each publication operation.

An unattended run selects only an item reported `ready-for-delivery` under [work definition](../define-work/SKILL.md), at the approved revision. A person's explicit request for one issue does not need that state.

An open product decision, deferred work, or a dependency that has not reached its required state blocks the affected implementation. Do not reinterpret the requested behavior to avoid that gate.

## Required reading

Read unconditional dependencies before acting and conditional dependencies before the matching operation. Skip a file below only when its full text is still in your context. A summary of it or another actor's reading does not count.

- Read the [owned writes](../principle-owned-writes/SKILL.md), [source and evidence](../principle-source-evidence/SKILL.md), and [trust boundaries](../principle-trust-boundaries/SKILL.md) principles.
- Read the [project context contract](../coordinate-work/references/project-context.md).
- Read [Git safety](references/git-safety.md).
- Read the [assignment and handoff contract](../coordinate-work/references/assignment-and-handoff.md).
- Read the [implementation skill](../implement-change/SKILL.md).

Read the source criteria, repository instructions, relevant existing code, quality commands, and PR template before implementation. The reviewer loads its own required reading and receives inspection evidence from an authorized owner.

## Steps

1. Confirm one accepted source and its requested behavior. Preserve its contracts. Return scope or contract changes to the user before implementing them. Record the requested completion state without treating it as publication authority.
2. Establish owned paths and the integration owner. Follow Git safety for the workspace and branch.
3. Implement the complete behavior, affected callers, tests, required runtime smoke checks, accessibility obligations, and criterion-linked proof. Read [coordination](../coordinate-work/SKILL.md) before dispatch, ownership transfer, or cross-owner integration.
4. Stop all writers before final integration checks. Obtain independent static review for code changes and resolve in-scope findings under the project's severity mapping. Without a mapping a finding stays `unclassified`. Do not classify it yourself. Blocking or unclassified findings prevent readiness.
5. Run the project's required focused checks and full local quality gates through authorized worker operations. Preserve failed or unverified results. Diagnose failures and use the applicable bounded repair procedure rather than weakening checks or skipping required behavior.
6. If commit, push, and PR creation are each authorized, apply the Git safety commit and publication gates and publish one PR. Otherwise stop before the unauthorized operation.
7. Wait with finite timeouts for required PR CI and review conditions on the published head. Report merge-ready only after every required condition passes on that head. For a bounded repair loop over CI and review, use [ship loop](../ship-change/SKILL.md), which runs steps 1-6 here and adds the repair loop.

If the assignment explicitly requires separate PRs or dependency merge gates, finish the first merge-ready PR, identify the next authorized unit, and stop. Do not merge or start dependent follow-up work. An explicitly requested stack under [stacked PRs](../ship-change/references/stacked-prs.md) continues to the next PR instead.

## Verification

Require the accepted behavior, required proof, independent review, and local gates to match the delivered source. After publication, require the PR gates and review to match the current head. A source change invalidates stale review or execution claims according to their scope.

A local success does not prove remote CI passed. Passing CI does not prove an omitted local or manual requirement.

## Output and stop conditions

Return the delivered behavior, source identity, review result, local verification, CI state, and remaining permissions or blockers. Include a commit SHA and PR URL only when they exist. State whether the PR remains unmerged and whether dependent work has started.

Stop at the requested authorized state. Report a publication block separately from implementation status.
