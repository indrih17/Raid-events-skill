# Validation record: 2026-10-06

## Initial checks

The original preparation passed 24 unittest cases and the repository check. The archived README matched Git blob `248e16dfa99740f6ac6a25f2a3f11491cf553df1`. Route generation and extraction were checked with synthetic fixtures. A dated source audit was recorded at SimC SHA `cafc27227ec08760cb391d6a798e104435c29a87`.

The engine was not supplied or run; generated overlays were not runtime-validated. The standard skill validator initially lacked PyYAML, so a dependency-free validator checked the actual simple frontmatter. No Python check proves game mechanics.

## Warcraft CLI integration

Pinned Warcraft CLI installation, provider interfaces, live Wowhead spell 10060 and Wiki COMBAT_LOG_EVENT_UNFILTERED reads passed. Windows needed tzdata 2026.5 and PYTHONUTF8=1. WCL report reads were not validated without credentials; engine simulations and talent round-trip were not validated without a configured SimC binary.

## English scope revision

The active package was renamed to wow-raid-events, converted to English, and detached from the removed exploratory investigations. All 26 unittest cases passed, including standalone skill-copy validation, broken-link rejection and refusal to omit the repository archive. Repository checks passed with the original Git blob unchanged. Synthetic metric comparison, exact route generation, pip dependency checks and the relocated Warcraft CLI doctor passed. The active documentation scan found no Cyrillic text or removed investigation topics; only the generator retains its required infrastructure options. Validation applies to tooling and package structure, not a real encounter replay.
