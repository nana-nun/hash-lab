"""Compute BIC-style correlations for all mini-sha output bit pairs."""

from __future__ import annotations

import csv
import json
import math
import random
import struct
import sys
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hash_lab.experiments import flip_one_bit, holm_adjusted_p_values
from src.hash_lab.mini_sha import digest


OUT_DIR = Path("results/2026-05-16-avalanche-mini-sha-bic-all-output-pairs")
ROUNDS_LIST = [12, 13, 14, 16]
INPUT_BYTES = 32
OUTPUT_BYTES = 32
SEEDS = [1, 2, 3, 4, 5]
SAMPLES_PER_SEED = 1000
BASE_RNG_SEED = 20260516
ALPHA = 0.05


def avalanche_bytes(data: bytes, changed: bytes, rounds: int) -> bytes:
    left = digest(data, rounds=rounds, output_bytes=OUTPUT_BYTES)
    right = digest(changed, rounds=rounds, output_bytes=OUTPUT_BYTES)
    return bytes(a ^ b for a, b in zip(left, right))


def collect_bitsets(rounds: int) -> tuple[list[int], int]:
    input_bits = INPUT_BYTES * 8
    output_bits = OUTPUT_BYTES * 8
    bitsets = [0] * output_bits
    sample_index = 0

    for seed in SEEDS:
        rng_seed = BASE_RNG_SEED + rounds * 1_000_000 + seed
        rng = random.Random(rng_seed)
        for _ in range(SAMPLES_PER_SEED):
            data = rng.randbytes(INPUT_BYTES)
            input_bit_index = rng.randrange(input_bits)
            changed = flip_one_bit(data, input_bit_index)
            vector = avalanche_bytes(data, changed, rounds)
            sample_mask = 1 << sample_index
            for byte_index, value in enumerate(vector):
                for shift in range(7, -1, -1):
                    if (value >> shift) & 1:
                        bitsets[byte_index * 8 + (7 - shift)] |= sample_mask
            sample_index += 1

    return bitsets, sample_index


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


def correlation_p_value(samples: int, correlation: float) -> float:
    # For a 2x2 table, n * phi^2 is the Pearson chi-square statistic with df=1.
    chi_square = samples * correlation * correlation
    return math.erfc(math.sqrt(chi_square / 2))


def color_correlation(correlation: float, scale: float) -> tuple[int, int, int]:
    if scale <= 0:
        return (255, 255, 255)
    intensity = min(1.0, abs(correlation) / scale)
    channel = int(round(255 * (1 - intensity)))
    if correlation < 0:
        return (channel, channel, 255)
    if correlation > 0:
        return (255, channel, channel)
    return (255, 255, 255)


def write_png(path: Path, width: int, height: int, pixels: list[tuple[int, int, int]]) -> None:
    if len(pixels) != width * height:
        raise ValueError("pixel count does not match image dimensions")

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw_rows = []
    for y in range(height):
        row = bytearray([0])
        for red, green, blue in pixels[y * width : (y + 1) * width]:
            row.extend((red, green, blue))
        raw_rows.append(bytes(row))

    png = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", zlib.compress(b"".join(raw_rows), level=9)),
            chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(png)


