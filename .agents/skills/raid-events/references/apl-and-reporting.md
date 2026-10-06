# APL, retarget и priority reporting

## Event expressions

Ищи в expanded APL:
~~~text
raid_event.adds.up
raid_event.adds.remains
raid_event.adds.in
raid_event.pull.exists
raid_event.pull.in
raid_event.pull.remains
fight_style.dungeonroute
~~~

При переходе /adds → /pull прежний adds gating может потерять смысл. Поддержку expression, sentinel value без события и aggregation по нескольким events проверь в source своей версии. Не считай raid_event.adds.remains lifetime каждой отдельной priority цели.

Пример идеи из исходника, а не готовый полный APL:
~~~simc
actions.cooldowns+=/berserk,if=((fight_style.dungeonroute&raid_event.pull.remains>=15)|(!fight_style.dungeonroute&(!raid_event.adds.up|raid_event.adds.remains>=15)))
~~~
Остальные условия cooldown сохранены из actual class APL. Не заменяй их учебной строкой.

## Симметрия эксперимента

Сравнивая fight styles, сохраняй одинаковое намерение APL: минимальное окно для CD, target choice, movement, resource carryover и BL. Literal identical APL может быть не semantic identical, если expressions относятся к другому типу event.

Сохрани diff APL как самостоятельный artifact. Если совместимость потребовала адаптации, объясни change и отдельно проверь влияние, чтобы не приписать его gear.

## Retarget

Исходный пример:
~~~simc
actions=retarget,target_if=max:target.health,line_cd=5
~~~
actions= переопределяет список, поэтому эту строку нельзя бездумно вставить в готовый профиль с combat actions. Проверь реальное место retarget в APL и syntax своей версии.

max:target.health не обязательно выбирает реальный priority target; при synthetic HP зависит от lifetime и текущего состояния. line_cd=5 добавляет задержку между попытками смены. Логируй actual target swaps.

Proc может таргетить triggering state, а не current player target. Retarget APL и invulnerable event retarget — разные пути.

## Priority damage

merge_enemy_priority_dmg=1 управляет представлением/агрегацией отчёта, не командует player выбором priority цели. Проверь actual actions и per-target damage.

Для priority comparison:
- задавай конкретные GUID/windows;
- показывай damage в window, первые hit timestamps и burst;
- отделяй collateral cleave от намеренного focus;
- фиксируй alive exposure и count;
- не суммируй merged row и исходные rows повторно.

DPS в коротком window и full-route DPS используют разные denominators. Total damage полезен для неизменного fixed duration, но не достаточен для health-driven route с меняющимся TTK.

## Pets и guardians

Проверяй owner, target acquisition, summon/despawn, travel и inherited target. Player retarget не гарантирует немедленного pet retarget. Parent/child aggregate не доказательство per-target распределения pet damage.

## Проверка cooldown gating

Для одного trace выпиши t, active enemies, target IDs, adds/pull up/in/remains, cooldown ready, условие APL и выбранное действие. Профиль может правильно ждать next pull, а может держать CD из-за sentinel value/неподходящего expression. Финальный DPS не различает эти причины.
