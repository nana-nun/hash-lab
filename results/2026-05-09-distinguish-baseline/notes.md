# Distinguisher Baseline

## Question

`mini-sha` の出力とランダムbit列を識別する実験で、logistic regression の精度は random guess baseline と比べてどれくらい高いか。

## Hypothesis

round数が増えるほど `test_accuracy` は random guess baseline の `0.5` に近づく。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli distinguish --rounds 2 4 8 16 --samples 1000 --epochs 8 --seed 1 --output results\2026-05-09-distinguish-baseline\metrics.csv --format csv`
- Executed at: `2026-05-09T19:27:38+09:00`
- Seed: `1`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16`
- Dataset size: 各roundにつき hash出力 `1000` 件、ランダムbit列 `1000` 件、合計 `2000` 件
- Model config: logistic regression、`epochs=8`、`learning_rate=0.08`、256 bit features

## Baseline

- random guess baseline: `0.5`
- majority baseline: shuffle後のtest splitのラベル分布から算出。この実行では各roundで `0.5225`。

## Result

| rounds | train_accuracy | test_accuracy | random_guess_baseline | test_accuracy_minus_baseline |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 1.0000 | 1.0000 | 0.5000 | 0.5000 |
| 4 | 0.6175 | 0.4975 | 0.5000 | -0.0025 |
| 8 | 0.5919 | 0.4925 | 0.5000 | -0.0075 |
| 16 | 0.6100 | 0.4900 | 0.5000 | -0.0100 |

詳細なCSVは `metrics.csv` に保存した。

## Interpretation

2 rounds では logistic regression が完全に識別できた。4 rounds 以降では `test_accuracy` が random guess baseline の近くにあり、この設定では汎化できる識別信号は確認できなかった。

`train_accuracy` は 4/8/16 rounds でも `0.59` から `0.62` 程度まで上がっているが、`test_accuracy` は baseline 付近なので、学習した重みがtest splitに一般化しているとは言いにくい。

## Limitations

- seedは `1` の単発実行のみ。
- logistic regression の学習率、epoch数、dataset size は固定。
- baseline差分は random guess の `0.5` との差分であり、統計的有意性や信頼区間は未評価。
- majority baseline は test split のラベル分布に依存する。

## Next

- Issue #15 で seedを複数に増やし、roundごとの `test_accuracy_minus_baseline` の平均とばらつきを確認する。
- dataset size と epochs を変え、4 rounds 以降の結果が安定して random guess 付近に留まるか確認する。
