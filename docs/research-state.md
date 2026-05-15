# hash-lab Research State

この文書は、AIエージェントと人間が「ここまで何が分かっているか」を短時間で確認するための現在地メモです。詳細な数値や解釈は各 `results/*/notes.md` と `references/notes/` を一次参照にしてください。

## Scope

hash-lab は、実運用中の SHA-256 やネットワークを攻撃するためのリポジトリではありません。対象は toy hash、reduced-round SHA-like hash、local simulation、avalanche 測定、baseline 付き distinguisher 実験です。

## Current Findings

### mini-sha avalanche

`mini-sha` の avalanche 測定では、round 数が増えるほど mean flip ratio が `0.5` に近づく傾向がある。

主要結果:

| Result | Rounds | Summary |
| --- | --- | --- |
| `results/2026-05-09-avalanche-mini-sha/` | `2, 4, 8, 16, 32` | single seed の小規模測定。16/32 rounds は `0.5` 付近、2/4/8 rounds は低い。 |
| `results/2026-05-09-avalanche-mini-sha-multi-seed/` | `2, 4, 8, 16, 32` | seeds `1..5`、各round `2000 samples`。16/32 rounds は複数seedでも `0.5` 付近。 |
| `results/2026-05-10-avalanche-mini-sha-rounds-9-15/` | `9, 10, 11, 12, 13, 14, 15` | 中間領域を測定。12 rounds は `0.493620`、13 rounds 以降は `0.5` 付近で、主な境界は12から13 rounds の間に見える。 |
| `results/2026-05-10-avalanche-mini-sha-bit-positions-9-15/` | `9, 10, 11, 12, 13, 14, 15` | 9-15 rounds の出力bit位置別測定。12 rounds は bit別最大差分 `0.046000` が残り、13-15 rounds は min/max も `0.5` 付近へ狭まる。 |
| `results/2026-05-10-avalanche-mini-sha-bit-ci-9-15/` | `9, 10, 11, 12, 13, 14, 15` | 9-15 rounds の出力bit位置ごとの Wilson CI と Holm補正を計算。12 rounds は補正後 `35` bit が棄却、13 rounds は `1` bit、14/15 rounds は `0` bit。 |
| `results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/` | `12, 13, 14` | seeds `1..20` で 13 rounds の bit255 を再確認。bit255 は flip rate `0.483950` で補正後も棄却され、13 rounds の Holm reject count は `5`、14 rounds は `0`。 |
| `results/2026-05-10-avalanche-mini-sha-13-bit255-seed-ci/` | `13` | 13 rounds bit255 を seed別 flip rate の bootstrap で区間推定。95% CI は `[0.479425, 0.488675]` で baseline `0.5` を含まず、合算 Wilson CI とほぼ同じ結論。 |
| `results/2026-05-12-avalanche-mini-sha-13-rejected-bits-seed-ci/` | `13` | 13 rounds で Holm補正後に残った `225, 228, 231, 254, 255` を seed階層CIで比較。5bitすべての95% CIが baseline `0.5` を含まず、bit255 が最も低い。 |
| `results/2026-05-12-avalanche-mini-sha-13-bit255-input-bits/` | `13` | 13 rounds bit255 を入力bit位置別に測定。Holm補正後 `32` input bits が baseline `0.5` と矛盾し、偏りは input bits `224..254` 付近に強く局在。 |
| `results/2026-05-12-avalanche-mini-sha-13-rejected-bits-input-localization/` | `13` | 13 rounds の rejected output bits `225, 228, 231, 254, 255` を入力bit位置別に比較。5bitすべてで input bits `224..254` 付近に強い局在偏りが見える。 |
| `results/2026-05-12-avalanche-mini-sha-12-14-bit255-input-bits/` | `12, 13, 14` | 12/13/14 rounds の bit255 を入力bit位置別に比較。Holm reject count は `61 -> 32 -> 10` と減り、14 rounds でも input bits `226..254` 付近に小さな局在偏りが残る。 |
| `results/2026-05-16-avalanche-mini-sha-input-output-heatmap/` | `12, 13, 14, 16` | 全 input bit x output bit の flip rate heatmap を探索的に測定。input bits `224..254` の平均絶対差分は 12 rounds `0.098593`、13 rounds `0.033291`、14 rounds `0.022493`、16 rounds `0.021961` で、12/13 rounds の局在偏りが 14/16 rounds で大きく縮小。 |
| `results/2026-05-14-avalanche-mini-sha-bic-rejected-bits/` | `12, 13, 14` | `225, 228, 231, 254, 255` の output bit pair correlation を fixed input bits 小集合で測定。最大絶対相関は 12 rounds `0.729431`、13 rounds `0.566370`、14 rounds `0.067618`。 |
| `results/2026-05-10-avalanche-mini-sha-12-13-ci/` | `12, 13` | 12/13 rounds の per-sample CI と seed階層CIを計算。12 rounds は両CIで `0.5` を含まず、13 rounds は seed階層CIで `0.5` を含む。 |
| `results/2026-05-09-avalanche-mini-sha-uncertainty/` | `2, 4, 8, 16, 32` | seed mean を単位に簡易95% t区間を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |
| `results/2026-05-10-avalanche-mini-sha-bootstrap/` | `2, 4, 8, 16, 32` | per-sample flip ratio を保存し、percentile bootstrap 95% CI を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |
| `results/2026-05-10-avalanche-mini-sha-bit-positions/` | `2, 4, 8, 16, 32` | 出力bit位置ごとの flip rate を測定。2/4/8 rounds はbit別にも大きく偏り、16/32 rounds は aggregate min/max も `0.5` 付近。 |
| `results/2026-05-10-avalanche-mini-sha-bit-ci/` | `2, 4, 8, 16, 32` | 出力bit位置ごとの Wilson CI と Holm補正を計算。2/4/8 rounds は全bitで偏り、16/32 rounds は補正後に baseline との差を棄却するbitなし。 |
| `results/2026-05-10-avalanche-mini-sha-seed-bootstrap/` | `2, 4, 8, 16, 32` | seed階層を保つ percentile bootstrap 95% CI を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |
| `results/2026-05-12-avalanche-mini-sha-16-32-seed-count/` | `16, 32` | seed数を `1..20` に増やして seed階層bootstrap CIを計算。16 rounds は `[0.499729, 0.500629]`、32 rounds は `[0.499645, 0.500437]` で baseline `0.5` を含む。 |

