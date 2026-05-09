# mini-sha Avalanche 9-15 rounds 中間領域測定

## Question

`mini-sha` の avalanche effect は、8 rounds から16 rounds の間のどのround付近で mean flip ratio `0.5` に近づくか。

## Hypothesis

round数を9から15へ増やすにつれて mean flip ratio は単調または概ね単調に `0.5` へ近づく。

## Setup

- Command: `@'<inline script>'@ | .\.venv\Scripts\python.exe -`
- Executed at: `2026-05-10T02:03:58+09:00`
- Hash / rounds: `mini-sha` / `9, 10, 11, 12, 13, 14, 15`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`
- Model config: none

保存ファイル:

- `seed_metrics.csv`: seed別の `mean / stdev / min / max / baseline_delta`。
- `aggregate_metrics.csv`: round別の seed mean 集約。
- `config.json`: 実行条件。

## Baseline

Issue #7 の複数seed結果を baseline として参照した。

| rounds | Issue #7 mean_of_means |
| ---: | ---: |
| 8 | 0.3259 |
| 16 | 0.5001 |

理想的な random-like avalanche の期待値は mean flip ratio `0.5`。

## Result

詳細なCSVは `seed_metrics.csv` と `aggregate_metrics.csv` に保存した。

| rounds | seeds | samples/seed | mean_of_means | stdev_of_means | min_mean | max_mean | baseline_delta |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 5 | 2000 | 0.386652 | 0.003911 | 0.379207 | 0.390504 | -0.113348 |
| 10 | 5 | 2000 | 0.437913 | 0.002321 | 0.433549 | 0.440521 | -0.062087 |
| 11 | 5 | 2000 | 0.473403 | 0.001123 | 0.471207 | 0.474334 | -0.026597 |
| 12 | 5 | 2000 | 0.493620 | 0.000435 | 0.493133 | 0.494291 | -0.006380 |
| 13 | 5 | 2000 | 0.499301 | 0.000731 | 0.498332 | 0.500178 | -0.000699 |
| 14 | 5 | 2000 | 0.499936 | 0.000168 | 0.499670 | 0.500127 | -0.000064 |
| 15 | 5 | 2000 | 0.499847 | 0.000735 | 0.498756 | 0.500764 | -0.000153 |

## Interpretation

9から12 rounds では、round数が増えるにつれて mean flip ratio が大きく上がり、baseline `0.5` との差が縮んだ。今回の条件では、8 rounds の `0.3259` から 12 rounds の `0.493620` までが主な遷移領域に見える。

13/14/15 rounds は mean_of_means が `0.5` に非常に近い。特に13 rounds で `0.499301` まで到達し、14/15 rounds でもほぼ同じ水準に留まった。今回の aggregate mean だけを見る限り、`0.5` 付近への境界は 12から13 rounds の間にある可能性が高い。

ただし、これは aggregate mean flip ratio の結果であり、bit位置ごとの小さな偏り、per-sample CI、seed階層CI、distinguisher との対応まではこの実験だけでは判断しない。

## Limitations

- seeds は `1..5` の5個だけ。
- 各seed・各round `2000 samples` であり、13 rounds 以降の小さな差分には追加の不確実性評価が必要。
- aggregate mean のみを扱い、bit位置ごとの偏りや BIC 風指標は評価していない。
- avalanche が `0.5` 付近でも、distinguisher が同じroundで baseline 付近になるとは限らない。

## Next

- 12/13 rounds 周辺で per-sample bootstrap CI または seed階層bootstrap CI を計算し、`0.5` 付近への境界を不確実性込みで確認する: #35
- 9から15 rounds の bit位置別 flip rate を測定し、aggregate mean では見えない偏りが残るか確認する: #36
- 9から15 rounds の distinguisher baseline と比較し、avalanche の境界と識別困難性の境界が一致するか確認する: #19
