# BIC と bit間相関の測定メモ

## Citation

- Webster and Tavares, *On the Design of S-Boxes*, 1986.
  - DOI: `10.1007/3-540-39799-X_41`
  - BibTeX key: `webster_design_1986`
- Upadhyay et al., *Investigating the Avalanche Effect of Various Cryptographically Secure Hash Functions and Hash-Based Applications*, 2022.
  - DOI: `10.1109/ACCESS.2022.3215778`
  - BibTeX key: `upadhyay_avalanche_2022`
- Madarro-Capó et al., *Bit Independence Criterion Extended to Stream Ciphers*, 2020.
  - DOI: `10.3390/app10217668`
  - BibTeX key: `madarro_bic_2020`

## Question

hash-lab の avalanche 実験で、aggregate mean や output bit別 flip rate の次に、BIC / bit間相関をどう測るべきか。

## Short Answer

BIC は、入力bitを固定して反転したとき、各 output bit が `0.5` に近い確率で変わるだけでなく、output bit同士の反転イベントが独立に近いかを見る。hash-lab の既存 `bit_metrics.csv` は output bitごとの flip count だけを保存しているため、BIC や pairwise correlation は後から正しく計算できない。次に実装するなら、サンプルごとの avalanche vector を保存する必要がある。

## What BIC Measures

SAC は、入力bit `i` を反転したときに output bit `j` が変わる確率を見る。

```text
Pr[V_j^i = 1] ~= 0.5
```

BIC は、同じ入力bit `i` に対して、output bit `j` と `k` の反転イベントが独立かを見る。

```text
Pr[V_j^i = 1 and V_k^i = 1] ~= Pr[V_j^i = 1] * Pr[V_k^i = 1]
```

実装上は、サンプルごとの avalanche vector `V^i = f(x) xor f(x xor e_i)` を作り、各 output bit pair `(j, k)` について Pearson correlation、covariance、phi coefficient、または joint count を見る。

## Existing Data vs Needed Data

既存の `results/*/bit_metrics.csv` で計算できるもの:

- round別・seed別・output bit別の `flip_rate`
- output bit別の min / max / mean
- output bitごとの Wilson CI や Holm補正
- output bit単独の baseline delta

既存の `bit_metrics.csv` だけでは計算できないもの:

- output bit `j` と `k` が同じサンプルで同時に反転した回数
- output bit pair の covariance / Pearson correlation
- BIC の pairwise independence statistic
- input bit位置を固定したときの output bit pair correlation

理由は、`bit_metrics.csv` が output bitごとの集約済み flip count だけを持ち、サンプルIDや avalanche vector を持たないためである。たとえば bit `j` と `k` の flip count がそれぞれ `1000/2000` でも、同じ1000サンプルで一緒に反転したのか、別々に反転したのかは分からない。

## Recommended Data Format

最小実装では、全digestを保存するより、avalanche vector を bitset / hex string としてサンプル単位で保存する。

推奨列:

- `experiment`
- `rounds`
- `seed`
- `sample_index`
- `input_bit_index`
- `output_bits`
- `avalanche_hex`

`input_bit_index` をランダムに選ぶ aggregate avalanche の場合も、BIC では入力bitごとに条件が変わるため、反転した入力bitを保存する。Issue #44 のように入力bitを固定する場合は、`input_bit_index` ごとに pairwise correlation を計算できる。

集約出力の推奨列:

- `rounds`
- `seed` または `seed_group`
- `input_bit_index` または `all_random_input_bits`
- `output_bit_j`
- `output_bit_k`
- `samples`
- `joint_11_count`
- `flip_rate_j`
- `flip_rate_k`
- `joint_rate_11`
- `covariance`
- `pearson_correlation`
- `abs_correlation`

## First Hash-Lab Measurement

最初の BIC 風測定は、全 `256 x 255 / 2` pair をいきなり重く見るより、次の小さい条件から始める。

- hash / rounds: `mini-sha` / `12, 13, 14`
- input bit mode: Issue #44 と同じ fixed input bit、または random input bit flip とは分けて実行
- output bits: まず Issue #47 の rejected bits `225, 228, 231, 254, 255` と bit255周辺
- samples: 既存結果と比較できるよう seedとsamplesを明記

この測定なら、bit255 の局在偏りと周辺 output bits が同じサンプルで連動しているかを見られる。もし全output bit pairへ広げるなら、pair数が `32640` になるため、multiple testing と可視化を先に決める。

## Interpretation

BIC / pairwise correlation が大きい場合:

- output bitごとの flip rate が `0.5` に近くても、反転イベントが一緒に動いている候補。
- aggregate avalanche では見えない構造的な依存が残っている候補。
- ML classifier や低次統計baselineが拾える信号の候補。

BIC / pairwise correlation が小さい場合:

- その測定条件では output bit pair の線形相関は見えにくい。
- 高次依存、input bit位置別の局在、digest-vs-random の別特徴量までは否定しない。

安全な表現:

- toy / reduced-round hash の avalanche vector 内の依存を測った。
- 実SHA-256の安全性や攻撃可能性は主張しない。
- BIC は追加の観測軸であり、SAC、bit frequency、distinguisher accuracy と同義ではない。

## Next

- #77 で `avalanche-vector` 形式の保存コマンドを追加し、サンプルごとの `avalanche_hex` と `input_bit_index` を必須にする。
- #74 / #75 の input-bit局在比較と組み合わせる場合は、rejected output bits の pairwise correlation を小さく見る。
- 全bit pairを扱う前に、visualization と multiple testing の方針を `notes.md` に残す。
