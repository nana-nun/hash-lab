"""A small SHA256-inspired toy hash for reduced-round experiments.

This is not SHA256 and must not be used for security. It is intentionally
small enough to make reduced-round behavior easy to inspect.
"""

from __future__ import annotations

import struct

MASK32 = 0xFFFFFFFF

INITIAL_STATE = (
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
)

ROUND_CONSTANTS = (
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
)


def rotate_right(value: int, shift: int) -> int:
    shift %= 32
    return ((value >> shift) | (value << (32 - shift))) & MASK32


def choice(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)


def majority(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def big_sigma0(x: int) -> int:
    return rotate_right(x, 2) ^ rotate_right(x, 13) ^ rotate_right(x, 22)


def big_sigma1(x: int) -> int:
    return rotate_right(x, 6) ^ rotate_right(x, 11) ^ rotate_right(x, 25)


def small_sigma0(x: int) -> int:
    return rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3)


def small_sigma1(x: int) -> int:
    return rotate_right(x, 17) ^ rotate_right(x, 19) ^ (x >> 10)


def pad_block(data: bytes) -> bytes:
    """Pad data into one 64-byte block for toy experiments."""
    if len(data) > 55:
        raise ValueError("mini_sha accepts at most 55 bytes")

    bit_length = len(data) * 8
    padded = data + b"\x80"
    padded += b"\x00" * (56 - len(padded))
    padded += struct.pack(">Q", bit_length)
    return padded


def message_schedule(block: bytes, rounds: int) -> list[int]:
    if len(block) != 64:
        raise ValueError("block must be exactly 64 bytes")
    if rounds < 1:
        raise ValueError("rounds must be positive")

    words = list(struct.unpack(">16I", block))
    for i in range(16, rounds):
        word = (
            small_sigma1(words[i - 2])
            + words[i - 7]
            + small_sigma0(words[i - 15])
            + words[i - 16]
        ) & MASK32
        words.append(word)
    return words[:rounds]


def digest(data: bytes, rounds: int = 16, output_bytes: int = 32) -> bytes:
    """Hash a short byte string with a configurable number of rounds."""
    if output_bytes < 1 or output_bytes > 32:
        raise ValueError("output_bytes must be between 1 and 32")

    block = pad_block(data)
    schedule = message_schedule(block, rounds)
    a, b, c, d, e, f, g, h = INITIAL_STATE

    for i, word in enumerate(schedule):
        k = ROUND_CONSTANTS[i % len(ROUND_CONSTANTS)]
        t1 = (h + big_sigma1(e) + choice(e, f, g) + k + word) & MASK32
        t2 = (big_sigma0(a) + majority(a, b, c)) & MASK32
        h = g
        g = f
        f = e
        e = (d + t1) & MASK32
        d = c
        c = b
        b = a
        a = (t1 + t2) & MASK32

    state = (
        (INITIAL_STATE[0] + a) & MASK32,
        (INITIAL_STATE[1] + b) & MASK32,
        (INITIAL_STATE[2] + c) & MASK32,
        (INITIAL_STATE[3] + d) & MASK32,
        (INITIAL_STATE[4] + e) & MASK32,
        (INITIAL_STATE[5] + f) & MASK32,
        (INITIAL_STATE[6] + g) & MASK32,
        (INITIAL_STATE[7] + h) & MASK32,
    )
    return struct.pack(">8I", *state)[:output_bytes]


def digest_bits(data: bytes, rounds: int = 16, output_bytes: int = 32) -> list[int]:
    out = digest(data, rounds=rounds, output_bytes=output_bytes)
    return [(byte >> shift) & 1 for byte in out for shift in range(7, -1, -1)]
