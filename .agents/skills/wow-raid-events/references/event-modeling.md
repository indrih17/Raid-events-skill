# Modeling raid events

Set `fight_style` before custom events; it may initialize or clear them. `raid_events=` starts a list and `raid_events+=` appends. An accidental second assignment can erase earlier events. The [SimC RaidEvents wiki](https://github.com/simulationcraft/simc/wiki/RaidEvents) helps navigation; verify syntax against the source/build used.

## Fixed timeline

Use a fixed-time setup for a declared observed window, disable automatic Bloodlust when supplying observed timings, and verify the expanded configuration. This does not create an exact replay: RNG, APL behavior and encounter approximations still matter.

Represent trash with `/adds`; use `type=add_boss` only for an evidence-supported boss classification. Targets with different start/end times require separate events. `count=N` is appropriate only when their windows coincide; retain real GUID mapping outside the profile.

For fixed lifetimes use checked `duration_min=duration_max=duration` bounds. The generator's default `duration_stddev=1` is an approximation with jitter, not a timestamp-perfect mode.

## Scheduling

- `first` sets an initial occurrence; cooldown/period schedules later occurrences.
- `last` can restrict starts without truncating an already active event; inspect the scheduler.
- `timestamps` supplies a finite colon-separated list of absolute starts, for example `10:70:140`.
- In the audited SHA, timestamps cannot be combined with first/last or their percentage options.
- A single timestamp expresses one intended start; keep cooldown valid for sanity checks.
- Separate adds events can overlap. One adds event has its own overlapping-spawn restrictions.

The historical `cooldown=5160` convention is not a guarantee for an arbitrary route. The generator uses finite starts and a route-length-aware cooldown. Its baseline anchor is encounter infrastructure, not an observed mob; verify that it contributes no fictitious damage. Do not remove infrastructure options from a generated overlay without checking the resulting timeline.

## Bloodlust

Use actual player buff times. `override.bloodlust=0` disables automatic application; the generator supplies `/buff,buff_name=bloodlust` with explicit timestamps and 40-second fixed bounds. If the observed buff was shorter, verify how to represent it in the relevant build. Absolute timings in a fixed route and timings tied to health-driven pull progression answer different questions.

## Output and verification

Generate a teaching overlay from [example-timeline.json](../assets/example-timeline.json), then add a real player profile and validate in the intended SimC build. Keep PULL separators, unique names, evidence comments and uncertainty. State whether the result is a teaching overlay, parsing checked or simulated. Source inspection alone does not establish successful parsing. See [validation](validation.md).
