---
name: delivery-secure-boundaries
description: Threat-model and assess or harden input, authorization, data, dependency, destructive-operation, and LLM trust boundaries.
---

# Secure delivery boundaries

## When to use

Use this skill when work crosses a trust boundary or needs a scoped security assessment. Assessment can remain read-only. Hardening requires implementation authority, and independent security review requires a separate reviewer actor.

## Inputs

Use the accepted scope, repository security contracts, affected assets and data flows, authorization limits, dependency install boundary, and assigned proof. Resolve named project rules from repository evidence instead of treating another project's identifiers as universal controls.

## Required reading

Read these files in full before acting. Recover truncated output before proceeding.

- Read [delivery authority](../principle-delivery-authority/SKILL.md), [source evidence](../principle-delivery-source-evidence/SKILL.md), and [trust boundaries](../principle-delivery-trust-boundaries/SKILL.md).
- Read [project context](../delivery-coordinate-work/references/project-context.md), then the accepted source and applicable architecture, authentication, isolation, outbound, privacy, and quality contracts in full.
- Read the complete [security checklist](references/security-checklist.md). Apply its personal-data, LLM, dependency, and destructive-path sections when those boundaries exist.
- For repairs, read [implementation](../delivery-implement-change/SKILL.md). For repository mutation or publication, read [Git safety](../delivery-deliver-change/references/git-safety.md).

## Steps

1. Map trust boundaries before selecting controls. Include requests, uploads, webhooks, APIs, queues, model output, process arguments, environments, shared filenames, and job paths. Trust follows who can write a value, not whether it arrived through a local channel.
2. Name assets, including credentials, personal data, privileged operations, payment data, and money movement. Apply spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege to each affected boundary. Write abuse cases beside use cases and make them part of the assigned proof.
3. Identify applicable controls in the checklist and their owning repository implementations. Reuse existing authentication, schema validation, error envelopes, outbound helpers, and rate limiters. Do not establish competing conventions from examples.
4. Obtain explicit approval before new or changed authentication, sensitive-data categories, external integrations, CORS policies, uploads, rate limits, or elevated roles and permissions. Existing authorization for the exact change is sufficient. Loading this skill supplies none.
5. In assessment-only or bound no-edit mode, produce findings without repairing source or configuration. In authorized hardening mode, implement the smallest complete control and its focused abuse-case proof within owned files.
6. Preserve the source severity label for each finding. Apply the project's explicit mapping to blocking, non-blocking, or unclassified. Unclassified findings block readiness pending clarification. Do not silently reinterpret a scanner's labels or treat an absent mapping as non-blocking.
7. Report control evidence and limitations separately. A clean scanner result does not prove safe runtime behavior, package trust, privacy compliance, or security outside its coverage.

## Verification

Use assigned checks to demonstrate boundary validation, protected-operation authorization, generic errors, required headers, shared authentication limiting, outbound restrictions, safe destructive paths, and absence of exposed secrets within inspected scope. Include relevant privacy and LLM checks.

Before release, require the detected package manager's native audit against the authoritative lockfile and approved dependency script policy. No unmitigated reachable critical or high dependency finding may pass readiness. Evidence of unreachable code must cover runtime, build, test, and deployment paths. Broader verification remains subject to assignment authority.

## Output and stop conditions

Return the trust-boundary map, assets, abuse cases, applicable controls, findings with original severity and normalized category, executed checks, coverage gaps, and next owners. Separate implemented controls from proposals and author evidence from independent review.

Stop when the scoped assessment or authorized hardening is complete. Missing boundaries, unclear authorization, unclassified findings, and required controls without proof prevent a readiness claim. Return proposed actions unexecuted when authority is absent. Security evidence does not authorize publication, production changes, or release.
