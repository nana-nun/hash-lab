# Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning

## Citation

- Authors: Aron Gohr
- Year: 2019
- Link: https://doi.org/10.13154/tosc.v2019.i2.299-320
- BibTeX key: `gohr_speck_2019`

## Summary

round-reduced Speck32/64 に対して deep learning を用いた neural distinguisher を構成し、古典的な differential cryptanalysis と組み合わせる代表的な文献。hash function ではなく block cipher が対象だが、reduced-round な暗号プリミティブに対して ML classifier を distinguisher として使う発想の主軸文献になる。

hash-lab では攻撃手順の再現ではなく、toy / reduced-round SHA-like hash に対して「ML が何を識別しているのか」「単純 baseline をどれだけ超えるのか」を考えるための背景として読む。

## Important Ideas

- neural network を、暗号出力とランダム出力を分ける distinguisher として使う。
- round数が増えるほど識別は難しくなり、reduced-round 設定が重要になる。
- ML の精度は単独では解釈しにくく、差分構造や既存解析との関係を見る必要がある。
- 実験では training / test の分離、入力差分、sample size、評価指標が重要になる。

## Relation to hash-lab

`mini-sha` の logistic regression distinguisher は Gohr 型の深い neural distinguisher よりかなり単純な baseline に近い。これは最初の段階として望ましい。hash-lab では、MLP や CNN を試す前に random guess、majority baseline、bit frequency、logistic regression を並べる。

Gohr 2019 は「ML で高精度が出たら成功」と読むのではなく、「どの reduced-round 条件で、どの baseline を超え、何を学習している可能性があるか」を問うための参照点として使う。

## Questions

- hash 出力 vs random bit列の task は、Gohr 型の chosen-difference task とどこが違うか。
- `mini-sha` で neural model を増やす前に、logistic regression が拾う bit frequency 以外の信号を確認できるか。
- ML が baseline を超えた場合、入力差分や出力bit位置との対応をどう可視化するか。
