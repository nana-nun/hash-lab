# mini-sha Avalanche 不確実性指標

## Question

`mini-sha` の round別 mean flip ratio について、複数seedの結果から見ると、どのroundを `0.5` 付近と解釈できるか。

## Hypothesis

16/32 rounds の mean flip ratio は簡易的な不確実性指標を見ても `0.5` 付近に収まる。一方、8 rounds 以下は `0.5` から明確に離れる。

## Setup

- Command: `.\.venv\Scripts\python.exe -c "<inline script>"`
- Executed at: `2026-05-09T23:19:05+09:00`
- Source: `results/2026-05-09-avalanche-mini-sha-multi-seed/seed_metrics.csv`
- Seeds: `1, 2, 3, 4, 5`
- Hash / rounds: `mini-sha` / `2, 4, 8, 16, 32`
- Dataset size: 各seed・各round設定あたり `2000 samples`
- Model config: none

## Baseline

理想的な random-like avalanche の期待値として、mean flip ratio `0.5` を baseline にした。

不確実性の単位は seed ごとの mean flip ratio とした。roundごとに5個の seed mean から、sample standard deviation、standard error、df=4 の t分布を使った両側95%区間を計算した。

## Result

詳細なCSVは `uncertainty_metrics.csv` に保存した。

| rounds | mean_of_means | sample_stdev | standard_error | 95% CI | baseline_delta | delta 95% CI | includes 0.5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2 | 0.014140 | 0.000937 | 0.000419 | [0.012977, 0.015303] | -0.485860 | [-0.487023, -0.484697] | no |
| 4 | 0.083360 | 0.003141 | 0.001404 | [0.079461, 0.087259] | -0.416640 | [-0.420539, -0.412741] | no |
| 8 | 0.325880 | 0.005360 | 0.002397 | [0.319224, 0.332536] | -0.174120 | [-0.180776, -0.167464] | no |
| 16 | 0.500120 | 0.000864 | 0.000387 | [0.499047, 0.501193] | 0.000120 | [-0.000953, 0.001193] | yes |
| 32 | 0.499880 | 0.000522 | 0.000233 | [0.499232, 0.500528] | -0.000120 | [-0.000768, 0.000528] | yes |

## Interpretation

2/4/8 rounds は、seed間のばらつきを入れた簡易95%区間でも baseline `0.5` から大きく離れている。今回の条件では、8 rounds 以下は random-like avalanche に達していないと解釈できる。

16/32 rounds は、mean が `0.5` に非常に近く、簡易95%区間も `0.5` を含む。今回の seed集合と samples では、16 rounds 以上を `0.5` 付近に安定していると書く根拠は前回より少し強くなった。

ただし、この区間は seed mean を5点だけ使った探索的な不確実性指標であり、入力サンプル単位の厳密な独立性や roundごとの分布形までは検証していない。したがって「16 rounds 以上で完全に理想的」とは言わず、「この測定条件では baseline 0.5 と矛盾しにくい」程度に留める。

## Limitations

- seed は `1..5` の5個だけ。
- 既存結果の集計値から計算しており、生の per-sample flip ratio から bootstrap したものではない。
- t区間は seed mean の分布を簡易的に扱ったもので、厳密な統計検定ではない。
- round 9から15の境界領域は含めていない。
- 出力bit位置ごとの偏りは評価していない。

## Next

- round 9から15の中間領域を測定し、`0.5` 付近へ移る境界を細かく見る: #9
- 出力bit位置ごとの flip rate を保存し、特定bitに偏りが残るか確認する: #8
- per-sample flip ratio を保存し、bootstrap confidence interval を計算する: #22
