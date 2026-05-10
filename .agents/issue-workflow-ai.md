# Issue Workflow for AI Agents

hash-lab でIssueを読む、作る、実装するときのAI向け手順です。

## First Steps

1. Read `AGENTS.md`.
2. Confirm the task stays inside the research scope.
3. Read the relevant Issue and linked files.
4. Check the current GitHub Projects entry when project access is available.
5. If the Issue is too broad, split it into smaller proposed Issues instead of implementing everything at once.

## Safety Boundary

Do not create or implement Issues for:

- attacking wallets, private keys, signatures, live mining pools, real networks, or production systems
- optimizing real mining operations
- producing concrete misuse instructions

Keep work local, educational, and reduced-scale.

## Creating Issues

Use one primary type label:

- `t:exp`
- `t:ref`
- `t:impl`
- `t:docs`
- `t:maint`

Use at most one priority label:

- `p:0`
- `p:1`
- `p:2`

Priority labels guide work ordering:

- Use `p:0` only for blockers, urgent correctness/reproducibility fixes, workflow failures that prevent current work, or safety/scope corrections.
- Use `p:1` for work that should happen next because it unblocks or materially improves near-term experiments, implementation, review, or interpretation.
- Use `p:2` for useful backlog work that does not block the current path. Default new Issues to `p:2` when urgency is unclear.

When reviewing existing Issues, do not bulk-change priority mechanically. Read dependencies, referenced result files, related PRs, and current Project `Status` first. Keep `p:0` small enough that it means "do this before normal work". Prefer a small set of `p:1` Issues over marking the whole backlog as next.

Do not add `s:*` status labels to new Issues. Use the GitHub Projects `Status` field for workflow state.

## GitHub Projects

Use `https://github.com/users/nana-nun/projects/2` as the current hash-lab planning project.

When project access is available, check the project before implementation and again before finishing:

```powershell
gh project view 2 --owner "@me" --format json
gh project item-list 2 --owner "@me" --format json --limit 100
gh project field-list 2 --owner "@me" --format json
```

Use the project `Status` field for workflow state such as `Todo`, `Ready`, `In Progress`, `Review`, `Done`, or `Blocked` when those options exist. Keep Issue labels for type (`t:*`) and priority (`p:*`). Do not create new `s:*` labels.

When an AI agent claims an Issue, the claim is not complete until the GitHub Projects `Status` is updated from `Todo` or `Ready` to `In Progress` and then verified. Do this before creating files, running experiments, or implementing code. If the status update or verification fails, stop without implementation and report the blocker.

When a PR is opened for an Issue, update the GitHub Projects `Status` to `Review` when the option exists. If that update fails, leave a clear note in the PR or final response.

Use `gh project item-edit` with the project item id, the `Status` field id, and the target single-select option id discovered from `gh project item-list` and `gh project field-list`. After editing, rerun `gh issue view <number> --repo nana-nun/hash-lab --json projectItems` or `gh project item-list ...` and confirm the visible status changed.

If `gh project ...` fails because the token is missing `read:project`, ask the user to run:

```powershell
gh auth refresh --hostname github.com -s read:project
```

If the task requires updating project fields, the token may need the broader `project` scope:

```powershell
gh auth refresh --hostname github.com -s project
```

## Required Issue Content

Prefer this structure:

```markdown
## Goal

## Context

## Tasks

- [ ] ...

## Acceptance Criteria

- [ ] ...

## References
```

For experiment Issues, include:

```markdown
## Hypothesis

## Baseline

## Metrics

## Reproducibility

- Command:
- Seed:
- Hash / rounds:
- Dataset size:
- Model config:
```

For reference Issues, capture URL, book title, paper title, authors, year, DOI, and BibTeX status when available.

## Implementing Issues

- Check the Issue's GitHub Projects `Status` when available. If it is not `Ready`, `Todo`, or otherwise clearly available for work, mention the mismatch before proceeding.
- After writing the claim comment, update the Issue's GitHub Projects `Status` to `In Progress` and verify the updated status is visible. Do not implement if the Issue remains `Todo` or `Ready`.
- Before creating an implementation branch, run `git fetch origin` and start from the latest `origin/main`.
- If the Issue depends on an unmerged PR, branch from that PR branch and mention the dependency in the PR body.
- Avoid sibling PRs from stale `main` when changing shared files such as `docs/research-state.md`, `results/README.md`, or `src/hash_lab/experiments.py`; these files are frequent conflict points.
- Use `.venv` for Python commands. For module execution or inline scripts that import `hash_lab`, set `PYTHONPATH=src` first, for example PowerShell `$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m hash_lab.cli ...`.
- If a Python command fails with `ModuleNotFoundError: No module named 'hash_lab'`, retry once with `PYTHONPATH=src` before changing code.
- Before experiment analysis, read `docs/research-state.md`, `results/README.md`, relevant `results/*/notes.md`, and relevant `references/notes/`.
- Add a baseline before AI/neural experiments.
- Save experiment outputs under `results/` when results are part of the task.
- Update `references/` for literature tasks.
- Update `docs/research-state.md` when a completed experiment or reference task changes the current interpretation of the project.
- Run the relevant test or CLI sample before finishing.
- Before opening a PR, fetch and merge or rebase the latest `origin/main`, resolve conflicts locally, and rerun verification.
- After opening a PR, update the Issue's GitHub Projects `Status` to `Review` when possible and verify or report the blocker.
- Report changed files, verification, GitHub Projects status observations, and remaining limitations in the Issue or final response.

## Local Environment Blockers

- If `gh ...` or `git fetch` fails with a proxy error to `127.0.0.1:9`, retry the same network operation with the approved/escalated execution path instead of changing repository files.
- If a git command fails with `.git/*.lock` `Permission denied`, retry the same git operation with the approved/escalated execution path. Do not delete lock files unless a human explicitly asks and the resolved path has been checked.
- If `.codex/environments/environment.toml` is changed, keep the edit narrow because the file is autogenerated. Prefer changes that prevent repeated setup failures, such as clearing proxy variables or setting `PYTHONPATH`.

## Label Skills

When implementing an Issue, use `hash-lab-issue-runner` for the common workflow and then read the skill that matches the primary `t:*` label.

| Label | Skill | Focus |
| --- | --- | --- |
| `t:exp` | `hash-lab-exp-issue` | 実験設計、baseline、metrics、`results/`、再現性 |
| `t:ref` | `hash-lab-ref-issue` | 文献、リンク、BibTeX、読書メモ、出典確認 |
| `t:impl` | `hash-lab-impl-issue` | コード変更、CLI/API互換性、テスト、最小変更 |
| `t:docs` | `hash-lab-docs-issue` | README、docs、人間向け日本語Markdown、研究メモ |
| `t:maint` | `hash-lab-maint-issue` | 環境、CI、依存、リポジトリ整理、Skill整備 |

Use `p:*` labels for priority. Use GitHub Projects `Status` for readiness and workflow state.
