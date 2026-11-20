# Candidate binding contract

This contract applies only when a release candidate is bound. Ordinary implementation and review use a commit SHA or an inspected diff.

A release candidate uses this identity triple:

| Field | Meaning |
|---|---|
| `candidateId` | A stable source identity followed by `-C<n>`, with an increasing attempt number |
| `acceptanceVersion` | An immutable revision or digest of the exact accepted criteria and contracts |
| `manifestDigest` | The digest of the candidate manifest that accounts for paths, contents, and deletions |

Use the project's existing identity format when it defines one. Otherwise use `PR-<number>`, `issue-<number>`, or an agreed source slug as the stable identity. For example, `PR-42-C1` does not require a Feature ID. Include the repository identity in the record to distinguish equal PR numbers across repositories.

If the acceptance source has no immutable version, capture its accepted contents and compute a digest. Do not use a mutable issue URL, invented version, or timestamp alone as `acceptanceVersion`.

Record the source commit or snapshot alongside the triple. Stop if a required manifest or immutable acceptance record cannot be produced with the project's available tooling. Never fabricate a digest.

Stop all writers before binding. Any candidate file change, including formatting or generated output, invalidates that binding. Record the superseded identity and create the next candidate before collecting replacement evidence.

Each gate result records the triple, command, tool version, configuration, execution identity, date, exit code, and evidence location. Reconcile scanner coverage against every manifest path. Record deleted paths and unsupported paths as skipped with reasons. Account for non-candidate exclusions separately. An exclusion cannot waive a required check of candidate source.
