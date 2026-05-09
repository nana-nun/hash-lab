# Distinguisher Baseline 複数seed確認

## Question

`mini-sha` の出力とランダムbit列を識別する logistic regression 実験で、`test_accuracy - 0.5` は seed を変えても round ごとに同じ傾向を示すか。

## Hypothesis

2 rounds は random guess baseline を大きく上回る。4 rounds 以降は複数seed平均でも `test_accuracy - 0.5` が 0 付近に留まる。

## Setup

- Command: `.\.venv\Scripts\python.exe -c "<inline script>"`
- Executed at: `2026-05-09T22:22:46+09:00`
- Seeds: `1, 2, 3, 4, 5`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16`
- Dataset size: 各seed・各roundにつき hash出力 `1000` 件、ランダムbit列 `1000` 件、合計 `2000` 件
- Model config: logistic regression、`epochs=8`、`learning_rate=0.08`、256 bit features

## Baseline

- random guess baseline: `0.5`
- majority baseline: shuffle後のtest splitのラベル分布から seed ごとに算出。今回の範囲では `0.5025` から `0.5225`。

Issue #2 の single-seed 結果は seed `1`、`samples=1000`、`epochs=8` で以下だった。

| rounds | train_accuracy | test_accuracy | test_accuracy_minus_baseline |
| ---: | ---: | ---: | ---: |
| 2 | 1.0000 | 1.0000 | 0.5000 |
| 4 | 0.6175 | 0.4975 | -0.0025 |
| 8 | 0.5919 | 0.4925 | -0.0075 |
| 16 | 0.6100 | 0.4900 | -0.0100 |

## Result

seed別の結果は `seed_metrics.csv`、round別の集約結果は `aggregate_metrics.csv` に保存した。

| rounds | seeds | samples/seed | mean_train_accuracy | mean_test_accuracy | mean_test_accuracy_minus_baseline | stdev_test_accuracy_minus_baseline | min | max | mean_train_test_gap |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 5 | 1000 | 1.0000 | 0.9975 | 0.4975 | 0.0016 | 0.4950 | 0.5000 | 0.0025 |
| 4 | 5 | 1000 | 0.6054 | 0.5045 | 0.0045 | 0.0263 | -0.0425 | 0.0350 | 0.1009 |
| 8 | 5 | 1000 | 0.5910 | 0.5055 | 0.0055 | 0.0246 | -0.0225 | 0.0375 | 0.0855 |
| 16 | 5 | 1000 | 0.5923 | 0.4875 | -0.0125 | 0.0284 | -0.0675 | 0.0100 | 0.1048 |

## Interpretation

2 rounds は全seedで `test_accuracy` がほぼ 1.0 になり、logistic regression が明確に識別できた。

4/8/16 rounds は、平均の `test_accuracy_minus_baseline` がそれぞれ `0.0045`、`0.0055`、`-0.0125` で、random guess baseline の近くに留まった。seed別には 4 rounds で `-0.0425` から `0.0350`、8 rounds で `-0.0225` から `0.0375`、16 rounds で `-0.0675` から `0.0100` の範囲に散らばっている。

一方で 4/8/16 rounds の `train_accuracy` は平均で `0.59` から `0.61` 程度まで上がり、`mean_train_test_gap` も `0.0855` から `0.1048` ある。今回の条件では、train split に合わせた重みは作れているが、test split へ一般化する識別信号は確認できない。

## Limitations

- seed は `1..5` の5個だけで、信頼区間や有意性検定は未実施。
- dataset size は各seed・各round `1000 samples/class`、epochs は `8` に固定した。
- logistic regression のみを見ており、MLPなど別モデルでは未確認。
- majority baseline との差分ではなく、Issue #2 と同じ random guess baseline `0.5` との差分を主指標にした。

## Next

- dataset size と epochs を変えた感度を測定する: #18
- 4/8/16 rounds について、より多いseedまたは信頼区間で random guess 近傍かを確認する。