def measure_round(rounds: int) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    output_bits = OUTPUT_BYTES * 8
    bitsets, samples = collect_bitsets(rounds)
    ones_counts = [bits.bit_count() for bits in bitsets]
    pair_rows: list[dict[str, object]] = []
    correlations = [[0.0 for _ in range(output_bits)] for _ in range(output_bits)]

    for output_bit_j in range(output_bits):
        ones_j = ones_counts[output_bit_j]
        for output_bit_k in range(output_bit_j + 1, output_bits):
            ones_k = ones_counts[output_bit_k]
            joint_11_count = (bitsets[output_bit_j] & bitsets[output_bit_k]).bit_count()
            flip_rate_j = ones_j / samples
            flip_rate_k = ones_k / samples
            joint_rate = joint_11_count / samples
            covariance = joint_rate - flip_rate_j * flip_rate_k
            pearson, pearson_defined = pearson_from_counts(samples, ones_j, ones_k, joint_11_count)
            raw_p_value = correlation_p_value(samples, pearson) if pearson_defined else 1.0
            correlations[output_bit_j][output_bit_k] = pearson
            correlations[output_bit_k][output_bit_j] = pearson
            pair_rows.append(
                {
                    "rounds": rounds,
                    "input_bit_mode": "random",
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
                    "p_value_method": "pearson_chi_square_df1_from_phi",
                    "raw_p_value": raw_p_value,
                }
            )

    adjusted = holm_adjusted_p_values([float(row["raw_p_value"]) for row in pair_rows])
    for row, adjusted_p in zip(pair_rows, adjusted):
        row["raw_p_value"] = f"{float(row['raw_p_value']):.8g}"
        row["holm_adjusted_p_value"] = f"{adjusted_p:.8g}"
        row["holm_reject_independence"] = adjusted_p < ALPHA

    defined_rows = [row for row in pair_rows if row["pearson_defined"]]
    rejected_rows = [row for row in defined_rows if row["holm_reject_independence"]]
    max_row = max(defined_rows, key=lambda row: float(row["abs_correlation"]))
    top_rows = sorted(defined_rows, key=lambda row: float(row["abs_correlation"]), reverse=True)[:20]

    max_abs = float(max_row["abs_correlation"])
    pixels: list[tuple[int, int, int]] = []
    for y in range(output_bits):
        for x in range(output_bits):
            pixels.append(color_correlation(correlations[y][x], max_abs))
    write_png(OUT_DIR / f"round_{rounds}_pair_correlation_heatmap.png", output_bits, output_bits, pixels)

    summary = {
        "rounds": rounds,
        "input_bit_mode": "random",
        "output_bits": output_bits,
        "output_bit_pairs": len(pair_rows),
        "seed_count": len(SEEDS),
        "samples_per_seed": SAMPLES_PER_SEED,
        "samples": samples,
        "defined_pair_rows": len(defined_rows),
        "holm_reject_count": len(rejected_rows),
        "alpha": f"{ALPHA:.6f}",
        "max_abs_correlation": max_row["abs_correlation"],
        "max_abs_correlation_output_bit_j": max_row["output_bit_j"],
        "max_abs_correlation_output_bit_k": max_row["output_bit_k"],
        "max_abs_correlation_value": max_row["pearson_correlation"],
        "heatmap_png": f"round_{rounds}_pair_correlation_heatmap.png",
    }
    return pair_rows, top_rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pair_rows: list[dict[str, object]] = []
    top_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for rounds in ROUNDS_LIST:
        round_pair_rows, round_top_rows, summary = measure_round(rounds)
        pair_rows.extend(round_pair_rows)
        top_rows.extend(round_top_rows)
        summary_rows.append(summary)

    write_csv(OUT_DIR / "pair_correlation.csv", pair_rows)
    write_csv(OUT_DIR / "top_pairs.csv", top_rows)
    write_csv(OUT_DIR / "summary.csv", summary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "avalanche-mini-sha-bic-all-output-pairs",
        "issue": 86,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-16-avalanche-mini-sha-bic-all-output-pairs/compute_bic_all_output_pairs.py",
        "hash": "mini-sha",
        "rounds": ROUNDS_LIST,
        "input_bit_mode": "random",
        "input_bytes": INPUT_BYTES,
        "output_bytes": OUTPUT_BYTES,
        "output_bit_pairs_per_round": (OUTPUT_BYTES * 8) * (OUTPUT_BYTES * 8 - 1) // 2,
        "seeds": SEEDS,
        "samples_per_seed": SAMPLES_PER_SEED,
        "samples_per_round": len(SEEDS) * SAMPLES_PER_SEED,
        "baseline": "independent output bit flips have covariance and Pearson correlation near 0",
        "p_value_method": "Pearson chi-square df=1 approximation from phi correlation",
        "multiple_comparison": "Holm over all output bit pairs per round",
        "alpha": ALPHA,
        "base_rng_seed": BASE_RNG_SEED,
        "heatmap": {
            "format": "png",
            "width": OUTPUT_BYTES * 8,
            "height": OUTPUT_BYTES * 8,
            "x_axis": "output_bit_k",
            "y_axis": "output_bit_j",
            "color_scale": "blue negative correlation, white zero, red positive correlation; scaled per round by max absolute correlation",
        },
        "outputs": {
            "pair_correlation": "pair_correlation.csv",
            "top_pairs": "top_pairs.csv",
            "summary": "summary.csv",
            "heatmap_png_pattern": "round_<rounds>_pair_correlation_heatmap.png",
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
