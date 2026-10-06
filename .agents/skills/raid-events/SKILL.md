---
name: raid-events
description: Reconstruct M+ target timelines from combat logs and MDT, build SimulationCraft raid events, and investigate proc targeting, invulnerability, RPPM, haste, and unexpected damage results.
---

# Raid Events / SimC investigator

Восстанавливай target timeline по данным и расследуй реализацию SimC с проверяемой цепочкой доказательств. Пиши объяснения по-русски, если пользователь не выбрал другой язык.

## Выбор материалов

- Маршрут из лога: [combat-log-reconstruction](references/combat-log-reconstruction.md), [event-modeling](references/event-modeling.md), [model-limitations](references/model-limitations.md).
- Proc/потерянные попадания: [proc-debugging](references/proc-debugging.md), [target-selection](references/target-selection.md), [invulnerable-actors](references/invulnerable-actors.md).
- Частота и haste: [rppm-haste](references/rppm-haste.md).
- Контроль качества: [evidence-rules](references/evidence-rules.md), [minimal-repros](references/minimal-repros.md), [validation](references/validation.md).
- APL и priority damage: [apl-and-reporting](references/apl-and-reporting.md).
- Работа с кодом: [sources-and-code](references/sources-and-code.md), [source audit](references/source-audit-2026-10-06.md).
- Общий алгоритм: [methodology](references/methodology.md).
- Практический пример: [Perfected Guillotine](references/case-studies/perfected-guillotine-invulnerable.md).
- Автоматизация и форматы: [tools-and-examples](references/tools-and-examples.md).

Читай только главы, нужные для задачи. Skill переносится всей папкой вместе с resources.

## Рабочий алгоритм

1. Уточни проверяемый вопрос и измеряемую величину: реальный timeline, число proc, зарегистрированные результаты, damage per result, priority damage или TTK. Зафиксируй доступные артефакты и отсутствующие данные.
2. Для маршрута найди начало/конец ключа и группу. Веди отдельную запись на GUID spawn. До профиля составь таблицу пуллов, initial/spawned mobs, phases, BL, downtime и неопределённостей. Chain pulls не дублируй.
3. Для механики зафиксируй SimC SHA/build и IDs. Проследи создание effect/action/callback, условия trigger, выбор initial target, target list/cache, cap, impact и запись stats. Не останавливайся на одном подозрительном фрагменте.
4. Сделай минимальный контроль, меняя один фактор. Разделяй двух атакуемых целей и двух actor всего; отмечай существование invulnerable dummy. Отдельно проверь debug timeline и статистические серии.
5. Сравни execution/direct/tick results, damage, per-target results, active time и trigger rate. Проверь единицы, owner и aggregation. Ratio of means не выдавай за mean per-proc ratio.
6. Сопоставь эксперимент с кодом и альтернативами. Присвой каждой формулировке уровень доказательности.
7. Выдай вывод, границы, профиль/команду, таблицу метрик, ссылки на код по SHA и следующий различающий эксперимент, если причина не установлена.

## Инварианты

- Combat log выше маршрутной догадки; MDT — состав initial mobs, не автоматическое доказательство lifetime. Неопределённость нельзя превращать в точный timestamp.
- Для time-driven /adds дополнительный урон не сокращает duration; synthetic HP может менять execute/HP-dependent effects.
- /invulnerable может менять target state и доступные списки. /stun моделирует игрока, а не downtime цели.
- Сохраняй исходный материал; не выдумывай IDs, профили, code evidence или отсутствующую историю.
- Одноразовость события проверяй по scheduler; cooldown=5160 — исходная конвенция, не гарантия для любого маршрута.
- Для route-модели сохраняй исходный default duration_stddev=1 с объяснением jitter; для точного диагностического repro задавай проверенные bounds.
- Не делай вывод из одного DPS. num_executes и num_direct_results требуют проверки semantics соответствующей action.
- Guillotine historical observation: 43.662/87.184/10.534M baseline; 43.719/43.643/5.200M с invulnerable. Примерно 1.997 → 0.998 results/execution. Доказано изменение зарегистрированных попаданий в предоставленных данных; точная причина отдельно не доказана.
- Не утверждай, что «добавление invulnerable всегда ломает AoE» или что «ignore_invulnerable_targets гарантированно исправляет любой proc».
- Публикация/commit и любые внешние изменения выполняются только в пределах текущей задачи пользователя.

## Формат результата

Для маршрута: таблица → один непрерывный SimC block с русскими комментариями и PULL-разделителями → статус проверки и ограничения.
Для расследования: вопрос → наблюдения → проверенный код → вывод → гипотезы/неизвестное → repro и источники.
Готовый case study содержит provenance, версии, metric definitions и falsification controls. Используй [шаблон](assets/investigation-template.md).
