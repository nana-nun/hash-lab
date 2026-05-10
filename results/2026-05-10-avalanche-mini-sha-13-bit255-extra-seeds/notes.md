# mini-sha 13 rounds bit255 追加seed確認

## Question

`mini-sha` 13 rounds の `output_bit_index=255` で Issue #40 に残った偏りは、seed数を増やしても baseline `0.5` と矛盾するか。

## Hypothesis

13 rounds の bit255 の偏りは seedを増やすと弱まり、Holm補正後には baseline `0.5` と矛盾しにくくなる。

## Setup

- Command 1: `C:\Users\nanau\source\hash-lab\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bits --rounds 12 13 14 --samples 2000 --seeds 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 --bit-output results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/round_summary.csv`
- Command 2: `C:\Users\nanau\source\hash-lab\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bit-ci --rounds 12 13 14 --bit-input results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_metrics.csv --bit-ci-output results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_ci_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_ci_summary.csv`
- Executed at: `2026-05-10T10:11:31+09:00`
- Hash / rounds: `mini-sha` / `12, 13, 14`
- Seeds: `1..20`
- Dataset size: 各seed・各round `2000 samples`、round/bitごとに合計 `40000 samples`
- Output: `256` bits
- CI: Wilson score 95% CI
- Multiple comparison: round内256 bitに対する Holm 補正、`alpha=0.05`
- Model config: none

保存ファイル:

- `bit_metrics.csv`: seed別・round別・bit位置別の flip count と flip rate。
- `round_summary.csv`: round別の aggregate mean、bit位置別 min/max、最大baseline差分。
- `bit_ci_metrics.csv`: round/bit別の Wilson CI、raw p-value、Holm補正後 p-value。
- `bit_ci_summary.csv`: round別の reject count と CI excludes baseline count。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として、各出力bit位置の flip rate `0.5` を baseline にした。

## Result

round別 summary:

| rounds | mean_flip_rate | min_flip_rate | min_bit_index | max_flip_rate | max_bit_index | max_abs_delta_from_0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 0.493308 | 0.448125 | 255 | 0.507350 | 67 | 0.051875 |
| 13 | 0.499466 | 0.483950 | 255 | 0.509025 | 119 | 0.016050 |
| 14 | 0.499940 | 0.493450 | 153 | 0.506125 | 168 | 0.006550 |

CI と Holm補正 summary:

| rounds | total_samples_per_bit | min_flip_rate | max_flip_rate | max_abs_delta_from_0.5 | CI excludes 0.5 count | Holm reject count |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 40000 | 0.448125 | 0.507350 | 0.051875 | 101 | 67 |
| 13 | 40000 | 0.483950 | 0.509025 | 0.016050 | 51 | 5 |
| 14 | 40000 | 0.493450 | 0.506125 | 0.006550 | 17 | 0 |

13 rounds の `output_bit_index=255`:

| total_samples | flip_count | flip_rate | Wilson CI | baseline_delta | raw p-value | Holm adjusted p-value | Holm reject |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 40000 | 19358 | 0.483950 | `[0.479054, 0.488849]` | -0.016050 | 1.4082286e-10 | 3.6050653e-08 | True |

13 rounds で Holm補正後に残ったbitは `225, 228, 231, 254, 255` の5個だった。

Issue #40 との比較:

| Condition | Seeds | Samples per round/bit | bit255 flip_rate | bit255 Holm adjusted p-value | 13 rounds Holm reject count |
| --- | ---: | ---: | ---: | ---: | ---: |
| Issue #40 | 1..5 | 10000 | 0.478400 | 0.0041793164 | 1 |
| This run | 1..20 | 40000 | 0.483950 | 3.6050653e-08 | 5 |

## Interpretation

仮説は部分的に外れた。bit255 の差分自体は `-0.021600` から `-0.016050` へ弱まったが、seed数と総sample数を増やしても baseline `0.5` とは矛盾したままだった。むしろ total samples per bit が `10000` から `40000` へ増えたため、Holm adjusted p-value は小さくなった。

13 rounds では bit255 が引き続き最小 flip rate で、追加seed後も局所的な残差偏りの候補として残った。ただし 12 rounds の Holm reject count `67` と比べると、13 rounds は `5` まで減っており、14 rounds は `0` だった。大局的には 12から13 rounds の間で bit位置別偏りが大きく弱まり、14 rounds では今回の補正条件で棄却されるbitは確認されなかった。

13 rounds の seed別 bit255 flip rate は `0.468500` から `0.502500` まで広がった。seed `5, 10, 20` は `0.5` 付近または少し上であり、全seedで一様に同じ強さの低下が出ているわけではない。

## Limitations

- p-value は baseline `0.5` の二項分布に対する正規近似であり、厳密二項検定ではない。
- round/bitごとに seedを合算しており、seed階層のばらつきを統計モデルとしては扱っていない。
- seeds は `1..20` で、より広い seed範囲や異なるsamples per seedでは結果が変わる可能性がある。
- Holm補正は round内256 bitを対象にした。12/13/14 rounds 全体をまたぐ補正ではない。
- bit255 の偏りが、入力bit位置や内部状態のどの構造に由来するかは未確認。

## Next

- 13 rounds の `output_bit_index=255` について、入力bit位置ごとの条件付き flip rate を測定し、特定入力bitに由来する偏りか確認する: #44
- 13 rounds の bit255 を seed階層 bootstrap または seed単位の区間推定で確認する: #45
