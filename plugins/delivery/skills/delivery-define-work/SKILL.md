---
name: delivery-define-work
description: Define or refine product scope, observable acceptance criteria, outcome metrics, and real dependencies for assigned work.
---

# Define delivery work

## When to use

Use this skill for a product decision, discovery question, backlog item, readiness assessment, or dependency map. Work at the assigned planning level. Refining a child does not authorize rewriting its parent.

## Inputs

Use the request, authorized scope, current accepted decisions, relevant research, and existing backlog. Resolve the project's hierarchy, identifiers, templates, and allowed artifact locations from repository instructions. Do not impose a universal hierarchy or invent research, commitments, dates, or approval.

## Required reading

Read these files in full before acting. Recover truncated output before proceeding.

- Read [delivery authority](../principle-delivery-authority/SKILL.md) and [source evidence](../principle-delivery-source-evidence/SKILL.md).
- Read [project context](../delivery-coordinate-work/references/project-context.md), then the applicable product instructions, templates, accepted source, and supplied evidence in full.
- For changed interactions, read [experience design](../delivery-design-experience/SKILL.md) and the project's design system before specifying the flow.

## Steps

1. Identify the exact decision and reporting cutoff. Separate accepted decisions from proposals, stakeholder suggestions, and assumptions. Return clarification questions without inventing their answers.
2. Preserve existing identities and accepted terminology. Mark proposed identities as drafts when the project requires approval. Bind approval to the exact content revision, not merely an item's title or status.
3. Describe the user outcome, scope, non-goals, permissions, limits, and observable behavior in the assigned request or artifact. Keep capability indexes limited to the information their repository contract permits. Do not create a separate planning document by default.
4. Keep stories end-to-end across their success, empty, error, and permission paths. Do not turn implementation layers into separate user stories. Leave architecture, estimates, concurrency, security controls, technical tasks, and verification commands to their authorized owners.
5. Write concrete acceptance criteria for boundaries and failure outcomes. Preserve existing criterion identifiers and accepted invariants. Label unresolved semantics and alternatives as proposals for a named decision owner.
6. Map real dependencies using the predecessor, dependent item, required input, owner, and ready condition. Separate containment from blocking. Reject role-order gates, dependency cycles, and waits for a parent to be complete without a missing input. Mark an unconfirmed owner as an ownership blocker.
7. Define each outcome metric's meaning, unit, population, window, source, baseline, and guardrails. Label unknown baselines and unapproved targets as proposals. Place research at the closest justified parent with a learning question and exit condition. Technical research remains with the technical owner.
8. Surface overlap, contradictions, and conflicts with accepted direction. Request a decision only for unresolved product choices or a scope change. Do not change criteria to make an implementation pass.

## Verification

Check that each criterion names an observable result and that each factual claim cites inspected evidence. Check dependency inputs and owners against actual contracts. Report missing evidence rather than inventing readiness. This is requirements analysis, not candidate verification, technical acceptance, measured outcome achievement, or release approval.

## Output and stop conditions

Return the complete assigned artifact, not only identifiers or a synopsis. Include its identity and revision when used, parent links, scope, flows, criteria, approved decisions, evidence and counterevidence, assumptions, and blockers. Report what remains unapproved and name the next owner with the exact required input.

Stop at the requested planning boundary. Missing critical evidence or conflicting commitments block the affected decision. Product approval does not authorize implementation, publication, deployment, or release.
