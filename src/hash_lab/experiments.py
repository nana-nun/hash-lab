"""Experiment runners for hash-lab."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .mini_sha import digest, digest_bits


@dataclass(frozen=True)
class AvalancheResult:
    rounds: int
    samples: int
    mean: float
    stdev: float
    minimum: float
    maximum: float


@dataclass(frozen=True)
class BootstrapResult:
    rounds: int
    seeds: int
    samples_per_seed: int
    total_samples: int
    baseline: float
    mean: float
    ci_level: float
    ci_low: float
    ci_high: float
    baseline_delta: float
    baseline_delta_ci_low: float
    baseline_delta_ci_high: float
    ci_contains_baseline: bool


@dataclass(frozen=True)
class BitAvalancheResult:
    rounds: int
    seed: int
    samples: int
    output_bits: int
    flip_counts: tuple[int, ...]

    @property
    def flip_rates(self) -> tuple[float, ...]:
        return tuple(count / self.samples for count in self.flip_counts)

    @property
    def mean_flip_rate(self) -> float:
        return sum(self.flip_rates) / self.output_bits

    @property
    def min_flip_rate(self) -> float:
        return min(self.flip_rates)

    @property
    def max_flip_rate(self) -> float:
        return max(self.flip_rates)


@dataclass(frozen=True)
class DistinguishResult:
    rounds: int
    samples: int
    epochs: int
    random_guess_baseline: float
    majority_baseline: float
    train_accuracy: float
    test_accuracy: float
    test_accuracy_minus_baseline: float


def hamming_distance(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        raise ValueError("inputs must have equal length")
    return sum((a ^ b).bit_count() for a, b in zip(left, right))


def flip_one_bit(data: bytes, bit_index: int) -> bytes:
    values = bytearray(data)
    byte_index, shift = divmod(bit_index, 8)
    values[byte_index] ^= 1 << (7 - shift)
    return bytes(values)


def avalanche_ratios(rounds: int, samples: int, input_bytes: int = 32, seed: int = 1) -> list[float]:
    rng = random.Random(seed)
    ratios: list[float] = []

    for _ in range(samples):
        data = rng.randbytes(input_bytes)
        bit_index = rng.randrange(input_bytes * 8)
        changed = flip_one_bit(data, bit_index)
        left = digest(data, rounds=rounds)
        right = digest(changed, rounds=rounds)
        ratios.append(hamming_distance(left, right) / (len(left) * 8))

    return ratios


def summarize_ratios(rounds: int, ratios: list[float]) -> AvalancheResult:
    mean = sum(ratios) / len(ratios)
    variance = sum((item - mean) ** 2 for item in ratios) / len(ratios)
    return AvalancheResult(
        rounds=rounds,
        samples=len(ratios),
        mean=mean,
        stdev=math.sqrt(variance),
        minimum=min(ratios),
        maximum=max(ratios),
    )


def avalanche(rounds: int, samples: int, input_bytes: int = 32, seed: int = 1) -> AvalancheResult:
    return summarize_ratios(
        rounds,
        avalanche_ratios(rounds, samples=samples, input_bytes=input_bytes, seed=seed),
    )


def bit_avalanche(
    rounds: int,
    samples: int,
    input_bytes: int = 32,
    output_bytes: int = 32,
    seed: int = 1,
) -> BitAvalancheResult:
    rng = random.Random(seed)
    output_bits = output_bytes * 8
    flip_counts = [0] * output_bits

    for _ in range(samples):
        data = rng.randbytes(input_bytes)
        bit_index = rng.randrange(input_bytes * 8)
        changed = flip_one_bit(data, bit_index)
        left = digest(data, rounds=rounds, output_bytes=output_bytes)
        right = digest(changed, rounds=rounds, output_bytes=output_bytes)
        for byte_index, value in enumerate(a ^ b for a, b in zip(left, right)):
            for shift in range(7, -1, -1):
                output_bit_index = byte_index * 8 + (7 - shift)
                flip_counts[output_bit_index] += (value >> shift) & 1

    return BitAvalancheResult(
        rounds=rounds,
        seed=seed,
        samples=samples,
        output_bits=output_bits,
        flip_counts=tuple(flip_counts),
    )


def percentile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("values must not be empty")
    if probability < 0 or probability > 1:
        raise ValueError("probability must be between 0 and 1")
    if len(sorted_values) == 1:
        return sorted_values[0]

    index = probability * (len(sorted_values) - 1)
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return sorted_values[lower]
    weight = index - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def bootstrap_mean_ci(
    values: list[float],
    iterations: int = 2000,
    ci_level: float = 0.95,
    seed: int = 1,
) -> tuple[float, float]:
    if not values:
        raise ValueError("values must not be empty")
    if iterations < 1:
        raise ValueError("iterations must be positive")
    if ci_level <= 0 or ci_level >= 1:
        raise ValueError("ci_level must be between 0 and 1")

    rng = random.Random(seed)
    sample_size = len(values)
    means: list[float] = []
    for _ in range(iterations):
        total = 0.0
        for _ in range(sample_size):
            total += values[rng.randrange(sample_size)]
        means.append(total / sample_size)

    means.sort()
    tail = (1 - ci_level) / 2
    return percentile(means, tail), percentile(means, 1 - tail)


def hierarchical_bootstrap_mean_ci(
    values_by_seed: dict[int, list[float]],
    iterations: int = 2000,
    ci_level: float = 0.95,
    seed: int = 1,
) -> tuple[float, float]:
    if not values_by_seed:
        raise ValueError("values_by_seed must not be empty")
    if iterations < 1:
        raise ValueError("iterations must be positive")
    if ci_level <= 0 or ci_level >= 1:
        raise ValueError("ci_level must be between 0 and 1")

    rng = random.Random(seed)
    seed_ids = sorted(values_by_seed)
    means: list[float] = []
    for _ in range(iterations):
        total = 0.0
        count = 0
        for _ in seed_ids:
            seed_values = values_by_seed[rng.choice(seed_ids)]
            sample_size = len(seed_values)
            for _ in range(sample_size):
                total += seed_values[rng.randrange(sample_size)]
            count += sample_size
        means.append(total / count)

    means.sort()
    tail = (1 - ci_level) / 2
    return percentile(means, tail), percentile(means, 1 - tail)


def read_per_sample_ratios(path: Path) -> dict[int, dict[int, list[float]]]:
    values: dict[int, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            values[int(row["rounds"])][int(row["seed"])].append(float(row["flip_ratio"]))
    return {rounds: dict(seeds) for rounds, seeds in values.items()}


def read_metrics_by_round(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {int(row["rounds"]): row for row in csv.DictReader(handle)}


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)


def make_distinguish_dataset(rounds: int, samples: int, seed: int = 1) -> list[tuple[list[int], int]]:
    rng = random.Random(seed)
    rows: list[tuple[list[int], int]] = []

    for _ in range(samples):
        data = rng.randbytes(32)
        rows.append((digest_bits(data, rounds=rounds), 1))
        random_bits = [rng.randrange(2) for _ in range(256)]
        rows.append((random_bits, 0))

    rng.shuffle(rows)
    return rows


def train_logistic(
    rows: list[tuple[list[int], int]],
    epochs: int,
    learning_rate: float = 0.08,
) -> tuple[list[float], float]:
    feature_count = len(rows[0][0])
    weights = [0.0] * feature_count
    bias = 0.0

    for _ in range(epochs):
        for features, label in rows:
            centered = [2 * bit - 1 for bit in features]
            score = bias + sum(weight * value for weight, value in zip(weights, centered))
            prediction = sigmoid(score)
            error = prediction - label
            for i, value in enumerate(centered):
                weights[i] -= learning_rate * error * value
            bias -= learning_rate * error

    return weights, bias


def accuracy(rows: list[tuple[list[int], int]], weights: list[float], bias: float) -> float:
    correct = 0
    for features, label in rows:
        centered = [2 * bit - 1 for bit in features]
        score = bias + sum(weight * value for weight, value in zip(weights, centered))
        predicted = 1 if sigmoid(score) >= 0.5 else 0
        correct += int(predicted == label)
    return correct / len(rows)


def majority_baseline_accuracy(rows: list[tuple[list[int], int]]) -> float:
    positives = sum(label for _, label in rows)
    negatives = len(rows) - positives
    return max(positives, negatives) / len(rows)


def distinguish(rounds: int, samples: int, epochs: int, seed: int = 1) -> DistinguishResult:
    rows = make_distinguish_dataset(rounds, samples=samples, seed=seed)
    split = int(len(rows) * 0.8)
    train_rows = rows[:split]
    test_rows = rows[split:]
    weights, bias = train_logistic(train_rows, epochs=epochs)
    random_guess_baseline = 0.5
    test_accuracy = accuracy(test_rows, weights, bias)
    return DistinguishResult(
        rounds=rounds,
        samples=samples,
        epochs=epochs,
        random_guess_baseline=random_guess_baseline,
        majority_baseline=majority_baseline_accuracy(test_rows),
        train_accuracy=accuracy(train_rows, weights, bias),
        test_accuracy=test_accuracy,
        test_accuracy_minus_baseline=test_accuracy - random_guess_baseline,
    )


def add_common_rounds(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--rounds", nargs="+", type=int, required=True)
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", type=Path, help="Save results to this CSV or JSON path")
    parser.add_argument("--format", choices=("csv", "json"), default="csv", help="Output file format")


def write_rows_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_results_json(path: Path, metadata: dict[str, object], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"metadata": metadata, "results": rows}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def save_results(
    args: argparse.Namespace,
    metadata: dict[str, object],
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    if args.output is None:
        return

    if args.format == "csv":
        write_rows_csv(args.output, fieldnames, rows)
        return

    write_results_json(args.output, metadata, rows)


def run_avalanche(args: argparse.Namespace) -> None:
    print("rounds,samples,mean,stdev,min,max")
    rows: list[dict[str, object]] = []
    for rounds in args.rounds:
        result = avalanche(rounds, samples=args.samples, seed=args.seed)
        rows.append(
            {
                "experiment": "avalanche",
                "seed": args.seed,
                "rounds": result.rounds,
                "samples": result.samples,
                "mean": round(result.mean, 4),
                "stdev": round(result.stdev, 4),
                "min": round(result.minimum, 4),
                "max": round(result.maximum, 4),
            }
        )
        print(
            f"{result.rounds},{result.samples},"
            f"{result.mean:.4f},{result.stdev:.4f},{result.minimum:.4f},{result.maximum:.4f}"
        )
    save_results(
        args,
        {
            "experiment": "avalanche",
            "seed": args.seed,
            "rounds": args.rounds,
            "samples": args.samples,
        },
        ["experiment", "seed", "rounds", "samples", "mean", "stdev", "min", "max"],
        rows,
    )


def run_avalanche_bootstrap(args: argparse.Namespace) -> None:
    sample_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for rounds in args.rounds:
        round_ratios: list[float] = []
        for seed in args.seeds:
            ratios = avalanche_ratios(rounds, samples=args.samples, seed=seed)
            round_ratios.extend(ratios)
            for sample_index, ratio in enumerate(ratios):
                sample_rows.append(
                    {
                        "experiment": "avalanche_bootstrap",
                        "rounds": rounds,
                        "seed": seed,
                        "sample_index": sample_index,
                        "flip_ratio": f"{ratio:.8f}",
                    }
                )

        result = summarize_ratios(rounds, round_ratios)
        ci_low, ci_high = bootstrap_mean_ci(
            round_ratios,
            iterations=args.bootstrap_iterations,
            ci_level=args.ci_level,
            seed=args.bootstrap_seed + rounds,
        )
        bootstrap = BootstrapResult(
            rounds=rounds,
            seeds=len(args.seeds),
            samples_per_seed=args.samples,
            total_samples=len(round_ratios),
            baseline=args.baseline,
            mean=result.mean,
            ci_level=args.ci_level,
            ci_low=ci_low,
            ci_high=ci_high,
            baseline_delta=result.mean - args.baseline,
            baseline_delta_ci_low=ci_low - args.baseline,
            baseline_delta_ci_high=ci_high - args.baseline,
            ci_contains_baseline=ci_low <= args.baseline <= ci_high,
        )
        summary_rows.append(
            {
                "rounds": bootstrap.rounds,
                "seeds": bootstrap.seeds,
                "samples_per_seed": bootstrap.samples_per_seed,
                "total_samples": bootstrap.total_samples,
                "baseline": f"{bootstrap.baseline:.6f}",
                "mean": f"{bootstrap.mean:.6f}",
                "ci_level": f"{bootstrap.ci_level:.6f}",
                "ci_method": "per_sample_percentile_bootstrap",
                "bootstrap_iterations": args.bootstrap_iterations,
                "bootstrap_seed": args.bootstrap_seed + rounds,
                "ci_low": f"{bootstrap.ci_low:.6f}",
                "ci_high": f"{bootstrap.ci_high:.6f}",
                "baseline_delta": f"{bootstrap.baseline_delta:.6f}",
                "baseline_delta_ci_low": f"{bootstrap.baseline_delta_ci_low:.6f}",
                "baseline_delta_ci_high": f"{bootstrap.baseline_delta_ci_high:.6f}",
                "ci_contains_baseline": bootstrap.ci_contains_baseline,
                "min": f"{result.minimum:.6f}",
                "max": f"{result.maximum:.6f}",
            }
        )

    print(
        "rounds,seeds,samples_per_seed,total_samples,baseline,mean,ci_level,ci_method,"
        "bootstrap_iterations,bootstrap_seed,ci_low,ci_high,baseline_delta,"
        "baseline_delta_ci_low,baseline_delta_ci_high,ci_contains_baseline,min,max"
    )
    for row in summary_rows:
        print(",".join(str(row[field]) for field in row))

    write_rows_csv(
        args.samples_output,
        ["experiment", "rounds", "seed", "sample_index", "flip_ratio"],
        sample_rows,
    )
    write_rows_csv(
        args.summary_output,
        [
            "rounds",
            "seeds",
            "samples_per_seed",
            "total_samples",
            "baseline",
            "mean",
            "ci_level",
            "ci_method",
            "bootstrap_iterations",
            "bootstrap_seed",
            "ci_low",
            "ci_high",
            "baseline_delta",
            "baseline_delta_ci_low",
            "baseline_delta_ci_high",
            "ci_contains_baseline",
            "min",
            "max",
        ],
        summary_rows,
    )


def run_avalanche_bits(args: argparse.Namespace) -> None:
    bit_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for rounds in args.rounds:
        seed_results = [
            bit_avalanche(rounds, samples=args.samples, seed=seed, output_bytes=args.output_bytes)
            for seed in args.seeds
        ]
        output_bits = seed_results[0].output_bits
        aggregate_counts = [0] * output_bits

        for result in seed_results:
            for bit_index, (count, rate) in enumerate(zip(result.flip_counts, result.flip_rates)):
                aggregate_counts[bit_index] += count
                bit_rows.append(
                    {
                        "rounds": result.rounds,
                        "seed": result.seed,
                        "samples": result.samples,
                        "output_bit_index": bit_index,
                        "flip_count": count,
                        "flip_rate": f"{rate:.6f}",
                    }
                )

        aggregate_samples = args.samples * len(args.seeds)
        aggregate_rates = [count / aggregate_samples for count in aggregate_counts]
        summary_rows.append(
            {
                "rounds": rounds,
                "seeds": len(args.seeds),
                "samples_per_seed": args.samples,
                "total_samples": aggregate_samples,
                "output_bits": output_bits,
                "mean_flip_rate": f"{sum(aggregate_rates) / output_bits:.6f}",
                "min_flip_rate": f"{min(aggregate_rates):.6f}",
                "min_bit_index": aggregate_rates.index(min(aggregate_rates)),
                "max_flip_rate": f"{max(aggregate_rates):.6f}",
                "max_bit_index": aggregate_rates.index(max(aggregate_rates)),
                "max_abs_delta_from_baseline": f"{max(abs(rate - args.baseline) for rate in aggregate_rates):.6f}",
            }
        )

    bit_fieldnames = ["rounds", "seed", "samples", "output_bit_index", "flip_count", "flip_rate"]
    summary_fieldnames = [
        "rounds",
        "seeds",
        "samples_per_seed",
        "total_samples",
        "output_bits",
        "mean_flip_rate",
        "min_flip_rate",
        "min_bit_index",
        "max_flip_rate",
        "max_bit_index",
        "max_abs_delta_from_baseline",
    ]

    print(",".join(summary_fieldnames))
    for row in summary_rows:
        print(",".join(str(row[field]) for field in summary_fieldnames))

    write_rows_csv(args.bit_output, bit_fieldnames, bit_rows)
    write_rows_csv(args.summary_output, summary_fieldnames, summary_rows)


def run_avalanche_seed_bootstrap(args: argparse.Namespace) -> None:
    ratios_by_round = read_per_sample_ratios(args.samples_input)
    per_sample_metrics = (
        read_metrics_by_round(args.per_sample_metrics) if args.per_sample_metrics is not None else {}
    )
    summary_rows: list[dict[str, object]] = []

    for rounds in args.rounds:
        values_by_seed = ratios_by_round[rounds]
        all_ratios = [ratio for ratios in values_by_seed.values() for ratio in ratios]
        result = summarize_ratios(rounds, all_ratios)
        ci_low, ci_high = hierarchical_bootstrap_mean_ci(
            values_by_seed,
            iterations=args.bootstrap_iterations,
            ci_level=args.ci_level,
            seed=args.bootstrap_seed + rounds,
        )
        per_sample = per_sample_metrics.get(rounds, {})
        per_sample_ci_low = per_sample.get("ci_low", "")
        per_sample_ci_high = per_sample.get("ci_high", "")
        row = {
            "rounds": rounds,
            "seeds": len(values_by_seed),
            "samples_per_seed": min(len(ratios) for ratios in values_by_seed.values()),
            "total_samples": len(all_ratios),
            "baseline": f"{args.baseline:.6f}",
            "mean": f"{result.mean:.6f}",
            "ci_level": f"{args.ci_level:.6f}",
            "ci_method": "hierarchical_seed_percentile_bootstrap",
            "bootstrap_iterations": args.bootstrap_iterations,
            "bootstrap_seed": args.bootstrap_seed + rounds,
            "ci_low": f"{ci_low:.6f}",
            "ci_high": f"{ci_high:.6f}",
            "baseline_delta": f"{result.mean - args.baseline:.6f}",
            "baseline_delta_ci_low": f"{ci_low - args.baseline:.6f}",
            "baseline_delta_ci_high": f"{ci_high - args.baseline:.6f}",
            "ci_contains_baseline": ci_low <= args.baseline <= ci_high,
            "per_sample_ci_low": per_sample_ci_low,
            "per_sample_ci_high": per_sample_ci_high,
            "ci_low_minus_per_sample": (
                f"{ci_low - float(per_sample_ci_low):.6f}" if per_sample_ci_low else ""
            ),
            "ci_high_minus_per_sample": (
                f"{ci_high - float(per_sample_ci_high):.6f}" if per_sample_ci_high else ""
            ),
            "min": f"{result.minimum:.6f}",
            "max": f"{result.maximum:.6f}",
        }
        summary_rows.append(row)

    fieldnames = [
        "rounds",
        "seeds",
        "samples_per_seed",
        "total_samples",
        "baseline",
        "mean",
        "ci_level",
        "ci_method",
        "bootstrap_iterations",
        "bootstrap_seed",
        "ci_low",
        "ci_high",
        "baseline_delta",
        "baseline_delta_ci_low",
        "baseline_delta_ci_high",
        "ci_contains_baseline",
        "per_sample_ci_low",
        "per_sample_ci_high",
        "ci_low_minus_per_sample",
        "ci_high_minus_per_sample",
        "min",
        "max",
    ]
    print(",".join(fieldnames))
    for row in summary_rows:
        print(",".join(str(row[field]) for field in fieldnames))

    write_rows_csv(args.summary_output, fieldnames, summary_rows)


def run_distinguish(args: argparse.Namespace) -> None:
    print(
        "rounds,samples,epochs,random_guess_baseline,majority_baseline,"
        "train_accuracy,test_accuracy,test_accuracy_minus_baseline"
    )
    rows: list[dict[str, object]] = []
    for rounds in args.rounds:
        result = distinguish(rounds, samples=args.samples, epochs=args.epochs, seed=args.seed)
        rows.append(
            {
                "experiment": "distinguish",
                "seed": args.seed,
                "rounds": result.rounds,
                "samples": result.samples,
                "epochs": result.epochs,
                "random_guess_baseline": round(result.random_guess_baseline, 4),
                "majority_baseline": round(result.majority_baseline, 4),
                "train_accuracy": round(result.train_accuracy, 4),
                "test_accuracy": round(result.test_accuracy, 4),
                "test_accuracy_minus_baseline": round(result.test_accuracy_minus_baseline, 4),
            }
        )
        print(
            f"{result.rounds},{result.samples},{result.epochs},"
            f"{result.random_guess_baseline:.4f},{result.majority_baseline:.4f},"
            f"{result.train_accuracy:.4f},{result.test_accuracy:.4f},"
            f"{result.test_accuracy_minus_baseline:.4f}"
        )
    save_results(
        args,
        {
            "experiment": "distinguish",
            "seed": args.seed,
            "rounds": args.rounds,
            "samples": args.samples,
            "epochs": args.epochs,
            "random_guess_baseline": 0.5,
        },
        [
            "experiment",
            "seed",
            "rounds",
            "samples",
            "epochs",
            "random_guess_baseline",
            "majority_baseline",
            "train_accuracy",
            "test_accuracy",
            "test_accuracy_minus_baseline",
        ],
        rows,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reduced-round hash experiments")
    subparsers = parser.add_subparsers(required=True)

    avalanche_parser = subparsers.add_parser("avalanche")
    add_common_rounds(avalanche_parser)
    avalanche_parser.set_defaults(func=run_avalanche)

    avalanche_bootstrap_parser = subparsers.add_parser("avalanche-bootstrap")
    avalanche_bootstrap_parser.add_argument("--rounds", nargs="+", type=int, required=True)
    avalanche_bootstrap_parser.add_argument("--samples", type=int, default=500)
    avalanche_bootstrap_parser.add_argument("--seeds", nargs="+", type=int, required=True)
    avalanche_bootstrap_parser.add_argument("--samples-output", type=Path, required=True)
    avalanche_bootstrap_parser.add_argument("--summary-output", type=Path, required=True)
    avalanche_bootstrap_parser.add_argument("--bootstrap-iterations", type=int, default=2000)
    avalanche_bootstrap_parser.add_argument("--bootstrap-seed", type=int, default=20260510)
    avalanche_bootstrap_parser.add_argument("--ci-level", type=float, default=0.95)
    avalanche_bootstrap_parser.add_argument("--baseline", type=float, default=0.5)
    avalanche_bootstrap_parser.set_defaults(func=run_avalanche_bootstrap)

    avalanche_bits_parser = subparsers.add_parser("avalanche-bits")
    avalanche_bits_parser.add_argument("--rounds", nargs="+", type=int, required=True)
    avalanche_bits_parser.add_argument("--samples", type=int, default=500)
    avalanche_bits_parser.add_argument("--seeds", nargs="+", type=int, required=True)
    avalanche_bits_parser.add_argument("--bit-output", type=Path, required=True)
    avalanche_bits_parser.add_argument("--summary-output", type=Path, required=True)
    avalanche_bits_parser.add_argument("--output-bytes", type=int, default=32)
    avalanche_bits_parser.add_argument("--baseline", type=float, default=0.5)
    avalanche_bits_parser.set_defaults(func=run_avalanche_bits)

    avalanche_seed_bootstrap_parser = subparsers.add_parser("avalanche-seed-bootstrap")
    avalanche_seed_bootstrap_parser.add_argument("--rounds", nargs="+", type=int, required=True)
    avalanche_seed_bootstrap_parser.add_argument("--samples-input", type=Path, required=True)
    avalanche_seed_bootstrap_parser.add_argument("--summary-output", type=Path, required=True)
    avalanche_seed_bootstrap_parser.add_argument("--per-sample-metrics", type=Path)
    avalanche_seed_bootstrap_parser.add_argument("--bootstrap-iterations", type=int, default=2000)
    avalanche_seed_bootstrap_parser.add_argument("--bootstrap-seed", type=int, default=20260510)
    avalanche_seed_bootstrap_parser.add_argument("--ci-level", type=float, default=0.95)
    avalanche_seed_bootstrap_parser.add_argument("--baseline", type=float, default=0.5)
    avalanche_seed_bootstrap_parser.set_defaults(func=run_avalanche_seed_bootstrap)

    distinguish_parser = subparsers.add_parser("distinguish")
    add_common_rounds(distinguish_parser)
    distinguish_parser.add_argument("--epochs", type=int, default=10)
    distinguish_parser.set_defaults(func=run_distinguish)

    return parser
