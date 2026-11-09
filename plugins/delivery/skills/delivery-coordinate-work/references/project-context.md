# Project context contract

This contract defines the project facts a delivery action uses. Existing instructions, source files, package scripts, and the current assignment supply those facts. A new configuration file or planning document is not required.

## Required context by operation

| Context | Source | Required when |
|---|---|---|
| Scope and exclusions | Current request and accepted issue or design | Every action |
| Acceptance criteria and revision | Accepted source and linked contracts | Implementation, review, delivery, and release |
| Role and publication authority | User authorization and project instructions | Any edit, delegation, commit, push, merge, or deployment |
| Artifact locations and identifiers | Existing project conventions | Creating or changing planning or evidence artifacts |
| Architecture and data contracts | Owning modules and project documentation | Changing shared behavior, persistence, APIs, or jobs |
| UI conventions | Existing screens and the project design system | Designing or changing user interactions |
| Focused verification commands | Package scripts, existing checks, and assignment | Implementation and repair |
| Full gates and required CI | Project scripts and workflow configuration | Claiming merge-ready or release-ready |
| Review provider and severity mapping | Project review policy | Independent review and PR repair |
| Target, credentials, resource owner, and cleanup limits | Authorized environment assignment | Platform work and runtime checks with external effects |
| Candidate manifest tooling and acceptance record | Project release process | Binding release evidence |

A field that does not apply creates no new workflow requirement. An unknown required field blocks only the operation that needs it. Repository facts can settle tooling and conventions. Only an authorized person can settle missing product choices or permissions.

## Review policy

The policy identifies the independent reviewer or review service, required review conditions, and the meaning of each source severity. It also identifies who may accept findings and who may resolve review threads.

Provider names, mentions, and command syntax are project-specific. A delivery skill does not require a particular review vendor. Provider availability alone does not establish completed review of the current head.

Static review, runtime verification, technical acceptance, and release approval are separate responsibilities. The same person may hold multiple responsibilities only where project policy allows it. Author self-review is not independent review.

## Gate policy

A gate has a command or observation, expected outcome, owner, execution environment, and required source identity. The policy distinguishes focused checks, merge gates, and release gates.

Examples of release checks include integration tests, end-to-end scenarios, image scans, migration compatibility, and rollback evidence. The applicable set comes from the project. No fixed package manager or deployment stack is assumed.

A missing command does not prove that no gate exists. Repository scripts, CI configuration, runbooks, and accepted criteria jointly define the required evidence. An unavailable required gate remains `not verified`.

## Execution policy

The main session coordinates work. It may implement a bounded task only when project policy permits that role to write code. Otherwise an authorized worker owns the edits.

The optional `delivery-worker` profile permits file edits and command execution. Its tools do not enforce path ownership or environment isolation. The assignment and runtime must supply those limits.

The optional `delivery-reviewer` profile permits source inspection without command execution or file edits. An authorized inspection owner supplies the diff, Git metadata, and runtime evidence. The profile does not grant acceptance or publication authority.

Claude plugin installations expose these profiles as `delivery:delivery-worker` and `delivery:delivery-reviewer`. Direct Claude installations and pi use the unprefixed names. Select the registered runtime name rather than assuming that a profile's filename is its invocation name.

A skill cannot create child sessions, install an extension, or enforce a permission boundary by itself. When the required runtime capability is missing, report it. Sequential self-review cannot replace a required independent reviewer.

## Evidence storage

Use the existing issue, handoff, or evidence location. Create a separate artifact only when requested or when the project requires one. Link evidence that exists. Never report an invented file path as a delivered artifact.

Keep credentials and private runtime data out of portable skills and shared evidence. Preserve accepted identifiers and field labels in project artifacts even when the skill uses more general terms.
