"""Compute seed-level CIs for distinguisher baseline deltas."""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


SOURCE = Path("results/2026-05-10-distinguish-size-epochs-sensitivity/seed_metrics.csv")
OUT_DIR = Path("results/2026-05-12-distinguish-baseline-delta-ci")
ROUNDS = {4, 8, 16}
SAMPLES = [500, 1000, 2000]
EPOCHS = [4, 8, 16]
BASELINE_DELTA = 0.0
CI_LEVEL = 0.95
BOOTSTRAP_ITERATIONS = 10000
BOOTSTRAP_SEED = 20260512


def percentile(sorted_values: list[float], fraction: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = fraction * (len(sorted_values) - 1)
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def read_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            parsed = {
                "rounds": int(row["rounds"]),
                "seed": int(row["seed"]),
                "samples": int(row["samples"]),
                "epochs": int(row["epochs"]),
                "test_accuracy": float(row["test_accuracy"]),
                "test_accuracy_minus_baseline": float(row["test_accuracy_minus_baseline"]),
                "train_test_gap": float(row["train_test_gap"]),
            }
            if parsed["rounds"] in ROUNDS:
                rows.append(parsed)
    return rows


def bootstrap_ci(values: list[float], seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    boot_means = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        sample = [values[rng.randrange(len(values))] for _ in values]
        boot_means.append(sum(sample) / len(sample))
    boot_means.sort()
    alpha = 1 - CI_LEVEL
    return percentile(boot_means, alpha / 2), percentile(boot_means, 1 - alpha / 2)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    groups: dict[tuple[int, int, int], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(row["rounds"], row["samples"], row["epochs"])].append(row)

    seed_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for (rounds, samples, epochs), group in sorted(groups.items()):
        sorted_group = sorted(group, key=lambda item: item["seed"])
        deltas = [float(row["test_accuracy_minus_baseline"]) for row in sorted_group]
        for row in sorted_group:
            seed_rows.append(
                {
                    "rounds": row["rounds"],
                    "seed": row["seed"],
                    "samples": row["samples"],
                    "epochs": row["epochs"],
                    "test_accuracy": f"{float(row['test_accuracy']):.6f}",
                    "test_accuracy_minus_baseline": f"{float(row['test_accuracy_minus_baseline']):.6f}",
                    "train_test_gap": f"{float(row['train_test_gap']):.6f}",
                }
            )

        row_seed = BOOTSTRAP_SEED + rounds + samples + epochs
        ci_low, ci_high = bootstrap_ci(deltas, row_seed)
        mean_delta = sum(deltas) / len(deltas)
        mean_abs_delta = sum(abs(delta) for delta in deltas) / len(deltas)
        summary_rows.append(
            {
                "rounds": rounds,
                "samples": samples,
                "epochs": epochs,
                "seed_count": len(deltas),
                "baseline_delta": f"{BASELINE_DELTA:.6f}",
                "mean_test_accuracy_minus_baseline": f"{mean_delta:.6f}",
                "min_test_accuracy_minus_baseline": f"{min(deltas):.6f}",
                "max_test_accuracy_minus_baseline": f"{max(deltas):.6f}",
                "mean_abs_test_accuracy_minus_baseline": f"{mean_abs_delta:.6f}",
                "ci_level": f"{CI_LEVEL:.6f}",
                "ci_method": "seed_mean_percentile_bootstrap",
                "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
                "bootstrap_seed": row_seed,
                "ci_low": f"{ci_low:.6f}",
                "ci_high": f"{ci_high:.6f}",
                "ci_contains_zero": ci_low <= BASELINE_DELTA <= ci_high,
            }
        )

    seed_path = OUT_DIR / "seed_baseline_deltas.csv"
    with seed_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "rounds",
            "seed",
            "samples",
            "epochs",
            "test_accuracy",
            "test_accuracy_minus_baseline",
            "train_test_gap",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(seed_rows)

    summary_path = OUT_DIR / "baseline_delta_ci.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "rounds",
            "samples",
            "epochs",
            "seed_count",
            "baseline_delta",
            "mean_test_accuracy_minus_baseline",
            "min_test_accuracy_minus_baseline",
            "max_test_accuracy_minus_baseline",
            "mean_abs_test_accuracy_minus_baseline",
            "ci_level",
            "ci_method",
            "bootstrap_iterations",
            "bootstrap_seed",
            "ci_low",
            "ci_high",
            "ci_contains_zero",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "distinguish-baseline-delta-ci",
        "issue": 50,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-12-distinguish-baseline-delta-ci/compute_ci.py",
        "source": str(SOURCE).replace("\\", "/"),
        "outputs": {
            "seed_baseline_deltas": seed_path.name,
            "baseline_delta_ci": summary_path.name,
            "notes": "notes.md",
        },
        "hash": "mini-sha",
        "rounds": sorted(ROUNDS),
        "samples_per_class": SAMPLES,
        "epochs": EPOCHS,
        "seeds": [1, 2, 3, 4, 5],
        "metric": "test_accuracy_minus_baseline",
        "baseline_delta": BASELINE_DELTA,
        "ci_method": "seed_mean_percentile_bootstrap",
        "ci_level": CI_LEVEL,
        "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "model_config": "logistic regression from Issue #18 result files",
    }
    (OUT_DIR / "config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
