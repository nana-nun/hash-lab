# mini-sha Round-wise Avalanche CSV

## Question

mini-sha の round 数を増やすと、入力 1 bit 反転時の mean flip ratio は 0.5 に近づくか。

## Hypothesis

round 数が増えるほど拡散が強くなり、mean flip ratio は 0.5 に近づく。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche --rounds 2 4 8 16 32 --samples 500 --seed 1`
- Seed: `1`
- Hash / rounds: `mini-sha / 2, 4, 8, 16, 32`
- Dataset size: `500 samples per round setting`
- Model config: none

## Baseline

既存CLIの標準出力結果を baseline とした。CLI出力は `rounds,samples,mean,stdev,min,max` のCSV形式で、そのまま `metrics.csv` に保存した。

## Result

`metrics.csv` に round 数別の avalanche metrics を保存した。

| rounds | samples | mean | stdev | min | max |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 500 | 0.0145 | 0.0343 | 0.0000 | 0.1484 |
| 4 | 500 | 0.0789 | 0.1211 | 0.0000 | 0.4180 |
| 8 | 500 | 0.3146 | 0.1834 | 0.0078 | 0.6016 |
| 16 | 500 | 0.4996 | 0.0316 | 0.4062 | 0.5938 |
| 32 | 500 | 0.4989 | 0.0302 | 0.4102 | 0.5859 |

## Interpretation

2 and 4 rounds show weak diffusion: the mean flip ratio is far below 0.5 and some samples produce no output bit flips. At 8 rounds, diffusion improves but remains below the ideal 0.5 ratio. At 16 and 32 rounds, the mean is very close to 0.5 and the standard deviation becomes small, matching the hypothesis for this sample size.

## Limitations

- This is a toy SHA-like hash, not SHA-256.
- The result uses one seed and 500 samples per round setting.
- The experiment measures only single-bit input flips and aggregate output bit flips.
- No confidence interval or cross-seed stability check is included.

## Next

- Repeat with multiple seeds and larger sample sizes.
- Save JSON or CSV directly from the CLI in a future implementation issue.
- Compare this result with a random-output baseline.
