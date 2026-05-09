# mini-sha Avalanche bit位置別 Confidence Interval

## Question

`mini-sha` の出力bit位置ごとの flip rate について、16/32 rounds の小さなbit別差分は sampling noise と矛盾するか。

## Hypothesis

16/32 rounds の小さなbit別差分は、現在の sample size では sampling noise と矛盾しにくい。一方、2/4/8 rounds の大きな偏りは confidence interval を見ても baseline `0.5` から離れる。

## Setup

- Command: `C:\Users\nanau\source\hash-lab\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bit-ci --rounds 2 4 8 16 32 --bit-input results/2026-05-10-avalanche-mini-sha-bit-positions/bit_metrics.csv --bit-ci-output results/2026-05-10-avalanche-mini-sha-bit-ci/bit_ci_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-bit-ci/round_summary.csv`
- Executed at: `2026-05-10T02:42:55+09:00`
- Input: `results/2026-05-10-avalanche-mini-sha-bit-positions/bit_metrics.csv`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16, 32`
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
| 2 | 0.000000 | 0.062200 | 0.500000 | 256 | 256 |
| 4 | 0.003300 | 0.187200 | 0.496700 | 256 | 256 |
| 8 | 0.204900 | 0.442400 | 0.295100 | 256 | 256 |
| 16 | 0.487900 | 0.512100 | 0.012100 | 11 | 0 |
| 32 | 0.483400 | 0.516400 | 0.016600 | 17 | 0 |

## Interpretation

2/4/8 rounds は、全256 bitで Wilson 95% CI が baseline `0.5` を含まず、Holm補正後も全bitで baseline との差が残った。Issue #8 の「低roundではbit位置別にも大きく偏る」という解釈を、不確実性込みでも補強する。

16/32 rounds は、Wilson CI 単体ではそれぞれ 11 bit / 17 bit が baseline `0.5` を含まなかった。ただし round内256 bitの多重比較を Holm 補正すると、`alpha=0.05` で baseline を棄却するbitはなかった。今回の条件では、16/32 rounds の小さなbit別差分は sampling noise と矛盾しにくい。

この結果は Issue #8 の round summary と整合する。16/32 rounds の aggregate min/max は `0.5` 付近にあり、補正後のbit別検定でも大きな構造的偏りは確認できなかった。

## Limitations

- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- round/bitごとに seedを合算しており、seed階層のばらつきは明示的には扱っていない。
- seeds は `1..5` の5個だけ。
- Holm補正は round内256 bitを対象にした。round間を含めた全比較補正ではない。
- 入力bit位置ごとの条件付き偏りや bit independence は評価していない。

## Next

- seed数を増やして 16/32 rounds の bit別CIが同じ傾向を保つか確認する。
- round 9から15の中間領域で bit位置別CIを計算し、12/13 rounds 境界のbit別偏りを見る。
