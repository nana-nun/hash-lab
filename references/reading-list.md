# Reading List

## Core: Hash Functions and Reduced-Round SHA-like Analysis

- NIST, FIPS PUB 180-4, *Secure Hash Standard (SHS)*, 2015.
  - BibTeX: `nist_fips_180_4`
  - SHA-1/SHA-2系の標準仕様。SHA256の構造確認用。標準名、略称、title表記が揺れやすいので、hash-lab では `FIPS PUB 180-4: Secure Hash Standard (SHS)` として扱う。
- Henri Gilbert and Helena Handschuh, *Security Analysis of SHA-256 and Sisters*, 2003.
  - SHA-256系の初期解析研究。
- Somitra Kumar Sanadhya and Palash Sarkar, *Attacking Reduced Round SHA-256*, 2008.
  - BibTeX: `sanadhya_attacking_2008`
  - Note: `references/notes/mini-sha-bit255-local-differential-background.md`
  - 18-step collision と24-step semi-free-start collision を扱う、reduced-round SHA-256解析の出発点として使う。
- Ivica Nikolić and Alex Biryukov, *Collisions for Step-Reduced SHA-256*, 2008.
  - BibTeX: `nikolic_collisions_2008`
  - Note: `references/notes/mini-sha-bit255-local-differential-background.md`
  - step-reduced SHA-256 の collision / semi-free-start collision / near-collision の基準文献。
- Kazumaro Aoki, Jian Guo, Krystian Matusiewicz, Yu Sasaki, and Lei Wang, *Preimages for Step-Reduced SHA-2*, 2009.
  - reduced SHA-2 の preimage attack を調べるときの比較対象。toy preimage baseline の設計にも関係する。
- Alex Biryukov, Mario Lamberger, Florian Mendel, and Ivica Nikolić, *Second-Order Differential Collisions for Reduced SHA-256*, 2011.
  - BibTeX: `biryukov_second_order_2011`
  - Note: `references/notes/mini-sha-bit255-local-differential-background.md`
  - higher-order / second-order differential の観点から、bit差分や局所差分をどう見るかの参考。
- Dmitry Khovratovich, Christian Rechberger, and Alexandra Savelieva, *Bicliques for Preimages: Attacks on Skein-512 and the SHA-2 Family*, 2011.
  - SHA-2 family への biclique preimage attack。小規模探索やGrover風探索と比較するときの背景文献。
- Florian Mendel, Tomislav Nad, and Martin Schläffer, *Improving Local Collisions: New Attacks on Reduced SHA-256*, 2013.
  - BibTeX: `mendel_improving_2013`
  - Note: `references/notes/mini-sha-bit255-local-differential-background.md`
  - 28-step collision、31-step collision、38-step semi-free-start collision など、局所衝突探索の改善を追うために読む。
- Christophe De Cannière and Christian Rechberger, *Finding SHA-1 Characteristics: General Results and Applications*, 2006.
  - BibTeX: `de_canniere_sha1_2006`
  - Note: `references/notes/mini-sha-bit255-local-differential-background.md`
  - 差分特性探索の考え方の参考。

## Core: Avalanche Criteria and Hash Measurements

- A. F. Webster and Stafford E. Tavares, *On the Design of S-Boxes*, 1986.
  - BibTeX: `webster_design_1986`
  - Note: `references/notes/webster-tavares-sboxes-1986.md`
  - BIC note: `references/notes/bic-bit-correlation-methods.md`
  - avalanche effect と Strict Avalanche Criterion の源流として読む。hash-lab の bit flip 実験で「平均0.5」を baseline にする理由を整理するための基礎文献。
- Réjane Forré, *The Strict Avalanche Criterion: Spectral Properties of Boolean Functions and an Extended Definition*, 1988.
  - BibTeX: `forre_strict_1988`
  - Note: `references/notes/forre-strict-avalanche-1988.md`
  - SAC を Boolean function の spectral property として扱う文献。toy hash の出力bit単位の偏りを見るときの理論背景。
- Sheelagh Lloyd, *Counting Binary Functions with Certain Cryptographic Properties*, 1992.
  - SAC、balance、correlation immunity の関係を整理する文献。avalanche だけで「安全」と言い切れない理由の確認に使う。
- Bart Preneel, Werner Van Leekwijck, Luc Van Linden, René Govaerts, and Joos Vandewalle, *Propagation Characteristics of Boolean Functions*, 1990.
  - BibTeX: `preneel_propagation_1990`
  - Note: `references/notes/input-bit-avalanche-influence.md`
  - SAC を propagation criterion として一般化し、入力差分方向ごとの導関数・自己相関で見る考え方を与える。Issue #44 の「入力bit位置を固定して output bit 255 の flip rate を見る」設計に近い。
