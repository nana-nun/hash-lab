---
name: hash-lab-docs-issue
description: Use with hash-lab-issue-runner when a GitHub Issue has the primary label t:docs or asks for README/docs updates, Japanese research notes, experiment note examples, documentation cleanup, or human-facing Markdown in hash-lab.
---

# Hash Lab Docs Issue

Use this skill after `hash-lab-issue-runner` has confirmed the Issue, labels, branch, and safety scope.

## Check Before Work

- Write human-facing repository documentation in Japanese.
- Keep command names, paths, API names, section names, and labels in English when they are technical identifiers.
- Separate claims, hypotheses, results, interpretation, limitations, and next steps.
- Keep docs inside the safe research framing: toy hash, reduced-round SHA-like hash, local experiments, and educational analysis.

## File Placement

- Use `README.md` for top-level orientation.
- Use `docs/` for human workflow, design notes, and reusable explanations.
- Use `results/*/notes.md` for experiment-specific interpretation.
- Use `references/` for literature and source material rather than general docs.

## Writing Guidance

- Prefer concise sections with actionable examples.
- Include commands only when they are safe, local, and reproducible.
- Link related Issues, result directories, references, or templates when they help future work.
- Do not mix a result claim into a hypothesis section.

## Verification

- Check Markdown rendering shape by reading the changed file.
- Run `rg` for renamed headings, paths, or links when relevant.
- If docs mention commands, run the command or state clearly when it is not run.

## Done Criteria

- The requested docs are added or updated in the expected location.
- The prose is Japanese where human-facing.
- The PR or final response lists changed docs and any commands verified.
