# WoW Raid Events

A portable Codex skill for World of Warcraft Mythic+ encounter reconstruction and SimulationCraft research. Build target timelines from combat logs, use MDT to contextualize planned pulls, generate raid-event overlays, and validate model assumptions before comparing results.

The skill also provides workflows for Wowhead, Warcraft Wiki, Warcraft Logs, guides, Raider.IO, Lorrgs, local SimC and shared Raidbots reports. These tools retrieve source data on demand; this repository is not a local WoW database.

## Start here

- Reconstruct a route: [combat logs](.agents/skills/wow-raid-events/references/combat-log-reconstruction.md), [event modeling](.agents/skills/wow-raid-events/references/event-modeling.md), [validation](.agents/skills/wow-raid-events/references/validation.md).
- Choose a model: [fixed windows versus health-driven routes](.agents/skills/wow-raid-events/references/model-limitations.md).
- Research WoW data: [CLI setup](.agents/skills/wow-raid-events/references/warcraft-cli.md), [Wowhead/Wiki/guides](.agents/skills/wow-raid-events/references/warcraft-content.md), [WCL events](.agents/skills/wow-raid-events/references/warcraft-logs.md).
- Inspect simulations: [SimC/Raidbots](.agents/skills/wow-raid-events/references/warcraft-simulation.md), [APL/reporting](.agents/skills/wow-raid-events/references/apl-and-reporting.md).
- Check a conclusion: [evidence rules](.agents/skills/wow-raid-events/references/evidence-rules.md), [reproductions](.agents/skills/wow-raid-events/references/minimal-repros.md), [source provenance](.agents/skills/wow-raid-events/references/sources-and-code.md).

[SKILL.md](.agents/skills/wow-raid-events/SKILL.md) routes the workflow; detailed chapters, scripts and examples live inside the same folder.

## Install and use

Open this repository in Codex and invoke `$wow-raid-events`. For another project, copy the **entire** `.agents/skills/wow-raid-events` folder into that project's `.agents/skills` directory. References, scripts and assets are required; copying only SKILL.md loses the supporting resources. The previous `$raid-events` name is replaced by `$wow-raid-events`.

Example request:

> Use $wow-raid-events to reconstruct target windows from this Mythic+ log. Identify chain pulls and spawned adds, mark uncertain lifetimes, and produce a pull table and SimulationCraft encounter overlay.

Documentation and generated comments are English. The assistant can respond in the user's language.

## Tools

Offline tools need Python 3.10+ and the standard library:

```text
python .agents/skills/wow-raid-events/scripts/build_route.py .agents/skills/wow-raid-events/assets/example-timeline.json --exact --output route.simc
python .agents/skills/wow-raid-events/scripts/compare_results.py .agents/skills/wow-raid-events/assets/example-comparison.json
python .agents/skills/wow-raid-events/scripts/extract_action.py report.json --player YOUR_PLAYER --action YOUR_ACTION --label baseline --output baseline.json
python .agents/skills/wow-raid-events/scripts/check_repository.py
python -m unittest discover -s .agents/skills/wow-raid-events/scripts/tests -v
```

The route generator consumes an already reconstructed spawn ledger; it does not infer a route from raw logs. Bundled data is explicitly synthetic. Generated overlays require a real player profile and compatible SimC engine validation.

The optional Warcraft CLI needs Python 3.12+ and dependencies. Follow [setup](.agents/skills/wow-raid-events/references/warcraft-cli.md). Recreate its ignored virtual environment after copying or moving the skill. WCL requires credentials and SimC runs require a configured engine binary; installing the CLI alone provides neither.

## Evidence and maintenance

Combat logs establish observations; MDT and route plans do not prove actual lifetimes. Fixed-window simulations do not automatically predict how extra player damage shortens group kill times. Keep units, owner, aggregation, versions and uncertainty explicit. Source reading, parsing checks and simulation runs have different verification status.

See [repository rules](AGENTS.md), [maintenance scope](.agents/skills/wow-raid-events/references/knowledge-maintenance.md), [provenance](source/provenance.md) and [validation record](source/validation-record.md). The original Russian methodology is preserved unchanged in [source/original-methodology.md](source/original-methodology.md) as a historical archive, not the current skill entrypoint. Individual exploratory investigations removed from the active skill remain recoverable in Git history.
