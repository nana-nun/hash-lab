# mini-sha Avalanche 9-15 rounds 出力bit位置別測定

## Question

`mini-sha` avalanche の 9-15 rounds について、aggregate mean が `0.5` に近づく境界でも出力bit位置ごとの flip rate の偏りが残るか。

## Hypothesis

9-12 rounds では bit位置ごとの偏りが残り、13-15 rounds では aggregate bit-position min/max も `0.5` 付近に近づく。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bits --rounds 9 10 11 12 13 14 15 --samples 2000 --seeds 1 2 3 4 5 --bit-output results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/bit_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/round_summary.csv`
- Executed at: `2026-05-10T05:52:31+09:00`
- Hash / rounds: `mini-sha` / `9, 10, 11, 12, 13, 14, 15`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`、roundごとに合計 `10000 samples`
- Output: `256` bits
- Model config: none

保存ファイル:

- `bit_metrics.csv`: `rounds, seed, output_bit_index, flip_count, flip_rate` を保存した bit位置別データ。
- `round_summary.csv`: round別に bit位置ごとの aggregate `min / max / mean` と、最大の baseline 差分を保存した。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値は、各出力bit位置で flip rate `0.5`。比較対象として、Issue #8 の `2, 4, 8, 16, 32` bit位置別測定と、Issue #9 の `9-15` aggregate mean 測定を参照した。

## Result

詳細なCSVは `bit_metrics.csv` と `round_summary.csv` に保存した。

| rounds | mean_flip_rate | min_flip_rate | min_bit_index | max_flip_rate | max_bit_index | max_abs_delta_from_0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 0.386652 | 0.266400 | 255 | 0.498800 | 28 | 0.233600 |
| 10 | 0.437913 | 0.328400 | 255 | 0.513200 | 9 | 0.171600 |
| 11 | 0.473403 | 0.396800 | 255 | 0.511400 | 37 | 0.103200 |
| 12 | 0.493620 | 0.454000 | 228 | 0.514300 | 69 | 0.046000 |
| 13 | 0.499301 | 0.478400 | 255 | 0.515000 | 119 | 0.021600 |
| 14 | 0.499936 | 0.485000 | 74 | 0.512600 | 168 | 0.015000 |
| 15 | 0.499846 | 0.486500 | 180 | 0.514600 | 184 | 0.014600 |

## Interpretation

9-12 rounds では、aggregate mean が `0.5` に近づく途中でも bit位置ごとの差が残っている。特に 9-11 rounds は最小bitの flip rate が `0.266400`、`0.328400`、`0.396800` と baseline から大きく離れており、aggregate mean だけでなく特定出力bitにも拡散不足が見える。

12 rounds は aggregate mean が `0.493620` まで近づくが、bit位置別では最小 `0.454000`、最大 `0.514300` で、最大 baseline 差分は `0.046000` 残る。Issue #9 の aggregate mean だけでは小さく見える 12 rounds の差分は、bit位置別に見るとまだ目立つ。

13 rounds では mean が `0.499301` になり、bit位置別範囲も `[0.478400, 0.515000]` まで狭くなる。14/15 rounds では範囲がさらに `[0.485000, 0.512600]`、`[0.486500, 0.514600]` になり、Issue #8 の 16/32 rounds と同程度の大きさに近づく。

今回の条件では、aggregate mean の主な境界は 12から13 rounds の間に見えるが、bit位置別の偏りも同じ境界付近で急に小さくなる。ただし 13 rounds の min/max は 14/15 rounds よりやや広く、13 rounds を random-like と断定するには bit位置別CIや seed数追加が必要。

## Limitations

- seeds は `1..5` の5個だけ。
- 各seed・各round `2000 samples` であり、bit位置ごとの小さな差分には追加の不確実性評価が必要。
- bit位置別の confidence interval、binomial test、多重比較補正はこの実験では実施していない。
- 入力bit位置ごとの条件付き偏りや bit independence は評価していない。
- avalanche が `0.5` 付近でも、distinguisher が同じroundで baseline 付近になるとは限らない。

## Next

- 9-15 rounds の bit位置別 CI と多重比較補正を計算し、12/13 rounds 周辺の特定bit偏りが sampling noise と矛盾するか確認する: #40
- 9-15 rounds の distinguisher baseline と比較し、avalanche の境界と識別困難性の境界が一致するか確認する: #19
