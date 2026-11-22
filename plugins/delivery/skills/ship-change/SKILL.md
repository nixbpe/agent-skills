---
name: ship-change
description: Drive one explicitly requested change from implementation through a published PR to merge-ready, as a bounded, resumable loop over CI and independent review, without merging.
disable-model-invocation: true
---

# Ship one change to merge-ready

## When to use

Use this skill for an explicit request to take one issue or capability change from implementation to a merge-ready PR, repairing CI failures and review findings along the way. It sequences [change delivery](../deliver-change/SKILL.md) and [PR repair](../repair-pr/SKILL.md) and owns only the loop: its states, caps, durable record, resume, and no-progress stop.

For an explicitly requested stack of PRs, [stacked PRs](references/stacked-prs.md) runs this loop once per PR and replaces the stop after the first PR in change delivery.

Use [change delivery](../deliver-change/SKILL.md) alone when the request stops at an open PR without a repair loop. Use [PR repair](../repair-pr/SKILL.md) alone for a PR that already exists and has no record from this skill.

## Inputs

Obtain the accepted source and criteria, the workspace, the project's review provider or separate reviewer actor, and the wait timeouts for CI and review. Take the timeouts from project context. When it has none, ask once at intake.

When the source holds several features or changes, such as an epic, report each one's readiness and whether a merged or open PR already delivers it. Then ask the user to pick one, or to request a stack explicitly. Do not choose for them, and do not treat the whole source as one change.

Collect the permission bundle once at intake: branch creation, `COMMIT_MODE: owned-slice`, push to the named branch, PR creation, review request, PR body update, comment posting, thread resolution, and writing to the source's decision record. Ask again only after a material change in scope. Each missing permission stops the loop before the operation that needs it. This skill never merges, force-pushes, retargets, or deploys.

Record whether the user delegated decisions. Delegation covers technical choices only. A decision that changes behavior, security, accepted scope, or an irreversible operation still blocks under [coordination](../coordinate-work/SKILL.md), and delegation never covers merge, force-push, retarget, or deploy. Each decision taken under delegation goes to the state record, the PR's risk section, and the source's decision record as unapproved, with the choice, the alternative not chosen, the risk, and how to reverse it. Without permission to write one of those locations, report the decision in the output instead. A delegated decision never becomes an approved requirement.

