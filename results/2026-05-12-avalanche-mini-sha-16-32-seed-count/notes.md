# mini-sha 16/32 rounds seed数追加 seed階層CI

## Question

`mini-sha` 16/32 rounds の mean flip ratio は、seed数を `1..20` に増やしても baseline `0.5` 付近に留まるか。

## Hypothesis

seed数を増やしても 16/32 rounds の mean flip ratio は baseline `0.5` 付近に留まり、seed階層bootstrap CI は baseline `0.5` を含む。

## Setup

- Command 1: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bootstrap --rounds 16 32 --samples 2000 --seeds 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 --samples-output results/2026-05-12-avalanche-mini-sha-16-32-seed-count/per_sample_flip_ratios.csv --summary-output results/2026-05-12-avalanche-mini-sha-16-32-seed-count/per_sample_bootstrap_metrics.csv --bootstrap-iterations 2000 --bootstrap-seed 20260512`
- Command 2: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-seed-bootstrap --rounds 16 32 --samples-input results/2026-05-12-avalanche-mini-sha-16-32-seed-count/per_sample_flip_ratios.csv --per-sample-metrics results/2026-05-12-avalanche-mini-sha-16-32-seed-count/per_sample_bootstrap_metrics.csv --summary-output results/2026-05-12-avalanche-mini-sha-16-32-seed-count/seed_bootstrap_metrics.csv --bootstrap-iterations 2000 --bootstrap-seed 20260512`
- Executed at: `2026-05-12T15:38:05+09:00`
- Hash / rounds: `mini-sha` / `16, 32`
- Seeds: `1..20`
- Dataset size: 各seed・各round `2000 samples`、roundごとに合計 `40000` per-sample ratios
- Bootstrap: seedを復元抽出し、選ばれたseed内でsampleも復元抽出する hierarchical percentile bootstrap、`2000` iterations
- Model config: none

保存ファイル:

- `per_sample_flip_ratios.csv`: seed別・sample別の flip ratio。
- `per_sample_bootstrap_metrics.csv`: per-sample bootstrap CI。
- `seed_bootstrap_metrics.csv`: seed階層bootstrap CI と per-sample CI との差分。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として mean flip ratio `0.5` を baseline にした。

比較対象は Issue #29 の seeds `1..5`、各seed・各round `2000 samples` の seed階層bootstrap CI。

## Result

seed数を `1..20` に増やしても、16/32 rounds の seed階層bootstrap 95% CI は baseline `0.5` を含んだ。

| rounds | seeds | total_samples | mean | seed階層 bootstrap 95% CI | baseline_delta | delta 95% CI | includes 0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 16 | 20 | 40000 | 0.500182 | `[0.499729, 0.500629]` | 0.000182 | `[-0.000271, 0.000629]` | yes |
| 32 | 20 | 40000 | 0.500040 | `[0.499645, 0.500437]` | 0.000040 | `[-0.000355, 0.000437]` | yes |

Issue #29 との比較:

| rounds | seeds | mean | seed階層 bootstrap 95% CI | includes 0.5 |
| ---: | ---: | ---: | ---: | :--- |
| 16 | 5 | 0.500120 | `[0.499178, 0.500965]` | yes |
| 16 | 20 | 0.500182 | `[0.499729, 0.500629]` | yes |
| 32 | 5 | 0.499881 | `[0.499159, 0.500614]` | yes |
| 32 | 20 | 0.500040 | `[0.499645, 0.500437]` | yes |

per-sample bootstrap との比較:

| rounds | seed階層 CI | per-sample CI | seed CI low - per-sample low | seed CI high - per-sample high |
| ---: | ---: | ---: | ---: | ---: |
| 16 | `[0.499729, 0.500629]` | `[0.499889, 0.500488]` | -0.000160 | 0.000141 |
| 32 | `[0.499645, 0.500437]` | `[0.499753, 0.500340]` | -0.000108 | 0.000097 |

## Interpretation

仮説は支持された。seeds `1..20` に増やしても、16/32 rounds の mean flip ratio は baseline `0.5` 付近に留まり、seed階層bootstrap CI は baseline `0.5` を含んだ。

Issue #29 の seeds `1..5` と比べると、CI は少し狭くなった。16 rounds は `[0.499178, 0.500965]` から `[0.499729, 0.500629]`、32 rounds は `[0.499159, 0.500614]` から `[0.499645, 0.500437]` になった。seed数を増やしても解釈は変わらず、16/32 rounds の aggregate mean は今回の条件では random-like avalanche baseline と矛盾しにくい。

ただし、aggregate mean が `0.5` 付近であることは、出力bit位置ごとの偏りや bit independence を保証しない。実際に 13 rounds では局所的な bit偏りが残っているため、16/32 rounds についても必要なら bit位置別や BIC 風指標で別途確認する。

## Limitations

- seeds は `1..20` の連番で、より広い seed範囲では結果が変わる可能性がある。
- bootstrap iterations は Issue #29 と同じ `2000` で、尾部の精密推定には限界がある。
- aggregate mean flip ratio だけを見ており、出力bit位置別偏りや bit間相関は評価していない。
- `mini-sha` toy hash の reduced-round 結果であり、実運用SHA-256の安全性を主張するものではない。

## Next

- #56 で BIC と bit間相関の測定方法を整理する。
- 必要なら 16/32 rounds でも seed数を増やした bit位置別CIを測り、aggregate mean では見えない小さな偏りを確認する。
