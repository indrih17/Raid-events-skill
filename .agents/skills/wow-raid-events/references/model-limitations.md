# Model choice and limitations

| Property | Duration-based adds | Health-driven route |
|---|---|---|
| Observed absolute windows | Assigned directly | May change with kills |
| Damage causes death | Lifetime fixed by duration | Health is depleted by damage |
| Extra DPS advances next pull | Usually no | May do so |
| HP percentage | Can be synthesized from remaining lifetime | Depends on enemy implementation |
| Group contribution | Does not supply marginal feedback by itself | Requires a checked group-damage model |
| Absolute Bloodlust | Easy to hold fixed | May land in a different pull after acceleration |

For ordinary adds in the audited [add_t::health_percentage](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/class_modules/sc_enemy.cpp#L1070), HP percentage follows remaining lifetime divided by total duration. This is a source fact for that SHA, not a rule for every enemy class.

A linear synthetic HP curve changes time spent under execute thresholds. Real group burst, healing, phases and priority focus can produce different curves. Check whether an effect reads HP at snapshot or impact, uses live or stored state, and applies to child actions. Do not assign guessed HP merely because an option exists: verify which value the lifetime and HP expressions actually use.

A fixed-window model answers what damage the player deals under those windows, not how much faster the group kills the pack. A health-driven single-player simulation can overstate the real feedback if the player accounts for only a fraction of group damage. Document player share, party approximation and response model. Do not average the two models into a supposed truth without justification.

Spawn windows do not define range, geometry or line of sight. Add count does not define priority. Replacing a target can reset state and ramp. A continuous route retains resource/cooldown carryover, unlike isolated pack simulations. Keep uncertain windows as sensitivity variants; do not silently treat estimates as measured lifetimes.
