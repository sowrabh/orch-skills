"""Rebuild .claude-plugin/marketplace.json from Orchestra Research's marketplace.

Every skill across their category plugins goes into one plugin named `orch`,
so the skills are invoked as /orch:<skill>. The plugin source is pinned to
upstream's current main commit, so content changes arrive as a commit here.
"""
import json
import pathlib
import subprocess
import sys
import urllib.request

UPSTREAM = "Orchestra-Research/AI-research-SKILLs"
OUT = pathlib.Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"


def upstream_head():
    out = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{UPSTREAM}.git", "refs/heads/main"],
        check=True, capture_output=True, text=True,
    ).stdout.split()
    return out[0]


def upstream_marketplace(sha):
    url = f"https://raw.githubusercontent.com/{UPSTREAM}/{sha}/.claude-plugin/marketplace.json"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def build():
    sha = upstream_head()
    up = upstream_marketplace(sha)
    skills = []
    for plugin in up["plugins"]:
        for path in plugin.get("skills", []):
            if path not in skills:
                skills.append(path)
    return {
        "name": "orch-skills",
        "owner": {"name": "sowrabh"},
        "metadata": {
            "description": (
                f"Orchestra Research's AI Research Skills (https://github.com/{UPSTREAM}) "
                "as one plugin, so every skill shares the orch: prefix."
            ),
            "version": up.get("metadata", {}).get("version"),
        },
        "plugins": [
            {
                "name": "orch",
                "description": f"All {len(skills)} AI Research Skills from Orchestra Research: research orchestration, ideation, training, fine-tuning, post-training, evaluation, interpretability, inference, and paper writing.",
                "source": {"source": "github", "repo": UPSTREAM, "sha": sha},
                "strict": False,
                "skills": skills,
            }
        ],
    }


def main():
    new = json.dumps(build(), indent=2) + "\n"
    old = OUT.read_text() if OUT.exists() else ""
    if new == old:
        print("unchanged")
        return 0
    OUT.write_text(new)
    print("updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
