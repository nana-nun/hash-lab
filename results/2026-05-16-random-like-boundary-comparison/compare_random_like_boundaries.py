"""Compare round boundaries across existing mini-sha random-like metrics."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


OUT_DIR = Path("results/2026-05-16-random-like-boundary-comparison")
ROUND_COMPARISON = Path("results/2026-05-10-avalanche-distinguisher-round-comparison/round_comparison.csv")
INPUT_OUTPUT_HEATMAP = Path("results/2026-05-16-avalanche-mini-sha-input-output-heatmap/summary.csv")
BIC_ALL_PAIRS = Path("results/2026-05-16-avalanche-mini-sha-bic-all-output-pairs/summary.csv")
BIC_FIXED_SMALL = Path("results/2026-05-14-avalanche-mini-sha-bic-rejected-bits/summary.csv")


def read_by_round(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {int(row["rounds"]): row for row in csv.DictReader(handle)}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def yes_no(value: bool | None) -> str:
    if value is None:
        return "not_measured"
    return "yes" if value else "no"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    round_comparison = read_by_round(ROUND_COMPARISON)
    heatmap = read_by_round(INPUT_OUTPUT_HEATMAP)
    bic_all = read_by_round(BIC_ALL_PAIRS)
    bic_fixed = read_by_round(BIC_FIXED_SMALL)
    rounds = sorted(set(round_comparison) | set(heatmap) | set(bic_all) | set(bic_fixed))

    rows: list[dict[str, object]] = []
    for rounds_value in rounds:
        aggregate = round_comparison.get(rounds_value, {})
        heat = heatmap.get(rounds_value, {})
        bic = bic_all.get(rounds_value, {})
        fixed_bic = bic_fixed.get(rounds_value, {})

        avalanche_delta = float(aggregate["avalanche_baseline_delta"]) if aggregate else None
        bit_rejects = int(aggregate["bit_holm_reject_count"]) if aggregate else None
        distinguisher_available = aggregate.get("distinguisher_available") == "True"
        distinguisher_delta = (
            float(aggregate["distinguisher_test_accuracy_minus_baseline"])
            if distinguisher_available
            else None
        )
        heatmap_mean_abs_224_254 = {
            12: 0.098593,
            13: 0.033291,
            14: 0.022493,
            16: 0.021961,
        }.get(rounds_value)
        heatmap_mean_abs_all = {
            12: 0.033357,
            13: 0.023679,
            14: 0.022190,
            16: 0.022252,
        }.get(rounds_value)

        rows.append(
            {
                "rounds": rounds_value,
                "aggregate_avalanche_mean": aggregate.get("avalanche_mean", ""),
                "aggregate_abs_delta_from_0_5": f"{abs(avalanche_delta):.6f}" if avalanche_delta is not None else "",
                "aggregate_random_like_threshold_0_001": yes_no(
                    abs(avalanche_delta) <= 0.001 if avalanche_delta is not None else None
                ),
                "output_bit_sac_holm_reject_count": bit_rejects if bit_rejects is not None else "",
                "output_bit_sac_random_like_no_holm_rejects": yes_no(
                    bit_rejects == 0 if bit_rejects is not None else None
                ),
                "input_output_heatmap_mean_abs_delta_all": f"{heatmap_mean_abs_all:.6f}"
                if heatmap_mean_abs_all is not None
                else "",
                "input_output_heatmap_mean_abs_delta_input_224_254": f"{heatmap_mean_abs_224_254:.6f}"
                if heatmap_mean_abs_224_254 is not None
                else "",
                "input_output_heatmap_max_abs_delta": heat.get("max_abs_delta_from_0_5", ""),
                "bic_all_pairs_holm_reject_count": bic.get("holm_reject_count", ""),
                "bic_all_pairs_random_like_no_holm_rejects": yes_no(
                    int(bic["holm_reject_count"]) == 0 if bic else None
                ),
                "bic_all_pairs_max_abs_correlation": bic.get("max_abs_correlation", ""),
                "bic_fixed_small_max_abs_correlation": fixed_bic.get("max_abs_correlation", ""),
                "distinguisher_available": distinguisher_available,
                "distinguisher_test_accuracy_minus_baseline": f"{distinguisher_delta:.6f}"
                if distinguisher_delta is not None
                else "",
                "distinguisher_near_baseline_abs_delta_le_0_02": yes_no(
                    abs(distinguisher_delta) <= 0.02 if distinguisher_delta is not None else None
                ),
            }
        )

    boundary_rows = [
        {
            "metric": "aggregate mean flip ratio",
            "random_like_rule": "abs(mean - 0.5) <= 0.001",
            "first_random_like_round_in_available_data": 13,
            "evidence": "9-12 rounds remain below threshold; 13-15 rounds are within 0.001 in 9-15 data; 16/32 are also near 0.5.",
            "limitation": "Threshold is an interpretation aid, not a formal statistical test.",
        },
        {
            "metric": "output-bit SAC style Holm rejects",
            "random_like_rule": "round has zero output bits rejecting baseline 0.5 after Holm correction",
            "first_random_like_round_in_available_data": 14,
            "evidence": "Holm reject count decreases 35 at 12 rounds, 1 at 13 rounds, then 0 at 14/15/16/32 rounds.",
            "limitation": "Uses output-bit aggregate over random input bit flips; input-localized effects can be hidden.",
        },
        {
            "metric": "input-output localized heatmap",
            "random_like_rule": "input bits 224..254 mean abs delta falls near all-cell mean abs delta",
            "first_random_like_round_in_available_data": 14,
            "evidence": "224..254 mean abs delta: 12=0.098593, 13=0.033291, 14=0.022493, 16=0.021961.",
            "limitation": "Exploratory heatmap with 320 samples per cell and no per-cell multiple testing.",
        },
        {
            "metric": "BIC all output pairs, random input bit mode",
            "random_like_rule": "zero output bit pairs reject independence after Holm correction",
            "first_random_like_round_in_available_data": 13,
            "evidence": "12 rounds has 22 rejected pairs; 13/14/16 rounds have 0 rejected pairs.",
            "limitation": "Random input bit mode can average out fixed-input local dependence.",
        },
        {
            "metric": "BIC selected rejected bits, fixed input bits",
            "random_like_rule": "max abs pair correlation becomes small in selected-bit small run",
            "first_random_like_round_in_available_data": 14,
            "evidence": "Max abs correlation falls from 12=0.729431 and 13=0.566370 to 14=0.067618.",
            "limitation": "Small selected-bit run without confidence intervals or multiple testing.",
        },
        {
            "metric": "logistic regression distinguisher",
            "random_like_rule": "abs(test accuracy - 0.5) <= 0.02",
            "first_random_like_round_in_available_data": 4,
            "evidence": "2 rounds is strongly distinguishable; 4/8/16 rounds are near baseline in existing logistic run.",
            "limitation": "9-15 and 32 rounds are not measured for this distinguisher yet; see issue #53.",
        },
    ]

    write_csv(OUT_DIR / "round_metric_comparison.csv", rows)
    write_csv(OUT_DIR / "boundary_summary.csv", boundary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "random-like-boundary-comparison",
        "issue": 95,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-16-random-like-boundary-comparison/compare_random_like_boundaries.py",
        "inputs": {
            "round_comparison": str(ROUND_COMPARISON),
            "input_output_heatmap": str(INPUT_OUTPUT_HEATMAP),
            "bic_all_pairs": str(BIC_ALL_PAIRS),
            "bic_fixed_small": str(BIC_FIXED_SMALL),
        },
        "outputs": {
            "round_metric_comparison": "round_metric_comparison.csv",
            "boundary_summary": "boundary_summary.csv",
            "notes": "notes.md",
        },
        "model_config": None,
    }
    (OUT_DIR / "config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
