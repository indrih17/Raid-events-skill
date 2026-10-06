# Provenance and source preservation

## Original methodology

Repository: indrih17/Raid-events-skill. Original main was read on 2026-10-06 at commit `e453c502fa3287296e73e898bd9c706fce614d2c`. Original README Git blob: `248e16dfa99740f6ac6a25f2a3f11491cf553df1`. Its full Russian text is preserved byte-for-byte in [original-methodology.md](original-methodology.md). [Original version](https://github.com/indrih17/Raid-events-skill/blob/e453c502fa3287296e73e898bd9c706fce614d2c/README.md).

The accessible chat “Скиллы и агенты Codex”, conversation ID `6ac46703-e464-83ed-8cf1-e4969a8d3aef`, discussed packaging and migration, not full raw experiment reports. No unavailable research history, player profiles, binaries, seeds or reports was reconstructed by assumption. A linked Gist was not counted as independent evidence for the same README.

The original 17 sections informed the reusable chapters: reconstruction, event modeling, model limitations, APL/reporting, source research and validation. Some original examples are historical and do not define the current skill's scope. The original archive remains Russian by preservation requirement; current user-facing documentation is English.

## Source and tool checks

The dated SimC source audit uses SHA `cafc27227ec08760cb391d6a798e104435c29a87`. It records source facts, not a matching historical binary or game-behavior validation. Generated inputs are teaching overlays; Python checks are not SimulationCraft runs.

Duration_stddev=1 remains the approximate route default; exact diagnostics use fixed bounds. The original cooldown=5160 convention is not universal, so the generator uses finite timestamp starts and a route-length-aware cooldown. Counter semantics require owner/result/aggregation checks.

## Warcraft CLI adaptation

On 2026-10-06 the owner requested useful workflows from aurokin/warcraft_cli. Audited SHA: `dd77084311d169b812c5a3884c8441e595306aae`, package 0.6.0. The content, logs and simulation references adapt its interfaces with SHA links. Upstream source/skill was not republished wholesale. No license file was found in the reviewed upstream tree; external installation does not relicense it.

Pinned CLI dependencies are recorded in the skill's assets. The ignored local environment was installed separately. Wrapper/provider interface checks and live Wowhead spell 10060 and Wiki COMBAT_LOG_EVENT_UNFILTERED reads succeeded after adding tzdata 2026.5 and enabling Python UTF-8 on Windows. WCL credentials and configured SimC engine were absent; report extraction and simulations were not validated. The adaptation was published in commit `4bb65ace0219137c0766499b151d77852bfd1dc3`.

Source text, guides and comments remain distinct from code/runtime evidence. Static APL analysis is not a simulation; WCL summaries do not prove lifetimes and pagination must be checked.

## English scope revision and rename

Later on 2026-10-06 the owner requested an English public skill with WoW in its name, removing Guillotine, invulnerable and haste/RPPM investigations because they were exploratory personal questions. The active skill is now `wow-raid-events`; README, references, templates, generated comments and paths were updated.

Dedicated investigation chapters, case study, historical numeric fixture and focused reproduction overlays were removed from the distributed skill. Their prior contents remain in Git history, including commit `4bb65ace0219137c0766499b151d77852bfd1dc3`; removal is a scope decision, not a claim that the observations were disproved. Generic comparison/extraction tests now use clearly synthetic fictional actions and values, without altering historical results. General route infrastructure remains in the generator because removing it would change the encounter model; it is not presented as a separate mechanism investigation.

The original archive is unchanged. Reusable evidence, target-selection, model and validation guidance remains. Repository publication permission stays scoped to the owner's base rather than becoming permission for users who copy the skill.
