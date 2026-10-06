# Методология расследования

## Содержание
Вопрос → пакет данных → гипотезы → код → минимальный контроль → метрики → интерпретация → отчёт.

## 1. Сначала определить вопрос

Разные вопросы требуют разных моделей:
- «Как предмет работает на том же наблюдаемом маршруте?» — фиксированный target timeline.
- «Насколько предмет ускоряет ключ?» — модель group TTK с допущениями о вкладе группы; duration adds для этого недостаточны.
- «Почему у proc меньше hits?» — action-level counters и per-target trace.
- «Скалируется ли RPPM с haste?» — конфигурация RPPM плюс эксперимент с контролем eligible attempts.
- «Почему APL держит CD?» — значения выражений events и выбранная target state.
- «Работает ли это в игре?» — игровые наблюдения; SimC показывает реализацию модели.

Переформулируй расплывчатое «теряет половину урона» в проверяемые варианты: меньше executions, меньше результатов на execution, меньше damage/result, другая длительность или потеря тиков.

## 2. Пакет входных данных

Зафиксируй: вопрос, source SHA/build, дата и game build, live/PTR, player/spec, gear/item levels/bonus IDs/set bonus, talents, APL, encounter options, targets, debug/distance settings, seed, threads, iterations, длительность, raw reports. Неизвестное явно оставь неизвестным.

Профиль должен быть полным expanded input, а не только ссылкой на меняющийся импорт. Сохрани фактическую команду, stdout/stderr и hash executable, если доступен. Если binary SHA нельзя связать с source SHA, сообщи это.

## 3. Гипотезы и различающие проверки

| Симптом | Возможная причина | Контроль |
|---|---|---|
| Меньше executions | eligibility, RPPM, ICD, downtime | attempts и successful callback |
| Столько же executions, меньше results | target list, cap, early return, report scope | candidates → selected → impacts |
| Столько же results, меньше damage | HP multiplier, role, crit, mitigation | per-result amount и HP |
| Другой DPS при том же damage | denominator / active time | elapsed vs active duration |
| Только short windows теряют hits | delay/travel/despawn | ordered event trace |
| Только set bonus меняет outcome | дочерняя action / другой spell | set on/off с контролем gear |
| Разница только в агрегате | child merging / pets / priority report | raw action owner rows |

Один и тот же симптом может иметь несколько причин одновременно. Выбери эксперимент, где гипотезы предсказывают разные наблюдения, а не просто ещё один полный gear sim.

## 4. Код и эксперимент — два независимых слоя

Найди entry registration по ID, затем создание effect/action, callback flags и overrides. Проследи путь до result accounting. Точное имя функции без вызовов не доказывает, что исследуемый профиль её использовал.

Эксперимент требует одинаковых исходных параметров и одной осознанной разницы. Выполни сначала parsing/smoke run, затем короткий one-iteration debug, затем series без debug. Одного seed достаточно для trace; для вывода о частоте нужны серии и uncertainty.

Если различие исчезло при сокращении профиля, возвращай факторы постепенно: второй target, dummy, talent, set bonus, расстояние, HP regime, fight style, retarget.

## 5. Итог

Отчёт отвечает:
1. Что наблюдали и в каких условиях.
2. Какая величина изменилась.
3. Какие участки кода реально прочитаны.
4. Что это доказывает в данном scope.
5. Какие альтернативы ещё не исключены.
6. Как повторить и что измерять дальше.

Не заканчивай расследование словами «похоже, баг» без scope и границ. Если данных достаточно только для симптома, именно симптом является завершённым проверенным результатом.
