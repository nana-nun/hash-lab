# Distinguisher 9-15 / 32 rounds 測定

## Question

`mini-sha` の logistic regression distinguisher は、avalanche 境界として見ている 9..15 rounds と 32 rounds でも random guess baseline 付近に留まるか。

## Hypothesis

9..15 rounds と 32 rounds の `test_accuracy_minus_baseline` は、既存の 4/8/16 rounds と同じく `0` 付近に留まる。特に 12/13 rounds 周辺で avalanche 指標に差が残っていても、線形distinguisherの test accuracy が安定して baseline を上回るとは限らない。

## Setup

- Command: `.\.venv\Scripts\python.exe results\2026-05-16-distinguish-9-15-32\run_experiment.py`
- Comparison command: `.\.venv\Scripts\python.exe results\2026-05-16-distinguish-9-15-32\compare_with_avalanche.py`
- Executed at: `2026-05-16T20:52:43+09:00`
- Seeds: `1, 2, 3, 4, 5`
- Hash / rounds: `mini-sha` / `9, 10, 11, 12, 13, 14, 15, 32`
- Dataset size: 各seed・各roundにつき hash出力 `2000` 件、同数のランダムbit列
- Model config: logistic regression、`learning_rate=0.08`、256 bit features、train split `0.8`
- Epochs: `8`
- CI: seed別 `test_accuracy_minus_baseline` の percentile bootstrap 95% CI、`2000` iterations

## Baseline

- random guess baseline: `0.5`
- majority baseline: shuffle後のtest splitのラベル分布から seed ごとに算出。今回の平均は各roundで `0.5115`。

比較対象として、Issue #18 の `samples=2000`, `epochs=8` では、4/8/16 rounds の平均 `test_accuracy_minus_baseline` はそれぞれ `0.0007`, `0.0013`, `-0.0118` だった。

## Result

seed別の結果は `seed_metrics.csv`、round別集約は `aggregate_metrics.csv`、既存avalanche指標との横比較は `round_comparison.csv` に保存した。

| rounds | mean_test_accuracy | mean delta | 95% CI | contains 0 |
| ---: | ---: | ---: | ---: | :--- |
| 9 | 0.4995 | -0.0005 | `[-0.0117, 0.0135]` | yes |
| 10 | 0.5033 | 0.0033 | `[-0.0162, 0.0228]` | yes |
| 11 | 0.4910 | -0.0090 | `[-0.0268, 0.0040]` | yes |
| 12 | 0.4998 | -0.0002 | `[-0.0062, 0.0055]` | yes |
| 13 | 0.5018 | 0.0018 | `[-0.0105, 0.0128]` | yes |
| 14 | 0.5008 | 0.0008 | `[-0.0237, 0.0235]` | yes |
| 15 | 0.4903 | -0.0097 | `[-0.0252, 0.0053]` | yes |
| 32 | 0.5103 | 0.0103 | `[0.0003, 0.0203]` | no |

avalanche / SAC風指標との比較:

| rounds | avalanche mean | SAC Holm reject count | distinguisher delta |
| ---: | ---: | ---: | ---: |
| 9 | 0.386652 | 234 | -0.0005 |
| 10 | 0.437913 | 167 | 0.0033 |
| 11 | 0.473403 | 97 | -0.0090 |
| 12 | 0.493620 | 35 | -0.0002 |
| 13 | 0.499301 | 1 | 0.0018 |
| 14 | 0.499936 | 0 | 0.0008 |
| 15 | 0.499847 | 0 | -0.0097 |
| 32 | 0.499900 | 0 | 0.0103 |

## Interpretation

9..15 rounds では仮説と一致し、logistic regression の `test_accuracy_minus_baseline` は seed階層bootstrap CIで `0` を含んだ。9/10/11/12 rounds は avalanche mean や出力bit別SAC風指標ではまだ偏りが大きいが、今回の digest-vs-random-bit列 logistic regression では test split に一般化する識別信号としては見えなかった。

12/13 rounds 周辺では、avalanche 側の境界と logistic regression 側の境界は一致しない。12 rounds は avalanche mean が `0.493620`、SAC Holm reject count が `35` だが、distinguisher delta は `-0.0002` だった。13 rounds も local な bit偏り候補は残るが、線形distinguisherは baseline 付近に留まった。

32 rounds は平均deltaが `0.0103` で、今回の seed階層bootstrap CIは `0` を含まなかった。ただし seedは5個だけで、固定されたtrain/test split設計と同じハイパーパラメータの単発gridで見た小さな正方向差分なので、「32 rounds が識別可能」とはまだ扱わない。16 rounds の既存CIでは正方向の安定した差分は見えておらず、32 rounds だけを追加seedや複数splitで再確認する必要がある。

## Limitations

- seed は `1..5` の5個だけ。
- train/test split は各seedで1回だけで、split単位のばらつきは見ていない。
- logistic regression のみで、MLPやCNN、差分ペア型distinguisherは未確認。
- digest列 vs random bit列の分類であり、Gohr系の fixed input difference pair task とは異なる。
- 32 rounds の小さな正方向差分は探索的な観察であり、追加seedや複数splitなしに強い主張へ使わない。

## Next

- 32 rounds の小さな正方向deltaを、追加seedsと複数train/test splitで再測定する: #104
- #51 / #87 で容量の大きいモデルと比較するときは、今回の logistic regression 結果を baseline として使う。
- #89 / #88 の差分ペア型実験では、今回の digest-vs-random-bit列実験とタスク設計が違うことを明記する。
