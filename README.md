# agent-skills

Personal instructions and reusable resources for Claude Code and pi coding agent.
Keep one local checkout, share skills, and install agent-specific resources into
your home directory. The installer requires Python 3.9 or newer and no Python
dependencies. Workbook export has separate Python requirements listed below.
No npm publishing is needed.

The Orbit planning suite contains 1 workflow router, 12 action skills, and 8
shared principles. The English software delivery suite contains 11 action skills
and 4 shared principles. Two optional execution profiles, `delivery-worker` and
`delivery-reviewer`, have separate Claude and pi definitions. Commands and pi
prompt templates remain empty because actions are invoked as skills.

## Layout

| Path | Purpose | Installed destination |
|------|---------|-----------------------|
| `AGENTS.md` | Instructions for maintaining this repository | Not installed |
| `CLAUDE.md` | Symlink to `AGENTS.md` for this repository | Not installed |
| `instructions/personal.md` | Personal instructions for every project | Combined with rules into each agent's global instruction file |
| `rules/*.md` | Shared rules, included in filename order | Included in the generated instructions |
| `skills/<name>/SKILL.md` | Shared skills | Claude symlinks; pi package resources |
| `commands/*.md` | Claude slash commands | `~/.claude/commands/<name>.md` |
| `agents/*.md` | Claude subagent definitions | `~/.claude/agents/<name>.md` |
| `pi/prompts/*.md` | pi prompt templates | Loaded through the pi package |
| `pi/agents/*.md` | pi subagent definitions | Discovered from this package by the optional `pi-subagents` extension |
| `package.json` | Private pi package manifest | Registered by absolute checkout path |
| `scripts/setup.py` | Install, uninstall and check commands | Run from this checkout |
| `tests/test_setup.py` | Installer safety regressions | Run locally |

Generated instructions go to `~/.claude/CLAUDE.md` and
`~/.pi/agent/AGENTS.md`. They contain the rule text directly, so agents do not
need to resolve this repository's relative paths.

Claude resources are linked individually. pi loads `skills/` and
`pi/prompts/*.md` through the `packages` array in `~/.pi/agent/settings.json`.
The installer adds the local package declaration without invoking pi or
installing dependencies. It does not create duplicate pi skill symlinks.

## Orbit planning skills

Start with [Orbit cost estimate](skills/orbit-cost-estimate/SKILL.md). The guide
is written in Thai for people who prepare and review estimates. It explains
which action to choose, what inputs it needs and where each result is written.
The suite plans scope, effort, duration, resources and risk. It does not
calculate financial costs, rate cards or selling prices.

### Reading order

1. Open the workflow guide to choose an action.
2. Read that action's `SKILL.md` for prerequisites, steps, outputs and stop rules.
3. Read its linked principles for shared decisions.
4. Open `references/contract.md` for the complete schema, formulas and templates.

The short guides use the same six sections: when to use the action, required
inputs, required rules, workflow, outputs and stop conditions, and an example
request. Technical terms, artifact names, IDs and contract headings retain
their original spelling.

### Choose an action

| Goal | Skill | Planning artifact |
|---|---|---|
| Analyze a TOR or RFP | [orbit-analyze-tor](skills/orbit-analyze-tor/SKILL.md) | Step 00 |
| Define intake and scope | [orbit-define-scope](skills/orbit-define-scope/SKILL.md) | Step 01 |
| Design architecture and constraints | [orbit-design-architecture](skills/orbit-design-architecture/SKILL.md) | Step 02 |
| Inventory functional features | [orbit-inventory-features](skills/orbit-inventory-features/SKILL.md) | Step 03.1 |
| Build backlog and screen/API inventory | [orbit-build-backlog](skills/orbit-build-backlog/SKILL.md) | Step 03.2 |
| Build work packages and ownership | [orbit-build-wbs](skills/orbit-build-wbs/SKILL.md) | Step 03.3 |
| Estimate raw effort and review it | [orbit-size-effort](skills/orbit-size-effort/SKILL.md) | Step 04 Estimate and Review |
| Plan staffing, capacity and schedule | [orbit-plan-resources](skills/orbit-plan-resources/SKILL.md) | Step 05 |
| Assess risk and finalize planning | [orbit-assess-risk](skills/orbit-assess-risk/SKILL.md) | Step 06 |
| Prepare a workbook for review | [orbit-prepare-workbook](skills/orbit-prepare-workbook/SKILL.md) | Workbook Markdown |
| Export a reviewed workbook | [orbit-export-workbook](skills/orbit-export-workbook/SKILL.md) | XLSX |
| Draw an approved architecture | [orbit-draw-architecture](skills/orbit-draw-architecture/SKILL.md) | SVG and PNG |

