# mini-sha Avalanche 12/13 rounds 境界CI

## Question

`mini-sha` の avalanche effect は、12 rounds から13 rounds の境界で、不確実性込みでも baseline `0.5` 付近へ移るように見えるか。

## Hypothesis

12 rounds は bootstrap CI でも baseline `0.5` よりやや低く、13 rounds は baseline `0.5` と矛盾しにくい。

## Setup

- Command:
  - `$env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m hash_lab.cli avalanche-bootstrap --rounds 12 13 --samples 2000 --seeds 1 2 3 4 5 --samples-output results\2026-05-10-avalanche-mini-sha-12-13-ci\per_sample_flip_ratios.csv --summary-output results\2026-05-10-avalanche-mini-sha-12-13-ci\per_sample_bootstrap_metrics.csv --bootstrap-iterations 2000 --bootstrap-seed 20260510 --ci-level 0.95 --baseline 0.5`
  - `$env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m hash_lab.cli avalanche-seed-bootstrap --rounds 12 13 --samples-input results\2026-05-10-avalanche-mini-sha-12-13-ci\per_sample_flip_ratios.csv --summary-output results\2026-05-10-avalanche-mini-sha-12-13-ci\seed_bootstrap_metrics.csv --per-sample-metrics results\2026-05-10-avalanche-mini-sha-12-13-ci\per_sample_bootstrap_metrics.csv --bootstrap-iterations 2000 --bootstrap-seed 20260510 --ci-level 0.95 --baseline 0.5`
- Executed at: `2026-05-10T02:37:05+09:00`
- Hash / rounds: `mini-sha` / `12, 13`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`
- Bootstrap: percentile bootstrap、`2000 iterations`、`ci_level=0.95`
- Model config: none

保存ファイル:

- `per_sample_flip_ratios.csv`: seedごとの per-sample flip ratio。
- `per_sample_bootstrap_metrics.csv`: roundごとの per-sample percentile bootstrap CI。
- `seed_bootstrap_metrics.csv`: seed階層を保つ hierarchical percentile bootstrap CI。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値は mean flip ratio `0.5`。

Issue #9 の `results/2026-05-10-avalanche-mini-sha-rounds-9-15/aggregate_metrics.csv` では、12 rounds は `mean_of_means=0.493620`、13 rounds は `mean_of_means=0.499301` だった。

## Result

| rounds | mean | per-sample 95% CI | per-sample includes 0.5 | seed階層 95% CI | seed階層 includes 0.5 | baseline_delta |
| ---: | ---: | ---: | --- | ---: | --- | ---: |
| 12 | 0.493620 | [0.492915, 0.494339] | false | [0.492833, 0.494454] | false | -0.006380 |
| 13 | 0.499301 | [0.498677, 0.499905] | false | [0.498378, 0.500203] | true | -0.000699 |

## Interpretation

12 rounds は per-sample CI と seed階層CI のどちらでも baseline `0.5` を含まなかった。Issue #9 の aggregate mean で見えた「12 rounds はまだ少し低い」という観察は、不確実性込みでも同じ向きに見える。

13 rounds は解釈が分かれた。per-sample CI は上限 `0.499905` で `0.5` をわずかに含まない。一方、seed階層CI は `[0.498378, 0.500203]` で `0.5` を含む。seed間のばらつきを保つ見方では、13 rounds は baseline `0.5` と矛盾しにくい。

今回の条件では、12から13 rounds の間が avalanche mean の主な境界という Issue #9 の解釈を補強する。ただし、13 rounds の差分は小さく、CI手法によって baseline の含み方が変わるため、厳密な閾値としては扱わない。

## Limitations

- seeds は `1..5` の5個だけ。
- bootstrap は探索的な区間推定であり、同一seed内のサンプルを完全に独立な母集団として扱えるとは限らない。
- 13 rounds の per-sample CI は `0.5` をごくわずかに下回るため、丸めや追加seedで判断が変わる可能性がある。
- aggregate mean のCIだけを扱い、bit位置ごとの偏りや distinguisher との対応は評価していない。

## Next

- 9から15 rounds の bit位置別 flip rate を測定し、aggregate mean では見えない偏りが残るか確認する: #36
- 9から15 rounds の distinguisher baseline と比較し、avalanche の境界と識別困難性の境界が一致するか確認する: #19
