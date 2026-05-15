# mini-sha all output bit pair BIC / correlation

## Question

`mini-sha` の rounds `12, 13, 14, 16` で、全 output bit pair の avalanche vector 相関はどう見えるか。SAC風の output bit別 flip rate や input-output heatmap では見えない依存構造が残るか。

## Hypothesis

12 rounds では後半 output bit 周辺に補正後も残る pairwise correlation があり、13/14/16 rounds では random input bit mode で平均すると補正後に残るpairは大きく減る。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-16-avalanche-mini-sha-bic-all-output-pairs/compute_bic_all_output_pairs.py`
- Executed at: `2026-05-16T00:34:06+09:00`
- Hash / rounds: `mini-sha` / `12, 13, 14, 16`
- Input mode: random input bit flip
- Output bits: `256`
- Output bit pairs: 各round `32640` pairs
- Seeds: `1..5`
- Dataset size: 各round `5000 samples`
- Baseline: 独立な output bit flip では covariance と Pearson/phi correlation は `0` 付近
- P-value: `n * phi^2` を df=1 の Pearson chi-square 近似として扱う
- Multiple comparison: roundごとに全 output bit pair へ Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `compute_bic_all_output_pairs.py`: 全 output bit pair の相関計算スクリプト。
- `pair_correlation.csv`: output bit pairごとの joint count、flip rate、covariance、Pearson correlation、raw/adjusted p-value。
- `top_pairs.csv`: round別の絶対相関上位20 pair。
- `summary.csv`: round別の最大絶対相関と Holm reject count。
- `round_12_pair_correlation_heatmap.png`, `round_13_pair_correlation_heatmap.png`, `round_14_pair_correlation_heatmap.png`, `round_16_pair_correlation_heatmap.png`: pair correlation heatmap。青が負、白が0付近、赤が正。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、output bit pair `(j, k)` の反転イベントはほぼ独立で、covariance と Pearson/phi correlation は `0` 付近になる。

## Result

12 rounds では Holm補正後に `22` pair が残った。13/14/16 rounds では、今回の random input bit mode と `5000 samples` では補正後に残るpairはなかった。

| rounds | output bit pairs | samples | max_abs_correlation | max pair | signed correlation | Holm reject count |
| ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 12 | 32640 | 5000 | 0.09787985 | `(233, 234)` | 0.09787985 | 22 |
| 13 | 32640 | 5000 | 0.05636122 | `(114, 192)` | -0.05636122 | 0 |
| 14 | 32640 | 5000 | 0.05817582 | `(130, 232)` | -0.05817582 | 0 |
| 16 | 32640 | 5000 | 0.06246363 | `(82, 180)` | -0.06246363 | 0 |

12 rounds の絶対相関上位:

| output bit pair | correlation | Holm adjusted p-value | reject |
| --- | ---: | ---: | --- |
| `(233, 234)` | 0.09787985 | 0.000000146 | True |
| `(224, 225)` | 0.09617774 | 0.000000340 | True |
| `(224, 230)` | 0.09190688 | 0.000002643 | True |
| `(244, 245)` | 0.09071457 | 0.000004611 | True |
| `(252, 253)` | 0.08950869 | 0.000008042 | True |
| `(254, 255)` | 0.08915240 | 0.000009464 | True |

## Interpretation

仮説は探索的には支持された。12 rounds では `224..255` 周辺の隣接または近傍 output bit pair が上位に多く、SAC風の単独bit flip rate だけでは見えない出力bit間依存が残っている。これは既存の small BIC 測定で `(254, 255)` 周辺に強い相関が見えたこととも方向は合う。

一方で、13 rounds 以降は random input bit mode で全 output bit pair を平均すると、Holm補正後に残るpairはなかった。#85 の input-output heatmap では 13 rounds に input bits `224..254` 付近の局在が残っていたため、局所的な fixed input bit 条件では依存が残っていても、random input bit で平均すると相殺される可能性がある。

この結果は「13 rounds以降に依存構造が存在しない」という主張ではない。今回の測定は random input bit mode、各round `5000 samples`、pairwise Pearson/phi correlation に限った探索である。

## Limitations

- random input bit mode で測ったため、input bit位置ごとの局在依存は平均で相殺される可能性がある。
- 各round `5000 samples` なので、小さい相関や局所条件の安定性評価には不足する可能性がある。
- p-value は Pearson chi-square df=1 の近似であり、厳密検定や信頼区間ではない。
- pairwise correlation は高次依存を否定しない。
- toy / reduced-round `mini-sha` の局所測定であり、実SHA-256の安全性や攻撃可能性は主張しない。

## Next

- #95 で aggregate avalanche、SAC風指標、input-output heatmap、BIC、distinguisher の round境界を比較する。
- fixed input bit mode で、#85 の heatmap上位input bitに絞った全 output bit pair correlation を追加すると、局所依存の相殺を確認しやすい。
- 13/14/16 rounds の上位pairは、必要なら samples / seeds を増やして再測定する。
