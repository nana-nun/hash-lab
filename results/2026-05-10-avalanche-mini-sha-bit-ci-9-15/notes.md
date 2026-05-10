# mini-sha Avalanche 9-15 rounds bit位置別 Confidence Interval

## Question

`mini-sha` avalanche の 9-15 rounds について、12/13 rounds 周辺の出力bit位置別偏りは sampling noise と矛盾するか。

## Hypothesis

12 rounds では複数の出力bit位置で baseline `0.5` との差が Holm補正後も残り、13-15 rounds では補正後に棄却されるbit数が大きく減る。

## Setup

- Command: `C:\Users\nanau\source\hash-lab\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bit-ci --rounds 9 10 11 12 13 14 15 --bit-input results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/bit_metrics.csv --bit-ci-output results/2026-05-10-avalanche-mini-sha-bit-ci-9-15/bit_ci_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-bit-ci-9-15/round_summary.csv`
- Executed at: `2026-05-10T09:53:59+09:00`
- Input: `results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/bit_metrics.csv`
- Hash / rounds: `mini-sha` / `9, 10, 11, 12, 13, 14, 15`
- Seeds: `1, 2, 3, 4, 5`
- Dataset size: 各seed・各round `2000 samples`、round/bitごとに合計 `10000 samples`
- Output: `256` bits
- CI: Wilson score 95% CI
- Multiple comparison: round内256 bitに対する Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `bit_ci_metrics.csv`: round/bit別の aggregate flip rate、Wilson CI、baseline差分、raw p-value、Holm補正後 p-value。
- `round_summary.csv`: round別の min/max、最大baseline差分、CIがbaselineを含まないbit数、Holm補正後にbaselineを棄却したbit数。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として、各出力bit位置の flip rate `0.5` を baseline にした。

## Result

詳細なCSVは `bit_ci_metrics.csv` と `round_summary.csv` に保存した。

| rounds | min_flip_rate | max_flip_rate | max_abs_delta_from_0.5 | CI excludes 0.5 count | Holm reject count |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 0.266400 | 0.498800 | 0.233600 | 245 | 234 |
| 10 | 0.328400 | 0.513200 | 0.171600 | 188 | 167 |
| 11 | 0.396800 | 0.511400 | 0.103200 | 126 | 97 |
| 12 | 0.454000 | 0.514300 | 0.046000 | 66 | 35 |
| 13 | 0.478400 | 0.515000 | 0.021600 | 20 | 1 |
| 14 | 0.485000 | 0.512600 | 0.015000 | 14 | 0 |
| 15 | 0.486500 | 0.514600 | 0.014600 | 16 | 0 |

13 rounds で Holm補正後に残ったbitは `output_bit_index=255` で、flip rate は `0.478400`、Holm adjusted p-value は `0.0041793164` だった。

## Interpretation

9-12 rounds では、round内256 bitの Holm補正後も baseline `0.5` との差を棄却するbitが多く残った。特に 9-11 rounds は棄却bit数が `234`, `167`, `97` で、Issue #36 の bit位置別 min/max で見えた低round側の偏りは sampling noise だけでは説明しにくい。

12 rounds は aggregate mean が `0.493620` まで近づいていたが、bit位置別には `35` bit が Holm補正後も baseline と矛盾した。Issue #36 の最大差分 `0.046000` は、現在の sample size では単なる偶然差分とは言いにくい。

13 rounds では Holm reject count が `1` まで落ち、14/15 rounds では `0` になった。13 rounds の Wilson CI単体では `20` bit が baseline `0.5` を含まないが、多重比較を考えると補正後に残るbitは限定的で、14/15 rounds は補正後に棄却されるbitがない。

今回の条件では、bit位置別の偏りも 12から13 rounds の間で大きく弱まる。これは Issue #36 の min/max比較と、Issue #37 の 12/13 rounds seed階層CIで見えた境界と整合する。

## Limitations

- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- round/bitごとに seedを合算しており、seed階層のばらつきは明示的には扱っていない。
- seeds は `1..5` の5個だけ。
- Holm補正は round内256 bitを対象にした。round間を含めた全比較補正ではない。
- 13 rounds の `output_bit_index=255` は補正後も棄却されたが、seed追加や入力bit位置ごとの条件付き測定で安定性を確認していない。
- avalanche が `0.5` 付近でも、distinguisher が同じroundで baseline 付近になるとは限らない。

## Next

- 13 rounds の `output_bit_index=255` が seed追加後も残るか確認する: #42
- 9-15 rounds の distinguisher baseline と比較し、avalanche の境界と識別困難性の境界が一致するか確認する: #19
