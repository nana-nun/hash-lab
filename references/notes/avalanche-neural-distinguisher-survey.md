# Avalanche と Neural Distinguisher 先行研究メモ

## Citation

- Authors: A. F. Webster and Stafford E. Tavares; Réjane Forré; Sheelagh Lloyd; Darshana Upadhyay et al.; Aron Gohr; Adrien Benamira et al.; Carlo Brunetta and Pablo Picazo-Sanchez; Ongee Jeong and Inkyu Moon
- Year: 1986, 1988, 1992, 2019, 2021, 2022, 2024
- Link:
  - https://doi.org/10.1007/3-540-39799-X_41
  - https://www.iacr.org/cryptodb/data/paper.php?pubkey=1303
  - https://doi.org/10.1007/BF00193564
  - https://doi.org/10.1109/ACCESS.2022.3215778
  - https://iacr.org/cryptodb/data/paper.php?pubkey=29885
  - https://eprint.iacr.org/2021/287
  - https://doi.org/10.1007/s13389-021-00262-x
  - https://doi.org/10.1109/ICTC62082.2024.10826852
- BibTeX key:
  - `webster_design_1986`
  - `forre_strict_1988`
  - `lloyd_counting_1992`
  - `upadhyay_avalanche_2022`
  - `gohr_speck_2019`
  - `benamira_deeper_2021`
  - `brunetta_modelling_2022`
  - `jeong_hash_2024`

## Summary

hash-lab の現在の実験は、古典的な avalanche / Strict Avalanche Criterion、reduced-round hash cryptanalysis、機械学習による distinguisher の交差点にある。

Webster and Tavares は avalanche effect と S-box 設計基準の基礎を与える。Forré と Lloyd は SAC を Boolean function の性質として扱い、balance や correlation immunity との関係を整理している。これらは `mean flip ratio = 0.5` を baseline にする理由と、その baseline だけでは安全性全体を言えない理由を説明する背景になる。

Upadhyay et al. は実ハッシュ関数や hash-based application で avalanche effect を実験的に調べている。hash-lab の toy / reduced-round 実験とは対象が違うが、SAC、BIC、randomness tests を組み合わせる測定設計の参考になる。

Gohr は neural distinguisher を reduced-round Speck に使い、ML が differential cryptanalysis の一部を補えることを示した。Benamira et al. はその neural distinguisher の中身を解釈し、差分分布表に近いものを学んでいることを示した。Brunetta and Picazo-Sanchez は cryptographic distinguisher を classifier として扱う一般的な方法論を述べている。

Jeong and Moon は MD5 を対象に deep learning-based hash function cryptanalysis を扱う最近の短い conference paper である。hash function に近い例として重要だが、hash-lab ではまず小さい toy / reduced-round 設定、単純 baseline、再現可能な metrics を優先する。

## Important Ideas

- avalanche effect は入力1 bitの変化が出力bitの約半分に伝わることを見る拡散指標。
- SAC は bit単位の条件であり、collision resistance や preimage resistance そのものではない。
- reduced-round の実験では、round数を変えることで「どこから random-like に見えるか」を観察できる。
- neural distinguisher の精度だけを見ると過大解釈しやすい。random guess、majority baseline、単純統計量、logistic regression との比較が必要。
- ML distinguisher が成功した場合でも、それが新しい構造を発見したのか、既知の差分分布や単純な偏りを拾っただけなのかを分けて考える必要がある。

## Relation to hash-lab

現在の `mini-sha` 実験では、avalanche 測定と hash出力 vs random bit列の distinguisher を別々に見ている。先行研究の整理からは、次の比較軸が自然に出てくる。

- avalanche mean だけでなく、出力bit位置ごとの flip rate と BIC 風の指標を見る。
- 2/4/8/16/32 rounds のような粗い round比較に加え、境界領域を細かく測る。
- neural / logistic distinguisher の前に、random guess、majority baseline、bit frequency、低次統計量を置く。
- ML が baseline を超えたときは、どのbit位置や差分構造を見ているかを後続実験で確認する。

この整理は実システムへの攻撃手順ではなく、toy hash と reduced-round SHA-like hash の学習可能性を調べるための安全な研究背景として使う。

## Questions

- `mini-sha` の 9から15 rounds で、avalanche と distinguisher accuracy の境界は一致するか。
- 出力bit位置ごとの偏りは、logistic regression の重みと対応するか。
- `mean flip ratio = 0.5` に近いが BIC や bit frequency に偏りが残る round はあるか。
- MD5 / SHA-like の既存 deep learning hash cryptanalysis と比較するには、どの toy task が最小で再現しやすいか。
