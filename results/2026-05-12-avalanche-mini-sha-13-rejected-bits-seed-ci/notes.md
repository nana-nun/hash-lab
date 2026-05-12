# mini-sha 13 rounds rejected bits seed階層CI比較

## Question

Issue #42 で 13 rounds の Holm補正後に残った `output_bit_index=225, 228, 231, 254, 255` は、seed階層で見ても baseline `0.5` と矛盾するか。

## Hypothesis

bit255 と近い bit254 は seed階層CIでも baseline `0.5` を含みにくい。一方で bit225, bit228, bit231 は seed単位で見ると不確実性が広がり、baseline `0.5` を含む可能性がある。

## Setup

- Command: `.\.venv\Scripts\python.exe -m hash_lab.cli avalanche-bit-seed-ci --rounds 13 --output-bits 225 228 231 254 255 --bit-input results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_metrics.csv --pooled-ci-input results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_ci_metrics.csv --seed-output results/2026-05-12-avalanche-mini-sha-13-rejected-bits-seed-ci/seed_bit_metrics.csv --summary-output results/2026-05-12-avalanche-mini-sha-13-rejected-bits-seed-ci/seed_ci_summary.csv --bootstrap-iterations 10000 --bootstrap-seed 20260512`
- Executed at: `2026-05-12T13:35:01+09:00`
- Hash / rounds: `mini-sha` / `13`
- Output bits: `225, 228, 231, 254, 255`
- Seeds: `1..20`
- Dataset size: 各seed `2000 samples`、各bit合計 `40000 samples`
- CI: seed別 flip rate の percentile bootstrap 95% CI
- Bootstrap iterations: `10000`
- Bootstrap seed: command base seed `20260512`。実際の行別 seed は `base + rounds + output_bit_index`。
- Model config: none

保存ファイル:

- `seed_bit_metrics.csv`: bitごとの seed別 flip count、flip rate、baseline delta。
- `seed_ci_summary.csv`: bitごとの seed mean bootstrap CI と pooled Wilson CI の比較。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として、各出力bit位置の flip rate `0.5` を baseline にした。

## Result

5つの rejected bits は、seed mean bootstrap CI でもすべて baseline `0.5` を含まなかった。

| output_bit_index | seed_mean_flip_rate | seed_min_flip_rate | seed_max_flip_rate | seed_mean bootstrap CI | baseline_delta CI | CI contains 0.5 | pooled Wilson CI |
| ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 225 | 0.489825 | 0.459500 | 0.504000 | `[0.485125, 0.494000]` | `[-0.014875, -0.006000]` | False | `[0.484927, 0.494725]` |
| 228 | 0.490200 | 0.478500 | 0.515000 | `[0.486725, 0.494125]` | `[-0.013275, -0.005875]` | False | `[0.485302, 0.495100]` |
| 231 | 0.489875 | 0.471500 | 0.510500 | `[0.485275, 0.494450]` | `[-0.014725, -0.005550]` | False | `[0.484977, 0.494775]` |
| 254 | 0.489550 | 0.462500 | 0.509500 | `[0.484900, 0.493775]` | `[-0.015100, -0.006225]` | False | `[0.484652, 0.494450]` |
| 255 | 0.483950 | 0.468500 | 0.502500 | `[0.479450, 0.488650]` | `[-0.020550, -0.011350]` | False | `[0.479054, 0.488849]` |

Issue #45 の bit255 単独結果との比較:

| Source | output_bit_index | seed_mean_flip_rate | seed_mean bootstrap CI | contains 0.5 |
| --- | ---: | ---: | ---: | --- |
| Issue #45 | 255 | 0.483950 | `[0.479425, 0.488675]` | False |
| This run | 255 | 0.483950 | `[0.479450, 0.488650]` | False |

bit255 は5bitの中で最も低く、baseline delta は `-0.016050` だった。他の4bitも `-0.009800` から `-0.010450` の低い flip rate を示した。

## Interpretation

仮説は半分外れた。bit254 と bit255 だけでなく、bit225, bit228, bit231 も seed階層CIで baseline `0.5` を含まなかった。Issue #42 の Holm補正後に残った5bitは、seed別平均を単位に見ても同じ方向の残差偏り候補として残る。

ただし、各bitの seed別範囲は広い。たとえば bit225 は `0.459500` から `0.504000`、bit228 は `0.478500` から `0.515000` まで動く。全seedで必ず baseline より低いわけではなく、20 seed の平均として低い、という結果に留める。

Issue #45 の bit255 CIとはほぼ同じ結論だった。bootstrap seed が異なるため境界値はわずかに違うが、bit255 が baseline `0.5` を含まない点は変わらない。

## Limitations

- bootstrap は seed別 flip rate 20点を再標本化したもので、各seed内の binomial sampling uncertainty は別にはモデル化していない。
- seeds は `1..20` の連番で、より広い seed範囲では結果が変わる可能性がある。
- 対象は Issue #42 で Holm補正後に残った5bitだけで、13 rounds の全bitを seed階層で再評価したものではない。
- この結果だけでは、偏りが入力bit位置、内部状態、または特定の差分伝播に由来するかは分からない。
- 実運用SHA-256への攻撃可能性を示す結果ではなく、toy/reduced-round の局所的な avalanche 残差の測定である。

## Next

- #44 で `output_bit_index=255` の入力bit位置別 flip rate を測定し、偏りが特定入力bitに局在するか確認する。
- #57 で 13 rounds bit255 と周辺bitの残差偏りを解釈するための reduced-round SHA-like 構造解析文献を整理する。
