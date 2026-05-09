# mini-sha Avalanche 出力bit位置別測定

## Question

`mini-sha` の aggregate mean flip ratio が `0.5` に近いroundでも、出力bit位置ごとの flip rate に偏りは残るか。

## Hypothesis

16 round 以上では多くの出力bit位置で flip rate が `0.5` に近づくが、低roundではbit位置ごとの偏りが残る。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bits --rounds 2 4 8 16 32 --samples 2000 --seeds 1 2 3 4 5 --bit-output results/2026-05-10-avalanche-mini-sha-bit-positions/bit_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-bit-positions/round_summary.csv`
- Executed at: `2026-05-10T01:23:32+09:00`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16, 32`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`、roundごとに合計 `10000 samples`
- Output: `256` bits
- Model config: none

保存ファイル:

- `bit_metrics.csv`: `rounds, seed, output_bit_index, flip_count, flip_rate` を保存した bit位置別データ。
- `round_summary.csv`: round別に bit位置ごとの aggregate `min / max / mean` と、最大の baseline 差分を保存した。
- `config.json`: 実行条件。

## Baseline

Issue #7 / `results/2026-05-09-avalanche-mini-sha-multi-seed/aggregate_metrics.csv` の aggregate mean を baseline として参照した。理想的な random-like avalanche の期待値は、各出力bit位置でも flip rate `0.5`。

## Result

詳細なCSVは `bit_metrics.csv` と `round_summary.csv` に保存した。

| rounds | mean_flip_rate | min_flip_rate | min_bit_index | max_flip_rate | max_bit_index | max_abs_delta_from_0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.014161 | 0.000000 | 64 | 0.062200 | 13 | 0.500000 |
| 4 | 0.083370 | 0.003300 | 127 | 0.187200 | 17 | 0.496700 |
| 8 | 0.325878 | 0.204900 | 255 | 0.442400 | 4 | 0.295100 |
| 16 | 0.500120 | 0.487900 | 155 | 0.512100 | 192 | 0.012100 |
| 32 | 0.499881 | 0.483400 | 241 | 0.516400 | 176 | 0.016600 |

## Interpretation

2/4/8 rounds では、aggregate mean だけでなく bit位置ごとの flip rate でも baseline `0.5` から大きく離れている。特に 2/4 rounds は、ほとんど反転しない出力bit位置があり、低roundでは拡散が出力全体に十分届いていない。

16/32 rounds では aggregate mean が `0.5` 付近にあり、bit位置ごとの aggregate min/max も `0.5` の近くに収まった。今回の条件では、16/32 rounds で aggregate mean に隠れた大きな特定bit偏りは見えていない。

一方で、32 rounds の aggregate bit別範囲は `[0.483400, 0.516400]` で、16 rounds より少し広い。これは sampling noise、seed集合、または toy hash の局所的な偏りの可能性がある。今回は bit位置別の信頼区間や多重比較補正をしていないため、特定bitの小さな差分を構造的な偏りとは断定しない。

## Limitations

- seeds は `1..5` の5個だけ。
- 各seed・各round `2000 samples` であり、bit位置ごとの小さな差分を判定するには追加の不確実性評価が必要。
- bit位置別の confidence interval、binomial test、多重比較補正は未実施。
- 入力bit位置ごとの条件付き偏りや bit independence は評価していない。
- round 9から15の境界領域は含めていない。

## Next

- round 9から15の中間領域を測定し、`0.5` 付近へ移る境界を細かく見る: #9
- bit位置ごとの confidence interval と多重比較を追加し、16/32 rounds の小さな差分が sampling noise と矛盾するか確認する: #33
