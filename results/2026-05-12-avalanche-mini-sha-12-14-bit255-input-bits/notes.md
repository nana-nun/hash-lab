# mini-sha 12/13/14 rounds bit255 入力bit位置別偏り

## Question

`mini-sha` の `output_bit_index=255` に対する入力bit位置別の偏りは、12/13/14 rounds でどう変わるか。

## Hypothesis

12 rounds では input bits `224..254` 付近の局在偏りが 13 rounds より強く、14 rounds では 13 rounds より弱くなる。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-12-avalanche-mini-sha-12-14-bit255-input-bits/compute_round_input_bit_bias.py`
- Executed at: `2026-05-12T20:28:55+09:00`
- Hash / rounds: `mini-sha` / `12, 13, 14`
- Input: `32` bytes, `256` input bits
- Output bit: `255`
- Seeds: `1..20`
- Dataset size: 各round・各seed・各input bit `500 samples`、各round・各input bit合計 `10000 samples`
- CI: Wilson score 95% CI
- Multiple comparison: roundごとに 256 input bit positions に対する Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `compute_round_input_bit_bias.py`: round別・入力bit位置別測定スクリプト。
- `seed_input_bit_metrics.csv`: round別・seed別・input bit別の flip count と flip rate。
- `input_bit_ci_metrics.csv`: round別・input bit別の pooled flip rate、Wilson CI、raw p-value、Holm補正後 p-value。
- `summary.csv`: round別の min/max、reject count、rejected input bits の要約。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、各round・各入力bit位置から `output_bit_index=255` への flip rate は `0.5` になる。

## Result

round が増えるにつれて局在偏りは弱まった。ただし 14 rounds でも input bits `226..254` 付近の一部は Holm補正後に baseline `0.5` と矛盾した。

summary:

| rounds | mean_flip_rate | min_flip_rate | max_flip_rate | max_abs_delta_from_0.5 | CI excludes baseline count | Holm reject count |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 0.450715 | 0.000000 at input bit 224 | 1.000000 at input bit 230 | 0.500000 | 72 | 61 |
| 13 | 0.488720 | 0.064900 at input bit 224 | 0.842300 at input bit 237 | 0.435100 | 49 | 32 |
| 14 | 0.499887 | 0.420200 at input bit 236 | 0.577200 at input bit 250 | 0.079800 | 22 | 10 |

12 rounds の最も極端な input bits:

| direction | input_bit_index | flip_rate | Wilson CI | baseline_delta | Holm reject |
| --- | ---: | ---: | ---: | ---: | --- |
| low | 224 | 0.000000 | `[0.000000, 0.000384]` | -0.500000 | True |
| low | 225 | 0.000000 | `[0.000000, 0.000384]` | -0.500000 | True |
| low | 226 | 0.000000 | `[0.000000, 0.000384]` | -0.500000 | True |
| high | 230 | 1.000000 | `[0.999616, 1.000000]` | 0.500000 | True |
| high | 244 | 1.000000 | `[0.999616, 1.000000]` | 0.500000 | True |

14 rounds の最も極端な input bits:

| direction | input_bit_index | flip_rate | Wilson CI | baseline_delta | Holm reject |
| --- | ---: | ---: | ---: | ---: | --- |
| low | 236 | 0.420200 | `[0.410558, 0.429903]` | -0.079800 | True |
| low | 248 | 0.454500 | `[0.444760, 0.464275]` | -0.045500 | True |
| high | 250 | 0.577200 | `[0.567490, 0.586851]` | 0.077200 | True |
| high | 254 | 0.560200 | `[0.550450, 0.569904]` | 0.060200 | True |
| high | 231 | 0.556900 | `[0.547144, 0.566612]` | 0.056900 | True |

Holm補正後に残った input bits:

| rounds | rejected input bits |
| ---: | --- |
| 12 | `162, 165, 167, 171, 172, 176, 182, 184, 186, 190, 192, 194, 195, 196, 197, 199, 200, 201, 203, 204, 205, 208, 209, 210, 211, 213, 214, 215, 216, 218, 219, 221, 222, 224, 225, 226, 227, 228, 229, 230, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 246, 247, 248, 249, 251, 252, 253, 254` |
| 13 | `194, 199, 203, 204, 214, 216, 218, 221, 222, 224, 226, 227, 228, 229, 231, 232, 233, 235, 236, 237, 240, 241, 242, 243, 245, 246, 247, 248, 250, 251, 253, 254` |
| 14 | `226, 231, 235, 236, 240, 246, 247, 248, 250, 254` |

## Interpretation

仮説はおおむね支持された。12 rounds では `output_bit_index=255` への影響が input bits `224..254` 付近で特に強く、input bit によって flip rate が `0.0` または `1.0` まで振れた。13 rounds では同じ範囲の局在が残るが、reject count と最大差分は小さくなる。14 rounds では aggregate mean が `0.499887` まで baseline に近づく一方、input bit を固定すると `226, 231, 235, 236, 240, 246, 247, 248, 250, 254` が Holm補正後にも残った。

Issue #42 の出力bit位置別 aggregate では 14 rounds の bit255 は round内256bitの Holm補正後に棄却されなかった。今回の測定では input bit を固定した条件付き偏りを見ているため、aggregate では相殺される小さな局在が見えた可能性がある。これは「14 rounds 全体が識別できる」という主張ではなく、bit255 の特定入力位置に限った探索的な残差構造として扱う。

## Limitations

- 各 round・input bit は合計 `10000 samples` で、非常に小さい差分の安定性確認にはまだ限界がある。
- roundごとに 256 input bit positions の Holm補正をしたが、round間の追加比較までは補正していない。
- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- `output_bit_index=255` のみを対象にした。他の output bits で同じ round変化が起きるかは未確認。
- 局在の原因となる内部状態、message schedule、carry propagation はこの測定だけでは分からない。

## Next

- #77 の BIC 用 sample-level avalanche vector 保存で、input bit間または output bit間の相関を追えるようにする。
- #57 で reduced-round SHA-like 構造解析文献を整理し、後半 input bits の局在を読むための仮説を作る。
