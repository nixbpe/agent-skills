---
name: delivery-design-experience
description: Specify user flows, interaction states, and accessibility behavior for an assigned delivery or discovery question.
---

# Design the delivery experience

## When to use

Use this skill to design or clarify an interaction, assess implementation against an accepted flow, or answer a bounded discovery question. It does not authorize code changes or new product scope.

## Inputs

Use the assigned user goal or discovery question, intended audience when known, accepted criteria, relevant constraints, existing interactions, and supplied research. Separate known facts, assumptions, and proposals.

## Required reading

Read these files in full before acting. Recover truncated output before proceeding.

- Read [delivery authority](../principle-delivery-authority/SKILL.md) and [source evidence](../principle-delivery-source-evidence/SKILL.md).
- Read [project context](../delivery-coordinate-work/references/project-context.md), then the accepted request, project design system, accessibility rules, relevant routes and components, and supplied research in full.
- If product scope needs refinement, read [work definition](../delivery-define-work/SKILL.md). Do not silently convert a design choice into an accepted requirement.

## Steps

1. Restate the bounded user goal and current criteria. For discovery, name the question, method, safe scope, and learning exit. Ask only for critical facts or preferences that the repository and evidence cannot answer.
2. Describe entry points, the main flow, alternate paths, exits, and recovery paths. Follow the existing layout and content conventions rather than selecting a new design system.
3. Specify loading, empty, success, validation, error, and permission states. Include recovery actions, retained input, retry behavior, and disabled controls. Mark a state inapplicable only with a reason grounded in the flow.
4. Describe content hierarchy, labels, actions, navigation, and responsive behavior. Add a compact wireframe only when it resolves an interaction question.
5. Specify keyboard navigation, focus movement, accessible names, status announcements, contrast requirements, and error association using the project's accessibility conventions.
6. Trace each changed behavior to observable criteria. Label unaccepted designs and criterion changes as proposals. Send scope changes to the product decision owner instead of approving them yourself.
7. Return the flow in the assigned request or response. Create a separate design document only when authorized. Do not choose a new stack, integration, business requirement, API, or schema as part of experience design.

## Verification

Compare the proposed flow with inspected components and accepted criteria. Distinguish source inspection from visual, keyboard, screen-reader, and usability testing. Claim those runtime checks only when actually performed with appropriate authority. Do not infer accessibility compliance from a component name or a static review.

## Output and stop conditions

Return the complete requested flow, state descriptions, accessibility notes, optional wireframe, evidence, open decisions, and next owner. Report whether the design is drafted, proposed for approval, or blocked. For a narrow question, return the answer and supporting evidence rather than expanding into a full design.

Stop when the assigned design or discovery question is answered. Missing critical inputs block the affected decision. Design approval is not implementation readiness, start authorization, independent acceptance, or release approval.
