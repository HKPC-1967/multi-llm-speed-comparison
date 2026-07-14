# Agent Guide

Use this guide to understand and modify the project safely.

## Project Purpose

This project benchmarks LLM response latency and output token throughput across several cloud providers. It exports one Excel workbook with summary, per-call details, and task configuration sheets.

## Main Files

- `src/multi_llm_speed_comparison/config.py`: user-editable benchmark settings. Keep `RUNS_PER_MODEL`, `TEMPERATURE`, `BENCHMARK_TASKS`, and `MODEL_CONFIGS` easy to find near the top.
- `src/multi_llm_speed_comparison/clients.py`: provider-specific request code. Add a new client here if a platform needs a different URL, auth header, request body, or response parser.
- `src/multi_llm_speed_comparison/runner.py`: benchmark loop, averaging, token fallback estimation, and Excel export.
- `src/multi_llm_speed_comparison/cli.py`: command line entry point.
- `.env.copy`: commit-safe environment template. Never put real secrets in this file.
- `.env`: local secret file ignored by git.
- `README.md`: user-facing setup, run, and extension instructions.

## Provider Clients

- `AzureOpenAIClient`: Azure OpenAI chat completions deployment URL.
- `AzureFoundryClient`: Azure AI Foundry chat completions URL.
- `AzureFoundryOpenAIClient`: Azure AI Foundry OpenAI Responses API URL, currently used by GPT-5.4 Mini.
- `OpenAICompatibleClient`: OpenAI-compatible chat completions URL, currently used by Alibaba Cloud DashScope.
- `OpenAICompatibleResponsesClient`: OpenAI-compatible Responses API URL via the OpenAI SDK.

## Architecture Rules

- Keep dependencies pinned with `==` in `pyproject.toml`.
- Do not commit `.env`, `.venv`, or generated `outputs/` files.
- Keep all documentation, code comments, and user-facing strings in English.
- If adding a new provider that uses an existing request style, add only a `ModelConfig`.
- If adding a provider with different request behavior, create a new client class and register it in `build_client()`.
- Preserve the `Summary` sheet shape: model names as rows and task metric groups as columns. Use a two-row header where each task name is a merged cell above response time, output tokens, and token/second.
- Preserve the `Details` sheet purpose: each model/task/run should include the full answer text and output token count.
- Preserve the `Tasks` sheet purpose: each benchmark task should include the configured name, prompt, and temperature.
- When architecture, run commands, environment variables, or project structure change, update both `README.md` and this `AGENTS.md`.

## Common Commands

```powershell
uv sync
uv run multi-llm-speed-comparison
uv run multi-llm-speed-comparison --output outputs/my_result.xlsx
uv run ruff check .
uv run python -m compileall src
```

## Extension Checklist

1. Add or update environment variables in `.env.copy`.
2. Add the model in `MODEL_CONFIGS`.
3. Add or update a client in `clients.py` if the provider request shape is new.
4. Run lint and import checks.
5. Update `README.md` and `AGENTS.md` if behavior, commands, or structure changed.
