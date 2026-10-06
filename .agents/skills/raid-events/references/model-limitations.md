# Выбор модели и её ограничения

## Что сохраняет каждая модель

| Свойство | Duration-based /adds | Health-driven DungeonRoute /pull |
|---|---|---|
| Наблюдаемые absolute windows | Задаются напрямую | Обычно меняются вместе с kills |
| Damage → смерть | Lifetime задан duration | HP расходуется damage |
| Дополнительный DPS → следующий pull | Обычно нет | Может ускорить |
| HP% обычного add | Синтезируется по remaining duration | Зависит от реализации enemy/health |
| Party contribution | Не моделирует marginal feedback сама | Нужна проверка состава и damage группы |
| BL по absolute time | Естественно фиксировать | Может попасть в другой pull после ускорения |

Для обычного duration add в прочитанном [add_t::health_percentage](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/class_modules/sc_enemy.cpp#L1070) HP% = remaining lifetime / total duration × 100. Это code fact по SHA, не универсальный закон всех enemy types.

## Execute и HP-dependent damage

Синтетический linear HP задаёт искусственное распределение времени ниже threshold. В игре HP может падать нелинейно из-за group burst, healing, immunity, phase mechanics и priority focus.

Guillotine multiplier в текущем коде зависит от missing HP. Поэтому одинаковые counts при другой HP curve могут дать другой damage/result. Отдельно проверяй:
- HP sampled at snapshot или impact;
- live target HP vs stored state;
- threshold/continuous multiplier;
- разные lifetime, phase target replacement;
- role и set bonus;
- damage children, не наследующие те же условия.

Не заменяй HP на guessed реальные миллионы лишь потому, что /adds принимает health option: проверь, какая функция используется для lifetime и HP expressions.

## Marginal TTK

Если игрок увеличил damage на ΔDPS, duration adds оставляют прежнюю жизнь targets. Это подходящий вопрос «что я нанесу при тех же окнах», но не «на сколько секунд быстрее погибнет группа мобов».

В single-player health-driven route весь заданный HP может сниматься одним simulated player. Тогда изменение его DPS может переоценивать реальный feedback относительно игры, где он делает только долю group damage. Если в симуляции есть другие реальные actors/damage, оценка меняется: сначала проверь model composition.

Не усредняй результаты двух моделей как автоматическую истину. Они могут служить sensitivity bounds только при обосновании допущений. Запиши player share, group damage approximation и response model.

## Ещё ограничения

- Spawn windows не задают автоматически range/geometry или line of sight.
- Add count не задаёт priority behavior.
- Target replacement может удалить dots/debuffs и изменить ramp.
- Fixed route включает resource/cooldown carryover по sim state; проверь поведение между окнами без targets.
- Повторение расходников, potion и Bloodlust зависит от APL/options.
- Death игрока и wipe не моделируются простым отсутствием adds.
- Танк damage и survivability не следует объединять в один вывод, если incoming damage не построен.
- Одно и то же абсолютное окно priority target может быть недостаточно для реального requirement по burst; сравни damage в окне и время первых hits.

## Как сравнивать gear

Зафиксируй одинаковый expanded player profile кроме исследуемой замены, target windows, APL, geometry, BL, route length и game data. Покажи total damage, damage по priority windows, downtime, proc metrics и uncertainty. Если предмет меняет target lifetime в игре, добавь отдельную health-driven sensitivity, не выдавая fixed-window ranking за доказанный ranking скорости ключа.
