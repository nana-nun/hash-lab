# Randomness tests and low-order statistics for hash outputs

## Citation

- Authors: Lawrence E. Bassham et al.; Pierre L'Ecuyer and Richard Simard; George Marsaglia and Wai Wan Tsang; Meltem Sönmez Turan et al.
- Year: 2002, 2007, 2010, 2018
- Link:
  - https://csrc.nist.gov/pubs/sp/800/22/r1/upd1/final
  - https://dl.acm.org/doi/10.1145/1268776.1268777
  - https://www.jstatsoft.org/article/view/v007i03
  - https://csrc.nist.gov/pubs/sp/800/90/b/final
- BibTeX key: `nist_sp800_22r1a_2010`, `lecuyer_testu01_2007`, `marsaglia_difficult_2002`, `nist_sp800_90b_2018`

## Summary

hash出力とrandom bit列の差をML classifier以外で見るには、まず小さな統計量をbaselineとして置くのがよい。NIST SP 800-22 Rev. 1a は frequency、block frequency、runs、longest run、serial、approximate entropy など、bit列に対する代表的な統計testの入口になる。TestU01 はより広いRNG empirical testing libraryで、Diehard系や古典的なRNG testの分類を調べるときの基準になる。Marsaglia and Tsang 2002 は、単純なfrequencyだけでは拾いにくい失敗例を探す発想を示す。

ただし、これらは暗号学的安全性の証明ではない。NIST SP 800-22 のページにも revision planning note があり、SP 800-90B はentropy source validationやhealth testsの別文脈を扱う。hash-lab では、test suiteに通るかどうかではなく、toy / reduced-round hash のround数に沿ってどの低次統計量がrandom-like baselineへ近づくかを見る。

## Important Ideas

- frequency test: digest全体またはround別streamで `1` の割合が `0.5` からどれだけ離れるかを見る。既存のavalanche bit-position biasとは違い、入力反転ではなくhash出力そのものの偏りを見る。
- runs test: 連続する同じbitの長さがrandom bit列と比べて極端かを見る。低roundで構造的な連続や交互パターンが出るなら、logistic regressionより軽いbaselineで拾える可能性がある。
- serial / block frequency: 2-bit、3-bit、4-bit blockなどの出現頻度を見る。`00, 01, 10, 11` の偏りは、pairwise correlationやbit-position biasより粗いが実装しやすい。
- pairwise correlation: digest内のbit位置ペア、または連続digest stream上の隣接bitの相関を見る。BIC系のIssue #56と近いが、hash output vs random stream のbaselineとしても使える。
- p-valueの多重性: test batteryは多数のp-valueを出すので、単発の小さいp-valueを過大解釈しない。round、seed、bit位置、block sizeを増やす場合は補正またはseed階層の集約を検討する。
- sample size: NIST/TestU01/PractRand級のtestは十分長いstreamを前提にすることが多い。hash-lab の小規模実験では、まずseed別に軽量統計量と信頼区間を保存する方が再現しやすい。

## Relation to hash-lab

Issue #19 では、4/8 rounds のavalanche偏りが大きい一方で logistic regression distinguisher はtest splitでrandom guess付近だった。これは「hash outputとrandom bit列の差」を現在のML特徴量が拾えていないだけかもしれない。そこで、次のbaseline候補を優先する。

1. digest bit frequency: round、seed、bit位置ごとの `ones_rate` とWilson CI。
2. low-order block frequency: digest streamを連結し、2-bit / 4-bit block頻度のchi-squareまたはtotal variation distance。
3. runs: digest stream単位とdigest境界を分け、runs countとlongest runを保存する。
4. adjacent / selected pair correlation: まず隣接bitと同一word内ペアに限定し、BIC full pair matrixは別Issueに回す。
5. external battery comparison: 保存streamが十分長くなってから、Dieharder / PractRand / TestU01相当の結果と比較する。

この順番なら、外部tool依存なしで `src/hash_lab` に小さく追加でき、random guess baselineやlogistic regression baselineと横比較しやすい。

## Limitations

- NIST SP 800-22 やTestU01はRNG評価の文脈が中心で、hash関数の暗号学的安全性を直接評価するものではない。
- toy hash の短いdigest streamでは、testの近似分布やp-valueが安定しない可能性がある。
- 入力分布、digestの連結方法、seed階層、round数を混ぜると解釈が崩れやすい。
- randomness testが通ってもdistinguisherが存在しないとは言えない。逆に、失敗しても実システム攻撃の手順には直結させない。

## Questions

- Issue #51 のMLP比較前に、frequency / runs / serial baselineを同じround軸で追加すべきか。
- digest境界を跨ぐrunsやblock frequencyは、hash output streamとして扱う場合とdigest単位で扱う場合のどちらがhash-labの目的に合うか。
- 低次統計量のCIはsample単位、digest単位、seed単位のどれを主にするべきか。
