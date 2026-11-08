# agent-skills

Personal instructions and reusable resources for Claude Code and pi coding agent.
Keep one local checkout, share skills, and install agent-specific resources into
your home directory. Python 3.9 or newer is required; no Python dependencies or
npm publishing are needed.

The resource directories start empty. Installation currently provides the
personal writing rules and registers the checkout with pi.

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
python3 -B -m unittest discover -s tests -v
python3 scripts/setup.py check --source-only
```

The tests use disposable checkouts and home directories. They cover dry-run,
repeat installation, conflicts across agents, modified managed files, stale
links, settings preservation, package ownership and symlinked config paths.

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
