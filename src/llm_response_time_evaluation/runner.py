"""Benchmark runner and Excel export."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import tiktoken
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font

from llm_response_time_evaluation.clients import build_client
from llm_response_time_evaluation.config import (
    BENCHMARK_TASKS,
    MODEL_CONFIGS,
    RUNS_PER_MODEL,
    BenchmarkTask,
    ModelConfig,
)


@dataclass(frozen=True)
class TaskAverage:
    response_time_seconds: float | None
    tokens_per_second: float | None
    error: str | None = None


def run_benchmark(output_path: Path) -> Path:
    load_dotenv()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict[str, TaskAverage]] = {}
    for model_config in MODEL_CONFIGS:
        results[model_config.display_name] = {}
        for task in BENCHMARK_TASKS:
            results[model_config.display_name][task.name] = _run_task_average(
                model_config=model_config,
                task=task,
                runs=RUNS_PER_MODEL,
            )

    _write_excel(output_path=output_path, results=results)
    return output_path


def default_output_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path("outputs") / f"llm_benchmark_{timestamp}.xlsx"


def _run_task_average(
    model_config: ModelConfig,
    task: BenchmarkTask,
    runs: int,
) -> TaskAverage:
    try:
        client = build_client(model_config)
    except Exception as exc:  # noqa: BLE001
        return TaskAverage(None, None, str(exc))

    latencies: list[float] = []
    throughputs: list[float] = []

    for _ in range(runs):
        try:
            started_at = time.perf_counter()
            response = client.complete(task.prompt)
            latency = time.perf_counter() - started_at
            output_tokens = response.output_tokens or _estimate_tokens(response.text)
            token_per_second = output_tokens / latency if latency > 0 else 0
        except Exception as exc:  # noqa: BLE001
            return TaskAverage(None, None, str(exc))

        latencies.append(latency)
        throughputs.append(token_per_second)

    return TaskAverage(
        response_time_seconds=statistics.fmean(latencies),
        tokens_per_second=statistics.fmean(throughputs),
    )


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:  # noqa: BLE001
        return max(1, len(text) // 4)


def _write_excel(
    output_path: Path,
    results: dict[str, dict[str, TaskAverage]],
) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Summary"

    header = ["Model"]
    for task in BENCHMARK_TASKS:
        header.extend(
            [
                f"{task.name}-response time",
                f"{task.name}-token/second",
            ]
        )
    header.append("error")
    sheet.append(header)

    for cell in sheet[1]:
        cell.font = Font(bold=True)

    for model_name, task_results in results.items():
        row: list[object] = [model_name]
        errors: list[str] = []
        for task in BENCHMARK_TASKS:
            average = task_results[task.name]
            row.append(_round_or_blank(average.response_time_seconds))
            row.append(_round_or_blank(average.tokens_per_second))
            if average.error:
                errors.append(f"{task.name}: {average.error}")
        row.append("; ".join(errors))
        sheet.append(row)

    for column_cells in sheet.columns:
        max_length = max(len(str(cell.value or "")) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = min(
            max(max_length + 2, 12),
            80,
        )

    workbook.save(output_path)


def _round_or_blank(value: float | None) -> float | str:
    if value is None:
        return ""
    return round(value, 4)
