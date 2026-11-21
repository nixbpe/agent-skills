---
name: principle-source-evidence
description: "Use when reporting software verification, judging review findings, or tying evidence to the source revision it was observed on."
---

# Tie every verdict to its evidence

## Separate evidence from inference

For each required criterion, report `observed pass`, `observed fail`, or `not verified`. Identify the scenario, expected result, actual result, command or observation, and source revision. Distinguish your own observation from producer evidence and inference.

A successful build does not prove runtime behavior. A source review does not prove UI appearance, accessibility, query performance, or deployment readiness. A started process does not prove that its service accepts the required operation.

Missing, stale, partial, or mismatched evidence remains `not verified`. Report unavailable tools and skipped checks with their effect on the requested outcome. Do not invent measurements or convert warnings into passes.

## Identify ordinary work without release ceremony

Use a commit SHA for committed work. For uncommitted work, identify the changed paths and the inspected diff or snapshot. Record the acceptance source and its current revision.

Ordinary implementation and review do not require a release candidate manifest. When the source changes, repeat the affected checks and reviews. Do not reuse a verdict merely because the branch name is unchanged.

A gate result counts only for a tree that stayed unchanged while it ran. Record the HEAD and the working tree identity before and after each gate run. If either changed during the run, including through your own edit, a merge, or another writer, report that run as `not verified` and run it again on the stable tree. A failure seen while other heavy gates ran alongside is evidence of contention until it reproduces alone.

## Bind a release candidate

Binding applies only to release qualification or an assignment that names a bound candidate. Before binding, or before judging evidence against a binding, read the [candidate binding contract](../qualify-release/references/candidate-binding.md). Any candidate file change invalidates the binding.

## Review findings without changing their meaning

Each finding records its ID, source severity, violated criterion or contract, location, trigger, impact, and required proof. Merge duplicate findings without losing affected locations. Separate defects, evidence gaps, and proposals outside the accepted scope.

Use the project's documented severity mapping to derive `blocking` or `non-blocking`. Keep the original severity alongside that decision. Do not assume that `P2` and `Major` mean the same thing. When no mapping exists, mark the finding `unclassified` and resolve its blocking status before declaring readiness.

A required criterion failure, security or data-loss risk, or missing required evidence blocks acceptance regardless of cosmetic labels. Formatting preferences and optional new requirements are not defects in the accepted scope.

## Keep independent review independent

A separate reviewer inspects the source, affected consumers, tests, and supplied evidence. An author rereading their own work is self-review. Label it accordingly.

A read-only reviewer does not run gates or repair files. The coordinator supplies diffs and Git metadata from an authorized inspection owner. The reviewer returns findings and a recommendation. The authorized acceptance owner decides the disposition.

For release acceptance, every required criterion and gate must pass on the same unchanged binding. Review approval does not authorize merge or deployment.
