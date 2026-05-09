# Results Index

このディレクトリは、保存済み実験結果の索引です。AIエージェントは新しい分析を始める前に、このファイルと該当する `notes.md`、metrics CSV/JSON、`docs/research-state.md` を確認してください。

## Experiments

| Directory | Type | Key Files | Summary |
| --- | --- | --- | --- |
| `2026-05-09-avalanche-mini-sha/` | avalanche | `metrics.csv`, `notes.md` | `mini-sha` の single-seed avalanche 初期測定。round 数が増えるほど mean flip ratio が `0.5` に近づく傾向を確認。 |
| `2026-05-09-avalanche-mini-sha-multi-seed/` | avalanche | `seed_metrics.csv`, `aggregate_metrics.csv`, `notes.md` | seeds `1..5`、各round `2000 samples`。16/32 rounds は複数seedでも `0.5` 付近。 |
| `2026-05-10-avalanche-mini-sha-rounds-9-15/` | avalanche | `seed_metrics.csv`, `aggregate_metrics.csv`, `config.json`, `notes.md` | 9-15 rounds の中間領域を測定。12 rounds は `0.493620`、13 rounds 以降は `0.5` 付近で、主な境界は12から13 rounds の間に見える。 |
| `2026-05-09-avalanche-mini-sha-uncertainty/` | avalanche uncertainty | `uncertainty_metrics.csv`, `config.json`, `notes.md` | seed mean から標準誤差と簡易95% t区間を計算。2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-10-avalanche-mini-sha-bootstrap/` | avalanche uncertainty | `per_sample_flip_ratios.csv`, `bootstrap_metrics.csv`, `config.json`, `notes.md` | per-sample flip ratio を保存し、percentile bootstrap 95% CI を計算。2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-10-avalanche-mini-sha-bit-positions/` | avalanche bit positions | `bit_metrics.csv`, `round_summary.csv`, `config.json`, `notes.md` | 出力bit位置ごとの flip rate を測定。2/4/8 rounds はbit別にも大きく偏り、16/32 rounds は aggregate min/max も `0.5` 付近。 |
| `2026-05-10-avalanche-mini-sha-seed-bootstrap/` | avalanche uncertainty | `seed_bootstrap_metrics.csv`, `config.json`, `notes.md` | seed階層を保つ percentile bootstrap 95% CI を計算。per-sample bootstrap より少し広いが、2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-09-distinguish-baseline/` | distinguisher | `metrics.csv`, `config.json`, `notes.md` | logistic regression の seed `1` baseline。2 rounds は識別可能、4/8/16 rounds は random guess 付近。 |
| `2026-05-09-distinguish-baseline-multi-seed/` | distinguisher | `seed_metrics.csv`, `aggregate_metrics.csv`, `config.json`, `notes.md` | seeds `1..5` の distinguisher baseline。2 rounds は強く識別可能、4/8/16 rounds は平均で baseline 付近。 |

## Reading Order

実験結果を解釈するときは、次の順で読む。

1. `docs/research-state.md`
2. この `results/README.md`
3. 該当する `results/<experiment>/notes.md`
4. 該当する metrics CSV/JSON
5. `references/notes/avalanche-neural-distinguisher-survey.md`

## Interpretation Rules

- `0.5` 付近という表現は、対象metric、seed数、samples、区間推定の方法を一緒に確認してから使う。
- single-seed の結果だけで安定性を主張しない。
- train accuracy と test accuracy を混同しない。
- neural/ML 実験では random guess、majority baseline、単純統計量との差を記録する。
- `Limitations` と `Next` は、既存Issueで covered されているか確認する。
