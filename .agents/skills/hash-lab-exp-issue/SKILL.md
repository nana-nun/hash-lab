---
name: hash-lab-exp-issue
description: Use with hash-lab-issue-runner when a GitHub Issue has the primary label t:exp or asks for experiments, measurements, evaluations, avalanche tests, distinguishers, baselines, saved metrics, or reproducible reduced-round/toy hash results.
---

# Hash Lab Experiment Issue

Use this skill after `hash-lab-issue-runner` has confirmed the Issue, labels, branch, and safety scope.

## Check Before Work

- Confirm the Issue states a concrete question, hypothesis, baseline, metrics, and reproducibility details.
- Read `docs/research-state.md` and `results/README.md` before designing or interpreting an experiment.
- Read any relevant prior `results/*/notes.md`, metrics CSV/JSON, and `references/notes/` files before claiming novelty or interpreting a result.
- If the Issue does not name a baseline, add the simplest relevant one before any neural or advanced model work.
- Keep the experiment local, reduced-scale, and inside toy hash or reduced-round SHA-like scope.
- Prefer small runs first. Record when a result is exploratory rather than conclusive.

## Expected Outputs

- Store saved experiment outputs under `results/<date>-<short-name>/` when the Issue asks for persistent results.
- Include `config.json` or equivalent parameters when a run is saved.
- Include metrics in machine-readable form when practical, such as `metrics.json` or CSV.
- Write `notes.md` in Japanese for human-facing experiment interpretation.

## Notes Structure

Use `docs/experiment-log-template.md` and keep these sections separate:

- `Question`
- `Hypothesis`
- `Setup`
- `Baseline`
- `Result`
- `Interpretation`
- `Limitations`
- `Next`

## Verification

- Run the exact CLI sample, script, or test that exercises the experiment path.
- Record command, seed, target hash or rounds, dataset size, model config, metrics, and execution timestamp when results are saved.
- Compare results against the baseline in the notes or final report.
- Compare new interpretations against `docs/research-state.md`; update it when the current understanding changes.
- Do not overstate negative results; say what was not tested.

## Done Criteria

- The Issue's metrics are reported.
- Saved result files are linked from the PR or final response.
- Limitations and concrete next steps are explicit.
- Any actionable follow-up from `Limitations` or `Next` is created as a separate Issue when it is not already covered.
