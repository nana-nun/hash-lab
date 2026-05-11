import csv
import json
import unittest
from argparse import Namespace
from pathlib import Path

from src.hash_lab.experiments import (
    avalanche,
    avalanche_ratios,
    bit_avalanche,
    bootstrap_mean_ci,
    baseline_normal_p_value,
    distinguish,
    flip_one_bit,
    hamming_distance,
    hierarchical_bootstrap_mean_ci,
    holm_adjusted_p_values,
    low_order_stats,
    majority_baseline_accuracy,
    percentile,
    read_bit_metrics,
    read_bit_metrics_by_seed,
    read_metrics_by_round_and_bit,
    read_per_sample_ratios,
    run_low_order_stats,
    save_results,
    wilson_score_ci,
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

    def test_avalanche_ratios_are_reproducible(self):
        left = avalanche_ratios(rounds=4, samples=5, seed=7)
        right = avalanche_ratios(rounds=4, samples=5, seed=7)

        self.assertEqual(left, right)
        self.assertEqual(len(left), 5)
        self.assertTrue(all(0 <= ratio <= 1 for ratio in left))

    def test_bit_avalanche_mean_matches_avalanche_mean(self):
        aggregate = avalanche(rounds=4, samples=10, seed=2)
        per_bit = bit_avalanche(rounds=4, samples=10, seed=2)

        self.assertEqual(len(per_bit.flip_counts), 256)
        self.assertAlmostEqual(per_bit.mean_flip_rate, aggregate.mean)

    def test_percentile_interpolates(self):
        self.assertEqual(percentile([0.0, 10.0], 0.5), 5.0)

    def test_bootstrap_mean_ci_is_reproducible(self):
        left = bootstrap_mean_ci([0.0, 0.5, 1.0], iterations=20, seed=3)
        right = bootstrap_mean_ci([0.0, 0.5, 1.0], iterations=20, seed=3)

        self.assertEqual(left, right)
        self.assertLessEqual(left[0], left[1])

    def test_hierarchical_bootstrap_mean_ci_is_reproducible(self):
        values_by_seed = {1: [0.0, 0.25], 2: [0.75, 1.0]}
        left = hierarchical_bootstrap_mean_ci(values_by_seed, iterations=20, seed=5)
        right = hierarchical_bootstrap_mean_ci(values_by_seed, iterations=20, seed=5)

        self.assertEqual(left, right)
        self.assertLessEqual(left[0], left[1])

    def test_read_per_sample_ratios_groups_by_round_and_seed(self):
        output = Path("results/test-per-sample-ratios.csv")
        try:
            output.write_text(
                "experiment,rounds,seed,sample_index,flip_ratio\n"
                "avalanche_bootstrap,4,1,0,0.12500000\n"
                "avalanche_bootstrap,4,2,0,0.25000000\n",
                encoding="utf-8",
            )

            grouped = read_per_sample_ratios(output)

            self.assertEqual(grouped[4][1], [0.125])
            self.assertEqual(grouped[4][2], [0.25])
        finally:
            output.unlink(missing_ok=True)

    def test_read_bit_metrics_aggregates_seeds(self):
        output = Path("results/test-bit-metrics.csv")
        try:
            output.write_text(
                "rounds,seed,samples,output_bit_index,flip_count,flip_rate\n"
                "4,1,10,0,6,0.600000\n"
                "4,2,10,0,4,0.400000\n"
                "4,1,10,1,7,0.700000\n",
                encoding="utf-8",
            )

            grouped = read_bit_metrics(output)

            self.assertEqual(grouped[4][0], {"flips": 10, "samples": 20})
            self.assertEqual(grouped[4][1], {"flips": 7, "samples": 10})
        finally:
            output.unlink(missing_ok=True)

    def test_read_bit_metrics_by_seed_preserves_seed_buckets(self):
        output = Path("results/test-bit-metrics-by-seed.csv")
        try:
            output.write_text(
                "rounds,seed,samples,output_bit_index,flip_count,flip_rate\n"
                "13,1,10,255,4,0.400000\n"
                "13,2,10,255,6,0.600000\n"
                "13,1,10,254,5,0.500000\n",
                encoding="utf-8",
            )

            grouped = read_bit_metrics_by_seed(output)

            self.assertEqual(grouped[13][255][1], {"flips": 4, "samples": 10})
            self.assertEqual(grouped[13][255][2], {"flips": 6, "samples": 10})
            self.assertEqual(grouped[13][254][1], {"flips": 5, "samples": 10})
        finally:
            output.unlink(missing_ok=True)

    def test_read_metrics_by_round_and_bit_keys_by_both_columns(self):
        output = Path("results/test-round-bit-metrics.csv")
        try:
            output.write_text(
                "rounds,output_bit_index,ci_low,ci_high\n"
                "13,254,0.490000,0.510000\n"
                "13,255,0.480000,0.490000\n",
                encoding="utf-8",
            )

            grouped = read_metrics_by_round_and_bit(output)

            self.assertEqual(grouped[(13, 255)]["ci_low"], "0.480000")
            self.assertEqual(grouped[(13, 254)]["ci_high"], "0.510000")
        finally:
            output.unlink(missing_ok=True)

    def test_wilson_score_ci_bounds_rate(self):
        low, high = wilson_score_ci(50, 100)

        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.5)

    def test_baseline_normal_p_value_is_larger_near_baseline(self):
        near = baseline_normal_p_value(50, 100)
        far = baseline_normal_p_value(80, 100)

        self.assertGreater(near, far)

    def test_holm_adjusted_p_values_are_monotone_by_rank(self):
        adjusted = holm_adjusted_p_values([0.03, 0.001, 0.02])

        self.assertEqual(len(adjusted), 3)
        self.assertGreaterEqual(adjusted[2], adjusted[1])

    def test_low_order_stats_reports_hash_and_random_sources(self):
        results = low_order_stats(rounds=4, samples=3, seed=11, output_bytes=2, block_size=2)

        self.assertEqual({result.source for result in results}, {"mini_sha", "random"})
        for result in results:
            self.assertEqual(result.samples, 3)
            self.assertEqual(result.output_bits, 16)
            self.assertEqual(result.bit_count, 48)
            self.assertEqual(len(result.block_counts), 4)
            self.assertEqual(result.total_blocks, 24)
            self.assertTrue(0 <= result.ones_rate <= 1)
            self.assertEqual(len(result.runs), 3)
            self.assertEqual(len(result.longest_runs), 3)

    def test_run_low_order_stats_writes_summary_and_block_csvs(self):
        summary_output = Path("results/test-low-order-summary.csv")
        block_output = Path("results/test-low-order-blocks.csv")
        try:
            summary_output.unlink(missing_ok=True)
            block_output.unlink(missing_ok=True)
            args = Namespace(
                rounds=[4],
                samples=2,
                seeds=[1],
                summary_output=summary_output,
                block_output=block_output,
                input_bytes=32,
                output_bytes=2,
                block_size=4,
            )

            run_low_order_stats(args)

            with summary_output.open(newline="", encoding="utf-8") as handle:
                summary_rows = list(csv.DictReader(handle))
            with block_output.open(newline="", encoding="utf-8") as handle:
                block_rows = list(csv.DictReader(handle))

            self.assertEqual(len(summary_rows), 2)
            self.assertEqual({row["source"] for row in summary_rows}, {"mini_sha", "random"})
            self.assertEqual(summary_rows[0]["rounds"], "4")
            self.assertEqual(summary_rows[0]["seed"], "1")
            self.assertEqual(summary_rows[0]["samples"], "2")
            self.assertEqual(len(block_rows), 32)
            self.assertIn("block_rate_minus_uniform", block_rows[0])
        finally:
            summary_output.unlink(missing_ok=True)
            block_output.unlink(missing_ok=True)

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
