# Происхождение и сохранение материалов

## Исходный README

- Repository: indrih17/Raid-events-skill.
- Прочитан из main 2026-10-06.
- Исходный commit: e453c502fa3287296e73e898bd9c706fce614d2c.
- Git blob SHA README: 248e16dfa99740f6ac6a25f2a3f11491cf553df1.
- [Исходная версия](https://github.com/indrih17/Raid-events-skill/blob/e453c502fa3287296e73e898bd9c706fce614d2c/README.md).
- Содержимое сохранено целиком в original-methodology.md; новая методичка не заменяет архив.

## Доступный контекст

Прочитан доступный чат «Скиллы и агенты Codex», conversation ID 6ac46703-e464-83ed-8cf1-e4969a8d3aef. Он содержит обсуждение структуры skill и переноса материала, но не сырые отчёты Guillotine. Числа эксперимента взяты из текущего прямого запроса пользователя и сохранены отдельно как historical observation.

Связанный Gist не использован как дополнительное независимое доказательство: текущий README уже предоставлен в репозитории как исходный материал. Недоступные исследования из других чатов, полные combat logs, исходный gear profile, бинарник SimC, seed, iteration count и JSON/HTML отчёты не предоставлены. Их параметры не восстановлены предположениями.

## Где сохранены все 17 исходных разделов

| № | Исходная тема | Новая глава в references |
|---|---|---|
| 1 | Реальный timeline / источники | combat-log-reconstruction, sources-and-code |
| 2 | Итоговый code block / Pull naming | event-modeling |
| 3 | Базовые настройки / dummy / 5160 | event-modeling, validation |
| 4 | Trash, add_boss, count | event-modeling |
| 5 | Spawned adds / роль игрока | combat-log-reconstruction |
| 6 | Boss phases | combat-log-reconstruction, event-modeling |
| 7 | Invulnerable / stun | invulnerable-actors |
| 8 | Bloodlust timestamps | event-modeling, rppm-haste |
| 9 | Chain pulls / GUID | combat-log-reconstruction |
| 10 | Synthetic HP / duration | model-limitations |
| 11 | DungeonRoute vs Raid Events | model-limitations |
| 12 | APL adds/pull expressions | apl-and-reporting |
| 13 | Retarget / priority reporting | target-selection, apl-and-reporting |
| 14 | Разбор combat log | combat-log-reconstruction |
| 15 | Таблица перед кодом | combat-log-reconstruction, validation |
| 16 | Проверка route | validation |
| 17 | Gear/talents/CD/distribution | methodology, model-limitations |

## Уточнения без переписывания истории

1. duration_stddev=1 сохраняется как авторский route default. Это jitter, поэтому «реальный timeline» означает приближение; строгий тест фиксирует duration_min/max.
2. cooldown=5160 сохраняется как исходная конвенция для маршрута короче выбранного интервала. Генератор использует конечный timestamps-список, чтобы одноразовость не зависела от длительности ключа.
3. Новая проверка кода подтверждает clear_debuffs и synthetic HP в конкретном SHA; это не доказательство версии исторического эксперимента.
4. Разница 43.662 → 43.719 невелика, но без dispersions нельзя доказать равенство proc rates статистически.
5. Direct results в агрегате требуют проверки result categories; слово «попадания» в historical case не превращает любую direct-results строку в successful damaging hits.
6. Текущая стандартная repo discovery папка — .agents/skills. Весь skill расположен там, без двух расходящихся копий.

## Новые материалы

Процедуры, контроли, шаблоны и scripts написаны для этого репозитория. Source audit основан на чтении первичного SimC C++ по SHA cafc27227ec08760cb391d6a798e104435c29a87. Все generated examples обозначены учебными. Запуски инструментов проверки не являются запуском SimulationCraft.
