# agent-skills

Reusable prompts that nixbpe uses with coding agents: a shared `AGENTS.md`
with its rule files, slash commands, skills and subagent definitions. Copy
what you need into your own project or home directory. MIT licensed.

## Layout

| Path | What it holds | Where it goes when you use it |
|------|---------------|-------------------------------|
| `AGENTS.md` | Instructions for any agent that reads `AGENTS.md` (Codex, Cursor, Copilot and others). Points to the rule files under `rules/`. | Project root |
| `rules/` | Rule files that `AGENTS.md` refers to. `writing-style.md` holds the writing style rules for docs, reviews, commit messages, comments and replies, in Thai and English. | Project root, next to `AGENTS.md` |
| `CLAUDE.md` | Symlink to `AGENTS.md`, so Claude Code reads the same file. | Project root |
| `commands/` | Slash commands, one Markdown file per command. | `.claude/commands/` or `~/.claude/commands/` |
| `skills/` | Skills, one folder per skill with a `SKILL.md` inside. | `.claude/skills/` or `~/.claude/skills/` |
| `agents/` | Subagent definitions, one Markdown file per agent. | `.claude/agents/` or `~/.claude/agents/` |

A `.claude/` path applies to one repo. A `~/.claude/` path applies to every
project on the machine.

## Use

Copy the instruction file and its rules into a project:

```sh
cp path/to/agent-skills/AGENTS.md .
cp -r path/to/agent-skills/rules .
ln -s AGENTS.md CLAUDE.md
```

Install a command, skill or agent for one project:

```sh
mkdir -p .claude/commands .claude/skills .claude/agents
cp path/to/agent-skills/commands/<name>.md .claude/commands/
cp -r path/to/agent-skills/skills/<name> .claude/skills/
cp path/to/agent-skills/agents/<name>.md .claude/agents/
```

Replace `.claude/` with `~/.claude/` to install for every project.

Commands run as `/<name>`. Skills load when their description matches the task,
or when invoked as `/<name>`. Agents run through the Agent tool by name.

## License

MIT. See [LICENSE](LICENSE). Use, copy and modify freely.
