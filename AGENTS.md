# Working on WoW Raid Events

This repository contains an English methodology and Codex skill for World of Warcraft encounter modeling with SimulationCraft. Its focus is observed Mythic+ target timelines and conclusions supported by data, code and reproducible controls.

- Preserve source/original-methodology.md byte-for-byte. Put corrections in references and explain changes in source/provenance.md.
- The main skill is .agents/skills/wow-raid-events/SKILL.md. Keep detail in references, examples in assets and deterministic tools in scripts.
- Keep active documentation, templates and generated comments in English. Respond to users in their chosen language.
- Keep the default workflow reusable. Do not reintroduce removed one-off item/mechanic studies without a user request.
- Do not replace combat-log evidence with assumptions from MDT or DungeonRoute. Never invent GUIDs, lifetimes, HP, IDs, simulations or unavailable history.
- Separate observations, checked source facts, hypotheses and unknowns. Preserve SHA, binary build, game data, input, commands and sources.
- When investigating a triggered action, check callback, initial target, candidate list/cache, cap, impact and statistics. Player target need not equal action target.
- Execution and direct-result counters need owner, action, aggregation and result-type checks; they are not universal proc/hit counters.
- Label SimC artifacts as teaching overlays, parsing checked, simulated or historical observations. Do not publish unsupported syntax as working.
- For script changes run unittest and check_repository.py; check invalid input, arithmetic, schemas and ambiguity rejection.
- Check portable links and the complete skill package; avoid duplicating chapters in SKILL.md.
- Do not modify source logs or upstream SimC to force a result. Keep diagnostic patches separate from baseline.
- The owner authorized relevant verified maintenance commits and ordinary pushes to main of indrih17/Raid-events-skill without repeated approval. This is limited to that base; later restrictions take precedence and it does not transfer to another user's repository. Follow [maintenance rules](.agents/skills/wow-raid-events/references/knowledge-maintenance.md).