Actions can run directly when their approved input artifacts are available.
They do not require invoking the router first. Install all 21 skills together
because actions load shared principles and references from sibling directories.
Do not copy a single `SKILL.md` without its dependencies.

Each action stops after its own output. The router advances the planning
workflow only under the recorded authorization and after quality gates pass.
Preparing workbook Markdown and exporting XLSX have a separate review gate.
Architecture diagrams need approved architecture, not a completed Step 06.

### Invoke a skill

After installation, use `/orbit-cost-estimate` in Claude Code or
`/skill:orbit-cost-estimate` in pi. Replace the router name with an action name
to invoke it directly.

For example, give the selected skill this request:

> ใช้ approved artifacts ใน output/ ประเมิน Raw MD แล้วส่ง Estimate และ Review
> เป็นคู่ให้ตรวจ อย่าทำ resource planning ต่อ

Project inputs and `output/` belong to the working project. Bundled contracts,
scripts and reference data resolve from the installed skill directory.

### Optional runtime requirements

| Action | Requirement |
|---|---|
| TOR analysis with non-text input | Docling conversion under the action's source-quality contract |
| Workbook export | Python 3.10+ and the bundled [requirements.txt](skills/orbit-export-workbook/scripts/requirements.txt), installed in a suitable environment |
| Workbook recalculation | Excel or LibreOffice; otherwise report `Not recalculated` |
| Workbook layout | Noto Sans Thai, or an installed Thai-capable font selected with `defaults.font_name`; inspect the rendered workbook before delivery |
| Diagram generation | A project-local SVG renderer and an SVG viewer; `rsvg-convert` for PNG export |

The workbook converter is bundled with the export skill. Always pass an
explicit project config with source-derived phase bands. The diagram skill
guides creation of a project-local renderer from approved nodes and edges.

After recalculation, verify the actual XLSX against its Markdown and config:

```sh
python skills/orbit-export-workbook/scripts/verify_workbook.py \
  --input output/estimation_workbook.md \
  --workbook output/estimation_workbook.xlsx \
  --config output/workbook_config.yaml \
  --output output/workbook_verification.json
```

Exit codes are `0` for `Pass`, `1` for `Warning`, `2` for `Fail`, and `3` for
input or runtime errors. The verifier independently checks supported arithmetic,
identifiers, formula transfer and warning disclosure. It does not calculate
formulas or establish whether source scope, actors or approvals are correct.
Missing formula caches remain unresolved. Review those limits alongside the
generated findings.

### Maintain the suite

Shared policy lives in `principle-orbit-*`. Each action owns its detailed
contract. The router owns selection and sequencing, not duplicate formulas.
Optional architecture profiles are references to evaluate, not required stacks.

## Software delivery skills

Use `delivery-*` for software requirements, design, implementation, review, and
release qualification. These skills use the working project's contracts and
commands. They do not require a particular stack, review vendor, or planning
hierarchy.

### Choose a delivery action

| Goal | Skill | Result |
|---|---|---|
| Define product scope and criteria | [delivery-define-work](skills/delivery-define-work/SKILL.md) | Accepted decisions, proposals, and observable criteria |
| Resolve shared technical contracts | [delivery-design-solution](skills/delivery-design-solution/SKILL.md) | Changed contracts and bounded tasks |
| Design UI flows and states | [delivery-design-experience](skills/delivery-design-experience/SKILL.md) | Flow, state, and accessibility requirements |
| Implement one authorized change | [delivery-implement-change](skills/delivery-implement-change/SKILL.md) | Changed behavior and author-produced proof |
| Diagnose and repair a failure | [delivery-debug](skills/delivery-debug/SKILL.md) | Causal diagnosis, repair, and regression proof |
| Review source and supplied evidence | [delivery-review-change](skills/delivery-review-change/SKILL.md) | Static findings and a recommendation |
| Assess security boundaries | [delivery-secure-boundaries](skills/delivery-secure-boundaries/SKILL.md) | Threats, controls, and coverage gaps |
| Assign and integrate owned work | [delivery-coordinate-work](skills/delivery-coordinate-work/SKILL.md) | Coordinated handoffs and integration evidence |
| Deliver a requested change as a PR | [delivery-deliver-change](skills/delivery-deliver-change/SKILL.md) | An unmerged PR after authorized publication and verification |
| Resolve an existing PR's findings | [delivery-review-pr](skills/delivery-review-pr/SKILL.md) | Head-specific evidence and bounded repair results |
| Qualify a merge-ready release candidate | [delivery-qualify-release](skills/delivery-qualify-release/SKILL.md) | A source-bound readiness verdict, without deployment |

