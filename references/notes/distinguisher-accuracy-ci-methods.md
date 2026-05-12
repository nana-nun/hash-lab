# Distinguisher精度の信頼区間と検定メモ

## Citation

- Wilson, *Probable Inference, the Law of Succession, and Statistical Inference*, 1927.
  - DOI: `10.1080/01621459.1927.10502953`
  - BibTeX key: `wilson_probable_1927`
- Brown, Cai, and DasGupta, *Interval Estimation for a Binomial Proportion*, 2001.
  - DOI: `10.1214/ss/1009213286`
  - BibTeX key: `brown_interval_2001`
- Efron, *Bootstrap Methods: Another Look at the Jackknife*, 1979.
  - DOI: `10.1214/aos/1176344552`
  - BibTeX key: `efron_bootstrap_1979`
- Holm, *A Simple Sequentially Rejective Multiple Test Procedure*, 1979.
  - URL: `https://www.jstor.org/stable/4615733`
  - BibTeX key: `holm_sequentially_1979`
- Dietterich, *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms*, 1998.
  - DOI: `10.1162/089976698300017197`
  - BibTeX key: `dietterich_tests_1998`
- Nadeau and Bengio, *Inference for the Generalization Error*, 2003.
  - DOI: `10.1023/A:1024068626366`
  - BibTeX key: `nadeau_inference_2003`
- Kohavi, *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection*, 1995.
  - DOI: `10.5555/1643031.1643047`
  - BibTeX key: `kohavi_cross_validation_1995`

## Question

hash-lab の logistic regression distinguisher で、`test_accuracy_minus_baseline` の信頼区間や検定をどの単位で作るべきか。

## Hypothesis

test split内の正解数だけを二項比率として扱うと、同じ学習設定を別seedで回したときのばらつきを過小評価する。hash-lab の現状では、まず seedを実験反復単位として bootstrap CI を作り、必要に応じて test split内の Wilson CI を補助的に併記するのがよい。

## Source Summary

Wilson と Brown, Cai, DasGupta は、accuracy や flip rate のような比率に区間を付けるときの基礎になる。test splitの `correct / total` を二項比率として見るなら、Wald interval より Wilson interval を優先する。ただし、これは「固定された学習済みモデルが固定分布から引いたtest sampleでどれだけ当たったか」の不確実性であり、seedやtraining setの違いまでは含まない。

Efron は bootstrap の基礎文献。hash-lab では seed `1..5` のように反復数が少ないため、bootstrap CI は厳密な保証ではなく探索的な不確実性表示として使う。Issue #50 の `results/2026-05-12-distinguish-baseline-delta-ci/notes.md` はこの扱いに近く、seed別 `test_accuracy_minus_baseline` を再標本化して seed平均CIを作っている。

Dietterich と Nadeau / Bengio は、classifier評価で train/test split やcross-validationの反復を独立な測定のように扱う危険を説明する。hash-lab の distinguisher でも、同じデータ生成手順・同じround・同じモデル設定から作られた複数runは完全に独立な母集団ではない。特にモデル比較や「baselineを上回る」と主張するときは、test sampleの二項誤差だけでなく、seed、training set、test split、model initialization のばらつきを分けて考える必要がある。

Holm は複数条件を同時に見るときの補正の基本文献。round、samples、epochs、model family、output bit などを多数見る場合、最大値や有意になった条件だけを後から拾うと過大評価になる。Issue #50 のような grid全体の探索では、単一条件のCIだけでなく、条件数が多いことを解釈に残す。

Kohavi は cross-validation と bootstrap を accuracy estimation / model selection の文脈で比較する。hash-lab では当面、モデル選択の勝者を決めるより、固定した baseline model が random guess を安定して超えるかを見る。そのため、複雑なCV比較よりも、seed固定の再現性と小さなbaseline差分の不確実性を優先する。

## Recommended Use in hash-lab

### Seed平均CI

目的: 実験seedを変えても `test_accuracy_minus_baseline` が同じ方向に残るかを見る。

使う場面:

- Issue #50 のように、既存の seed別 metrics を再分析する。
- seed数が少ないが、test split内の正解数だけではなく実験run間のばらつきを見たい。
- `4/8/16 rounds は random guess 付近` のような解釈を支える。

注意:

- seed数 `1..5` では CI は粗い。
- bootstrap CI は探索的で、強い有意性主張には使いすぎない。
- seed集合を変えたら結果が変わる可能性を `Limitations` に残す。

### Test split単位のWilson CI

目的: 1つの学習済みrunで、test accuracy が `0.5` とどれくらい離れているかを見る。

使う場面:

- test sample数が小さく、accuracy の丸め誤差や二項sampling noise を見たい。
- roundやmodelごとの seed別行に補助列として CI を付けたい。

注意:

- training setやseedの違いは含まない。
- 複数seedを単純に合算すると、seed間ばらつきを隠すことがある。

### t interval

目的: seed別値を平均と標準偏差で素朴に要約する。

使う場面:

- seed数がもう少し多い場合の簡易summary。
- bootstrap CIと大きく矛盾しないかの sanity check。

注意:

- seed数が5程度では正規性仮定を強く見ない。
- 外れseedに敏感なので、seed別値も保存する。

### Permutation test

目的: `hash output` と `random bits` のラベルが交換可能という帰無仮説の下で、classifier accuracy や statistic がどの程度珍しいかを見る。

使う場面:

- 1つの条件で「この特徴量・モデルが本当にラベル情報を拾っているか」を確認したい。
- データセットが小さく、二項近似や正規近似を避けたい。

注意:

- 学習を含む permutation は重い。label shuffle後に再学習するなら計算量を明記する。
- 多数条件で回す場合は補正が必要。

## Multiple Testing

複数条件を同時に見る場合は、次の単位を先に決める。

- round別に主張するのか。
- samples / epochs の grid全体から最大差分を見るのか。
- model family 比較まで含めるのか。
- output bitやinput bitの多数比較も含むのか。

hash-lab では、まず family を小さく定義する。たとえば Issue #50 の再分析なら、`round in {4,8,16}`、`samples in {500,1000,2000}`、`epochs in {4,8,16}` の27条件を探索gridとして扱う。単一条件だけを強く主張せず、「27条件のうち正方向に baseline を安定して上回るものは見えない」のように書く。

Holm補正は family-wise error を抑えたいときに使いやすい。Benjamini-Hochberg は探索的に候補を拾う場合に候補だが、hash-lab の現状では結果数が少ないので、まず Holm と効果量の併記で十分。

## Relation to Issue #50

Issue #50 の結果では、4/8/16 rounds の27条件中26条件で seed平均 bootstrap CI が `0` を含んだ。残る1条件は負方向で、`baselineを上回る` 方向ではなかった。このため、logistic regression distinguisher が random guess を安定して超える証拠は見えない、という解釈は妥当。

ただし、この結論は「現在の logistic regression、features、dataset size、seeds `1..5` では」という範囲に限る。MLP、CNN/RNN系、特徴量設計、9..15 rounds への拡張では、同じ評価単位を保ちつつ再確認する必要がある。

## Next

- #51 の MLP比較では、logistic regression と MLP の両方について seed別 `test_accuracy_minus_baseline` を保存し、同じseed集合で比較する。
- #53 の round拡張では、roundごとの seed平均CIを出し、roundをまたいで最も良い条件だけを拾わない。
- accuracy だけでなく train-test gap、majority baselineとの差分、低次統計baselineとの差分も同じ表に残す。
