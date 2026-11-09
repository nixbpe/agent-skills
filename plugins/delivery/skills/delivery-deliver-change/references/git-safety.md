# Git safety and publication

## Permissions

Implementation, commit, push, PR creation, review posting, thread resolution, merge, deployment, force-push, and history rewrite are separate permissions. Loading or invoking a skill grants none of them. Passing checks also grants none.

Use `COMMIT_MODE: none` when commit authority is absent or unclear. With explicit `owned-slice` permission, the named owner may commit only its assigned behavior and proof. One integration owner handles cross-slice commits and any separately authorized publication. Relay the exact target and scope of each permission to that owner.

An invocation that asks for delivery does not silently override `COMMIT_MODE: none`. Finish authorized local work and report the missing permission before any unauthorized operation. A permission for one source, branch, or target does not transfer to another.

## Branches and checkpoints

Follow established branch conventions. Prefer short-lived branches and one cohesive change per branch when the project has no contrary policy. Use the project's feature, fix, chore, or refactor naming convention rather than inventing an identity. For a request without an issue, cite the request and use `Closes: none` where the PR template requires an issue field.

If branch creation is authorized and the work starts on the default branch, create the scoped working branch before edits. Do not switch a shared directory beneath other writers. Use isolated worktrees for parallel branches or experiments.

A scoped diff or isolated worktree provides a checkpoint without a commit. Save owned changes before removing a workspace. Workspace cleanup does not preserve uncommitted work automatically.

Never use repository-wide `git reset --hard`, `git restore`, `git clean`, or stash in a dirty or shared worktree. Restore only authorized owned paths or hunks after confirming that no later writer touched them. Unclear ownership blocks recovery. Preserve user changes and partial work on stop or handover.

## Commit gates

Before an authorized commit, require all of these conditions.

- The commit contains one logical behavior and its proof. It does not absorb unrelated dependencies, refactors, formatting, or user work.
- The owner has completed the applicable project checks. Documentation-only changes need their applicable reference and formatting checks, not unrelated application gates.
- The owner stages exact owned paths, not an unbounded repository-wide selection.
- The owner inspects `git diff --cached --name-only` and `git diff --cached --check`.
- The staged bytes and deletions match the accepted source. When a candidate is bound, reconcile the staged content against its manifest. Ordinary implementation does not need a release manifest.
- No secret, unexpected generated output, ambient file, or mismatched staged content remains.

Any failed condition blocks the commit. A source-changing formatter or generator invalidates bound evidence under the [source and evidence principle](../../principle-delivery-source-evidence/SKILL.md).

Use the repository's commit message convention. If none exists, use `<type>: <short description>` with `feat`, `fix`, `refactor`, `test`, `docs`, or `chore`. Keep the subject at most 72 characters without a trailing period. The optional body explains why.

Prefer small reviewable commits. About 100 changed lines is a sizing prompt, not a gate. Changes beyond about 1000 lines need a cohesive split or an explanation such as a complete deletion or automated migration. Never create scaffold-only commits merely to meet a size target.

## Generated files and secrets

Commit generated files only when repository policy requires them. Lockfiles and migrations may be required source. Build output, real `.env` files, private keys, and unshared IDE settings do not belong in a commit.

Use the established ignore policy for dependencies, build output, local environment values, and private keys. Do not add exclusions that hide candidate source or required evidence. Report accidental secret exposure through the project's security procedure without reproducing the value.

Shared generated outputs have one integration owner under the [assignment and handoff contract](../../delivery-coordinate-work/references/assignment-and-handoff.md). Other owners return the required change instead of running a command that overwrites shared output.

## Publication gates

Push only to the authorized branch after the required local checks pass. Open or update a PR only with the matching permission. Follow its template and include the source, delivered scope, risks, criterion-linked evidence, and gate results for the exact head SHA. Keep detailed worker handoffs outside the PR body.

Use existing protections and approval gates. Never bypass a required check or fabricate a green status. Never force-push a shared branch without explicit authorization. A PR repair assignment forbids force-push, history rewrite, retargeting, and changes to other branches even when the owner can push normal repair commits.

Merge-ready means that the required review and CI conditions pass on the same head. It does not authorize merge, release, deployment, or dependent follow-up work. Branch deletion after merge also requires applicable cleanup authority.

If publication authority or a required gate is missing, report the local result, failed or unverified conditions, and the exact next permission or evidence needed. Do not claim that an unopened PR exists or that a pending CI run passed.
