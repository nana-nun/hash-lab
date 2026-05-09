# mini-sha Avalanche Per-sample Bootstrap CI

## Question

`mini-sha` の per-sample flip ratio を保存して bootstrap confidence interval を計算すると、round別 mean flip ratio は baseline `0.5` に対してどう見えるか。

## Hypothesis

16/32 rounds は per-sample bootstrap CI でも mean flip ratio が `0.5` 付近に留まる。一方、8 rounds 以下は `0.5` から明確に離れる。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bootstrap --rounds 2 4 8 16 32 --samples 2000 --seeds 1 2 3 4 5 --bootstrap-iterations 2000 --bootstrap-seed 20260510 --samples-output results/2026-05-10-avalanche-mini-sha-bootstrap/per_sample_flip_ratios.csv --summary-output results/2026-05-10-avalanche-mini-sha-bootstrap/bootstrap_metrics.csv`
- Executed at: `2026-05-10T00:31:50+09:00`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16, 32`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`、roundごとに合計 `10000` per-sample ratios
- Bootstrap: percentile bootstrap、`2000` iterations、seed base `20260510`
- Model config: none

保存ファイル:

- `per_sample_flip_ratios.csv`: `rounds, seed, sample_index, flip_ratio` を保存した per-sample データ。
- `bootstrap_metrics.csv`: round別 mean、bootstrap 95% CI、baselineとの差分。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として mean flip ratio `0.5` を baseline にした。

比較対象として、Issue #20 の `results/2026-05-09-avalanche-mini-sha-uncertainty/uncertainty_metrics.csv` にある seed mean 5点からの簡易95% t区間も参照した。

## Result

詳細なCSVは `bootstrap_metrics.csv` に保存した。

| rounds | mean | per-sample bootstrap 95% CI | baseline_delta | delta 95% CI | includes 0.5 | Issue #20 t 95% CI |
| ---: | ---: | ---: | ---: | ---: | :--- | :--- |
| 2 | 0.014161 | [0.013515, 0.014802] | -0.485839 | [-0.486485, -0.485198] | no | [0.012977, 0.015303] |
| 4 | 0.083370 | [0.080976, 0.085898] | -0.416630 | [-0.419024, -0.414102] | no | [0.079461, 0.087259] |
| 8 | 0.325878 | [0.322394, 0.329630] | -0.174122 | [-0.177606, -0.170370] | no | [0.319224, 0.332536] |
| 16 | 0.500120 | [0.499486, 0.500725] | 0.000120 | [-0.000514, 0.000725] | yes | [0.499047, 0.501193] |
| 32 | 0.499881 | [0.499309, 0.500491] | -0.000119 | [-0.000691, 0.000491] | yes | [0.499232, 0.500528] |

## Interpretation

2/4/8 rounds は per-sample bootstrap 95% CI でも baseline `0.5` を含まない。今回の条件では、8 rounds 以下は random-like avalanche に達していないという既存解釈を補強する。

16/32 rounds は per-sample bootstrap 95% CI が baseline `0.5` を含む。seed mean だけを使った Issue #20 の簡易 t区間と同じ方向であり、今回の測定条件では 16 rounds 以上が `0.5` 付近に留まるという見方と矛盾しにくい。

Issue #20 の t区間との違いは、区間推定の単位にある。Issue #20 は seedごとの mean 5点から seed間のばらつきを見た。今回の bootstrap は全 per-sample ratio を再標本化しており、入力サンプル単位の分布を直接使っている。ただし、同一seed内のサンプルや固定されたハッシュ構造を完全に独立な母集団として扱えるとは限らないため、厳密な統計検定ではなく探索的な不確実性指標として読む。

## Limitations

- seeds は `1..5` の5個だけ。
- roundごとに全seedの per-sample ratio をまとめて bootstrap しており、seed階層を明示した hierarchical bootstrap ではない。
- bootstrap iterations は `2000` で、より精密な尾部推定は未確認。
- round 9から15の境界領域は含めていない。
- 出力bit位置ごとの偏りや bit independence は評価していない。

## Next

- round 9から15の中間領域を測定し、`0.5` 付近へ移る境界を細かく見る: #9
- 出力bit位置ごとの flip rate を保存し、特定bitに偏りが残るか確認する: #8
- seed階層を保つ hierarchical bootstrap または seed-stratified bootstrap を追加し、per-sample bootstrap と比較する: #29
