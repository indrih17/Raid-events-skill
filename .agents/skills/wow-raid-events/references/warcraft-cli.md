# Warcraft CLI: sources and setup

Adapted for this skill on 2026-10-06 from aurokin/warcraft_cli, SHA `dd77084311d169b812c5a3884c8441e595306aae`, package `0.6.0`. [Upstream skill](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/SKILL.md), [package manifest](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/pyproject.toml). These are adapted workflows, not a local snapshot of WoW databases. Upstream code is an external dependency; installing it does not validate every live endpoint.

## Choose a source

| Question | Provider/reference |
|---|---|
| Spell/item/NPC IDs, tooltips, comments, hotfixes | wowhead, [content](warcraft-content.md) |
| WoW API, combat-log payload, UI events | warcraft-wiki, [content](warcraft-content.md) |
| Guides and published builds | wowhead/method/icy-veins, [content](warcraft-content.md) |
| Reports, events, participants, auras, target damage | warcraftlogs, [logs](warcraft-logs.md) |
| Top-parse raid cooldown timelines and composition | lorrgs, [logs](warcraft-logs.md) |
| Mythic+ runs, seasons, affixes and profiles | raiderio |
| Local APL, talents and simulations | simc, [simulation](warcraft-simulation.md) |
| Shared Raidbots report and input | raidbots, [simulation](warcraft-simulation.md) |
| Official Game Data/Profile reads | blizzard |
| Addon metadata and changelog | curseforge |

If the source is unclear, use `warcraft resolve "<query>"`, then `warcraft search "<query>"`. Inspect failed providers, warnings, confidence and candidates. Resolve ambiguity using IDs, class/spec, version and URL; the first result is not automatically correct. Switch to the specific provider once identified.

## Portable environment

Python 3.12+ is required for this optional CLI. From the skill folder in PowerShell:

```powershell
python -m venv .warcraft-runtime
& ./.warcraft-runtime/Scripts/python.exe -m pip install -r assets/warcraft-cli-requirements.txt
$env:PYTHONUTF8 = '1'
$env:PATH = (Join-Path (Get-Location) '.warcraft-runtime/Scripts') + [IO.Path]::PathSeparator + $env:PATH
warcraft doctor
```

On POSIX use `.warcraft-runtime/bin/python` and put `.warcraft-runtime/bin` on the current session's PATH. In later sessions restore PATH or use an absolute executable path derived from the skill location. The environment is ignored by Git and must be recreated after relocating the skill. Do not install a similarly named PyPI package by guesswork or run upstream deployment commands that change global wrappers. The Python `simc` command is a wrapper; configure the actual engine binary and source separately.

The pinned requirements include `tzdata==2026.5`: on Windows the Wowhead import otherwise failed because `America/Chicago` was unavailable. `PYTHONUTF8=1` fixed a Wiki output error under legacy console encoding. These environment fixes do not modify upstream code.

Initial checks on 2026-10-06: wrapper doctor and provider help worked; live Wowhead spell 10060 and Wiki COMBAT_LOG_EVENT_UNFILTERED reads succeeded. WCL credentials and a configured SimC binary were absent, so report API extraction, talent round-trip and simulations were not validated. Other providers had interface checks, not live contract validation. Check readiness again for each new task.

## Output contract

Standard output is a JSON envelope containing `ok`, `provider`, `command`, `kind`, `schema_version`, `query`, `provenance`, `data`, and `error` on failure. Save the full response and command. Read payloads from `data`.

Global options precede subcommands, for example `warcraft --pretty search ...`. `--fields` projects selected paths; it does not traverse arrays through `data.results.name`. Missing projected fields are not proof of absence in the source. `--compact` shortens prose and lists affected paths in provenance; retain full output for evidence. `wowhead --stream` emits JSONL headers and records.

Read cache provenance, source freshness and warnings. Fetch time is not source-update time. Disable a provider's cache for one session/run with `<PROVIDER>_CACHE_BACKEND=none` when necessary; wrapper queries can reach several providers. Keep retail/PTR/beta/Classic and provider-specific ID systems separate. Expansion-aware routing does not establish universal provider coverage.

Exit codes: 0 success; 1 inspect the cause; 2 fix usage; 3 check authorization; 4 verify identity/scope; 5 upstream/network failure, allowing one delayed retry. `ok=true` does not establish completeness or confident identity.

## Other providers

Raider.IO: `raiderio dungeons`, `raiderio affixes --region eu`, `raiderio character <region> <realm> <name>`, `raiderio sample mythic-plus-runs`, `raiderio distribution mythic-plus-runs`, `raiderio cutoffs --region eu`. Preserve season, key level, roster, patch and sample size. `logged_run_id` is not a WCL report code. Composition and completion time do not prove pull windows. `last_crawled_at` can be old despite a fresh fetch; rank zero means unranked. Leaderboard samples do not represent the entire population.

Blizzard: `blizzard doctor`, `blizzard item <id>`, realm/profile commands as documented by help. Its API requires credentials. Preserve region, namespace, locale and game version. An official item record does not establish the effect's implementation in a particular SimC build.

CurseForge: `curseforge doctor`, `curseforge addon <slug-or-id>`; the API requires a key. Metadata/changelogs help identify MDT or Simulationcraft addon versions but do not establish a user's route. No standalone WowProgress provider reference was present in the audited upstream skill; inspect current help if progression research requires it.

Keep secrets and auth state out of Git. Public pages can also be accessed through web/browser tools. Missing credentials, parser failures and unavailable endpoints are limitations, not empty results.
