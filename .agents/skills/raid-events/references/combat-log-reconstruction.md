# Восстановление M+ из combat log

## Содержание
Границы ключа; идентичность целей; lifetimes; chain pulls; spawned targets; phases; Bloodlust; итоговая таблица.

## Время и группа

1. Найди CHALLENGE_MODE_START и CHALLENGE_MODE_END, если формат лога их содержит. Отсутствие маркера не заменяй выдуманным start: укажи выбранную альтернативную границу.
2. Определи пять игроков по roster/идентичности персонажей, отдельно pets/guardians и summons. Не считай всех источников damage игроками.
3. Нормализуй timestamps к одному t0. Сохрани исходное время, timezone, millisecond precision, log offset и выбранный zero.
4. Установи, что означает max_time: длительность ключа, наблюдаемого боевого фрагмента или route overlay. Обрезанные начало/конец меняют exposure.
5. Не объединяй timestamps разных экспортов до проверки их clocks и относительного offset.

## Таблица spawn identities

Основной ключ — полный GUID конкретного spawn, не NPC ID и не отображаемое имя. Для каждого GUID:
- NPC ID, имя, initial/spawned, источник идентификации;
- earliest observed interaction, earliest damage, earliest visible summon/spawn;
- last damage, death/despawn, phase disappearance;
- назначенный pull и связи с chain pull;
- доступность для атак исследуемого игрока;
- lower/upper bounds появления и исчезновения;
- evidence events и confidence.

Одинаковый NPC в разных пулах получает suffix P01/P02. GUID включает spawn identity, но извлечение NPC ID зависит от формата; не делай универсальный парсер одного шаблона для всех версий.

## Начало и конец жизни

Первый damage не всегда spawn: цель могла существовать раньше, а лог мог не содержать видимого summon. Последний damage не всегда death: цель могла жить, быть пропущенной группой или уйти в immunity. Death event сильнее догадки из последнего удара, но проверяй полноту лога.

Различай:
- existence window — actor существует;
- attackable window — можно наносить урон;
- observed damage window — игрок/группа реально наносили урон;
- priority window — цель должна быть основной.

Для uncertain lifetime сохраняй interval bounds и sensitivity variants. Не превращай t=first damage в достоверный spawn без пометки. Если распил цели на два /adds теряет dots, это ограничение модели, а не исправленная история.

## Пуллы и chain pulls

Строй пуллы по группе конкретных spawn, а не только по временным окнам. При overlap одна и та же цель может пережить вступление следующей пачки. В итоговой модели GUID представлен один раз, даже если обсуждается в двух narrative pulls.

Initial mobs определяй по MDT/маршруту вместе с наблюдением. MDT не доказывает, что все отмеченные NPC атакованы одновременно. Combat log выше маршрутной догадки. Рассмотри:
- pre-pull damage;
- patrol joining;
- mobs pulled later;
- перетаскивание surviving targets;
- reset/re-engage без нового GUID;
- combat resurrection / duplicate exports;
- начало следующего пула до смерти последней цели предыдущего.

Если живой GUID имеет несколько окон доступности, обозначь window IDs; генерировать его как независимые actors допустимо только с явно потерянной continuity.

## Spawned adds и роль

Учитывай реальные атакуемые boss adds, Healing Tide Totem, Council totems, Animated Gold, Half-Finished Mummies, Minions и другие spawned targets, даже если MDT их не содержит. Эти названия — сохранённые примеры исходного материала, не универсальный список для каждого сезона.

Не создавай DPS target лишь из наличия механики в DungeonRoute. Например, coffin Mchimba из исходного README не моделируется для танка автоматически. Проверяй фактический доступ/роль. «Танк не наносил damage» и «цель недоступна танку» — разные факты: отсутствие damage может быть решением игрока.

## Boss phases

Веди boss lifetime отдельно от phase/add windows. HP-triggered phase в игре не делает raid event автоматически health-driven; в восстановлении используй observed timestamp.

Учебный пример исходной структуры:
- boss 1620–1840;
- add B 1628–1672;
- boss alone 1672–1714;
- phase C 1714–1840.

Нельзя создать все три цели на 1620. Также нельзя считать start C равным death B без данных. Для immunity phase сначала оцени target state continuity; см. invulnerable-actors.md.

## Bloodlust и downtime

BL фиксируй по реальному buff gain на игроке, duration/refresh и источнику. Cast success может не означать buff у исследуемого игрока. Разделяй разные haste buffs; не подставляй bloodlust для любого ускорения.

Downtime классифицируй: нет атакуемых целей, forced movement, player stun, смерть игрока, range, mechanic assignment, добровольный idle. Не все интервалы без damage — stun или отсутствующие enemies. Используй отдельные доказательства.

## Таблица перед кодом

| Pull | Start | End | Duration | Initial mobs | Spawned mobs | Boss/Trash | Фазы/priority | BL | Неопределённость |
|---|---:|---:|---:|---|---|---|---|---|---|
| P01 | observed | observed | End−Start | GUID set | GUID set | по данным | отдельные окна | absolute t | bounds/source |

Дополнительно сохрани машиночитаемый список lifetimes. Таблица на уровне pull не заменяет список targets с разной смертью. Когда данные достаточны, промежуточное подтверждение таблицы не обязательно; реконструкция всё равно предшествует генерации.
