# Минимальные repro и воспроизводимость

## Что такое repro

Минимальный repro сохраняет механизм симптома и убирает нерелевантные зависимости. Encounter overlay без player/item profile — только часть repro. Historical Guillotine controls нельзя честно восстановить из одних средних.

Пакет:
- expanded player.simc, encounter.simc, run command;
- build/SHA, executable hash, live/PTR/game data;
- profile/input hashes, item/spell/set IDs;
- seed, threads, iterations, fixed/vary duration, RNG options;
- JSON/HTML, stdout/stderr;
- one-iteration debug и instrumentation patch, если нужен;
- normalised metrics и собственный README case.

## Три режима

1. Parsing/smoke: небольшой запуск для syntax и наличия нужной action.
2. Trace: iterations=1, threads=1, debug/log; event order и target IDs.
3. Statistical series: без debug, фиксированные inputs, достаточные repetitions для нужной метрики.

Не выдавай успешный parser check за доказательство mechanics. Не выдавай один trace за статистическую частоту. Не выбирай число iterations только по round number: редкий proc может требовать больше.

## Учебная матрица Guillotine

В assets/repro есть:
- baseline-two-targets.simc: base target + один add;
- invulnerable-two-vulnerable.simc: invulnerable base + два adds;
- invulnerable-one-vulnerable.simc: invulnerable base + один add;
- haste-trace.simc: параметры длительности для controlled haste investigation.

Это диагностические overlays, **не исторические профили**, и они ещё не запускались в SimC. Первые два имеют две vulnerable цели, но не полностью идентичную инфраструктуру: base enemy и add различаются. Поэтому они полезны для первоначального smoke test, но не достаточны для attribution invulnerable-only cause. Для окончательного контроля нужны одинаковые actor classes/HP/geometry или инструментированный harness.

Не добавляй active_enemies=2 к overlay с двумя /adds, думая, что это сохраняет total=2: может появиться дополнительный baseline actor. Читай expanded report и trace.

## Команды запуска

Из папки с сохранённым player profile:
~~~text
simc player.simc baseline-two-targets.simc iterations=10000 threads=1 seed=1001 json2=baseline.json html=baseline.html
simc player.simc invulnerable-two-vulnerable.simc iterations=10000 threads=1 seed=1001 json2=invulnerable.json html=invulnerable.html
simc player.simc invulnerable-two-vulnerable.simc iterations=1 threads=1 seed=1001 debug=1 log=1 output=trace.txt
~~~
Эти команды — шаблоны для установленного совместимого simc, не записи уже выполненных запусков. Файл player.simc должен содержать требуемый gear/set и не перезаписывать encounter позднее. 10000 — стартовая иллюстрация, не статистическая гарантия.

## Минимизация без уничтожения симптома

Убери consumables/прочие procs по одному; затем talents/APL complexity; сохрани eligible triggers. Сокращай duration, только пока симптом воспроизводится. Убедись, что initialisation/set bonus и role не потеряны.

При исчезновении симптома запиши последний удалённый factor и верни его как control. Делать «идеально чистый» профиль без нужного callback бессмысленно.

## Регрессионная матрица после найденной причины

Проверяй one target, 2 targets, >cap targets, dummy on/off, invulnerability toggle, retarget, distance, despawn after trigger, set bonus off/on, HP curves и pets только когда они касаются механизма. Новый patch должен исправлять известный симптом и сохранять прежние controls. Для bug report приложи smallest input и полный provenance.
