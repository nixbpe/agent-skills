---
name: qualify-release
description: Qualify an explicitly selected merge-ready change for release with immutable candidate binding, environment proof, full gates, and independent evidence review.
---

# Qualify a release candidate

## When to use

Use this skill when the user requests release qualification of a merge-ready change. Stop at release-ready. Release approval and deployment remain separate human decisions with their own target, scope, and external approval gates.

Do not require this workflow for ordinary implementation or PR review. A release manifest is required only when this workflow binds a candidate or an existing assignment explicitly uses a bound candidate.

## Inputs

Obtain the selected PR, issue, or explicitly scoped change, its merge-ready evidence, frozen acceptance content, approved contracts, and authorized environment. Require the target constraints, environment owner, worker gate owners, independent reviewer, and source inspection owner.

Use an existing accepted identifier when one exists. Otherwise derive a stable source reference as `PR-N`, `issue-N`, or a scoped slug. Do not invent a Feature ID.

Stop if merge-ready evidence, frozen acceptance, target identity, or required access is missing. An assumption cannot replace a production target or credential.

## Required reading

Read unconditional dependencies before acting and conditional dependencies before the matching operation.

- Read the [authority](../principle-authority/SKILL.md), [owned writes](../principle-owned-writes/SKILL.md), [source and evidence](../principle-source-evidence/SKILL.md), and [trust boundaries](../principle-trust-boundaries/SKILL.md) principles. They own the rules on permissions, ownership, evidence labels, severity mapping, and untrusted data, which this skill does not repeat.
- Read the [candidate binding contract](references/candidate-binding.md).
- Read the [project context contract](../coordinate-work/references/project-context.md).
- Read the [assignment and handoff contract](../coordinate-work/references/assignment-and-handoff.md).
- Read [Git safety](../deliver-change/references/git-safety.md).
- Read the [static review skill](../review-change/SKILL.md), [platform work contract](../implement-change/references/platform-work.md), and [security skill](../secure-boundaries/SKILL.md).

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
5. Name the candidate `<source-ref>-C<n>` and record its triple under the candidate binding contract. Every bound review, gate, scanner report, and verdict cites the same triple. Preserve evidence as immutable records outside candidate source. Do not overwrite a previous result to disguise a repair.
6. Assign no-edit application gates and platform scanners to authorized worker owners, who read [implementation](../implement-change/SKILL.md) before execution or repair. Run the project's required release gate categories, including validation, integration, coverage, end-to-end behavior, security, and image scanning where required. Required build and environment checks remain required. PR CI does not prove an omitted gate. Run missing authorized gates or report them `not verified`.
7. For every scanner result, require the gate record fields and manifest path accounting in the candidate binding contract. Reconcile `nonCandidateExclusions` separately. A skipped scanner, unscanned required path, or execution error is no result, not a pass.
8. Obtain independent bound-evidence review from a separate reviewer actor. Supply the authorized-owner diff, metadata, manifest, criterion proof, environment checkpoint, and scanner evidence. The reviewer performs static inspection only. Require matching identity and scope, complete manifest accounting, and each criterion as `observed pass`, `observed fail`, or `not verified`.
9. Batch findings and failed gates into one repair cycle. Read [debugging](../debug-failure/SKILL.md) before diagnosing failures. Repair only frozen acceptance defects or violations of approved contracts. Source changes invalidate the candidate: return to `mutating`, repeat source review, bind the next candidate, and regenerate required proof. Record the superseded candidate and addressed findings. Without source changes, rerun failed gates without relabeling stale or mismatched evidence.
10. Count repair cycles from the immutable evidence records of this source reference, including superseded candidates from earlier sessions, not from the current session alone. Allow one repair cycle and one final delta review. Permit a second and last cycle only for a reproducible blocking defect. Under the Blocker/Major/Minor/Nit scheme, that exception requires a reproducible Blocker or Major defect. A missing proof record alone does not authorize an extra cycle. Record non-blocking follow-ups. Do not increase the cap or broaden acceptance yourself.
11. Send only a candidate with passing required gates to final delta review. Require the reviewer to check manifest identity, proof closing prior findings, absence of repair regressions, complete evidence on this binding, and separately recorded out-of-scope observations. The final disposition is `APPROVED` or `CHANGES_REQUESTED`, with original finding labels and IDs. New preferences that violate neither frozen acceptance nor an existing contract are not blocking defects.

Any candidate-source change, including formatting or generated output, invalidates the binding. Report the invalidated candidate explicitly. Never carry its verdict onto changed source or edit its immutable manifest in place. Evidence-only additions outside candidate source retain their actual binding and cannot claim new execution.

## Verification

Require frozen acceptance, resolved blocking findings, no unclassified findings, passing full gates, a passing environment checkpoint, and independent approval on one unchanged binding. Missing, mismatched, failed, or unverified required evidence blocks release-ready.

The authorized coordinator decides technical acceptance from the evidence.

## Output and stop conditions

Return the current state, candidate triple, source identity, superseded candidate IDs, criterion results, gate evidence, scanner coverage, environment checkpoint, independent disposition, repair cycles used, and remaining decisions. State exactly which operations were executed and which remain proposed.

Report `release-ready` only when all conditions hold on the same unchanged binding. At the repair cap, stop with remaining finding IDs, evidence, and the decision required. If the user stops, preserve source, immutable evidence, resource ownership, and actual results under the handoff protocol.

After release, the project's own signals judge quality: user-perceived performance, shipped change volume, and revert rate. A revert rate counts only reverts. It omits defects fixed in a later change, so track follow-up fix changes beside it. Report these only from data the project provides.

Never deploy, merge, publish a release, destroy infrastructure, rotate credentials, or delete persistent data under this skill alone. Those operations require separate explicit authority and applicable external approvals.
