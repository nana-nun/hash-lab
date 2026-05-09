# Reading List

## Core: Hash Functions and Reduced-Round SHA-like Analysis

- NIST, FIPS PUB 180-4, *Secure Hash Standard (SHS)*, 2015.
  - BibTeX: `nist_fips_180_4`
  - SHA-1/SHA-2系の標準仕様。SHA256の構造確認用。標準名、略称、title表記が揺れやすいので、hash-lab では `FIPS PUB 180-4: Secure Hash Standard (SHS)` として扱う。
- Henri Gilbert and Helena Handschuh, *Security Analysis of SHA-256 and Sisters*, 2003.
  - SHA-256系の初期解析研究。
- Somitra Kumar Sanadhya and Palash Sarkar, *Attacking Reduced Round SHA-256*, 2008.
  - 18-step collision と24-step semi-free-start collision を扱う、reduced-round SHA-256解析の出発点として使う。
- Ivica Nikolić and Alex Biryukov, *Collisions for Step-Reduced SHA-256*, 2008.
  - step-reduced SHA-256 の collision / semi-free-start collision / near-collision の基準文献。
- Kazumaro Aoki, Jian Guo, Krystian Matusiewicz, Yu Sasaki, and Lei Wang, *Preimages for Step-Reduced SHA-2*, 2009.
  - reduced SHA-2 の preimage attack を調べるときの比較対象。toy preimage baseline の設計にも関係する。
- Alex Biryukov, Mario Lamberger, Florian Mendel, and Ivica Nikolić, *Second-Order Differential Collisions for Reduced SHA-256*, 2011.
  - higher-order / second-order differential の観点から、bit差分や局所差分をどう見るかの参考。
- Dmitry Khovratovich, Christian Rechberger, and Alexandra Savelieva, *Bicliques for Preimages: Attacks on Skein-512 and the SHA-2 Family*, 2011.
  - SHA-2 family への biclique preimage attack。小規模探索やGrover風探索と比較するときの背景文献。
- Florian Mendel, Tomislav Nad, and Martin Schläffer, *Improving Local Collisions: New Attacks on Reduced SHA-256*, 2013.
  - 28-step collision、31-step collision、38-step semi-free-start collision など、局所衝突探索の改善を追うために読む。
- Christophe De Cannière and Christian Rechberger, *Finding SHA-1 Characteristics: General Results and Applications*, 2006.
  - 差分特性探索の考え方の参考。

## Core: Avalanche Criteria and Hash Measurements

- A. F. Webster and Stafford E. Tavares, *On the Design of S-Boxes*, 1986.
  - BibTeX: `webster_design_1986`
  - Note: `references/notes/webster-tavares-sboxes-1986.md`
  - avalanche effect と Strict Avalanche Criterion の源流として読む。hash-lab の bit flip 実験で「平均0.5」を baseline にする理由を整理するための基礎文献。
- Réjane Forré, *The Strict Avalanche Criterion: Spectral Properties of Boolean Functions and an Extended Definition*, 1988.
  - BibTeX: `forre_strict_1988`
  - Note: `references/notes/forre-strict-avalanche-1988.md`
  - SAC を Boolean function の spectral property として扱う文献。toy hash の出力bit単位の偏りを見るときの理論背景。
- Sheelagh Lloyd, *Counting Binary Functions with Certain Cryptographic Properties*, 1992.
  - SAC、balance、correlation immunity の関係を整理する文献。avalanche だけで「安全」と言い切れない理由の確認に使う。
- Darshana Upadhyay, Nupur Gaikwad, Marzia Zaman, and Srinivas Sampalli, *Investigating the Avalanche Effect of Various Cryptographically Secure Hash Functions and Hash-Based Applications*, 2022.
  - BibTeX: `upadhyay_avalanche_2022`
  - Note: `references/notes/upadhyay-avalanche-2022.md`
  - 複数の実ハッシュ関数と hash-based application で avalanche / SAC / BIC / randomness tests を測った実験研究。hash-lab の測定項目を増やすときの比較対象。

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
  - distinguish problem を機械学習 classifier として定式化する一般的な方法論。hash出力 vs random bit列の local distinguisher 実験の枠組み整理に使う。
- Ongee Jeong and Inkyu Moon, *Deep Learning-Based Hash Function Cryptanalysis*, 2024.
  - MD5 の step 数を変え、fully-connected neural network と BiLSTM で学習する hash function 寄りの最近例。hash-lab の reduced-round/toy hash の学習実験と近いが、短い conference paper なので補助文献として扱う。
- François-Xavier Standaert, *Introduction to Side-Channel Attacks*, 2010.
  - ML暗号解析とは別系統だが、統計的漏洩・識別の考え方の参考。

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
