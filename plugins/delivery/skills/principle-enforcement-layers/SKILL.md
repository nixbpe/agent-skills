---
name: principle-enforcement-layers
description: "Use when writing or reviewing code, comments, docs, or rules, and when a human correction or repeated review finding suggests a missing guardrail."
---

# Enforce at the lowest layer

## Pick the lowest layer that holds

Put each constraint in the lowest layer that can enforce it. Earlier layers are checked by machines on every change. Later layers depend on a reader noticing.

1. Codebase design: names, types, API shape, module boundaries that make the mistake unrepresentable.
2. Static analysis: type checks, lint rules, dependency-boundary checks, CI checks.
3. Verification: tests and runtime observation of the behavior.
4. Prose: repository instructions, skill text, documentation.
5. Human review.

Add prose only when layers 1 to 3 cannot express the constraint, and state why. Move a recurring review finding down a layer instead of repeating the comment.

## Treat existing code as precedent

Agents copy what they find. Do not copy a workaround, deprecated API, retry, sleep, zero-delay timer, broad catch, or suppression because it appears elsewhere in the repository. Report the instance in the handoff. Fix it only inside the assigned scope.

Do not mask a symptom. Find the cause, or stop and report the missing evidence.

## Turn corrections into guardrails

A human correction or a finding that repeats is a missing guardrail. In order, propose:

1. A design or type change that removes the mistake.
2. A lint rule or test whose failure message states the constraint and the fix.
3. A prose rule, only when the first two are impossible, with the reason.

Search for existing instances of the same mistake and list them. Do not record a one-off correction as a permanent rule.

## Keep comments and documents scarce

Express intent through names, types, tests, and lint messages. A comment is allowed only when all of these hold:

- No name, type, test, or lint rule can carry the constraint.
- It states why (an external fact, a non-obvious invariant, a spec or ticket reference), never what the code does.
- It takes one or two lines and links the source when one exists.

Do not write comments that restate code, narrate history, hold a TODO without a tracked issue ID, justify a workaround, or contain commented-out code. Remove such comments from lines you already modify.

Do not create or extend Markdown files unless the assignment asks for one. Do not repeat in prose what code, types, or tests already state. Existing license headers, directive comments (`eslint-disable`, `@ts-expect-error`, `# noqa`), and documentation required by a contract or standard stay unchanged.

## Report what the layers proved

Name the layer that enforces each new constraint and the command or observation that proves it. A constraint that exists only in prose is reported as unenforced.
