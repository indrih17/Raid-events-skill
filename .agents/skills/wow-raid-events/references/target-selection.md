# Tracing target selection

Player target, action target, callback target, state target, cached candidates and child-action targets can differ. APL retargeting does not establish a triggered action's selection. Check custom callbacks and overrides.

| Stage | Record |
|---|---|
| Trigger | Time, owner, action, state and target |
| Callback | Eligibility, activation, success and custom path |
| Initial target | Identity and origin |
| Candidates | Full ordered list, actor states and cache validity |
| Filtering | Before/after predicates and geometry |
| Selection | Cap, split/chain behavior and selected indices |
| Scheduling | Target, execution and impact times |
| Impact | Target state, result and amount |
| Stats | Owner, action, result categories and child aggregation |

In the audited [available_targets](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1738), primary-target handling precedes collecting remaining candidates. Read the predicates and the caller's actual path before inferring any specific effect's result. [target_list](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1766) involves caching and optional distance filtering; check invalidation on relevant state transitions and iteration resets.

Determine cap from action code, spell data, chain/reduced-AoE settings or a custom loop. Test filtering order versus cap application. Candidate count and `active_enemies` need not be the same quantity. Change ordering, count or geometry separately, preserving the rest of the setup.

Join the trace with a unique execution identity or an unambiguous time/owner/action/state tuple. Locate the transition that explains an absent result: filtering, selection, disappearance before impact, or reporting scope. Instrument without changing selection or random decisions; save the patch and verify baseline behavior. Without the trace, report observed counts and the unresolved alternatives.
