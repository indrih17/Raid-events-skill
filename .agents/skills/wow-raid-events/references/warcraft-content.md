# Wowhead, Warcraft Wiki and guides

Use the [CLI setup and provenance rules](warcraft-cli.md). Interfaces are adapted from the pinned [Wowhead reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/wowhead.md) and [Wiki reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/warcraft-wiki.md). They describe tools, not verified gameplay mechanics.

## Wowhead

```text
wowhead search "<name and type>"
wowhead resolve "<query>"
wowhead entity spell <id>
wowhead entity item <id>
wowhead entity npc <id>
wowhead entity --url <entity-url>
wowhead entity-page --url <entity-url>
wowhead comments --help
wowhead guide <guide-id-or-url>
wowhead guide-full --help
wowhead guide-export --help
wowhead news --help
wowhead blue-tracker --help
wowhead news-post <news-url>
wowhead talent-calc --help
```

Verify entity ID, expansion and locale before interpreting the page. `entity-page` provides fuller relations; drop/vendor listviews may include sample counts, cost or stock. A sampled drop rate is not a universal probability. Missing quick-facts fields remain unknown.

For an effect investigation, record item, driver, buff and damage IDs separately. Identical names can identify different spells. Tooltips and comments guide discovery; code, logs and controls establish implementation. Preserve player comments as dated/versioned accounts rather than proven mechanics.

For hotfix research record both publication and change dates, patch and source. Historical date filters require enough pages: inspect scan stop reason, unparsed timestamps and truncation. One page without a result does not establish absence. Guide categories and individual guides use different commands.

Talent calculators, profiler and dressing-room surfaces inspect tool state rather than promising full decoding. Validate retail exports through SimC; Classic calculators are not interchangeable with retail SimC.

## Warcraft Wiki

```text
warcraft-wiki search "<query>"
warcraft-wiki resolve "<query>"
warcraft-wiki api CombatLogGetCurrentEventInfo
warcraft-wiki event COMBAT_LOG_EVENT_UNFILTERED
warcraft-wiki event ENCOUNTER_START
warcraft-wiki article "<exact title>"
```

Use `api` for functions, enums, CVars and programming/framework documentation; `event` for event payloads and handlers; `article` for broader reference. Read signature, arguments, full text, limitations and page freshness. If programming classification rejects a page, try its exact article title.

Before changing a raw-log parser, compare common fields and event-specific suffixes against the game's version and a real source row. Lua API payloads, text WoWCombatLog and WCL normalized JSON use different schemas. A documented field is not proof that the supplied artifact contains it. Do not substitute a WCL actor ID for a spawn GUID.

## Guide comparison

Use `method search`/`method guide` or `icy-veins search`/`icy-veins guide`, checking source syntax in help. `warcraft guide-compare-query "<class spec guide>"` orchestrates sources; `warcraft guide-compare <bundle-a> <bundle-b>` compares exported bundles. `guide-builds-simc` hands explicit published builds to SimC.

Preserve raw sections, citations, freshness, redirects and failed pages. Extracted `analysis_surfaces` supplement the source text. Compare matching patch, class/spec, hero tree, target context and content type. Guide disagreement is a testable question, not a simulation result. Do not invent a missing import string from prose. Calculator conversions may omit PvP talents; retain the original URL. See [simulation](warcraft-simulation.md).
