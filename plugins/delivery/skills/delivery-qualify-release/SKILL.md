---
name: delivery-qualify-release
description: Qualify an explicitly selected merge-ready change for release with immutable candidate binding, environment proof, full gates, and independent evidence review.
---

# Qualify a release candidate

## When to use

Use this skill when the user requests release qualification of a merge-ready change. Stop at release-ready. Release approval and deployment remain separate human decisions with their own target, scope, and external approval gates.

Do not require this workflow for ordinary implementation or PR review. A release manifest is required only when this workflow binds a candidate or an existing assignment explicitly uses a bound candidate.

## Inputs

Obtain the selected PR, issue, or explicitly scoped change, its merge-ready evidence, frozen acceptance content, approved contracts, and authorized environment. Require the target constraints, environment owner, worker gate owners, independent reviewer, and source inspection owner.

Use an existing accepted identifier when one exists. Otherwise derive a stable source reference as `PR-N`, `issue-N`, or a scoped slug. Do not invent a Feature ID. Derive `acceptanceVersion` from the immutable accepted-content revision or digest, not from the current date or an invented version number.

Stop if merge-ready evidence, frozen acceptance, target identity, or required access is missing. An assumption cannot replace a production target or credential.

## Required reading

Read every listed file completely before acting. Recover truncated reads and resolve links from their containing document.

- Read the [authority principle](../principle-delivery-authority/SKILL.md).
- Read the [owned writes principle](../principle-delivery-owned-writes/SKILL.md).
- Read the [source and evidence principle](../principle-delivery-source-evidence/SKILL.md).
- Read the [trust boundaries principle](../principle-delivery-trust-boundaries/SKILL.md).
- Read the [project context contract](../delivery-coordinate-work/references/project-context.md).
- Read the [assignment and handoff contract](../delivery-coordinate-work/references/assignment-and-handoff.md).
- Read [Git safety](../delivery-deliver-change/references/git-safety.md).
- Read the [static review skill](../delivery-review-change/SKILL.md), [implementation skill](../delivery-implement-change/SKILL.md), and [platform work contract](../delivery-implement-change/references/platform-work.md).
- Read the [security skill](../delivery-secure-boundaries/SKILL.md) and [debugging skill](../delivery-debug/SKILL.md).

Read the repository's release, quality, environment, migration, recovery, and deployment instructions. Resolve actual commands from existing scripts and configuration. Do not invent a package manager, scanner, CI job, or manifest command.

## Steps

1. Confirm that the selected source is merge-ready and that acceptance is frozen. Record the requested stop state as `release-ready`. Preserve the source and criterion IDs. Route new requirements back through the project's acceptance authority instead of adding them during final review.
2. Obtain one platform checkpoint with evidence for the applicable environment obligations.

   - Record TLS, allowed origins, secret interfaces without secret values, replicas, credentials readiness, and database permissions.
   - Record database, cache, and container readiness where used, shared-service ownership, required environment names without values, and the frozen migration digest.
   - Record deployment and migration compatibility, observed health, rollback limits, operability, and the recovery runbook.
   - Record task-owned services, containers, and volumes with their observed state and cleanup owner.

   A launch command or running process does not prove readiness. Require a health response, connection, or exercised operation. A destructive migration is safely reversible only with observed reversal evidence. Name each failed prerequisite, cause when established, and affected gate. Do not apply infrastructure or migrations outside authorized scope.
3. Follow the states `mutating`, `source-complete`, `reviewed`, `bound`, `validating`, and `release-ready`. Report only the current state. After every writer stops, finish authorized lockfile, generated-file, and formatting work before source review and binding.
4. Bind the reviewed source through the authorized binding owner. Use a clean commit SHA with a complete candidate manifest, or the project's immutable worktree snapshot mechanism. Include untracked candidate files and deletions. Distinguish unrelated ambient files rather than silently absorbing or ignoring them. If their ownership cannot be separated, stop.
5. Name the candidate `<source-ref>-C<n>`. Record the triple `candidateId`, `acceptanceVersion`, and `manifestDigest`, with its source identity and immutable manifest. Every bound review, gate, scanner report, and verdict cites the same triple. Preserve evidence as immutable records outside candidate source. Do not overwrite a previous result to disguise a repair.
6. Assign no-edit application gates and platform scanners to authorized worker owners. These are execution assignments, not static review. Run the project's required release gate categories, including validation, integration, coverage, end-to-end behavior, security, and image scanning where the project requires them. Required build and environment checks remain required. PR CI is not proof of an omitted end-to-end or manual gate. Run the missing authorized gate or report it `not verified`.
7. For every scanner result, require the binding, exact command, tool version, configuration, execution identity, date, exit code, and result location. Account for every manifest path as scanned or scanner-skipped with a reason. Deleted paths count as skipped. Reconcile `nonCandidateExclusions` separately. They never waive coverage of candidate source. A skipped scanner, unscanned required path, or execution error is no result, not a pass.
8. Obtain independent bound-evidence review from a separate reviewer actor. Supply the authorized-owner diff, metadata, manifest, criterion proof, environment checkpoint, and scanner evidence. The reviewer performs static inspection only. Require matching identity and scope, complete manifest accounting, and each criterion as `observed pass`, `observed fail`, or `not verified`.
9. Batch findings and failed gates into one repair cycle. Diagnose causes before editing. Repair only frozen acceptance defects or violations of existing approved contracts. If source changes, invalidate the old candidate, return to `mutating`, and repeat source review before binding the next candidate ID. Record the superseded candidate and addressed findings. Regenerate all required proof against the new binding. If source remains unchanged, rerun failed gates without relabeling stale or mismatched evidence as current.
10. Allow one repair cycle and one final delta review. Permit a second and last cycle only for a reproducible blocking defect. Under the Blocker/Major/Minor/Nit scheme, that exception requires a reproducible Blocker or Major defect. A missing proof record alone does not authorize an extra cycle. Record non-blocking follow-ups. Do not increase the cap or broaden acceptance yourself.
11. Send only a candidate with passing required gates to final delta review. Require the reviewer to check manifest identity, proof closing prior findings, absence of repair regressions, complete evidence on this binding, and separately recorded out-of-scope observations. The final disposition is `APPROVED` or `CHANGES_REQUESTED`, with original finding labels and IDs. New preferences that violate neither frozen acceptance nor an existing contract are not blocking defects.

Any candidate-source change, including formatting or generated output, invalidates the binding. Report the invalidated candidate explicitly. Never carry its verdict onto changed source or edit its immutable manifest in place. Evidence-only additions outside candidate source retain their actual binding and cannot claim new execution.

## Verification

Require frozen acceptance, resolved blocking findings, no unclassified findings, passing full gates, a passing environment checkpoint, and independent approval on one unchanged binding. Missing, mismatched, failed, or unverified required evidence blocks release-ready.

Review recommendations do not themselves grant technical acceptance. The authorized coordinator makes that decision from the evidence. Technical acceptance does not grant product acceptance, publication, release approval, or deployment permission.

## Output and stop conditions

Return the current state, candidate triple, source identity, superseded candidate IDs, criterion results, gate evidence, scanner coverage, environment checkpoint, independent disposition, repair cycles used, and remaining decisions. State exactly which operations were executed and which remain proposed.

Report `release-ready` only when all conditions hold on the same unchanged binding. At the repair cap, stop with remaining finding IDs, evidence, and the decision required. If the user stops, preserve source, immutable evidence, resource ownership, and actual results under the handoff protocol.

Never deploy, merge, publish a release, destroy infrastructure, rotate credentials, or delete persistent data under this skill alone. Those operations require separate explicit authority and applicable external approvals.
