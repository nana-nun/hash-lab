---
name: hash-lab-issue-runner
description: Use when working on a hash-lab GitHub Issue end-to-end, including reading the Issue, checking AGENTS.md safety scope, creating an issue branch, running reduced-scale experiments or implementation tasks, recording reproducibility details, validating with .venv commands, and preparing a PR with verification notes.
---

# Hash Lab Issue Runner

Use this skill for one GitHub Issue at a time in the `hash-lab` repository.

## Workflow

1. Read `AGENTS.md`, `.agents/issue-workflow-ai.md`, and any relevant task-specific skill.
2. Inspect the target GitHub Issue with `gh issue view <number>` and confirm the goal, tasks, acceptance criteria, references, and labels.
3. Confirm the Issue stays within hash-lab scope: toy hash, reduced-round SHA-like hash, avalanche measurement, local baselines, small simulations, references, docs, or maintenance.
4. Do not proceed with wallet, private key, signature, live network, mining pool, production system, or misuse-enabling tasks.
5. Check `git status --short --branch` before edits and preserve unrelated user changes.
6. Create a dedicated branch named `issue-<number>-<short-slug>`.
7. Use the project `.venv` for Python commands. Create it only if missing.
8. Make the smallest change that satisfies the Issue. For experiments, record command, seed, hash/rounds, dataset size, metrics, timestamp when useful, interpretation, limitations, and next steps.
9. Save experiment outputs under `results/<date>-<short-name>/` when the Issue asks for saved results.
10. Run the relevant tests or CLI sample before finishing.
11. Review `Limitations` and `Next` in any new or updated result notes. If a concrete follow-up is needed, create a separate GitHub Issue before finishing instead of hiding the work in the PR text.
12. Commit the changes, push the branch, and create a PR with `gh pr create`.
13. Include the Issue closing keyword, changed files summary, verification commands, results, limitations, created follow-up Issues, and remaining follow-ups in the PR body or final response.

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
