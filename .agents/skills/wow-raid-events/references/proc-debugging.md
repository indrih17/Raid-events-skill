# Investigating a triggered action

Identify the item, driver, damage and buff IDs separately; report action names need not match those IDs. Start with source searches for the verified name/ID, then read registration, constructors, initialization, inherited behavior and overrides. A search hit is navigation, not evidence that the path was active.

Follow registration, effect data/scaling, action creation, callback activation, eligibility/suppression, success decision, scheduling, execution, impact and stats aggregation. Check profile conditions such as gear, set, spec and role. Keep data-driven coefficients and caps tied to the actual game data/build.

Separate trigger attempts, successful callbacks, action executions, direct/tick results and reported damage. A buff proc can have no damaging action; one callback can create several child actions. Missing damage can reflect target selection, scheduling, result type or report scope, so do not identify a cause from headline DPS.

Trace the requested mechanism using [target selection](target-selection.md), [evidence rules](evidence-rules.md) and [minimal reproductions](minimal-repros.md). Keep general procedures here; do not promote a one-off item investigation into the default skill workflow.
