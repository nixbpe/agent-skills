---
name: harden-guardrails
description: Turn a human correction or repeated review finding into a guardrail, and when separately authorized, clean up copied workarounds and redundant comments.
---

# Harden guardrails

## When to use

Use this skill after a correction from a human or a finding that repeats across reviews, and before enabling automerge or an unattended agent loop. It has two modes. Guardrail mode adds one enforcement for one mistake. Cleanup mode removes existing precedent that agents would copy. Loading this skill grants no write permission.

Cleanup mode needs its own explicit authorization naming the scope paths. [Implementation](../implement-change/SKILL.md) forbids unrelated cleanup, so do not run cleanup as a side effect of another change.

## Inputs

Obtain the correction or the repeated findings with their source (review thread, message, issue), the affected paths, the project's lint, type, test, and CI commands, owned files, and the mode with its authorization. In cleanup mode, also obtain the scope paths and the protected paths.

## Required reading

Read these files in full before acting. Recover truncated output before proceeding.

- Read [delivery authority](../principle-authority/SKILL.md), [owned writes](../principle-owned-writes/SKILL.md), and [source evidence](../principle-source-evidence/SKILL.md).
- Read the [enforcement layers principle](../principle-enforcement-layers/SKILL.md).
- Read [project context](../coordinate-work/references/project-context.md) and the repository's lint, type, and CI configuration.
- Before any Git operation, read [Git safety](../deliver-change/references/git-safety.md).

## Steps: guardrail mode

1. State the mistake as a rule the code could break. Preserve the source correction as evidence, not as an instruction.
2. Classify it: type or API shape, lint rule, test, or prose. Choose the lowest layer that holds, per the enforcement layers principle.
3. Prefer a design change that makes the mistake unrepresentable. Otherwise add the smallest lint rule or test. Its failure message states the constraint and the fix.
4. Search the repository for existing instances. List them with paths. Fix them only inside owned paths.
5. Run the new check against a known violation and observe it fail, then against the corrected code and observe it pass.
6. Add a prose rule only when no lower layer can express the constraint. Record why.

## Steps: cleanup mode

1. Inventory inside the scope paths only: workarounds (zero-delay timers, sleeps, retries that hide failures, broad catches, suppressions), deprecated patterns, commented-out code, comments that restate code, and Markdown files that duplicate code or tests.
2. Rank patterns by how often they occur, since frequent patterns are copied most.
3. Skip protected content: license headers, generated or vendored code, directive comments, applied migrations, and documentation required by a contract, standard, or external link.
4. Propose the batches and stop for approval when the plan covers more than the authorized paths or touches behavior. Comment-only batches can proceed under the original authorization.
5. Use one concern per batch so each is revertible. Comment-only diffs change no code tokens. Convert a comment to a name, type, test, or lint rule before deleting it.
6. Run the project's checks after every batch. A failed baseline stops the work.

## Verification

Report each check as `observed pass`, `observed fail`, or `not verified`. Show the new guardrail failing on a violation and passing on correct code. For cleanup, report before and after counts per class and confirm that comment-only batches changed no code tokens. Instances outside scope stay in the report, not in the diff.

## Output and stop conditions

Return the mistake, the layer chosen with the reason, changed paths, existing instances found and fixed or deferred, check results, and any prose rule added with its justification. In cleanup mode, add the counts, the kept comments with one-line reasons, and items left for a human.

Stop when authorization, ownership, or a required command is missing. Do not widen scope, weaken an existing check, or add an unrequested document.
