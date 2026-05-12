# Results Index

このディレクトリは、保存済み実験結果の索引です。AIエージェントは新しい分析を始める前に、このファイルと該当する `notes.md`、metrics CSV/JSON、`docs/research-state.md` を確認してください。

## Experiments

| Directory | Type | Key Files | Summary |
| --- | --- | --- | --- |
| `2026-05-09-avalanche-mini-sha/` | avalanche | `metrics.csv`, `notes.md` | `mini-sha` の single-seed avalanche 初期測定。round 数が増えるほど mean flip ratio が `0.5` に近づく傾向を確認。 |
| `2026-05-09-avalanche-mini-sha-multi-seed/` | avalanche | `seed_metrics.csv`, `aggregate_metrics.csv`, `notes.md` | seeds `1..5`、各round `2000 samples`。16/32 rounds は複数seedでも `0.5` 付近。 |
| `2026-05-10-avalanche-mini-sha-rounds-9-15/` | avalanche | `seed_metrics.csv`, `aggregate_metrics.csv`, `config.json`, `notes.md` | 9-15 rounds の中間領域を測定。12 rounds は `0.493620`、13 rounds 以降は `0.5` 付近で、主な境界は12から13 rounds の間に見える。 |
| `2026-05-10-avalanche-mini-sha-bit-positions-9-15/` | avalanche bit positions | `bit_metrics.csv`, `round_summary.csv`, `config.json`, `notes.md` | 9-15 rounds の出力bit位置別 flip rate を測定。9-12 rounds はbit別偏りが残り、13-15 rounds で min/max も `0.5` 付近に近づく。 |
| `2026-05-10-avalanche-mini-sha-bit-ci-9-15/` | avalanche bit positions | `bit_ci_metrics.csv`, `round_summary.csv`, `config.json`, `notes.md` | 9-15 rounds の出力bit位置ごとの Wilson CI と Holm補正を計算。12 rounds は補正後 `35` bit が棄却、13 rounds は `1` bit、14/15 rounds は `0` bit。 |
| `2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/` | avalanche bit positions | `bit_metrics.csv`, `bit_ci_metrics.csv`, `round_summary.csv`, `bit_ci_summary.csv`, `config.json`, `notes.md` | 13 rounds の bit255 を seeds `1..20` で確認。bit255 は flip rate `0.483950` で補正後も棄却され、13 rounds の Holm reject count は `5`、14 rounds は `0`。 |
| `2026-05-10-avalanche-mini-sha-13-bit255-seed-ci/` | avalanche uncertainty | `seed_bit_metrics.csv`, `seed_ci_summary.csv`, `config.json`, `notes.md` | 13 rounds bit255 を seed別 flip rate の bootstrap で区間推定。95% CI は `[0.479425, 0.488675]` で baseline `0.5` を含まない。 |
| `2026-05-12-avalanche-mini-sha-13-rejected-bits-seed-ci/` | avalanche uncertainty | `seed_bit_metrics.csv`, `seed_ci_summary.csv`, `config.json`, `notes.md` | 13 rounds で Holm補正後に残った `225, 228, 231, 254, 255` を seed階層CIで比較。5bitすべての95% CIが baseline `0.5` を含まない。 |
| `2026-05-12-avalanche-mini-sha-13-bit255-input-bits/` | avalanche input bit positions | `seed_input_bit_metrics.csv`, `input_bit_ci_metrics.csv`, `summary.csv`, `compute_input_bit_bias.py`, `config.json`, `notes.md` | 13 rounds bit255 を入力bit位置別に測定。Holm補正後 `32` input bits が baseline `0.5` と矛盾し、偏りは input bits `224..254` 付近に強く局在。 |
| `2026-05-10-avalanche-mini-sha-12-13-ci/` | avalanche uncertainty | `per_sample_flip_ratios.csv`, `per_sample_bootstrap_metrics.csv`, `seed_bootstrap_metrics.csv`, `config.json`, `notes.md` | 12/13 rounds の境界CIを計算。12 rounds は両CIで `0.5` を含まず、13 rounds は seed階層CIで `0.5` を含む。 |
| `2026-05-09-avalanche-mini-sha-uncertainty/` | avalanche uncertainty | `uncertainty_metrics.csv`, `config.json`, `notes.md` | seed mean から標準誤差と簡易95% t区間を計算。2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-10-avalanche-mini-sha-bootstrap/` | avalanche uncertainty | `per_sample_flip_ratios.csv`, `bootstrap_metrics.csv`, `config.json`, `notes.md` | per-sample flip ratio を保存し、percentile bootstrap 95% CI を計算。2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-10-avalanche-mini-sha-bit-positions/` | avalanche bit positions | `bit_metrics.csv`, `round_summary.csv`, `config.json`, `notes.md` | 出力bit位置ごとの flip rate を測定。2/4/8 rounds はbit別にも大きく偏り、16/32 rounds は aggregate min/max も `0.5` 付近。 |
| `2026-05-10-avalanche-mini-sha-bit-ci/` | avalanche bit positions | `bit_ci_metrics.csv`, `round_summary.csv`, `config.json`, `notes.md` | 出力bit位置ごとの Wilson CI と Holm補正を計算。2/4/8 rounds は全bitで偏り、16/32 rounds は補正後に棄却されるbitなし。 |
| `2026-05-10-avalanche-mini-sha-seed-bootstrap/` | avalanche uncertainty | `seed_bootstrap_metrics.csv`, `config.json`, `notes.md` | seed階層を保つ percentile bootstrap 95% CI を計算。per-sample bootstrap より少し広いが、2/4/8 rounds は baseline `0.5` を含まず、16/32 rounds は含む。 |
| `2026-05-12-avalanche-mini-sha-16-32-seed-count/` | avalanche uncertainty | `per_sample_flip_ratios.csv`, `per_sample_bootstrap_metrics.csv`, `seed_bootstrap_metrics.csv`, `config.json`, `notes.md` | 16/32 rounds の seed数を `1..20` に増やして seed階層bootstrap CIを計算。両roundとも baseline `0.5` を含み、Issue #29 よりCIが少し狭まった。 |
| `2026-05-09-distinguish-baseline/` | distinguisher | `metrics.csv`, `config.json`, `notes.md` | logistic regression の seed `1` baseline。2 rounds は識別可能、4/8/16 rounds は random guess 付近。 |
| `2026-05-09-distinguish-baseline-multi-seed/` | distinguisher | `seed_metrics.csv`, `aggregate_metrics.csv`, `config.json`, `notes.md` | seeds `1..5` の distinguisher baseline。2 rounds は強く識別可能、4/8/16 rounds は平均で baseline 付近。 |
| `2026-05-10-distinguish-size-epochs-sensitivity/` | distinguisher | `seed_metrics.csv`, `aggregate_metrics.csv`, `config.json`, `notes.md` | samples `500,1000,2000` と epochs `4,8,16` の感度測定。2 rounds は強く識別可能、4/8/16 rounds は平均で baseline 付近。 |
| `2026-05-12-distinguish-baseline-delta-ci/` | distinguisher uncertainty | `baseline_delta_ci.csv`, `seed_baseline_deltas.csv`, `compute_ci.py`, `config.json`, `notes.md` | Issue #18 の 4/8/16 rounds について `test_accuracy_minus_baseline` の seed階層CIを計算。27条件中26条件でCIが `0` を含み、残り1条件は負方向。 |
| `2026-05-10-avalanche-distinguisher-round-comparison/` | comparison | `round_comparison.csv`, `config.json`, `notes.md` | avalanche、bit位置偏り、distinguisher baseline差分をround別に横比較。4/8 rounds は avalanche 側に偏りが残るが logistic regression test delta は baseline 付近。 |

## Reading Order

実験結果を解釈するときは、次の順で読む。

1. `docs/research-state.md`
2. この `results/README.md`
3. 該当する `results/<experiment>/notes.md`
4. 該当する metrics CSV/JSON
5. `references/notes/avalanche-neural-distinguisher-survey.md`

## Interpretation Rules

- `0.5` 付近という表現は、対象metric、seed数、samples、区間推定の方法を一緒に確認してから使う。
- single-seed の結果だけで安定性を主張しない。
- train accuracy と test accuracy を混同しない。
- neural/ML 実験では random guess、majority baseline、単純統計量との差を記録する。
- `Limitations` と `Next` は、既存Issueで covered されているか確認する。
