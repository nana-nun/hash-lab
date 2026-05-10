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

優先度は「重要度」だけでなく、次の作業順を決めるためのラベルです。迷ったら低めに置き、あとで見直します。

### `p:0`: すぐ必要

今の作業を進めるためのブロッカー、または安全・再現性・運用上すぐ直す必要があるものに使います。

例:

- 進行中IssueやPRを止めている不具合
- 実験結果の解釈を誤らせるデータ・計算・記録の誤り
- Project / Issue workflow が壊れていて、着手やレビューが進められない
- scope外や危険な方向へ作業が進むのを防ぐための修正

### `p:1`: 次にやる

近い実験・実装・調査の前提になるもの、または次の数タスク以内で処理したいものに使います。

例:

- 既に予定している実験Issueの設計に必要な文献調査
- 共有ファイルやCLIの改善で、複数の後続Issueを楽にするもの
- `Review` 中のPRから出た、merge前または直後に処理したい follow-up
- baseline や検証方法が不足していて、次の結果比較に影響するもの

### `p:2`: 後でよい

価値はあるが、今の作業を止めていないものに使います。新規Issueは、明確に急ぎでなければまず `p:2` から始めます。

例:

- 将来の実験候補
- 参考文献の追加調査
- 便利だが現在の検証には必須ではないCLIやdocs改善
- 調査メモから生まれた実装・実験の後回し候補

## Priority Review

優先度は固定ではありません。次のタイミングで見直します。

- 新しいPRを作る前
- `Review` 中のPRがmergeされた後
- 実験結果の `Limitations` / `Next` から follow-up Issue を作るとき
- open Issue が増えて `p:2` だけでは作業順が分かりにくくなったとき

見直し手順:

1. `p:0` は本当に今の作業を止めているものだけに絞る。
2. 次に進めたいIssueを少数だけ `p:1` に上げる。
3. 後でよい候補は `p:2` のままにする。
4. ラベルを変える場合は、可能ならIssueコメントに理由を短く残す。

既存Issueを一括で変更するときは、内容を読まずに機械的に上げ下げしません。特に `t:exp` は依存する結果ファイル、`t:ref` は後続実験、`t:impl` は共有コードへの影響を確認してから優先度を変えます。

## Status

進行状況はIssueラベルではなく、GitHub Projects の `Status` で管理します。

現在のProject:

- `https://github.com/users/nana-nun/projects/2`

推奨する `Status`:

| Status | 意味 |
| --- | --- |
| `Todo` | 未着手 |
| `Ready` | 着手可能 |
| `In Progress` | 作業中 |
| `Review` | PR確認中、または人間の確認待ち |
| `Blocked` | 外部要因や判断待ち |
| `Done` | 完了 |

`s:ready`、`s:block`、`s:research` のような状態ラベルは新規Issueでは使いません。

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
