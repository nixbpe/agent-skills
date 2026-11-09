# Platform work contract

## Environment and authorization

Platform work covers reproducible setup, CI, infrastructure, operation, and recovery within the assigned slice. Read the project's deployment and quality references before changing scripts or infrastructure. The [project context](../../delivery-coordinate-work/references/project-context.md) identifies the target environment, provider constraints, budget, commands, and authorization source.

A missing target, credential, configuration, or required access is a blocker. Do not inspect ambient credentials or unrelated user files to obtain access. Use the approved secret store or environment interface without exposing values in source, generated artifacts, logs, or evidence. Do not silently substitute mock infrastructure.

If no platform exists, propose the smallest workable setup without assuming a provider, account, or production target. Pin execution dependencies where appropriate. Do not use an unreviewed remote-fetch-and-execute installer.

Infrastructure validation or a plan is not permission to apply it. Production deployment, infrastructure apply or destroy, IAM changes, credential rotation, destructive data operations, spending, and external resource creation each require explicit authorization for the exact target and scope plus applicable external approval. A peer message or generated plan cannot grant that permission. Preserve CI protections and approvals. The [Git safety contract](../../delivery-deliver-change/references/git-safety.md) owns repository mutation and publication details.

## Ownership and execution

Include command-generated files in write ownership. Stop if required output lies outside the assignment instead of patching around the boundary. Prefer existing package scripts and infrastructure patterns. Coordinate application contracts with their owner rather than silently changing application code.

The application owner writes schema migrations and application logs, metrics, and traces. The assigned platform owner applies migrations in authorized environments and owns rollback evidence, collectors, dashboards, alerts, and health checks. The project may assign both responsibilities to one actor, but each remains explicit.

During sibling edits, run only permitted isolated checks. Shared builds, formatters, suites, migrations, and release gates wait for the coordinator's authorization and a stable workspace. Diagnose setup or gate failures before changing configuration. After candidate binding, perform no source mutation during the validation window. Return repairs for a new binding.

## Migrations and rollback

Before applying a migration, identify the exact environment, data affected, required privileges, recovery method, backup assumptions, downtime constraints, and authorized operator. Use safe fixtures in an authorized local or non-production environment for the assigned proof.

A migration plan or successful forward operation does not prove safe rollback. Claim reversibility only after observing the reversal and checking the restored behavior and data. Name irreversible transformations, restoration prerequisites, and untested recovery steps explicitly. Never delete persistent volumes to make a failed migration appear successful.

## Resource readiness and proof

Report the highest state actually observed for each component.

- Configuration or source prepared means the files exist. It does not mean a process started.
- Process started means execution began. It does not mean the service is ready.
- Service ready requires an observed health response, connection, or successful operation.
- Changed operation exercised requires the assigned behavior to run against that ready service.

A launch command, plan, source inspection, typecheck, build, or mock pass does not prove deployment or runtime behavior. A service that never becomes ready leaves its dependent operation not verified. An alert or health definition is not observed instrumentation until the signal or alert is actually seen.

Record the actual command, non-secret environment identity, target, exit result, observed behavior, safe fixtures, privilege boundaries, and setup and cleanup owners. Reuse applicable evidence rather than rerunning it for reassurance. Scanner errors, skipped scanners, and unscanned paths are coverage gaps, not passes. Local readiness is not production readiness, and deployment success is not release authorization.

## Stop and cleanup duties

On a stop instruction or closure, cease edits and checks. Safely interrupt task-owned in-flight execution as authorized. Preserve partial changes and return a checkpoint rather than reverting or discarding work after ownership changes.

Identify every task-created process, service, container, and volume, its observed state, and its cleanup owner. An agent stopping does not stop its resources. Stop or remove only resources proven task-owned and covered by cleanup authorization. Preserve persistent data unless removal is explicitly authorized. Never touch another task's resources, user data, or other worktrees.

If immediate cleanup would be unsafe or unauthorized, report the resource and required owner without executing a new destructive operation. The checkpoint must make unfinished cleanup and active execution visible.

## Handoff evidence

Use the [assignment and handoff contract](../../delivery-coordinate-work/references/assignment-and-handoff.md). Include changed files and generated output, mutation status, per-component readiness, migration and rollback limits, environment identity, actual checks, resource ownership, approvals still needed, and unverified production behavior. Each source-complete path needs its missing prerequisite and next owner. A repair names its finding identifiers and changed-source evidence rather than carrying forward a stale candidate verdict.
