# Проверка кода SimC от 2026-10-06

Repository: simulationcraft/simc. Branch при чтении: midnight.
Полный SHA: cafc27227ec08760cb391d6a798e104435c29a87.
Это проверка исходников, не запуск binary и не provenance исторического Guillotine experiment.

## Проверенные места

| Факт по этому SHA | Код | Граница вывода |
|---|---|---|
| Guillotine registration/implementation, driver 1291728 | [unique_gear_midnight.cpp:6313](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6313) | Не устанавливает весь inherited AoE path |
| Damage spell 1306604, Perfected 1306624 и set branch | [6352](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6352) | Не доказывает historical gear/set |
| Missing-HP multiplier | [6342](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6342) | Coefficient data нужно читать отдельно |
| Impact child Venomfang при set bonus | [6328](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6328) | Compound/direct scope требует report |
| Invulnerable start вызывает clear_debuffs, halt, optional retarget | [raid_event.cpp:1472](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L1472) | Не универсальная характеристика всех immunity mechanics |
| Ignore option меняет target_non_sleeping_list и active_enemies | [player.cpp:505](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/player.cpp#L505) | Actor references могут оставаться |
| Invulnerable mitigation обнуляет amount | [player.cpp:8429](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/player.cpp#L8429) | Не устанавливает наличие/отсутствие stats result |
| Primary target precedes remaining targets в available_targets | [action.cpp:1738](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1738) | Реальный initial target/filter/override неизвестен без trace |
| Cached list и optional distance filter | [action.cpp:1766](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1766) | Нужно проверить invalidation |
| Callback initial target и snapshot schedule | [dbc_proc_callback.cpp:363](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/dbc_proc_callback.cpp#L363) | Custom callbacks могут менять путь |
| Add HP% по remaining duration | [sc_enemy.cpp:1070](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/class_modules/sc_enemy.cpp#L1070) | Не все enemy classes |
| Direct result count суммирует categories | [stats.cpp:231](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/stats.cpp#L231) | Не автоматически damaging hits |
| RPPM mask/coefficients/BLP | [proc_rng.cpp:48](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/proc_rng.cpp#L48) | Не установлена effective Guillotine mask |
| Same-timestamp rejection | [proc_rng.cpp:100](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/proc_rng.cpp#L100) | Applies только к этому RNG path |
| max_interval 3.5s, max BLP 1000s | [proc_rng.hpp:88](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/proc_rng.hpp#L88) | Version-specific constants |
| timestamps separator ':' и relative scheduling conversion | [raid_event.cpp:2822](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2822) | Input absolute; внутренние интервалы преобразуются parser |
| timestamps запрещены с first/last/% options | [raid_event.cpp:2786](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2786) | Не смешивать параметры |
| duration_min/max options | [raid_event.cpp:2366](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L2366) | Syntax чтён; binary parsing не запускался |
| Adds запрещает overlap своего spawning | [raid_event.cpp:118](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L118) | Отдельные events — отдельный сценарий |

## Что осталось открытым

- Effective AoE cap, spell coefficients и RPPM mask Perfected Guillotine для historical experiment.
- Initial target каждого historical proc и полные ordered candidate lists.
- Место потери каждого historical direct result.
- Scope урона 10.534M/5.200M: direct/compound/children.
- Причинность конкретного C++ участка без matching runtime trace.
- Поведение в игре и builds, отличающихся от данного SHA.

Первичный [SimC repository](https://github.com/simulationcraft/simc/tree/cafc27227ec08760cb391d6a798e104435c29a87) и [RaidEvents wiki](https://github.com/simulationcraft/simc/wiki/RaidEvents). Wiki здесь использована для навигации, а versions-specific claims опираются на прочитанный source.
