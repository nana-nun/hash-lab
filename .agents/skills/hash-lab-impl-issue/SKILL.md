---
name: hash-lab-impl-issue
description: Use with hash-lab-issue-runner when a GitHub Issue has the primary label t:impl or asks for code implementation, feature additions, refactors, CLI changes, output formats, tests, or local hash-lab tooling changes.
---

# Hash Lab Implementation Issue

Use this skill after `hash-lab-issue-runner` has confirmed the Issue, labels, branch, and safety scope.

## Check Before Work

- Inspect existing code, tests, CLI entrypoints, and naming patterns before editing.
- Keep the change as small as the Issue allows.
- Prefer standard library or existing dependencies unless the Issue explicitly justifies a new package.
- Preserve CLI/API compatibility unless the Issue asks for a breaking change.
- Do not implement functionality that targets real mining, wallets, private keys, signatures, live networks, or production systems.

## Implementation Shape

- Add or update tests near the behavior being changed.
- For result export or experiment tooling, keep outputs reproducible and easy to cite from `results/`.
- For CLI changes, document new flags or output behavior in the relevant human-facing Markdown when needed.
- If the Issue is too broad, split it into smaller follow-up Issues before implementing unrelated features.

## Verification

- Use the project `.venv` for Python commands.
- Run focused tests first, then broader tests when shared behavior changes.
- Run a CLI sample when the change affects command-line behavior.
- Record exact commands and outcomes in the PR or final response.

## Done Criteria

- The acceptance criteria are satisfied by code and tests.
- New behavior has a focused test or a clearly explained manual verification command.
- Any limitations, compatibility notes, or follow-up Issues are explicit.
