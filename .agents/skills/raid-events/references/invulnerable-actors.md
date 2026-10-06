# Invulnerable actor: состояние, lists и downtime

## Разные понятия

Invulnerable, sleeping, dead, out of range и отсутствующий actor — разные состояния. Удаление цели из доступного списка не обязательно уничтожает actor или обнуляет references на неё. Нулевой damage не обязательно означает отсутствие зарегистрированного result.

## Проверенные побочные эффекты

В [invulnerable_event_t::_start](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/raid_event.cpp#L1472):
1. target->clear_debuffs();
2. increment invulnerable;
3. halt игроков;
4. acquire_target при retarget=1.

В [invulnerable_debuff_t](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/player.cpp#L505) ignore_invulnerable_targets удаляет actor из target_non_sleeping_list при начале buff и возвращает при expire, меняя active_enemies.

В [target_mitigation](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/player/player.cpp#L8429) invulnerable может обнулить result_amount. Scope — SHA cafc27227ec08760cb391d6a798e104435c29a87. Эти code facts не являются доказанной причиной Guillotine observation.

## Dummy для route

Постоянно invulnerable base target помогает держать route infrastructure, но его нужно проверять:
- immunity начинается до первого harmful action;
- primary target player/action/proc не остаётся неожиданно dummy;
- dummy отсутствует в damage denominator/priority row;
- нет zero-damage direct results, меняющих трактовку counters;
- между adds нет вредоносного damage по dummy;
- при summon/expire targets cache и retarget обновляются;
- counts у изучаемого proc проверены отдельно.

ignore_invulnerable_targets=1 и retarget=1 — настройки route, не гарантия одинаковых фильтров для каждого custom proc.

## Boss phase continuity

Не применяй /invulnerable без оценки clear_debuffs. Если в игре dots/debuffs должны сохраняться, такой event может моделировать другую механику. Проверь точную clear_debuffs реализацию и классовые target data: не объявляй, что абсолютно любое состояние любого класса уничтожается без чтения кода.

Альтернативы зависят от question:
- отдельные attackable windows, если потеря state допустима;
- специализированное событие/patch в изолированном тесте, если нужно сохранить state;
- моделирование ограничения действий/позиции, если actor остаётся доступным;
- явное ограничение «эту continuity текущий профиль не воспроизводит».

Разбиение boss на независимые adds тоже сбрасывает identity/state и не является универсально точной заменой.

## Player stun не target downtime

/stun применяется к игроку. Его допустимо использовать только при доказанном player stun/эквивалентной потере control, а не как замену недоступной цели. Movement тоже не равно total damage prohibition: instant/ranged/melee actions могут реагировать по-разному.

## Контрольный тест

Запусти короткое окно до/во время/после immunity:
- target IDs и states;
- dots/debuffs до и после start;
- player/action/proc target;
- candidate list и active_enemies;
- scheduled impacts через boundary;
- damage и direct/tick categories;
- APL gating и resumed actions.

Покажи, что именно соответствует игре, а что является ограничением SimC. См. target-selection.md и Guillotine case.
