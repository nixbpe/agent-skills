#!/usr/bin/env python3
"""Install personal agent resources without replacing unmanaged files."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ("claude", "pi")


def digest(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def present(path):
    return path.exists() or path.is_symlink()


def safe_path(home, relative):
    path = home / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Invalid managed path: " + relative)
    for parent in (path, *path.parents):
        if parent == home:
            break
        if parent.is_symlink():
            if parent == path:
                continue
            raise ValueError("Symlinked parent directory: " + str(parent))
        if parent != path and parent.exists() and not parent.is_dir():
            raise ValueError("Parent is not a directory: " + str(parent))
    return path


def load_json(path):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError("Expected a regular JSON file: " + str(path))
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object: " + str(path))
    return value


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def matches(path, entry):
    if entry["kind"] == "link":
        return path.is_symlink() and os.readlink(path) == entry["target"]
    return (path.is_file() and not path.is_symlink()
            and digest(path.read_text(encoding="utf-8")) == entry["sha256"])


def validate_sources():
    manifest = load_json(ROOT / "package.json")
    if manifest.get("pi") != {"skills": ["./skills"], "prompts": ["./pi/prompts/*.md"]}:
        raise ValueError("package.json must expose skills/ and pi/prompts/*.md")
    for directory in ("skills", "commands", "agents", "pi/prompts"):
        if not (ROOT / directory).is_dir():
            raise ValueError("Missing resource directory: " + directory)
    for skill in sorted((ROOT / "skills").iterdir()):
        if skill.name.startswith("."):
            continue
        document = skill / "SKILL.md"
        if not skill.is_dir() or not document.is_file():
            raise ValueError("Expected skills/<name>/SKILL.md: " + str(skill))
        text = document.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        if not frontmatter:
            raise ValueError("Missing frontmatter: " + str(document))
        for field in ("name", "description"):
            values = re.findall(r"^" + field + r":[ \t]*([^\r\n]+)$", frontmatter[1], re.M)
            if len(values) != 1:
                raise ValueError("Expected one single-line " + field + ": " + str(document))
            value = values[0].strip().strip("\"'")
            if not value or value.startswith(("#", "|", ">")):
                raise ValueError("Use a nonempty single-line " + field + ": " + str(document))
            if field == "name" and (value != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 64):
                raise ValueError("Skill name must match its lowercase kebab-case directory: " + str(document))
    parts = [ROOT / "instructions/personal.md", *sorted((ROOT / "rules").glob("*.md"))]
    if len(parts) == 1:
        raise ValueError("No rules/*.md files found")
    return "\n\n".join(path.read_text(encoding="utf-8").strip() for path in parts) + "\n"


def desired_files(agent, instructions):
    instruction_path = ".claude/CLAUDE.md" if agent == "claude" else ".pi/agent/AGENTS.md"
    files = {instruction_path: {"kind": "file", "sha256": digest(instructions)}}
    if agent == "claude":
        for directory in ("skills", "commands", "agents"):
            pattern = "*/SKILL.md" if directory == "skills" else "*.md"
            for source in sorted((ROOT / directory).glob(pattern)):
                source = source.parent if directory == "skills" else source
                files[".claude/" + directory + "/" + source.name] = {
                    "kind": "link", "target": str(source)
                }
    return files


def owned_path(agent, relative):
    if agent == "pi":
        return relative == ".pi/agent/AGENTS.md"
    path = Path(relative)
    return relative == ".claude/CLAUDE.md" or (
        len(path.parts) == 3 and path.parts[0] == ".claude"
        and path.parts[1] in ("skills", "commands", "agents")
    )


def same_package(entry, settings_path):
    source = entry.get("source") if isinstance(entry, dict) else entry
    if not isinstance(source, str):
        raise ValueError("Invalid package entry in " + str(settings_path))
    if source.startswith(("/", "./", "../", "~/")):
        path = Path(source).expanduser()
        if not path.is_absolute():
            path = settings_path.parent / path
        return path.resolve() == ROOT
    return False


def plan_pi(home, mode, state, actions):
    path = safe_path(home, ".pi/agent/settings.json")
    settings = load_json(path)
    packages = settings.get("packages", [])
    if not isinstance(packages, list):
        raise ValueError("packages must be an array: " + str(path))
    matching = [entry for entry in packages if same_package(entry, path)]
    owned = state.get("package")
    if owned and matching and matching != [str(ROOT)]:
        raise ValueError("Managed pi package entry was changed: " + str(path))
    if not owned and matching:
        raise ValueError("pi package already registered outside this installer: " + str(ROOT))
    if mode == "check":
        if not owned or matching != [str(ROOT)]:
            raise ValueError("Missing managed pi package registration: " + str(path))
        return owned
    if mode == "install":
        metadata = owned or {"settings_existed": path.exists(), "packages_existed": "packages" in settings}
        if not matching:
            settings["packages"] = [*packages, str(ROOT)]
            actions.append(("write", path, json_text(settings)))
        return metadata
    if owned and matching:
        settings["packages"] = [entry for entry in packages if entry != str(ROOT)]
        if not settings["packages"] and not owned["packages_existed"]:
            del settings["packages"]
        if not settings and not owned["settings_existed"]:
            actions.append(("remove", path, None))
        else:
            actions.append(("write", path, json_text(settings)))
    return None


def plan(home, agent, mode, instructions):
    actions = []
    state_path = safe_path(home, ".local/state/agent-skills/" + agent + ".json")
    state = load_json(state_path)
    if state and (state.get("version") != 1 or state.get("source") != str(ROOT)):
        raise ValueError("State belongs to another checkout or version: " + str(state_path))
    if not state and mode == "uninstall":
        print(agent + ": nothing installed by this checkout")
        return actions
    if not state and mode == "check":
        raise ValueError(agent + ": no installation record")
    old_files = state.get("files", {})
    for relative, entry in old_files.items():
        if not owned_path(agent, relative):
            raise ValueError("Invalid ownership record: " + relative)
        path = safe_path(home, relative)
        if present(path) and not matches(path, entry):
            raise ValueError("Managed file was changed; leaving it untouched: " + str(path))
    files = desired_files(agent, instructions) if mode != "uninstall" else {}
    for relative, entry in files.items():
        path = safe_path(home, relative)
        if present(path) and relative not in old_files:
            raise ValueError("Unmanaged destination already exists: " + str(path))
        if mode == "check":
            if not matches(path, entry):
                raise ValueError("Missing or outdated resource: " + str(path))
            if entry["kind"] == "link" and not path.exists():
                raise ValueError("Broken resource symlink: " + str(path))
        elif not matches(path, entry):
            if present(path) and entry["kind"] == "link":
                actions.append(("remove", path, None))
            actions.append(("link", path, entry["target"]) if entry["kind"] == "link"
                           else ("write", path, instructions))
    for relative in old_files.keys() - files.keys():
        path = safe_path(home, relative)
        if mode == "check":
            raise ValueError("Stale installed resource; run install: " + str(path))
        if present(path):
            actions.append(("remove", path, None))
    package = plan_pi(home, mode, state, actions) if agent == "pi" else None
    if mode == "install":
        new_state = {"version": 1, "source": str(ROOT), "files": files}
        if package:
            new_state["package"] = package
        if new_state != state:
            actions.append(("write", state_path, json_text(new_state)))
    elif mode == "uninstall":
        actions.append(("remove", state_path, None))
    else:
        print(agent + ": installed resources match this checkout")
    return actions


def apply(actions, dry_run):
    for operation, path, content in actions:
        print(("would " if dry_run else "") + operation + " " + str(path))
        if dry_run:
            continue
        if operation == "remove":
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if operation == "link":
                path.symlink_to(content)
            else:
                temporary = None
                try:
                    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
                        temporary = Path(stream.name)
                        stream.write(content)
                    temporary.replace(path)
                finally:
                    if temporary is not None and temporary.exists():
                        temporary.unlink()
    if not actions:
        print("No changes needed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall", "check"))
    parser.add_argument("--agent", choices=(*AGENTS, "both"), default="both")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Target home directory (default: current user's home)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print changes without writing")
    parser.add_argument("--source-only", action="store_true", help="Check repository resources without inspecting an installation")
    args = parser.parse_args()
    if args.source_only and args.action != "check":
        parser.error("--source-only requires check")
    try:
        instructions = validate_sources() if args.action != "uninstall" else ""
        if args.source_only:
            print("Repository resources are valid.")
            return 0
        home = args.home.expanduser().resolve()
        if home.exists() and not home.is_dir():
            raise ValueError("Home is not a directory: " + str(home))
        agents = AGENTS if args.agent == "both" else (args.agent,)
        # Preflight every selected agent before mutating either installation.
        actions = [action for agent in agents for action in plan(home, agent, args.action, instructions)]
        apply(actions, args.dry_run)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