- Xian-Mo Zhang and Yuliang Zheng, *GAC - the Criterion for Global Avalanche Characteristics of Cryptographic Functions*, 1995.
  - BibTeX: `zhang_gac_1995`
  - Note: `references/notes/avalanche-criteria-limitations.md`
  - SAC や propagation criterion の限界を指摘し、暗号関数の avalanche characteristics をより大域的に見る GAC を提案する文献。hash-lab では avalanche 指標を過大解釈しないための背景として読む。
- Ryan O'Donnell, *Analysis of Boolean Functions*, 2014.
  - BibTeX: `odonnell_analysis_2014`
  - Note: `references/notes/input-bit-avalanche-influence.md`
  - Boolean function の influence / Fourier analysis の標準的な教科書。hash-lab では厳密な全入力空間解析ではなく、sampled influence として入力bit位置別 flip rate を解釈するための語彙に使う。
- Aniruddha Biswas and Palash Sarkar, *Influence of a Set of Variables on a Boolean Function*, 2023.
  - BibTeX: `biswas_influence_2023`
  - Note: `references/notes/input-bit-avalanche-influence.md`
  - 変数集合の influence を自己相関ベースで扱う近年の整理。単一入力bitだけでなく、複数bit差分や内部語単位へ測定を広げる場合の背景として読む。
- Evaristo José Madarro-Capó et al., *Bit Independence Criterion Extended to Stream Ciphers*, 2020.
  - BibTeX: `madarro_bic_2020`
  - Note: `references/notes/input-bit-avalanche-influence.md`
  - BIC note: `references/notes/bic-bit-correlation-methods.md`
  - BIC を input-output bit dependency の実験アルゴリズムとして拡張する文献。hash-lab では stream cipher評価そのものではなく、入力bit・出力bitの依存行列を作る発想の参考にする。
- Darshana Upadhyay, Nupur Gaikwad, Marzia Zaman, and Srinivas Sampalli, *Investigating the Avalanche Effect of Various Cryptographically Secure Hash Functions and Hash-Based Applications*, 2022.
  - BibTeX: `upadhyay_avalanche_2022`
  - Note: `references/notes/upadhyay-avalanche-2022.md`
  - BIC note: `references/notes/bic-bit-correlation-methods.md`
  - 複数の実ハッシュ関数と hash-based application で avalanche / SAC / BIC / randomness tests を測った実験研究。hash-lab の測定項目を増やすときの比較対象。
- Lawrence E. Bassham et al., *A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications*, NIST SP 800-22 Rev. 1a, 2010.
  - BibTeX: `nist_sp800_22r1a_2010`
  - Note: `references/notes/randomness-tests-low-order-statistics.md`
  - frequency、runs、serial、approximate entropy などの統計test候補を整理する基準文献。hash-lab では合格/不合格を安全性の証明にせず、toy hash の低次統計baseline候補として読む。
- Pierre L'Ecuyer and Richard Simard, *TestU01: A C Library for Empirical Testing of Random Number Generators*, 2007.
  - BibTeX: `lecuyer_testu01_2007`
  - Note: `references/notes/randomness-tests-low-order-statistics.md`
  - RNG empirical testing の大きなtest batteryと分類の文献。hash-lab ではまず小さなfrequency/runs/correlationから始め、必要なら大規模batteryとの対応を見る。
- George Marsaglia and Wai Wan Tsang, *Some Difficult-to-Pass Tests of Randomness*, 2002.
  - BibTeX: `marsaglia_difficult_2002`
  - Note: `references/notes/randomness-tests-low-order-statistics.md`
  - GCD、birthday spacing、Gorilla test など、単純な統計では拾いにくい偏りを探す発想の参考。hash-lab の初期実装では過剰に重くしない。
- Meltem Sönmez Turan et al., *Recommendation for the Entropy Sources Used for Random Bit Generation*, NIST SP 800-90B, 2018.
  - BibTeX: `nist_sp800_90b_2018`
  - Note: `references/notes/randomness-tests-low-order-statistics.md`
  - entropy source validation と health tests の文献。hash-lab のhash出力評価そのものではないが、「統計testは安全性証明ではない」という注意を補強する背景。

## Core: Neural Cryptanalysis and Machine Learning

- Aron Gohr, *Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning*, 2019.
  - BibTeX: `gohr_speck_2019`
  - Note: `references/notes/gohr-speck-deep-learning-2019.md`
  - neural cryptanalysis の代表的な出発点。hash-lab では攻撃手順ではなく、reduced-round の distinguisher 実験を baseline と比較するための背景として読む。
- Adrien Benamira, David Gerault, Thomas Peyrin, and Quan Quan Tan, *A Deeper Look at Machine Learning-Based Cryptanalysis*, 2021.
  - BibTeX: `benamira_deeper_2021`
  - Note: `references/notes/benamira-deeper-look-2021.md`
  - Gohr型 neural distinguisher が何を学んでいるかを解釈する文献。hash-lab では neural distinguisher の精度だけでなく、単純な統計量や baseline との差を見る理由になる。
