# Warcraft Logs, M+ события и Lorrgs

Источник интерфейса: [upstream WCL reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/warcraftlogs.md). Setup и JSON: [warcraft-cli](warcraft-cli.md). Методика реконструкции остаётся в [combat-log-reconstruction](combat-log-reconstruction.md).

## Доступ и scope

`warcraftlogs doctor`, `warcraftlogs auth status`, `warcraftlogs rate-limit` показывают готовность. Публичный API требует `WARCRAFTLOGS_CLIENT_ID` и `WARCRAFTLOGS_CLIENT_SECRET`. Приватные отчёты требуют пользовательского OAuth и разрешённого доступа; `auth login`/`auth pkce-login` настраиваются отдельно с зарегистрированным redirect URI. Для private reports нужны соответствующие scopes, включая `view-private-reports`; один `view-user-profile` недостаточен. Не запускай login/logout без задачи об авторизации и не выводи токены.

Выбирай `--site retail|classic|fresh` до subcommand. Report code относится к одному site. Начни с `report-fights`; явно задай fight ID, даже если URL содержит его. CLI принимает report URL или code; это не Raider.IO run ID.

```text
warcraftlogs report-fights <report>
warcraftlogs report-master-data <report>
warcraftlogs report-player-details <report> --fight-id <id>
warcraftlogs report-events <report> --fight-id <id>
warcraftlogs report-table <report> --data-type damage-done --fight-id <id>
warcraftlogs report-encounter-damage-target-summary <report> --fight-id <id>
warcraftlogs report-encounter-casts <report> --fight-id <id> --hostility-type enemies
warcraftlogs report-encounter-aura-summary <report> --fight-id <id> --ability-id <spell-id>
```

## Полнота событий и время

`report-events` возвращает одну страницу. Поле `data.next_page_timestamp` означает необходимость следующего запроса с теми же filters и `--start-time <timestamp>`. Сохраняй fight/window end; повторяй до отсутствия next-page marker. При null events, GraphQL warnings или обрыве полнота неизвестна. Если cursor не растёт, остановись и зарегистрируй ошибку; не зацикливай запросы. При соединении страниц не удаляй разные события только потому, что timestamps совпали.

В `report-events/table/graph` start/end — миллисекунды от начала отчёта. В encounter-командах `--window-start-ms/--window-end-ms` задают offset внутри fight. Для абсолютного времени прибавь report start, для key-relative времени вычти выбранное начало ключа; явно сохрани преобразование. Даты listing/sampled запросов могут использовать epoch ms/ISO вместо report offsets.

Clamping окна отражён в `query.effective_window_*`, `window_clamped`; uptime нормализуй по фактической duration. В casts-команде `casts.truncated` показывает неполноту даже при наличии агрегатов. Completed `cast` count не учитывает все begincast/empower events и не равен proc executions или damaging impacts.

Если typed command не покрывает нужный event/filter, используй `warcraftlogs graphql --query @query.graphql` с явными variables после проверки schema/help. `provenance.graphql_warnings` сигнализирует partial result. Не публикуй непроверенный GraphQL как работающий запрос.

## Применение к target timeline

1. Сохрани key/fight bounds, site, zone, difficulty, keystone level, roster и report master data. Fight list не гарантирует отдельные trash pulls.
2. Выгрузи нужные полные event slices и проверь NPC identity/instance поля. Actor ID WCL — локальный идентификатор отчёта; если spawn GUID не доступен, сохраняй WCL identity отдельно, отмечай mapping неизвестным. Не генерируй GUID из догадки.
3. Урон по целям, cast windows и aura bands помогают найти участки для проверки. Первая/последняя запись damage не доказывает spawn/death; отсутствующие события не становятся точными lifetime boundaries.
4. Chain pulls, spawned adds, invulnerability и BL проверяй по событиям с confidence/evidence. Summary не заменяет событие и не доказывает all-target coverage. Raid-specific encounter analytics не объявляй универсальным M+ parser.

Ауры: `aura_holder` — носитель, `applied_by` — наложивший. Upstream `--view-by source` группирует по носителю, `--view-by target` — по caster; читай `row_actor` и query. Для BL извлекай источник и фактические bands/events, а не только total uptime. Не смешивай report-local class IDs с Blizzard IDs.

## Таланты и сравнения

`warcraftlogs report-player-talents <report> --fight-id <id> --actor-id <id> --out <packet.json>` извлекает scoped raw talent tree. `transport_status: raw_only` не означает проверенный SimC build. Передай packet в [simulation](warcraft-simulation.md) для round-trip validation.

Cross-report analytics (`boss-kills`, `spec-kill-samples`, `ability-usage-summary`) — ограниченные выборки. Сохраняй sample size, selection/truncation, duplicate handling, difficulty/key-level mix, freshness. Верхние быстрые kills не являются случайной или глобальной выборкой.

Lorrgs: `lorrgs specs`, `lorrgs bosses`, `lorrgs spec-ranking <spec-slug> <boss-slug>`, `lorrgs report-overview <report>`. `warcraft cooldown-packet <report-url> --actor-id <id> --phase <n>` связывает cast events WCL с контекстом Lorrgs. Проверь `player_casts.complete`, partial errors, phase source и пригодность top-parse samples. Нумерация фаз может различаться; сравнивай encounter phase identity. Received externals не считаются собственными casts. Если Lorrgs не имеет отчёта или фаз, top-parse сравнение отсутствует; не достраивай его. Timings лучших parses помогают сформулировать гипотезу, но не доказывают оптимальность для другого M+ pull.
