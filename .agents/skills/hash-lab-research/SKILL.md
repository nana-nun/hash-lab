---
name: hash-lab-research
description: Use when working in the hash-lab repository on reduced-round hash experiments, Markdown research notes, reference management, Python .venv execution, experiment reproducibility, or toy/neural cryptanalysis workflows.
---

# Hash Lab Research

## Workflow

1. Read `AGENTS.md` first and follow it as the primary policy.
2. Keep the research scope limited to toy hash, reduced-round SHA-like hash, and small-scale simulations.
3. Store research notes as Markdown and keep references under `references/`.
4. Use `.venv` before running Python commands.
5. Add a simple baseline before AI/neural experiments.
6. Record commands, seed, config, metrics, and limitations when saving results.
7. Run the relevant test or CLI sample after implementation.

## Research Notes

When writing experiment notes, separate:

- `Question`
- `Hypothesis`
- `Setup`
- `Baseline`
- `Result`
- `Interpretation`
- `Limitations`
- `Next`

Use `docs/experiment-log-template.md` as the default template.

## Safety Boundary

Do not provide or implement workflows for attacking wallets, private keys, signatures, live mining pools, real networks, or production systems. Keep experiments educational, local, and reduced-scale.
