# Distinguisher dataset size / epochs 感度測定

## Question

`mini-sha` の logistic regression distinguisher で、dataset size と epochs を変えても `test_accuracy - 0.5` は random guess baseline 付近に留まるか。

## Hypothesis

4/8/16 rounds では dataset size や epochs を増やしても `test_accuracy - 0.5` は 0 付近に留まる。2 rounds は設定に関係なく baseline を大きく上回る。

## Setup

- Command: `.\.venv\Scripts\python.exe -c "<inline script>"`
- Executed at: `2026-05-10T21:00:25+09:00`
- Seeds: `1, 2, 3, 4, 5`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16`
- Dataset size: 各seed・各roundにつき hash出力 `500, 1000, 2000` 件、同数のランダムbit列
- Model config: logistic regression、`learning_rate=0.08`、256 bit features、train split `0.8`
- Epochs: `4, 8, 16`

## Baseline

- random guess baseline: `0.5`
- majority baseline: shuffle後のtest splitのラベル分布から seed ごとに算出。

Issue #15 の比較対象は seeds `1..5`、`samples=1000`、`epochs=8` で、4/8/16 rounds の平均 `test_accuracy_minus_baseline` はそれぞれ `0.0045`、`0.0055`、`-0.0125` だった。

## Result

seed別の結果は `seed_metrics.csv`、round / samples / epochs 別の集約結果は `aggregate_metrics.csv` に保存した。

2 rounds は全条件で明確に識別できた。`samples=2000` では epochs `4, 8, 16` の平均 `test_accuracy_minus_baseline` がそれぞれ `0.4995`、`0.4995`、`0.5000` だった。

4/8/16 rounds は、今回のgridでは平均 `test_accuracy_minus_baseline` がすべて `-0.0160` から `0.0110` の範囲に留まった。最大の正方向平均は 4 rounds / samples `500` / epochs `16` の `0.0110`、最大の負方向平均は 8 rounds / samples `500` / epochs `4` の `-0.0160` だった。

`samples=2000` では seed間のばらつきもやや小さくなった。

| rounds | samples | epochs | mean_test_accuracy_minus_baseline | stdev | mean_train_test_gap |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 2000 | 4 | -0.0040 | 0.0157 | 0.0474 |
| 8 | 2000 | 4 | 0.0007 | 0.0203 | 0.0405 |
| 16 | 2000 | 4 | -0.0065 | 0.0163 | 0.0616 |
| 4 | 2000 | 8 | 0.0007 | 0.0140 | 0.0467 |
| 8 | 2000 | 8 | 0.0013 | 0.0181 | 0.0435 |
| 16 | 2000 | 8 | -0.0118 | 0.0209 | 0.0660 |
| 4 | 2000 | 16 | 0.0028 | 0.0116 | 0.0434 |
| 8 | 2000 | 16 | 0.0048 | 0.0210 | 0.0406 |
| 16 | 2000 | 16 | -0.0010 | 0.0126 | 0.0518 |

`samples=500` では train accuracy が `0.67` から `0.71` 程度まで上がる一方、test accuracy は random guess 付近だった。`samples=1000` と `samples=2000` では train accuracy 自体が下がり、train-test gap も小さくなった。

## Interpretation

今回の条件では、2 rounds は logistic regression で安定して識別できる。これは Issue #2 と Issue #15 の結果と一致する。

4/8/16 rounds は、dataset size を `500` から `2000`、epochs を `4` から `16` に変えても、平均 `test_accuracy - 0.5` は 0 付近に留まった。epochs を増やしても test 側の差分が一貫して大きくなる傾向は見えない。

`samples=500` では train-test gap が `0.17` から `0.21` 程度あり、train split に合わせた重みは作れているが、test split へ一般化していない。`samples=2000` では gap が `0.04` から `0.07` 程度まで縮み、過学習の見え方も弱くなった。

## Limitations

- seed は `1..5` の5個だけで、信頼区間や有意性検定は未実施。
- 最大 dataset size は `2000 samples/class` で、Issue本文に例示された `5000` までは実行していない。
- logistic regression のみを見ており、MLPや別特徴量では未確認。
- majority baselineとの差分ではなく、Issue #2 / #15 と同じ random guess baseline `0.5` との差分を主指標にした。

## Next

- 4/8/16 rounds で seed数を増やすか既存seedを使い、`test_accuracy_minus_baseline` の信頼区間を計算する: #50
- MLPなど容量の大きいモデルで同じ baseline 差分を測定する場合は、今回の logistic regression 結果を比較対象にする: #51
