---
name: implement-change
description: Implement one authorized behavioral slice or produce no-edit evidence against an assigned candidate.
---

# Implement a change

## When to use

Use this skill for application, API, UI, platform, or repair work with accepted criteria. It also supports no-edit evidence assignments. Default to one assigned slice. Execute a whole plan only when the request explicitly authorizes that plan.

## Inputs

Use the outcome, source criteria, owned files, non-goals, verification scope, required proof, commit permission, sibling ownership, and any candidate binding.

## Required reading

Read these files in full before acting. They own the rules on permissions, ownership, evidence labels, untrusted data, and comments, which this skill does not repeat.

- Read [owned writes](../principle-owned-writes/SKILL.md), [source evidence](../principle-source-evidence/SKILL.md), and [trust boundaries](../principle-trust-boundaries/SKILL.md).
- Read [project context](../coordinate-work/references/project-context.md) and [assignment and handoff](../coordinate-work/references/assignment-and-handoff.md), then the actual request, repository instructions, touched contracts, and assigned procedures in full.
- Read the [enforcement layers principle](../principle-enforcement-layers/SKILL.md).
- Before any Git mutation or publication, read [Git safety](../deliver-change/references/git-safety.md).
- For infrastructure, CI, setup, environments, or migrations, read [platform work](references/platform-work.md).
- For failures, read [debugging](../debug-failure/SKILL.md). For changed security boundaries, read [boundary security](../secure-boundaries/SKILL.md). When the assignment follows a correction, read [guardrail hardening](../harden-guardrails/SKILL.md).

## Steps

1. Select implementation or no-edit evidence mode from the assignment. In no-edit mode, run only assigned checks against the specified binding. Change no source, tests, generated files, configuration, or commits. Return findings for repair rather than fixing them.
2. In implementation mode, identify accepted behavior and trace affected callers before editing. Report missing, conflicting, or infeasible criteria to their owner.
3. For a defect, preserve supplied failure evidence and establish a focused reproduction when permitted. Do not rerun a reported failure merely to confirm it. Add a regression that demonstrates the actual behavioral failure.
4. Implement the smallest complete vertical slice. Use contract-first tasks for parallel consumers or risk-first tasks for uncertain behavior. Preserve validation, data-loss prevention, security, accessibility, and conservative defaults. Unfinished user-visible behavior stays disabled when the accepted contract permits staged delivery.
5. Migrate affected callers and tests with changed contracts. Do not add compatibility shims, speculative wrappers, unrelated cleanup, invented dependencies, fake services, or missing-configuration defaults. Do not suppress type errors or alter unexplained expectations to obtain a pass. Do not reuse an existing workaround, directly or through a shared helper. Report it instead.
6. Test observable outcomes with real implementations. Mock only slow or nondeterministic external boundaries. Use focused unit tests for pure logic, integration checks for boundaries, and end-to-end checks for critical flows. Avoid tests that only echo mocks, copied fields, or forwarding.
7. Discover commands from repository scripts. Diagnose failures before another edit.
8. For an explicitly authorized plan, preserve the baseline and execute its dependency-ordered behavioral slices. Keep task and proof details in the existing handoff. Do not infer plan authorization from a capability index.
9. Report unrelated findings without fixing them.

## Verification

Report each executed command with its scope and the behavior exercised, using the source evidence labels. List skipped and proposed commands separately. For asynchronous behavior, identify coverage of ordering, retries, identity changes, and late completions. For a changed user-visible behavior, cite the feature by the name in the project's existing UI or docs and attach the observation (screenshot, recording, or state trace) from the running app when the project can produce one. Otherwise report it `not verified`. No-edit results remain author-produced evidence, not independent acceptance.

When evidence is bound, include the exact assigned binding.

## Output and stop conditions

Return the canonical handoff, including caller migrations and named gaps. Mark the slice author-verified only when executed proof covers the changed behavior and affected callers. Otherwise report source-complete with exact unverified paths or blocked.

Stop after the assigned slice unless a full plan was explicitly authorized. Stop for ambiguous criteria, out-of-scope causes, failed gates without a bounded repair, or irreversible work lacking authorization.
