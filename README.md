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
python -m unittest discover -s tests
```

実験結果を `results/` 配下に保存する例:

```powershell
python -m src.hash_lab.cli avalanche --rounds 2 4 8 16 32 --samples 500 --seed 1 --output results/avalanche.csv --format csv
python -m src.hash_lab.cli distinguish --rounds 2 4 8 16 --samples 1000 --epochs 8 --seed 1 --output results/distinguish.json --format json
```

`--output` を指定しない場合は、従来どおり標準出力だけに結果を表示します。保存するCSVには `experiment`、`seed`、`rounds`、`samples` などの実行条件を含めます。JSONは `metadata` と `results` に分けて保存します。

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
