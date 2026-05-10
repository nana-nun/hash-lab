# Avalanche / Distinguisher round別比較

## Question

`mini-sha` の avalanche metrics と logistic regression distinguisher metrics は、round数に沿って同じ傾向を示すか。特に aggregate avalanche が `0.5` 付近に見えるroundで、distinguisher が random guess baseline を超えるか確認する。

## Hypothesis

aggregate avalanche mean が `0.5` に近いroundほど、distinguisher の `test_accuracy - 0.5` も小さくなる。ただし、bit位置ごとの偏りが残るroundでは、aggregate mean だけでは説明できない差が出る可能性がある。

## Setup

- Command: `$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -c "<inline script>"`
- Hash / rounds: `mini-sha` / `2, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 32`
- Avalanche sources:
  - `results/2026-05-09-avalanche-mini-sha-multi-seed/aggregate_metrics.csv`
  - `results/2026-05-10-avalanche-mini-sha-rounds-9-15/aggregate_metrics.csv`
- Bit-position sources:
  - `results/2026-05-10-avalanche-mini-sha-bit-positions/round_summary.csv`
  - `results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/round_summary.csv`
  - `results/2026-05-10-avalanche-mini-sha-bit-ci/round_summary.csv`
  - `results/2026-05-10-avalanche-mini-sha-bit-ci-9-15/round_summary.csv`
- Distinguisher source: `results/2026-05-09-distinguish-baseline-multi-seed/aggregate_metrics.csv`
- Distinguisher condition: seeds `1..5`、`1000 samples/class`、`epochs=8`、logistic regression

## Baseline

- avalanche aggregate mean: `0.5`
- output bit position flip rate: `0.5`
- distinguisher random guess accuracy: `0.5`

## Result

横比較は `round_comparison.csv` に保存した。

| rounds | avalanche mean | avalanche delta | max bit delta | Holm reject bits | distinguisher test delta |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.0142 | -0.4858 | 0.5000 | 256 | 0.4975 |
| 4 | 0.0834 | -0.4166 | 0.4967 | 256 | 0.0045 |
| 8 | 0.3259 | -0.1741 | 0.2951 | 256 | 0.0055 |
| 12 | 0.493620 | -0.006380 | 0.046000 | 35 | 未測定 |
| 13 | 0.499301 | -0.000699 | 0.021600 | 1 | 未測定 |
| 14 | 0.499936 | -0.000064 | 0.015000 | 0 | 未測定 |
| 15 | 0.499847 | -0.000153 | 0.014600 | 0 | 未測定 |
| 16 | 0.5001 | 0.0001 | 0.0121 | 0 | -0.0125 |
| 32 | 0.4999 | -0.0001 | 0.0166 | 0 | 未測定 |

2 rounds は avalanche mean が baseline から大きく離れ、distinguisher も `test_accuracy_minus_baseline=0.4975` で強く識別できた。

4/8 rounds は avalanche と bit位置指標では強い偏りが残ったが、logistic regression distinguisher の test delta は `0.0045` / `0.0055` で random guess 付近だった。train accuracy はそれぞれ `0.6054` / `0.5910` まで上がっているため、train split に合わせた重みは作れているが、test split に汎化する識別信号は見えていない。

16 rounds は aggregate avalanche、bit位置の Holm補正、distinguisher のすべてで baseline 付近だった。`test_accuracy_minus_baseline=-0.0125` は seed間ばらつきの範囲内に見える。

9-15 rounds は avalanche / bit-position 側だけが揃っている。12 rounds は aggregate mean が `0.493620` まで近づく一方、Holm補正後も `35` bit が baseline `0.5` と矛盾する。13 rounds は aggregate mean が `0.499301` で、Holm reject count は `1` まで減るが、bit255 の残差偏りが後続Issueで確認されている。

## Interpretation

aggregate avalanche が悪い 2 rounds では、distinguisher も強く識別できた。一方、4/8 rounds では aggregate avalanche と bit位置偏りが明確に悪くても、今回の logistic regression は test split で baseline を超えなかった。

この結果は、avalanche metrics と logistic regression distinguisher が同じ性質を測っているわけではないことを示す。avalanche は入力bit反転に対する出力変化を測り、現在の distinguisher は digest とランダムbit列の線形分離を測る。4/8 rounds の偏りは avalanche 上は大きいが、今回の特徴量とモデルでは汎化する識別器として使えていない。

16 rounds 以降は、少なくとも既存の aggregate avalanche、bit位置CI、logistic regression baseline では random-like baseline 付近に見える。ただし 13 rounds の bit255 のような局所的な残差偏りは、aggregate mean だけでは見落とす。

## Limitations

- Distinguisher は `2, 4, 8, 16` rounds だけで、`9..15` rounds と `32` rounds は未測定。
- Distinguisher は logistic regression のみで、MLPなど容量の大きいモデルでは未確認。
- Distinguisher の信頼区間は未計算。seed数も `1..5` に限られる。
- Avalanche は `2000 samples/seed`、distinguisher は `1000 samples/class/seed` で、dataset size が完全には揃っていない。
- 横比較は相関の探索であり、因果や安全性の主張ではない。

## Next

- `9..15` rounds と `32` rounds の logistic regression distinguisher を測定し、avalanche境界と同じround軸で比較する: #53
- `test_accuracy_minus_baseline` の信頼区間を計算する: #50
- MLP distinguisher を logistic regression baseline と比較する: #51
