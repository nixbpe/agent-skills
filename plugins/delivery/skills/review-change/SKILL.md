---
name: review-change
description: Review a source change and producer evidence through independent static correctness, security, and acceptance lenses without executing code.
---

# Review a change independently

## When to use

Use this skill for static review before validation, independent review of bound evidence, or a final delta review. It does not repair source, execute checks, approve release, or decide product acceptance. Use [PR repair](../repair-pr/SKILL.md) for an explicitly requested mutating PR workflow.

## Inputs

Obtain the accepted criteria, approved contracts, non-goals, source identity, author handoff, and review phase. An authorized inspection owner supplies the complete diff, changed-path inventory, deletions, and Git metadata. Obtain producer evidence and the candidate triple when the review concerns a bound candidate.

The reviewer must be a separate actor from the implementer. Stop with the exact missing input if the candidate or acceptance contract cannot be identified.

## Required reading

Read each listed file completely before acting.

- Read the [source and evidence](../principle-source-evidence/SKILL.md), [trust boundaries](../principle-trust-boundaries/SKILL.md), and [enforcement layers](../principle-enforcement-layers/SKILL.md) principles.
- For a bound candidate, read the [candidate binding contract](../qualify-release/references/candidate-binding.md).
- Read the [project context contract](../coordinate-work/references/project-context.md) and applicable repository instructions.
- Read the [security review skill](../secure-boundaries/SKILL.md). When the change touches external input, authorization, tenant scope, secrets, personal data, dependencies, outbound calls, model output, or a destructive operation, also read its [security checklist](../secure-boundaries/references/security-checklist.md). Read the checklist when that is unclear. Apply both statically in this assignment, and state in the report whether the checklist applied.

Read the assigned source, criteria, architecture rules, and affected tests in full at the relevant contract boundaries. Read UI conventions for UI changes and quality rules for evidence claims.

## Steps

1. Confirm the source, criteria, phase, and scope. Account for every changed file and hunk, including deletions. Record unrelated changes separately. Before binding, identify the reviewed source without requiring a release manifest.
2. Read the complete changed test scenarios, setup, mocks, teardown, and independent assertion oracles. Check whether the assertions detect the regression and cover boundaries, failures, state changes, and relevant interleavings. When a test could pass without the change, or a mechanism looks unnecessary, request a mutation check from the worker: remove the change or the mechanism and report which tests fail. A mechanism whose removal fails no test is unproven, and the remedy is to delete it or add the test that needs it.
3. Read each affected function or type in full, its imports, shared state, consumers, and tests. Read whole files when symbol boundaries leave behavior unclear. For generated changes, inspect the generator, contract inputs, emitted declarations, and drift evidence.
4. Trace complete sensitive paths through unchanged code. Include entry guards, tenant or permission scope, transaction and lock order, state transitions, failures, commit or rollback, cancellation, and teardown. Report an unresolved path as a context gap, not as reviewed.
5. Apply the following three lenses to the same source and criteria. Return one consolidated findings batch, not separate serial review workflows.

   - Correctness and maintainability cover behavior, readability, architecture, performance, and simplification. Check dependency direction, canonical helper reuse, explicit types, hidden fallback behavior, duplicated policy, and complexity moved rather than removed. Flag violations of the enforcement layers principle. For a repeated workaround, the remedy removes it from the changed code or cites the contract that requires it. Do not propose extracting it into a shared helper. Suggest a concrete remedy that removes concepts or restores ownership.
   - Security covers the applicable threat boundaries and checklist controls. A general review does not prove that sensitive paths ran. A missing cache identity input that can expose another user's data retains the source label `Critical` when that label applies, and requires the project's explicit blocking mapping.
   - Observable acceptance compares requirement-linked producer evidence with every accepted criterion. Preserve existing criterion IDs. Judge the evidence without running the scenario yourself.

6. Inspect source-visible performance costs. Look for N+1 requests, per-item waits, unbounded work, incompatible index shapes, leaked connections, oversized pool totals, heavy synchronous work, and unnecessary allocation. Review cache identity, staleness, invalidation, eviction, durability, and stampede handling. For UI changes, inspect measured memoization claims, heavy imports, virtualization, layout work, image dimensions and loading priority, fonts, and cache policy. Require measurements for latency, query plans, bundle size, or runtime impact. Do not invent targets or turn reference values into acceptance criteria.
7. Flag unmeasured optimization, removed load-bearing waits, disabled tests, or weakened validation. Treat structural regressions as defects only with an established contract or concrete impact. A change above about 300 lines, mixed refactoring and behavior, or growth beyond about 1000 lines prompts decomposition review, not an automatic rejection. Complete deletions and automated refactors can be larger.
8. Inspect the author's actual focused checks, required UI observations, and runtime measurements. Focused proof is not a substitute for full gate evidence. For a bound review, reconcile every criterion and scanner-covered manifest path against the exact binding. Review final deltas for resolved findings, repair regressions, unchanged identity, and complete evidence.
9. Consolidate duplicates under stable finding IDs and classify each finding under the source evidence principle. Add a normalized category.

State whether each claim comes from inspected source, producer-observed execution, or inference. Do not promote speculation, formatter preferences, pre-existing issues, or new requirements into candidate defects.

## Verification

Do not edit files or execute commands, applications, tests, builds, scanners, profilers, or benchmarks. Receive command output from the authorized owner. Missing runtime proof stays `not verified` and returns to a worker assignment.

Recommend acceptance of bound evidence only when every required criterion passes on the same binding and scanner coverage reconciles. Missing, mismatched, skipped, or errored execution is not a pass.

## Output and stop conditions

Return one batch with the phase-appropriate recommendation, source identity, files and evidence read, finding counts, open boundaries, and required next owner. Preserve the assignment's labels. Pre-validation recommendations are `ready for validation`, `changes requested`, or `blocked`. Bound-evidence recommendations are `accepted`, `changes requested`, or `not verified`.

Use `changes requested` for observed failure. Use `blocked` or `not verified` for missing prerequisites or proof, according to the review phase. Report out-of-scope observations separately. Return the report without creating a document unless the assignment requests one.

The coordinator resolves conflicting findings and decides technical acceptance. The reviewer neither repairs findings nor opens another workflow.
