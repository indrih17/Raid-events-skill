# RPPM и haste investigation

## Что доказывает scaling

Не выводи haste scaling из tooltip, из общего DPS или из числа hit events. Разделяй:
- base RPPM/frequency;
- item/role/spec modifiers;
- RPPM scaling mask;
- частоту eligible attempts;
- cap interval и BLP;
- cooldown;
- damage/crit/HP scaling;
- длительность active windows.

Сначала найди effective configuration для конкретного effect. Настройка generic RPPM механизма не доказывает, что Guillotine использует RPPM_HASTE.

## Проверенный алгоритм

В [real_ppm_t::proc_chance](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/proc_rng.cpp#L48) для прочитанного SHA:

~~~text
effective_rppm = base_frequency × modifier × enabled_coefficients
dt = min(now - last_trigger_attempt, max_interval)
base_chance = effective_rppm × dt / 60
chance = base_chance × BLP_factor
~~~

Enabled coefficients зависят от mask: haste, crit, auto-attack speed. BLP_factor использует accumulated_blp и expected interval. В trigger накопление ограничено max_interval на попытку; при success оно сбрасывается. Повторный attempt в тот же timestamp отклоняется.

В [proc_rng.hpp](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/sim/proc_rng.hpp#L88) max_interval=3.5s и max_bad_luck_prot=1000s. Это версии-конкретные значения; не подставляй «обычные 10 секунд» из памяти.

В [dbc_proc_callback_t::initialize](https://github.com/simulationcraft/simc/blob/cafc27227ec08760cb391d6a798e104435c29a87/engine/action/dbc_proc_callback.cpp#L289) RPPM берётся из effect.rppm(), modifier и scale, когда включён. Custom implementation может отличаться.

## Экспериментальная матрица

1. Один и тот же player/spec/gear/item level/set, фиксированный encounter и одинаковая APL.
2. Baseline haste, controlled higher haste, при необходимости несколько ступеней.
3. Отдельно buff haste (BL window) и rating haste: проверь, какие cache coefficients они меняют.
4. Контроль damage modifiers/crit/mastery/HP; не меняй gear сразу с несколькими stats, если вопрос только о haste.
5. Достаточно длинный постоянный target window для оценки rate, затем route windows/downtime.
6. Toggle scaling только в отдельной диагностической сборке, если исследуешь engine; пометь, что это другой model.
7. Повтори series seeds и отчитай uncertainty конкретных proc metrics.

## Метрики

- eligible trigger attempts и timestamps;
- roll probability, scale flags, coefficients;
- successful callback count;
- damage action executions;
- results/execution;
- damage/result;
- first proc latency и inter-proc intervals;
- число procs внутри/снаружи BL;
- elapsed/active exposure и время без eligible events.

Rate/min = successes × 60 / выбранный exposure. Для route укажи обе величины: per elapsed route minute и per eligible/active minute. Нельзя смешивать их при сравнениях.

## Причины ложного вывода

- Haste ускоряет auto attacks/casts и даёт больше opportunities даже без прямого RPPM_HASTE.
- Direct RPPM_HASTE может работать, но finite-window count быть noisy.
- Same-timestamp AoE events не обязательно независимые attempts.
- BLP/reset/warmup и downtime меняют first proc behavior.
- Дополнительный proc damage может иметь HP/crit scaling независимо от frequency.
- Bloodlust по absolute time и pull-start BL сдвигаются по-разному.
- Дробное num_executes — mean over iterations, не fractional real proc.
- Set bonus может менять action или child, не только rate.

## Вывод

Пиши отдельно: «В effective configuration mask найден RPPM_HASTE»; «В series rate вырос с интервалом неопределённости»; «Изменение damage включает/не включает изменение hits per execution». Если effective mask не прочитан, это гипотеза о scaling, даже при росте observed count.
