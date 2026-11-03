# orch-skills

A one-plugin marketplace for [Orchestra Research's AI Research Skills](https://github.com/Orchestra-Research/AI-research-SKILLs).
Upstream ships 23 category plugins, so each skill gets its category as a prefix. This marketplace puts all of them
in one plugin named `orch`, so every skill is `/orch:<skill>`, for example `/orch:autoresearch` or `/orch:grpo-rl-training`.

The skills are not copied here. `.claude-plugin/marketplace.json` points at the upstream repo, pinned to a commit.
`scripts/build.py` regenerates it from upstream's own marketplace file, and the `Sync from upstream` workflow runs it
every day at 08:00 IST, committing only when upstream changed. Run it by hand with `python3 scripts/build.py`.

Install in claude.ai: Customize -> Plugins -> Add -> Add marketplace -> this repo, then add the `orch` plugin.
Install in Claude Code: `/plugin marketplace add sowrabh/orch-skills`, then `/plugin install orch@orch-skills`.
