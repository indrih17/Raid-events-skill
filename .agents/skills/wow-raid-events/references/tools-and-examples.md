# Scripts and examples

Offline scripts require Python 3.10+ and the standard library. Run repository examples from its root. The optional [Warcraft CLI](warcraft-cli.md) separately requires Python 3.12+ and network dependencies.

## Compare normalized metrics

```text
python .agents/skills/wow-raid-events/scripts/compare_results.py .agents/skills/wow-raid-events/assets/example-comparison.json
python .agents/skills/wow-raid-events/scripts/compare_results.py baseline.json variant.json --json
```

Input schema_version=1 has a nonempty cases list; its first case is baseline. Each case requires label, action, owner, num_executes, num_direct_results, damage and damage_scope. Counters are numeric means or objects with numeric mean. Reject negative/nonfinite/bool/missing values and duplicate labels. Action, owner and damage scope must agree.

The tool reports ratio of means and absolute/percentage deltas; zero denominators are undefined/null. It does not infer significance, confidence intervals or causality. Damage/result is intentionally not treated as a physical metric when direct/compound scope is unknown. The bundled comparison uses explicitly synthetic values and fictional action labels.

## Extract one action

```text
python .agents/skills/wow-raid-events/scripts/extract_action.py report.json --player YOUR_PLAYER --action YOUR_ACTION --label baseline --output baseline.json
```

Supported layout is `sim.players[].stats` with children; pet stats require explicit --pet via stats_pets. Exactly one player/action match is required. The tool does not search arbitrary layouts or sum parent/child damage. Layout was checked against [report_json.cpp](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/report/json/report_json.cpp#L273); other versions may require an adapter.

Default damage-field is actual_amount, which can include direct/tick contributions. Compound amount can aggregate children. Neither default means direct-only damage. Sample objects must have mean; sum/count are not substitutes. Missing fields are rejected unless --missing-zero explicitly declares the supported zero assumption. Output records selected path, owner, spell ID, source hash and assumptions. Tests use synthetic reports.

## Build a route overlay

```text
python .agents/skills/wow-raid-events/scripts/build_route.py .agents/skills/wow-raid-events/assets/example-timeline.json --output route.simc
python .agents/skills/wow-raid-events/scripts/build_route.py .agents/skills/wow-raid-events/assets/example-timeline.json --exact --output route-exact.simc
```

Input schema_version=1 contains duration, targets and optional absolute bloodlust timestamps. Each target requires guid, name, pull, start, end, kind trash/boss, origin initial/spawned, confidence confirmed/estimated and evidence. Optional npc_id is null when unknown. Fixture identities are explicitly synthetic; do not substitute them for real GUIDs.

Reject duplicate GUIDs/name collisions and require `0 <= start < end <= duration`. Names are safe ASCII with a P01-style suffix. Different windows are not merged. Default lifetime jitter is duration_stddev=1; --exact fixes bounds. Starts use finite timestamps, baseline infrastructure spans the route, boss events are classified explicitly, and Bloodlust uses fixed 40-second bounds.

The generator accepts an already reconstructed ledger. It does not parse raw logs, establish evidence truth, define geometry/priority, predict party kill times or preserve arbitrary state across replacement actors. Choose uncertain bounds as declared sensitivity variants before generation. Output remains a teaching encounter overlay until validated with a real player profile and compatible engine.

## Repository checks

```text
python .agents/skills/wow-raid-events/scripts/check_repository.py
python -m unittest discover -s .agents/skills/wow-raid-events/scripts/tests -v
```

Checks cover simple name/description frontmatter, portable file links, required resources, synthetic fixtures and the archived original Git blob. Tests cover arithmetic, scopes, invalid values, ambiguous extraction, target identities, windows and scheduling. They are not SimC regression tests. In a standalone copied skill, source preservation is checked only when the repository archive is present.

The JSON fixtures are teaching examples. The investigation template records a future real study. No bundled generated overlay has been validated in the SimC engine.
