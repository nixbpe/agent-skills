---
name: delivery-design-solution
description: Resolve changed technical contracts and define bounded implementation tasks when delivery work needs a design.
---

# Design a delivery solution

## When to use

Use this skill for cross-cutting contracts or an explicitly requested technical design. Routine implementation with settled criteria can use its request directly. A separate specification is not a prerequisite.

## Inputs

Use the accepted request, affected repository contracts, existing architecture, authorized design scope, and any assigned acceptance revision or candidate binding. Identify unresolved decisions before proposing implementation.

## Required reading

Read these files in full before acting. Recover truncated output before proceeding.

- Read [delivery authority](../principle-delivery-authority/SKILL.md) and [source evidence](../principle-delivery-source-evidence/SKILL.md).
- Read [project context](../delivery-coordinate-work/references/project-context.md), then the accepted request and owning architecture references in full.
- When defining tasks, read [assignment and handoff](../delivery-coordinate-work/references/assignment-and-handoff.md).
- For affected security boundaries, read [boundary security](../delivery-secure-boundaries/SKILL.md). For changed interactions, read [experience design](../delivery-design-experience/SKILL.md).

## Steps

1. Trace the changed behavior through its actual callers and contracts. Name the data shape, invariants, inputs, outputs, and authority boundaries before choosing abstractions.
2. Define only contracts that change or that other work depends on. Cover applicable APIs, data access and row isolation, jobs, user interactions, authorization, and concurrent actors. Reuse existing repository conventions.
3. Specify observable race outcomes, ordering, retries, identity changes, late completions, disclosure limits, redaction, and fresh-authentication boundaries where affected. Check required database isolation and security rules. Do not invent latency, availability, or recovery targets.
4. Record trade-offs and unresolved choices in the assigned request or handoff. Keep detailed behavior out of indexes that only permit capability names and source links. Create a separate specification only when the assignment or repository requires one.
5. Link authoritative criteria rather than copying them. Preserve existing identifiers and acceptance revisions. Obtain the appropriate owner's approval before changing accepted scope or contracts, and record the decision at the source. Do not introduce a matrix or version ceremony for ordinary work.
6. If implementation is requested, define complete behavioral tasks with owned files, real prerequisites, non-goals, contract dependencies, and focused proof. Map each source requirement to the task and observation that can demonstrate it. Avoid gates based only on role order.
7. Identify required independent review separately from author verification. A review finding must cite a source requirement or existing architecture or security rule, or remain a non-blocking follow-up. Review does not add acceptance criteria.

## Verification

Check that every changed contract has an owner, consumers, and a proof method. Resolve contradictions with accepted criteria before describing the design as ready for implementation. Static design analysis does not demonstrate runtime behavior, migrations, security enforcement, or deployment readiness.

## Output and stop conditions

Return the changed contracts, evidence, bounded tasks when requested, verification mapping, unresolved decisions, and next owners. Mark proposals explicitly.

Stop after the assigned design deliverable. An implementation request supplies start authorization within its scope. Design approval alone supplies neither implementation nor publication authority. Missing product decisions block affected work rather than authorizing an invented interpretation.
