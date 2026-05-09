# On the Design of S-Boxes

## Citation

- Authors: A. F. Webster and Stafford E. Tavares
- Year: 1986
- Link: https://doi.org/10.1007/3-540-39799-X_41
- BibTeX key: `webster_design_1986`

## Summary

S-box 設計の文脈で avalanche effect と Strict Avalanche Criterion を扱う基礎文献。入力の1 bitを変えたとき、各出力bitが確率 `1/2` で変わるべき、という見方を整理する出発点になる。

hash-lab では SHA-like な toy hash 全体を S-box と同じ対象として扱うわけではないが、bit flip 実験で `mean flip ratio = 0.5` を baseline にする理由を説明するための主軸文献として読む。

## Important Ideas

- avalanche effect は「入力差分が出力へ十分に拡散するか」を見る局所的な性質。
- SAC は入力bitと出力bitの組ごとに、反転確率が `1/2` に近いかを見る条件。
- 平均値だけでなく、入力bit位置と出力bit位置の組ごとの偏りを見る必要がある。
- avalanche が良いことは有用な設計条件だが、それだけで collision resistance や preimage resistance を保証しない。

## Relation to hash-lab

`mini-sha` の avalanche 測定では、round 数を増やすと mean flip ratio が `0.5` に近づくかを見ている。この文献は、その `0.5` を「ランダムらしい拡散」の期待値として扱う根拠になる。

次の実験では、平均値だけでなく出力bit位置ごとの flip rate を保存し、SAC 風に「どの入力bitがどの出力bitへ伝わりにくいか」を見ると、2/4/8 rounds の弱さをより具体的に説明できる。

## Questions

- `mini-sha` で input bit x output bit の flip matrix を保存すると、低roundの偏りは局所的に見えるか。
- mean flip ratio は `0.5` 付近でも、特定の出力bitだけ偏る round はあるか。
- SAC 風の測定を neural distinguisher の特徴量解釈とつなげられるか。
