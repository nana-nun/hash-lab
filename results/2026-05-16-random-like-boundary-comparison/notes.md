# random-like化するround境界の複数指標比較

## Question

`mini-sha` は何roundから random-like に見えるのか。aggregate mean、output bit別SAC風指標、input-output局在偏り、BIC pair correlation、ML distinguisher で同じ境界になるか。

## Hypothesis

単一の境界ではなく、指標ごとに見える境界はずれる。aggregate mean は 13 rounds で `0.5` 付近に見え始めるが、bit別・局在・BIC系の指標では 14 rounds 以降まで残差構造が見える可能性がある。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-16-random-like-boundary-comparison/compare_random_like_boundaries.py`
- Executed at: `2026-05-16`
- Input results:
  - `results/2026-05-10-avalanche-distinguisher-round-comparison/round_comparison.csv`
  - `results/2026-05-16-avalanche-mini-sha-input-output-heatmap/summary.csv`
  - `results/2026-05-16-avalanche-mini-sha-bic-all-output-pairs/summary.csv`
  - `results/2026-05-14-avalanche-mini-sha-bic-rejected-bits/summary.csv`
- Output files:
  - `round_metric_comparison.csv`
  - `boundary_summary.csv`
  - `config.json`
- Model config: none

## Baseline

各指標で次のような「random-likeに見える」探索的ルールを置いた。

- aggregate mean flip ratio: `abs(mean - 0.5) <= 0.001`
- output-bit SAC風指標: Holm補正後に baseline `0.5` と矛盾する output bit が `0`
- input-output heatmap: input bits `224..254` の平均絶対差分が全体平均に近づく
- BIC all output pairs: Holm補正後に独立性と矛盾する output bit pair が `0`
- logistic regression distinguisher: `abs(test accuracy - 0.5) <= 0.02`

これらは比較のための整理ルールであり、暗号学的安全性の定義ではない。

## Result

指標ごとの境界はずれた。

| Metric | random-like に見え始めるround | Evidence |
| --- | ---: | --- |
| aggregate mean flip ratio | 13 | 13-15 rounds は `abs(mean - 0.5) <= 0.001`。 |
| output-bit SAC風 Holm rejects | 14 | reject count は 12 rounds `35`、13 rounds `1`、14/15/16/32 rounds `0`。 |
| input-output localized heatmap | 14 | input bits `224..254` の mean abs delta は 12 rounds `0.098593`、13 rounds `0.033291`、14 rounds `0.022493`、16 rounds `0.021961`。 |
| BIC all output pairs, random input bit mode | 13 | 12 rounds は Holm補正後 `22` pairs、13/14/16 rounds は `0` pairs。 |
| BIC selected rejected bits, fixed input bits | 14 | max abs correlation は 12 rounds `0.729431`、13 rounds `0.566370`、14 rounds `0.067618`。 |
| logistic regression distinguisher | 4 | 2 rounds は強く識別可能、4/8/16 rounds は既存のlogistic runでは baseline付近。 |

## Interpretation

「12/13 rounds 境界」は aggregate mean と random input bit mode の BIC では見える。13 rounds から mean flip ratio は `0.5` にかなり近く、全 output bit pair correlation も random input bit mode では Holm補正後に残らなかった。

一方で、output bit別SAC風の Holm rejects、input-output局在heatmap、fixed input bit 条件の selected BIC では、13 rounds にまだ残差構造が見える。これらの指標では、より自然な境界は 13/14 rounds 付近になる。

logistic regression distinguisher は別の軸で、既存結果では 4/8/16 rounds が baseline付近に見える。ただし 9-15 rounds と32 rounds は未測定なので、avalanche境界と同じ軸で比較するには Issue #53 の結果が必要である。

## Limitations

- 境界判定ルールは探索的な整理用で、厳密な安全性定義ではない。
- input-output heatmap は各cell `320 samples` で、per-cell のCIや多重比較補正はない。
- BIC all output pairs は random input bit mode であり、fixed input bit の局所依存は相殺される可能性がある。
- selected BIC は小規模な fixed input bits / output bits の結果で、全pairではない。
- ML distinguisher は 9-15 rounds と32 rounds が未測定で、モデルも logistic regression に限られる。

## Next

- Issue #53 で 9-15 rounds と32 rounds の logistic regression distinguisher を測定し、avalanche境界と同じround軸で比較する。
- #94 で distinguisher が見ているbit寄与を確認し、avalanche / BIC の局所構造と接続する。
- #89 で入力差分を探索し、random input bit mode で相殺される局所依存を fixed delta で見直す。
