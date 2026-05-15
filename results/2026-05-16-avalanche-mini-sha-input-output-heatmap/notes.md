# mini-sha input bit x output bit avalanche heatmap

## Question

`mini-sha` の rounds `12, 13, 14, 16` で、入力bit位置と出力bit位置の全組み合わせの flip rate はどう見えるか。既存結果で見えていた input bits `224..254` 付近の局在偏りは、全出力bitに広げても残るか。

## Hypothesis

12/13 rounds では input bits `224..254` 付近を中心に局所的な偏りが見え、14/16 rounds では偏りが縮小する。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-16-avalanche-mini-sha-input-output-heatmap/compute_input_output_heatmap.py`
- Executed at: `2026-05-16T00:18:07+09:00`
- Hash / rounds: `mini-sha` / `12, 13, 14, 16`
- Input: `32` bytes, `256` input bits
- Output: `32` bytes, `256` output bits
- Seeds: `1..5`
- Dataset size: 各round・各input bit・各seed `64 samples`、各cell合計 `320 samples`
- Baseline: flip rate `0.5`
- Model config: none

保存ファイル:

- `compute_input_output_heatmap.py`: 全 input bit x output bit の測定スクリプト。
- `flip_rate_matrix.csv`: round / input bit / output bit ごとの flip count と flip rate。
- `baseline_delta_matrix.csv`: baseline `0.5` からの差分。
- `summary.csv`: round別の平均、min/max、最大絶対差分。
- `round_12_baseline_delta_heatmap.png`, `round_13_baseline_delta_heatmap.png`, `round_14_baseline_delta_heatmap.png`, `round_16_baseline_delta_heatmap.png`: baseline delta heatmap。青が負、白が0付近、赤が正。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、各入力bit位置と各出力bit位置の組で flip rate は `0.5` 付近になる。

## Result

rounds 12/13 では後半 input bits に局在した強い偏りが見え、14/16 では大きく縮小した。

| rounds | mean_flip_rate | min_flip_rate | max_flip_rate | max_abs_delta_from_0.5 | max_abs_delta cell |
| ---: | ---: | ---: | ---: | ---: | --- |
| 12 | 0.493231 | 0.000000 | 1.000000 | 0.500000 | input bit `224`, output bit `109` |
| 13 | 0.499396 | 0.062500 | 0.853125 | 0.437500 | input bit `224`, output bit `255` |
| 14 | 0.500082 | 0.378125 | 0.625000 | 0.125000 | input bit `29`, output bit `164` |
| 16 | 0.500068 | 0.375000 | 0.621875 | 0.125000 | input bit `5`, output bit `107` |

input bits `224..254` 付近だけを見ると、平均絶対差分は次のように縮小した。

| rounds | mean abs delta, all cells | mean abs delta, input bits 224..254 | max abs delta, input bits 224..254 |
| ---: | ---: | ---: | ---: |
| 12 | 0.033357 | 0.098593 | 0.500000 |
| 13 | 0.023679 | 0.033291 | 0.437500 |
| 14 | 0.022190 | 0.022493 | 0.121875 |
| 16 | 0.022252 | 0.021961 | 0.100000 |

## Interpretation

仮説は探索的には支持された。12 rounds では input bits `224..254` 付近に強い局在偏りが見え、13 rounds でも `output_bit_index=255` などで大きな差分が残った。これは既存の bit255 / rejected bits 入力bit位置別測定と整合する。

14/16 rounds では aggregate mean が `0.5` 付近で、input bits `224..254` の平均絶対差分も全体平均に近づいた。今回の条件では、12/13 rounds で見えた後半入力bitの局在は 14/16 rounds でかなり弱くなる。

ただし、各cellの合計サンプル数は `320` と小さい。14/16 rounds の最大絶対差分 `0.125000` は、単一cellの極値としては sampling noise の影響を強く受ける可能性がある。今回のheatmapは、構造の候補を探すための可視化であり、個々のcellの有意性を断定するものではない。

## Limitations

- 各 round / input bit / output bit cell は合計 `320 samples` で、既存の bit255 測定よりかなり小さい。
- Wilson CI や多重比較補正はまだ計算していない。
- heatmap の色は roundごとの最大絶対差分で正規化しているため、round間の色の強さをそのまま絶対比較しない。
- toy / reduced-round `mini-sha` の局所測定であり、実SHA-256の安全性や攻撃可能性は主張しない。

## Next

- #86 で全 output bit pair correlation を測り、SAC風heatmapでは見えない依存構造を確認する。
- #95 で aggregate avalanche、output bit別SAC、input-output heatmap、BIC、distinguisher の round境界を比較する。
- 必要なら 14/16 rounds の上位cellだけ samples / seeds を増やして再測定する。
