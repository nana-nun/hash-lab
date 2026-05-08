# mini-sha ラウンド数別 Avalanche CSV

## Question

mini-sha の round 数を増やすと、入力 1 bit 反転時の mean flip ratio は 0.5 に近づくか。

## Hypothesis

round 数が増えるほど拡散が強くなり、mean flip ratio は 0.5 に近づく。

## Setup

- Command: `.\.venv\Scripts\python.exe -m src.hash_lab.cli avalanche --rounds 2 4 8 16 32 --samples 500 --seed 1`
- Seed: `1`
- Hash / rounds: `mini-sha / 2, 4, 8, 16, 32`
- Dataset size: 各 round 設定あたり `500 samples`
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

2 round と 4 round では拡散が弱く、mean flip ratio は 0.5 から大きく離れている。また、一部のサンプルでは出力bitの反転が発生していない。8 round では拡散が改善するが、理想的な 0.5 にはまだ届いていない。16 round と 32 round では mean が 0.5 にかなり近く、stdev も小さくなるため、このサンプルサイズでは仮説と整合する結果になった。

## Limitations

- 対象は toy SHA-like hash であり、SHA-256 ではない。
- seed は `1` のみで、各 round 設定あたり 500 samples だけを測定した。
- 測定対象は入力 1 bit 反転と、出力bit反転率の集計値に限られる。
- 信頼区間や複数seedでの安定性確認はまだ行っていない。

## Next

- 複数seedとより大きな sample size で再実行する。
- 今後の実装Issueで、CLIからJSONまたはCSVを直接保存できるようにする。
- random-output baseline と比較する。