- Carlo Brunetta and Pablo Picazo-Sanchez, *Modelling Cryptographic Distinguishers Using Machine Learning*, 2022.
  - BibTeX: `brunetta_modelling_2022`
  - Note: `references/notes/avalanche-vs-distinguisher.md`
  - distinguish problem を機械学習 classifier として定式化する一般的な方法論。hash出力 vs random bit列の local distinguisher 実験の枠組み整理に使う。
- Ongee Jeong and Inkyu Moon, *Deep Learning-Based Hash Function Cryptanalysis*, 2024.
  - MD5 の step 数を変え、fully-connected neural network と BiLSTM で学習する hash function 寄りの最近例。hash-lab の reduced-round/toy hash の学習実験と近いが、短い conference paper なので補助文献として扱う。
- François-Xavier Standaert, *Introduction to Side-Channel Attacks*, 2010.
  - ML暗号解析とは別系統だが、統計的漏洩・識別の考え方の参考。

## Core: Cryptographic Distinguishers and Pseudorandomness

- Mihir Bellare and Phillip Rogaway, *Introduction to Modern Cryptography*, 2005.
  - BibTeX: `bellare_rogaway_modern_2005`
  - Note: `references/notes/avalanche-vs-distinguisher.md`
  - PRF、hash function、indistinguishability の基本的なゲームベースの考え方を確認するための講義ノート。hash-lab では「classifier accuracy が少し高い」ことと「暗号学的に強い distinguisher がある」ことを分けて読むために使う。
- Michael Luby, *Pseudorandomness and Cryptographic Applications*, 1996.
  - BibTeX: `luby_pseudorandomness_1996`
  - Note: `references/notes/avalanche-vs-distinguisher.md`
  - pseudorandomness を「効率的な観測者がランダムと区別できない」性質として見る背景。hash-lab の toy hash 実験では、この厳密な安全性定義ではなく、局所的な小規模 distinguisher task を扱っていることを明確にする。

## Core: Statistical Evaluation

- Edwin B. Wilson, *Probable Inference, the Law of Succession, and Statistical Inference*, 1927.
  - BibTeX: `wilson_probable_1927`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - classifier accuracy や bit flip rate を二項比率として見るときの Wilson score interval の基礎文献。
- Lawrence D. Brown, T. Tony Cai, and Anirban DasGupta, *Interval Estimation for a Binomial Proportion*, 2001.
  - BibTeX: `brown_interval_2001`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - Wald interval の弱さと Wilson などの代替を比較する整理。hash-lab では test split単位の accuracy CI を使うときの基準にする。
- Bradley Efron, *Bootstrap Methods: Another Look at the Jackknife*, 1979.
  - BibTeX: `efron_bootstrap_1979`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - seed平均や実験条件ごとの平均差分に分布仮定を置きにくいとき、bootstrap CI を探索的に使う背景。
- Sture Holm, *A Simple Sequentially Rejective Multiple Test Procedure*, 1979.
  - BibTeX: `holm_sequentially_1979`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - round、samples、epochs、bit位置など複数条件を見るときの family-wise error control の基本文献。
- Thomas G. Dietterich, *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms*, 1998.
  - BibTeX: `dietterich_tests_1998`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - classifier比較で単純な split反復や比率差検定が過大に有意になりやすいことを警告する文献。hash-lab では seedやtrain/test splitを独立サンプルのように扱いすぎないために読む。
- Claude Nadeau and Yoshua Bengio, *Inference for the Generalization Error*, 2003.
  - BibTeX: `nadeau_inference_2003`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - generalization error の分散推定では training set のランダム性も考える必要がある、という整理。seed階層CIとtest split内CIを分ける理由になる。
- Ron Kohavi, *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection*, 1995.
  - BibTeX: `kohavi_cross_validation_1995`
  - Note: `references/notes/distinguisher-accuracy-ci-methods.md`
  - cross-validation と bootstrap を accuracy estimation / model selection の観点で比較する古典的実験。hash-lab ではモデル選択を強く主張せず、固定設定の不確実性評価として読む。

## Background: Bitcoin and Mining

- Satoshi Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System*, 2008.
  - BitcoinのPoW、ブロック、署名の基本文献。hash-lab では実ネットワークや実マイニング最適化には使わず、hash / PoW の背景理解に留める。

## Background: Quantum Computing

- Lov K. Grover, *A Fast Quantum Mechanical Algorithm for Database Search*, 1996.
  - 総当たり探索を平方根オーダーにするGrover探索。hash-lab では小規模な Grover風探索シミュレーションの背景として扱う。
- Peter W. Shor, *Algorithms for Quantum Computation: Discrete Logarithms and Factoring*, 1994.
  - 署名方式や公開鍵暗号に大きい影響を持つShorアルゴリズム。hash-lab の主軸である avalanche / distinguisher とは別の背景文献として置く。

## Topics to Add

- Differential cryptanalysis
- Meet-in-the-middle attacks
- Hash function distinguishers
- Random oracle model
- Avalanche criteria
