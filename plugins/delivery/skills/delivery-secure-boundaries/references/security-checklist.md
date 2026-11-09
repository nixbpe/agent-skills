# Delivery security checklist

## Evidence and applicability

For each applicable control, record the owning implementation, inspected scope, executed proof, result, and remaining gap. Use `observed pass`, `observed fail`, or `not verified` for checks. Mark an irrelevant control not applicable with a reason. Read the [project context](../../delivery-coordinate-work/references/project-context.md) and actual repository rules before selecting commands or policy values. Examples below define neither a new stack nor production authorization.

## Threat boundaries

- Identify who can write each request, upload, webhook, external response, queue payload, model response, environment value, process argument, filename, and job directory.
- Name credentials, personal data, payment information, privileged operations, and other protected assets.
- Examine spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege at each affected boundary.
- Write concrete abuse cases and identify the observations that prove rejection without disclosure or unintended mutation.

## Authentication and authorization

- Use the existing authentication library and session policy. Do not create a separate password or session implementation.
- Protect session cookies with `httpOnly`, `secure`, and the approved `sameSite` and lifetime policy. Do not put sessions in client-accessible storage.
- Rate-limit login and recovery separately from general request limiting. Use shared state when traffic crosses instances and verify the approved failure behavior.
- Make reset and invitation tokens time-limited and single-use. Apply the project's multi-factor and fresh-authentication requirements to sensitive operations.
- Check current membership, tenant isolation, resource ownership, and operation permission before protected lookup. Check elevated permissions per operation rather than trusting a prior screen or client flag.
- Test unauthenticated, wrong-owner, wrong-tenant, stale-membership, and insufficient-role requests. Verify both denied actions and disclosure limits.

## Input, output, and transport

- Validate external input with the shared schema, allowlists, length limits, numeric ranges, and appropriate format libraries. Client validation does not replace server enforcement.
- Parameterize database queries. Constrain command arguments and avoid shell interpretation of untrusted values. Never pass user-controlled input into `eval`.
- Preserve framework output escaping. Raw HTML requires an approved sanitizer at the untrusted boundary, not direct assignment to `innerHTML`.
- Restrict uploads by approved type and size. Validate content rather than trusting extensions or client metadata.
- Validate redirects against the approved policy. For server-side requests, use the shared outbound implementation and verify allowed destinations, blocked private and reserved addresses, redirects, TLS validation, and connection-time behavior together. A separate DNS check leaves a rebinding gap.
- Use HTTPS for external HTTP integrations unless the accepted product contract explicitly requires controlled HTTP targets. Preserve the approved exception's restrictions rather than weakening unrelated integrations.
- Use the repository's standard error envelope. Production responses must not expose stack traces, SQL, credentials, or internal validation details.
- Inspect actual CSP, HSTS, frame restrictions, content-type protections, referrer policy, and permissions policy where applicable. Use approved values rather than copying a header set without checking compatibility. Do not treat legacy browser XSS filters as an alternative to CSP and escaping.
- Restrict credentialed CORS to exact approved origins. Do not combine credentials with a wildcard origin.

## Secrets and sensitive data

- Use response allowlists to exclude password hashes, tokens, and other sensitive fields.
- Keep credentials, full payment details, and personal data out of logs and telemetry. Read secrets through the approved environment interface without literal fallbacks.
- Run the repository's actual secrets scanner within the authorized scope. Keyword searches do not replace it. Inspect relevant generated output and staged scope under the [Git safety contract](../../delivery-deliver-change/references/git-safety.md).
- Keep real environment files and private keys out of version control. Example configuration contains placeholders only.
- Apply required encryption at rest and to backups. A committed secret is compromised. An authorized owner must rotate or revoke it before history cleanup. Do not perform credential rotation without authority.

## Dependency and supply-chain controls

1. Identify the install boundary that owns the lockfile. Treat nested projects independently only when outside the workspace. Corroborate package-manager metadata, lockfiles, and CI. Stop on disagreement or competing authoritative lockfiles, and pin the manager version.
2. Before first dependency execution, disable lifecycle scripts or enforce a documented fail-closed policy. Review pending scripts and approve only required packages. Record the policy through authorized changes, then verify a clean frozen or immutable install. Never blanket-approve scripts.
3. Run the detected package manager's native audit against the committed authoritative lockfile before release. Do not claim an execution error or unsupported check as a pass.
4. Assess vulnerable-code reachability across runtime, build, test, and deployment. Critical or high reachable findings require an update, patch, replacement, or an explicitly approved effective mitigation before readiness. Confirmed unreachable critical or high findings remain tracked with evidence and a review date.
5. For moderate findings, retain the source distinction between production-reachable work for the next release cycle and development-only work tracked for later. Track low findings in regular updates. Apply the project's explicit severity mapping to readiness, and leave unclear mappings unclassified rather than guessing.
6. If no patch exists, evaluate a workaround or replacement. An exception needs the affected function, deployment context, reachability evidence, mitigation or deferral reason, authorized decision owner, and review date. An allowlist entry alone does not mitigate reachable vulnerable code.
7. Never force audit remediation automatically. Preview the diff and read changelogs. Upgrade one dependency per change, including its transitive lockfile effects, and check behavior before and after. Do not hand-edit the lockfile.
8. Where supported, verify package signatures and provenance. Investigate absent provenance rather than treating it as proof of compromise or trust.
9. Review package ownership, maintenance, release age, provenance, transitive graph, license, size, and typosquatting. Review dependency, lockfile, and script-policy changes together. Prefer existing dependencies when they already meet the need.

