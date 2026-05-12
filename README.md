# hash-lab

縮小ラウンドハッシュがどこまで「学習不能」になるかを調べるための研究MVPです。

このリポジトリは SHA256 の完全攻略を目的にしません。代わりに、SHA256 風の小さなハッシュ関数を作り、ラウンド数を変えながら次の性質を測定します。

- Avalanche Effect: 入力を 1 bit 変えたとき出力がどれくらい変わるか
- Reduced Round: ラウンド数が少ないときに偏りや相関が残るか
- Neural/ML Cryptanalysis: 簡単な識別器がハッシュ出力とランダム列を見分けられるか

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m src.hash_lab.cli avalanche --rounds 4 8 16 32 --samples 200
python -m src.hash_lab.cli distinguish --rounds 2 4 8 16 --samples 1000 --epochs 8
python -m src.hash_lab.cli low-order-stats --rounds 4 8 --samples 200 --seeds 1 --summary-output results/low-order-summary.csv --block-output results/low-order-blocks.csv
python -m src.hash_lab.cli avalanche-vectors --rounds 12 13 --samples 20 --seeds 1 --vector-output results/avalanche-vectors.csv
python -m unittest discover -s tests
```

実験結果を `results/` 配下に保存する例:

```powershell
python -m src.hash_lab.cli avalanche --rounds 2 4 8 16 32 --samples 500 --seed 1 --output results/avalanche.csv --format csv
python -m src.hash_lab.cli distinguish --rounds 2 4 8 16 --samples 1000 --epochs 8 --seed 1 --output results/distinguish.json --format json
python -m src.hash_lab.cli low-order-stats --rounds 2 4 8 16 --samples 500 --seeds 1 2 3 --block-size 4 --summary-output results/low-order-summary.csv --block-output results/low-order-blocks.csv
python -m src.hash_lab.cli avalanche-vectors --rounds 12 13 14 --samples 500 --seeds 1 2 3 --fixed-input-bit 255 --vector-output results/avalanche-vectors.csv
```

`--output` を指定しない場合は、従来どおり標準出力だけに結果を表示します。保存するCSVには `experiment`、`seed`、`rounds`、`samples` などの実行条件を含めます。JSONは `metadata` と `results` に分けて保存します。

`low-order-stats` は ML classifier を使わず、`mini_sha` のdigest列と同じ長さのrandom bit列について、ones rate、runs count、longest run、2-bit/4-bit block frequencyを集計します。`summary-output` には round・seed・samples・hash設定と低次統計の要約、`block-output` には block値ごとの頻度と一様分布との差分を保存します。

`avalanche-vectors` は BIC / output bit pair correlation の前処理として、sample単位の avalanche vector をCSV保存します。CSVには `rounds`、`seed`、`sample_index`、`input_bit_index`、`output_bits`、`avalanche_hex` が含まれます。`--fixed-input-bit` を指定すると入力bitを固定し、省略すると各sampleでランダムな入力bitを反転します。

実験ノートを書くときは `docs/experiment-log-template.md` を使います。書き方の例として、`docs/experiment-log-example-avalanche-mini-sha.md` に mini-sha avalanche の小規模実験ノートがあります。

現在の実験結果と先行研究の接続は `docs/research-state.md` にまとめています。保存済み結果の索引は `results/README.md`、文献メモは `references/notes/` を参照してください。

## Working Rules

このリポジトリで作業するときの一次参照は `AGENTS.md` です。Repo内Skillは `.agents/skills/hash-lab-research/` にあります。

## Project Layout

```text
docs/       研究メモと実験方針
references/ 参考文献、BibTeX、読書メモ
src/        実験用コード
tests/      単体テスト
results/    実験結果の保存先
notebooks/  将来の分析ノート置き場
```

## Current MVP

`src/hash_lab/mini_sha.py` は教育・研究用の SHA256 風 toy hash です。32 bit word、ARX 演算、ラウンド数切替、固定長出力を備えています。

実験の主眼は「ラウンド数が増えるにつれて、出力がランダムと区別しにくくなるか」を観察することです。

## Safety Scope

このプロジェクトは縮小ラウンド・toy hash の学習可能性を扱います。実運用中の暗号資産ネットワーク、ウォレット、鍵、署名、マイニングプールに対する攻撃や不正利用は扱いません。
