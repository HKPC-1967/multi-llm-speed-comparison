# LLM Response Time Evaluation

This Python project benchmarks response time, output tokens, and output token throughput for multiple LLM models across providers. It writes an Excel file where each row is a model and each task contributes three columns: response time, output tokens, and token/second.

## Supported Models

The initial configuration includes:

- Azure OpenAI GPT-4.1
- Azure AI Foundry GPT-5.4 Mini through the OpenAI Responses API
- Azure AI Foundry DeepSeek-V4-Flash
- Alibaba Cloud DeepSeek-V4-Flash through DashScope's OpenAI-compatible API

## Setup

Install dependencies with `uv`:

```powershell
uv sync
```

Create your local environment file:

```powershell
Copy-Item .env.copy .env
```

Then edit `.env` and replace every placeholder value with your real endpoint, key, API version, deployment name, or model name.

## Run

Run the benchmark and write an Excel file under `outputs/`:

```powershell
uv run llm-response-time-evaluation
```

Use a custom Excel output path:

```powershell
uv run llm-response-time-evaluation --output outputs/my_result.xlsx
```

The module entry point also works:

```powershell
uv run python -m llm_response_time_evaluation
```

## Configure Benchmark Inputs

Edit `src/llm_response_time_evaluation/config.py`.

The main values are near the top of the file:

- `RUNS_PER_MODEL`: how many calls to make for each model/task pair before averaging.
- `BENCHMARK_TASKS`: named prompt tasks, such as `0.01k`, `1k`, or `2k`.
- `MODEL_CONFIGS`: the models to benchmark and the environment variables they use.

Example task addition:

```python
BENCHMARK_TASKS = [
    BenchmarkTask(name="0.01k", prompt="0123456789"),
    BenchmarkTask(name="1k", prompt="paste roughly 1k tokens here"),
    BenchmarkTask(name="2k", prompt="paste roughly 2k tokens here"),
]
```

## Output Format

The Excel workbook has a `Summary` sheet and a `Details` sheet.

The `Summary` sheet has the model name in the first column. Each benchmark task adds three columns:

- `<task name> - response time`
- `<task name> - output tokens`
- `<task name> - token/second`

For example, tasks named `1k` and `2k` produce columns like `1k - response time`, `1k - output tokens`, `1k - token/second`, `2k - response time`, `2k - output tokens`, and `2k - token/second`.

The `Details` sheet records each individual call with model name, task name, run number, response time, output token count, token/second, full answer text, and error message if the call failed.

## Extending Providers

The provider design is split into configuration and request clients:

- Add a model row in `MODEL_CONFIGS` when the new model uses an existing request style.
- Add a new client class in `src/llm_response_time_evaluation/clients.py` when the platform has a different URL shape, authentication method, request body, or response body.
- Register the new provider string in `build_client()`.
- Add matching placeholder variables to `.env.copy`.
- Update this README and `AGENTS.md` whenever the architecture or startup steps change.

This keeps provider-specific request code isolated while the benchmark runner and Excel writer stay unchanged.

Current provider strings:

- `azure_openai`: Azure OpenAI chat completions deployment URL.
- `azure_foundry`: Azure AI Foundry chat completions URL.
- `azure_foundry_openai`: Azure AI Foundry OpenAI Responses API URL, currently used by GPT-5.4 Mini.
- `openai_compatible`: OpenAI-compatible chat completions URL, currently used by Alibaba Cloud DashScope.
