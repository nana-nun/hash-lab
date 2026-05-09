# Issue Workflow for AI Agents

hash-lab でIssueを読む、作る、実装するときのAI向け手順です。

## First Steps

1. Read `AGENTS.md`.
2. Confirm the task stays inside the research scope.
3. Read the relevant Issue and linked files.
4. If the Issue is too broad, split it into smaller proposed Issues instead of implementing everything at once.

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

Use status labels only when helpful:

- `s:ready`
- `s:block`
- `s:research`

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

- Use `.venv` for Python commands.
- Before experiment analysis, read `docs/research-state.md`, `results/README.md`, relevant `results/*/notes.md`, and relevant `references/notes/`.
- Add a baseline before AI/neural experiments.
- Save experiment outputs under `results/` when results are part of the task.
- Update `references/` for literature tasks.
- Update `docs/research-state.md` when a completed experiment or reference task changes the current interpretation of the project.
- Run the relevant test or CLI sample before finishing.
- Report changed files, verification, and remaining limitations in the Issue or final response.

## Label Skills

When implementing an Issue, use `hash-lab-issue-runner` for the common workflow and then read the skill that matches the primary `t:*` label.

| Label | Skill | Focus |
| --- | --- | --- |
| `t:exp` | `hash-lab-exp-issue` | 実験設計、baseline、metrics、`results/`、再現性 |
| `t:ref` | `hash-lab-ref-issue` | 文献、リンク、BibTeX、読書メモ、出典確認 |
| `t:impl` | `hash-lab-impl-issue` | コード変更、CLI/API互換性、テスト、最小変更 |
| `t:docs` | `hash-lab-docs-issue` | README、docs、人間向け日本語Markdown、研究メモ |
| `t:maint` | `hash-lab-maint-issue` | 環境、CI、依存、リポジトリ整理、Skill整備 |

Use `p:*` labels for priority and `s:*` labels for readiness/research state. Do not treat them as separate implementation workflows.
