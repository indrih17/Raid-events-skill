# Warcraft Logs, Mythic+ events and Lorrgs

Interfaces come from the pinned [WCL reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/warcraftlogs.md). See [setup](warcraft-cli.md) and [reconstruction](combat-log-reconstruction.md).

## Access and scope

Check `warcraftlogs doctor`, `warcraftlogs auth status` and `warcraftlogs rate-limit`. Public API reads require `WARCRAFTLOGS_CLIENT_ID` and `WARCRAFTLOGS_CLIENT_SECRET`. Private reports require authorized user OAuth and appropriate scopes, including `view-private-reports`; `view-user-profile` alone is insufficient. Login/PKCE uses a registered redirect URI. Do not change authorization state without an authorization task or expose tokens.

Select `--site retail|classic|fresh` before the subcommand. Report codes belong to their site. Start with fights and select an explicit fight ID, even when a URL already encodes one. A Raider.IO run ID is not a WCL report code.

```text
warcraftlogs report-fights <report>
warcraftlogs report-master-data <report>
warcraftlogs report-player-details <report> --fight-id <id>
warcraftlogs report-events <report> --fight-id <id>
warcraftlogs report-table <report> --data-type damage-done --fight-id <id>
warcraftlogs report-encounter-damage-target-summary <report> --fight-id <id>
warcraftlogs report-encounter-casts <report> --fight-id <id> --hostility-type enemies
warcraftlogs report-encounter-aura-summary <report> --fight-id <id> --ability-id <spell-id>
```

## Completeness and clocks

`report-events` returns one page. A non-null `data.next_page_timestamp` requires another request with the same filters and `--start-time` set to that cursor. Preserve the intended end boundary and fetch to completion. Null events, warnings or interrupted pagination leave completeness unknown. Stop and record an error if the cursor does not advance. Distinct events can share a timestamp; do not deduplicate on time alone.

Event/table/graph start/end options use milliseconds from report start. Encounter `--window-start-ms/--window-end-ms` are fight-relative offsets. Preserve transformations to wall-clock or key-relative time. Listing/sampled queries may instead use epoch milliseconds or ISO dates. Use effective clamped window duration for uptime normalization.

Casts summaries can be truncated even when aggregate rows exist. Completed cast counts do not count all begin/empower events and do not equal proc executions or damage impacts. Check query, truncation and warnings before concluding an event was absent.

For uncovered fields use scoped `warcraftlogs graphql --query @query.graphql` only after inspecting schema/help. Preserve partial GraphQL warnings. Do not publish an untested GraphQL query as working.

## Target timeline

Save key bounds, site, zone, difficulty, key level, roster and master data. Fight lists do not guarantee individual trash-pull boundaries. Fetch complete relevant event slices and inspect NPC identity/instance fields. WCL actor IDs are report-local identities; if a spawn GUID is unavailable, preserve the WCL identity separately and mark the mapping unknown. Do not fabricate a GUID.

Damage summaries, casts and aura bands help find intervals for inspection but do not prove spawn/death. Use event evidence for chain pulls, spawned adds, phases, player access and Bloodlust. Raid-specific analytics are not a universal Mythic+ parser.

Aura holder and applied-by identities differ. In the audited interface, `--view-by source` groups by holder and `--view-by target` by caster; inspect `row_actor` and query. Bloodlust needs actual events/bands and recipients, not just total uptime. Keep WCL and Blizzard class numbering separate.

## Talents and comparisons

`warcraftlogs report-player-talents <report> --fight-id <id> --actor-id <id> --out <packet.json>` exports a scoped raw tree. `raw_only` is not a validated SimC build; use [talent transport](warcraft-simulation.md).

Cross-report commands such as boss-kills, spec-kill-samples and ability-usage-summary are samples. Preserve selection, sample size, truncation, duplicate policy, difficulty/key-level mix and freshness. Fastest kills are not a random or complete population.

Lorrgs supplies raid top-parse context: `lorrgs specs`, `lorrgs bosses`, `lorrgs spec-ranking <spec-slug> <boss-slug>`, `lorrgs report-overview <report>`. `warcraft cooldown-packet <report-url> --actor-id <id> --phase <n>` joins that context to WCL casts. Check completeness, phase identity/source, partial errors and usable samples. Received external buffs are not the player's own casts. If reports/phases are unavailable, do not fabricate comparisons. Another raid parse's timing does not establish an optimal Mythic+ cooldown plan.
