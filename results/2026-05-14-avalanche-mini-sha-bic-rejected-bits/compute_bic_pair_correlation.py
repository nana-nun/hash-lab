"""Compute small BIC-style output bit pair correlations from avalanche vectors."""

from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hash_lab.experiments import avalanche_vectors


OUT_DIR = Path("results/2026-05-14-avalanche-mini-sha-bic-rejected-bits")
ROUNDS_LIST = [12, 13, 14]
INPUT_BITS = [224, 236, 248, 250, 254]
OUTPUT_BITS = [225, 228, 231, 254, 255]
SEEDS = list(range(1, 6))
SAMPLES_PER_SEED = 1000
INPUT_BYTES = 32
OUTPUT_BYTES = 32


def bit_at(avalanche_hex: str, bit_index: int) -> int:
    data = bytes.fromhex(avalanche_hex)
    byte_index, shift = divmod(bit_index, 8)
    return (data[byte_index] >> (7 - shift)) & 1


def pearson_from_counts(samples: int, ones_j: int, ones_k: int, joint_11: int) -> tuple[float, bool]:
    p_j = ones_j / samples
    p_k = ones_k / samples
    joint_rate = joint_11 / samples
    covariance = joint_rate - p_j * p_k
    variance_j = p_j * (1 - p_j)
    variance_k = p_k * (1 - p_k)
    if variance_j == 0 or variance_k == 0:
        return 0.0, False
    return covariance / math.sqrt(variance_j * variance_k), True


def collect_vectors() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rounds in ROUNDS_LIST:
        for input_bit_index in INPUT_BITS:
            for seed in SEEDS:
                for sample in avalanche_vectors(
                    rounds=rounds,
                    samples=SAMPLES_PER_SEED,
                    seed=seed,
                    input_bytes=INPUT_BYTES,
                    output_bytes=OUTPUT_BYTES,
                    fixed_input_bit=input_bit_index,
                ):
                    rows.append(
                        {
                            "experiment": "avalanche_vectors",
                            "rounds": sample.rounds,
                            "seed": sample.seed,
                            "sample_index": sample.sample_index,
                            "input_bit_index": sample.input_bit_index,
                            "input_bit_mode": sample.input_bit_mode,
                            "input_bytes": sample.input_bytes,
                            "output_bits": sample.output_bits,
                            "avalanche_hex": sample.avalanche_hex,
                        }
                    )
    return rows


def compute_pair_correlations(vector_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[int, int], list[dict[str, object]]] = {}
    for row in vector_rows:
        key = (int(row["rounds"]), int(row["input_bit_index"]))
        groups.setdefault(key, []).append(row)

    pair_rows: list[dict[str, object]] = []
    for (rounds, input_bit_index), rows in sorted(groups.items()):
        samples = len(rows)
        bit_values = {
            bit_index: [bit_at(str(row["avalanche_hex"]), bit_index) for row in rows]
            for bit_index in OUTPUT_BITS
        }
        for output_bit_j, output_bit_k in combinations(OUTPUT_BITS, 2):
            values_j = bit_values[output_bit_j]
            values_k = bit_values[output_bit_k]
            ones_j = sum(values_j)
            ones_k = sum(values_k)
            joint_11_count = sum(j & k for j, k in zip(values_j, values_k))
            flip_rate_j = ones_j / samples
            flip_rate_k = ones_k / samples
            joint_rate = joint_11_count / samples
            covariance = joint_rate - flip_rate_j * flip_rate_k
            pearson, pearson_defined = pearson_from_counts(samples, ones_j, ones_k, joint_11_count)
            pair_rows.append(
                {
                    "rounds": rounds,
                    "input_bit_index": input_bit_index,
                    "input_bit_mode": "fixed",
                    "output_bit_j": output_bit_j,
                    "output_bit_k": output_bit_k,
                    "samples": samples,
                    "joint_11_count": joint_11_count,
                    "flip_rate_j": f"{flip_rate_j:.6f}",
                    "flip_rate_k": f"{flip_rate_k:.6f}",
                    "joint_rate_11": f"{joint_rate:.6f}",
                    "expected_joint_rate_independent": f"{flip_rate_j * flip_rate_k:.6f}",
                    "covariance": f"{covariance:.8f}",
                    "pearson_correlation": f"{pearson:.8f}" if pearson_defined else "",
                    "pearson_defined": pearson_defined,
                    "abs_correlation": f"{abs(pearson):.8f}" if pearson_defined else "",
                }
            )
    return pair_rows


def summarize(pair_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    summary_rows: list[dict[str, object]] = []
    for rounds in ROUNDS_LIST:
        round_rows = [row for row in pair_rows if int(row["rounds"]) == rounds]
        defined_rows = [row for row in round_rows if row["pearson_defined"]]
        max_row = max(defined_rows, key=lambda row: float(row["abs_correlation"]))
        summary_rows.append(
            {
                "rounds": rounds,
                "input_bits": " ".join(str(bit) for bit in INPUT_BITS),
                "output_bits": " ".join(str(bit) for bit in OUTPUT_BITS),
                "input_bit_count": len(INPUT_BITS),
                "output_bit_count": len(OUTPUT_BITS),
                "output_bit_pairs": len(list(combinations(OUTPUT_BITS, 2))),
                "seed_count": len(SEEDS),
                "samples_per_seed": SAMPLES_PER_SEED,
                "samples_per_input_bit": len(SEEDS) * SAMPLES_PER_SEED,
                "pair_rows": len(round_rows),
                "defined_pair_rows": len(defined_rows),
                "max_abs_correlation": max_row["abs_correlation"],
                "max_abs_correlation_input_bit_index": max_row["input_bit_index"],
                "max_abs_correlation_output_bit_j": max_row["output_bit_j"],
                "max_abs_correlation_output_bit_k": max_row["output_bit_k"],
                "max_abs_correlation_value": max_row["pearson_correlation"],
            }
        )
    return summary_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    vector_rows = collect_vectors()
    pair_rows = compute_pair_correlations(vector_rows)
    summary_rows = summarize(pair_rows)

    write_csv(OUT_DIR / "avalanche_vectors.csv", vector_rows)
    write_csv(OUT_DIR / "pair_correlation.csv", pair_rows)
    write_csv(OUT_DIR / "summary.csv", summary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "avalanche-mini-sha-bic-rejected-bits",
        "issue": 83,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-14-avalanche-mini-sha-bic-rejected-bits/compute_bic_pair_correlation.py",
        "hash": "mini-sha",
        "rounds": ROUNDS_LIST,
        "input_bit_mode": "fixed",
        "input_bits": INPUT_BITS,
        "output_bits": OUTPUT_BITS,
        "output_bit_pairs": [list(pair) for pair in combinations(OUTPUT_BITS, 2)],
        "seeds": SEEDS,
        "samples_per_seed": SAMPLES_PER_SEED,
        "samples_per_input_bit": len(SEEDS) * SAMPLES_PER_SEED,
        "input_bytes": INPUT_BYTES,
        "output_bytes": OUTPUT_BYTES,
        "baseline": "independent output bit flips have covariance and Pearson correlation near 0",
        "outputs": {
            "avalanche_vectors": "avalanche_vectors.csv",
            "pair_correlation": "pair_correlation.csv",
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
