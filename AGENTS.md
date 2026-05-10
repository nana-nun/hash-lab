# hash-lab Agent Guide

このファイルは、hash-lab でAIエージェントが作業するときの一次参照です。迷ったら、まずこの方針を優先してください。

## Research Goal

このリポジトリの目的は「SHA256を破る」ことではありません。

目的は、toy hash や reduced-round SHA-like hash を使って、暗号学的ハッシュ関数がどこまで学習不能になるかを調べることです。

## Research Scope

対象にするもの:

- toy hash
- reduced-round SHA-like hash
- avalanche effect の測定
- neural distinguisher
- brute force baseline
- SAT/SMT による小規模探索
- Grover風探索のシミュレーション

対象外にするもの:

- 実在ネットワークへのマイニング最適化
- ウォレット、秘密鍵、署名の攻撃
- 実マイニングプールへの接続
- 実運用中システムへの攻撃手順
- 不正利用につながる具体的な攻撃手順

## Documentation

- 研究メモ、設計メモ、実験メモは基本的に Markdown (`.md`) で書く。
- 人間が読む文書は日本語で書く。例: `README.md`、`docs/`、`references/`、`results/*/notes.md`。
- AIエージェントが読む文書は英語で書く。例: `.agents/` 配下のワークフロー、スキル、ポリシー。
- 人間向け文書にコマンド名、列名、API名、セクション名などの技術的な識別子を書く場合は、英語のまま残してよい。
- 主張、仮説、結果を混ぜない。研究メモでは、できるだけ `Question`、`Hypothesis`、`Setup`、`Result`、`Interpretation`、`Limitations`、`Next` を分ける。
- 参考文献を追加するときは、URL、書籍名、論文題、著者、年、DOI が分かる範囲で必ず残す。
- BibTeXで管理できる文献は `references/papers.bib` に追加する。
- Web記事やリンク集は `references/links.md` に追加する。
- 読書メモは `references/notes/` に Markdown で作成する。

## Experiment Principle

AIモデルを使う前に、必ず単純なベースラインを用意する。

例:

- random guess
- brute force
- frequency analysis
- simple statistical test
- logistic regression / small MLP

AIモデルの精度だけでなく、ベースラインとの差分を記録する。

## Reproducibility

実験結果を保存する場合は、可能な範囲で以下を残す。

- 実行コマンド
- seed
- 対象hash / round数
- dataset size
- model config
- metrics
- 実行日時

結果を保存する場合は、`results/` 配下に実験ごとのディレクトリを作る。

```text
results/
  2026-05-08-avalanche-mini-sha/
    config.json
    metrics.json
    notes.md
```

## Issue Workflow

- タスク管理は GitHub Issue を基本にする。
- Issueの進行状況は GitHub Projects でも確認する。現在のProjectは `https://github.com/users/nana-nun/projects/2` を使う。
- 人間向けの運用は `docs/issue-workflow-human.md` を参照する。
- AI向けの運用は `.agents/issue-workflow-ai.md` を参照する。
- AIエージェントが GitHub CLI を使う場合は、フルパスではなく `gh ...` 形式で実行する。
- GitHub Projects を `gh project ...` で確認するには `read:project` scope が必要な場合がある。権限不足なら `gh auth refresh --hostname github.com -s read:project` を案内する。Status更新まで行う場合は `project` scope が必要になる場合がある。
- よく使うコマンド例:
  - `gh issue list --repo nana-nun/hash-lab --state open --limit 20`
  - `gh issue view <number> --repo nana-nun/hash-lab`
  - `gh project view 2 --owner "@me" --format json`
  - `gh project item-list 2 --owner "@me" --format json --limit 100`
  - `gh project field-list 2 --owner "@me" --format json`
  - `gh project item-edit --project-id <project-id> --id <item-id> --field-id <status-field-id> --single-select-option-id <option-id>`
  - `gh issue create --repo nana-nun/hash-lab --title "<title>" --label "t:exp" --body "<body>"`
  - `gh pr create --repo nana-nun/hash-lab --base master --head <branch> --title "<title>" --body "<body>"`
