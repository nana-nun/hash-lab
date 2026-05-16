"""Join Issue #53 distinguisher metrics with existing avalanche metrics."""

from __future__ import annotations

import csv
from pathlib import Path

from hash_lab.experiments import write_rows_csv


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
ROUNDS = [9, 10, 11, 12, 13, 14, 15, 32]


def read_by_round(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {int(row["rounds"]): row for row in csv.DictReader(handle)}


def main() -> None:
    avalanche_9_15 = read_by_round(ROOT / "results/2026-05-10-avalanche-mini-sha-rounds-9-15/aggregate_metrics.csv")
    avalanche_2_32 = read_by_round(ROOT / "results/2026-05-09-avalanche-mini-sha-multi-seed/aggregate_metrics.csv")
    sac_9_15 = read_by_round(ROOT / "results/2026-05-10-avalanche-mini-sha-bit-ci-9-15/round_summary.csv")
    sac_2_32 = read_by_round(ROOT / "results/2026-05-10-avalanche-mini-sha-bit-ci/round_summary.csv")
    distinguisher = read_by_round(OUT_DIR / "aggregate_metrics.csv")

    rows: list[dict[str, object]] = []
    for rounds in ROUNDS:
        avalanche = avalanche_9_15[rounds] if rounds in avalanche_9_15 else avalanche_2_32[rounds]
        sac = sac_9_15[rounds] if rounds in sac_9_15 else sac_2_32[rounds]
        dist = distinguisher[rounds]
        rows.append(
            {
                "rounds": rounds,
                "avalanche_mean": avalanche["mean_of_means"],
                "avalanche_baseline_delta": avalanche.get(
                    "baseline_delta",
                    f"{float(avalanche['mean_of_means']) - 0.5:.6f}",
                ),
                "sac_max_abs_delta_from_baseline": sac["max_abs_delta_from_baseline"],
                "sac_holm_reject_count": sac["holm_reject_count"],
                "distinguisher_mean_test_accuracy": dist["mean_test_accuracy"],
                "distinguisher_test_accuracy_minus_baseline": dist["mean_test_accuracy_minus_baseline"],
                "distinguisher_delta_ci_low": dist["baseline_delta_ci_low"],
                "distinguisher_delta_ci_high": dist["baseline_delta_ci_high"],
                "distinguisher_delta_ci_contains_zero": dist["ci_contains_zero"],
            }
        )

    fieldnames = [
        "rounds",
        "avalanche_mean",
        "avalanche_baseline_delta",
        "sac_max_abs_delta_from_baseline",
        "sac_holm_reject_count",
        "distinguisher_mean_test_accuracy",
        "distinguisher_test_accuracy_minus_baseline",
        "distinguisher_delta_ci_low",
        "distinguisher_delta_ci_high",
        "distinguisher_delta_ci_contains_zero",
    ]
    write_rows_csv(OUT_DIR / "round_comparison.csv", fieldnames, rows)
    print(",".join(fieldnames))
    for row in rows:
        print(",".join(str(row[field]) for field in fieldnames))


if __name__ == "__main__":
    main()
