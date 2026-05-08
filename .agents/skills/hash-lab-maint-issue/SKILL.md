---
name: hash-lab-maint-issue
description: Use with hash-lab-issue-runner when a GitHub Issue has the primary label t:maint or asks for environment setup, CI, repository cleanup, dependency management, workflow updates, skill maintenance, or operational hygiene in hash-lab.
---

# Hash Lab Maintenance Issue

Use this skill after `hash-lab-issue-runner` has confirmed the Issue, labels, branch, and safety scope.

## Check Before Work

- Identify whether the task changes developer workflow, CI, dependencies, repository structure, or agent instructions.
- Keep maintenance changes narrow and reversible.
- Preserve unrelated user changes and generated results.
- Avoid adding dependencies unless they reduce repeated work or are required by the Issue.

## Maintenance Areas

- Environment: `.venv`, setup instructions, dependency files, and reproducible commands.
- CI and checks: test commands, lint commands, and validation scripts.
- Repository hygiene: file organization, stale docs, issue workflow, labels, and templates.
- Skills and agents: `.agents/skills/`, `.agents/issue-workflow-ai.md`, and agent-facing policy updates.

## Verification

- Run the smallest command that validates the maintenance change.
- For skills, run `quick_validate.py` on each new or updated skill.
- For workflow docs, use `rg` to confirm the documented labels, paths, or skill names exist.
- For dependency or setup changes, verify commands inside the project `.venv` when Python is involved.

## Done Criteria

- The maintenance change is documented where future agents or humans will look.
- Validation output is reported in the PR or final response.
- Any residual operational risk or follow-up cleanup is stated plainly.