Record whether the run is attended or unattended. An unattended run requires every precondition in [unattended operation](../coordinate-work/SKILL.md#unattended-operation) to be `observed pass` and a durable record location. Otherwise run attended or stop.

## Required reading

Read unconditional dependencies before acting and conditional dependencies before the matching state.

- Read the [owned writes](../principle-owned-writes/SKILL.md), [source and evidence](../principle-source-evidence/SKILL.md), and [trust boundaries](../principle-trust-boundaries/SKILL.md) principles.
- Read the [project context contract](../coordinate-work/references/project-context.md), the [assignment and handoff contract](../coordinate-work/references/assignment-and-handoff.md), and [Git safety](../deliver-change/references/git-safety.md).
- Before `IMPLEMENTING`, read [change delivery](../deliver-change/SKILL.md) and [coordination](../coordinate-work/SKILL.md). Before `REPAIRING`, read [PR repair](../repair-pr/SKILL.md). Before diagnosing any failure, read [debugging](../debug-failure/SKILL.md).

## States

| State | Work | Exit |
|---|---|---|
| `INTAKE` | Read the state record. Confirm source, permissions, mode, and timeouts. | Next state from the record, or `IMPLEMENTING`. Missing input goes to `BLOCKED`. |
| `IMPLEMENTING` | Change delivery steps 1-3 through `delivery-worker`. | Source-complete handoff. |
| `LOCAL_VERIFY` | Change delivery steps 4-5: independent static review, then focused checks and full local gates. | All pass goes to `PUBLISHING`. A failure starts a local repair round. |
| `PUBLISHING` | Change delivery step 6: commit gate, push, and PR creation. A PR that delivers only part of its source references the source without a closing keyword. Then request independent review for the head through the project's configured mechanism. | PR URL and head SHA recorded, review requested. |
| `AWAITING` | PR repair steps 1-5 and 6.5-6.7 on the current head: wait with finite timeouts for required CI and independent review, triage findings, rebut disputed ones with evidence, close verified threads, and recheck the head. | All merge-ready conditions pass goes to `MERGE_READY`. A failure or blocking finding goes to `REPAIRING`. A timeout goes to `BLOCKED` with the pending conditions. |
| `REPAIRING` | One PR repair round, steps 6.1-6.4. | New head pushed, back to `AWAITING`. |
| `MERGE_READY` | Read back the state record, the PR body's head SHA and the open threads from the PR, then report only what was read. | End. A later in-scope request for this PR reopens the loop at `REPAIRING`. |
| `SUPERSEDED` | Report the merged or open change that delivers the same source, and the overlap. | End. Closing the PR needs its own permission. |
| `CLOSED` | Record who closed the PR and why. | End. A reopened PR resumes at `AWAITING` on its actual head with the recorded counts. |
| `BLOCKED` | Report the failed condition, the decision needed, and the next owner. | End. |

## Caps and no-progress stop

`LOCAL_VERIFY` allows at most eight repair rounds across every session for this change. This cap replaces the single integration repair in [coordination](../coordinate-work/SKILL.md) step 10. Each round batches blocking or unclassified findings and failed gates, diagnoses causes, repairs only accepted criterion or contract defects, runs focused checks, reruns failed gates, and refreshes independent review for changed source. A failure remaining after round eight goes to `BLOCKED`. Do not publish with a failed local gate.

`REPAIRING` uses the three-round cap of [PR repair](../repair-pr/SKILL.md) unchanged. This skill adds no rounds of its own. Do not combine the two caps, carry unused local rounds into PR repair, or reset either count by restarting the skill.

A failure signature is the check name with its first error line, or the finding ID. When a round ends with a signature that the previous round also ended with, go to `BLOCKED` even if the cap has rounds left. A new signature counts as progress.

## Base and dependency drift

Record the base branch SHA and, for each PR this change depends on or overlaps, its head SHA and scope. Before every push, PR creation, or PR close, and before declaring `MERGE_READY`, fetch and compare them with the record.

- When a lower PR of the same stack gets a new head, follow [stacked PRs](references/stacked-prs.md), including when it touches the same paths. The rules below then apply to the stack's own base and to PRs outside the stack.
- When the base moved only on paths this change does not touch, record the new SHA and continue.
- When the base moved on paths this change touches, or a dependency PR's scope or state changed, go to `BLOCKED` and return the overlap and the options. Follow [merging the base](../deliver-change/references/git-safety.md#merging-the-base) before any merge.
- When another change already delivers the same source, go to `SUPERSEDED`.

A fetch that completes before a long operation does not cover a push after it. Compare again immediately before the push.

## Work requested after merge-ready

A user request for more work on the same PR after `MERGE_READY` enters `REPAIRING` and counts as one PR repair round against the three-round cap. A request outside the accepted source is a new change with its own record. `MERGE_READY` holds only for the head it was reported on.

## State record

Keep one record per change. Before publication, write it to the project's durable evidence location. When the project names none and the source is an issue, a comment on that issue with the same marker serves, with comment permission. After publication, keep it in a PR comment marked `ship-change-state: v1`, only with comment permission. The record holds the source, state, PR URL, head SHA, base SHA, each dependency PR's head SHA and scope, `pre_pr_repairs`, `pr_repair_rounds`, each PR repair round's head SHA and addressed finding IDs, the last failure signatures, each unapproved delegated decision, and the update time. This record is the PR repair round record, so both skills read and write one counter. Update it at every state change.

At `INTAKE`, read the record before any other action and resume from it. When the recorded head differs from the PR's actual head, resume at `AWAITING` with evidence for the actual head only. Without a durable location, run attended and report that both caps are unenforced across sessions.

## Verification

Merge-ready uses the [Git safety](../deliver-change/references/git-safety.md) and [PR repair](../repair-pr/SKILL.md) definitions on the same head. A new head invalidates review and CI claims tied only to an earlier head. A local pass does not prove remote CI. A thread resolution alone is not acceptance.

## Output and stop conditions

Return the final state, source, PR URL and head SHA when they exist, rounds used against each cap, CI and review state per required condition, open findings by original priority, unapproved delegated decisions, non-blocking follow-ups, and remaining permissions or blockers. State that the PR remains unmerged.

Stop at `MERGE_READY`, `BLOCKED`, `SUPERSEDED`, or `CLOSED`. Further rounds after an exhausted cap or a no-progress stop require new user approval. On a user stop, follow the stop protocol in the [assignment and handoff contract](../coordinate-work/references/assignment-and-handoff.md) and update the record.
