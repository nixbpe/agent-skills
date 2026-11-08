# agent-skills

Personal instructions and reusable resources for Claude Code and pi coding agent.
Keep one local checkout, share skills, and install agent-specific resources into
your home directory. The installer requires Python 3.9 or newer and no Python
dependencies. Workbook export has separate Python requirements listed below.
No npm publishing is needed.

The repository includes the Orbit planning suite: 1 workflow router, 12 action
skills and 8 shared principles. Commands, Claude subagents and pi prompt
templates remain empty.

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
- Put pi prompt templates in `pi/prompts/*.md`; invoke them as `/<name>`.

Claude commands are not automatically converted into pi prompts. pi subagents
require an extension; Claude's `agents/` directory is not installed into pi.

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
