# Perfected Guillotine и invulnerable actor

## Вопрос

Почему в эксперименте с invulnerable actor у Perfected Guillotine стало примерно вдвое меньше зарегистрированных попаданий и среднего урона при близком среднем числе executions?

## Provenance и статус

Источник чисел — прямой запрос пользователя при продолжении чата «Скиллы и агенты Codex», 2026-10-06. Сохранены без изменения. Raw JSON/HTML, historical player profile, encounter input, SimC SHA/build, iterations, seeds, game build и полные per-target результаты не предоставлены.

Статус: **historical observation, E1**. Эксперимент не был повторно запущен в ходе подготовки этой методички. «Baseline 2-target» — предоставленное описание; точное устройство actor graph неизвестно. Не реконструируй его задним числом.

## Числа

| Метрика | Baseline 2-target | С invulnerable |
|---|---:|---:|
| num_executes | 43.662 | 43.719 |
| num_direct_results | 87.184 | 43.643 |
| Direct results / execution | 1.996793550 | 0.998261625 |
| Условное shorthand hits/proc | ≈1.997 | ≈0.998 |
| Средний урон | 10.534M | 5.200M |

Расчёты по средним:
- Executions: +0.057, приблизительно +0.1305%.
- Direct results: −43.541, приблизительно −49.9415%.
- Средний урон: −5.334M, приблизительно −50.6360%.
- 10.534M/87.184 ≈120824.922 и 5.200M/43.643 ≈119148.546 damage/result **только как арифметика**; physical interpretation требует совместимого scope damage и counters.

Нормализованные входы: [guillotine-observations.json](../../assets/guillotine-observations.json). Сравнение воспроизводится compare_results.py. В JSON damage_scope=unspecified: direct vs compound в историческом отчёте неизвестен.

## Доказано наблюдением

В предоставленном эксперименте изменилось число зарегистрированных попаданий (reported direct results): почти двукратное падение при близких средних executions. Аналогично почти вдвое упал средний reported damage.

Основной наблюдаемый эффект находится в results per execution, а не в сильном падении reported execution count. Это не утверждение о строгом статистическом равенстве rates: без uncertainty оно не доказано.

## Не доказано только этими числами

- Точная причина и место потери results.
- Что каждый proc потерял ровно один hit.
- Что именно invulnerable dummy занял AoE slot.
- Что cap равен 2 или изменился.
- Что proc target остался dummy.
- Что невидимые/нулевые results не попали в отчёт.
- Что underlying successful callback count равен num_executes.
- Что damage scope не включает Venomfang или другие children.
- Что toggle ignore_invulnerable_targets исправляет проблему.
- Что то же самое происходит в игре.
- Что current source соответствует historical binary.

## Проверенный текущий код

В SHA cafc27227ec08760cb391d6a798e104435c29a87 найдены:
- [Guillotine implementation](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/unique_gear_midnight.cpp#L6313), driver 1291728, normal damage 1306604, Perfected 1306624.
- Set branch MID_BOZ B2 переключает name/spell, использует set scaling и impact_action Venomfang.
- composite_target_multiplier зависит от missing HP.
- Подключается dbc_proc_callback_t.
- [Invulnerable event](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L1472) очищает debuffs, increments immunity, halt и optional retarget.
- [Ignore option](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/player.cpp#L505) меняет non-sleeping list.
- [Available targets](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/action.cpp#L1738) отдельно добавляет primary target перед остальными candidates.

Эти фрагменты мотивируют проверку target chain, но не завершают causal proof. Полная [карта кода](../source-audit-2026-10-06.md).

## Гипотезы и falsification

| Гипотеза | Предсказание | Проверка |
|---|---|---|
| Invalid candidate занимает cap slot | List содержит actor, cap выбирает его вместо vulnerable | Ordered candidates и selected states |
| Initial target proc неверный | Callback state/target отличаются от ожидаемого | Trigger → get_target → schedule state |
| Target исчезает до impact | Selected vulnerable есть, но impact after despawn | Event timestamps и sleeping check |
| Results фильтруются/агрегируются в report | Raw impacts присутствуют, row counts расходятся | Owner/action/raw categories |
| Меньше eligible triggers / rate | Callback successes заметно меньше | Attempts/roll/success counters |
| Другой HP multiplier | Results сопоставимы, amount/result зависит от HP | HP at multiplier evaluation |
| Incompatible encounter setup | Число vulnerable или actor types различается | Expanded targets и matched graph |

Несколько механизмов могут действовать одновременно.

## Следующий различающий эксперимент

1. Получить historical inputs/build/reports, если сохранились.
2. Зафиксировать два vulnerable targets с одинаковыми windows, HP regime и geometry.
3. Отдельно менять наличие/состояние invulnerable actor, ignore flag, retarget и ordering.
4. Проверить one target и 3+ target controls, set bonus on/off.
5. В одном trace записать proc trigger target, callback success, initial target, full candidate list, cap-selected targets, каждый impact и stats.
6. В series сравнить E, R, R/E, damage, damage scope, per-target distributions и uncertainty.
7. Сопоставить конкретный потерянный result с проверенной code chain.

Учебные [overlays](../../assets/repro/baseline-two-targets.simc) помогают начать диагностику; они не заменяют исторический repro и имеют различие base/add infrastructure, описанное в minimal-repros.md.

## Практический урок

Invulnerable base actor требует action-level контроля при построении route. Хорошая внешняя DPS-картина не подтверждает правильность target selection каждого proc. Правильный вывод этого case: изменение зарегистрированных попаданий установлено, точная причина остаётся открытой.