現在の解釈:

- 2/4/8 rounds は random-like avalanche には届いていない。
- 9から12 rounds で mean flip ratio は急速に `0.5` へ近づく。12 rounds はCI込みでも `0.5` より低く、bit位置別にも最大差分 `0.046000` が残る。bit位置別CIでは 12 rounds は Holm補正後に `35` bit が baseline `0.5` と矛盾し、13 rounds は `1` bit、14/15 rounds は `0` bitまで減る。
- seeds `1..20` に増やすと、13 rounds の bit255 は差分が `-0.016050` に弱まるが補正後も baseline `0.5` と矛盾する。seed別 flip rate の bootstrap でも 95% CI は baseline `0.5` を含まない。Holm補正後に残った `225, 228, 231, 254, 255` も seed階層CIではすべて baseline `0.5` を含まず、13 rounds の局所的な残差偏り候補として残る。入力bit位置別測定では、5つの rejected output bits すべてで input bits `224..254` 付近に強い局在偏りが見え、aggregate 測定では正負の偏りが相殺されていた可能性が高い。bit255 を 12/13/14 rounds で横比較すると、入力bit位置別 Holm reject count は `61 -> 32 -> 10` と減り、14 rounds でも aggregate では見えにくい小さな局在偏りが残る。全 input bit x output bit heatmap でも、input bits `224..254` の平均絶対差分は 12/13 rounds で全体平均より大きく、14/16 rounds で全体平均付近まで縮小した。BIC風の小規模pair correlationでは、rejected output bits の最大絶対相関も 12 rounds `0.729431`、13 rounds `0.566370`、14 rounds `0.067618` と弱まった。
- 16/32 rounds の bit位置別の小さな差分は、round内256 bitの Holm補正後には baseline `0.5` との差として棄却されなかった。
- 16/32 rounds の aggregate mean は seeds `1..20` に増やしても seed階層bootstrap CI が baseline `0.5` を含み、seed数5個の Issue #29 と同じ解釈だった。
- ただし seed階層 bootstrap は seed集合と再標本化設計に依存する探索的な不確実性指標であり、全 output bit pair の BIC 風指標、heatmap 上位cellの追加samples確認、より広い入力差分方向はまだ未確認。

### mini-sha distinguisher

`mini-sha` の digest とランダムbit列を logistic regression で識別する実験では、2 rounds は明確に識別できるが、4/8/16 rounds は random guess baseline 付近に留まっている。

主要結果:

