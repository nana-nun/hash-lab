"""Experiment runners for hash-lab."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

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
class DistinguishResult:
    rounds: int
    samples: int
    epochs: int
    train_accuracy: float
    test_accuracy: float


def hamming_distance(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        raise ValueError("inputs must have equal length")
    return sum((a ^ b).bit_count() for a, b in zip(left, right))


def flip_one_bit(data: bytes, bit_index: int) -> bytes:
    values = bytearray(data)
    byte_index, shift = divmod(bit_index, 8)
    values[byte_index] ^= 1 << (7 - shift)
    return bytes(values)


def avalanche(rounds: int, samples: int, input_bytes: int = 32, seed: int = 1) -> AvalancheResult:
    rng = random.Random(seed)
    ratios: list[float] = []

    for _ in range(samples):
        data = rng.randbytes(input_bytes)
        bit_index = rng.randrange(input_bytes * 8)
        changed = flip_one_bit(data, bit_index)
        left = digest(data, rounds=rounds)
        right = digest(changed, rounds=rounds)
        ratios.append(hamming_distance(left, right) / (len(left) * 8))

    mean = sum(ratios) / len(ratios)
    variance = sum((item - mean) ** 2 for item in ratios) / len(ratios)
    return AvalancheResult(
        rounds=rounds,
        samples=samples,
        mean=mean,
        stdev=math.sqrt(variance),
        minimum=min(ratios),
        maximum=max(ratios),
    )


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


def distinguish(rounds: int, samples: int, epochs: int, seed: int = 1) -> DistinguishResult:
    rows = make_distinguish_dataset(rounds, samples=samples, seed=seed)
    split = int(len(rows) * 0.8)
    train_rows = rows[:split]
    test_rows = rows[split:]
    weights, bias = train_logistic(train_rows, epochs=epochs)
    return DistinguishResult(
        rounds=rounds,
        samples=samples,
        epochs=epochs,
        train_accuracy=accuracy(train_rows, weights, bias),
        test_accuracy=accuracy(test_rows, weights, bias),
    )


def add_common_rounds(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--rounds", nargs="+", type=int, required=True)
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--seed", type=int, default=1)


def run_avalanche(args: argparse.Namespace) -> None:
    print("rounds,samples,mean,stdev,min,max")
    for rounds in args.rounds:
        result = avalanche(rounds, samples=args.samples, seed=args.seed)
        print(
            f"{result.rounds},{result.samples},"
            f"{result.mean:.4f},{result.stdev:.4f},{result.minimum:.4f},{result.maximum:.4f}"
        )


def run_distinguish(args: argparse.Namespace) -> None:
    print("rounds,samples,epochs,train_accuracy,test_accuracy")
    for rounds in args.rounds:
        result = distinguish(rounds, samples=args.samples, epochs=args.epochs, seed=args.seed)
        print(
            f"{result.rounds},{result.samples},{result.epochs},"
            f"{result.train_accuracy:.4f},{result.test_accuracy:.4f}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reduced-round hash experiments")
    subparsers = parser.add_subparsers(required=True)

    avalanche_parser = subparsers.add_parser("avalanche")
    add_common_rounds(avalanche_parser)
    avalanche_parser.set_defaults(func=run_avalanche)

    distinguish_parser = subparsers.add_parser("distinguish")
    add_common_rounds(distinguish_parser)
    distinguish_parser.add_argument("--epochs", type=int, default=10)
    distinguish_parser.set_defaults(func=run_distinguish)

    return parser
