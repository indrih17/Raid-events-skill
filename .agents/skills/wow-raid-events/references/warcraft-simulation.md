# SimC, Raidbots and talent transport

Adapted from the pinned [SimC](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/simc.md) and [Raidbots](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/raidbots.md) references. See [setup](warcraft-cli.md), [reproductions](minimal-repros.md) and [evidence](evidence-rules.md). The Python `simc` wrapper is separate from the SimC engine.

## Local inspection

```text
simc doctor
simc repo
simc verify-clean
simc spec-files "<class spec>"
simc describe-build --help
simc priority --help
simc inactive-actions --help
simc analysis-packet <apl-path> --targets 1
simc find-action --help
simc trace-action --help
```

Check readiness and configure the existing source/binary using documented options. Checkout/build mutates the environment and is unnecessary for a read-only question; do not replace the user's baseline. Source-search commands require rg. Record engine SHA, binary/game data and CLI SHA separately.

Use identify/describe commands for an explicit export/build source. `identify-build ok=true` with confidence none/low does not identify the spec. Inspect candidates. APL filenames are hints, not proof; multi-actor inputs require checking the selected owner.

Static priority, prune, branch, intent and opener analysis is not a full dynamic simulation. Possible/unknown branches are not inactive and a static opener does not prove first cast. Use runtime tracing when required. CLI search helps navigation but does not replace the complete [action investigation](proc-debugging.md).

## Talent transport

```text
simc validate-talent-transport --build-packet <raw-packet.json> --out <validated-packet.json>
warcraft talent-describe <validated-packet.json> --apl-path <apl-path>
simc compare-builds --help
simc modify-build --help
```

Check validation status, round-trip and unresolved rows. Build packets are accepted only by identify/decode/describe/validate-talent-transport; other commands require checked split talent strings. Do not silently lose entries, ranks or hero selection. Successful SimC encoding does not establish game import validity, point budgets or prerequisites. Classic exports are not retail builds.

Compare explicit published guide builds with citations, patch and freshness. Handoff can be partial, failed or have no build references: state which parts are missing.

## Runs and comparisons

`simc sim <profile.simc>` is the consumer wrapper; `simc run` is lower-level execution. Inspect help and final settings/disclosures. Presets, default gear/talents, profile settings and overrides can alter the intended experiment. Explicitly record settings, seeds, threads and outputs for a controlled reproduction.

Use build-harness, validate-apl and compare-apls with separate variants. Do not rewrite upstream source or baseline. Default-gear harness DPS does not predict the user's absolute damage. Warnings can indicate ignored conditions; address them before long runs.

Headline DPS/action counts do not automatically explain mechanics. Verify owner and result semantics; retain raw JSON and use the [offline tools](tools-and-examples.md) where appropriate. Preserve error estimates and use an uncertainty model suited to the actual metric rather than a universal mean-error ranking rule.

## Raidbots

```text
raidbots doctor
raidbots inspect-report <report-url-or-id>
raidbots input <report-url-or-id>
raidbots explain-input --file <addon-export.simc>
```

These commands read shared reports and hand inputs to local SimC; they do not submit cloud simulations. Preserve report/data/input citations, settings, version and freshness. Top Gear/Droptimizer reports may lack per-action detail; do not reconstruct it from headline DPS.

For local repetition save full `data.input`, inspect imports/paths and settings, and use the appropriate engine build. Reading a report is an observation of a published result; parsing checked and simulated require separate successful validation.
