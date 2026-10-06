# Reconstructing a Mythic+ target timeline

## Time and roster

Find key start/end markers if the format includes them. If not, state the alternative boundary and its uncertainty. Identify the five players separately from pets, guardians and summons. Preserve original timestamps, timezone, precision and offsets; normalize to one declared t0. Do not merge exports before checking their clocks. State whether `max_time` covers the whole key, a combat segment or an overlay.

## Spawn ledger

Use the full GUID of each observed spawn, not the NPC ID or display name. Store NPC identity and its source, initial/spawned classification, earliest interaction/damage/spawn evidence, last damage/death/despawn evidence, pull membership, player access, appearance/disappearance bounds and confidence. GUID formats vary by game/log version; do not apply one extraction pattern universally.

The first hit is not necessarily spawn and the last hit is not necessarily death. Keep existence, attackable, observed-damage and priority windows distinct. Explicit death evidence is stronger than last-hit inference, subject to log completeness. For uncertain bounds, retain intervals and declared sensitivity variants. Splitting one target into separate actors can lose dots and other persistent state.

## Pulls and phases

Group pulls by spawn identities and engagement evidence. A surviving target can overlap a later pull; represent its GUID once. Check late joins, patrols, pre-pull damage, resets, carried survivors and duplicated exports. MDT helps identify planned initial mobs but does not establish simultaneous engagement. Spawned targets can be absent from MDT: include them only when supported by observation and relevant player access.

Keep boss lifetime separate from phase and add windows. A phase triggered by HP in game can still be represented by its observed time in a fixed timeline. Do not infer the start of one phase from the death of an unrelated add.

## Bloodlust and downtime

Record the player's actual buff gains, refreshes, source and duration. A cast does not prove the player received the buff. Classify downtime from evidence: no attackable enemies, movement, range, player death, control effects, mechanic assignment or voluntary idle. An absence of damage alone does not identify the cause.

## Table before generation

| Pull | Start | End | Duration | Initial targets | Spawned targets | Boss/trash | Phase/priority | Bloodlust | Uncertainty |
|---|---:|---:|---:|---|---|---|---|---|---|
| P01 | observed | observed | end-start | GUID set | GUID set | evidence | explicit windows | t from t0 | bounds/source |

Also retain a machine-readable ledger: a pull-level table cannot express different deaths within the same pack. See [event modeling](event-modeling.md) and [WCL access](warcraft-logs.md).
