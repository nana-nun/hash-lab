"""Command line entrypoint for hash-lab."""

from __future__ import annotations

from .experiments import build_parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
