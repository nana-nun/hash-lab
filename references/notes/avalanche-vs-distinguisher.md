# Avalanche指標とDistinguisher指標の違い

## Citation

- Webster and Tavares, *On the Design of S-Boxes*, 1986.
  - DOI: `10.1007/3-540-39799-X_41`
  - BibTeX key: `webster_design_1986`
- Forré, *The Strict Avalanche Criterion: Spectral Properties of Boolean Functions and an Extended Definition*, 1988.
  - DOI: `10.1007/0-387-34799-2_31`
  - BibTeX key: `forre_strict_1988`
- Brunetta and Picazo-Sanchez, *Modelling Cryptographic Distinguishers Using Machine Learning*, 2022.
  - DOI: `10.1007/s13389-021-00262-x`
  - BibTeX key: `brunetta_modelling_2022`
- Bellare and Rogaway, *Introduction to Modern Cryptography*, 2005.
  - URL: `https://www.cs.ucdavis.edu/~rogaway/classes/227/fall03/book/index.html`
  - BibTeX key: `bellare_rogaway_modern_2005`
- Luby, *Pseudorandomness and Cryptographic Applications*, 1996.
  - DOI: `10.2307/j.ctvs32rpn`
  - BibTeX key: `luby_pseudorandomness_1996`
- Benamira et al., *A Deeper Look at Machine Learning-Based Cryptanalysis*, 2021.
  - DOI: `10.1007/978-3-030-77870-5_28`
  - BibTeX key: `benamira_deeper_2021`

## Question

Issue #19 のように、avalanche 側では偏りが大きいのに logistic regression distinguisher は random guess 付近だった場合、何を言えて、何を言えないか。

## Short Answer

avalanche は「入力を少し変えたときに出力がどれだけ変わるか」を測る局所的な拡散指標で、distinguisher は「観測した出力や特徴量から、ある生成過程とランダムを区別できるか」を測る識別課題である。両者は関連することがあるが同義ではない。

hash-lab の現在の logistic regression task は、digest と random bit列を 256 bit features として分類する小さな supervised learning task である。これは暗号学の一般的な indistinguishability game そのものではなく、固定したデータ生成、特徴量、モデル、samples、seeds の範囲での local distinguisher 実験として読む。

## What Avalanche Measures

Webster and Tavares の avalanche / SAC の見方では、入力1 bitを反転したとき、各出力bitが確率 `1/2` で変わることを期待する。hash-lab の `mean_flip_rate`、出力bit位置別 `flip_rate`、Wilson CI、Holm補正は、この期待値 `0.5` からのずれを見る。

この指標で言えること:

- round数を増やすと、入力差分の拡散が `0.5` に近づくか。
- aggregate mean が `0.5` に近くても、特定出力bitに偏りが残るか。
- 入力bit位置や出力bit位置ごとの局所的な伝播の弱さがあるか。

この指標だけでは言えないこと:

- hash出力が任意の効率的観測者に対してランダムと区別不能か。
- collision resistance や preimage resistance があるか。
- ML classifier が digest単体から汎化する識別信号を得られるか。

## What the Distinguisher Measures

Bellare and Rogaway や Luby の文脈では、pseudorandomness は効率的な観測者がランダムと区別できないこととして扱う。hash-lab の ML distinguisher はこの大きな考え方の小さな実験版で、`mini-sha` digest と random bit列を classifier が区別できるかを見る。

Brunetta and Picazo-Sanchez は cryptographic distinguisher を machine learning classifier として扱う枠組みを与える。Benamira et al. は、neural distinguisher が高精度でも、既知の差分分布や単純な統計的特徴を拾っている可能性を確認する必要があることを示す。

hash-lab の logistic regression 指標で言えること:

- 現在の特徴量とモデルで、test split に汎化する線形識別信号が見えるか。
- random guess baseline `0.5` や majority baseline と比べてどの程度上回るか。
- train-test gap が大きい場合、学習はできても汎化していない可能性があるか。

この指標だけでは言えないこと:

- avalanche bias が存在しないこと。
- MLP、CNN/RNN、別特徴量、別roundでも識別不能であること。
- 暗号学的な意味で完全な pseudorandomness があること。

## Relation to Issue #19

Issue #19 では、2 rounds は avalanche mean が大きく baseline から離れ、logistic regression も強く識別できた。一方、4/8 rounds は avalanche と bit位置指標では強い偏りが残ったが、logistic regression の test delta は `0.0045` / `0.0055` で random guess 付近だった。

この結果から言えること:

- 2 rounds は拡散指標でも digest-vs-random classifier でも明らかに弱い。
- 4/8 rounds は入力差分に対する拡散は弱いが、現在の digest単体・線形classifier taskでは汎化する識別信号として使えていない。
- 16 rounds は既存の aggregate avalanche、bit位置CI、logistic regression baseline では baseline 付近に見える。

言えないこと:

- 4/8 rounds の avalanche bias が重要でない、とは言えない。
- 16 rounds 以上が安全、とは言えない。
- 13 rounds の bit255 のような局所偏りが ML classifier に必ず現れる、とは言えない。

## Practical Reading Rules

- `avalanche mean ~= 0.5` は、拡散平均が random-like baseline に近いという意味に留める。
- `Holm reject count = 0` は、その測定条件と補正単位では出力bit位置別の差が見えなかった、という意味に留める。
- `test_accuracy_minus_baseline ~= 0` は、そのデータ生成、特徴量、モデル、seed集合では classifier が汎化していない、という意味に留める。
- `train_accuracy` が高く `test_accuracy` が低い場合は、構造発見ではなく過学習の候補として先に読む。
- ML が baseline を超えた場合は、bit frequency、runs、pairwise correlation、logistic regression weights、known differential bias などの単純な説明を先に確認する。

## Next

- #53 で 9..15 rounds と32 rounds の logistic regression distinguisher を測定し、avalanche境界と同じround軸で比較する。
- #51 で MLPを試す場合も、logistic regression baseline、低次統計baseline、train-test gap を同時に保存する。
- #56 で BIC / bit間相関を整理し、avalanche と digest-vs-random classifier の間に置ける中間指標を増やす。
