# Evidence and metric interpretation

| Level | Basis | Allowed claim |
|---|---|---|
| E0 | Idea, tooltip or unsupported account | Hypothesis requiring verification |
| E1 | Supplied observations with incomplete provenance | In the supplied data... |
| E2 | Preserved runnable input and repeatable control | Reproduces in this build/profile... |
| E3 | Complete code chain plus matching event/target trace | Cause established for these conditions... |
| E4 | Regression controls across stated cases/builds | Generalization checked for the listed cases... |

This is a local convention, not an official standard. Attach a level to each claim. A checked source fact can be recorded by SHA without giving a causal explanation E3. E4 does not establish every future build or behavior in WoW itself.

## Metrics

`num_executes` counts the executions associated with a stats action; it is not a universal successful-proc counter. `num_direct_results` aggregates registered result categories, not necessarily successful damaging hits. Ticks, buff applications and callback successes have their own semantics. Identify owner, action, result types and child aggregation before comparing.

Specify whether damage is actual or compound, includes children/ticks, and is total damage or DPS. The ratio of mean results to mean executions is not the mean of per-proc ratios and does not reveal the outcome of every proc. A zero denominator is undefined.

With aligned direct-only scopes, damage can be decomposed as executions times results/execution times damage/result. With periodic or child damage, misses, absorbs or different owners, separate those components first. A change in damage alone does not locate a lost result or establish a cause.

## Uncertainty

Preserve iterations, seeds, means and error estimates when available. DPS target error does not guarantee precision for a rare effect. Similar means do not prove equivalence; different means under unmatched inputs do not establish causality. Use real iteration or replicate observations for intervals, not fractional aggregate counts. Do not assume identical seeds preserve matched RNG streams after changing an event graph. A single debug iteration establishes an observed event order, not typical frequency. Declare any conditional sample or exclusion of zero-execution runs.
