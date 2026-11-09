---
name: delivery-coordinate-work
description: Coordinate approved software work through explicit ownership, worker evidence, independent review, and bounded integration at the requested readiness state.
---

# Coordinate approved work

## When to use

Use this skill to assign implementation, platform work, validation, or repairs across ownership boundaries. Use it directly with an accepted request or issue. A routine change does not require a separate specification or all delivery workflows in sequence.

Keep release qualification separate. The main session may implement when project policy permits. Delegate when role restrictions, independent review, or separate ownership require another actor.

## Inputs

Identify the requested outcome, accepted source and criteria, applicable repository instructions, owned workspace, and authorization limits. Use `STOP_AT: merge-ready` for a request to implement and verify to completion. Otherwise use the requested state, normally `review-ready`. Never silently reduce end-to-end work to a partial result or promote implementation into release qualification.

Obtain the relevant application and platform contracts, project commands, review requirements, and target constraints from existing project evidence. Read the code and its conventions before dispatch. A missing decision that changes behavior, security, scope, or an irreversible operation blocks the affected work. Label harmless assumptions without inventing quality targets.

## Required reading

Read every listed file completely before acting. Recover truncated reads and resolve links from their containing document.

- Read the [authority principle](../principle-delivery-authority/SKILL.md).
- Read the [owned writes principle](../principle-delivery-owned-writes/SKILL.md).
- Read the [source and evidence principle](../principle-delivery-source-evidence/SKILL.md).
- Read the [trust boundaries principle](../principle-delivery-trust-boundaries/SKILL.md).
- Read the [project context contract](references/project-context.md).
- Read the [assignment and handoff contract](references/assignment-and-handoff.md).
- Read [Git safety](../delivery-deliver-change/references/git-safety.md).

Read the procedure skills assigned to each operation before performing that operation. Use [implementation](../delivery-implement-change/SKILL.md) for application or platform changes and [static review](../delivery-review-change/SKILL.md) for the independent reviewer. Use [technical design](../delivery-design-solution/SKILL.md) only when cross-cutting contracts need design. Use [experience design](../delivery-design-experience/SKILL.md) when an affected UI flow is unsettled.

## Steps

1. State the accepted outcome, scope, requested stop state, and any blocking decision. Distinguish approved requirements, repository invariants, delegated decisions, assumptions, and proposals. Design approval alone does not authorize implementation.
2. Map each criterion to an owned behavioral slice or integrated verification. Split by behavior, failure, permission, or application-platform boundary. Give each shared file one integration owner. Set contracts and prerequisites before dispatch. Do not create an actor for each criterion.
3. Prepare assignments with the canonical fields. Set commit authority from the user's actual authorization. Do not require a particular model, provider, task ID syntax, or planning document. Send relevant source sections and shared invariants rather than an entire unrelated feature or raw logs.
4. Dispatch independent assignments together only when ownership is disjoint. Keep dependent work behind its contract and evidence gates. While siblings write, permit only the focused verification named in their assignments. The integration owner handles shared generators and whole-project commands after writers stop.
5. Receive handoffs without polling. Follow the canonical waiting and transfer protocol for stalled work or ownership changes. Record assignment state, actual source identity, findings, and blockers. Record a candidate triple only when release binding exists.
6. Review each completed slice against criteria, contracts, and non-goals before dependent work starts. Return blocking findings to its owner with the triggering evidence and expected proof. Require stateful evidence to show triggers, mutations or interleavings, and preserved state. Data-writing integration tests need run-unique fixtures and owned cleanup. Missing runtime proof leaves the slice source-complete rather than author-verified.
7. After all writers stop, have the authorized integration owner settle shared outputs, formatting, and documentation. Assign focused integration checks and smoke tests, including required database isolation, authorization, and security checks. Close proof gaps through worker operations. A static reviewer never runs those checks.
8. At `review-ready`, report the implemented scope and every check as `observed pass`, `observed fail`, or `not verified`. Claim readiness only if the requested implementation and required focused proof are complete. Otherwise report the exact blocker or failed condition.
9. At `merge-ready`, obtain one final independent static review for code changes, including integration and changes since slice reviews. Apply repository policy for non-code review. Assign the project's full PR gate commands after writers stop. Typical gate categories are validation, coverage, build, and security, but the repository determines the exact commands and targets.
10. Batch integration findings and failed gates into one repair. Diagnose the causes before editing. Repair only accepted criterion or contract defects. Run the assigned focused checks and rerun failed gates after repair. Refresh independent review for changed source. If a blocking or unclassified finding, failed gate, or missing proof remains, stop and return the evidence and decision needed. Do not invent an unbounded repair loop.

For an existing PR, use [PR repair](../delivery-review-pr/SKILL.md) when explicitly requested. Its three-round cap replaces this integration repair step. For bound release work, use [release qualification](../delivery-qualify-release/SKILL.md) and its separate repair cap. Do not combine caps or reset a consumed cap by changing workflow names.

## Verification

Verify outcomes through owner evidence against the exact reviewed source. Keep review, focused proof, full gates, and environment evidence distinct. Existing valid evidence can be reused only when its identity and scope still match. Merge-ready requires the applicable independent review and PR gates. Full release checks, image scanning, binding, and environment readiness belong to release qualification.

The coordinator decides technical integration and triage within delegated authority. It cannot change accepted scope, downgrade finding severity, infer production approval, or substitute a design for observed behavior.

## Output and stop conditions

Return the reached state, accepted source, delivered behavior, owner handoffs, review disposition, per-criterion evidence, gate results, repair count, and remaining blockers. Name the next owner and exact action when work cannot proceed. Omit empty sections.

Stop for a missing critical contract, unresolved reviewer conflict, unsatisfied frozen criterion, exhausted repair cap, missing infrastructure decision, or user work that cannot be separated safely. Return the precise decision and available options. Publication follows separate authority under Git safety.

On a user stop, follow the assignment and handoff stop protocol. Preserve partial work and actual check results. Do not continue dispatch, repairs, or validation to obtain a cleaner final report.
