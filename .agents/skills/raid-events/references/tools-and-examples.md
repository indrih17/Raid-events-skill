# Инструменты и примеры

Все scripts: Python 3.10+, стандартная библиотека, без доступа к сети. Команды ниже выполняются из корня репозитория. Они проверяют/преобразуют данные; не запускают SimC и не устанавливают механику автоматически.

## compare_results.py

~~~text
python .agents/skills/raid-events/scripts/compare_results.py .agents/skills/raid-events/assets/guillotine-observations.json
python .agents/skills/raid-events/scripts/compare_results.py baseline.json invulnerable.json --json
~~~

Принимает normalised schema_version=1 с cases. Первая case — baseline.
Обязательные поля каждой case: label, action, owner, num_executes, num_direct_results, damage, damage_scope. Метрики — число или объект с numeric mean. Запрещены отрицательные значения, NaN/Infinity, bool, missing fields и повторные label. Action/owner/damage_scope должны совпадать.

~~~json
{"schema_version":1,"cases":[{"label":"baseline","action":"perfected_guillotine","owner":"Player","num_executes":43.662,"num_direct_results":87.184,"damage":10534000,"damage_scope":"unspecified"}]}
~~~

Считает R/E и absolute/percent deltas. При zero denominator выдаёт undefined/null. Не строит CI из усреднённых counts и не определяет causality. Damage/result намеренно не рассчитывается как физическая метрика при неизвестном direct/compound scope.

## extract_action.py

~~~text
python .agents/skills/raid-events/scripts/extract_action.py report.json --player Player --action perfected_guillotine --label baseline --output baseline.json
~~~

Поддерживает явно выбранный layout sim.players[].stats с children, а pets только через --pet и stats_pets. Выбирает exact name и требует ровно одну matching player/action. Не ищет наугад во всех JSON объектах, не объединяет одинаковые actions и не суммирует parent/child.

Схема сверена по [report_json.cpp](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/report/json/report_json.cpp#L273). Реальные historical reports не предоставлены; extraction проверена synthetic fixtures. Другие layouts/версии могут требовать adapter.

Default damage-field=actual_amount, который может включать direct и ticks соответствующей stats action. --damage-field compound_amount включает aggregated child scope по report semantics. Ни один default не означает automatically direct-only damage.

Поля sample принимаются только как number или object с mean; sum/count не подставляются вместо mean. Некоторые zero fields SimC может omit: default extractor отказывает, а --missing-zero явно разрешает принять отсутствующие num_direct_results/actual_amount за ноль и записывает это в output metadata. Не применяй option к report без достаточных details.

Output содержит path выбранной row, spell ID, owner, source file SHA256 и объявленные zero assumptions. Результаты разных owners/scopes сравнивай только после осмысленной нормализации.

## build_route.py

~~~text
python .agents/skills/raid-events/scripts/build_route.py .agents/skills/raid-events/assets/example-timeline.json --output route.simc
python .agents/skills/raid-events/scripts/build_route.py .agents/skills/raid-events/assets/example-timeline.json --exact --output route-exact.simc
~~~

Input: schema_version=1, duration, targets, optional bloodlust list absolute timestamps. Каждый target имеет guid, name, pull, start, end, kind trash/boss, origin initial/spawned, confidence confirmed/estimated и evidence. npc_id необязателен; unknown — null.

Каждый GUID один раз; collisions и duplicate GUID отвергаются, чтобы chain pulls не удвоили targets. Окна 0 ≤ start < end ≤ route duration. Names безопасные ASCII; выход получает _P01 suffix. Targets с разными windows никогда не группируются автоматически.

Default duration_stddev=1 сохраняет route approximation. --exact фиксирует min/max lifetime. Generated dummy живёт route+1, starts через конечный timestamps=0. BL finite timestamps, exact 40-second duration. /adds для trash, type=add_boss только kind=boss.

Input уже должен быть реконструирован: скрипт не разбирает raw combat log, не проверяет истинность evidence, не задаёт priority targeting, group HP, range, APL или dot continuity. Uncertain lifetimes сначала выбираются как объявленный sensitivity variant. Generated output остаётся encounter overlay, не полным player profile.

## check_repository.py и tests

~~~text
python .agents/skills/raid-events/scripts/check_repository.py
python -m unittest discover -s .agents/skills/raid-events/scripts/tests -v
~~~

Frontmatter проверяется встроенным валидатором простых name/description scalar fields; он не предназначен для произвольного YAML. Штатный quick_validate.py в среде подготовки не запускался успешно из-за отсутствующего PyYAML; отдельная проверка здесь полностью покрывает фактически используемый простой manifest.

Проверка blob сравнивает архив source/original-methodology.md с исходным Git blob SHA. Перекодирование или изменение line endings считается изменением источника.

Tests проверяют arithmetic, zero/missing/bad values, scope compatibility, GUID duplicate rejection, exact boundaries, boss classification, BL order и ambiguous extraction. Это не SimC regression suite.

## Статус примеров

assets/example-timeline.json — synthetic учебный маршрут.
assets/guillotine-observations.json — user-provided historical means.
assets/repro/*.simc — учебные overlays, не запущенные в SimC при создании.
assets/investigation-template.md — структура нового отчёта.

Для подлинного reproduction дополнительно нужны real profile, binary/build и raw reports; см. minimal-repros.md.
