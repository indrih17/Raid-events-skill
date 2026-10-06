# Проверка target selection

## Почему player target недостаточно

У SimC одновременно могут существовать player->target, action->target, state->target, callback target, cached target list и target конкретной дочерней action. Они могут различаться. Retarget APL не доказывает корректность AoE proc; proc callback может использовать target triggering state.

В прочитанном [dbc_proc_callback_t::execute/get_target](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/dbc_proc_callback.cpp#L363) outgoing callback возвращает переданную цель и затем сохраняет proc state для schedule_execute. Для входящих callbacks логика другая. Проверь overrides/custom execute functions исследуемого эффекта.

## Цепочка проверки

| Этап | Что записать | Что может сломать интерпретацию |
|---|---|---|
| Trigger | triggering action/state/target/time | indirect proc, suppression, owner |
| Callback | flags, success, ICD, custom fn | callback вовсе не вызван |
| Initial target | actor ID и происхождение | stale state, current player target |
| Candidate list | каждый actor, порядок, состояния | cache, sleeping, invulnerable |
| Filtering | до/после predicate и geometry | разные filter paths |
| AoE selection | cap, split/chain, индексы | invalid actor занимает slot |
| Scheduling | target и execute/impact times | travel delay, despawn |
| Impact | target alive/state, result, amount | early return, mitigation |
| Stats | owner/action/results/children | aggregation/нулевые damage results |

## Available targets и cache

В проверенном [action_t::available_targets](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1738) action primary target сначала добавляется при проверке sleeping/enemy/callback, затем берутся остальные targets из target_non_sleeping_list. Локальная функция сама не содержит универсальной отдельной invulnerable проверки primary target.

Это не доказывает, что invulnerable действительно попал в Guillotine list: нужно подтвердить initial target, фильтры и реальный execution path. Возможная ошибка вывода — увидеть этот фрагмент и объявить причину без tracing callback.

target_list использует target_cache; distance filtering вызывается при distance_targeting_enabled. Проверь overrides и invalidation при summon/dismiss/invulnerable, set_target/acquire_target и iteration reset. В debug есть output regeneration; cache valid может означать, что нового output нет, а не что кандидатов нет.

## Cap и ordering

Выясни источник cap: C++ aoe, spell data, chain targets, custom num_targets, reduced_aoe_targets или отдельный loop. Не считай число targets в tooltip доказательством фактического cap.

Проверь, что происходит раньше: исключение invalid targets или ограничение list size. Отдельно меняй ordering/names/spawn order при неизменном составе; изменение результата тогда помогает искать dependence on list index, но само не доказывает баг.

«Две атакуемые цели + один invulnerable actor» и «два actor всего, один invulnerable» — разные controls. Общее active_enemies тоже может отличаться от списка кандидатов action.

## Минимальная матрица

A: две vulnerable цели, без invulnerable.
B: те же две vulnerable цели и invulnerable actor.
C: тот же состав B, ignore_invulnerable_targets toggle.
D: тот же состав B, проверенный retarget вариант.
E: две vulnerable цели, dummy существует, но состояние доступности варьируется отдельно.
F: одна vulnerable цель как expected one-result control.
G: 3+ vulnerable targets для определения cap/ordering.
H: та же геометрия с distance filtering on/off.
I: delayed despawn или immunity after trigger для различения schedule/impact.

Не меняй одновременно active_enemies, adds count, HP, set bonus и APL. Если без dummy нельзя создать эквивалентную инфраструктуру, явно укажи difference и сделай controls, позволяющие её отделить.

## Trace, который устанавливает причину

Записывай один proc ID или однозначную связку time + owner + action + state:
trigger state → callback success → initial target → full ordered candidates → selected targets → каждого scheduled state → каждого impact → stats.
Отсутствие result объясняется конкретным переходом, например candidate был отфильтрован, cap его не выбрал, target успел исчезнуть или result не учитывается в выбранном report scope.

Если нужна instrumentation, добавь минимальный диагностический output без изменения selection/roll. Сохрани patch отдельно; сравни контрольный output до/после. Не исправляй selection одновременно с tracing.

## Что написать в выводе

Укажи какие этапы подтверждены, точный source SHA, profile/build, target identity и где result потерялся. Если trace не получен, ограничь вывод observed counts и перечисли оставшиеся механизмы.
