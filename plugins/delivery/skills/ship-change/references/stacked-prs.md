# Stacked PRs

A stack is a set of PRs where each PR's base is the head branch of the PR below it. Run the [ship loop](../SKILL.md) once per PR, bottom-up, in merge order. Each PR has its own state record, head SHA and repair caps. A lower PR's new head is the expected base of the PR above it, so it is not the drift that sends a change to `BLOCKED`.

## Intake

Ask once for the whole stack, not per PR:

- The permission bundle of the loop, for every branch in the stack.
- Whether a PR that reaches a cap blocks only the PRs above it or the whole stack. The default is only the PRs above it. A capped PR still needs new user approval for further rounds. The policy decides only whether independent PRs continue.

## Merge-down

Merge down when a lower PR reaches `MERGE_READY`, not after each of its repair pushes. Until then the PRs above it keep their own loops on the head they last merged, and none of them reports `MERGE_READY`.

1. Fetch the lower branch and merge it into the PR directly above it under [merging the base](../../deliver-change/references/git-safety.md#merging-the-base). PRs further up receive it when that PR in turn reaches `MERGE_READY`.
2. Rerun the gates on the merged branch. Evidence covers only the paths the merge left unchanged.
3. Push the branch, then request independent review for its new head.

A merge-down without conflicts is not a repair round. Resolving a textual conflict is a repair by the owner of the upper PR and counts as one round against that PR's three-round cap. When both sides implement the same contract, it is a product decision under Git safety.

## State changes

- A merge-down changes the upper PR's head, so its earlier review and CI claims no longer hold. It returns to `AWAITING`, including from `MERGE_READY`.
- When the stack's own base moves, the bottom PR handles it under the drift rules of the loop. The result reaches the PRs above through merge-down.
- When a lower PR becomes `BLOCKED`, `CLOSED`, or `SUPERSEDED`, or merges in a way that rewrites its commits, every PR above it goes to `BLOCKED` with the decision needed.

## Record

Each PR's `ship-change-state: v1` record adds its position in the stack, the PR below it, the lower PR's head SHA that was last merged down, and the list of PRs above it.

## Report

Return one table with the merge order, each PR's head SHA, CI and review state, rounds used and open findings. State that every PR is unmerged and that retargeting each PR's base after the one below it merges is the user's action.
