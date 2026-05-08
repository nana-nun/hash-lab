# mini-sha 複数seed Avalanche 再測定

## Question

Issue #1 の single-seed avalanche 結果は、seed を変えても再現するか。

## Hypothesis

16 round 以上では、複数seedでも mean flip ratio は 0.5 付近で安定する。2, 4, 8 round では、低roundほど 0.5 からの乖離が残る。

## Setup

- Command: `.\.venv\Scripts\python.exe -c "<inline script>"`
- Seeds: `1, 2, 3, 4, 5`
- Hash / rounds: `mini-sha / 2, 4, 8, 16, 32`
- Dataset size: 各seed・各round設定あたり `2000 samples`
- Model config: none

Inline script:

```python
from src.hash_lab.experiments import avalanche
import statistics

rounds = [2, 4, 8, 16, 32]
seeds = [1, 2, 3, 4, 5]
samples = 2000

print("seed,rounds,samples,mean,stdev,min,max")
rows = []
for seed in seeds:
    for rounds_value in rounds:
        result = avalanche(rounds_value, samples=samples, seed=seed)
        rows.append((seed, rounds_value, result))
        print(
            f"{seed},{rounds_value},{result.samples},"
            f"{result.mean:.4f},{result.stdev:.4f},"
            f"{result.minimum:.4f},{result.maximum:.4f}"
        )

print("---aggregate---")
print("rounds,seeds,samples_per_seed,mean_of_means,stdev_of_means,min_mean,max_mean")
for rounds_value in rounds:
    means = [result.mean for _, row_rounds, result in rows if row_rounds == rounds_value]
    print(
        f"{rounds_value},{len(seeds)},{samples},"
        f"{statistics.mean(means):.4f},{statistics.pstdev(means):.4f},"
        f"{min(means):.4f},{max(means):.4f}"
    )
```

## Baseline

Issue #1 の single-seed 結果を baseline とする。Issue #1 では seed `1`、各round設定あたり `500 samples` で測定した。

| rounds | Issue #1 mean |
| ---: | ---: |
| 2 | 0.0145 |
| 4 | 0.0789 |
| 8 | 0.3146 |
| 16 | 0.4996 |
| 32 | 0.4989 |

## Result

seed別の結果は `seed_metrics.csv`、round別の集約結果は `aggregate_metrics.csv` に保存した。

| rounds | seeds | samples/seed | mean_of_means | stdev_of_means | min_mean | max_mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 5 | 2000 | 0.0142 | 0.0009 | 0.0128 | 0.0151 |
| 4 | 5 | 2000 | 0.0834 | 0.0028 | 0.0791 | 0.0863 |
| 8 | 5 | 2000 | 0.3259 | 0.0048 | 0.3175 | 0.3321 |
| 16 | 5 | 2000 | 0.5001 | 0.0008 | 0.4988 | 0.5011 |
| 32 | 5 | 2000 | 0.4999 | 0.0005 | 0.4992 | 0.5005 |

## Interpretation

Issue #1 の観察はおおむね再現した。2 round と 4 round は複数seedでも 0.5 から大きく離れ、8 round でも 0.5 には届かない。一方で、16 round と 32 round はどのseedでも mean がほぼ 0.5 付近にあり、seed間の mean のばらつきも小さい。今回の条件では、16 round 以上で avalanche effect が安定しているように見える。

Issue #1 との違いとして、4 round と 8 round の mean は少し高くなった。これは samples を 500 から 2000 に増やした影響、または seed集合によるばらつきの可能性がある。ただし、round数が増えるほど 0.5 に近づくという全体傾向は変わらない。

## Limitations

- 対象は toy SHA-like hash であり、SHA-256 ではない。
- seed は `1..5` の5個だけで、網羅的なseed探索ではない。
- 各round設定あたり 2000 samples のため、より細かい信頼区間評価には不足する可能性がある。
- 測定対象は入力 1 bit 反転時の集計的な出力bit反転率だけで、bit位置ごとの偏りは見ていない。

## Next

- round 9から15の中間領域を測定し、0.5 付近へ移る境界を細かく見る: #9
- 出力bit位置ごとの flip rate を保存し、特定bitに偏りが残るか確認する: #8
- CLIにCSV/JSON保存オプションを追加して、手動保存を減らす: #4
