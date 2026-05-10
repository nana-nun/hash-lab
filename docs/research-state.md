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
| `results/2026-05-10-avalanche-mini-sha-12-13-ci/` | `12, 13` | 12/13 rounds の per-sample CI と seed階層CIを計算。12 rounds は両CIで `0.5` を含まず、13 rounds は seed階層CIで `0.5` を含む。 |
| `results/2026-05-09-avalanche-mini-sha-uncertainty/` | `2, 4, 8, 16, 32` | seed mean を単位に簡易95% t区間を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |
| `results/2026-05-10-avalanche-mini-sha-bootstrap/` | `2, 4, 8, 16, 32` | per-sample flip ratio を保存し、percentile bootstrap 95% CI を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |
| `results/2026-05-10-avalanche-mini-sha-bit-positions/` | `2, 4, 8, 16, 32` | 出力bit位置ごとの flip rate を測定。2/4/8 rounds はbit別にも大きく偏り、16/32 rounds は aggregate min/max も `0.5` 付近。 |
| `results/2026-05-10-avalanche-mini-sha-bit-ci/` | `2, 4, 8, 16, 32` | 出力bit位置ごとの Wilson CI と Holm補正を計算。2/4/8 rounds は全bitで偏り、16/32 rounds は補正後に baseline との差を棄却するbitなし。 |
| `results/2026-05-10-avalanche-mini-sha-seed-bootstrap/` | `2, 4, 8, 16, 32` | seed階層を保つ percentile bootstrap 95% CI を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |

現在の解釈:

- 2/4/8 rounds は random-like avalanche には届いていない。
- 9から12 rounds で mean flip ratio は急速に `0.5` へ近づく。12 rounds はCI込みでも `0.5` より低く、bit位置別にも最大差分 `0.046000` が残る。bit位置別CIでは 12 rounds は Holm補正後に `35` bit が baseline `0.5` と矛盾し、13 rounds は `1` bit、14/15 rounds は `0` bitまで減る。
- seeds `1..20` に増やすと、13 rounds の bit255 は差分が `-0.016050` に弱まるが補正後も baseline `0.5` と矛盾する。seed別 flip rate の bootstrap でも 95% CI は baseline `0.5` を含まず、bit255 は残差偏り候補として残る。入力bit位置別の追加確認が必要。
- 16/32 rounds の bit位置別の小さな差分は、round内256 bitの Holm補正後には baseline `0.5` との差として棄却されなかった。
- ただし seed階層 bootstrap も seed数5個の探索的な指標であり、BIC 風指標や入力bit位置ごとの条件付き偏りはまだ未確認。

### mini-sha distinguisher

`mini-sha` の digest とランダムbit列を logistic regression で識別する実験では、2 rounds は明確に識別できるが、4/8/16 rounds は random guess baseline 付近に留まっている。

主要結果:

| Result | Rounds | Summary |
| --- | --- | --- |
| `results/2026-05-09-distinguish-baseline/` | `2, 4, 8, 16` | seed `1`、`samples=1000`、`epochs=8`。2 rounds は `test_accuracy=1.0`、4/8/16 rounds は `0.5` 付近。 |
| `results/2026-05-09-distinguish-baseline-multi-seed/` | `2, 4, 8, 16` | seeds `1..5`。2 rounds は平均 `test_accuracy_minus_baseline=0.4975`、4/8/16 rounds は平均で `0` 付近。 |
| `results/2026-05-10-distinguish-size-epochs-sensitivity/` | `2, 4, 8, 16` | samples `500,1000,2000`、epochs `4,8,16` のgrid。2 rounds は強く識別可能、4/8/16 rounds は全条件で平均 `test_accuracy_minus_baseline` が `-0.0160` から `0.0110` の範囲。 |

現在の解釈:

- 2 rounds は logistic regression でほぼ完全に識別できる。
- 4/8/16 rounds は train accuracy が上がっても test accuracy は baseline 付近で、汎化する識別信号は確認できていない。dataset size と epochs を変えても、この傾向は今回のgridでは変わらなかった。
- MLP などのモデル差と信頼区間は未確認。

## Literature Context

読むべき先行研究メモ:

- `references/reading-list.md`
- `references/notes/avalanche-neural-distinguisher-survey.md`
- `references/notes/webster-tavares-sboxes-1986.md`
- `references/notes/forre-strict-avalanche-1988.md`
- `references/notes/upadhyay-avalanche-2022.md`
- `references/notes/gohr-speck-deep-learning-2019.md`
- `references/notes/benamira-deeper-look-2021.md`
- `references/papers.bib`

実験解釈との対応:

| Topic | Relevant References | Use in hash-lab |
| --- | --- | --- |
| Avalanche / SAC | Webster and Tavares 1986; Forré 1988; Lloyd 1992 | `mean flip ratio = 0.5` を baseline にする背景。avalanche だけで安全性全体を主張しないための注意。 |
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
- 9から15 rounds の中間領域で avalanche と distinguisher の境界は一致するか。
- 出力bit位置ごとの小さな差分は seed数を増やしても sampling noise と矛盾しないか。
- seed数を増やしても 16/32 rounds は `0.5` 付近と言えるか。
- logistic regression より容量の大きいモデルでも distinguisher の test accuracy は baseline 付近に留まるか。
- neural/ML distinguisher が baseline を超えた場合、どのbit位置や差分構造を見ているか。
