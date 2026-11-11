# agent-skills

Reusable skills for Claude Code and pi.

| Suite | Use it for |
|---|---|
| [cost-estimate](#planning-skills) | Scope, effort, staffing, schedule, risk, and estimation workbooks. Does not calculate prices |
| [delivery](#software-delivery-skills) | Define, design, implement, debug, review, and qualify software changes |

## Install

Install and authenticate Claude Code or pi first. Choose one Claude installation
method to avoid loading duplicate skills.

### Install Claude plugins

Run in your terminal. Install either plugin or both:

```sh
claude plugin marketplace add nixbpe/agent-skills
claude plugin install cost-estimate@nixbpe-agent-skills
claude plugin install delivery@nixbpe-agent-skills
claude plugin list
```

Start a new Claude Code session. Installation defaults to user scope. Add
`--scope project` to an install command to limit it to a project. Plugins do not
change global instructions or install pi resources.

### pi

Requires Python 3.9 or newer. The installer installs both suites and personal
instructions for pi:

```sh
git clone https://github.com/nixbpe/agent-skills.git
cd agent-skills
python3 scripts/setup.py install --agent pi --dry-run
python3 scripts/setup.py install --agent pi
python3 scripts/setup.py check --agent pi
```

Start a fresh pi session and keep the checkout in place while installed.

### Direct Claude installation

For local skills and personal instructions instead of plugins, clone the repo
as above and run:

```sh
python3 scripts/setup.py install --agent claude --dry-run
python3 scripts/setup.py install --agent claude
python3 scripts/setup.py check --agent claude
```

Start a new session. This installs both suites and writes `~/.claude/CLAUDE.md`.
Use `--agent` explicitly. Without it, the installer targets both agents. The
installer uses standard config locations, not custom `CLAUDE_CONFIG_DIR` or
`PI_CODING_AGENT_DIR` paths.

### Switch from direct Claude installation

Back up personal instructions you need, then run from the checkout that owns
the direct installation:

```sh
python3 scripts/setup.py uninstall --agent claude --dry-run
python3 scripts/setup.py uninstall --agent claude
```

This removes installer-owned Claude resources, including the generated
`~/.claude/CLAUDE.md`. It leaves pi and unmanaged files alone. Resolve reported
ownership conflicts without deleting your edits, then install the plugins.

## Use the skills

Run the examples inside an agent session opened in your working project, not
in the terminal. Paths and issue numbers below are examples. Replace them with
your actual inputs and accepted scope.

| Installation | Invocation |
|---|---|
| Claude plugin | `/cost-estimate:<skill-name>` or `/delivery:<skill-name>` |
| Direct Claude | `/<skill-name>` |
| pi | `/skill:<skill-name>` |

For example, the same debugging request in each installation:

```text
/delivery:delivery-debug Fix the reported checkout failure using the attached logs. Verify the repair. Do not commit or push.
/delivery-debug Fix the reported checkout failure using the attached logs. Verify the repair. Do not commit or push.
/skill:delivery-debug Fix the reported checkout failure using the attached logs. Verify the repair. Do not commit or push.
```

Choose one invocation, not all three. The examples below use Claude plugins.

### Planning skills

Use the [cost-estimate guide](plugins/cost-estimate/skills/cost-estimate/SKILL.md)
when starting an estimate or deciding the next step:

```text
/cost-estimate:cost-estimate Which skill draws an approved architecture? Recommend the skill only. Do not inspect project inputs or start work.
/cost-estimate:cost-estimate Analyze docs/requirements.pdf and stop after Step 00 for review. Ask about unresolved scope before proceeding.
```

Run individual actions when their approved inputs are available. These are
separate requests, not a batch to execute without review.

#### Analyze requirements and define scope

```text
/cost-estimate:analyze-tor Analyze docs/requirements.pdf. Produce Step 00 with unclear requirements and questions for the customer.
/cost-estimate:define-scope Use approved Step 00 in output/ to produce Step 01. Separate confirmed scope, pending decisions, and exclusions.
/cost-estimate:design-architecture Use approved Step 01 in output/ to produce Step 02. Compare architecture options against integrations and NFRs. Do not assume a cloud provider.
```

#### Break down the work

```text
/cost-estimate:inventory-features Use approved Steps 01 and 02 in output/ to produce Step 03.1. Break features into units that can be estimated.
/cost-estimate:build-backlog Use approved Step 03.1 in output/ to produce Step 03.2 with backlog and UI/API inventory. Identify shared APIs.
/cost-estimate:build-wbs Use approved Step 03.2 in output/ to produce Step 03.3. Separate shared work and specialist owners. Do not estimate effort yet.
```

#### Estimate effort, staffing, and risk

```text
/cost-estimate:size-effort Use approved Step 03 artifacts in output/ to produce Step 04 Estimate and Review. Estimate Raw MD and list warranty separately. Stop before staffing.
/cost-estimate:plan-resources Use the approved Step 04 revision in output/ to produce Step 05 staffing and weekly schedule. Preserve Raw MD and separate warranty.
/cost-estimate:assess-risk Use approved Step 05 in output/ to produce Step 06. Assess external risks and separate P75 contingency from management reserve. Do not change Raw MD or Adjusted MD.
```

#### Export a workbook or draw architecture

```text
/cost-estimate:prepare-workbook Prepare output/estimation_workbook.md from approved Steps 01-06. Keep scenarios separate from the baseline. Stop for Markdown review before XLSX export.
/cost-estimate:export-workbook Export the approved output/estimation_workbook.md revision to XLSX using output/workbook_config.yaml and phase bands from Step 05. Verify totals and report Not recalculated if recalculation is unavailable.
/cost-estimate:draw-architecture Draw SVG and PNG from approved Step 02 in output/. Use its hosting model and distinguish future scenarios from the baseline.
```

Approve the specific workbook Markdown revision before requesting export.
Architecture drawings need approved Step 02, not a completed estimate.

### Software delivery skills

Supply the accepted criteria, relevant files, verification scope, and permitted
operations. Each action can run independently when its inputs are available.

#### Define and design a change

```text
/delivery:delivery-define-work Turn the saved-cart request into scope, non-goals, and observable acceptance criteria in the project's existing backlog. Ask about unresolved product decisions. Do not implement.
/delivery:delivery-design-solution Design the API and persistence changes for the approved saved-cart criteria. Compare them with existing contracts and split the work into bounded tasks. Do not edit application code.
/delivery:delivery-design-experience Design the saved-cart flow against the approved criteria. Cover empty, loading, failure, and keyboard-accessible states. Do not invent user research.
```

#### Implement or debug

```text
/delivery:delivery-debug Explain the parser failure from the supplied source and stack trace. Read files only. Do not execute commands, edit files, delegate, or create resources.
/delivery:delivery-implement-change Implement the approved saved-cart task in src/cart/ and its tests. Preserve the agreed API. Exercise the changed behavior and report evidence. Do not commit or push.
/delivery:delivery-debug Diagnose the checkout failure using the supplied reproduction and logs. Repair only the affected cart code and verify the fix. Do not change accepted behavior or publish.
```

#### Review code and security

Run code review with a reviewer separate from the implementer. Supply the full
diff, source identity, accepted criteria, and author verification evidence.

```text
/delivery:delivery-review-change Independently review the supplied saved-cart diff and author handoff against the accepted criteria. Report findings with file references and missing evidence. Do not edit files or execute commands.
/delivery:delivery-secure-boundaries Review the cart API changes for authorization, tenant isolation, and untrusted input handling. Use the project's security rules. Report evidence-backed findings without changing code or installing dependencies.
```

#### Coordinate work and handle a PR

```text
/delivery:delivery-coordinate-work Coordinate the approved saved-cart change across API and UI owners. Assign non-overlapping files and verification duties, then obtain independent review. Stop at merge-ready. Do not merge or deploy.
/delivery:delivery-deliver-change Implement issue #42 against its accepted criteria and verify it. You may create a branch, commit, push, and open a PR. Stop with the PR open. Do not merge or deploy.
/delivery:delivery-review-pr Review PR #42 at its current head against accepted criteria and required checks. You may repair in-scope defects on its branch, commit, and push. Obtain independent review and stop at merge-ready. Do not merge.
```

The last two examples explicitly authorize publication. Remove those permissions
if you only want local work or findings.

#### Qualify a release

Provide merge-ready evidence, frozen acceptance, the target environment, access
limits, and named gate owners and an independent reviewer:

```text
/delivery:delivery-qualify-release Qualify PR #42 using the supplied merge-ready evidence, frozen criteria, and approved staging environment. Use the named gate owners and independent reviewer. Stop at release-ready. Do not merge, deploy, or publish a release. Report missing prerequisites as blockers.
```

Release qualification does not authorize deployment.

### Optional execution profiles

Use a separate worker for assigned edits and a separate reviewer when independent
review is required. For Claude plugins, request the profiles by name:

```text
Use delivery:delivery-worker to implement the approved cart task within src/cart/ and its tests. Then use delivery:delivery-reviewer to independently review the supplied diff and verification evidence. Do not publish.
```

Direct Claude and pi use `delivery-worker` and `delivery-reviewer` without the
plugin prefix. For pi subagents, install the optional extension and restart pi:

```sh
pi install npm:pi-subagents
```

The worker can edit and run checks. The reviewer only reads source and supplied
evidence. Self-review does not satisfy independent review. Check the effective
profile if your project defines another profile with the same name.

## Runtime requirements

Install extra tools only for the actions you use.

| Task | Requirements |
|---|---|
| Non-text TOR input | Docling conversion as required by the analysis skill |
| XLSX export | Python 3.10+ and the bundled [requirements.txt](plugins/cost-estimate/skills/export-workbook/scripts/requirements.txt) |
| Workbook recalculation | Excel or LibreOffice. Otherwise report `Not recalculated` |
| Thai workbook layout | Noto Sans Thai or a configured Thai-capable font. Inspect the rendered workbook |
| Architecture drawings | SVG renderer and viewer, plus `rsvg-convert` for PNG export |

See the [workbook export guide](plugins/cost-estimate/skills/export-workbook/SKILL.md)
for configuration and verification. Export alone does not prove formula
recalculation or approval of the source estimate.

## Update and uninstall

### Update or remove plugins

Update only installed plugins, then start a new session:

```sh
claude plugin marketplace update nixbpe-agent-skills
claude plugin update cost-estimate@nixbpe-agent-skills
claude plugin update delivery@nixbpe-agent-skills
```

To remove either plugin:

```sh
claude plugin uninstall cost-estimate@nixbpe-agent-skills
claude plugin uninstall delivery@nixbpe-agent-skills
```

### Checkout-based installations

Run from the checkout that owns the installation. For pi:

```sh
git pull --ff-only
python3 scripts/setup.py install --agent pi
python3 scripts/setup.py check --agent pi
```

To uninstall:

```sh
python3 scripts/setup.py uninstall --agent pi --dry-run
python3 scripts/setup.py uninstall --agent pi
```

Use `--agent claude` for direct Claude installations and retain any custom
`--home` value. Uninstall removes owned resources, including generated personal
instructions. Back up edits first. Before moving the checkout, uninstall from
its original location, then move and reinstall. Restart the agent after updates.

## Troubleshooting

| Problem | Action |
|---|---|
| Skill not found | Check `claude plugin list` or run the installer's `check --agent pi` or `check --agent claude`. Start a fresh session and use the correct invocation prefix |
| Duplicate skills | Follow [Switch from direct Claude installation](#switch-from-direct-claude-installation) |
| Installer reports a conflict | Preserve your edits and resolve the reported file or package entry. Do not delete unmanaged files or ownership records to force installation |
| Links broke after moving the checkout | Restore the original location, uninstall there, then move and reinstall |
| Required input or tool is missing | Supply the requested artifact, approval, access, or dependency before retrying. An unverified result is not a pass |

Installer checks verify resources, not model authentication or skill behavior.
Keep credentials outside this repository and authenticate through each agent.

## License

MIT. See [LICENSE](LICENSE).
