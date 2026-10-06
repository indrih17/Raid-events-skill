# Proc debugging: от ID до статистики

## Entry points

Начни с идентичности: item ID, driver spell ID, damage spell ID, buff spell ID, set bonus и названия report actions могут не совпадать. Из tooltip/имени нельзя выводить C++ ID без проверки registration.

В локальном SimC:
~~~text
rg -n -i "guillotine|1291728|1306604|1306624" engine
rg -n "register_special_effect|execute_action|dbc_proc_callback_t" engine/player
rg -n "available_targets|target_list|schedule_execute|impact" engine/action
~~~
Поиск — навигация, не доказательство. Читай окружающие constructor/init и overrides.

## Слои

1. Registration связывает driver с implementation.
2. special_effect получает spell data, ppm/rppm flags, item scaling и custom fields.
3. Action constructor задаёт base amount, role, school, AoE, children.
4. Callback init выбирает eligible flags и RNG.
5. trigger проверяет eligibility/ICD/suppression.
6. roll определяет success.
7. execute выбирает target и schedules state.
8. action execute/impact создаёт results.
9. stats aggregate формирует report.

Если callback существует, но не registered/active для профиля, чтение его кода не объясняет output.

## Guillotine в текущем коде

[zuljins_guillotine_technique](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6313):
- driver 1291728;
- обычный damage spell 1306604;
- Perfected Guillotine spell 1306624 при MID_BOZ B2;
- action называется guillotine или perfected_guillotine;
- base damage берётся из driver effect 1;
- multiplier растёт с missing HP через driver effect 2;
- Perfected branch включает set bonus scaling и impact_action Venomfang;
- effect.execute_action создаётся и подключается dbc_proc_callback_t.

Эта карта проверена в текущем SHA. Она не устанавливает cap из spell data, не доказывает haste scaling и не показывает historical profile. Проверяй DBC/overrides и inherited generic_proc_t в соответствующем build.

## Eligibility и частота

Зафиксируй:
- outgoing/incoming event;
- attack/spell/direct/tick/crit requirements;
- can_proc_from_procs и suppression;
- ICD/cooldown/shared cooldown;
- buff gating/stack/max stack;
- set bonus and role;
- child callbacks;
- RNG model: fixed chance, PPM, RPPM, custom.

Увеличение hits AoE не обязательно даёт столько же независимых RPPM attempts. В текущем real_ppm_t same timestamp может подавлять повторную попытку. См. rppm-haste.md.

## Owner и children

Проверь parent/child stats merging, pet ownership, duplicate action rows, priority grouping. Venomfang как дочерний impact не обязан иметь те же executions/results, что родитель. Report compound damage может включать его, direct counter родителя — нет.

Не суммируй parent compound и child damage повторно. Для trace сохраняй raw owner/action identity. Для ratio D/R используй совместимые direct damage и direct result scopes.

## Минимальная диагностика

Сначала полностью включи требуемый item/set в реальном profile и убедись, что action появилась. Затем убери лишние effects по одному. Если proc исчез, это не «zero rate»: возможно выключена registration branch или отсутствует eligible trigger.

Сохрани first trigger, first success, counts по каждому этапу и отказы. Delay/travel может отправить результат на уже sleeping target. Разница num_executes и num_direct_results может быть scheduling или stats, а не только target cap.

Диагностическая instrumentation не должна менять RNG или target graph. Не вызывай дополнительный roll для «посмотреть вероятность»: логируй уже вычисленное значение.
