# mini-sha 13 rounds bit255 seed階層CI

## Question

`mini-sha` 13 rounds の `output_bit_index=255` に残った偏りは、seedを合算せず seed単位の不確実性として見ても baseline `0.5` と矛盾するか。

## Hypothesis

seed階層で区間推定すると、Issue #42 の合算二項近似より不確実性が広がり、bit255 の baseline `0.5` との差は弱く見える。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche-bit-seed-ci --rounds 13 --output-bits 255 --bit-input results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_metrics.csv --pooled-ci-input results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/bit_ci_metrics.csv --seed-output results/2026-05-10-avalanche-mini-sha-13-bit255-seed-ci/seed_bit_metrics.csv --summary-output results/2026-05-10-avalanche-mini-sha-13-bit255-seed-ci/seed_ci_summary.csv --bootstrap-iterations 10000 --bootstrap-seed 20260510`
- Executed at: `2026-05-10T18:57:00+09:00`
- Hash / rounds: `mini-sha` / `13`
- Output bit: `255`
- Seeds: `1..20`
- Dataset size: 各seed `2000 samples`、合計 `40000 samples`
- CI: seed別 flip rate の percentile bootstrap 95% CI
- Bootstrap iterations: `10000`
- Bootstrap seed: `20260778`
- Model config: none

保存ファイル:

- `seed_bit_metrics.csv`: seed別の bit255 flip count、flip rate、baseline delta。
- `seed_ci_summary.csv`: seed mean bootstrap CI と Issue #42 の pooled Wilson CI との比較。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche の期待値として、`output_bit_index=255` の flip rate `0.5` を baseline にした。

## Result

seed別 flip rate は `0.468500` から `0.502500` まで広がった。seed mean は pooled flip rate と同じ `0.483950` だった。

| metric | value |
| --- | ---: |
| seed_count | 20 |
| samples_per_seed | 2000 |
| total_samples | 40000 |
| pooled_flip_rate | 0.483950 |
| seed_mean_flip_rate | 0.483950 |
| seed_min_flip_rate | 0.468500 |
| seed_max_flip_rate | 0.502500 |
| seed_mean bootstrap CI | `[0.479425, 0.488675]` |
| baseline_delta | -0.016050 |
| baseline_delta CI | `[-0.020575, -0.011325]` |
| CI contains baseline 0.5 | False |

Issue #42 の合算 Wilson CI との比較:

| method | CI | contains 0.5 |
| --- | ---: | --- |
| pooled Wilson score | `[0.479054, 0.488849]` | False |
| seed mean percentile bootstrap | `[0.479425, 0.488675]` | False |

## Interpretation

仮説は支持されなかった。seed階層を seed別 flip rate の bootstrap として扱っても、CI は Issue #42 の合算 Wilson CI とほぼ同じ幅に留まり、baseline `0.5` を含まなかった。

一方で seed別の値は一様ではない。seed `5`, `10`, `20` は `0.5` 付近または少し上にあり、全seedで同じ強さの低下が出ているわけではない。それでも 20 seed の seed mean としては、bit255 の低い flip rate は今回の条件では残差偏り候補として残る。

## Limitations

- bootstrap は seed別 flip rate 20点を再標本化したもので、各seed内の binomial sampling uncertainty は別にはモデル化していない。
- seeds は `1..20` の連番であり、より広い seed範囲では結果が変わる可能性がある。
- 対象は `rounds=13`、`output_bit_index=255` のみで、他の rejected bits との seed階層比較は未実施。
- bit255 の偏りが入力bit位置や内部状態のどこに由来するかは、この実験では分からない。

## Next

- #44 で入力bit位置別に `output_bit_index=255` への flip rate を測定し、偏りが局在するか確認する。
- 13 rounds で Holm補正後に残った `225, 228, 231, 254, 255` の seed階層CIを横並びで比較する: #47
