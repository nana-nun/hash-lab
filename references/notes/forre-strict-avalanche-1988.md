# The Strict Avalanche Criterion

## Citation

- Authors: Réjane Forré
- Year: 1988
- Link: https://www.iacr.org/cryptodb/data/paper.php?pubkey=1303
- BibTeX key: `forre_strict_1988`

## Summary

Strict Avalanche Criterion を Boolean function の spectral property として扱い、SAC をより構造的に理解するための文献。avalanche を単なる実験平均ではなく、Boolean function の性質として見るための背景を与える。

hash-lab では詳細なスペクトル解析をすぐ実装するより、まず toy / reduced-round hash の出力bitごとの偏り、bit間の依存、round数による変化を測るための理論的な地図として使う。

## Important Ideas

- SAC は Boolean function の出力が入力bit反転に対してどれだけ均等に変わるかを見る。
- spectral property として見ると、単純な flip ratio の平均よりも強い構造情報を扱える。
- avalanche の評価は bit単位だけでなく、Boolean function 全体の相関や線形性とも関係する。
- 実験で観測した偏りがノイズなのか構造なのかを分けるには、複数seedや信頼区間が必要になる。

## Relation to hash-lab

現在の `mini-sha` 実験は mean flip ratio と logistic regression distinguisher を別々に見ている。この文献は、両者の間に「bitごとの反転確率」「bit間相関」「低次統計量」という中間の観測項目を置く理由になる。

実装上は、まず per-output-bit flip rate と BIC 風のペア相関を小さく追加し、スペクトル解析は後続の研究課題として扱うのが安全で再現しやすい。

## Questions

- `mini-sha` の出力bitを Boolean function として見たとき、round数ごとの相関の落ち方はどう変わるか。
- 低roundで logistic regression が拾う信号は、SAC 違反と対応しているか。
- spectral property まで踏み込む前に、どの軽量な統計量を baseline として置くべきか。
