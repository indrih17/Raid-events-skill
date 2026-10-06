# Проверка готового route и расследования

## Перед генерацией

- Границы ключа и t0 известны или объявлены approximation.
- Roster и pets отделены.
- Каждый GUID учтён один раз; повторные окна обозначены.
- Initial mobs согласованы с MDT и log.
- Spawned атакуемые targets не пропущены.
- Chain overlaps сохранены без двойного счёта.
- Start/death/last damage не смешаны без confidence.
- Boss phases и priority windows имеют evidence.
- BL связан с absolute timestamp и реальным buff.
- Таблица pull summary и target ledger построены.

## Конфигурация

- max_time соответствует declared timeline scope.
- fixed_time/vary length явно заданы.
- fight_style стоит до raid_events.
- Нет позднего raid_events=, стирающего route.
- Обычный trash не add_boss; boss classification обоснована.
- Группируются только действительно одинаковые windows.
- Имена имеют pull suffix, collision отсутствует.
- Точный режим фиксирует min/max; approximate использует исходный stddev=1 с пометкой.
- Одноразовость проверена, особенно route >5160.
- Dummy invulnerable всё окно, no unintended dummy damage.
- Нет /stun как замены target downtime.
- Invulnerable/target replacement continuity оценена.
- Авто BL отключён, явные windows правильны.
- Geometry не выдумана.

## APL и runtime

Проверь expanded APL, adds/pull expressions, retarget, cooldown gating, potion и resource carryover. После parser/smoke run проверь actual event trace:
start/finish каждого event, summons/expirations, active_enemies, player/proc targets, BL gain/expire, downtime. Пустой interval без damage не доказывает, что player idle из-за отсутствия targets.

strict_parsing не проверяет реалистичность timeline и не заменяет source audit.

## Сравнение результатов

Нужные scopes:
- damage / DPS / exposure;
- priority damage по target/window;
- E/R/tick counts;
- direct vs compound/children;
- per-target actual amounts;
- proc attempts и successful callbacks, если frequency question;
- uncertainty конкретных metrics.

Не применяй uncertainty player DPS к rare proc count. Не называй current source proof historical runtime.

## Инструменты

check_repository.py проверяет внутренние Markdown file links, сохранение исходного blob, JSON fixtures и наличие ресурсов. unittest проверяет observable arithmetic, schema rejection, GUID duplicate handling, deterministic windows, extraction ambiguity. Это проверки репозитория и Python scripts, **не запуск SimC**.

build_route.py — валидатор нормализованного target ledger и генератор overlay. Он не является полным SimC parser, log parser или механической проверкой source. Успешная генерация не доказывает, что конкретный binary примет каждую option.

## Статус выдачи

Обязательно обозначь:
- generated example / syntax checked / simulated;
- verified SHA/build;
- отсутствующие artifacts;
- known model approximations;
- strongest supported claim.

Если binary нет, сохрани полезные inputs и не утверждай, что sim был выполнен.
