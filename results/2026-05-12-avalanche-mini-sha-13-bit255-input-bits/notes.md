# mini-sha 13 rounds bit255 入力bit位置別偏り

## Question

`mini-sha` 13 rounds の `output_bit_index=255` に残った偏りは、特定の入力bit位置に由来するか。

## Hypothesis

13 rounds bit255 の偏りは全入力bitに均一ではなく、特定の入力bit位置または近い範囲に強く現れる。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-12-avalanche-mini-sha-13-bit255-input-bits/compute_input_bit_bias.py`
- Executed at: `2026-05-12T14:17:35+09:00`
- Hash / rounds: `mini-sha` / `13`
- Input: `32` bytes, `256` input bits
- Output bit: `255`
- Seeds: `1..20`
- Dataset size: 各seed・各input bit `500 samples`、各input bit合計 `10000 samples`
- CI: Wilson score 95% CI
- Multiple comparison: 256 input bit positions に対する Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `compute_input_bit_bias.py`: 入力bit位置別測定スクリプト。
- `seed_input_bit_metrics.csv`: seed別・input bit別の flip count と flip rate。
- `input_bit_ci_metrics.csv`: input bit別の pooled flip rate、Wilson CI、raw p-value、Holm補正後 p-value。
- `summary.csv`: min/max、reject count、rejected input bits の要約。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、各入力bit位置から `output_bit_index=255` への flip rate は `0.5` になる。

## Result

入力bit位置別の偏りは強く局在した。256 input bits のうち、Wilson CI が baseline `0.5` を含まないものは `49`、Holm補正後に baseline と矛盾するものは `32` だった。

summary:

| metric | value |
| --- | ---: |
| input_bits | 256 |
| seed_count | 20 |
| samples_per_seed_per_input_bit | 500 |
| total_samples_per_input_bit | 10000 |
| mean_flip_rate across input bits | 0.488720 |
| min_flip_rate | 0.064900 at input bit 224 |
| max_flip_rate | 0.842300 at input bit 237 |
| max_abs_delta_from_0.5 | 0.435100 |
| CI excludes baseline count | 49 |
| Holm reject count | 32 |

最も低い input bits:

| input_bit_index | flip_rate | Wilson CI | baseline_delta | Holm reject |
| ---: | ---: | ---: | ---: | --- |
| 224 | 0.064900 | `[0.060237, 0.069897]` | -0.435100 | True |
| 229 | 0.137900 | `[0.131281, 0.144797]` | -0.362100 | True |
| 248 | 0.157900 | `[0.150885, 0.165178]` | -0.342100 | True |
| 228 | 0.210800 | `[0.202918, 0.218905]` | -0.289200 | True |
| 247 | 0.237300 | `[0.229064, 0.245738]` | -0.262700 | True |

最も高い input bits:

| input_bit_index | flip_rate | Wilson CI | baseline_delta | Holm reject |
| ---: | ---: | ---: | ---: | --- |
| 237 | 0.842300 | `[0.835025, 0.849312]` | 0.342300 | True |
| 243 | 0.839500 | `[0.832175, 0.846564]` | 0.339500 | True |
| 233 | 0.826400 | `[0.818851, 0.833698]` | 0.326400 | True |
| 218 | 0.585200 | `[0.575513, 0.594822]` | 0.085200 | True |
| 222 | 0.569600 | `[0.559871, 0.579276]` | 0.069600 | True |

Holm補正後に残った input bits:

`194, 199, 203, 204, 214, 216, 218, 221, 222, 224, 226, 227, 228, 229, 231, 232, 233, 235, 236, 237, 240, 241, 242, 243, 245, 246, 247, 248, 250, 251, 253, 254`

## Interpretation

仮説は支持された。13 rounds bit255 の偏りは全入力bitに均一ではなく、入力bit `224..254` 付近に強く局在している。特に input bit `224` は flip rate `0.064900`、input bit `237` は `0.842300` で、baseline `0.5` から大きく離れた。

Issue #42 の aggregate bit255 flip rate は `0.483950` だった。今回の input bit位置別平均は `0.488720` で、集約すると小さな負方向の差分に見える。一方、入力bitを固定すると強い正負の偏りが混在しており、aggregate 測定では互いに相殺されていた可能性が高い。

Holm補正後に残った input bits はほぼ後半の局所範囲に集中している。`mini-sha` の 13 rounds では、message schedule と圧縮関数の構造上、output bit255 への影響が入力bit位置によってかなり違うことを示す探索的結果と読む。

## Limitations

- 各 input bit は合計 `10000 samples` で、Issue #42 の aggregate bit255 `40000 samples` より小さい。
- 入力bit位置ごとに固定して測ったため、Issue #42 の random input bit flip 測定とは sampling design が異なる。
- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- 13 rounds / output bit255 のみを対象にした。12/14 rounds や他の rejected output bits との比較は未確認。
- どの内部状態や message schedule word が原因かは、この測定だけでは分からない。

## Next

- #57 で bit255 残差偏りを読むための reduced-round SHA-like 構造解析文献を整理する。
- 必要なら、12/14 rounds でも同じ input bit位置別測定を行い、局在範囲が round 増加で消えるか確認する。
- 必要なら、Issue #47 の rejected output bits `225, 228, 231, 254, 255` それぞれで input bit位置別測定を行い、同じ入力範囲に局在するか比較する。
