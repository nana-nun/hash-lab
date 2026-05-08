import unittest

from src.hash_lab.experiments import flip_one_bit, hamming_distance
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


if __name__ == "__main__":
    unittest.main()
