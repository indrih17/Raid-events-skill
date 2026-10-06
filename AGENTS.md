# Правила работы в Raid-events-skill

Этот репозиторий — русскоязычная методичка и Codex skill для SimulationCraft. Основная задача: восстановление наблюдаемого M+ target timeline и проверка механик по данным, коду и воспроизводимым экспериментам.

- Сохраняй source/original-methodology.md неизменным. Исправления и уточнения размещай в references; поясняй расхождения в source/provenance.md.
- Основной skill: .agents/skills/raid-events/SKILL.md. Подробности вынесены в references, примеры в assets, детерминированная автоматизация в scripts.
- Не заменяй combat log предположениями из MDT или DungeonRoute. Не выдумывай GUID, lifetime, HP, spell/item IDs, результаты симуляции или недоступную историю.
- Для каждого вывода разделяй наблюдение, проверенный код, гипотезу и неизвестное. Сохраняй SHA, build, game data, profile, параметры запуска и источники.
- При расследовании proc проверяй всю цепочку callback → initial target → available_targets/target_list/cache → AoE cap → impact → stats. Player target не обязательно равен proc target.
- num_executes не универсальный счётчик успешных proc; num_direct_results не универсальный счётчик успешных damaging hits. Проверь owner, action, aggregation и result types.
- Известные числа Guillotine сохраняй точно. Эксперимент показывает изменение зарегистрированных попаданий, но сам по себе не определяет точную причину.
- Не публикуй неподтверждённый syntax как рабочий профиль. Для SimC примеров явно указывай статус: учебный overlay, parsing checked, simulated или historical observation.
- При изменении scripts запускай unittest и check_repository.py; проверь ошибочные входы, арифметику, schema и отказ при неоднозначности.
- Проверяй ссылки и переносимость skill целиком; не дублируй главы в SKILL.md.
- Не меняй чужие логи или исходный SimC ради нужного результата. Диагностический patch держи отдельно от baseline.
- Работа с main разрешается текущим запросом пользователя. Эта инструкция не даёт постоянного разрешения на будущие push, merge или внешние публикации; следуй авторизации конкретной задачи.
