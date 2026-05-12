"""Compare input-bit localization for rejected mini-sha output bits."""

from __future__ import annotations

import csv
import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hash_lab.experiments import (
    baseline_normal_p_value,
    flip_one_bit,
    holm_adjusted_p_values,
    wilson_score_ci,
)
from src.hash_lab.mini_sha import digest


OUT_DIR = Path("results/2026-05-12-avalanche-mini-sha-13-rejected-bits-input-localization")
ROUNDS = 13
INPUT_BYTES = 32
OUTPUT_BYTES = 32
OUTPUT_BIT_INDICES = [225, 228, 231, 254, 255]
SEEDS = list(range(1, 21))
SAMPLES_PER_SEED_PER_INPUT_BIT = 500
BASELINE = 0.5
ALPHA = 0.05
BASE_RNG_SEED = 20260512


def selected_output_bits(data: bytes) -> dict[int, int]:
    out = digest(data, rounds=ROUNDS, output_bytes=OUTPUT_BYTES)
    bits = {}
    for output_bit_index in OUTPUT_BIT_INDICES:
        byte_index, shift = divmod(output_bit_index, 8)
        bits[output_bit_index] = (out[byte_index] >> (7 - shift)) & 1
    return bits


def measure() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    seed_rows: list[dict[str, object]] = []
    input_rows_by_output: dict[int, list[dict[str, object]]] = {
        output_bit_index: [] for output_bit_index in OUTPUT_BIT_INDICES
    }
    input_bits = INPUT_BYTES * 8

    for input_bit_index in range(input_bits):
        total_flips_by_output = {output_bit_index: 0 for output_bit_index in OUTPUT_BIT_INDICES}
        seed_rates_by_output: dict[int, list[float]] = {
            output_bit_index: [] for output_bit_index in OUTPUT_BIT_INDICES
        }

        for seed in SEEDS:
            rng_seed = BASE_RNG_SEED + seed * 1000 + input_bit_index
            rng = random.Random(rng_seed)
            seed_flips_by_output = {output_bit_index: 0 for output_bit_index in OUTPUT_BIT_INDICES}
            for _ in range(SAMPLES_PER_SEED_PER_INPUT_BIT):
                data = rng.randbytes(INPUT_BYTES)
                changed = flip_one_bit(data, input_bit_index)
                left = selected_output_bits(data)
                right = selected_output_bits(changed)
                for output_bit_index in OUTPUT_BIT_INDICES:
                    seed_flips_by_output[output_bit_index] += (
                        left[output_bit_index] ^ right[output_bit_index]
                    )

            for output_bit_index, flip_count in seed_flips_by_output.items():
                flip_rate = flip_count / SAMPLES_PER_SEED_PER_INPUT_BIT
                seed_rates_by_output[output_bit_index].append(flip_rate)
                total_flips_by_output[output_bit_index] += flip_count
                seed_rows.append(
                    {
                        "rounds": ROUNDS,
                        "output_bit_index": output_bit_index,
                        "input_bit_index": input_bit_index,
                        "seed": seed,
                        "rng_seed": rng_seed,
                        "samples": SAMPLES_PER_SEED_PER_INPUT_BIT,
                        "flip_count": flip_count,
                        "flip_rate": f"{flip_rate:.6f}",
                        "baseline_delta": f"{flip_rate - BASELINE:.6f}",
                    }
                )

        total_samples = len(SEEDS) * SAMPLES_PER_SEED_PER_INPUT_BIT
        for output_bit_index in OUTPUT_BIT_INDICES:
            total_flips = total_flips_by_output[output_bit_index]
            seed_rates = seed_rates_by_output[output_bit_index]
            ci_low, ci_high = wilson_score_ci(total_flips, total_samples)
            flip_rate = total_flips / total_samples
            input_rows_by_output[output_bit_index].append(
                {
                    "rounds": ROUNDS,
                    "output_bit_index": output_bit_index,
                    "input_bit_index": input_bit_index,
                    "seed_count": len(SEEDS),
                    "samples_per_seed": SAMPLES_PER_SEED_PER_INPUT_BIT,
                    "total_samples": total_samples,
                    "flip_count": total_flips,
                    "baseline": f"{BASELINE:.6f}",
                    "flip_rate": f"{flip_rate:.6f}",
                    "ci_level": "0.950000",
                    "ci_method": "wilson_score",
                    "ci_low": f"{ci_low:.6f}",
                    "ci_high": f"{ci_high:.6f}",
                    "baseline_delta": f"{flip_rate - BASELINE:.6f}",
                    "ci_contains_baseline": ci_low <= BASELINE <= ci_high,
                    "p_value_method": "normal_approximation_two_sided",
                    "raw_p_value": baseline_normal_p_value(total_flips, total_samples, BASELINE),
                    "seed_min_flip_rate": f"{min(seed_rates):.6f}",
                    "seed_max_flip_rate": f"{max(seed_rates):.6f}",
                }
            )

    input_rows: list[dict[str, object]] = []
    for output_bit_index in OUTPUT_BIT_INDICES:
        output_rows = input_rows_by_output[output_bit_index]
        adjusted = holm_adjusted_p_values([float(row["raw_p_value"]) for row in output_rows])
        for row, adjusted_p in zip(output_rows, adjusted):
            row["raw_p_value"] = f"{float(row['raw_p_value']):.8g}"
            row["holm_adjusted_p_value"] = f"{adjusted_p:.8g}"
            row["holm_reject_baseline"] = adjusted_p < ALPHA
        input_rows.extend(output_rows)

    summary_rows: list[dict[str, object]] = []
    for output_bit_index in OUTPUT_BIT_INDICES:
        rows = [row for row in input_rows if row["output_bit_index"] == output_bit_index]
        reject_rows = [row for row in rows if row["holm_reject_baseline"]]
        summary_rows.append(
            {
                "rounds": ROUNDS,
                "output_bit_index": output_bit_index,
                "input_bits": input_bits,
                "seed_count": len(SEEDS),
                "samples_per_seed_per_input_bit": SAMPLES_PER_SEED_PER_INPUT_BIT,
                "total_samples_per_input_bit": len(SEEDS) * SAMPLES_PER_SEED_PER_INPUT_BIT,
                "baseline": f"{BASELINE:.6f}",
                "mean_flip_rate": f"{sum(float(row['flip_rate']) for row in rows) / input_bits:.6f}",
                "min_flip_rate": min(row["flip_rate"] for row in rows),
                "min_input_bit_index": min(rows, key=lambda row: row["flip_rate"])[
                    "input_bit_index"
                ],
                "max_flip_rate": max(row["flip_rate"] for row in rows),
                "max_input_bit_index": max(rows, key=lambda row: row["flip_rate"])[
                    "input_bit_index"
                ],
                "max_abs_delta_from_0_5": f"{max(abs(float(row['baseline_delta'])) for row in rows):.6f}",
                "ci_excludes_baseline_count": sum(
                    row["ci_contains_baseline"] is False for row in rows
                ),
                "holm_reject_count": len(reject_rows),
                "holm_rejected_input_bits": " ".join(
                    str(row["input_bit_index"]) for row in reject_rows
                ),
            }
        )
    return seed_rows, input_rows, summary_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seed_rows, input_rows, summary_rows = measure()
    write_csv(OUT_DIR / "seed_input_bit_metrics.csv", seed_rows)
    write_csv(OUT_DIR / "input_bit_ci_metrics.csv", input_rows)
    write_csv(OUT_DIR / "summary.csv", summary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "avalanche-mini-sha-13-rejected-bits-input-localization",
        "issue": 75,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-12-avalanche-mini-sha-13-rejected-bits-input-localization/compute_rejected_bits_input_localization.py",
        "hash": "mini-sha",
        "rounds": ROUNDS,
        "input_bytes": INPUT_BYTES,
        "output_bytes": OUTPUT_BYTES,
        "output_bit_indices": OUTPUT_BIT_INDICES,
        "seeds": SEEDS,
        "samples_per_seed_per_input_bit": SAMPLES_PER_SEED_PER_INPUT_BIT,
        "total_samples_per_input_bit": len(SEEDS) * SAMPLES_PER_SEED_PER_INPUT_BIT,
        "baseline": BASELINE,
        "ci_method": "wilson_score",
        "ci_level": 0.95,
        "multiple_comparison": "Holm over 256 input bit positions per output bit",
        "alpha": ALPHA,
        "base_rng_seed": BASE_RNG_SEED,
        "outputs": {
            "seed_input_bit_metrics": "seed_input_bit_metrics.csv",
            "input_bit_ci_metrics": "input_bit_ci_metrics.csv",
            "summary": "summary.csv",
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
