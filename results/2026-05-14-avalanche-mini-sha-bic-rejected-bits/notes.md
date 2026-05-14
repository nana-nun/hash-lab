# mini-sha rejected bits BIC / output bit pair correlation 小規模測定

## Question

`avalanche-vectors` の sample-level `avalanche_hex` から、13 rounds の rejected output bits 周辺に output bit pair correlation が残っているか。12/13/14 rounds でその強さはどう変わるか。

## Hypothesis

13 rounds の rejected output bits `225, 228, 231, 254, 255` では、input bits `224..254` 付近の局在偏りと対応する pairwise correlation が残る。14 rounds では相関は弱まり、一部の局所pairだけに小さな残差が残る。

## Setup

- Command: `.\.venv\Scripts\python.exe results/2026-05-14-avalanche-mini-sha-bic-rejected-bits/compute_bic_pair_correlation.py`
- Executed at: `2026-05-14T08:59:48+09:00`
- Hash / rounds: `mini-sha` / `12, 13, 14`
- Input mode: fixed input bit
- Input bits: `224, 236, 248, 250, 254`
- Output bits: `225, 228, 231, 254, 255`
- Output bit pairs: 各round・各input bitごとに `10` pairs
- Seeds: `1..5`
- Dataset size: 各round・各input bit `5000 samples`
- Model config: none

保存ファイル:

- `compute_bic_pair_correlation.py`: sample-level vector生成とpair correlation集計スクリプト。
- `avalanche_vectors.csv`: `avalanche-vectors` 相当の sample-level `avalanche_hex`。
- `pair_correlation.csv`: output bit pairごとの joint count、flip rates、covariance、Pearson correlation。
- `summary.csv`: round別の最大絶対相関。
- `config.json`: 実行条件。

## Baseline

理想的な random-like avalanche では、同じ入力bit条件で output bit pair `(j, k)` の反転イベントはほぼ独立になり、covariance と Pearson correlation は `0` 付近になる。

## Result

round が増えるにつれて、最大絶対相関は大きく下がった。

| rounds | defined pair rows | max_abs_correlation | input bit | output bit pair | signed correlation |
| ---: | ---: | ---: | ---: | --- | ---: |
| 12 | 43 / 50 | 0.72943074 | 236 | `(254, 255)` | 0.72943074 |
| 13 | 50 / 50 | 0.56636973 | 236 | `(254, 255)` | -0.56636973 |
| 14 | 50 / 50 | 0.06761781 | 250 | `(225, 255)` | -0.06761781 |

絶対相関の大きいpair:

| rounds | input_bit_index | output bit pair | flip_rate_j | flip_rate_k | joint_rate_11 | covariance | Pearson correlation |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 12 | 236 | `(254, 255)` | 0.010200 | 0.019000 | 0.010200 | 0.01000620 | 0.72943074 |
| 12 | 248 | `(254, 255)` | 0.963400 | 0.070200 | 0.033600 | -0.03403068 | -0.70935468 |
| 13 | 236 | `(254, 255)` | 0.831800 | 0.258400 | 0.122200 | -0.09273712 | -0.56636973 |
| 12 | 250 | `(254, 255)` | 0.243000 | 0.478800 | 0.233200 | 0.11685160 | 0.54538641 |
| 12 | 248 | `(228, 231)` | 0.001600 | 0.006200 | 0.001400 | 0.00139008 | 0.44308003 |
| 13 | 250 | `(254, 255)` | 0.292400 | 0.363000 | 0.179600 | 0.07345880 | 0.33584447 |
| 14 | 250 | `(225, 255)` | 0.493000 | 0.577600 | 0.251400 | -0.03340680 | -0.06761781 |

12 rounds では一部の output bits が常に `0` になり、Pearson correlation が定義できないpairが `7` 件あった。これらは独立性以前に片方の反転率が退化している条件として扱う。

## Interpretation

仮説は探索的には支持された。12/13 rounds では `output_bit_index=254` と `255` の組に強い正負の相関が見え、特に input bit `236` と `248` で大きい。これは #74 / #75 で見えた後半 input bits の局在偏りが、単独output bitのflip rateだけでなく、output bit pairの同時反転構造にも現れている可能性を示す。

14 rounds では最大絶対相関が `0.06761781` まで下がった。これは 14 rounds の aggregate avalanche が `0.5` 付近に近づくという既存解釈と整合する。ただし、今回の条件では小さな相関が完全に消えたとは言えず、サンプル数や対象pairを増やして安定性を見る余地がある。

## Limitations

- 対象は fixed input bits `224, 236, 248, 250, 254` と output bits `225, 228, 231, 254, 255` だけで、全output bit pairではない。
- 各round・input bitは `5000 samples` であり、小さい相関の安定性評価には不足する可能性がある。
- Pearson correlation の信頼区間や多重比較補正はまだ計算していない。
- 12 rounds では反転率が `0` または `1` に近い退化条件があり、Pearson correlation が定義できないpairがある。
- toy / reduced-round `mini-sha` の局所測定であり、実SHA-256の安全性や攻撃可能性は主張しない。

## Next

- 14 rounds の小さい相関について、seed数またはsamplesを増やした再測定で安定性を見る。
- 全output bit pairへ広げる前に、pair数 `32640` に対する可視化と多重比較方針を決める。
- random input bit mode と fixed input bit mode を分けて比較し、局在条件を平均したときに相関が相殺されるか確認する。
