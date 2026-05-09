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
| `results/2026-05-09-avalanche-mini-sha-uncertainty/` | `2, 4, 8, 16, 32` | seed mean を単位に簡易95% t区間を計算。2/4/8 rounds は `0.5` を含まず、16/32 rounds は `0.5` を含む。 |

現在の解釈:

- 2/4/8 rounds は random-like avalanche には届いていない。
- 16/32 rounds は、現在の測定条件では baseline `0.5` と矛盾しにくい。
- ただし per-sample bootstrap、bit位置ごとの偏り、BIC 風指標はまだ未確認。

### mini-sha distinguisher

`mini-sha` の digest とランダムbit列を logistic regression で識別する実験では、2 rounds は明確に識別できるが、4/8/16 rounds は random guess baseline 付近に留まっている。

主要結果:

| Result | Rounds | Summary |
| --- | --- | --- |
| `results/2026-05-09-distinguish-baseline/` | `2, 4, 8, 16` | seed `1`、`samples=1000`、`epochs=8`。2 rounds は `test_accuracy=1.0`、4/8/16 rounds は `0.5` 付近。 |
| `results/2026-05-09-distinguish-baseline-multi-seed/` | `2, 4, 8, 16` | seeds `1..5`。2 rounds は平均 `test_accuracy_minus_baseline=0.4975`、4/8/16 rounds は平均で `0` 付近。 |

現在の解釈:

- 2 rounds は logistic regression でほぼ完全に識別できる。
- 4/8/16 rounds は train accuracy が上がっても test accuracy は baseline 付近で、汎化する識別信号は確認できていない。
- dataset size、epochs、MLP などのモデル差、信頼区間は未確認。

## Literature Context

読むべき先行研究メモ:

- `references/reading-list.md`
- `references/notes/avalanche-neural-distinguisher-survey.md`
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

- 9から15 rounds の中間領域で avalanche と distinguisher の境界は一致するか。
- 出力bit位置ごとの flip rate に偏りは残るか。
- per-sample bootstrap CI でも 16/32 rounds は `0.5` 付近と言えるか。
- dataset size と epochs を変えても distinguisher の test accuracy は baseline 付近に留まるか。
- neural/ML distinguisher が baseline を超えた場合、どのbit位置や差分構造を見ているか。
