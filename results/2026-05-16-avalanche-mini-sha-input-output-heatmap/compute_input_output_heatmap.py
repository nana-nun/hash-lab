"""Measure mini-sha input-bit x output-bit avalanche heatmaps."""

from __future__ import annotations

import csv
import json
import random
import struct
import sys
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hash_lab.experiments import flip_one_bit
from src.hash_lab.mini_sha import digest


OUT_DIR = Path("results/2026-05-16-avalanche-mini-sha-input-output-heatmap")
ROUNDS_LIST = [12, 13, 14, 16]
INPUT_BYTES = 32
OUTPUT_BYTES = 32
SEEDS = [1, 2, 3, 4, 5]
SAMPLES_PER_SEED_PER_INPUT_BIT = 64
BASELINE = 0.5
BASE_RNG_SEED = 20260516


def avalanche_bits(data: bytes, changed: bytes, rounds: int) -> list[int]:
    left = digest(data, rounds=rounds, output_bytes=OUTPUT_BYTES)
    right = digest(changed, rounds=rounds, output_bytes=OUTPUT_BYTES)
    bits: list[int] = []
    for value in (a ^ b for a, b in zip(left, right)):
        bits.extend((value >> shift) & 1 for shift in range(7, -1, -1))
    return bits


def color_delta(delta: float, scale: float) -> tuple[int, int, int]:
    if scale <= 0:
        return (255, 255, 255)
    intensity = min(1.0, abs(delta) / scale)
    channel = int(round(255 * (1 - intensity)))
    if delta < 0:
        return (channel, channel, 255)
    if delta > 0:
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
    input_bits = INPUT_BYTES * 8
    output_bits = OUTPUT_BYTES * 8
    total_samples = len(SEEDS) * SAMPLES_PER_SEED_PER_INPUT_BIT
    matrix_rows: list[dict[str, object]] = []
    delta_rows: list[dict[str, object]] = []

    for input_bit_index in range(input_bits):
        flip_counts = [0] * output_bits
        for seed in SEEDS:
            rng_seed = BASE_RNG_SEED + rounds * 1_000_000 + seed * 1000 + input_bit_index
            rng = random.Random(rng_seed)
            for _ in range(SAMPLES_PER_SEED_PER_INPUT_BIT):
                data = rng.randbytes(INPUT_BYTES)
                changed = flip_one_bit(data, input_bit_index)
                for output_bit_index, bit in enumerate(avalanche_bits(data, changed, rounds)):
                    flip_counts[output_bit_index] += bit

        for output_bit_index, flip_count in enumerate(flip_counts):
            flip_rate = flip_count / total_samples
            delta = flip_rate - BASELINE
            matrix_rows.append(
                {
                    "rounds": rounds,
                    "input_bit_index": input_bit_index,
                    "output_bit_index": output_bit_index,
                    "seed_count": len(SEEDS),
                    "samples_per_seed": SAMPLES_PER_SEED_PER_INPUT_BIT,
                    "total_samples": total_samples,
                    "flip_count": flip_count,
                    "flip_rate": f"{flip_rate:.6f}",
                }
            )
            delta_rows.append(
                {
                    "rounds": rounds,
                    "input_bit_index": input_bit_index,
                    "output_bit_index": output_bit_index,
                    "baseline": f"{BASELINE:.6f}",
                    "baseline_delta": f"{delta:.6f}",
                    "abs_delta": f"{abs(delta):.6f}",
                }
            )

    deltas = [float(row["baseline_delta"]) for row in delta_rows]
    max_abs_delta = max(abs(delta) for delta in deltas)
    pixels = [color_delta(delta, max_abs_delta) for delta in deltas]
    write_png(OUT_DIR / f"round_{rounds}_baseline_delta_heatmap.png", output_bits, input_bits, pixels)

    max_abs_row = max(delta_rows, key=lambda row: float(row["abs_delta"]))
    summary = {
        "rounds": rounds,
        "input_bits": input_bits,
        "output_bits": output_bits,
        "matrix_cells": input_bits * output_bits,
        "seed_count": len(SEEDS),
        "samples_per_seed_per_input_bit": SAMPLES_PER_SEED_PER_INPUT_BIT,
        "total_samples_per_cell": total_samples,
        "baseline": f"{BASELINE:.6f}",
        "mean_flip_rate": f"{sum(float(row['flip_rate']) for row in matrix_rows) / len(matrix_rows):.6f}",
        "min_flip_rate": min(row["flip_rate"] for row in matrix_rows),
        "max_flip_rate": max(row["flip_rate"] for row in matrix_rows),
        "max_abs_delta_from_0_5": f"{max_abs_delta:.6f}",
        "max_abs_delta_input_bit_index": max_abs_row["input_bit_index"],
        "max_abs_delta_output_bit_index": max_abs_row["output_bit_index"],
        "heatmap_png": f"round_{rounds}_baseline_delta_heatmap.png",
    }
    return matrix_rows, delta_rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix_rows: list[dict[str, object]] = []
    delta_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for rounds in ROUNDS_LIST:
        round_matrix_rows, round_delta_rows, summary = measure_round(rounds)
        matrix_rows.extend(round_matrix_rows)
        delta_rows.extend(round_delta_rows)
        summary_rows.append(summary)

    write_csv(OUT_DIR / "flip_rate_matrix.csv", matrix_rows)
    write_csv(OUT_DIR / "baseline_delta_matrix.csv", delta_rows)
    write_csv(OUT_DIR / "summary.csv", summary_rows)

    jst = timezone(timedelta(hours=9))
    config = {
        "experiment": "avalanche-mini-sha-input-output-heatmap",
        "issue": 85,
        "executed_at": datetime.now(jst).replace(microsecond=0).isoformat(),
        "command": ".\\.venv\\Scripts\\python.exe results/2026-05-16-avalanche-mini-sha-input-output-heatmap/compute_input_output_heatmap.py",
        "hash": "mini-sha",
        "rounds": ROUNDS_LIST,
        "input_bytes": INPUT_BYTES,
        "output_bytes": OUTPUT_BYTES,
        "seeds": SEEDS,
        "samples_per_seed_per_input_bit": SAMPLES_PER_SEED_PER_INPUT_BIT,
        "total_samples_per_cell": len(SEEDS) * SAMPLES_PER_SEED_PER_INPUT_BIT,
        "baseline": BASELINE,
        "base_rng_seed": BASE_RNG_SEED,
        "heatmap": {
            "format": "png",
            "width": OUTPUT_BYTES * 8,
            "height": INPUT_BYTES * 8,
            "x_axis": "output_bit_index",
            "y_axis": "input_bit_index",
            "color_scale": "blue negative delta, white zero, red positive delta; scaled per round by max absolute delta",
        },
        "outputs": {
            "flip_rate_matrix": "flip_rate_matrix.csv",
            "baseline_delta_matrix": "baseline_delta_matrix.csv",
            "summary": "summary.csv",
            "heatmap_png_pattern": "round_<rounds>_baseline_delta_heatmap.png",
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
