# 実験結果 metadata.json schema

新しいCLI実験で結果ファイルを保存するときは、同じ結果ディレクトリに `metadata.json` を保存する。

## 目的

`metadata.json` は、人間が読む `notes.md` や機械可読なCSV/JSON結果をあとで再利用しやすくするための共通メタデータである。過去の結果には `config.json` だけがある場合もあり、それらは互換性のためそのまま残す。

## 保存場所

結果ファイル群と同じディレクトリに置く。

```text
results/<experiment>/
  metrics.csv
  summary.csv
  metadata.json
  notes.md
```

CLIで単一ファイルを保存する場合も、保存先の親ディレクトリに `metadata.json` を作る。複数の出力ファイルがあるCLIでは、共通の親ディレクトリに作る。

## Schema

| Field | Meaning |
| --- | --- |
| `schema_version` | metadata schema の整数バージョン。初期値は `1`。 |
| `metadata` | 実験固有の条件。例: `experiment`, `rounds`, `seeds`, `samples`, `baseline`, `model_config`。 |
| `command` | 実行時の `sys.argv`。 |
| `args` | CLI引数をJSON化したもの。`Path` は文字列で保存する。 |
| `git_commit` | 実行時点のGit commit hash。取得できない場合は `null`。 |
| `python` | Python version と implementation。 |
| `package_versions` | 実行環境で取得できた Python package versions。 |
| `outputs` | この実行が書いた主要ファイル名。 |

## 互換性方針

- 既存の `config.json` は削除しない。
- 過去結果に `metadata.json` がない場合も有効な結果として扱う。
- 新しいCLI保存処理では `metadata.json` を優先して追加する。
- 研究ノートで重要な解釈、制限、次の課題を書く場所は引き続き `notes.md` とする。
