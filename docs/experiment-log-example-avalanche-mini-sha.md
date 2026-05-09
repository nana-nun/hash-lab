# 実験ノート例: mini-sha avalanche

このファイルは `docs/experiment-log-template.md` を使った実験ノート例です。初期実験として、toy hash である `mini-sha` の round 数別 avalanche effect を記録します。

関連Issue: [#5](https://github.com/nana-nun/hash-lab/issues/5)

関連結果: `results/2026-05-09-avalanche-mini-sha/`

## Question

`mini-sha` の round 数を増やすと、入力を 1 bit 反転したときの出力bit反転率は理想値の `0.5` に近づくか。

## Hypothesis

round 数が増えるほど内部状態の拡散が強くなり、平均出力bit反転率は `0.5` に近づく。

この段階では、`16 rounds` 以上で `0.5` 付近に近づくと予想する。ただし、これは実験前の仮説であり、結果ではない。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche --rounds 2 4 8 16 32 --samples 500 --seed 1`
- Seed: `1`
- Hash / rounds: `mini-sha / 2, 4, 8, 16, 32`
- Dataset size: 各 round 設定につき `500 samples`
- Model config: none。AI/MLモデルは使わず、入力 1 bit 反転時の Hamming distance を測定する。
- Metrics: `mean`, `stdev`, `min`, `max`

## Baseline

比較の基準は、理想的にランダム化された 256 bit 出力で期待される出力bit反転率 `0.5` とする。

この実験では、AIモデルを使わないため train/test accuracy のような学習baselineはない。代わりに、各roundの `mean` が `0.5` にどれだけ近いかを見て、拡散の弱いroundを見分ける。

## Result

実行結果は `results/2026-05-09-avalanche-mini-sha/metrics.csv` に保存されている。

| rounds | samples | mean | stdev | min | max |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 500 | 0.0145 | 0.0343 | 0.0000 | 0.1484 |
| 4 | 500 | 0.0789 | 0.1211 | 0.0000 | 0.4180 |
| 8 | 500 | 0.3146 | 0.1834 | 0.0078 | 0.6016 |
| 16 | 500 | 0.4996 | 0.0316 | 0.4062 | 0.5938 |
| 32 | 500 | 0.4989 | 0.0302 | 0.4102 | 0.5859 |

## Interpretation

2 rounds と 4 rounds では `mean` が `0.5` から大きく離れており、入力 1 bit の変化が出力全体へ十分に拡散していない。特に `min=0.0000` のサンプルがあり、出力bitがまったく変わらない場合が観測された。

8 rounds では `mean=0.3146` まで上がるが、まだ理想値 `0.5` には届いていない。

16 rounds と 32 rounds では `mean` が `0.5` に非常に近く、`stdev` も小さくなった。この小規模な測定では、仮説と整合する結果になった。

## Limitations

- 対象は研究用の toy SHA-like hash であり、SHA-256 そのものではない。
- seed は `1` のみ。
- 各 round の dataset size は `500 samples` のみ。
- 測定対象は入力 1 bit 反転時の出力bit反転率だけで、bit位置ごとの偏りや複数seedでのばらつきは未確認。
- この結果だけでは、識別器に対する学習不能性までは主張できない。

## Next

- 複数seedで再実行し、`mean` と `stdev` の安定性を確認する。
- 出力bit位置ごとの偏りを測定する。
- neural/ML distinguisher の結果と比較し、avalanche が良く見える round でも識別器が差を拾えるか確認する。

## References

- [Issue #5](https://github.com/nana-nun/hash-lab/issues/5)
- `AGENTS.md`
- `docs/experiment-log-template.md`
- `results/2026-05-09-avalanche-mini-sha/metrics.csv`
- `results/2026-05-09-avalanche-mini-sha/notes.md`
