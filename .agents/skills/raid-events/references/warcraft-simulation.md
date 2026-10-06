# Warcraft CLI: SimC, Raidbots и talent transport

Адаптация [SimC reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/simc.md) и [Raidbots reference](https://github.com/aurokin/warcraft_cli/blob/dd77084311d169b812c5a3884c8441e595306aae/skills/warcraft/references/raidbots.md). См. [setup](warcraft-cli.md), [minimal-repros](minimal-repros.md), [evidence-rules](evidence-rules.md). Установленный Python `simc` wrapper не является SimC engine.

## Локальная инспекция

```text
simc doctor
simc repo
simc verify-clean
simc spec-files "<class spec>"
simc describe-build --help
simc priority --help
simc inactive-actions --help
simc analysis-packet <apl-path> --targets 1
simc find-action --help
simc trace-action --help
```

Сначала doctor/repo и настройка пути к существующим исходникам/бинарнику через доступные options. Команды checkout/build меняют окружение и не нужны для read-only вопроса. Не используй их так, чтобы заменить baseline пользователя. `find-action/trace-action` требуют rg. Сохраняй SimC SHA, binary build/game data отдельно от Warcraft CLI SHA.

Для exact build используй `identify-build`/`describe-build` с явным talent export или build source согласно help. `identify-build ok=true` с confidence none/low не устанавливает spec. Неоднозначные candidates требуют проверки. APL basename — подсказка, не доказательство spec; несколько actor в input требуют проверки выбранного owner.

Static `priority`, `apl-prune`, `apl-branch-trace`, `apl-intent`, `opener` не исполняют полную динамику боя. `possible/unknown` не означает inactive, а статический opener не доказывает first cast. Для runtime нужны `first-cast`/`log-actions` или прямой debug run. CLI source search сокращает поиск, но proc всё равно проверяется по всей цепочке [proc-debugging](proc-debugging.md).

## Talent transport

```text
simc validate-talent-transport --build-packet <raw-packet.json> --out <validated-packet.json>
warcraft talent-describe <validated-packet.json> --apl-path <apl-path>
simc compare-builds --help
simc modify-build --help
```

Проверяй validation status, round-trip и unresolved rows. `--build-packet` поддержан только identify/decode/describe/validate-talent-transport; для других commands используй проверенные split talent strings. Нельзя silently потерять unknown entry, rank или hero selection. Game import, point budget и prerequisites не следуют автоматически из успешного SimC encoding. Classic exports не принимай за retail build.

Для сравнения гайдов бери explicit published builds, сохраняя citations, patch и freshness. `guide-builds-simc` может вернуть partial/failed/no-build status: сообщай какие части отсутствуют.

## Реальный запуск

`simc sim <profile.simc>` — consumer wrapper; `simc run` — low-level execution. Перед запуском прочитай help и конечные settings/disclosures. Quick preset, harness defaults, profile settings и CLI overrides могут менять iterations/max_time/default gear/default talents. Для нашего controlled repro явно фиксируй эти значения, seed/threads и все outputs; arbitrary preset не становится правилом точности.

Для APL comparisons доступны `build-harness`, `validate-apl`, `compare-apls`. Делай отдельный harness/variant; исходники SimC и baseline не переписывай. Default gear harness годится для объявленного относительного сравнения и не предсказывает DPS реального игрока. Warnings могут означать проигнорированную condition; проверяй их до дорогого запуска.

Сводный DPS и action_counts не отвечают автоматически на lost impacts. `action_counts`/CPM требуют owner/result semantics. Продолжай использовать raw JSON и [extract_action/compare_results](tools-and-examples.md). Сохраняй error estimates; близкие средние сами по себе не доказывают равенство или точный ranking. Не заменяй анализ uncertainty универсальным правилом из upstream prose о «двух значениях ближе одного mean_error».

## Raidbots

```text
raidbots doctor
raidbots inspect-report <report-url-or-id>
raidbots input <report-url-or-id>
raidbots explain-input --file <addon-export.simc>
```

Это чтение опубликованного report и передача input в локальный SimC. CLI не отправляет новые cloud simulations. Сохраняй report/data/input citations, settings, SimC version и freshness. Top Gear/Droptimizer profilesets не обязательно содержат per-action details; отсутствие этих данных не восстанавливай из headline DPS.

Для локального повторения сохрани полный `data.input` отдельным файлом, проверь внешние imports/paths, profile settings и доступность build. Прочитанный report — наблюдение опубликованного результата; локальное parsing и simulated подтверждаются отдельным успешным запуском. Указывай статус каждого артефакта явно.
