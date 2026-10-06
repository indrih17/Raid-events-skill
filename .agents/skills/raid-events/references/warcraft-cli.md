# Warcraft CLI: источники и установка

Адаптация возможностей aurokin/warcraft_cli для нашей методики, 2026-10-06. Проверенный upstream SHA: `dd77084311d169b812c5a3884c8441e595306aae`, package version `0.6.0`. [Исходный skill](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/SKILL.md), [manifest](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/pyproject.toml). Здесь самостоятельная русская адаптация; upstream код устанавливается как внешняя зависимость. Это не импорт WoW-базы данных и не подтверждение всех live endpoints.

## Выбор инструмента

| Вопрос | Провайдер и reference |
|---|---|
| Spell/item/NPC IDs, tooltip, комментарии, hotfix/news | wowhead, [content](warcraft-content.md) |
| WoW API, combat-log payload, UI events | warcraft-wiki, [content](warcraft-content.md) |
| Гайды, билды, различия рекомендаций | wowhead/method/icy-veins, [content](warcraft-content.md) |
| Отчёт, события, участники, ауры, урон по целям | warcraftlogs, [logs](warcraft-logs.md) |
| Составы, cooldown timings в лучших raid parses | lorrgs, [logs](warcraft-logs.md) |
| M+ runs, сезон, аффиксы, профили | raiderio, см. ниже |
| Локальная APL, таланты, controlled simulation | simc, [simulation](warcraft-simulation.md) |
| Опубликованный Raidbots report и его input | raidbots, [simulation](warcraft-simulation.md) |
| Официальные Game Data/Profile данные | blizzard, см. ниже |
| Версия аддона и changelog | curseforge, см. ниже |

Если источник неизвестен: `warcraft resolve "<query>"`, затем `warcraft search "<query>"`. Читай `failed_providers`, `provider_warnings`, confidence и кандидатов. Неоднозначность разрешай по ID, class/spec, версии и URL; первый результат не становится фактом. После выбора источника используй конкретный провайдер.

## Переносимое окружение

Python 3.12+; CLI не встроен в Python-скрипты нашей базы. Из папки skill в PowerShell:

```powershell
python -m venv .warcraft-runtime
& ./.warcraft-runtime/Scripts/python.exe -m pip install 'warcraft @ git+https://github.com/aurokin/warcraft_cli.git@dd77084311d169b812c5a3884c8441e595306aae' 'tzdata==2026.5'
$env:PYTHONUTF8 = '1'
$env:PATH = (Join-Path (Get-Location) '.warcraft-runtime/Scripts') + [IO.Path]::PathSeparator + $env:PATH
warcraft doctor
```

На POSIX используй `.warcraft-runtime/bin/python` и добавь `.warcraft-runtime/bin` в PATH текущей сессии. В следующей сессии заново задай PATH либо вызывай exe по абсолютному пути от расположения skill. Окружение исключено из Git; перенос папки skill требует повторной установки. Не устанавливай одноимённый пакет из PyPI по догадке. Не запускай upstream Makefile для изменения глобальных wrappers. Все дальнейшие команды предполагают выбранное окружение. `simc` в нём — Python wrapper; настоящий SimC executable и исходники настраиваются отдельно.

Windows: upstream не объявляет `tzdata` в dependencies, но импорт Wowhead требует `America/Chicago`; без пакета наблюдался `ZoneInfoNotFoundError`. `PYTHONUTF8=1` устраняет наблюдавшуюся ошибку вывода Wiki `UnicodeEncodeError` в legacy console encoding. Оба исправления выполнены в окружении, upstream код не изменён. Для воспроизводимой установки проверенного набора зависимостей используй `pip install -r assets/warcraft-cli-requirements.txt` из папки skill после создания venv.

Статус проверки 2026-10-06: wrapper doctor и help провайдеров запускаются; live `wowhead entity spell 10060` и `warcraft-wiki event COMBAT_LOG_EVENT_UNFILTERED` успешны. WCL auth status показал `configured=false`, `client_credentials_configured=false`; report API не проверен. SimC doctor показал отсутствующие configured checkout/binary; симуляции и talent round-trip не запускались. Остальные провайдеры покрыты проверкой интерфейса, а не live data contracts. Этот статус — история установки, в новом исследовании проверяй готовность заново.

## Контракт данных

- Обычный ответ — JSON envelope: `ok`, `provider`, `command`, `kind`, `schema_version`, `query`, `provenance`, `data`; при ошибке также `error`. Полезная нагрузка находится в `data`. Сохраняй полный ответ и команду, не только пересказ.
- Глобальные options идут до subcommand: `warcraft --pretty search ...`. `--fields data.results` делает projection; массив не обходится через `data.results.name`. Отсутствие поля в projection не означает отсутствие в источнике.
- `--compact` сокращает prose; сокращённые пути отмечены в `provenance.compacted_paths`. Для доказательства сохрани полный output. `wowhead --stream` возвращает JSONL с header и record-строками.
- Читай `provenance.cache`, source freshness и warnings. Время запуска не равно времени обновления источника. Для обхода cache конкретного провайдера используй в текущей сессии `<PROVIDER>_CACHE_BACKEND=none`; wrapper может обращаться к нескольким провайдерам.
- Exit 0: успех; 1: прочитай причину; 2: исправь usage; 3: проверь auth; 4: проверь ID/scope; 5: сетевой сбой, допустима одна повторная попытка с задержкой. `ok=true` не доказывает completeness или уверенную идентификацию.
- `--expansion <profile>` у wrapper ограничивает routing; подтвердить покрытие нужно по ответу. Не смешивай retail/PTR/beta/Classic, patch, class IDs и expansion IDs разных сайтов.

## Дополнительные источники

Raider.IO: `raiderio dungeons`, `raiderio affixes --region eu`, `raiderio character <region> <realm> <name>`, `raiderio sample mythic-plus-runs`, `raiderio distribution mythic-plus-runs`. Для рейтингов игрока — `raiderio cutoffs --region eu`. Команды/фильтры уточняй через `--help`. Указывай сезон, уровень ключа, roster, patch и объём выборки. `logged_run_id` не WCL report code; состав и время ключа не доказывают pull timeline. `last_crawled_at` может быть старым даже при свежем fetch. Нулевой rank — unranked. Leaderboard samples не описывают всех игроков.

Blizzard: `blizzard doctor`, `blizzard item <id>`, `blizzard realm ...`, `blizzard character ...`; API требует своих credentials. Namespace, region, locale и game version сохраняй вместе с IDs. Официальная запись предмета не заменяет проверку реализации proc и difficulty scaling в конкретном SimC build.

CurseForge: `curseforge doctor`, `curseforge addon <slug-or-id>`; для API нужен ключ. Полезен для версий MDT/Simulationcraft addon и changelog, но changelog не доказывает структуру маршрута пользователя. WowProgress можно исследовать отдельно при задаче о progression; самостоятельный provider reference для него в upstream skill отсутствует, поэтому syntax здесь не добавлен.

Секреты и локальное auth-state не коммить. Для доступных публичных страниц можно использовать web/browser без CLI. Недоступный endpoint, отсутствующие credentials или broken parser отмечай как ограничение, а не как пустой результат.
