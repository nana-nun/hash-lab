# SAC / BIC / GAC と avalanche 指標の限界

## Citation

- Webster and Tavares, *On the Design of S-Boxes*, 1986.
  - DOI: `10.1007/3-540-39799-X_41`
  - BibTeX key: `webster_design_1986`
- Forré, *The Strict Avalanche Criterion: Spectral Properties of Boolean Functions and an Extended Definition*, 1988.
  - DOI: `10.1007/0-387-34799-2_31`
  - BibTeX key: `forre_strict_1988`
- Preneel et al., *Propagation Characteristics of Boolean Functions*, 1990.
  - DOI: `10.1007/3-540-46877-3_14`
  - BibTeX key: `preneel_propagation_1990`
- Zhang and Zheng, *GAC - the Criterion for Global Avalanche Characteristics of Cryptographic Functions*, 1995.
  - DOI: `10.3217/jucs-001-05-0320`
  - URL: https://www.jucs.org/jucs_1_5/gac_the_criterion_for.html
  - BibTeX key: `zhang_gac_1995`
- Upadhyay et al., *Investigating the Avalanche Effect of Various Cryptographically Secure Hash Functions and Hash-Based Applications*, 2022.
  - DOI: `10.1109/ACCESS.2022.3215778`
  - BibTeX key: `upadhyay_avalanche_2022`

## Question

hash-lab の avalanche 実験で `mean flip ratio = 0.5` に近いこと、SAC風の bit別 flip rate、BIC風の bit pair correlation は、それぞれ何を言えて、何を言えないのか。

## Short Answer

`mean flip ratio = 0.5` に近いことは、入力を変えたときの出力反転数が平均として random-like に見える、という局所的な観測である。これは有用な baseline だが、暗号学的安全性全体を示す条件ではない。

SAC は入力bit反転に対して各出力bitが `0.5` 程度で反転するかを見る。BIC はそれに加えて、出力bit同士の反転イベントが独立に近いかを見る。Propagation criterion は単一bitだけでなく、より一般の入力差分方向に対する出力変化を見る。GAC は、Zhang and Zheng が SAC や propagation criterion の限界を指摘したうえで、関数全体の avalanche characteristics をより大域的に測るために提案した基準である。

## Criteria Map

| 指標 | 見ているもの | hash-lab での読み方 | 主な限界 |
| --- | --- | --- | --- |
| aggregate avalanche | 入力変更後、出力bit全体の何割が反転したか | round数が増えると全体平均が `0.5` へ近づくかを見る最初の baseline | bit位置別の偏り、bit間依存、入力差分方向の違いを平均で隠す |
| SAC | 入力bit `i` の反転で出力bit `j` が `0.5` 程度で反転するか | output bit別、input bit x output bit別の flip rate として測る | 各bit単独の反転確率であり、出力bit同士の依存は見えない |
| BIC | 同じ入力変化に対する出力bit `j` と `k` の反転が独立に近いか | sample単位の avalanche vector から pair correlation を測る | pairwise な依存だけで、高次依存や別の識別信号までは否定しない |
| propagation criterion | 単一bitに限らない入力差分方向で出力変化が balanced か | single-bit delta から multi-bit delta 探索へ広げる理論的な橋 | 全差分方向を網羅するには探索空間が大きい |
| GAC | 関数全体の avalanche characteristics を大域的に評価する | SAC/BICだけで安全性を言い切らないための警告として使う | hash-lab の有限sample実験では厳密な大域評価ではなく、近似的・探索的な観測に留まる |

## Relation to Current Results

hash-lab の `mini-sha` 実験では、round数が増えると aggregate mean は `0.5` に近づく。特に 16/32 rounds は seed階層CIでも `0.5` 付近に見えている。一方で 12/13/14 rounds 周辺では、aggregate だけでは見えにくい output bit別偏り、input bit位置別の局在、BIC風の pair correlation が見えている。

この差は「avalancheが良いから安全」と読まないために重要である。aggregate mean は第一の観測軸であり、SAC風の bit別測定、BIC風の依存測定、distinguisher baseline、randomness tests は別の観測軸である。ある指標が random-like に見えても、別の指標で構造が残る可能性がある。

## What Hash-Lab Can Claim

- toy / reduced-round hash の特定条件で、aggregate avalanche、bit別 flip rate、BIC風相関、distinguisher accuracy が baseline と比べてどう見えたか。
- `mini-sha` では 12/13 rounds 周辺で aggregate と局所指標の見え方がずれる可能性があること。
- avalanche 指標は、round数による拡散の変化を観察するための有用な測定軸であること。

## What Hash-Lab Should Not Claim

- `mean flip ratio = 0.5` に近いので暗号学的に安全である、とは言わない。
- SAC や BIC を満たすように見えるので collision resistance / preimage resistance / pseudorandomness が示された、とは言わない。
- toy / reduced-round の結果から、実用 SHA-256 を攻撃できる、弱められる、または破れる、とは言わない。
- 有限sampleの p-value や補正後 reject count だけで、構造の原因や攻撃可能性を断定しない。

## Recommended Wording

安全な表現:

- 「この条件では aggregate avalanche は baseline `0.5` に近い」
- 「この条件では output bit別 / input bit別に局所的な残差偏り候補が見える」
- 「BIC風の pair correlation は、SACだけでは見えない依存構造の候補を示す」
- 「この結果は toy / reduced-round hash の探索的測定であり、実用 SHA-256 の安全性について直接の主張をしない」

避ける表現:

- 「avalancheが良いので安全」
- 「SACを満たすのでランダム」
- 「MLで見分けられないので破れない」
- 「reduced-round の偏りから full SHA-256 の攻撃につながる」

## Next

- Issue #85 の input bit x output bit heatmap では、aggregate mean と局所構造を分けて書く。
- Issue #86 の全 output bit pair correlation では、BIC風測定を SAC の代替ではなく追加軸として扱う。
- Issue #95 の round境界比較では、指標ごとに random-like に見える境界がずれる可能性を前提に表を作る。