| Result | Rounds | Summary |
| --- | --- | --- |
| `results/2026-05-09-distinguish-baseline/` | `2, 4, 8, 16` | seed `1`、`samples=1000`、`epochs=8`。2 rounds は `test_accuracy=1.0`、4/8/16 rounds は `0.5` 付近。 |
| `results/2026-05-09-distinguish-baseline-multi-seed/` | `2, 4, 8, 16` | seeds `1..5`。2 rounds は平均 `test_accuracy_minus_baseline=0.4975`、4/8/16 rounds は平均で `0` 付近。 |
| `results/2026-05-10-distinguish-size-epochs-sensitivity/` | `2, 4, 8, 16` | samples `500,1000,2000`、epochs `4,8,16` のgrid。2 rounds は強く識別可能、4/8/16 rounds は全条件で平均 `test_accuracy_minus_baseline` が `-0.0160` から `0.0110` の範囲。 |
| `results/2026-05-12-distinguish-baseline-delta-ci/` | `4, 8, 16` | Issue #18 のgridについて `test_accuracy_minus_baseline` の seed階層CIを計算。27条件中26条件でCIが `0` を含み、残り1条件は負方向だった。 |
| `results/2026-05-10-avalanche-distinguisher-round-comparison/` | `2, 4, 8, 9..16, 32` | avalanche、bit位置偏り、distinguisherをround別に横比較。4/8 rounds は avalanche 側で偏りが大きいが、logistic regression の test delta は baseline付近。 |

現在の解釈:

- 2 rounds は logistic regression でほぼ完全に識別できる。
- 4/8/16 rounds は train accuracy が上がっても test accuracy は baseline 付近で、汎化する識別信号は確認できていない。dataset size と epochs を変えても、この傾向は今回のgridでは変わらなかった。seed階層CIでも 27条件中26条件は `test_accuracy_minus_baseline = 0` を含み、1条件だけ `0` を含まなかったが方向は負だった。
- 4/8 rounds は avalanche と bit位置偏りでは baseline から大きく離れるが、logistic regression distinguisher の test accuracy は baseline付近に留まる。avalanche 偏りがそのまま現在の線形distinguisherに使えるとは限らない。
- MLP などのモデル差と信頼区間は未確認。

## Literature Context

読むべき先行研究メモ:

- `references/reading-list.md`
- `references/notes/avalanche-neural-distinguisher-survey.md`
- `references/notes/webster-tavares-sboxes-1986.md`
- `references/notes/forre-strict-avalanche-1988.md`
- `references/notes/avalanche-criteria-limitations.md`
- `references/notes/upadhyay-avalanche-2022.md`
- `references/notes/gohr-speck-deep-learning-2019.md`
- `references/notes/benamira-deeper-look-2021.md`
- `references/papers.bib`

実験解釈との対応:

| Topic | Relevant References | Use in hash-lab |
| --- | --- | --- |
| Avalanche / SAC / GAC | Webster and Tavares 1986; Forré 1988; Lloyd 1992; Zhang and Zheng 1995 | `mean flip ratio = 0.5` を baseline にする背景。SAC、BIC、propagation criterion、GAC の違いを踏まえ、avalanche だけで安全性全体を主張しないための注意。 |
| Hash avalanche measurement | Upadhyay et al. 2022 | SAC、BIC、randomness tests など、今後の測定項目を増やす参考。 |
| Reduced-round SHA-like cryptanalysis | Gilbert and Handschuh 2003; Sanadhya and Sarkar 2008; Nikolić and Biryukov 2008; Biryukov et al. 2011 | reduced-round 実験を本物の SHA-256 攻撃と混同せず、toy/local な比較対象として位置づける。 |
| Neural distinguisher | Gohr 2019; Benamira et al. 2021; Brunetta and Picazo-Sanchez 2022 | ML classifier の精度だけでなく、baseline、単純統計、解釈可能性を見る理由。 |
| Hash function + deep learning | Jeong and Moon 2024 | hash function 寄りの最近例。短い論文なので補助的に扱う。 |

## Analysis Checklist for AI Agents

新しい実験や分析を始める前に、AIエージェントは次を確認する。

1. `AGENTS.md` で安全範囲を確認する。
2. 対応する Issue と label skill を読む。
3. この `docs/research-state.md` を読み、既存結果と未確認事項を確認する。
4. 関連する `results/*/notes.md` と metrics CSV/JSON を読む。
5. 関連する `references/reading-list.md` と `references/notes/` を確認する。
6. 仮説、baseline、結果、解釈、制限を混ぜない。
7. `Limitations` と `Next` に具体的な未対応事項があれば、既存Issueで covered されているか確認し、未coveredなら follow-up Issue にする。

## Open Questions

- 12/13 rounds 周辺の avalanche 境界は不確実性込みでも同じ位置に見えるか。
- 9から15 rounds と32 rounds で、logistic regression distinguisher も baseline 付近に留まるか。
- 出力bit位置ごとの小さな差分は seed数を増やしても sampling noise と矛盾しないか。
- seed数を増やしても 16/32 rounds は `0.5` 付近と言えるか。
- logistic regression より容量の大きいモデルでも distinguisher の test accuracy は baseline 付近に留まるか。
- neural/ML distinguisher が baseline を超えた場合、どのbit位置や差分構造を見ているか。
