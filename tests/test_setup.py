import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent


class SetupSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="agent-skills-test-")
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name).resolve()
        self.repo = base / "source with spaces"
        self.home = base / "home"
        self.home.mkdir()
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def run_setup(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts/setup.py"), *args, "--home", str(self.home)],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def put(self, relative, content):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def snapshot(self):
        return {
            str(path.relative_to(self.home)): ("link", str(path.readlink())) if path.is_symlink()
            else ("file", path.read_bytes()) if path.is_file() else ("directory", None)
            for path in self.home.rglob("*")
        }

    def test_dry_run_and_repeated_install_preserve_state(self):
        self.run_setup("install", "--dry-run")
        self.assertEqual(self.snapshot(), {})
        self.run_setup("install")
        installed = self.snapshot()
        self.run_setup("install")
        self.assertEqual(self.snapshot(), installed)
        self.run_setup("uninstall", "--dry-run")
        self.assertEqual(self.snapshot(), installed)
        self.run_setup("uninstall")
        self.assertFalse(any(path.is_file() or path.is_symlink() for path in self.home.rglob("*")))
        self.run_setup("uninstall")

    def test_conflict_in_second_agent_prevents_all_changes(self):
        self.put(".pi/agent/AGENTS.md", "Existing personal instructions\n")
        before = self.snapshot()
        self.run_setup("install", success=False)
        self.assertEqual(self.snapshot(), before)

    def test_modified_owned_file_blocks_update_and_uninstall(self):
        self.run_setup("install")
        self.put(".claude/CLAUDE.md", "User changed these instructions\n")
        before = self.snapshot()
        for action in ("install", "uninstall", "check"):
            self.run_setup(action, success=False)
            self.assertEqual(self.snapshot(), before)

    def test_uninstall_preserves_unrelated_pi_settings_and_resources(self):
        settings_path = self.put(".pi/agent/settings.json", json.dumps({"theme": "dark", "packages": ["npm:other"]}))
        self.put(".claude/skills/user-skill/SKILL.md", "User-owned skill\n")
        self.run_setup("install")
        settings = json.loads(settings_path.read_text())
        self.assertEqual(settings["packages"], ["npm:other", str(self.repo)])
        settings["packages"].append("npm:added-later")
        settings["theme"] = "light"
        settings_path.write_text(json.dumps(settings))
        self.run_setup("uninstall")
        self.assertEqual(json.loads(settings_path.read_text()), {
            "theme": "light", "packages": ["npm:other", "npm:added-later"]
        })
        self.assertEqual((self.home / ".claude/skills/user-skill/SKILL.md").read_text(), "User-owned skill\n")

    def test_changed_package_filters_are_not_removed(self):
        self.run_setup("install", "--agent", "pi")
        self.put(".pi/agent/settings.json", json.dumps({"packages": [{"source": str(self.repo), "skills": []}]}))
        before = self.snapshot()
        self.run_setup("uninstall", "--agent", "pi", success=False)
        self.assertEqual(self.snapshot(), before)

    def test_removed_source_is_pruned_and_new_rules_regenerated(self):
        source = self.repo / "commands/review.md"
        source.write_text("Review the current changes.\n")
        self.run_setup("install", "--agent", "claude")
        link = self.home / ".claude/commands/review.md"
        self.assertEqual(link.read_text(), source.read_text())
        source.unlink()
        (self.repo / "rules/additional.md").write_text("Use the project's test command.\n")
        self.run_setup("check", "--agent", "claude", success=False)
        self.run_setup("install", "--agent", "claude")
        self.assertFalse(link.is_symlink())
        self.assertIn("Use the project's test command.", (self.home / ".claude/CLAUDE.md").read_text())

    def test_symlinked_config_directory_is_rejected(self):
        outside = self.home.parent / "outside"
        outside.mkdir()
        (self.home / ".claude").symlink_to(outside, target_is_directory=True)
        self.run_setup("install", success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_preexisting_package_is_not_adopted(self):
        self.put(".pi/agent/settings.json", json.dumps({"packages": [str(self.repo)]}))
        before = self.snapshot()
        self.run_setup("install", success=False)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
