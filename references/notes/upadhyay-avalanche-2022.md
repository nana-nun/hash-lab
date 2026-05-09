# Investigating the Avalanche Effect of Various Cryptographically Secure Hash Functions and Hash-Based Applications

## Citation

- Authors: Darshana Upadhyay, Nupur Gaikwad, Marzia Zaman, and Srinivas Sampalli
- Year: 2022
- Link: https://doi.org/10.1109/ACCESS.2022.3215778
- BibTeX key: `upadhyay_avalanche_2022`

## Summary

複数の暗号学的ハッシュ関数と hash-based application について、avalanche effect、SAC、BIC、randomness tests などを実験的に比較する文献。実運用のハッシュ関数を対象にしているため、hash-lab の toy / reduced-round 実験とは目的が異なるが、測定項目の整理に役立つ。

hash-lab では「実ハッシュを破る」方向ではなく、toy hash が round数の増加でどの測定指標から random-like に近づくかを見るための参考として使う。

## Important Ideas

- avalanche mean だけでなく、SAC、BIC、randomness tests を組み合わせて評価している。
- hash-based application のように入力分布や利用形態が変わると、測定の見方も変わる。
- 単一の指標だけで「安全」と判断するのではなく、複数の観測項目を並べる必要がある。
- 実験条件、入力生成、sample size を明示しないと比較が難しい。

## Relation to hash-lab

`mini-sha` の現状は mean flip ratio と logistic regression distinguisher が中心で、BIC 風指標や randomness tests は未確認。この文献は、次に測る候補を増やすときのチェックリストになる。

ただし hash-lab では標準ハッシュ関数の優劣比較ではなく、reduced-round / toy hash の学習不能性への移り変わりを調べる。したがって、測定対象は小さく保ち、baseline、seed、dataset size、round数を必ず残す。

## Questions

- `mini-sha` で BIC 風の bit-pair independence を測る最小実装は何か。
- randomness tests を入れる前に、bit frequency と run length だけで十分な baseline になるか。
- avalanche 指標と distinguisher accuracy の境界roundは一致するか。
