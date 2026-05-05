"""Command line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from multi_llm_speed_comparison.runner import default_output_path, run_benchmark


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark LLM response time and token throughput.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path(),
        help="Excel output path. Defaults to outputs/llm_benchmark_<timestamp>.xlsx.",
    )
    args = parser.parse_args()

    output_path = run_benchmark(args.output)
    print(f"Benchmark complete. Excel written to: {output_path}")


if __name__ == "__main__":
    main()
