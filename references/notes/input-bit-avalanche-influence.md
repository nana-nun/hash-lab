# 入力bit位置別 avalanche / influence メモ

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
- O'Donnell, *Analysis of Boolean Functions*, 2014.
  - DOI: `10.1017/CBO9781139814782`
  - BibTeX key: `odonnell_analysis_2014`
- Biswas and Sarkar, *Influence of a Set of Variables on a Boolean Function*, 2023.
  - DOI: `10.1137/22M1503531`
  - BibTeX key: `biswas_influence_2023`
- Madarro-Capó et al., *Bit Independence Criterion Extended to Stream Ciphers*, 2020.
  - DOI: `10.3390/app10217668`
  - BibTeX key: `madarro_bic_2020`

## Question

Issue #44 で `mini-sha` 13 rounds の `output_bit_index=255` を見るとき、入力bit位置ごとの avalanche をどの観点で集計すべきか。

## Hypothesis

`output_bit_index=255` の残差偏りが特定の入力bit位置に由来するなら、入力bit位置を固定した flip rate 行列で一部の列または語境界に偏りが集中する。全入力bitで同程度なら、局所的な入力bit依存というより、出力bit側または round構造全体の残差偏りとして解釈するほうが自然になる。

## Source Summary

Webster and Tavares は avalanche effect と SAC を、入力bitを1つ反転したときの出力変化として定式化する基礎文献。hash-lab の既存 `avalanche-bits` は出力bit位置ごとの flip rate を保存しているが、反転した入力bit位置を集計後に捨てているため、入力bitごとの寄与はまだ見えない。

Forré と Preneel et al. は、SAC を Boolean function の導関数、自己相関、propagation criterion として見るための理論的な背景になる。Issue #44 では完全な Walsh / autocorrelation 解析までは不要だが、「固定した差分方向に対する出力bitの導関数が balanced か」という読み替えが使える。

O'Donnell は influence を Boolean function 解析の基本概念として整理している。hash-lab の toy hash では全入力空間を列挙できない条件が多いので、入力bit `i` の influence は「sampled influence」、つまり `Pr_x[f_j(x) != f_j(x xor e_i)]` の推定値として扱うのがよい。

Biswas and Sarkar は変数集合の influence を扱う。Issue #44 の最初の実験は単一入力bitでよいが、偏りが語単位や message schedule のまとまりに見える場合は、複数入力bit集合の influence へ広げる候補になる。

Madarro-Capó et al. は BIC を input-output bit dependency の実験アルゴリズムとして拡張している。対象は stream cipher だが、入力bitと出力bitの依存行列を作り、理想的な独立性からのずれを統計的に見る発想は、hash-lab の reduced-round hash 測定にも転用しやすい。

## Measurement Design for Issue #44

入力bit位置別の基本単位は、round `r`、seed `s`、入力bit `i`、出力bit `j` の flip count と flip rate にする。

```text
flip_rate[r, s, i, j] = count(f_r(x)_j != f_r(x xor e_i)_j) / samples
```

Issue #44 で最初に見る対象は `round=13`、`output_bit_index=255` に絞る。既存の random input bit flip 測定との差は、既存測定が入力bit位置をランダム化して平均した値であるのに対し、この測定は入力bit `i` を固定して条件付き flip rate を見る点にある。

優先して保存したい列:

- `round`
- `seed`
- `input_bit_index`
- `output_bit_index`
- `samples`
- `flip_count`
- `flip_rate`
- `baseline_delta_from_0_5`

集約では、入力bitごとに seed平均と seed階層CIを出す。入力bit数が多い場合は、まず `output_bit_index=255` のみで Holm補正または Benjamini-Hochberg を検討し、後で全出力bit行列へ広げる。入力bit `i` と出力bit `j` の全行列を同時に検定すると比較数が大きくなり、Issue #44 の目的より重くなる。

## Interpretation

入力bit位置別 flip rate は「この入力bitが出力bitに影響する確率」の推定であり、完全な意味での安全性や攻撃可能性を示すものではない。特定入力bitで低い flip rate が出ても、それは local residual bias の候補であって、実運用ハッシュへの攻撃手順ではない。

Issue #44 では次の読み方が使いやすい。

- 多くの入力bitで `0.5` より低い: `output_bit_index=255` 側に広い残差偏りがある候補。
- 少数の入力bitだけ低い: 入力bit位置または message word 境界に由来する局所的な候補。
- seed間で符号や大きさが揺れる: 合算二項CIより seed階層CIを優先して読む。
- 入力bit位置の近傍や語単位でまとまる: 単一bit influence から変数集合 influence へ広げる候補。

## Limitations

- 全入力空間の influence ではなく、有限samplesの推定値に留まる。
- `mini-sha` の toy / reduced-round 条件での観測なので、実ハッシュ全体の主張にはしない。
- 入力bit位置を固定すると比較数が増えるため、p-valueだけでなく効果量と seed間の安定性を併記する必要がある。
- 既存 `bit_metrics.csv` は入力bit位置を保存していないため、Issue #44 では新しい保存形式が必要になる。

## Next

- Issue #44 では、まず `round=13`、`output_bit_index=255`、seeds `1..20`、各seed `2000 samples` にそろえて測る。
- 出力は `input_bit_metrics.csv` と `input_bit_summary.csv` のように、既存の `bit_metrics.csv` と区別できる名前にする。
- 結果解釈では `results/2026-05-10-avalanche-mini-sha-13-bit255-extra-seeds/notes.md` と `results/2026-05-12-avalanche-mini-sha-13-rejected-bits-seed-ci/notes.md` を比較対象にする。
