# Source audit: 2026-10-06

Repository: simulationcraft/simc. Source SHA: `cafc27227ec08760cb391d6a798e104435c29a87`. This records a source-reading pass, not a matching binary run or game-behavior validation.

| Checked behavior | Source | Limit |
|---|---|---|
| Primary and remaining target candidates | [action.cpp:1738](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1738) | Caller, predicates and overrides still matter |
| Cached list and distance filtering | [action.cpp:1766](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1766) | Check invalidation and runtime list |
| Callback initial target and scheduling | [dbc_proc_callback.cpp:363](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/dbc_proc_callback.cpp#L363) | Custom callbacks may differ |
| Add HP from remaining duration | [sc_enemy.cpp:1070](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/class_modules/sc_enemy.cpp#L1070) | Not all enemy classes |
| Direct result category aggregation | [stats.cpp:231](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/stats.cpp#L231) | Not automatically damaging hits |
| Timestamp parsing and scheduling conversion | [raid_event.cpp:2822](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2822) | Input uses absolute starts |
| Timestamps incompatible with first/last options | [raid_event.cpp:2786](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2786) | Do not combine them |
| Duration bounds options | [raid_event.cpp:2366](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2366) | Source read; parsing not run |
| Overlap restriction within an adds event | [raid_event.cpp:118](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L118) | Separate events are a different case |

Use the [source workflow](sources-and-code.md) for new claims. This registry intentionally contains reusable encounter/action facts rather than individual item experiments.
