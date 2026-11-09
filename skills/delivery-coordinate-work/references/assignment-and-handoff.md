# Assignment and handoff contract

## Assignment fields

An assignment names one outcome and its owner. The current request, issue, or accepted specification supplies its authority and criteria. Routine work needs no separate planning document.

Every assignment contains the following information.

- `OWNER` names the actor, role, and integration owner where work crosses slices. Model routing follows the available project configuration.
- `SOURCE` identifies the request or immutable source revision and the relevant criteria or specification headings. Preserve existing criterion IDs.
- `OUTCOME` states the complete behavior, proof, or decision expected from this assignment.
- `SCOPE` lists the owned paths, workspace, permitted operations, and excluded work. Commands that change generated files count as writes.
- `CONTRACTS` names the interfaces, invariants, prerequisites, dependency order, and sibling ownership that affect the work.
- `VERIFY` lists permitted checks and when they may run. While siblings write, replace shared suites, builds, formatters, and migrations with explicitly permitted focused checks.
- `PROOF` states the evidence required for each criterion, including failure, privacy, state, and race scenarios where relevant.
- `COMMIT_MODE` is `none` unless the user authorizes `owned-slice`. Commit permission never grants publication permission.
- `STOP_AT` names `review-ready` or `merge-ready` for implementation. Release qualification requires its own authorization.
- `PROCEDURES` lists the skills and repository references the owner must read completely before acting. An owner reports a missing prerequisite instead of inventing a replacement workflow.
- `BINDING` identifies the source under review. Include the release candidate triple only when a candidate is bound.

Platform assignments also name the authorized environment, provider constraints, budget limits, secret interface, and resource cleanup owner. A research assignment names its question, method, safe scope, and observable learning outcome instead of promising implementation.

An authorized inspection owner supplies static reviewers with diffs, changed-path inventories, and Git metadata. A static reviewer does not collect those inputs by executing commands. No-edit runtime proof remains an assigned worker operation, not a read-only review operation.

## Ownership and concurrency

One owner receives a complete behavior, its consumers, error handling, and regression proof. A criterion is not automatically a separate assignment. Application and platform responsibilities split at an actual ownership boundary.

Independent assignments can run together only with disjoint writes and settled contracts. Parent-child containment does not imply dependency order. Shared files and generated outputs have one integration owner. That owner runs generators only after contributing writers stop.

An implementation owner may be the main session when project policy permits. A coordinator with a no-code role must delegate implementation. Independent review always uses a separate reviewer actor. Workers return evidence and proposed dispositions. The authorized coordinator decides integration, triage, binding, and technical acceptance.

The coordinator tracks each assignment's owner, state, source identity, open finding IDs, and blockers. It records a candidate triple only after binding. A running actor does not prove progress, and a delivered assignment does not prove execution started.

## Result fields

A handoff contains `OWNER`, `CHANGED FILES`, `PROOF`, and any `BLOCKER`. A details link appears only when that artifact exists.

`CHANGED FILES` lists exact paths, command-generated changes, and whether mutation stopped. `PROOF` maps each criterion to `observed pass`, `observed fail`, or `not verified`. It identifies commands, execution scope, results, and evidence locations without raw logs or secrets. Scanner proof includes coverage limitations and the manifest accounting required by the [source and evidence principle](../../principle-delivery-source-evidence/SKILL.md).

The handoff distinguishes source-complete work from author-verified work. It records unexercised paths, their blocking prerequisites, and the next owner. A launch command is not service readiness. Service readiness needs an observed health response, connection, or operation. A build or mock pass is not proof of deployment or user behavior.

A repair handoff lists the finding IDs addressed and the new proof. It identifies invalidated candidates without carrying their verdicts onto changed source. Task-created processes, containers, and persistent volumes retain their identities, observed state, cleanup authority, and cleanup owner.

## Ownership transfer

1. The current owner stops edits and mutating commands. It safely finishes or interrupts in-flight work.
2. The owner reports changed paths, intent, partial state, outstanding operations, and every process that can still write.
3. The coordinator acknowledges that checkpoint and names the next owner and ready condition.
4. The next owner confirms that no previous writer remains. A mismatch between the checkpoint and the files blocks takeover until the coordinator resolves it.
5. The previous owner makes no later edits in the transferred scope. Further changes become dependencies sent to the coordinator.

Unplanned generated changes are dependencies, not completed work. Neither owner overwrites or reverts another contributor's changes to force a clean handoff. Recovery and publication follow [Git safety](../../delivery-deliver-change/references/git-safety.md).

## Waiting and stopping

Use delivered results and finite waits. A timeout is neither failure nor success. After a missing result, stalled work, or concrete doubt, inspect once or request one checkpoint. Inspect again only after a new trigger. Redispatch only after confirmed failure and an authorized ownership transfer.

On a user stop, halt dispatch and repair. Notify active owners, safely cancel known owned jobs, and preserve partial changes. Do not wake agents to continue work or seek a verdict. Interrupted checks remain `not verified`. Completed checks retain their actual results. An agent stopping does not prove that its resources stopped.

Remove only confirmed task-owned resources within explicit cleanup authority. Preserve persistent data unless deletion is authorized. Report the current checkpoint again only when new evidence changes it.
