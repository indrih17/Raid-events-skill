# Уровни доказательности и статистика

## Уровни

| Уровень | Основание | Допустимая формулировка |
|---|---|---|
| E0 | Идея / tooltip / пересказ без raw data | «Гипотеза, требует проверки» |
| E1 | Предоставленные численные наблюдения, неполный provenance | «В предоставленных данных…» |
| E2 | Сохранённый runnable input и повторяемый контроль | «В этой сборке и профиле воспроизводится…» |
| E3 | Полная связанная code chain и event/per-target trace | «Причина установлена для этих условий…» |
| E4 | Регрессионные controls, несколько условий/сборок; отдельно game evidence | «Обобщение проверено на перечисленных случаях…» |

Это локальная шкала методички, не официальный стандарт. Code reading само по себе можно фиксировать как code fact по SHA, не присваивая причинному утверждению E3. Уровень привязан к конкретному claim, а не целому документу. E4 не означает доказательство всех будущих builds или WoW behavior.

## Семантика метрик

- num_executes — усреднённое число executions соответствующей stats action; один proc может создавать несколько actions или вообще buff.
- num_direct_results — агрегат зарегистрированных direct result categories; это не автоматически только successful damage hits.
- num_tick_results — отдельный агрегат периодических результатов.
- Damage — уточни actual vs total, direct vs compound с children, средний total damage vs DPS и единицы.
- Proc count — если это отдельная строка callback/buff, не смешивай её с damage action executions.

Для определённой простейшей direct-damage action полезно R/E, где R — direct results, E — executes. Для Guillotine это исторически обозначено как hits/proc, но точное безопасное имя метрики — direct results per execution.

Отношение средних R̄/Ē не равно среднему отношений отдельных proc. Оно также не показывает распределение «у каждого proc был один hit». При E=0 отношение не определено; не записывай 0 и не дели молча.

## Декомпозиция урона

При согласованных scope и только direct damage:
D ≈ E × (R/E) × (D/R).
Если есть ticks, child actions, absorbs, misses, overkill или разные owners, такая формула требует отдельного разложения. Не дели compound damage, включающий Venomfang, на direct results родителя как будто это damage одного Guillotine hit.

Рост D может происходить без роста E из-за HP, crit, role multiplier, target cap или target mix. Падение D не устанавливает место потери result.

## Неопределённость

- Сохраняй iteration count, seeds, mean, стандартную ошибку/интервалы, когда доступны.
- Target_error/DPS error не гарантирует достаточную точность редкого proc или разницы counts.
- Два близких средних не доказывают равенство rates; два сильно разных средних без matched inputs не доказывают причину.
- Повторяй независимые seed blocks. Если используешь paired differences, обоснуй pairing; одинаковый seed после изменения event graph не гарантирует одинаковых RNG streams.
- CI вычисляй по реальным iteration/replicate observations. Не выводи Poisson confidence из дробных усреднённых counts.
- Результат одного debug iteration показывает event order, но не типичную proc frequency.
- Не исключай нулевые executions из средних без объявления conditional sample.

## Формулировки для Guillotine

Корректно: «В предоставленном эксперименте R/E снизилось примерно с 1.997 до 0.998 при близких средних E. Зарегистрированных direct results стало примерно вдвое меньше».

Недостаточно доказательств для: «dummy съедает второй AoE slot», «proc стал реже», «все потерянные results принадлежат dummy», «это доказанный баг игры», «опция ignore_invulnerable_targets исправляет эффект».

Проверка текущего C++ может показать возможный механизм, но старый эксперимент без версии и trace остаётся E1 по provenance.
