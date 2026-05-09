# mini-sha Avalanche Seed階層 Bootstrap CI

## Question

`mini-sha` の per-sample flip ratio に対して seed階層を保つ bootstrap confidence interval を計算すると、per-sample bootstrap CI と比べて round別 mean flip ratio の解釈は変わるか。

## Hypothesis

16/32 rounds は seed階層を保つ bootstrap でも baseline `0.5` を含む。一方、2/4/8 rounds は baseline `0.5` から明確に離れる。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-seed-bootstrap --rounds 2 4 8 16 32 --samples-input results/2026-05-10-avalanche-mini-sha-bootstrap/per_sample_flip_ratios.csv --per-sample-metrics results/2026-05-10-avalanche-mini-sha-bootstrap/bootstrap_metrics.csv --bootstrap-iterations 2000 --bootstrap-seed 20260510 --summary-output results/2026-05-10-avalanche-mini-sha-seed-bootstrap/seed_bootstrap_metrics.csv`
- Executed at: `2026-05-10T00:58:57+09:00`
- Input: `results/2026-05-10-avalanche-mini-sha-bootstrap/per_sample_flip_ratios.csv`
- Comparison input: `results/2026-05-10-avalanche-mini-sha-bootstrap/bootstrap_metrics.csv`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16, 32`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`、roundごとに合計 `10000` per-sample ratios
- Bootstrap: seedを復元抽出し、選ばれたseed内でsampleも復元抽出する hierarchical percentile bootstrap、`2000` iterations、seed base `20260510`
- Model config: none

保存ファイル:

- `seed_bootstrap_metrics.csv`: round別 mean、seed階層bootstrap 95% CI、per-sample bootstrap CI との差分。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として mean flip ratio `0.5` を baseline にした。

比較対象は Issue #22 の per-sample bootstrap CI。Issue #22 は round内の全 per-sample ratio を直接再標本化した。今回の方法は seedを先に再標本化し、そのseed内のsampleを再標本化することで seed間のばらつきを区間に反映しやすくした。

## Result

詳細なCSVは `seed_bootstrap_metrics.csv` に保存した。

| rounds | mean | seed階層 bootstrap 95% CI | per-sample bootstrap 95% CI | baseline_delta | delta 95% CI | includes 0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2 | 0.014161 | [0.013137, 0.015133] | [0.013515, 0.014802] | -0.485839 | [-0.486863, -0.484867] | no |
| 4 | 0.083370 | [0.079825, 0.086706] | [0.080976, 0.085898] | -0.416630 | [-0.420175, -0.413294] | no |
| 8 | 0.325878 | [0.320520, 0.331128] | [0.322394, 0.329630] | -0.174122 | [-0.179480, -0.168872] | no |
| 16 | 0.500120 | [0.499178, 0.500965] | [0.499486, 0.500725] | 0.000120 | [-0.000822, 0.000965] | yes |
| 32 | 0.499881 | [0.499159, 0.500614] | [0.499309, 0.500491] | -0.000119 | [-0.000841, 0.000614] | yes |

## Interpretation

seed階層bootstrapでも、2/4/8 rounds の 95% CI は baseline `0.5` を含まない。したがって、8 rounds 以下が random-like avalanche に達していないという解釈は per-sample bootstrap より保守的な見方でも変わらない。

16/32 rounds の 95% CI は baseline `0.5` を含む。今回の条件では、seed階層を保っても 16 rounds 以上は baseline `0.5` と矛盾しにくい。

per-sample bootstrap と比べると、seed階層bootstrap の区間は多くのroundで少し広い。これは seed間の mean の違いを再標本化に含めたためと解釈できる。ただし seed数は5個だけなので、seed階層の区間も探索的な不確実性指標に留める。

## Limitations

- seeds は `1..5` の5個だけで、seed階層の分布を安定して推定するには少ない。
- seed内sample数は `2000` だが、seed抽出単位は5点しかない。
- bootstrap iterations は `2000` で、より精密な尾部推定は未確認。
- round 9から15の境界領域は含めていない。
- 出力bit位置ごとの偏りや bit independence は評価していない。

## Next

- 16/32 rounds について seed数を増やし、seed階層bootstrap CI が baseline `0.5` を含むか確認する: #31
- round 9から15の中間領域を測定し、`0.5` 付近へ移る境界を細かく見る: #9
- 出力bit位置ごとの flip rate を保存し、特定bitに偏りが残るか確認する: #8
