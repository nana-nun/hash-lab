# A Deeper Look at Machine Learning-Based Cryptanalysis

## Citation

- Authors: Adrien Benamira, David Gerault, Thomas Peyrin, and Quan Quan Tan
- Year: 2021
- Link: https://eprint.iacr.org/2021/287
- BibTeX key: `benamira_deeper_2021`

## Summary

Gohr 型 neural distinguisher が何を学んでいるのかを掘り下げる文献。ML classifier の精度をそのまま新しい暗号解析能力と見るのではなく、差分分布や既存の統計的構造との関係を調べる必要があることを示す。

hash-lab では neural distinguisher の解釈を慎重にするための主軸文献として扱う。特に、accuracy が baseline を超えたときに「未知の構造を学習した」とすぐ主張せず、単純統計や既知の偏りとの差分を見る理由になる。

## Important Ideas

- neural distinguisher の内部は、既存の差分的な情報に近いものを利用している可能性がある。
- ML の結果は、baseline、特徴量、入力差分、データ生成方法に強く依存する。
- 解釈可能性を確認しないと、精度の高さを過大評価しやすい。
- classical distinguisher と neural distinguisher を対立させるより、何を補っているかを調べる方が有益。

## Relation to hash-lab

`mini-sha` の現在の distinguisher 実験では、2 rounds は logistic regression で識別でき、4/8/16 rounds は baseline 付近に留まっている。この結果を読むとき、Benamira et al. は「ML が見ている信号は何か」を確認するための注意書きになる。

次に MLP を導入する場合でも、まず bit frequency、low-order statistics、logistic regression weights を保存し、deep model がそれ以上の情報を使っているかを分けて見る。

## Questions

- `mini-sha` の 2 rounds で logistic regression が学習している重みは、出力bitの偏りそのものか。
- 4/8/16 rounds で train accuracy だけ上がる場合、それは構造学習ではなく過学習として説明できるか。
- neural distinguisher の説明用に、どの可視化を最小で追加すべきか。
