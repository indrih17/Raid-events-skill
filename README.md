# WoW Raid Events

A portable Codex skill for World of Warcraft simulation research, built around two main workflows:

1. **Build Dungeon Route and Raid Events models from combat logs.** Reconstruct what the group actually fought, preserve the evidence and choose a SimulationCraft encounter model that answers the question.
2. **Investigate and improve SimulationCraft.** Trace implementation, explain unexpected results, build reproducible experiments and develop changes with controls against an unchanged baseline.

## Build encounter models from logs

Reconstruct key boundaries, pull composition, distinct target spawns, chain pulls, boss phases, spawned adds, Bloodlust and downtime. Use MDT to contextualize planned initial composition while keeping the combat log as the source of observed events.

Choose between **Dungeon Route** for a health-driven model and **Raid Events** for observed time windows. The choice matters: fixed lifetimes answer damage under the same windows, while a health-driven route can answer questions about changing kill times only with appropriate target health and group-damage assumptions.

The intended result is an evidence-backed pull table, documented model inputs and an encounter profile with explicit uncertainty and verification status. For Dungeon Route, verify the format and required inputs against the selected implementation/build; do not infer missing HP from target lifetimes. The bundled generator produces Raid Events overlays from an already reconstructed ledger; it is not an automatic raw-log parser or a Dungeon Route exporter.

Read: [combat-log reconstruction](.agents/skills/wow-raid-events/references/combat-log-reconstruction.md), [event modeling](.agents/skills/wow-raid-events/references/event-modeling.md), [model choice](.agents/skills/wow-raid-events/references/model-limitations.md), [validation](.agents/skills/wow-raid-events/references/validation.md).

## Investigate and improve SimulationCraft

Inspect the relevant source, APL, game data and report semantics. Trace an action from registration and callback through target selection, scheduling, impact and statistics. Distinguish an implementation issue from a profile mistake, an encounter approximation or a misleading metric.

Construct a minimal reproduction, compare controlled variants and check the quantities relevant to the question rather than relying on headline DPS. When a change is needed, develop it in a separate branch or checkout, keep diagnostic instrumentation distinct from the proposed fix, and verify the result against baseline and relevant regression controls. Preserve source SHA, binary build, inputs, commands and reports so another researcher can assess the result.

This is an agent workflow for research and development, not an automatic patch generator or a guarantee that every modeled behavior matches the game. Changes need evidence appropriate to their scope.

Read: [source research](.agents/skills/wow-raid-events/references/sources-and-code.md), [action investigation](.agents/skills/wow-raid-events/references/proc-debugging.md), [target selection](.agents/skills/wow-raid-events/references/target-selection.md), [minimal reproductions](.agents/skills/wow-raid-events/references/minimal-repros.md), [evidence rules](.agents/skills/wow-raid-events/references/evidence-rules.md).

## Supporting capabilities

- **WoW source research:** retrieve spell/item/NPC information, API documentation, guides and log data through Wowhead, Warcraft Wiki, Warcraft Logs, Method/Icy Veins, Raider.IO, Lorrgs, Blizzard and CurseForge. See [CLI setup](.agents/skills/wow-raid-events/references/warcraft-cli.md), [content research](.agents/skills/wow-raid-events/references/warcraft-content.md) and [WCL events](.agents/skills/wow-raid-events/references/warcraft-logs.md).
- **Simulation and build analysis:** inspect APLs and talents, compare profiles and consume shared Raidbots reports. See [SimC/Raidbots](.agents/skills/wow-raid-events/references/warcraft-simulation.md) and [APL/reporting](.agents/skills/wow-raid-events/references/apl-and-reporting.md).
- **Reproducible tooling:** generate overlays, extract action statistics, compare aligned metrics and validate the package. See [scripts and examples](.agents/skills/wow-raid-events/references/tools-and-examples.md).

These tools retrieve external data on demand; this repository is not a local WoW database. [SKILL.md](.agents/skills/wow-raid-events/SKILL.md) routes the workflow; supporting references, scripts and assets live in the same folder.

## Install and use

Open this repository in Codex and invoke `$wow-raid-events`. For another project, copy the **entire** `.agents/skills/wow-raid-events` folder into that project's `.agents/skills` directory. References, scripts and assets are required; copying only SKILL.md loses the supporting resources. The previous `$raid-events` name is replaced by `$wow-raid-events`.

Example requests:

> Use $wow-raid-events to reconstruct this Mythic+ run from its combat log. Build a pull table, choose Dungeon Route or Raid Events for the question, and document missing inputs, uncertain windows and validation status.

> Use $wow-raid-events to investigate this unexpected SimulationCraft result. Trace the relevant implementation, create a minimal reproduction, and develop and validate a fix if the evidence supports one.

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
