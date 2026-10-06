# Minimal reproductions

An encounter overlay without the relevant player/profile data is only part of a reproduction. Do not recreate unavailable inputs from aggregate observations.

Preserve expanded player and encounter inputs, command, source SHA, binary hash/build, game data, gear/talent/ID identity, seed, threads, iterations, duration/RNG settings, JSON/HTML reports and stdout/stderr. If needed, keep a one-iteration trace and diagnostic patch separately from baseline.

Use three distinct modes: a small parsing/smoke run, a trace run for event order and target identity, and a statistical series for the chosen metric. Parsing success does not establish mechanics; one trace does not establish frequency. Choose iterations based on precision needs rather than a fixed round number.

Remove unrelated factors one at a time, retaining the triggers and initialization that produce the symptom. Shorten duration only while the symptom remains reproducible. If it disappears, restore the last removed factor as a control.

Use matched target count, actor type, geometry and HP where relevant. Test ordering, delayed despawn, state transitions, children or pets only when they distinguish a plausible mechanism. Keep the smallest useful input and complete provenance for a bug report. The [investigation template](../assets/investigation-template.md) records the result.