- Issueは `t:exp`、`t:ref`、`t:impl`、`t:docs`、`t:maint` のいずれかを基本分類にする。
- Issueラベルは基本分類の `t:*` と優先度の `p:*` を使い、進行状況は GitHub Projects の `Status` で管理する。新規Issueに `s:*` ラベルは付けない。
- 優先度は `p:0` = すぐ必要、`p:1` = 次にやる、`p:2` = 後でよい。迷う新規Issueは `p:2` から始め、ブロッカーや近い実験・実装の前提だけを `p:0` / `p:1` に上げる。詳しい基準は `docs/issue-workflow-human.md` と `.agents/issue-workflow-ai.md` を参照する。
- AIエージェントがIssueを担当するときは、claimコメントを書いた後、実装前に GitHub Projects の `Status` を `In Progress` に変更し、変更後の状態が見えることを確認する。Status更新または確認ができない場合は、ファイル変更や実装に進まず停止して報告する。
- PR作成後は、可能なら GitHub Projects の `Status` を `Review` に変更し、変更できない場合はPRまたは最終応答にその理由を残す。
- 実装前に関連Issueを確認し、完了後にテスト結果、実験結果、制限、残課題をIssueまたは最終応答に残す。
- 実装ブランチを切る前に `git fetch origin` し、原則として最新の `origin/main` から開始する。
- 未マージPRの成果物に依存するIssueは、そのPRブランチから派生し、PR本文に依存関係を書く。
- `docs/research-state.md`、`results/README.md`、`src/hash_lab/experiments.py` のような共有ファイルを更新する場合は、PR作成前に最新の `origin/main` を取り込み、衝突をローカルで解消してからpushする。
- scope外の攻撃的タスクはIssue化しない。既にある場合も進めず、研究範囲内の安全な代替に分解する。

## Python

- Pythonを動かす場合は、プロジェクト直下の `.venv` を使う。
- `.venv` がない場合は作成してから使う。
- `python -m hash_lab...` や inline script で `src/hash_lab` を import する場合は、PowerShellで `$env:PYTHONPATH="src"` を設定してから実行する。`ModuleNotFoundError: No module named 'hash_lab'` が出た場合は、まず `PYTHONPATH` の不足を疑う。
- 依存パッケージを追加するときは、理由と用途をREADMEまたは関連ドキュメントに残す。

PowerShell例:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Operational Notes

- Codex環境では、sandbox内のネットワークが `127.0.0.1:9` proxy に向いて `proxyconnect tcp ... actively refused` で失敗することがある。その場合は同じ `gh ...` / `git fetch` / `git push` 操作を権限付きで再実行し、必要に応じて環境設定で proxy 変数が解除されているか確認する。
- Codex環境では `.git` 配下に sandbox 由来の Deny ACL があり、通常権限のGitが `.git/index.lock` や `.git/ORIG_HEAD.lock` を作れないことがある。`git fetch`、`git switch`、`git merge`、`git add`、`git commit`、`git push` のような `.git` に書き込むGit操作は、失敗を待たず最初から権限付きで実行してよい。`git status`、`git diff`、`git log`、`git show` のような読み取り操作は通常実行でよい。
- `.codex/environments/environment.toml` は自動生成ファイルなので、手で変える場合は今回の詰まりを防ぐための最小限に留め、変更理由をPRまたは最終応答に残す。

## Change Policy

- 既存構成を尊重し、小さく検証可能な実験として追加する。
- 実験コードは、まず標準ライブラリまたは軽い依存で始める。
- 実装後は、該当するテストまたはCLIサンプルを実行する。
- 実験結果を解釈するときは、限界と未確認事項を明記する。
