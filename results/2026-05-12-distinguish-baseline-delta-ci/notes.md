# Distinguisher baseline差分のseed階層CI

## Question

Issue #18 の logistic regression 感度測定について、4/8/16 rounds の `test_accuracy_minus_baseline` は random guess baseline 付近に留まるか。

## Hypothesis

4/8/16 rounds の `test_accuracy_minus_baseline` は、samples と epochs を変えても seed平均の95% CIが `0` を含む。もし `0` を含まない条件があっても、正方向に安定して baseline を上回るのではなく、小さな偶然変動として見える。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-12-distinguish-baseline-delta-ci/compute_ci.py`
- Executed at: `2026-05-12T13:54:16+09:00`
- Source: `results/2026-05-10-distinguish-size-epochs-sensitivity/seed_metrics.csv`
- Hash / rounds: `mini-sha` / `4, 8, 16`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各roundにつき hash出力 `500, 1000, 2000` 件、同数のランダムbit列
- Model config: Issue #18 の logistic regression 結果を再利用。`learning_rate=0.08`、256 bit features、train split `0.8`
- Epochs: `4, 8, 16`
- CI: seed別 `test_accuracy_minus_baseline` の percentile bootstrap 95% CI
- Bootstrap iterations: `10000`
- Bootstrap seed: command base seed `20260512`。実際の行別 seed は `base + rounds + samples + epochs`。

保存ファイル:

- `compute_ci.py`: CI計算スクリプト。
- `seed_baseline_deltas.csv`: seed別の `test_accuracy_minus_baseline` と train-test gap。
- `baseline_delta_ci.csv`: round / samples / epochs ごとの seed平均CI。
- `config.json`: 実行条件。

## Baseline

random guess accuracy `0.5` を baseline とし、主指標は `test_accuracy_minus_baseline = test_accuracy - 0.5` とした。CIでは baseline delta `0` を含むかを確認した。

## Result

4/8/16 rounds の 27条件のうち、26条件で seed平均 bootstrap CI は `0` を含んだ。`0` を含まなかったのは 16 rounds / samples `1000` / epochs `16` の1条件だけで、平均差分は `-0.010000` と負方向だった。

平均差分の絶対値が大きい条件:

| rounds | samples | epochs | mean_test_accuracy_minus_baseline | CI | contains 0 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 8 | 500 | 4 | -0.016000 | `[-0.039000, 0.016000]` | True |
| 16 | 1000 | 8 | -0.012500 | `[-0.041000, 0.006500]` | True |
| 16 | 2000 | 8 | -0.011780 | `[-0.030280, 0.006720]` | True |
| 4 | 500 | 4 | -0.011000 | `[-0.051000, 0.032000]` | True |
| 4 | 500 | 16 | 0.011000 | `[-0.020000, 0.040000]` | True |
| 16 | 1000 | 16 | -0.010000 | `[-0.017500, -0.002500]` | False |

`samples=2000` の条件:

| rounds | epochs | mean_test_accuracy_minus_baseline | CI | contains 0 |
| ---: | ---: | ---: | ---: | --- |
| 4 | 4 | -0.003980 | `[-0.017240, 0.011540]` | True |
| 8 | 4 | 0.000740 | `[-0.017500, 0.017960]` | True |
| 16 | 4 | -0.006500 | `[-0.020740, 0.009220]` | True |
| 4 | 8 | 0.000740 | `[-0.011740, 0.012720]` | True |
| 8 | 8 | 0.001260 | `[-0.015720, 0.015000]` | True |
| 16 | 8 | -0.011780 | `[-0.030280, 0.006720]` | True |
| 4 | 16 | 0.002760 | `[-0.007720, 0.012480]` | True |
| 8 | 16 | 0.004760 | `[-0.012980, 0.022500]` | True |
| 16 | 16 | -0.001000 | `[-0.010480, 0.011480]` | True |

## Interpretation

今回の seed階層CIでは、4/8/16 rounds の logistic regression distinguisher が random guess baseline を安定して上回る証拠は見えなかった。正方向の平均差分が最大だった条件は 4 rounds / samples `500` / epochs `16` の `0.011000` だが、CI は `[-0.020000, 0.040000]` で `0` を含む。

唯一 `0` を含まなかった条件は 16 rounds / samples `1000` / epochs `16` で、方向は負だった。このため、少なくとも Issue #18 のgridでは「baseline を超える汎化性能」ではなく、random guess 付近の小さな seed変動として読むのが妥当。

`samples=2000` では全条件のCIが `0` を含み、平均差分も `-0.011780` から `0.004760` の範囲に留まった。Issue #18 の「4/8/16 rounds は平均で baseline 付近」という解釈は、seed平均CIを付けても大きくは変わらない。

## Limitations

- seed は `1..5` の5点だけで、bootstrap CIは探索的な目安に留まる。
- seed別平均を再標本化しており、test split内の二項sampling uncertaintyは別にはモデル化していない。
- Issue #18 の既存結果を再分析しただけで、新しい学習実行はしていない。
- logistic regression のみを対象にしており、MLPやCNN/RNN系、特徴量設計の違いは未確認。
- `test_accuracy_minus_baseline` は random guess baseline `0.5` との差分であり、majority baselineとの差分ではない。

## Next

- #51 で MLP distinguisher を logistic regression baseline と比較する。
- #53 で 9-15 rounds と32 rounds の logistic regression distinguisherを測定し、avalanche境界と同じround軸で比較する。
- #58 で classifier accuracy のCI設計、seed単位とtest split単位の扱い、multiple testing の整理を文献ベースで進める。
