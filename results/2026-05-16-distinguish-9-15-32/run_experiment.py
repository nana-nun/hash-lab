"""Run Issue #53 logistic regression distinguisher measurements."""

from __future__ import annotations

import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

from hash_lab.experiments import bootstrap_mean_ci, distinguish, git_commit_hash, write_rows_csv


OUT_DIR = Path(__file__).resolve().parent
ROUNDS = [9, 10, 11, 12, 13, 14, 15, 32]
SEEDS = [1, 2, 3, 4, 5]
SAMPLES = 2000
EPOCHS = 8
LEARNING_RATE = 0.08
RANDOM_GUESS_BASELINE = 0.5
BOOTSTRAP_ITERATIONS = 2000
BOOTSTRAP_SEED = 20260516
CI_LEVEL = 0.95
COMMAND = r".\.venv\Scripts\python.exe results\2026-05-16-distinguish-9-15-32\run_experiment.py"


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values) / (len(values) - 1))


def fmt(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def main() -> None:
    executed_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    seed_rows: list[dict[str, object]] = []
    aggregate_rows: list[dict[str, object]] = []

    for rounds in ROUNDS:
        round_rows: list[dict[str, object]] = []
        for seed in SEEDS:
            result = distinguish(rounds, samples=SAMPLES, epochs=EPOCHS, seed=seed)
            row = {
                "rounds": rounds,
                "seed": seed,
                "samples": result.samples,
                "epochs": result.epochs,
                "random_guess_baseline": fmt(result.random_guess_baseline, 4),
                "majority_baseline": fmt(result.majority_baseline, 4),
                "train_accuracy": fmt(result.train_accuracy, 4),
                "test_accuracy": fmt(result.test_accuracy, 4),
                "test_accuracy_minus_baseline": fmt(result.test_accuracy_minus_baseline, 4),
                "train_test_gap": fmt(result.train_accuracy - result.test_accuracy, 4),
            }
            seed_rows.append(row)
            round_rows.append(row)

        deltas = [float(row["test_accuracy_minus_baseline"]) for row in round_rows]
        ci_low, ci_high = bootstrap_mean_ci(
            deltas,
            iterations=BOOTSTRAP_ITERATIONS,
            ci_level=CI_LEVEL,
            seed=BOOTSTRAP_SEED + rounds,
        )
        aggregate_rows.append(
            {
                "rounds": rounds,
                "seed_count": len(SEEDS),
                "samples": SAMPLES,
                "epochs": EPOCHS,
                "random_guess_baseline": fmt(RANDOM_GUESS_BASELINE, 4),
                "mean_majority_baseline": fmt(mean([float(row["majority_baseline"]) for row in round_rows]), 4),
                "mean_train_accuracy": fmt(mean([float(row["train_accuracy"]) for row in round_rows]), 4),
                "mean_test_accuracy": fmt(mean([float(row["test_accuracy"]) for row in round_rows]), 4),
                "mean_test_accuracy_minus_baseline": fmt(mean(deltas), 4),
                "stdev_test_accuracy_minus_baseline": fmt(sample_stdev(deltas), 4),
                "min_test_accuracy_minus_baseline": fmt(min(deltas), 4),
                "max_test_accuracy_minus_baseline": fmt(max(deltas), 4),
                "mean_train_test_gap": fmt(mean([float(row["train_test_gap"]) for row in round_rows]), 4),
                "ci_level": fmt(CI_LEVEL, 4),
                "ci_method": "seed_mean_percentile_bootstrap",
                "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
                "bootstrap_seed": BOOTSTRAP_SEED + rounds,
                "baseline_delta_ci_low": fmt(ci_low, 4),
                "baseline_delta_ci_high": fmt(ci_high, 4),
                "ci_contains_zero": ci_low <= 0.0 <= ci_high,
            }
        )

    seed_fieldnames = [
        "rounds",
        "seed",
        "samples",
        "epochs",
        "random_guess_baseline",
        "majority_baseline",
        "train_accuracy",
        "test_accuracy",
        "test_accuracy_minus_baseline",
        "train_test_gap",
    ]
    aggregate_fieldnames = [
        "rounds",
        "seed_count",
        "samples",
        "epochs",
        "random_guess_baseline",
        "mean_majority_baseline",
        "mean_train_accuracy",
        "mean_test_accuracy",
        "mean_test_accuracy_minus_baseline",
        "stdev_test_accuracy_minus_baseline",
        "min_test_accuracy_minus_baseline",
        "max_test_accuracy_minus_baseline",
        "mean_train_test_gap",
        "ci_level",
        "ci_method",
        "bootstrap_iterations",
        "bootstrap_seed",
        "baseline_delta_ci_low",
        "baseline_delta_ci_high",
        "ci_contains_zero",
    ]
    write_rows_csv(OUT_DIR / "seed_metrics.csv", seed_fieldnames, seed_rows)
    write_rows_csv(OUT_DIR / "aggregate_metrics.csv", aggregate_fieldnames, aggregate_rows)

    config = {
        "experiment": "distinguish-9-15-32",
        "issue": 53,
        "command": COMMAND,
        "executed_at": executed_at,
        "rounds": ROUNDS,
        "seeds": SEEDS,
        "samples_per_seed_per_round": SAMPLES,
        "epochs": EPOCHS,
        "model_config": {
            "model": "logistic_regression",
            "learning_rate": LEARNING_RATE,
            "features": "256 centered digest bits",
            "train_split": 0.8,
        },
        "baseline": {
            "random_guess_accuracy": RANDOM_GUESS_BASELINE,
            "majority_baseline": "computed from each shuffled test split",
        },
        "ci": {
            "metric": "test_accuracy_minus_baseline",
            "method": "seed_mean_percentile_bootstrap",
            "iterations": BOOTSTRAP_ITERATIONS,
            "ci_level": CI_LEVEL,
            "bootstrap_seed": BOOTSTRAP_SEED,
        },
        "outputs": {
            "seed_metrics": "seed_metrics.csv",
            "aggregate_metrics": "aggregate_metrics.csv",
        },
    }
    (OUT_DIR / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    metadata = {
        "schema_version": 1,
        "metadata": config,
        "command": COMMAND.split(),
        "git_commit": git_commit_hash(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "outputs": config["outputs"],
    }
    (OUT_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(",".join(aggregate_fieldnames))
    for row in aggregate_rows:
        print(",".join(str(row[field]) for field in aggregate_fieldnames))


if __name__ == "__main__":
    main()