Invoke an action directly when its inputs are available. For example, use
`/delivery-debug` in Claude or `/skill:delivery-debug` in pi. Supply the failure
evidence, affected project, and authorized repair scope. No router or complete
planning sequence is required.

Each action lists its inputs, required reading, steps, verification, and stop
conditions. Follow links relative to the document that contains them. Keep all
15 delivery skills installed together so their dependencies resolve.

### Apply shared principles

| Principle | Decision it governs |
|---|---|
| [principle-delivery-authority](skills/principle-delivery-authority/SKILL.md) | Scope, role limits, and separate publication permissions |
| [principle-delivery-owned-writes](skills/principle-delivery-owned-writes/SKILL.md) | File ownership, shared resources, transfer, and stopping writers |
| [principle-delivery-source-evidence](skills/principle-delivery-source-evidence/SKILL.md) | Verification status, independent review, severity mapping, and candidate identity |
| [principle-delivery-trust-boundaries](skills/principle-delivery-trust-boundaries/SKILL.md) | Untrusted input, access control, credentials, and destructive operations |

Use the [project context contract](skills/delivery-coordinate-work/references/project-context.md)
to locate project-specific facts in existing instructions, scripts, and accepted
sources. Do not create a new configuration file just to use a skill.

Ordinary implementation needs no release manifest. Release qualification binds
`candidateId`, `acceptanceVersion`, and `manifestDigest` to immutable source and
accepted criteria. PR-only work can use a source identity such as `PR-42-C1`.
Review findings retain their source severity and use the project's blocking
mapping. Unknown mappings remain unresolved.

### Choose an execution profile

The main session coordinates work. It can implement a small change when project
policy permits. Use a separate worker for role restrictions or independent
ownership. Use a separate reviewer when independent review is required.

| Profile | Tools and responsibility | Limits |
|---|---|---|
| `delivery-worker` | Reads, edits, and executes assigned checks | No implicit publication, production access, or child delegation |
| `delivery-reviewer` | Reads source and supplied evidence | No command execution, file edits, repairs, or release approval |

The coordinator supplies resolved skill paths, accepted criteria, ownership,
verification scope, and authorization through the
[assignment contract](skills/delivery-coordinate-work/references/assignment-and-handoff.md).
For a reviewer, it also supplies diffs and Git metadata collected by an
authorized inspection owner. No profile hardcodes a model.

The installer links Claude profiles from `agents/`. pi profiles are exposed by
the `pi-subagents.agents` field in `package.json`. To use them, install the
optional extension in your pi environment:

```sh
pi install npm:pi-subagents
```

Register this checkout with the repository installer, then start a fresh pi
session. The extension discovers the two definitions under `pi/agents/`.
Existing same-name project or user profiles can take precedence. Inspect the
effective definition before relying on its tools. The installer does not install
the extension or change model overrides.

The skills work without subagents for procedures that permit one actor.
Self-review does not satisfy independent review. Tool lists constrain available
operations, but they do not isolate files, credentials, or environments. Keep
mandatory permissions in runtime configuration or always-on project instructions.

### Adopt the suite in a project

Install the suite without deleting existing project instructions. Map the
project's commands, review policy, roles, and release identifiers to the shared
contracts. Preserve any stricter project restrictions.

Check skill discovery and effective worker and reviewer tools in each runtime.
Exercise a bounded implementation, a read-only review, and a failed release gate
before removing replaced project definitions. Verify that existing review and
publication requirements still hold. This repository does not migrate another
project or modify its settings during installation.

## Use

Run these commands from the checkout:

```sh
python3 scripts/setup.py check --source-only
python3 scripts/setup.py install --dry-run
python3 scripts/setup.py install
python3 scripts/setup.py check
```

