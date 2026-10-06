---
name: wow-raid-events
description: Reconstruct World of Warcraft Mythic+ target timelines from combat logs and MDT, build SimulationCraft raid events, validate encounter models and APLs, and research WoW data through Wowhead, Warcraft Wiki and Warcraft Logs.
---

# WoW Raid Events

Turn observed World of Warcraft encounters into documented SimulationCraft models. Support route reconstruction, source research and reproducible comparisons. Respond in the user's language; keep reusable documentation and generated comments in English unless requested otherwise.

## Choose a reference

- Reconstruct a route: [combat logs](references/combat-log-reconstruction.md), [event modeling](references/event-modeling.md), [model limitations](references/model-limitations.md).
- Research game data: [Warcraft CLI setup](references/warcraft-cli.md), [Wowhead, Wiki and guides](references/warcraft-content.md), [WCL and Lorrgs](references/warcraft-logs.md).
- Inspect or compare simulations: [SimC and Raidbots](references/warcraft-simulation.md), [APL and reporting](references/apl-and-reporting.md).
- Investigate an action when requested: [proc debugging](references/proc-debugging.md), [target selection](references/target-selection.md).
- Verify a conclusion: [evidence rules](references/evidence-rules.md), [minimal reproductions](references/minimal-repros.md), [validation](references/validation.md), [source audit](references/source-audit-2026-10-06.md).
- Workflows and resources: [methodology](references/methodology.md), [scripts and examples](references/tools-and-examples.md), [knowledge maintenance](references/knowledge-maintenance.md).

Load only the references relevant to the task. Distribute the entire skill folder, including references, scripts and assets.

## Workflow

1. Define the question, measured quantity and available artifacts. Record missing information.
2. For a route, establish key boundaries, roster and a ledger of distinct target spawns. Build a pull table before generating events. Record phases, spawned targets, Bloodlust, downtime and uncertainty; do not duplicate surviving targets across chain pulls.
3. Choose a model that answers the question. Fixed lifetimes preserve observed windows; they do not predict how extra player damage changes group kill times.
4. Record the SimC source SHA, binary build, game data, profile and run settings. For an implementation question, follow registration, callback, target selection, impact and statistics rather than treating one source fragment as a complete explanation.
5. Use a minimal control that changes one factor. Check the event timeline separately from statistical series. Verify metric units, owners, result categories and aggregation.
6. Separate observations, source facts, hypotheses and unknowns. Keep provenance and report the verification status of every profile.
7. Deliver the result, limits, inputs, commands and sources. Save new verified knowledge only when it adds something useful, following the maintenance rules.

## Invariants

- Combat logs establish observations; MDT describes planned initial composition. Neither a route plan nor a guide proves target lifetimes.
- Never invent GUIDs, IDs, HP, timestamps, simulation outputs or unavailable history.
- Keep the observed, attackable and priority windows distinct. Target replacement may lose state continuity.
- Duration-based adds can have synthetic HP. Additional DPS does not automatically shorten their lifetime.
- A finite timestamp list controls event starts. Check scheduler behavior and duration bounds in the actual build.
- The route generator retains `duration_stddev=1` for approximate windows; use `--exact` for fixed lifetime bounds.
- Executions, direct results, ticks, damage and proc counts require action-specific interpretation. Headline DPS alone does not explain a mechanism.
- Do not edit source logs or upstream SimC to obtain a desired result. Keep diagnostic patches separate from baseline.

## Deliverables

For routes: pull table, then one continuous SimC block with English comments and PULL separators, followed by verification status and limitations.

For investigations: question, observations, checked code, conclusion, hypotheses/unknowns and reproduction artifacts. Use the [investigation template](assets/investigation-template.md).
