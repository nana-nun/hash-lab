# Issue Workflow for Humans

hash-lab では、研究・実験・参考資料収集・コード生成を GitHub Issue で管理します。

## Basic Rule

1 Issue = 1つの検証可能なタスクにします。

良いIssue:

- mini-sha の round 数別 avalanche 結果を CSV 保存する
- reduced-round SHA-256 cryptanalysis 文献を5本収集する
- results 保存用の JSON/CSV 出力オプションを CLI に追加する

大きすぎるIssue:

- neural cryptanalysis を全部やる
- SHA256 関連文献を全部調べる
- 実験基盤を完成させる

## Issue Types

| Label | 用途 |
| --- | --- |
| `t:exp` | 実験、測定、評価 |
| `t:ref` | 文献、リンク、読書メモ |
| `t:impl` | コード生成、機能追加、リファクタ |
| `t:docs` | README、docs、研究メモ |
| `t:maint` | 環境、CI、整理、運用 |

## Priority

| Label | 意味 |
| --- | --- |
| `p:0` | すぐ必要 |
| `p:1` | 次にやる |
| `p:2` | 後でよい |

## Status

| Label | 意味 |
| --- | --- |
| `s:ready` | 着手可能 |
| `s:block` | 外部要因や判断待ち |
| `s:research` | 先に調査が必要 |

## Title Format

タイトルは短く、何を完了すればよいか分かる形にします。

```text
[exp] mini-shaのround数別avalanche結果をCSV保存する
[ref] reduced-round SHA-256 cryptanalysis文献を5本収集する
[impl] CLIにJSON/CSV出力オプションを追加する
[docs] 実験ノート例を1本追加する
[maint] .venvセットアップ手順を整理する
```

## Body Format

Issue本文には、できるだけ次を含めます。

- Goal
- Context
- Tasks
- Acceptance Criteria
- References

実験Issueでは、さらに次を含めます。

- Hypothesis
- Baseline
- Metrics
- Reproducibility

参考資料Issueでは、URL、書籍名、論文題、著者、年、DOI、BibTeX有無を分かる範囲で残します。

## Done Criteria

Issueを閉じる前に、該当するものを残します。

- 実装Issue: 変更内容、テスト結果、制限
- 実験Issue: コマンド、seed、round数、dataset size、metrics、結果保存先
- 文献Issue: `references/papers.bib`、`references/links.md`、`references/notes/` の更新先
- docs Issue: 追加/更新したMarkdownファイル

## Initial Issue Examples

- `t:exp`: mini-shaのround数別avalanche結果をCSV保存する
- `t:exp`: distinguisherにrandom guess baselineを明示追加する
- `t:ref`: reduced-round SHA-256 cryptanalysis文献を5本収集する
- `t:impl`: results保存用のJSON/CSV出力オプションをCLIに追加する
- `t:docs`: 実験ノート例を1本追加する
