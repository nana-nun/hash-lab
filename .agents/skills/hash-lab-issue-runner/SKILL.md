---
name: hash-lab-issue-runner
description: Use when working on a hash-lab GitHub Issue end-to-end, including reading the Issue, checking AGENTS.md safety scope, creating an issue branch, running reduced-scale experiments or implementation tasks, recording reproducibility details, validating with .venv commands, and preparing a PR with verification notes.
---

# Hash Lab Issue Runner

Use this skill for one GitHub Issue at a time in the `hash-lab` repository.

## Workflow

1. Read `AGENTS.md`, `.agents/issue-workflow-ai.md`, and any relevant task-specific skill.
2. Inspect the target GitHub Issue with `gh issue view <number>` and confirm the goal, tasks, acceptance criteria, references, and labels.
3. Check GitHub Projects #2 when access is available:
   - `gh project view 2 --owner "@me" --format json`
   - `gh project item-list 2 --owner "@me" --format json --limit 100`
   - `gh project field-list 2 --owner "@me" --format json`
   - If the token lacks `read:project`, ask the user to run `gh auth refresh --hostname github.com -s read:project`.
   - If project field updates are required, the token may need `project` scope.
4. Compare the Issue's project `Status` with the planned work. Treat project `Status` as the source of truth for readiness and workflow state.
5. Before implementation, claim the Issue with a comment, update the GitHub Projects `Status` to `In Progress`, and verify the Issue no longer shows `Todo` or `Ready`. Use `gh project item-edit` with the project item id, `Status` field id, and target option id discovered from `gh project item-list` / `gh project field-list`. If the status update or verification fails, stop without file changes.
6. Identify exactly one primary `t:*` label and read the matching label skill:
   - `t:exp`: `hash-lab-exp-issue`
   - `t:ref`: `hash-lab-ref-issue`
   - `t:impl`: `hash-lab-impl-issue`
   - `t:docs`: `hash-lab-docs-issue`
   - `t:maint`: `hash-lab-maint-issue`
7. Treat `p:*` labels as priority signals. Do not add or rely on `s:*` labels for status; use GitHub Projects `Status`.
8. Confirm the Issue stays within hash-lab scope: toy hash, reduced-round SHA-like hash, avalanche measurement, local baselines, small simulations, references, docs, or maintenance.
9. Do not proceed with wallet, private key, signature, live network, mining pool, production system, or misuse-enabling tasks.
10. Check `git status --short --branch` before edits and preserve unrelated user changes.
11. Before creating the branch, synchronize the base with `git fetch origin` and start from the latest `origin/main` unless the Issue explicitly depends on an unmerged PR.
12. If the Issue depends on an unmerged PR, branch from that PR branch and say so in the PR body. Do not create a sibling PR from stale `main` when it updates shared files such as `docs/research-state.md`, `results/README.md`, or `src/hash_lab/experiments.py`.
13. Create a dedicated branch named `issue-<number>-<short-slug>`.
14. Use the project `.venv` for Python commands. Create it only if missing.
15. Make the smallest change that satisfies the Issue, using the label skill for output placement and verification details.
16. Run the relevant tests, validation command, or CLI sample before finishing.
17. Before committing or opening the PR, fetch and merge or rebase the latest `origin/main`, resolve conflicts locally, and rerun verification. Prefer fixing conflicts before the PR is created over leaving GitHub's "This branch has conflicts" state for the user.
18. Review any `Limitations` and `Next` notes. If a concrete follow-up is needed, create a separate GitHub Issue before finishing instead of hiding the work in the PR text.
19. Commit the changes, push the branch, and create a PR with `gh pr create`.
20. After opening the PR, update the GitHub Projects `Status` to `Review` when possible and verify it. If the update fails, record the reason in the PR or final response.
21. Include the Issue closing keyword, changed files summary, verification commands, results, GitHub Projects status observations, limitations, created follow-up Issues, and remaining follow-ups in the PR body or final response.

## Experiment Notes

Use `docs/experiment-log-template.md` as the default structure:

- `Question`
- `Hypothesis`
- `Setup`
- `Baseline`
- `Result`
- `Interpretation`
- `Limitations`
- `Next`

Keep claims, hypotheses, and results separate.

## Label Skills

Use the primary `t:*` label to load the task-specific guide:

| Label | Skill | Use for |
| --- | --- | --- |
| `t:exp` | `hash-lab-exp-issue` | experiments, measurements, metrics, saved results |
| `t:ref` | `hash-lab-ref-issue` | papers, links, BibTeX, reading notes |
| `t:impl` | `hash-lab-impl-issue` | code, CLI behavior, tests, refactors |
| `t:docs` | `hash-lab-docs-issue` | README, docs, Japanese research notes |
| `t:maint` | `hash-lab-maint-issue` | environment, CI, repo hygiene, skills |

## PR Checklist

- Reference the Issue with `Closes #<number>` when the acceptance criteria are fully satisfied.
- Mention the branch name.
- List the exact verification command and result.
- For experiments, mention where the result files are stored.
- Mention any follow-up Issues created from the result interpretation.
- State limitations plainly instead of overstating the result.

## Follow-up Issue Checklist

- Create follow-up Issues from concrete `Limitations` or `Next` items when they are actionable and not already covered by an open Issue.
- Keep follow-up Issues inside the hash-lab safety scope.
- Use a human-readable Japanese Issue body for GitHub Issues.
- Include `Goal`, `Context`, `Tasks`, `Acceptance Criteria`, and `References`.
- For experiment follow-ups, also include `Hypothesis`, `Baseline`, `Metrics`, and `Reproducibility`.
- Link the source Issue, result directory, metrics file, and notes file when available.
