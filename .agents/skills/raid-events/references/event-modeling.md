# Моделирование raid events

## Порядок конфигурации

fight_style может устанавливать/очищать список raid events. Задавай style перед пользовательскими событиями; потом raid_events= задаёт начальный список, raid_events+= дополняет его. Повторный raid_events= может стереть ранее построенный route. См. [официальную wiki](https://github.com/simulationcraft/simc/wiki/RaidEvents).

Для восстановления фиксированного route исходная конвенция:
~~~simc
fight_style=Patchwerk
fixed_time=1
max_time=300
vary_combat_length=0
ignore_invulnerable_targets=1
strict_parsing=1
active_enemies=1
override.bloodlust=0
~~~
300 — учебная длительность, заменить фактической. Эти настройки сами по себе не дают идентичного replay: random duration, RNG, APL и механики остаются отдельными факторами.

## Базовый dummy

Dummy нужен как инфраструктурная цель для модели с adds; он invulnerable весь route и не должен давать фиктивный damage. Исходное правило:
~~~simc
raid_events=/invulnerable,cooldown=5160,duration=5160,retarget=1
~~~
5160 — исходный безопасный интервал для одноразовых событий в соответствующем коротком route. Для длинного route, других bounds или scheduler он не универсален. В точном generated overlay используется конечный timestamps=0 и явно фиксированная duration, превышающая route. Обязательно проверь старт в t=0 и отсутствие pre-event damage по dummy.

Invulnerable — изменение состояния actor, а не удаление его существования. Опция ignore_invulnerable_targets меняет доступные списки в текущем коде, но не заменяет проверку proc target. См. invulnerable-actors.md и source audit.

## Trash и bosses

Обычные targets — /adds. type=add_boss только для реального boss/boss-like target, когда классификация обоснована. Название моба не задаёт автоматически его механические свойства.

Если несколько targets появляются вместе и имеют одинаковую duration, можно count=N. Если spawn/death различаются — отдельные события. Count не отражает GUID identity в реальном логе, поэтому сохрани mapping вне .simc.

Для точного lifetime используй duration_min=duration_max=duration в версии, где эти параметры проверены. duration_stddev=1 сохраняется default для route approximations, но добавляет ± jitter с bounds; это не timestamp-perfect режим.

## First, cooldown и timestamps

- first задаёт первое появление; cooldown/period задаёт последующие события по scheduler.
- last ограничивает планирование starts, а не обязательно обрезает active duration. Проверяй код своей версии.
- timestamps задаёт конечный список абсолютных времён через двоеточие, например timestamps=10:70:140.
- В проверенном SHA timestamps несовместим с first/last и first_pct/last_pct. Не смешивай их.
- Для одноразового add используй один timestamp; cooldown оставь валидным и достаточно большим для sanity checks, хотя starts определяет timestamps.
- Перекрытие разных /adds событий допустимо моделировать отдельно. В проверенном коде один adds event не поддерживает собственные overlapping spawns без соответствующего ограничения.

Не полагайся на wiki defaults без проверки: zero stddev, duration/cooldown bounds и aliases могли меняться. Генератор фиксирует min/max, когда нужен deterministic lifetime.

## Учебный overlay с phase windows

~~~simc
# Учебные числа, не исторический Guillotine repro. Нужен player profile.
fight_style=Patchwerk
fixed_time=1
max_time=300
vary_combat_length=0
strict_parsing=1
ignore_invulnerable_targets=1
override.bloodlust=0
# Dummy недоступен все 300 секунд; конечный список starts
raid_events=/invulnerable,timestamps=0,cooldown=5160,duration=301,duration_min=301,duration_max=301,retarget=1
# ============================================================
# PULL 1
# ============================================================
raid_events+=/adds,name=Trash_P01,timestamps=5,count=2,cooldown=5160,duration=30,duration_stddev=1
raid_events+=/adds,name=Totem_P01,timestamps=14,count=1,cooldown=5160,duration=8,duration_min=8,duration_max=8
# ============================================================
# PULL 2
# ============================================================
raid_events+=/adds,name=Boss_P02,timestamps=50,count=1,type=add_boss,cooldown=5160,duration=120,duration_min=120,duration_max=120
raid_events+=/adds,name=PhaseAdd_P02,timestamps=80,count=1,cooldown=5160,duration=25,duration_min=25,duration_max=25
raid_events+=/buff,buff_name=bloodlust,timestamps=60,duration=40,duration_min=40,duration_max=40
~~~

Профиль — иллюстрация syntax по прочитанному коду, не проверенный запуск SimC. Для настоящего route данные берутся из таблицы/GUID ledger. Не копируй учебный Boss без наблюдаемого boss window.

## Bloodlust

Отключи auto BL override.bloodlust=0. Задай /buff,buff_name=bloodlust,duration=40,timestamps=… по фактическим временам; при укороченном buff проверь возможность корректного моделирования. Фиксируй duration bounds для exact diagnostic test.

Absolute BL в time-driven route и BL на номере health-driven pull отвечают разным вопросам: сокращение предыдущих пуллов сдвигает второй вариант. Не сравнивай их как идентичные условия.

## Финальный формат

Один непрерывный code block с русскими комментариями, PULL-разделителями и уникальными suffix. Укажи перед ним table и uncertainties, после — status parsing/simulation, список approximations и контроль dummy. Не делай «красивый полный маршрут» из неизвестных lifetimes.
