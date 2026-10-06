# Raid Events и SimulationCraft: исследовательская методичка

Практическое руководство по восстановлению M+ target timeline из combat log и MDT, проверке реализации SimC и сравнению экипировки, эффектов и APL. Здесь одновременно находятся подробная методичка для человека и переносимый Codex skill.

## С чего начать

1. Для маршрута: [восстановление лога](.agents/skills/raid-events/references/combat-log-reconstruction.md), затем [моделирование событий](.agents/skills/raid-events/references/event-modeling.md) и [проверка профиля](.agents/skills/raid-events/references/validation.md).
2. Для странного proc: [методология](.agents/skills/raid-events/references/methodology.md), [уровни доказательности](.agents/skills/raid-events/references/evidence-rules.md), [target selection](.agents/skills/raid-events/references/target-selection.md).
3. Для Guillotine: [разбор эксперимента](.agents/skills/raid-events/references/case-studies/perfected-guillotine-invulnerable.md).
4. Для haste/RPPM: [отдельная глава](.agents/skills/raid-events/references/rppm-haste.md).
5. Для исходных правил: [полная неизменённая копия README](source/original-methodology.md) и [карта сохранения всех 17 разделов](source/provenance.md).

## Главные выводы

- Combat log задаёт наблюдаемый таймлайн; MDT помогает определить начальный состав. DungeonRoute не заменяет фактические данные.
- Обычные duration-based adds сохраняют окна жизни, но их HP% синтетический; увеличение DPS не моделирует полноценный вклад игрока в сокращение TTK группы.
- Invulnerable actor нельзя считать безвредной декорацией: нужно проверять debuffs, target lists, retarget и каждый proc.
- В эксперименте Perfected Guillotine baseline: 43.662 executions, 87.184 direct results, 10.534M среднего урона. С invulnerable: 43.719, 43.643, 5.200M. Получается примерно 1.997 и 0.998 зарегистрированных direct results на execution.
- Эти данные доказывают изменение числа зарегистрированных попаданий в предоставленном эксперименте. Они сами по себе не доказывают точную причину, конкретную потерянную цель, ошибку target cap или поведение в игре.
- DPS, proc attempts, successful procs, executions, direct results и damage — разные величины.

## Содержание

| Материал | Назначение |
|---|---|
| [SKILL.md](.agents/skills/raid-events/SKILL.md) | Короткий рабочий алгоритм и выбор нужной главы |
| [AGENTS.md](AGENTS.md) | Правила сопровождения этого репозитория |
| [Сопровождение базы](.agents/skills/raid-events/references/knowledge-maintenance.md) | Самостоятельное сохранение проверенных находок, исправления и публикация в main |
| [Методология](.agents/skills/raid-events/references/methodology.md) | От вопроса до проверяемого вывода |
| [Доказательства](.agents/skills/raid-events/references/evidence-rules.md) | Границы вывода, статистика, альтернативы |
| [Combat log](.agents/skills/raid-events/references/combat-log-reconstruction.md) | GUID, пуллы, spawned adds, фазы, BL |
| [Raid events](.agents/skills/raid-events/references/event-modeling.md) | Duration, timestamps, dummy, разбиение событий |
| [Выбор модели](.agents/skills/raid-events/references/model-limitations.md) | Time-driven и health-driven TTK, execute, party damage |
| [Target selection](.agents/skills/raid-events/references/target-selection.md) | Callback → target list → cap → impact → stats |
| [Invulnerable](.agents/skills/raid-events/references/invulnerable-actors.md) | Debuffs, lists, primary target, downtime |
| [Proc debugging](.agents/skills/raid-events/references/proc-debugging.md) | Driver IDs, callbacks, дочерние actions |
| [RPPM/haste](.agents/skills/raid-events/references/rppm-haste.md) | Масштабирование, BLP, attempts, контроль переменных |
| [APL](.agents/skills/raid-events/references/apl-and-reporting.md) | Adds/pull gating, retarget, priority damage |
| [Repro](.agents/skills/raid-events/references/minimal-repros.md) | Воспроизводимая матрица и пакет артефактов |
| [Источники и код](.agents/skills/raid-events/references/sources-and-code.md) | SHA, первоисточники, call chain, provenance |
| [Проверка](.agents/skills/raid-events/references/validation.md) | Timeline, parsing, статистика, контроль результата |
| [Реестр кода](.agents/skills/raid-events/references/source-audit-2026-10-06.md) | Проверенные места конкретного SimC commit |
| [Примеры и инструменты](.agents/skills/raid-events/references/tools-and-examples.md) | Запуск, формат JSON, ограничения скриптов |

## Подключение skill

Skill расположен в стандартном repo-scoped каталоге .agents/skills/raid-events. Открой этот репозиторий в Codex и вызови $raid-events. Для другого проекта скопируй **всю** папку raid-events в его .agents/skills, включая references, scripts и assets. Перенос одного SKILL.md потеряет методичку и инструменты.

Актуальная схема обнаружения описана в [официальной документации](https://learn.chatgpt.com/docs/build-skills). Папка skills в старых предложениях структуры была упаковочным примером; здесь выбран непосредственно обнаруживаемый каталог без дублирующих копий.

Пример запроса: «Используй $raid-events: восстанови окна целей по этому логу; отметь неопределённые lifetime; сформируй таблицу и профиль; проверь Guillotine отдельно».

## Инструменты

Python 3.10+, стандартная библиотека, без сетевых запросов:

~~~text
python .agents/skills/raid-events/scripts/compare_results.py .agents/skills/raid-events/assets/guillotine-observations.json
python .agents/skills/raid-events/scripts/build_route.py .agents/skills/raid-events/assets/example-timeline.json --output route.simc
python .agents/skills/raid-events/scripts/extract_action.py report.json --player YOUR_PLAYER --action perfected_guillotine --label baseline --output baseline.json
python .agents/skills/raid-events/scripts/check_repository.py
python -m unittest discover -s .agents/skills/raid-events/scripts/tests -v
~~~

Генератор принимает уже реконструированные lifetimes, не угадывает маршрут из сырого лога. Примеры — учебные encounter overlays: к ним нужен реальный player profile. Historical Guillotine experiment не воспроизведён здесь: исходные профили, бинарник, seed и отчёты не предоставлены.

## Границы наполнения

Сохранены весь текущий README, предоставленные численные находки и релевантный контекст доступного чата. Добавлены воспроизводимые процедуры и проверка текущего кода. Недоступные прошлые исследования не восстановлены по памяти. Проверка текущего кода датирована 2026-10-06 и привязана к SHA; её нельзя задним числом считать доказательством причины старого эксперимента.

[Происхождение материалов и отсутствующие артефакты](source/provenance.md). [Запись выполненных проверок](source/validation-record.md). Новые исследования добавляй отдельными case studies со своими версиями, профилями и evidence.
