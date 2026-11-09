---
name: principle-delivery-source-evidence
description: "Use when reporting software verification, judging review findings, or binding release evidence to an immutable source and acceptance revision."
---

# Tie every verdict to its evidence

## Separate evidence from inference

For each required criterion, report `observed pass`, `observed fail`, or `not verified`. Identify the scenario, expected result, actual result, command or observation, and source revision. Distinguish your own observation from producer evidence and inference.

A successful build does not prove runtime behavior. A source review does not prove UI appearance, accessibility, query performance, or deployment readiness. A started process does not prove that its service accepts the required operation.

Missing, stale, partial, or mismatched evidence remains `not verified`. Report unavailable tools and skipped checks with their effect on the requested outcome. Do not invent measurements or convert warnings into passes.

## Identify ordinary work without release ceremony

Use a commit SHA for committed work. For uncommitted work, identify the changed paths and the inspected diff or snapshot. Record the acceptance source and its current revision.

Ordinary implementation and review do not require a release candidate manifest. When the source changes, repeat the affected checks and reviews. Do not reuse a verdict merely because the branch name is unchanged.

## Bind a release candidate

A release candidate uses this identity triple:

| Field | Meaning |
|---|---|
| `candidateId` | A stable source identity followed by `-C<n>`, with an increasing attempt number |
| `acceptanceVersion` | An immutable revision or digest of the exact accepted criteria and contracts |
| `manifestDigest` | The digest of the candidate manifest that accounts for paths, contents, and deletions |

Use the project's existing identity format when it defines one. Otherwise use `PR-<number>`, `issue-<number>`, or an agreed source slug as the stable identity. For example, `PR-42-C1` does not require a Feature ID. Include the repository identity in the record to distinguish equal PR numbers across repositories.

If the acceptance source has no immutable version, capture its accepted contents and compute a digest. Do not use a mutable issue URL, invented version, or timestamp alone as `acceptanceVersion`.

Record the source commit or snapshot alongside the triple. Stop if a required manifest or immutable acceptance record cannot be produced with the project's available tooling. Never fabricate a digest.

Stop all writers before binding. Any candidate file change, including formatting or generated output, invalidates that binding. Record the superseded identity and create the next candidate before collecting replacement evidence.

Each gate result records the triple, command, tool version, configuration, execution identity, date, exit code, and evidence location. Reconcile scanner coverage against every manifest path. Record deleted paths and unsupported paths as skipped with reasons. Account for non-candidate exclusions separately. An exclusion cannot waive a required check of candidate source.

## Review findings without changing their meaning

Each finding records its ID, source severity, violated criterion or contract, location, trigger, impact, and required proof. Merge duplicate findings without losing affected locations. Separate defects, evidence gaps, and proposals outside the accepted scope.

Use the project's documented severity mapping to derive `blocking` or `non-blocking`. Keep the original severity alongside that decision. Do not assume that `P2` and `Major` mean the same thing. When no mapping exists, mark the finding `unclassified` and resolve its blocking status before declaring readiness.

A required criterion failure, security or data-loss risk, or missing required evidence blocks acceptance regardless of cosmetic labels. Formatting preferences and optional new requirements are not defects in the accepted scope.

## Keep independent review independent

A separate reviewer inspects the source, affected consumers, tests, and supplied evidence. An author rereading their own work is self-review. Label it accordingly.

A read-only reviewer does not run gates or repair files. The coordinator supplies diffs and Git metadata from an authorized inspection owner. The reviewer returns findings and a recommendation. The authorized acceptance owner decides the disposition.

For release acceptance, every required criterion and gate must pass on the same unchanged binding. Review approval does not authorize merge or deployment.
