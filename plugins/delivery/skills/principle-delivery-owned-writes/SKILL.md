---
name: principle-delivery-owned-writes
description: "Use when assigning software edits, running parallel workers, generating shared outputs, transferring ownership, or stopping work."
---

# Give each mutation one owner

## Assign files and shared resources

Name one owner for each write scope before work starts. Include generated files, lockfiles, schemas, migrations, test fixtures, services, and shared databases. List non-goals and dependencies in the assignment.

Parallelize only work with independent inputs and non-overlapping writes. Assign one integration owner for shared outputs. That owner regenerates shared artifacts after the contributing edits settle.

A separate agent context does not isolate files, branches, credentials, or services. Use separate worktrees or environments when writers would otherwise share mutable state. Record any shared resource and its lifecycle owner.

## Keep checks within the assignment

Workers run the focused checks their assignment permits. A coordinator schedules shared or full checks after relevant writers stop. Record checks that were deferred instead of treating them as passed.

When an unexpected change overlaps your scope, stop editing that area. Identify its owner and reconcile the dependency. Do not overwrite, restore, stash, or delete another owner's work.

## Transfer ownership deliberately

Use the assignment and handoff contract supplied by the coordinator. Report completed edits, partial work, outstanding commands, resource identities, and the next ready condition.

Before accepting ownership, confirm that the previous owner has stopped every writer in that scope. Compare the checkpoint with the actual files. Resolve discrepancies before editing.

After the coordinator acknowledges a transfer, the previous owner makes no further edits in that scope. Send new needs to the current owner.

## Stop without losing work

Stop owned mutating jobs before reporting that mutation has stopped. Preserve partial work and report its state. Do not treat a timeout, lost connection, or cancellation request as proof that a process has exited.

Release only resources you own and are authorized to remove. Preserve data and volumes unless deletion is authorized. Report surviving jobs, containers, services, and cleanup owners when shutdown cannot be confirmed.

A worker's completion message is evidence to inspect, not proof that its files are integrated or its processes have stopped.