The default target is both agents. Select one with `--agent claude` or
`--agent pi`. Install and authenticate the agent CLIs separately; this
repository does not manage credentials, model selection, hooks or MCP servers.

Installation targets the standard directories under the current user's home.
Use `--home /path/to/home` to target a different home or a disposable sandbox.
Custom `CLAUDE_CONFIG_DIR` and `PI_CODING_AGENT_DIR` locations are not used by the
installer. Run the agents with their standard config locations when using this
setup.

### Update

After updating the checkout or adding resources, run:

```sh
python3 scripts/setup.py install
python3 scripts/setup.py check
```

Existing linked resources reflect edits directly. Rerun installation to add or
remove Claude links and regenerate personal instructions. Restart Claude Code
or start a fresh pi session after updating resources.

Keep the checkout in place while it is installed. Before moving it, uninstall
from the original location, move it, then install again.

### Uninstall

```sh
python3 scripts/setup.py uninstall --dry-run
python3 scripts/setup.py uninstall
```

Use the same `--agent` and `--home` options to limit removal. Uninstall removes
owned files, links and the pi package declaration. It leaves unrelated
resources, settings and empty directories in place.

### Conflict handling

The installer checks both selected agents before writing anything. An existing
destination without an ownership record is a conflict, even if its contents
match. A pi package entry registered outside this installer is also a conflict.
Resolve the reported destination manually, then rerun the command.

Ownership records live in `~/.local/state/agent-skills/claude.json` and
`~/.local/state/agent-skills/pi.json`. Do not delete these while resources remain
installed. They identify the checkout, generated file hashes and symlink targets.

Edit personal instructions in this checkout, rather than editing generated
files. If a managed file or package filter changes outside the installer,
update and uninstall stop without changing it. Back up your edits and restore
the managed version before retrying.

The installer preserves unrelated pi settings and package entries, but
rewrites the settings file as formatted JSON when its package entry changes.
Symlinked config directories and JSON files are rejected. Stop agents and
other config editors while installing: writes are atomic per JSON or text
file, but the whole installation is not a transaction.

Keep API keys, tokens, sessions and machine-specific settings outside this
repository. Login through each agent separately.

## Add resources

### Shared skills

Add `skills/<name>/SKILL.md` with YAML frontmatter containing `name` and
`description`, followed by the instructions. Use a lowercase kebab-case name
matching the directory, with at most 64 characters.

This repository's checker requires nonempty, single-line `name` and
`description` values. It checks those fields rather than implementing a full
YAML validator. Optional `scripts/` and `references/` directories belong inside
the skill directory. Keep tool names and instructions portable across agents.

Claude Code invokes a skill as `/<name>`; pi uses `/skill:<name>`.

### Agent-specific resources

- Put Claude slash commands in `commands/*.md`.
- Put Claude subagent definitions in `agents/*.md`.
- Put pi subagent definitions in `pi/agents/*.md`. Install `pi-subagents` to load them through this package's manifest.
- Put pi prompt templates in `pi/prompts/*.md`; invoke them as `/<name>`.

Claude commands are not automatically converted into pi prompts. Claude's
`agents/` directory is not installed into pi. Use native tool names in each
runtime's definitions and inspect the effective profile after registration.

## Verify

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r skills/orbit-export-workbook/scripts/requirements.txt
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python scripts/setup.py check --source-only
```

The tests use disposable checkouts and home directories. They cover dry-run,
repeat installation, conflicts across agents, modified managed files, stale
links, settings preservation, package ownership and symlinked config paths.
Workbook tests cover identifier preservation, independent arithmetic, cached
formula values and disclosure of unresolved findings.

To exercise the installer without changing your actual configuration:

```sh
sandbox="$(mktemp -d)"
python3 scripts/setup.py install --home "$sandbox"
python3 scripts/setup.py check --home "$sandbox"
PI_CODING_AGENT_DIR="$sandbox/.pi/agent" pi list
python3 scripts/setup.py uninstall --home "$sandbox"
```

The sandbox remains available for inspection; remove it when finished.
`check` validates installed resources and ownership, not model authentication
or agent behavior. After installing real skills, open an unrelated project and
invoke one in each agent to verify discovery and execution.

## References

- [Claude Code instructions and rules](https://code.claude.com/docs/en/memory)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)
- [pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)

## License

MIT. See [LICENSE](LICENSE). Use, copy and modify freely.
