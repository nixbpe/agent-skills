import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parent.parent
PLUGINS = sorted((ROOT / "plugins").iterdir())
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def frontmatter_name(document):
    match = re.search(r"^name:\s*(\S+)\s*$", document.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else None


class SkillPackagingTests(unittest.TestCase):
    def test_skill_name_matches_directory(self):
        for document in ROOT.glob("plugins/*/skills/*/SKILL.md"):
            self.assertEqual(frontmatter_name(document), document.parent.name, str(document))

    def test_skill_names_are_unique_across_plugins(self):
        names = [path.parent.name for path in ROOT.glob("plugins/*/skills/*/SKILL.md")]
        self.assertEqual(sorted(names), sorted(set(names)))

    def test_skill_name_does_not_repeat_plugin_namespace(self):
        for document in ROOT.glob("plugins/*/skills/*/SKILL.md"):
            plugin = document.parents[2].name
            if document.parent.name == plugin:
                continue
            self.assertNotIn(plugin + "-", document.parent.name, str(document))

    def test_relative_links_resolve(self):
        documents = [ROOT / "README.md", *ROOT.glob("plugins/**/*.md"), *ROOT.glob("pi/**/*.md")]
        for document in documents:
            for target in LINK.findall(document.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+:", target):
                    continue
                self.assertTrue((document.parent / target).exists(), f"{document}: {target}")

    def test_marketplace_lists_every_plugin(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        listed = {entry["name"]: entry["source"] for entry in marketplace["plugins"]}
        self.assertEqual(sorted(listed), [plugin.name for plugin in PLUGINS])
        for plugin in PLUGINS:
            manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], plugin.name)
            self.assertEqual((ROOT / listed[plugin.name]).resolve(), plugin)


if __name__ == "__main__":
    unittest.main()
