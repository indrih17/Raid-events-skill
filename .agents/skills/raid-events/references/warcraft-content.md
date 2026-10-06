# Wowhead, Warcraft Wiki и гайды

Общие setup/provenance правила: [warcraft-cli](warcraft-cli.md). Команды адаптированы из upstream references по SHA `dd77084311d169b812c5a3884c8441e595306aae`: [Wowhead](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/wowhead.md), [Wiki](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/warcraft-wiki.md). Это справочник CLI, а не проверенные утверждения о механиках игры.

## Wowhead

```text
wowhead search "<название и тип>"
wowhead resolve "<query>"
wowhead entity spell <id>
wowhead entity item <id>
wowhead entity npc <id>
wowhead entity --url <wowhead-entity-url>
wowhead entity-page --url <wowhead-entity-url>
wowhead comments --help
wowhead guide <guide-id-or-url>
wowhead guide-full --help
wowhead guide-export --help
wowhead news --help
wowhead blue-tracker --help
wowhead news-post <news-url>
wowhead talent-calc --help
```

Сначала найди entity и проверь ID, expansion и locale. `entity-page` нужен для подробных связей; drop/vendor listview может содержать sample counts, цены, stock. Не превращай sample drop rate в универсальную вероятность. `facts`/tooltip описывают опубликованную страницу; отсутствие facts key означает неизвестное поле.

Для исследования proc отдельно выпиши item ID, spell IDs эффектов и связанных damage/buff actions. Одно название может относиться к нескольким spells. Tooltip и комментарии дают направление поиска; подтвердить targeting/RPPM/cap нужно кодом, логом и контрольным экспериментом по [proc-debugging](proc-debugging.md). Комментарии игроков сохраняй как свидетельство с датой/версией, а не как установленную механику.

Для hotfix сохраняй дату публикации и дату изменения, patch и источник. Date filters требуют достаточного числа pages; `scan.stop_reason`, `scan.unparsed_timestamps`, `truncated`/total показывают границы поиска. Не заключай «изменений не было» по первой странице. Каталог `/guides/` и отдельная `/guide/` имеют разные команды.

Talent-calc/profiler/dressing-room содержат tool state; не обещай полное декодирование. Retail talent export проверяется через SimC; Classic calculator и retail SimC не взаимозаменяемы.

## Warcraft Wiki

```text
warcraft-wiki search "<query>"
warcraft-wiki resolve "<query>"
warcraft-wiki api CombatLogGetCurrentEventInfo
warcraft-wiki event COMBAT_LOG_EVENT_UNFILTERED
warcraft-wiki event ENCOUNTER_START
warcraft-wiki article "<точное название>"
```

`api` — функции, enum, CVar, UI framework, XML/TOC; `event` — event payload и UI handlers; `article` — общая статья. Читай `reference.signature`, `reference.arguments`, полный `content.text`, ограничения и актуальность страницы. Если `api/event` отвергает классификацию страницы, попробуй её точное название через `article`.

Перед изменением raw-log parser сверяй общие поля и suffix конкретного event type с версией игры и реальной строкой лога. Lua API payload, текстовый WoWCombatLog и WCL normalized event JSON имеют разные schemas. Документированная сигнатура не доказывает наличие значения в пользовательском артефакте. Не подставляй WCL actor ID вместо spawn GUID.

## Сравнение гайдов

Method/Icy Veins: `method search "<query>"`, `method guide <source>`, `icy-veins search "<query>"`, `icy-veins guide <source>`. Форму source и options проверь через help.

Для нескольких источников: `warcraft guide-compare-query "<class spec guide>"`; для уже экспортированных bundles — `warcraft guide-compare <bundle-a> <bundle-b>`. При необходимости `guide-builds-simc` передаёт явно опубликованные билды в SimC. Сохраняй raw sections, citations, freshness, redirects и failed pages. `analysis_surfaces` — извлечённый слой, а не замена исходного текста.

Сравнивай одинаковые patch, spec, hero tree, ST/AoE и тип контента. Разногласие гайдов оформляй как проверяемый вопрос; популярность рекомендации не является симуляцией. Не придумывай отсутствующий talent import из prose. Icy Veins calculator conversion может не включать PvP talents; сохрани calculator URL. См. [simulation](warcraft-simulation.md).