A runtime-versus-development label does not establish reachability. A clean audit does not prove dependency trust.

## Personal data and privacy

Classify each new field as non-personal, personal, or sensitive using the applicable policy. Personal data includes names, email addresses, IP addresses, and user or device identifiers. Sensitive data can include health, finance, location, biometrics, government identifiers, and information about minors. Sensitive categories require an approved collection basis and stricter controls.

- State the purpose of each collected field and minimize collection. Do not treat a proposed analytics metric as permission to collect personal data.
- Define retention and an executable deletion path for every store, including backups, caches, search indexes, and analytics copies. Document backup expiry or restoration controls where immediate selective deletion is not supported.
- Make data findable for required export, correction, and deletion rights. Exercise the affected paths with safe fixtures rather than claiming compliance from schema inspection.
- Obtain auditable consent where required by the approved collection and sharing policy. Treat analytics, advertising, and LLM vendors as third-party recipients. Establish the required data-processing agreement before sharing personal data.
- Resolve residency and legal obligations from the applicable users and jurisdictions. Do not hardcode one jurisdiction's law as a universal rule.
- When an incident exposes personal data, report the evidence and escalate the applicable notification clock to the authorized incident owner. Do not invent a legal deadline or silently omit the obligation.

## LLM and retrieval boundaries

- Treat model output as untrusted input. Validate and encode it before use in SQL, commands, HTML, file paths, or structured actions. Never execute generated text directly.
- Assume user messages, fetched pages, documents, retrieved text, and model responses can contain prompt injection. Prompts are not an authorization boundary. Enforce permissions and argument validation in code.
- Keep secrets, cross-tenant data, and protected internal instructions out of exposed prompt content. Anything provided to the model may appear in its output.
- Give tools and agents minimum permissions. Require applicable confirmation and authorization for destructive or irreversible actions even if a model suggests them.
- Bound tokens, request rates, spend, loop count, and recursion depth. Verify stop behavior rather than relying on a prompt to limit consumption.
- Partition retrieval and embeddings by tenant. Validate documents before indexing and enforce access during retrieval. Check that one tenant cannot retrieve another tenant's data.
- Include model and retrieval dependencies in supply-chain review. Report output-handling, injection, disclosure, excessive-agency, consumption, and retrieval-isolation evidence separately.

## Destructive derived paths

Before delete, move, or overwrite, resolve the target's real location, including symlinks. Require all of these conditions before the operation.

- The target is beneath an allowlisted root using a path-component-aware comparison.
- The target is at least one path component below the root. The root itself is never a valid target.
- Authenticated ownership evidence identifies the exact target as task-owned. Read it before the destructive call and before teardown destroys that evidence.

A marker file alone is self-attestation. Compare it with an expected owner from authenticated state and protect its integrity with restrictive ownership or a message authentication code. Local shape, a plausible directory name, or a process argument is not authorization.

On mutable shared hierarchies, prevent check/use races with descriptor-held, no-follow, beneath-root operations. If the platform cannot provide those guarantees, keep the hierarchy unchanged under exclusive control for the entire operation. If neither is possible, stop. Logging a safe rendering of the rejected path does not authorize fallback to its parent.

### Worked example for task cleanup

An authorized job owns a private temporary directory below an allowlisted task root. The coordinator supplies the expected job identity from authenticated assignment state. A user-controlled argument names a cleanup candidate. The example permits deleting only that owned directory, not the root or arbitrary contents elsewhere.

1. Open the configured task root through a trusted path. Establish exclusive control of the relevant hierarchy or obtain the platform's descriptor-based confinement guarantees before checking the candidate.
2. Resolve the candidate relative to that root without following a path outside it. Compare path components, not string prefixes. Reject the root itself, a sibling with a similar prefix, parent traversal, and a symlink escape.
3. Read the ownership record through the same protected hierarchy. Verify its integrity and compare its owner and target identity with the authenticated assignment. A candidate-created marker saying it owns itself is insufficient.
4. Confirm that cleanup authorization covers this exact directory and operation. Refuse deletion when the candidate contains persistent data whose removal was not authorized.
5. Delete through the held confined descriptors, or while the exclusive hierarchy guarantee still holds. Do not release that protection between validation and deletion.
6. If any check fails, report the rejected target safely and stop. Never retry against the allowlisted root, a parent directory, or a broader glob.

Exercise this control with disposable fixtures only. Cover the root itself, a prefix-collision sibling, traversal, a symlink escape, a forged marker, a valid owned child, and a concurrent replacement attempt when the hierarchy can be shared. Record actual observations. This worked example does not authorize destructive testing against user data.
