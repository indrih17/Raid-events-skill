# APL and reporting

Route timing does not automatically create priority behavior. Specify which target should be primary, when that priority applies, and how the player's APL reaches it. Distinguish total damage from damage to the priority target.

Check the actual build's expressions and action-list support before using adds/pull gating. Read initialization, list dispatch and target-selection conditions. A static branch analysis can establish an unreachable branch only under its stated conditions; possible/unknown branches still depend on runtime state.

For comparisons, keep gear, talents, encounter, options and baseline constant while changing the intended APL factor. Verify the expanded inputs and warnings. Resource and cooldown carryover across a continuous route makes independently simulated packs a different model.

Report player and pet owners separately unless aggregation is deliberate. Preserve per-target damage, active/exposure time, deaths and priority windows. Total DPS can increase while priority damage falls. Do not infer a proc's target from the player's selected target. See [target selection](target-selection.md) and [SimC workflow](warcraft-simulation.md).
