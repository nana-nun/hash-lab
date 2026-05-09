import csv
import json
import unittest
from argparse import Namespace
from pathlib import Path

from src.hash_lab.experiments import (
    distinguish,
    flip_one_bit,
    hamming_distance,
    majority_baseline_accuracy,
    save_results,
)
from src.hash_lab.mini_sha import digest, digest_bits, pad_block


class MiniShaTests(unittest.TestCase):
    def test_digest_is_deterministic(self):
        left = digest(b"hash-lab", rounds=8)
        right = digest(b"hash-lab", rounds=8)
        self.assertEqual(left, right)

    def test_rounds_change_digest(self):
        self.assertNotEqual(digest(b"hash-lab", rounds=4), digest(b"hash-lab", rounds=12))

    def test_digest_bits_matches_output_size(self):
        self.assertEqual(len(digest_bits(b"abc", rounds=8, output_bytes=4)), 32)

    def test_pad_block_size(self):
        self.assertEqual(len(pad_block(b"abc")), 64)

    def test_flip_one_bit(self):
        self.assertEqual(flip_one_bit(b"\x00", 0), b"\x80")
        self.assertEqual(flip_one_bit(b"\x00", 7), b"\x01")

    def test_hamming_distance(self):
        self.assertEqual(hamming_distance(b"\x00", b"\xff"), 8)

    def test_majority_baseline_accuracy(self):
        rows = [([0], 1), ([1], 1), ([0], 0), ([1], 1)]

        self.assertEqual(majority_baseline_accuracy(rows), 0.75)

    def test_distinguish_reports_random_guess_baseline_delta(self):
        result = distinguish(rounds=2, samples=20, epochs=1, seed=1)

        self.assertEqual(result.random_guess_baseline, 0.5)
        self.assertAlmostEqual(
            result.test_accuracy_minus_baseline,
            result.test_accuracy - result.random_guess_baseline,
        )

    def test_save_results_csv(self):
        output = Path("results/test-save-results.csv")
        try:
            output.unlink(missing_ok=True)
            args = Namespace(output=output, format="csv")
            save_results(
                args,
                {"experiment": "avalanche", "seed": 1},
                ["experiment", "seed", "rounds", "samples", "mean"],
                [
                    {
                        "experiment": "avalanche",
                        "seed": 1,
                        "rounds": 4,
                        "samples": 10,
                        "mean": 0.125,
                    }
                ],
            )

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rows[0]["experiment"], "avalanche")
            self.assertEqual(rows[0]["seed"], "1")
            self.assertEqual(rows[0]["rounds"], "4")
        finally:
            output.unlink(missing_ok=True)

    def test_save_results_json(self):
        output = Path("results/test-save-results.json")
        try:
            output.unlink(missing_ok=True)
            args = Namespace(output=output, format="json")
            save_results(
                args,
                {"experiment": "distinguish", "seed": 3, "epochs": 2},
                ["experiment", "seed", "rounds"],
                [{"experiment": "distinguish", "seed": 3, "rounds": 8}],
            )

            payload = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(payload["metadata"]["experiment"], "distinguish")
            self.assertEqual(payload["metadata"]["seed"], 3)
            self.assertEqual(payload["results"][0]["rounds"], 8)
        finally:
            output.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
