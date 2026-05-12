# mini-sha 13 rounds bit255 残差偏りの解析背景

## Citation

- Sanadhya and Sarkar, *Attacking Reduced Round SHA-256*, 2008.
  - DOI: `10.1007/978-3-540-68914-0_8`
  - BibTeX key: `sanadhya_attacking_2008`
- Nikolić and Biryukov, *Collisions for Step-Reduced SHA-256*, 2008.
  - DOI: `10.1007/978-3-540-71039-4_1`
  - BibTeX key: `nikolic_collisions_2008`
- Biryukov, Lamberger, Mendel, and Nikolić, *Second-Order Differential Collisions for Reduced SHA-256*, 2011.
  - DOI: `10.1007/978-3-642-25385-0_15`
  - BibTeX key: `biryukov_second_order_2011`
- Mendel, Nad, and Schläffer, *Improving Local Collisions: New Attacks on Reduced SHA-256*, 2013.
  - DOI: `10.1007/978-3-642-38348-9_16`
  - BibTeX key: `mendel_improving_2013`
- De Cannière and Rechberger, *Finding SHA-1 Characteristics: General Results and Applications*, 2006.
  - DOI: `10.1007/11935230_1`
  - BibTeX key: `de_canniere_sha1_2006`
- Preneel et al., *Propagation Characteristics of Boolean Functions*, 1990.
  - DOI: `10.1007/3-540-46877-3_14`
  - BibTeX key: `preneel_propagation_1990`

## Question

`mini-sha` 13 rounds の `output_bit_index=255` に残った偏りを、reduced-round SHA-like hash の安全な toy 解釈としてどう読むか。

## Short Answer

bit255 の残差偏りは、実SHA-256への攻撃可能性ではなく、reduced-round / toy SHA-like 構造で特定の入力word範囲から特定の出力word末尾へ差分が十分に拡散しきっていない候補として読む。特に Issue #44 では input bits `224..254` 付近に強い局在があり、aggregate flip rate では相殺されていた正負の偏りが、入力bit位置を固定すると見えた。

## Source Summary

Sanadhya and Sarkar、Nikolić and Biryukov、Mendel et al. は、step-reduced SHA-256 で衝突や semi-free-start collision を扱う文献である。hash-lab では攻撃手順として使わず、round数を減らすと message word、state update、carry、rotation の局所構造が残りやすいという背景として読む。

Biryukov et al. は second-order differential collisions を扱い、単純な1bit差分だけでなく、複数差分や局所的な差分の組み合わせが reduced-round SHA-256 で意味を持つことを示す背景になる。Issue #44 の結果で input bits `224..254` 付近に強い正負の偏りが混在したことは、単一のaggregate値よりも局所差分の分布を見る必要がある、という方向と合う。

De Cannière and Rechberger は SHA-1 の差分特性探索の文献で、SHA-like compression function では message schedule と state update をまたぐ差分伝播を追う必要があることの参考になる。mini-sha は SHA-256 そのものではないが、8 word state、choice / majority、sigma、message word injection という形が似ているため、局所的な bit/word 伝播を見る観点を借りられる。

Preneel et al. の propagation criterion は、入力差分方向を固定したときの出力bitの balancedness を見るための理論的な背景になる。Issue #44 の input-bit-position 測定は、`output_bit_index=255` について単一入力bit方向の sampled derivative を測っている、と読み替えられる。

## Relation to mini-sha

`mini-sha` は 64-byte blockを16個の32-bit wordとして読み、13 rounds では message schedule expansion ではなく初期16 wordのうち `words[0..12]` が直接 round word として使われる。Issue #44 の強い局在範囲 `224..254` は、32-byte入力の最後の32-bit wordに相当する `word[7]` 付近である。

`output_bit_index=255` は digest末尾の bit であり、最終 state word 側の観測である。13 rounds では、入力 `word[7]` が round 7 で注入されたあと、残り数roundの state rotation / addition / boolean functions を経て出力末尾へ現れる。このため、`word[7]` 付近から最終出力wordへの拡散が 13 rounds ではまだ十分に均されていない、という仮説が自然に立つ。

ただし、これは構造候補であって証明ではない。carry propagation、rotation、choice/majority、feed-forward のどれが主要因かは、追加の内部状態トレースや round比較なしには分からない。

## How to Explain the bit255 Result

Issue #42 / #45 / #47 の output-bit単位の結果では、13 rounds の bit255 と周辺 rejected bits は seed階層でも baseline `0.5` を含まなかった。これは「出力bit側に小さい負方向の残差がある」ことを示す。

Issue #44 の入力bit位置別結果では、平均すると `0.488720` だが、input bit `224` は `0.064900`、input bit `237` は `0.842300` で、正負の強い偏りが混在した。このため、aggregate bit255 flip rate `0.483950` は局所的な正負の偏りが相殺された後の値として読むべきである。

安全な表現:

- 13 rounds の bit255 には、入力word 7 付近に局在した avalanche residual bias がある。
- aggregate flip rate だけでは、正負の局所偏りが相殺されて見えにくい。
- reduced-round SHA-like の局所差分伝播を調べる toy evidence として有用である。

避ける表現:

- SHA-256 の弱点を示した。
- 攻撃手順につながる。
- bit255 の原因が特定の内部演算だと確定した。
- 13 rounds 以外や他の output bit でも同じだと断定する。

## Visualization Ideas

- input bit index を横軸、flip rate または baseline delta を縦軸にした line plot。
- 32-bit word境界ごとに縦線を引き、`word[7]` 付近の局在を見やすくする。
- 正方向と負方向を色分けした heatmap。対象を広げる場合は output bit x input bit の行列にする。
- 12/13/14 rounds を同じ軸で並べ、局在が round増加で弱まるかを見る。
- rejected output bits `225, 228, 231, 254, 255` を横並びにし、同じ input bit範囲に局在するかを見る。

## Next

- #74 で 12/14 rounds でも bit255 の input-bit-position 測定を行い、局在が round増加で弱まるか確認する。
- #75 で 13 rounds の rejected output bits `225, 228, 231, 254, 255` を横並びにし、同じ input word範囲に局在するか確認する。
- 内部状態トレースを追加する場合は、攻撃手順ではなく toy hash の差分可視化として、roundごとの state word baseline delta を保存する。
