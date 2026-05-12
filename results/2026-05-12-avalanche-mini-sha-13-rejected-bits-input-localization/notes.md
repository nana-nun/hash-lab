# mini-sha 13 rounds rejected output bits 入力bit局在比較

## Question

Issue #47 で seed階層CIでも残った output bits `225, 228, 231, 254, 255` は、同じ入力bit範囲に局在した偏りを持つか。

## Hypothesis

rejected output bits `225, 228, 231, 254, 255` は、同じ input bits `224..254` 付近に偏りが集中するが、正負の方向や最大偏り位置は output bit ごとに異なる。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-12-avalanche-mini-sha-13-rejected-bits-input-localization/compute_rejected_bits_input_localization.py`
- Executed at: `2026-05-12T19:42:25+09:00`
- Hash / rounds: `mini-sha` / `13`
- Input: `32` bytes, `256` input bits
- Output bits: `225, 228, 231, 254, 255`
- Seeds: `1..20`
- Dataset size: 各seed・各input bit `500 samples`、各input bit・各output bit合計 `10000 samples`
- CI: Wilson score 95% CI
- Multiple comparison: output bit ごとに 256 input bit positions へ Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `compute_rejected_bits_input_localization.py`: 入力bit位置別測定スクリプト。
- `seed_input_bit_metrics.csv`: output bit / input bit / seed別の flip count と flip rate。
- `input_bit_ci_metrics.csv`: output bit / input bit別の pooled flip rate、Wilson CI、raw p-value、Holm補正後 p-value。
- `summary.csv`: output bit別の min/max、reject count、rejected input bits の要約。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、各入力bit位置から各対象 output bit への flip rate は `0.5` になる。

## Result

5つの rejected output bits はすべて、入力bit位置別に強い局在偏りを示した。Holm補正後に残った input bit 数は output bit ごとに `25..32` 個だった。

| output_bit_index | mean_flip_rate | min flip rate / input bit | max flip rate / input bit | CI excludes 0.5 count | Holm reject count |
| ---: | ---: | --- | --- | ---: | ---: |
| 225 | 0.494162 | 0.195400 / 231 | 0.781900 / 245 | 41 | 25 |
| 228 | 0.492892 | 0.198500 / 234 | 0.785900 / 248 | 41 | 28 |
| 231 | 0.494541 | 0.166700 / 224 | 0.798700 / 251 | 45 | 26 |
| 254 | 0.490956 | 0.135700 / 228 | 0.839300 / 236 | 43 | 26 |
| 255 | 0.488720 | 0.064900 / 224 | 0.842300 / 237 | 49 | 32 |

Holm補正後に残った input bits のうち、input bits `224..254` に入る数:

| output_bit_index | rejected bits in 224..254 | total Holm rejects |
| ---: | ---: | ---: |
| 225 | 21 | 25 |
| 228 | 22 | 28 |
| 231 | 21 | 26 |
| 254 | 21 | 26 |
| 255 | 23 | 32 |

bit255 の summary は Issue #44 と同じ sampling design で再計算され、同じ min/max と reject count になった。

## Interpretation

仮説は支持された。Issue #47 で seed階層CIでも残った5つの output bits は、いずれも input bits `224..254` 付近に強い局在偏りを持つ。これは、13 rounds の残差偏りが単一の output bit だけの偶然ではなく、入力後半の局所範囲から複数の後半 output bits へ伝播する構造的な偏り候補であることを示す。

一方で、最大偏り位置と方向は output bit ごとに異なる。たとえば bit255 は input bit `224` で非常に低い flip rate `0.064900`、input bit `237` で高い flip rate `0.842300` を示す。bit225 は min が input bit `231`、max が `245` で、bit228 は min が `234`、max が `248` だった。したがって「同じ入力範囲に局在する」とは言えるが、各 output bit が同じ符号・同じ位置で偏っているわけではない。

Issue #47 の aggregate な seed階層CIでは、5つの output bits はすべて平均として baseline `0.5` より低かった。今回の入力bit位置別測定では、強い正方向と負方向の偏りが混在している。aggregate 指標はそれらを平均した結果であり、局所構造を見るには input bit位置別の保存が必要になる。

## Limitations

- 各 input bit / output bit は合計 `10000 samples` で、Issue #47 の output bitごとの合計 `40000 samples` より小さい。
- 入力bit位置ごとに固定して測ったため、Issue #42 / #47 の random input bit flip 測定とは sampling design が異なる。
- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- 13 rounds の rejected output bitsだけを対象にした。12/14 rounds で局在がどう変化するかは #74 で未確認。
- どの内部状態、message schedule word、または carry / rotation の相互作用が原因かは、この測定だけでは分からない。

## Next

- #74 で 12/14 rounds でも bit255 の入力bit位置別偏りを比較し、局在が round 増加で弱まるか確認する。
- #57 の文献メモを使い、局所差分・差分伝播の観点から input bits `224..254` 付近の解釈を深める。
- #77 のサンプル単位 avalanche vector 保存を実装し、BIC / output bit pair correlation でも同じ範囲の依存が見えるか確認できるようにする。
